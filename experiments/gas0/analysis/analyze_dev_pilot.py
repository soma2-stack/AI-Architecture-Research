from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "experiments/gas0/analysis/dev_pilot_qwen35_20260929"
summary = json.loads((RUN / "pilot_summary.json").read_text(encoding="utf-8"))
cell_dirs = {"C1": "C1_dev_arena_seed1_retry_after_empty_ledger_fix",
             "C4": "C4_dev_arena_seed1_retry_after_empty_commit_fix"}
rows = {}
for cell, result in summary["cells"].items():
    folder = cell_dirs.get(cell, f"{cell}_dev_arena_seed1")
    base = RUN / folder
    events = []
    plan_ok, plan_total = [], 0
    all_tools = []
    for log in sorted(base.glob("stage*.jsonl")):
        stage = int(log.stem.removeprefix("stage"))
        items = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        ts = [x for x in items if x.get("type") == "tool"]
        all_tools.extend(ts)
        if ts:
            first = ts[0]
            ok = first.get("name") == "plan"
            plan_total += 1
            if ok: plan_ok.append(stage)
        for item in ts:
            r = item.get("result")
            failures = r.get("failed", {}) if isinstance(r, dict) else {}
            if isinstance(r, dict) and "notice" in r:
                try: failures = json.loads(r["notice"]).get("failed", {})
                except (ValueError, TypeError):
                    failures = {m: "truncated notice" for m in re.findall(r"tests[/\\][^'\" ]+\.py::[A-Za-z_0-9]+", r["notice"])}
            if isinstance(failures, dict) and failures:
                events.append({"stage": stage, "call": item.get("call"), "tests": sorted(failures)})
    streak = {}
    repeated = set()
    for event in events:
        failed = set(event["tests"])
        for test in list(streak):
            if test not in failed: streak[test] = 0
        for test in failed:
            streak[test] = streak.get(test, 0) + 1
            if streak[test] >= 3: repeated.add(test)
    bad_indexes = [i for i, item in enumerate(all_tools) if item.get("name") == "format_error"]
    recovered = sum(any(item.get("name") != "format_error" for item in all_tools[i + 1:])
                    for i in bad_indexes)
    scores = []
    for file in sorted(base.glob("stage*_score.json")):
        scores.append(json.loads(file.read_text(encoding="utf-8")))
    models = [x for log in sorted(base.glob("stage*.jsonl"))
              for x in (json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip())
              if x.get("type") == "model"]
    first_violations = []
    for log in sorted(base.glob("stage*.jsonl")):
        stage = int(log.stem.removeprefix("stage"))
        first = next((x for x in all_tools if x.get("stage") == stage), None)
        if first and first.get("name") != "plan": first_violations.append(stage)
    rows[cell] = {
        "status": result.get("status"), "RPS": result.get("RPS"),
        "mean_stage_completion": result.get("mean_stage_completion"),
        "final_CR": result.get("final"), "requirement_retention": result.get("requirement_retention"),
        "regressions": result.get("regressions"), "scored_stages": len(scores),
        "stage_metrics": [{"stage": s.get("stage"), "SC": s.get("SC"), "CR": s.get("CR"),
                           "calls": s.get("calls"),
                           "agent_loop_errors": s.get("format_errors"),
                           "test_executions": s.get("test_executions"), "done": s.get("done")}
                          for s in scores],
        "agent_loop_error_count_scored": sum(int(s.get("format_errors", 0)) for s in scores),
        "format_error_events_in_raw_logs": sum(t.get("name") == "format_error" for t in all_tools),
        "format_error_recoveries": recovered,
        "first_action_plan_pass_stages": plan_ok, "first_action_plan_total_stages": plan_total,
        "first_action_plan_violations": first_violations,
        "repeated_failure_test_ids_observed": sorted(repeated),
        "failure_event_count": len(events), "repeated_failure_limitations": "Identical normalized diff-hunk recurrence is not derivable from the JSONL schema.",
        "model_calls_logged": len(models),
        "prompt_tokens": sum(m["usage"]["prompt_tokens"] for m in models),
        "completion_tokens": sum(m["usage"]["completion_tokens"] for m in models),
        "peak_context_tokens": max((m["usage"]["peak_context_tokens"] for m in models), default=0),
        "gpu_seconds_upper_bound_logged": sum(m["usage"]["wall_seconds"] for m in models),
        "test_executions_scored": sum(int(s.get("test_executions", 0)) for s in scores),
        "wall_seconds": result.get("episode_wall_elapsed_seconds"),
        "harness_or_runtime_error": result.get("error"),
    }
get = lambda c: rows[c]["RPS"]
contrasts = {"C1_minus_C0": get("C1")-get("C0"), "C2_minus_C0": get("C2")-get("C0"),
             "C3_minus_C0": get("C3")-get("C0"), "C4_minus_C0": None,
             "C4_minus_C3": None, "C4_minus_max_C1_C2": None}
