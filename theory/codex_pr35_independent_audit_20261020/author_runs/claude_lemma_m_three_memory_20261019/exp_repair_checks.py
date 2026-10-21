"""Exact-recurrence tests of the repaired ingredients (PROOF.md section 5R). NUMERICAL, not a proof.

Construction S of exp_S_check.py (A = .38, spike from row 19, parking), two antipodal histories.
State-level checks (all t, all rows):
  S1  sp_t := sum_(l>=1) h_t(l) >= (k-4) s_t                         (Lemma 5.0R, step 1)
  S2  h_t(d-1) >= 0; undriven cycle rows >= s_t; never-held/parked off-cycle rows == s_t
  S3  pre_1(t+1) >= a (gamma/sqrt k)(1 - gamma/sqrt k)(k-4) s_t + .05  and  g_1 <= 4 e^(-2 pre_1)
  S4  g_1(t) <= eps_g(n) = 4.009 exp(-.05 sqrt(n/2)) for t >= 2 (needs s_t >= .025, recorded)
  S5  t = 1: h_1(1) = s_1, so delta_1(1) = 0 (the row-1 gate exception carries no credit)
  S6  front deviation mass per time <= D_f = 39.73; active-pair |delta| <= .1316
Credit-level checks for one memory column c (both histories):
  C1  recursion (5.1) and broadcast identity (5.2) residuals
  C2  births: max_t |g_t(1) a Y_(t-1)(0)| <= eps_g(n) sup|Y(0)| (t >= 2), and = 0 at t = 1
  C3  Lemma 5.1R(a) with measured inputs: A_max <= kappa_c A_max + Q lhat + eps_g Y0max
  C4  Lemma 5.2R(i):  Acal (1 - kappa_A - eps_g u1) <= (Q + eps_g sqrt k)(Lambda + sigma_S)
  C5  Lemma 5.2R(iv): |Delta SO(c)| <= kappa_s Acal + Lambda2 + sigma_S, and Delta SO = exact second-order part
Run: python -I exp_repair_checks.py n H D [state_only]
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp_S_check as SC
from m3sim import O_apply

Q, DF, DB = 1600.0, 39.73, 40.01


def run(n, H, D, theta, state_only=False):
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    eps_g = 4.009 * math.exp(-.05 * sk)
    T, Ts, sigs, pairs, fp = SC.schedule(n, D, H, theta)
    _, _, _, _, fm = SC.schedule(n, D, H, -theta)
    pair_rows = set(r for p in pairs for r in p)
    c = pairs[0][0]
    w = -np.ones(k) / sk; w[0] += 1
    hist = {}
    for nm, f in (("p", fp), ("m", fm)):
        hist[nm] = {"h": np.zeros(n), "B": np.zeros(k), "O": np.zeros(k), "Z": np.zeros(k), "o": 0.0}
    rec = {"n": n, "H": H, "D": D, "theta": [round(float(x), 4) for x in theta]}
    S1 = S2a = S2b = S3a = S4 = 1e9; S2c = S3b = 0.0; s_min = 1.0; S6a = S6b = 0.0
    g1_t1 = None; resid51 = resid52 = resid52abs = y0max = 0.0; birth_ratio = 0.0; birth_t1 = 0.0
    seq = {nm: {"lam": [], "A": [], "Y0": [], "S": [], "dc": []} for nm in ("p", "m")}
    Zspike_part = {"SO": 0.0}
    held_cycle = lambda t: (d - 1 - (T - t)) if t >= Ts else None
    for t in range(1, T + 1):
        for nm, f in (("p", fp), ("m", fm)):
            Hh = hist[nm]; h = Hh["h"]; hm = h[:k]
            pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
            hn = np.tanh(pre)
            s_new = float(hn[k - 1])                      # never-driven off-cycle row = bath
            sc = f(t)
            for r, v in sc.items():
                hn[r] = s_new if v is None else v
            gm = 1 - hn[:k] ** 2; ghat = 1 - s_new ** 2
            if nm == "p":
                s_min = min(s_min, s_new) if t >= 1 else s_min
                # S1, S2, S3 at time t (state h = h_t, pre_1 of t is pre[1] computed from h_(t-1))
                sp = float(hn[1:k].sum())
                S1 = min(S1, sp - (k - 4) * s_new)
                S2a = min(S2a, float(hn[d - 1]))
                hc = held_cycle(t)
                cyc = np.arange(1, d); und = cyc[cyc != hc] if hc is not None else cyc
                S2b = min(S2b, float((hn[und] - s_new).min()))
                off = np.arange(d, k)
                act = [r for r in pair_rows if r in sc and sc[r] is not None]
                offm = np.setdiff1d(off, np.array(act, dtype=int)) if act else off
                S2c = max(S2c, float(np.abs(hn[offm] - s_new).max()))
                if t >= 2:
                    s_prev = hist["p"]["s"]
                    sp_prev = hist["p"]["sp"]
                    bound = a * (gam / sk) * (1 - gam / sk) * (k - 4) * s_prev + .05
                    S3a = min(S3a, float(pre[1] - bound))
                    S3b = max(S3b, float(gm[1] - 4 * math.exp(-2 * pre[1])))
                    S4 = min(S4, eps_g - float(gm[1]))
                else:
                    g1_t1 = (float(hn[1]), s_new)
                dl = gm - ghat
                S6a = max(S6a, float(np.abs(dl[und]).sum()))
                if act:
                    S6b = max(S6b, float(np.abs(dl[act]).max()))
                Hh["s"] = s_new; Hh["sp"] = sp
            if state_only:
                Hh["h"] = hn
                continue
            # ---- credit for column c
            cc = float(h[k:].sum() / (sig * l))
            B, O, Zp, o = Hh["B"], Hh["O"], Hh["Z"], Hh["o"]
            delta = gm - ghat; delta[0] = 0.0
            St = float(delta[1:].sum())
            # predecessor contents Z_(t-1)(pi^-1 j)
            pred = np.empty(k); pred[0] = 0.0; pred[1] = Zp[0]; pred[2:d] = Zp[1:d - 1]; pred[d:] = Zp[d:]
            lam_t = (gam * a / k) * (delta[c] * o + float(delta[1:] @ pred[1:])) + (gam / k) * cc * gm[c]
            A_t = a * Zp[d - 1]
            Bn = a * O_apply(B[:, None], k, d, gam)[:, 0]; Bn[c] += cc; Bn *= gm
            On = np.zeros(k); On[2:d] = gm[2:d] * a * O[1:d - 1]; On[d:] = gm[d:] * a * O[d:]; On[c] += cc * gm[c]
            Yn = Bn - gam * w * float(w @ Bn)                       # Y = U B'
            Zn = Yn - On; Zn[0] = Yn[0]
            kap = (gam / sk) * (delta - gam * St / k)
            recur = gm * a * pred + kap * A_t - lam_t
            resid51 = max(resid51, float(np.abs(Zn[1:] - recur[1:]).max()) / max(1e-300, float(np.abs(Zn).max())))
            y0 = (ghat + gam * St / k) * A_t + (sk / gam) * lam_t
            resid52 = max(resid52, abs(float(Yn[0]) - y0) / max(1e-300, abs(float(Yn[0])) + 1e-30))
            resid52abs = max(resid52abs, abs(float(Yn[0]) - y0)); y0max = max(y0max, abs(float(Yn[0])))
            if t >= 2:
                birth_ratio = max(birth_ratio, abs(gm[1] * a * Zp[0]))
            else:
                birth_t1 = abs(gm[1] * a * Zp[0])
            sq = seq[nm]
            sq["lam"].append(lam_t); sq["A"].append(A_t); sq["Y0"].append(float(Yn[0])); sq["S"].append(St)
            sq["dc"].append((float(delta[c]), o, cc, float(gm[c])))
            Hh["B"], Hh["O"], Hh["Z"], Hh["o"] = Bn, On, Zn, float(On[c])
            Hh["h"] = hn
    rec.update({"S1 min(sp - (k-4)s)": S1, "S2 min h(d-1)": S2a, "S2 min(undriven cycle - s)": S2b,
                "S2 max |off-cycle inactive - s|": S2c, "S3 min(pre_1 - bound)": S3a,
                "S3 max(g_1 - 4e^-2pre)": S3b, "S4 min(eps_g - g_1), t>=2": S4, "eps_g(n)": eps_g,
                "bath min (t>=1)": s_min, "S5 (h_1(1), s_1)": g1_t1, "S6 max front mass": S6a,
                "S6 max active-pair |delta|": S6b})
    state_pass = bool(S1 >= -1e-9 and S2a >= 0 and S2b >= -1e-12 and S2c <= 1e-12 and S3a >= -1e-9
                      and S3b <= 1e-15 and (s_min < .025 or S4 >= 0) and g1_t1[0] == g1_t1[1]
                      and S6a <= DF and S6b <= .1316)
    rec["state_pass"] = state_pass
    if state_only:
        return rec
    # ---- credit-level aggregate checks
    lp, lm = np.array(seq["p"]["lam"]), np.array(seq["m"]["lam"])
    Ap, Am = np.array(seq["p"]["A"]), np.array(seq["m"]["A"])
    Y0p = np.array(seq["p"]["Y0"]); Sp, Sm = np.array(seq["p"]["S"]), np.array(seq["m"]["S"])
    lhat = float(np.abs(lp).max()); Amax = float(np.abs(Ap).max()); Y0max = float(np.abs(Y0p).max())
    kc = (gam / sk) * (DF + gam * DB * Q / k)
    kA = (gam / sk) * DB * (1 + gam / 2)
    ks = (gam / sk) * (.1009 ** 2 + gam * DB / k)
    u1 = 1 + gam * DB / k
    # first-order leak lambda1 (own + injection) per history
    def lam1(nm):
        return np.array([(gam * a / k) * dc * o + (gam / k) * cc * gc for (dc, o, cc, gc) in seq[nm]["dc"]])
    l1p, l1m = lam1("p"), lam1("m")
    dl = lp - lm; dl1 = l1p - l1m; dl2 = dl - dl1
    Lam = float(np.abs(dl).sum()); Lam1 = float(np.abs(dl1).sum()); Lam2 = float(np.abs(dl2).sum())
    Acal = float(np.abs(Ap - Am).sum())
    sigS = (gam ** 2 / k ** 1.5) * float((np.abs(Sp - Sm) * np.abs(Am)).sum())
    # exact second-order part on the spike: Delta Z_T(d-1) - Delta F1, Delta F1 = -sum a^(T-t) Delta lambda1_t (t >= Ts)
    ts = np.arange(1, T + 1)
    wts = np.where(ts >= Ts, a ** (T - ts), 0.0)
    dF1 = -float((wts * dl1).sum())
    dZT = float(hist["p"]["Z"][d - 1] - hist["m"]["Z"][d - 1])
    dSO = dZT - dF1
    rec.update({"C1 residual (5.1)": resid51, "C1 residual (5.2)": resid52, "C1 residual (5.2) abs/max|Y0|": resid52abs / max(y0max, 1e-300),
                "C2 max birth |g_1 a Y(0)| (t>=2)": birth_ratio, "C2 eps_g*sup|Y0|": eps_g * Y0max,
                "C2 birth at t=1": birth_t1,
                "C3 lhs A_max": Amax, "C3 rhs kc*Amax+Q*lhat+eps_g*Y0max": kc * Amax + Q * lhat + eps_g * Y0max,
                "C4 lhs": Acal * (1 - kA - eps_g * u1), "C4 rhs": (Q + eps_g * sk) * (Lam + sigS),
                "C5 |dSO|": abs(dSO), "C5 rhs ks*Acal+Lam2+sigS": ks * Acal + Lam2 + sigS,
                "dF1": dF1, "dSO/dF1": dSO / dF1 if dF1 else None, "Lambda1": Lam1, "Lambda2": Lam2})
    rec["all_pass"] = bool(state_pass and resid51 < 1e-8 and birth_t1 == 0.0
                           and birth_ratio <= eps_g * Y0max + 1e-300
                           and Amax <= rec["C3 rhs kc*Amax+Q*lhat+eps_g*Y0max"]
                           and rec["C4 lhs"] <= rec["C4 rhs"] and abs(dSO) <= rec["C5 rhs ks*Acal+Lam2+sigS"] * (1 + 1e-9))
    return rec


def main():
    n = int(sys.argv[1]); H = int(sys.argv[2]); D = int(sys.argv[3])
    state_only = len(sys.argv) > 4 and sys.argv[4] == "state_only"
    rng = np.random.default_rng(9)
    th2 = rng.normal(size=D); th2 /= np.linalg.norm(th2)
    out = []
    for th in (np.eye(D)[0], th2):
        r = run(n, H, D, th, state_only)
        print(json.dumps(r), flush=True); out.append(r)
    fn = os.path.join(HERE, "exp_repair_checks_result.json")
    old = json.load(open(fn)) if os.path.exists(fn) else []
    key = lambda r: (r["n"], r["H"], r["D"], tuple(r["theta"]), "C1 residual (5.1)" in r)
    keep = [r for r in old if key(r) not in {key(x) for x in out}]
    json.dump(keep + out, open(fn, "w"), indent=1)


if __name__ == "__main__":
    main()
