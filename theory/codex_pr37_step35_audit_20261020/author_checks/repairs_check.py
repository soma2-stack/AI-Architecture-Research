"""Reproducible checks for the PR #37 repairs (PROOF.md section R, after Codex's audit of ac759bb).

(A) Cor. R2 comparison: a legal, exact-common-endpoint, two-history example at n = 1e8 (m = 2, T = 3)
    with S_j = 0 in both histories, but a nonzero readout of the source-specific creation
    q delta_t(j)(a o_(t-1) + c_t) w. Derived here independently by a class reduction (rows 0, 1, 2,
    and the bulk), evaluated with 60-digit mpmath; the class formula is cross-checked against a
    full-vector float64 simulation of the same three-step history at n = 4096 and 16384.
(B) Cor. D3: the forcing-acquired part must subtract the DAMPED baseline. Exact rational diagnostic
    (pure-forcing scalar recurrence, a = 1 - 1e-8, mu = 1e-8, sigma_0 = 10, 10 steps).
(C) Theorem M_F: F_s is a ceiling, so n/F_s is not monotone (exact jump 182 -> 183 at
    n = 11785591396 -> 11785591400); the continuous envelope f(n) = 1 + ln(1.01 sqrt(n/2))/r_H gives
    n/F_s >= n/f(n) >= 1e10/f(1e10) for n >= 1e10, since f(n) > 1/(2 r_H).
(D) Lemma 1.3: the exact coefficient (2.18 g/sqrt k)(23/(64*1.2) + 1/(8 HI)) at n = 1e8.
(E) Lemma R constants for all sizes, with S4's bound g_1 <= 4 exp(-.0297 sqrt k + .92):
    one-step HI(1 + sqrt2 gamma + sqrt(k) g_1), F-step 1 + HI(sqrt2 gamma + sqrt(k) g_1), and the
    terminal F-step case |chi^T w| <= A_1 + 1 = 2.18.
Run: python -I repairs_check.py   (writes repairs_check_result.json)
"""
import json, math, os
from fractions import Fraction as Q
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
mp.mp.dps = 60


