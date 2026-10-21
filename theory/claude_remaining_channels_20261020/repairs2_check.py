"""Step 3.6 repairs: independent reproduction of Codex's Step-3.5 counterexamples, and checks of the
repaired statements (PROOF.md section R2).

(A) Theorem 7.5, nonzero initial content: R0, n = 1e8, one off-cycle retainer i (P = 1), credit
    column j off the cycle, m = 1, T = 3; zero inputs through t = 2, retainer set to 0 at t = 3;
    I = (2, 3], so E = Q = 0. Class reduction (standard rows 0, 1, 2, bulk, j, i), 60-digit mpmath;
    cross-checked against full-vector float64 simulation of the same history at n = 4096, 16384.
    Reports: the literal first-version readout bound (violated, factor ~1.504), the repaired total
    bound A{1.33 (M* + |sigma_t1|) + 1.29 P (omega_t1 + Q)}, and the exact decomposition
    chi^T y_T = chibar Lambda sigma_t1 + a^L chi^T d_t1 + Acq.
(B) Lemma 7.2, total drift can be negative: n = 1e8, m = 5000, T = 3 (4999 off-cycle rows set to .49
    and one retainer set to 0 at t = 2): bath change, retainer drift, and the positive integral I.
(C) Theorem 7.3, cycle front starts: the safe count 1 + floor((H + Lam - 1)/d) over the expanded window;
    Codex's boundary example (two front starts, 1 + H/d = 1.991).
(D) Corollary 7.4(b): a one-step, zero-input interval with retention exp(-.003) < a(1 - s_3^2).
(E) Symmetric-reset arithmetic: exact discrete average deficits for linear samples
    beta^2 (R-1)(2R-1)/6, beta^2 (R^2-1)/12, beta^2 (R^2+2)/12 (exact rationals).
Run: python -I repairs2_check.py   (writes repairs2_check_result.json)
"""
import json, math, os
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
mp.mp.dps = 60


def consts(n, F, sqrt):
    k = n / 2; a = 1 - 1 / n; sk = sqrt(k); g = 1 / (1 - 1 / sk); return k, a, sk, g


# ---------------------------------------------------------------- (A) class reduction, standard rows
def theorem75_class(n, prec=True):
    F = mp.mpf if prec else float; tanh = mp.tanh if prec else math.tanh
    sqrt = mp.sqrt if prec else math.sqrt; atanh = mp.atanh if prec else math.atanh
    n = F(n); k, a, sk, ga = consts(n, F, sqrt); b = F("0.05"); lam = 1 / (100 * n)
    HI = 1 - tanh(F("0.25")) ** 2; LO = 1 - tanh(F("0.75")) ** 2
    sig = b
    for _ in range(300):
        sig = tanh(lam * sig + b)
    s1 = tanh(b)                                   # t = 1: every memory and source row
    J1 = ga * s1 / sk - ga ** 2 * (k - 1) * s1 / k
    s2 = tanh(a * (s1 + J1) + b)                   # bulk at t = 2 (rows >= 2)
    h21 = tanh(a * (J1 + ga * (k - 1) * s1 / sk) + b)
    c2 = s1 / sig; c3 = tanh(lam * s1 + b) / sig   # source rows: tanh(.05), tanh(lam s1 + .05)
    b2 = c2 * (1 - s2 ** 2)                        # B_2 = b2 e_j
    sp2 = h21 + (k - 2) * s2
    J2 = ga * s2 / sk - ga ** 2 * sp2 / k
    s3 = tanh(a * (s2 + J2) + b)                   # bulk at t = 3 (j is bulk)
    h31 = tanh(a * (J2 + ga * sp2 / sk) + b); h32 = tanh(a * (h21 + J2) + b)
    g1, g2, gb = 1 - h31 ** 2, 1 - h32 ** 2, 1 - s3 ** 2
    xin = abs(atanh(F(0)) - (a * (s2 + J2) + b))   # retainer set to 0 at t = 3
    # one O application to b2 e_j (j off-cycle): rows >= 1 get J = -g^2 b2/k; row 1 adds g b2/sk; row j adds b2
    Jc = -ga ** 2 * b2 / k
    B3 = {"r1": g1 * a * (Jc + ga * b2 / sk), "r2": g2 * a * Jc, "bulk": gb * a * Jc,
          "j": gb * (a * (b2 + Jc) + c3), "i": 1 * a * Jc}
    mult = {"r1": 1, "r2": 1, "bulk": k - 5, "j": 1, "i": 1}     # memory rows >= 1: 1+1+(k-5)+1+1 = k-1
    tot3 = sum(mult[c] * B3[c] for c in B3)
    Y3i = B3["i"] - ga * tot3 / k                  # U-row i:  B(i) - (gamma/k) sum_l B(l)   (B(0) = 0)
    Y2i = 0 - ga * b2 / k
    Lam = a * (1 - ga * 1 * s3 ** 2 / k)           # P = 1, mu_3 = gamma s_3^2/k
    chi = a * (HI - ga * (LO + (HI - LO) / k) + ga * LO / sk)    # query HI on i, LO elsewhere
    A = abs(chi); Mstar = abs(Y3i - Lam * Y2i)
    actual = abs(chi * Y3i)
    literal = A * F("1.33") * Mstar                # first version: replace sigma by sigma - Lambda sigma_t1
    repaired = A * (F("1.33") * (Mstar + abs(Y2i)))
    decomp_resid = abs(chi * Y3i - (chi * Lam * Y2i + chi * (Y3i - Lam * Y2i)))   # P = 1: d = 0
    return {"sigma_2": Y2i, "sigma_3": Y3i, "M*": Mstar, "A": A, "actual": actual, "literal bound": literal,
            "repaired bound": repaired, "violation factor": actual / literal, "input": xin,
            "decomposition residual": decomp_resid, "Lambda": Lam}


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def theorem75_full(n):
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); sig = .05
    for _ in range(300):
        sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / sk; w[0] += 1
    j, i = d + 5, d + 9
    h = np.zeros(n); b = np.zeros(k); Ys = {}
    for t in (1, 2, 3):
        pre = np.empty(n); pre[:k] = a * O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        if t == 3:
            hn[i] = 0.0
        g = 1 - hn[:k] ** 2; c = h[k:].sum() / (sig * l)
        e = np.zeros(k); e[j] = c
        b = g * (a * O_apply(b, k, d, gam) + e)
        h = hn
        Ys[t] = float(b[i] - gam * (w @ b) * w[i])          # U-row i of column j
    return Ys


