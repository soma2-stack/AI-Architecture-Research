"""All-n certificate for the repaired second-order bound (PROOF.md section 5R, Proposition 5.4).

Replaces the refuted grid certificate `constants_so.py` (Codex audit F1).

Method (exact rational arithmetic, no floating point in the certificate path).
* Put x = n^(1/4) and fix a rational x_* > 0. Every quantity of Lemmas 5.1R/5.2R is bounded above,
  for ALL real x >= x_* (hence all integers n >= x_*^4, with H = ceil(40 n^(3/4)) and
  D = floor((n/4 - 41)/(H+1)) handled through H in [40 x^3, 40 x^3 + 1] and D <= x/160),
  by an "envelope"   E(x) = sum_p c_p (x/x_*)^p,  with rational c_p >= 0 and integer p.
* The bound chain uses only +, x and t -> 1/(1-t) (no subtraction, no division), so envelopes
  compose: sums and products of nonnegative upper bounds are upper bounds, and
  1/(1 - u(x)) <= 1/(1 - E_u(x_*)) whenever every exponent of E_u is <= 0 and E_u(x_*) < 1
  (then E_u is nonincreasing on [x_*, inf), so u(x) <= E_u(x) <= E_u(x_*) < 1).
* If the final envelope of eps_SO has every exponent <= 0, then eps_SO(n) <= E(x) <= E(x_*) for
  all n >= x_*^4. The script asserts this and E(x_*) <= 1/2. No grid, no monotonicity of rounded
  functions, and no limit argument is used.
* Coefficients are rounded UP to 40 significant digits (outward), which preserves validity.

The SAME bound chain `chain(A)` is also evaluated pointwise in high-precision Decimal at given
integers n with exact integer H and D, and high-precision gamma, a^(-d), F*. The exponentially
small, strictly positive front gate is retained via a proven positive rational upper bound:
a direct Decimal exponential cannot represent it at the largest dimensions. Thus the
pointwise calculation is a conservative upper-bound consistency test, NOT an exact evaluation
of the front gate, and NOT part of the proof. Test dimensions include the audit's rounding
points, 1e166, 1e168, 1e180, ... .

Run: python -I envelope_certificate.py   (writes envelope_certificate_result.json)
"""
import json, math, os
from decimal import Decimal, getcontext
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- constants (exact rationals)
Q = F(1600)                 # 1/s_lo^2
XB = F("0.1316")            # |delta| on active pair rows (>= tanh(.38)^2, s_hi^2)
DF = F("39.73")             # front deviation mass incl. row 1 (Codex-certified < 39.723)
DB = F("40.01")             # sum_j |delta_t(j)| and |S_t|  (39.73 + .1009^2 + 2*.1316 < 40.01)
CS = F("0.3331")            # |x+ - x-| <= c_s Pi (Codex-certified)
CSTAR = 1 + F(1, 10**12)
S_HI, S_LO = F("0.1009"), F(1, 40)
EG0 = F("4.009")            # Lemma 5.0R: g_1(t) <= EG0 exp(-.05 sqrt(k)) for t >= 2
R_LO, R_HI = F("1.41421356"), F("1.41421357")     # sqrt(2) bracket
NEXP = 40                   # eps_g envelope exponent
SIGDIG = 40


