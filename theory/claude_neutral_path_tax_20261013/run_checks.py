"""Reproducible checks for the neutral-path-tax study (Claude, 2026-10-13).

DIAGNOSTIC ONLY: finite-n numerics cannot prove an asymptotic statement.
Runs in about two to three minutes on one core (float64, numpy + torch CPU).
Writes run_checks_result.json next to this file.  Large-n results (32k-128k) are
produced separately with  python -I scaling_run.py <n> <W>  (see scaling.json).
"""
import json
import math
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "4")
from hubcore import Frozen, design, run, ff_sep, reduced_model, LO, HI  # noqa: E402

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
    except Exception:
        pass

RES = {}


def rec(key, val):
    RES[key] = val
    print(f"{key}: {json.dumps(val, default=float)}", flush=True)


def check_algebra():
    F = Frozen(2000)
    k, d, g = F.k, F.d, F.gamma
    M = np.stack([F.O(np.eye(k)[j]) for j in range(k)], axis=1)
    u = np.ones(k) / math.sqrt(k)
    e = np.eye(k)
    rng = np.random.default_rng(0)
    x = rng.normal(size=k)
    x[0] = 0.0
    Ox = F.O(x)
    S = x[1:].sum()
    J = g * x[d - 1] / math.sqrt(k) - g * g * S / k
    out = {
        "orthogonality_err": float(np.abs(M @ M.T - np.eye(k)).max()),
        "row_identity_err": float(max(abs(Ox[0]), abs(Ox[1] - (J + g * S / math.sqrt(k))),
                                      np.abs(Ox[2:d] - (x[1:d - 1] + J)).max(),
                                      np.abs(Ox[d:] - (x[d:] + J)).max())),
        "O_e0_minus_e0": float(np.abs(F.O(e[0]) - e[0]).max()),
        "O_u_formula_err": float(np.abs(F.O(u) - (e[1] + g / math.sqrt(k) * (e[0] - u))).max()),
        "O_e(d-1)_broadcast_formula_err": float(np.abs(
            F.O(e[d - 1]) - ((1 - g * g / k) * u + g / math.sqrt(k) * e[1]
                            + (g * g / k - g / math.sqrt(k)) * e[0])).max()),
        "broadcast_entry_rows_2..k-1": float(F.O(e[d - 1])[5]),
        "1/sqrt(k)": 1 / math.sqrt(k),
    }
    rec("A_exact_householder_algebra", out)


