"""Full-model validation of the cheap 'ramped hole': zero burn-in B0, linear ramp of one off-cycle
coordinate from h*_i to 0 over Nr steps, exact hold at 0 for Th steps, linear ramp back over Nup
steps, then EXACT landing at h* (dense correction, counted).  usage: exp_ramp.py n B0 Nr Th Nup [query]
"""
import os, sys, json, math, time
import numpy as np
from model import Model
from sim import Sim, GLO, GHI, credit_from_M

n, B0, Nr, Th, Nup = (int(s) for s in sys.argv[1:6])
QUERY = len(sys.argv) > 6 and sys.argv[6] == "1"
t_start = time.time()
M = Model(n)
hs = M.polish(M.fixed_point(), 20)
k, d, l = M.k, M.d, M.l
ath = np.arctanh(hs)
i = d + (k - d) // 2
Hi = hs[i]
t1, t2, t3, T = B0 + Nr, B0 + Nr + Th, B0 + Nr + Th + Nup, B0 + Nr + Th + Nup + 1


def pol(t, h, pre):
    if t <= B0:
        return None
    if t <= t1:
        y = Hi * (1 - (t - B0) / Nr)
    elif t <= t2:
        y = 0.0
    elif t <= t3:
        y = Hi * (t - t2) / Nup
    else:
        return M.R(hs - h)   # == atanh(h*) - pre exactly (proof eq. 14); stable when h*_1 rounds to 1
    return (np.array([i]), np.array([math.atanh(y) - pre[i]]))


S = Sim(M, hs, pol, T, ckpt=int(os.environ.get("CKPT", "500")))
e = S.xnorm2
row = dict(n=n, B0=B0, Nr=Nr, Th=Th, Nup=Nup, T=T, energy=S.energy, R=math.sqrt(S.energy),
           E_burnin=float(e[:B0 + 1].sum()), E_ramp_down=float(e[B0 + 1:t1 + 1].sum()),
           E_hold=float(e[t1 + 1:t2 + 1].sum()), E_ramp_up=float(e[t2 + 1:t3 + 1].sum()),
           E_land=float(e[T]), Bstar2_Th=M.Bstar ** 2 * Th, end_err=float(np.linalg.norm(S.hT - hs)),
           upper_M=S.upper_M, credit_upper=credit_from_M(M, S.upper_M),
           max_dev=float(S.dev.max()), max_dev_after_burnin=float(S.dev[B0:].max()),
           sim_secs=time.time() - t_start)
V = np.zeros((1, k - 1)); V[0, i - 1] = 1.0
Z = S.forward(V)
row["lower_M"] = float(np.linalg.norm(Z[0])); row["credit_lower"] = credit_from_M(M, row["lower_M"])
row["hole_coord_share"] = float(abs(Z[0, i]) / np.linalg.norm(Z[0]))
if QUERY:
    ones = np.ones(n); g = GLO * ones; g[i] = GHI
    Y = np.stack([S.query_adjoint([GHI * ones]), S.query_adjoint([g])])
    W = S.adjoint(Y)
    row["query_L1_allGHI"] = math.sqrt(l) / n * float(np.linalg.norm(W[0]))
    row["query_L1_spike"] = math.sqrt(l) / n * float(np.linalg.norm(W[1]))
row["secs"] = time.time() - t_start
print(json.dumps(row), flush=True)
json.dump(row, open(f"ramp_n{n}_B{B0}_Nr{Nr}_Th{Th}_Nup{Nup}.json", "w"), indent=1)
