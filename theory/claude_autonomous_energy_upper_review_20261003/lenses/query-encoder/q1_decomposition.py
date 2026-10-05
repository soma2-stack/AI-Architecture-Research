"""Hostile check of the past/direct gradient decomposition, query legality,
normalization and the all-query bound (13), written from the model only.

Model: h_t = tanh(R h_{t-1} + W x_t + b), W=I, b=.05*1, h_0=0, archived dense R.
Query: L>=1 future preactivations v_j in [1/4,3/4]^n realised by
x_j = v_j - R h_{j-1} - b (computed once, then HELD FIXED for derivatives).
Loss q^T h_{T+L}/beta, q=1/sqrt(n), beta=max(1,||R||F) frozen.

Checks:
 1. full backprop gradient == finite differences (inputs held fixed) for R,W,b;
 2. gradient == past part S_T^* xi_Q + direct part, xi_Q independent of h_T;
 3. two histories of DIFFERENT length landing on the SAME h_T have bitwise-equal
    direct parts (R,W,b) while past parts differ;
 4. alternative convention (re-solve the control under perturbed theta) gives
    the zero gradient (so the fixed-input convention is the only non-trivial one);
 5. selected block: past gradient == B_T^* xi_Q, and adversarial search over
    legal queries (L=1,2) of w_R||B_T^* xi_Q||_F / ((a/n)||B_T||op) stays <1;
 6. normalization numbers: beta=||R||F>1, w_R/beta=1/n, beta>sqrt(n)/2.
"""
import json
import numpy as np

rng = np.random.default_rng(20261003)


def build(n):
    k, d, l = n // 2, n // 4, n - n // 2
    a = 1 - 1 / n
    w = -np.ones(k) / np.sqrt(k)
    w[0] += 1
    gam = 2 / (w @ w)
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)  # (Pv)(i)=v(i-1)
    O = U @ P @ U
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O
    R0[k:, k:] = np.eye(l) / (100 * n)
    raw = R0 + np.ones((n, n)) / (1e8 * n ** 3)
    R = raw * (a / np.linalg.norm(raw, 2))
    return dict(n=n, k=k, d=d, l=l, a=a, R=R, R0=R0, W=np.eye(n), b=0.05 * np.ones(n))


def forward(R, W, b, xs, h0=None):
    n = R.shape[0]
    h = np.zeros(n) if h0 is None else h0
    hs = [h]
    for x in xs:
        h = np.tanh(R @ h + W @ x + b)
        hs.append(h)
    return hs


def controls(R, b, hT, vs):
    """future raw inputs realising preactivations vs from hT (W=I)."""
    xs, h = [], hT
    for v in vs:
        x = v - R @ h - b
        xs.append(x)
        h = np.tanh(v)
    return xs


def backprop(R, W, hs, xs, lam_end, t_from, t_to):
    """Accumulate gradient contributions of steps t in (t_from, t_to] (1-based
    step index t uses hs[t-1], xs[t-1], hs[t]); returns grads and adjoint at t_from."""
    n = R.shape[0]
    gR, gW, gb = np.zeros((n, n)), np.zeros((n, n)), np.zeros(n)
    lam = lam_end
    for t in range(t_to, t_from, -1):
        dlt = (1 - hs[t] ** 2) * lam
        gR += np.outer(dlt, hs[t - 1])
        gW += np.outer(dlt, xs[t - 1])
        gb += dlt
        lam = R.T @ dlt
    return gR, gW, gb, lam


def loss(R, W, b, xs_all, q, beta):
    return q @ forward(R, W, b, xs_all)[-1] / beta


def history(n, T, Rabs):
    X = rng.normal(size=(T, n))
    X *= Rabs / np.linalg.norm(X)
    return list(X)


