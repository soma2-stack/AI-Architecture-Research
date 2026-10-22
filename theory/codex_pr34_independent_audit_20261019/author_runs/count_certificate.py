"""Combined listing count for Corollary 6.2R (Codex audit F2): exact rational certificate.

For the section S(n) (m = 3, T = n/2), Theorem 4 of PR #28 (all legal queries) supplies a state
listing Phi with |Phi| <= N_1 + N_2 + N_3, where (PR #28 Theorem 4, setup)
    kappa = 1.5e-4, Lam = 4.5e5, y = T/sqrt(n) = sqrt(n)/2,
    W' = ceil((8 + .5 ln+ y)/kappa), W_s = ceil(19/kappa), W = min(T, W' + W_s),
    N_1 = (2m+1)(4W + Lam + 4),  p = (2m+1)(W' + Lam + 1),  L = min(T, d-1),
    N_2 = 2.32e5 (pL/n)^2 + 2p,  N_3 = 1.3e7 F_s,  F_s = ceil(ln(1.01 sqrt k)/r_H),  r_H = -ln HI.
Lemma M (original form) asks for Psi with |Psi| <= C0 m + C1 (mT/n)^2 + C2 ln^2 n = 3 C0 + 2.25 C1 + C2 ln^2 n.
A joint zero of (Phi, Psi) on S^(D-1) exists whenever D > |Phi| + |Psi| (sparse Borsuk-Ulam,
PR #28 Lemma 2.1). With u = ln n and D >= e^(u/4)/161 (n >= 1e18; Codex audit section 4), it suffices that

    g(u) := e^(u/4)/161 - P_C(u) > 0,   P_C(u) := alpha0 + alpha1 u + alpha2 u^2 >= N_1+N_2+N_3+|Psi|.

The script builds rational alpha_i (outward), and certifies g(u_1) > 0, g'(u_1) > 0, g''(u_1) > 0 at a
rational u_1 <= ln n_1. Since g'' = e^(u/4)/2576 - 2 alpha2 is increasing, g'' > 0 on [u_1, inf), so g' and
then g are increasing there; hence the condition holds for EVERY n >= n_1.
Run: python -I count_certificate.py   (writes count_certificate_result.json)
"""
import json, os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
KAP, LAM = F(15, 100000), F(450000)
LN2_LO, LN101_HI, RH_LO = F("0.6931"), F("0.01"), F("0.0618")


def exp_lower(y, M=400):
    y = F(y); term = F(1); s = F(1)
    for j in range(1, M + 1):
        term *= y / j; s += term
    return s


def exp_upper_small(x, N=40):
    x = F(x); term = F(1); s = F(1)
    for j in range(1, N + 1):
        term *= x / j; s += term
    return s + (term * x / (N + 1)) / (1 - x / (N + 2))


def side_checks():
    # ln 2 >= .6931:  e^.6931 <= 2
    assert exp_upper_small(LN2_LO) <= 2
    # ln 1.01 <= .01 because e^x >= 1 + x (no computation needed)
    # r_H = 2 ln cosh(.25) >= .0618  <=>  cosh(.25) >= e^.0309 ; cosh(.25) >= 1 + .25^2/2 + .25^4/24
    assert 1 + F(1, 32) + F(1, 6144) >= exp_upper_small(F(309, 10000))
    return True


def poly_coeffs(C0, C1, C2):
    """alpha0 + alpha1 u + alpha2 u^2 >= N_1 + N_2 + N_3 + 3 C0 + 2.25 C1 + C2 u^2 for u = ln n >= ln 4."""
    # W' <= (8 + u/4 - ln2/2)/kappa + 1 = Aw + Bw u     (ln+ y = u/2 - ln 2 >= 0 for n >= 4)
    Aw = (8 - LN2_LO / 2) / KAP + 1
    Bw = 1 / (4 * KAP)
    Ws = 126667                                           # ceil(19/1.5e-4)
    assert Ws - 1 < 19 / KAP <= Ws
    # N_1 <= 7(4(W' + Ws) + Lam + 4)
    n1_0 = 7 * (4 * (Aw + Ws) + LAM + 4); n1_1 = 28 * Bw
    # p <= 7(W' + Lam + 1) = p0 + p1 u ;  pL/n <= p/4 ;  N_2 <= 2.32e5 p^2/16 + 2p
    p0 = 7 * (Aw + LAM + 1); p1 = 7 * Bw
    c = F(232000) / 16
    n2_0 = c * p0 ** 2 + 2 * p0; n2_1 = 2 * c * p0 * p1 + 2 * p1; n2_2 = c * p1 ** 2
    # F_s <= (ln 1.01 + (u - ln 2)/2)/r_H + 1 <= (ln1.01)/r_H + 1 + u/(2 r_H)
    n3_0 = F(13 * 10 ** 6) * (LN101_HI / RH_LO + 1); n3_1 = F(13 * 10 ** 6) / (2 * RH_LO)
    a0 = n1_0 + n2_0 + n3_0 + 3 * F(C0) + F(9, 4) * F(C1)
    a1 = n1_1 + n2_1 + n3_1
    a2 = n2_2 + F(C2)
    return a0, a1, a2


def certify(C0, C1, C2, u1):
    a0, a1, a2 = poly_coeffs(C0, C1, C2)
    E = exp_lower(F(u1) / 4)                              # e^(u1/4) >= E
    g = E / 161 - (a0 + a1 * u1 + a2 * u1 ** 2)
    g1 = E / 644 - (a1 + 2 * a2 * u1)
    g2 = E / 2576 - 2 * a2
    return g > 0 and g1 > 0 and g2 > 0


def smallest_decade(C0, C1, C2):
    """Smallest integer e such that the certificate holds at u1 = rational lower bound of ln(10^e)."""
    LN10_LO = F("2.302585")                                # ln 10 >= 2.302585
    assert exp_upper_small(LN10_LO / 4) ** 4 <= 10
    for e in range(18, 400):
        u1 = e * LN10_LO
        if certify(C0, C1, C2, u1):
            return e
    return None


def main():
    side_checks()
    out = {}
    a0, a1, a2 = poly_coeffs(0, 0, 0)
    out["P_0(u) coefficients (C = 0)"] = [f"{float(a0):.6e}", f"{float(a1):.6e}", f"{float(a2):.6e}"]
    rows = []
    for C in ((0, 0, 0), (10 ** 3, 10 ** 3, 10 ** 3), (10 ** 6, 10 ** 6, 10 ** 6), (10 ** 9, 10 ** 9, 10 ** 9),
              (10 ** 12, 10 ** 12, 10 ** 12), (10 ** 18, 10 ** 18, 10 ** 18), (10 ** 30, 10 ** 30, 10 ** 30)):
        e = smallest_decade(*C)
        rows.append({"C0,C1,C2": list(C), "certified for all n >= 10^e, e =": e})
        print(json.dumps(rows[-1]))
    out["thresholds"] = rows
    # a lower check: at n = 1e79 the sufficient condition fails for C = 0 (so the threshold ~1e80 is not loose by decades)
    LN10_HI = F("2.302586")
    u = 79 * LN10_HI
    from decimal import Decimal, getcontext
    getcontext().prec = 40
    val = Decimal(10) ** (Decimal(79) / 4) / 161 - Decimal(float(a0 + a1 * u + a2 * u * u))
    out["g(ln 1e79), C = 0 (negative: the sufficient condition is not met there)"] = f"{val:.4e}"
    json.dump(out, open(os.path.join(HERE, "count_certificate_result.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
