import numpy as np
from scipy.optimize import minimize
from harness import Z0, fourier_projector, phi
from t2_adversary import make, profiles
def vvec(S,tau,delta,n,k,d):
    F=S.shape[0]; ids=np.arange(d); f=np.arange(1,F+1)
    c=delta/F*np.sum(S[:,(ids+tau)%d]*np.cos(2*np.pi*f*tau/d)[:,None],axis=0)
    v=np.zeros(k); v[:d]=phi(c)/np.sqrt(n); return v,c
for kerA in [False,True]:
    for (n,F) in [(200,1),(400,2),(800,4),(1600,4),(1600,8),(3200,8)]:
        if kerA and 2*F+1>(n//4)//4: continue
        k,d,a,w,gam=make(n); perp=fourier_projector(d,F) if kerA else None
        res={}
        for delta in (0.05,0.002):
            def o6(raw):
                v,c=vvec(profiles(raw,F,d,perp),0,delta,n,k,d); return -abs(v.sum())/(delta**2*d/(4*F**2*np.sqrt(n)))
            def o8(raw):
                v,c=vvec(profiles(raw,F,d,perp),0,delta,n,k,d); p=v.copy(); p[0]=0
                return -(abs(p.sum())/np.sqrt(k))/(delta**2/(8*F**2)+4*delta/n)
            rng=np.random.default_rng(1)
            for name,o in (("(6) |sum v|",o6),("(8) beta_p",o8)):
                best=0
                for x0 in [np.tile(rng.normal(size=d),F), rng.normal(size=F*d), np.tile(np.sign(np.cos(2*np.pi*np.arange(d)/d)),F)]:
                    r=minimize(o,x0,method="L-BFGS-B",options=dict(maxiter=80)); best=max(best,-r.fun)
                res[(name,delta)]=best
        print(f"kerA={kerA!s:5s} n={n:5d} F={F}: "+"  ".join(f"{nm} d={dl}: {v:.3f}" for (nm,dl),v in res.items()),flush=True)
