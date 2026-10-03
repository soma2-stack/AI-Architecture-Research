"""E1: hostile check of Lemma 2 (16) and its consequence (17) at scalar level.

Lemma 2: for p,z in (-1,1), |p|>=m: |atanh z - atanh p| >= (1+p^2/4)|z-p|.
We test the secant ratio over a dense grid including negative z, z near +-1,
z near 0, p negative, and the minimiser z=-p/2 of the quadratic average.
"""
import numpy as np
import mpmath as mp

m = 1 / 50
worst = (np.inf, None)
ps = np.concatenate([np.linspace(m, 0.999999, 4001), -np.linspace(m, 0.999999, 4001)])
zs = np.concatenate([np.linspace(-0.999999999, 0.999999999, 20001),
                     np.array([0.0, 1e-12, -1e-12])])
for p in ps:
    z = zs[np.abs(zs - p) > 1e-9]
    ratio = (np.arctanh(z) - np.arctanh(p)) / (z - p) / (1 + p * p / 4)
    i = np.argmin(ratio)
    if ratio[i] < worst[0]:
        worst = (ratio[i], (p, z[i]))
print("min over grid of secant/(1+p^2/4):", worst)

# exact minimiser of the integrated lower bound: z=-p/2 gives 1+p^2/4 exactly for
# the polynomial bound; the true secant is strictly larger. high precision check
mp.mp.dps = 50
for p in [mp.mpf(1) / 50, mp.mpf("0.05"), mp.mpf("0.5"), mp.mpf("-0.02")]:
    z = -p / 2
    sec = (mp.atanh(z) - mp.atanh(p)) / (z - p)
    print("p=", p, " z=-p/2 secant=", mp.nstr(sec, 20), " 1+p^2/4=", mp.nstr(1 + p * p / 4, 20),
          " slack=", mp.nstr(sec - 1 - p * p / 4, 6))
# kappa as given
print("kappa = 1/(1+m^2/4) =", 1 / (1 + m * m / 4), " = 10000/10001 ?", 10000 / 10001)
# the lemma constant for p = typical plateau value H=tanh(.05)
H = np.tanh(0.05)
print("plateau H=tanh(.05)=", H, " local radial const 1+H^2/4=", 1 + H * H / 4,
      " true local gate gap at h*: 1-(1-H^2)=", H * H)
