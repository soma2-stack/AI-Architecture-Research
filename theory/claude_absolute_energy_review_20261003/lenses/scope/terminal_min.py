"""Hostile check of PROOF.md (8): min over |h|<=1 of ||R h + b0 1|| for the ACTUAL frozen R
(archived construction) vs L_n=(b0-lam)sqrt(l)-e_n sqrt(n), plus a sharper source+memory bound.
Relaxation over the closed cube is a SUPERSET of reachable h_{T-1}, so min_cube >= L_n is necessary
for (8) to hold; min_cube < L_n would refute it."""
import os
os.environ["OMP_NUM_THREADS"]="4"
import sys, json, numpy as np
from scipy.optimize import lsq_linear
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build
b0=0.05
out=[]
for n in (200, 256, 400, 1000, 2000):
    M=build(n, dense="checks")
    R, R0, k, l = M["R"], M["R0"], M["k"], M["ell"]
    lam=1/(100*n); en=4/(1e8*n*n)
    res=lsq_linear(R, -b0*np.ones(n), bounds=(-1,1), method="bvls", tol=1e-14, max_iter=20000)
    h=res.x; val=np.linalg.norm(R@h+b0)
    src=np.linalg.norm((R@h+b0)[k:]); mem=np.linalg.norm((R@h+b0)[:k])
    Ln=(b0-lam)*np.sqrt(l)-en*np.sqrt(n)
    # analytic reference memory minimum: ||(|b0 O^T 1| - a)_+||
    O=M["O"]; a=M["a"]
    g=np.abs(b0*(O.T@np.ones(k)))
    memref=np.linalg.norm(np.maximum(g-a,0))
    sharp=np.sqrt(((b0-lam)*np.sqrt(l))**2+memref**2)-en*np.sqrt(n)
    row=dict(n=n, eR=float(M["eR"]), en=en, min_cube=float(val), min_src_block=float(src), min_mem_block=float(mem),
             L_n=float(Ln), bound_0499=0.0499*np.sqrt(n/2), memref=float(memref), sharp_bound=float(sharp),
             ratio_min_over_Ln=float(val/Ln), b0_sqrt_n=b0*np.sqrt(n), maxabs_OT1_times_b0=float(g.max()))
    out.append(row); print(json.dumps(row))
json.dump(out, open("terminal_min.json","w"), indent=1)
