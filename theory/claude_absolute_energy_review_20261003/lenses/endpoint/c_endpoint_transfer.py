"""(c) What happens to the accepted center if the common endpoint h=0 is replaced
by h*: reset input size/admissibility, reset energy, center energy; plus checks of
(1) with ACTUAL R vs (3)-(5), C_abs, B_n sign threshold. Diagnostics only."""
import numpy as np
import mpmath as mp
from model import build, fixed_point, B0

s, z0 = 0.4, 0.15
for n in (200, 400, 800, 1600):
    M = build(n)
    R, R0, k, ell, a, lam, en = (M[x] for x in ("R", "R0", "k", "ell", "a", "lam", "en"))
    b = B0 * np.ones(n)
    hstar, _ = fixed_point(R, b)
    beta = np.sqrt(z0 / n)
    p = np.r_[np.zeros(k), s * np.ones(ell)]
    v = np.r_[beta * np.ones(k), s * np.ones(ell)]
    N = int(np.ceil(4 * n * np.log(n))) + 1
    q = np.arctanh(v) - B0

    def E2(Rm, end):
        e_prep = np.linalg.norm(np.arctanh(p) - B0) ** 2
        e_first = np.linalg.norm(q - Rm @ p) ** 2
        e_int = (N - 1) * np.linalg.norm(q - Rm @ v) ** 2
        x_reset = np.arctanh(end) - Rm @ v - B0
        return e_prep + e_first + e_int + np.linalg.norm(x_reset) ** 2, x_reset

    ER2, xr0 = E2(R, np.zeros(n))
    E02, _ = E2(R0, np.zeros(n))
    Delta = en * np.sqrt(s * s * ell + N * (beta * beta * k + s * s * ell))
    # closed formula (3)
    A, Bb = np.arctanh(s), np.arctanh(beta)
    E0f = np.sqrt(k * (2 * B0 ** 2 + N * ((Bb - B0) ** 2 + a * a * beta * beta))
                  + ell * ((A - B0) ** 2 + N * (A - B0 - lam * s) ** 2 + (B0 + lam * s) ** 2))
    EHs2, xrs = E2(R, hstar)
    print(f"n={n}: E_R={np.sqrt(ER2):.9f} E0(closed)={E0f:.9f} |E_R-E0|={abs(np.sqrt(ER2)-E0f):.2e} Delta_n={Delta:.2e} "
          f"E_R/(n sqrt log n)={np.sqrt(ER2)/(n*np.sqrt(np.log(n))):.6f}")
    print(f"   reset->0: ||x||={np.linalg.norm(xr0):.4f} max|x|={np.max(np.abs(xr0)):.4f};  reset->h*: ||x||={np.linalg.norm(xrs):.4f} "
          f"max|x|={np.max(np.abs(xrs)):.4f} (past cube needs <1/2); center energy with endpoint h*: {np.sqrt(EHs2):.6f}")
    # zero-input relaxation from window state v to h*, then one correction; report energy & max input
    hcur = v.copy()
    for T in range(1, 20 * n + 1):
        if T in (1, n // 4, n, 5 * n, 20 * n):
            xc = np.arctanh(hstar) - R @ hcur - B0
            print(f"   relax {T-1} zero steps from window state then correct: ||x||={np.linalg.norm(xc):.3e} max|x|={np.max(np.abs(xc)):.3e}")
        hcur = np.tanh(R @ hcur + b)

C = mp.sqrt(2 * (mp.mpf(1) / 400 + (mp.atanh(mp.mpf(2) / 5) - mp.mpf(1) / 20) ** 2))
print("C_abs =", mp.nstr(C, 20))

# B_n sign threshold
def Bn(n):
    k = n // 2; r = k - 1; a = 1 - 1 / n
    Lat = 1 / (1 - 1 / (4 * n)); Cn = np.sqrt(r / (4 * n))
    return B0 * np.sqrt(r) - (Lat + a) * Cn - 4 / (1e8 * n ** 1.5)
signs = [(n, Bn(n) > 0) for n in range(200, 2001)]
first_pos = min(n for n, ok in signs if ok)
print("B_n>0 first at n =", first_pos, " all positive after:", all(ok for n, ok in signs if n >= first_pos),
      " B_399=", Bn(399), " B_400=", Bn(400))
# exact rational threshold check
from fractions import Fraction as F
print("200000000/249001 =", F(200000000, 249001), float(F(200000000, 249001)))
print("(499/10000)^2/2 =", F(499, 10000) ** 2 / 2)
print("min coefficient b0-lam-2e_n at n=200:", F(1, 20) - F(1, 20000) - F(8, 10 ** 8 * 200 ** 2))
# memory-block cancellation threshold: b0(sqrt k - gam/sqrt k) <= a
for n in range(796, 812, 2):
    k = n // 2; gam = 1 / (1 - 1 / np.sqrt(k))
    print(n, B0 * (np.sqrt(k) - gam / np.sqrt(k)) - (1 - 1 / n))
