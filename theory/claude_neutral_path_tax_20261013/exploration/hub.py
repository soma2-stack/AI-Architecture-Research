"""Hub-broadcast construction in the exact frozen reference model R0.

History (all inputs via the exact reference inverse lift x = atanh(target) - R0 h - b
on driven coordinates; every other coordinate gets ZERO input):
  * autonomous from h0 = 0 for t < ts;
  * H holes created at ts on cycle rows p0 + 2j (j = 0..H-1), held at exactly 0 while
    they travel along the cycle; hole j reaches row d-1 at tb_j;
  * write at tw_j = tb_j + 1 on off-cycle pairs S: h = c + delta*theta_p, c - delta*theta_p
    (balanced: the selected sum, hence J, is public);
  * reset at tw_j + 1 on S to a public target (autonomous value of a no-write run);
  * endpoint T = last reset time.
Credit for one fixed-feature parameter direction v (unit, uniform on the hole paths):
  B_t v = G_t (R0 B_(t-1) v + c_t E v),  c_t = f_s^T h_(t-1)^src / (sigma sqrt(l)).
Separation lower bound (projection on v, one-step legal query, gates in [lo,hi]):
  (sigma sqrt(l)/n) * max_gf |(R0 dB_T v)^T gf| / sqrt(n).
"""
import math
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402

LO = 1.0 / math.cosh(0.75) ** 2
HI = 1.0 / math.cosh(0.25) ** 2


def run_history(F, H, theta, c=0.2, delta=0.15, p0=40, ts=4, spacing=2, S=None,
                v=None, record_credit=True):
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    if S is None:
        S = np.arange(d, d + 2 * (len(theta)))
    pairs_a = S[0::2]
    pairs_b = S[1::2]
    holes0 = np.array([p0 + spacing * j for j in range(H)])
    # arrival time of hole j at row d-1
    tb = ts + (d - 1 - holes0)
    tw = tb + 1
    order = np.argsort(tw)
    tw_sorted = tw[order]
    T = int(tw_sorted.max()) + 1
    writes = {int(t): j for j, t in zip(order, tw_sorted)}
    resets = set(int(t) + 1 for t in tw_sorted)
    h = np.zeros(n)
    Bv = np.zeros(n)
    if v is None:
        v = np.zeros(n)
        lo_row, hi_row = holes0.min(), d - 1
        v[lo_row:hi_row + 1] = 1.0
        v /= np.linalg.norm(v)
    Ev = v.copy()
    Ev[0] = 0.0          # E embeds selected memory rows 1..k-1 only
    Ev[k:] = 0.0
    srcnorm = F.sigma * math.sqrt(F.l)
    max_in = 0.0
    supp = 0
    target_reset = None
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        x = np.zeros(n)
        tgt = np.tanh(pre)
        if t >= ts:
            for j in range(H):
                pos = holes0[j] + (t - ts)
                if pos <= d - 1:
                    tgt[pos] = 0.0
        if t in writes:
            tgt[pairs_a] = c + delta * theta
            tgt[pairs_b] = c - delta * theta
        if t in resets:
            tgt[S] = F.b0  # public target for the off-cycle written rows
        drive = np.abs(np.arctanh(np.clip(tgt, -0.999999, 0.999999)) - pre) > 0
        drive &= (tgt != np.tanh(pre))
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        max_in = max(max_in, float(np.abs(x).max()))
        supp += int(drive.sum())
        h_prev = h
        h = np.tanh(pre + x)
        if record_credit:
            ct = h_prev[k:].sum() / math.sqrt(F.l) / srcnorm
            Bv = (1.0 - h * h) * (F.R0(Bv) + ct * Ev)
    return dict(h=h, Bv=Bv, T=T, max_in=max_in, supp=supp, tw=tw_sorted, v=v)


def separation(F, dBv):
    z = F.R0(dBv)
    pos = np.where(z > 0, HI, LO) @ z
    neg = -(np.where(z > 0, LO, HI) @ z)
    best = max(pos, neg)
    return F.sigma * math.sqrt(F.l) / F.n * best / math.sqrt(F.n)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1])
    H = int(sys.argv[2])
    F = Frozen(n)
    rng = np.random.default_rng(1)
    P = (F.k - F.d) // 2 - 2
    theta = rng.choice([-1.0, 1.0], size=P)
    r1 = run_history(F, H, theta)
    r2 = run_history(F, H, -theta)
    endpoint = float(np.abs(r1["h"] - r2["h"]).max())
    sep = separation(F, r1["Bv"] - r2["Bv"])
    print(f"n={n} H={H} T={r1['T']} endpoint_diff={endpoint:.2e} max_in={max(r1['max_in'], r2['max_in']):.3f} "
          f"supp={r1['supp']} supp/n={r1['supp']/n:.2f} sep={sep:.6f} sep/H={sep/H:.6f}")
