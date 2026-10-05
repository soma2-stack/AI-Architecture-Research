"""(b) Minimise total raw-input energy over T-step histories h_0=0 -> h_T=0 EXACTLY.

Interior states h_t = tanh(u_t), t=1..T-1 (free u_t in R^n); inputs by the exact lift
x_t = u_t - R h_(t-1) - b (t<T), x_T = -R h_(T-1) - b (forces h_T = tanh(0) = 0).
Energy = sum_t ||x_t||^2.  Analytic gradient; L-BFGS-B; multiple inits.
"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
from model import build, claimed_bound, analytic_box_R0, B0


def make_fg(R, b, T, n):
    RT = R.T

    def fg(z):
        U = z.reshape(T - 1, n)
        H = np.tanh(U)
        prev = np.vstack([np.zeros(n), H])          # h_0..h_(T-1)
        X = np.empty((T, n))
        X[:T - 1] = U - prev[:T - 1] @ RT - b
        X[T - 1] = -prev[T - 1] @ RT - b
        f = float(np.sum(X * X))
        G = 2 * X[:T - 1] - 2 * (1 - H * H) * (X[1:] @ R)   # R^T x_{t+1} as row: x R
        return f, G.ravel()
    return fg


def check_grad(fg, z, eps=1e-6):
    rng = np.random.default_rng(0)
    v = rng.standard_normal(z.size)
    f1, _ = fg(z + eps * v)
    f2, _ = fg(z - eps * v)
    _, g = fg(z)
    return abs((f1 - f2) / (2 * eps) - g @ v) / (abs(g @ v) + 1e-12)


def verify(R, b, T, n, z):
    """Forward-simulate the actual recurrence with the produced inputs; report ||h_T||."""
    U = z.reshape(T - 1, n) if T > 1 else np.zeros((0, n))
    H = np.tanh(U)
    prev = np.vstack([np.zeros(n), H])
    X = np.empty((T, n))
    if T > 1:
        X[:T - 1] = U - prev[:T - 1] @ R.T - b
    X[T - 1] = -prev[T - 1] @ R.T - b
    h = np.zeros(n)
    for t in range(T):
        h = np.tanh(R @ h + X[t] + b)
    return float(np.linalg.norm(h)), float(np.linalg.norm(X)), float(np.max(np.abs(X)))


def run(n, Ts, n_random=3, maxiter=20000):
    M = build(n)
    R, b = M["R"], M["b"]
    Ln = claimed_bound(n)
    box, _, _ = analytic_box_R0(n)
    rows = []
    for T in Ts:
        t0 = time.time()
        if T == 1:
            e = B0 * np.sqrt(n)
            hT, nx, mx = verify(R, b, 1, n, np.zeros(0))
            rows.append(dict(n=n, T=T, best_norm=nx, init="(no free variables)", hT=hT,
                             ratio_claimed=nx / Ln, ratio_b0sqrtn=nx / (B0 * np.sqrt(n)),
                             ratio_box=nx / box, max_abs_input=mx))
            print(json.dumps(rows[-1]), flush=True)
            continue
        fg = make_fg(R, b, T, n)
        inits = {}
        inits["zero"] = np.zeros((T - 1) * n)
        # autonomous run: x_t = 0 for t<T
        U = np.zeros((T - 1, n)); h = np.zeros(n)
        for t in range(T - 1):
            U[t] = R @ h + b; h = np.tanh(U[t])
        inits["autonomous"] = U.ravel().copy()
        # box-optimal terminal pre-state, earlier states zero
        from scipy.optimize import lsq_linear
        hs = lsq_linear(R, -b, bounds=(-0.999, 0.999), method="bvls").x
        U = np.zeros((T - 1, n)); U[-1] = np.arctanh(hs)
        inits["box_terminal"] = U.ravel().copy()
        # small negative everywhere (counter-bias)
        inits["minus_bias"] = np.full((T - 1) * n, -B0)
        rng = np.random.default_rng(12345 + T + n)
        for r in range(n_random):
            inits[f"rand{r}"] = rng.standard_normal((T - 1) * n) * [0.05, 0.5, 2.0][r % 3]
        gerr = check_grad(fg, inits["rand0"])
        best = None
        allres = {}
        for name, z0 in inits.items():
            res = minimize(fg, z0, jac=True, method="L-BFGS-B",
                           options=dict(maxiter=maxiter, maxfun=4 * maxiter, ftol=1e-16, gtol=1e-11, maxcor=30))
            allres[name] = float(np.sqrt(res.fun))
            if best is None or res.fun < best[0]:
                best = (res.fun, name, res.x, res.nit, float(np.max(np.abs(res.jac))))
        hT, nx, mx = verify(R, b, T, n, best[2])
        Ubest = best[2].reshape(T - 1, n)
        rows.append(dict(n=n, T=T, best_norm=float(np.sqrt(best[0])), init=best[1], nit=best[3],
                         grad_inf=best[4], grad_check_relerr=gerr, hT=hT, recomputed_norm=nx,
                         max_abs_input=mx, max_abs_h=float(np.max(np.abs(np.tanh(Ubest)))),
                         ratio_claimed=float(np.sqrt(best[0]) / Ln),
                         ratio_b0sqrtn=float(np.sqrt(best[0]) / (B0 * np.sqrt(n))),
                         ratio_box=float(np.sqrt(best[0]) / box),
                         all_inits=allres, secs=time.time() - t0))
        print(json.dumps(rows[-1]), flush=True)
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1])
    Ts = [int(t) for t in sys.argv[2].split(",")]
    rows = run(n, Ts)
    json.dump(rows, open(f"b_hist_n{n}.json", "w"), indent=1)
