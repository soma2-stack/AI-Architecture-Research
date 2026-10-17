"""Independent reference checker: audit of the "Port-Localized Shift-Holonomy
Recurrence" (here called QSR, quadratic shift register) proposed by Gemini.

Claude, 2026-10-13.  DIAGNOSTIC ONLY.  Every number here is finite-size
evidence; none of it proves an asymptotic statement.  The proofs are in
PROOF.md.  Exact rational arithmetic (fractions.Fraction) is used where an
identity is claimed to hold exactly.  Floating point is IEEE float64.

Run:  python -I checks.py            (writes checks_result.json next to it)
"""
import json
import math
import os
import sys
import time
from fractions import Fraction

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_default_dtype(torch.float64)
torch.set_num_threads(4)

if sys.platform == "win32":  # BelowNormal priority on the owner's machine
    try:
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
    except Exception:  # pragma: no cover
        pass

RESULTS = {}
SEED = 20261013
W_TRANSPLANT = 0.035  # w_n = 0.035/sqrt(n): the original fixed-feature weight sigma*sqrt(l)/n


def rec(key, value):
    RESULTS[key] = value
    print(f"{key}: {json.dumps(value, default=float)}", flush=True)


# ----------------------------------------------------------------------------
# Core QSR model.  State h in R^n, n = R*m, block r (1-indexed) is h[(r-1)m:rm].
# (S h)^(1) = h^(R), (S h)^(r) = h^(r-1).  psi(u) = u^2/2 on block 1 only.
#   h_t = S(h_{t-1} + E1 psi(h_{t-1}^(1))) + E1 x_t        (+ b when trained)
# The model is diagonal in the within-block index i: m independent copies.
# ----------------------------------------------------------------------------

def psi(u):
    return 0.5 * u * u


def S_apply(h, R, m):
    return np.roll(h.reshape(R, m), 1, axis=0).reshape(-1)


def ST_apply(h, R, m, k=1):
    return np.roll(h.reshape(R, m), -k, axis=0).reshape(-1)


def S_matrix(R, m):
    P = np.zeros((R, R))
    for r in range(R):
        P[(r + 1) % R, r] = 1.0
    return np.kron(P, np.eye(m))


def step(h, x, R, m):
    p = h.copy()
    p[:m] = p[:m] + psi(p[:m])
    hn = S_apply(p, R, m)
    hn[:m] = hn[:m] + x
    return hn


def run(xs, R, m, h0=None):
    n = R * m
    h = np.zeros(n) if h0 is None else np.array(h0, dtype=float)
    hs = [h]
    for x in xs:
        h = step(h, x, R, m)
        hs.append(h)
    return hs  # hs[t] = h_t


def backprop(hs, lam_end, R, m):
    """lams[t] = dL/dh_t:  lambda_{t-1} = D_t S^T lambda_t,
    D_t = I + E1 diag(h_{t-1}^(1)) E1^T."""
    T = len(hs) - 1
    lams = [None] * (T + 1)
    lams[T] = np.array(lam_end, dtype=float)
    for t in range(T, 0, -1):
        v = ST_apply(lams[t], R, m)
        v[:m] = v[:m] * (1.0 + hs[t - 1][:m])
        lams[t - 1] = v
    return lams


def run_port(xs, R, m):
    """Memory-light forward pass: port (block-1) states h_t^(1), t=0..T, and h_T."""
    h = np.zeros(R * m)
    ports = [h[:m].copy()]
    for x in xs:
        h = step(h, x, R, m)
        ports.append(h[:m].copy())
    return ports, h


def backprop_sum(ports, mu, R, m):
    """Returns (sum_{t=1}^T lambda_t, lambda_0) given lambda_T = mu."""
    T = len(ports) - 1
    lam = np.array(mu, dtype=float)
    total = np.zeros_like(lam)
    for t in range(T, 0, -1):
        total += lam
        v = ST_apply(lam, R, m)
        v[:m] = v[:m] * (1.0 + ports[t - 1])
        lam = v
    return total, lam


def past_bias_grad(xs_hist, mu, R, m):
    """Past part sum_{t<=T} lambda_t of the bias gradient, given lambda_T = mu."""
    ports, hT = run_port(xs_hist, R, m)
    total, _ = backprop_sum(ports, mu, R, m)
    return total, hT


def gemini_inputs(z):
    """z has shape (R, m): z[r-1] = z^(r).  Write R blocks, then cancel."""
    R = z.shape[0]
    return [z[r].copy() for r in range(R)] + [-(z[r] + psi(z[r])) for r in range(R)]


def repair_inputs(z, q):
    """Accumulate q*R zero-input steps, then Gemini's write/cancel."""
    R, m = z.shape
    return [np.zeros(m) for _ in range(q * R)] + gemini_inputs(z)


def future_head_inputs(v):
    """Fixed-head legal query: R port inputs v^(1..R) then one zero step."""
    R, m = v.shape
    return [v[r].copy() for r in range(R)] + [np.zeros(m)]


def gamma_closed_form(z):
    """Phi_{2R}(z) = diag(1+z^(R), 1+z^(R-1), ..., 1+z^(1)) (block order 1..R)."""
    return 1.0 + z[::-1].reshape(-1)


def mu_closed(v):
    """Claimed fixed-head adjoint at h_T: mu^(R+1-r) = (1 + v^(r))/sqrt(n)."""
    R, m = v.shape
    n = R * m
    mu = np.zeros((R, m))
    for r in range(1, R + 1):
        mu[R - r] = (1.0 + v[r - 1]) / math.sqrt(n)
    return mu.reshape(-1)


def mu_from_future(v, R, m):
    n = R * m
    hs = run(future_head_inputs(v), R, m)
    return backprop(hs, np.ones(n) / math.sqrt(n), R, m)[0]


