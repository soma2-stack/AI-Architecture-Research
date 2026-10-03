"""Adversarial per-step search over a SUPERSET of section profiles:
s_f with sum 0, ||s||_inf<=1, ||s||_2<=sqrt(d)/(4F) (optionally in ker A).
Fast exact step via the rank-two identity (validated in t1 to 1e-19)."""
import numpy as np, sys
from scipy.optimize import minimize
from harness import Z0, fourier_projector, phi

def make(n):
    k,d=n//2,n//4; a=1-1/n
    w=-np.ones(k)/np.sqrt(k); w[0]+=1; gam=1/(1-1/np.sqrt(k))
    return k,d,a,w,gam

def Pv(v,d):
    out=v.copy(); out[:d]=np.roll(v[:d],1); return out

def step_parts(S,tau,delta,n,k,d,a,w,gam):
    F=S.shape[0]; ids=np.arange(d); f=np.arange(1,F+1)
    def cvec(t):
        return delta/F*np.sum(S[:,(ids+t)%d]*np.cos(2*np.pi*f*t/d)[:,None],axis=0)
    out=[]
    for t in (tau,tau+1):
        c=cvec(t); v=np.zeros(k); v[:d]=phi(c)/np.sqrt(n); p=v.copy(); p[0]=0; out.append(p)
    pn,pp=out
    Ppp=Pv(pp,d); Pw=Pv(w,d)
    Op=Ppp-gam*w*(w@Ppp)-gam*Pw*(w@pp)+gam**2*w*(w@Pw)*(w@pp)
    base=np.full(k,np.sqrt(Z0/n)); base[0]=0
    A1=np.arctanh(base+pn)-np.arctanh(base)-pn
    A2=pn-Ppp; A3=-(Op-Ppp); A4=(1-a)*Op
    dx=A1+A2+A3+A4
    return dx,A1,A2,A3,A4,pn,pp

def profiles(raw,F,d,perp):
    S=[]
    for f in range(F):
        u=raw[f*d:(f+1)*d]
        u=perp@u if perp is not None else u-u.mean()
        nu=np.linalg.norm(u); ni=np.max(np.abs(u))
        if nu==0: S.append(u); continue
        S.append(u*min(np.sqrt(d)/(4*F)/nu,1/ni))
    return np.array(S)

def run(n,F,delta,kerA,objective,seed,iters=60):
    k,d,a,w,gam=make(n)
    perp=fourier_projector(d,F) if kerA else None
    scale=delta/np.sqrt(n)+delta**2/F**2+delta/n
    def obj(raw):
        S=profiles(raw,F,d,perp)
        dx,A1,A2,A3,A4,pn,pp=step_parts(S,0,delta,n,k,d,a,w,gam)
        if objective=="dx": return -np.linalg.norm(dx)/scale
        if objective=="mean": return -abs(pn.sum()+0.0)/(delta**2*d/(4*F**2*np.sqrt(n)))
        if objective=="A3": return -np.linalg.norm(A3)/(7*delta/np.sqrt(n)+delta**2/F**2)
        if objective=="A2": return -np.linalg.norm(A2)/(4*delta/np.sqrt(n)+8*delta/n)
    rng=np.random.default_rng(seed)
    best=None
    starts=[rng.normal(size=F*d)]
    # structured starts: identical profiles with spikes at nodes d-1,0,1
    s=rng.normal(size=d); s[[0,1,d-1]]=10; starts.append(np.tile(s,F))
    s=np.ones(d); s[d//2:]=-1; starts.append(np.tile(s,F))
    for x0 in starts:
        r=minimize(obj,x0,method="L-BFGS-B",options=dict(maxiter=iters))
        if best is None or r.fun<best.fun: best=r
    return -best.fun

if __name__=="__main__":
    for objective in ["dx","mean","A2","A3"]:
        for kerA in [False,True]:
            for (n,F) in [(200,1),(400,2),(800,2),(800,4),(1600,4),(1600,8)]:
                if kerA and 2*F+1>(n//4)//4: continue
                vals=[run(n,F,delta,kerA,objective,s) for delta in (0.05,) for s in (0,)]
                bound={"dx":"16(+mean term coef)","mean":"1","A2":"1","A3":"1"}[objective]
                print(f"{objective:5s} kerA={kerA!s:5s} n={n:5d} F={F}: worst ratio {max(vals):.4f} (analytic cap {bound})",flush=True)
