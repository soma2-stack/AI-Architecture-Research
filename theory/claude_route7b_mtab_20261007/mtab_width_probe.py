"""Probe: does any legal survivor profile family give mass reuse?
For each family: operator norm / stable rank of the protected operator (independent temporal
filters), Haar-l1 width constant in a natural class order (Theorem NC bound when non-crossing),
and an optimised orthonormal basis (a rigorous instance certificate gamma, checked on ALL atoms).
D - q <= (gamma Lambda/s)^2; gamma = 1 is the single-orthonormal-reader budget."""
import numpy as np, time, sys
from mtab_core import *

def fam_rates(C, N, rng):
    eps = np.geomspace(1e-5, 1 - GL, C)
    return np.repeat((1 - eps)[:, None], N, axis=1)

def fam_staggered(C, N, rng):
    G = np.full((C, N), GH); tc = (np.arange(C) + 1) * N // (C + 1)
    for c in range(C): G[c, :tc[c]] = GL
    return G

def fam_random(C, N, rng, blk=50):
    nb = N // blk
    return np.repeat(np.where(rng.random((C, nb)) < 0.5, GL, GH), blk, axis=1)[:, :N]

def fam_bands(C, N, rng, M=4):
    """MTAB-X: M time bands; in band m class c is low for rank_m(c)*B/C steps (random rank)."""
    B = N // M; G = np.full((C, N), GH)
    for m in range(M):
        rk = rng.permutation(C)
        for c in range(C): G[c, m*B: m*B + rk[c]*B//C] = GL
    return G

FAMS = [("rates (non-crossing)", fam_rates), ("staggered (non-crossing)", fam_staggered),
        ("random gate words (crossing)", fam_random), ("bands M=4 (crossing)", lambda C,N,r: fam_bands(C,N,r,4)),
        ("bands M=16 (crossing)", lambda C,N,r: fam_bands(C,N,r,16))]
rng = np.random.default_rng(7)
N = 2400
print(f"gates in [{GL},{GH}], a={A}, write interval N={N}")
for C in [8, 16, 32, 64]:
    for name, fam in FAMS:
        t0 = time.time()
        Phi = profiles_from_gates(fam(C, N, rng)); At = atoms(Phi)
        sv = np.linalg.svd(At, compute_uv=False)
        order = np.argsort(-Phi[:, N // 2])                      # natural order: value at mid write
        gH_ = gamma_haar_order(At, order)
        nM, s23 = crossing_orders(Phi)
        sub = At[:, ::4]
        H = haar_basis(C)[:, :]; Q0 = H[:, np.argsort(order)] if False else haar_basis(C) @ np.eye(C)[order]
        g_opt, Q = optimize_basis(sub, Q0, iters=400)
        g_cert = gamma_basis(At, Q)                              # rigorous for this instance (all atoms)
        print(f"C={C:3d} {name:30s} ||U||op={sv[0]:7.2f} stable-rank={np.sum(sv**2)/sv[0]**2:5.2f} "
              f"max||a_t||={np.linalg.norm(At,axis=0).max():.3f}  gamma_Haar(order)={gH_:.3f}  "
              f"gamma_cert(opt basis)={g_cert:.3f}  #level-orders={nM:3d} (sum mu^2/3)^3={s23:6.2f}  ({time.time()-t0:.0f}s)", flush=True)
print("Theorem NC constant 1+2^-1/2 =", 1 + 2**-0.5)
