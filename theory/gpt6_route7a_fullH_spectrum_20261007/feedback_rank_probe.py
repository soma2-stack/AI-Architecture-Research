"""Finite-difference feedback Jacobian under ONE optimized legal one-step query.
Import optimized_query_probe.py in same folder. Structural experiment only.
"""
import math,time,json,argparse,numpy as np
from optimized_query_probe import Model,times,SIGMA

def case(n,m,R,step=.5,seed=2):
    model=Model(n);r=model.r;L=math.ceil(math.sqrt(n*R))
    rng=np.random.default_rng(seed)
    zero=np.zeros((R,m));plus=np.ones((R,m));minus=-plus
    tplus,tminus=[times(n,m,R,L,x) for x in (plus,minus)]
    glo=1/math.cosh(.75)**2;ghi=1/math.cosh(.25)**2
    scale=SIGMA*math.sqrt(n//2)/n
    def diff_MT(c,full):
        return model.MT(tplus,c,full=full)-model.MT(tminus,c,full=full)
    def diff_M(z,full):
        return model.M(tplus,z,full=full)-model.M(tminus,z,full=full)
    best=(0.,None,None)
    for kind in ('M','H'):
        g=np.full(r,ghi)
        for t in range(8):
            c=model.a*model.OT(g)/math.sqrt(n)
            if kind=='M':
                z=diff_MT(c,True); dM=diff_M(z,True)
            else:
                z=diff_MT(c,True)-diff_MT(c,False)
                dM=diff_M(z,True)-diff_M(z,False)
            val=scale*np.linalg.norm(z)
            if kind=='H' and val>best[0]:best=(val,g.copy(),t)
            grad=model.a*model.O(dM)/math.sqrt(n)
            newg=np.where(grad>=0,ghi,glo)
            if np.array_equal(newg,g):break
            g=newg
    val,g,its=best
    assert g is not None
    c=model.a*model.OT(g)/math.sqrt(n)
    columns=[]
    for j in range(R):
        for i in range(m):
            x=np.zeros((R,m));x[j,i]=step
            yp=times(n,m,R,L,x);ym=times(n,m,R,L,-x)
            zp=model.MT(yp,c,full=True)-model.MT(yp,c,full=False)
            zm=model.MT(ym,c,full=True)-model.MT(ym,c,full=False)
            columns.append(scale*(zp-zm)/(2*step))
    J=np.asarray(columns)
    s=np.linalg.svd(J@J.T,compute_uv=False)
    singular=np.sqrt(np.maximum(s,0))
    tol=max(1e-14,singular[0]*1e-7)
    return dict(n=n,m=m,R=R,params=m*R,L=L,N=L+3*R+1,optimized_H_query=val,
                optimized_query_steps=its,linearized_jacobian_l2op=float(singular[0]),
                linearized_jacobian_l2min=float(singular[-1]),
                linearized_jacobian_stable_rank=float((singular**2).sum()/singular[0]**2),
                above_10pct=int((singular>.1*singular[0]).sum()),
                above_1pct=int((singular>.01*singular[0]).sum()),
                numeric_rank_gt_tol=int((singular>tol).sum()),
                singular_head=[float(v) for v in singular[:8]])

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--n',type=int,default=4096)
    ap.add_argument('--m',type=int,default=8)
    ap.add_argument('--rs',default='4,16')
    a=ap.parse_args()
    for R in map(int,a.rs.split(',')):
        t=time.time();out=case(a.n,a.m,R)
        out['runtime_s']=round(time.time()-t,2)
        print(json.dumps(out),flush=True)
