"""Multi-start legal one-step future query search on corrected chronological
Route 7A reference histories. Run beside chronological_probe.py.
Finite and local-search only: no claim of global query optimum or legal
asymptotic corridor width.
"""
import math,json,time
import numpy as np
from chronological_probe import make_history,Mt,Mv,o_apply,SIGMA

def probe(n,m,R,starts=5,iters=4,seed=17):
    rng=np.random.default_rng(seed);r=n//2-1;a=1-1/n
    p=make_history(n,m,R,np.ones((R,m)))
    q=make_history(n,m,R,-np.ones((R,m)))
    ghi=1/math.cosh(.25)**2;glo=1/math.cosh(.75)**2
    scale=SIGMA*math.sqrt(n//2)/n
    def dMT(c,mode):
        z=Mt(n,p['gates'],c)-Mt(n,q['gates'],c)
        if mode=='H':
            z-=Mt(n,p['gates'],c,True)-Mt(n,q['gates'],c,True)
        return z
    def dM(z,mode):
        v=Mv(n,p['gates'],z)-Mv(n,q['gates'],z)
        if mode=='H':
            v-=Mv(n,p['gates'],z,True)-Mv(n,q['gates'],z,True)
        return v
    result={}
    for mode in ('M','H'):
        best=0.;seed_scores=[]
        for s in range(starts):
            if s==0:g=np.full(r,ghi)
            elif s==1:g=np.full(r,glo)
            else:g=rng.choice([glo,ghi],size=r)
            local_best=0.
            for j in range(iters+1):
                c=a*o_apply(n,g,transpose=True)/math.sqrt(n)
                z=dMT(c,mode);val=scale*np.linalg.norm(z)
                best=max(best,float(val));local_best=max(local_best,float(val))
                if j==iters:break
                grad=a*o_apply(n,dM(z,mode))/math.sqrt(n)
                ng=np.where(grad>=0,ghi,glo)
                if np.array_equal(ng,g):break
                g=ng
            seed_scores.append(local_best)
        result[mode]=dict(best=best,per_seed=seed_scores)
    return dict(n=n,m=m,R=R,starts=starts,iters=iters,results=result)

if __name__=='__main__':
    for n,m,R in [(32768,8,4),(65536,32,16)]:
        t=time.time();z=probe(n,m,R,starts=5,iters=4)
        z['seconds']=round(time.time()-t,2)
        print(json.dumps(z),flush=True)
