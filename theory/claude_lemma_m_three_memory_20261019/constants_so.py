"""SUPERSEDED / REFUTED (kept unchanged below as a negative result; see PROOF.md section 5R).

Codex audit F1 (../codex_pr33_independent_audit_20261019/AUDIT.md): this certificate uses the FIXED
row-1 gate bound EPSG = 4e^-200, so a_L contains EPSG*Q*sqrt(k), which grows without bound.
At n = 10^166 its eps_SO is 2.199 > 1/2, and at 10^168 the bootstrap assertion e < 1 fails. The
monotonicity sentence below is false (H/n also increases at rounding points). The all-n
replacement is envelope_certificate.py, with the n-dependent gate bound of Lemma 5.0R.

Original docstring:
Certificate for Lemma 5.1 (background bounds) and Lemma 5.2 (second-order bound) of PROOF.md.

Evaluates every coefficient of section 5 in 50-digit decimals at a given n, with
H = ceil(40 n^(3/4)) and D = floor((d - 41)/(H + 1)). It reports eps_SO and checks
eps_SO <= 1/2. Each coefficient is a finite sum of terms of the form
C n^(-p) or C H n^(-p) with p > 0, and H n^(-1) = 40 n^(-1/4). Hence each is decreasing in n,
and the check at n_* certifies all n >= n_* (also verified on a grid of larger n).
Run: python -I constants_so.py   (writes constants_so_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))

S_LO, S_HI = D("0.025"), D("0.1009")
Q = 1 / S_LO ** 2                     # sum_w q^w <= 1/(1-q) <= 1/s_lo^2
XB = D("0.1316")                      # max |delta| on active pair rows
DF = D("39.73")                       # front deviation mass incl. row 1 (constants_seq)
DB = D("40.01")                       # bound on sum_j |delta_t(j)| and |S_t|
CS = D("0.3331")                      # |x+ - x-| <= c_s Pi
CSTAR = 1 + D("1e-12")
EPSG = D(4) * (D(-200)).exp()         # row-1 gate
ADMAX = None


def coeffs(n):
    n = D(n); k = n / 2; d = n / 4; sk = k.sqrt()
    gam = 1 / (1 - 1 / sk)
    H = (40 * n ** (D(3) / 4)).to_integral_value(rounding="ROUND_CEILING")
    Dm = ((d - 41) / (H + 1)).to_integral_value(rounding="ROUND_FLOOR")
    a_d = (-(d + 1) / (n - 1)).exp()                     # a^d >= e^(-(d+1)/(n-1)) (crude, safe)
    # capture constants
    kc = (gam / sk) * (DF + gam * DB * Q / k)
    kb = gam ** 2 * DB * Q / k ** D("1.5")
    kh = (gam / sk) * (XB + gam * DB / k)
    ks = (gam / sk) * (S_HI ** 2 + gam * DB / k)
    kA = (gam / sk) * DB * (1 + gam / 2)
    # ---- Lemma 5.1 background (one history, one memory column)
    Q1 = (Q + EPSG * sk / gam) / (1 - kc - EPSG * (1 + gam * DB / k))
    Q2 = kb * Q1 + Q
    Eeta = Q2 + (H + 1) * (kh * Q1 + 1)
    Epi = Q1 + d * (ks * Q1 + 1)
    cfb = (gam / k) * ((1 + gam * DB / k) * Q1 + sk / gam + DF * Q1 + S_HI ** 2 * Epi + 2 * XB * Eeta)
    assert cfb < 1
    fsup = (gam / k) * CSTAR * (XB * (Q + H + 1) + 1)
    lhat = fsup / (1 - cfb)
    Lin_f = (gam / k) * CSTAR * ((S_HI ** 2 * (H + 1) + 7 * XB) * (Q + H + 1) + H + 1)
    Lin = Lin_f + (H + 1) * cfb * lhat                   # sum of |lambda| over the memory's window
    eta_self = Q2 * lhat + kh * Q1 * lhat * (H + 1) + Lin
    cout = (gam / k) * (S_HI ** 2 * d + 2 * XB * (H + 1))
    assert cout < 1
    lout = ((gam / k) * CSTAR + (1 / sk + (gam / k) * ((1 + gam * DB / k) * Q1 + DF * Q1 + S_HI ** 2 * (Q1 + d * ks * Q1)
            + 2 * XB * (Q2 + (H + 1) * kh * Q1))) * lhat + (gam / k) * S_HI ** 2 * Lin) / (1 - cout)
    # arrivals summed over another memory's window: (H+1) kc Q1 lhat + Q L_in + (H+1) Q lout
    eta_oth = Q2 * lhat + kh * ((H + 1) * kc * Q1 * lhat + Q * Lin + (H + 1) * Q * lout) + (H + 1) * lout
    # ---- Lemma 5.2 difference bootstrap
    bA = Q / (1 - kA - EPSG * Q * D(2))
    aL = (gam / k) * (sk / gam + DF * Q + 2 * XB * (H + 1) * (2 + Q / H) + S_HI ** 2 * d) + EPSG * Q * sk
    aA = (gam / k) * ((1 + gam * DB / k) + DF * Q * (gam / sk) * (1 + gam * DB / k) + S_HI ** 2 * d * ks
                      + 2 * XB * (H + 1) * (kh + kb))
    e = aL + aA * bA
    assert e < 1
    # per unit Pi sources (self: i' = i, oth: i' != i). sigma_S per unit Pi:
    sS = (gam ** 2 / k ** D("1.5")) * Q1 * lhat * 14 * CS
    def src(eta):
        pulse = 14 * CS * (eta + (gam / sk) * (1 + 2 * gam / k) * Q1 * lhat)
        R = (gam / k) * ((gam / k) * Q1 * lhat * 14 * CS + DF * Q * sS + S_HI ** 2 * d * sS
                         + 2 * XB * (H + 1) * ((2 + Q / H) * sS + pulse) + 14 * CS * eta)
        # Lambda2 <= (e Lambda1 + aA bA sS + R)/(1-e); |dSO| <= (1 + ks bA) Lambda2 + ks bA Lambda1 + (1 + ks bA) sS
        return ((1 + ks * bA) * (aA * bA * sS + R) / (1 - e)) + (1 + ks * bA) * sS
    eps1 = ks * bA + (1 + ks * bA) * e / (1 - e)
    Fstar = (gam / k) * a_d ** 2 * D("0.99") * S_LO ** 2 * (H / 2 - D("0.5")) * (H / 2 - 7)
    Phi_self, Phi_oth = src(eta_self), src(eta_oth)
    epsSO = eps1 / a_d + (Phi_self + Dm * Phi_oth) / Fstar
    return {"n": str(n), "H": str(H), "D": str(Dm), "eps1/a^d": float(eps1 / a_d),
            "Phi_self/F*": float(Phi_self / Fstar), "D*Phi_oth/F*": float(Dm * Phi_oth / Fstar),
            "eps_SO": float(epsSO), "cfb": float(cfb), "e": float(e), "lhat*k": float(lhat * k),
            "eta_self/eta_oth": float(eta_self / eta_oth)}


def main():
    out = []
    grid = [D(10) ** p for p in range(8, 17, 2)] + [D(10) ** (D(16) + D(j) / 20) for j in range(0, 481)]
    first = None
    for nn in grid:
        r = coeffs(nn.to_integral_value() // 4 * 4)
        if first is None and r["eps_SO"] <= .5:
            first = r["n"]
        if r["eps_SO"] > .5 and first is not None:
            raise SystemExit("eps_SO not monotone on the grid")
        if nn < D(10) ** 16 or (nn >= D(10) ** 16 and (int((nn.ln() / D(10).ln() * 20).to_integral_value()) % 40 == 0)):
            print(json.dumps({kk: (f"{v:.3e}" if isinstance(v, float) else v) for kk, v in r.items()}))
        print(json.dumps({kk: (f"{v:.3e}" if isinstance(v, float) else v) for kk, v in r.items()}))
        out.append(r)
    print("first grid point with eps_SO <= 1/2:", first, "; all later grid points (to 1e40) also satisfy it")
    json.dump({"first_n_with_eps_SO_le_half": first, "grid": out}, open(os.path.join(HERE, "constants_so_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
