"""Maximize the ACTUAL legal-query credit over L=1 queries (gates g in [GLO,GHI]^n, any
preactivation box point is legal) for a fixed history: convex maximization of
||N g||, N g = M_T^*(R^T(g o q)); vertex ascent g <- argmax_vertex <N^*N g_cur, g>.
usage: t5_query_ascent.py n kind   (kind: offhole | cyclehole | baseline)
"""
import os, sys, json, math
import numpy as np
from model import Model
from sim import Sim, GLO, GHI

n = int(sys.argv[1]); kind = sys.argv[2]
M = Model(n); hs = M.polish(M.fixed_point(), 20); k, d, l = M.k, M.d, M.l
i0 = d + (k - d) // 2
q = np.full(n, 1 / math.sqrt(n))
if kind == "offhole":
    Th = 2 * n; T = Th + 1
    pol = lambda t, h, pre: (np.array([i0]), np.array([-pre[i0]])) if t <= Th else M.R(hs - h)
elif kind == "cyclehole":
    Th = d - 3; T = Th + 1; jend = d - 2
    pol = lambda t, h, pre: (np.array([jend - (Th - t)]), np.array([-pre[jend - (Th - t)]])) if t <= Th else M.R(hs - h)
else:
    T = 20001
    pol = lambda t, h, pre: M.R(hs - h) if t == T else None
S = Sim(M, hs, pol, T, ckpt=500)


def credit(G):   # G: (p,n) gate rows -> credits and adjoint outputs
    Y = M.RT(G * q)
    Wv = S.adjoint(Y)
    return math.sqrt(l) / n * np.linalg.norm(Wv, axis=1), Wv


ones = np.ones(n)
starts = {"allGHI": GHI * ones, "allGLO": GLO * ones}
g = GLO * ones; g[i0] = GHI; starts["spike_offcycle"] = g
g = GLO * ones.copy(); g[d - 1] = GHI; starts["spike_d-1"] = g
res = {}
for name, g in [(kk, vv) for kk, vv in starts.items() if kk in os.environ.get("STARTS", "allGHI,allGLO,spike_offcycle,spike_d-1").split(",")]:
    hist = []
    for it in range(int(os.environ.get("ITERS", "6"))):
        c, Wv = credit(g[None, :])
        hist.append(float(c[0]))
        # gradient of ||N g||^2 wrt g: 2 q o R(M (M^* R^T(g q)))
        Z = S.forward(Wv)            # M (M^* y)
        grad = q * M.R(Z)[0]
        gnew = np.where(grad > 0, GHI, GLO)
        if np.array_equal(gnew, g):
            break
        g = gnew
    res[name] = dict(history=hist, final=hist[-1], n_GHI=int((g == GHI).sum()))
    print(name, json.dumps(res[name]), flush=True)
json.dump(dict(n=n, kind=kind, T=T, results=res, theorem_side_cap=None), open(f"query_ascent_n{n}_{kind}.json", "w"), indent=1)
