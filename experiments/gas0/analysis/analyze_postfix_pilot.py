"""Descriptive table and plan-first audit for the post-fix DEV pilot. One seed: no inference."""
from __future__ import annotations

import json
from pathlib import Path

RUN = Path(__file__).resolve().parent / "dev_pilot_qwen35_postfix_20260929"
PLAN_REJECTION = "first action must be plan"


def _rows(base: Path, stage: int):
    log = base / f"stage{stage}.jsonl"
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []


def _accepted_plan(row) -> bool:
    return row["name"] == "plan" and not (isinstance(row["result"], dict) and "error" in row["result"])


def audit_cell(base: Path) -> dict:
    stages, malformed, recovered, plan_rejections = {}, 0, 0, 0
    for stage in range(1, 9):
        tools = [row for row in _rows(base, stage) if row["type"] == "tool"]
        if not tools:
            continue
        executed = [row for row in tools if row["name"] != "format_error"]
        accepted = next((i for i, row in enumerate(tools) if _accepted_plan(row)), None)
        before = tools[:accepted] if accepted is not None else tools
        stages[stage] = {
            "first_call_plan": _accepted_plan(tools[0]),
            "first_executed_action": executed[0]["name"] if executed else None,
            "accepted_plan_at_call": tools[accepted]["call"] if accepted is not None else None,
            "non_plan_executed_before_plan": sum(row["name"] not in ("format_error", "plan")
                                                 for row in before),
            "plan_rejections": sum(row["name"] == "format_error"
                                   and row["result"].get("error") == PLAN_REJECTION for row in tools),
        }
        plan_rejections += stages[stage]["plan_rejections"]
        for index, row in enumerate(tools):
            if row["name"] != "format_error" or row["result"].get("error") == PLAN_REJECTION:
                continue
            malformed += 1
            nxt = tools[index + 1] if index + 1 < len(tools) else None
            recovered += bool(nxt and nxt["name"] != "format_error")
    held = all(s["non_plan_executed_before_plan"] == 0 and
               s["first_executed_action"] in ("plan", None) for s in stages.values())
    return {"attempted_stages": len(stages), "plan_first_enforced_every_stage": held,
            "stages_first_executed_plan": sum(s["first_executed_action"] == "plan" for s in stages.values()),
            "stages_plan_on_first_call": sum(s["first_call_plan"] for s in stages.values()),
            "stages_without_accepted_plan": [k for k, s in stages.items() if s["accepted_plan_at_call"] is None],
            "plan_first_rejections": plan_rejections,
            "malformed_calls": malformed, "malformed_recovered_next_call": recovered,
            "stages": stages}


def main():
    summary = json.loads((RUN / "postfix_pilot_summary.json").read_text(encoding="utf-8"))
    table = {}
    for cell, result in summary["cells"].items():
        base = RUN / result["directory"]
        audit = audit_cell(base)
        res = result.get("resources", {})
        table[cell] = {
            "status": result["status"],
            "RPS": result.get("RPS"),
            "mean_stage_completion": result.get("mean_stage_completion"),
            "final_CR": result.get("final"),
            "requirement_retention": result.get("requirement_retention"),
            "declared_done_stages": result.get("declared_done_stages"),
            "model_calls": res.get("model_calls"),
            "test_executions": res.get("test_executions"),
            "harness_format_errors": res.get("format_errors"),
            "plan_first_rejections": audit["plan_first_rejections"],
            "malformed_calls": audit["malformed_calls"],
            "malformed_recovered_next_call": audit["malformed_recovered_next_call"],
            "prompt_tokens": res.get("prompt_tokens"),
            "completion_tokens": res.get("completion_tokens"),
            "peak_context_tokens": res.get("peak_context_tokens"),
            "gpu_seconds_upper_bound": res.get("gpu_seconds_upper_bound"),
            "gpu_cap_charged_seconds": result["gpu_cap"]["charged_seconds"],
            "episode_wall_seconds": result.get("episode_wall_elapsed_seconds"),
            "plan_first_audit": audit,
        }
    complete = {c: r for c, r in table.items() if r["status"] == "complete"}
    diffs = {}
    for metric in ("RPS", "mean_stage_completion", "final_CR", "requirement_retention"):
        v = {c: r[metric] for c, r in complete.items() if r[metric] is not None}
        d = {f"{c}-C0": v[c] - v["C0"] for c in ("C1", "C2", "C3", "C4") if c in v and "C0" in v}
        if {"C4", "C3"} <= v.keys():
            d["C4-C3"] = v["C4"] - v["C3"]
        if {"C4", "C1", "C2"} <= v.keys():
            d["C4-max(C1,C2)"] = v["C4"] - max(v["C1"], v["C2"])
        diffs[metric] = d
    out = {"note": "one seed, one DEV project: descriptive only; no significance, synergy or improvement claim",
           "cells": table, "descriptive_differences": diffs,
           "cumulative_charged_gpu_seconds": summary.get("cumulative_charged_gpu_seconds"),
           "gpu_cap_seconds": summary["gpu_cap_seconds"],
           "aborted_attempts": [{k: a.get(k) for k in ("cell", "status", "error", "directory")}
                                for a in summary.get("aborted_attempts", [])]}
    (RUN / "postfix_pilot_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                                                     encoding="utf-8")
    print(json.dumps({c: {k: v for k, v in r.items() if k != "plan_first_audit"} for c, r in table.items()},
                     indent=1))
    print(json.dumps(diffs, indent=1))
    print({c: {k: r["plan_first_audit"][k] for k in ("attempted_stages", "plan_first_enforced_every_stage",
                                                      "stages_first_executed_plan", "stages_plan_on_first_call",
                                                      "stages_without_accepted_plan")} for c, r in table.items()})


if __name__ == "__main__":
    main()
