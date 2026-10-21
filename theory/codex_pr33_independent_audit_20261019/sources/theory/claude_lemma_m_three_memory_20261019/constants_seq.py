"""Decimal certificates for the sequential construction S (PROOF.md sections 4-6).

50-digit decimals; every assertion compares a certified value with the number used in PROOF.md.
  L. legality: front-chain gap at age 18, spike start, pulse, reset, park inputs;
  P. the pulse profile Pi(z) = (1 - v(-z)^2)^7 - (1 - v(z)^2)^7, v(z) = tanh(A(1+z)/2), A = .38:
     monotonicity condition, Pi(1), the minimum of Pi(z)/z on a fine grid with a Lipschitz margin,
     and the slope bound |v(z)^2 - v(-z)^2| <= c_s Pi(z);
  F. front deviation mass per step;
  R. the first-order readout coefficient and the hold length needed for robustness.
Run: python -I constants_seq.py   (writes constants_seq_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))


def tanh(x):
    e = (2 * x).exp(); return (e - 1) / (e + 1)


def atanh(x):
    return ((1 + x) / (1 - x)).ln() / 2


def main():
    r = {}
    s_lo, s_hi = D("0.025"), D("0.1009")
    A = D("0.38")
    # ---- L. legality
    jmax = atanh(s_hi) - s_lo * (1 - D("1e-8"))          # |aJ + .05| upper bound: atanh(s_t) - a s_(t-1)
    jmin = atanh(s_lo) - s_hi
    J = max(jmax, -jmin)
    r["L: |aJ+.05| <= "] = str(J)[:10]
    assert J <= D("0.0763")
    g = D(1)
    for _ in range(18):
        g = tanh(g)                                      # gap at age u <= tanh^(u-1)(1); row 19 has age 18
    r["L: tanh^(18)(1)"] = str(g)[:10]
    spike0 = g + atanh(s_hi)                             # |pre| at the first spike position (row 20)
    r["L: first spike input <= "] = str(spike0)[:10]
    assert spike0 <= D("0.39")
    pulse0 = A + J; reset = tanh(A) + J; pulse_later = (A - tanh(A)) + J; park = s_hi
    r["L: pulse first step <= "] = str(pulse0)[:8]; r["L: reset after pulse <= "] = str(reset)[:8]
    r["L: later pulse steps <= "] = str(pulse_later)[:8]; r["L: park <= "] = str(park)
    assert max(pulse0, reset, pulse_later, park, spike0, J, atanh(s_hi)) < D("0.4564")
    # ---- P. pulse profile
    xmax = tanh(A) ** 2
    r["P: v_max^2 = tanh(.38)^2"] = str(xmax)[:10]
    assert xmax < D(1) / 7                               # x(1-x)^w increasing on [0, xmax] for w <= 6

    def v2(z):
        return tanh(A * (1 + z) / 2) ** 2

    def Pi(z):
        return (1 - v2(-z)) ** 7 - (1 - v2(z)) ** 7
    r["P: Pi(1)"] = str(Pi(D(1)))[:10]
    # min of Pi(z)/z. Pi is increasing (Pi' > 0, below). On [0, Z0], Pi(z)/z >= min Pi' (mean value from 0):
    # Pi'(w) = 7[(1-x+)^6 x+' + (1-x-)^6 |x-'|] >= 14 (1-x1)^6 A t(u_min), with x' = A t(u),
    # t(u) = tanh(u) sech^2(u) increasing on [0, .65], u_min = A(1 - Z0)/2 and x+- <= x1 = tanh(A(1+Z0)/2)^2.
    # On [Z0, 1] a grid z_j = Z0 + (1-Z0) j/N gives Pi(z) >= Pi(z_(j-1)) and z <= z_j.
    assert A < D("0.65")
    Z0 = D("0.1"); N = 2000
    um = A * (1 - Z0) / 2; x1 = tanh(A * (1 + Z0) / 2) ** 2
    worst = 14 * (1 - x1) ** 6 * A * tanh(um) * (1 - tanh(um) ** 2)
    r["P: Pi(z)/z lower bound on [0, .1]"] = str(worst)[:10]
    for jj in range(1, N + 1):
        z0 = Z0 + (1 - Z0) * D(jj - 1) / N; z1 = Z0 + (1 - Z0) * D(jj) / N
        worst = min(worst, Pi(z0) / z1)
    r["P: pi0 = min Pi(z)/z (certified lower bound)"] = str(worst)[:10]
    assert worst >= D("0.60")
    # slope bound: |v2(z) - v2(-z)| <= Pi(z) / (7 (1 - xmax)^6)
    cs = 1 / (7 * (1 - xmax) ** 6)
    r["P: c_s = 1/(7(1-xmax)^6)"] = str(cs)[:10]
    assert cs <= D("0.34")
    # ---- F. front deviation mass: |delta| = gap (y + s) <= gap (2 s_hi + gap); gap_(u+1) <= min(tanh(gap_u), (1 - s_lo^2) gap_u)
    gap = D(1); tot = D(0); q = 1 - s_lo ** 2
    for u in range(1, 200000):
        tot += gap * (2 * s_hi + gap)
        gap = min(tanh(gap), q * gap)
        if gap < D("1e-30"):
            break
    Dfront = tot + 1                                     # + row 1 (|delta_1| <= 1)
    r["F: front deviation mass per step <= "] = str(Dfront)[:10]
    assert Dfront <= D("60")
    # ---- R. readout: a HI sqrt(k) Delta F1 >= cR (H/2 - 7)^2 Pi(z) / sqrt(n),
    #      cR = HI * a^(2d+1) * .99 * s_lo^2 * gamma * sqrt(2) (sqrt k = sqrt(n/2)); a^(2d+1) >= exp(-.5001)
    HI = 1 - tanh(D("0.25")) ** 2
    cR = HI * (-D("0.5001")).exp() * D("0.99") * s_lo ** 2 * D(2).sqrt()
    r["R: cR"] = str(cR)[:10]
    tau_max = D("0.0567")                                # tau <= .002 sqrt(2) n / .0499
    # robustness with second-order allowance eps_SO = 1/2: (1/2) cR (H/2-7)^2 pi0 / sqrt n > .0567 n
    hcoef = (2 * tau_max / (cR * worst)).sqrt() * 2      # H/2 - 7 > hcoef/2 n^(3/4)  <=>  H > hcoef n^(3/4) + 14
    r["R: H > h n^(3/4) + 14 with h = "] = str(hcoef)[:8]
    assert hcoef <= D("60")
    json.dump(r, open(os.path.join(HERE, "constants_seq_result.json"), "w"), indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
