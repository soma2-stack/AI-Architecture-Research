"""Spike drift-capture construction in the exact R0 skeleton (numpy, CPU).

Scaled-down instance of the D=1 construction in PROOF.md section 3 (refutation of Hypothesis B):
* a spike hole (state 0, gate exactly 1) along the diagonal ending at (d-1, T), from row 7;
* arrival holes of length ell on every diagonal ending at d-1 at a pre-window time;
* consecutive arrivals are paired and modulated for J_M steps with opposite states
  +-tanh(DELTA (1+theta)/2) at offset JOFF before arrival, then reset to 0 (balanced: the
  state Sum' and J are identical in both histories at every time);
* everything else autonomous.
For theta = +1 and theta = -1 the script integrates the exact state recurrence
h_t = tanh(R0 h_(t-1) + x_t + .05) with all inputs computed as x = atanh(target) - pre, checks
|x| < .5, equal endpoint and equal window states, and computes the uniform one-step legal
query readout Gamma = Delta B_T^T nu (nu = R0^T(g_f 1)) by the exact adjoint
Gamma(r) = sum_t c_t g_r(t) phi_t(r), phi_T = nu, phi_(t-1) = R0^T(g_t * phi_t).
It also checks that no own (local-path) profile of a row at T differs between the
histories, so the whole readout difference is bus content, and compares Gamma with the
first-order drift-capture prediction of PROOF.md (3.4).
Finite-n illustration of exact mechanics only; it does not reach the theorem's n range.
Run: python -I exp_drift_capture.py [n[:ell] ...]   (default ell = d-8)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2
DELTA, J_M, JOFF = .45, 7, 2


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def OT_apply(y, k, d, gam):
    x = np.empty_like(y); x[0] = y[0]
    x[1:d - 1] = y[2:d]; x[d - 1] = 0.0; x[d:] = y[d:]
    s1 = y[1:].sum()
    x[1:] += -gam ** 2 * s1 / k + gam * y[1] / math.sqrt(k)
    x[d - 1] += gam * s1 / math.sqrt(k)
    return x


def schedule(n, ell, wsim):
    k, d = n // 2, n // 4
    T = (d - 8) + ell + wsim + 40
    Ts = T - (d - 8)                       # spike at row 7 at time Ts, row d-1 at T
    alo, ahi = Ts + 1, T - wsim - 2 * J_M  # arrival times (d-1 reached at t_A)
    if (ahi - alo) % 2 == 0:
        ahi -= 1
    drv = {}                               # t -> dict(row -> (base_target, sign_or_0))
    def put(t, r, tgt):
        drv.setdefault(t, {})[r] = tgt
    for t in range(Ts, T + 1):
        put(t, d - 1 - (T - t), ("hole", 0))
    pairs = []
    for tA in range(alo, ahi, 2):
        pairs.append(tA)
        for tB, sgn in ((tA, +1), (tA + 1, -1)):
            for t in range(tB - ell + 1, tB + 1):
                r = d - 1 - (tB - t)
                mod = (tA - JOFF - J_M + 1) <= t <= (tA - JOFF)
                put(t, r, ("mod", sgn) if mod else ("hole", 0))
    return dict(n=n, k=k, d=d, T=T, Ts=Ts, alo=alo, ahi=ahi, pairs=pairs, drv=drv, ell=ell)


def run_history(S, theta, keep_every):
    n, k, d, T = S["n"], S["k"], S["d"], S["T"]
    l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    h = np.zeros(n); ck = {0: h.copy()}; maxx = 0.0
    sig = 0.05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    for t in range(1, T + 1):
        pre = np.empty(n)
        pre[:k] = a * O_apply(h[:k], k, d, gam) + .05
        pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r, (kind, sgn) in S["drv"].get(t, {}).items():
            tgt = 0.0 if kind == "hole" else math.tanh(sgn * DELTA * (1 + theta) / 2)
            x = math.atanh(tgt) - pre[r]
            maxx = max(maxx, abs(x)); hn[r] = tgt
        h = hn
        if t % keep_every == 0 or t == T:
            ck[t] = h.copy()
    return ck, maxx, sig


def segment_states(S, ck, t_a, t_b, theta):
    """Recompute states for t in [t_a, t_b] from checkpoint t_a - 1."""
    n, k, d = S["n"], S["k"], S["d"]
    a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    h = ck[t_a - 1].copy(); out = {t_a - 1: h.copy()}
    for t in range(t_a, t_b + 1):
        pre = np.empty(n)
        pre[:k] = a * O_apply(h[:k], k, d, gam) + .05
        pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r, (kind, sgn) in S["drv"].get(t, {}).items():
            hn[r] = 0.0 if kind == "hole" else math.tanh(sgn * DELTA * (1 + theta) / 2)
        h = hn; out[t] = h.copy()
    return out


def S_T_apply(y, k, d):
    """Transpose of the local skeleton S on memory rows (S e_j = e_(j+1), 1<=j<=d-2; off-cycle fixed)."""
    x = np.zeros_like(y)
    x[1:d - 1] = y[2:d]; x[d:] = y[d:]
    return x


def lockstep_readout(S, cks, sig, gf, svals):
    """Backward pass for both histories at once.
    Returns Gamma^+ - Gamma^-, the first-order drift-capture prediction difference, the number of
    (row,time) positions with a gate difference, and how many lie on a local path of a row at T."""
    n, k, d, T = S["n"], S["k"], S["d"], S["T"]
    l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    nu = np.empty(n); nu[:k] = a * gf * OT_apply(np.ones(k), k, d, gam); nu[k:] = lam * gf
    phi = {1: nu.copy(), -1: nu.copy()}; psi = {1: np.zeros(k), -1: np.zeros(k)}
    Gam = {1: np.zeros(n), -1: np.zeros(n)}; pred = {1: np.zeros(n), -1: np.zeros(n)}
    arrivals = set(range(S["alo"], S["ahi"] + 2))
    bounds = sorted(cks[1].keys()); nbad = 0; hits = 0
    for i in range(len(bounds) - 1, 0, -1):
        ta, tb = bounds[i - 1] + 1, bounds[i]
        st = {th: segment_states(S, cks[th], ta, tb, th) for th in (1, -1)}
        for t in range(tb, ta - 1, -1):
            gp_ = {}
            for th in (1, -1):
                g = 1 - st[th][t] ** 2
                c = st[th][t - 1][k:].sum() / (sig * l)
                gp = g * phi[th]
                Gam[th][1:] += c * gp[1:]
                nphi = np.empty(n)
                nphi[:k] = a * OT_apply(gp[:k], k, d, gam); nphi[k:] = lam * gp[k:]
                phi[th] = nphi
                # prediction: weight w_t injected at row d-1 at arrival time t (captured at t+1)
                if t in arrivals and t + 1 <= T:
                    s = svals[t + 1]
                    psi[th][d - 1] += a * gf * gam * a ** (T - t) * s * s
                pred[th][1:k] += c * g[1:k] * psi[th][1:k]
                psi[th] = a * S_T_apply(g[:k] * psi[th], k, d)
                gp_[th] = g
            dg = np.abs(gp_[1] - gp_[-1]); idx = np.nonzero(dg > 1e-13)[0]
            nbad += len(idx)
            for r in idx:
                if (1 <= r <= d - 1 and r + (T - t) <= d - 1) or (d <= r < k):
                    hits += 1
    return Gam[1] - Gam[-1], pred[1] - pred[-1], nbad, hits


def main():
    specs = sys.argv[1:] or ["4096", "16384"]
    out = []
    for sp in specs:
        n = int(sp.split(":")[0]); d = n // 4
        ell = int(sp.split(":")[1]) if ":" in sp else d - 8
        S = schedule(n, ell, wsim=max(64, n // 64))
        K = 128
        cks, maxx = {}, 0.0
        for theta in (1, -1):
            ck, mx, sig = run_history(S, theta, K)
            cks[theta] = ck; maxx = max(maxx, mx)
        # bath state per time from the theta=+1 history (off-cycle row k-1); recompute cheaply
        svals = {}
        bounds = sorted(cks[1].keys())
        for i in range(1, len(bounds)):
            st = segment_states(S, cks[1], bounds[i - 1] + 1, bounds[i], 1)
            for t, h in st.items():
                svals[t] = h[S["k"] - 1]
        Gam, pred, nbad, hits = lockstep_readout(S, cks, sig, HI, svals)
        T = S["T"]
        hT = cks[1][T] - cks[-1][T]
        last_mod = max(S["pairs"]) - JOFF if S["pairs"] else 0
        win_diff = max(float(np.abs(cks[1][t] - cks[-1][t]).max()) for t in cks[1] if t > last_mod + 1)
        tau = .002 * n * math.sqrt(n) / (sig * math.sqrt(n - n // 2))
        r = {"n": n, "T": T, "ell": ell, "pairs": len(S["pairs"]),
             "max_abs_input": maxx,
             "endpoint_diff": float(np.abs(hT).max()),
             "window_state_diff_at_checkpoints": win_diff,
             "positions_with_gate_difference": int(nbad),
             "of_which_on_a_local_path_of_a_row_at_T": int(hits),
             "norm_Gamma": float(np.linalg.norm(Gam)),
             "norm_pred_first_order": float(np.linalg.norm(pred)),
             "rel_err_pred": float(np.linalg.norm(Gam - pred) / max(1e-300, np.linalg.norm(Gam))),
             "tau": tau, "Gamma_over_tau": float(np.linalg.norm(Gam) / tau),
             "bath_s_range": [float(min(svals.values())), float(max(svals.values()))]}
        print(json.dumps(r), flush=True); out.append(r)
    with open(os.path.join(HERE, "exp_drift_capture_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
