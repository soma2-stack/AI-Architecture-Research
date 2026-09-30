"""Run one cell of the owner-authorized final DEV pilot (Option B) on the corrected harness.

`dev_arena`, seed 1, C0 through C4 in frozen order, each from Stage 1 in a new directory
under `dev_pilot_qwen35_final_20260930/`. Earlier pilot directories are read-only history.

No cumulative GPU cap (the owner lifted it for this final comparison). The 300 s request
timeout (`gpu_cap.CappedClient`), the stage limits in the harness, and the pre-cell
disk and GPU-temperature check stay in force. Before every cell the runner checks the
frozen harness hashes, the logged failure-feedback fix hashes, and the dev_arena and
scoring tree hashes.

A cell that aborts is recorded and never retried here: the owner decides on any rerun.
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
from analysis.gpu_cap import CappedClient  # noqa: E402
from analysis.run_qwen35_c4_postfix import _plan_first_audit, _usage  # noqa: E402
from analysis.run_qwen35_dev_pilot import _format_recovery  # noqa: E402
from analysis.run_qwen35_postfix_pilot import MODEL_ALIAS, REQUEST_TIMEOUT_SECONDS, _hardware_check  # noqa: E402

CELLS = ("C0", "C1", "C2", "C3", "C4")
RUN_ROOT = GAS / "analysis" / "dev_pilot_qwen35_final_20260930"
SUMMARY = RUN_ROOT / "final_pilot_summary.json"
# Tree hashes verified before the final pilot (unchanged in git since af63fcb).
DEV_ARENA_TREE_SHA256 = "ff664bb0d8ee7645038f900fb0b723cb38c9f6978642c49409ad3c9685bf28cb"
SCORING_TREE_SHA256 = "a1cd78f3b4eda59df709f966cb265ea43e905a75ded2405bc1718a757bc7b973"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            digest.update(path.relative_to(GAS).as_posix().encode())
            digest.update(_sha256(path).encode())
    return digest.hexdigest()


def _verify(frozen: dict) -> dict:
    checks = {
        "harness/context.py": frozen["context_policy"]["assembler_policy_sha256"],
        "harness/agent_loop.py": frozen["tool_calling"]["agent_loop_sha256"],
        **frozen["harness_amendments"][-1]["files_sha256_after"],
    }
    for rel, digest in checks.items():
        if _sha256(GAS / rel) != digest:
            raise RuntimeError(f"{rel} differs from its frozen/logged hash")
    if tree_sha256(GAS / "bench" / "dev_arena") != DEV_ARENA_TREE_SHA256:
        raise RuntimeError("dev_arena benchmark tree changed")
    if tree_sha256(GAS / "scoring") != SCORING_TREE_SHA256:
        raise RuntimeError("scoring tree changed")
    if frozen["model"]["name"] != "Qwen3.5-9B Q6_K" or frozen["decoding"]["seed"] != 1:
        raise RuntimeError("unexpected frozen model or seed")
    return {**checks, "bench/dev_arena": DEV_ARENA_TREE_SHA256, "scoring": SCORING_TREE_SHA256}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CELLS:
        raise SystemExit("Usage: python analysis/run_qwen35_final_pilot.py C0|C1|C2|C3|C4")
    cell = sys.argv[1]
    frozen_path = GAS / "frozen_config.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    verified = _verify(frozen)

    summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {
        "protocol": "GAS-0 Candidate A / final one-seed dev_arena DEV pilot (owner Option B), "
                    "corrected failure-feedback harness",
        "project": "dev_arena", "seed": 1, "cell_order": list(CELLS),
        "gpu_cap_seconds": None, "gpu_cap_basis": "cumulative cap lifted by the owner for this final comparison",
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
        "verified_hashes": verified, "frozen_config_sha256": _sha256(frozen_path),
        "cells": {}, "evaluation_projects_used": False, "phase_2_run": False,
    }
    if cell in summary["cells"]:
        raise FileExistsError(f"final-pilot result already recorded for {cell}")
    if any(previous not in summary["cells"] for previous in CELLS[:CELLS.index(cell)]):
        raise RuntimeError("pilot cells must run in frozen C0-C4 order")
    if any(row["status"] != "complete" for row in summary["cells"].values()):
        raise RuntimeError("an earlier cell did not complete; owner review required")
    out = RUN_ROOT / f"{cell}_dev_arena_seed1"
    if out.exists():
        raise FileExistsError(f"refusing to overwrite pilot episode: {out}")

    hardware = _hardware_check()
    inner = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=REQUEST_TIMEOUT_SECONDS)
    if inner.check_context(16384) != frozen["runtime"]["server_context_tokens"]:
        raise RuntimeError("effective sequence context differs from frozen value")
    template = inner._get("/props").get("chat_template", "")
    if hashlib.sha256(template.encode("utf-8")).hexdigest() != frozen["runtime"]["active_template_sha256"]:
        raise RuntimeError("active chat template differs from frozen hash")
    client = CappedClient(inner, None)

    started, started_utc = time.monotonic(), datetime.now(timezone.utc).isoformat()
    print(f"START {cell} dev_arena seed=1", flush=True)
    try:
        result = run_episode(GAS / "bench" / "dev_arena", cell, 1, client, out, 9_000_000_000)
        result["status"] = "complete"
        result["mean_stage_completion"] = mean(stage["SC"] for stage in result["stages"])
        result["declared_done_stages"] = sum(
            bool(json.loads((out / f"stage{s}_score.json").read_text(encoding="utf-8"))["done"])
            for s in range(1, 9))
        result["format_error_recovery"] = _format_recovery(out)
    except Exception as exc:
        result = {"status": "aborted", "error": f"{type(exc).__name__}: {exc}",
                  "traceback": traceback.format_exc(), "resources": _usage(out)}
    result.update({"directory": out.name, "started_utc": started_utc,
                   "episode_wall_elapsed_seconds": time.monotonic() - started,
                   "scored_stages": sorted(int(p.stem[5:-6]) for p in out.glob("stage*_score.json")),
                   "plan_first_audit": _plan_first_audit(out), "gpu_cap": client.stats(),
                   "hardware_at_start": hardware, "hashes_verified_at_start": True})
    summary["cells"][cell] = result
    summary["updated_utc"] = datetime.now(timezone.utc).isoformat()
    summary["cumulative_charged_gpu_seconds"] = sum(
        row["gpu_cap"]["charged_seconds"] for row in summary["cells"].values())
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
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
