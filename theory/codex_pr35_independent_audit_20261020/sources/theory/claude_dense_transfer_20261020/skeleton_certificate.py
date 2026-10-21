"""All-n certificate for the skeleton-coded sequential section S_K (PROOF.md section 9).

S_K is S with r = 2D - 1 memory pairs, hold H = 250 N3^2 (N3 = floor(n^(1/3))), and section dimension
D = floor(N3/2400). Pair c carries the amplitude z_c(theta) = clip(L (M theta)_c, [-1,1]) for a fixed
r x D Vandermonde matrix M (Lemma 9.1: at least j = r - D + 1 = D pairs saturate for every unit theta).

The second-order bound is the SAME bound chain as PR #34 (`chain` imported unchanged from
../claude_lemma_m_three_memory_20261019/envelope_certificate.py). Only the primitive envelopes change,
because H and the number of memories r now scale as n^(2/3) and n^(1/3). Variable: y = n^(1/12).
The script certifies, for all integers n >= y_*^12:
  (a) every closure condition and eps_SO(n) <= E (exact rational envelope, all exponents <= 0);
  (b) robustness: (1 - E) c_R Pi(1) sqrt(j) (H/2 - 7)^2 / n^(3/2) > .0567 (>= tau/n), with
      c_R >= .0004988 and Pi(1) >= .6272 (both rationally certified in the Codex PR #33 audit);
  (c) fit: r (H + 1) <= d - 41.
A pointwise high-precision consistency check (not part of the proof) is run at several n.
Run: python -I skeleton_certificate.py   (writes skeleton_certificate_result.json)
"""
import importlib.util, json, math, os
from decimal import Decimal, getcontext
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "claude_lemma_m_three_memory_20261019", "envelope_certificate.py")
spec = importlib.util.spec_from_file_location("ec", SRC); ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
Env, chain = ec.Env, ec.chain

HH, KAPPA_DEN = 250, 2400          # H = 250 N3^2 ; D = floor(N3/2400) ; r = 2D - 1
C_R, PI1 = F("0.0004988"), F("0.6272")


