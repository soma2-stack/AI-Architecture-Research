"""Matched comparison additions and finite-difference step sensitivity."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json
from pathlib import Path
import numpy as np
from run_experiments import case,save
from long_window import *
ROOT=Path(__file__).resolve().parent
path=ROOT/'scaling_results.json'
out=json.loads(path.read_text()) if path.exists() else dict(cases=[],finite_difference=[])
for n,m,R in [(65536,8,4),(32768,16,4),(65536,16,4)]:
    for W in [1,64]:
        if any((x['n'],x['m'],x['R'],x['W'])==(n,m,R,W) for x in out['cases']):continue
        x=case(n,m,R,W,256);out['cases'].append(x);save(path,out)
        print(n,m,R,W,max(q['best_M'] for q in x['queries']),flush=True)
if not out['finite_difference']:
    n=16384;m=4;R=2;W=64;L=128;r=n//2-1
    rng=np.random.default_rng(4);hi=1/math.cosh(.25)**2;lo=1/math.cosh(.75)**2
    c=(1-1/n)*op(n,rng.choice([lo,hi],r),True)/math.sqrt(n)
    scale=SIGMA*math.sqrt(n//2)/n
    previous=None
    for h in [.02,.01,.005]:
        ctrl=np.zeros((R,m));ctrl[0,0]=h
        p=history(n,m,R,W,ctrl,L);neg=history(n,m,R,W,-ctrl,L)
        M=scale*transpose_pair(p,neg,c)/(2*h)
        H=M-scale*transpose_pair(p,neg,c,True)/(2*h)
        out['finite_difference'].append(dict(step=h,H_norm=float(np.linalg.norm(H)),
            relative_change_from_previous=None if previous is None else float(np.linalg.norm(H-previous)/np.linalg.norm(H))))
        previous=H
    save(path,out)
