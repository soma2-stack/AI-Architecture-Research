"""Eight-stage GAS-0 episode loop; no hidden tests enter model context."""
from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from .conditions import CONDITIONS
from .context import assemble
from .gate import RegressionGate, git
from .ledger import Ledger
from .tools import ToolRunner, tool_schemas
from scoring.hidden_runner import score_stage
from scoring.metrics import score_episode

SYSTEM = """You are working on one software project over eight stages. Use exactly
one tool action per reply. The first action of each stage MUST be plan(steps).
Do not claim a requirement is verified unless a test supports it. You can run
the visible tests; hidden tests and scores are inaccessible. Stage requests are
given once and may disappear from later context. Keep edits focused and finish
each stage with declare_stage_done(summary)."""


def _write_jsonl(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, default=str, sort_keys=True) + "\n")


def _init_workspace(project: Path, dest: Path):
    shutil.copytree(project / "starter", dest,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
    subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
    git(dest, "add", "-A")
    git(dest, "-c", "user.name=GAS0", "-c", "user.email=gas0@local",
        "commit", "-qm", "starter")


def _stage_intake(project: Path, workspace: Path, stage: int):
    pkg = project / "stages" / f"s{stage}"
    visible = pkg / "visible"
    for source in visible.rglob("test_*.py"):
        target = workspace / "tests" / source.relative_to(visible)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    supersedes = pkg / "supersedes.json"
    retired = set(json.loads(supersedes.read_text())) if supersedes.exists() else set()
    for path in retired:
        target = workspace / path
        if target.exists():
            target.unlink()
    if (pkg / "bug.patch").exists():
        subprocess.run(["git", "apply", str(pkg / "bug.patch")], cwd=workspace, check=True)
    if (pkg / "scenario.py").exists():
        target = workspace / "scenarios" / "stage7.py"
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(pkg / "scenario.py", target)
    if (pkg / "static_checks.py").exists():
        target = workspace / "tests" / f"test_stage{stage}_static.py"
        shutil.copy2(pkg / "static_checks.py", target)
    git(workspace, "add", "-A")
    git(workspace, "-c", "user.name=GAS0", "-c", "user.email=gas0@local",
        "commit", "--allow-empty", "-qm", f"stage {stage} intake")
    return (pkg / "request.md").read_text(), retired


def _one_action(message, tools):
    if not isinstance(message, dict):
        raise ValueError("assistant message must be an object")
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or len(calls) != 1:
        raise ValueError("expected one tool call")
    call = calls[0]
    if not isinstance(call, dict) or call.get("type") != "function":
        raise ValueError("tool call must be a function call")
    if not isinstance(call.get("id"), str) or not call["id"]:
        raise ValueError("tool call id is missing")
    function = call.get("function")
    if not isinstance(function, dict):
        raise ValueError("tool function is missing")
    name = function.get("name")
    if not isinstance(name, str):
        raise ValueError("tool name is missing")
    if name not in {t["function"]["name"] for t in tools}:
        raise ValueError("unsupported tool")
    raw_arguments = function.get("arguments")
    if not isinstance(raw_arguments, str):
        raise ValueError("tool arguments must be a JSON string")
    try:
        args = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("tool arguments are not valid JSON") from exc
    if not isinstance(args, dict):
        raise ValueError("tool arguments must decode to a JSON object")
    return name, args


def _repair_message():
    """Return a safe user turn after an invalid call, without replaying it."""
    return {
        "role": "user",
        "content": (
            "FORMAT ERROR: The previous tool call was invalid and was not run. "
            "Make one repair attempt now: issue exactly one supported structured "
            "tool call with valid JSON object arguments. Do not put tool-call JSON "
            "in message text."
        ),
    }


def build_components(cell: str, workspace: Path, out: Path):
    """Wire the frozen C0-C4 factors: ledger (S), gate (V), and the coupling (gate writes ledger)."""
    condition = CONDITIONS[cell]
    ledger = Ledger(Path(out) / ".gas" / "ledger.json", condition.coupled) if condition.ledger else None
    gate = RegressionGate(workspace, ledger if condition.coupled else None) if condition.gate else None
    runner = ToolRunner(workspace, condition, ledger, gate)
    return condition, ledger, gate, runner, tool_schemas(condition.ledger)


def run_episode(project: Path, cell: str, seed: int, llm, out: Path,
                model_parameters: int, dry_oracle=False):
    """A dev/calibration/evaluation episode. Oracle is validation-only."""
    project = Path(project)
    out = Path(out)
    if hasattr(llm, "check_context"):
        llm.check_context(16384)
    out.mkdir(parents=True, exist_ok=False)
    workspace = out / "workspace"
    _init_workspace(project, workspace)
    condition, ledger, gate, runner, schemas = build_components(cell, workspace, out)
    history = []
    stages = []
    manifest = json.loads((project / "manifest.json").read_text())
    total_gpu = 0.0
    superseded = set()
    for stage in range(1, 9):
        request, retired = _stage_intake(project, workspace, stage)
        superseded |= retired
        runner.protected_paths |= {p.resolve() for p in (workspace / "tests").rglob("test_*.py")}
        stage_start = time.monotonic()
        runner.test_executions = 0
        runner.test_cpu_seconds = 0.0
        if gate:
            initial_gate = gate.stage_start()
            runner.test_executions += 1
            runner.test_cpu_seconds += initial_gate["seconds"]
        calls, errors, done, done_summary = 0, 0, False, ""
        stage_log = out / f"stage{stage}.jsonl"
        while calls < 30 and time.monotonic() - stage_start < 1200:
            if dry_oracle:
                raise NotImplementedError("oracle replay requires reference patch tool replay")
            edit_scope = set(runner.edit_scope)
            view = ledger.view(edit_scope, llm.count_tokens) if ledger else ""
            prompt = assemble(SYSTEM, request, history, view, schemas,
                              llm.count_tokens, runner.plan)
            message, usage = llm.chat(prompt, schemas, seed)
            calls += 1
            total_gpu += usage["wall_seconds"]
            if usage["peak_context_tokens"] > 16384 or usage["completion_tokens"] > 1024:
                raise RuntimeError("model context/completion budget violated")
            _write_jsonl(stage_log, {"type": "model", "stage": stage, "call": calls,
                                    "message": message, "usage": usage})
            try:
                name, args = _one_action(message, schemas)
                if calls == 1 and name != "plan":
                    raise ValueError("first action must be plan")
            except (ValueError, PermissionError, KeyError, TypeError) as exc:
                errors += 1
                result = {"error": str(exc)}
                name, args = "format_error", {}
                _write_jsonl(stage_log, {"type": "tool", "stage": stage, "call": calls,
                                        "name": name, "arguments": args, "result": result})
                # The malformed assistant response stays in the raw audit log only.
                # Do not synthesize a tool result or replay an invalid call object.
                history.append(_repair_message())
                continue

            try:
                result = runner.run(name, args, stage)
            except (ValueError, PermissionError, KeyError, TypeError, RuntimeError,
                    FileNotFoundError, FileExistsError) as exc:
                # This was a valid structured call that failed during execution.
                # Preserve the real tool error so the model can react to it.
                errors += 1
                result = {"error": str(exc)}
            _write_jsonl(stage_log, {"type": "tool", "stage": stage, "call": calls,
                                    "name": name, "arguments": args, "result": result})
            tool_calls = message["tool_calls"]
            history.append({"role": "assistant", "content": message.get("content") or "",
                            "tool_calls": tool_calls})
            history.append({"role": "tool", "tool_call_id": tool_calls[0]["id"],
                            "name": name, "arguments": args,
                            "content": json.dumps(result, default=str)[:4800]})
            if name == "declare_stage_done" and isinstance(result, dict) and result.get("done"):
                done = True
                done_summary = args["summary"]
                break
        hidden = score_stage(workspace, project, stage, superseded)
        if stage == 1:
            try:
                answers = json.loads(done_summary)
            except (json.JSONDecodeError, TypeError):
                answers = {}
            hidden["hidden_tests"].update({
                f"Q{i}": answers.get(f"q{i}") == manifest["orientation_answers"][f"q{i}"]
                for i in range(1, 9)
            })
        record = {"stage": stage, "calls": calls, "format_errors": errors,
                  "test_executions": runner.test_executions, "wall_seconds": time.monotonic()-stage_start,
                  "visible_test_seconds": runner.test_cpu_seconds,
                  "done": done, **hidden}
        stages.append(record)
        (out / f"stage{stage}_score.json").write_text(json.dumps(record, indent=2, sort_keys=True))
        if ledger:
            shutil.copy2(ledger.path, out / f"ledger_stage{stage}.json")
    metrics = score_episode(stages, manifest)
    usage_rows = []
    for stage in range(1, 9):
        for line in (out / f"stage{stage}.jsonl").read_text().splitlines():
            row = json.loads(line)
            if row["type"] == "model":
                usage_rows.append(row["usage"])
    metrics["resources"] = {
        "model_calls": len(usage_rows), "prompt_tokens": sum(u["prompt_tokens"] for u in usage_rows),
        "completion_tokens": sum(u["completion_tokens"] for u in usage_rows),
        "peak_context_tokens": max(u["peak_context_tokens"] for u in usage_rows),
        "estimated_flops": 2 * model_parameters * sum(u["prompt_tokens"] + u["completion_tokens"] for u in usage_rows),
        "gpu_seconds_upper_bound": total_gpu,
        "test_executions": sum(r["test_executions"] for r in stages),
        "visible_test_seconds": sum(r["visible_test_seconds"] for r in stages),
        "hidden_test_seconds": sum(r["test_seconds"] for r in stages),
        "tool_calls": sum(len((out / f"stage{k}.jsonl").read_text().splitlines()) // 2
                          for k in range(1, 9)),
        "wall_seconds": sum(r["wall_seconds"] for r in stages),
        "format_errors": sum(r["format_errors"] for r in stages),
    }
    (out / "episode.json").write_text(json.dumps(metrics, indent=2, sort_keys=True))
    return metrics
