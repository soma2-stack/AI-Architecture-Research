"""Dense-matrix transfer of Theorem R (PROOF.md section 2.4): exact dense dynamics, CPU, small n.

The prescribed frozen matrix (gamma_c_over_n_quadratic_20261001 section 7, c = 1) is
    R = (a/||B||op) B,   B = R0 + eta C,   C = u v^T/(||u|| ||v||),
with u, v the first admissible integer power vectors. t = 1 is admissible for both (D1 below),
so u = v = 1_n and C = 1 1^T/n. This script builds R as an EXPLICIT dense n x n matrix and runs the
drift-capture construction with ACTUAL inputs: x_t = atanh(target) - (R h_(t-1) + b) on driven
coordinates and x_t = 0 exactly elsewhere (no inverse lift). It checks:
  (D1) R0^-1 1 and 1^T R0^-1 have no zero entry (so t = 1 is the admissible power base);
       R and R^-1 have no zero entry; ||R||op = a; ||R - R0||op <= 2 eta;
  (D2) for theta = +1, -1, 0, .5: actual support = driven set, max |x| < .5,
       the state differences Delta h_t are supported on modulated positions, sum Delta h_t = 0,
       and h_T is common (exact-endpoint check in floating point);
  (D3) the zero-sum identity R Delta h = alpha R0 Delta h at every step;
  (D4) adversarial C = u v^T with v NOT proportional to 1 (power base t = 2, and a random positive
       v): the same sparse actual inputs no longer reach a common endpoint, and Delta h spreads
       to every coordinate (dense corrections would be needed);
  (D5) credit (n <= 512): actual dense credit B_t = G_t(R B_(t-1) + c_t E) vs the R0 credit
       B'_t = G_t(R0 B'_(t-1) + c_t E) with the same actual gates; uniform-query readouts
       nu_R^T Delta B_T and nu^T Delta B'_T (Hypothesis B's bus readout); zero own differences
       on local paths at T.
Runs use eta in {contract value 1e-8/n^2, and adversarially large 1e-6, 1e-3}: the exact identities
do not depend on eta being small. A high-precision variant (mpmath, 50 digits) of (D2)/(D3) is in
exp_dense_transfer_mp.py. Finite numerical evidence only; the theorem is proved in PROOF.md 2.4.
Run: python -I exp_dense_transfer.py
"""
import json, math, os, sys
import importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dc", os.path.join(HERE, "exp_drift_capture.py"))
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)


def R0_dense(n):
    k, d = n // 2, n // 4; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    R0 = np.zeros((n, n))
    for j in range(k):
        e = np.zeros(k); e[j] = 1.0
        R0[:k, j] = a * dc.O_apply(e, k, d, gam)
    R0[k:, k:] = lam * np.eye(n - k)
    return R0


