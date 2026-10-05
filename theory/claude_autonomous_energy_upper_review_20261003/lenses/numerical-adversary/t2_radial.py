"""Spot-check PROOF eq (17) (global radial contraction about h*) on adversarial steps at n=4000,
where min h* = 0.0237 >= m=1/50 so Lemma 2's hypothesis already holds."""
import numpy as np, math
from model import Model
n=4000; M=Model(n); hs=M.polish(M.fixed_point(),20); k=M.k
kappa=10000/10001
rng=np.random.default_rng(7); worst=0; worst_tight=0
for trial in range(3000):
    kind=trial%4
    if kind==0: h=np.tanh(rng.normal(size=n)*rng.choice([0.01,0.3,3]))
    elif kind==1: h=hs.copy(); idx=rng.choice(n,size=rng.integers(1,50),replace=False); h[idx]=rng.uniform(-1,1,size=len(idx))*0.999
    elif kind==2: h=hs+rng.normal(size=n)*1e-4
    else: h=hs.copy(); h[d:=rng.integers(M.d,k)]=0.0
    x=rng.normal(size=n)*rng.choice([0,1e-6,1e-2,1]) if kind!=3 else np.zeros(n)
    if kind==3: x[d]=-(M.R(h)+0.05)[d]
    hn=np.tanh(M.R(h)+x+0.05)
    lhs=np.linalg.norm(hn-hs); rhs=np.linalg.norm(M.R(h-hs)+x)
    if rhs>0:
        worst=max(worst,lhs/rhs)
print("max ||h_t-h*||/||R(h_{t-1}-h*)+x_t|| =",worst," kappa=",kappa, "OK" if worst<=kappa else "VIOLATION")
# coordinatewise secant at the actual h*: the TRUE contraction for a hole is 1/(atanh(H)/H)
H=M.Hstar; print("actual hole secant factor H/atanh(H) =",H/math.atanh(H), " vs kappa",kappa)
