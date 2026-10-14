"""Optimized hub-broadcast test: larger write contrast, many stages, K-step legal queries.

Writes on off-cycle pairs: (c+delta*theta, c-delta*theta); reset to b0.
Separation for the v-projected fixed-feature gradient under a K-step legal query whose
future gates on each off-cycle row are all HI or all LO by the sign of the credit difference.
"""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import LO, HI  # noqa: E402
from hub2 import run  # noqa: E402


def kstep_sep(F, dBv, K, S):
    """Lower bound: (sigma sqrt(l)/n) |lambda_T^T dBv| with a K-step aligned query."""
    n = F.n
    sgn = np.sign(dBv)
    best = 0.0
    for flip in (1.0, -1.0):
        g = np.full(n, 0.5 * (LO + HI))
        g[S] = np.where(flip * sgn[S] > 0, HI, LO)
        lam = np.ones(n) / math.sqrt(n)
        for _ in range(K):
            lam = F.R0T(g * lam)
        best = max(best, abs(lam @ dBv))
    return F.sigma * math.sqrt(F.l) / n * best


if __name__ == "__main__":
    n = int(sys.argv[1])
    H = int(sys.argv[2])
    c, delta = float(sys.argv[3]), float(sys.argv[4])
    F = Frozen(n)
    rng = np.random.default_rng(1)
    P = (F.k - F.d) // 2 - 2
    theta = rng.choice([-1.0, 1.0], size=P)
    S = np.arange(F.d, F.d + 2 * P)
    t0 = time.time()
    hA, BA, T, hc, gb, holes0 = run(F, H, theta, True, c=c, delta=delta, zerosum=True)
    hB, BB, *_ = run(F, H, -theta, True, c=c, delta=delta, zerosum=True)
    cA, CA, *_ = run(F, H, theta, False, c=c, delta=delta, zerosum=True)
    cB, CB, *_ = run(F, H, -theta, False, c=c, delta=delta, zerosum=True)
    dh, dc = BA - BB, CA - CB
    out = []
    for K in (1, 3, 5):
        out.append((K, kstep_sep(F, dh, K, S), kstep_sep(F, dc, K, S), kstep_sep(F, dh - dc, K, S)))
    print(f"n={n} H={H} c={c} delta={delta} endpoint={np.abs(hA-hB).max():.1e} " +
          " ".join(f"K={K}:tot={a:.5f},ctrl={b:.5f},hole={e:.5f}" for K, a, b, e in out) +
          f" time={time.time()-t0:.0f}s", flush=True)
