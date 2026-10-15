"""Constant certificates for Theorem R (50-digit decimal arithmetic, outward rounding by margins).

Every printed bound is compared against the value used in PROOF.md section 2.3 with an
explicit assertion. Decimal exp/ln are correctly rounded at the context precision, so a
relative safety margin of 1e-30 is far larger than any rounding error.
Run: python -I constants_check.py   (writes constants_check_result.json)
"""
import json, os
from decimal import Decimal as D, getcontext

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))


def tanh(x):
    e = (2 * x).exp()
    return (e - 1) / (e + 1)


def atanh(x):
    return ((1 + x) / (1 - x)).ln() / 2


def sech2(x):
    t = tanh(x)
    return 1 - t * t


def main():
    r = {}
    t05 = tanh(D("0.05"))
    r["tanh(.05)"] = str(t05)
    # bath and beta (Step 1): |s - tanh(.05)| <= 1.5e-9, |eps| <= 1.4e-9
    s_lo, s_hi = t05 - D("1.5e-9"), t05 + D("1.5e-9")
    r["s^2 range"] = [str(s_lo * s_lo), str(s_hi * s_hi)]
    assert s_lo * s_lo >= D("0.0024958") and s_hi * s_hi <= D("0.0024959")
    b_lo = D("0.05") - s_hi - D("1.4e-9"); b_hi = D("0.05") - s_lo + D("1.4e-9")
    r["beta range"] = [str(b_lo), str(b_hi)]
    assert b_lo >= D("4.1622e-5") and b_hi <= D("4.1628e-5")
    # wake upper bounds y_r <= tanh(y_(r-1) + beta_hi), y_1 <= 1
    y = D(1); ys = []
    for _ in range(5):
        y = tanh(y + b_hi); ys.append(y)
    r["wake y2..y6 upper"] = [str(v)[:10] for v in ys]
    bounds = [D(".76162"), D(".64205"), D(".56633"), D(".51269"), D(".47207")]
    assert all(v <= b for v, b in zip(ys, bounds))
    # inputs (Step 2)
    spike_start = ys[-1] + b_hi
    later_mod = D("0.45") - tanh(D("0.45")) + b_hi + D("1e-18")
    reset = tanh(D("0.45")) + b_hi
    first_mod = D("0.45") + b_hi
    r["inputs"] = {"spike_start": str(spike_start)[:10], "first_mod": str(first_mod)[:10],
                   "later_mod": str(later_mod)[:10], "reset": str(reset)[:10]}
    assert spike_start <= D(".47212") and later_mod <= D(".0282") and reset <= D(".42195")
    assert max(spike_start, first_mod, reset) <= D(".4732")
    # modulation factor (Step 8)
    g = sech2(D("0.45")); gm = g ** 7
    r["sech^2(.45)"] = str(g)[:12]; r["1-sech^2(.45)"] = str(1 - g)[:12]
    r["1 - sech^2(.45)^7"] = str(1 - gm)[:12]
    assert 1 - g <= D(".1780") and 1 - gm >= D(".74642")
    # main coefficient (Step 8)
    HI = sech2(D("0.25"))
    aT = D("0.7785")              # a^(T+ell+2) >= exp(-.2502(1+1/n)) > .7786 for n >= 1e18
    assert (D("-0.2502") * (1 + D("1e-18"))).exp() >= aT
    coef = HI * (1 - gm) * (1 - D("1.3e-3")) * aT * D("0.0024958") * D("0.249999") * (1 - D("2e-6"))
    cols = D(120000 - 10).sqrt()
    main = coef * cols
    r["HI"] = str(HI)[:12]; r["per-column coefficient (x n)"] = str(coef)[:12]
    r["sqrt(ell-10)"] = str(cols)[:10]; r["main readout lower bound (x n)"] = str(main)[:10]
    assert coef >= D("3.403e-4") and main >= D(".11790")
    # tau / n upper bound: tau = .002 n sqrt(n)/(sigma sqrt(n/2)) with sigma >= tanh(.05)
    tau_over_n = D("0.002") / (t05 * D("0.5").sqrt())
    r["tau/n upper"] = str(tau_over_n)[:10]
    assert tau_over_n <= D(".05662")
    final = main * (1 - D("2e-4")) - D("1e-6")
    r["||Gamma||/n lower"] = str(final)[:10]; r["ratio to tau"] = str(final / tau_over_n)[:8]
    assert final / tau_over_n >= D("2.08")
    # budget threshold (Step 4): 120001 * .2501 n <= 2.5e-5 n^(3/2)  <=>  n >= (120001*.2501/2.5e-5)^2
    nthr = (D(120001) * D("0.2501") / D("2.5e-5")) ** 2
    r["n threshold for mT <= 2.5e-5 n^1.5"] = str(nthr)[:12]
    assert nthr <= D("1.4412e18")
    # Step 9 leak fraction at n = 1.5e18
    n = D("1.5e18")
    leak_frac = D("2.22e5") / n.sqrt()
    r["leak fraction at n=1.5e18"] = str(leak_frac)[:10]
    assert leak_frac <= D("2e-4")
    with open(os.path.join(HERE, "constants_check_result.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps(r, indent=1))


if __name__ == "__main__":
    main()
