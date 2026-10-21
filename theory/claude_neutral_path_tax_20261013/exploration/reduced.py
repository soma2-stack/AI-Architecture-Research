"""Reduced type-level model of the held window (n -> infinity limit), vertex code.

Types (fractions of the k memory rows): gate-1 written rows s/2, gate-g* written rows s/2,
bath rows s_b.  Scaled per-row credit xi = x sqrt(k)/c_h, scaled drive
    j = gamma - gamma^2 (s1 xi1 + sg xig + sb xib)           (broadcast minus mean)
    xi1' = a (xi1 + j),  xig' = g* a (xig + j),  xib' = gb a (xib + j).
Prediction:  sep = sigma sqrt(l)/n * (hi-lo)/2 /sqrt(n) * a^2 g_r * k s |xi1 - xig| * c_h/sqrt(k),
with c_h = sqrt(L1 L2/(L1+L2)) * (1 - exp(-T0/n)) n/T0   (hole credit incl. a^(T0-s) decay).
"""
import math
import sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 16000
s = float(sys.argv[2]) if len(sys.argv) > 2 else 0.92
c, delta = 0.22, 0.22
k, d = n // 2, n // 4
a, gamma = 1 - 1 / n, 1 / (1 - 1 / math.sqrt(k))
gstar = 1 - (c + delta) ** 2
gb = 1 - 0.12 ** 2            # bath gate during the window (state mean shift)
gr = 1 - 0.05 ** 2
L1, L2 = d - 40, k - d
T0 = d - 41
ch = math.sqrt(L1 * L2 / (L1 + L2)) * (1 - math.exp(-T0 / n)) * n / T0
sigma, l = 0.0499584, n - k
LO, HI = 1 / math.cosh(0.75) ** 2, 1 / math.cosh(0.25) ** 2
pref = sigma * math.sqrt(l) / n * (HI - LO) / 2 / math.sqrt(n) * a * a * gr * k * s * ch / math.sqrt(k)
s1 = sg = s / 2
sb = 1 - s
x1 = xg = xb = 0.0
out = []
for W in range(1, 81):
    j = gamma - gamma ** 2 * (s1 * x1 + sg * xg + sb * xb)
    x1, xg, xb = a * (x1 + j), gstar * a * (xg + j), gb * a * (xb + j)
    if W in (5, 10, 15, 20, 30, 80):
        out.append((W, pref * abs(x1 - xg)))
print(f"n={n} s={s} c_h/sqrt(k)={ch/math.sqrt(k):.3f} ceiling(2 sqrt(k) c_h)={pref*2/s:.5f} " +
      " ".join(f"W={W}:{v:.5f}" for W, v in out))
