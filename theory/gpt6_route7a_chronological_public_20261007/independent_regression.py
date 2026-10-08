"""Independent reference-level regression for corrected Route 7A trace-neutral
chronological history. Run beside chronological_probe.py with NumPy.
Checks actual LOCAL sensitivity matrix action on the all-ones vector, not only
the scalar trace formula. Also verifies public gate support and M/M^T pairing.
"""
import json, time
import numpy as np
from chronological_probe import make_history, Mv, Mt

def check(n,m,R,seed=431):
    rng=np.random.default_rng(seed)
    t0=time.time()
    pos=make_history(n,m,R,np.ones((R,m)))
    neg=make_history(n,m,R,-np.ones((R,m)))
    r=n//2-1
    d=n//4
    S=pos['S']
    ones=np.ones(r)
    Lpos=Mv(n,pos['gates'],ones,local=True)
    Lneg=Mv(n,neg['gates'],ones,local=True)
    matrix_trace_error=float(np.max(abs(Lpos-Lneg)))
    non_donor_max=0.
    fixed=np.r_[d+5+2*np.arange(m),d+6+2*np.arange(m)]-1
    for t,(g1,g2) in enumerate(zip(pos['gates'],neg['gates']),start=1):
        moving=np.r_[2*S+np.arange(m)+t,5*S+np.arange(m)+t]
        mask=np.ones(r,dtype=bool)
        mask[np.r_[moving,fixed]]=False
        non_donor_max=max(non_donor_max,float(np.max(abs(g1[mask]-g2[mask]))))
    v=rng.standard_normal(r)
    c=rng.standard_normal(r)
    z1=Mv(n,pos['gates'],v,local=False)
    z2=Mt(n,pos['gates'],c,local=False)
    pairing_error=float(abs(np.dot(z1,c)-np.dot(v,z2))/max(1.,abs(np.dot(z1,c))))
    assert matrix_trace_error<1e-8,(n,m,R,matrix_trace_error)
    assert non_donor_max<1e-12,(n,m,R,non_donor_max)
    assert pairing_error<1e-10,(n,m,R,pairing_error)
    assert np.max(abs(pos['endpoint']-neg['endpoint']))<1e-12
    return dict(n=n,m=m,R=R,matrix_level_local_trace_error=matrix_trace_error,
                max_non_donor_gate_diff=non_donor_max,
                forward_transpose_relative_error=pairing_error,
                elapsed_s=round(time.time()-t0,3))

if __name__=="__main__":
    for n,m,R in [(16384,4,2),(32768,8,4),(65536,32,16)]:
        print(json.dumps(check(n,m,R)),flush=True)
