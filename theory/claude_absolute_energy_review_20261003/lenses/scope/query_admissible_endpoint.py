"""Exploratory (numerics cannot prove all-n claims): minimal raw-input energy of a T-step history from h0=0
whose endpoint z=h_T makes the accepted realizable query box reachable, i.e. (R z)_i in (-0.3,1.2) for all i
(future input v in (-1/2,1/2)^n, b0=.05, preactivation in [1/4,3/4]^n). Penalty method + L-BFGS with exact backprop.
Compare with the zero-endpoint minimum ~ b0 sqrt(n)."""
import os; os.environ["OMP_NUM_THREADS"]="4"
import sys, json, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build
b0=0.05; HI, LO = 1.15, -0.25   # margin inside (-0.3,1.2)
def run(n, T, mu=1e4, seed=0):
    M=build(n, dense="checks"); R=M["R"]
    def fg(xflat):
        X=xflat.reshape(T,n); hs=[np.zeros(n)]
        for t in range(T): hs.append(np.tanh(R@hs[-1]+X[t]+b0))
        Rz=R@hs[-1]
        over=np.maximum(Rz-HI,0); under=np.maximum(LO-Rz,0)
        f=np.sum(X*X)+mu*(over@over+under@under)
        gRz=mu*2*(over-under)
        gh=R.T@gRz; gX=2*X.copy()
        for t in range(T-1,-1,-1):
            ga=gh*(1-hs[t+1]**2)
            gX[t]+=ga
            gh=R.T@ga
        return f, gX.ravel()
    rng=np.random.default_rng(seed)
    x0=1e-3*rng.standard_normal(T*n)
    res=minimize(fg, x0, jac=True, method="L-BFGS-B", options=dict(maxiter=20000, maxfun=40000, gtol=1e-10, ftol=1e-15))
    X=res.x.reshape(T,n); h=np.zeros(n)
    for t in range(T): h=np.tanh(R@h+X[t]+b0)
    Rz=R@h
    return dict(n=n,T=T,energy=float(np.linalg.norm(X)),max_Rz=float(Rz.max()),min_Rz=float(Rz.min()),
                admissible=bool(Rz.max()<1.2 and Rz.min()>-0.3), b0_sqrt_n=b0*np.sqrt(n), b0_sqrt_k=b0*np.sqrt(n//2),
                max_abs_input=float(np.abs(X).max()), iters=int(res.nit))
out=[]
for n in (2000, 4000):
    for T in (1,2,4,8,16):
        r=run(n,T); out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open("query_admissible_endpoint.json","w"), indent=1)
