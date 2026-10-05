"""Hostile audit of theory/claude_moving_spike_remainder_20261002.

Independent model. Reads Claude's saved coefficient arrays and screen bases.
Does not modify them.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

CLAUDE = Path(__file__).resolve().parents[1] / "claude_moving_spike_remainder_20261002"
CODEX = Path(__file__).resolve().parents[1] / "codex_two_pulse_corotating_20261002"
OUT = Path(__file__).resolve().parent
EPS = 1e-3
TWO = 2 * EPS


def sech2(x):
    t = math.tanh(x)
    return 1.0 - t * t


G_HI = sech2(0.25)
G_LO = sech2(0.75)
S_G = 0.5 * (G_HI - G_LO)


def build(n):
    k, d = n // 2, n // 4
    L = k - d
    a = 1.0 - 1.0 / n
    ck = 1.0 / (math.sqrt(k) - 1.0)
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1.0
    ww = float(w @ w)
    sig = 2.0 / ww
    U = np.eye(k) - sig * np.outer(w, w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)
    O = U @ P @ U
    V = np.zeros((k, d))
    V[1:d, : d - 1] = np.eye(d - 1)
    V[d:, -1] = 1.0 / math.sqrt(L)
    OA = V.T @ O @ V
    Theta = V.T @ U[:, :d]
    # T = O^T on the visible coordinates 1..k-1
    OT = O.T
    # embedding E: R^{k-1} -> R^k, coordinate 0 is 0
    return dict(n=n, k=k, d=d, L=L, a=a, ck=ck, U=U, O=O, OT=OT, V=V, OA=OA,
                Theta=Theta, beta0=math.sqrt(k / n), Hnorm=0.4 * math.sqrt(n - k),
                lam=a * G_HI, scale=(0.4 * math.sqrt(n - k)) / n)


def x_of(S, p):
    """Spike in visible coordinates (physical 1..k-1), length k-1."""
    k, ck = S["k"], S["ck"]
    c = ck / math.sqrt(k)
    x = np.full(k - 1, -c)
    if p == 0:
        x[:] = 1.0 / math.sqrt(k)
    else:
        x[p - 1] = 1.0 - c
    return x


def apply_T(S, x):
    v = np.zeros(S["k"])
    v[1:] = x
    w = S["OT"] @ v
    return w[1:]


def visible_from_latent(S, y):
    m = S["U"] @ y
    return m[1:]


def propagate_visible(S, gates):
    """gates (L,k) physical, gates[0] nearest the loss. Returns X_L, sigma, p."""
    X = S["beta0"] * x_of(S, 0)
    sigma = S["beta0"]
    for t, g in enumerate(gates, start=1):
        p = (-(t - 1)) % S["d"]
        gamma = float(g[1:].mean()) if p == 0 else float(g[p])
        sigma *= S["a"] * gamma
        X = S["a"] * apply_T(S, g[1:] * X)
    return X, sigma, (-len(gates)) % S["d"]


def propagate_latent(S, gates):
    y = np.zeros(S["k"])
    y[0] = S["beta0"]
    U, a = S["U"], S["a"]
    for g in gates:
        u = U @ y
        y = a * (S["OT"] @ (g * u))
    return y


def check_frame(n):
    S = build(n)
    k, d = S["k"], S["d"]
    # T orthogonal
    eye = np.eye(k - 1)
    cols = np.column_stack([apply_T(S, eye[:, i]) for i in range(k - 1)])
    orth = float(np.max(np.abs(cols.T @ cols - np.eye(k - 1))))
    # coordinate 0 does not leak: O^T e_0 = e_0
    e0 = np.zeros(k); e0[0] = 1.0
    leak = float(np.max(np.abs(S["OT"] @ e0 - e0)))
    shifts = []
    for p in range(d):
        xp = x_of(S, p)
        got = apply_T(S, xp)
        pred = x_of(S, (p - 1) % d)
        shifts.append(float(np.max(np.abs(got - pred))))
    # x_p = V theta_p in physical coords
    ident = []
    for p in range(d):
        phys = np.zeros(k)
        phys[1:] = x_of(S, p)
        ident.append(float(np.max(np.abs(phys - S["V"] @ S["Theta"][:, p]))))
    # decomposition vs full latent recursion
    rng = np.random.default_rng(n)
    dec = []
    for L in (1, 2, 5, 17):
        G = rng.uniform(G_LO, G_HI, size=(L, k))
        X, sigma, p = propagate_visible(S, G)
        y = propagate_latent(S, G)
        X2 = visible_from_latent(S, y)
        # spike factor from diagonal formula
        sig2 = S["beta0"]
        for t, g in enumerate(G, start=1):
            pp = (-(t - 1)) % d
            # M_pp = g · (U e_p)^2
            sig2 *= S["a"] * float(g @ (S["U"][:, pp] ** 2))
        dec.append({
            "L": L,
            "visible_vs_latent": float(np.max(np.abs(X - X2))),
            "sigma_vs_diag": abs(sigma - sig2),
            "remainder_identity": float(np.max(np.abs(X - sigma * x_of(S, p) - (X - sigma * x_of(S, p))))),
            "spike_removed_matches": float(np.linalg.norm(X - sigma * x_of(S, p) - (X2 - sig2 * x_of(S, p)))),
        })
    # constant gate is a pure spike
    pure = []
    for L in (1, 4, d):
        G = np.full((L, k), G_HI)
        X, sigma, p = propagate_visible(S, G)
        alpha = S["beta0"] * (S["lam"] ** L)
        pure.append({"L": L, "p": int(p), "sigma_err": abs(sigma - alpha),
                     "resid": float(np.linalg.norm(X - alpha * x_of(S, p)))})
    # leak norms
    c = S["ck"] / math.sqrt(k)
    # cycle leak max
    g = np.full(k, G_LO); g[1] = G_HI  # physical node 1
    ell = np.zeros(k - 1)
    # ell_l = -c (g_l - g_p) for l != p, 0 at p
    gp = g[1]
    for i, phys in enumerate(range(1, k)):
        ell[i] = 0.0 if phys == 1 else -c * (g[phys] - gp)
    omega_c = 2 * S["ck"] * S_G * math.sqrt(1 - 2 / k)
    # node 0
    g0 = np.array([G_HI if i % 2 == 0 else G_LO for i in range(k)])
    bar = g0[1:].mean()
    ell0 = (g0[1:] - bar) / math.sqrt(k)
    omega_0 = S_G * math.sqrt(1 - 1 / k)
    return {
        "n": n, "T_orth": orth, "e0_fixed": leak, "shift_max": max(shifts),
        "x_equals_V_theta": max(ident), "pure": pure,
        "omega_c_attained": float(np.linalg.norm(ell)), "omega_c_bound": omega_c,
        "omega_0_sample": float(np.linalg.norm(ell0)), "omega_0_bound": omega_0,
        "dec_max_visible": max(r["visible_vs_latent"] for r in dec),
        "dec_max_sigma": max(r["sigma_vs_diag"] for r in dec),
    }


def phi_star(grid=20001):
    lo = G_LO / G_HI
    xs = np.linspace(lo, 1.0, grid)
    f1 = (1 - xs) * xs ** 2 / (1 + xs)
    # y at an endpoint: distance to lo or to 1
    extra = np.maximum((xs - lo) ** 2, (1 - xs) ** 2)
    val = float(np.max(f1 + extra))
    # correct per-coordinate excess scale (1-x)/(1+x)
    alt = float(np.max((1 - xs) / (1 + xs)))
    return val, alt, lo


def r3_violation_search(n, trials=4000, seed=1):
    """Maximise lhs-rhs of the coded R3 step inequality over gates and remainder vectors."""
    S = build(n)
    k, ck = S["k"], S["ck"]
    c = ck / math.sqrt(k)
    cp = ck * math.sqrt(1 - 1 / k)
    phi, alt, lo = phi_star()
    A = phi * cp ** 2
    rng = np.random.default_rng(seed)
    worst = -1e9
    worst_info = None
    m = k - 1
    for trial in range(trials):
        # gates on X, spike at a random cycle node (physical 1..d-1)
        p = int(rng.integers(1, S["d"]))
        g = rng.uniform(lo, 1.0, size=m)
        # force the spike coordinate
        u = float(rng.uniform(lo, 1.0))
        g[p - 1] = u
        if trial % 5 == 0:
            g[:] = lo
            g[p - 1] = u
            if trial % 10 == 0:
                u = lo
                g[:] = 1.0
                g[p - 1] = u
        Sigma = float(rng.uniform(0.05, 1.0))
        # worst-direction candidate: sign of the linear term
        b = c * Sigma * (g - u)          # so term is g*R - b, wait (g-u) includes 0 at spike
        # linear coeff of R in the expansion of ||g R - c Sigma (g-u)||^2 is -2 g * c Sigma (g-u)
        lin = -2.0 * g * c * Sigma * (g - u)
        direction = np.sign(lin)
        direction[direction == 0] = 1.0
        direction /= np.linalg.norm(direction)
        # also a random direction
        rand = rng.normal(size=m)
        rand /= np.linalg.norm(rand)
        for direc in (direction, rand, -direction):
            alpha = float(direc @ ((g ** 2 - 1.0) * direc))  # <= 0
            beta = float(lin @ direc)
            const = float(np.sum((c * Sigma * (g - u)) ** 2))
            B = 2 * cp * (1 - u) * Sigma
            # max over rho>=0 of alpha rho^2 + beta rho + const - B rho - A Sigma^2
            # vertex rho = -(beta-B)/(2 alpha) if alpha<0
            quad_b = beta - B
            if alpha < -1e-15:
                rho = max(0.0, -quad_b / (2 * alpha))
            else:
                rho = 0.0 if quad_b <= 0 else 50.0
            viol = alpha * rho ** 2 + quad_b * rho + const - A * Sigma ** 2
            if viol > worst:
                worst = viol
                worst_info = {"trial": trial, "u": u, "Sigma": Sigma, "rho": rho, "p": p,
                              "viol": viol, "alpha": alpha}
    return {"n": n, "phi_star": phi, "alt_(1-x)/(1+x)_max": alt, "lo": lo,
            "worst_violation": worst, "info": worst_info}


def r1_absolute_sup(n, Lmax=None):
    """sup_L ||r||_R1 / (a s_g beta0). Peaks and the L=2/L=1 ratio."""
    k, d = n // 2, n // 4
    a = 1 - 1 / n
    ck = 1 / (math.sqrt(k) - 1)
    lam = a * G_HI
    w0 = math.sqrt(1 - 1 / k)
    wc = 2 * ck * math.sqrt(1 - 2 / k)
    cap = 2 * G_HI / S_G
    if Lmax is None:
        Lmax = 8 * d
    best, arg = -1.0, 1
    ratio21 = lam * (w0 + wc) / w0
    acc = 0.0
    series = []
    for L in range(1, Lmax + 1):
        acc += w0 if ((-(L - 1)) % d) == 0 else wc
        F = min(acc, cap)
        val = (lam ** (L - 1)) * F
        if val > best:
            best, arg = val, L
        if L in (1, 2, 3, 4, 8, d, 2 * d) or L == Lmax:
            series.append({"L": L, "abs": val, "F": F})
    return {"n": n, "ck": ck, "lam": lam, "L1": w0, "sup": best, "argL": arg,
            "A2_over_A1": ratio21, "series": series}


def wake_family(n, Ls):
    """g_hi on coordinates the spike has visited, g_lo elsewhere. Relative remainder."""
    S = build(n)
    rows = []
    for L in Ls:
        if L > S["d"]:
            continue
        G = np.full((L, S["k"]), G_LO)
        visited = set()
        for t in range(1, L + 1):
            p = (-(t - 1)) % S["d"]
            if p != 0:
                G[t - 1, p] = G_HI
            visited.add(p)
            # set this step's gate; visited including current
        # rebuild properly: at step t, g_hi on nodes already visited BEFORE this step? 
        # Theory: g_hi on coordinates the primary spike has already visited.
        G = np.full((L, S["k"]), G_LO)
        seen = []
        for t in range(1, L + 1):
            for p in seen:
                if p != 0:
                    G[t - 1, p] = G_HI
            seen.append((-(t - 1)) % S["d"])
        X, sigma, p = propagate_visible(S, G)
        r = X - sigma * x_of(S, p)
        unit = S["a"] * S_G * S["beta0"] * (S["lam"] ** (L - 1))
        rows.append({"L": L, "rel": float(np.linalg.norm(r) / unit),
                     "two_ck_sqrt": 2 * S["ck"] * math.sqrt(max(L - 1, 0))})
    return rows


def geo_sum(OA, a, N):
    d = OA.shape[0]
    A = a * OA

    def rec(n):
        if n == 0:
            return np.zeros((d, d)), np.eye(d)
        if n == 1:
            return np.eye(d), A.copy()
        if n % 2 == 0:
            S, P = rec(n // 2)
            return S + P @ S, P @ P
        S, P = rec(n - 1)
        return S + P, A @ P

    S, _ = rec(N)
    return S


def chart_diff(S, C, Q, Z):
    d, T = S["d"], Q.shape[0]
    amp = 0.055
    baseline = np.array([0.25 if i % 2 == 0 else -0.25 for i in range(d)])
    ck = 1 / (math.sqrt(S["k"]) - 1)

    def latent_of(coef):
        field = np.tanh(math.sqrt(T * d) * (Q @ coef @ Z.T))
        return baseline + amp * (field - field.mean(axis=1, keepdims=True))

    def gates_of(lat):
        G = np.zeros((T, d))
        phys = np.zeros((T, S["k"]))
        for t in range(T):
            rot = np.roll(lat[t], t)
            common = ck * rot[0]
            cyc = rot[1:] + common
            G[t, : d - 1] = 1 - cyc ** 2
            G[t, -1] = 1 - common ** 2
            tmp = np.zeros(S["k"])
            tmp[:d] = rot
            phys[t] = S["U"] @ tmp
        return G, phys

    def endpoint(G):
        C0 = geo_sum(S["OA"], S["a"], 3 * S["n"])
        s = (1 - S["a"] ** (3 * S["n"])) / (1 - S["a"])
        M = C0
        I = np.eye(d)
        for g in G:
            M = g[:, None] * (S["a"] * S["OA"] @ M + I)
            s = float(g[-1]) * (S["a"] * s + 1.0)
        return S["a"] * S["OA"] @ M + I, S["a"] * s + 1.0

    def inputs(phys):
        # previous state at the start of the active window: memory 0, source 0.4
        a, k, n = S["a"], S["k"], S["n"]
        delta = 1 / (100 * n)
        H = np.full(n - k, 0.4)
        prev = np.concatenate([np.zeros(k), H])
        # R0
        def Rmul(h):
            out = np.zeros_like(h)
            out[:k] = a * (S["O"] @ h[:k])
            out[k:] = delta * h[k:]
            return out
        xs = []
        mx = 0.0
        for t in range(phys.shape[0]):
            h = np.concatenate([phys[t], H])
            # clip for atanh domain
            if np.max(np.abs(h)) >= 1:
                return {"max_input": float("inf"), "endpoint": float("inf"), "max_h": float(np.max(np.abs(h)))}
            x = np.arctanh(h) - Rmul(prev) - 0.05
            mx = max(mx, float(np.max(np.abs(x))))
            xs.append(x)
            prev = h
        x = -Rmul(prev) - 0.05
        mx = max(mx, float(np.max(np.abs(x))))
        hend = np.tanh(Rmul(prev) + x + 0.05)
        return {"max_input": mx, "endpoint": float(np.max(np.abs(hend))),
                "max_h": float(np.max(np.abs(phys)))}

    lp, lm = latent_of(C), latent_of(-C)
    Gp, hp = gates_of(lp)
    Gm, hm = gates_of(lm)
    Cp, sp = endpoint(Gp)
    Cm, sm = endpoint(Gm)
    return Cp - Cm, float(sp - sm), inputs(hp), inputs(hm), lp, lm


def r1_ub_and_lb(S, dC, ds):
    rows = np.linalg.norm(dC.T @ S["Theta"], axis=0)
    M = max(float(np.linalg.norm(dC, 2)), abs(ds))
    d = S["d"]
    w0 = S_G * math.sqrt(1 - 1 / S["k"])
    wc = 2 * S["ck"] * S_G * math.sqrt(1 - 2 / S["k"])
    lam, b0, a = S["lam"], S["beta0"], S["a"]
    acc = 0.0
    best_u, best_l, Lu, Ll = 0.0, 0.0, 1, 1
    Lmax = 4 * d
    for L in range(1, Lmax + 1):
        acc += w0 if ((-(L - 1)) % d) == 0 else wc
        R = min(a * b0 * (lam ** (L - 1)) * acc, 2 * b0 * (lam ** L))
        spike = b0 * (lam ** L) * rows[(-L) % d]
        ub = spike + R * M
        if ub > best_u:
            best_u, Lu = ub, L
        if spike > best_l:
            best_l, Ll = spike, L
    # tail
    Lt = Lmax + 1
    acc2 = acc + (w0 if ((-(Lt - 1)) % d) == 0 else wc)
    Rtail = min(a * b0 * (lam ** (Lt - 1)) * acc2, 2 * b0 * (lam ** Lt))
    tail = b0 * (lam ** Lt) * float(rows.max()) + Rtail * M
    ub = S["scale"] * max(best_u, tail)
    lb = S["scale"] * best_l
    # constant-gate check at Ll
    G = np.full((Ll, S["k"]), G_HI)
    y = propagate_latent(S, G)
    z = S["V"].T @ (S["U"] @ y)
    dist = S["scale"] * float(np.linalg.norm(dC.T @ z))
    return {"UB1": ub, "LB_formula": lb, "LB_L": Ll, "UB_L": Lu,
            "constant_gate_distance": dist, "kappa": S["a"] * S["scale"] * M}


def sdp_upper(S, dC, ds, seed=0):
    k, d, n, a = S["k"], S["d"], S["n"], S["a"]
    W = dC.T @ S["OA"].T @ S["V"].T
    Q = W.T @ W
    L = S["L"]
    PZ = np.zeros((k, k))
    PZ[d:, d:] = np.eye(L) - np.ones((L, L)) / L
    Q = Q + (ds ** 2) * PZ
    mid = 0.5 * (G_HI + G_LO)
    m = np.full(k, mid)
    Qt = np.zeros((k + 1, k + 1))
    Qt[0, 0] = m @ Q @ m
    Qt[0, 1:] = Qt[1:, 0] = S_G * (Q @ m)
    Qt[1:, 1:] = S_G ** 2 * Q
    N = Qt.shape[0]
    rng = np.random.default_rng(seed)
    Y = rng.normal(size=(N, 16))
    Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    step = 1.0 / (np.max(np.abs(np.linalg.eigvalsh(Qt))) + 1e-30)
    for _ in range(400):
        Y = Y + step * (Qt @ Y)
        Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    mu = np.einsum("ij,ji->i", Qt, Y @ Y.T)
    lmin = float(np.linalg.eigvalsh(np.diag(mu) - Qt)[0])
    if lmin < 0:
        mu = mu - lmin * (1 + 1e-9) - 1e-12
    lmin2 = float(np.linalg.eigvalsh(np.diag(mu) - Qt)[0])
    # one vertex lower
    g = np.where(np.ones(k) > 0, G_HI, G_LO)
    # a few sign passes
    for _ in range(6):
        z = W @ g
        dN = g[d:] - g[d:].mean()
        grad = 2 * W.T @ z
        grad[d:] += 2 * (ds ** 2) * dN
        g = np.where(grad > 0, G_HI, G_LO)
    val = float((W @ g) @ (W @ g) + (ds ** 2) * np.sum((g[d:] - g[d:].mean()) ** 2))
    ub = S["scale"] * (a / math.sqrt(n)) * math.sqrt(float(mu.sum()))
    lo = S["scale"] * (a / math.sqrt(n)) * math.sqrt(max(val, 0.0))
    return {"sdp_upper": ub, "vertex_lower_rough": lo, "ratio": ub / lo if lo else None,
            "dual_min_eig": lmin2}


PAIRS = [
    (200, "chart_q_200_q2_rand_0_padded6.npy", "screen_200_200_6_sustained_spread.npz", 6),
    (200, "chart_adv2_200_ub_prev_screen_0.npy", "screen_200_200_6_sustained_spread.npz", 6),
    (200, "chart_adv2_200_ub_prev_random_0.npy", "screen_200_200_6_sustained_spread.npz", 6),
    (200, "chart_adv2_200_ub_random_5.npy", "screen_200_200_6_sustained_spread.npz", 6),
    (200, "chart_adv2_200_ub_prev_screen_3.npy", "screen_200_200_6_sustained_spread.npz", 6),
    (400, "chart_q_400_q2_rand_2_padded6.npy", "screen_400_400_6_sustained_spread.npz", 6),
    (400, "chart_p4c_400_chart_adv2_400_ub_random_1.npy", "screen_400_400_6_sustained_spread.npz", 6),
    (400, "chart_p4c_400_chart_adv2_400_ub_random_2.npy", "screen_400_400_6_sustained_spread.npz", 6),
    (400, "chart_p4c_400_chart_adv2_400_ub_prev_codex_kappa_opt_1.npy", "screen_400_400_6_sustained_spread.npz", 6),
    (400, "chart_p4d_400_rand21_1.npy", "screen_400_400_6_sustained_spread.npz", 6),
    (1000, "chart_p5full_1000_chart_q_1000_q2_s500_rand_0_padded7.npy", "screen_1000_1000_7_sustained_spread.npz", 7),
]


def audit_pairs():
    out = []
    cache = {}
    for n, fn, screen, qfull in PAIRS:
        C = np.load(CLAUDE / fn)
        if screen not in cache:
            z = np.load(CODEX / screen)
            cache[screen] = (z["Q"], z["Z"])
        Q, Z = cache[screen]
        S = build(n)
        dC, ds, ip, im, lp, lm = chart_diff(S, C, Q, Z)
        br = r1_ub_and_lb(S, dC, ds)
        # membership
        row_norms = np.linalg.norm(C, axis=1) if C.ndim == 2 else np.array([np.linalg.norm(C)])
        rec = {
            "file": fn, "n": n,
            "shape": list(C.shape),
            "coeff_norm": float(np.linalg.norm(C)),
            "row_norms": [float(x) for x in row_norms],
            "nonzero_rows": int(np.sum(row_norms > 1e-12)),
            "Q_shape": list(Q.shape), "Z_shape": list(Z.shape),
            "dC_op": float(np.linalg.norm(dC, 2)),
            "ds": ds,
            "UB1_2eps": br["UB1"] / TWO,
            "LB_const_2eps": br["constant_gate_distance"] / TWO,
            "LB_formula_2eps": br["LB_formula"] / TWO,
            "LB_vs_const_abs": abs(br["LB_formula"] - br["constant_gate_distance"]),
            "kappa_2eps": br["kappa"] / TWO,
            "max_input_plus": ip["max_input"],
            "max_input_minus": im["max_input"],
            "endpoint_plus": ip["endpoint"],
            "endpoint_minus": im["endpoint"],
            "max_h_plus": ip["max_h"],
            "max_h_minus": im["max_h"],
            "R1_certifies": bool(br["UB1"] + 1e-8 < TWO),
            "const_matches_formula": bool(abs(br["LB_formula"] - br["constant_gate_distance"]) < 1e-8),
        }
        out.append(rec)
        print(fn, "UB1", round(rec["UB1_2eps"], 4), "LBconst", round(rec["LB_const_2eps"], 4),
              "in", round(max(ip["max_input"], im["max_input"]), 4), "norm", round(rec["coeff_norm"], 6),
              "rows", rec["nonzero_rows"], flush=True)
    return out


def main():
    report = {}
    print("frame", flush=True)
    report["frame"] = [check_frame(n) for n in (200, 400, 1000)]
    print(json.dumps(report["frame"]), flush=True)
    print("phi/r3", flush=True)
    report["r3"] = [r3_violation_search(n, trials=2000, seed=n) for n in (200, 400)]
    print(json.dumps(report["r3"]), flush=True)
    print("horizon", flush=True)
    report["horizon"] = [r1_absolute_sup(n) for n in (200, 400, 1000, 2400, 4000)]
    for h in report["horizon"]:
        print(h["n"], "sup", h["sup"], "arg", h["argL"], "A2/A1", h["A2_over_A1"], "L1", h["L1"], flush=True)
    print("wake", flush=True)
    report["wake_200"] = wake_family(200, [2, 8, 16, 48])
    report["wake_4000"] = wake_family(4000, [2, 8, 64, 128])
    print(json.dumps({"200": report["wake_200"], "4000": report["wake_4000"]}), flush=True)
    print("pairs", flush=True)
    report["pairs"] = audit_pairs()
    # SDP on the headline collisions and one separated old-style pair if present
    print("sdp", flush=True)
    sdp = []
    for n, fn, screen, _q in PAIRS[:3] + PAIRS[5:6] + PAIRS[-1:]:
        C = np.load(CLAUDE / fn)
        Q, Z = np.load(CODEX / screen)["Q"], np.load(CODEX / screen)["Z"]
        S = build(n)
        dC, ds, *_ = chart_diff(S, C, Q, Z)
        r = sdp_upper(S, dC, ds)
        r["file"] = fn
        sdp.append(r)
        print(fn, json.dumps({k: r[k] for k in ("sdp_upper", "vertex_lower_rough", "ratio", "dual_min_eig")}), flush=True)
    report["sdp"] = sdp
    (OUT / "audit.json").write_text(json.dumps(report, indent=1))
    print("wrote audit.json", flush=True)


if __name__ == "__main__":
    main()
