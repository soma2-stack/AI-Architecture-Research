"""Shared tools for the dense-transfer study (independent of PR #29's scripts).

* R0_explicit(n): the explicit R0 = diag(a U P U, lam I) (columns via the exact skeleton action).
* prescribed_R(n): the frozen dense recipe, built explicitly:
    power vectors u_* = v_* = (1, t, ..., t^(n-1)) with the FIRST integer t >= 1 such that every
    entry of R0^-1 u_* (resp. v_*^T R0^-1) is nonzero; C = u_* v_*^T/(|u_*||v_*|);
    B = R0 + eta_j C with the first j >= 0 such that B and B^-1 have no zero entry,
    eta_j = 2^-j/(1e8 n^2);  R = (a/||B||op) B.
  Returns R, alpha, eta, t, j and the checks performed.
* schedule_S(n, D, H, A, R_0row): the PR #33/#34 sequential construction S (spike from row 19 when
  R_0row = 20; pairs (d+2i, d+2i+1); hold H; balanced 7-step pulse; parking at the bath).
* simulate(R, n, sched, theta, cols, ...): forward run with ACTUAL inputs
    x_t(i) = atanh(target_t(i)) - (R h_(t-1) + b)_i on driven rows, x_t(i) = 0 exactly elsewhere,
  optionally with the actual credit B_t = G_t(R B_(t-1) + c_t E) and the R0-skeleton credit
  B'_t = G_t(R0 B'_(t-1) + c_t E) (same actual gates) on chosen credit columns.
"""
import math
import numpy as np


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def R0_explicit(n):
    k, d = n // 2, n // 4; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O_apply(np.eye(k), k, d, gam)
    R0[k:, k:] = lam * np.eye(n - k)
    return R0


def prescribed_R(n, max_t=5, max_j=60):
    R0 = R0_explicit(n); a = 1 - 1 / n
    R0inv = np.linalg.inv(R0)
    tsel = None
    for t in range(1, max_t + 1):
        p = np.array([float(t) ** i for i in range(n)]) if t > 1 else np.ones(n)
        if np.all(np.abs(R0inv @ p) > 0) and np.all(np.abs(p @ R0inv) > 0):
            tsel = t; break
    assert tsel == 1, "power base t = 1 expected (PR #29 Lemma D1)"
    u = np.ones(n); C = np.outer(u, u) / n
    for j in range(max_j):
        eta = 2.0 ** (-j) / (1e8 * n ** 2)
        B = R0 + eta * C
        if np.all(B != 0) and np.all(np.linalg.inv(B) != 0):
            break
    nb = np.linalg.norm(B, 2)
    alpha = a / nb
    R = alpha * B
    info = {"t": tsel, "j": j, "eta": eta, "alpha": alpha, "1-alpha": 1 - alpha,
            "min|R0^-1 1|": float(np.abs(R0inv @ np.ones(n)).min()),
            "min|R|": float(np.abs(R).min()), "min|R^-1|": float(np.abs(np.linalg.inv(R)).min()),
            "||R||op - a": float(np.linalg.norm(R, 2) - a), "||R-R0||op": float(np.linalg.norm(R - R0, 2))}
    return R, R0, alpha, eta, info


def schedule_S(n, D, H, A=.38, R0row=20):
    k, d = n // 2, n // 4; T = 2 * d; Ts = T - (d - R0row)
    sig = [Ts + 20 + i * (H + 1) for i in range(D)]
    pairs = [(d + 2 * (i + 1), d + 2 * (i + 1) + 1) for i in range(D)]
    assert sig[-1] + H <= T, "construction does not fit"
    hm = H // 2

    def targets(t, z):
        out = {}
        if t >= Ts:
            out[d - 1 - (T - t)] = ("set", 0.0)
        for zi, st, (j, jp) in zip(z, sig, pairs):
            if st <= t < st + H:
                out[j] = ("set", 0.0); out[jp] = ("set", 0.0)
                if st + hm <= t < st + hm + 7:
                    v = math.tanh(A * (1 + zi) / 2); out[j] = ("set", v); out[jp] = ("set", -v)
            elif t == st + H:
                out[j] = ("park", None); out[jp] = ("park", None)
        return out
    return {"n": n, "k": k, "d": d, "T": T, "Ts": Ts, "sig": sig, "pairs": pairs, "H": H, "D": D,
            "targets": targets, "pulse_rows": [r for p in pairs for r in p]}


def source_scale(n, lam):
    sig = .05
    for _ in range(200):
        sig = math.tanh(lam * sig + .05)
    return sig


def simulate(Rmat, n, S, z, cols=(), R0=None, field=None, keep_states=False, hook=None):
    """Rmat: explicit n x n matrix, or None with field=(alpha, eta) to use the exact identity
    R h = alpha R0 h + (alpha eta/n)(1^T h) 1 (PR #29 Lemma D2) with the R0 skeleton action.
    cols: credit columns (state-row indices r: direction e_r f_s^T). Returns a dict."""
    k, d, T = S["k"], S["d"], S["T"]; l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / math.sqrt(k)); sig = source_scale(n, lam)
    cols = list(cols); q = len(cols)

    def Rmul(M):
        if Rmat is not None:
            return Rmat @ M
        al, eta = field
        out = np.empty_like(M)
        out[:k] = al * a * O_apply(M[:k], k, d, gam)
        out[k:] = al * lam * M[k:]
        out += (al * eta / n) * M.sum(0)
        return out

    def R0mul(M):
        out = np.empty_like(M)
        out[:k] = a * O_apply(M[:k], k, d, gam); out[k:] = lam * M[k:]
        return out

    h = np.zeros(n)
    B = np.zeros((n, q)); Bp = np.zeros((n, q)); Op = np.zeros((n, q))
    rec = {"support": [], "maxx": 0.0, "states": [] if keep_states else None, "bath": [], "gates": [] if keep_states else None}
    ar = np.arange(q)
    for t in range(1, T + 1):
        pre = Rmul(h[:, None])[:, 0] + .05
        hn = np.tanh(pre)
        s_t = float(hn[k - 1])                    # never-driven off-cycle row = bath
        x = np.zeros(n)
        for r, (kind, v) in S["targets"](t, z).items():
            tgt = s_t if kind == "park" else v
            x[r] = math.atanh(tgt) - pre[r]; hn[r] = tgt
        if hook is not None:
            hook(t, h, pre, hn, x, s_t)
        rec["support"].append(int(np.count_nonzero(x)))
        rec["maxx"] = max(rec["maxx"], float(np.abs(x).max()))
        rec["bath"].append(s_t)
        g = 1 - hn ** 2
        if q:
            c = float(h[k:].sum() / (sig * math.sqrt(l)) / math.sqrt(l))   # f_s^T h_src/(sigma sqrt l), f_s = 1/sqrt(l)
            Bn = Rmul(B); Bn[cols, ar] += c; B = g[:, None] * Bn
            Bpn = R0mul(Bp); Bpn[cols, ar] += c; Bp = g[:, None] * Bpn
            # own part (local skeleton) of B' for off-cycle memory columns: single scalar on row c
            On = np.zeros((n, q)); On[2:d] = g[2:d, None] * a * Op[1:d - 1]; On[d:k] = g[d:k, None] * a * Op[d:k]
            On[cols, ar] += c * g[cols]
            Op = On
        if keep_states:
            rec["states"].append(hn.copy()); rec["gates"].append(g.copy())
        h = hn
    rec.update({"h": h, "B": B, "Bp": Bp, "Op": Op, "sigma": sig})
    return rec
