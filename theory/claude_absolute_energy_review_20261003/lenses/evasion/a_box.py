"""(a) Single final step: min_{h in [-1,1]^n} ||R h + b0 1_n||_2 for the actual dense R."""
import json, time
import numpy as np
from scipy.optimize import lsq_linear
from model import build, claimed_bound, analytic_box_R0, B0

out = []
for n in (200, 400, 800, 1600, 3200):
    t0 = time.time()
    M = build(n)
    R, R0, b = M["R"], M["R0"], M["b"]
    k = M["k"]
    # structural checks
    O = M["O"]
    ones = np.ones(k)
    c = O.T @ ones
    res = lsq_linear(R, -b, bounds=(-1, 1), method="bvls", tol=1e-14, lsmr_tol=None)
    h = res.x
    val = np.linalg.norm(R @ h + b)
    res0 = lsq_linear(R0, -b, bounds=(-1, 1), method="bvls", tol=1e-14)
    val0 = np.linalg.norm(R0 @ res0.x + b)
    an, an_mem, an_src = analytic_box_R0(n)
    row = dict(n=n, eR=M["eR"], en=M["en"], eR_le_en=bool(M["eR"] <= M["en"]),
               one_T_O_one=float(ones @ O @ ones),
               c_max_index=int(np.argmax(np.abs(c))), d_minus_1=M["d"] - 1,
               c_max=float(np.max(np.abs(c))), c_pred=float(np.sqrt(k) - 1 / (np.sqrt(k) - 1)),
               box_min_R=val, box_min_R0=val0, analytic_box_R0=an,
               analytic_mem=an_mem, analytic_src=an_src,
               claimed_Ln=claimed_bound(n), b0_sqrt_n=B0 * np.sqrt(n),
               ratio_box_to_claimed=val / claimed_bound(n),
               ratio_box_to_b0sqrtn=val / (B0 * np.sqrt(n)),
               n_saturated=int(np.sum(np.abs(h) > 1 - 1e-9)),
               secs=time.time() - t0)
    out.append(row)
    print(json.dumps(row))
json.dump(out, open("a_box.json", "w"), indent=1)
