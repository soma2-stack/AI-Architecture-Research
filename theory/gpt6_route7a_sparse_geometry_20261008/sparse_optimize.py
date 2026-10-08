"""One legal one-step future-query vertex ascent on compressed Route 7A.
Only a sampled lower score; no global future-query optimum certificate.
Requires NumPy and sparse_geometry.py in same folder.
"""
import json,math,time
import numpy as np
from sparse_geometry import sparse_history,sparse_Mt,apply_OT,SIGMA

def apply_O(n,v):
    k=n//2;d=n//4;gamma=1/(1-1/math.sqrt(k))
    cv=gamma/math.sqrt(k);uc=-gamma**2/k
    w=np.zeros_like(v)
    w[1:d-1]=v[:d-2];w[d-1:]=v[d-1:]
    w+=uc*v.sum()+cv*v[d-2];w[0]+=cv*v.sum()
    return w

def sparse_Mv(n,history,v):
    a=1-1/n;w=np.zeros_like(v)
    for bulk,idx,gd in history:
        vv=a*apply_O(n,w)+v
        w=vv*bulk
        w[idx]+=gd*vv[idx]
    return w

def run(n=1048576,m=8,R=4):
    start=time.time();r=n//2-1;a=1-1/n
    pos=sparse_history(n,m,R,np.ones((R,m)))
    neg=sparse_history(n,m,R,-np.ones((R,m)))
    ghi=1/math.cosh(.25)**2;glo=1/math.cosh(.75)**2
    g=np.full(r,ghi);scale=SIGMA*math.sqrt(n//2)/n
    def score(g):
        c=a*apply_OT(n,g)/math.sqrt(n)
        z=sparse_Mt(n,pos['gates'],c)-sparse_Mt(n,neg['gates'],c)
        return float(scale*np.linalg.norm(z)),z
    initial,z=score(g)
    grad=a*apply_O(n,
        sparse_Mv(n,pos['gates'],z)-sparse_Mv(n,neg['gates'],z))/math.sqrt(n)
    vertex=np.where(grad>=0,ghi,glo)
    optimized,_=score(vertex)
    return dict(n=n,m=m,R=R,N=pos['N'],S=pos['S'],
                geometry=pos['valid_strong_geometry'],
                precharge_trace=pos['trace_after_precharge'],
                one_step_all_high=initial,
                after_one_vertex_step=optimized,
                max_found=max(initial,optimized),
                vertex_fraction_high=float(np.mean(vertex==ghi)),
                elapsed_s=round(time.time()-start,2))

if __name__=='__main__':
    print(json.dumps(run()),flush=True)
