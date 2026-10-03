"""Adversarial: can a multi-step history ending at h=0 beat the T=1 cost b0*sqrt(n)
and approach L_n? Local optimisation over preactivations y_t (h_t=tanh y_t),
t=1..T-1; final input forced to x_T=-R h_{T-1}-b0. Numerics give UPPER bounds on
the infimum only (local minima), used to locate it between L_n and b0 sqrt(n)."""
import numpy as np
from scipy.optimize import minimize
from model import build, B0

rng = np.random.default_rng(0)
for n in (200, 400, 1200):
    M = build(n); R = M["R"]; k = M["k"]; ell = M["ell"]; lam = M["lam"]; en = M["en"]
    b = B0 * np.ones(n)
    Ln = (B0 - lam) * np.sqrt(ell) - en * np.sqrt(n)

    def cost(yflat, T):
        Y = yflat.reshape(T - 1, n)
        H = np.tanh(Y)
        tot = 0.0
        gY = np.zeros_like(Y)
        hprev = np.zeros(n)
        res = []
        for t in range(T - 1):
            x = Y[t] - R @ hprev - b
            res.append(x)
            tot += x @ x
            hprev = H[t]
        xT = -R @ hprev - b
        tot += xT @ xT
        # gradient
        # d/dY_t of ||Y_t - R H_{t-1} - b||^2 = 2 x_t ; of ||Y_{t+1}-R H_t - b||^2 = -2 (R^T x_{t+1}) * (1-H_t^2)
        for t in range(T - 1):
            g = 2 * res[t]
            xnext = res[t + 1] if t + 1 < T - 1 else xT
            g += -2 * (R.T @ xnext) * (1 - H[t] ** 2)
            gY[t] = g
        return tot, gY.ravel()

    print(f"n={n}: L_n={Ln:.5f}  b0*sqrt(n)={B0*np.sqrt(n):.5f}")
    for T in (2, 3, 5, 10):
        best = np.inf
        for trial in range(4):
            y0 = (rng.normal(scale=0.3, size=(T - 1) * n) if trial else np.full((T - 1) * n, B0))
            r = minimize(cost, y0, args=(T,), jac=True, method="L-BFGS-B",
                         options=dict(maxiter=5000, maxfun=20000, gtol=1e-12, ftol=1e-15))
            best = min(best, np.sqrt(r.fun))
        print(f"   T={T}: best local min ||X|| = {best:.5f}")
