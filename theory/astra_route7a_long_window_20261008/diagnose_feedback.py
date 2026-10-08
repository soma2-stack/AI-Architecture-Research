"""Actual coupled field decomposition and H-targeted legal-query search."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import json,math
import numpy as np
from long_window import *
ROOT=Path(__file__).resolve().parent

def run():
    out=[]
    for W in [1,16,64]:
        n=16384;m=4;R=2;L=128;r=n//2-1;a=1-1/n
        x=np.random.default_rng(812).choice([-1.,1.],(R,m))
        p=history(n,m,R,W,x,L);neg=history(n,m,R,W,-x,L)
        v=np.zeros(r);v[n//4+4]=1
        fp=projected_feedback(p,v);fm=projected_feedback(neg,v)
        rows=[]
        for stage in range(R):
            t=L+(W+2)*stage;end=t+W+2;alpha=a*p['gh'];tau=p['incoming_traces'][t]
            jp=np.array(fp['J'][t:end]);jm=np.array(fm['J'][t:end])
            vp=np.array(fp['receiver_path'][t-1]);vm=np.array(fm['receiver_path'][t-1])
            kp=np.cumprod((a*p['dgs'][t:end])[::-1],axis=0)[::-1]
            km=np.cumprod((a*neg['dgs'][t:end])[::-1],axis=0)[::-1]
            deltaA=kp[0]-km[0];dlast=p['dgs'][end-1]-neg['dgs'][end-1]
            weights=np.array([sum(alpha**j for j in range(W-u+1)) for u in range(W+1)])
            old=kp[0]*(vp-vm)
            initial=deltaA*(vm-a*tau*jm[0])
            variation=a*dlast*(weights@np.diff(jm))
            coupled=kp.T@(jp-jm)
            actual=np.array(fp['receiver_path'][end-1])-fm['receiver_path'][end-1]
            err=float(np.max(abs(actual-old-initial-variation-coupled)))
            assert err<1e-12
            rows.append(dict(stage=stage,identity_error=err,old_max=float(np.max(abs(old))),
                unmatched_initial_max=float(np.max(abs(initial))),variation_max=float(np.max(abs(variation))),
                actual_delta_field_max=float(np.max(abs(coupled))),actual_delta_receiver_max=float(np.max(abs(actual)))))
        hi=1/math.cosh(.25)**2;lo=1/math.cosh(.75)**2;scale=SIGMA*math.sqrt(n//2)/n
        rng=np.random.default_rng(58);best=0.;bestM=0.
        for start in range(3):
            g=np.full(r,hi) if start==0 else rng.choice([lo,hi],r)
            for it in range(3):
                c=a*op(n,g,True)/math.sqrt(n)
                M=transpose_pair(p,neg,c);H=M-transpose_pair(p,neg,c,True)
                score=float(scale*np.linalg.norm(H))
                if score>best:best=score;bestM=float(scale*np.linalg.norm(M))
                if it<2:
                    zz=forward_pair(p,neg,H)-forward_pair(p,neg,H,True)
                    grad=a*op(n,zz)/math.sqrt(n);g=np.where(grad>=0,hi,lo)
        out.append(dict(n=n,m=m,R=R,W=W,L=L,blocks=rows,best_found_H=best,M_at_H_query=bestM))
    (ROOT/'feedback_diagnostics.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
