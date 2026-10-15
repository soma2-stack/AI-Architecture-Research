"""Exact check of Proposition M1 (the two-channel decomposition of the bus readout).

For random credit matrices B' (row 0 zero), random own parts O (row 0 zero) and random one-step
legal gates g in [LO, HI]^k, verifies

  sum_l nu_l bus_l  =  a sqrt(k) gbar Delta Z(d-1)  +  a sum_(i != d-1) eps_i Delta Z(i)
                       + (gamma/sqrt k)(w^T nu) sum_(i>=1) Delta O(i),

where nu = a O^T g (memory block of R0^T g), bus = B' - O (standard rows), Y = U B', Z = Y - O
(Z(0) = Y(0)), gbar = mean of g over memory rows 0..k-1, eps_i = (Ug)_(P(i)) (eps_(d-1) := 0).
It also checks |eps_i| <= .3404 and |w^T nu| <= 1.29.
Exact algebra; numerical residuals are floating-point only.
Run: python -I exp_two_channel_identity.py
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def mats(k, d):
    gam = 1 / (1 - 1 / math.sqrt(k)); u = np.ones(k) / math.sqrt(k)
    w = -u.copy(); w[0] += 1
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.zeros((k, k))
    for j in range(0, d - 1):
        P[j + 1, j] = 1.0                       # P e_j = e_(j+1) on the cycle
    P[0, d - 1] = 1.0                           # P e_(d-1) = e_0
    for j in range(d, k):
        P[j, j] = 1.0
    return gam, w, U, P, U @ P @ U


def main():
    rng = np.random.default_rng(7)
    out = []
    for n in (64, 400, 2000):
        k, d = n // 2, n // 4; a = 1 - 1 / n
        gam, w, U, P, O = mats(k, d)
        worst = 0.0; eps_max = 0.0; wn_max = 0.0
        for _ in range(5):
            Bp = rng.normal(size=(k, k)); Bp[0] = 0.0
            Bm = rng.normal(size=(k, k)); Bm[0] = 0.0
            Op = rng.normal(size=(k, k)); Op[0] = 0.0
            Om = rng.normal(size=(k, k)); Om[0] = 0.0
            g = rng.uniform(LO, HI, size=k)
            nu = a * O.T @ g
            lhs = nu @ ((Bp - Op) - (Bm - Om))
            Yp, Ym = U @ Bp, U @ Bm
            Zp, Zm = Yp - Op, Ym - Om
            Ug = U @ g
            gbar = g.mean()
            eps = np.array([Ug[np.nonzero(P[:, i])[0][0]] for i in range(k)])   # (Ug)_(P(i))
            eps[d - 1] = 0.0
            dZ = Zp - Zm; dO = Op - Om
            rhs = a * math.sqrt(k) * gbar * dZ[d - 1] + a * (eps @ dZ) + (gam / math.sqrt(k)) * (w @ nu) * dO[1:].sum(0)
            worst = max(worst, float(np.abs(lhs - rhs).max() / np.abs(lhs).max()))
            eps_max = max(eps_max, float(np.abs(eps).max())); wn_max = max(wn_max, abs(float(w @ nu)))
        rec = {"n": n, "rel_residual": worst, "max_abs_eps": eps_max, "max_abs_wTnu": wn_max}
        assert eps_max <= .3404 and wn_max <= 1.29
        print(json.dumps(rec)); out.append(rec)
    with open(os.path.join(HERE, "exp_two_channel_identity_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
