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
Candidate budgets remain candidate budgets, not equal primitive-work budgets.
All methods now receive paired test demonstrations, and costs include library acquisition.
Validity notes and preserved-result limitations: ../EXPERIMENT_VALIDITY_REPAIRS.md.
"""
import json, sys, time, itertools, hashlib
import numpy as np
from common import pool_run

L = 6
PR = {"R": lambda x: x[::-1], "S": lambda x: [(v + 1) % 10 for v in x], "W": lambda x: x[1:] + x[:1],
      "M": lambda x: [(3 * v) % 10 for v in x], "X": lambda x: [x[1], x[0]] + x[2:]}


def run(prog, x, lib, stats=None):
    for op in prog:
        if op in PR:
            if stats is not None:
                stats["primitive_steps"] = stats.get("primitive_steps", 0) + 1
            x = PR[op](x)
        else:
            x = run(lib[op], x, lib, stats=stats)
    return x


def rx(rng):
    return [int(v) for v in rng.integers(0, 10, L)]


def task(prog, rng, lib, k=4):
    xs = [rx(rng) for _ in range(k)]
    return [(x, run(prog, x, lib)) for x in xs]


def search(demos, ops, lib, budget, stats=None):
    n = 0
    for d in range(1, 20):
        for prog in itertools.product(ops, repeat=d):
            if n >= budget:
                return None, n
            n += 1
            if stats is not None:
                stats["programs_evaluated"] = stats.get("programs_evaluated", 0) + 1
            if all(run(prog, list(x), lib, stats=stats) == y for x, y in demos):
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
    acquisition_start = time.perf_counter()
    acquisition_stats = {"programs_evaluated": 0, "primitive_steps": 0}
    sols = []
    for t in phase1:
        demos = task(t, rng, base)
        p, n = search(demos, prims, {}, budget, stats=acquisition_stats)
        if p is not None: sols.append(p)
    res["phase1_solved"] = len(sols) / len(phase1)
    phase1_secs = time.perf_counter() - acquisition_start
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
    acquisition_secs = time.perf_counter() - acquisition_start
    res["acquisition"] = dict(**acquisition_stats, secs=acquisition_secs,
                              compression_secs=acquisition_secs - phase1_secs)
    # Construct once, before the method loop: identical demonstrations and checks.
    cases = [(task(t, rng, base), [run(t, x, base) for x in fresh]) for t in tests]
    case_hash = hashlib.sha256(json.dumps(dict(cases=cases, fresh=fresh), sort_keys=True).encode()).hexdigest()
    res["test_instances_sha256"] = case_hash
    for name, ops, lib in [("flat", prims, {}), ("library", prims + list(learned), learned),
                           ("oracle_lib", prims + ["A"], base)]:
        ok, cost = [], []
        search_stats = {"programs_evaluated": 0, "primitive_steps": 0}
        verification_stats = {"primitive_steps": 0}
        test_start = time.perf_counter()
        for demos, expected in cases:
            p, n = search(demos, ops, lib, budget, stats=search_stats)
            good = p is not None and all(run(p, x, lib, stats=verification_stats) == y for x, y in zip(fresh, expected))
            ok.append(good); cost.append(n)
        test_secs = time.perf_counter() - test_start
        acq_secs = acquisition_secs if name == "library" else 0.
        acq_steps = acquisition_stats["primitive_steps"] if name == "library" else 0
        res[name] = dict(solved=float(np.mean(ok)), median_programs=float(np.median(cost)),
                         test_instances_sha256=case_hash, test_programs=search_stats["programs_evaluated"],
                         search_primitive_steps=search_stats["primitive_steps"],
                         verification_primitive_steps=verification_stats["primitive_steps"],
                         acquisition_secs=acq_secs, test_secs=test_secs,
                         total_secs=acq_secs + test_secs if name != "oracle_lib" else None,
                         total_primitive_steps=(acq_steps + search_stats["primitive_steps"] + verification_stats["primitive_steps"])
                                               if name != "oracle_lib" else None,
                         cost_scope="acquisition_plus_test; benchmark_case_generation_excluded",
                         oracle_knowledge_cost_unmeasured=name == "oracle_lib",
                         by_type={"AA": float(np.mean(ok[:5])), "APA": float(np.mean(ok[5:10])), "AAA": float(np.mean(ok[10:]))})
    return dict(seed=seed, budget=budget, res=res)


if __name__ == "__main__":
    jobs = [(s, b) for s in range(1, 7) for b in [10**5, 10**6]]
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print(job((1, 10**5))); sys.exit()
    res = pool_run(job, jobs, procs=int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    json.dump(res, open("e8_validity_results.json", "w"), indent=1)
    print("done")
