"""(c)/(8) Approximate endpoints, autonomous fixed point endpoint, sharpened all-n bound check."""
import json
from fractions import Fraction as F
import numpy as np
import mpmath as mp
from scipy.optimize import root
from model import build, B0, analytic_box_R0

out = {}
# exact threshold constant
thr = F(200_000_000, 249_001)
out["threshold_exact"] = str(thr)
out["threshold_decimal"] = mp.nstr(mp.mpf(thr.numerator) / thr.denominator, 15)
out["0.0499^2/2 == 249001/2e8"] = (F(499, 10000) ** 2 / 2 == F(249001, 200000000))
mp.mp.dps = 40
out["C_abs"] = mp.nstr(mp.sqrt(2 * (mp.mpf(1) / 400 + (mp.atanh(mp.mpf(2) / 5) - mp.mpf(1) / 20) ** 2)), 25)

# sharpened all-n terminal bound m0(n) - e_n sqrt(n) vs sqrt(n)/20 - 0.721 and vs claimed
ns = np.arange(200, 2_000_001)
k = ns // 2; ell = ns - k; a = 1 - 1 / ns; lam = 1 / (100 * ns); s = np.sqrt(k)
en = 4 / (1e8 * ns ** 2)
mem = np.maximum(0, B0 * (s - 1 / (s - 1)) - a)
m0 = np.sqrt((B0 - lam) ** 2 * ell + mem ** 2)
sharp = m0 - en * np.sqrt(ns)
claimed = (B0 - lam) * np.sqrt(ell) - en * np.sqrt(ns)
target = np.sqrt(ns) / 20 - 0.721
out["min_over_n(sharp - (sqrt(n)/20-0.721))"] = float(np.min(sharp - target))
out["argmin_n"] = int(ns[np.argmin(sharp - target)])
out["sharp_ge_claimed_all_n"] = bool(np.all(sharp >= claimed - 1e-15))
out["first_n_mem_residual_positive"] = int(ns[np.argmax(mem > 0)])
for nn in (200, 800, 1600, 10_000, 1_000_000, 2_000_000):
    i = nn - 200
    out[f"n={nn}"] = dict(sharp=float(sharp[i]), claimed=float(claimed[i]), b0sqrtn=float(np.sqrt(nn) / 20),
                          sharp_minus_b0sqrtn=float(sharp[i] - np.sqrt(nn) / 20),
                          ratio_sharp_claimed=float(sharp[i] / claimed[i]))

# autonomous fixed point endpoint z*: h = tanh(R h + b)
fp = {}
for n in (200, 400, 800, 1600):
    M = build(n)
    R, b, k, d = M["R"], M["b"], M["k"], M["d"]
    h = np.zeros(n)
    for _ in range(200):
        h = np.tanh(R @ h + b)
    sol = root(lambda z: z - np.tanh(R @ z + b), h, jac=lambda z: np.eye(n) - (1 - np.tanh(R @ z + b) ** 2)[:, None] * R,
               method="hybr", tol=1e-14)
    z = sol.x
    resid = np.linalg.norm(z - np.tanh(R @ z + b))
    # terminal cost to land exactly on z from previous state h_prev: ||R(z - h_prev)||
    # zero-input run from 0 for T steps, then one correcting step
    costs = {}
    hh = np.zeros(n)
    for T in range(1, 20 * n + 1):
        if T in (1, 10, n, 5 * n, 20 * n):
            costs[T] = float(np.linalg.norm(R @ (z - hh)))
        hh = np.tanh(R @ hh + b)
    zm, zs = z[:k], z[k:]
    fp[n] = dict(residual=float(resid), mem_max_abs=float(np.max(np.abs(zm))),
                 mem_n_abs_gt_0_9=int(np.sum(np.abs(zm) > 0.9)), mem_mean=float(zm.mean()),
                 mem_rms=float(np.sqrt(np.mean(zm ** 2))),
                 src_mean=float(zs.mean()), tanh_b0=float(np.tanh(B0)),
                 terminal_bound_at_z=float(np.linalg.norm(np.arctanh(zs) - B0) - np.sqrt(len(zs)) / (100 * n)),
                 exact_landing_cost_after_T_free_steps=costs)
    print(n, json.dumps(fp[n]), flush=True)
out["autonomous_fixed_point"] = fp
json.dump(out, open("c_endpoint.json", "w"), indent=1, default=str)
print(json.dumps({k_: v for k_, v in out.items() if k_ != "autonomous_fixed_point"}, indent=1, default=str))
