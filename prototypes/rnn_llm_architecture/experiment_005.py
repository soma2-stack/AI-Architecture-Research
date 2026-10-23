"""Experiment 005: state-conditioned protected gate vs state-independent controls.

A bounded CPU-only synthetic paired-query test. This is a known GRU-style
state-dependent gating concept, NOT a new primitive or theorem construction.
"""
from __future__ import annotations
import argparse,json,math,platform,time
from dataclasses import asdict,dataclass
from pathlib import Path
import torch
from .experiment_002 import build
from .experiment_004 import paired_query_loss
from .experiment_002 import paired_selective_eval
from .candidates import CandidateConfig
from .state_gated import StateGatedProtectedLanguageModel

VARIANTS=('protected_w32','state_gated_w32','state_gated_random_w32','gru_w32','lstm_w32')

@dataclass(frozen=True)
class Config:
    variants:tuple[str,...]=VARIANTS
    seeds:tuple[int,...]=(17,29,43)
    train_delays:tuple[int,...]=(16,64)
    steps:int=200
    batch_size:int=16
    eval_batch:int=512
    lr:float=.002
    grad_clip:float=1.0
    max_wall_seconds:float=540.0
    def __post_init__(self):
        if not self.variants or len(set(self.variants))!=len(self.variants) or any(x not in VARIANTS for x in self.variants):raise ValueError('invalid variants')
        if not self.seeds or any(type(s) is not int for s in self.seeds):raise ValueError('invalid seeds')
        if not self.train_delays or any(type(d) is not int or d<1 for d in self.train_delays):raise ValueError('invalid delays')
        if any(type(d) is not int or d<1 for d in (self.steps,self.batch_size,self.eval_batch)):raise ValueError('invalid counts')
        if any(not math.isfinite(v) or v<=0 for v in (self.lr,self.grad_clip,self.max_wall_seconds)):raise ValueError('invalid resources')


def make_variant(name,seed):
    if name not in VARIANTS:raise ValueError('invalid variant')
    if name not in ('state_gated_w32','state_gated_random_w32'):
        return build(name,seed)
    opts={} if name=='state_gated_w32' else {'protected_basis':'random_orthogonal'}
    c=CandidateConfig(width=32,vocab_size=16,layers=2,protected_channels=8,
                      cell_type='protected',seed=seed,**opts)
    return StateGatedProtectedLanguageModel(c).cpu()


def execute(config:Config,*,output:Path):
    if output.exists():raise FileExistsError(f'output exists {output}')
    torch.manual_seed(0);torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    start=time.monotonic();report={'status':'running','config':asdict(config),
        'environment':{'torch':torch.__version__,'python':platform.python_version(),'device':'cpu'},
        'runs':[],'skipped':[],'scope':'supervised paired-slot gate mechanism test; NOT formal D'}
    # Interleave delay and variant per seed, and make fair model coverage.
    jobs=[(delay,seed,v) for delay in config.train_delays for seed in config.seeds for v in config.variants]
    try:
        for i,(delay,seed,variant) in enumerate(jobs):
            if time.monotonic()-start>=config.max_wall_seconds:
                report['skipped'].extend([{'delay':d,'seed':s,'variant':v,'reason':'wall_budget'} for d,s,v in jobs[i:]])
                break
            model=make_variant(variant,seed)
            opt=torch.optim.AdamW(model.parameters(),lr=config.lr)
            t0=time.monotonic();done=0;losses=[]
            for step in range(config.steps):
                if time.monotonic()-start>=config.max_wall_seconds:break
                model.train()
                batchseed=seed*1_000_003+step*8191+delay*17+97
                opt.zero_grad(set_to_none=True)
                loss=paired_query_loss(model,delay,config.batch_size,seed=batchseed)
                if not bool(torch.isfinite(loss)):raise FloatingPointError(f'bad loss {variant}/{seed}/{delay}/{step}')
                loss.backward()
                if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
                    raise FloatingPointError(f'bad grad {variant}/{seed}/{delay}/{step}')
                torch.nn.utils.clip_grad_norm_(model.parameters(),config.grad_clip)
                opt.step();done+=1;losses.append(float(loss.detach()))
            evals={str(h):paired_selective_eval(model,h,seed=seed+1_000_000,batch=config.eval_batch)
                   for h in (delay,2*delay,4*delay)}
            state_gates=[]
            for cell in model.cells:
                if hasattr(cell,'state_to_gate'):
                    state_gates.append(float(cell.state_to_gate.weight.detach().norm()))
            row={'train_delay':delay,'seed':seed,'variant':variant,
                 'steps_completed':done,'steps_requested':config.steps,'complete':done==config.steps,
                 'parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
                 'initial_loss':losses[0] if losses else None,'last_loss':losses[-1] if losses else None,
                 'state_gate_weight_l2_by_layer':state_gates if state_gates else None,
                 'evaluation':evals,'elapsed_seconds':time.monotonic()-t0}
            report['runs'].append(row)
            print(json.dumps({'finished':len(report['runs']),'variant':variant,'seed':seed,
                'train_delay':delay,'steps':done,'pair_accuracy':evals[str(delay)]['paired_both_accuracy']}),flush=True)
            if not row['complete']:
                report['skipped'].extend([{'delay':d,'seed':s,'variant':v,'reason':'wall_budget'} for d,s,v in jobs[i+1:]])
                break
        report['status']='complete' if not report['skipped'] and all(x['complete'] for x in report['runs']) else 'budget_limited'
    finally:
        report['elapsed_seconds']=time.monotonic()-start
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--variants',default=','.join(VARIANTS))
    p.add_argument('--seeds',default='17,29,43')
    p.add_argument('--train-delays',default='16,64')
    p.add_argument('--steps',default=200,type=int)
    p.add_argument('--batch',default=16,type=int)
    p.add_argument('--eval-batch',default=512,type=int)
    p.add_argument('--max-wall-seconds',default=540,type=float)
    args=p.parse_args(argv)
    cfg=Config(variants=tuple(args.variants.split(',')),seeds=tuple(map(int,args.seeds.split(','))),
        train_delays=tuple(map(int,args.train_delays.split(','))),steps=args.steps,
        batch_size=args.batch,eval_batch=args.eval_batch,max_wall_seconds=args.max_wall_seconds)
    report=execute(cfg,output=args.output)
    print(f"Experiment 005: {report['status']}; runs={len(report['runs'])}; skipped={len(report['skipped'])}; seconds={report['elapsed_seconds']:.1f}")
if __name__=='__main__':main()
