"""Diagnostics for the hub-broadcast mechanism: hole credit, control without holes."""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import separation  # noqa: E402


def run(F, H, theta, holes_on=True, c=0.2, delta=0.15, p0=40, ts=4, spacing=2,
        zerosum=False):
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    S = np.arange(d, d + 2 * len(theta))
    A, Bp = S[0::2], S[1::2]
    if zerosum and p0 == 40:
        p0 = d // 2
    holes0 = np.array([p0 + spacing * j for j in range(H)])
    tw = np.sort(ts + (d - 1 - holes0) + 1)
    T = int(tw.max()) + 1
    writes, resets = set(int(t) for t in tw), set(int(t) + 1 for t in tw)
    v = np.zeros(n)
    v[holes0.min():d] = 1.0
    if zerosum:   # negative weight on the cycle rows 2..p0-1, total sum zero
        L1, L2 = d - holes0.min(), holes0.min() - 2
        v[holes0.min():d] = 1.0 / L1
        v[2:holes0.min()] = -1.0 / L2
    v /= np.linalg.norm(v)
    Ev = v.copy()
    Ev[0] = 0.0
    srcn = F.sigma * math.sqrt(F.l)
    h = np.zeros(n)
    Bv = np.zeros(n)
    hole_credit = []
    gates_bath = []
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        tgt = np.tanh(pre)
        drive = np.zeros(n, dtype=bool)
        if holes_on and t >= ts:
            for j in range(H):
                pos = holes0[j] + (t - ts)
                if pos <= d - 1:
                    tgt[pos] = 0.0
                    drive[pos] = True
        if t in writes:
            tgt[A] = c + delta * theta
            tgt[Bp] = c - delta * theta
            drive[S] = True
        if t in resets:
            tgt[S] = F.b0
            drive[S] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        hp = h
        h = np.tanh(pre + x)
        ct = hp[k:].sum() / math.sqrt(F.l) / srcn
        Bv = (1.0 - h * h) * (F.R0(Bv) + ct * Ev)
        if holes_on and H > 0 and t == ts + (d - 1 - holes0.max()):
            hole_credit.append(float(Bv[d - 1]))
        if t == T // 2:
            gates_bath.append(float(np.median(1 - h[d // 2:d - 50] ** 2)))
            gates_bath.append(float(np.median(1 - h[S[-1] + 10:k] ** 2)) if S[-1] + 10 < k else float('nan'))
    return h, Bv, T, hole_credit, gates_bath, holes0


if __name__ == "__main__":
    n = int(sys.argv[1])
    H = int(sys.argv[2])
    F = Frozen(n)
    rng = np.random.default_rng(1)
    P = (F.k - F.d) // 2 - 2
    theta = rng.choice([-1.0, 1.0], size=P)
    t0 = time.time()
    out = {}
    for label, on in [("holes", True), ("control", False)]:
        h1, B1, T, hc, gb, holes0 = run(F, H, theta, on)
        h2, B2, _, _, _, _ = run(F, H, -theta, on)
        out[label] = (separation(F, B1 - B2), float(np.abs(h1 - h2).max()), hc, gb)
    T0 = F.d - 1 - holes0.max()
    print(f"n={n} H={H} T0={T0} sqrtT0={math.sqrt(T0):.1f} "
          f"sep_holes={out['holes'][0]:.6f} sep_control={out['control'][0]:.6f} "
          f"hole_credit_first={out['holes'][2]} bath_gates(cycle,offcycle)={out['holes'][3]} "
          f"endpoint={out['holes'][1]:.1e} time={time.time()-t0:.0f}s", flush=True)
