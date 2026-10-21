"""S under R = alpha (R0 + eta 1 1^T/n) at n = 16384, 65536 via the exact field identity (NUMERICAL).

The explicit-matrix runs (exp_dense_S.py) are limited to n <= 2048, where the bath is outside (H).
Here R h = alpha R0 h + (alpha eta/n)(1^T h) 1 (PR #29 Lemma D2, checked explicitly in exp_dense_S.py)
lets S run where s_t ~ .045-.049. Beyond the contract eta = 1e-8/n^2 (whose effect is below float
resolution at these n), the STRESS values eta = 1e-6, 1e-3 (alpha = 1 - 2 eta) are run to test that the
structural facts hold for every eta and that the credit perturbation obeys its bound.
Per history, at every t (hooks): Lemma 2.3D/5.0D facts
  sp_t - (k-4) s_t >= 0; pre_1(t) >= a'(gamma/sqrt k)(1 - gamma/sqrt k)(k-4) s_(t-1) + .05 - eta (t >= 2);
  g_1(t) <= eps_g(n) = 4.009 exp(-.05 sqrt(n/2)) (t >= 2); free cycle rows >= s_t;
  off-cycle rows outside the active pair == s_t; h_1(1) = s_1.
Across the two histories: actual support, max |x|, endpoint; credit ||B - B'|| per memory column versus
T ||R - R0|| c_* n; actual readout nu_R^T Delta B versus R0-skeleton a HI sqrt(k) Delta Z'_T(d-1).
Run: python -I exp_dense_large.py n H D eta [eta ...]   (appends to exp_dense_large_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dense_tools as T

HI = 1 / math.cosh(.25) ** 2


def run(n, H, D, eta, th):
    k, d = n // 2, n // 4; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    alpha = 1 - 2 * eta; ap = alpha * a
    S = T.schedule_S(n, D, H); Tt = S["T"]; Ts = S["Ts"]
    eps_g = 4.009 * math.exp(-.05 * math.sqrt(k))
    mem = [p[0] for p in S["pairs"]]; prow = set(S["pulse_rows"])
    res = {}
    for sgn in (1, -1):
        st = {"S1": 1e9, "S3": 1e9, "S4": 1e9, "S2a": 1e9, "S2b": 0.0, "h11": None, "sprev": None, "bath_min": 1, "bath_max": 0}
        z = sgn * th

        def hook(t, hprev, pre, hn, x, s_t, st=st, z=z):
            sp = float(hn[1:k].sum())
            if t >= 1:
                st["S1"] = min(st["S1"], sp - (k - 4) * s_t)
                st["bath_min"] = min(st["bath_min"], s_t); st["bath_max"] = max(st["bath_max"], s_t)
            if t >= 2:
                bound = ap * (gam / math.sqrt(k)) * (1 - gam / math.sqrt(k)) * (k - 4) * st["sprev"] + .05 - eta
                st["S3"] = min(st["S3"], float(pre[1]) - bound)
                st["S4"] = min(st["S4"], eps_g - float(1 - hn[1] ** 2))
            else:
                st["h11"] = (float(hn[1]), s_t)
            spike = d - 1 - (Tt - t) if t >= Ts else None
            cyc = np.arange(1, d)
            if spike is not None:
                cyc = cyc[cyc != spike]
            st["S2a"] = min(st["S2a"], float((hn[cyc] - s_t).min()))
            tg = S["targets"](t, z)
            act = [r for r in prow if r in tg and tg[r][0] == "set"]
            off = np.ones(k - d, bool)
            for r in act:
                off[r - d] = False
            st["S2b"] = max(st["S2b"], float(np.abs(hn[d:k][off] - s_t).max()))
            st["sprev"] = s_t
        r = T.simulate(None, n, S, z, mem, field=(alpha, eta), hook=hook)
        res[sgn] = (r, st)
    (P, sp), (M, sm) = res[1], res[-1]
    dB = P["B"] - M["B"]; dBp = P["Bp"] - M["Bp"]
    # nu_R = R^T (HI 1) = alpha R0^T (HI 1) + alpha eta HI 1  (R^T = alpha R0^T + (alpha eta/n) 1 1^T)
    w = -np.ones(k) / math.sqrt(k); w[0] += 1
    OT1 = np.zeros(k); OT1[d - 1] = math.sqrt(k); OT1 += gam * w           # O^T 1_k
    nu0 = np.concatenate([a * HI * OT1, lam * HI * np.ones(n - k)])
    nuR = alpha * nu0 + alpha * eta * HI
    r_act = nuR @ dB; r_ref = nu0 @ dBp
    dcol = float(max(np.linalg.norm(P["B"] - P["Bp"], axis=0).max(), np.linalg.norm(M["B"] - M["Bp"], axis=0).max()))
    eR = (1 - alpha) * a + alpha * eta
    rec = {"n": n, "H": H, "D": D, "eta": eta, "theta": np.round(th, 4).tolist(),
           "support max": max(max(P["support"]), max(M["support"])), "max|x|": max(P["maxx"], M["maxx"]),
           "endpoint max|Dh_T|": float(np.abs(P["h"] - M["h"]).max()),
           "S1 min(sp-(k-4)s)": min(sp["S1"], sm["S1"]), "S3 min(pre_1 - bound)": min(sp["S3"], sm["S3"]),
           "S4 min(eps_g - g_1)": min(sp["S4"], sm["S4"]), "eps_g": eps_g,
           "S2 min(free cycle - s)": min(sp["S2a"], sm["S2a"]), "S2 max|off-cycle inactive - s|": max(sp["S2b"], sm["S2b"]),
           "S5 h_1(1) == s_1": bool(sp["h11"][0] == sp["h11"][1]),
           "bath range": [min(sp["bath_min"], sm["bath_min"]), max(sp["bath_max"], sm["bath_max"])],
           "credit max||B-B'|| per col": dcol, "bound T||R-R0|| c n": Tt * eR * (1 + 1e-12) * n,
           "readout actual ||nu_R^T dB||": float(np.linalg.norm(r_act)), "readout R0-skeleton": float(np.linalg.norm(r_ref)),
           "max rel diff": float(np.abs(r_act / r_ref - 1).max())}
    rec["pass"] = bool(rec["support max"] <= 3 and rec["max|x|"] < .5 and rec["endpoint max|Dh_T|"] < 1e-12
                       and rec["S1 min(sp-(k-4)s)"] >= -1e-9 and rec["S3 min(pre_1 - bound)"] >= -1e-9
                       and (rec["bath range"][0] < .025 or rec["S4 min(eps_g - g_1)"] >= 0)
                       and rec["S2 min(free cycle - s)"] >= -1e-12 and rec["S2 max|off-cycle inactive - s|"] <= 1e-12
                       and rec["S5 h_1(1) == s_1"] and dcol <= rec["bound T||R-R0|| c n"])
    return rec


def main():
    n, H, D = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    etas = [float(x) for x in sys.argv[4:]] or [1e-8 / n ** 2]
    rng = np.random.default_rng(11); th = rng.normal(size=D); th /= np.linalg.norm(th)
    fn = os.path.join(HERE, "exp_dense_large_result.json")
    for eta in etas:
        rec = run(n, H, D, eta, th)
        print(json.dumps(rec), flush=True)
        old = json.load(open(fn)) if os.path.exists(fn) else []
        old = [o for o in old if not (o["n"] == n and o["eta"] == eta)]
        json.dump(old + [rec], open(fn, "w"), indent=1)


if __name__ == "__main__":
    main()
