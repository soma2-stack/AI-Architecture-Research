import numpy as np, math, time
from model import Model
for n in (200, 400, 1000):
    M = Model(n)
    Rd, R0 = M.dense_R()
    rng = np.random.default_rng(1)
    v = rng.normal(size=n)
    e1 = np.max(np.abs(M.R(v) - Rd @ v)); e2 = np.max(np.abs(M.RT(v) - Rd.T @ v))
    nr = np.linalg.norm(Rd, 2); nraw = np.linalg.norm(R0 + np.ones((n,n))*M.eps, 2)
    print(f"n={n} |Rv err|={e1:.2e} |RTv err|={e2:.2e} ||R||op-a={nr-M.a:.2e} c_dense={M.a/nraw!r} c_model={M.c!r}")
    # fixed point
    h = M.fixed_point()
    res = np.max(np.abs(h - np.tanh(Rd @ h + 0.05)))
    # zero-input iteration reference with dense R
    z = np.zeros(n)
    for t in range(200000):
        zn = np.tanh(Rd @ z + 0.05)
        if np.max(np.abs(zn - z)) < 1e-15: break
        z = zn
    print(f"   reduced fp residual={res:.2e}  |h_red - h_iter|={np.max(np.abs(h-z)):.2e} iters={t} min h*={h.min():.10f} argmin={h.argmin()} B*={M.Bstar:.3e} H={M.Hstar:.6f}")
# compare with the codex numbers (R0 only, no dense): n=200 min=-0.11760216435074086, n=2000 -0.0022257110610129443
for n in (200, 2000):
    M = Model(n, dense=False)
    h = M.fixed_point()
    print(n, "R0-only reduced min h*", repr(h.min()), "residual", np.max(np.abs(h - M.f(h))))
