"""Executable identity/validation checks; none is a proof of robust dimension."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,math
from pathlib import Path
import numpy as np
from compare import make
from private_echo import endpoint_error
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(33);a=1-1/16384;S=33;B=4
g=rng.uniform(.995,.99999,S);gm=g.copy()
for i in range(4):gm[8*i:8*i+8]=gm[8*i:8*i+8][::-1]
fp=np.cumprod(g[::-1])[::-1]*a**np.arange(S-1,-1,-1)
fm=np.cumprod(gm[::-1])[::-1]*a**np.arange(S-1,-1,-1)
ends=[0,8,16,24,32]
err=float(np.max(abs(fp[ends]-fm[ends])))
assert err<1e-14 and np.min(np.diff(fp))>=0 and np.min(np.diff(fm))>=0
assert np.linalg.norm(fp-fm)**2<=math.ceil(S/B)
public=[]
pa,qa,_,_=make(32768,8,4,16,256,'astra_echo')
for mode in ['astra_weak_echo','gpt_capture','gpt_interior_tied','gpt_interior_independent']:
    p,q,_,_=make(32768,8,4,16,256,mode)
    e=max(endpoint_error(pa,p),endpoint_error(pa,q));assert e<1e-11
    public.append(dict(variant=mode,cross_protocol_endpoint_error=e))
# Algebraic two-common-row receiver formula for heterogeneous boundary gates.
W=16;alpha=a*(1-16384**-2);d=.9974;last=.9976
J=rng.normal(size=(W+2,5));Vin=rng.normal(size=5);V=Vin.copy()
for gate,j in zip(np.r_[d,np.full(W,alpha/a),last],J):V=a*gate*(V+j)
A=a*a*alpha**W*d*last;Q=np.sum(alpha**np.arange(W,-1,-1)[:,None]*J[1:],axis=0)
formula=A*Vin+A*J[0]+a*last*Q
ee=float(np.max(abs(V-formula)));assert ee<1e-12
out=dict(monotone_boundary_code_error=err,local_residual_norm=float(np.linalg.norm(fp-fm)),
    monotone_code_bound=math.sqrt(math.ceil(S/B)),receiver_aggregate_error=ee,
    cross_protocol_common_endpoints=public)
(ROOT/'math_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
