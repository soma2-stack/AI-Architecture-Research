"""Experiment 006: frozen-state decodability at two stages of two-slot memory.

Test a *diagnosis*, not a theorem or a new architecture: can a probe decode
both final slot values from a trained frozen recurrent state even when the
model's native token readout cannot? Recreates 005 training because the old
run stored metrics, not weights. CPU-only. No trained-state write masks.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import platform
import time

import torch
from torch import nn
import torch.nn.functional as F

from .experiment_005 import make_variant, paired_query_loss
from .experiment_002 import _slot_targets, paired_selective_eval
from .learning_pilot import make_batch

VARIANTS = ("protected_w32", "state_gated_w32", "gru_w32", "lstm_w32")
STAGES = ("after_update", "after_distractors")
PROBES = ("linear", "mlp")


@dataclass(frozen=True)
class Config:
    variants: tuple[str, ...] = VARIANTS
    seeds: tuple[int, ...] = (17, 29, 43)
    delays: tuple[int, ...] = (16, 64)
    train_steps: int = 200
    train_batch: int = 16
    probe_examples: int = 2048
    test_examples: int = 1024
    probe_steps: int = 200
    probe_batch: int = 128
    lr: float = .002
    probe_lr: float = .01
    max_wall_seconds: float = 540.

    def __post_init__(self):
        if not self.variants or len(set(self.variants)) != len(self.variants) or any(v not in VARIANTS for v in self.variants):
            raise ValueError("unknown or repeated model variant")
        if not self.seeds or any(type(s) is not int or s < 0 for s in self.seeds):
            raise ValueError("seeds must be nonnegative integers")
        if not self.delays or any(type(d) is not int or d < 2 for d in self.delays):
            raise ValueError("delays must be integers >= 2")
        if any(type(x) is not int or x < 1 for x in (self.train_steps,self.train_batch,
                    self.probe_examples,self.test_examples,self.probe_steps,self.probe_batch)):
            raise ValueError("steps and batch counts must be positive integers")
        if any(not math.isfinite(x) or x <= 0 for x in (self.lr,self.probe_lr,self.max_wall_seconds)):
            raise ValueError("learning rates/wall cap must be finite and positive")


def flatten_recurrent_state(state):
    """One feature per recurrent state scalar. LSTM includes *both* h and c."""
    values=[]
    for layer in state:
        if isinstance(layer, torch.Tensor):
            values.append(layer)
        elif isinstance(layer, tuple) and len(layer) == 2 and all(isinstance(v, torch.Tensor) for v in layer):
            values.extend(layer)
        else:
            raise TypeError("Unsupported recurrent state structure")
    if not values or any(x.ndim != 2 or x.shape[0] != values[0].shape[0] for x in values):
        raise ValueError("Recurrent state must be nonempty [batch,width] tensors")
    return torch.cat(values, dim=1).detach()


@torch.no_grad()
def extract_features(model, delay: int, samples: int, *, seed: int, chunk: int = 128):
    """Strictly query-free prefixes; train/test RNG stream is caller-owned."""
    if samples <= 0 or chunk <= 0:
        raise ValueError("positive sample/chunk count required")
    ids, _, _ = make_batch("selective", delay, samples, seed=seed)
    prefix=ids[:,:-1]
    labels=_slot_targets(prefix,delay)
    update_end=6+delay//2
    assert prefix.shape[1] == 6+delay
    outputs={stage:[] for stage in STAGES}
    model.eval()
    for sl in range(0,samples,chunk):
        x=prefix[sl:sl+chunk]
        _, after_update=model(x[:,:update_end])
        _, after_distractors=model(x[:,update_end:],state=after_update)
        outputs["after_update"].append(flatten_recurrent_state(after_update).cpu())
        outputs["after_distractors"].append(flatten_recurrent_state(after_distractors).cpu())
    return {key: torch.cat(values,dim=0) for key,values in outputs.items()}, labels.cpu()


def build_probe(kind: str, features: int):
    if kind == "linear":
        return nn.Linear(features,4)
    if kind == "mlp":
        return nn.Sequential(nn.Linear(features,64),nn.Tanh(),nn.Linear(64,4))
    raise ValueError("unknown probe")


def score_pair(logits, labels):
    if logits.ndim != 2 or logits.shape != (len(labels),4) or labels.shape != (len(logits),2):
        raise ValueError("expected [batch,4] logits and [batch,2] labels")
    pred=logits.reshape(-1,2,2).argmax(-1)
    matches=pred.eq(labels)
    pair=matches.all(-1)
    unequal=labels[:,0]!=labels[:,1]
    return {"paired_both_accuracy":float(pair.float().mean()),
            "paired_on_unequal":float(pair[unequal].float().mean()) if bool(unequal.any()) else None,
            "paired_on_equal":float(pair[~unequal].float().mean()) if bool((~unequal).any()) else None,
            "per_slot_accuracy": [float(v) for v in matches.float().mean(0)],
            "unequal_fraction":float(unequal.float().mean()), "examples":len(labels)}


def fit_probe(train_x, train_y, test_x, test_y, *, kind, seed, steps, batch_size, lr):
    """Reader only; feature tensors are detached and fixed for optimization."""
    if train_x.ndim!=2 or test_x.ndim!=2 or train_x.shape[1]!=test_x.shape[1]:
        raise ValueError("probe input dimension mismatch")
    if len(train_y)!=len(train_x) or len(test_y)!=len(test_x):
        raise ValueError("probe label mismatch")
    if train_x.requires_grad or test_x.requires_grad:
        raise ValueError("probe must use detached frozen features")
    mean=train_x.mean(0,keepdim=True)
    std=train_x.std(0,keepdim=True,unbiased=False).clamp_min(1e-4)
    x=(train_x-mean)/std; t=(test_x-mean)/std
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        probe=build_probe(kind,train_x.shape[1])
    opt=torch.optim.AdamW(probe.parameters(),lr=lr)
    rng=torch.Generator(device="cpu").manual_seed(seed+9_000_001)
    probe.train()
    for _ in range(steps):
        rows=torch.randint(0,len(x),(batch_size,),generator=rng)
        logits=probe(x[rows]).reshape(-1,2,2)
        loss=(F.cross_entropy(logits[:,0],train_y[rows,0])+F.cross_entropy(logits[:,1],train_y[rows,1]))/2
        if not bool(torch.isfinite(loss)):
            raise FloatingPointError("nonfinite probe loss")
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(probe.parameters(),1.)
        opt.step()
    probe.eval()
    with torch.no_grad():
        return {"held_out":score_pair(probe(t),test_y),
                "training":score_pair(probe(x),train_y),
                "parameter_count":sum(p.numel() for p in probe.parameters())}


def train_model(variant,seed,delay,config:Config,*,began):
    """Same model-data seed/optimizer schedule as Experiment 005."""
    model=make_variant(variant,seed)
    optimizer=torch.optim.AdamW(model.parameters(),lr=config.lr)
    last_loss=None
    for step in range(config.train_steps):
        if time.monotonic()-began >= config.max_wall_seconds:
            return model,step,last_loss
        batch_seed=seed*1_000_003+step*8191+delay*17+97
        optimizer.zero_grad(set_to_none=True)
        loss=paired_query_loss(model,delay,config.train_batch,seed=batch_seed)
        if not bool(torch.isfinite(loss)):
            raise FloatingPointError("nonfinite training loss")
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
            raise FloatingPointError("nonfinite training gradient")
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        optimizer.step()
        last_loss=float(loss.detach())
    return model,config.train_steps,last_loss


def execute(config: Config, *, output: Path):
    if output.exists():
        raise FileExistsError("refusing to overwrite evidence")
    torch.set_num_threads(1)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    began=time.monotonic()
    report={"status":"running","environment":{"torch":torch.__version__,
            "python":platform.python_version(),"cpu_threads":torch.get_num_threads()},
            "config":asdict(config),"runs":[],"skipped":[],
            "scope":"bounded frozen-state probes, NOT formal D or proof of storage absence"}
    jobs=[(delay,seed,var) for delay in config.delays for seed in config.seeds for var in config.variants]
    try:
        for i,(delay,seed,var) in enumerate(jobs):
            if time.monotonic()-began>=config.max_wall_seconds:
                report["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i:])
                break
            # Same fixed stream for each model/seed; same train/eval generation across probes.
            model,trained,loss=train_model(var,seed,delay,config,began=began)
            row={"variant":var,"seed":seed,"train_delay":delay,"train_steps_completed":trained,
                 "train_loss_last":loss,
                 "model_parameters":sum(p.numel() for p in model.parameters() if p.requires_grad),
                 "native":{},"readers":{},"untrained_reference":{},"feature_dimension":None,"probe_complete":False}
            if trained !=config.train_steps:
                report["runs"].append(row)
                report["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i+1:])
                break
            model.eval()
            # Preserve separate held-out stream: no overlap with the model's train seeds.
            native_seed=seed+1_000_000
            row["native"]=paired_selective_eval(model,delay,seed=native_seed,batch=config.test_examples)
            probe_seed=7_000_000+seed*101+delay*19
            x_train,y_train=extract_features(model,delay,config.probe_examples,seed=probe_seed)
            x_test,y_test=extract_features(model,delay,config.test_examples,seed=native_seed)
            assert x_train[STAGES[0]].shape[1]==x_test[STAGES[0]].shape[1]
            row["feature_dimension"]=x_train[STAGES[0]].shape[1]
            for stage in STAGES:
                row["readers"][stage]={}
                for kind in PROBES:
                    if time.monotonic()-began>=config.max_wall_seconds:
                        break
                    result=fit_probe(x_train[stage],y_train,x_test[stage],y_test,
                                     kind=kind,seed=probe_seed+(0 if kind=="linear" else 1),
                                     steps=config.probe_steps,batch_size=config.probe_batch,lr=config.probe_lr)
                    row["readers"][stage][kind]=result
            # Control: identical random initialization with NO supervised recurrent training.
            # A probe may decode bits from random features; do not confuse probe
            # performance with learned recurrent memory without this control.
            if time.monotonic()-began < config.max_wall_seconds:
                untrained=make_variant(var,seed)
                untrained_train,_=extract_features(untrained,delay,config.probe_examples,seed=probe_seed)
                untrained_test,_=extract_features(untrained,delay,config.test_examples,seed=native_seed)
                for kind in PROBES:
                    if time.monotonic()-began>=config.max_wall_seconds:
                        break
                    row["untrained_reference"][kind]=fit_probe(
                        untrained_train["after_distractors"],y_train,
                        untrained_test["after_distractors"],y_test,
                        kind=kind,seed=probe_seed+(0 if kind=="linear" else 1),
                        steps=config.probe_steps,batch_size=config.probe_batch,lr=config.probe_lr)
            row["probe_complete"]=all(len(row["readers"].get(st,{}))==len(PROBES) for st in STAGES) and len(row["untrained_reference"])==len(PROBES)
            report["runs"].append(row)
            print(json.dumps({"finished":len(report["runs"]),"model":var,"seed":seed,
                "delay":delay,"native_unequal":row["native"]["paired_on_unequal"],
                "final_linear_unequal":row["readers"].get("after_distractors",{}).get("linear",{}).get("held_out",{}).get("paired_on_unequal")}),flush=True)
            if not row["probe_complete"]:
                report["skipped"].extend({"delay":d,"seed":s,"variant":v,"reason":"wall_budget"} for d,s,v in jobs[i+1:])
                break
        report["status"]="complete" if len(report["runs"])==len(jobs) and not report["skipped"] and all(row.get("probe_complete") for row in report["runs"]) else "budget_limited"
    finally:
        report["elapsed_seconds"]=time.monotonic()-began
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open("x",encoding="utf-8") as f:
            json.dump(report,f,indent=2)
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--variants",default=",".join(VARIANTS))
    p.add_argument("--seeds",default="17,29,43")
    p.add_argument("--delays",default="16,64")
    p.add_argument("--train-steps",type=int,default=200)
    p.add_argument("--train-batch",type=int,default=16)
    p.add_argument("--probe-examples",type=int,default=2048)
    p.add_argument("--test-examples",type=int,default=1024)
    p.add_argument("--probe-steps",type=int,default=200)
    p.add_argument("--probe-batch",type=int,default=128)
    p.add_argument("--max-wall-seconds",type=float,default=540)
    args=p.parse_args(argv)
    cfg=Config(variants=tuple(args.variants.split(",")),seeds=tuple(map(int,args.seeds.split(","))),
               delays=tuple(map(int,args.delays.split(","))),train_steps=args.train_steps,
               train_batch=args.train_batch,probe_examples=args.probe_examples,
               test_examples=args.test_examples,probe_steps=args.probe_steps,
               probe_batch=args.probe_batch,max_wall_seconds=args.max_wall_seconds)
    result=execute(cfg,output=args.output)
    print(f"Experiment 006: {result['status']}; runs={len(result['runs'])}; skipped={len(result['skipped'])}; seconds={result['elapsed_seconds']:.1f}")


if __name__=="__main__":
    main()
