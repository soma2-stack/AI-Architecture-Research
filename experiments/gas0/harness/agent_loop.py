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
    calls = message.get("tool_calls") or []
    if len(calls) != 1:
        raise ValueError("expected one tool call")
    function = calls[0]["function"]
    name = function["name"]
    if name not in {t["function"]["name"] for t in tools}:
        raise ValueError("unsupported tool")
    return name, json.loads(function["arguments"])


def run_episode(project: Path, cell: str, seed: int, llm, out: Path,
                model_parameters: int, dry_oracle=False):
    """A dev/calibration/evaluation episode. Oracle is validation-only."""
    condition = CONDITIONS[cell]
    project = Path(project)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    workspace = out / "workspace"
    _init_workspace(project, workspace)
    ledger = Ledger(out / ".gas" / "ledger.json", condition.coupled) if condition.ledger else None
    gate = RegressionGate(workspace, ledger if condition.coupled else None) if condition.gate else None
    runner = ToolRunner(workspace, condition, ledger, gate)
    schemas = tool_schemas(condition.ledger)
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
        if gate:
            gate.stage_start()
            runner.test_executions += 1
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
                result = runner.run(name, args, stage)
            except (ValueError, PermissionError, KeyError, TypeError, RuntimeError,
                    FileNotFoundError, FileExistsError) as exc:
                errors += 1
                result = {"error": str(exc)}
                if errors > 1:
                    # Invalid calls still consume budget and remain visible.
                    pass
                name, args = "format_error", {}
            _write_jsonl(stage_log, {"type": "tool", "stage": stage, "call": calls,
                                    "name": name, "arguments": args, "result": result})
            tool_calls = message.get("tool_calls") or []
            if tool_calls:
                history.append({"role": "assistant", "content": message.get("content") or "",
                                "tool_calls": tool_calls})
                history.append({"role": "tool", "tool_call_id": tool_calls[0]["id"],
                                "name": name, "arguments": args,
                                "content": json.dumps(result, default=str)[:4800]})
            else:
                history.append({"role": "assistant", "content": message.get("content") or ""})
                history.append({"role": "user", "content": "FORMAT ERROR: call exactly one tool."})
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
        "wall_seconds": sum(r["wall_seconds"] for r in stages),
        "format_errors": sum(r["format_errors"] for r in stages),
    }
    (out / "episode.json").write_text(json.dumps(metrics, indent=2, sort_keys=True))
    return metrics
