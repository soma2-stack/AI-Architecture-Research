"""Scope lens: (a) exact landing (14) through tanh with the ARCHIVED dense R,
(b) radial secant contraction (17) on random/bursty histories where h*>=1/50,
(e) autonomous transport at a moderate width where h* has ~zero coordinates.
Builds R exactly as the earlier accepted review harness: (R0+ones/(1e8 n^3))*a/||.||op.
Numerical diagnostics only (cannot prove all-n statements)."""
import sys, time
import numpy as np
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build  # read-only import of frozen-R builder

b0 = 0.05
t0 = time.process_time()


def fixed_point(R, n, tol=1e-15, maxit=400000):
    h = np.zeros(n)
    for it in range(maxit):
        nh = np.tanh(R @ h + b0)
        if np.max(np.abs(nh - h)) < tol:
            return nh, it
        h = nh
    return h, maxit


for n in (4000, 2106):
    M = build(n)
    R = M["R"]
    a = M["a"]
    print(f"\n=== n={n}: ||R||op={np.linalg.norm(R,2):.15f} a={a:.15f} ||R-R0||={M['eR']:.3e} <= {4/(1e8*n*n):.3e}")
    hs, it = fixed_point(R, n)
    print(f"actual dense h*: iters={it} min={hs.min():.8f} argmin={hs.argmin()} max={hs.max():.12f} ||h*||/sqrt(n)={np.linalg.norm(hs)/np.sqrt(n):.5f}")
    # (a) exact landing through tanh, from public zero-input burn-in z_B
    for Bsteps in (50, 500, 3000):
        z = np.zeros(n)
        for _ in range(Bsteps):
            z = np.tanh(R @ z + b0)
        x = R @ (hs - z)
        lhs = np.arctanh(hs) - R @ z - b0  # required input for exact landing
        hT = np.tanh(R @ z + x + b0)
        print(f"  B={Bsteps:5d}: ||atanh(h*)-Rz_B-b - R(h*-z_B)||={np.linalg.norm(lhs-x):.2e}"
              f"  ||x||={np.linalg.norm(x):.4e}  max|x_i|={np.abs(x).max():.4e}  land err={np.abs(hT-hs).max():.2e}"
              f"  a^(B+1)||h*||={a**(Bsteps+1)*np.linalg.norm(hs):.3e}")
    G = 1 - hs**2
    if hs.min() >= 1/50:
        kap = 10000/10001
        rng = np.random.default_rng(7)
        worst = 0.0
        for trial in range(3):
            T = 1500
            X = np.zeros((T, n))
            # bursty adversarial-ish energy: a few large pulses + noise, total norm 1
            for s in rng.choice(T, 6, replace=False):
                X[s] = rng.normal(size=n)
            X += 1e-3 * rng.normal(size=(T, n))
            X /= np.linalg.norm(X)
            h = np.zeros(n)
            for t in range(T):
                v = R @ (h - hs) + X[t]
                hn = np.tanh(R @ h + X[t] + b0)
                ratio = np.linalg.norm(hn - hs) / (kap * np.linalg.norm(v))
                worst = max(worst, ratio)
                h = hn
        print(f"  radial secant (17): max ||h_t-h*||/(kappa||R(h_(t-1)-h*)+x_t||) = {worst:.6f} (must be <=1)")
        print(f"  ||G*R||op={np.linalg.norm(G[:,None]*R,2):.6f}  a(1-m^2)={a*(1-1/2500):.6f}")
    else:
        # (e) near-critical autonomous transport at this width
        A = G[:, None] * R
        v = np.random.default_rng(1).normal(size=n)
        v /= np.linalg.norm(v)
        norms = []
        for j in range(4 * n):
            v = A @ v
            norms.append(np.linalg.norm(v))
        rate = (norms[-1] / norms[2 * n - 1]) ** (1 / (2 * n))
        off = hs[n // 4 + 1: n // 2]
        print(f"  off-cycle block: count={off.size} max|h|={np.abs(off).max():.3e} gate min={1-np.abs(off).max()**2:.10f}")
        print(f"  autonomous transport empirical decay rate per step={rate:.8f}; 1-1/n={1-1/n:.8f}; "
              f"=> e-fold memory ~{1/(1-rate):.0f} steps; sum_j ||A^j v|| ~ {1+sum(norms):.1f}")
print("CPU", time.process_time() - t0)