def closed_form_delta(dz, mu, R, m, q):
    """Past bias-gradient difference of the repair schedule (PROOF.md, Lemma 5):
    q 1_R (x) a + sum_{s=1}^R S^{-(2R-s)} delta_s,  a = sum_r dz^(r) * mu^(R+1-r)."""
    MU = mu.reshape(R, m)
    a = np.zeros(m)
    for r in range(1, R + 1):
        a += dz[r - 1] * MU[R - r]
    main = np.tile(a, R) * q
    win = np.zeros(R * m)
    for s in range(1, R + 1):
        delta = np.zeros((R, m))
        for r in range(s, R + 1):
            delta[R - r] = dz[r - 1] * MU[R - r]
        win += ST_apply(delta.reshape(-1), R, m, k=(2 * R - s) % R)
    return main + win, main, win, a


def sign_choice_v(dz, rho_f=0.5):
    """Per-coordinate sign-aligned nonexpansive query, v in {-rho_f, 0}."""
    R, m = dz.shape
    v = np.zeros((R, m))
    for i in range(m):
        col = dz[:, i]
        eps = 1.0 if col.sum() >= 0 else -1.0
        for r in range(R):
            v[r, i] = 0.0 if (np.sign(col[r]) == eps or col[r] == 0) else -rho_f
    return v


def random_sign_matrix(N, D, rng):
    return rng.choice([-1.0, 1.0], size=(N, D))


def code_theta(G, y):
    """theta(y) = (clip(4 G y), y): odd, continuous, injective, values in [-1,1]."""
    return np.concatenate([np.clip(4.0 * (G @ y), -1.0, 1.0), y])


def unit(rng, D):
    y = rng.normal(size=D)
    return y / np.linalg.norm(y)


# ----------------------------------------------------------------------------
# Section A: forward cancellation (float64 and exact rationals)
# ----------------------------------------------------------------------------

def frac_step(h, x, R, m):
    p = list(h)
    for i in range(m):
        p[i] = p[i] + p[i] * p[i] / 2
    hn = (p[(R - 1) * m:] + p[: (R - 1) * m]) if R > 1 else p
    hn = list(hn)
    for i in range(m):
        hn[i] = hn[i] + x[i]
    return hn


def section_A():
    rng = np.random.default_rng(SEED)
    out = {"float64": [], "exact": []}
    for R in [1, 2, 3, 4, 8]:
        for m in [1, 2, 5]:
            worst, worst_cont = 0.0, 0.0
            for _ in range(20):
                z = rng.uniform(-0.5, 0.5, size=(R, m))
                xs = gemini_inputs(z) + [np.zeros(m)] * (3 * R)
                hs = run(xs, R, m)
                worst = max(worst, float(np.abs(hs[2 * R]).max()))
                worst_cont = max(worst_cont, max(float(np.abs(h).max()) for h in hs[2 * R:]))
            out["float64"].append({"R": R, "m": m, "max|h_2R|": worst,
                                   "max|h_t| for 2R<=t<=5R": worst_cont})
    frng = np.random.default_rng(SEED + 1)
    for R in [1, 2, 3, 4, 8]:
        m = 2 if R <= 4 else 1
        ok = True
        for _ in range(5):
            z = [[Fraction(int(frng.integers(-32, 33)), 64) for _ in range(m)] for _ in range(R)]
            h = [Fraction(0)] * (R * m)
            xs = [z[r] for r in range(R)] + [[-(zz + zz * zz / 2) for zz in z[r]] for r in range(R)]
            traj = [h]
            for x in xs + [[Fraction(0)] * m] * (2 * R):
                h = frac_step(h, x, R, m)
                traj.append(h)
            ok = ok and all(all(v == 0 for v in hh) for hh in traj[2 * R:])
            expect = list(z[R - 1])  # h_R = (z^(R), w(z^(R-1)), ..., w(z^(1)))
            for r in range(R - 1, 0, -1):
                expect += [zz + zz * zz / 2 for zz in z[r - 1]]
            ok = ok and (traj[R] == expect)
        out["exact"].append({"R": R, "m": m, "exact zero endpoint, continuation, h_R structure": ok})
    rec("A_forward_cancellation", out)


# ----------------------------------------------------------------------------
# Section B: Jacobian Phi_T = dh_T/dh_0
# ----------------------------------------------------------------------------

def torch_forward_h0(h0, xs, R, m):
    h = h0
    for x in xs:
        h1 = h[:m]
        p = torch.cat([h1 + 0.5 * h1 * h1, h[m:]]).reshape(R, m)
        p = torch.roll(p, 1, dims=0).reshape(-1)
        h = p + torch.cat([torch.as_tensor(x), torch.zeros(R * m - m)])
    return h


def jacobian_product(hs, R, m):
    n = R * m
    Phi = np.eye(n)
    S = S_matrix(R, m)
    for t in range(1, len(hs)):
        D = np.eye(n)
        D[:m, :m] += np.diag(hs[t - 1][:m])
        Phi = S @ D @ Phi
    return Phi


