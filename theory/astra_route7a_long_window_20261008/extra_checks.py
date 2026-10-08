"""Independent kernel checks, finite public-premise certificate, held-bank variant."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,math,time
from pathlib import Path
import numpy as np
from long_window import *
ROOT=Path(__file__).resolve().parent

def public_certificate(n,m,N):
    # Deterministic worst-case support bound, not inferred from sampled histories.
    a=1-1/n;k=n//2;r=k-1;ga=1/(1-1/math.sqrt(k));cv=ga/math.sqrt(k);c=ga*ga/k
    Dmax=2*(N+6*m);err=(ga-1)+c*Dmax
    lo=math.tanh(.05-err);hi=math.tanh(.05+err)
    front_raw=.05+a*((cv*r-ga)*lo-(cv-c)*Dmax)
    fbound=4*math.exp(-2*front_raw) if front_raw>0 else 1.
    return dict(state_argument_error=err,bath_lower=lo,bath_upper=hi,
        bath_gate_bound=1-lo*lo if lo>0 else 1.,first_front_gate_bound=fbound,
        certified=bool(err<=.02 and fbound<=1/n and m<=n/16))

def kernels():
    rng=np.random.default_rng(11);out=[]
    for W in [1,4,8,16,32,64,256]:
        a=1-1/1048576;gh=1-1048576**-2;alpha=a*gh;tau=2040.;d=GSTAR+EPS
        TW=gh*sum(alpha**j for j in range(W));AW=1+a*TW;BW=a*alpha**W*(1+a*tau)
        last=GSTAR*(AW+BW*GSTAR)/(AW+BW*d)
        gp=np.r_[d,np.full(W,gh),last];gm=np.r_[GSTAR,np.full(W,gh),GSTAR]
        kp=np.cumprod((a*gp)[::-1])[::-1];km=np.cumprod((a*gm)[::-1])[::-1];dk=kp-km
        J=rng.normal(size=W+2);Vin=17.
        direct=dk[0]*Vin+dk@J
        G=np.array([sum(alpha**j for j in range(W-u+1)) for u in range(W+1)])
        centered=dk[0]*(Vin-a*tau*J[0])+a*(last-GSTAR)*(G@np.diff(J))
        error=abs(direct-centered);assert error<1e-9
        out.append(dict(W=W,Abel_identity_error=error,
            bounded_input_exact_gain=float(abs(dk[0])*a*tau+np.sum(abs(dk))),
            gain_bound=float(2*a*GSTAR/(GSTAR-EPS)*EPS*sum(alpha**j for j in range(W+1))),
            contraction=float(kp[0])))
    return out

def run():
    out=dict(kernels=kernels(),held_bank_cases=[])
    for W in [1,16,64]:
        n=32768;m=8;R=4;L=256;ctrl=np.random.default_rng(812).choice([-1.,1.],(R,m))
        p=history(n,m,R,W,ctrl,L,hold_survivors=True);neg=history(n,m,R,W,-ctrl,L,hold_survivors=True)
        assert endpoint_error(p,neg)<1e-11
        qs=[]
        for horizon in [1,4]:
            q,_=query_probe(p,neg,horizon,3,2);qs.append(q)
        out['held_bank_cases'].append(dict(n=n,m=m,R=R,W=W,L=L,N=p['N'],queries=qs,
            endpoint_error=endpoint_error(p,neg),maxtrace=p['maxtrace'],maxinput=p['maxinput']))
    out['public_certificates']=[dict(n=n,m=m,N=N,**public_certificate(n,m,N))
        for n,m,N in [(1048576,8,2048+4*(W+2)+1) for W in [1,16,64]]]
    (ROOT/'extra_results.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
