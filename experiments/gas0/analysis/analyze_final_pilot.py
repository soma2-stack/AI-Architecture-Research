"""Final-harness DEV pilot table, plan-first audit, gate and feedback-health audit.

One DEV project, one seed: descriptive only. No significance, synergy or superiority claim.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from analysis.analyze_postfix_pilot import audit_cell

RUN = Path(__file__).resolve().parent / "dev_pilot_qwen35_final_20260930"
EXCEPTION_LINE = re.compile(r"(^|\n)E +\w*(Error|Exception)\b|\b\w+(Error|Exception): ")
DATACLASS_CAUSE = re.compile(r"non-default argument '\w+' follows default argument")


def gate_audit(base: Path) -> dict:
    events, rollbacks, rollback_exc, dataclass, notices, valid, max_notice = {}, 0, 0, 0, 0, 0, 0
    decorator = 0
    per_stage = {}
    for stage in range(1, 9):
        log = base / f"stage{stage}.jsonl"
        if not log.exists():
            continue
        stage_events = {}
        for line in log.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            result = row.get("result")
            if row["type"] != "tool" or not isinstance(result, dict):
                continue
            if "notice" in result:
                notices += 1
                text = result["notice"]
                max_notice = max(max_notice, len(text))
                try:
                    payload = json.loads(text)
                    valid += 1
                except ValueError:
                    match = re.search(r'"event": "(\w+)"', text)
                    payload = {"event": match.group(1) if match else "?"}
                text = text.replace("\\n", "\n")
            elif "event" in result:
                payload, text = result, json.dumps(result).replace("\\n", "\n")
            else:
                continue
            event = payload.get("event", "?")
            events[event] = events.get(event, 0) + 1
            stage_events[event] = stage_events.get(event, 0) + 1
            if event == "REGRESSION_ROLLBACK":
                rollbacks += 1
                rollback_exc += bool(EXCEPTION_LINE.search(text))
                dataclass += bool(DATACLASS_CAUSE.search(text))
                decorator += "@dataclass" in text or "model.py:27" in text
        per_stage[stage] = stage_events
    ledger = base / "ledger_stage8.json"
    records = json.loads(ledger.read_text(encoding="utf-8"))["failures"] if ledger.exists() else []
    return {"gate_events": events, "per_stage": per_stage, "rollbacks": rollbacks,
            "rollbacks_showing_exception": rollback_exc,
            "rollbacks_with_dataclass_field_order_cause": dataclass,
            "rollbacks_through_model_py_27_dataclass_frame": decorator,
            "notices": notices, "valid_json_notices": valid, "max_notice_chars": max_notice,
            "failure_records": len(records),
            "failure_records_showing_exception": sum(bool(EXCEPTION_LINE.search(r["message_head"]))
                                                     for r in records),
            "max_failure_record_chars": max((len(r["message_head"]) for r in records), default=0),
            "max_failure_record_count": max((r["count"] for r in records), default=0)}


def hidden_by_stage(base: Path) -> list[str]:
    out = []
    for stage in range(1, 9):
        h = json.loads((base / f"stage{stage}_score.json").read_text(encoding="utf-8"))["hidden_tests"]
        out.append(f"{sum(v for k, v in h.items() if not k.startswith('Q'))}/"
                   f"{sum(1 for k in h if not k.startswith('Q'))}")
    return out


def main():
    summary = json.loads((RUN / "final_pilot_summary.json").read_text(encoding="utf-8"))
    table = {}
    for cell, result in summary["cells"].items():
        base = RUN / result["directory"]
        plan = audit_cell(base)
        res = result.get("resources", {})
        row = {
            "status": result["status"], "RPS": result.get("RPS"),
            "mean_stage_completion": result.get("mean_stage_completion"),
            "final_CR": result.get("final"), "requirement_retention": result.get("requirement_retention"),
            "declared_done_stages": result.get("declared_done_stages"),
            "model_calls": res.get("model_calls"), "test_executions": res.get("test_executions"),
            "prompt_tokens": res.get("prompt_tokens"), "completion_tokens": res.get("completion_tokens"),
            "peak_context_tokens": res.get("peak_context_tokens"),
            "gpu_seconds_upper_bound": res.get("gpu_seconds_upper_bound"),
            "episode_wall_seconds": result.get("episode_wall_elapsed_seconds"),
            "harness_format_errors": res.get("format_errors"),
            "plan_first_rejections": plan["plan_first_rejections"],
            "malformed_calls": plan["malformed_calls"],
            "malformed_recovered_next_call": plan["malformed_recovered_next_call"],
            "failed_or_timed_out_requests": result["gpu_cap"]["failed_requests"],
            "plan_first_audit": plan,
        }
        if result["status"] == "complete":
            row["hidden_pass_by_stage"] = hidden_by_stage(base)
        if cell in ("C2", "C3", "C4"):
            row["gate"] = gate_audit(base)
        table[cell] = row
    totals = {k: sum(r[k] or 0 for r in table.values())
              for k in ("model_calls", "prompt_tokens", "completion_tokens", "test_executions",
                        "gpu_seconds_upper_bound", "episode_wall_seconds")}
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
    out = {"note": "one DEV project, one seed: descriptive only; no significance, synergy, superiority, "
                   "VPS success or VPS failure claim",
           "cells": table, "totals": totals, "descriptive_differences": diffs,
           "verified_hashes": summary.get("verified_hashes")}
    (RUN / "final_pilot_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                                                   encoding="utf-8")
    brief = {c: {k: v for k, v in r.items() if k not in ("plan_first_audit",)} for c, r in table.items()}
    print(json.dumps(brief, indent=1))
    print(json.dumps(totals, indent=1))
    print(json.dumps(diffs, indent=1))


if __name__ == "__main__":
    main()