def section_B():
    rng = np.random.default_rng(SEED + 2)
    rows = []
    for R in [1, 2, 3, 4, 8]:
        for m in [1, 3]:
            n = R * m
            for extra in [0, 1, R, R + 2]:
                z = rng.uniform(-0.5, 0.5, size=(R, m))
                xs = gemini_inputs(z) + [np.zeros(m)] * extra
                T = len(xs)
                hs = run(xs, R, m)
                Phi = jacobian_product(hs, R, m)
                closed = np.linalg.matrix_power(S_matrix(R, m), T - 2 * R) @ np.diag(gamma_closed_form(z))
                J = torch.autograd.functional.jacobian(
                    lambda h0: torch_forward_h0(h0, xs, R, m), torch.zeros(n)).numpy()
                eps = 1e-6
                FD = np.zeros((n, n))
                for k in range(n):
                    e = np.zeros(n)
                    e[k] = eps
                    FD[:, k] = (run(xs, R, m, e)[-1] - run(xs, R, m, -e)[-1]) / (2 * eps)
                sv = np.linalg.svd(Phi, compute_uv=False)
                rows.append({"R": R, "m": m, "T": T,
                             "|prod-closed|": float(np.abs(Phi - closed).max()),
                             "|autograd-closed|": float(np.abs(J - closed).max()),
                             "|FD-closed|": float(np.abs(FD - closed).max()),
                             "sv_min": float(sv.min()), "sv_max": float(sv.max())})
    rec("B_jacobian_worst_errors", {k: max(r[k] for r in rows)
                                    for k in ["|prod-closed|", "|autograd-closed|", "|FD-closed|"]})
    rec("B_singular_value_range_random_z", [min(r["sv_min"] for r in rows), max(r["sv_max"] for r in rows)])
    # extremes are attained at z = -1/2 and z = +1/2
    R, m = 3, 2
    z = np.full((R, m), 0.5)
    z[0, 0] = -0.5
    sv = np.linalg.svd(jacobian_product(run(gemini_inputs(z), R, m), R, m), compute_uv=False)
    rec("B_singular_values_at_cube_vertex", [float(sv.min()), float(sv.max())])
    # exact rational check of the closed form for T = 2R and T = 2R + 3
    ok = True
    frng = np.random.default_rng(SEED + 3)
    for R in [1, 2, 3, 5]:
        m = 2
        n = R * m
        z = [[Fraction(int(frng.integers(-32, 33)), 64) for _ in range(m)] for _ in range(R)]
        xs = [z[r] for r in range(R)] + [[-(zz + zz * zz / 2) for zz in z[r]] for r in range(R)]
        for extra in [0, 3]:
            xx = xs + [[Fraction(0)] * m] * extra
            traj = [[Fraction(0)] * n]
            for x in xx:
                traj.append(frac_step(traj[-1], x, R, m))
            cols = [[Fraction(int(i == k)) for i in range(n)] for k in range(n)]
            for t in range(1, len(xx) + 1):
                new_cols = []
                for col in cols:
                    v = list(col)
                    for i in range(m):
                        v[i] = v[i] * (1 + traj[t - 1][i])
                    v = (v[(R - 1) * m:] + v[: (R - 1) * m]) if R > 1 else v
                    new_cols.append(v)
                cols = new_cols
            T = len(xx)
            diag = []
            for j in range(R):  # block j+1 carries z^(R-j)
                diag += [1 + zz for zz in z[R - 1 - j]]
            shift = (T - 2 * R) % R
            for k in range(n):
                target = [Fraction(0)] * n
                blk, i = divmod(k, m)
                target[((blk + shift) % R) * m + i] = diag[k]
                ok = ok and (cols[k] == target)
    rec("B_closed_form_exact_rational", ok)
    # monomial structure for a general multi-round history (not write/cancel)
    R, m = 4, 3
    xs = [rng.uniform(-0.15, 0.1, size=m) for _ in range(int(3.5 * R))]
    Phi = jacobian_product(run(xs, R, m), R, m)
    nz_r = (np.abs(Phi) > 1e-14).sum(axis=1)
    nz_c = (np.abs(Phi) > 1e-14).sum(axis=0)
    rec("B_general_history_Jacobian_is_monomial", bool((nz_r == 1).all() and (nz_c == 1).all()))


# ----------------------------------------------------------------------------
# Section C: input admissibility
# ----------------------------------------------------------------------------

def section_C():
    zz = np.linspace(-0.5, 0.5, 200001)
    rec("C_max_cancel_input_z_in_[-1/2,1/2]", float(np.abs(zz + psi(zz)).max()))
    rho = math.sqrt(2) - 1
    zr = np.linspace(-rho, rho, 200001)
    rec("C_max_cancel_input_z_in_[-(sqrt2-1),sqrt2-1]", float(np.abs(zr + psi(zr)).max()))
    zn = np.linspace(-0.5, 0.0, 200001)
    rec("C_max_cancel_input_z_in_[-1/2,0]", float(np.abs(zn + psi(zn)).max()))


# ----------------------------------------------------------------------------
# Section D: parameter gradients, adjoint formulas vs torch autograd
# ----------------------------------------------------------------------------

def torch_param_run(xs, R, m, W, c, U, b, th0, loss):
    n = R * m
    h = th0
    for x in xs:
        h1 = h[:m]
        p = torch.cat([h1 + c * 0.5 * h1 * h1, h[m:]])
        h = W @ p + torch.cat([U @ torch.as_tensor(x), torch.zeros(n - m)]) + b
    if loss == "head":
        return h.sum() / math.sqrt(n)
    return 0.5 * (h * h).sum()


def numpy_param_grads(xs, R, m, loss):
    n = R * m
    hs = run(xs, R, m)
    lam_end = np.ones(n) / math.sqrt(n) if loss == "head" else hs[-1].copy()
    lams = backprop(hs, lam_end, R, m)
    gW, gc, gU, gb = np.zeros((n, n)), np.zeros(m), np.zeros((m, m)), np.zeros(n)
    for t in range(1, len(xs) + 1):
        p = hs[t - 1].copy()
        p[:m] += psi(p[:m])
        gW += np.outer(lams[t], p)
        gc += ST_apply(lams[t], R, m)[:m] * psi(hs[t - 1][:m])
        gU += np.outer(lams[t][:m], xs[t - 1])
        gb += lams[t]
    return {"W": gW, "c": gc, "U": gU, "b": gb, "theta0": lams[0]}


