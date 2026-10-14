"""Continuous-write hub design: W adjacent holes broadcast on W consecutive steps while the
off-cycle pairs S are HELD at their code values; one reset at the end.  Zero-sum v."""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import separation  # noqa: E402


def run(F, W, theta, holes_on=True, c=0.22, delta=0.22, ts=4, S=None, return_inputs=False):
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    if S is None:
        S = np.arange(d, d + 2 * len(theta))
    A, Bp = S[0::2], S[1::2]
    p0 = d // 2
    holes0 = p0 + np.arange(W)                 # adjacent holes
    tb = ts + (d - 1 - holes0)                 # broadcast times (consecutive)
    t_first, t_last = int(tb.min()) + 1, int(tb.max()) + 1   # write window
    T = t_last + 1                             # reset step = endpoint
    v = np.zeros(n)
    L1, L2 = d - p0, p0 - 2
    v[p0:d] = 1.0 / L1
    v[2:p0] = -1.0 / L2
    v /= np.linalg.norm(v)
    Ev = v.copy()
    Ev[0] = 0.0
    srcn = F.sigma * math.sqrt(F.l)
    h = np.zeros(n)
    Bv = np.zeros(n)
    supp = 0
    max_in = 0.0
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        tgt = np.tanh(pre)
        drive = np.zeros(n, dtype=bool)
        if holes_on and t >= ts:
            pos = holes0 + (t - ts)
            pos = pos[pos <= d - 1]
            tgt[pos] = 0.0
            drive[pos] = True
        if t_first <= t <= t_last:
            tgt[A] = c + delta * theta
            tgt[Bp] = c - delta * theta
            drive[S] = True
        if t == T:
            tgt[S] = F.b0
            drive[S] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        supp += int(drive.sum())
        max_in = max(max_in, float(np.abs(x).max()))
        hp = h
        h = np.tanh(pre + x)
        ct = hp[k:].sum() / math.sqrt(F.l) / srcn
        Bv = (1.0 - h * h) * (F.R0(Bv) + ct * Ev)
    return h, Bv, T, supp, max_in


if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    c = float(sys.argv[3]) if len(sys.argv) > 3 else 0.22
    delta = float(sys.argv[4]) if len(sys.argv) > 4 else 0.22
    F = Frozen(n)
    rng = np.random.default_rng(1)
    P = (F.k - F.d) // 2 - 2
    theta = rng.choice([-1.0, 1.0], size=P)
    t0 = time.time()
    hA, BA, T, supp, mi = run(F, W, theta, True, c, delta)
    hB, BB, *_ = run(F, W, -theta, True, c, delta)
    cA, CA, *_ = run(F, W, theta, False, c, delta)
    cB, CB, *_ = run(F, W, -theta, False, c, delta)
    print(f"n={n} W={W} c={c} d={delta} endpoint={np.abs(hA-hB).max():.1e} max_in={mi:.3f} supp/n={supp/n:.1f} "
          f"sep_tot={separation(F, BA-BB):.5f} sep_ctrl={separation(F, CA-CB):.5f} "
          f"sep_hole={separation(F, (BA-BB)-(CA-CB)):.5f} time={time.time()-t0:.0f}s", flush=True)
