"""C4-only DEV smoke test for the bounded failure-feedback fix (dev_arena, seed 1, Stages 1-3).

This is mechanism validation only. It has no comparative use and must not replace C4 in
any C0-C4 table (see analysis/failure_feedback_fix_audit_20260930.json). It runs from
Stage 1 under the fixed harness and stops cleanly once Stage 3 is scored. Stage 2
introduces the shield field, where the pre-fix C4 dataclass loop began.

Protections: the unchanged 300 s per-request timeout (gpu_cap.CappedClient, no cumulative
cap), the pre-start disk/GPU-temperature check, and the frozen-hash checks.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GAS = ROOT / "experiments" / "gas0"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(GAS))

from experiments.gas0.harness.agent_loop import run_episode  # noqa: E402
from experiments.gas0.harness.llm_client import LlamaClient  # noqa: E402
from analysis.analyze_postfix_pilot import audit_cell  # noqa: E402
from analysis.gpu_cap import CappedClient  # noqa: E402
from analysis.run_qwen35_c4_postfix import _usage  # noqa: E402
from analysis.run_qwen35_postfix_pilot import MODEL_ALIAS, REQUEST_TIMEOUT_SECONDS, _hardware_check  # noqa: E402

RUN_ROOT = GAS / "analysis" / "dev_smoke_c4_feedback_20260930"
OUT = RUN_ROOT / "C4_dev_arena_seed1_stages1to3"
SUMMARY = RUN_ROOT / "smoke_summary.json"
LAST_STAGE = 3
PRIOR_C4 = GAS / "analysis" / "dev_pilot_qwen35_postfix_20260929" / "C4_dev_arena_seed1"
PRIOR_C3 = GAS / "analysis" / "dev_pilot_qwen35_postfix_20260929" / "C3_dev_arena_seed1"
CAUSE = re.compile(r"non-default argument '\w+' follows default argument")
EXCEPTION_LINE = re.compile(r"(^|\n)E +\w*(Error|Exception)\b|\w+(Error|Exception): ")


class SmokeComplete(Exception):
    pass


class StopAfterStage:
    """Ends the episode before the first model call after `last` stage has been scored."""

    def __init__(self, inner, out: Path, last: int):
        self.inner, self.out, self.last = inner, out, last

    def check_context(self, minimum=16384):
        return self.inner.check_context(minimum)

    def count_tokens(self, value, tools=None):
        return self.inner.count_tokens(value, tools)

    def chat(self, messages, tools, seed, max_tokens=1024):
        if (self.out / f"stage{self.last}_score.json").exists():
            raise SmokeComplete(f"stage {self.last} scored")
        return self.inner.chat(messages, tools, seed, max_tokens)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def feedback_audit(base: Path, stages) -> dict:
    """Per-stage gate events, whether each rollback notice shows an exception line, and the
    recorded dataclass field-order failure."""
    out = {}
    for stage in stages:
        log = base / f"stage{stage}.jsonl"
        if not log.exists():
            continue
        events, rollback_with_exc, rollbacks, cause_rollbacks, valid_json = {}, 0, 0, 0, 0
        for line in log.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            result = row.get("result")
            if row["type"] != "tool" or not isinstance(result, dict) or "notice" not in result:
                continue
            notice = result["notice"]
            try:
                json.loads(notice)
                valid_json += 1
            except ValueError:
                pass
            event = re.search(r'"event": "(\w+)"', notice)
            event = event.group(1) if event else "?"
            events[event] = events.get(event, 0) + 1
            if event == "REGRESSION_ROLLBACK":
                rollbacks += 1
                rollback_with_exc += bool(EXCEPTION_LINE.search(notice.replace("\\n", "\n")))
                cause_rollbacks += bool(CAUSE.search(notice))
        score = base / f"stage{stage}_score.json"
        hidden = None
        if score.exists():
            h = json.loads(score.read_text(encoding="utf-8"))["hidden_tests"]
            hidden = f"{sum(v for k, v in h.items() if not k.startswith('Q'))}/" \
                     f"{sum(1 for k in h if not k.startswith('Q'))}"
        out[str(stage)] = {"gate_events": events, "rollbacks": rollbacks,
                           "rollback_notices_showing_exception": rollback_with_exc,
                           "rollbacks_with_dataclass_field_order_cause": cause_rollbacks,
                           "valid_json_notices": valid_json, "hidden_pass": hidden}
    ledger = base / f"ledger_stage{max(stages)}.json"
    records = json.loads(ledger.read_text(encoding="utf-8"))["failures"] if ledger.exists() else []
    return {"stages": out,
            "max_failure_record_count": max((f["count"] for f in records), default=0),
            "failure_records_showing_exception": sum(bool(EXCEPTION_LINE.search(f["message_head"]))
                                                     for f in records),
            "failure_records": len(records)}


def main() -> int:
    frozen_path = GAS / "frozen_config.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if _sha256(GAS / "harness" / "context.py") != frozen["context_policy"]["assembler_policy_sha256"]:
        raise RuntimeError("context policy differs from frozen hash")
    if _sha256(GAS / "harness" / "agent_loop.py") != frozen["tool_calling"]["agent_loop_sha256"]:
        raise RuntimeError("agent loop differs from frozen hash")
    fix = frozen["harness_amendments"][-1]
    for rel, digest in fix["files_sha256_after"].items():
        if _sha256(GAS / rel) != digest:
            raise RuntimeError(f"{rel} differs from the logged failure-feedback fix")
    if SUMMARY.exists() or OUT.exists():
        raise FileExistsError("smoke already run; refusing to overwrite")

    hardware = _hardware_check()
    inner = LlamaClient("http://127.0.0.1:8088", MODEL_ALIAS, timeout=REQUEST_TIMEOUT_SECONDS)
    if inner.check_context(16384) != frozen["runtime"]["server_context_tokens"]:
        raise RuntimeError("effective sequence context differs from frozen value")
    template = inner._get("/props").get("chat_template", "")
    if hashlib.sha256(template.encode("utf-8")).hexdigest() != frozen["runtime"]["active_template_sha256"]:
        raise RuntimeError("active chat template differs from frozen hash")
    capped = CappedClient(inner, None)
    client = StopAfterStage(capped, OUT, LAST_STAGE)

    started, started_utc = time.monotonic(), datetime.now(timezone.utc).isoformat()
    print(f"START C4 feedback smoke stages 1-{LAST_STAGE}", flush=True)
    try:
        run_episode(GAS / "bench" / "dev_arena", "C4", 1, client, OUT, 9_000_000_000)
        status, error = "complete_episode", None
    except SmokeComplete as exc:
        status, error = "stopped_after_stage_3_as_planned", str(exc)
    except Exception as exc:
        status, error = "aborted", f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
    stages = range(1, LAST_STAGE + 1)
    summary = {
        "purpose": "C4-only mechanism smoke test of the bounded failure-feedback fix; no comparative use",
        "project": "dev_arena", "seed": 1, "cell": "C4", "stages": [1, LAST_STAGE],
        "status": status, "error": error, "started_utc": started_utc,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "wall_seconds": time.monotonic() - started,
        "hardware_at_start": hardware,
        "resources": _usage(OUT), "gpu_cap": capped.stats(),
        "test_executions_scored_stages": sum(
            json.loads((OUT / f"stage{s}_score.json").read_text(encoding="utf-8"))["test_executions"]
            for s in stages if (OUT / f"stage{s}_score.json").exists()),
        "plan_first": {k: v for k, v in audit_cell(OUT).items() if k != "stages"},
        "feedback": feedback_audit(OUT, stages),
        "prior_postfix_c4_same_stages": feedback_audit(PRIOR_C4, stages),
        "prior_postfix_c3_same_stages": feedback_audit(PRIOR_C3, stages),
        "harness_files_sha256": {rel: _sha256(GAS / rel) for rel in fix["files_sha256_after"]},
        "evaluation_projects_used": False, "phase_2_run": False,
    }
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(f"END {status} gpu={summary['resources']['gpu_seconds_upper_bound']:.1f}s", flush=True)
    return 0 if status != "aborted" else 1


if __name__ == "__main__":
    raise SystemExit(main())
