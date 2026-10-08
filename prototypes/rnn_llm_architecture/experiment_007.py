"""Experiment 007: native continuation versus query-aware frozen/joint memory readout.

Both A and B are queried independently from a single query-free recurrent prefix.
The frozen controls do not update the underlying recurrence. CPU only; bounded.
This does NOT test formal robust learning-credit dimension D.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import torch
from torch import nn
import torch.nn.functional as F

from .experiment_005 import make_variant, paired_query_loss
from .experiment_006 import flatten_recurrent_state, train_model
from .experiment_002 import _slot_targets, paired_selective_eval
from .learning_pilot import make_batch

VARIANTS = ("protected_w32", "gru_w32", "lstm_w32")
HEADS = ("frozen_top", "frozen_all", "joint_all")


@dataclass(frozen=True)
class Config:
    variants: tuple[str, ...] = VARIANTS
    seeds: tuple[int, ...] = (17, 29, 43)
    delays: tuple[int, ...] = (16, 64)
    pretrain_steps: int = 200
    additional_steps: int = 150
    batch_size: int = 16
    head_examples: int = 1024
    head_batch: int = 64
    eval_examples: int = 512
    lr: float = .002
    head_lr: float = .01
    max_wall_seconds: float = 540.0

    def __post_init__(self):
        if not self.variants or len(set(self.variants)) != len(self.variants) or any(v not in VARIANTS for v in self.variants):
            raise ValueError("invalid model variants")
        if not self.seeds or any(type(s) is not int or s < 0 for s in self.seeds):
            raise ValueError("invalid seeds")
        if not self.delays or any(type(d) is not int or d < 2 for d in self.delays):
            raise ValueError("invalid delays")
        if any(type(n) is not int or n < 1 for n in (self.pretrain_steps, self.additional_steps,
                     self.batch_size, self.head_examples, self.head_batch, self.eval_examples)):
            raise ValueError("counts and steps must be positive")
        if any(not math.isfinite(v) or v <= 0 for v in (self.lr,self.head_lr,self.max_wall_seconds)):
            raise ValueError("nonpositive or nonfinite resource setting")


def state_features(state, kind):
    """State exists before seeing the query; LSTM all-state includes cell memories."""
    if kind == "all":
        return torch.cat([item for layer in state for item in ((layer.hidden,layer.cell) if hasattr(layer,"hidden") else (layer,))],dim=1)
    if kind == "top":
        last = state[-1]
        return last.hidden if hasattr(last,"hidden") else last
    raise ValueError("invalid feature kind")


def paired_prefix(delay, batch, *, seed):
    ids, _, _ = make_batch("selective",delay,batch,seed=seed)
    prefix=ids[:,:-1]
    labels=_slot_targets(prefix,delay)
    return prefix,labels


class AddressedReadout(nn.Module):
    """Query-conditioned two-class MLP, identical architecture for all variants."""
    def __init__(self, features: int):
        super().__init__()
        if features < 1:
            raise ValueError("feature width must be positive")
        self.query_embedding=nn.Embedding(2,8)
        self.net=nn.Sequential(nn.Linear(features+8,64),nn.Tanh(),nn.Linear(64,2))

    def forward(self, state):
        if state.ndim != 2:
            raise ValueError("input must be [batch,features]")
        b=len(state)
        queries=torch.arange(2,device=state.device)
        query=self.query_embedding(queries).unsqueeze(0).expand(b,-1,-1)
        state=state[:,None,:].expand(-1,2,-1)
        return self.net(torch.cat((state,query),dim=-1))


def score(logits,labels,*,update_slot=None):
    if logits.shape!=(len(labels),2,2) or labels.shape!=(len(logits),2):
        raise ValueError("incorrect pair shapes")
    hits=logits.argmax(-1).eq(labels)
    both=hits.all(-1)
    unequal=labels[:,0]!=labels[:,1]
    result={"paired_both_accuracy":float(both.float().mean()),
        "paired_on_unequal":float(both[unequal].float().mean()) if bool(unequal.any()) else None,
        "paired_on_equal":float(both[~unequal].float().mean()) if bool((~unequal).any()) else None,
        "per_slot_accuracy":[float(t) for t in hits.float().mean(0)],
        "unequal_fraction":float(unequal.float().mean()),"examples":len(labels),
        "cross_entropy":float(F.cross_entropy(logits.reshape(-1,2),labels.reshape(-1)))}
    return result


def paired_loss(logits,labels):
    return F.cross_entropy(logits.reshape(-1,2),labels.reshape(-1))


def weight_digest(module):
    h=hashlib.sha256()
    for name,value in sorted(module.state_dict().items()):
        h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


@torch.no_grad()
def cached_features(model,delay,count,*,seed,kind,chunk=128):
    model.eval()
    ids,truth=paired_prefix(delay,count,seed=seed)
    out=[]
    for first in range(0,count,chunk):
        _,state=model(ids[first:first+chunk])
        out.append(state_features(state,kind).cpu())
    return torch.cat(out),truth


@torch.no_grad()
def eval_readout(model,head,delay,count,*,seed,kind):
    x,y=cached_features(model,delay,count,seed=seed,kind=kind)
    head.eval()
    return score(head(x),y)


def fit_frozen(model,*,delay,seed,kind,config,began):
    """Train addressed decoder on a separate fixed, labelled prefix dataset."""
    original_digest=weight_digest(model)
    features,labels=cached_features(model,delay,config.head_examples,
                    seed=8_000_003+seed*301+delay*41,kind=kind)
    # Standardize from training features only; recorded transform reused at evaluation.
    mean=features.mean(0,keepdim=True)
    sd=features.std(0,keepdim=True,unbiased=False).clamp_min(1.e-4)
    features=(features-mean)/sd
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed+5000+(1 if kind=='all' else 0))
        head=AddressedReadout(features.shape[1])
    opt=torch.optim.AdamW(head.parameters(),lr=config.head_lr)
    rng=torch.Generator().manual_seed(seed*7001+1)
    completed=0
    for i in range(config.additional_steps):
        if time.monotonic()-began>=config.max_wall_seconds:
            break
        chosen=torch.randint(0,len(features),(config.head_batch,),generator=rng)
        logits=head(features[chosen])
        loss=paired_loss(logits,labels[chosen]);guard_finite(loss,head)
        opt.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_(head.parameters(),1.)
        opt.step();completed+=1
    if weight_digest(model)!=original_digest:
        raise AssertionError("frozen readout mutated the recurrent trunk")
    return head,(mean,sd),completed


def guard_finite(loss,module):
    if not bool(torch.isfinite(loss)):
        raise FloatingPointError("nonfinite training loss")
    if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in module.parameters()):
        raise FloatingPointError("nonfinite training gradient")


def eval_frozen(model,head,normalizer,delay,count,*,seed,kind):
    x,y=cached_features(model,delay,count,seed=seed,kind=kind)
    mean,sd=normalizer
    head.eval()
    with torch.no_grad():
        return score(head((x-mean)/sd),y)


def train_joint(model,head,*,delay,seed,config,began):
    optimizer=torch.optim.AdamW([{"params":model.parameters(),"lr":config.lr},
                        {"params":head.parameters(),"lr":config.head_lr}],weight_decay=.01)
    done=0
    for step in range(config.additional_steps):
        if time.monotonic()-began>=config.max_wall_seconds:break
        ids,y=paired_prefix(delay,config.batch_size,seed=seed*1_000_003+(config.pretrain_steps+step)*8191+delay*17+97)
        model.train();head.train()
        _,state=model(ids)
        features=state_features(state,"all")
        logits=head(features)
        loss=paired_loss(logits,y)
        optimizer.zero_grad(set_to_none=True);loss.backward()
        guard_finite(loss,model);guard_finite(loss,head)
        torch.nn.utils.clip_grad_norm_(list(model.parameters())+list(head.parameters()),1.)
        optimizer.step();done+=1
    return done


def train_native_continue(model,*,delay,seed,config,began):
    opt=torch.optim.AdamW(model.parameters(),lr=config.lr)
    done=0
    for step in range(config.additional_steps):
        if time.monotonic()-began>=config.max_wall_seconds:break
        batchseed=seed*1_000_003+(config.pretrain_steps+step)*8191+delay*17+97
        model.train();opt.zero_grad(set_to_none=True)
        loss=paired_query_loss(model,delay,config.batch_size,seed=batchseed)
        guard_finite(loss,model)
        loss.backward();guard_finite(loss,model)
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        opt.step();done+=1
    return done


def execute(config:Config,*,output:Path):
    if output.exists():raise FileExistsError("output exists; refusing to overwrite evidence")
    torch.set_num_threads(1);torch.manual_seed(0);torch.use_deterministic_algorithms(True)
    began=time.monotonic()
    result={"status":"running","config":asdict(config),
        "environment":{"torch":torch.__version__,"python":platform.python_version(),"device":"cpu"},
        "scope":"bounded query-aware two-slot retrieval; not formal D", "runs":[],"skipped":[]}
    jobs=[(delay,seed,variant) for delay in config.delays for seed in config.seeds for variant in config.variants]
    try:
        for i,(delay,seed,variant) in enumerate(jobs):
            if time.monotonic()-began>=config.max_wall_seconds:
                result["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i:]);break
            # Original recurrence and original query head are trained together for 200 updates.
            class TrainingSettings:
                train_steps=config.pretrain_steps
                train_batch=config.batch_size
                lr=config.lr
                max_wall_seconds=config.max_wall_seconds
            base,trained,_=train_model(variant,seed,delay,TrainingSettings,began=began)
            row={"variant":variant,"seed":seed,"train_delay":delay,"pretrain_completed":trained,
                 "pretrain_requested":config.pretrain_steps,"conditions":{},
                 "trunk_parameters":sum(p.numel() for p in base.parameters() if p.requires_grad)}
            if trained!=config.pretrain_steps:
                result["runs"].append(row);result["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i+1:]);break
            eval_seed=seed+1_000_000
            row["conditions"]["native_200"]={str(h):paired_selective_eval(base,h,seed=eval_seed,batch=config.eval_examples)
                                                  for h in (delay,2*delay,4*delay)}
            for kind in ("top","all"):
                key="frozen_"+kind
                head,norm,done=fit_frozen(base,delay=delay,seed=seed,kind=kind,config=config,began=began)
                row["conditions"][key]={"steps":done,"head_parameters":sum(p.numel() for p in head.parameters()),
                    "evaluation":{str(h):eval_frozen(base,head,norm,h,config.eval_examples,seed=eval_seed,kind=kind)
                                  for h in (delay,2*delay,4*delay)}}
                if done!=config.additional_steps:break
            if all(row["conditions"].get("frozen_"+kind,{}).get("steps")==config.additional_steps for kind in ("top","all")):
                # Both new runs start from exactly the same pretrained original weights.
                continuation=copy.deepcopy(base)
                joint=copy.deepcopy(base)
                seed_for_head=seed+8008
                with torch.random.fork_rng(devices=[]):
                    torch.manual_seed(seed_for_head)
                    width=state_features(joint.initial_state(1),"all").shape[1]
                    joint_head=AddressedReadout(width)
                native_steps=train_native_continue(continuation,delay=delay,seed=seed,config=config,began=began)
                row["conditions"]["native_continued"]={"steps":native_steps,"evaluation":{
                    str(h):paired_selective_eval(continuation,h,seed=eval_seed,batch=config.eval_examples)
                    for h in (delay,2*delay,4*delay)}}
                if native_steps==config.additional_steps:
                    joint_steps=train_joint(joint,joint_head,delay=delay,seed=seed,config=config,began=began)
                    row["conditions"]["joint_all"]={"steps":joint_steps,"head_parameters":sum(p.numel() for p in joint_head.parameters()),
                       "evaluation":{str(h):eval_readout(joint,joint_head,h,config.eval_examples,seed=eval_seed,kind="all")
                          for h in (delay,2*delay,4*delay)}}
            row["complete"]=all(row["conditions"].get(k,{}).get("steps")==config.additional_steps
                                   for k in ("frozen_top","frozen_all","native_continued","joint_all"))
            result["runs"].append(row)
            print(json.dumps({"finished":len(result["runs"]),"variant":variant,"seed":seed,"delay":delay,
                "complete":row["complete"],"frozen_all_unequal":row["conditions"].get("frozen_all",{}).get("evaluation",{}).get(str(delay),{}).get("paired_on_unequal")}),flush=True)
            if not row["complete"]:
                result["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i+1:]);break
        result["status"]="complete" if len(result["runs"])==len(jobs) and not result["skipped"] and all(x["complete"] for x in result["runs"]) else "budget_limited"
    finally:
        result["elapsed_seconds"]=time.monotonic()-began
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open("x",encoding="utf-8") as f:json.dump(result,f,indent=2)
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--variants",default=",".join(VARIANTS))
    p.add_argument("--seeds",default="17,29,43")
    p.add_argument("--delays",default="16,64")
    p.add_argument("--pretrain-steps",type=int,default=200)
    p.add_argument("--additional-steps",type=int,default=150)
    p.add_argument("--batch",type=int,default=16)
    p.add_argument("--head-examples",type=int,default=1024)
    p.add_argument("--head-batch",type=int,default=64)
    p.add_argument("--eval-examples",type=int,default=512)
    p.add_argument("--max-wall-seconds",type=float,default=540)
    a=p.parse_args(argv)
    cfg=Config(variants=tuple(a.variants.split(",")),seeds=tuple(map(int,a.seeds.split(","))),
        delays=tuple(map(int,a.delays.split(","))),pretrain_steps=a.pretrain_steps,
        additional_steps=a.additional_steps,batch_size=a.batch,
        head_examples=a.head_examples,head_batch=a.head_batch,eval_examples=a.eval_examples,
        max_wall_seconds=a.max_wall_seconds)
    summary=execute(cfg,output=a.output)
    print(f"Experiment 007: {summary['status']}; runs={len(summary['runs'])}; skipped={len(summary['skipped'])}; seconds={summary['elapsed_seconds']:.1f}",flush=True)

if __name__=="__main__":main()
