"""Predeclared Section 7 scores from per-test outcomes."""
from __future__ import annotations

from collections import defaultdict
from statistics import mean, median


def score_episode(stage_results: list[dict], manifest: dict):
    if len(stage_results) != 8:
        raise ValueError("episode must have eight scored stages")
    per_stage = []
    first_green = {}
    regressions = []
    text_probe_results = []
    for stage, result in enumerate(stage_results, 1):
        outcomes = result["hidden_tests"]
        current = [p for p in manifest["probes"] if p["introduced"] == stage
                   and (p.get("retired") is None or p["retired"] > stage)]
        active = [p for p in manifest["probes"] if p["introduced"] <= stage
                  and (p.get("retired") is None or p["retired"] > stage)]
        cur_ids = [i for p in current for i in p["tests"]]
        all_ids = [i for p in active for i in p["tests"]]
        if not cur_ids or not all_ids:
            raise ValueError(f"missing stage {stage} probes")
        sc = mean(bool(outcomes.get(i, False)) for i in cur_ids)
        cr = mean(bool(outcomes.get(i, False)) for i in all_ids)
        per_stage.append({"stage": stage, "SC": sc, "CR": cr})
        for test in all_ids:
            if outcomes.get(test, False):
                first_green.setdefault(test, stage)
            elif test in first_green and first_green[test] < stage:
                regressions.append({"test": test, "first_green": first_green[test],
                                    "red_stage": stage})
        for p in active:
            if p.get("text_only") and p["introduced"] < stage:
                text_probe_results.extend(bool(outcomes.get(i, False)) for i in p["tests"])
    return {"RPS": mean(s["CR"] for s in per_stage), "final": per_stage[-1]["CR"],
            "stages": per_stage, "regressions": regressions,
            "requirement_retention": mean(text_probe_results) if text_probe_results else None}


def recovery(failure_events: list[dict]):
    recovered = [e for e in failure_events if e.get("recovered")]
    return {"probability": len(recovered) / len(failure_events) if failure_events else None,
            "median_calls": median(e["calls_to_recover"] for e in recovered) if recovered else None}