def dense_R(R0, eta, u=None, v=None):
    n = R0.shape[0]; a = 1 - 1 / n
    u = np.ones(n) if u is None else u; v = np.ones(n) if v is None else v
    C = np.outer(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    B = R0 + eta * C
    nb = np.linalg.norm(B, 2)
    return (a / nb) * B, a / nb


def run_states(S, R, theta):
    n, T = S["n"], S["T"]
    h = np.zeros(n); hs = [h.copy()]; xs = []; maxx = 0.0
    for t in range(1, T + 1):
        pre = R @ h + .05
        hn = np.tanh(pre); x = np.zeros(n)
        for r, (kind, sgn) in S["drv"].get(t, {}).items():
            tgt = 0.0 if kind == "hole" else math.tanh(sgn * dc.DELTA * (1 + theta) / 2)
            x[r] = math.atanh(tgt) - pre[r]; hn[r] = tgt
        maxx = max(maxx, float(np.abs(x).max()))
        h = hn; hs.append(h.copy()); xs.append(x)
    return hs, xs, maxx


def modulated_set(S, t):
    return {r for r, (kind, sgn) in S["drv"].get(t, {}).items() if kind == "mod"}


def state_checks(S, R, R0, alpha, thetas=(1, -1, 0, .5)):
    runs = {th: run_states(S, R, th) for th in thetas}
    out = {"max_abs_input": max(r[2] for r in runs.values())}
    supp_ok = True
    for th, (hs, xs, _) in runs.items():
        for t, x in enumerate(xs, start=1):
            drv = set(S["drv"].get(t, {}).keys())
            if not set(np.nonzero(x)[0].tolist()) <= drv:
                supp_ok = False
    out["actual_support_within_driven_set"] = supp_ok
    hp, hm = runs[1][0], runs[-1][0]
    off_mod = 0.0; zsum = 0.0; ident = 0.0
    for t in range(len(hp)):
        dh = hp[t] - hm[t]
        mods = modulated_set(S, t)
        mask = np.ones(len(dh), bool)
        for r in mods:
            mask[r] = False
        off_mod = max(off_mod, float(np.abs(dh[mask]).max()))
        zsum = max(zsum, abs(float(dh.sum())))
        ident = max(ident, float(np.abs(R @ dh - alpha * (R0 @ dh)).max()))
    out["max_state_diff_off_modulated_positions"] = off_mod
    out["max_abs_sum_Delta_h"] = zsum
    out["max_|R dh - alpha R0 dh|"] = ident
    T = S["T"]
    out["endpoint_diff_pm1"] = float(np.abs(hp[T] - hm[T]).max())
    out["endpoint_diff_all_theta"] = max(float(np.abs(runs[th][0][T] - hp[T]).max()) for th in thetas)
    return out, runs


def credit_checks(S, R, R0, runs, gf):
    n, k, d, T = S["n"], S["n"] // 2, S["n"] // 4, S["T"]
    l = n - k; lam = 1 / (100 * n)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    E = np.eye(n); E[0, 0] = 0.0
    res = {}
    Bs, Bps = {}, {}
    for th in (1, -1):
        hs = runs[th][0]
        B = np.zeros((n, n)); Bp = np.zeros((n, n))
        for t in range(1, T + 1):
            g = 1 - hs[t] ** 2
            c = hs[t - 1][k:].sum() / (sig * l)
            B = g[:, None] * (R @ B + c * E)
            Bp = g[:, None] * (R0 @ Bp + c * E)
        Bs[th], Bps[th] = B, Bp
    gvec = gf * np.ones(n)
    nuR = R.T @ gvec; nu0 = R0.T @ gvec
    dB = Bs[1] - Bs[-1]; dBp = Bps[1] - Bps[-1]
    GR = nuR @ dB; G0 = nu0 @ dBp
    tau = .002 * n * math.sqrt(n) / (sig * math.sqrt(l))
    res["norm_actual_readout_nuR_dB"] = float(np.linalg.norm(GR[1:]))
    res["norm_bus_readout_nu0_dBprime"] = float(np.linalg.norm(G0[1:]))
    res["norm_difference"] = float(np.linalg.norm((GR - G0)[1:]))
    res["tau"] = tau
    # own differences on local paths at T are zero: no gate difference on any local path of a row at T
    hits = 0
    for t in range(1, T + 1):
        dg = np.abs((1 - runs[1][0][t] ** 2) - (1 - runs[-1][0][t] ** 2))
        for r in np.nonzero(dg > 1e-13)[0]:
            if (1 <= r <= d - 1 and r + (T - t) <= d - 1) or (d <= r < k):
                hits += 1
    res["gate_differences_on_local_paths_at_T"] = hits
    return res


def main():
    out = []
    for n in (256, 512, 1024):
        k = n // 2; d = n // 4
        S = dc.schedule(n, 16, wsim=4 if n == 256 else 16)
        R0 = R0_dense(n)
        # (D1) admissibility of t = 1 and density
        inv0 = np.linalg.inv(R0)
        d1 = {"min_abs_entry_R0inv_1": float(np.abs(inv0 @ np.ones(n)).min()),
              "min_abs_entry_1T_R0inv": float(np.abs(np.ones(n) @ inv0).min())}
        for eta in (1e-8 / n ** 2, 1e-6, 1e-3):
            R, alpha = dense_R(R0, eta)
            rec = {"n": n, "eta": eta, "alpha": alpha, **d1,
                   "R_min_abs_entry": float(np.abs(R).min()),
                   "R_opnorm_minus_a": float(np.linalg.norm(R, 2) - (1 - 1 / n)),
                   "R_minus_R0_opnorm_over_2eta": float(np.linalg.norm(R - R0, 2) / (2 * eta))}
            if n <= 512:
                rec["Rinv_min_abs_entry"] = float(np.abs(np.linalg.inv(R)).min())
            st, runs = state_checks(S, R, R0, alpha)
            rec.update(st)
            if n <= 512 and eta != 1e-6:
                rec.update(credit_checks(S, R, R0, runs, dc.HI))
            print(json.dumps(rec), flush=True); out.append(rec)
        # (D4) adversarial rank-one perturbations whose right factor is not proportional to 1
        for name, v in (("power_t2", 2.0 ** (np.arange(n) - (n - 1))), ("random_pos", np.random.default_rng(1).uniform(.5, 1.5, n))):
            for eta in (1e-6, 1e-3):
                R, alpha = dense_R(R0, eta, u=np.ones(n), v=v)
                st, _ = state_checks(S, R, R0, alpha, thetas=(1, -1))
                rec = {"n": n, "adversarial_C": name, "eta": eta,
                       "endpoint_diff_pm1": st["endpoint_diff_pm1"],
                       "max_state_diff_off_modulated_positions": st["max_state_diff_off_modulated_positions"]}
                print(json.dumps(rec), flush=True); out.append(rec)
    with open(os.path.join(HERE, "exp_dense_transfer_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
