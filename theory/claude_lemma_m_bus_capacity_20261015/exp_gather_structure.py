"""Structural checks for Theorem M (PROOF.md sections 3-4), on random adversarial histories (small n).

For one history at a time (the statements are per-history), with the R0-skeleton credit B' and the
actual gates of an R0 forward trajectory driven by a random sparse schedule (holes held along
diagonals, a held gather spike with gaps, off-cycle holes, random large-amplitude drives), checks:
  (S1) the exact eight-part decomposition of the gather row's bus content (section 3):
       Z_T(d-1) = K_pos + K_neg + K_uni + K_bus + L_own_cyc + L_own_off + L_bus + W + F_ent;
  (S2) K_pos is non-decreasing in the cycle column index r = 1..d-1 and zero off the cycle
       (monotone in the offset from d-1), relative violation reported;
  (S3) TV(K_uni + L_own_cyc + W) <= (6 gamma c_max/k + 4 gamma^2 c_max/k^1.5) Sigma_P along the path,
       where L_own_cyc is the leak of CYCLE-row own contents; TV of every cycle-row own profile
       <= 2 c_max; off-cycle own contents are single-column scalars (reported: they can be large,
       which is why Theorem M treats off-cycle leak sources separately, part (d));
  (S4) the bath ceiling inequality of Lemma B with the measured m:
       s_(t+1) <= tanh(.05 + gamma^2 (m+1)(1 + s_hi + Sigma_neg)/k + 3 gamma/sqrt k),
       and the mass lower bound M_t >= -(1 + s_hi)(m+1) - (m+1) Sigma_neg.
Finite small-n evidence that the identities and structural inequalities have no missing term.
Not a proof; the theorem-scale constants are certified in constants_check.py.
Run: python -I exp_gather_structure.py
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA_NEG = 506.0


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def tv(v):
    return float(np.abs(np.diff(v)).sum())


def run(n, T, m, seed):
    rng = np.random.default_rng(seed)
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k)
    a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / sk)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / sk; w[0] += 1
    idx = np.arange(1, k)
    # schedule: hole diagonals (arrival-type), gather spike with gaps, off-cycle holes, random drives
    hole_diag = set(rng.choice(np.arange(-d, T), size=min(T, 6 * m), replace=False).tolist())
    spike_diag = T - (d - 1)
    off_holes = rng.choice(np.arange(d, k), size=max(1, m // 4), replace=False)
    h = np.zeros(n); s = 0.0
    B = np.zeros((k, k)); Y = np.zeros((k, k)); O = np.zeros((k, k))
    tf = max(1, T - d + 2)
    acc = {nm: np.zeros(k) for nm in ("K_pos", "K_neg", "K_uni", "K_bus", "L_own_cyc", "L_own_off", "L_bus", "W", "F_ent")}
    SigmaP = 0.0; maxtvO = 0.0; maxoff = 0.0; ceil_viol = 0.0; mass_viol = 0.0; max_drive = 0
    for t in range(1, T + 1):
        hm = h[:k]
        Jt = gam * hm[d - 1] / sk - gam ** 2 * hm[1:].sum() / k
        beta = .05 + a * Jt
        Mt = float((hm[1:] - s).sum())
        # Lemma B check (uses this step's mass and the next bath value)
        s_new = math.tanh(beta + a * s)
        bound = math.tanh(.05 + gam ** 2 * (m + 1) * (1 + .1009 + SIGMA_NEG) / k + 3 * gam / sk)
        ceil_viol = max(ceil_viol, s_new - bound)
        mass_viol = max(mass_viol, -(1 + .1009) * (m + 1) - (m + 1) * SIGMA_NEG - Mt)
        pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        drv = {}
        rows = np.arange(1, d)
        diag_ids = t - rows
        for r, dg in zip(rows, diag_ids):
            if dg in hole_diag and r >= 3:
                drv[int(r)] = 0.0
        r_sp = d - 1 - (T - t)
        if t >= tf and 7 <= r_sp <= d - 1 and rng.random() < .97:
            drv[int(r_sp)] = 0.0
        for r in off_holes:
            drv[int(r)] = 0.0
        extra = rng.choice(np.arange(1, k), size=max(1, m // 3), replace=False)
        for r in extra:
            drv[int(r)] = float(rng.uniform(-.95, .95))
        # enforce peak width m (keep the first m drives)
        drv = dict(list(drv.items())[:m])
        max_drive = max(max_drive, len(drv))
        for r, tgt in drv.items():
            hn[r] = tgt
        s = s_new
        ghat = 1 - s * s
        g = 1 - hn ** 2; gm = g[:k]
        c = h[k:].sum() / (sig * l)
        delta = gm[1:] - ghat
        St = float(delta.sum())
        # credit and U-coordinates
        Bn = a * O_apply(B, k, d, gam); Bn[idx, idx] += c; Bn *= gm[:, None]
        Yn = Bn + (gam / sk) * (w @ Bn)[None, :]; Yn[0] = Bn.sum(0) / sk
        On = np.zeros((k, k)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[idx, idx] += c * gm[1:]
        Zp = Y - O; Zp[0] = Y[0]
        if t >= tf:
            p = d - 1 - (T - t)
            for nm in acc:
                acc[nm] *= a * gm[p]
            dp = gm[p] - ghat
            Oarr = a * O[d - 1]; Zarr = a * Zp[d - 1]
            acc["K_pos"] += (gam / sk) * max(dp, 0.0) * Oarr
            acc["K_neg"] += -(gam / sk) * max(-dp, 0.0) * Oarr
            acc["K_uni"] += -(gam ** 2 / k ** 1.5) * St * Oarr
            acc["K_bus"] += (gam / sk) * (dp - gam * St / k) * Zarr
            # pi^-1 j: j-1 for cycle 2..d-1, 0 for j = 1, j for off-cycle
            Osrc = np.empty((k - 1, k)); Zsrc = np.empty((k - 1, k))
            Osrc[0] = 0.0; Osrc[1:d - 1] = O[1:d - 2 + 1][:d - 2]; Osrc[d - 1:] = O[d:k]
            Zsrc[0] = Y[0]; Zsrc[1:d - 1] = Zp[1:d - 1][:d - 2]; Zsrc[d - 1:] = Zp[d:k]
            dc_ = delta.copy(); dc_[d - 1:] = 0.0           # j = 1..d-1 cycle sources (index j-1)
            do_ = delta.copy(); do_[:d - 1] = 0.0           # j >= d off-cycle sources
            acc["L_own_cyc"] += -(gam * a / k) * (dc_ @ Osrc)
            acc["L_own_off"] += -(gam * a / k) * (do_ @ Osrc)
            acc["L_bus"] += -(gam * a / k) * (delta @ Zsrc)
            gv = gm.copy(); gv[0] = 0.0
            acc["W"] += -(gam / k) * c * gv
            if t == tf and p == 1:
                acc["F_ent"] += gm[1] * a * Y[0]
            SigmaP += float(np.abs(delta).sum())
        for r in range(1, d):                               # cycle rows only (Theorem M (c))
            if On[r].any():
                maxtvO = max(maxtvO, tv(On[r, 1:]))
        maxoff = max(maxoff, float(np.abs(On[d:, :]).max()))
        h = hn; B = Bn; Y = Yn; O = On
    ZT = Y[d - 1] - O[d - 1]
    recon = sum(acc.values())
    Kp = acc["K_pos"]
    cyc = Kp[1:d]; off = Kp[d:]
    viol = float(np.maximum(0.0, cyc[:-1] - cyc[1:]).max()) / max(1e-300, float(np.abs(cyc).max()))
    bv = acc["K_uni"] + acc["L_own_cyc"] + acc["W"]
    cmax = 1.0
    tv_bound = (6 * gam * cmax / k + 4 * gam ** 2 * cmax / k ** 1.5) * SigmaP
    return {"n": n, "T": T, "m": m, "seed": seed, "max_drives_per_step": max_drive,
            "S1_decomposition_rel_residual": float(np.abs(recon - ZT).max() / max(1e-300, np.abs(ZT).max())),
            "S2_K_pos_monotone_rel_violation": viol, "S2_K_pos_offcycle_max": float(np.abs(off).max()),
            "S3_TV_ratio_cycle_sources": tv(bv[1:]) / tv_bound, "S3_max_TV_cycle_own_profile": maxtvO,
            "S3_max_offcycle_own_scalar": maxoff,
            "S3_offcycle_leak_supported_on_offcycle_cols": bool(np.abs(acc["L_own_off"][:d]).max() == 0.0),
            "S4_ceiling_violation(<=0 ok)": ceil_viol, "S4_mass_violation(<=0 ok)": mass_viol,
            "term_norms": {nm: float(np.linalg.norm(v)) for nm, v in acc.items()}}


if __name__ == "__main__":
    out = []
    for n, T, m, seed in [(256, 300, 12, 1), (512, 400, 20, 2), (512, 700, 30, 3), (1024, 600, 40, 4)]:
        r = run(n, T, m, seed); print(json.dumps(r), flush=True); out.append(r)
    with open(os.path.join(HERE, "exp_gather_structure_result.json"), "w") as f:
        json.dump(out, f, indent=1)
