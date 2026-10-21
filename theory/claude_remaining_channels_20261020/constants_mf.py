"""Constant certificate for Theorem M_F (PROOF.md section 2): the first-order gather listing of PR #31
Theorem M, replicated on the F_s - 1 spike rows d-1, ..., d-F_s+1 with tolerance tau_F = tau/sqrt(F_s).

50-digit decimal arithmetic with outward rounding, in the style of PR #31 constants_check.py. The
inherited constants (s_hi = .1009, C_chain = 558, Lam + 1 = 450001, kappa = 1.5e-4, c_* = 1 + 1e-12,
tau >= .0566 n) are those certified there; they are restated, not re-derived.

Checks:
  * F_s upper bound F_s <= f(n) := 1 + (ln 1.01 + .5 ln(n/2))/r_H, r_H = -ln HI. Since F_s is a ceiling,
    n/F_s is NOT monotone (Codex audit); the argument uses the continuous envelope: n/f(n) increases
    because f(n) > 1/(2 r_H), so n/F_s >= n/f(n) >= 1e10/f(1e10) for n >= 1e10;
  * K_neg on every spike row: HI gamma 1.26 c_* sqrt(n) sqrt(F_s) <= tau/256 for n >= 1e10;
  * far-short arrivals at the floor lambda_0 = 1800004 + ceil(ln(F_s)/kappa);
  * far-long cutoff coefficient (unchanged 3.897e7), now with the factor F_s;
  * BV coefficient (unchanged 8.1e5), count factor F_s;
  * off-cycle coefficient (unchanged 1.4e8), count factor F_s^(1/3);
  * per-row ledger 14/256 (near columns listed exactly, block length 1).
Run: python -I constants_mf.py   (writes constants_mf_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
UP = 1 + D("1e-30")


def tanh(x):
    e = (2 * x).exp()
    return (e - 1) / (e + 1)


def sech2(x):
    t = tanh(x)
    return 1 - t * t


def Fs_upper(n):
    """F_s = ceil(ln(1.01 sqrt(k))/r_H) <= 1 + ln(1.01 sqrt(n/2))/r_H."""
    rH = -sech2(D("0.25")).ln()
    return 1 + (D("1.01") * (n / 2).sqrt()).ln() / rH


def main():
    r = {}
    LO, HI = sech2(D("0.75")), sech2(D("0.25"))
    rH = -HI.ln()
    r["r_H = -ln HI"] = str(rH)[:12]
    assert rH > D(".0618")
    tau_n = D("0.0566"); s_hi = D("0.1009"); s2 = s_hi * s_hi
    C_chain = D(558); Lam1 = D(450001); kap = D("1.5e-4"); cmax = 1 + D("1e-12")
    g = D(7071) / D(7070)                      # gamma bound for n >= 1e8

    # ---- F_s and the K_neg condition (n >= 1e10)
    n0 = D("1e10")
    Fs0 = Fs_upper(n0)
    r["F_s upper bound at n = 1e10"] = str(Fs0)[:10]
    # continuous envelope: d/dn [n / f(n)] > 0  <=>  f(n) > 1/(2 r_H); then n/F_s >= n/f(n) >= 1e10/f(1e10)
    assert Fs0 > 1 / (2 * rH)
    kneg_need = 256 * HI * g * D("1.26") * cmax / tau_n            # need sqrt(n/F_s) >= this
    r["K_neg: required sqrt(n/F_s)"] = str(kneg_need)[:10]
    r["K_neg: sqrt(n/F_s) at n = 1e10"] = str((n0 / Fs0).sqrt())[:10]
    assert (n0 / Fs0).sqrt() >= kneg_need

    # ---- far-short at lambda_0 = 1800004 + ceil(ln F_s / kappa):
    #      2 HI gamma s_hi^2 c_* (d/n) (1-kap)^(lambda_0/2)/sqrt(kap) <= tau_F/(256 n) = tau_n/(256 sqrt(F_s) n)
    #      (1-kap)^(lambda_0/2) <= exp(-kap lambda_0/2) <= exp(-135.0003) F_s^(-1/2)
    base = 2 * HI * g * s2 * cmax * D("0.25") * (-kap * D(1800004) / 2).exp() / kap.sqrt()
    r["far-short residual / n at lambda = 1800004 (times sqrt(F_s) after the ln F_s shift)"] = format(base, ".3e")
    assert base <= tau_n / 256
    # exp(-kap * ceil(ln F/kap)/2) <= F^(-1/2): exact, since kap*ceil(x/kap) >= x.

    # ---- far-long cutoff: lambda >= (c_l sqrt(F_s) mT/n)^2 with c_l = 512 HI gamma s_hi^2 c_* (Lam+1)/tau_n
    cl = 512 * HI * g * s2 * Lam1 * cmax / tau_n
    r["far-long c_l"] = format(cl, ".5e")
    assert cl <= D(38970000)
    coefK = D(38970000) ** 2 * UP              # near columns listed exactly (block 1): count lambda, not lambda/2
    r["count coefficient (x F_s^2 (mT/n)^2), captured-own part"] = format(coefK, ".4e")
    assert coefK <= D("1.519e15")

    # ---- BV part: B_L = (tau_F sqrt(k)/(c_b mT))^2, count (c_b mT/tau_F)^2 + 2 = F_s (c_b/tau_n)^2 (mT/n)^2 + 2
    cb = 64 * HI * 2 * D(6) * g * cmax * 2 * (1 + C_chain)
    assert cb <= D("8.1e5")
    coefL = (cb / tau_n) ** 2 * UP
    r["count coefficient (x F_s^2 (mT/n)^2), BV part"] = format(coefL, ".4e")
    assert coefL <= D("2.1e14")
    assert coefK + coefL <= D("1.73e15")

    # ---- off-cycle part: x_F = x F_s^(-1/3), count mT/x_F <= 1.4e8 F_s^(1/3) (mT)^(4/3)/n
    cd_inner = 256 * HI * g * cmax * (1 + C_chain) * Lam1 / (tau_n * D("0.5").sqrt())
    c_d = (cd_inner ** (D(2) / 3)) * UP
    r["count coefficient (x F_s^(4/3) (mT)^(4/3)/n), off-cycle part"] = format(c_d, ".4e")
    assert c_d <= D("1.4e8")

    # ---- per-row ledger: near 0 (exact) + far-long 1/64 + far-short 1/256 + K_neg 1/256 + BV 1/64 + off 1/64
    ledger = D(0) + D(1) / 64 + D(1) / 256 + D(1) / 256 + D(1) / 64 + D(1) / 64
    r["per-row ledger (x tau_F)"] = str(ledger)
    assert ledger == D(14) / D(256)
    # Cauchy-Schwarz over at most F_s - 1 spike rows with ||chi||_2 <= HI sqrt(k):
    # total <= HI sqrt(k) sqrt(F_s) max_f ||residual_f|| <= sqrt(F_s) (14/256) tau_F = (14/256) tau
    r["total first-order spike-row ledger (x tau)"] = "14/256"

    # ---- sample counts (coefficients only), for the REPORT table
    for nn in ("1e10", "1e16", "1e24", "1e40"):
        Fs = Fs_upper(D(nn))
        r["F_s upper at n = " + nn] = str(Fs)[:8]
    with open(os.path.join(HERE, "constants_mf_result.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
