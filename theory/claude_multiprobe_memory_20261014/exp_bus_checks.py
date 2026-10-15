"""Exact-identity and bound checks for the PR #28 repairs and the bus analysis (CPU, < 1 min).

A. Local skeleton: for x with x_0 = 0, O x = S x + 1 J(x) + (gamma/sqrt k) e_1 Sum(x),
   where S has NO image of e_(d-1) (own-injection paths terminate at row d-1).
B. Row 0: (R0^T g)_0 = a g_0 for every g; reference row-0 credit stays exactly 0.
C. U-coordinate gating formula (Lemma 7.1): for i >= 1,
   (U G U v)_i = g_i v_i + (gamma/sqrt k)(w^T v)(g_i - gamma w^T G w) + (gamma/sqrt k)(w^T G v).
D. U-coordinate credit dynamics: y_t = (U G_t U)(a P y_(t-1) + c U e_r) reproduces U B_t e_r.
F. Rank-two coupling split (Lemma 7.1(c), corrected leak coefficient gamma/sqrt k) and the
   broadcast-mode update Y(0) = gamma Gamma V(0) - w^T G V.
E. Multi-step legal readout weights: max |nu_i| over memory rows outside {0, d-1, ..., d-F}
   for random and adversarially correlated future gates, F = 1..40.
Run: python -I exp_bus_checks.py   (writes exp_bus_checks_result.json)
Numerical checks of exact identities and finite samples only; not proofs of the lemmas.
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def mats(k, d):
    gam = 1 / (1 - 1 / math.sqrt(k))
    u = np.ones(k) / math.sqrt(k)
    w = -u.copy(); w[0] += 1
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.zeros((k, k))
    for j in range(1, d):
        P[j, j - 1] = 1
    P[0, d - 1] = 1
    for j in range(d, k):
        P[j, j] = 1
    O = U @ P @ U
    S = np.zeros((k, k))           # local skeleton on rows >= 1
    for j in range(1, d - 1):
        S[j + 1, j] = 1            # e_j -> e_(j+1), 1 <= j <= d-2 ; no image of e_(d-1)
    for j in range(d, k):
        S[j, j] = 1
    return gam, u, w, U, P, O, S


def check_A(k, d, rng):
    gam, u, w, U, P, O, S = mats(k, d)
    err = 0.0
    for _ in range(5):
        x = rng.standard_normal(k); x[0] = 0
        J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * x[1:].sum() / k
        pred = S @ x
        pred[1:] += J
        pred[1] += gam * x[1:].sum() / math.sqrt(k)
        err = max(err, np.abs(O @ x - pred)[1:].max(), abs((O @ x)[0]))
    no_image = np.abs(S[:, d - 1]).max()
    return {"k": k, "local_skeleton_err": err, "S_column_d-1_max": float(no_image)}


def check_B(n, rng):
    k, d = n // 2, n // 4
    gam, u, w, U, P, O, S = mats(k, d)
    a = 1 - 1 / n
    g = rng.uniform(LO, HI, k)
    nu0 = (a * O.T @ g)[0]
    # reference row-0 credit
    B = np.zeros((k, k)); E = np.eye(k); E[0, 0] = 0
    for t in range(50):
        G = rng.uniform(0.2, 1.0, k)
        B = G[:, None] * (a * O @ B + E)
    return {"n": n, "row0_weight_err": abs(nu0 - a * g[0]), "row0_credit_max": float(np.abs(B[0]).max())}


def check_C(k, d, rng):
    gam, u, w, U, P, O, S = mats(k, d)
    err = 0.0
    for _ in range(5):
        g = rng.uniform(0, 1, k); G = np.diag(g)
        v = rng.standard_normal(k)
        lhs = U @ G @ U @ v
        rhs = g * v + (gam / math.sqrt(k)) * (w @ v) * (g - gam * (w @ G @ w)) + (gam / math.sqrt(k)) * (w @ G @ v)
        err = max(err, np.abs(lhs - rhs)[1:].max())
    return {"k": k, "UGU_formula_err_rows>=1": err}


def check_D(k, d, rng):
    gam, u, w, U, P, O, S = mats(k, d)
    a = 1 - 1 / (2 * k)
    r = 5
    x = np.zeros(k); y = np.zeros(k)
    err = 0.0
    for t in range(60):
        g = rng.uniform(0.3, 1.0, k); G = np.diag(g); c = rng.uniform(0.5, 1.5)
        er = np.zeros(k); er[r] = 1
        x = G @ (a * O @ x + c * er)
        y = (U @ G @ U) @ (a * P @ y + c * U @ er)
        err = max(err, np.abs(U @ x - y).max())
    return {"k": k, "U_credit_dynamics_err": err, "u_dot_y": float(abs(u @ y))}


def check_F(k, d, rng):
    """Lemma 7.1(b),(c): U G U = ghat I + D + X with D = diag(0, delta), and on credit-like V
    (u^T V = 0) the coupling splits as
    X V = (gam/sqrt k) delta (x) V_0 + (gam/sqrt k) w (x) sum_j delta_j V_j + gam^2 (sum delta/k) w (x) V_0;
    the broadcast-mode capture coefficient of U-coordinate i >= 1 is (gam/sqrt k)(delta_i - gam sum delta/k)."""
    gam, u, w, U, P, O, S = mats(k, d)
    err_split, err_cap, err_y0 = 0.0, 0.0, 0.0
    for _ in range(5):
        ghat = rng.uniform(.99, .9994)
        delta = rng.uniform(-.4, .0006, k); delta[0] = 0
        G = np.diag(ghat + delta)
        X = U @ G @ U - ghat * np.eye(k) - np.diag(delta)
        V = rng.standard_normal((k, 3)); V -= np.outer(u, u @ V)       # u^T V = 0
        sd = delta.sum()
        split = (gam / math.sqrt(k)) * np.outer(delta, V[0]) \
            + (gam / math.sqrt(k)) * np.outer(w, delta @ V) \
            + gam ** 2 * (sd / k) * np.outer(w, V[0])
        err_split = max(err_split, np.abs(X @ V - split).max())
        # capture coefficient of the broadcast mode V_0 on U-coordinates i >= 1 (consequence of the split)
        coef = (gam / math.sqrt(k)) * delta[1:] + gam ** 2 * (sd / k) * w[1:]
        err_cap = max(err_cap, np.abs(coef - (gam / math.sqrt(k)) * (delta[1:] - gam * sd / k)).max())
        Gm = ghat + delta; Gm[0] = ghat
        Gam = w @ (Gm * w)
        y0 = (U @ np.diag(Gm) @ U @ V)[0]
        err_y0 = max(err_y0, np.abs(y0 - (gam * Gam * V[0] - w @ (Gm[:, None] * V))).max())
    return {"k": k, "X_split_err": err_split, "capture_coeff_err": err_cap, "Y0_update_err": err_y0}


def check_E(n, rng, Fmax=40):
    k, d = n // 2, n // 4
    gam, u, w, U, P, O, S = mats(k, d)
    a = 1 - 1 / n
    out = []
    for mode in ["random", "correlated"]:
        worst = {}
        for F in range(1, Fmax + 1):
            gates = [rng.uniform(LO, HI, k) for _ in range(F)]
            phi = gates[-1] * np.ones(k)
            for j in range(F - 2, -1, -1):
                nu_j = a * O.T @ phi
                if mode == "correlated":   # future gates chosen to correlate with current weights
                    gj = np.where(nu_j > np.median(nu_j), HI, LO)
                else:
                    gj = gates[j]
                phi = gj * nu_j
            nu = a * O.T @ phi
            exc = {0} | {d - 1 - j for j in range(F)}
            mask = np.array([i not in exc for i in range(k)])
            worst[F] = float(np.abs(nu[mask]).max())
        out.append({"mode": mode, "max_nonexceptional_weight_by_F": worst,
                    "overall_max": max(worst.values())})
    return {"n": n, "results": out}


def main():
    rng = np.random.default_rng(7)
    res = {
        "A": [check_A(50, 25, rng), check_A(400, 200, rng)],
        "B": [check_B(200, rng), check_B(800, rng)],
        "C": [check_C(50, 25, rng), check_C(400, 200, rng)],
        "D": [check_D(50, 25, rng), check_D(300, 150, rng)],
        "E": [check_E(800, rng), check_E(4000, rng)],
        "F": [check_F(50, 25, rng), check_F(400, 200, rng), check_F(2000, 1000, rng)],
    }
    for r in res["A"]:
        assert r["local_skeleton_err"] < 1e-11 and r["S_column_d-1_max"] == 0
    for r in res["B"]:
        assert r["row0_weight_err"] < 1e-12 and r["row0_credit_max"] < 1e-12
    for r in res["C"]:
        assert r["UGU_formula_err_rows>=1"] < 1e-11
    for r in res["D"]:
        assert r["U_credit_dynamics_err"] < 1e-9
    for r in res["F"]:
        assert r["X_split_err"] < 1e-11 and r["capture_coeff_err"] < 1e-14 and r["Y0_update_err"] < 1e-11
    with open(os.path.join(HERE, "exp_bus_checks_result.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({kk: v for kk, v in res.items() if kk != "E"}, indent=1))
    for r in res["E"]:
        for m in r["results"]:
            print("E", r["n"], m["mode"], "overall max non-exceptional weight:", round(m["overall_max"], 4))


if __name__ == "__main__":
    main()