# ---------------------------------------------------------------- (A) class reduction
def class_example(n, prec=True):
    """States, gates, c_2 and the response chi^T M_3 w for the three-step history; returns dict."""
    F = mp.mpf if prec else float
    tanh = mp.tanh if prec else math.tanh
    atanh = mp.atanh if prec else math.atanh
    sqrt = mp.sqrt if prec else math.sqrt
    n = F(n); k = n / 2; a = 1 - 1 / n; sk = sqrt(k); ga = 1 / (1 - 1 / sk); b = F("0.05")
    HI = 1 / mp.cosh(F("0.25")) ** 2 if prec else 1 / math.cosh(.25) ** 2
    lam = 1 / (100 * n); sig = b
    for _ in range(200):
        sig = tanh(lam * sig + b)
    # t = 1: every memory row and every source row is tanh(.05)
    s1 = tanh(b)
    # t = 2 (O h_1): row 0 -> s1; row 1 -> J1 + gamma sp1/sqrt k; rows >= 2 -> s1 + J1
    sp1 = (k - 1) * s1
    J1 = ga * s1 / sk - ga ** 2 * sp1 / k
    h20 = tanh(a * s1 + b); h21 = tanh(a * (J1 + ga * sp1 / sk) + b); s2 = tanh(a * (s1 + J1) + b)
    # pair at t = 2: (+.2, -.2) in history +, (0, 0) in history -; zero sum, so sp2 and J2 are common
    sp2 = h21 + (k - 2) * s2 - 2 * s2 + 0           # rows 2..k-1 bulk except the pair, pair sums to 0
    J2 = ga * s2 / sk - ga ** 2 * sp2 / k
    h30 = tanh(a * h20 + b); h31 = tanh(a * (J2 + ga * sp2 / sk) + b)
    h32 = tanh(a * (h21 + J2) + b); s3 = tanh(a * (s2 + J2) + b)
    g0, g1, g2, gb = 1 - h30 ** 2, 1 - h31 ** 2, 1 - h32 ** 2, 1 - s3 ** 2
    # inputs: t2 pair targets vs preactivation atanh(s2); t3 reset of the pair to the bulk value s3
    x2 = max(abs(atanh(v) - atanh(s2)) for v in (F("0.2"), F("-0.2"), F(0)))
    x3 = max(abs(a * (s2 - v)) for v in (F("0.2"), F("-0.2"), F(0)))
    # response chi^T M_3 w with chi = a P^T U (HI 1) = a HI sqrt(k) e_(d-1) and M_3 = U G_3 U a P
    #   v = U P w: v0 = -1/sk - ga(1-2/sk)(1-1/sk); v1 = 1 - 1/sk + ga(1-2/sk)/sk; vo = (-1 + ga(1-2/sk))/sk
    c = ga * (1 - 2 / sk)
    v0 = -1 / sk - c * (1 - 1 / sk); v1 = 1 - 1 / sk + c / sk; vo = (-1 + c) / sk
    wGv = (1 - 1 / sk) * g0 * v0 - (g1 * v1 + g2 * vo + (k - 3) * gb * vo) / sk
    resp = a * HI * sk * a * (gb * vo + (ga / sk) * wGv)
    c2 = s1 / sig
    contrib = (ga / sk) * c2 * F("-0.04") * resp
    return {"s1": s1, "s2": s2, "s3": s3, "g": (g0, g1, g2, gb), "c2": c2, "resp": resp,
            "contrib": contrib, "x2": x2, "x3": x3, "delta2_plus": (1 - F("0.04")) - (1 - s2 ** 2),
            "delta2_minus": 1 - (1 - s2 ** 2)}


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def full_example(n):
    """Full-vector float64 simulation of both histories; returns S_j, S'_j and the readout of the
    source-specific creation difference, propagated by the true map, plus endpoint equality."""
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); HI = 1 / math.cosh(.25) ** 2
    w = -np.ones(k) / sk; w[0] += 1
    sig = .05
    for _ in range(200):
        sig = math.tanh(lam * sig + .05)
    j, jp = d + 7, d + 8
    res = {}
    for name, v in (("+", .2), ("-", 0.0)):
        h = np.zeros(n); o = 0.0; S = 0.0; Sp = 0.0; xmax = 0.0; G = []; deltas = []
        for t in (1, 2, 3):
            pre = np.empty(n); pre[:k] = a * O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
            hn = np.tanh(pre)
            c = h[k:].sum() / (sig * l)
            if t == 2:
                hn[j], hn[jp] = v, -v
                xmax = max(xmax, abs(math.atanh(v) - pre[j]), abs(math.atanh(-v) - pre[jp]))
            if t == 3:
                bulk = hn[d + 100]
                xmax = max(xmax, abs(math.atanh(bulk) - pre[j]), abs(math.atanh(bulk) - pre[jp]))
                hn[j], hn[jp] = bulk, bulk
            g = 1 - hn[:k] ** 2
            ghat = g[d + 100]                               # an undriven off-cycle bulk row
            dl = g[j] - ghat
            S += abs(dl) * o; Sp += abs(dl) * (a * o + c)
            deltas.append((dl, o, c)); G.append(g)
            o = g[j] * (a * o + c)
            h = hn
        res[name] = {"S": S, "Sp": Sp, "G": G, "deltas": deltas, "h": h, "xmax": xmax}
    # source-specific creation difference at t = 2 (o_1 = 0 in both): q c_2 Delta delta_2 w
    dl_p, o_p, c_p = res["+"]["deltas"][1]; dl_m, o_m, c_m = res["-"]["deltas"][1]
    dxi = (gam / sk) * ((dl_p * (a * o_p + c_p)) - (dl_m * (a * o_m + c_m))) * w
    # propagate by the true map M_3 = U G_3 U a P (G_3 common: endpoint states identical)
    def U(x):
        return x - gam * w * (w @ x)
    def P(x):
        y = np.empty_like(x); y[1:d] = x[0:d - 1]; y[0] = x[d - 1]; y[d:] = x[d:]
        return y
    G3 = res["+"]["G"][2]
    M3dxi = U(G3 * U(a * P(dxi)))
    g_q = np.full(k, HI)
    Ug = U(g_q); chi = np.empty(k); chi[:d - 1] = a * Ug[1:d]; chi[d - 1] = a * Ug[0]; chi[d:] = a * Ug[d:]
    readout = float(chi @ M3dxi)
    endpoint_gap = float(np.abs(res["+"]["h"] - res["-"]["h"]).max())
    gates_gap_t3 = float(np.abs(res["+"]["G"][2] - res["-"]["G"][2]).max())
    return {"S_j(+)": res["+"]["S"], "S_j(-)": res["-"]["S"], "S'_j(+)": res["+"]["Sp"], "S'_j(-)": res["-"]["Sp"],
            "source-specific readout (full)": readout, "endpoint max gap": endpoint_gap,
            "t=3 gate gap": gates_gap_t3, "max |x|": max(res["+"]["xmax"], res["-"]["xmax"])}


