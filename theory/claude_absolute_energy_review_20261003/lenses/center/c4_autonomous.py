"""Autonomous (zero-input) fixed point h* = tanh(R h* + b0 1) of the frozen dense family and the
energy of a history of the SAME length T=N+2 that ends EXACTLY at h*: zero input for T-1 steps,
then x_T = atanh(h*) - R h_(T-1) - b0 1 = R (h* - h_(T-1)).  Also the endpoint-z terminal bound (15)."""
import numpy as np
import sys
sys.path.insert(0, '.')
from c2_dense import build

for n in (200, 400, 1000):
    k, l, d, a, w, U, P, O, R0, R = build(n)
    b = 0.05 * np.ones(n)
    h = np.zeros(n)
    for _ in range(200000):
        hn = np.tanh(R @ h + b)
        if np.max(np.abs(hn - h)) < 1e-16:
            h = hn
            break
        h = hn
    hstar = h
    resid = np.linalg.norm(np.tanh(R @ hstar + b) - hstar)
    N = int(np.ceil(4 * n * np.log(n))) + 1
    T = N + 2
    g = np.zeros(n)
    for _ in range(T - 1):
        g = np.tanh(R @ g + b)
    xT = np.arctanh(hstar) - R @ g - b
    lam, en = 1 / (100 * n), 4e-8 / n**2
    bound15 = np.linalg.norm(np.arctanh(hstar[k:]) - 0.05) - lam * np.sqrt(l) - en * np.sqrt(n)
    print(f"n={n}: ||h*||={np.linalg.norm(hstar):.4f}  h*_source~{hstar[k]:.6f} (tanh(b0)={np.tanh(0.05):.6f})  "
          f"fixed-point residual={resid:.1e}  T={T}  energy of exact-h* history={np.linalg.norm(xT):.3e}  "
          f"terminal bound (15) at z=h*: {bound15:.3e}  (vs h=0 endpoint L_n={(0.05 - lam) * np.sqrt(l) - en * np.sqrt(n):.4f})")
