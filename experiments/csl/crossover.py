"""
H.1q — Crossover map: when does certified sequential structure learning (CSL-score) beat a joint sparse fit?
Vary the number of base features d (candidates = d + d(d-1)/2) and the number of true rules K.
CSL-score + SR retirement vs dense online L1-logistic over all candidates, with the L1 hyperparameters
chosen per cell as the BEST of a grid (favours the baseline). Metric: regret vs oracle (avg log-loss).
"""
import numpy as np, json, time, itertools
from csl_experiment import run
from multiprocessing import Pool

DS, KS, SEEDS = [20, 40, 80], [2, 4, 8, 16], [1, 2, 3, 4]
L1GRID = [dict(lr=lr, l1=l1) for lr in [0.001, 0.003] for l1 in [1e-4, 1e-3]]


def job(args):
    d, K, seed, pol, kw = args
    cfg = dict(d=d, K=K, lo=0.7, hi=1.4, drift=6000)
    r = run(cfg, pol, seed, 30000, **kw)
    r.update(d=d, K=K, kw=kw)
    return r


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "dense":
        cells = [(10, K) for K in [4, 8, 16, 24, 32]] + [(20, K) for K in [16, 32, 48, 64]]
        jobs = []
        for (d, K), s in itertools.product(cells, SEEDS):
            jobs.append((d, K, s, "CSL", dict(propose_k=1, adm_mode="score", ret_mode="statement", ret_detector="sr")))
            jobs.append((d, K, s, "ORACLE", {}))
            for kw in L1GRID + [dict(lr=0.01, l1=1e-4), dict(lr=0.01, l1=1e-3)]:
                jobs.append((d, K, s, "L1", kw))
        t0 = time.time()
        with Pool(12) as p:
            res = p.map(job, jobs, chunksize=1)
        json.dump(res, open("crossover_dense.json", "w"), indent=1)
        print("done", time.time() - t0); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "eg2":
        cells = [(20, 4), (40, 4), (80, 4), (20, 16), (40, 16), (80, 16)]
        grid = [dict(eta=e, U=U, gamma=g) for e in [0.12, 0.25, 0.5] for U in [8.0, 16.0, 32.0] for g in [1e-4]]
        jobs = [(d, K, s, "EG", kw) for (d, K) in cells for s in SEEDS for kw in grid]
        with Pool(12) as p:
            res = p.map(job, jobs, chunksize=1)
        json.dump(res, open("crossover_eg2.json", "w"), indent=1)
        print("done"); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "eg":
        cells = [(10, 4), (10, 16), (10, 32), (20, 4), (20, 16), (20, 32), (20, 64), (40, 4), (40, 16), (80, 4), (80, 16)]
        grid = [dict(eta=e, U=U, gamma=1e-4) for e in [0.03, 0.06, 0.12] for U in [4.0, 8.0]]
        jobs = [(d, K, s, "EG", kw) for (d, K) in cells for s in SEEDS for kw in grid]
        t0 = time.time()
        with Pool(12) as p:
            res = p.map(job, jobs, chunksize=1)
        json.dump(res, open("crossover_eg.json", "w"), indent=1)
        print("done", time.time() - t0); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "extra":
        jobs = [(d, K, s, "L1", kw) for d, K, s in itertools.product(DS, KS, SEEDS)
                for kw in [dict(lr=0.01, l1=1e-4), dict(lr=0.01, l1=1e-3)]]
        with Pool(12) as p:
            res = p.map(job, jobs, chunksize=1)
        json.dump(res, open("crossover_extra_l1.json", "w"), indent=1)
        print("done"); sys.exit()
    jobs = []
    for d, K, s in itertools.product(DS, KS, SEEDS):
        jobs.append((d, K, s, "CSL", dict(propose_k=1, adm_mode="score", ret_mode="statement", ret_detector="sr")))
        jobs.append((d, K, s, "ORACLE", {}))
        for kw in L1GRID:
            jobs.append((d, K, s, "L1", kw))
    t0 = time.time()
    with Pool(12) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open("crossover_results.json", "w"), indent=1)
    print("done", time.time() - t0)
