"""Extrapolate the measured extremal mechanism (off-cycle hole held at 0) to all widths and
compare with THEOREM 4's delta_0.  Uses the exact actual-model scalars B*(n),H(n),sigma(n)
from fp_scan.json (n<=1e8) and their n->inf limits beyond.  All in mpmath (huge n).
Hole history (validated in full simulation at n<=64000 to <0.5%):
  energy(Th) = E_cl + (Th-1) B*^2,  E_cl ~ (A H + B*)^2 + (A H)^2  (create + land),
  ||M_T e_i|| ~ sigma (1-A^Th)/(1-A) * A (1-H^2) + (decayed baseline),
  credit = (a/n) sqrt(l) ||M_T||.
"""
import json, math
import mpmath as mp
mp.mp.dps = 130
fp = {r["n"]: r for r in json.load(open("fp_scan.json"))}
b0 = mp.mpf(1) / 20
Hinf = mp.tanh(b0); Binf = b0 - Hinf


def scalars(n):
    if n in fp and n <= 10 ** 8:
        r = fp[n]
        return mp.mpf(r["Bstar"]), mp.mpf(r["H_offcycle"]), mp.mpf(r["source"])
    # n -> infinity: H -> tanh(b0) (cycle excess O(n^-1/2)), B* = atanh(H)-aH
    a = 1 - mp.mpf(1) / n
    H = Hinf
    return mp.atanh(H) - a * H, H, mp.tanh(b0)


def theorem_delta0(n, R):
    n = mp.mpf(n)
    L = mp.ceil(mp.log(100 * mp.sqrt(n)) / mp.log(mp.mpf(10001) / 10000))
    B = mp.ceil(10000 * (1 + 10000 * R) ** 2)
    H = B + 10000
    l = n - mp.floor(n / 2)
    return mp.sqrt(l) * (L + H) / n


def hole_credit(n, R):
    Bs, H, sig = scalars(n)
    nn = mp.mpf(n); a = 1 - 1 / nn; A = a
    l = nn - mp.floor(nn / 2)
    Ecl = (A * H + Bs) ** 2 + (A * H) ** 2
    if R ** 2 <= Ecl:
        Th = 0
    else:
        Th = mp.floor((R ** 2 - Ecl) / Bs ** 2) + 1
    gate = 1 - H * H
    z_hold = sig * (1 - A ** Th) / (1 - A) * A * gate
    z_base = sig * gate / (1 - A * gate)
    z = max(z_hold + z_base * A ** Th * gate ** 0, z_base)
    return a / nn * mp.sqrt(l) * z, Th, Bs, H


rows = []
eps = mp.mpf("0.001")
for R in ("0.0711", "0.1", "1", "4", "16"):
    Rm = mp.mpf(R)
    grid = [4000, 8000, 16000, 32000, 64000, 10**5, 3*10**5, 10**6, 10**7, 10**8] + [mp.mpf(10)**e for e in (9,10,12,14,16,18,20,22,24,26,30,40,60,80)]
    for n in grid:
        c, Th, Bs, H = hole_credit(n, Rm)
        d0 = theorem_delta0(n, Rm)
        rows.append(dict(R=R, log10n=float(mp.log10(n)), hole_credit=mp.nstr(c, 6), Th=mp.nstr(Th, 6),
                         delta0=mp.nstr(d0, 6), ratio=mp.nstr(c / d0, 4),
                         below_eps_half=bool(c < eps / 2)))
for r in rows:
    print(r)
# exact crossover where the hole credit falls below eps/2, per R (asymptotic regime)
cross = {}
for R in ("0.0711", "0.1", "1", "4", "16"):
    Rm = mp.mpf(R)
    f = lambda le: hole_credit(mp.mpf(10) ** le, Rm)[0] - eps / 2
    lo, hi = mp.mpf(9), mp.mpf(60)
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    cross[R] = float(hi)
    print("R", R, "hole credit < eps/2 for log10 n >", mp.nstr(hi, 6))
# theorem's own threshold (delta0<=eps/2)
for R in ("0.0711", "1", "16"):
    Rm = mp.mpf(R)
    lo, hi = mp.mpf(6), mp.mpf(100)
    for _ in range(200):
        mid = (lo + hi) / 2
        if theorem_delta0(mp.mpf(10) ** mid, Rm) > eps / 2: lo = mid
        else: hi = mid
    print("R", R, "theorem delta0 < eps/2 for log10 n >", mp.nstr(hi, 6))
# n^(1/4) energy law: R needed for hole credit = eps, large n
Bs, H, sig = scalars(10 ** 30)
coef = mp.sqrt(mp.sqrt(2) * eps / sig) * Bs
print("hole: credit>=eps achievable with R^2 = E_cl + sqrt(2) eps B*^2 sqrt(n)/sigma  -> R ~", mp.nstr(coef, 6), "* n^(1/4)",
      " ; theorem necessary coefficient sqrt(eps)/1e6 =", mp.nstr(mp.sqrt(eps) / 10 ** 6, 6))
json.dump(dict(rows=rows, crossover_log10n=cross), open("extrapolate.json", "w"), indent=1)
