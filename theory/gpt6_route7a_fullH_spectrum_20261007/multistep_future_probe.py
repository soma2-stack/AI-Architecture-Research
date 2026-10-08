"""Coordinate-wise extreme-vertex ascent for legal future gate words of lengths
1,2,4,8. Local search, not a global supremum, in a structural surrogate.
Requires optimized_query_probe.py in same directory.
"""
import math,json,time,numpy as np
from optimized_query_probe import Model,times,SIGMA

def solve(n=4096,m=8,R=16,lengths=(1,2,4,8),rounds=2):
    model=Model(n);r=model.r;a=model.a
    L=math.ceil(math.sqrt(n*R));xp=np.ones((R,m));xm=-xp
    tsp=times(n,m,R,L,xp);tsm=times(n,m,R,L,xm)
    glo=1/math.cosh(.75)**2;ghi=1/math.cosh(.25)**2
    scalar=SIGMA*math.sqrt(n//2)/n
    def DMT(v,mode):
        z=model.MT(tsp,v,True)-model.MT(tsm,v,True)
        if mode=='H':z-=model.MT(tsp,v,False)-model.MT(tsm,v,False)
        return z
    def DM(v,mode):
        z=model.M(tsp,v,True)-model.M(tsm,v,True)
        if mode=='H':z-=model.M(tsp,v,False)-model.M(tsm,v,False)
        return z
    rng=np.random.default_rng(3)
    out=[]
    for mode in ('M','H'):
      for ell in lengths:
        best=0.
        for seed in range(3):
            gates=[(np.full(r,ghi) if seed==0 else rng.choice([glo,ghi],size=r)).copy() for _ in range(ell)]
            def evaluate():
                c=np.ones(r)/math.sqrt(n)
                suffix=[None]*ell
                for j in range(ell-1,-1,-1):
                    suffix[j]=c.copy()
                    c=a*model.OT(gates[j]*c)
                z=DMT(c,mode)
                return float(scalar*np.linalg.norm(z)),z,suffix
            for _ in range(rounds):
                for j in range(ell):
                    val,z,suffix=evaluate()
                    best=max(best,val)
                    grad=DM(z,mode)
                    for jj in range(j+1):
                        v=a*model.O(grad)
                        if jj==j:
                            gg=v*suffix[j]
                            gates[j]=np.where(gg>=0,ghi,glo)
                        else:
                            grad=v*gates[jj]
            val,_,_=evaluate();best=max(best,val)
        out.append({'R':R,'length':ell,'mode':mode,'best_sampled':best})
    return out

if __name__=='__main__':
    for R,n,m in [(16,4096,8),(64,8192,16)]:
        start=time.time()
        for x in solve(n=n,m=m,R=R,lengths=(1,2,4,8),rounds=2):
            print(json.dumps(x),flush=True)
        print('time',R,round(time.time()-start,2),flush=True)
