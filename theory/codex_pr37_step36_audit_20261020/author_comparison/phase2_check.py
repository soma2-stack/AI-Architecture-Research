"""Verification of the Step 3.6 heterogeneous-retention results (PROOF.md section 10).
Small-n full-matrix computations of the exact R0-skeleton credit; operator-level gates (arbitrary
gates in (0,1], including anti-holes), not claimed to be legal histories. Checks:
  (P1) exact retainer row recursion  y_t(i) = a g_t(i) y_(t-1)(i) + F_t + kappa_t(i) v_t(0)
       with ONE common forcing F_t for all retainers (Lemma 1.2 on the full Y);
  (P2) Theorem 10.1: y_T(i) = rho_i(t1) y_t1(i) + sum_u lambda_u(i) Psi_u + C_T(i), with
       lambda >= 0, sum_u lambda_u(i) = 1, Psi_u = sum_(v>u) F_v;  |forced| <= max |Psi|;
  (P3) Theorem 7.5' (near-homogeneous gates, E <= 1/4, NONZERO initial vector): the aggregate
       bound (a) and the decomposition bound (b), with every term computed from its definition;
  (P4) Proposition 10.3: stationary response to constant forcing for arbitrary time-invariant
       heterogeneous gates (holes, partial holes, anti-holes): closed form and the ceiling
       |chi^T y*| < A |F_ext| k/(gamma s~^2), s~^2 = 1 - a ghat.
Run: python -I phase2_check.py   (writes phase2_check_result.json)
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def setup(n):
    k, d = n // 2, n // 4; sk = math.sqrt(k); a = 1 - 1 / n; ga = 1 / (1 - 1 / sk); q = ga / sk
    w = -np.ones(k) / sk; w[0] += 1
    U = np.eye(k) - ga * np.outer(w, w)
    perm = np.arange(k); perm[:d] = np.roll(np.arange(d), 1)      # P e_r = e_(r+1) on the cycle
    Pm = np.eye(k)[:, perm]
    Pm = np.zeros((k, k));
    for r in range(k):
        Pm[(r + 1) % d if r < d else r, r] = 1.0
    O = U @ Pm @ U
    return k, d, sk, a, ga, q, w, U, Pm, O


def run(n, T, t1, gate_fn, seed):
    rng = np.random.default_rng(seed)
    k, d, sk, a, ga, q, w, U, Pm, O = setup(n)
    j = d + 3; Hs = np.arange(d + 6, d + 12); P = len(Hs)
    b = np.zeros(k); Ys = []; F = {}; kap = {}; v0 = {}; gates = {}; ghat = {}; G_all = {}
    Ylast = U @ b
    resid = 0.0
    for t in range(1, T + 1):
        g = rng.uniform(.05, 1.0, k)                    # arbitrary gates elsewhere
        g[0] = rng.uniform(.5, 1.0)
        gb = .995 + .004 * math.sin(t / 7)              # nonautonomous bath reference gate
        g[d + 20:] = gb                                 # a never-deviating block (bath rows)
        g[Hs] = gate_fn(t, rng, P)
        g[j] = rng.uniform(.6, 1.0)
        c = 1.0 if t > 1 else 0.0
        e = np.zeros(k); e[j] = c
        bn = g * (a * (O @ b) + e)
        Y = U @ b; Yn = U @ bn
        v = a * (Pm @ Y)
        delta = g - gb; delta[0] = 0.0
        S = float(delta[1:].sum())
        Ft = -(ga / k) * float(delta[1:] @ v[1:]) - (ga / k) * c * g[j]
        kp = q * (delta - ga * S / k)
        pred = a * g[Hs] * Y[Hs] + Ft + kp[Hs] * v[0]
        resid = max(resid, float(np.abs(Yn[Hs] - pred).max()) / max(1e-300, float(np.abs(Yn[Hs]).max())))
        F[t] = Ft; kap[t] = kp[Hs].copy(); v0[t] = float(v[0]); gates[t] = g[Hs].copy(); ghat[t] = gb
        G_all[t] = (g.copy(), delta.copy(), v.copy(), c, Y.copy())
        b = bn
        Ys.append(Yn[Hs].copy())
    return {"resid": resid, "F": F, "kap": kap, "v0": v0, "gates": gates, "ghat": ghat, "Y": Ys, "G": G_all,
            "P": P, "Hs": Hs, "j": j, "a": a, "ga": ga, "q": q, "k": k}


def theorem_10_1(R, t1, T):
    a = R["a"]; Ys = R["Y"]; P = R["P"]
    yT = Ys[T - 1]; y1 = Ys[t1 - 1]
    rho = lambda i, u: float(np.prod([a * R["gates"][v][i] for v in range(u + 1, T + 1)]))
    Psi = {u: sum(R["F"][v] for v in range(u + 1, T + 1)) for u in range(t1, T)}
    worst = 0.0; forced_ratio = 0.0; wsum_err = 0.0; neg = 0.0
    for i in range(P):
        r = {u: rho(i, u) for u in range(t1, T + 1)}
        lam = {t1: r[t1 + 1]}
        for u in range(t1 + 1, T):
            lam[u] = r[u + 1] - r[u]
        neg = min(neg, min(lam.values()))
        wsum_err = max(wsum_err, abs(sum(lam.values()) - 1.0))
        forced = sum(lam[u] * Psi[u] for u in range(t1, T))
        cap = sum(r[u] * R["kap"][u][i] * R["v0"][u] for u in range(t1 + 1, T + 1))
        rec = r[t1] * y1[i] + forced + cap
        worst = max(worst, abs(rec - yT[i]) / max(1e-300, abs(yT[i])))
        forced_ratio = max(forced_ratio, abs(forced) / max(1e-300, max(abs(x) for x in Psi.values())))
    return {"reconstruction rel. residual": worst, "min lambda (>= 0)": neg, "max |sum lambda - 1|": wsum_err,
            "max |forced| / max|Psi| (<= 1)": forced_ratio}


def theorem_75p(R, t1, T, rng):
    """Near-homogeneous gates; nonzero initial vector; all terms from their definitions."""
    a, ga, q, k, P = R["a"], R["ga"], R["q"], R["k"], R["P"]
    Ys = R["Y"]; Hs = R["Hs"]; j = R["j"]
    eta = {t: float(np.max(1 - R["gates"][t])) for t in range(t1 + 1, T + 1)}
    E = sum(eta.values())
    sig = {t: float(Ys[t - 1].sum()) for t in range(t1, T + 1)}
    mu = {t: ga * P * (1 - R["ghat"][t]) / k for t in range(t1 + 1, T + 1)}
    Lam = {t1: 1.0}
    for t in range(t1 + 1, T + 1):
        Lam[t] = Lam[t - 1] * a * (1 - mu[t])
    Mstar = max(abs(sig[t] - Lam[t] * sig[t1]) for t in range(t1, T + 1))
    ysrc_pk = 0.0; neg = 0.0; Re = 0.0; Q = 0.0
    for t in range(t1 + 1, T + 1):
        g, delta, v, c, Yprev = R["G"][t]
        ysrc_pk = max(ysrc_pk, abs(a * Yprev[j]))
        neg += ga * P / k * max(-delta[j], 0.0) * abs(a * Yprev[j])
        others = np.array([l for l in range(1, k) if l not in set(Hs.tolist()) and l != j])
        e_t = float(R["kap"][t].sum() * R["v0"][t]) - ga * P / k * float(delta[others] @ v[others]) - P * (ga / k) * c * g[j]
        Re += abs(e_t)
        Q += q * eta[t] * abs(R["v0"][t])
    Ysrc = ysrc_pk + neg
    y1 = Ys[t1 - 1]; om1 = float(np.ptp(y1)); s1 = sig[t1]
    boundA = 1.494 * (Ysrc + Re + .331 * abs(s1) + 1.284 * E * P * (om1 + Q))
    chi = rng.uniform(-1, 1, P); A = float(np.abs(chi).max())
    yT = Ys[T - 1]; L = T - t1
    chibar = float(chi.sum()) / P; d1 = y1 - y1.mean()
    acq = float(chi @ yT) - (chibar * Lam[T] * s1 + a ** L * float(chi @ d1))
    boundB = A * (1.661 * Mstar + .661 * abs(s1) + .643 * P * om1 + 1.643 * P * Q)
    total = abs(float(chi @ yT)); boundTot = A * (1.661 * (Mstar + abs(s1)) + 1.643 * P * (om1 + Q))
    return {"E": E, "M*/bound(a)": Mstar / boundA, "|Acq|/bound(b)": abs(acq) / boundB,
            "|total|/bound(c)": total / boundTot, "initial sigma": s1, "initial spread": om1}


def prop_10_3(rng, trials=2000):
    worst = 0.0; resid = 0.0; mind = 1.0
    for _ in range(trials):
        n = int(rng.choice([1e4, 1e6, 1e8])); k = n / 2; a = 1 - 1 / n; ga = 1 / (1 - 1 / math.sqrt(k))
        P = int(rng.integers(1, 200)) if rng.random() < .5 else int(rng.integers(1, int(k / ga * .99)))
        P = min(P, 3000)
        ghat = 1 - rng.uniform(.025, .1) ** 2
        kind = rng.random()
        g = rng.uniform(.05, 1.0, P) if kind < .3 else (rng.choice([1.0, ghat, .6], P) if kind < .6 else 1 - rng.uniform(0, .02, P))
        delta = g - ghat
        Am = a * np.diag(g) - (ga * a / k) * np.outer(np.ones(P), delta)
        Fext = 1.0
        ystar = np.linalg.solve(np.eye(P) - Am, np.ones(P) * Fext)
        u = 1 / (1 - a * g); Usum = u.sum(); st2 = 1 - a * ghat
        denom = 1 - ga * P / k + ga * st2 * Usum / k
        mind = min(mind, denom)
        closed = (Fext / denom) * u
        resid = max(resid, float(np.abs(ystar - closed).max() / np.abs(closed).max()))
        chi = rng.uniform(-1, 1, P); A = float(np.abs(chi).max())
        ceiling = A * abs(Fext) * k / (ga * st2)
        worst = max(worst, abs(float(chi @ ystar)) / ceiling)
    return {"closed-form rel. residual": resid, "max |chi^T y*| / ceiling (< 1)": worst, "min denominator (> 0)": mind}


def prop_10_4(R, t1, T):
    """Convex-averaging recursion of the cumulative common forcing Phi for a positive-deviation
    population (delta_v(l) >= 0 on Hs); verifies the identity term by term and the sup bound."""
    a, ga, k, P = R["a"], R["ga"], R["k"], R["P"]; Hs = R["Hs"]; j = R["j"]; Ys = R["Y"]
    Phi = {t1: 0.0}
    for v in range(t1 + 1, T + 1):
        Phi[v] = Phi[v - 1] + R["F"][v]
    resid = 0.0; theta_max = 0.0; sup_budget = 0.0; supPhi = 0.0
    hs = set(Hs.tolist())
    for v in range(t1 + 2, T + 1):
        g, delta, vv, c, Yprev = R["G"][v]
        dH = delta[Hs]
        assert (dH >= -1e-15).all()
        theta = ga * a / k * float(dH.sum()); theta_max = max(theta_max, theta)
        out = np.array([l for l in range(1, k) if l not in hs])
        Fext = -(ga / k) * float(delta[out] @ vv[out]) - (ga / k) * c * g[j]
        # representation of y_(v-1)(l) at end time v-1
        avg = 0.0; Iv = 0.0
        for idx in range(P):
            rho = lambda u: float(np.prod([a * R["gates"][w][idx] for w in range(u + 1, v)]))   # end time v-1
            r = {u: rho(u) for u in range(t1, v)}
            lam = {t1: r[t1 + 1]}
            for u in range(t1 + 1, v - 1):
                lam[u] = r[u + 1] - r[u]
            Phibar = sum(lam[u] * Phi[u] for u in lam)
            cap = sum(r[u] * R["kap"][u][idx] * R["v0"][u] for u in range(t1 + 1, v))
            init = r[t1] * Ys[t1 - 1][idx]
            avg += dH[idx] * Phibar
            Iv += -(ga * a / k) * dH[idx] * (init + cap)
        rhs = (1 - theta) * Phi[v - 1] + (ga * a / k) * avg + Fext + Iv
        resid = max(resid, abs(rhs - Phi[v]) / max(1e-300, abs(Phi[v])))
        sup_budget += abs(Fext) + abs(Iv)
        supPhi = max(supPhi, abs(Phi[v]))
    return {"identity rel. residual": resid, "max theta (< 1)": theta_max,
            "max|Phi| / sum(|F_ext| + |I|) (<= 1)": supPhi / max(1e-300, sup_budget + abs(R["F"][t1 + 1]))}


def main():
    out = {}
    rng = np.random.default_rng(20261020)
    for (n, T, t1, kind) in ((128, 70, 25, "anti"), (256, 90, 30, "anti"), (256, 90, 30, "mixed")):
        if kind == "anti":
            gf = lambda t, r, P: r.uniform(.05, 1.0, P)                   # strongly heterogeneous, anti-holes
        else:
            gf = lambda t, r, P: np.where(np.arange(P) % 2 == 0, 1.0, r.uniform(.3, .995, P))
        R = run(n, T, t1, gf, seed=7 + n)
        res = theorem_10_1(R, t1, T); res["row recursion rel. residual (P1)"] = R["resid"]
        out[f"P1-P2 n={n} {kind}"] = res; print(json.dumps({f"P1-P2 n={n} {kind}": res}))
        assert R["resid"] < 1e-10 and res["reconstruction rel. residual"] < 1e-9 and res["min lambda (>= 0)"] >= 0
        assert res["max |sum lambda - 1|"] < 1e-12 and res["max |forced| / max|Psi| (<= 1)"] <= 1 + 1e-12
    worst = {"M*/bound(a)": 0, "|Acq|/bound(b)": 0, "|total|/bound(c)": 0}
    for trial in range(12):
        n = 256 if trial % 2 else 128; T = 80; t1 = 30
        def gf(t, r, P, t1=t1, T=T):
            if t <= t1:
                return r.uniform(.05, 1.0, P)           # arbitrary history before t1: nonzero, spread initial vector
            return 1 - r.uniform(0, 1, P) * (.25 / (T - t1))
        R = run(n, T, t1, gf, seed=100 + trial)
        r75 = theorem_75p(R, t1, T, rng)
        assert r75["E"] <= .25 + 1e-12
        for kk in worst:
            worst[kk] = max(worst[kk], r75[kk])
    out["P3 Theorem 7.5' worst ratios (all must be <= 1)"] = worst; print(json.dumps(worst))
    assert all(v <= 1 for v in worst.values())
    worst4 = {"identity rel. residual": 0.0, "max theta (< 1)": 0.0, "max|Phi| / sum(|F_ext| + |I|) (<= 1)": 0.0}
    for trial in range(6):
        n = 128 if trial % 2 else 256
        gb_ref = lambda t: .995 + .004 * math.sin(t / 7)
        gf = (lambda t, r, P, gb_ref=gb_ref: gb_ref(t) + r.uniform(0, 1, P) * (1 - gb_ref(t)))   # gates in [ghat, 1]
        R = run(n, 60, 20, gf, seed=300 + trial)
        r4 = prop_10_4(R, 20, 60)
        for kk in worst4:
            worst4[kk] = max(worst4[kk], r4[kk])
    out["P5 Proposition 10.4 (positive deviations)"] = worst4; print(json.dumps(worst4))
    assert worst4["identity rel. residual"] < 1e-8 and worst4["max theta (< 1)"] < 1 and worst4["max|Phi| / sum(|F_ext| + |I|) (<= 1)"] <= 1 + 1e-12
    p4 = prop_10_3(rng); out["P4 Proposition 10.3"] = p4; print(json.dumps(p4))
    assert p4["closed-form rel. residual"] < 1e-8 and p4["max |chi^T y*| / ceiling (< 1)"] < 1 and p4["min denominator (> 0)"] > 0
    json.dump(out, open(os.path.join(HERE, "phase2_check_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
