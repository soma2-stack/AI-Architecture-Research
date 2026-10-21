"""Phase 2: heterogeneous retention with sparse staggered resets (PROOF.md section 7).

Exact column-restricted recurrences (PR #32 colsim.py, imported read-only), n = 65536, R0, legal
inputs, every nonzero input counted, cost = peak actual width x full horizon.

Schedule (as in Codex's E4 reset probe, AUDIT section 7.3):
  warm-up zero inputs to t = 499; source pair (j, j') held at 0 for H_p = 1800 steps from t = 500;
  in history + only, a balanced 7-step pulse (+v, -v), v = tanh(.38), at the midpoint, then reset
  to 0 and hold; release at t = 2300; gap G; horizon T = 2300 + G.
  P = 2048 off-cycle retainers, common to both histories, maintained from t = 500 to T by:
    hold      continuous holds at state 0 (width P);
    stag R    one reset to target y0 every R steps, phases staggered (row i at t = i mod R);
    sync R    one reset every R steps, all retainers at the same step (peak width P);
    target    y0 = 0, or the symmetric target y0 = -beta R/2, beta = atanh(s) - a s (bath drift).
Readout: the exact optimum over the legal one-step gate box of the one-column CENTERED readout
(gather row d-1 excluded) on column j: max over g in [LO,HI]^k of |g^T (a U P z_c)|.
Prediction (section 7.2): a reset retainer drifts up at beta per step, so its gate deficit
averages (beta R)^2/3 (target 0) or (beta R)^2/12 (symmetric); retained deposits keep a fraction
~ exp(-deficit x retention time) relative to exact holds.
Run: python -I exp_resets.py [--long]   (writes exp_resets_result.json or exp_resets_long_result.json)
"""
import importlib.util, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "claude_lemma_m_rest_20261016", "colsim.py")
spec = importlib.util.spec_from_file_location("colsim", SRC); cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def run(n, T, drives, cols):
    k, d = n // 2, n // 4; l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    cols = np.asarray(cols); nc = len(cols)
    h = np.zeros(n); B = np.zeros((k, nc)); O = np.zeros((k, nc))
    xmax = 0.0; width = 0; total = 0; baths = []
    for t in range(1, T + 1):
        pre = np.empty(n); pre[:k] = a * cs.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        rows, tg = drives(t, hn)
        if len(rows):
            x = np.arctanh(tg) - pre[rows]
            nz = np.abs(x) > 0
            xmax = max(xmax, float(np.abs(x).max())); width = max(width, int(nz.sum())); total += int(nz.sum())
            hn[rows] = tg
        g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * cs.O_apply(B, k, d, gam); Bn[cols, np.arange(nc)] += c; Bn *= gm[:, None]
        On = np.zeros((k, nc)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[cols, np.arange(nc)] += c * gm[cols]
        B, O, h = Bn, On, hn
        if t % 50 == 0:
            baths.append(float(h[k - 1]))
    return {"Z": cs._yz(B, O, k, gam), "xmax": xmax, "width": width, "total": total,
            "bath": float(np.median(baths[-20:]))}


def make(n, mode, R, target, G, z, P=2048, Hp=1800, t0=500, beta=None, phase_shift=0):
    k, d = n // 2, n // 4
    j, jp = d + 1000, d + 1001
    ret = np.arange(d + 2000, d + 2000 + P)
    te = t0 + Hp; T = te + G
    pulse = set(range(t0 + Hp // 2, t0 + Hp // 2 + 7)); v = math.tanh(.38)
    y0 = 0.0 if target == "zero" else -beta * R / 2
    phases = (np.arange(P) + phase_shift) % max(R, 1)
    def drives(t, hn):
        rows, tg = [], []
        if t0 <= t < te:
            rows += [j, jp]
            tg += ([v, -v] if (z > 0 and t in pulse) else [0.0, 0.0])
        if mode != "none" and t0 <= t <= T:
            if mode == "hold":
                rr = ret
            elif mode == "stag":
                rr = ret[phases == (t % R)]
            else:  # sync
                rr = ret if t % R == 0 else ret[:0]
            if len(rr):
                rows += rr.tolist(); tg += [0.0 if mode == "hold" else y0] * len(rr)
        return np.asarray(rows, dtype=int), np.asarray(tg, dtype=float)
    return drives, T, [j, jp]


def centered_readout(dZ, n):
    k, d = n // 2, n // 4; a = 1 - 1 / n
    zc = dZ.copy(); zc[d - 1] = 0.0
    c = cs.chi_adjoint(zc, k, d, a)                 # a U P z_c, so that readout = g^T c
    up = float(np.maximum(LO * c, HI * c).sum()); dn = float(np.minimum(LO * c, HI * c).sum())
    return max(abs(up), abs(dn))


def config(n, mode, R, target, G, beta=None):
    out = {}
    for z in (+1, -1):
        drives, T, cols = make(n, mode, R, target, G, z, beta=beta)
        out[z] = run(n, T, drives, cols)
    dZ = out[1]["Z"][:, 0] - out[-1]["Z"][:, 0]
    r = centered_readout(dZ, n)
    m = max(out[1]["width"], out[-1]["width"])
    return {"mode": mode, "R": R, "target": target, "G": G, "T": T, "readout": r, "peak width m": m,
            "mT": m * T, "total drives (+)": out[1]["total"], "max|x|": max(out[1]["xmax"], out[-1]["xmax"]),
            "bath": out[1]["bath"]}


def main():
    n = 65536; a = 1 - 1 / n
    long = "--long" in sys.argv
    G = 12000 if long else 3000
    rows = []
    base = config(n, "hold", 1, "zero", G); rows.append(base); print(json.dumps(base), flush=True)
    s = base["bath"]; beta = math.atanh(s) - a * s
    print(json.dumps({"bath s": s, "drift beta": beta}), flush=True)
    plan = [("stag", 64, "zero"), ("stag", 256, "zero"), ("stag", 64, "sym"), ("stag", 256, "sym")]
    if not long:
        plan = [("none", 1, "zero"), ("stag", 16, "zero")] + plan + [("sync", 64, "zero"), ("stag", 1024, "zero"),
                                                                    ("stag", 1024, "sym")]
    Hret = (1800 // 2) + G                       # mean retention time of the deposits (mid-hold to T)
    for mode, R, tgt in plan:
        r = config(n, mode, R, tgt, G, beta=beta)
        r["ratio to hold"] = r["readout"] / base["readout"]
        if mode in ("stag", "sync"):
            defi = (beta * R) ** 2 / (3 if tgt == "zero" else 12)
            r["predicted ratio exp(-deficit x H_ret)"] = math.exp(-defi * Hret)
        rows.append(r); print(json.dumps(r), flush=True)
    json.dump({"n": n, "G": G, "bath s": s, "beta": beta, "rows": rows},
              open(os.path.join(HERE, "exp_resets_long_result.json" if long else "exp_resets_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
