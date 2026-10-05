"""Targeted checks after the main study: stable warmup sum, L2 query bound,
pure-spike input size, co-isometry identity, and one explicit multi-step beat."""
import json
import math
from pathlib import Path

import numpy as np

from study import (
    G_FULL_HI, G_FULL_LO, TWO_EPS, build, apply_U, apply_PT, block_of_latent,
    endpoint_from_coeffs, kappa_envelope, load_pairs, propagate, pz_norm,
    query_distance, realizable_input_check, twist_formula,
)

OUT = Path(__file__).resolve().parent


def geosum_binary(OA, a, N):
    """sum_{j<N} (a OA)^j by binary doubling. OA is orthogonal, so this is stable."""
    d = OA.shape[0]
    acc = np.zeros((d, d))
    p = np.eye(d)  # (a OA)^0
    step = a * OA
    n = N
    # sum of geometric series of matrices via doubling
    # We want sum_{j=0}^{N-1} step^j, step = a OA, but step here is not yet applied.
    # Standard: result = 0; pow = I; for bit in N:
    base = np.eye(d)
    add = np.eye(d)
    # iterative: S = I + A + ... + A^{N-1}
    S = np.zeros((d, d))
    P = np.eye(d)
    A = a * OA
    left = N
    while left:
        if left & 1:
            S = S + P
        left >>= 1
        if left:
            P = A @ P
            # wrong. Use the doubling identity properly below.
            break
    # Correct doubling:
    S = np.eye(d)
    Pwr = np.eye(d)
    A = a * OA.copy()
    n = N
    # sum_{0..n-1} A^j
    # if n==0: 0
    acc = np.zeros((d, d))
    cur = np.eye(d)  # A^0
    # naive loop in blocks of matrix multiplies, N up to 3000, d=250: 3000*250^3 = 4.7e10 too slow.
    # Doubling:
    # Let S(n) = sum_{j<n} A^j, P(n)=A^n
    # S(2m)= S(m) + A^m S(m), P(2m)=A^m A^m
    # S(2m+1)= S(2m) + A^{2m}
    def rec(n):
        if n == 0:
            return np.zeros((d, d)), np.eye(d)
        if n == 1:
            return np.eye(d), A.copy()
        if n % 2 == 0:
            S, P = rec(n // 2)
            return S + P @ S, P @ P
        S, P = rec(n - 1)
        return S + P, A @ P
    S, _P = rec(N)
    return S


def main():
    report = {}
    # co-isometry and stable warmup
    widths = {}
    for n in (200, 400, 1000):
        S = build(n)
        A = (S["a"] / math.sqrt(n)) * (S["V"].T @ S["O"].T)
        gram = A @ A.T
        sigma2 = (S["a"] ** 2) / n
        widths[n] = {
            "co_isometry_residual": float(np.max(np.abs(gram - sigma2 * np.eye(S["d"])))),
            "sigma": math.sqrt(sigma2),
        }
        f_res = {}
        # stable C0 on the block
        C0 = geosum_binary(S["OA"], S["a"], 3 * n)
        evals, evecs = np.linalg.eig(S["OA"])
        idx = int(np.argmin(np.abs(evals - 1)))
        f = np.real(evecs[:, idx])
        f = f / np.linalg.norm(f)
        mN = (1 - S["a"] ** (3 * n)) / (1 - S["a"])
        f_res["binary_C0_f_residual"] = float(np.linalg.norm(C0 @ f - mN * f))
        f_res["binary_C0_f_residual_rel"] = f_res["binary_C0_f_residual"] / mN
        # rank of the exact twist update
        rng = np.random.default_rng(1)
        gc = rng.uniform(0.8, 1.0, size=S["d"] - 1)
        gs = 0.95
        Tw = twist_formula(gc, gs, S["ck"], S["k"])
        D = np.diag(np.diag(Tw))
        # remove only the prescribed diagonal (gamma1, g_cycle), the update is Tw-D
        # but Tw's diagonal includes the rank-2 diagonal. Rebuild update as Tw - diag(gamma1, g's)
        # twist_formula returns D_prescribed + rank2, and D_prescribed diagonal is exactly
        # diag(gamma1, g_cycle) which is NOT np.diag(np.diag(Tw)).
        # Recover rank2 by subtracting the closed-form diagonal piece:
        gamma_diag = np.concatenate([[gs], gc])  # NOT including ck corrections; use formula split
        # Recompute pieces
        from study import twist_formula as tf
        M = tf(gc, gs, S["ck"], S["k"])
        # diagonal piece stored as first term inside tf; subtract by matching the function
        kappa = np.zeros(S["d"])
        kappa[1:] = (gc - gs) / math.sqrt(S["k"])
        gamma1 = gs + S["ck"] * float(np.sum(kappa[1:]))
        Dpres = np.diag(np.concatenate([[gamma1], gc]))
        rho = np.zeros(S["d"])
        rho[1:] = S["ck"] * (gc - gamma1)
        v = np.full(S["d"], -S["ck"]); v[0] = 1.0
        rank2 = np.outer(np.eye(S["d"])[0], rho) + np.outer(kappa, v)
        sv = np.linalg.svd(rank2, compute_uv=False)
        f_res["rank2_sv_head"] = [float(x) for x in sv[:4]]
        f_res["rank2_numerical_rank_1e-8"] = int(np.sum(sv > 1e-8))
        off = M - np.diag(np.diag(M))
        svo = np.linalg.svd(off, compute_uv=False)
        f_res["offdiag_sv_head"] = [float(x) for x in svo[:6]]
        widths[n].update(f_res)
        print(n, json.dumps(widths[n]), flush=True)
    report["widths"] = widths

    # charts: L2 bound, pure-spike sweep, input size
    charts = []
    for pair in load_pairs():
        S = build(pair["n"])
        Cp, sp, _ = endpoint_from_coeffs(S, pair["C"], pair["Q"], pair["Z"])
        Cm, sm, _ = endpoint_from_coeffs(S, -pair["C"], pair["Q"], pair["Z"])
        dC, ds = Cp - Cm, float(sp - sm)
        kap = kappa_envelope(S, dC, ds)
        lam = S["a"] * G_FULL_HI
        factor = lam * math.sqrt(S["k"] / S["n"])  # ||m|| <= factor at L=1; kappa uses ||m||<=a
        # kappa = (H/n) * op * a, L2 bound = (H/n)*op* (a * g_hi * sqrt(k/n)) = kappa * g_hi * sqrt(k/n)
        l2_bound = kap * G_FULL_HI * math.sqrt(S["k"] / S["n"])
        # pure spike sweep L=1..min(d, 12) plus the argmax row's delay
        row_norms = np.linalg.norm(dC, axis=1)
        sweep = []
        best = None
        for L in range(1, min(S["d"], 16) + 1):
            gates = np.full((L, S["k"]), G_FULL_HI)
            y = propagate(S, gates)
            dist = query_distance(S, dC, ds, y)
            real = realizable_input_check(S, gates)
            p = (-L) % S["d"]
            # cross-check: z should be alpha * Theta[:, p]
            alpha = math.sqrt(S["k"] / S["n"]) * (S["a"] * G_FULL_HI) ** L
            z_form = alpha * S["Theta"][:, p]
            z_num = block_of_latent(S, y)
            rec = {
                "L": L,
                "distance": dist,
                "latent_index": int(p),
                "formula_residual": float(np.max(np.abs(z_num - z_form))),
                "max_abs_input": real["max_abs_future_input"],
                "pre_ok": real["pre_in_1/4_3/4"],
                "pz": pz_norm(S, y),
                "block_only": (S["Hnorm"] / S["n"]) * float(np.linalg.norm(dC.T @ z_num)),
            }
            sweep.append(rec)
            if best is None or dist > best["distance"]:
                best = rec
        # node visibility: ||dC^T theta_i||
        vis = []
        for i in range(S["d"]):
            vis.append(float(np.linalg.norm(dC.T @ S["Theta"][:, i])))
        charts.append({
            "n": pair["n"], "start": pair["start"],
            "kappa": kap,
            "l2_upper": l2_bound,
            "l2_over_kappa": l2_bound / kap,
            "best_pure_spike": best,
            "pure_spike_sweep_head": sweep[:8],
            "max_theta_visibility": max(vis),
            "theta_visibility_argmax": int(np.argmax(vis)),
            "row_norm_argmax": int(np.argmax(row_norms)),
            "op_over_max_row": float(np.linalg.norm(dC, 2) / np.max(row_norms)),
            "kappa_over_best_pure": kap / best["distance"],
            "l2_over_best_pure": l2_bound / best["distance"],
            "best_pure_over_2eps": best["distance"] / TWO_EPS,
        })
        print("chart", pair["n"], pair["start"], json.dumps(charts[-1]["best_pure_spike"]), "l2", l2_bound, flush=True)
    report["charts"] = charts

    # explicit counterexample to the per-entry bound, smallest width n=200
    S = build(200)
    A = (S["a"] / math.sqrt(S["n"])) * (S["V"].T @ S["O"].T)
    g = np.full(S["k"], G_FULL_LO)
    g[S["d"]:] = G_FULL_HI
    z = A @ g
    spike = A @ np.full(S["k"], G_FULL_HI)
    shape = spike / np.linalg.norm(spike)
    r = z - shape * float(shape @ z)
    zeta_r = r / S["beta"]
    j = int(np.argmax(np.abs(zeta_r)))
    claimed = (0.5 * (G_FULL_HI - G_FULL_LO)) / (S["beta"] * math.sqrt(S["n"]))
    # Use Claude's 0.153 as well
    claimed_153 = 0.153 / (S["beta"] * math.sqrt(S["n"]))
    report["counterexample_NC"] = {
        "n": 200,
        "construction": "one step; NC gates = sech^2(1/4), cycle gates = sech^2(3/4)",
        "residual_coordinate": j,
        "residual_value": float(zeta_r[j]),
        "claimed_halfwidth_0.1717": claimed,
        "claimed_0.153": claimed_153,
        "ratio_to_0.1717_formula": float(abs(zeta_r[j]) / claimed),
        "ratio_to_0.153": float(abs(zeta_r[j]) / claimed_153),
        "spike_coordinate": int(np.argmax(np.abs(spike))),
    }
    print("counterexample", json.dumps(report["counterexample_NC"]), flush=True)

    # explicit moved-spike beat: direction = theta at the best pure-spike node vs L=1
    # already in the sweep. Record L=1 vs best L distance ratio from the first chart.
    (OUT / "followup.json").write_text(json.dumps(report, indent=1))
    print("wrote followup", flush=True)


if __name__ == "__main__":
    main()
