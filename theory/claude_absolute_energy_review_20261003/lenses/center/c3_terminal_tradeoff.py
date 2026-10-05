"""(i) Constants in (8)-(10); (ii) sharp terminal minimum min_{h in [-1,1]^n} ||R h + b0 1||
for the ACTUAL dense R (exact convex box-constrained least squares) vs the claimed L_n and vs a
sharpened closed form that also uses the memory block; (iii) the trivial one-step history;
(iv) a 2-step history optimiser to see that multi-step resets cannot go below the one-step bound;
(v) eq. (14) elimination check at huge n."""
import numpy as np
import mpmath as mp
from fractions import Fraction as Fr
from scipy.optimize import lsq_linear, minimize
import sys
sys.path.insert(0, '.')
from c2_dense import build

# (i) constants
b0 = Fr(1, 20)
coef = b0 - Fr(1, 20000) - Fr(8, 10**8 * 200**2)
print("b0 - lambda_max - 2 e_max =", coef, float(coef), "> 0.0499:", coef > Fr(499, 10000))
print("sqrt(n/l) <= sqrt(2) (proof uses 2): fine")
print("0.0499^2/2 =", Fr(499, 10000)**2 / 2, "==", Fr(249001, 200000000))
mp.mp.dps = 40
print("2e8/249001 =", mp.nstr(mp.mpf(200000000) / 249001, 20))
print("sharp asymptotic constant 1/b0^2 =", 1 / float(b0)**2)

# (ii)-(iv)
for n in (200, 400, 1000, 2000):
    k, l, d, a, w, U, P, O, R0, R = build(n)
    lam = 1 / (100 * n)
    en = 4e-8 / n**2
    gam = 2 / (w @ w)
    Ln = (0.05 - lam) * np.sqrt(l) - en * np.sqrt(n)
    mem_sharp = max(0.0, 0.05 * (np.sqrt(k) - gam / np.sqrt(k)) - a)
    Lsharp = np.sqrt(l * (0.05 - lam)**2 + mem_sharp**2) - en * np.sqrt(n)
    # exact min over the closed box of ||R h + b0 1|| (convex)
    res = lsq_linear(R, -0.05 * np.ones(n), bounds=(-1, 1), lsmr_tol='auto', tol=1e-14, max_iter=5000)
    exact_min = np.linalg.norm(R @ res.x + 0.05)
    # memory-block-only and source-block-only minima for R0
    resm = lsq_linear(a * O, -0.05 * np.ones(k), bounds=(-1, 1), tol=1e-14, max_iter=5000)
    mem_min = np.linalg.norm(a * O @ resm.x + 0.05)
    one_step = 0.05 * np.sqrt(n)
    print(f"n={n}: claimed L_n={Ln:.6f}  0.0499*sqrt(n/2)={0.0499 * np.sqrt(n / 2):.6f}  sharpened={Lsharp:.6f}  "
          f"exact min_h||Rh+b||={exact_min:.6f}  (R0 memory-block min={mem_min:.6f} vs closed {mem_sharp:.6f})  "
          f"one-step history ||X||=b0 sqrt(n)={one_step:.6f}")
    # (iv) 2-step history 0 -> h1 -> 0 : minimise ||atanh(h1)-b0||^2 + ||R h1 + b0||^2 over h1 in (-1,1)^n
    def f(u):
        h = np.tanh(u)
        x1 = u - 0.05
        x2 = R @ h + 0.05
        val = x1 @ x1 + x2 @ x2
        g = 2 * x1 + (R.T @ (2 * x2)) * (1 - h**2)
        return val, g
    best = np.inf
    for u0 in (np.zeros(n), np.full(n, 0.05), -np.arctanh(np.clip(res.x, -0.999, 0.999))):
        r = minimize(f, u0, jac=True, method='L-BFGS-B', options=dict(maxiter=20000, ftol=1e-15, gtol=1e-12))
        best = min(best, np.sqrt(r.fun))
    print(f"      best 2-step zero-endpoint history energy found={best:.6f}  (>= exact one-step terminal min? {best >= exact_min - 1e-9})")

# (v) eq. (14)
mp.mp.dps = 60
b0m, s = mp.mpf(1) / 20, mp.mpf(2) / 5
C = mp.sqrt(2 * (b0m**2 + (mp.atanh(s) - b0m)**2))
for e10 in (900, 5000, 50000):
    n = mp.mpf(10)**e10
    d = mp.floor(n / 4)
    D = mp.floor(d / 10**6) * mp.floor(n**(mp.mpf(1) / 18))
    D_asym = n**(mp.mpf(19) / 18) / (4 * 10**6)
    Rfam = C * (4e6 * D)**(mp.mpf(18) / 19) * mp.sqrt(mp.mpf(18) / 19 * mp.log(4e6 * D))
    Ecen = C * n * mp.sqrt(mp.log(n))
    print(f"n=1e{e10}: D/D_asym-1={mp.nstr(D / D_asym - 1, 5)}  D/(n^(19/18)/2e7)={mp.nstr(D / (n**(mp.mpf(19) / 18) / 2e7), 6)}  "
          f"R_family(14)/(C n sqrt log n)-1={mp.nstr(Rfam / Ecen - 1, 5)}")
