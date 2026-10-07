"""Adaptive search (NOT proof): the Fan points sit near Voronoi vertices (measure ~0),
so uniform sampling misses them. Hill-climb ||f||_1^2/||f||_2^2 on the sphere."""
import numpy as np, sys
rng=np.random.default_rng(1)
def sphere(n,D):
    x=rng.standard_normal((n,D)); return x/np.linalg.norm(x,axis=1,keepdims=True)
def ratio(Y): return (np.abs(Y).sum(-1)**2)/(np.square(Y).sum(-1))
def sparse_net_map(D,N,temp):
    A=sphere(N,D)
    def f(T):
        P=T@A.T; W=np.exp((np.abs(P)-np.abs(P).max(-1,keepdims=True))/temp)
        return np.sign(P)*W*np.abs(P)
    return f
for D in [5,6,8]:
    f=sparse_net_map(D,600,0.002)
    S=sphere(20000,D); r=ratio(f(S)); idx=np.argsort(r)[-200:]
    best=0
    for i in idx:
        x=S[i]; rx=ratio(f(x[None]))[0]; step=0.05
        for it in range(3000):
            y=x+step*rng.standard_normal(D); y/=np.linalg.norm(y)
            ry=ratio(f(y[None]))[0]
            if ry>rx: x,rx=y,ry
            else: step*=0.995
            if step<1e-7: break
        best=max(best,rx)
    print(f"D={D}: adaptive max ratio = {best:.4f}  (lemma predicts >= {D}): pass={best>=D*0.999}")
