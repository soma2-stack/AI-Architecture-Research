"""Run one clean post-plan-first-fix C4 dev_arena seed-1 episode from Stage 1.

The pre-fix pilot record (`pilot_summary.json` and every earlier attempt
directory) is read only. This run writes a new directory and a new summary.
The unchanged 3-GPU-hour pilot cap is enforced during the episode: a model
call starts only if the cumulative upper bound, plus a reservation larger than
any single pilot call, stays within the cap. Otherwise the episode stops
cleanly and the partial result is recorded.
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

RUN_ROOT = GAS / "analysis" / "dev_pilot_qwen35_20260929"
PILOT_SUMMARY = RUN_ROOT / "pilot_summary.json"
SUMMARY = RUN_ROOT / "c4_postfix_summary.json"
OUT = RUN_ROOT / "C4_dev_arena_seed1_clean_after_plan_first_fix"
GPU_CAP_SECONDS = 3 * 3600
# The largest single-call wall time in the 802 pre-fix pilot calls was 36.672 s.
PER_CALL_RESERVATION_SECONDS = 60.0
MODEL_ALIAS = "qwen3.5-9b-q6k"


class PilotBudgetExhausted(RuntimeError):
    pass


class CappedClient:
    """Forwards to the frozen client; refuses a call that could cross the pilot cap."""

    def __init__(self, inner: LlamaClient, used_before: float):
        self.inner = inner
        self.used_before = used_before
        self.spent = 0.0
        self.calls = 0

    def check_context(self, minimum=16384):
        return self.inner.check_context(minimum)

    def count_tokens(self, value, tools=None):
        return self.inner.count_tokens(value, tools)

    def chat(self, messages, tools, seed, max_tokens=1024):
        if self.used_before + self.spent + PER_CALL_RESERVATION_SECONDS > GPU_CAP_SECONDS:
            raise PilotBudgetExhausted(
                f"pilot GPU cap: {self.used_before + self.spent:.3f}s used of {GPU_CAP_SECONDS}s; "
                f"next call needs a {PER_CALL_RESERVATION_SECONDS:.0f}s reservation")
        message, usage = self.inner.chat(messages, tools, seed, max_tokens)
        self.spent += usage["wall_seconds"]
        self.calls += 1
        return message, usage


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(out: Path, stage: int):
    log = out / f"stage{stage}.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def _usage(out: Path) -> dict:
    rows = [row["usage"] for stage in range(1, 9) for row in _rows(out, stage)
            if row["type"] == "model"]
    return {
        "model_calls": len(rows),
        "gpu_seconds_upper_bound": sum(row["wall_seconds"] for row in rows),
        "prompt_tokens": sum(row["prompt_tokens"] for row in rows),
        "completion_tokens": sum(row["completion_tokens"] for row in rows),
        "peak_context_tokens": max((row["peak_context_tokens"] for row in rows), default=0),
    }


def _plan_first_audit(out: Path) -> dict:
    stages = {}
    for stage in range(1, 9):
        tools = [row for row in _rows(out, stage) if row["type"] == "tool"]
        if not tools:
            continue
        executed = [row["name"] for row in tools if row["name"] != "format_error"]
        rejected = [row for row in tools if row["name"] == "format_error"
                    and row.get("result", {}).get("error") == "first action must be plan"]
        malformed_before_plan = [row for row in tools if row["name"] == "format_error"
                                 and row.get("plan_required")
                                 and row.get("result", {}).get("error") != "first action must be plan"]
        stages[str(stage)] = {
            "first_executed_action": executed[0] if executed else None,
            "first_call_was_plan": tools[0]["name"] == "plan",
            "non_plan_actions_rejected_before_plan": len(rejected),
            "malformed_calls_before_plan": len(malformed_before_plan),
            "calls_before_accepted_plan": next(
                (i + 1 for i, row in enumerate(tools)
                 if row["name"] == "plan" and "error" not in (row["result"] if isinstance(row["result"], dict) else {})),
                None),
        }
    return {
        "attempted_stages": len(stages),
        "stages_whose_first_executed_action_is_plan": sum(
            s["first_executed_action"] == "plan" for s in stages.values()),
        "stages_with_executed_actions": sum(s["first_executed_action"] is not None for s in stages.values()),
        "stages": stages,
    }


def _test_executions(out: Path) -> int:
    return sum(json.loads(p.read_text(encoding="utf-8"))["test_executions"]
               for p in sorted(out.glob("stage*_score.json")))


def main() -> int:
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
    if SUMMARY.exists() or OUT.exists():
        raise FileExistsError("post-fix C4 already attempted; refusing to overwrite")

    pilot = json.loads(PILOT_SUMMARY.read_text(encoding="utf-8"))
    used_before = pilot["cumulative_gpu_seconds_upper_bound"]
    if used_before + PER_CALL_RESERVATION_SECONDS > GPU_CAP_SECONDS:
        raise RuntimeError("pilot GPU-time cap reached")

    inner = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=300)
    if inner.check_context(16384) != frozen["runtime"]["server_context_tokens"]:
        raise RuntimeError("effective sequence context differs from frozen value")
    active_template = inner._get("/props").get("chat_template", "")
    if hashlib.sha256(active_template.encode("utf-8")).hexdigest() != frozen["runtime"]["active_template_sha256"]:
        raise RuntimeError("active chat template differs from frozen hash")
    client = CappedClient(inner, used_before)

    summary = {
        "protocol": "GAS-0 Candidate A / one-seed dev_arena pilot: clean post-fix C4 rerun from Stage 1",
        "reason": "plan-first enforcement fix; pre-fix C4 attempts are preserved and not resumed",
        "frozen_config_sha256": _sha256(frozen_path),
        "agent_loop_sha256": _sha256(GAS / "harness" / "agent_loop.py"),
        "tools_sha256": _sha256(GAS / "harness" / "tools.py"),
        "project": "dev_arena", "seed": 1, "cell": "C4",
        "gpu_cap_seconds": GPU_CAP_SECONDS,
        "per_call_reservation_seconds": PER_CALL_RESERVATION_SECONDS,
        "pilot_gpu_seconds_before": used_before,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "evaluation_projects_used": False,
        "phase_2_run": False,
    }
    started = time.monotonic()
    print(f"START C4 post-fix dev_arena seed=1 used_gpu_upper={used_before:.3f}s", flush=True)
    try:
        result = run_episode(GAS / "bench" / "dev_arena", "C4", 1, client, OUT, 9_000_000_000)
        result["status"] = "complete"
        result["mean_stage_completion"] = mean(stage["SC"] for stage in result["stages"])
    except PilotBudgetExhausted as exc:
        result = {"status": "stopped_at_gpu_cap", "error": str(exc)}
    except Exception as exc:
        result = {"status": "aborted", "error": f"{type(exc).__name__}: {exc}",
                  "traceback": traceback.format_exc()}
    result["episode_wall_elapsed_seconds"] = time.monotonic() - started
    result["run_resources"] = {**_usage(OUT), "test_executions_scored_stages": _test_executions(OUT)}
    result["scored_stages"] = sorted(int(p.stem[5:-6]) for p in OUT.glob("stage*_score.json"))
    result["plan_first_audit"] = _plan_first_audit(OUT)
    summary["result"] = result
    summary["pilot_gpu_seconds_after"] = used_before + result["run_resources"]["gpu_seconds_upper_bound"]
    summary["finished_utc"] = datetime.now(timezone.utc).isoformat()
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(f"END C4 {result['status']} run_gpu={result['run_resources']['gpu_seconds_upper_bound']:.3f}s "
          f"total={summary['pilot_gpu_seconds_after']:.3f}s scored={result['scored_stages']}", flush=True)
    if result["status"] != "complete":
        print(result["error"], flush=True)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
