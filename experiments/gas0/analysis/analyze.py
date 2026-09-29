"""Frozen Section 10 project-cluster bootstrap and decision metrics."""
from __future__ import annotations

import math
import random
from statistics import mean


def logit(x, epsilon=1e-4):
    x = min(max(x, epsilon), 1 - epsilon)
    return math.log(x / (1 - x))


def aggregate(rows, scale=lambda x: x):
    by = {}
    for r in rows:
        by.setdefault((r["project"], r["cell"]), []).append(scale(r["RPS"]))
    projects = sorted({r["project"] for r in rows})
    cells = ["C0", "C1", "C2", "C3", "C4"]
    return {c: mean(mean(by[p, c]) for p in projects) for c in cells}


def contrasts(m):
    ds, dv, dsv = m["C1"] - m["C0"], m["C2"] - m["C0"], m["C4"] - m["C0"]
    return {"delta_s": ds, "delta_v": dv, "delta_sv": dsv,
            "interaction": dsv - ds - dv, "coupling": m["C4"] - m["C3"],
            "beyond_best_single": m["C4"] - max(m["C1"], m["C2"])}


def bootstrap(rows, n=10000, seed=0, scale=lambda x: x):
    projects = sorted({r["project"] for r in rows})
    grouped = {(p, c): [r for r in rows if r["project"] == p and r["cell"] == c]
               for p in projects for c in ["C0", "C1", "C2", "C3", "C4"]}
    if any(not v for v in grouped.values()):
        raise ValueError("incomplete project-cell matrix")
    rng = random.Random(seed)
    samples = {key: [] for key in contrasts(aggregate(rows)).keys()}
    for _ in range(n):
        sample = rng.choices(projects, k=len(projects))
        m = {c: mean(mean(scale(rng.choice(grouped[p, c])["RPS"]) for _ in range(len(grouped[p, c])))
                     for p in sample)
             for c in ["C0", "C1", "C2", "C3", "C4"]}
        for key, value in contrasts(m).items():
            samples[key].append(value)
    return {key: (sorted(values)[int(0.05*n)], sorted(values)[int(0.95*n)])
            for key, values in samples.items()}


def classify(rows):
    m = aggregate(rows)
    d = contrasts(m)
    ci = bootstrap(rows)
    threshold = max(0.05, 0.25*(abs(d["delta_s"])+abs(d["delta_v"])))
    if d["interaction"] <= -0.05 and ci["interaction"][1] < 0:
        verdict = "NEGATIVE INTERACTION"
    elif (d["interaction"] >= threshold and ci["interaction"][0] > 0 and
          d["beyond_best_single"] > 0 and ci["beyond_best_single"][0] > 0):
        verdict = "POSITIVE SYNERGY"
    elif d["beyond_best_single"] > 0 and ci["beyond_best_single"][0] > 0:
        verdict = "ADDITIVE BENEFIT"
    else:
        verdict = "NO SYNERGY"
    coupling = ("COUPLING MATTERS" if d["coupling"] >= 0.05 and ci["coupling"][0] > 0
                else "CO-PRESENCE SUFFICES" if ci["coupling"][0] <= 0 <= ci["coupling"][1]
                else "INCONCLUSIVE COUPLING")
    return {"means": m, "contrasts": d, "ci90": ci, "verdict": verdict,
            "coupling": coupling}
