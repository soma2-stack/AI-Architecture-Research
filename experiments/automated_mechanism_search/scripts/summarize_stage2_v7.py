"""Descriptive summary of the official v7 Stage-2 run (reads runs/stage2_v7/ only; no evaluation).

Writes runs/stage2_v7/summary_by_class.json: label counts for constructor proposals by primary
class (C1 / C2 / C3, from construction.jsonl.gz) and for mutation / crossover offspring, Tier-1
quality and per-task effect distributions, and the archive cells."""
import collections
import gzip
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(HERE, "runs", "stage2_v7")


def _load(name):
    path = os.path.join(RUN, name)
    op = gzip.open if name.endswith(".gz") else open
    with op(path, "rt") as f:
        return [json.loads(line) for line in f]


def _q(vals):
    v = np.array([x for x in vals if x is not None], dtype=float)
    if not len(v):
        return {"n": 0}
    return {"n": int(len(v)), "max": float(v.max()), "p90": float(np.percentile(v, 90)),
            "median": float(np.median(v)), "min": float(v.min()), "n_ge_0.15": int((v >= 0.15).sum()),
            "n_gt_0": int((v > 0).sum())}


def main():
    recs = _load("records.jsonl.gz")
    cons = {c["pid"]: c for c in _load("construction.jsonl.gz")}
    groups = collections.defaultdict(list)
    for r in recs:
        c = cons.get(r["pid"])
        groups[("constructor", c["v6_class"]) if c else ("offspring", "-")].append(r)
    out = {"n_records": len(recs), "groups": {}}
    for (src, cls), rs in sorted(groups.items()):
        t1 = [r for r in rs if r["label"] == "TIER1_EVALUATED"]
        eff = collections.defaultdict(list)
        for r in t1:
            for t, e in (r["tier1"].get("effects") or {}).items():
                eff[t].append(e if isinstance(e, (int, float)) and np.isfinite(e) else None)
        out["groups"][f"{src}:{cls}"] = {
            "n": len(rs), "labels": dict(collections.Counter(r["label"] for r in rs)),
            "quality": _q([r["quality"] for r in t1]),
            "effects": {t: _q(v) for t, v in eff.items()},
            "tier1_pass_on_best": sum(bool(r["tier1"].get("tier1_pass_on_best")) for r in t1),
            "best_task": dict(collections.Counter(r["tier1"].get("best_task") for r in t1)),
        }
    arch = json.load(open(os.path.join(RUN, "archive.json")))
    out["archive"] = {k: {"pid": v["pid"], "quality": v["quality"], "best_task": v["tier1"].get("best_task"),
                          "tier1_pass_on_best": v["tier1"].get("tier1_pass_on_best"),
                          "constructor_class": (cons.get(v["pid"]) or {}).get("v6_class", "offspring")}
                      for k, v in arch.items()}
    with open(os.path.join(RUN, "summary_by_class.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps({g: {k: v[k] for k in ("n", "labels", "quality", "tier1_pass_on_best")}
                      for g, v in out["groups"].items()}, indent=1))
    print("archive cells:", len(arch))


if __name__ == "__main__":
    main()
