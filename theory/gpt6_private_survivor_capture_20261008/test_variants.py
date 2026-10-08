"""Reproduce private capture versus private interior controls; frozen reference model.
Uses Astra's chronological forward tanh and exact rank-two full sensitivity.
All-high legal one-step queries only; not global maxima or robust-width proofs.
"""
import math,json,time
import numpy as np
from private_survivor_variant import history,endpoint_error,transpose_pair,op,SIGMA

def measure(n,m,R,W,L,interior=False,seed=84,query=True):
    rng=np.random.default_rng(seed);z=np.zeros((R,m))
    if interior:
        y=rng.choice([-1.,1.],size=(R,m,W-1))
        kw=lambda x: dict(private_interior=x,hold_survivors=True)
    else:
        y=rng.choice([-1.,1.],size=(R,m))
        kw=lambda x: dict(private_capture=x,hold_survivors=True)
    t=time.time()
    p=history(n,m,R,W,z,L=L,**kw(y))
    q=history(n,m,R,W,z,L=L,**kw(-y))
    end=endpoint_error(p,q)
    assert end<1e-11
    assert max(p["maxtrace"],q["maxtrace"])<1e-8
    out=dict(n=n,m=m,R=R,W=W,L=L,N=p["N"],private_controls=y.size,
             variant="interior" if interior else "capture",
             strong_geometry=p["strong_geometry"],endpoint_error=end,
             max_trace_error=max(p["maxtrace"],q["maxtrace"]),
             max_input=max(p["maxinput"],q["maxinput"]))
    if query:
        a=1-1/n
        g=np.full(n//2-1,1/math.cosh(.25)**2)
        c=a*op(n,g,True)/math.sqrt(n)
        M=transpose_pair(p,q,c)
        Lloc=transpose_pair(p,q,c,True)
        scale=SIGMA*math.sqrt(n//2)/n
        out.update(M=float(scale*np.linalg.norm(M)),
                   L=float(scale*np.linalg.norm(Lloc)),
                   H=float(scale*np.linalg.norm(M-Lloc)))
    out["seconds"]=round(time.time()-t,2)
    return out

if __name__=="__main__":
    for case in [(16384,4,2,8,128),(32768,8,4,16,256),(32768,8,4,64,256)]:
        for interior in (False,True):
            print(json.dumps(measure(*case,interior=interior)),flush=True)
    for interior in (False,True):
        # Run only state/trace/geometry check on the million-width case;
        # optimized large-width queries require more time.
        print(json.dumps(measure(1048576,8,4,16,2048,interior=interior,query=False)),flush=True)
