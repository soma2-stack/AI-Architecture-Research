"""Run one authorized GAS-0 dev_arena pilot cell with the frozen Qwen model.

Invoke once per cell, C0 through C4. The output path must be new. This script
uses the existing harness and does not change any condition or prompt.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[3]
GAS = ROOT / "experiments" / "gas0"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(GAS))

from experiments.gas0.harness.agent_loop import run_episode  # noqa: E402
from experiments.gas0.harness.llm_client import LlamaClient  # noqa: E402


CELLS = ("C0", "C1", "C2", "C3", "C4")
RUN_ROOT = GAS / "analysis" / "dev_pilot_qwen35_20260929"
SUMMARY = RUN_ROOT / "pilot_summary.json"
GPU_CAP_SECONDS = 3 * 3600
MODEL_ALIAS = "qwen3.5-9b-q6k"


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _format_recovery(out: Path) -> dict:
    invalid = recovered = 0
    for stage in range(1, 9):
        rows = [json.loads(line) for line in (out / f"stage{stage}.jsonl").read_text().splitlines()]
        for index, row in enumerate(rows):
            if row.get("type") != "tool" or row.get("name") != "format_error":
                continue
            invalid += 1
            next_tool = next((item for item in rows[index + 1:] if item.get("type") == "tool"), None)
            if next_tool is not None and next_tool.get("name") != "format_error":
                recovered += 1
    return {"malformed_call_records": invalid, "recovered_on_next_call": recovered}


def _partial_usage(out: Path) -> dict:
    rows = []
    for log in sorted(out.glob("stage*.jsonl")):
        rows.extend(json.loads(line)["usage"] for line in log.read_text(encoding="utf-8").splitlines()
                    if json.loads(line).get("type") == "model")
    return {
        "model_calls": len(rows),
        "gpu_seconds_upper_bound": sum(row["wall_seconds"] for row in rows),
        "prompt_tokens": sum(row["prompt_tokens"] for row in rows),
        "completion_tokens": sum(row["completion_tokens"] for row in rows),
        "peak_context_tokens": max((row["peak_context_tokens"] for row in rows), default=0),
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CELLS:
        raise SystemExit("Usage: python analysis/run_qwen35_dev_pilot.py C0|C1|C2|C3|C4")
    cell = sys.argv[1]
    frozen_path = GAS / "frozen_config.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if frozen["model"]["name"] != "Qwen3.5-9B Q6_K" or frozen["decoding"]["seed"] != 1:
        raise RuntimeError("unexpected frozen model or seed")
    if _sha256(GAS / "harness" / "context.py") != frozen["context_policy"]["assembler_policy_sha256"]:
        raise RuntimeError("context policy differs from frozen hash")
    if _sha256(GAS / "harness" / "agent_loop.py") != frozen["tool_calling"]["agent_loop_sha256"]:
        raise RuntimeError("agent loop differs from frozen hash")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {
        "protocol": "GAS-0 Candidate A / one-seed dev_arena pilot",
        "frozen_model_commit": "87959946ef828f83254653c76294cef982e70bb1",
        "frozen_config_sha256": _sha256(frozen_path),
        "project": "dev_arena",
        "seed": 1,
        "cell_order": list(CELLS),
        "gpu_cap_seconds": GPU_CAP_SECONDS,
        "cells": {},
        "evaluation_projects_used": False,
        "phase_2_run": False,
    }
    retry_reason = None
    if cell in summary["cells"]:
        prior = summary["cells"][cell]
        if (cell == "C1" and prior.get("status") == "aborted"
                and "ledger.json" in prior.get("error", "")
                and not any(row["cell"] == cell for row in summary.get("aborted_attempts", []))):
            retry_reason = "empty_ledger_fix"
        elif (cell == "C4" and prior.get("status") == "aborted"
              and "green checkpoint" in prior.get("error", "")
              and not any(row["cell"] == cell for row in summary.get("aborted_attempts", []))):
            retry_reason = "empty_commit_fix"
        if retry_reason:
            prior["resources"] = _partial_usage(RUN_ROOT / f"{cell}_dev_arena_seed1")
            summary.setdefault("aborted_attempts", []).append({"cell": cell, **prior})
            del summary["cells"][cell]
        else:
            raise FileExistsError(f"pilot result already recorded for {cell}")
    if any(previous not in summary["cells"] for previous in CELLS[:CELLS.index(cell)]):
        raise RuntimeError("pilot cells must run in frozen C0-C4 order")
    used = sum(row.get("resources", {}).get("gpu_seconds_upper_bound", 0.0)
               for row in [*summary["cells"].values(), *summary.get("aborted_attempts", [])])
    if used >= GPU_CAP_SECONDS:
        raise RuntimeError("pilot GPU-time cap reached")
    suffix = f"_retry_after_{retry_reason}" if retry_reason else ""
    out = RUN_ROOT / f"{cell}_dev_arena_seed1{suffix}"
    if out.exists():
        raise FileExistsError(f"refusing to overwrite pilot episode: {out}")

    client = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=300)
    if client.check_context(16384) != frozen["runtime"]["server_context_tokens"]:
        raise RuntimeError("effective sequence context differs from frozen value")
    active_template = client._get("/props").get("chat_template", "")
    if hashlib.sha256(active_template.encode("utf-8")).hexdigest() != frozen["runtime"]["active_template_sha256"]:
        raise RuntimeError("active chat template differs from frozen hash")

    started = time.monotonic()
    print(f"START {cell} dev_arena seed=1 used_gpu_upper={used:.3f}s", flush=True)
    try:
        result = run_episode(GAS / "bench" / "dev_arena", cell, 1, client, out, 9_000_000_000)
        stages = [json.loads((out / f"stage{stage}_score.json").read_text(encoding="utf-8"))
                  for stage in range(1, 9)]
        result["status"] = "complete"
        result["mean_stage_completion"] = mean(stage["SC"] for stage in result["stages"])
        result["declared_done_stages"] = sum(bool(stage["done"]) for stage in stages)
        result["format_error_recovery"] = _format_recovery(out)
        result["episode_wall_elapsed_seconds"] = time.monotonic() - started
    except Exception as exc:
        result = {
            "status": "aborted",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
            "episode_wall_elapsed_seconds": time.monotonic() - started,
            "resources": _partial_usage(out),
        }
    summary["cells"][cell] = result
    summary["updated_utc"] = datetime.now(timezone.utc).isoformat()
    summary["cumulative_gpu_seconds_upper_bound"] = sum(
        row.get("resources", {}).get("gpu_seconds_upper_bound", 0.0)
        for row in [*summary["cells"].values(), *summary.get("aborted_attempts", [])]
    )
    _write(SUMMARY, summary)
    print(f"END {cell} {result['status']} gpu_upper={summary['cumulative_gpu_seconds_upper_bound']:.3f}s", flush=True)
    if result["status"] == "complete":
        print(f"RPS={result['RPS']:.9f} SC={result['mean_stage_completion']:.9f} "
              f"calls={result['resources']['model_calls']}", flush=True)
    else:
        print(result["error"], flush=True)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
