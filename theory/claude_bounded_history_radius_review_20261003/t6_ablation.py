import numpy as np
from harness import *
def radius_variant(M,S,delta,N,direction=+1,signs=None):
    n,k,d,F=M["n"],M["k"],M["d"],S.shape[0]; R=M["R"]; base=M["base"].copy()
    if signs is not None: base[1:d]*=signs[1:d]
    def p_at(t):
        tau=N-t; ids=np.arange(d); f=np.arange(1,F+1)
        c=delta/F*np.sum(S[:,(direction*ids+tau)%d]*np.cos(2*np.pi*f*tau/d)[:,None],axis=0)
        h=base.copy(); sg=np.ones(d) if signs is None else signs
        h[1:d]=sg[1:d]*np.sqrt((Z0-c[1:d])/n); return h-base
    tot=0; prev=np.zeros(n)
    for t in range(1,N+1):
        dh=p_at(t)
        dx=np.arctanh(base+dh)-np.arctanh(base)-(R@prev if t>1 else 0)
        tot+=dx@dx; prev=dh
    dx=-R@prev; tot+=dx@dx
    return np.sqrt(tot)
rng=np.random.default_rng(3)
for (n,F) in [(400,2),(800,4)]:
    M=build(n); d=M["d"]; N=int(np.ceil(4*n*np.log(n)))+1; delta=0.05
    perp=fourier_projector(d,F); B=perp@rng.normal(size=(d,4))/np.sqrt(d)
    Y=rng.normal(size=(F,4)); Y/=np.linalg.norm(Y); S=construction_profiles(d,F,B,Y,perp)
    alt=np.where(np.arange(d)%2==0,1.0,-1.0)
    r_co=radius_variant(M,S,delta,N,+1); r_anti=radius_variant(M,S,delta,N,-1); r_alt=radius_variant(M,S,delta,N,+1,alt)
    print(f"n={n} F={F}: co-moving (as proved) R={r_co:.4e} | reversed drift R={r_anti:.4e} ({r_anti/r_co:.0f}x) | alternating signs R={r_alt:.4e} ({r_alt/r_co:.0f}x) | majorant {majorant(n,F,delta,N):.3e}")