def up(c):
    """Round a nonnegative rational UP to SIGDIG significant digits."""
    c = F(c)
    assert c >= 0
    if c == 0:
        return c
    e = len(str(c.numerator)) - len(str(c.denominator))          # 10^(e-1) < c < 10^(e+1)
    sh = SIGDIG - e
    if sh >= 0:
        m = -((-c.numerator * 10 ** sh) // c.denominator)
        return F(m, 10 ** sh)
    m = -((-c.numerator) // (c.denominator * 10 ** (-sh)))
    return F(m * 10 ** (-sh))


class Env:
    """sum_p c_p (x/x_*)^p with c_p >= 0; an upper bound valid for every x >= x_*."""

    def __init__(self, t=None):
        self.t = {}
        for p, c in (t or {}).items():
            c = F(c)
            assert c >= 0, "negative coefficient"
            if c:
                self.t[p] = up(self.t.get(p, F(0)) + c)

    @staticmethod
    def lift(o):
        return o if isinstance(o, Env) else Env({0: o})

    def __add__(self, o):
        o = Env.lift(o); r = dict(self.t)
        for p, c in o.t.items():
            r[p] = r.get(p, F(0)) + c
        return Env(r)
    __radd__ = __add__

    def __mul__(self, o):
        o = Env.lift(o); r = {}
        for p, c in self.t.items():
            for q, e in o.t.items():
                r[p + q] = r.get(p + q, F(0)) + c * e
        return Env(r)
    __rmul__ = __mul__

    def maxexp(self):
        return max(self.t) if self.t else -10 ** 9

    def value(self):
        return sum(self.t.values(), F(0))


# ---------------------------------------------------------------- rational special-function bounds
def exp_upper(x, N=40):
    """Upper bound for e^x, 0 <= x <= 2 (Taylor + geometric tail)."""
    x = F(x); assert 0 <= x <= 2
    term = F(1); s = F(1)
    for j in range(1, N + 1):
        term *= x / j; s += term
    return s + (term * x / (N + 1)) / (1 - x / (N + 2))


def exp_lower_big(y, M=20):
    """Lower bound for e^y, y >= 0 (Taylor partial sum)."""
    y = F(y); term = F(1); s = F(1)
    for j in range(1, M + 1):
        term *= y / j; s += term
    return s


class EnvArith:
    """Primitive envelopes for x >= x_* (n = x^4)."""

    def __init__(self, xs):
        xs = F(xs); self.xs = xs
        assert R_LO ** 2 < 2 < R_HI ** 2
        n_star = xs ** 4
        assert n_star >= 10 ** 8
        self.c = lambda v: Env({0: F(v)})
        self.inv_k = Env({-4: 2 / xs ** 4})                      # 1/k = 2 x^-4
        self.sk = Env({2: xs ** 2 / R_LO})                       # sqrt k = x^2/sqrt 2
        self.inv_sk = Env({-2: R_HI / xs ** 2})
        self.gam = Env({0: 1 / (1 - R_HI / xs ** 2)})            # gamma decreasing in x
        self.dd = Env({4: xs ** 4 / 4})                          # d = x^4/4
        self.H1 = Env({3: 40 * xs ** 3, 0: 2})                   # H+1 <= 40x^3 + 2
        self.invH = Env({-3: 1 / (40 * xs ** 3)})                # 1/H <= 1/(40 x^3)
        self.Dm = Env({1: xs / 160})                             # D <= x/160
        # eps_g(n) = EG0 exp(-.05 x^2/sqrt 2) <= EG0 exp(-c x^2), c = .05/R_HI
        c = F(1, 20) / R_HI
        assert c * xs ** 2 >= F(NEXP, 2)                         # => (x/x*)^NEXP e^{-c(x^2-x*^2)} <= 1
        cg = EG0 / exp_lower_big(c * xs ** 2)
        self.epsg = Env({-NEXP: cg})
        self.cg = cg
        # a^-d <= exp(1/4 + 1/(4(n-1)));  a^-(2d+1) <= exp(1/2 + 3/(2(n-1)))
        e1 = exp_upper(F(1, 4) + F(1, 4) / (n_star - 1))
        e2 = exp_upper(F(1, 2) + F(3, 2) / (n_star - 1))
        self.inv_ad = Env({0: e1})
        # F* >= (2/x^4) e^-... .99 s_lo^2 (H-1)(H-14)/4 >= 792 s_lo^2 (1-.35/x*^3)^2 x^2 / e2
        fl = 792 * S_LO ** 2 * (1 - F(35, 100) / xs ** 3) ** 2 / e2 * xs ** 2
        self.invF = Env({-2: 1 / fl})

    def inv1m(self, u):
        assert u.maxexp() <= 0, "closure argument not nonincreasing"
        v = u.value()
        assert v < 1, "closure condition fails"
        return Env({0: 1 / (1 - v)})


class DecArith:
    """Exact integer geometry and conservative Decimal upper-bound evaluation at n (not a proof)."""

    def __init__(self, n):
        assert n % 4 == 0
        getcontext().prec = len(str(n)) + 60
        Dd = Decimal
        self.n = n
        k = Dd(n) / 2; self.c = lambda v: Dd(F(v).numerator) / Dd(F(v).denominator)
        sk = k.sqrt()
        self.inv_k, self.sk, self.inv_sk = 1 / k, sk, 1 / sk
        self.gam = 1 / (1 - 1 / sk)
        self.dd = Dd(n) / 4
        H = ceil_root4(40 ** 4 * n ** 3)                         # ceil(40 n^(3/4)) exactly
        self.H = H
        self.H1, self.invH = Dd(H + 1), 1 / Dd(H)
        self.Dm = Dd((n // 4 - 41) // (H + 1))
        self.D = (n // 4 - 41) // (H + 1)
        # Keep the positive front-gate term. Decimal exp(-.05*sqrt(k)) underflows at
        # theorem-scale n; use the proven rational envelope bound instead of zero.
        # n >= XS^4 and NEXP=40 give eps_g(n) <= c_g*(XS^4/n)^10, with c_g>0.
        xs = 31622
        assert n >= xs ** 4 and NEXP % 4 == 0
        cg = EG0 / exp_lower_big((F(1, 20) / R_HI) * xs ** 2)
        self.epsg = self.c(cg) * (Dd(xs ** 4) / Dd(n)) ** (NEXP // 4)
        assert self.epsg > 0
        lna = (1 - 1 / Dd(n)).ln()
        self.inv_ad = (-(self.dd) * lna).exp()
        Fs = self.gam / k * ((2 * self.dd + 1) * lna).exp() * Dd("0.99") * self.c(S_LO) ** 2 \
            * Dd(H // 2) * Dd(-(-H // 2) - 7)
        self.invF = 1 / Fs

    def inv1m(self, u):
        assert u < 1, "pointwise closure fails"
        return 1 / (1 - u)


def ceil_root4(m):
    """ceil(m^(1/4)) for a positive integer m (exact integer arithmetic)."""
    r = math.isqrt(math.isqrt(m))            # floor(m^(1/4))
    return r if r ** 4 >= m else r + 1


def icbrt_floor(m):
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


def H_jump_after(n):
    """Return (n0, n1): consecutive multiples of 4 with n0 <= n < ..., H(n1) = H(n0) + 1 (a rounding jump)."""
    H0 = ceil_root4(40 ** 4 * n ** 3)
    # H(n) <= H0  <=>  40^4 n^3 <= H0^4  <=>  n <= floor(cbrt(H0^4 / 40^4))
    nmax = icbrt_floor(H0 ** 4 // 40 ** 4)
    while 40 ** 4 * (nmax + 1) ** 3 <= H0 ** 4:
        nmax += 1
    n0 = nmax // 4 * 4
    n1 = n0 + 4
    assert ceil_root4(40 ** 4 * n0 ** 3) == H0 and ceil_root4(40 ** 4 * n1 ** 3) == H0 + 1
    return n0, n1


# ---------------------------------------------------------------- the bound chain (Lemmas 5.1R, 5.2R)
def chain(A):
    c = A.c
    one, two = c(1), c(2)
    Qc, XBc, DFc, DBc, CSc, CST, SH2 = c(Q), c(XB), c(DF), c(DB), c(CS), c(CSTAR), c(S_HI ** 2)
    g, ik, isk, sk, dd, H1, iH, eg = A.gam, A.inv_k, A.inv_sk, A.sk, A.dd, A.H1, A.invH, A.epsg
    gk, gsk = g * ik, g * isk
    u1 = one + g * DBc * ik                                     # 1 + gamma Dbar/k
    # capture constants
    kc = gsk * (DFc + g * DBc * Qc * ik)
    kb = g * g * DBc * Qc * ik * isk
    kh = gsk * (XBc + g * DBc * ik)
    ks = gsk * (SH2 + g * DBc * ik)
    kA = gsk * DBc * (one + g * c(F(1, 2)))
    # Lemma 5.1R: background bounds (one history, one memory column)
    Q1 = (Qc + eg * sk) * A.inv1m(kc + eg * u1)
    Q2 = kb * Q1 + Qc
    Eeta = Q2 + H1 * (kh * Q1 + one)
    Epi = Q1 + dd * (ks * Q1 + one)
    cfb = gk * (u1 * Q1 + DFc * Q1 + SH2 * Epi + two * XBc * Eeta) + isk
    fsup = gk * CST * (XBc * (Qc + H1) + one)
    lhat = fsup * A.inv1m(cfb)
    Lin = gk * CST * ((SH2 * H1 + c(7) * XBc) * (Qc + H1) + H1) + H1 * cfb * lhat
    eta_self = Q2 * lhat + kh * Q1 * lhat * H1 + Lin
    cout = gk * (SH2 * dd + two * XBc * H1)
    Y0 = u1 * Q1 * lhat + sk * lhat                             # sup |Y_t(0)| (sqrt k/gamma <= sqrt k)
    lout = (gk * CST + gk * SH2 * Lin
            + (isk + gk * (u1 * Q1 + DFc * Q1 + SH2 * Q1 * (one + dd * ks) + two * XBc * (Q2 + H1 * kh * Q1))) * lhat) \
        * A.inv1m(cout)
    eta_oth = Q2 * lhat + kh * (H1 * kc * Q1 * lhat + Qc * Lin + H1 * Qc * lout + H1 * eg * Y0) + H1 * lout
    # Lemma 5.2R: difference bootstrap
    bA = (Qc + eg * sk) * A.inv1m(kA + eg * u1)
    sS = g * g * ik * isk * Q1 * lhat * c(14) * CSc             # sigma_S per unit Pi
    aL = isk + gk * (DFc * Qc + SH2 * dd + two * XBc * H1 * (two + Qc * iH)) + DFc * eg * isk
    aA = gk * (u1 * (one + DFc * Qc * gsk + DFc * eg) + SH2 * dd * ks + two * XBc * H1 * (kh + kb))
    e = aL + aA * bA
    ie = A.inv1m(e)

    def src(eta):
        pulse = c(14) * CSc * (eta + gsk * (one + two * gk) * Q1 * lhat)
        R = gk * ((one + DFc * eg) * gk * Q1 * lhat * c(14) * CSc + DFc * Qc * sS + SH2 * dd * sS
                  + two * XBc * H1 * ((two + Qc * iH) * sS + pulse) + c(14) * CSc * eta)
        return (one + ks * bA) * (aA * bA * sS + R) * ie + ks * bA * sS + sS

    eps1 = ks * bA + (one + ks * bA) * e * ie
    Ps, Po = src(eta_self), src(eta_oth)
    t1, t2, t3 = eps1 * A.inv_ad, Ps * A.invF, A.Dm * Po * A.invF
    return {"eps_SO": t1 + t2 + t3, "eps1/a^d": t1, "Phi_self/F*": t2, "D*Phi_oth/F*": t3,
            "e": e, "cfb": cfb, "cout": cout, "kc+": kc + eg * u1, "kA+": kA + eg * u1}


def envelope(xs):
    A = EnvArith(xs)
    r = chain(A)
    return A, r


def smallest_xstar(lo, hi):
    """Bisect for the least integer x_* in [lo, hi] at which the envelope certifies eps_SO <= 1/2."""
    def ok(xs):
        try:
            _, r = envelope(xs)
        except AssertionError:
            return False
        E = r["eps_SO"]
        return E.maxexp() <= 0 and E.value() <= F(1, 2)
    assert ok(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def sci(v, lim):
    return str(v) if v < 10 ** lim else "{:.5e}".format(Decimal(v))


def front_gate_constants():
    """Lemma 5.0R constants, n >= 1e8: pre_1 >= .025 sqrt(k) - .1/sqrt(k) - .025 sqrt(k)/n >= .025 sqrt(k) - .001,
    and sech^2(p) <= 4 e^(-2p) <= 4 e^(.002) e^(-.05 sqrt k) <= EG0 e^(-.05 sqrt k)."""
    beta_max = F(1, 7071)                 # sqrt(k) >= sqrt(5e7) > 7071
    sk_over_n_max = F(1, 14142)           # sqrt(k)/n = 1/sqrt(2n) <= 1/sqrt(2e8) < 1/14142
    assert 7071 ** 2 <= 5 * 10 ** 7 and 14142 ** 2 <= 2 * 10 ** 8
    slack = F(1, 10) * beta_max + F(1, 40) * sk_over_n_max
    assert slack <= F(1, 1000)
    eg = 4 * exp_upper(F(2, 1000))
    assert eg <= EG0
    return {"pre_1 slack (<= .001)": float(slack), "4 e^.002 (<= 4.009)": float(eg)}


def main():
    out = {}
    out["Lemma 5.0R constants"] = front_gate_constants()
    XS = 31622                                                   # 31622^4 < 10^18
    A, r = envelope(XS)
    E = r["eps_SO"]
    assert E.maxexp() <= 0, "final envelope not nonincreasing"
    val = E.value()
    assert val <= F(".3747"), "the theorem's stated second-order margin must hold"
    out["x_star"] = XS
    out["n_star = x_star^4"] = str(XS ** 4)
    out["certified: eps_SO(n) <= value for all n >= x_star^4"] = float(val)
    out["max exponent of final envelope"] = E.maxexp()
    out["components at x_star (upper bounds)"] = {kk: float(v.value()) for kk, v in r.items()}
    out["component max exponents"] = {kk: v.maxexp() for kk, v in r.items()}
    out["eps_g envelope coefficient c_g (upper bound of eps_g at x_star)"] = f"{float(A.cg):.3e}"
    xmin = smallest_xstar(1000, XS)
    _, rmin = envelope(xmin)
    out["bisection: integer x_star certified by the same method"] = xmin
    out["corresponding n_star"] = f"{xmin ** 4:.6e}"
    out["envelope eps_SO at that x_star"] = float(rmin["eps_SO"].value())
    # consistency tests: envelope (x_* = XS) dominates the pointwise formula at adversarial n
    tests = []
    cands = [10 ** 18, 10 ** 18 + 4, 1000000000000000280, 1000000000000000284,
             4 * ((XS + 1) ** 4 // 4 + 1), 10 ** 24, 10 ** 40, 10 ** 160, 10 ** 164, 10 ** 165,
             10 ** 166, 10 ** 168, 10 ** 180, 10 ** 300, 10 ** 1000]
    # adversarial rounding: consecutive multiples of 4 at which H = ceil(40 n^(3/4)) jumps up
    for base in (10 ** 18, 10 ** 30, 10 ** 60, 10 ** 166):
        cands += list(H_jump_after(base))
    for n in cands:
        n = n // 4 * 4
        P = DecArith(n)
        rp = chain(P)
        # envelope evaluated at this n's own x = n^(1/4) (it must dominate pointwise there too)
        xr = Decimal(n) ** (Decimal(1) / 4) / Decimal(XS)
        Ex = sum(Decimal(cf.numerator) / Decimal(cf.denominator) * xr ** p for p, cf in E.t.items())
        rec = {"n": sci(n, 20), "H": sci(P.H, 30), "D": sci(P.D, 30),
               "front_gate_upper_bound_positive": bool(P.epsg > 0),
               "envelope_at_own_x": float(Ex), "dominated_at_own_x": bool(rp["eps_SO"] <= Ex),
               "eps_SO_pointwise": float(rp["eps_SO"]), "e_pointwise": float(rp["e"]),
               "envelope_bound": float(val), "dominated": bool(rp["eps_SO"] <= Decimal(val.numerator) / Decimal(val.denominator))}
        assert rec["dominated"] and rec["dominated_at_own_x"]
        tests.append(rec)
        print(json.dumps(rec))
    out["pointwise consistency tests (not part of the proof)"] = tests
    json.dump(out, open(os.path.join(HERE, "envelope_certificate_result.json"), "w"), indent=1)
    print(json.dumps({kk: v for kk, v in out.items() if kk != "pointwise consistency tests (not part of the proof)"}, indent=1))


if __name__ == "__main__":
    main()
