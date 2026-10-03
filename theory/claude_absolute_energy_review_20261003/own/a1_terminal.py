import numpy as np, sys
from fractions import Fraction as Q
from scipy.optimize import lsq_linear
from harness import build
b0=0.05
# exact rational constants
worst=Q(1,20)-Q(1,100*200)-2*Q(4,10**8*200**2)
print("b0-lambda-2e_n at n=200:",worst,float(worst),">499/10000:",worst>Q(499,10000))
print("threshold 2e8/249001 =",Q(200000000,249001),float(Q(200000000,249001)))
print("(499/10000)^2/2 =",Q(499,10000)**2/2)
for n in [200,400,800,1600]:
    M=build(n); R=M["R"]; k,l,d=M["k"],M["ell"],M["d"]; gam=M["gam"]; a=M["a"]; eR=M["eR"]
    # exact single-step minimum of ||R h + b0 1|| over the closed cube
    res=lsq_linear(R,-b0*np.ones(n),bounds=(-1,1),method='bvls',tol=1e-14,max_iter=10000)
    single=np.linalg.norm(R@res.x+b0)
    codex=(b0-1/(100*n))*np.sqrt(l)-4/(1e8*n**2)*np.sqrt(n)
    # sharpened analytic bound: source block plus memory direction u = O e_(d-1)
    al_s=(b0-1/(100*n))*np.sqrt(l)
    al_u=b0*np.sqrt(k)-b0*gam/np.sqrt(k)-a
    sharp=np.sqrt(al_s**2+max(al_u,0)**2)-4/(1e8*n**2)*np.sqrt(n)
    # check O^T 1 structure
    OT1=M["O"].T@np.ones(k)
    big=np.argsort(-np.abs(OT1))[:3]
    print(f"n={n}: Codex L_n={codex:.6f}  sharpened={sharp:.6f}  exact single-step min={single:.6f}  b0*sqrt(n)={b0*np.sqrt(n):.6f}"
          f" | O^T1 largest coords {list(big)} vals {np.round(OT1[big],4)} (sqrt k={np.sqrt(k):.4f}, d-1={d-1})"
          f" | saturated coords in minimizer: {int(np.sum(np.abs(res.x)>1-1e-9))}")