def section_D():
    rng = np.random.default_rng(SEED + 4)
    worst = 0.0
    for R, m in [(1, 4), (2, 3), (3, 2), (4, 2)]:
        n = R * m
        for loss in ["head", "half_sq"]:
            z = rng.uniform(-0.5, 0.0, size=(R, m))
            v = rng.uniform(-0.5, 0.0, size=(R, m))
            xs = repair_inputs(z, 2) + future_head_inputs(v)
            W = torch.tensor(S_matrix(R, m), requires_grad=True)
            c = torch.ones(m, requires_grad=True)
            U = torch.eye(m, requires_grad=True)
            b = torch.zeros(n, requires_grad=True)
            th0 = torch.zeros(n, requires_grad=True)
            torch_param_run(xs, R, m, W, c, U, b, th0, loss).backward()
            g = numpy_param_grads(xs, R, m, loss)
            for name, tens in [("W", W), ("c", c), ("U", U), ("b", b), ("theta0", th0)]:
                worst = max(worst, float(np.abs(tens.grad.numpy() - g[name]).max()))
    rec("D_param_grads_adjoint_vs_autograd_max_abs_err", worst)
    # theta0-gradient equals Phi^T lambda_T (the "holonomy"), Gemini schedule
    R, m = 3, 2
    n = R * m
    z = rng.uniform(-0.5, 0.5, size=(R, m))
    v = rng.uniform(-0.5, 0.0, size=(R, m))
    hs = run(gemini_inputs(z) + future_head_inputs(v), R, m)
    lams = backprop(hs, np.ones(n) / math.sqrt(n), R, m)
    err = float(np.abs(lams[0] - gamma_closed_form(z) * lams[2 * R]).max())
    rec("D_theta0_grad_equals_Gamma(z)*lambda_T_err", err)


# ----------------------------------------------------------------------------
# Section E: Gemini's schedule under several metrics
# ----------------------------------------------------------------------------

