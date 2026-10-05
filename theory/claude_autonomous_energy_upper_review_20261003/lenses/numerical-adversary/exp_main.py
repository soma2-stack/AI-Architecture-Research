"""Main adversarial-history table for one width n.  usage: python3 exp_main.py n [power_max_n]
All histories start at h_0=0; every input (burn-in, holds, landing correction) is counted.
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from model import Model
from sim import Sim, GLO, GHI, credit_from_M

n = int(sys.argv[1])
POWER_MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 16000
t_start = time.time()
M = Model(n)
hs = M.fixed_point()
hs = M.polish(hs, 50)
k, d, l = M.k, M.d, M.l
ath = np.arctanh(hs)
out = dict(n=n, Bstar=M.Bstar, H=M.Hstar, min_h=float(hs.min()), sigma_star=float(hs[k]),
           ceiling=float(M.a * math.sqrt(l) * hs[k]), rows=[])


def land(pre):
    return ath - pre      # dense exact landing: next state is h* exactly


def baseline(B0):
    def pol(t, h, pre):
        if t == B0 + 1:
            return land(pre)
        return None
    return pol


def offhole(i, Th, t0=1):
    def pol(t, h, pre):
        if t0 <= t < t0 + Th:
            return (np.array([i]), np.array([-pre[i]]))
        if t == t0 + Th:
            return land(pre)
        return None
    return pol


def cyclehole(Th, jend):
    # hole at j(t)=jend-(Th-t), t=1..Th, then landing at Th+1
    def pol(t, h, pre):
        if 1 <= t <= Th:
            j = jend - (Th - t)
            return (np.array([j]), np.array([-pre[j]]))
        if t == Th + 1:
            return land(pre)
        return None
    return pol


def evaluate(name, pol, T, probe_idx, do_power, queries=True, extra=None, path=None):
    t0 = time.time()
    S = Sim(M, hs, pol, T, ckpt=400)
    row = dict(name=name, T=T, energy=S.energy, R_needed=math.sqrt(S.energy),
               end_err=float(np.linalg.norm(S.hT - hs)), src_spread=S.src_spread,
               upper_M=S.upper_M, credit_upper=credit_from_M(M, S.upper_M))
    # bad steps in the theorem's sense (deviation > m/2 = 0.01), and steps with min|h|<0.01
    row["steps_dev_gt_0.01"] = int((S.dev[1:] > 0.01).sum())
    if extra:
        row.update(extra)
    # probe lower bound
    V = np.zeros((len(probe_idx) + (path is not None), k - 1))
    for r_, i in enumerate(probe_idx):
        V[r_, i - 1] = 1.0
    if path is not None:
        V[-1, path[0] - 1:path[1]] = 1.0 / math.sqrt(path[1] - path[0] + 1)
    Z = S.forward(V)
    norms = np.linalg.norm(Z, axis=1)
    row["probe_idx"] = [int(i) for i in probe_idx]
    row["probe_norms"] = norms.tolist()
    sv = np.linalg.svd(Z, compute_uv=False)[0]
    row["lower_M"] = float(sv)
    row["credit_lower"] = credit_from_M(M, sv)
    if do_power:
        v0 = V[int(np.argmax(norms))]
        top, hist = S.opnorm(v0=v0, iters=12, tol=1e-6, block=2)
        row["power_M"] = top
        row["power_hist"] = hist
        row["credit_exact"] = credit_from_M(M, top)
    if queries:
        qs = {}
        ones = np.ones(n)
        gates_sets = {
            "L1_allGHI": [GHI * ones],
            "L2_allGHI": [GHI * ones, GHI * ones],
            "L3_allGHI": [GHI * ones, GHI * ones, GHI * ones],
        }
        for pi in probe_idx[:1]:
            g = GLO * ones.copy(); g[pi] = GHI
            gates_sets[f"L1_spike{pi}"] = [g]
        keys = list(gates_sets)
        Y = np.stack([S.query_adjoint(gates_sets[kk]) for kk in keys])
        Wq = S.adjoint(Y)
        for kk, w in zip(keys, Wq):
            qs[kk] = math.sqrt(M.l) / M.n * float(np.linalg.norm(w))
        # theorem-side cap for each query: (1/n)*||xi*beta||*sqrt(l)*||M||  <= (a/n)sqrt(l)||M||
        row["query_adjoint_norms"] = [float(np.linalg.norm(y)) for y in Y]
        row["query_credit"] = qs
    row["secs"] = time.time() - t0
    out["rows"].append(row)
    print(json.dumps({kk: (vv if not isinstance(vv, list) or len(vv) < 8 else vv[-3:]) for kk, vv in row.items()}), flush=True)
    return S, row


power = n <= POWER_MAX
ONLY = os.environ.get('ONLY', 'ABCD')
ioff = d + (k - d) // 2          # an off-cycle selected coordinate
# A. baseline: zero burn-in then exact landing
B0 = 20000
if 'A' in ONLY: evaluate("baseline_B0=20000", baseline(B0), B0 + 1, [ioff, d - 1, d - 2], power)
# B. off-cycle hole from t=1 held Th=2n (saturating), then land
if 'B' in ONLY: evaluate("offhole_Th=2n", offhole(ioff, 2 * n), 2 * n + 1, [ioff, d - 1], power and n <= 8000,
         extra=dict(Th=2 * n))
# C. off-cycle hole with FIXED short hold (energy-limited emulation)
for Th in ((500, 2000, 8000) if 'C' in ONLY else ()):
    evaluate(f"offhole_Th={Th}", offhole(ioff, Th), Th + 1, [ioff, d - 1], power and n <= 8000,
             queries=(Th == 2000), extra=dict(Th=Th))
# D. co-moving cycle hole ending at d-2, landing makes it read by L=1 uniform head at d-1
Thc = d - 3
if 'D' in ONLY: evaluate("cyclehole_fullpass", cyclehole(Thc, d - 2), Thc + 1, [d - 1, d - 2, ioff], power,
         extra=dict(Th=Thc), path=(d - 2 - Thc + 1, d - 2))
Thc2 = min(2000, d - 3)
if 'D' in ONLY: evaluate("cyclehole_Th=2000", cyclehole(Thc2, d - 2), Thc2 + 1, [d - 1, d - 2, ioff], power,
         extra=dict(Th=Thc2), path=(d - 2 - Thc2 + 1, d - 2))
out["secs"] = time.time() - t_start
json.dump(out, open(f"main_n{n}_{ONLY}.json", "w"), indent=1)
print("done", n, out["secs"])
