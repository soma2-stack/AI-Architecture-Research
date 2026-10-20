"""Route-2 probe: second-order RELAY through held arrival rows, versus the direct off-cycle leak.

Mechanism (PROOF.md section 4.1). An off-cycle pair (j, j') is held at state 0 for H_p steps and,
in the "+" history only, pulsed for 7 steps with the balanced states (+v, -v), v = tanh(.38).
* Scenario A (direct, first order): the gather path (U-row d-1 at T) is held throughout the pair's
  activity, so the pair's leak enters the gather row directly (Theorem M's L_off).
* Scenario B (relay, second order): the gather path is held only AFTER the pair's activity, for
  H_g steps. The H_g cycle contents that will arrive during that hold are held at 0 from the start
  of the pair's activity until they arrive. They retain the pair's leak; the gather captures them
  (Theorem M's K_bus). Nothing first-order reaches the gather row.
* Scenario B0: as B, but the arrival rows are not held (bath-level relay only).
Readout: HI sqrt(k) |Delta Z_T(d-1)(j)| (the gather channel on the pair column).
Predictions: undamped relay = H_g (gamma/sqrt k) s^2 a z HI sqrt(k), with z the direct-leak content
of scenario A; Lemma D's common-mode damping (rate gamma s^2 |H|/k per step) reduces it.
Column-restricted exact recurrences (credit columns never mix), n = 65536; CPU only.
Run: python -I exp_relay.py   (writes exp_relay_result.json)
Version 2: a gap G = 3000 (s^2 G ~ 7) separates the pair release from the gather hold, so the
first-order leak of the relaxing source cannot reach the gather row (version 1 lacked the gap and
its "relay" was mostly that first-order leak; see CHECKS.md).
"""
import importlib.util, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "claude_lemma_m_rest_20261016", "colsim.py")
spec = importlib.util.spec_from_file_location("colsim", SRC); cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
HI = 1 / math.cosh(.25) ** 2


def hist_vec(n, T, cols, drives, track_row=None):
    """colsim.hist with vectorised drives: drives(t) -> (rows int array, targets float array)."""
    k, d = n // 2, n // 4; l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / math.sqrt(k))
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    cols = np.asarray(cols); nc = len(cols)
    h = np.zeros(n); B = np.zeros((k, nc)); O = np.zeros((k, nc)); xmax = 0.0; maxw = 0
    track = np.zeros(T + 1)
    for t in range(1, T + 1):
        pre = np.empty(n); pre[:k] = a * cs.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        rows, tg = drives(t)
        if len(rows):
            x = np.arctanh(tg) - pre[rows]; xmax = max(xmax, float(np.abs(x).max())); hn[rows] = tg
            maxw = max(maxw, len(rows))
        g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * cs.O_apply(B, k, d, gam); Bn[cols, np.arange(nc)] += c; Bn *= gm[:, None]
        On = np.zeros((k, nc)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[cols, np.arange(nc)] += c * gm[cols]
        B, O, h = Bn, On, hn
        if track_row is not None:
            track[t] = O[track_row, 0]
    return {"Z": cs._yz(B, O, k, gam), "O": O, "h": h, "xmax": xmax, "width": maxw, "track": track}


def scenario(n, kind, Hp, Hg, z, W0=1500, G=0):
    k, d = n // 2, n // 4
    j, jp = d + 1000, d + 1001
    tp = W0; te = tp + Hp                       # pair activity [tp, te)
    T = te + G + Hg + 2
    pulse = range(tp + Hp // 2, tp + Hp // 2 + 7)
    v = math.tanh(.38)
    arrivals = range(T - Hg + 1, T + 1)
    def drives(t):
        rows, tg = [], []
        if tp <= t < te:
            rows += [j, jp]
            tg += ([v, -v] if (z > 0 and t in pulse) else [0.0, 0.0])
        if kind == "A" and t >= tp:
            r = d - 1 - (T - t)
            if r >= 2:
                rows.append(r); tg.append(0.0)
        if kind in ("B", "B0") and t >= T - Hg:
            r = d - 1 - (T - t)
            if r >= 2:
                rows.append(r); tg.append(0.0)
        if kind == "B" and t >= tp:
            # contents arriving at time ta are at row d-1-(ta-1-t) at time t, for t <= ta-1
            lo = d - 1 - (T - 1 - t); hi = d - 1 - (T - Hg - t)
            rr = np.arange(max(2, lo), min(d - 1, hi) + 1)
            rr = rr[rr != d - 1 - (T - t)]       # the gather path itself is handled above
            rows += rr.tolist(); tg += [0.0] * len(rr)
        return np.asarray(rows, dtype=int), np.asarray(tg, dtype=float)
    out = hist_vec(n, T, [j, jp], drives, track_row=j)
    return out, T


def main():
    n = 65536; k = n // 2; d = n // 4; sk = math.sqrt(k); gam = 1 / (1 - 1 / sk); a = 1 - 1 / n
    Hp = 2000; G = 3000
    res = {"n": n, "H_p": Hp, "gap G (s^2 G ~ 7)": G, "rows": []}
    def readout(kind, Hg, gap):
        o_p, T = scenario(n, kind, Hp, Hg, +1, G=gap); o_m, _ = scenario(n, kind, Hp, Hg, -1, G=gap)
        dZ = o_p["Z"][d - 1, 0] - o_m["Z"][d - 1, 0]
        s = float(np.median(o_p["h"][d + 2000:d + 2100]))
        peak = float(np.abs(o_p["track"] - o_m["track"]).max())
        return HI * sk * abs(dZ), dZ, s, max(o_p["xmax"], o_m["xmax"]), max(o_p["width"], o_m["width"]), peak
    rA, zA, s, xA, wA, pk = readout("A", 0, 0)
    res["direct (A), no gap"] = {"readout": rA, "gather content diff": zA, "bath s": s, "max|x|": xA,
                                 "width": wA, "peak |Delta O_j|": pk}
    print(json.dumps(res["direct (A), no gap"]), flush=True)
    for Hg in (100, 400, 1600, 3200, 6400, 11000):
        rB, zB, s, xB, wB, pk = readout("B", Hg, G)
        r0, z0, _, _, _, _ = readout("B0", Hg, G)
        row = {"H_g": Hg, "relay readout (B)": rB, "no-hold control (B0)": r0,
               "peak |Delta O_j|": pk, "ceiling HI s peak": HI * s * pk, "ratio B/ceiling": rB / (HI * s * pk),
               "K_bus-only ceiling HI gamma s^2 peak": HI * gam * s * s * pk,
               "common-mode damping exponent gamma s^2 H_g (H_p+G)/k": gam * s * s * Hg * (Hp + G) / k,
               "max|x|": xB, "peak width": wB}
        res["rows"].append(row); print(json.dumps(row), flush=True)
    json.dump(res, open(os.path.join(HERE, "exp_relay_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
