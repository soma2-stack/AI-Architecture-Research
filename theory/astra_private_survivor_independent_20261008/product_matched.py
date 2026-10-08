"""Post-comparison falsifier: opposite interior words with equal gate products.
Independent invention after checkpoint; uses explicitly matched GPT-6 gate engine.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,time
from pathlib import Path
import numpy as np
from compare import gpt
from private_echo import query_probe,endpoint_error
ROOT=Path(__file__).resolve().parent
p=ROOT/'product_matched_results.json';out=json.loads(p.read_text()) if p.exists() else []
for n,m,R,W,L in [(16384,4,2,16,128),(32768,8,4,16,256),(32768,8,4,64,256),(65536,16,8,16,256)]:
    if any((x['n'],x['m'],x['R'],x['W'])==(n,m,R,W) for x in out):continue
    rng=np.random.default_rng(812);h=(W-1)//2;u=rng.choice([-1.,1.],(R,m,h))
    z=np.concatenate([u,np.zeros((R,m,1)),-u[:,:,::-1]],axis=2)
    gh=1-n**-2;gp=gh-1e-4*(1+z)/2;gm=gh-1e-4*(1-z)/2
    prod_error=float(np.max(abs(np.prod(gp,axis=2)-np.prod(gm,axis=2))))
    assert prod_error<1e-13
    p1=gpt.history(n,m,R,W,np.zeros((R,m)),L,hold_survivors=True,private_interior=z)
    p2=gpt.history(n,m,R,W,np.zeros((R,m)),L,hold_survivors=True,private_interior=-z)
    assert endpoint_error(p1,p2)<1e-10
    qs=[query_probe(p1,p2,t,2,1)[0] for t in [1,2,4,8]]
    row=dict(n=n,m=m,R=R,W=W,L=L,N=p1['N'],controls=m*R*h,product_error=prod_error,
        endpoint_error=endpoint_error(p1,p2),queries=qs)
    out.append(row);p.write_text(json.dumps(out,indent=2,allow_nan=False))
    print(n,m,R,W,max(q['best_M'] for q in qs),flush=True)
