"""Experiment 010: capacity versus slot count/value alphabet, CPU-only.

Runs ONLY through explicit CLI. Uses existing trainable token RNNs without changes.
Known prior art / structure-aware baseline: a token-addressed delta-rule memory.
This baseline reads the WRITE/QUERY addresses provided as input token IDs; this is
an explicit inductive advantage, not an architecture-matched neural comparison.
No oracle write masks, labels, or final values are passed to learned RNNs.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn, Tensor
import torch.nn.functional as F

from .candidates import CandidateConfig, CandidateLanguageModel
from .gated import GatedConfig, GatedLanguageModel

# IDs deliberately partitioned; query tokens cannot reveal desired value.
PAD=0
WRITE_START=2     # WRITE_0 .. WRITE_7
VALUE_START=10    # VALUE_0 .. VALUE_3
QUERY_START=14    # QUERY_0 .. QUERY_7
FILLER_START=22   # 22..30 (includes no valid WRITE/QUERY/VALUE tokens)
VOCAB=32
VARIANTS=("protected", "protected_no_retain", "gru24", "gru32", "delta_rule")


def generator_batch(slots: int, values: int, delay: int, batch: int, *, seed: int,
                    min_updates: int=1, max_updates: int=3) -> Tensor:
    """Random initial writes for every slot; random marked updates and decoy VALUE tokens.

    Return query-free token histories [B,2*slots+delay]. Update positions are
    uniformly chosen without overlapping two-token commands. No answer leakage.
    """
    if type(slots) is not int or slots not in (2,4,8) or type(values) is not int or values not in (2,4):
        raise ValueError("slots must be 2/4/8; values must be 2/4")
    if type(delay) is not int or type(batch) is not int or batch<1 or delay<2*max_updates+1:
        raise ValueError("invalid length or batch")
    if not 1<=min_updates<=max_updates<=3 or type(seed) is not int:
        raise ValueError("invalid updates or seed")
    g=torch.Generator(device="cpu").manual_seed(seed)
    # Balance initial values/slots approximately; all downstream seeds held out.
    initial=torch.randint(values,(batch,slots),generator=g)
    prefix=torch.empty((batch,2*slots),dtype=torch.long)
    order=torch.argsort(torch.rand(batch,slots,generator=g),dim=1)
    prefix[:,0::2]=WRITE_START+order
    prefix[:,1::2]=VALUE_START+initial.gather(1,order)
    body=torch.randint(FILLER_START,FILLER_START+8,(batch,delay),generator=g)
    noise=torch.randint(VALUE_START,VALUE_START+values,(batch,delay),generator=g)
    body=torch.where(torch.rand(batch,delay,generator=g)<.25, noise, body)
    counts=torch.randint(min_updates,max_updates+1,(batch,),generator=g)
    update_slots=torch.randint(slots,(batch,max_updates),generator=g)
    update_vals=torch.randint(values,(batch,max_updates),generator=g)
    priorities=torch.rand((batch,delay),generator=g)
    for i in range(batch):
        k=int(counts[i]); starts=torch.sort(torch.argsort(priorities[i,:delay-k])[:k]).values+torch.arange(k)
        body[i,starts]=WRITE_START+update_slots[i,:k]
        body[i,starts+1]=VALUE_START+update_vals[i,:k]
    return torch.cat((prefix,body),dim=1)


def replay(tokens: Tensor, slots: int, values: int) -> Tensor:
    """Independent reference semantics; a VALUE token writes only after a WRITE tag."""
    if tokens.dtype!=torch.long or tokens.ndim!=2: raise ValueError("tokens must be [B,T] long")
    b,t=tokens.shape
    result=torch.full((b,slots),-1,dtype=torch.long)
    pending=torch.full((b,),-1,dtype=torch.long)
    for j in range(t):
        tok=tokens[:,j]
        val=(tok>=VALUE_START)&(tok<VALUE_START+values)
        valid=val&(pending>=0)
        for s in range(slots):
            result[:,s]=torch.where(valid&(pending==s),tok-VALUE_START,result[:,s])
        # Every VALUE closes the pending write; nonvalue tokens other than
        # WRITE clear pending, making stray bits non-writes.
        pending=torch.where((tok>=WRITE_START)&(tok<WRITE_START+slots),tok-WRITE_START,-1)
    if (result<0).any():raise ValueError("history missing initial slot write")
    return result


def last_marked_value(prefix:Tensor,slots:int,values:int)->Tensor:
    prev=torch.full((prefix.shape[0],),-1,dtype=torch.long)
    last=torch.full_like(prev,-1)
    for j in range(prefix.shape[1]):
        tok=prefix[:,j]
        v=(tok>=VALUE_START)&(tok<VALUE_START+values)&(prev>=0)
        last=torch.where(v,tok-VALUE_START,last)
        prev=torch.where((tok>=WRITE_START)&(tok<WRITE_START+slots),tok-WRITE_START,-1)
    return last


def query_histories(prefix:Tensor,slots:int)->Tensor:
    """[B*S,T+1], slot-major batches, identical prefix for each query."""
    b,t=prefix.shape
    all_ids=prefix.repeat(slots,1)
    q=torch.arange(slots).repeat_interleave(b)+QUERY_START
    return torch.cat((all_ids,q[:,None]),dim=1)


class DeltaRule(nn.Module):
    """Known explicit keyed delta-rule memory; uses token event grammar.

    M_s <- M_s + (embedding(value)-M_s), implemented as a delta write with
    eta=1 at identified tag/value pairs. The differentiable value embeddings
    and readout are trained, but addressing and write detection are PROVIDED.
    This is a structured reference, NOT a matched architecture comparison.
    """
    def __init__(self,slots:int,values:int,seed:int):
        super().__init__()
        self.slots=slots;self.values=values
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            self.value_embedding=nn.Embedding(values,32)
            self.readout=nn.Linear(32,values)
        self.vocab=VOCAB
    def forward(self,ids:Tensor):
        b,t=ids.shape
        memory=self.value_embedding.weight.new_zeros(b,self.slots,32)
        pending=torch.full((b,),-1,device=ids.device,dtype=torch.long)
        for j in range(t):
            token=ids[:,j]
            is_val=(token>=VALUE_START)&(token<VALUE_START+self.values)
            for s in range(self.slots):
                mask=(is_val&(pending==s))[:,None]
                data=self.value_embedding((token-VALUE_START).clamp(0,self.values-1))
                current=memory[:,s]
                # Functional delta write avoids in-place autograd mutations.
                selected=torch.where(mask,current+(data-current),current)
                memory=torch.stack([selected if k==s else memory[:,k] for k in range(self.slots)],dim=1)
            pending=torch.where((token>=WRITE_START)&(token<WRITE_START+self.slots),token-WRITE_START,-1)
        query=(ids[:,-1]-QUERY_START).clamp(0,self.slots-1)
        picked=memory[torch.arange(b,device=ids.device),query]
        # Output logit convention matches trainable RNNs: labels are 0..values-1.
        return self.readout(picked)


def build(name:str,slots:int,values:int,seed:int):
    if name not in VARIANTS:raise ValueError("unknown model")
    if name=="delta_rule":return DeltaRule(slots,values,seed)
    if name.startswith("gru"):
        width=24 if name=="gru24" else 32
        return GatedLanguageModel(GatedConfig(vocab_size=VOCAB,width=width,layers=2,cell_type="gru",seed=seed))
    return CandidateLanguageModel(CandidateConfig(vocab_size=VOCAB,width=32,layers=2,protected_channels=8,
                         cell_type="protected",seed=seed,retain_slow=(name=="protected")))


def predictions(model, history:Tensor, slots:int, values:int)->Tensor:
    all_ids=query_histories(history,slots)
    raw=model(all_ids)
    if isinstance(model,DeltaRule): lg=raw
    else: lg=raw[0][:,-1,VALUE_START:VALUE_START+values]
    # [S,B] -> [B,S]
    return lg.reshape(slots,history.shape[0],values).transpose(0,1)


def metrics(pred:Tensor,y:Tensor,values:int)->dict:
    exact=pred.eq(y)
    whole=exact.all(1)
    varied=(y.max(1).values!=y.min(1).values)
    return {"per_slot":float(exact.float().mean()),"whole":float(whole.float().mean()),
            "whole_varied":float(whole[varied].float().mean()) if bool(varied.any()) else None,
            "varied_count":int(varied.sum()),"whole_guess_chance":values**(-y.shape[1]),
            "copy_latest_upper_chance_varied":0.0}


@dataclass(frozen=True)
class Config:
    variants:tuple[str,...]=("protected","protected_no_retain","gru24","delta_rule")
    tasks:tuple[tuple[int,int],...]=((2,2),(4,2),(8,2),(4,4),(8,4))
    seeds:tuple[int,...]=(17,29,43)
    delay:int=64
    eval_delays:tuple[int,...]=(64,256)
    steps:int=800
    batch:int=12
    eval_batch:int=128
    eval_every:int=200
    lr:float=.002
    clip:float=1.0
    max_wall_seconds:float=750.0

    def __post_init__(self):
        if not self.variants or len(set(self.variants))!=len(self.variants) or any(v not in VARIANTS for v in self.variants):raise ValueError("bad variants")
        if not self.tasks or len(set(self.tasks))!=len(self.tasks) or any(s not in (2,4,8) or v not in (2,4) for s,v in self.tasks):raise ValueError("bad tasks")
        if not self.seeds or len(set(self.seeds))!=len(self.seeds) or any(type(s)!=int or s<0 for s in self.seeds):raise ValueError("bad seeds")
        if self.delay<7 or any(d<7 for d in self.eval_delays):raise ValueError("bad delays")
        if any(type(x)!=int or x<1 for x in (self.steps,self.batch,self.eval_batch,self.eval_every)):raise ValueError("bad budgets")
        if any(not math.isfinite(x) or x<=0 for x in (self.lr,self.clip,self.max_wall_seconds)):raise ValueError("bad float budgets")


def run_one(name:str,slots:int,values:int,seed:int,cfg:Config,deadline:float)->dict:
    model=build(name,slots,values,seed)
    model.train(); opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr)
    t0=time.monotonic();steps=0;losses=[];curve=[];status="complete"
    for step in range(cfg.steps):
        if time.monotonic()>deadline: status="time_limit";break
        model.train()
        hist=generator_batch(slots,values,cfg.delay,cfg.batch,seed=seed*1_000_003+step*8191+slots*197+values)
        labels=replay(hist,slots,values)
        opt.zero_grad(set_to_none=True)
        logits=predictions(model,hist,slots,values)
        loss=F.cross_entropy(logits.reshape(-1,values),labels.reshape(-1))
        if not bool(torch.isfinite(loss)):status="nonfinite_loss";break
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()): status="nonfinite_grad";break
        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),cfg.clip)
        opt.step();steps+=1;losses.append(float(loss.detach()))
        if steps%cfg.eval_every==0:
            score=evaluate(model,slots,values,cfg.delay,seed=seed+9_000_000,histories=cfg.eval_batch)
            curve.append({"step":steps,"whole_varied":score["whole_varied"],"whole":score["whole"],"loss":float(loss.detach())})
    out={"variant":name,"slots":slots,"values":values,"seed":seed,"steps":steps,"status":status,
         "parameters":sum(p.numel() for p in model.parameters()),"elapsed_s":round(time.monotonic()-t0,3),
         "loss_first":losses[0] if losses else None,"loss_last":losses[-1] if losses else None,"curve":curve}
    if steps>0:
        out["eval"]={str(delay):evaluate(model,slots,values,delay,seed=seed+8_000_000+delay,histories=cfg.eval_batch)
                     for delay in cfg.eval_delays}
    return out


@torch.no_grad()
def evaluate(model,slots:int,values:int,delay:int,*,seed:int,histories:int)->dict:
    model.eval()
    x=generator_batch(slots,values,delay,histories,seed=seed)
    y=replay(x,slots,values)
    chunks=[]
    # Reduce peak CPU RAM on long-sequence evals; still tests all queried slots.
    for a in range(0,histories,32):
        x0=x[a:a+32]
        out=predictions(model,x0,slots,values).argmax(-1)
        chunks.append(out)
    pred=torch.cat(chunks)
    m=metrics(pred,y,values)
    # Exact grammar parser upper bound, not presented as learned accuracy.
    m["oracle_replay_whole"]=1.0
    # Naive last-written-value shortcut: same answer to every slot.
    w=last_marked_value(x,slots,values)
    naive=w[:,None].expand_as(y)
    m["last_write_copy_whole"] = float(naive.eq(y).all(1).float().mean())
    m["histories"]=histories
    return m


def execute(cfg:Config,path:Path)->dict:
    if path.exists():raise FileExistsError(path)
    torch.set_num_threads(1)
    torch.manual_seed(0)
    began=time.monotonic();deadline=began+cfg.max_wall_seconds
    jobs=[(s,v,name,seed) for s,v in cfg.tasks for seed in cfg.seeds for name in cfg.variants]
    result={"status":"running","config":asdict(cfg),"environment":{"torch":torch.__version__,"cpu_threads":torch.get_num_threads(),"python":platform.python_version(),"cuda_available":torch.cuda.is_available(),"CUDA_VISIBLE_DEVICES":os.environ.get("CUDA_VISIBLE_DEVICES")},
            "scope":"synthetic supervised scaling pilot. Delta-rule has grammar-aware inductive bias; oracle is reference rule, not trained model. NOT formal theorem evidence.","runs":[],"skipped":[]}
    try:
        for i,(slots,values,name,seed) in enumerate(jobs):
            if time.monotonic()>deadline:
                result["skipped"]=[{"slots":s,"values":v,"variant":n,"seed":sd,"reason":"wall_budget"} for s,v,n,sd in jobs[i:]]
                break
            model_row=run_one(name,slots,values,seed,cfg,deadline)
            result["runs"].append(model_row)
            print(json.dumps({"completed":len(result["runs"]),"of":len(jobs),"variant":name,"slots":slots,"values":values,"seed":seed,"status":model_row["status"],"steps":model_row["steps"],
                              "primary":model_row.get("eval",{}).get(str(cfg.delay),{}).get("whole_varied")}),flush=True)
    finally:
        result["elapsed_seconds"]=round(time.monotonic()-began,3)
        result["status"]="complete" if not result["skipped"] and len(result["runs"])==len(jobs) and all(r["status"]=="complete" for r in result["runs"]) else "incomplete"
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x',encoding="utf-8") as f:json.dump(result,f,indent=2)
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="Bounded CPU-only RNN capacity study")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--variants",default=",".join(Config.variants))
    p.add_argument("--tasks",default="2x2,4x2,8x2,4x4,8x4")
    p.add_argument("--seeds",default="17,29,43")
    p.add_argument("--steps",type=int,default=800)
    p.add_argument("--batch",type=int,default=12)
    p.add_argument("--delay",type=int,default=64)
    p.add_argument("--eval-delays",default="64,256")
    p.add_argument("--eval-batch",type=int,default=128)
    p.add_argument("--eval-every",type=int,default=200)
    p.add_argument("--max-wall-seconds",type=float,default=750)
    a=p.parse_args(argv)
    ints=lambda s:tuple(int(x) for x in s.split(","))
    tasks=tuple(tuple(int(x) for x in item.split("x")) for item in a.tasks.split(","))
    c=Config(variants=tuple(a.variants.split(",")),tasks=tasks,seeds=ints(a.seeds),steps=a.steps,batch=a.batch,delay=a.delay,
             eval_delays=ints(a.eval_delays),eval_batch=a.eval_batch,eval_every=a.eval_every,max_wall_seconds=a.max_wall_seconds)
    r=execute(c,a.output)
    print(f"Experiment 010: {r['status']} {len(r['runs'])} runs, {len(r['skipped'])} skipped, {r['elapsed_seconds']} seconds")

if __name__=="__main__":main()
