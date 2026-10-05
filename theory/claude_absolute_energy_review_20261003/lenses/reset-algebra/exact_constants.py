"""Exact rational / high-precision audit of PROOF.md (8),(9),(10) and REPORT table."""
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 60

b0 = F(1, 20)
def lam(n): return F(1, 100*n)
def e(n): return F(4, 10**8 * n**2)

# (9) coefficient at n=200 and monotonicity
c200 = b0 - lam(200) - 2*e(200)
print("b0-lam-2e at n=200 =", c200, "=", float(c200), "> 499/10000 ?", c200 > F(499, 10000))
print("margin over 499/10000:", c200 - F(499, 10000), float(c200 - F(499,10000)))
# monotone increasing in n: d/dn [-1/(100n) - 8e-8/n^2] = 1/(100n^2)+16e-8/n^3 > 0
ok = all(b0 - lam(n) - 2*e(n) < b0 - lam(n+1) - 2*e(n+1) for n in range(200, 5000))
print("strictly increasing on [200,5000):", ok)
# smallest n for which b0-lam-sqrt2*e_n > 0.0499 (domain-extension question)
for n in range(1, 400):
    if b0 - lam(n) - 2*e(n) > F(499, 10000):
        print("first n with b0-lam-2e > .0499:", n); break
# (9)-(10) constants
k2 = F(499, 10000)**2 / 2
print("(0.0499)^2/2 =", k2, "== 249001/200000000:", k2 == F(249001, 200000000))
inv = F(200000000, 249001)
print("200000000/249001 =", mp.mpf(inv.numerator)/inv.denominator)
print("803.209626 >= exact?", F(803209626, 10**6) >= inv)

# exact-ish check of L_n > 0.0499 sqrt(n/2) for all n in [200, 200000] in high precision
def Ln(n):
    n_ = mp.mpf(n); l = n - n//2
    return (mp.mpf(1)/20 - 1/(100*n_))*mp.sqrt(l) - 4/(mp.mpf(10)**8*n_**2)*mp.sqrt(n_)
worst = None
for n in list(range(200, 20001)) + [10**k for k in range(5, 13)]:
    ratio = Ln(n) / (mp.mpf('0.0499')*mp.sqrt(mp.mpf(n)/2))
    if worst is None or ratio < worst[1]:
        worst = (n, ratio)
print("min over tested n of L_n/(0.0499 sqrt(n/2)) :", worst[0], mp.nstr(worst[1], 15))

# REPORT table column
print("\nREPORT table 'Universal terminal norm lower bound' recomputed:")
for n in (200, 256, 400, 1000, 2000, 10**6):
    print(n, "l=", n - n//2, mp.nstr(Ln(n), 15), " 0.0499*sqrt(n/2)=", mp.nstr(mp.mpf('0.0499')*mp.sqrt(mp.mpf(n)/2), 12),
          " b0*sqrt(n)=", mp.nstr(mp.sqrt(n)/20, 12))

# C_abs
C = mp.sqrt(2*(mp.mpf(1)/400 + (mp.atanh(mp.mpf(2)/5) - mp.mpf(1)/20)**2))
print("\nC_abs =", mp.nstr(C, 40))
