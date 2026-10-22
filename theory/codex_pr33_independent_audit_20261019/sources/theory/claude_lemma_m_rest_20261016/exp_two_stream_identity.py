"""Exact check of the two-stream representation of the bus (Lemma M_rest note, Prop. S1).

For the R0-skeleton credit B'_t = G_t (a O B'_(t-1) + c_t E) with ARBITRARY gates (row 0
included), Y = U B', own O (local skeleton), Z = Y - O (Z(0) = Y(0)), and ANY query vector chi
on the k U-rows, the script verifies

    chi^T Z_T  =  sum_t [ C_t(chi) a_t  -  R_t(chi) lhat_t ]                      (S1)

with the two streams (common to all rows)
    a_t    = a Y_(t-1)(d-1)                          (broadcast arrival)
    lhat_t = (gamma/k) sum_(j>=1) delta_t(j) V_t(j) + (gamma/k) c_t g_t^T   (leak + w-injection),
V_t = a P Y_(t-1), delta = g - ghat (any reference scalar ghat_t), and the scalar coefficients
    C_t = sum_i chi_i rho^(i)_t kappa_t(p^i_t)  +  entry/row-0 terms,
    R_t = sum_i chi_i rho^(i)_t                 -  (sqrt(k)/gamma) * entry/row-0 terms,
built from the paths p^i of the U-rows. It also checks the row-0 (broadcast) formula
    Y_t(0) = (ghat_t + gamma S_t/k + e0_t) a_t + (sqrt(k)/gamma) lhat_t ,  S_t = sum_(j>=1) delta_t(j),
where e0_t is a possible row-0 gate-deviation coefficient; the fit shows e0 = 0 (the row-0
gate multiplies B'(0) = 0 and never enters).
Exact algebra; residuals are floating-point only.
Run: python -I exp_two_stream_identity.py
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def mats(k, d):
    gam = 1 / (1 - 1 / math.sqrt(k)); u = np.ones(k) / math.sqrt(k)
    w = -u.copy(); w[0] += 1
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.zeros((k, k))
    for j in range(0, d - 1):
        P[j + 1, j] = 1.0
    P[0, d - 1] = 1.0
    for j in range(d, k):
        P[j, j] = 1.0
    return gam, U, P, U @ P @ U


def pred(i, d):
    """predecessor U-row of i under the shift (row whose content moves into i)."""
    if i == 0:
        return d - 1
    if i < d:
        return i - 1          # i = 1 receives from row 0
    return i


def run(n, T, rng, row0_dev):
    k, d = n // 2, n // 4; a = 1 - 1 / n
    gam, U, P, O = mats(k, d)
    sk = math.sqrt(k)
    # gates: bath reference ghat_t, holes (g ~ 1), driven rows (g in [.75,.95]), row 0 optional deviation
    ghat = rng.uniform(.95, .999, size=T + 1)
    G = np.empty((T + 1, k))
    for t in range(1, T + 1):
        g = np.full(k, ghat[t])
        m = rng.integers(0, 6)
        idx = rng.choice(np.arange(1, k), size=m, replace=False)
        g[idx] = rng.uniform(.75, 1.0, size=m)
        if row0_dev:
            g[0] = rng.uniform(.8, 1.0)
        G[t] = g
    c = np.concatenate([[0.0, 0.0], rng.uniform(.5, 1.0, size=T - 1)])
    E = np.eye(k); E[0, 0] = 0.0
    Bp = np.zeros((k, k)); Own = np.zeros((k, k))
    Ys = [np.zeros((k, k))]; Os = [np.zeros((k, k))]
    for t in range(1, T + 1):
        g = G[t]
        Bp = g[:, None] * (a * O @ Bp + c[t] * E)
        On = np.zeros((k, k))
        On[2:d] = g[2:d, None] * a * Own[1:d - 1]
        On[d:] = g[d:, None] * a * Own[d:]
        ii = np.arange(1, k); On[ii, ii] += c[t] * g[1:]
        Own = On
        Ys.append(U @ Bp); Os.append(Own.copy())
    # streams
    avec = [None]; lhat = [None]; S = np.zeros(T + 1); dl = np.zeros((T + 1, k))
    row0_res = 0.0; e0fit = []
    for t in range(1, T + 1):
        g = G[t]; delta = g - ghat[t]; delta_m = delta.copy(); delta_m[0] = 0.0
        S[t] = delta_m.sum(); dl[t] = delta
        V = a * P @ Ys[t - 1]
        at = V[0].copy()                      # = a Y_(t-1)(d-1)
        gcol = g.copy(); gcol[0] = 0.0
        lh = (gam / k) * (delta_m @ V) + (gam / k) * c[t] * gcol
        avec.append(at); lhat.append(lh)
        # row-0 check: Y_t(0) - (ghat + gamma S/k) a_t - (sqrt k/gamma) lhat_t = e0 * a_t ?
        r = Ys[t][0] - (ghat[t] + gam * S[t] / k) * at - (sk / gam) * lh
        nrm = float(at @ at)
        e0 = float(r @ at / nrm) if nrm > 0 else 0.0
        e0fit.append((t, e0, float(delta[0])))
        row0_res = max(row0_res, float(np.abs(r - e0 * at).max()))
    # PROOF.md Prop. S1(b): the row-0 gate does not enter (B'(0) = 0), so e0 must vanish.
    # fit e0 = alpha * delta_0 by least squares across times
    xs = np.array([d0 for (_, _, d0) in e0fit]); ys = np.array([e0 for (_, e0, _) in e0fit])
    alpha = float(xs @ ys / (xs @ xs)) if (xs @ xs) > 0 else 0.0
    e0_lin_res = float(np.abs(ys - alpha * xs).max()) if (xs @ xs) > 0 else float(np.abs(ys).max())

    def e0coef(t):
        return alpha * dl[t][0]

    # representation for random chi
    worst = 0.0
    for _ in range(3):
        chi = rng.normal(size=k)
        Ccoef = np.zeros(T + 1); Rcoef = np.zeros(T + 1)
        # row 0 at T
        Ccoef[T] += chi[0] * (ghat[T] + gam * S[T] / k + e0coef(T))
        Rcoef[T] -= chi[0] * sk / gam
        for i in range(1, k):
            rho = 1.0; p = i; t = T
            while t >= 1:
                g = G[t]; delta = g[p] - ghat[t]
                kap = (gam / sk) * (delta - gam * S[t] / k)
                Ccoef[t] += chi[i] * rho * kap
                Rcoef[t] += chi[i] * rho
                q = pred(p, d)
                if q == 0:                          # entry: rho_t g_1(t) a Y_(t-1)(0)
                    if t - 1 >= 1:
                        f = chi[i] * rho * g[p] * a
                        Ccoef[t - 1] += f * (ghat[t - 1] + gam * S[t - 1] / k + e0coef(t - 1))
                        Rcoef[t - 1] -= f * sk / gam
                    break
                rho *= a * g[p]; p = q; t -= 1
        rhs = np.zeros(k)
        for t in range(1, T + 1):
            rhs += Ccoef[t] * avec[t] - Rcoef[t] * lhat[t]
        Z = Ys[T] - Os[T]
        lhs = chi @ Z
        worst = max(worst, float(np.abs(lhs - rhs).max() / max(1e-300, np.abs(lhs).max())))
    return {"n": n, "T": T, "row0_dev": row0_dev, "rel_residual_S1": worst,
            "row0_formula_max_residual": row0_res, "e0_over_delta0_fit": alpha,
            "e0_linear_fit_residual": e0_lin_res}


def main():
    rng = np.random.default_rng(11)
    out = []
    for n, T in ((64, 70), (200, 160)):
        for row0 in (False, True):
            rec = run(n, T, rng, row0)
            print(json.dumps(rec)); out.append(rec)
    with open(os.path.join(HERE, "exp_two_stream_identity_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()


def creation_check(n=64, T=60, seed=5):
    """Prop. S5: Z_t - M_t Z_(t-1) = (U D U - D) a P O_(t-1) + e0 (x) g_0 a O_(t-1)(d-1) + (c gamma/sqrt k) w (x) g^T E,
    with M_t = U G_t U a P (exact, any gates), D = diag(g - ghat) for any scalar ghat."""
    rng = np.random.default_rng(seed)
    k, d = n // 2, n // 4; a = 1 - 1 / n
    gam, U, P, O = mats(k, d); sk = math.sqrt(k)
    w = -np.ones(k) / sk; w[0] += 1
    E = np.eye(k); E[0, 0] = 0.0
    Bp = np.zeros((k, k)); Own = np.zeros((k, k)); Zprev = np.zeros((k, k)); worst = 0.0
    for t in range(1, T + 1):
        g = rng.uniform(.6, 1.0, size=k); c = rng.uniform(.5, 1.0); ghat = rng.uniform(.9, 1.0)
        Bp = g[:, None] * (a * O @ Bp + c * E)
        On = np.zeros((k, k)); On[2:d] = g[2:d, None] * a * Own[1:d - 1]; On[d:] = g[d:, None] * a * Own[d:]
        ii = np.arange(1, k); On[ii, ii] += c * g[1:]
        Y = U @ Bp; Z = Y - On
        M = U @ np.diag(g) @ U @ (a * P)
        Dm = np.diag(g - ghat)
        xi = (U @ Dm @ U - Dm) @ (a * P @ Own)
        xi[0] += g[0] * a * Own[d - 1]
        gE = g.copy(); gE[0] = 0.0
        xi += (c * gam / sk) * np.outer(w, gE)
        res = Z - M @ Zprev - xi
        worst = max(worst, float(np.abs(res).max() / max(1.0, np.abs(Z).max())))
        Own = On; Zprev = Z
    return worst


if __name__ == "__main__":
    print(json.dumps({"S5_creation_rel_residual": creation_check(64), "S5_creation_rel_residual_n200": creation_check(200, 50)}))
