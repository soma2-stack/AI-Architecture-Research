"""
H.1g — Occam scaling law test.  Theory: time from proposal to certification T ~ (ln(M/alpha) + c)/g,
M = candidates proposed per window. So T should grow LINEARLY in ln(M) (not in M).
We vary proposals per 50-step slot k in {1,2,4,8,16} (M = 200k per 10k steps), pool size 40k,
and measure, for exact true-rule claims, the test delay = admission time - proposal time.
"""
import numpy as np, json, time, sys
from csl_experiment import Grower, RuleStream, CONFIGS
from multiprocessing import Pool

def job(args):
    k, seed, N = args
    cfg = CONFIGS["A_pilot"]
    st = RuleStream(cfg["d"], cfg["K"], cfg["lo"], cfg["hi"], cfg["drift"], 0.5, np.random.default_rng(seed))
    g = Grower(cfg["d"], "CSL", np.random.default_rng(seed + 12345), propose_k=k, max_pending=40 * k,
               adm_mode="score", ret_mode="statement", ret_detector="sr")
    for t in range(N):
        x, y, _ = st.step(); g.step(t, x, y)
    true_sets = {tuple(r["feats"]): abs(r["beta"]) for (_, r) in st.history}
    delays = [(ta - tb, true_sets[tuple(f)]) for (ta, f, tb) in g.born_log if tuple(f) in true_sets]
    spur = 0
    for (t, ev, f) in g.log:
        if ev == "admit" and not any(set(f) & a for a in st.active_feature_sets(t, 2000)):
            spur += 1
    return dict(k=k, seed=seed, alpha_c=g.alpha_c, test_delays=delays, spurious=spur)

if __name__ == "__main__":
    jobs = [(k, s, 20000) for k in [1, 2, 4, 8, 16] for s in range(1, 9)]
    t0 = time.time()
    with Pool(12) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open("occam_results.json", "w"), indent=1)
    print("done", time.time() - t0)
