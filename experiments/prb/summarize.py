import json, os, sys
import numpy as np
from collections import defaultdict


def z3():
    rows = []
    for f in ["z3_n5.jsonl", "z3_n7.jsonl", "z3_n9.jsonl"]:
        if os.path.exists(f):
            rows += [json.loads(l) for l in open(f)]
    g = defaultdict(list)
    for r in rows: g[(r["n"], r["m"])].append(r)
    conds = ("direct_map", "direct_told", "cot_map", "cot_told")
    for k in sorted(g):
        rs = g[k]
        line = f"n={k[0]} m={k[1]} (episodes {len(rs)}, nsol {[r['csp_n_solutions'] for r in rs]})"
        for c in conds:
            v = [r[c] for r in rs if not r[c].get("skipped")]
            acc = [x.get("acc") for x in v]; acc = [a if a is not None else 0.0 for a in acc]
            ms = [x.get("map_score") for x in v if x.get("map_score") is not None]
            cons = [x.get("code_consistent_with_demos") for x in v if x.get("code_consistent_with_demos") is not None]
            fol = [x.get("answers_follow_code") for x in v if x.get("answers_follow_code") is not None]
            unf = sum(1 for x in v if x.get("done") == "length")
            line += f"\n   {c:12s} acc {np.mean(acc):.2f}  map {np.mean(ms) if ms else float('nan'):.2f}  code-consistent {np.mean(cons) if cons else float('nan'):.2f}  answers-follow-code {np.mean(fol) if fol else float('nan'):.2f}  hit-limit {unf}  tokens {np.mean([x.get('eval_count') or 0 for x in v]):.0f}"
        print(line)


def z4():
    rows = [json.loads(l) for l in open("z4_n7.jsonl")] if os.path.exists("z4_n7.jsonl") else []
    g = defaultdict(list)
    for r in rows: g[r["m"]].append(r)
    for m in sorted(g):
        rs = g[m]
        print(f"m={m} episodes {len(rs)} digit {np.mean([r['digit_interface_acc'] for r in rs]):.2f} scorer-search unseen {np.mean([r['scorer_search_unseen_acc'] for r in rs]):.2f} nsol {[r['csp_n_solutions'] for r in rs]}")
        for meth in ("free", "sinkhorn"):
            v = [r[meth] for r in rs]
            print(f"   {meth:8s} train {np.mean([x['train_acc'] for x in v]):.2f} unseen {np.mean([x['unseen_acc'] for x in v]):.2f} "
                  f"map {np.mean([x['map_score'] for x in v]):.2f} bijection {sum(x['map_is_bijection'] for x in v)}/{len(v)} coherence {np.mean([x['coherence'] for x in v]):.2f} "
                  f"per-episode unseen {[round(x['unseen_acc'], 2) for x in v]}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "z3"): z3()
    if which in ("all", "z4"): z4()
