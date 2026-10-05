"""Validate: forward/adjoint consistency, and ||B_T||op == sqrt(l)||M_T||op by brute-force
full-K-block sensitivity (recursion (1) of PROOF) at tiny width (algebra check only)."""
import numpy as np, math
from model import Model
from sim import Sim
n=40; M=Model(n); Rd,_=M.dense_R(); k,l,r=M.k,M.l,M.r
h=M.fixed_point(); 
rng=np.random.default_rng(3)
X=rng.normal(size=(61,n))*0.3; X[:,k:]=X[:,[k]]   # uniform source inputs
pol=lambda t,hh,pre: X[t]
T=60
S=Sim(M,h,pol,T,ckpt=7)
# brute force B_T on vec(K), K in R^{r x l}
B=np.zeros((n,r*l)); hh=np.zeros(n)
for t in range(1,T+1):
    hs=hh[k:].copy()
    hh=np.tanh(Rd@hh+0.05+X[t])
    Inj=np.zeros((n,r*l))
    for i in range(r):
        Inj[1+i,i*l:(i+1)*l]=hs
    B=(1-hh**2)[:,None]*(Rd@B+Inj)
print("state match", np.abs(hh-S.hT).max())
nB=np.linalg.norm(B,2)
# dense M_T
Mm=S.forward(np.eye(k-1)).T   # n x (k-1)
print("||B_T||op brute", nB, " sqrt(l)||M_T||", math.sqrt(l)*np.linalg.norm(Mm,2))
Y=rng.normal(size=(2,n)); V=rng.normal(size=(2,k-1))
print("adjoint consistency", np.abs(Y@S.forward(V).T - S.adjoint(Y)@V.T).max())
top,hist=S.opnorm(iters=50,block=3)
print("power iteration", top, "dense", np.linalg.norm(Mm,2), "upper", S.upper_M)
