"""(d) exact minimum of ||x_sel|| between two consecutive weak selected states,
and (extra) exact minimum one-step reset cost min_{h in [-1,1]^n} ||R h + b0 1||.
Bounded least squares (convex). Diagnostic numerics only."""
import json, time
import numpy as np
from scipy.optimize import lsq_linear
from model import build, B0

rows = []
for n in (200, 256, 300, 400, 600, 800, 1200, 1600):
    t0 = time.time()
    M = build(n)
    R, k, d, ell, r, a, lam, en, O = (M[x] for x in ("R", "k", "d", "ell", "r", "a", "lam", "en", "O"))
    c = 1 / (2 * np.sqrt(n))
    G = np.arctanh(c)
    Lat = 1 / (1 - 1 / (4 * n))
    Cn = np.sqrt(r / (4 * n))
    Bn = B0 * np.sqrt(r) - (Lat + a) * Cn - en * np.sqrt(n)
    # variables: g (r), hprev (n): x_sel = g - R[sel,:] hprev - b0 1_r
    sel = np.arange(1, k)
    A = np.hstack([np.eye(r), -R[sel, :]])
    lb = np.r_[-G * np.ones(r), -np.ones(n)]
    ub = np.r_[G * np.ones(r), np.ones(n)]
    lb[r + sel] = -c          # previous selected coords in weak cube
    ub[r + sel] = c
    rhs = B0 * np.ones(r)
    sol = lsq_linear(A, rhs, bounds=(lb, ub), method="bvls", tol=1e-13, lsmr_tol=None)
    exact = np.linalg.norm(A @ sol.x - rhs)
    # analytic projection bound onto 1_r
    v = O.T @ (np.ones(k) - np.eye(k)[0])  # O^T 1_sel (physical, coord0 should be 0)
    proj = B0 * np.sqrt(r) - np.sqrt(r) * G - a * c * np.abs(v[1:]).sum() / np.sqrt(r) - en * np.sqrt(n)
    # reference R0 version of the same exact minimum
    A0 = np.hstack([np.eye(r), -M["R0"][sel, :]])
    sol0 = lsq_linear(A0, rhs, bounds=(lb, ub), method="bvls", tol=1e-13)
    exact0 = np.linalg.norm(A0 @ sol0.x - rhs)
    # extra: exact one-step reset minimum to h=0 from any previous state in [-1,1]^n
    solr = lsq_linear(R, -B0 * np.ones(n), bounds=(-np.ones(n), np.ones(n)), method="bvls", tol=1e-13)
    reset_min = np.linalg.norm(R @ solr.x + B0)
    Ln = (B0 - lam) * np.sqrt(ell) - en * np.sqrt(n)
    gam = 1 / (1 - 1 / np.sqrt(k))
    mem_part = max(0.0, B0 * (np.sqrt(k) - gam / np.sqrt(k)) - a)
    sharp = np.sqrt((B0 - lam) ** 2 * ell + mem_part ** 2) - en * np.sqrt(n)
    N = int(np.ceil(4 * n * np.log(n))) + 1
    row = dict(n=n, Bn=Bn, exact_weak_min=exact, exact_weak_min_R0=exact0, proj_bound=proj,
               ratio_exact_over_Bn=exact / Bn if Bn > 0 else None,
               window_lower_Bn=np.sqrt(N - 1) * max(0, Bn), window_lower_exact=np.sqrt(N - 1) * exact,
               b0sqrt2_n_sqrtlog=B0 * np.sqrt(2) * n * np.sqrt(np.log(n)),
               Ln=Ln, reset_min=reset_min, reset_sharp_formula=sharp, b0_sqrt_n=B0 * np.sqrt(n),
               v0=float(v[0]), vL1=float(np.abs(v[1:]).sum()), two_sqrtk=2 * np.sqrt(k),
               status=(sol.status, sol0.status, solr.status), sec=time.time() - t0)
    rows.append(row)
    print({kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in row.items()}, flush=True)

json.dump(rows, open("d_weak_window.json", "w"), indent=1, default=float)
