"""Small-n audit of the own/bus error analysis of Theorem R (PROOF.md section 2.3, Steps 8-10).

Runs the exact credit recurrence of the drift-capture construction (R = R0, scaled n) for both
histories theta = +1, -1, in U-coordinates Y = U B' (memory block, memory columns), together with
the own parts O (local skeleton S with the actual gates) and the bus parts Z = Y - O. Checks:
  (X1) Lemma 1.2 for every memory U-row i >= 1 at every step (max residual);
  (X2) the broadcast identity (Step 9, (9.3))
         Y_t(0) = ghat V(0) + (1/sqrt k) sum_i delta_i V(i) + (gam/k)(sum delta) V(0) + (c/sqrt k) g^T;
  (X3) own differences Delta O_t(i) are supported on rows d-10..d-1 (Step 9, (O1));
  (X4) the exact unrolled spike decomposition (main, arrival bus, non-arrival, kappa, leak,
       w-injection, init) reproduces Delta Y_T(d-1) (Step 10);
and evaluates every inequality of Lemma E and the error bound (10.1), with the measured sup
quantities and the measured small-n constants (Sigma, Dbar, Lambda, nu_N, mu, mu_d, w, g1max,
s^2) in place of the theorem-scale constants. It reports LHS and RHS of each.
Finite small-n evidence that the identities are exact and the inequalities omit no term.
It is not a proof and does not reach the theorem's regime n >= 1.5e18.
Run: python -I exp_error_bounds.py [n[:ell] ...]     (default 512 1024 2048 2048:32)
"""
import json, math, os, sys
import importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dc", os.path.join(HERE, "exp_drift_capture.py"))
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)


