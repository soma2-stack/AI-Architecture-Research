"""Minimise TOTAL history energy sum_t ||x_t||^2 over T-step histories with
h_0=0, h_T=0 on the actual dense R (interior states h_t=tanh(u_t) free).
x_t = atanh(h_t) - R h_{t-1} - b.  Tries to beat L_n and b0 sqrt(n)."""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "2"
import numpy as np, time
from scipy.optimize import minimize
from adversary import build, Ln, Lsharp

def energy_grad(uflat, R, b, T, n):
    U = uflat.reshape(T-1, n)
    H = np.vstack([np.zeros(n), np.tanh(U), np.zeros(n)])   # h_0..h_T
    Ah = np.vstack([np.zeros(n), U, np.zeros(n)])           # atanh(h_t)=u_t
    X = Ah[1:] - H[:-1]@R.T - b                              # x_1..x_T
    E = np.sum(X*X)
    # grad wrt u_t (t=1..T-1): d x_t/d u_t = I ; d x_{t+1}/d u_t = -R diag(sech^2 u_t)
    G = 2*X[:-1] - 2*(X[1:]@R)*(1 - np.tanh(U)**2)
    return E, G.ravel()

rng = np.random.default_rng(0)
for n in (200, 400, 1000):
    M = build(n); R = M["R"]; b = 0.05*np.ones(n)
    best = (np.inf, None)
    for T in (1, 2, 3, 4, 6, 10, 20):
        if T == 1:
            E = n*0.05**2; best = min(best, (E, T), key=lambda z: z[0]); print(n, T, np.sqrt(E)); continue
        vals = []
        for trial in range(4):
            if trial == 0: u0 = np.zeros((T-1)*n)
            elif trial == 1: u0 = np.full((T-1)*n, -3.0)          # push source to -1 saturation
            else: u0 = rng.normal(0, 1.0 if trial == 2 else 0.1, (T-1)*n)
            r = minimize(energy_grad, u0, args=(R, b, T, n), jac=True, method="L-BFGS-B",
                         options=dict(maxiter=4000, gtol=1e-12, ftol=1e-15))
            vals.append(np.sqrt(r.fun))
        m = min(vals); best = min(best, (m**2, T), key=lambda z: z[0])
        print(n, T, "min ||X|| over trials:", round(m, 9))
    print(f"n={n}: best ||X||={np.sqrt(best[0]):.9f} at T={best[1]};  L_n={Ln(n):.9f}  Lsharp={Lsharp(n)[0]:.9f}  b0*sqrt(n)={0.05*np.sqrt(n):.9f}")
    assert np.sqrt(best[0]) >= Ln(n)
