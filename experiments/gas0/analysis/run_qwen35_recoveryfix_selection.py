"""Run the authorized from-scratch Qwen3.5 C0 selection screen only.

This script is intentionally limited to dev_arena and budget_planner, seed 1.
It is not a C0-C4 pilot and never opens an evaluation project.
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "gas0"))

from experiments.gas0.harness.agent_loop import run_episode  # noqa: E402
from experiments.gas0.harness.llm_client import LlamaClient  # noqa: E402


ANALYSIS = ROOT / "experiments" / "gas0" / "analysis"
RUN_ROOT = ANALYSIS / "model_selection_recoveryfix_20260929"
MODEL_ALIAS = "qwen3.5-9b-q6k"
PROJECTS = ("dev_arena", "budget_planner")


def _save(report):
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    target = RUN_ROOT / "model_selection.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _format_error_counts(run_dir: Path):
    failures = recoveries = 0
    for stage in range(1, 9):
        path = run_dir / f"stage{stage}.jsonl"
        if not path.exists():
            continue
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        for index, row in enumerate(rows):
            if row.get("type") == "tool" and row.get("name") == "format_error":
                failures += 1
                next_tool = next((candidate for candidate in rows[index + 1:]
                                  if candidate.get("type") == "tool"), None)
                if next_tool and next_tool.get("name") != "format_error":
                    recoveries += 1
    return {"format_error_records": failures, "recovered_on_next_call": recoveries}


def main():
    prior = json.loads((ANALYSIS / "model_selection_amended_20260929.json").read_text(encoding="utf-8"))
    candidate = prior["candidates"][0]
    preflight = json.loads((ANALYSIS / "qwen35_malformed_recovery_preflight_20260929.json").read_text(encoding="utf-8"))
    if not preflight.get("passed"):
        raise RuntimeError("malformed-call synthetic preflight did not pass")

    client = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=300)
    context = client.check_context(16384)
    if context != 16384:
        raise RuntimeError(f"unexpected per-slot context: {context}")

    report = {
        "date": "2026-09-29",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "model": candidate["model"],
        "model_repo": candidate["model_repo"],
        "model_revision": candidate["model_revision"],
        "gguf_repo": candidate["gguf_repo"],
        "gguf_revision": candidate["gguf_revision"],
        "gguf_file": candidate["gguf_file"],
        "gguf_sha256": candidate["gguf_sha256"],
        "quantization": "Q6_K",
        "runtime": prior["runtime"],
        "active_template_sha256": preflight["active_template_sha256"],
        "selection_protocol": {
            "condition": "C0",
            "projects": list(PROJECTS),
            "seed": 1,
            "context_tokens_per_sequence": context,
            "parallel": 1,
            "parallel_tool_calls": False,
            "max_calls_per_stage": 30,
            "max_completion_tokens_per_call": 1024,
            "temperature": 0.2,
            "top_p": 0.95,
            "max_test_executions_per_stage": 40,
            "stage_limit_minutes": 20,
            "budget_planner_rps_gate": [0.2, 0.8],
            "context_serialization_commit": "aaaf80acfac62d9533ddc4b9e2a15fff5752fb63",
            "tool_recovery_commit": "a50c678edb338a152961288269a2adf7e7810a35",
        },
        "synthetic_recovery_preflight": "qwen35_malformed_recovery_preflight_20260929.json",
        "per_sequence_context": context,
        "projects": {},
        "eligible": False,
        "frozen_config_created": False,
        "C0_C4_pilot_run": False,
        "evaluation_projects_used": False,
        "phase_2_run": False,
    }
    _save(report)

    for project_name in PROJECTS:
        output = RUN_ROOT / "qwen35" / f"{project_name}_seed1"
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite prior run: {output}")
        started = time.monotonic()
        print(f"START {project_name}", flush=True)
        try:
            metrics = run_episode(
                ROOT / "experiments" / "gas0" / "bench" / project_name,
                "C0", 1, client, output, 9_000_000_000,
            )
            metrics["status"] = "complete"
            metrics["episode_wall_elapsed_seconds"] = time.monotonic() - started
            metrics["format_error_recovery"] = _format_error_counts(output)
            report["projects"][project_name] = metrics
            print(
                f"DONE {project_name} RPS={metrics['RPS']:.9f} "
                f"calls={metrics['resources']['model_calls']} "
                f"gpu_seconds_upper_bound={metrics['resources']['gpu_seconds_upper_bound']:.3f}",
                flush=True,
            )
        except Exception as exc:
            report["projects"][project_name] = {
                "status": "aborted",
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
                "partial_run_dir": str(output),
                "format_error_recovery": _format_error_counts(output) if output.exists() else {},
                "episode_wall_elapsed_seconds": time.monotonic() - started,
            }
            print(f"ABORT {project_name}: {report['projects'][project_name]['error']}", flush=True)
        _save(report)

    dev = report["projects"].get("dev_arena", {})
    budget = report["projects"].get("budget_planner", {})
    report["eligible"] = (
        dev.get("status") == "complete"
        and budget.get("status") == "complete"
        and 0.20 <= budget.get("RPS", -1) <= 0.80
    )
    report["status"] = "complete" if all(
        report["projects"].get(name, {}).get("status") == "complete" for name in PROJECTS
    ) else "selection_failed"
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["decision"] = (
        "eligible; freeze Qwen3.5 and stop before C0-C4"
        if report["eligible"] else
        "ineligible; stop this candidate per owner instruction"
    )
    _save(report)
    print(json.dumps({
        "status": report["status"],
        "eligible": report["eligible"],
        "projects": {
            name: {
                "status": row.get("status"),
                "RPS": row.get("RPS"),
                "format_errors": row.get("resources", {}).get("format_errors"),
                "format_error_recovery": row.get("format_error_recovery"),
            }
            for name, row in report["projects"].items()
        },
    }, indent=2), flush=True)
    return 0 if report["eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