def main():
    out = {}
    n = 200
    M = build(n)
    R, W, b, a, k, l = M["R"], M["W"], M["b"], M["a"], M["k"], M["l"]
    q = np.ones(n) / np.sqrt(n)
    beta = max(1.0, np.linalg.norm(R, "fro"))
    wR = np.linalg.norm(R, "fro") / n
    out["normalization"] = dict(beta=beta, wR_over_beta_times_n=wR / beta * n,
                                beta_over_half_sqrt_n=beta / (np.sqrt(n) / 2),
                                opnorm_R=np.linalg.norm(R, 2), a=a,
                                eR=np.linalg.norm(R - M["R0"], 2), e_bound=4 / (1e8 * n ** 2))

    # ---------- 1,2: decomposition + finite differences -------------
    T, L, Rabs = 60, 3, 1.0
    xp = history(n, T, Rabs)
    hs_p = forward(R, W, b, xp)
    hT = hs_p[-1]
    vs = [rng.uniform(0.25, 0.75, size=n) for _ in range(L)]
    xf = controls(R, b, hT, vs)
    xs_all = xp + xf
    hs = forward(R, W, b, xs_all)
    pre_err = max(np.abs(R @ hs[T + j] + xf[j] + b - vs[j]).max() for j in range(L))
    gR, gW, gb, _ = backprop(R, W, hs, xs_all, q / beta, 0, T + L)
    # direct part: future steps only; adjoint at h_T = xi_Q
    dR, dW, db, xi = backprop(R, W, hs, xs_all, q / beta, T, T + L)
    pR, pW, pb, _ = backprop(R, W, hs, xs_all, xi, 0, T)
    # xi_Q from future gates only
    lam = q / beta
    for v in reversed(vs):
        lam = R.T @ ((1 - np.tanh(v) ** 2) * lam)
    out["decomposition"] = dict(
        future_preactivation_err=float(pre_err),
        sum_err_R=float(np.abs(gR - dR - pR).max()),
        sum_err_W=float(np.abs(gW - dW - pW).max()),
        sum_err_b=float(np.abs(gb - db - pb).max()),
        xi_from_query_only_err=float(np.abs(lam - xi).max()),
        xi_norm_over_a_over_beta=float(np.linalg.norm(xi) / (a / beta)))
    fd = []
    for which in ("R", "W", "b"):
        D = rng.normal(size=(n, n) if which != "b" else n)
        D /= np.linalg.norm(D)
        eps = 1e-5
        args_p = [R, W, b]
        args_m = [R, W, b]
        i = "RWb".index(which)
        args_p = [A + eps * D if j == i else A for j, A in enumerate(args_p)]
        args_m = [A - eps * D if j == i else A for j, A in enumerate(args_m)]
        num = (loss(*args_p, xs_all, q, beta) - loss(*args_m, xs_all, q, beta)) / (2 * eps)
        ana = float(np.sum([gR, gW, gb][i] * D))
        # alternative convention: re-solve the controls under perturbed theta
        def alt(Rx, Wx, bx):
            hsx = forward(Rx, Wx, bx, xp)
            xfx = controls(Rx, bx, hsx[-1], vs)   # W=I only matters if Wx=I
            hh = hsx[-1]
            for j, x in enumerate(xfx):
                hh = np.tanh(Rx @ hh + x + bx)   # NOTE: uses W=I realisation
            return q @ hh / beta
        alt_num = (alt(*args_p) - alt(*args_m)) / (2 * eps) if which != "W" else None
        fd.append(dict(group=which, finite_diff=float(num), analytic=ana,
                       rel_err=float(abs(num - ana) / max(1e-30, abs(ana))),
                       resolve_control_derivative=None if alt_num is None else float(alt_num)))
    out["finite_difference"] = fd

    # ---------- 3: same endpoint, different lengths -------------
    T2 = 37
    xq = history(n, T2, 0.7)
    hs_q = forward(R, W, b, xq[:-1])
    xq[-1] = np.arctanh(hT) - R @ hs_q[-1] - b      # exact landing on h_T of history 1
    hs_q = forward(R, W, b, xq)
    land_err = float(np.abs(hs_q[-1] - hT).max())
    xs_all2 = xq + controls(R, b, hs_q[-1], vs)
    hs2 = forward(R, W, b, xs_all2)
    dR2, dW2, db2, xi2 = backprop(R, W, hs2, xs_all2, q / beta, T2, T2 + L)
    pR2, _, _, _ = backprop(R, W, hs2, xs_all2, xi2, 0, T2)
    out["same_endpoint"] = dict(
        landing_err=land_err,
        direct_R_diff=float(np.abs(dR2 - dR).max()), direct_W_diff=float(np.abs(dW2 - dW).max()),
        direct_b_diff=float(np.abs(db2 - db).max()), xi_diff=float(np.abs(xi2 - xi).max()),
        past_R_diff_norm=float(np.linalg.norm(pR2 - pR)), past_R_norm=float(np.linalg.norm(pR)))

    # ---------- 5: selected block B_T and adversarial queries -------------
    r = k - 1
    sel = np.arange(1, k)
    src = np.arange(k, n)
    B = np.zeros((n, r * l))
    for t in range(1, T + 1):
        G = 1 - hs_p[t] ** 2
        inj = np.zeros((n, r * l))
        hsrc = hs_p[t - 1][src]
        for i in range(r):
            inj[sel[i], i * l:(i + 1) * l] = hsrc
        B = G[:, None] * (R @ B + inj)
    Bop = np.linalg.norm(B, 2)
    pastsel = pR[np.ix_(sel, src)]
    out["selected_block"] = dict(
        BT_adjoint_vs_backprop_err=float(np.abs((B.T @ xi).reshape(r, l) - pastsel).max()),
        BT_op=float(Bop), sqrt_l_times_T=float(np.sqrt(l) * T))
    glo, ghi = 1 / np.cosh(0.75) ** 2, 1 / np.cosh(0.25) ** 2
    BtRt = B.T @ R.T
    best = {}
    for Lq in (1, 2):
        bestv = 0
        for trial in range(40):
            gs = [rng.choice([glo, ghi], size=n) for _ in range(Lq)]
            for sweep in range(30):
                changed = False
                for j in range(Lq):
                    # adjoint xi = R^T G_1 R^T G_2 ... q/beta ; linearize in g_j
                    def xi_of(gs_):
                        lam_ = q / beta
                        for g in reversed(gs_):
                            lam_ = R.T @ (g * lam_)
                        return lam_
                    lam_ = q / beta
                    for g in reversed(gs[j + 1:]):
                        lam_ = R.T @ (g * lam_)
                    pre = lam_  # vector multiplied by g_j
                    # xi = Mj (g_j * pre), Mj = R^T G_1 ... R^T (first j factors) R^T
                    def apply_prefix(y):
                        y = R.T @ y
                        for g in reversed(gs[:j]):
                            y = R.T @ (g * y)
                        return y
                    cur = B.T @ xi_of(gs)
                    # gradient of ||cur||^2 wrt g_j: 2 * pre_i * [Mj^T B B^T xi]_i
                    # Mj^T = (prefix)^T: compute by explicit small matrix
                    Mj = np.column_stack([apply_prefix(e) for e in np.eye(n)])
                    grad = pre * (Mj.T @ (B @ cur))
                    newg = np.where(grad >= 0, ghi, glo)
                    if not np.array_equal(newg, gs[j]):
                        gs[j] = newg
                        changed = True
                if not changed:
                    break
            val = wR * np.linalg.norm(B.T @ xi_of(gs))
            bestv = max(bestv, val)
        # also aligned-by-SVD attempt (not legal in general; for reference only)
        best[Lq] = dict(best_legal=float(bestv), bound_13=float(a / n * Bop),
                        ratio=float(bestv / (a / n * Bop)))
    out["adversarial_queries"] = best
    out["unrestricted_unit_adjoint_ratio_reference"] = float(
        wR * Bop * (a / beta) / (a / n * Bop))
    print(json.dumps(out, indent=1))
    with open(__file__.replace(".py", "_out.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
