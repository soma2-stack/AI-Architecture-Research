import json, time, sys, numpy as np
from scipy.optimize import minimize
from model import build, claimed_bound, B0
from b_hist import make_fg, verify
n = int(sys.argv[1]); Ts = [int(t) for t in sys.argv[2].split(",")]
M = build(n); R, b, k, d, U_, P = M["R"], M["b"], M["k"], M["d"], M["U"], M["P"]
for T in Ts:
    t0 = time.time()
    fg = make_fg(R, b, T, n)
    best = None
    for name, z0 in {"zero": np.zeros((T-1)*n), "rand": np.random.default_rng(T).standard_normal((T-1)*n)*0.1}.items():
        res = minimize(fg, z0, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=6000, maxfun=24000, ftol=1e-15, gtol=1e-10, maxcor=30))
        if best is None or res.fun < best[0]:
            best = (res.fun, name, res.x, res.nit)
    Uu = best[2].reshape(T-1, n); H = np.tanh(Uu)
    prev = np.vstack([np.zeros(n), H])
    X = np.empty((T, n)); X[:T-1] = Uu - prev[:T-1] @ R.T - b; X[T-1] = -prev[T-1] @ R.T - b
    mem = float(np.sum(X[:, :k]**2)); src = float(np.sum(X[:, k:]**2))
    lat = (U_ @ H[:, :k].T).T  # latent coords y = U h_m
    print(json.dumps(dict(n=n, T=T, norm=float(np.sqrt(best[0])), ratio_b0sqrtn=float(np.sqrt(best[0])/(B0*np.sqrt(n))),
        mem_energy=mem, mem_ref_b0sq_k=B0**2*k, src_energy=src, src_ref_b0sq_l=B0**2*(n-k),
        step_energy=[round(float(v),5) for v in np.sum(X**2, axis=1)][:3] + ["..."] + [round(float(v),5) for v in np.sum(X**2, axis=1)][-3:],
        max_abs_h=float(np.max(np.abs(H))), max_lat0=float(np.max(np.abs(lat[:,0]))),
        secs=time.time()-t0)), flush=True)
