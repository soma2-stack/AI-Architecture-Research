"""Decimal certificates for the Lemma M_rest note (50 digits, outward rounding).

S2. The bath-coherent gain: max over x >= 0 of x exp(-s_lo^2 x) = 1/(e s_lo^2).
S4. Front saturation. Under (H) with m + 1 <= 1e-5 n and n >= 1e8, for t >= 1,
      sp_t := sum_(l>=1) h_t(l) >= .025 (k-1) - 507.1009 (m+1)        (Lemma B mass floor),
      pre_1(t+1) >= a sp_t (gamma/sqrt k)(1 - gamma/sqrt k) - a gamma/sqrt k + .05 - 1/2 - 1e-20  (dense R: eta-terms <= 1e-20),
      g_1(t+1) = sech^2(pre_1) <= 4 exp(-2 pre_1).
Run: python -I constants_rest.py   (writes constants_rest_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    r = {}
    s_lo = D("0.025")
    e = D(1).exp()
    peak = 1 / (e * s_lo * s_lo)
    r["S2: 1/(e s_lo^2)"] = str(peak)[:12]
    gain_extra = D("0.3435") * (1 + peak)
    r["S2: .3435 (1 + 1/(e s_lo^2))"] = str(gain_extra)[:12]
    assert gain_extra <= 203
    # S4, at the worst admissible point n = 1e8 (the bound improves with n: it is linear in sqrt k)
    n = D(10) ** 8; k = n / 2; sk = k.sqrt(); a = 1 - 1 / n
    gam = 1 / (1 - 1 / sk)
    mp1 = D("1e-5") * n
    sp = D("0.025") * (k - 1) - D("507.1009") * mp1
    r["S4: sp lower bound / k"] = str(sp / k)[:10]
    fac = (gam / sk) * (1 - gam / sk)
    pre = a * sp * fac - a * gam / sk + D("0.05") - D("0.5") - D("1e-20")
    r["S4: pre_1 lower bound at n = 1e8"] = str(pre)[:10]
    assert pre >= D("104")
    lg = (D(4) * (-2 * pre).exp()).ln()
    r["S4: ln g_1 upper bound"] = str(lg)[:10]
    assert lg <= D("-206")
    # coefficient of sqrt(k) in pre (for the general-n statement pre >= c sqrt(k) - .46)
    c = (D("0.025") - D("507.1009") * D("2e-5")) * (1 - gam / sk) * a
    r["S4: c in pre_1 >= c sqrt(k) - .46 (n >= 1e8)"] = str(c)[:10]
    assert c >= D("0.01485")
    with open(os.path.join(HERE, "constants_rest_result.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
