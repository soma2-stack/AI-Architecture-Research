"""Exact rational certificate for the dense-transfer constants (PROOF.md sections 2-4).

All quantities use only: n >= 1e18 (Theorems), n >= 1e8 (state lemmas), eta <= 1e-8/n^2,
alpha in [1 - 2 eta, 1), a = 1 - 1/n, a' = alpha a, |phi_t| <= eta, c_* = 1 + 1e-12,
H = ceil(40 n^(3/4)), D <= n^(1/4)/160, T = n/2, HI = sech^2(.25) < .9406.
  L  legality: dense field bound |a' J + .05 + phi| <= .0763 and the other input bounds (unchanged
     numbers; the dense terms only enter through a' <= 1 and a' >= 1 - 1e-8 - 2e-24).
  F  front gate: total slack .1/sqrt(k) + .025 sqrt(k)/n + 2 eta (.025 sqrt k) + eta <= .001.
  E  credit and readout perturbation:
       ||R - R0||op <= (1 - alpha) a + alpha eta <= 3 eta,
       ||B_T(:,c) - B'_T(:,c)|| <= T (3 eta) c_* n <= 1.5e-8 c_*          (per column),
       readout perturbation <= HI sqrt(n) 2(1.5e-8 c_*) sqrt(D) + 3 eta HI sqrt(n) 2.1 c_* n sqrt(D)
                            <= 3e-9 n^(5/8)     for n >= 1e18;
  R  robustness: .078 n (1 - n^(-3/4))^2 - 3e-9 n^(5/8) - 4e3 n^(3/8) > .0567 n >= tau for n >= 1e18.
Run: python -I constants_dense.py   (writes constants_dense_result.json)
"""
import json, os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))


def atanh_upper(x, N=30):
    x = F(x); s = sum((x ** (2 * j + 1) / (2 * j + 1) for j in range(N + 1)), F(0))
    return s + x ** (2 * N + 3) / ((2 * N + 3) * (1 - x * x))


def atanh_lower(x, N=30):
    x = F(x); return sum((x ** (2 * j + 1) / (2 * j + 1) for j in range(N + 1)), F(0))


def main():
    r = {}
    s_lo, s_hi = F(1, 40), F("0.1009")
    n8 = 10 ** 8
    eta8 = F(1, 10 ** 8) / n8 ** 2                      # eta at n = 1e8 (largest admissible)
    ap_min = (1 - F(1, n8)) * (1 - 2 * eta8)
    # L: field bound  a'J + .05 + phi = atanh(s_t) - a' s_(t-1)  in [atanh(s_lo) - s_hi, atanh(s_hi) - a'_min s_lo]
    up = atanh_upper(s_hi) - ap_min * s_lo
    lo = atanh_lower(s_lo) - s_hi
    assert max(up, -lo) <= F("0.0763")
    r["L field bound (<= .0763)"] = float(max(up, -lo))
    # F: front-gate slack
    sk_min = 7071                                      # sqrt(k) >= 7071 for n >= 1e8
    slack = F(1, 10) / sk_min + F(1, 40) / 14142 + 2 * eta8 * F(1, 40) * 10 ** 6 + eta8
    assert slack <= F(1, 1000)
    r["F front-gate slack (<= .001)"] = float(slack)
    # E: per-column credit perturbation, any n >= 1e8 (eta <= 1e-8/n^2, T = n/2):
    #    T * 3 eta * c_* * n <= (n/2) * 3e-8/n^2 * c_* * n = 1.5e-8 c_*
    cstar = 1 + F(1, 10 ** 12)
    per_col = F(3, 2) * F(1, 10 ** 8) * cstar
    r["E per-column ||B - B'|| <= "] = float(per_col)
    # readout perturbation at n >= 1e18, written as c1 n^(5/8) + c2 n^(1/8)/... ; bound each by multiples of n^(5/8)
    HI = F("0.9406")
    # term1: HI sqrt(n) * 2 per_col * sqrt(D),  sqrt(D) <= n^(1/8)/sqrt(160)  ->  HI 2 per_col / sqrt(160) * n^(5/8)
    inv_sqrt160 = F(1, 12)                             # 1/sqrt(160) < 1/12.6 < 1/12
    t1 = HI * 2 * per_col * inv_sqrt160
    # term2: 3 eta HI sqrt(n) * 2.1 c_* n sqrt(D) <= 3e-8 n^-2 HI 2.1 c_* n^(3/2) n^(1/8)/12 = O(n^(-3/8)) <= t2 n^(5/8)
    t2 = F(3, 10 ** 8) * HI * F(21, 10) * cstar * inv_sqrt160          # coefficient of n^(-3/8) = n^(5/8)/n
    c_pert = t1 + t2 / 10 ** 18                                         # n >= 1e18
    assert c_pert <= F(3, 10 ** 9)
    r["E readout perturbation coefficient of n^(5/8) (<= 3e-9)"] = float(c_pert)
    # R: robustness at n >= 1e18, using n^(-3/8) <= 1e-6.75 < 1e-6 and n^(-5/8) <= 1e-11.25 < 1e-11
    x34 = F(1, 10 ** 13)                               # n^(-3/4) <= 1e-13.5
    lhs = F("0.078") * (1 - x34) ** 2 - c_pert * F(1, 10 ** 6) - 4000 * F(1, 10 ** 11)   # all divided by n
    assert lhs > F("0.0567")
    r["R (readout - perturbations)/n lower bound at n >= 1e18"] = float(lhs)
    r["R tau/n upper"] = .0567
    # the .078 constant: (1 - .3747)(4.988e-4)(.6272)(400) >= .078
    c078 = (1 - F("0.3747")) * F("0.0004988") * F("0.6272") * 400
    assert c078 >= F("0.078")
    r["R first-order constant (>= .078)"] = float(c078)
    json.dump(r, open(os.path.join(HERE, "constants_dense_result.json"), "w"), indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
