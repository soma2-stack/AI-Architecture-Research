"""Full-model random / structured search at n=4000 at MATCHED total energy (incl. landing).
Reference = ramped off-cycle hole. Competitors: random sparse pulse trains, rotating (resonant,
P-aligned) cycle patterns, uniform off-cycle bias shift, random dense noise.  Score = sup credit
via block power iteration (lower bound on (a/n)sqrt(l)||M_T||) + analytic upper; legal L1 query.
"""
import os, sys, json, math, time
import numpy as np
from model import Model
from sim import Sim, GLO, GHI, credit_from_M

n = 4000
M = Model(n); hs = M.polish(M.fixed_point(), 20); k, d, l = M.k, M.d, M.l
i0 = d + (k - d) // 2
H, Bs = hs[i0], M.Bstar
B0, Th, Nup = 6000, 4000, 100
Nr = int(round(H / Bs))
W = Th + Nr + Nup           # active window
T = B0 + W + 1
rng = np.random.default_rng(11)


def land(h):
    return M.R(hs - h)


def ramp_ref(t, h, pre):
    if t <= B0: return None
    if t == T: return land(h)
    s = t - B0
    if s <= Nr: y = H * (1 - s / Nr)
    elif s <= Nr + Th: y = 0.0
    else: y = H * (s - Nr - Th) / Nup
    return (np.array([i0]), np.array([math.atanh(y) - pre[i0]]))


def evaluate(name, pol):
    t0 = time.time()
    S = Sim(M, hs, pol, T, ckpt=500)
    top, hist = S.opnorm(iters=5, tol=1e-5, block=2, seed=3)
    ones = np.ones(n)
    Y = np.stack([S.query_adjoint([GHI * ones])])
    Wq = S.adjoint(Y)
    r = dict(name=name, energy=S.energy, R=math.sqrt(S.energy), credit_power=credit_from_M(M, top),
             credit_upper=credit_from_M(M, S.upper_M), legal_L1=math.sqrt(l) / n * float(np.linalg.norm(Wq[0])),
             max_dev=float(S.dev[B0 + 1:].max()), secs=time.time() - t0)
    print(json.dumps(r), flush=True)
    return r


rows = [evaluate("ramp_hold_reference", ramp_ref)]
E = rows[0]["energy"]
# helper: scale an input schedule to energy E (landing cost is extra and reported)
def scaled(sched):
    tot = sum(float(v @ v) for _, (_, v) in sched.items())
    c = math.sqrt(E * 0.9 / tot)
    return {t: (ix, v * c) for t, (ix, v) in sched.items()}

for trial in range(2):
    sched = {}
    for _ in range(400):
        t = int(rng.integers(B0 + 1, T)); ix = rng.choice(np.arange(1, k), size=3, replace=False)
        sched[t] = (ix, rng.normal(size=3))
    sched = scaled(sched)
    pol = (lambda sc: (lambda t, h, pre: land(h) if t == T else (sc[t] if t in sc else None)))(sched)
    rows.append(evaluate(f"random_sparse_{trial}", pol))
cyc = np.arange(1, d)
for f in (0, 3):
    base = {t: (cyc, np.cos(2 * np.pi * f * (cyc - t) / d)) for t in range(B0 + 1, T)}
    sched = scaled(base)
    pol = (lambda sc: (lambda t, h, pre: land(h) if t == T else (sc[t] if t in sc else None)))(sched)
    rows.append(evaluate(f"resonant_rotating_f{f}", pol))
off = np.arange(d, k)
base = {t: (off, -np.ones(len(off))) for t in range(B0 + 1, T)}
sched = scaled(base)
pol = (lambda sc: (lambda t, h, pre: land(h) if t == T else (sc[t] if t in sc else None)))(sched)
rows.append(evaluate("uniform_offcycle_bias_shift", pol))
json.dump(dict(n=n, E_ref=E, rows=rows), open("random_search_n4000.json", "w"), indent=1)