partial_test_executions = {}
aborted_attempt_audit = []
for attempt_index, attempt in enumerate(summary.get("aborted_attempts", []), start=1):
    cell = attempt["cell"]
    base = RUN / f"{cell}_dev_arena_seed1"
    tool_rows = [json.loads(line) for log in sorted(base.glob("stage*.jsonl"))
                 for line in log.read_text(encoding="utf-8").splitlines() if line.strip()
                 for _ in [0] if json.loads(line).get("type") == "tool"]
    bad = [i for i, item in enumerate(tool_rows) if item.get("name") == "format_error"]
    aborted_attempt_audit.append({
        "cell": cell, "attempt_index": attempt_index, "error": attempt.get("error"),
        "model_calls": attempt.get("resources", {}).get("model_calls"),
        "gpu_seconds_upper_bound": attempt.get("resources", {}).get("gpu_seconds_upper_bound"),
        "format_error_events": len(bad),
        "format_error_recoveries": sum(any(item.get("name") != "format_error" for item in tool_rows[i + 1:])
                                        for i in bad),
    })
    scored = {int(p.stem[5:-6]) for p in base.glob("stage*_score.json")}
    count = 0
    for log in base.glob("stage*.jsonl"):
        stage = int(log.stem.removeprefix("stage"))
        if stage in scored:
            continue
        items = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        count += sum(item.get("type") == "tool" and item.get("name") in {
            "run_tests", "edit_file", "delete_file", "undo_last_edit"
        } for item in items)
        if cell in {"C2", "C3", "C4"}:
            count += 1  # cumulative visible-test gate at stage start
    partial_test_executions[f"{cell}:aborted_attempt_{attempt_index}"] = count
for cell, result in summary["cells"].items():
    if result.get("status") != "aborted" or cell not in cell_dirs:
        continue
    base = RUN / cell_dirs[cell]
    scored = {int(p.stem[5:-6]) for p in base.glob("stage*_score.json")}
    unscored = set(range(1, 9)) - scored
    partial_test_executions[f"{cell}:final_aborted_attempt"] = len(unscored) if cell in {"C2", "C3", "C4"} else 0
    base = RUN / cell_dirs[cell]
    tool_rows = [json.loads(line) for log in sorted(base.glob("stage*.jsonl"))
                 for line in log.read_text(encoding="utf-8").splitlines() if line.strip()
                 for _ in [0] if json.loads(line).get("type") == "tool"]
    bad = [i for i, item in enumerate(tool_rows) if item.get("name") == "format_error"]
    aborted_attempt_audit.append({
        "cell": cell, "attempt_index": "final", "error": result.get("error"),
        "model_calls": result.get("resources", {}).get("model_calls"),
        "gpu_seconds_upper_bound": result.get("resources", {}).get("gpu_seconds_upper_bound"),
        "format_error_events": len(bad),
        "format_error_recoveries": sum(any(item.get("name") != "format_error" for item in tool_rows[i + 1:])
                                        for i in bad),
    })
report = {"protocol":"GAS-0 Candidate A / one-seed dev_arena pilot", "seed":1,
          "frozen_model_commit":summary["frozen_model_commit"], "frozen_config_sha256":summary["frozen_config_sha256"],
          "cells":rows, "contrasts":contrasts, "aborted_attempts":aborted_attempt_audit,
          "partial_test_executions_by_aborted_attempt":partial_test_executions,
          "cumulative_gpu_seconds_upper_bound_including_aborts":summary["cumulative_gpu_seconds_upper_bound"],
          "gpu_cap_seconds":summary["gpu_cap_seconds"],
          "all_five_cells_complete":False, "evaluation_projects_used":False, "phase_2_run":False,
          "error_count_semantics":"stage*_score.json format_errors is the agent-loop errors counter; code increments it for both structured-call validation failures and valid tool execution exceptions. format_error_events_in_raw_logs counts only entries actually logged as the format_error tool.",
          "readiness":"NOT READY. C4 remained incomplete after a local llama.cpp connection timeout. A complete C4 restart exceeds the remaining GPU cap. The frozen plan-first rule was also bypassed after invalid first actions in multiple stages.",
          "plan_rule_detail":"Harness enforces plan only when calls == 1. If the first response is invalid/non-plan, a later valid non-plan action proceeds; first tool events show the bypass.",
          "interpretation":"One-seed pilot diagnostics only; no statistical synergy claim."}
out = RUN / "pilot_analysis.json"
out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
print(json.dumps({"contrasts":contrasts, "cumulative_gpu_seconds":summary["cumulative_gpu_seconds_upper_bound"],
                  "cells":{c:{"status":v["status"],"RPS":v["RPS"],"SC":v["mean_stage_completion"],
                             "CR":v["final_CR"],"retention":v["requirement_retention"],
                             "scored_stages":v["scored_stages"],"calls":v["model_calls_logged"],
                             "agent_loop_errors":v["agent_loop_error_count_scored"],"raw_format_errors":v["format_error_events_in_raw_logs"],
                             "format_recoveries":v["format_error_recoveries"],"plan_pass":len(v["first_action_plan_pass_stages"]),
                             "plan_total":v["first_action_plan_total_stages"],"repeated":v["repeated_failure_test_ids_observed"]}
                           for c,v in rows.items()}}, indent=2))
