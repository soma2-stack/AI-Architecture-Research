"""Stacking multiple legal one-step adjoints is diagnostic ONLY; it is not
one legal query and is NOT a robust-separation certificate.
"""
import numpy as np,math,json,time
from optimized_query_probe import Model,times,SIGMA

def run(n=4096,m=4,R=16,queries=5):
    model=Model(n);r=model.r;L=math.ceil(math.sqrt(n*R))
    zero=np.zeros((R,m))
    glo=1/math.cosh(.75)**2;ghi=1/math.cosh(.25)**2
    rng=np.random.default_rng(19)
    gates=[np.full(r,ghi),np.full(r,glo),
           np.where(np.arange(r)%2,ghi,glo)]
    gates.extend(rng.choice([glo,ghi],size=r) for _ in range(max(0,queries-3)))
    qs=[model.a*model.OT(g)/math.sqrt(n) for g in gates[:queries]]
    A=[]
    for j in range(R):
        for i in range(m):
            x=zero.copy();x[j,i]=.5
            tp=times(n,m,R,L,x);tm=times(n,m,R,L,-x)
            rows=[]
            for c in qs:
                hp=model.MT(tp,c,True)-model.MT(tp,c,False)
                hm=model.MT(tm,c,True)-model.MT(tm,c,False)
                rows.append(SIGMA*math.sqrt(n//2)/n*(hp-hm))
            A.append(np.concatenate(rows))
    J=np.asarray(A)
    sv=np.sqrt(np.maximum(np.linalg.svd(J@J.T,compute_uv=False),0))/math.sqrt(queries)
    return {'n':n,'m':m,'R':R,'queries':queries,
            'stacked_stable_rank':float((sv**2).sum()/sv[0]**2),
            'above_10pct':int((sv>.1*sv[0]).sum()),
            'top':float(sv[0]),'tail':float(sv[-1])}

if __name__=='__main__':
    for q in [1,2,3,5]:
        t=time.time();x=run(queries=q);x['sec']=round(time.time()-t,2)
        print(json.dumps(x),flush=True)
