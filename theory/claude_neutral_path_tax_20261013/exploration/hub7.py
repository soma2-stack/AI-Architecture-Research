"""Hub design v7: long holes (p0=40), zero-sum v with negative part on off-cycle rows,
co-moving cycle pairs beyond the wake + off-cycle pairs, held through W consecutive
broadcasts, one reset.  Reports fixed-feature (d_F) projected separation, total and
hole-only (linear decomposition against a no-hole control)."""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import LO, HI  # noqa: E402


def design(F, W, p0=40, ts=4, wake_skip=600):
    d = F.d
    holes0 = p0 + np.arange(W)
    tb = ts + (d - 1 - holes0)
    t1, tL = int(tb.min()) + 1, int(tb.max()) + 1
    hole_tail_t1 = int(holes0.min()) + (t1 - ts)        # lowest hole row at t1
    q0 = wake_skip
    Pc = max(0, (hole_tail_t1 - 5 - q0) // 2)
    Poff = (F.k - d) // 2 - 1
    Soff = d + np.arange(2 * Poff)
    return dict(ts=ts, holes0=holes0, t1=t1, tL=tL, T=tL + 1, q0=q0, Pc=Pc, Soff=Soff, p0=p0)


def direction(F, D):
    n, d = F.n, F.d
    v = np.zeros(n)
    L1 = d - D["p0"]
    L2 = F.k - d
    v[D["p0"]:d] = 1.0 / L1
    v[d:F.k] = -1.0 / L2
    return v / np.linalg.norm(v)


def run(F, D, theta_c, theta_o, holes_on=True, c=0.22, delta=0.22):
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    ts, holes0, t1, tL, T, q0, Pc, Soff = (D[x] for x in ("ts", "holes0", "t1", "tL", "T", "q0", "Pc", "Soff"))
    v = direction(F, D)
    Ev = v.copy()
    Ev[0] = 0.0
    srcn = F.sigma * math.sqrt(F.l)
    h = np.zeros(n)
    Bf = np.zeros(n)
    supp, max_in = 0, 0.0
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        tgt = np.tanh(pre)
        drive = np.zeros(n, dtype=bool)
        if holes_on and t >= ts:
            pos = holes0 + (t - ts)
            pos = pos[pos <= d - 1]
            tgt[pos] = 0.0
            drive[pos] = True
        if t1 <= t <= tL:
            j = t - t1
            if Pc > 0:
                ra = q0 + j + 2 * np.arange(Pc)
                tgt[ra] = c + delta * theta_c
                tgt[ra + 1] = c - delta * theta_c
                drive[ra] = True
                drive[ra + 1] = True
            tgt[Soff[0::2]] = c + delta * theta_o
            tgt[Soff[1::2]] = c - delta * theta_o
            drive[Soff] = True
        if t == T:
            if Pc > 0:
                rows = q0 + (tL - t1) + 1 + np.arange(2 * Pc)
                tgt[rows] = math.tanh(0.05)
                drive[rows] = True
            tgt[Soff] = F.b0
            drive[Soff] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        supp += int(drive.sum())
        max_in = max(max_in, float(np.abs(x).max()))
        hp = h
        h = np.tanh(pre + x)
        ct = hp[k:].sum() / math.sqrt(F.l) / srcn
        Bf = (1.0 - h * h) * (F.R0(Bf) + ct * Ev)
    return h, Bf, supp, max_in


def ff_sep(F, dB):
    z = F.R0(dB)
    best = max(np.where(z > 0, HI, LO) @ z, -(np.where(z > 0, LO, HI) @ z))
    return F.sigma * math.sqrt(F.l) / F.n * best / math.sqrt(F.n)


if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    F = Frozen(n)
    D = design(F, W)
    rng = np.random.default_rng(7)
    tc = rng.choice([-1.0, 1.0], size=D["Pc"])
    to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
    t0 = time.time()
    hA, fA, supp, mi = run(F, D, tc, to, True)
    hB, fB, *_ = run(F, D, -tc, -to, True)
    cA, gA, *_ = run(F, D, tc, to, False)
    cB, gB, *_ = run(F, D, -tc, -to, False)
    print(f"n={n} W={W} Pc={D['Pc']} Poff={len(D['Soff'])//2} T={D['T']} endpoint={np.abs(hA-hB).max():.1e} "
          f"max_in={mi:.3f} supp/n={supp/n:.1f} | dF tot={ff_sep(F, fA-fB):.5f} ctrl={ff_sep(F, gA-gB):.5f} "
          f"hole={ff_sep(F, (fA-fB)-(gA-gB)):.5f} | time={time.time()-t0:.0f}s", flush=True)
