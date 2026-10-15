"""Exact-identity checks for the Hypothesis B investigation (numpy, CPU, seconds).

I1. Uniform-query U-gather: for future gates g*1, chi := U (a O^T g 1_k) = a g sqrt(k) e_(d-1);
    for F future steps (Lemma 1.1) chi_F = (a g)^F sqrt(k) e_(d-F) (checked for F = 2, 3, 7).
I2. Structured O and O^T (skeleton + broadcast + front) agree with dense U P U.
I3. Hole capture coefficient: if row i has gate 1 at step t, the U-coordinate update of i is
    Y_t(i) = a Y_(t-1)(i-1) + kap * Y_(t-1)(d-1) - (gam a/k) sum_(j>=1) g_j Y_(t-1)(pi^-1 j)
             + c_t [U G_t E](i,:),
    kap = (gam a/sqrt k) (s^2 - ghat/sqrt k - gam sum_(j>=1) delta_j / k),  ghat = 1 - s^2.
Numerical checks of exact identities only.
"""
import json, math, os
import numpy as np

def mats(k, d):
    gam = 1 / (1 - 1 / math.sqrt(k)); u = np.ones(k) / math.sqrt(k)
    w = -u.copy(); w[0] += 1
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.zeros((k, k))
    for j in range(1, d): P[j, j - 1] = 1
    P[0, d - 1] = 1
    for j in range(d, k): P[j, j] = 1
    return gam, u, w, U, P, U @ P @ U

def O_apply(x, k, d, gam):
    y = np.zeros_like(x); y[0] = x[0]
    sp = x[1:].sum(); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y

def OT_apply(y, k, d, gam):
    x = np.zeros_like(y); x[0] = y[0]
    x[1:d - 1] = y[2:d]; x[d:] = y[d:]
    s1 = y[1:].sum()
    x[1:] += -gam ** 2 * s1 / k + gam * y[1] / math.sqrt(k)
    x[d - 1] += gam * s1 / math.sqrt(k)
    return x

def main():
    rng = np.random.default_rng(3); out = {}
    for k, d in [(64, 32), (400, 200), (2000, 1000)]:
        gam, u, w, U, P, O = mats(k, d); a = 1 - 1 / (2 * k)
        g = rng.uniform(.6, .94)
        chi = U @ (a * O.T @ (g * np.ones(k)))
        e = np.zeros(k); e[d - 1] = 1
        r = {"I1_err": float(np.abs(chi - a * g * math.sqrt(k) * e).max())}
        # I1F: F-step uniform queries, chi_F = (a g)^F sqrt(k) e_(d-F)
        errF = 0.0
        for F in (2, 3, 7):
            nuF = np.ones(k)
            for _ in range(F):
                nuF = a * O.T @ (g * nuF)
            eF = np.zeros(k); eF[d - F] = 1
            errF = max(errF, float(np.abs(U @ nuF - (a * g) ** F * math.sqrt(k) * eF).max()))
        r["I1F_err"] = errF
        x = rng.standard_normal(k); y = rng.standard_normal(k)
        r["I2_O_err"] = float(np.abs(O @ x - O_apply(x, k, d, gam)).max())
        r["I2_OT_err"] = float(np.abs(O.T @ y - OT_apply(y, k, d, gam)).max())
        # I3: random credit-like V (u^T Y = 0), gates with row i a hole
        s = rng.uniform(.03, .07); ghat = 1 - s * s
        gt = ghat + rng.uniform(-.3, .002, k); gt[0] = ghat
        i = d // 2; gt[i] = 1.0
        Yp = rng.standard_normal((k, 3)); Yp -= np.outer(u, u @ Yp)
        c = 1.01; G = np.diag(gt); E = np.eye(k); E[0, 0] = 0
        Y = U @ G @ U @ (a * P @ Yp) + c * (U @ G @ E)[:, :3]
        delta = gt - ghat; delta[0] = 0
        kap = (gam * a / math.sqrt(k)) * (s * s - ghat / math.sqrt(k) - gam * delta[1:].sum() / k)
        V = a * P @ Yp
        pred = a * Yp[i - 1] + kap * Yp[d - 1] - (gam / k) * (gt[1:, None] * V[1:]).sum(0) + c * (U @ G @ E)[i, :3]
        r["I3_err"] = float(np.abs(Y[i] - pred).max())
        out[f"k={k}"] = r
    for v in out.values():
        assert v["I1_err"] < 1e-9 and v["I1F_err"] < 1e-9 and v["I2_O_err"] < 1e-11 and v["I2_OT_err"] < 1e-11 and v["I3_err"] < 1e-11
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp_identities_u_result.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
