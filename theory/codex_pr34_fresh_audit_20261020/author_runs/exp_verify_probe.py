"""Independent verification of the external three-memory probe (external_20261018/).

For n = 256, 512 and the three offset patterns, with the independent simulator m3sim.py:
* recompute the eight bit-pattern readouts Z_T(d-1) on the three memory columns, the "own
  signals", the context dependence and the additivity error, exactly as the probe defines them;
* check legality: max |x| over every state setting, peak support m, exact common endpoint;
* record the bath level s and the deviation mass sum_j |delta_t(j)|;
* attribute each single-bit effect and the largest cross-bit interaction to the nine terms.
Run: python -I exp_verify_probe.py   (writes exp_verify_probe_result.json)
"""
import itertools, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim

PROBE = {  # external_20261018/lemma_m_three_memory_results.txt (rounded there to 1e-4 %)
    (256, (0, 0, 0)): (1.766, 1.7153), (256, (0, 4, 8)): (2.8271, 2.7833), (256, (0, 8, 16)): (2.8747, 2.8354),
    (512, (0, 0, 0)): (0.8469, 0.8356), (512, (0, 4, 8)): (1.3535, 1.3434), (512, (0, 8, 16)): (1.4387, 1.4291)}


def one(n, off):
    combos = list(itertools.product((0, 1), repeat=3))
    runs = {}
    for b in combos:
        T, cols, f = m3sim.probe_schedule(n, b, off)
        runs[b] = m3sim.run(n, T, cols, f)
    z = runs[(0, 0, 0)]["Z"]
    unit = [runs[tuple(int(t == i) for t in range(3))]["Z"] - z for i in range(3)]
    own = np.array([abs(unit[i][i]) for i in range(3)])
    ctx = 0.0; worst = None
    for i in range(3):
        for bx in itertools.product((0, 1), repeat=2):
            v = [0, 0, 0]; oth = [j for j in range(3) if j != i]
            for j, bb in zip(oth, bx):
                v[j] = bb
            lo = tuple(v); v[i] = 1; hi = tuple(v)
            e = abs((runs[hi]["Z"][i] - runs[lo]["Z"][i]) - unit[i][i]) / own[i]
            if e > ctx:
                ctx, worst = e, (i, lo, hi)
    add = max(float(np.max(np.abs(runs[b]["Z"] - z - sum(unit[i] * b[i] for i in range(3))) / own)) for b in combos)
    # attribution of the worst interaction: second difference of each part on column i
    i, lo, hi = worst
    base_lo = list(lo); base_lo[i] = 0
    zero_ctx = tuple(0 if j != i else 0 for j in range(3)); one_ctx = tuple(int(j == i) for j in range(3))
    inter = {nm: float((runs[hi]["parts"][nm][i] - runs[lo]["parts"][nm][i])
                       - (runs[one_ctx]["parts"][nm][i] - runs[zero_ctx]["parts"][nm][i])) for nm in m3sim.NAMES}
    single = {nm: float(runs[one_ctx]["parts"][nm][i] - runs[zero_ctx]["parts"][nm][i]) for nm in m3sim.NAMES}
    recon = max(float(np.abs(sum(r["parts"][nm] for nm in m3sim.NAMES) - r["Z"]).max()) for r in runs.values())
    hs = [r["h"] for r in runs.values()]
    endpoint = max(float(np.abs(x - hs[0]).max()) for x in hs)
    T = 2 * (n // 4)
    r0 = runs[(0, 0, 0)]
    rec = {"n": n, "offsets": list(off), "own_signals": own.round(8).tolist(),
           "context_dependence_pct": round(100 * ctx, 4), "additivity_error_pct": round(100 * add, 4),
           "probe_reported_pct": PROBE[(n, off)],
           "distinct": len({tuple(np.round(r["Z"], 10)) for r in runs.values()}),
           "xmax": max(r["xmax"] for r in runs.values()), "m_peak": max(r["m_peak"] for r in runs.values()),
           "endpoint_max_state_diff": endpoint, "nine_term_reconstruction_residual": recon,
           "bath_s_at_T/2,T": [float(r0["bath"][T // 2]), float(r0["bath"][T])],
           "mean_devmass": float(r0["devmass"][1:].mean()), "k": n // 2,
           "worst_interaction": {"memory": i, "context_lo": list(lo), "context_hi": list(hi)},
           "single_bit_parts_on_own_column": single, "interaction_parts_on_own_column": inter}
    return rec


def main():
    out = []
    for n in (256, 512):
        for off in ((0, 0, 0), (0, 4, 8), (0, 8, 16)):
            r = one(n, off)
            print(json.dumps({kk: r[kk] for kk in ("n", "offsets", "own_signals", "context_dependence_pct",
                                                   "additivity_error_pct", "probe_reported_pct", "xmax", "m_peak",
                                                   "endpoint_max_state_diff", "bath_s_at_T/2,T", "mean_devmass")}))
            out.append(r)
    with open(os.path.join(HERE, "exp_verify_probe_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