def check_background():
    F = Frozen(16000)
    D = design(F, 30)
    r = run(F, D, np.ones(D["Pc"]), np.ones(len(D["Soff"]) // 2), True, record=True)
    xs = r["xs"]
    d = F.d
    hole_inputs_pre = [float(np.abs(x[D["holes0"][0] + (t - D["ts"] + 1)]).max())
                       for t, x in enumerate(xs[D["ts"]:D["t1"] - 2], start=D["ts"])
                       if D["holes0"][0] + (t - D["ts"] + 1) <= d - 1][:2000]
    rec("B_background_and_holes", {
        "n": F.n, "max_input_overall": r["max_in"],
        "hole_maintenance_input_before_window_max": max(hole_inputs_pre),
        "hole_credit_at_first_broadcast": r["hole_credit"],
        "hole_credit/sqrt(k)": r["hole_credit"][0] / math.sqrt(F.k),
        "predicted_c_h/sqrt(k)": reduced_model(F.n, 0.92, 1)[2]})


def pair(F, D, tc, to):
    A = run(F, D, tc, to, True)
    B = run(F, D, -tc, -to, True)
    C = run(F, D, tc, to, False)
    E = run(F, D, -tc, -to, False)
    dh, dc = A["Bf"] - B["Bf"], C["Bf"] - E["Bf"]
    return dict(endpoint=float(np.abs(A["h"] - B["h"]).max()), max_in=max(A["max_in"], B["max_in"]),
                supp_over_n=A["supp"] / F.n, total=ff_sep(F, dh), control=ff_sep(F, dc),
                hole_only=ff_sep(F, dh - dc))


def check_hub_scaling():
    rows = []
    for n in (4000, 8000, 16000):
        F = Frozen(n)
        D = design(F, 30)
        rng = np.random.default_rng(7)
        tc = rng.choice([-1.0, 1.0], size=D["Pc"])
        to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
        p = pair(F, D, tc, to)
        assert p["endpoint"] < 1e-12 and p["max_in"] < 0.5
        rows.append(dict(n=n, W=30, Pc=D["Pc"], Poff=len(D["Soff"]) // 2, T=D["T"], **p))
    rec("C_hub_vertex_code_W30", rows)


def check_W_scan():
    F = Frozen(16000)
    rng = np.random.default_rng(7)
    rows = []
    for W in (5, 10, 15, 20, 30, 80):
        D = design(F, W)
        tc = rng.choice([-1.0, 1.0], size=D["Pc"])
        to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
        p = pair(F, D, tc, to)
        s = 2 * (D["Pc"] + len(D["Soff"]) // 2) / F.k
        rows.append(dict(W=W, hole_only=p["hole_only"], reduced_model=reduced_model(F.n, s, W)[0],
                         supp_over_n=p["supp_over_n"]))
    rec("D_held_window_scan_n16000", rows)


def check_codes():
    F = Frozen(16000)
    D = design(F, 30)
    Pc, Po = D["Pc"], len(D["Soff"]) // 2
    rng = np.random.default_rng(11)
    G = rng.normal(size=(Pc + Po, 20))
    rows = []
    for _ in range(3):
        y = rng.normal(size=20)
        y /= np.linalg.norm(y)
        th = np.clip(8.0 * (G @ y), -1.0, 1.0)
        p = pair(F, D, th[:Pc], th[Pc:])
        rows.append(dict(saturated_fraction=float(np.mean(np.abs(th) >= 1)), **p))
    rec("E_continuous_code_points_n16000_W30", rows)


def check_autograd():
    import torch
    torch.set_default_dtype(torch.float64)
    rows = []
    for n in (400, 800):
        F = Frozen(n)
        D = design(F, 6, p0=10, wake_skip=8)
        rng = np.random.default_rng(3)
        tc = rng.choice([-1.0, 1.0], size=D["Pc"])
        to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
        A = run(F, D, tc, to, True, record=True)
        B = run(F, D, -tc, -to, True, record=True)
        dB = A["Bf"] - B["Bf"]
        z = F.R0(dB)
        gf = np.where(z > 0, HI, LO)
        formula = F.sigma * math.sqrt(F.l) / n * (gf @ z) / math.sqrt(n)
        R0d = np.stack([F.R0(np.eye(n)[j]) for j in range(n)], axis=1)
        from hubcore import direction
        v = direction(F, D)
        Ev = v.copy()
        Ev[0] = 0.0
        fs = np.zeros(n)
        fs[F.k:] = 1 / math.sqrt(F.l)
        comps = []
        for xs in (A["xs"], B["xs"]):
            R = torch.tensor(R0d, requires_grad=True)
            b = torch.full((n,), F.b0)
            h = torch.zeros(n)
            for x in xs:
                h = torch.tanh(R @ h + torch.as_tensor(x) + b)
            p = torch.where(torch.as_tensor(gf) > 0.9, torch.tensor(0.25), torch.tensor(0.75))
            xf = p - (R.detach() @ h.detach()) - b
            h1 = torch.tanh(R @ h + xf + b)
            Rn = float(torch.linalg.norm(R.detach()))
            L = h1.sum() / math.sqrt(n) / max(1.0, Rn)
            L.backward()
            comps.append(Rn / n * float(Ev @ R.grad.numpy() @ fs))
        rel = abs((comps[0] - comps[1]) - formula) / abs(formula)
        assert rel < 1e-10
        rows.append(dict(n=n, autograd_pair_difference=comps[0] - comps[1], formula=formula, rel_err=rel))
    rec("F_autograd_end_to_end", rows)


def check_reduced_asymptotics():
    rows = []
    for n, s in ((16000, 0.92), (64000, 0.96), (10 ** 8, 0.99)):
        rows.append(dict(n=n, s=s, **{f"W={W}": reduced_model(n, s, W)[0] for W in (10, 20, 30, 80)},
                         ceiling=reduced_model(n, s, 1)[1], c_h_over_sqrt_k=reduced_model(n, s, 1)[2]))
    rec("G_reduced_model", rows)


if __name__ == "__main__":
    t0 = time.time()
    check_algebra()
    check_background()
    check_hub_scaling()
    check_W_scan()
    check_codes()
    check_autograd()
    check_reduced_asymptotics()
    rec("runtime_seconds", round(time.time() - t0, 1))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_checks_result.json"), "w") as f:
        json.dump(RES, f, indent=1, default=float)
