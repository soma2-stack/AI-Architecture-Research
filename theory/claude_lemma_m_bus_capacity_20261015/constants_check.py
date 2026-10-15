"""Constant certificates for the Lemma M note (50-digit decimal arithmetic, outward rounding).

Sections:
  B. Bath ceiling (Lemma B): the below-bath gap comparison sequence, its sum Sigma_neg, the
     self-consistent ceiling s_hi, and the per-chain gate-deviation constant C_chain.
  M. Theorem M (first-order gather capacity): the ledger, the near block length b = 2, the
     short-arrival cutoff, and the coefficients of the listing size: (mT/n)^2 for parts (a), (c),
     (mT)^(4/3)/n for the off-cycle part (d).
Every assertion compares a certified value with the number used in PROOF.md.
Run: python -I constants_check.py   (writes constants_check_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
UP = 1 + D("1e-30")


def tanh(x):
    e = (2 * x).exp()
    return (e - 1) / (e + 1)


def atanh(x):
    return ((1 + x) / (1 - x)).ln() / 2


def sech2(x):
    t = tanh(x)
    return 1 - t * t


def itanh2(lo, hi):
    """integral of tanh^2 over [lo, hi] = (hi - tanh hi) - (lo - tanh lo)."""
    return (hi - tanh(hi)) - (lo - tanh(lo))


def main():
    r = {}
    # ---------------- B. bath ceiling
    s_lo = D("0.025")                              # PR #27 Lemma 2.4 (bath floor), n >= 1e8, m <= c0 n
    b0 = atanh(s_lo)
    r["b0 = atanh(s_lo)"] = str(b0)[:14]

    def psi(Dd):                                   # min over B >= b0 of int_(B-D)^B tanh^2
        if Dd <= 2 * b0:
            return itanh2(b0 - Dd, b0)
        return 2 * (Dd / 2 - tanh(Dd / 2))

    # comparison sequence delta_(u+1) = delta_u - psi(delta_u) + margin, delta_0 = 2
    dlt = D(2); Ssum = D(0); it = 0; margin = D("1e-40")
    while dlt > b0 / 2:
        Ssum += dlt
        dlt = dlt - psi(dlt) + margin
        it += 1
    q = tanh(b0 / 2) ** 2                          # geometric rate once delta <= b0/2
    tail = dlt / q
    Sneg = (Ssum + tail) * UP
    r["B: comparison iterations"] = it
    r["B: Sigma_neg (sum of below-bath gaps along one chain)"] = str(Sneg)[:10]
    assert Sneg <= D("506")
    Sneg = D("506")
    # self-consistent ceiling: s_hi = tanh(.05 + g2 (m+1)/k (1 + s_hi + Sigma_neg) + g2 n rho + 3 gamma/sqrt k)
    mk = D(10002) / D(99999999)                    # (m+1)/k for n >= 1e8, m <= 5e-5 n (PR #27)
    g = D(7071) / D(7070); g2 = g * g              # gamma bound (sqrt k > 7071)
    E = 3 * g / D(7071)                            # |E_t| <= 3 gamma/sqrt k
    nrho = D("4e-12")
    s_hi_cand = D("0.1009")
    val = tanh(D("0.05") + g2 * mk * (1 + s_hi_cand + Sneg) + g2 * nrho + E) * UP
    r["B: ceiling map at candidate .1009"] = str(val)[:10]
    assert val <= s_hi_cand                        # induction closes with s_hi = .1009
    s_hi = s_hi_cand
    r["B: s_hi"] = str(s_hi); r["B: s_hi^2"] = str(s_hi * s_hi)
    # per-chain gate deviation sum: above-bath <= 2 * 223 (PR #27), below-bath <= (1 + s_hi) Sigma_neg
    C_chain = max(2 * D(223), (1 + s_hi) * Sneg)
    r["B: C_chain"] = str(C_chain)[:10]
    assert C_chain <= D("558")
    C_chain = D("558")

    # ---------------- M. Theorem M ledger and constants
    LO, HI = sech2(D("0.75")), sech2(D("0.25"))
    tau_n = D("0.0566")                            # tau >= .0566 n (PR #28 section 0)
    Lam1 = D(450001)                               # Lam + 1, PR #27 Lemma 2.5
    kap = D("1.5e-4")
    s2 = s_hi * s_hi
    cmax = 1 + D("1e-30")                          # undriven source, R0 or prescribed dense R
    # near residual: HI * gamma * s_hi^2 * (d-1) * sqrt(b) <= tau/16 with d <= n/4, b = 2
    near = HI * g * s2 * cmax * D("0.25") * D(2).sqrt()
    r["M: near residual / n (b = 2)"] = str(near)[:10]
    assert near <= tau_n / 16
    # far-long (front protection handled by lambda >= 4(Lam+1)): long arrivals have N_t >= (j+1)/(4(Lam+1)),
    # readout <= 8 HI gamma s_hi^2 cmax (Lam+1) mT/sqrt(lambda) <= tau/64
    #   <=> lambda >= (512 HI gamma s_hi^2 cmax (Lam+1) mT/tau)^2
    cl = 512 * HI * g * s2 * Lam1 * cmax / tau_n
    coefK = (cl * cl / 2) * UP                     # count ceil(lambda/2)
    r["M: far-long coefficient c_l (lambda >= (c_l mT/n)^2)"] = format(cl, ".4e")
    r["M: count coefficient for (mT/n)^2, captured-own part"] = format(coefK, ".4e")
    assert coefK <= D("7.6e14")
    lam_min = max(D(100000), 4 * Lam1)
    r["M: lambda floor max(lambda_s, 4(Lam+1))"] = str(lam_min)
    assert lam_min == D(1800004)
    # far-short: 2 HI gamma s_hi^2 (d/n) (1-kap)^(lambda/2)/sqrt(kap) <= tau/256
    lam_s = D(100000)
    short = 2 * HI * g * s2 * cmax * D("0.25") * ((1 - kap).ln() * lam_s / 2).exp() / kap.sqrt()
    r["M: far-short residual / n at lambda_s = 1e5"] = format(short, ".4e")
    assert short <= tau_n / 256
    # K^neg: 2 HI gamma * 1.26 * sqrt(d) <= tau/256  for n >= 1e8 (sqrt(d) <= sqrt(n)/2)
    nmin = D("1e8")
    kneg = 2 * HI * g * D("1.26") * cmax * (nmin.sqrt() / 2) / nmin
    r["M: K^neg residual / n at n = 1e8"] = format(kneg, ".4e")
    assert kneg <= tau_n / 256
    # BV part: readout <= HI sqrt(k) sqrt(b_L) 2 (TV) with TV <= (6 gamma cmax/k + 4 gamma^2 cmax/k^1.5) Sigma_P,
    #          Sigma_P <= 2 (1 + C_chain) mT.  Require <= tau/64:
    #          sqrt(b_L) <= tau sqrt(k) / (64 * HI * 2 * 6.0001 gamma cmax * 2 (1 + C_chain) mT)
    cb = 64 * HI * 2 * D("6.0001") * g * cmax * 2 * (1 + C_chain)
    # count = ceil((k-1)/b_L) <= (k-1) (cb mT)^2/(tau^2 k) + 2 <= (cb mT/tau)^2 + 2
    coefL = (cb / tau_n) ** 2 * UP
    r["M: BV constant c_b"] = format(cb, ".4e")
    r["M: count coefficient for (mT/n)^2, BV part"] = format(coefL, ".4e")
    assert coefL <= D("4.0e14")
    # (d) off-cycle leak sources (public schedules): list the columns of off-cycle rows with N_j >= N_0.
    #     unlisted readout <= 4 HI gamma cmax (1 + C_chain)(Lam+1) N_0^(3/2) sqrt(mT)/sqrt(k) <= tau/64
    #     count = mT/N_0 = (mT)^(4/3) [256 HI gamma cmax (1+C_chain)(Lam+1)/(tau sqrt(k))]^(2/3)
    #     with tau sqrt(k) >= .0566 n sqrt(n/2):  count <= c_d (mT)^(4/3)/n
    cd_inner = 256 * HI * g * cmax * (1 + C_chain) * Lam1 / (tau_n * D("0.5").sqrt())   # times n^(-3/2)
    c_d = (cd_inner ** (D(2) / 3)) * UP
    r["M: count coefficient for (mT)^(4/3)/n, off-cycle part"] = format(c_d, ".4e")
    assert c_d <= D("1.6e8")
    ledger = D(1) / 16 + D(1) / 64 + D(1) / 256 + D(1) / 256 + D(1) / 64 + D(1) / 64
    r["M: first-order gather ledger (x tau)"] = str(ledger)
    assert ledger == D(30) / D(256)
    with open(os.path.join(HERE, "constants_check_result.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