def section_E():
    rng = np.random.default_rng(SEED + 5)
    out = {}
    errs = []
    for R, m in [(1, 3), (2, 2), (3, 3), (5, 2)]:
        v = rng.uniform(-0.5, 0.0, size=(R, m))
        errs.append(float(np.abs(mu_from_future(v, R, m) - mu_closed(v)).max()))
    out["fixed_head_mu_closed_form_err"] = max(errs)
    # Gemini's terminal adjoints g_T(v) (loss 1/2||h_{T+R}||^2) span R^n
    R, m = 3, 2
    n = R * m
    G = []
    for _ in range(3 * n):
        v = rng.uniform(-0.5, 0.5, size=(R, m))
        hs = run([v[r] for r in range(R)], R, m)
        G.append(backprop(hs, hs[-1], R, m)[0])
    out["gemini_g_T_samples_rank"] = int(np.linalg.matrix_rank(np.array(G)))
    # Gemini literal metric: theta0-gradient, loss 1/2||h_{T+R}||^2, v in [-1/2,1/2]^m
    lit = []
    vgrid = np.linspace(-0.5, 0.5, 20001)
    g1 = float(np.abs(vgrid).max())
    gj = float(np.abs((1 + vgrid) * (vgrid + psi(vgrid))).max())
    for R, m in [(1, 4), (2, 3), (4, 2), (8, 2)]:
        n = R * m
        worst_boundary = math.inf
        for trial in range(30):
            z = rng.uniform(-0.5, 0.5, size=(R, m)) if trial % 2 else np.zeros((R, m))
            z.reshape(-1)[rng.integers(n)] = 0.5 * rng.choice([-1, 1])
            gam = gamma_closed_form(z) - gamma_closed_form(-z)  # = 2 z~
            best = np.full(n, gj)
            best[:m] = g1
            sep = float(np.linalg.norm(gam * best))
            for _ in range(5):  # actual forward/backward at random v never exceeds it
                v = rng.uniform(-0.5, 0.5, size=(R, m))
                h1 = run(gemini_inputs(z) + [v[r] for r in range(R)], R, m)
                h2 = run(gemini_inputs(-z) + [v[r] for r in range(R)], R, m)
                d = np.linalg.norm(backprop(h1, h1[-1], R, m)[0] - backprop(h2, h2[-1], R, m)[0])
                assert d <= sep + 1e-12
            worst_boundary = min(worst_boundary, sep)
        lit.append({"R": R, "m": m, "min sup-separation over cube-boundary samples": worst_boundary})
    out["gemini_literal_metric (theta0, 1/2||h||^2)"] = lit
    out["max |lambda_T entry|: block1, blocks>=2"] = [g1, gj]
    # theta0 parameter, fixed head 1/sqrt(n): single saturated coordinate is diluted
    dil = []
    for n_target in [16, 64, 256, 1024, 4096]:
        R, m = 2, n_target // 2
        n = R * m
        z = np.zeros((R, m))
        z[0, 0] = 0.5
        gam = gamma_closed_form(z) - gamma_closed_form(-z)
        dil.append({"n": n, "unit adjoint": float(np.abs(gam).max()),
                    "fixed head (best nonexpansive)": float(np.linalg.norm(gam) / math.sqrt(n))})
    out["theta0_single_saturated_coordinate"] = dil
    # Gemini schedule, bias parameter, transplanted weight; sep <= 2wT
    rows = []
    for label, Rfun in [("R=2", lambda n: 2), ("R=3", lambda n: 3), ("R=sqrt(n)", lambda n: int(round(math.sqrt(n))))]:
        for n_target in [64, 256, 1024, 4096]:
            R = Rfun(n_target)
            m = n_target // R
            n = R * m
            w = W_TRANSPLANT / math.sqrt(n)
            D_emp = max(1, n // 16)
            G = random_sign_matrix(n - D_emp, D_emp, rng)
            worst = math.inf
            for _ in range(6):
                th = code_theta(G, unit(rng, D_emp))
                zp = (-0.25 * (1 + th)).reshape(R, m)
                zm = (-0.25 * (1 - th)).reshape(R, m)
                mu = mu_closed(sign_choice_v(zp - zm))
                d1, _ = past_bias_grad(gemini_inputs(zp), mu, R, m)
                d2, _ = past_bias_grad(gemini_inputs(zm), mu, R, m)
                worst = min(worst, w * float(np.linalg.norm(d1 - d2)))
            rows.append({"schedule": label, "R": R, "n": n, "T": 2 * R,
                         "min over samples of w*||delta grad_b|| (sign query)": worst,
                         "upper bound 2wT": 2 * w * 2 * R})
    out["gemini_schedule_bias_transplanted_w"] = rows
    rec("E_metrics", out)


# ----------------------------------------------------------------------------
# Section F: accumulate-then-gate repair
# ----------------------------------------------------------------------------

def section_F():
    rng = np.random.default_rng(SEED + 6)
    out = {"closed_form_check": [], "scaling": []}
    rho, rho_f = 0.5, 0.5
    for R, m, q in [(1, 5, 3), (2, 4, 2), (3, 3, 4), (5, 2, 3), (8, 2, 2)]:
        z1 = -(rho / 2) * (1 + rng.uniform(-1, 1, size=(R, m)))
        z2 = -(rho / 2) * (1 + rng.uniform(-1, 1, size=(R, m)))
        mu = mu_closed(rng.uniform(-rho_f, 0.0, size=(R, m)))
        g1, hT1 = past_bias_grad(repair_inputs(z1, q), mu, R, m)
        g2, hT2 = past_bias_grad(repair_inputs(z2, q), mu, R, m)
        cf = closed_form_delta(z1 - z2, mu, R, m, q)[0]
        out["closed_form_check"].append({"R": R, "m": m, "q": q,
                                         "|actual-closed|": float(np.abs((g1 - g2) - cf).max()),
                                         "endpoints exactly zero": bool(np.abs(hT1).max() == 0 and np.abs(hT2).max() == 0)})
    # future part of the full bias gradient is identical for the pair
    R, m, q = 3, 2, 2
    n = R * m
    th = rng.uniform(-1, 1, size=(R, m))
    v = rng.uniform(-rho_f, 0.0, size=(R, m))
    fut = []
    for sgn in [1, -1]:
        z = -(rho / 2) * (1 + sgn * th)
        hist = repair_inputs(z, q)
        hs = run(hist + future_head_inputs(v), R, m)
        lams = backprop(hs, np.ones(n) / math.sqrt(n), R, m)
        fut.append(np.sum(lams[len(hist) + 1:], axis=0))
    out["future_part_difference"] = float(np.abs(fut[0] - fut[1]).max())
    # scaling with n = R^2, q = 193, transplanted weight w = 0.035/sqrt(n)
    q = 193
    for R in [8, 16, 32, 64]:
        m = R
        n = R * m
        w = W_TRANSPLANT / math.sqrt(n)
        D_emp = max(1, n // 16)
        G = random_sign_matrix(n - D_emp, D_emp, rng)
        worst_sep, worst_ratio, min_l1 = math.inf, math.inf, math.inf
        for trial in range(6):
            th = code_theta(G, unit(rng, D_emp)).reshape(R, m)
            zp, zm = -(rho / 2) * (1 + th), -(rho / 2) * (1 - th)
            dz = zp - zm
            mu = mu_closed(sign_choice_v(dz))
            cf = closed_form_delta(dz, mu, R, m, q)[0]
            actual = float(np.linalg.norm(cf))
            if trial < 2:  # the actual recurrence for two samples
                g1, h1 = past_bias_grad(repair_inputs(zp, q), mu, R, m)
                g2, h2 = past_bias_grad(repair_inputs(zm, q), mu, R, m)
                assert abs(float(np.linalg.norm(g1 - g2)) - actual) < 1e-9 * max(1.0, actual)
                assert np.abs(h1).max() == 0 and np.abs(h2).max() == 0
            l1, l2 = float(np.abs(dz).sum()), float(np.linalg.norm(dz))
            lower = (q * R * rho_f / (2 * n)) * l1 - R * l2 / math.sqrt(n)
            assert actual >= lower - 1e-9
            worst_sep = min(worst_sep, w * actual)
            worst_ratio = min(worst_ratio, actual / lower)
            min_l1 = min(min_l1, l1 / (rho * n))
        out["scaling"].append({"R": R, "m": m, "n": n, "T": (q + 2) * R, "mT/n": q + 2,
                               "active coordinate-time/n": 2,
                               "D (empirical code)": D_emp,
                               "min normalized sep, w=0.035/sqrt(n)": worst_sep,
                               "theorem lower bound wR (needs ||dz||_1>=rho n/16.02)": w * R,
                               "min actual/(proved inequality)": worst_ratio,
                               "min ||dz||_1/(rho n)": min_l1})
    rec("F_repair", out)


def section_F4():
    """Is the sign query close to the best nonexpansive fixed-head query?"""
    rng = np.random.default_rng(SEED + 7)
    rows = []
    rho, rho_f, q = 0.5, 0.5, 3
    for R, m in [(2, 4), (3, 4), (4, 4), (4, 8)]:
        n = R * m
        D_emp = max(1, n // 8)
        G = random_sign_matrix(n - D_emp, D_emp, rng)
        th = code_theta(G, unit(rng, D_emp)).reshape(R, m)
        dz = -rho * th
        M = np.zeros((n, n))
        for k in range(n):
            e = np.zeros(n)
            e[k] = 1.0
            M[:, k] = closed_form_delta(dz, e, R, m, q)[0]
        lo, hi = (1 - rho_f) / math.sqrt(n), 1.0 / math.sqrt(n)
        sign_val = float(np.linalg.norm(M @ mu_closed(sign_choice_v(dz, rho_f))))
        best = 0.0
        if n <= 16:
            for bits in range(1 << n):
                mu = np.array([hi if (bits >> k) & 1 else lo for k in range(n)])
                best = max(best, float(np.linalg.norm(M @ mu)))
            method = "exhaustive over box vertices (objective convex)"
        else:
            for _ in range(40):
                mu = np.where(rng.random(n) < 0.5, lo, hi)
                improved = True
                while improved:
                    improved = False
                    for k in range(n):
                        cur = np.linalg.norm(M @ mu)
                        old = mu[k]
                        mu[k] = lo if old == hi else hi
                        if np.linalg.norm(M @ mu) > cur + 1e-15:
                            improved = True
                        else:
                            mu[k] = old
                best = max(best, float(np.linalg.norm(M @ mu)))
            method = "vertex coordinate ascent, 40 random starts"
        rows.append({"R": R, "m": m, "n": n, "sign query": sign_val, "best found": best,
                     "sign/best": sign_val / best, "method": method})
    rec("F4_query_optimality", rows)


# ----------------------------------------------------------------------------
# Section G: short-window upper bound ||delta grad_b|| <= 2T (nonexpansive class)
# ----------------------------------------------------------------------------

def section_G():
    rng = np.random.default_rng(SEED + 8)
    worst = 0.0
    for _ in range(200):
        R = int(rng.integers(1, 6))
        m = int(rng.integers(1, 5))
        xs1, xs2 = [], []
        for _ in range(int(rng.integers(1, 4))):
            gap = int(rng.integers(0, 2 * R))
            xs1 += [np.zeros(m)] * gap
            xs2 += [np.zeros(m)] * gap
            xs1 += gemini_inputs(rng.uniform(-0.5, 0.0, size=(R, m)))
            xs2 += gemini_inputs(rng.uniform(-0.5, 0.0, size=(R, m)))
        T = len(xs1)
        mu = mu_closed(rng.uniform(-0.5, 0.0, size=(R, m)))
        g1, h1 = past_bias_grad(xs1, mu, R, m)
        g2, h2 = past_bias_grad(xs2, mu, R, m)
        assert np.abs(h1).max() == 0 and np.abs(h2).max() == 0
        worst = max(worst, float(np.linalg.norm(g1 - g2)) / (2 * T))
    rec("G_max ||delta grad_b||/(2T) over 200 random nonexpansive pairs (<=1 required)", worst)


# ----------------------------------------------------------------------------
# Section H: clipped random-sign code diagnostics (whole-sphere thickness)
# ----------------------------------------------------------------------------

def section_H():
    rng = np.random.default_rng(SEED + 9)
    torch.manual_seed(SEED + 9)
    rows = []
    for N, D in [(2000, 2), (2000, 20), (2000, 100), (2000, 250)]:
        G = random_sign_matrix(N, D, rng)
        opn = float(np.linalg.norm(G, 2) / math.sqrt(N))
        Gt = torch.tensor(G)
        best = math.inf
        for _ in range(20):
            y = torch.randn(D)
            y = (y / y.norm()).requires_grad_(True)
            opt = torch.optim.Adam([y], lr=0.02)
            for _ in range(300):
                s = Gt @ (y / y.norm())
                obj = torch.clamp(16.0 * s * s, max=1.0).sum()
                opt.zero_grad()
                obj.backward()
                opt.step()
            yy = (y / y.norm()).detach().numpy()
            best = min(best, float((np.abs(G @ yy) >= 0.25).mean()))
        rows.append({"N": N, "D": D, "||G||op/sqrt(N)": opn,
                     "min found fraction |(Gy)_i|>=1/4": best,
                     "Lemma 7 guarantee (only for D<=N/1000)": 1 / 16})
    rec("H_code_diagnostics", rows)


# ----------------------------------------------------------------------------
# Section I: ablations
# ----------------------------------------------------------------------------

def tanh_shift_run(xs, R, m, bias):
    h = np.zeros(R * m)
    hs = [h]
    for x in xs:
        pre = S_apply(h, R, m) + bias
        pre[:m] += x
        h = np.tanh(pre)
        hs.append(h)
    return hs


def tanh_shift_bias_grad(hs, lam_T, R, m):
    """Past bias gradient sum_t G_t lambda_t of h_t = tanh(S h_{t-1} + E1 x_t + b)."""
    lam = np.array(lam_T, dtype=float)
    gb = np.zeros_like(lam)
    for t in range(len(hs) - 1, 0, -1):
        gl = (1.0 - hs[t] ** 2) * lam
        gb += gl
        lam = ST_apply(gl, R, m)
    return gb


def section_I():
    rng = np.random.default_rng(SEED + 10)
    out = {}
    # (I1) zero-bias tanh RNN with recurrent matrix = cyclic block shift
    rows = []
    q = 193
    for R in [8, 16, 32]:
        m = R
        n = R * m
        w = W_TRANSPLANT / math.sqrt(n)
        D_emp = max(1, n // 16)
        G = random_sign_matrix(n - D_emp, D_emp, rng)
        th = code_theta(G, unit(rng, D_emp)).reshape(R, m)
        hist = []
        max_in = 0.0
        for sgn in [1, -1]:
            zz = np.sqrt((1 + sgn * th) / (2 * R))  # small writes: R-step gate products O(1)
            xs = [np.zeros(m) for _ in range(q * R)] + [np.arctanh(zz[r]) for r in range(R)]
            hs = tanh_shift_run(xs, R, m, np.zeros(n))
            h = hs[-1]
            for r in range(R):  # cancel each value as it re-enters the port: exact zero
                pre = S_apply(h, R, m)
                x = -pre[:m].copy()
                pre[:m] += x
                h = np.tanh(pre)
                xs.append(x)
                hs.append(h)
            max_in = max(max_in, float(np.abs(np.concatenate(xs)).max()))
            hist.append(hs)
        endpoint = max(float(np.abs(hist[0][-1]).max()), float(np.abs(hist[1][-1]).max()))
        # the map mu -> delta grad_b is diagonal in the within-block index i:
        # recover the R x R map of each i with R adjoint sweeps, then sign-align
        cols = []
        for j in range(R):
            mu = np.zeros((R, m))
            mu[j] = 1.0
            mu = mu.reshape(-1)
            cols.append((tanh_shift_bias_grad(hist[0], mu, R, m) -
                         tanh_shift_bias_grad(hist[1], mu, R, m)).reshape(R, m))
        lo, hi = 0.5 / math.sqrt(n), 1.0 / math.sqrt(n)
        MU = np.zeros((R, m))
        for i in range(m):
            Mi = np.stack([cols[j][:, i] for j in range(R)], axis=1)  # out-block x mu-block
            c = Mi.mean(axis=0)
            eps = 1.0 if c.sum() >= 0 else -1.0
            MU[:, i] = np.where(np.sign(c) == eps, hi, lo)
        mu = MU.reshape(-1)
        sep_sign = w * float(np.linalg.norm(tanh_shift_bias_grad(hist[0], mu, R, m) -
                                            tanh_shift_bias_grad(hist[1], mu, R, m)))
        sep_unif = w * float(np.linalg.norm(tanh_shift_bias_grad(hist[0], np.full(n, hi), R, m) -
                                            tanh_shift_bias_grad(hist[1], np.full(n, hi), R, m)))
        rows.append({"R": R, "n": n, "T": (q + 2) * R, "endpoint max|h_T|": endpoint,
                     "max |input|": max_in,
                     "normalized sep, sign-aligned adjoint (idealized family)": sep_sign,
                     "normalized sep, uniform head adjoint": sep_unif})
    out["zero_bias_tanh_cyclic_shift_RNN"] = rows
    # (I2) the bias tax: same RNN with bias .05 and zero input
    R, m = 16, 16
    n = R * m
    hs = tanh_shift_run([np.zeros(m) for _ in range(400)], R, m, 0.05 * np.ones(n))
    hstar = float(hs[-1].mean())
    gb = tanh_shift_bias_grad(hs, np.ones(n) / math.sqrt(n), R, m)
    out["bias_tax_tanh_shift_b=.05"] = {
        "autonomous state h*": hstar, "autonomous gate 1-h*^2": 1 - hstar ** 2,
        "||bias credit|| after 400 zero-input steps": float(np.linalg.norm(gb)),
        "geometric ceiling 1/(1-gate)": 1.0 / hstar ** 2,
        "note": "non-port blocks receive no input, so they cannot be held neutral at any cost"}
    # (I3) R = 1 (no shift, m = n): necessary and sufficient horizons
    rows = []
    for n in [64, 256, 1024, 4096, 16384, 65536]:
        w = W_TRANSPLANT / math.sqrt(n)
        T_nec = 0.001 / w  # Theorem 3: robust pair needs T > eps/w
        T0_suff = math.ceil(8 * (0.002 / w + 0.5))  # best-case kappa = 1 in Theorem 4
        rows.append({"n": n, "m": n, "T necessary >": T_nec, "mT necessary >": n * T_nec,
                     "mT_nec/n^1.5": n * T_nec / n ** 1.5, "T0 sufficient (kappa=1)": T0_suff})
    out["R=1_no_shift_cost"] = rows
    # (I4) expansive histories (outside the nonexpansive class), R = 1:
    # hold h = a for k steps, credit sum_j (1+a)^j.  Code a = .3 +- .1
    rows = []
    for n in [64, 1024, 16384, 2 ** 20]:
        w = W_TRANSPLANT / math.sqrt(n)
        k = 0
        while True:
            k += 1
            T = k + 2
            f = lambda a: ((1 + a) ** T - 1) / a
            # spread code: |delta| = f(.4) - f(.2) on every coordinate, mu entries >= 1/(2 sqrt n)
            sep = w * (f(0.4) - f(0.2)) * 0.5
            if sep >= 0.002:
                break
        rows.append({"n": n, "horizon T": k + 2, "log n": math.log(n),
                     "mT (m=n)": n * (k + 2), "mT/n^1.5": n * (k + 2) / n ** 1.5})
    # verify the closed-form credit with the actual recurrence for a small case
    R, m, T_hold = 1, 6, 9
    a = rng.uniform(0.2, 0.4, size=m)
    xs = [a.copy()] + [-psi(a) for _ in range(T_hold)] + [-(a + psi(a))]
    T = len(xs)
    ports, hT = run_port(xs, R, m)
    mu = np.ones(m) / math.sqrt(m)
    tot, _ = backprop_sum(ports, mu, R, m)
    pred = ((1 + a) ** T - 1) / a * mu  # sum_{j=0}^{T-1} (1+a)^j mu
    out["expansive_amplification_R=1"] = {"rows": rows,
                                          "closed form check err": float(np.abs(tot - pred).max()),
                                          "endpoint": float(np.abs(hT).max())}
    rec("I_ablations", out)


# ----------------------------------------------------------------------------
# Section K: fixed-feature transplant of the original normalization
#   state (h, s), h in R^{n_mem} (QSR), s in R^l (identity source block);
#   recurrent matrix W_full = [[S, K], [0, I_l]], K frozen at 0;
#   group RMS w_W = ||W_full||_F/n_tot, beta = ||W_full||_F, head 1/sqrt(n_tot);
#   fixed feature f_s = 1_l/sqrt(l); source prepared to sigma*1_l through the
#   source input channel, m coordinates per step (width never exceeds m).
# ----------------------------------------------------------------------------

def transplant_schedule(z, q, sigma, v=None):
    R, m = z.shape
    l = R * m
    mem = [np.zeros(m) for _ in range(R)] + [np.zeros(m) for _ in range(q * R)] + gemini_inputs(z)
    src = []
    for r in range(R):
        xi = np.zeros(l)
        xi[r * m:(r + 1) * m] = sigma
        src.append(xi)
    T = len(mem)
    if v is not None:
        mem = mem + future_head_inputs(v)
    src = src + [np.zeros(l) for _ in range(len(mem) - R)]
    return mem, src, T


def fixed_feature_projection_numpy(mem, src, mu_mem, T, R, m):
    """(1/n_tot) sum_{t<=T} lambda_t^mem (f_s^T s_{t-1}) given lambda_T^mem = mu_mem
    (past part only; the future part is common to both histories)."""
    l = R * m
    ports, hT = run_port(mem[:T], R, m)
    s = np.zeros(l)
    c = [0.0]
    for t in range(T):
        s = s + src[t]
        c.append(float(s.sum() / math.sqrt(l)))  # c[t] = f_s^T s_t
    lam = np.array(mu_mem, dtype=float)
    total = np.zeros_like(lam)
    for t in range(T, 0, -1):
        total += c[t - 1] * lam
        vv = ST_apply(lam, R, m)
        vv[:m] = vv[:m] * (1.0 + ports[t - 1])
        lam = vv
    return total, hT


def section_K():
    rng = np.random.default_rng(SEED + 12)
    out = {}
    sigma, rho, rho_f = 0.05, 0.5, 0.5
    # (K1) autograd: normalized fixed-feature projection of the full W_full gradient
    R, m, q = 4, 4, 5
    n_mem = R * m
    l = n_mem
    n_tot = n_mem + l
    th = rng.uniform(-1, 1, size=(R, m))
    v = rng.uniform(-rho_f, 0.0, size=(R, m))
    errs = []
    for sgn in [1, -1]:
        z = -(rho / 2) * (1 + sgn * th)
        mem, src, T = transplant_schedule(z, q, sigma, v)
        Wf = torch.zeros(n_tot, n_tot)
        Wf[:n_mem, :n_mem] = torch.tensor(S_matrix(R, m))
        Wf[n_mem:, n_mem:] = torch.eye(l)
        Wf.requires_grad_(True)
        state = torch.zeros(n_tot)
        for t in range(len(mem)):
            h1 = state[:m]
            p = torch.cat([h1 + 0.5 * h1 * h1, state[m:]])
            inp = torch.cat([torch.as_tensor(mem[t]), torch.zeros(n_mem - m), torch.as_tensor(src[t])])
            state = Wf @ p + inp
        frob = math.sqrt(n_tot)
        loss = state.sum() / math.sqrt(n_tot) / frob
        loss.backward()
        Gn = Wf.grad.numpy() * (frob / n_tot)
        proj_autograd = Gn[:n_mem, n_mem:] @ (np.ones(l) / math.sqrt(l))
        # numpy: full (past + future) sum with lambda at the final time = head
        hs = run(mem, R, m)
        lams = backprop(hs, np.ones(n_mem) / math.sqrt(n_tot), R, m)
        s = np.zeros(l)
        tot = np.zeros(n_mem)
        for t in range(1, len(mem) + 1):
            tot += lams[t] * (s.sum() / math.sqrt(l))
            s = s + src[t - 1]
        errs.append(float(np.abs(proj_autograd - tot / n_tot).max()))
    out["autograd_vs_formula_max_err"] = max(errs)
    # (K2) scaling, q = 193, l = n_mem = R^2, sign query
    q = 193
    rows = []
    for R in [8, 16, 32]:
        m = R
        n_mem = R * m
        l = n_mem
        n_tot = n_mem + l
        D_emp = max(1, n_mem // 16)
        G = random_sign_matrix(n_mem - D_emp, D_emp, rng)
        worst, worst_ratio = math.inf, math.inf
        for trial in range(3):
            th = code_theta(G, unit(rng, D_emp)).reshape(R, m)
            zp, zm = -(rho / 2) * (1 + th), -(rho / 2) * (1 - th)
            dz = zp - zm
            mu_mem = mu_closed(sign_choice_v(dz)) * math.sqrt(n_mem / n_tot)  # head 1/sqrt(n_tot)
            memp, srcp, T = transplant_schedule(zp, q, sigma)
            memm, srcm, _ = transplant_schedule(zm, q, sigma)
            gp, hp = fixed_feature_projection_numpy(memp, srcp, mu_mem, T, R, m)
            gm, hm = fixed_feature_projection_numpy(memm, srcm, mu_mem, T, R, m)
            assert np.abs(hp).max() == 0 and np.abs(hm).max() == 0
            dF = float(np.linalg.norm(gp - gm)) / n_tot
            l1, l2 = float(np.abs(dz).sum()), float(np.linalg.norm(dz))
            ineq = sigma * math.sqrt(l) * (q * R * rho_f * l1 / (2 * math.sqrt(n_tot * n_mem))
                                           - 2 * R * l2 / math.sqrt(n_tot)) / n_tot
            assert dF >= ineq - 1e-12
            worst = min(worst, dF)
            worst_ratio = min(worst_ratio, dF / ineq)
        lemma_bound = (sigma / (2 * math.sqrt(n_tot))) * rho * R * (q * rho_f / 32.032 - 2)
        rows.append({"R": R, "m": m, "n_mem": n_mem, "n_tot": n_tot, "T": (q + 3) * R,
                     "max input width": m, "mT/n_tot": m * (q + 3) * R / n_tot,
                     "min d_F (normalized fixed-feature, sign query)": worst,
                     "Corollary 4.3 bound (code-lemma constants)": lemma_bound,
                     "min d_F/(proved inequality)": worst_ratio})
    out["scaling"] = rows
    rec("K_fixed_feature_transplant", out)


# ----------------------------------------------------------------------------
# Section J: miscellaneous structural facts
# ----------------------------------------------------------------------------

def section_J():
    out = {}
    for eps in [1e-2, 1e-3]:
        h, k = eps, 0
        while h < 1e6:
            h = h + 0.5 * h * h
            k += 1
        out[f"rounds to blow-up from +{eps}"] = k
        out[f"2/eps for eps={eps}"] = 2 / eps
    rng = np.random.default_rng(SEED + 11)
    R, m = 3, 2
    z = rng.uniform(-0.5, 0.5, size=(R, m))
    res = []
    for d in [1e-2, 1e-3, 1e-4]:
        delta = d * rng.normal(size=R * m)
        hT = run(gemini_inputs(z), R, m, delta)[-1]
        res.append({"|delta|": d, "||h_T - Phi delta|| / ||delta||^2":
                    float(np.linalg.norm(hT - gamma_closed_form(z) * delta) / np.linalg.norm(delta) ** 2)})
    out["perturbed initial state: endpoint error is second order"] = res
    rec("J_misc", out)


if __name__ == "__main__":
    t0 = time.time()
    rec("versions", {"python": sys.version.split()[0], "numpy": np.__version__,
                     "torch": torch.__version__, "dtype": "float64", "seed": SEED})
    for sec in [section_A, section_B, section_C, section_D, section_E, section_F,
                section_F4, section_G, section_H, section_I, section_K, section_J]:
        s0 = time.time()
        sec()
        print(f"  [{sec.__name__} {time.time() - s0:.1f}s]", flush=True)
    rec("runtime_seconds", round(time.time() - t0, 1))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "checks_result.json"), "w") as f:
        json.dump(RESULTS, f, indent=1, default=float)
