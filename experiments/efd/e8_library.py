"""
E8 — acquiring a reusable abstraction across tasks (library learning) vs flat search.
DSL on digit strings of length 6: R reverse, S +1 mod 10, W rotate-left, M x3 mod 10, X swap positions 0,1.
A hidden abstraction A = a fixed depth-4 composition (random per seed, non-trivial).
Phase 1 ("experience"): 12 tasks of the form A∘P or P∘A (P a single primitive), 4 demos each.
Test: tasks A∘A (depth 8), A∘P∘A (9), A∘A∘A (12), each with 4 demos.
Learners (all search-based; budget = max programs evaluated per task):
  flat          : breadth-first enumeration over the 5 primitives, up to the budget
  library       : solve phase-1 tasks by flat search, then add the most frequent contiguous sub-program
                  (length 2..4) across the phase-1 solutions to the library (compression, DreamCoder-style);
                  search test tasks over primitives + library
  oracle_lib    : library contains A itself (upper bound)
Metric: fraction of test tasks solved (a program consistent with the demos that also generalises to 20 fresh inputs).
"""
import json, sys, time, itertools
import numpy as np
from common import pool_run

L = 6
PR = {"R": lambda x: x[::-1], "S": lambda x: [(v + 1) % 10 for v in x], "W": lambda x: x[1:] + x[:1],
      "M": lambda x: [(3 * v) % 10 for v in x], "X": lambda x: [x[1], x[0]] + x[2:]}


def run(prog, x, lib):
    for op in prog:
        if op in PR:
            x = PR[op](x)
        else:
            x = run(lib[op], x, lib)
    return x


def rx(rng):
    return [int(v) for v in rng.integers(0, 10, L)]


def task(prog, rng, lib, k=4):
    xs = [rx(rng) for _ in range(k)]
    return [(x, run(prog, x, lib)) for x in xs]


def search(demos, ops, lib, budget):
    n = 0
    for d in range(1, 20):
        for prog in itertools.product(ops, repeat=d):
            n += 1
            if n > budget:
                return None, n
            if all(run(prog, list(x), lib) == y for x, y in demos):
                return prog, n
    return None, n


def expand(prog, lib):
    out = []
    for op in prog:
        out += expand(lib[op], lib) if op in lib else [op]
    return out


def job(args):
    seed, budget = args
    rng = np.random.default_rng(seed)
    prims = list(PR)
    # hidden abstraction: depth-4, not reducible to a shorter program on random inputs
    while True:
        A = tuple(prims[int(i)] for i in rng.integers(0, 5, 4))
        xs = [rx(rng) for _ in range(30)]
        tgt = [run(A, x, {}) for x in xs]
        shorter = any(all(run(p, x, {}) == t for x, t in zip(xs, tgt)) for d in range(1, 4) for p in itertools.product(prims, repeat=d))
        if not shorter: break
    base = {"A": A}
    phase1 = [(("A", p) if i % 2 else (p, "A")) for i, p in enumerate(prims + prims + prims[:2])]
    tests = [("A", "A")] * 5 + [("A", p, "A") for p in prims] + [("A", "A", "A")] * 5
    fresh = [rx(rng) for _ in range(20)]
    res = {}
    # phase 1 by flat search
    sols = []
    for t in phase1:
        demos = task(t, rng, base)
        p, n = search(demos, prims, {}, budget)
        if p is not None: sols.append(p)
    res["phase1_solved"] = len(sols) / len(phase1)
    # compression (MDL-style, as in DreamCoder/Stitch, simplified): repeatedly add the contiguous sub-program with
    # the largest description-length saving count*(len-1), rewrite the solutions with it, up to 2 abstractions
    learned = {}
    cur = [list(p) for p in sols]
    for it in range(2):
        counts = {}
        for p in cur:
            seen = set()
            for l in range(2, 5):
                for i in range(len(p) - l + 1):
                    sub = tuple(p[i:i + l])
                    if sub not in seen:
                        counts[sub] = counts.get(sub, 0) + 1; seen.add(sub)
        cands = [(c * (len(k) - 1), k) for k, c in counts.items() if c >= 2]
        if not cands: break
        gain, best = max(cands)
        name = f"L{it+1}"; learned[name] = best
        new_cur = []
        for p in cur:
            q, i = [], 0
            while i < len(p):
                if tuple(p[i:i + len(best)]) == best: q.append(name); i += len(best)
                else: q.append(p[i]); i += 1
            new_cur.append(q)
        cur = new_cur
    res["learned_abstractions"] = {k: "".join(expand(v, learned)) for k, v in learned.items()}
    res["true_abstraction"] = "".join(A)
    for name, ops, lib in [("flat", prims, {}), ("library", prims + list(learned), learned),
                           ("oracle_lib", prims + ["A"], base)]:
        ok, cost = [], []
        for t in tests:
            demos = task(t, rng, base)
            p, n = search(demos, ops, lib, budget)
            good = p is not None and all(run(p, x, lib) == run(t, x, base) for x in fresh)
            ok.append(good); cost.append(n)
        res[name] = dict(solved=float(np.mean(ok)), median_programs=float(np.median(cost)),
                         by_type={"AA": float(np.mean(ok[:5])), "APA": float(np.mean(ok[5:10])), "AAA": float(np.mean(ok[10:]))})
    return dict(seed=seed, budget=budget, res=res)


if __name__ == "__main__":
    jobs = [(s, b) for s in range(1, 7) for b in [10**5, 10**6]]
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job((1, 10**5))); sys.exit()
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    json.dump(res, open("e8_results.json", "w"), indent=1)
    print("done")
