"""Identity checks for the complete readout ledger (PROOF.md sections 1-3), small n, full matrices.

Two R0 forward histories (a "+" and a "-" history, sharing a random public sparse schedule and
differing in the amplitudes of a few drives) give the R0-skeleton credit B', Y = U B', the own part O
(local skeleton, U-row indexing) and Z = Y - O. Checked:
  (C1) the nine-term decomposition (PR #31 (4.1)) holds for EVERY spike U-row d-f, f = 1..F_max,
       along its own path p_t = d-f-(T-t) (Theorem M_F uses this); the arrival stream is row d-1's;
  (C2) F-step legal queries (random future gates in [LO, HI], F = 1..F_max): chi = U nu with
       nu = (aO)^T G1 ... (aO)^T GF 1; the readout identity
       nu^T Delta(B' - O) = sum_(f<=F) chi(d-f) Delta Z(d-f) + sum_(other) chi(i) Delta Z(i) + (chi-nu)^T Delta O,
       and the Lemma 1.2' weight facts used by Theorem M_F: ||chi||_2 <= HI^F sqrt(k), the
       non-spike maximum of |chi_i|, |w^T chi|;
  (C3) Lemma D (common-mode damping), exact: for a homogeneous hole set H (off-cycle rows held at
       state 0, so g = 1), sum_H Y_t = (1 - gamma |H| delta_H/k) sum_H V_t + (sum_H kappa_t) V_t(0)
       - (gamma |H|/k) sum_(j not in H) delta_t(j) V_t(j) + injection.
Finite-precision evidence that the identities have no missing term. Not a proof.
Run: python -I ledger_check.py   (writes ledger_check_result.json)
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def O_matrix(k, d, gam):
    return O_apply(np.eye(k), k, d, gam)


def make_schedule(n, T, m, seed):
    rng = np.random.default_rng(seed)
    k, d = n // 2, n // 4
    sched = {}
    holes_diag = set(rng.choice(np.arange(-d, T), size=min(T, 4 * m), replace=False).tolist())
    H_off = rng.choice(np.arange(d, k), size=6, replace=False)       # homogeneous off-cycle hole set
    for t in range(1, T + 1):
        drv = {}
        for r in rng.choice(np.arange(1, k), size=max(1, m // 4), replace=False):
            if int(r) not in H_off:
                drv[int(r)] = ("code", float(rng.uniform(-.9, .9)))
        if T // 4 <= t <= 3 * T // 4:
            for r in H_off:
                drv[int(r)] = ("hole", 0.0)
        for r in range(3, d):
            if (t - r) in holes_diag:
                drv[r] = ("hole", 0.0)
        for f in range(1, 4):                                         # spikes on rows d-1, d-2, d-3
            r = d - f - (T - t)
            if 7 <= r <= d - 1 and rng.random() < .95:
                drv[r] = ("hole", 0.0)
        sched[t] = dict(list(drv.items())[:m])
    return sched, [int(r) for r in H_off]


def run_history(n, T, sched, sign, F_max, H_off):
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k)
    a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / sk)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / sk; w[0] += 1
    idx = np.arange(1, k)
    h = np.zeros(n)
    B = np.zeros((k, k)); Y = np.zeros((k, k)); O = np.zeros((k, k))
    names = ("K_pos", "K_neg", "K_uni", "K_bus", "L_cyc", "L_off", "L_bus", "W", "F_ent")
    acc = {f: {nm: np.zeros(k) for nm in names} for f in range(1, F_max + 1)}
    lemD = 0.0; lemD_scale = 0.0; Hset = np.array(H_off)
    s = 0.0
    for t in range(1, T + 1):
        hm = h[:k]
        Jt = gam * hm[d - 1] / sk - gam ** 2 * hm[1:].sum() / k
        s_new = math.tanh(.05 + a * Jt + a * s)               # bath of a never-driven off-cycle row
        pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        for r, (kind, v) in sched[t].items():
            hn[r] = v if kind == "hole" else sign * v
        s = s_new; ghat = 1 - s * s
        g = 1 - hn ** 2; gm = g[:k]
        c = h[k:].sum() / (sig * l)
        delta = gm - ghat; delta[0] = 0.0
        St = float(delta[1:].sum())
        Bn = a * O_apply(B, k, d, gam); Bn[idx, idx] += c; Bn *= gm[:, None]
        Yn = Bn + (gam / sk) * (w @ Bn)[None, :]; Yn[0] = Bn.sum(0) / sk
        On = np.zeros((k, k)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[idx, idx] += c * gm[1:]
        Zp = Y - O; Zp[0] = Y[0]
        # V_t = a P Y_(t-1): V(0) = a Y(d-1), V(r) = a Y(r-1) on the cycle (r >= 1), V(j) = a Y(j) off-cycle
        V = np.empty((k, k)); V[0] = a * Y[d - 1]; V[1:d] = a * Y[0:d - 1]; V[d:] = a * Y[d:]
        Vo = np.zeros((k, k)); Vo[2:d] = a * O[1:d - 1]; Vo[d:] = a * O[d:]; Vo[0] = a * O[d - 1]
        Vz = V - Vo                                            # bus part of V (Vz(1) = a Y(0))
        kap = (gam / sk) * (delta - gam * St / k)
        gv = gm.copy(); gv[0] = 0.0
        for f in range(1, F_max + 1):
            tf = max(1, T - d + f + 1)
            if t < tf:
                continue
            p = d - f - (T - t)
            A = acc[f]
            for nm in A:
                A[nm] *= a * gm[p]
            dp = delta[p]
            A["K_pos"] += (gam / sk) * max(dp, 0.0) * Vo[0]
            A["K_neg"] += -(gam / sk) * max(-dp, 0.0) * Vo[0]
            A["K_uni"] += -(gam ** 2 / k ** 1.5) * St * Vo[0]
            A["K_bus"] += kap[p] * Vz[0]
            dc = delta.copy(); dc[d:] = 0.0; dc[0] = 0.0
            do = delta.copy(); do[:d] = 0.0
            A["L_cyc"] += -(gam / k) * (dc @ Vo)
            A["L_off"] += -(gam / k) * (do @ Vo)
            A["L_bus"] += -(gam / k) * (delta @ Vz)
            gv = gm.copy(); gv[0] = 0.0
            A["W"] += -(gam / k) * c * gv
            if t == tf and p == 1:
                A["F_ent"] += gm[1] * Vz[1]
        # Lemma D on the homogeneous hole set (all held at 0 at this step and the previous one)
        if all(sched[t].get(int(r), ("", 1.0))[1] == 0.0 for r in Hset) and np.all(gm[Hset] == 1.0):
            dH = 1.0 - ghat
            lhs = Yn[Hset].sum(0)
            others = np.setdiff1d(np.arange(1, k), Hset)
            inj = np.zeros(k); inj[Hset] += c * gm[Hset]; inj -= len(Hset) * (gam / k) * c * gv
            rhs = (1 - gam * len(Hset) * dH / k) * V[Hset].sum(0) + kap[Hset].sum() * V[0] \
                - (gam * len(Hset) / k) * (delta[others] @ V[others]) + inj
            lemD = max(lemD, float(np.abs(lhs - rhs).max())); lemD_scale = max(lemD_scale, float(np.abs(lhs).max()))
        h = hn; B = Bn; Y = Yn; O = On
    Z = Y - O; Z[0] = Y[0]
    return {"B": B, "Y": Y, "O": O, "Z": Z, "acc": acc, "lemD": lemD, "lemD_scale": lemD_scale}


def main():
    out = {"runs": []}
    for (n, T, m, seed) in ((512, 300, 24, 1), (512, 420, 40, 2), (1024, 600, 48, 3)):
        k, d = n // 2, n // 4; sk = math.sqrt(k); a = 1 - 1 / n; gam = 1 / (1 - 1 / sk)
        F_max = 6
        sched, H_off = make_schedule(n, T, m, seed)
        hp = run_history(n, T, sched, +1, F_max, H_off)
        hm = run_history(n, T, sched, -1, F_max, H_off)
        row = {"n": n, "T": T, "m": m, "seed": seed}
        # (C1) nine-term reconstruction for every spike row, both histories
        c1 = 0.0
        for H in (hp, hm):
            for f in range(1, F_max + 1):
                rec = sum(H["acc"][f].values())
                ZT = H["Z"][d - f]
                c1 = max(c1, float(np.abs(rec - ZT).max()) / max(1e-300, float(np.abs(ZT).max())))
        row["C1 nine-term relative residual (max over rows d-1..d-6)"] = c1
        # (C2) F-step queries
        rng = np.random.default_rng(100 + seed)
        Om = O_matrix(k, d, gam)
        w = -np.ones(k) / sk; w[0] += 1
        U = np.eye(k) - gam * np.outer(w, w)
        dB = (hp["B"] - hp["O"]) - (hm["B"] - hm["O"])
        dZ = hp["Z"] - hm["Z"]; dO = hp["O"] - hm["O"]
        worst = {"identity": 0.0, "norm_ratio": 0.0, "nonspike_max": 0.0, "wchi_max": 0.0}
        for F in range(1, F_max + 1):
            for rep in range(8):
                gs = [rng.uniform(LO, HI, k) for _ in range(F)]
                if rep % 4 == 1:
                    gs = [np.where(rng.random(k) < .5, LO, HI) for _ in range(F)]
                if rep % 4 == 2:
                    gs = [np.full(k, HI) for _ in range(F)]
                nu = np.ones(k)
                for gg in reversed(gs):
                    nu = a * Om.T @ (gg * nu)
                chi = U @ nu
                spikes = [d - f for f in range(1, F + 1)]
                others = [i for i in range(k) if i not in spikes]
                lhs = nu @ dB
                rhs = sum(chi[i] * dZ[i] for i in spikes) + chi[others] @ dZ[others] + (chi - nu) @ dO
                worst["identity"] = max(worst["identity"], float(np.abs(lhs - rhs).max()) / max(1e-300, float(np.abs(lhs).max())))
                worst["lhs_max"] = max(worst.get("lhs_max", 0.0), float(np.abs(lhs).max()))
                worst["norm_ratio"] = max(worst["norm_ratio"], float(np.linalg.norm(chi)) / (HI ** F * sk))
                worst["nonspike_max"] = max(worst["nonspike_max"], float(np.abs(chi[others]).max()))
                worst["wchi_max"] = max(worst["wchi_max"], abs(float(w @ chi)))
        row["C2 F-step identity relative residual"] = worst["identity"]
        row["C2 max |nu^T Delta bus| (nonzero: the histories differ)"] = worst["lhs_max"]
        row["C2 max ||chi||_2 / (HI^F sqrt k)  (must be <= 1)"] = worst["norm_ratio"]
        row["C2 max non-spike |chi_i|  (Lemma 1.2' asymptotic 1.159 + O(1/sqrt k))"] = worst["nonspike_max"]
        row["C2 max |w^T chi|  (proof uses <= A_1 + 1)"] = worst["wchi_max"]
        row["C3 Lemma D max abs residual"] = max(hp["lemD"], hm["lemD"])
        row["C3 Lemma D max abs hole-sum"] = max(hp["lemD_scale"], hm["lemD_scale"])
        out["runs"].append(row); print(json.dumps(row))
    json.dump(out, open(os.path.join(HERE, "ledger_check_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
