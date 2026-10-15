"""Constant certificates for Theorem R (50-digit decimal arithmetic, outward rounding by margins).

Every printed bound is compared against the value used in PROOF.md section 2.3 with an
explicit assertion. Decimal exp/ln are correctly rounded at the context precision, so a
relative safety margin of 1e-30 is far larger than any rounding error.

Sections:
  A. bath, beta, wake, inputs, modulation factor        (Steps 1, 2, 3)
  B. front-chain excess sums (self-contained comparison chain, Step 1)
  C. gate/delta budgets Sigma, Dbar, nu_N, mu, mu_d, w, Lambda, own-content norms (Step 9)
  D. the majorant system of Lemma E at k0 = 7.5e17, solved and verified (Step 9)
  E. main term, error assembly, final ratio to tau, budget threshold (Steps 4, 8, 10)
Run: python -I constants_check.py   (writes constants_check_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
UP = 1 + D("1e-30")            # outward rounding factor


def tanh(x):
    e = (2 * x).exp()
    return (e - 1) / (e + 1)


def sech2(x):
    t = tanh(x)
    return 1 - t * t


def main():
    r = {}
    # ---------------- A. bath, beta, wake, inputs, modulation factor
    t05 = tanh(D("0.05"))
    r["tanh(.05)"] = str(t05)
    s_lo, s_hi = t05 - D("1.5e-9"), t05 + D("1.5e-9")          # |s_t - tanh(.05)| <= 1.5e-9
    r["s^2 range"] = [str(s_lo * s_lo), str(s_hi * s_hi)]
    assert s_lo * s_lo >= D("0.0024958") and s_hi * s_hi <= D("0.0024959")
    b_lo = D("0.05") - s_hi - D("1.4e-9"); b_hi = D("0.05") - s_lo + D("1.4e-9")
    r["beta range"] = [str(b_lo), str(b_hi)]
    assert b_lo >= D("4.1622e-5") and b_hi <= D("4.1628e-5")
    y = D(1); ys = []
    for _ in range(5):
        y = tanh(y + b_hi); ys.append(y)
    r["wake y2..y6 upper"] = [str(v)[:10] for v in ys]
    bounds = [D(".76162"), D(".64205"), D(".56633"), D(".51269"), D(".47207")]
    assert all(v <= b for v, b in zip(ys, bounds))
    spike_start = ys[-1] + b_hi
    later_mod = D("0.45") - tanh(D("0.45")) + b_hi + D("1e-18")
    reset = tanh(D("0.45")) + b_hi
    first_mod = D("0.45") + b_hi
    r["inputs"] = {"spike_start": str(spike_start)[:10], "first_mod": str(first_mod)[:10],
                   "later_mod": str(later_mod)[:10], "reset": str(reset)[:10]}
    assert spike_start <= D(".47212") and later_mod <= D(".0282") and reset <= D(".42195")
    assert max(spike_start, first_mod, reset) <= D(".4732")
    g45 = sech2(D("0.45")); gm7 = g45 ** 7
    mod_lo, mod_hi = (1 - gm7) / UP, (1 - gm7) * UP
    r["sech^2(.45)"] = str(g45)[:12]; r["1-sech^2(.45)"] = str(1 - g45)[:12]
    r["1 - sech^2(.45)^7"] = str(1 - gm7)[:12]
    assert 1 - g45 <= D(".1780") and mod_lo >= D(".74642") and mod_hi <= D(".746425")
    # |delta^+| at a modulated position: ghat_t - sech^2(.45) <= (1 - s_lo^2) - sech^2(.45)
    dmod = (1 - s_lo * s_lo) - g45
    r["|delta| at modulated position"] = str(dmod)[:10]
    assert dmod <= D(".1756")

    # ---------------- B. front-chain excess (Step 1, Lemma 1.5)
    # z_1 <= 1, z_r <= qg tanh(z_(r-1)), qg = 1 - s_lo^2; sums of z_r and of z_r (z_r + 2 s_hi)
    qg = 1 - s_lo * s_lo
    z = D(1); Sz = D(1); Sd = D(0); it = 1
    while z > D("1e-40"):
        z = qg * tanh(z); it += 1; Sz += z; Sd += z * (z + 2 * s_hi)
    tail = z * qg / (1 - qg)          # z_(r+1) <= qg z_r beyond the last term
    Sz = (Sz + tail) * UP; Sd = (Sd + tail * (z + 2 * s_hi)) * UP
    r["front chain: iterations"] = it
    r["front chain: sum_(r>=1) z_r"] = str(Sz)[:10]
    r["front chain: sum_(r>=2) (y_r^2 - s^2)"] = str(Sd)[:10]
    assert Sz <= D("51.7") and Sd <= D("11.82")
    M_bound = Sz + D("0.0501") * (120000 + 9)
    r["|M_t| bound"] = str(M_bound)[:10]
    assert M_bound <= D("6.35e3")

    # ---------------- C. budgets (Step 9, (O4))
    ell = 120000
    s2 = D("0.0024959"); slo2 = D("0.0024958")
    assert 1 / slo2 <= 401                                    # 1/(1 - a ghat) <= 1/s_lo^2 <= 401
    Lam = D(ell + 401)
    Sig = (1 + Sd + (ell + 1) * s2 + 8 * D(".1756")) * UP     # front + chains + holes&spike + modulated
    Db = (1 + Sd + (ell - 7) * s2 + 7 * D(".1756")) * UP      # along one non-spike diagonal
    nuN = 8 * D(".1756") + s2
    mu = 8 * D(".1780"); mud = 7 * D(".1780"); wv = (D(8).sqrt() * D(".1780")) * UP
    gh = 1 - slo2
    fc = gh * gh / (1 - gh * gh)                              # front-chain part of an own profile
    Oh = (D(ell) + fc).sqrt() * UP
    OD = mod_hi * Oh
    r["budgets"] = {"Sigma": str(Sig)[:8], "Dbar": str(Db)[:8], "nu_N": str(nuN)[:8], "mu": str(mu),
                    "mu_d": str(mud), "w": str(wv)[:8], "Lambda": str(Lam), "front-chain own^2": str(fc)[:8],
                    "O_h": str(Oh)[:9], "O_Delta": str(OD)[:9]}
    assert Sig <= 314 and Db <= 314 and nuN <= D("1.41") and wv <= D(".50347")
    assert Oh <= D("346.70") and OD <= D("258.79")
    Sig = D(314); Db = D(314); nuN = D("1.41"); wv = D(".50347"); Oh = D("346.70"); OD = D("258.79")

    # ---------------- D. majorant system of Lemma E at k0 (all coefficients non-increasing in k)
    k0 = D("7.5e17")
    sk = k0.sqrt()
    q = (1 / sk) * UP
    gb = (1 / (1 - q)) * UP
    # front gate: g_1 <= 4 exp(-2 * .0498 sqrt k); g1q := g_1max / q = 4 sqrt(k) exp(-.0996 sqrt k)
    ln_g1q = D(4).ln() + sk.ln() - D(".0996") * sk
    assert ln_g1q <= -D(230) * D(10).ln()                     # g1q <= 1e-230
    g1q = D("1e-230")
    rs = (D("0.5") + 194 * q * q).sqrt() * UP                 # q * sqrt(k/2 + 194)

    def F(x):
        zh, B0, Sh, zm, B0m, Sm = x
        A = OD + q * zh; Am = Oh + q * zm
        nzh = (g1q * B0 + gb * (Db + gb * Sig * Lam * q * q) * A + gb * (mud + gb * mu * Lam * q * q) * Am
               + gb * Lam * q * (B0 + Sig * q * zh + nuN * OD + mu * Oh + mu * q * zm + wv)
               + gb * Lam * s2 * Sh + mud * zm)
        nB0 = (A + q * (B0 + Sig * q * zh + nuN * OD + mu * (Oh + q * zm)) + s2 * Sh
               + gb * q * q * (Sig * A + mu * Am) + q * wv)
        nSh = (q * q * zh + gb / 2 * (s2 + gb * Sig * q * q) * A + gb * gb * mu * q * q / 2 * Am
               + gb * q / 2 * (B0 + Sig * q * zh + nuN * OD + mu * (Oh + q * zm) + wv))
        nzm = (g1q * B0m + gb * (Db + gb * Sig * Lam * q * q) * Am
               + gb * Lam * q * (B0m + Sig * (Oh + q * zm)) + gb * Lam * s2 * Sm + gb * Lam)
        nB0m = Am + q * (B0m + Sig * (Oh + q * zm)) + s2 * Sm + gb * q * q * Sig * Am + 1
        nSm = (rs + q * q * zm + gb / 2 * (s2 + gb * Sig * q * q) * Am
               + gb * q / 2 * (B0m + Sig * (Oh + q * zm)) + gb / 2)
        return [nzh, nB0, nSh, nzm, nB0m, nSm]

    x = [D(0)] * 6
    for _ in range(80):
        x = F(x)
    xs = [v * (1 + D("1e-6")) + D("1e-6") for v in x]         # candidate super-solution
    Fx = F(xs)
    assert all(fv <= xv for fv, xv in zip(Fx, xs))            # F(x*) <= x*  =>  X <= x*
    assert all(fv < xv for fv, xv in zip(Fx, xs))             # strict => spectral radius < 1
    names = ["zeta_hat=sqrt(k)zeta", "B0", "S_hat=S/sqrt(k)", "zeta_hat-", "B0-", "S_hat-"]
    r["Lemma E certified bounds (x*)"] = {nm: str(v)[:10] for nm, v in zip(names, xs)}
    cert = {"zeta_hat": D("3.6809e5"), "B0": D("258.80"), "S_hat": D(".32296"),
            "zeta_hat_m": D("2.2978e5"), "B0_m": D("347.71"), "S_hat_m": D("1.6399")}
    assert all(v <= c for v, c in zip(xs, cert.values()))
    zh, B0, Sh, zm, B0m, Sm = cert.values()

    # ---------------- E. main term and error assembly (Steps 8, 10)
    HI = sech2(D("0.25"))
    aT = D("0.7785")              # a^(T+ell+2) >= exp(-.2502(1+1/n)) for n >= 1.5e18
    assert (D("-0.2502") * (1 + D("1e-18"))).exp() >= aT
    kap_fac = (slo2 - gb * Sig * q * q)                        # kappa^+ >= (a/sqrt k) kap_fac
    rho_fac = 1 - gb * s2 * D("0.5002")                         # (1 - gam s^2/k)^T, T/k <= .5002
    assert rho_fac >= 1 - D("1.3e-3")
    coef = HI * mod_lo * rho_fac * aT * kap_fac * D("0.249999") * (1 - D("1e-12"))
    cols = D(ell - 10).sqrt()
    mainv = coef * cols
    r["HI"] = str(HI)[:12]; r["per-column coefficient (x n)"] = str(coef)[:12]
    r["sqrt(ell-10)"] = str(cols)[:10]; r["main readout lower bound (x n)"] = str(mainv)[:10]
    assert coef >= D("3.403e-4") and mainv >= D(".11791")
    Am = Oh + q * zm
    EY = (q * zh + gb / 2 * (s2 + gb * Sig * q * q) * zh + gb * gb * mu * q / 2 * Am
          + gb / 2 * (B0 + Sig * q * zh + nuN * OD + mu * (Oh + q * zm) + wv))
    r["E_Y (error of Delta Y_T(d-1) on C, units of c_max=1)"] = str(EY)[:10]
    assert EY <= D("1019")
    n0 = D("1.5e18")
    err_frac = HI * D(1019) / (2 * n0).sqrt()                  # readout error / n, non-increasing in n
    r["readout error / n at n=1.5e18"] = format(err_frac, ".6e")
    assert err_frac <= D("5.6e-7")
    tau_over_n = D("0.002") / (t05 * D("0.5").sqrt())
    r["tau/n upper"] = str(tau_over_n)[:10]
    assert tau_over_n <= D(".05662")
    final = D(".11791") - D("5.6e-7")
    r["||Gamma||/n lower"] = str(final)[:10]; r["ratio to tau"] = str(final / tau_over_n)[:8]
    assert final >= D(".1179") and final / tau_over_n >= D("2.08")
    # budget threshold (Step 4): 120001 * .2501 n <= 2.5e-5 n^(3/2)  <=>  n >= (120001*.2501/2.5e-5)^2
    nthr = (D(120001) * D("0.2501") / D("2.5e-5")) ** 2
    r["n threshold for mT <= 2.5e-5 n^1.5"] = format(nthr, ".6e")
    assert nthr <= D("1.4412e18")
    # horizon fractions at n0 (both non-increasing in n): T <= .2501 n, |A| >= .249999 n, T+ell+2 <= .2502 n
    Wt = (30 + n0.ln()) / D("1.5e-4") + 1
    assert (ell + 33 + Wt) / n0 <= D("1e-4") and (2 * ell + 35 + Wt) / n0 <= D("2e-4")
    assert (Wt + 27) / n0 <= D("1e-6")
    with open(os.path.join(HERE, "constants_check_result.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
