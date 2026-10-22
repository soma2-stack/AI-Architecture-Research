"""Column-restricted two-history simulator (shared by the Lemma M_rest experiments).

Credit columns never mix (PROOF.md Prop. S1), so the R0-skeleton credit B' and its own part can
be simulated on a chosen subset of credit columns at large n. The hidden state h is simulated in
full (O(n) per step). Drives are state settings: a scheduled row is set to a target value, as in
PR #31's experiments; legality of the targets (|x| < 1/2) is checked and reported.

hist(n, T, cols, schedule) -> dict with Z_T, O_T (k x len(cols)), the final state, the bath
trajectory and the maximal |x| used. `schedule(t)` returns {row: target state}.
"""
import math
import numpy as np


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def _yz(B, O, k, gam):
    sk = math.sqrt(k); w = -np.ones(k) / sk; w[0] += 1
    Y = B + (gam / sk) * (w @ B)[None, :]; Y[0] = B.sum(0) / sk
    Z = Y - O; Z[0] = Y[0]
    return Z


def hist(n, T, cols, schedule, bath_row=None, checkpoints=()):
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    cols = np.asarray(cols); nc = len(cols)
    w = -np.ones(k) / sk; w[0] += 1
    h = np.zeros(n); B = np.zeros((k, nc)); O = np.zeros((k, nc))
    xmax = 0.0; baths = np.zeros(T + 1); snaps = {}; checkpoints = set(checkpoints)
    if bath_row is None:
        bath_row = k - 1
    for t in range(1, T + 1):
        hm = h[:k]
        pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r, v in schedule(t).items():
            x = math.atanh(v) - pre[r]
            xmax = max(xmax, abs(x)); hn[r] = v
        g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * O_apply(B, k, d, gam)
        Bn[cols, np.arange(nc)] += c
        Bn *= gm[:, None]
        On = np.zeros((k, nc)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[cols, np.arange(nc)] += c * gm[cols]
        B, O, h = Bn, On, hn
        baths[t] = h[bath_row]
        if t in checkpoints:
            snaps[t] = {"Z": _yz(B, O, k, gam), "O": O.copy(), "h": h.copy()}
    return {"Z": _yz(B, O, k, gam), "O": O, "h": h, "bath": baths, "xmax": xmax, "snaps": snaps}


def chi_matrix_apply(g, k, d, a):
    """chi = a P^T U g (Prop. M1), without forming U."""
    sk = math.sqrt(k); gam = 1 / (1 - 1 / sk)
    wg = g[0] - g.sum() / sk
    Ug = g + (gam / sk) * wg; Ug[0] = g[0] - wg
    chi = np.empty(k)
    chi[:d - 1] = a * Ug[1:d]; chi[d - 1] = a * Ug[0]; chi[d:] = a * Ug[d:]
    return chi


def chi_adjoint(v, k, d, a):
    """g-gradient of g -> chi(g)^T v, i.e. (a P^T U)^T v = a U P v."""
    sk = math.sqrt(k); gam = 1 / (1 - 1 / sk)
    Pv = np.empty(k); Pv[1:d] = v[:d - 1]; Pv[0] = v[d - 1]; Pv[d:] = v[d:]
    w = -np.ones(k) / sk; w[0] += 1
    return a * (Pv - gam * w * (w @ Pv))


def best_query(M, k, d, a, LO, HI, starts=4, iters=40, seed=0):
    """Lower bound on sup over g in {LO,HI}^k of ||chi(g)^T M|| by alternating maximization."""
    rng = np.random.default_rng(seed); best = 0.0; gbest = None
    for st in range(starts):
        g = rng.choice([LO, HI], size=k) if st else np.full(k, HI)
        for _ in range(iters):
            r = chi_matrix_apply(g, k, d, a) @ M; nr = np.linalg.norm(r)
            if nr == 0:
                break
            coef = chi_adjoint(M @ (r / nr), k, d, a)
            gn = np.where(coef > 0, HI, LO)
            if np.array_equal(gn, g):
                break
            g = gn
        val = float(np.linalg.norm(chi_matrix_apply(g, k, d, a) @ M))
        if val > best:
            best, gbest = val, g
    return best, gbest
