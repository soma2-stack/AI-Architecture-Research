"""Experiment 003: contradictory-bit distractor interference in recurrent memory.

CPU supervised learning on explicit invocation only. Not a new RNN proof,
not an RL collector, and not a test of formal robust learning-credit D.
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
from torch import Tensor
import torch.nn.functional as F

from .experiment_002 import build
from .learning_pilot import BIT0, BIT1, QUERY, DISTRACTOR_START, DISTRACTOR_END, query_loss

STORE = 5
REGIMES = ("benign", "interfering")
EVAL_REGIMES = ("benign", "interfering", "all_bits")
VARIANTS = ("tanh_w32", "near_critical_w32", "protected_w32", "gru_w32",
            "lstm_w32", "protected_random_w32", "protected_no_project_w32")

@dataclass(frozen=True)
class Config:
    variants:tuple[str,...]=VARIANTS
    regimes:tuple[str,...]=REGIMES
    seeds:tuple[int,...]=(17,29,43)
    train_delay:int=64
    eval_delays:tuple[int,...]=(64,128,256)
    steps:int=150
    batch_size:int=16
    eval_batch:int=512
    lr:float=.002
    grad_clip:float=1.0
    max_wall_seconds:float=540.0
    def __post_init__(self):
        if not self.variants or len(set(self.variants))!=len(self.variants) or any(v not in VARIANTS for v in self.variants):
            raise ValueError("invalid variants")
        if not self.regimes or any(v not in REGIMES for v in self.regimes):
            raise ValueError("invalid regimes")
        if not self.seeds or any(type(s) is not int for s in self.seeds):
            raise ValueError("invalid seeds")
        if not self.eval_delays or any(type(x) is not int or x<1 for x in (*self.eval_delays,self.train_delay)):
            raise ValueError("invalid delays")
        if any(type(x) is not int or x<1 for x in (self.steps,self.batch_size,self.eval_batch)):
            raise ValueError("invalid batch or step count")
        if any(not math.isfinite(x) or x<=0 for x in (self.lr,self.grad_clip,self.max_wall_seconds)):
            raise ValueError("invalid numerical hyperparameters")


def make_batch(regime:str,delay:int,batch:int,*,seed:int)->tuple[Tensor,Tensor,dict]:
    """One marked write followed by distractors that may contain bit tokens.

    The **same** BIT0/BIT1 tokens occur as targets and as conflicting noise.
    Noise carries no STORE marker, so original value is identifiable only
    by remembering the tagged write, not by reading the last bit token.
    """
    if regime not in EVAL_REGIMES or delay<1 or batch<1:
        raise ValueError("invalid noise regime, delay or batch size")
    gen=torch.Generator(device='cpu').manual_seed(seed)
    labels=(torch.randperm(batch,generator=gen)%2).long()
    fillers=torch.randint(DISTRACTOR_START,DISTRACTOR_END,(batch,delay),generator=gen)
    bits=torch.randint(BIT0,BIT1+1,(batch,delay),generator=gen)
    if regime=='all_bits':noise=bits
    elif regime=='benign':noise=fillers
    else:
        is_bit=torch.rand((batch,delay),generator=gen)<.5
        noise=torch.where(is_bit,bits,fillers)
    tokens=torch.cat((torch.full((batch,1),STORE,dtype=torch.long),
                      labels[:,None]+BIT0,noise,
                      torch.full((batch,1),QUERY,dtype=torch.long)),dim=1)
    # A deliberately weak last-seen-bit heuristic will be near chance on
    # independent noise: it is not a viable shortcut to the marked value.
    conflicting=(noise.eq(BIT0+(1-labels)[:,None])).any(dim=1)
    return tokens,labels,{"conflicting_noise_fraction":float(conflicting.float().mean()),
                           "bit_noise_fraction":float(((noise==BIT0)|(noise==BIT1)).float().mean())}


@torch.no_grad()
def evaluate(model,regime,delay,*,seed,batch):
    model.eval()
    ids,y,meta=make_batch(regime,delay,batch,seed=seed)
    logits=model(ids)[0][:,-1,BIT0:BIT1+1]
    pred=logits.argmax(dim=1)
    return {"accuracy":float(pred.eq(y).float().mean()),
            "loss":float(F.cross_entropy(logits,y)),
            "examples":batch,
            "positive_fraction":float(y.float().mean()),
            **meta}


def execute(config:Config,*,output:Path):
    if output.exists():raise FileExistsError(f"refusing overwrite of {output}")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(0)
    began=time.monotonic()
    report={"status":"running","config":asdict(config),
            "environment":{"torch":torch.__version__,"python":platform.python_version(),"device":"cpu"},
            "runs":[],"skipped":[],"scope":"synthetic supervised interference test, not formal D"}
    jobs=[(regime,seed,var) for regime in config.regimes for seed in config.seeds for var in config.variants]
    try:
        for i,(regime,seed,var) in enumerate(jobs):
            if time.monotonic()-began>=config.max_wall_seconds:
                report['skipped'].extend([{"regime":r,"seed":s,"variant":v,"reason":"wall_budget"} for r,s,v in jobs[i:]])
                break
            model=build(var,seed)
            opt=torch.optim.AdamW(model.parameters(),lr=config.lr)
            losses=[];completed=0;runstart=time.monotonic()
            for step in range(config.steps):
                if time.monotonic()-began>=config.max_wall_seconds:break
                model.train()
                batch_seed=seed*1_000_003+step*8191+config.train_delay*17+(0 if regime=='benign' else 97)
                ids,y,_=make_batch(regime,config.train_delay,config.batch_size,seed=batch_seed)
                opt.zero_grad(set_to_none=True)
                loss=query_loss(model,ids,y)
                if not bool(torch.isfinite(loss)):
                    raise FloatingPointError(f"nonfinite loss {var}/{regime}/{seed}/{step}")
                loss.backward()
                if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
                    raise FloatingPointError(f"nonfinite gradient {var}/{regime}/{seed}/{step}")
                torch.nn.utils.clip_grad_norm_(model.parameters(),config.grad_clip)
                opt.step();completed+=1;losses.append(float(loss.detach()))
            measures={}
            for testregime in EVAL_REGIMES:
                measures[testregime]={str(d):evaluate(model,testregime,d,
                    seed=seed+1_000_000,batch=config.eval_batch) for d in config.eval_delays}
            row={"regime":regime,"seed":seed,"variant":var,"complete":completed==config.steps,
                 "steps_completed":completed,"steps_requested":config.steps,
                 "train_loss_first":losses[0] if losses else None,
                 "train_loss_last":losses[-1] if losses else None,
                 "parameters":sum(p.numel() for p in model.parameters() if p.requires_grad),
                 "metrics":measures,"elapsed_seconds":time.monotonic()-runstart}
            report['runs'].append(row)
            print(json.dumps({"finished":len(report['runs']),"regime":regime,"variant":var,
                              "seed":seed,"steps":completed,
                              "tested_noise_accuracy_64":measures['interfering'][str(config.train_delay)]['accuracy']}),flush=True)
            if not row['complete']:
                report['skipped'].extend([{"regime":r,"seed":s,"variant":v,"reason":"wall_budget"}
                                          for r,s,v in jobs[i+1:]])
                break
        report['status']='complete' if not report['skipped'] and all(r['complete'] for r in report['runs']) else 'budget_limited'
    finally:
        report['elapsed_seconds']=time.monotonic()-began
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--variants',default=','.join(VARIANTS))
    p.add_argument('--regimes',default='benign,interfering')
    p.add_argument('--seeds',default='17,29,43')
    p.add_argument('--train-delay',type=int,default=64)
    p.add_argument('--eval-delays',default='64,128,256')
    p.add_argument('--steps',type=int,default=150)
    p.add_argument('--batch',type=int,default=16)
    p.add_argument('--eval-batch',type=int,default=512)
    p.add_argument('--max-wall-seconds',type=float,default=540)
    args=p.parse_args(argv)
    cfg=Config(variants=tuple(args.variants.split(',')),regimes=tuple(args.regimes.split(',')),
        seeds=tuple(map(int,args.seeds.split(','))),train_delay=args.train_delay,
        eval_delays=tuple(map(int,args.eval_delays.split(','))),steps=args.steps,
        batch_size=args.batch,eval_batch=args.eval_batch,max_wall_seconds=args.max_wall_seconds)
    result=execute(cfg,output=args.output)
    print(f"Experiment 003 status: {result['status']}; runs={len(result['runs'])}; skipped={len(result['skipped'])}; seconds={result['elapsed_seconds']:.1f}")

if __name__=='__main__':main()
