"""
Y.4c — removes the 'complete product' hint from Y.4. The world has 5 symbols x 4 styles but 4 of the 20
(symbol, style) combinations do not exist (16 surface forms). Pairs whose output would be a missing form never
occur. The search places the 16 observed surface forms injectively into a K x M grid with EMPTY cells allowed
(dummy placeholders), and MDL chooses (K, M) among all grids with 16 <= K*M <= 25 — including the complete
4 x 4 grid, which is the tempting wrong answer. True surface IDs are used (perception removed; Y.4 showed it is solved).
"""
import json, sys, math, time
import numpy as np
from common import pool_run
import y4_functional_symbols as Y


def world(seed, rho, K=5, M=4, drop=4):
    rng = np.random.default_rng(seed)
    T = Y.latin(rng, K)
    cells = [(k, m) for k in range(K) for m in range(M)]
    missing = set(map(tuple, np.array(cells)[rng.choice(len(cells), drop, replace=False)]))
    present = [c for c in cells if c not in missing]
    sid = {c: i for i, c in enumerate(present)}
    S = len(present)
    def out(a, b):
        (ka, ma), (kb, mb) = present[a], present[b]
        c = (int(T[ka, kb]), ma)
        return sid.get(c)
    pairs = [(a, b) for a in range(S) for b in range(S) if out(a, b) is not None]
    while True:
        m = rng.random(len(pairs)) < rho
        tr = [p for p, k in zip(pairs, m) if k]
        if len({a for a, b in tr}) == S and len({b for a, b in tr}) == S: break
    te = [p for p, k in zip(pairs, m) if not k]
    return S, out, tr, te, present


def search_grid(rel, S, K, M, rng, restarts=30, iters=250):
    # dummy ids S..K*M-1 are empty cells; they never occur in rel
    return Y.search_factorisation(rel, K * M, K, M, rng, restarts=restarts, iters=iters)


def job(args):
    seed, rho = args
    S, out, tr, te, present = world(seed, rho)
    rel = {(a, b): out(a, b) for a, b in tr}
    rng = np.random.default_rng(seed + 5)
    table = []
    for K in range(2, 9):
        for M in range(2, 9):
            if not (S <= K * M <= 25): continue
            sols = search_grid(rel, S, K, M, rng)
            best = max(sols, key=lambda z: z[0])
            exc = 2 * len(rel) - best[0]
            bits = S * math.log2(K * M) + len(best[2]) * math.log2(K) + len(best[3]) * math.log2(M) + exc * math.log2(S * S)
            table.append((bits, K, M, best))
    # trivial 'no structure' model: a table over surface pairs
    table.append((len(rel) * math.log2(S), 1, S, None))
    table.sort(key=lambda z: z[0])
    bits, K, M, best = table[0]
    if best is None:
        acc = 0.0
    else:
        pred = Y.predictor_from(best, K, M, np.random.default_rng(1))
        acc = float(np.mean([pred(a, b) == out(a, b) for a, b in te]))
    true_grid = next((t for t in table if t[1] == 5 and t[2] == 4), None)
    return dict(seed=seed, rho=rho, S=S, n_train=len(tr), n_test=len(te), chosen=[K, M], test_acc=acc,
                top3=[(round(t[0], 1), t[1], t[2]) for t in table[:3]],
                bits_true_5x4=round(true_grid[0], 1) if true_grid else None,
                bits_4x4=round(next(t[0] for t in table if t[1] == 4 and t[2] == 4), 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job((1, 0.35))); sys.exit()
    jobs = [(s, rho) for s in range(1, 6) for rho in [0.2, 0.35, 0.6]]
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    json.dump(res, open("y4c_results.json", "w"), indent=1)
    print("done")