def main():
    out = {}
    # (A)
    for nn in (4096, 16384):
        fe = full_example(nn); ce = class_example(nn, prec=False)
        out[f"A: n={nn} full-vector"] = fe
        out[f"A: n={nn} class formula contribution"] = float(ce["contrib"])
        out[f"A: n={nn} relative difference"] = abs(fe["source-specific readout (full)"] - float(ce["contrib"])) / abs(float(ce["contrib"]))
        assert abs(fe["S_j(+)"]) == 0.0 and abs(fe["S_j(-)"]) == 0.0
        assert out[f"A: n={nn} relative difference"] < 1e-8 and fe["endpoint max gap"] == 0.0
    ce = class_example(10 ** 8)
    out["A: n=1e8 response chi^T M_3 w"] = mp.nstr(ce["resp"], 15)
    out["A: n=1e8 source-specific readout difference"] = mp.nstr(ce["contrib"], 15)
    out["A: n=1e8 max |input|"] = mp.nstr(max(ce["x2"], ce["x3"]), 12)
    out["A: n=1e8 Delta delta_2(j)"] = mp.nstr(ce["delta2_plus"] - ce["delta2_minus"], 12)
    out["A: n=1e8 c_2"] = mp.nstr(ce["c2"], 12)
    assert ce["contrib"] != 0 and max(ce["x2"], ce["x3"]) < mp.mpf("0.5")
    assert abs(ce["delta2_plus"] - ce["delta2_minus"] + mp.mpf("0.04")) < mp.mpf("1e-50")
    # (B)
    a = 1 - Q(1, 10 ** 8); mu = Q(1, 10 ** 8); s0 = Q(10); N = 10
    damped = (a * (1 - mu)) ** N * s0
    undamped_baseline = a ** N * s0
    out["B: claimed acquired part (undamped baseline)"] = float(damped - undamped_baseline)
    out["B: corrected acquired part (damped baseline)"] = float(damped - damped)
    assert damped - undamped_baseline < 0
    # (C)
    rH = -2 * mp.log(1 / mp.cosh(mp.mpf("0.25")) ** 0.5) if False else -mp.log(1 / mp.cosh(mp.mpf("0.25")) ** 2)
    def Fs(nv):
        kk = mp.mpf(nv) / 2
        return int(mp.ceil(mp.log(mp.mpf("1.01") * mp.sqrt(kk)) / rH))
    def f(nv):
        return 1 + mp.log(mp.mpf("1.01") * mp.sqrt(mp.mpf(nv) / 2)) / rH
    nl, nr = 11785591396, 11785591400
    out["C: F_s(11785591396), F_s(11785591400)"] = [Fs(nl), Fs(nr)]
    out["C: n/F_s left, right"] = [float(mp.mpf(nl) / Fs(nl)), float(mp.mpf(nr) / Fs(nr))]
    assert Fs(nl) == 182 and Fs(nr) == 183 and mp.mpf(nl) / Fs(nl) > mp.mpf(nr) / Fs(nr)
    # envelope: d/dn [n/f(n)] = (f - n f')/f^2 = (f - 1/(2 rH))/f^2 > 0 iff f > 1/(2 rH)
    assert f(10 ** 10) > 1 / (2 * rH)
    out["C: sqrt(1e10/f(1e10)) (needs >= 5357.85)"] = float(mp.sqrt(mp.mpf(10) ** 10 / f(10 ** 10)))
    assert mp.sqrt(mp.mpf(10) ** 10 / f(10 ** 10)) >= mp.mpf("5357.85")
    # (D)
    HI = 1 / mp.cosh(mp.mpf("0.25")) ** 2
    k8 = mp.mpf(10) ** 8 / 2; g8 = 1 / (1 - 1 / mp.sqrt(k8))
    wc = mp.mpf("2.18") * g8 / mp.sqrt(k8)
    coef = wc / mp.mpf("1.2") * mp.mpf(23) / 64 + wc / HI / 8
    out["D: Lemma 1.3 coefficient at n=1e8"] = mp.nstr(coef, 12)
    assert coef < mp.mpf("1.4e-4")
    # (E) Lemma R, all sizes (x = sqrt k >= sqrt(5e7); x exp(-.0297 x) decreasing for x > 1/.0297)
    x = mp.sqrt(mp.mpf("5e7")); gam = 1 / (1 - 1 / x)
    tail = x * 4 * mp.e ** (-mp.mpf("0.0297") * x + mp.mpf("0.92"))
    one = HI * (1 + mp.sqrt(2) * gam + tail); fst = 1 + HI * (mp.sqrt(2) * gam + tail)
    out["E: Lemma R one-step bound (all n >= 1e8, S4 domain)"] = mp.nstr(one, 12)
    out["E: Lemma R F-step bound (t < T)"] = mp.nstr(fst, 12)
    out["E: Lemma R F-step terminal |chi^T w| <= A_1 + 1"] = 2.18
    out["E: terminal one-step |chi^T w| <= HI + .3436"] = mp.nstr(HI + mp.mpf(".3436"), 8)
    assert one < mp.mpf("2.27") and fst < mp.mpf("2.33")
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, "repairs_check_result.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
