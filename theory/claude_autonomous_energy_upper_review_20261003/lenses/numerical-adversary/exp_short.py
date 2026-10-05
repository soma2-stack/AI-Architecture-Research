"""Energy-limited emulation: zero burn-in B0, create an off-cycle hole, hold Th steps, land
exactly at h*. Credit is measured at the landing time.  usage: exp_short.py n B0 Th1,Th2,...
Probe lower bound (e_i) + analytic upper bound; optional power iteration (env POWER=1).
Also a 'pulse' variant: re-create the hole every P steps and let it relax freely (env PULSE=P).
"""
import os, sys, json, math, time
import numpy as np
from model import Model
from sim import Sim, GLO, GHI, credit_from_M

n = int(sys.argv[1]); B0 = int(sys.argv[2]); Ths = [int(s) for s in sys.argv[3].split(",")]
POWER = os.environ.get("POWER", "0") == "1"
QUER = os.environ.get("QUERY", "1") == "1"
PULSE = int(os.environ.get("PULSE", "0"))
M = Model(n)
hs = M.polish(M.fixed_point(), 20)
k, d, l = M.k, M.d, M.l
ath = np.arctanh(hs)
ioff = d + (k - d) // 2
rows = []


def pol_hold(Th):
    def pol(t, h, pre):
        if t == B0 + Th + 1:
            return ath - pre
        if B0 < t <= B0 + Th:
            if PULSE and (t - B0 - 1) % PULSE != 0:
                return None
            return (np.array([ioff]), np.array([-pre[ioff]]))
        return None
    return pol


for Th in Ths:
    t0 = time.time()
    T = B0 + Th + 1
    S = Sim(M, hs, pol_hold(Th), T, ckpt=500)
    hold_e = float(S.xnorm2[B0 + 1:B0 + Th + 1].sum())
    row = dict(n=n, B0=B0, Th=Th, pulse=PULSE, energy=S.energy, R_needed=math.sqrt(S.energy),
               burnin_energy=float(S.xnorm2[:B0 + 1].sum()), create_energy=float(S.xnorm2[B0 + 1]),
               hold_energy_excl_create=hold_e - float(S.xnorm2[B0 + 1]),
               land_energy=float(S.xnorm2[T]), Bstar_sq_times_Th=M.Bstar ** 2 * Th,
               end_err=float(np.linalg.norm(S.hT - hs)), upper_M=S.upper_M,
               credit_upper=credit_from_M(M, S.upper_M))
    V = np.zeros((1, k - 1)); V[0, ioff - 1] = 1.0
    Z = S.forward(V)
    row["lower_M"] = float(np.linalg.norm(Z[0]))
    row["credit_lower"] = credit_from_M(M, row["lower_M"])
    # mechanism formula: sigma*sum_j a^j over the hold + landing gate
    sig = hs[k]
    row["formula_credit"] = M.a / n * math.sqrt(l) * sig * (1 - M.A ** Th) / (1 - M.A) * M.A * (1 - hs[ioff] ** 2)
    if POWER:
        top, hist = S.opnorm(v0=V[0], iters=8, tol=1e-6, block=2)
        row["power_M"] = top; row["credit_exact"] = credit_from_M(M, top)
    if QUER:
        ones = np.ones(n)
        g = GLO * ones; g[ioff] = GHI
        Y = np.stack([S.query_adjoint([GHI * ones]), S.query_adjoint([g])])
        W = S.adjoint(Y)
        row["query_L1_allGHI"] = math.sqrt(l) / n * float(np.linalg.norm(W[0]))
        row["query_L1_spike"] = math.sqrt(l) / n * float(np.linalg.norm(W[1]))
    row["secs"] = time.time() - t0
    rows.append(row)
    print(json.dumps(row), flush=True)
json.dump(rows, open(f"short_n{n}_B{B0}_{sys.argv[3].replace(',', '-')}_p{PULSE}.json", "w"), indent=1)
