import numpy as np
from harness import *
from t2_adversary import make, step_parts, profiles
def total_radius_fast(S,delta,n,N):
    k,d,a,w,gam=make(n)
    sq=np.array([np.sum(step_parts(S,tau,delta,n,k,d,a,w,gam)[0]**2) for tau in range(d)])
    cnt,rem=divmod(N-1,d)
    ps=[]
    for t in (N-1,0):
        F=S.shape[0]; ids=np.arange(d); f=np.arange(1,F+1)
        c=delta/F*np.sum(S[:,(ids+t)%d]*np.cos(2*np.pi*f*t/d)[:,None],axis=0)
        v=np.zeros(k); v[:d]=phi(c)/np.sqrt(n); v[0]=0; ps.append(v)
    base=np.full(k,np.sqrt(Z0/n)); base[0]=0
    first=np.arctanh(base+ps[0])-np.arctanh(base)
    reset=(1-1/n)*np.linalg.norm(ps[1])  # ||R0 p|| = a||p|| (O orthogonal); E negligible
    return np.sqrt(cnt*sq.sum()+sq[:rem].sum()+first@first+reset**2)
rng=np.random.default_rng(7)
for (n,F,q) in [(400,2,4),(800,4,4),(1600,4,6)]:
    M=build(n); d=M["d"]; N=int(np.ceil(4*n*np.log(n)))+1; delta=0.05
    perp=fourier_projector(d,F); B=perp@rng.normal(size=(d,q))/np.sqrt(d)
    scale=np.sqrt(N)*(delta/np.sqrt(n)+delta**2/F**2+delta/n)+delta/F
    def obj(Y):
        Y=Y.reshape(F,q)/np.linalg.norm(Y)
        return total_radius_fast(construction_profiles(d,F,B,Y,perp),delta,n,N)
    # boundary-sphere hill climb, including the "all harmonics aligned" start
    starts=[rng.normal(size=F*q) for _ in range(4)]+[np.tile(rng.normal(size=q),F)]
    best=-1
    for Y in starts:
        cur=obj(Y); step=0.5
        for it in range(150):
            Z=Y+step*rng.normal(size=F*q); val=obj(Z)
            if val>cur: Y,cur=Z,val
            else: step*=0.97
        best=max(best,cur)
    # superset: arbitrary zero-sum profiles with the two norm caps, all harmonics identical (max alignment)
    sup=-1
    for trial in range(6):
        raw=np.tile(rng.normal(size=d),F) if trial%2 else rng.normal(size=F*d)
        if trial>=4: s=np.sign(np.cos(2*np.pi*np.arange(d)/d+rng.uniform(0,6.3))); raw=np.tile(s,F)
        sup=max(sup,total_radius_fast(profiles(raw,F,d,None),delta,n,N))
    print(f"n={n} F={F} q={q} N={N} delta={delta}: section worst R={best:.4e}, superset worst R={sup:.4e}, "
          f"scale sqrt(N)(d/sqrt n+d^2/F^2+d/n)+d/F={scale:.4e}, majorant={majorant(n,F,delta,N):.4e}, worst/majorant={max(best,sup)/majorant(n,F,delta,N):.4f}",flush=True)