def run(n, ell=None, wsim=64):
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); q = 1 / sk
    a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / sk)
    ell = ell or d - 8
    S = dc.schedule(n, ell, wsim=wsim); T, Ts = S["T"], S["Ts"]
    arrivals = set(range(S["alo"], S["ahi"] + 1))
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / sk; w[0] += 1
    idx = np.arange(1, k)
    st = {th: dict(h=np.zeros(n), B=np.zeros((k, k)), Y=np.zeros((k, k)), O=np.zeros((k, k)))
          for th in (1, -1)}
    # sup quantities
    sup = dict(zeta=0., B0=0., S=0., A=0., zeta_m=0., B0_m=0., S_m=0., A_m=0., OD=0., Oh=0., Os=0.)
    cst = dict(Sigma=0., mu=0., w=0., nuN=0., g1max=0., s2max=0., s2min=1.)
    res = dict(X1=0., X2=0.); dO_rows_bad = 0; dO_rows_minmax = [d, -1]
    nd = T + d + 2; off = d + 1                       # diagonal id = t - i, shifted by off
    Dsum = np.zeros((2, nd)); Lam = np.zeros(nd); mud = np.zeros(nd)
    acc = {nm: np.zeros(k) for nm in ("main", "arrbus", "nonarr", "kappa", "leak", "winj", "init")}
    dO_prev = np.zeros((k, k)); spike_diag = T - (d - 1) + off
    for t in range(1, T + 1):
        rec = {}
        for th in (1, -1):
            s_ = st[th]; h = s_["h"]
            pre = np.empty(n); pre[:k] = a * dc.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
            hn = np.tanh(pre)
            for r, (kind, sgn) in S["drv"].get(t, {}).items():
                hn[r] = 0.0 if kind == "hole" else math.tanh(sgn * dc.DELTA * (1 + th) / 2)
            c = h[k:].sum() / (sig * l)
            g = 1 - hn ** 2; gm = g[:k]
            Yp, Op = s_["Y"], s_["O"]
            Bn = a * dc_O_mat(s_["B"], k, d, gam)
            Bn[idx, idx] += c
            Bn *= gm[:, None]
            Y = Bn + (gam / sk) * (w @ Bn)[None, :]; Y[0] = Bn.sum(0) / sk
            On = np.zeros((k, k)); On[2:d] = gm[2:d, None] * a * Op[1:d - 1]; On[d:] = gm[d:, None] * a * Op[d:]
            On[idx, idx] += c * gm[1:]
            ghat = 1 - hn[k - 1] ** 2
            delta = gm[1:] - ghat
            Vp = np.empty_like(Yp); Vp[0] = Yp[d - 1]; Vp[1:d] = Yp[0:d - 1]; Vp[d:] = Yp[d:]   # P Y_(t-1)
            V = a * Vp
            gvec = gm.copy(); gvec[0] = 0.0
            lk = delta @ V[1:]
            rhs = gm[1:, None] * V[1:] + (gam / sk) * (delta - gam * delta.sum() / k)[:, None] * V[0][None, :] \
                - (gam / k) * lk[None, :] - (gam / k) * c * gvec[None, :]
            rhs[np.arange(k - 1), idx] += c * gm[1:]
            sc = max(1e-300, np.abs(Y).max())
            res["X1"] = max(res["X1"], float(np.abs(Y[1:] - rhs).max() / sc))
            y0 = ghat * V[0] + lk / sk + (gam / k) * delta.sum() * V[0] + (c / sk) * gvec
            res["X2"] = max(res["X2"], float(np.abs(Y[0] - y0).max() / sc))
            rec[th] = dict(hn=hn, gm=gm, c=c, Y=Y, O=On, Yp=Yp, Vp=Vp, delta=delta, ghat=ghat)
            s_["h"] = hn; s_["B"] = Bn; s_["Y"] = Y; s_["O"] = On
        P_, M_ = rec[1], rec[-1]
        s2 = 1 - P_["ghat"]
        cst["s2max"] = max(cst["s2max"], s2); cst["s2min"] = min(cst["s2min"], s2) if t >= 2 else cst["s2min"]
        sp = (d - 1 - (T - t)) if t >= Ts - 1 else None
        dY = P_["Y"] - M_["Y"]; dO = P_["O"] - M_["O"]; dZ = dY[1:d] - dO[1:d]
        Zm = M_["Y"][1:d] - M_["O"][1:d]
        mask = np.ones(d - 1, bool)          # zeta: all cycle positions except spike positions (i_t, t >= Ts)
        if sp is not None and t >= Ts:
            mask[sp - 1] = False
        nz = np.linalg.norm(dZ, axis=1); nzm = np.linalg.norm(Zm, axis=1)
        sup["zeta"] = max(sup["zeta"], float(nz[mask].max()))
        sup["zeta_m"] = max(sup["zeta_m"], float(nzm[mask].max()))
        sup["B0"] = max(sup["B0"], float(np.linalg.norm(dY[0])))
        sup["B0_m"] = max(sup["B0_m"], float(np.linalg.norm(M_["Y"][0])))
        if t < T:
            sup["A"] = max(sup["A"], float(np.linalg.norm(dY[d - 1])))
            sup["A_m"] = max(sup["A_m"], float(np.linalg.norm(M_["Y"][d - 1])))
        if sp is not None:
            sup["S"] = max(sup["S"], float(np.linalg.norm(dY[sp])))
            sup["S_m"] = max(sup["S_m"], float(np.linalg.norm(M_["Y"][sp])))
            sup["Os"] = max(sup["Os"], float(np.linalg.norm(M_["O"][sp])))
        ndO = np.linalg.norm(dO[1:d], axis=1)
        sup["OD"] = max(sup["OD"], float(ndO.max()))
        for O_ in (P_["O"], M_["O"]):
            sup["Oh"] = max(sup["Oh"], float(np.linalg.norm(O_[1:d], axis=1)[mask].max()))
        rows = np.nonzero(ndO > 1e-12 * max(1.0, sup["OD"]))[0] + 1
        if len(rows):
            dO_rows_minmax = [min(dO_rows_minmax[0], int(rows.min())), max(dO_rows_minmax[1], int(rows.max()))]
            dO_rows_bad += int(((rows < d - 10) | (rows > d - 1)).sum())
        # gate budgets
        dg = P_["gm"] - M_["gm"]
        cst["mu"] = max(cst["mu"], float(np.abs(dg[1:]).sum())); cst["w"] = max(cst["w"], float(np.linalg.norm(dg[1:])))
        for R_ in (P_, M_):
            cst["Sigma"] = max(cst["Sigma"], float(np.abs(R_["delta"]).sum()))
        if t >= 2:
            cst["g1max"] = max(cst["g1max"], float(P_["gm"][1]), float(M_["gm"][1]))
        # rows j whose source carries an own difference at t-1
        srcO = np.zeros(k, bool); srcO[1:d] = np.linalg.norm(dO_prev[0:d - 1], axis=1) > 1e-12 * max(1.0, sup["OD"])   # j <- j-1 (float-level noise excluded, as in X3)
        srcO[1] = False                                                                          # j = 1 reads row 0
        cst["nuN"] = max(cst["nuN"], float(np.abs(P_["delta"])[srcO[1:]].sum()))
        # per-diagonal sums on cycle rows 1..d-1 (id = t - i)
        ids = t - np.arange(1, d) + off
        Dsum[0, ids] += np.abs(P_["delta"][:d - 1]); Dsum[1, ids] += np.abs(M_["delta"][:d - 1])
        Lam[ids] = a * P_["gm"][1:d] * Lam[ids] + 1.0
        mud[ids] += np.abs(dg[1:d])
        # exact unrolled spike decomposition, t in [Ts, T]
        if t >= Ts:
            i_t = sp
            tr = a * (1 - gam * s2 / k)
            for nm in acc:
                acc[nm] *= tr
            if t == Ts:
                acc["init"] = tr * (P_["Yp"][6] - M_["Yp"][6])
            kp = (gam * a / sk) * (s2 - gam * P_["delta"].sum() / k)
            km = (gam * a / sk) * (s2 - gam * M_["delta"].sum() / k)
            dYp = P_["Yp"] - M_["Yp"]
            if (t - 1) in arrivals:
                acc["main"] += kp * dO_prev[d - 1]
                acc["arrbus"] += kp * (dYp[d - 1] - dO_prev[d - 1])
            else:
                acc["nonarr"] += kp * dYp[d - 1]
            acc["kappa"] += (kp - km) * M_["Yp"][d - 1]
            dVp = P_["Vp"] - M_["Vp"]
            dd = P_["delta"] - M_["delta"]
            m = np.ones(k - 1, bool); m[i_t - 1] = False
            acc["leak"] += -(gam * a / k) * ((P_["delta"][m]) @ dVp[1:][m] + dd[m] @ M_["Vp"][1:][m])
            gv = dg.copy(); gv[0] = 0.0
            acc["winj"] += -(gam / k) * P_["c"] * gv
        dO_prev = dO
    dYT = st[1]["Y"][d - 1] - st[-1]["Y"][d - 1]
    recon = sum(acc.values())
    nondiag = np.ones(nd, bool); nondiag[spike_diag] = False
    cst["Dbar"] = float(Dsum[:, nondiag].max()); cst["Lambda"] = float(Lam[nondiag].max())
    cst["mu_d"] = float(mud[nondiag].max())
    # column set C = {d-1-j : 10 <= j <= ell-1}
    C = np.array([d - 1 - j for j in range(10, ell)], int)
    err_C = float(np.linalg.norm((dYT - acc["main"])[C]))
    main_C = float(np.linalg.norm(acc["main"][C]))
    # inequalities of Lemma E with measured quantities (unscaled form, see PROOF.md Lemma E, (E1)-(E6))
    z, B0, Sx, A, zm, B0m, Sm, Am = (sup[x] for x in ("zeta", "B0", "S", "A", "zeta_m", "B0_m", "S_m", "A_m"))
    OD, Oh = sup["OD"], sup["Oh"]
    Sg, Db, Lm, nuN, mu, mu_d, wv, g1, s2b = (cst[x] for x in ("Sigma", "Dbar", "Lambda", "nuN", "mu", "mu_d", "w", "g1max", "s2max"))
    ns = d - 7
    leak_d = B0 + Sg * z + nuN * OD + mu * (Oh + zm) + wv
    rhs = {
        "zeta": g1 * B0 + gam * q * (Db + gam * Sg * Lm / k) * A + gam * q * (mu_d + gam * mu * Lm / k) * Am
                + (gam * Lm / k) * (B0 + s2b * Sx + Sg * z + nuN * OD + mu * (Oh + zm) + wv) + mu_d * zm,
        "B0": A + q * (B0 + s2b * Sx + Sg * z + nuN * OD + mu * (Oh + zm)) + gam * q * q * (Sg * A + mu * Am) + q * wv,
        "S": z + ns * (gam * q * (s2b + gam * Sg / k) * A + gam ** 2 * mu * q ** 3 * Am + (gam / k) * leak_d),
        "zeta_m": g1 * B0m + gam * q * (Db + gam * Sg * Lm / k) * Am + (gam * Lm / k) * (B0m + s2b * Sm + Sg * (Oh + zm)) + gam * Lm * q,
        "B0_m": Am + q * (B0m + s2b * Sm + Sg * (Oh + zm)) + gam * q * q * Sg * Am + 1.0,
        "S_m": sup["Os"] + zm + ns * (gam * q * (s2b + gam * Sg / k) * Am + (gam / k) * (B0m + Sg * (Oh + zm)) + gam * q),
        "E_Y": z + ns * gam * q * (s2b + gam * Sg / k) * z + ns * gam ** 2 * mu * q ** 3 * Am + ns * (gam / k) * leak_d,
    }
    lhs = {"zeta": z, "B0": B0, "S": Sx, "zeta_m": zm, "B0_m": B0m, "S_m": Sm, "E_Y": err_C}
    terms = {nm: float(np.linalg.norm(v)) for nm, v in acc.items()}
    return {"n": n, "ell": ell, "T": T, "sqrt_k": sk,
            "X1_lemma12_rel_residual": res["X1"], "X2_broadcast_identity_rel_residual": res["X2"],
            "X3_dO_rows_range": dO_rows_minmax, "X3_dO_rows_outside_d-10..d-1": dO_rows_bad,
            "X4_unrolled_spike_rel_residual": float(np.abs(recon - dYT).max() / np.abs(dYT).max()),
            "spike_terms_norm": terms, "main_on_C": main_C, "error_on_C": err_C,
            "sups": sup, "small_n_constants": cst,
            "inequalities": {x: {"lhs": lhs[x], "rhs": rhs[x], "holds": bool(lhs[x] <= rhs[x])} for x in lhs}}


def dc_O_mat(X, k, d, gam):
    Y = np.empty_like(X); Y[0] = X[0]
    sp = X[1:].sum(0); J = gam * X[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    Y[1] = 0.0; Y[2:d] = X[1:d - 1]; Y[d:] = X[d:]
    Y[1:] += J; Y[1] += gam * sp / math.sqrt(k)
    return Y


if __name__ == "__main__":
    out = []
    for spc in sys.argv[1:] or ["512", "1024", "2048", "2048:32"]:
        n = int(spc.split(":")[0]); ell = int(spc.split(":")[1]) if ":" in spc else None
        r = run(n, ell); print(json.dumps(r), flush=True); out.append(r)
    with open(os.path.join(HERE, "exp_error_bounds_result.json"), "w") as f:
        json.dump(out, f, indent=1)