class EnvArithY:
    """Primitive envelopes for y = n^(1/12) >= y_*."""

    def __init__(self, ys):
        ys = F(ys); self.ys = ys
        n_star = ys ** 12
        assert n_star >= 10 ** 8
        R_LO, R_HI = ec.R_LO, ec.R_HI
        self.c = lambda v: Env({0: F(v)})
        self.inv_k = Env({-12: 2 / ys ** 12})
        self.sk = Env({6: ys ** 6 / R_LO})
        self.inv_sk = Env({-6: R_HI / ys ** 6})
        self.gam = Env({0: 1 / (1 - R_HI / ys ** 6)})
        self.dd = Env({12: ys ** 12 / 4})
        self.H1 = Env({8: HH * ys ** 8, 0: 1})                     # H + 1 <= 250 n^(2/3) + 1
        lo = (1 - 1 / ys ** 4) ** 2                                 # (n^(1/3) - 1)^2 >= n^(2/3)(1 - y*^-4)^2
        self.invH = Env({-8: 1 / (HH * lo * ys ** 8)})
        self.Dm = Env({4: ys ** 4 / (KAPPA_DEN // 2)})              # r <= 2 N3/2400 <= y^4/1200
        c = F(1, 20) / R_HI
        assert c * ys ** 6 >= F(ec.NEXP, 6)                         # (y/y*)^N e^{-c(y^6 - y*^6)} <= 1
        cg = ec.EG0 / ec.exp_lower_big(c * ys ** 6)
        self.epsg = Env({-ec.NEXP: cg}); self.cg = cg
        e1 = ec.exp_upper(F(1, 4) + F(1, 4) / (n_star - 1))
        e2 = ec.exp_upper(F(1, 2) + F(3, 2) / (n_star - 1))
        self.inv_ad = Env({0: e1})
        Hlo_star = HH * lo * ys ** 8
        fl = F(495, 1000) * HH ** 2 * ec.S_LO ** 2 * lo ** 2 * (1 - 14 / Hlo_star) ** 2 / e2 * ys ** 4
        self.invF = Env({-4: 1 / fl})                               # F* >= fl (y/y*)^4

    def inv1m(self, u):
        assert u.maxexp() <= 0, "closure argument not nonincreasing"
        v = u.value(); assert v < 1, "closure condition fails"
        return Env({0: 1 / (1 - v)})


def robust_ok(ys, E):
    """(1 - E) c_R Pi(1) sqrt(j) (H/2 - 7)^2 / n^(3/2) > .0567 for all y >= y_*, j >= (y^4 - 2401)/2400."""
    ys = F(ys)
    g = (1 - F(2401) / ys ** 4) * (1 - 1 / ys ** 4) ** 4 * (1 - F(7) / (125 * (ys ** 4 - 1) ** 2)) ** 2
    finf = F(125) ** 2 / 49                                       # 1/sqrt(2400) >= 1/49
    val = (1 - E) * C_R * PI1 * finf * g
    return val > F("0.0567"), val


def certify(ys):
    A = EnvArithY(ys)
    r = chain(A)
    E = r["eps_SO"]
    if E.maxexp() > 0:
        return False, None, None, r
    ok, val = robust_ok(ys, E.value())
    # fit: r(H+1) <= y^4/1200 (250 y^8 + 1) <= n/4 - 41  <=>  250/1200 + 1/(1200 y^8) + 41/y^12 <= 1/4
    fit = F(HH, KAPPA_DEN // 2) + 1 / (F(KAPPA_DEN // 2) * F(ys) ** 8) + F(41) / F(ys) ** 12 <= F(1, 4)
    return ok and fit, E.value(), val, r


def icbrt(m):
    lo, hi = 0, 1
    while hi ** 3 <= m:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 3 <= m:
            lo = mid
        else:
            hi = mid
    return lo


class DecArithS:
    """Pointwise (consistency only, not a proof): exact integer H = 250 N3^2, r = 2D - 1, at n >= y_*^12.
    The tiny front gate is kept positive through the proved envelope bound c_g(y_*) (y_*^12/n)^(NEXP/12)."""

    def __init__(self, n, ys):
        assert n % 4 == 0 and n >= ys ** 12
        getcontext().prec = len(str(n)) + 60
        Dd = Decimal; self.c = lambda v: Dd(F(v).numerator) / Dd(F(v).denominator)
        k = Dd(n) / 2; sk = k.sqrt()
        self.inv_k, self.sk, self.inv_sk = 1 / k, sk, 1 / sk
        self.gam = 1 / (1 - 1 / sk); self.dd = Dd(n) / 4
        N3 = icbrt(n); H = HH * N3 * N3; Dsec = N3 // KAPPA_DEN; r = 2 * Dsec - 1
        self.H, self.D, self.r = H, Dsec, r
        self.H1, self.invH, self.Dm = Dd(H + 1), 1 / Dd(H), Dd(r)
        cg = ec.EG0 / ec.exp_lower_big((F(1, 20) / ec.R_HI) * F(ys) ** 6)
        self.epsg = self.c(cg) * (Dd(ys ** 12) / Dd(n)) ** (Dd(ec.NEXP) / 12)
        assert self.epsg > 0
        lna = (1 - 1 / Dd(n)).ln()
        self.inv_ad = (-(self.dd) * lna).exp()
        Fs = self.gam / k * ((2 * self.dd + 1) * lna).exp() * Dd("0.99") * self.c(ec.S_LO) ** 2 * Dd(H // 2) * Dd(-(-H // 2) - 7)
        self.invF = 1 / Fs

    def inv1m(self, u):
        assert u < 1, "pointwise closure fails"
        return 1 / (1 - u)


def main():
    out = {}
    # smallest integer y_* certified (bisection on a monotone-in-practice predicate; any certified y_* is valid)
    lo, hi = 10, 400
    assert certify(hi)[0]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        try:
            ok = certify(mid)[0]
        except AssertionError:
            ok = False
        if ok:
            hi = mid
        else:
            lo = mid
    ys = hi
    ok, E, val, r = certify(ys)
    assert ok
    out["y_star"] = ys
    out["n_star = y_star^12"] = f"{F(ys) ** 12:.6e}" if False else "{:.6e}".format(Decimal(ys) ** 12)
    out["certified eps_SO <= E for all n >= n_star"] = float(E)
    out["robustness ratio lower bound (needs > .0567)"] = float(val)
    out["components at y_star"] = {kk: float(v.value()) for kk, v in r.items()}
    out["component max exponents"] = {kk: v.maxexp() for kk, v in r.items()}
    out["D at n_star (>= y^4/2400 - 2)"] = float(F(ys) ** 4 / 2400 - 2)
    # consistency: pointwise chain at several n is dominated by the envelope value E (n >= n_star)
    tests = []
    nstar = ys ** 12
    for n in [nstar + (-nstar) % 4, 10 ** 24, 10 ** 30, 10 ** 40, 10 ** 60, 10 ** 100]:
        if n < nstar:
            continue
        n = n // 4 * 4
        P = DecArithS(n, ys)
        rp = chain(P)
        rec = {"n": "{:.4e}".format(Decimal(n)), "D": P.D, "r": P.r, "H": "{:.4e}".format(Decimal(P.H)),
               "eps_SO pointwise": float(rp["eps_SO"]), "<= E": bool(rp["eps_SO"] <= Decimal(E.numerator) / Decimal(E.denominator))}
        assert rec["<= E"]
        tests.append(rec); print(json.dumps(rec))
    out["pointwise consistency (not proof)"] = tests
    json.dump(out, open(os.path.join(HERE, "skeleton_certificate_result.json"), "w"), indent=1)
    print(json.dumps({kk: v for kk, v in out.items() if kk != "pointwise consistency (not proof)"}, indent=1))


if __name__ == "__main__":
    main()
