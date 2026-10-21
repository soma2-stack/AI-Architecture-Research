"""Phase 3 decision experiment: can switching heterogeneous retainers PUMP retained memory without
bound (the one loophole left by Proposition 10.3, which caps every stationary response)?

Hypotheses.  H1: the centered readout / peak source content grows with the number of cycles.
             H2: it saturates at a bounded multiple (a transient overshoot of the stationary ceiling).
Prediction of the switching analysis (PROOF.md section 10.4): geometric saturation, ratio factor
mu = (P_B/P)(1 + P_A/k) per cycle, final gain ~ 1/(1 - P_B/k) over the homogeneous ceiling.

Exact column-restricted recurrences (PR #32 colsim.py, read-only), R0, n = 65536, legal inputs,
exact common states at every cycle end. Each cycle: an ON phase (H_on steps) in which the source
pair (j, j') and groups A, B are held at 0, with a balanced 7-step pulse (+v, -v), v = tanh(.38),
at mid-phase in history + only; then an OFF phase (H_off steps) in which the source pair and
group B run free (no input) while group A stays held. Controls: B held in both phases
("control"), and no group B ("A only"). This is a structural test (widths ~ P_A + P_B), not a
resource-efficient construction.
Readout at each cycle end: exact optimum over the legal one-step gate box of the one-column
CENTERED bus readout on column j; normalised by the running peak |Delta Y_t(j)| (full transformed
source credit) and by the running peak |Delta O_t(j)| (own).
Run: python -I exp_pump.py [--long]   (writes exp_pump_result.json; --long: 30 cycles, P_A = 1000, writes exp_pump_long_result.json)
"""
import importlib.util, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "claude_lemma_m_rest_20261016", "colsim.py")
spec = importlib.util.spec_from_file_location("colsim", SRC); cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def simulate(n, z, PA, PB, mode, C, Hon, Hoff, t0=500):
    k, d = n // 2, n // 4; l = n - k; a = 1 - 1 / n; lam = 1 / (100 * n); sk = math.sqrt(k)
    gam = 1 / (1 - 1 / sk); sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    j, jp = d, d + 1
    A = np.arange(d + 10, d + 10 + PA); B = np.arange(d + 10 + PA, d + 10 + PA + PB)
    assert d + 10 + PA + PB <= k
    v = math.tanh(.38); L = Hon + Hoff; T = t0 + C * L - 1
    cols = np.array([j, jp]); nc = 2
    h = np.zeros(n); Bc = np.zeros((k, nc)); Oc = np.zeros((k, nc))
    xmax = 0.0; width = 0; Yj = np.zeros(T + 1); Oj = np.zeros(T + 1); snaps = {}
    for t in range(1, T + 1):
        pre = np.empty(n); pre[:k] = a * cs.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        rows = []; tg = []
        if t >= t0:
            c, r = divmod(t - t0, L)
            on = r < Hon
            if on:
                pulse = z > 0 and Hon // 2 <= r < Hon // 2 + 7
                rows += [j, jp]; tg += ([v, -v] if pulse else [0.0, 0.0])
            rows += A.tolist(); tg += [0.0] * len(A)
            if PB and (on or mode == "control"):
                rows += B.tolist(); tg += [0.0] * len(B)
        if rows:
            rr = np.asarray(rows); tt = np.asarray(tg)
            x = np.arctanh(tt) - pre[rr]; xmax = max(xmax, float(np.abs(x).max()))
            width = max(width, int((np.abs(x) > 0).sum())); hn[rr] = tt
        g = 1 - hn ** 2; gm = g[:k]; cc = h[k:].sum() / (sig * l)
        Bn = a * cs.O_apply(Bc, k, d, gam); Bn[cols, np.arange(nc)] += cc; Bn *= gm[:, None]
        On = np.zeros((k, nc)); On[2:d] = gm[2:d, None] * a * Oc[1:d - 1]; On[d:] = gm[d:, None] * a * Oc[d:]
        On[cols, np.arange(nc)] += cc * gm[cols]
        Bc, Oc, h = Bn, On, hn
        b = Bc[:, 0]
        Yj[t] = b[j] + (gam / sk) * (b[0] - b.sum() / sk)          # U-row j: b(j) - gamma w_j (w^T b)
        Oj[t] = Oc[j, 0]
        if t >= t0 and (t - t0 + 1) % L == 0:
            snaps[(t - t0 + 1) // L] = cs._yz(Bc, Oc, k, gam)[:, 0].copy()
    return {"Yj": Yj, "Oj": Oj, "snaps": snaps, "xmax": xmax, "width": width, "T": T, "h": h}


def centered_readout(dZ, n):
    k, d = n // 2, n // 4; a = 1 - 1 / n
    zc = dZ.copy(); zc[d - 1] = 0.0
    c = cs.chi_adjoint(zc, k, d, a)
    return max(abs(float(np.maximum(LO * c, HI * c).sum())), abs(float(np.minimum(LO * c, HI * c).sum())))


def main():
    import sys
    n = 65536; Hon, Hoff = 800, 1200
    if "--long" in sys.argv:
        C = 30; configs = [("pump", 1000, 12000), ("A only", 1000, 0)]
    else:
        C = 12; configs = [("pump", 4000, 12000), ("control", 4000, 12000), ("A only", 4000, 0), ("pump", 1000, 12000)]
    res = {"n": n, "cycles": C, "H_on": Hon, "H_off": Hoff, "rows": []}
    for mode, PA, PB in configs:
        sp = simulate(n, +1, PA, PB, mode, C, Hon, Hoff); sm = simulate(n, -1, PA, PB, mode, C, Hon, Hoff)
        dY = np.abs(sp["Yj"] - sm["Yj"]); dO = np.abs(sp["Oj"] - sm["Oj"])
        L = Hon + Hoff; curve = []
        for c in range(1, C + 1):
            tc = 500 + c * L - 1
            r = centered_readout(sp["snaps"][c] - sm["snaps"][c], n)
            curve.append({"cycle": c, "readout": r, "peak|dY_j|": float(dY[:tc + 1].max()),
                          "peak|dO_j|": float(dO[:tc + 1].max()),
                          "readout/peak|dY_j|": r / float(dY[:tc + 1].max())})
        row = {"mode": mode, "P_A": PA, "P_B": PB, "max|x|": max(sp["xmax"], sm["xmax"]),
               "peak width": max(sp["width"], sm["width"]),
               "endpoint max gap": float(np.abs(sp["h"] - sm["h"]).max()), "curve": curve}
        res["rows"].append(row)
        print(json.dumps({"mode": mode, "P_A": PA, "P_B": PB,
                          "ratios": [round(cv["readout/peak|dY_j|"], 5) for cv in curve],
                          "readouts": [round(cv["readout"], 4) for cv in curve],
                          "endpoint gap": row["endpoint max gap"], "max|x|": row["max|x|"]}), flush=True)
    json.dump(res, open(os.path.join(HERE, "exp_pump_long_result.json" if "--long" in sys.argv else "exp_pump_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
