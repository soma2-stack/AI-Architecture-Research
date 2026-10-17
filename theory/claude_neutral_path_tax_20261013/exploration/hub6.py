"""Strongest hub design in the exact frozen reference model.

* W adjacent holes (gate exactly 1, maintained by input) start at p0 = d/2 at time ts and
  broadcast through the Householder row d-1 on W consecutive steps.
* During the broadcast window the written pairs are HELD at code values:
  off-cycle pairs (stationary) and co-moving cycle pairs (shift +1 per step).
* One reset step at the end (successor rows of the cycle block, the off-cycle block).
* Credits for one zero-sum direction v: fixed-feature (source factor c_t, E masks row 0)
  and bias (injection v every step).  Normalized weights: ff = sigma sqrt(l)/n,
  bias = w_b/beta = 0.05/||R0||_F.  One-step legal query (gates in [LO, HI]).
"""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import LO, HI  # noqa: E402


def best_query_value(F, dB):
    z = F.R0(dB)
    return max(np.where(z > 0, HI, LO) @ z, -(np.where(z > 0, LO, HI) @ z)) / math.sqrt(F.n)


def query_vector(F, dB):
    z = F.R0(dB)
    g1 = np.where(z > 0, HI, LO)
    g2 = np.where(z > 0, LO, HI)
    return g1 if abs(g1 @ z) >= abs(g2 @ z) else g2


def design(F, W, Pc, Poff, wake=None):
    d = F.d
    ts = 4
    p0 = d // 2
    holes0 = p0 + np.arange(W)
    tb = ts + (d - 1 - holes0)
    t1, tL = int(tb.min()) + 1, int(tb.max()) + 1
    if wake is None:
        wake = max(60, d // 8)
    # cycle block at time t1 must sit beyond the wake and behind the hole block
    q0 = wake + t1
    hole_tail_t1 = int(holes0.min()) + (t1 - ts)
    Pc = min(Pc, max(0, (hole_tail_t1 - 5 - q0) // 2))
    Soff = np.arange(d, d + 2 * Poff)
    return dict(ts=ts, p0=p0, holes0=holes0, t1=t1, tL=tL, T=tL + 1, q0=q0, Pc=Pc, Soff=Soff)


def run(F, W, theta_c, theta_o, D, holes_on=True, c=0.22, delta=0.22):
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    ts, holes0, t1, tL, T, q0, Pc, Soff = (D[x] for x in ("ts", "holes0", "t1", "tL", "T", "q0", "Pc", "Soff"))
    v = np.zeros(n)
    p0 = D["p0"]
    v[p0:d] = 1.0 / (d - p0)
    v[2:p0] = -1.0 / (p0 - 2)
    v /= np.linalg.norm(v)
    Ev = v.copy()
    Ev[0] = 0.0
    srcn = F.sigma * math.sqrt(F.l)
    h = np.zeros(n)
    Bf = np.zeros(n)
    Bb = np.zeros(n)
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
                rows = q0 + (tL - t1) + 1 + np.arange(2 * Pc)   # successors of the last cycle block
                tgt[rows] = np.tanh(pre[rows] * 0 + 0.05)          # public target
                drive[rows] = True
            tgt[Soff] = F.b0
            drive[Soff] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        supp += int(drive.sum())
        max_in = max(max_in, float(np.abs(x).max()))
        hp = h
        h = np.tanh(pre + x)
        gate = 1.0 - h * h
        ct = hp[k:].sum() / math.sqrt(F.l) / srcn
        Bf = gate * (F.R0(Bf) + ct * Ev)
        Bb = gate * (F.R0(Bb) + v)
    return h, Bf, Bb, supp, max_in


if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    use_cyc = len(sys.argv) <= 3 or sys.argv[3] != "nocyc"
    F = Frozen(n)
    D = design(F, W, Pc=(F.d // 2) if use_cyc else 0, Poff=(F.k - F.d) // 2 - 2)
    rng = np.random.default_rng(7)
    tc = rng.choice([-1.0, 1.0], size=D["Pc"])
    to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
    t0 = time.time()
    hA, fA, bA, supp, mi = run(F, W, tc, to, D, True)
    hB, fB, bB, *_ = run(F, W, -tc, -to, D, True)
    cA, gA, eA, *_ = run(F, W, tc, to, D, False)
    cB, gB, eB, *_ = run(F, W, -tc, -to, D, False)
    wff = F.sigma * math.sqrt(F.l) / n
    wb = 0.05 / math.sqrt(F.a ** 2 * F.k + F.delta ** 2 * F.l)
    res = {}
    for lab, df, db in [("tot", fA - fB, bA - bB), ("hole", (fA - fB) - (gA - gB), (bA - bB) - (eA - eB)),
                        ("ctrl", gA - gB, eA - eB)]:
        # one common query for both groups: choose it on the ff difference (same pattern)
        gq = query_vector(F, df)
        ff = wff * abs(gq @ F.R0(df)) / math.sqrt(n)
        bb = wb * abs(gq @ F.R0(db)) / math.sqrt(n)
        res[lab] = (ff, bb, math.hypot(ff, bb))
    print(f"n={n} W={W} Pc={D['Pc']} Poff={len(D['Soff'])//2} T={D['T']} endpoint={np.abs(hA-hB).max():.1e} "
          f"max_in={mi:.3f} supp/n={supp/n:.1f} | " +
          " ".join(f"{lab}: ff={a:.5f} bias={b2:.5f} full={c2:.5f}" for lab, (a, b2, c2) in res.items()) +
          f" | time={time.time()-t0:.0f}s", flush=True)
