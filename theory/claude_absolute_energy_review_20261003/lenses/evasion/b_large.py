"""(b') Larger widths, short horizons, including a saturated 'pulse' init that targets the
only memory direction (physical coordinate d-1) that can partially cancel the terminal bias."""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
from model import build, claimed_bound, analytic_box_R0, B0
from b_hist import make_fg, verify

rows = []
for n in (int(a) for a in sys.argv[1].split(",")):
    M = build(n)
    R, b, d = M["R"], M["b"], M["d"]
    Ln = claimed_bound(n)
    box, _, _ = analytic_box_R0(n)
    for T in (2, 3, 5):
        t0 = time.time()
        fg = make_fg(R, b, T, n)
        inits = {"zero": np.zeros((T - 1) * n)}
        U = np.zeros((T - 1, n)); h = np.zeros(n)
        for t in range(T - 1):
            U[t] = R @ h + b; h = np.tanh(U[t])
        inits["autonomous"] = U.ravel().copy()
        for kap in (1.0, 2.5):
            U = np.zeros((T - 1, n)); U[-1, d - 1] = -kap
            inits[f"pulse{kap}"] = U.ravel().copy()
        rng = np.random.default_rng(7 + n + T)
        inits["rand"] = rng.standard_normal((T - 1) * n) * 0.5
        best, allres = None, {}
        for name, z0 in inits.items():
            res = minimize(fg, z0, jac=True, method="L-BFGS-B",
                           options=dict(maxiter=5000, maxfun=20000, ftol=1e-15, gtol=1e-10, maxcor=30))
            allres[name] = float(np.sqrt(res.fun))
            if best is None or res.fun < best[0]:
                best = (res.fun, name, res.x)
        hT, nx, mx = verify(R, b, T, n, best[2])
        rows.append(dict(n=n, T=T, best_norm=float(np.sqrt(best[0])), init=best[1], hT=hT,
                         claimed=Ln, box=box, b0sqrtn=B0 * np.sqrt(n),
                         ratio_claimed=float(np.sqrt(best[0]) / Ln),
                         ratio_b0sqrtn=float(np.sqrt(best[0]) / (B0 * np.sqrt(n))),
                         all_inits=allres, secs=time.time() - t0))
        print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open("b_large.json", "w"), indent=1)
