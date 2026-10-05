import json, time, numpy as np
from scipy.optimize import minimize
from model import build, claimed_bound, B0
from b_hist import make_fg, verify
n = 200
M = build(n); R, b = M["R"], M["b"]
rows = []
for T in (20, 50, 100):
    t0 = time.time()
    fg = make_fg(R, b, T, n)
    best = None
    for name, z0 in {"zero": np.zeros((T-1)*n), "minus_bias": np.full((T-1)*n, -B0)}.items():
        res = minimize(fg, z0, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=4000, maxfun=16000, ftol=1e-15, gtol=1e-10, maxcor=30))
        if best is None or res.fun < best[0]:
            best = (res.fun, name, res.x, res.nit)
    hT, nx, mx = verify(R, b, T, n, best[2])
    rows.append(dict(n=n, T=T, best_norm=float(np.sqrt(best[0])), init=best[1], nit=best[3], hT=hT,
                     ratio_b0sqrtn=float(np.sqrt(best[0])/(B0*np.sqrt(n))),
                     ratio_claimed=float(np.sqrt(best[0])/claimed_bound(n)), secs=time.time()-t0))
    print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open("b_long.json", "w"), indent=1)
