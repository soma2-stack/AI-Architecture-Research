"""Experiment 004: dual-query supervised selective two-slot memory.

No implicit training. CLI CPU-only pilot; formal robust credit dimension is
not measured. Trains *both* queries on identical histories to remove the
75% single-query last-write shortcut from the training objective.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
import time
from dataclasses import dataclass,asdict
from pathlib import Path
import torch
from torch import Tensor,nn
import torch.nn.functional as F

from .experiment_002 import _slot_targets,paired_selective_eval,build
from .learning_pilot import BIT0,BIT1,QUERY_A,QUERY_B,make_batch

VARIANTS=("tanh_w32","near_critical_w32","protected_w32","gru_w32","lstm_w32",
          "gru_w24","lstm_w20","protected_random_w32","protected_no_project_w32")

@dataclass(frozen=True)
class Config:
    variants:tuple[str,...]=VARIANTS
    seeds:tuple[int,...]=(17,29,43)
    train_delay:int=64
    eval_delays:tuple[int,...]=(64,128,256)
    steps:int=240
    batch_size:int=16
    eval_batch:int=512
    lr:float=.002
    grad_clip:float=1.
    max_wall_seconds:float=540.
    def __post_init__(self):
        if not self.variants or len(set(self.variants))!=len(self.variants) or any(v not in VARIANTS for v in self.variants):raise ValueError('invalid variants')
        if not self.seeds or any(type(s) is not int for s in self.seeds):raise ValueError('invalid seeds')
        if not self.eval_delays or any(type(i) is not int or i<1 for i in (*self.eval_delays,self.train_delay)):raise ValueError('invalid delays')
        if any(type(i) is not int or i<1 for i in (self.steps,self.batch_size,self.eval_batch)):raise ValueError('invalid steps/batch')
        if any(not math.isfinite(x) or x<=0 for x in (self.lr,self.grad_clip,self.max_wall_seconds)):raise ValueError('invalid resources')


def _paired_inputs(delay:int,batch:int,*,seed:int):
    ids,_,meta=make_batch('selective',delay,batch,seed=seed)
    values=_slot_targets(ids[:,:-1],delay)
    a=ids.clone();b=ids.clone();a[:,-1]=QUERY_A;b[:,-1]=QUERY_B
    return torch.cat((a,b),dim=0),torch.cat((values[:,0],values[:,1]),dim=0),meta


def paired_query_loss(model:nn.Module,delay:int,batch:int,*,seed:int):
    x,y,_=_paired_inputs(delay,batch,seed=seed)
    logits=model(x)[0][:,-1,BIT0:BIT1+1]
    return F.cross_entropy(logits,y)


def execute(config:Config,*,output:Path):
    if output.exists():raise FileExistsError(f'refusing overwrite of {output}')
    torch.manual_seed(0);torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    began=time.monotonic();report={"status":"running","config":asdict(config),
        "environment":{"torch":torch.__version__,"python":platform.python_version(),"device":"cpu"},
        "runs":[],"skipped":[],"scope":"dual-query synthetic supervised memory, NOT formal D"}
    jobs=[(seed,var) for seed in config.seeds for var in config.variants]
    try:
        for i,(seed,var) in enumerate(jobs):
            if time.monotonic()-began>=config.max_wall_seconds:
                report['skipped'].extend([{"seed":s,"variant":v,"reason":"wall_budget"} for s,v in jobs[i:]])
                break
            model=build(var,seed)
            optim=torch.optim.AdamW(model.parameters(),lr=config.lr)
            losses=[];done=0;start=time.monotonic()
            for step in range(config.steps):
                if time.monotonic()-began>=config.max_wall_seconds:break
                model.train()
                batch_seed=seed*1_000_003+step*8191+config.train_delay*17+97
                optim.zero_grad(set_to_none=True)
                loss=paired_query_loss(model,config.train_delay,config.batch_size,seed=batch_seed)
                if not bool(torch.isfinite(loss)):raise FloatingPointError(f'bad loss {var} {seed} {step}')
                loss.backward()
                if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
                    raise FloatingPointError(f'bad gradient {var} {seed} {step}')
                torch.nn.utils.clip_grad_norm_(model.parameters(),config.grad_clip)
                optim.step();done+=1;losses.append(float(loss.detach()))
            metrics={str(d):paired_selective_eval(model,d,seed=seed+1_000_000,batch=config.eval_batch) for d in config.eval_delays}
            row={"seed":seed,"variant":var,"steps_requested":config.steps,"steps_completed":done,
                 "complete":done==config.steps,"train_loss_first":losses[0] if losses else None,
                 "train_loss_last":losses[-1] if losses else None,"evaluation":metrics,
                 "parameters":sum(p.numel() for p in model.parameters() if p.requires_grad),
                 "elapsed_seconds":time.monotonic()-start}
            report['runs'].append(row)
            print(json.dumps({"finished":len(report['runs']),"variant":var,"seed":seed,"steps":done,
                "paired_both_at64":metrics[str(config.train_delay)]['paired_both_accuracy']}),flush=True)
            if not row['complete']:
                report['skipped'].extend([{"seed":s,"variant":v,"reason":"wall_budget"} for s,v in jobs[i+1:]])
                break
        report['status']='complete' if not report['skipped'] and all(r['complete'] for r in report['runs']) else 'budget_limited'
    finally:
        report['elapsed_seconds']=time.monotonic()-began
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    return report


def main(argv=None):
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--output',required=True,type=Path)
    a.add_argument('--variants',default=','.join(VARIANTS))
    a.add_argument('--seeds',default='17,29,43')
    a.add_argument('--train-delay',type=int,default=64)
    a.add_argument('--eval-delays',default='64,128,256')
    a.add_argument('--steps',type=int,default=240)
    a.add_argument('--batch',type=int,default=16)
    a.add_argument('--eval-batch',type=int,default=512)
    a.add_argument('--max-wall-seconds',type=float,default=540)
    args=a.parse_args(argv)
    cfg=Config(variants=tuple(args.variants.split(',')),seeds=tuple(map(int,args.seeds.split(','))),
        train_delay=args.train_delay,eval_delays=tuple(map(int,args.eval_delays.split(','))),
        steps=args.steps,batch_size=args.batch,eval_batch=args.eval_batch,max_wall_seconds=args.max_wall_seconds)
    result=execute(cfg,output=args.output)
    print(f"Experiment 004 status: {result['status']}, runs={len(result['runs'])}, skipped={len(result['skipped'])}, time={result['elapsed_seconds']:.1f}s")
if __name__=='__main__':main()
