"""Run one cell of the owner-authorized post-plan-first-fix DEV pilot (dev_arena, seed 1).

Invoke once per cell, C0 through C4, in order. Every cell starts from Stage 1
in a new directory under `dev_pilot_qwen35_postfix_20260929/`. The pre-fix
pilot directories and summaries are read-only history.

The owner authorized a new GPU budget. This pilot uses its own 3-GPU-hour cap,
the design's DEV-pilot size, enforced per request by `gpu_cap.CappedClient`.

An aborted cell may be rerun only with an explicit retry reason. The aborted
attempt is kept in `aborted_attempts` and its directory is kept.
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
from analysis.gpu_cap import CappedClient, PilotBudgetExhausted  # noqa: E402
from analysis.run_qwen35_c4_postfix import _plan_first_audit, _usage  # noqa: E402
from analysis.run_qwen35_dev_pilot import _format_recovery  # noqa: E402

CELLS = ("C0", "C1", "C2", "C3", "C4")
RUN_ROOT = GAS / "analysis" / "dev_pilot_qwen35_postfix_20260929"
SUMMARY = RUN_ROOT / "postfix_pilot_summary.json"
GPU_CAP_SECONDS = 3 * 3600
MODEL_ALIAS = "qwen3.5-9b-q6k"
REQUEST_TIMEOUT_SECONDS = 300  # unchanged client timeout; bounds each request


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _charged(row: dict) -> float:
    return row.get("gpu_cap", {}).get("charged_seconds", 0.0)


def main() -> int:
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in CELLS:
        raise SystemExit("Usage: python analysis/run_qwen35_postfix_pilot.py C0|C1|C2|C3|C4 [retry_reason]")
    cell = sys.argv[1]
    retry_reason = sys.argv[2] if len(sys.argv) == 3 else None
    frozen_path = GAS / "frozen_config.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if frozen["model"]["name"] != "Qwen3.5-9B Q6_K" or frozen["decoding"]["seed"] != 1:
        raise RuntimeError("unexpected frozen model or seed")
    if _sha256(GAS / "harness" / "context.py") != frozen["context_policy"]["assembler_policy_sha256"]:
        raise RuntimeError("context policy differs from frozen hash")
    if _sha256(GAS / "harness" / "agent_loop.py") != frozen["tool_calling"]["agent_loop_sha256"]:
        raise RuntimeError("agent loop differs from frozen hash")
    if "plan_first_enforcement" not in frozen["tool_calling"]:
        raise RuntimeError("plan-first fix is not recorded in frozen_config.json")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {
        "protocol": "GAS-0 Candidate A / one-seed dev_arena DEV pilot, post plan-first fix",
        "plan_first_fix_commit": "9650008b9c793db25fda233d7742c5ec0abd09a9",
        "project": "dev_arena", "seed": 1, "cell_order": list(CELLS),
        "gpu_cap_seconds": GPU_CAP_SECONDS,
        "gpu_cap_basis": "new owner-authorized budget; design DEV-pilot size (3 GPU-hours), "
                         "separate from the exhausted pre-fix pilot",
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "cells": {}, "aborted_attempts": [],
        "evaluation_projects_used": False, "phase_2_run": False,
    }
    if cell in summary["cells"]:
        prior = summary["cells"][cell]
        if not retry_reason or prior.get("status") != "aborted":
            raise FileExistsError(f"post-fix result already recorded for {cell}")
        summary["aborted_attempts"].append({"cell": cell, **prior})
        del summary["cells"][cell]
    elif retry_reason:
        raise RuntimeError("retry reason given but no aborted attempt is recorded")
    if any(previous not in summary["cells"] for previous in CELLS[:CELLS.index(cell)]):
        raise RuntimeError("pilot cells must run in frozen C0-C4 order")
    if any(row.get("status") == "stopped_at_gpu_cap" for row in summary["cells"].values()):
        raise RuntimeError("pilot GPU cap already reached")
    used = sum(_charged(row) for row in [*summary["cells"].values(), *summary["aborted_attempts"]])
    attempt = sum(row["cell"] == cell for row in summary["aborted_attempts"])
    out = RUN_ROOT / (f"{cell}_dev_arena_seed1" + (f"_retry{attempt}_{retry_reason}" if retry_reason else ""))
    if out.exists():
        raise FileExistsError(f"refusing to overwrite pilot episode: {out}")

    inner = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=REQUEST_TIMEOUT_SECONDS)
    if inner.check_context(16384) != frozen["runtime"]["server_context_tokens"]:
        raise RuntimeError("effective sequence context differs from frozen value")
    active_template = inner._get("/props").get("chat_template", "")
    if hashlib.sha256(active_template.encode("utf-8")).hexdigest() != frozen["runtime"]["active_template_sha256"]:
        raise RuntimeError("active chat template differs from frozen hash")
    client = CappedClient(inner, GPU_CAP_SECONDS, used_before=used)
    if client.reservation > client.remaining():
        raise RuntimeError("pilot GPU cap reached")
    summary.setdefault("agent_loop_sha256", _sha256(GAS / "harness" / "agent_loop.py"))
    summary.setdefault("tools_sha256", _sha256(GAS / "harness" / "tools.py"))
    summary.setdefault("frozen_config_sha256", _sha256(frozen_path))

    started = time.monotonic()
    started_utc = datetime.now(timezone.utc).isoformat()
    print(f"START {cell} dev_arena seed=1 charged_before={used:.3f}s", flush=True)
    try:
        result = run_episode(GAS / "bench" / "dev_arena", cell, 1, client, out, 9_000_000_000)
        result["status"] = "complete"
        result["mean_stage_completion"] = mean(stage["SC"] for stage in result["stages"])
        result["declared_done_stages"] = sum(
            bool(json.loads((out / f"stage{s}_score.json").read_text(encoding="utf-8"))["done"])
            for s in range(1, 9))
        result["format_error_recovery"] = _format_recovery(out)
    except PilotBudgetExhausted as exc:
        result = {"status": "stopped_at_gpu_cap", "error": str(exc), "resources": _usage(out)}
    except Exception as exc:
        result = {"status": "aborted", "error": f"{type(exc).__name__}: {exc}",
                  "traceback": traceback.format_exc(), "resources": _usage(out)}
    result["directory"] = out.name
    result["started_utc"] = started_utc
    result["episode_wall_elapsed_seconds"] = time.monotonic() - started
    result["scored_stages"] = sorted(int(p.stem[5:-6]) for p in out.glob("stage*_score.json"))
    result["plan_first_audit"] = _plan_first_audit(out)
    result["gpu_cap"] = client.stats()
    if retry_reason:
        result["retry_reason"] = retry_reason
    summary["cells"][cell] = result
    summary["updated_utc"] = datetime.now(timezone.utc).isoformat()
    summary["cumulative_charged_gpu_seconds"] = sum(
        _charged(row) for row in [*summary["cells"].values(), *summary["aborted_attempts"]])
    _write(SUMMARY, summary)
    print(f"END {cell} {result['status']} charged_total={summary['cumulative_charged_gpu_seconds']:.3f}s",
          flush=True)
    if result["status"] == "complete":
        print(f"RPS={result['RPS']:.9f} SC={result['mean_stage_completion']:.9f} "
              f"calls={result['resources']['model_calls']}", flush=True)
    else:
        print(result["error"], flush=True)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
