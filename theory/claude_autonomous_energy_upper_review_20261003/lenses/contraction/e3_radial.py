"""E3: hostile numeric probe of the global radial bound (17)
   ||h_t-h*|| <= kappa ||R(h_{t-1}-h*)+x_t||,   kappa=10000/10001,
on wild states far from h* (uniform in (-1,1), near +-1, near 0, sign-flipped
h*, -h*/2 which is the Lemma-2 near-tight point), random huge/small inputs,
at n=1e6 (theorem regime) with the actual dense R.  Also report the best
possible per-step constant max_i secant ratio and what (17) does NOT say:
(i) no contraction of differences between two non-fixed trajectories,
(ii) no bound on G_t R beyond ||G_t||*a.  Numerics can refute, not prove."""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import numpy as np
from model import Model

n = 1000000
M = Model(n)
hs = np.load(f"hstar_{n}.npy")
kappa = 10000 / 10001
rng = np.random.default_rng(1)
cases = {
    "uniform(-1,1)": lambda: rng.uniform(-1, 1, n) * (1 - 1e-12),
    "near +1": lambda: 1 - rng.uniform(0, 1e-6, n),
    "near -1": lambda: -1 + rng.uniform(0, 1e-6, n),
    "near 0": lambda: rng.normal(0, 1e-4, n),
    "-h*": lambda: -hs,
    "-h*/2 (Lemma-2 tight)": lambda: -hs / 2,
    "h*+tiny": lambda: hs + rng.normal(0, 1e-9, n),
}
inputs = {
    "x=0": lambda: np.zeros(n),
    "x small": lambda: rng.normal(0, 1e-3, n),
    "x huge": lambda: rng.normal(0, 10, n),
    "x lands -h*/2": None,  # choose x so that h_t = -h*/2 exactly
}
worst = 0.0
for cn, cf in cases.items():
    for xn, xf in inputs.items():
        hprev = cf()
        if xf is None:
            target = -hs / 2
            x = np.arctanh(target) - M.R(hprev) - M.b0
        else:
            x = xf()
        ht = M.step(hprev, x)
        lhs = np.linalg.norm(ht - hs)
        v = M.R(hprev - hs) + x
        rhs = kappa * np.linalg.norm(v)
        # exact identity check: atanh(h_t)-atanh(h*) == v (up to fp)
        ratio = lhs / rhs if rhs > 0 else 0.0
        worst = max(worst, ratio)
        print(f"{cn:24s} {xn:14s} ||h_t-h*||={lhs:.6e} kappa||v||={rhs:.6e} ratio={ratio:.6f}")
print("worst ratio (must be <=1):", worst)