# ---------------------------------------------------------------- (B) negative total drift
def negative_drift():
    F = mp.mpf; n = F(10) ** 8; k, a, sk, ga = consts(n, F, mp.sqrt); b = F("0.05")
    s1 = mp.tanh(b); J1 = ga * s1 / sk - ga ** 2 * (k - 1) * s1 / k
    s2 = mp.tanh(a * (s1 + J1) + b); h21 = mp.tanh(a * (J1 + ga * (k - 1) * s1 / sk) + b)
    sp2 = h21 + (k - 2 - 5000) * s2 + 4999 * F("0.49") + 0
    J2 = ga * s2 / sk - ga ** 2 * sp2 / k
    field = b + a * J2
    s3 = mp.tanh(a * s2 + field); y3 = mp.tanh(field)
    I = (mp.atanh(s3) - s3) - (field - mp.tanh(field))
    x49 = abs(mp.atanh(F("0.49")) - mp.atanh(s2)); x0 = abs(mp.atanh(s2))
    ident = (y3 - 0) - ((s3 - s2) + (1 - a) * (s2 - 0) + I)
    return {"s2": s2, "s3": s3, "bath change": s3 - s2, "retainer drift y3 - y2": y3, "I": I,
            "max input": max(x49, x0), "identity residual": ident}


def main():
    out = {}
    # (A)
    for nn in (4096, 16384):
        full = theorem75_full(nn); cl = theorem75_class(nn, prec=False)
        out[f"A: n={nn} Y_2(i) full / class"] = [full[2], float(cl["sigma_2"])]
        out[f"A: n={nn} Y_3(i) full / class"] = [full[3], float(cl["sigma_3"])]
        assert abs(full[3] - float(cl["sigma_3"])) <= 1e-9 * abs(full[3])
        assert abs(full[2] - float(cl["sigma_2"])) <= 1e-9 * abs(full[2])
    r = theorem75_class(10 ** 8)
    for kk in ("sigma_2", "sigma_3", "M*", "actual", "literal bound", "repaired bound", "violation factor", "input",
               "decomposition residual"):
        out["A: n=1e8 " + kk] = mp.nstr(r[kk], 15)
    assert r["actual"] > r["literal bound"] and r["actual"] <= r["repaired bound"] and r["input"] < mp.mpf("0.5")
    # (B)
    nd = negative_drift()
    for kk in nd:
        out["B: " + kk] = mp.nstr(nd[kk], 14)
    assert nd["retainer drift y3 - y2"] < 0 and nd["I"] > mp.mpf("1.6e-6") and nd["bath change"] > mp.mpf("-0.001")
    assert nd["max input"] < mp.mpf("0.5") and abs(nd["identity residual"]) < mp.mpf("1e-40")
    # (C)
    d = 25000000; Lam = 450000; H = 50000001 - 25225002 + 1
    starts = [t for t in (25000001, 50000001) if 50000001 - H + 1 - Lam <= t <= 50000001]
    safe = 1 + (H + Lam - 1) // d
    out["C: front starts in expanded window"] = len(starts); out["C: 1 + H/d"] = 1 + H / d; out["C: safe count"] = safe
    assert len(starts) == 2 and 1 + H / d < 2 and safe >= len(starts)
    # (D)
    F = mp.mpf; n = F(10) ** 8; k, a, sk, ga = consts(n, F, mp.sqrt); b = F("0.05")
    s1 = mp.tanh(b); J1 = ga * s1 / sk - ga ** 2 * (k - 1) * s1 / k
    s2 = mp.tanh(a * (s1 + J1) + b); h21 = mp.tanh(a * (J1 + ga * (k - 1) * s1 / sk) + b)
    J2 = ga * s2 / sk - ga ** 2 * (h21 + (k - 2) * s2) / k
    s3 = mp.tanh(a * (s2 + J2) + b)
    ret = a * (1 - s3 ** 2)
    out["D: one-step retention a g_3 (zero inputs)"] = mp.nstr(ret, 13); out["D: exp(-.003)"] = mp.nstr(mp.e ** F("-0.003"), 13)
    assert ret > mp.e ** F("-0.003")
    # (E)
    for R in (16, 64, 256, 1024):
        z = sum(Fr(r) ** 2 for r in range(R)) / R
        opt = sum((Fr(r) - Fr(R - 1, 2)) ** 2 for r in range(R)) / R
        auth = sum((Fr(r) - Fr(R, 2)) ** 2 for r in range(R)) / R
        assert z == Fr((R - 1) * (2 * R - 1), 6) and opt == Fr(R * R - 1, 12) and auth == Fr(R * R + 2, 12)
    out["E: discrete reset averages (units beta^2)"] = "zero (R-1)(2R-1)/6, optimal (R^2-1)/12, -R/2 target (R^2+2)/12: exact for R = 16, 64, 256, 1024"
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, "repairs2_check_result.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
