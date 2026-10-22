"""Checks for Proposition R1 and Lemma R (PROOF.md section 3.2).

(R1) Exact all-order creation for an off-cycle credit column j: with the TRUE U-row map
     M_t = U G_t U a P (no zero-sum assumption),
         Z_t(., j) = M_t Z_(t-1)(., j) + xi_t,
         xi_t = (gamma/sqrt k) [ (a delta_t(j) O_(t-1)(j) + c_t g_t(j)) w + a O_(t-1)(j) U Delta_t w ],
     where Delta_t = G_t - ghat_t I.  Checked at n = 512, 1024 on random adversarial histories.
(R2) Lemma R: for every one-step legal query chi = a P^T U g and every t <= T,
         | chi^T Phi^U(T, t) w |  <=  HI + HI sqrt(k) (g_1max + gamma sqrt(2)/sqrt(k)),
     where g_1max is the largest front-row gate after t. Evaluated by back-propagating chi
     (adjoint of M) at n = 65536 with T = 1500, holes, a held gather spike and random drives.
Finite-precision evidence only; the statements are proved in PROOF.md.
Run: python -I lemma_r_check.py   (writes lemma_r_check_result.json)
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def OT_apply(x, k, d, gam):
    """O^T x (O orthogonal): adjoint of O_apply, derived from its formula."""
    sk = math.sqrt(k)
    # O x = S x + 1_{>=1} J(x) + (gam/sqrt k) e1 sp(x), with S the local shift; J(x) = gam x_(d-1)/sk - gam^2 sp/k
    y = np.zeros_like(x); y[0] = x[0]
    y[1:d - 1] += x[2:d]; y[d:] += x[d:]
    s1 = x[1:].sum(0)                                   # coefficient of J
    y[d - 1] += gam * s1 / sk
    y[1:] += -gam ** 2 * s1 / k + gam * x[1] / sk
    return y


def U_apply(x, k):
    sk = math.sqrt(k); gam = 1 / (1 - 1 / sk)
    w = -np.ones(k) / sk; w[0] += 1
    return x - gam * np.multiply.outer(w, w @ x) if x.ndim == 2 else x - gam * w * (w @ x)


def P_apply(x, k, d):
    y = np.empty_like(x); y[1:d] = x[0:d - 1]; y[0] = x[d - 1]; y[d:] = x[d:]
    return y


def PT_apply(x, k, d):
    y = np.empty_like(x); y[0:d - 1] = x[1:d]; y[d - 1] = x[0]; y[d:] = x[d:]
    return y


def check_R1(n, T, seed):
    rng = np.random.default_rng(seed)
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); w = -np.ones(k) / sk; w[0] += 1
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    js = [d + 3, d + 10, k - 5]                         # off-cycle columns (driven, held, bath)
    h = np.zeros(n); B = np.zeros((k, len(js))); Oown = np.zeros(len(js)); Zrec = np.zeros((k, len(js)))
    s = 0.0; worst = 0.0
    for t in range(1, T + 1):
        hm = h[:k]
        Jt = gam * hm[d - 1] / sk - gam ** 2 * hm[1:].sum() / k
        s = math.tanh(.05 + a * Jt + a * s)
        pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r in rng.choice(np.arange(2, k), size=12, replace=False):
            hn[r] = rng.uniform(-.9, .9)
        if 50 <= t <= 2 * T // 3:
            hn[d + 10] = 0.0                            # a held off-cycle hole (column js[1])
        if t % 7 == 0:
            hn[d + 3] = .3 * (-1) ** (t // 7)           # a driven off-cycle row (column js[0])
        ghat = 1 - s * s; g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * O_apply(B, k, d, gam); Bn[js, np.arange(len(js))] += c; Bn *= gm[:, None]
        On = gm[js] * (a * Oown + c)
        # exact creation with the true U-map: Z_t = M_t Z_(t-1) + xi_t
        Delta = gm - ghat
        UDw = U_apply(Delta * w, k)
        xi = np.empty((k, len(js)))
        for q, j in enumerate(js):
            xi[:, q] = (gam / sk) * ((a * Delta[j] * Oown[q] + c * gm[j]) * w + a * Oown[q] * UDw)
        Zrec = U_apply(gm[:, None] * U_apply(a * P_apply(Zrec, k, d), k), k) + xi
        B, Oown, h = Bn, On, hn
        Y = U_apply(B, k); Z = Y.copy()
        for q, j in enumerate(js):
            Z[j, q] -= Oown[q]
        worst = max(worst, float(np.abs(Z - Zrec).max()) / max(1e-300, float(np.abs(Z).max())))
    return worst


def check_R2(n, T, seed, nq=6):
    rng = np.random.default_rng(seed)
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); w = -np.ones(k) / sk; w[0] += 1
    h = np.zeros(n); gates = np.zeros((T + 1, k), dtype=np.float32)
    for t in range(1, T + 1):
        pre = np.empty(n); pre[:k] = a * O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r in rng.choice(np.arange(2, k), size=40, replace=False):
            hn[r] = rng.uniform(-.9, .9)
        r_sp = d - 1 - (T - t)
        if 2 <= r_sp <= d - 1:
            hn[r_sp] = 0.0                               # held gather spike
        if t > T // 3:
            hn[d + 100:d + 400] = 0.0                    # 300 off-cycle holes
        gates[t] = (1 - hn[:k] ** 2).astype(np.float32); h = hn
    g1max_after = np.maximum.accumulate(gates[::-1, 1])[::-1]   # max_(u >= t) g_1(u)
    worst_ratio = 0.0; worst_abs = 0.0
    for qi in range(nq):
        gq = rng.uniform(LO, HI, k) if qi % 3 else np.where(rng.random(k) < .5, LO, HI)
        if qi == 0:
            gq = np.full(k, HI)
        chi = a * PT_apply(U_apply(gq, k), k, d)                 # one-step query, U-coordinates
        x = chi.copy()                                           # x_t = Phi^U(T,t)^T chi
        for t in range(T, 0, -1):
            val = float(x @ w)
            bound = HI + HI * sk * (float(g1max_after[t + 1]) if t < T else 0.0) + HI * gam * math.sqrt(2) if t < T else HI + .35
            worst_ratio = max(worst_ratio, abs(val) / bound); worst_abs = max(worst_abs, abs(val))
            # adjoint of M_t = U G_t U a P:  M_t^T x = a P^T U G_t U x
            x = a * PT_apply(U_apply(gates[t].astype(float) * U_apply(x, k), k), k, d)
    return worst_ratio, worst_abs, float(gates[1:, 1].max())


def main():
    out = {}
    for (n, T, seed) in ((512, 260, 1), (1024, 400, 2)):
        out[f"R1 relative residual n={n}"] = check_R1(n, T, seed); print(json.dumps(out))
    r, va, g1 = check_R2(65536, 1500, 3)
    out["R2 n=65536: max |chi^T Phi w| / bound"] = r
    out["R2 n=65536: max |chi^T Phi w|"] = va
    out["R2 n=65536: max front gate g_1"] = g1
    print(json.dumps(out))
    json.dump(out, open(os.path.join(HERE, "lemma_r_check_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
