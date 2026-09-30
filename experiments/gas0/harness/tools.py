"""Narrow workspace tools shared by all conditions except ledger calls."""
from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from .gate import bounded_failure_text, git, run_visible


def _inside(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or ".git" in path.parts or ".gas" in path.parts:
        raise ValueError("path outside editable workspace")
    return path


class ToolRunner:
    def __init__(self, workspace: Path, condition, ledger=None, gate=None):
        self.root = Path(workspace).resolve()
        self.condition = condition
        self.ledger = ledger
        self.gate = gate
        self.test_executions = 0
        self.test_cpu_seconds = 0.0
        self.history = []
        self.edit_scope = []
        self.plan = ""
        self.last_edit = None
        self.protected_paths: set[Path] = set()

    def _track(self, name, arguments, path=None):
        self.history.append({"name": name, "arguments": arguments})
        if path is not None:
            self.edit_scope.append(str(path.relative_to(self.root)))
            self.edit_scope = self.edit_scope[-3:]

    def _test(self, selector=None):
        if self.test_executions >= 40:
            raise RuntimeError("stage test-execution cap reached")
        self.test_executions += 1
        result = run_visible(self.root, selector)
        self.test_cpu_seconds += result["seconds"]
        return result

    def run(self, name: str, args: dict, stage: int):
        if name in {"read_file", "edit_file", "create_file", "delete_file"}:
            path = _inside(self.root, args["path"])
        else:
            path = None
        self._track(name, args, path)
        if name == "list_files":
            base = _inside(self.root, args.get("path", "."))
            depth = min(max(int(args.get("depth", 2)), 0), 5)
            return [str(p.relative_to(self.root)) for p in base.rglob("*")
                    if p.is_file() and ".git" not in p.parts and ".gas" not in p.parts
                    and len(p.relative_to(base).parts) <= depth][:300]
        if name == "read_file":
            lines = path.read_text().splitlines()
            start = max(1, int(args.get("start", 1)))
            end = min(len(lines), int(args.get("end", start + 299)), start + 299)
            return "\n".join(f"{i+1}: {lines[i]}" for i in range(start-1, end))
        if name == "grep":
            pattern = re.compile(args["pattern"])
            glob = args.get("glob", "*")
            hits = []
            for p in self.root.rglob("*"):
                if not p.is_file() or ".git" in p.parts or ".gas" in p.parts:
                    continue
                if not fnmatch.fnmatch(p.relative_to(self.root).as_posix(), glob):
                    continue
                try:
                    for n, line in enumerate(p.read_text().splitlines(), 1):
                        if pattern.search(line):
                            hits.append(f"{p.relative_to(self.root)}:{n}: {line[:300]}")
                            if len(hits) == 50:
                                return hits
                except (UnicodeDecodeError, OSError):
                    pass
            return hits
        if name == "edit_file":
            if path in self.protected_paths:
                raise PermissionError("shipped test is read-only")
            self._ensure_test_budget()
            old = args["old"]
            content = path.read_text()
            if not old or content.count(old) != 1:
                raise ValueError("old text must match exactly once")
            self.last_edit = (path, True, path.read_bytes())
            path.write_bytes(content.replace(old, args["new"], 1).encode("utf-8"))
            return self._modified()
        if name == "create_file":
            self._ensure_test_budget()
            if path.exists():
                raise FileExistsError(path)
            self.last_edit = (path, False, None)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(args["content"].encode("utf-8"))
            return self._modified()
        if name == "delete_file":
            if path in self.protected_paths:
                raise PermissionError("shipped test is read-only")
            self._ensure_test_budget()
            self.last_edit = (path, True, path.read_bytes())
            path.unlink()
            return self._modified()
        if name == "undo_last_edit":
            self._ensure_test_budget()
            if self.last_edit is None:
                return "no edit to undo"
            target, existed, content = self.last_edit
            if existed:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            elif target.exists():
                target.unlink()
            self.last_edit = None
            return self._modified()
        if name == "run_tests":
            result = self._test(args.get("selector"))
            return {"passed": len(result["passed"]), "failed": result["failed"],
                    "output": result["output"][-3000:]}
        if name == "run_scenario":
            script = _inside(self.root, "scenarios/" + args["name"] + ".py")
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.root) + os.pathsep + env.get("PYTHONPATH", "")
            proc = subprocess.run([sys.executable, str(script)], cwd=self.root,
                                  capture_output=True, text=True, timeout=30, env=env)
            return {"exit_code": proc.returncode,
                    "tail": (proc.stdout + proc.stderr)[-3000:]}
        if name == "plan":
            steps = args["steps"]
            if not isinstance(steps, list) or not all(isinstance(step, str) for step in steps):
                raise ValueError("plan steps must be an array of strings")
            self.plan = json.dumps(steps, ensure_ascii=False)
            return "plan recorded"
        if name == "declare_stage_done":
            return {"done": True, "summary": args["summary"]}
        if not self.condition.ledger or not self.ledger:
            raise ValueError("unknown tool")
        if name == "ledger_add":
            return self.ledger.add(args["kind"], args["text"], stage)
        if name == "ledger_link":
            return self.ledger.link(args["id"], args.get("tests", []), args.get("symbols", []))
        if name == "ledger_set_status":
            return self.ledger.set_status(args["id"], args["status"], superseded_by=args.get("superseded_by"))
        if name == "ledger_note":
            return self.ledger.note(args["id"], args["text"])
        if name == "task_add":
            return self.ledger.task_add(args["req"], args["text"], stage)
        if name == "task_update":
            return self.ledger.task_update(args["id"], args["state"])
        raise ValueError("unknown tool")

    def _modified(self):
        if not self.gate:
            return "edit accepted; tests voluntary"
        self.test_executions += 1
        event = self.gate.after_edit()
        self.test_cpu_seconds += event["result"]["seconds"]
        if event["event"] == "REGRESSION_ROLLBACK":
            self.last_edit = None
        summary = {"event": event["event"], "failed": event["result"]["failed"],
                   "passed": len(event["result"]["passed"])}
        if self.condition.coupled:
            return {"notice": bounded_notice(summary, 800)}
        return summary

    def _ensure_test_budget(self):
        if self.gate and self.test_executions >= 40:
            raise RuntimeError("stage test-execution cap reached")


def bounded_notice(summary: dict, limit: int) -> str:
    """Serialize a gate summary as valid JSON of at most `limit` characters.

    Slicing the serialized JSON cut the failure texts mid-traceback (and left invalid JSON).
    Here each failure text is bounded with `bounded_failure_text`, so its exception block is
    kept. Failures that still do not fit are counted in `more_failed` instead of shown."""
    text = json.dumps(summary)
    if len(text) <= limit:
        return text
    failed = summary.get("failed") or {}
    for keep in range(len(failed), -1, -1):
        shown = dict(list(failed.items())[:keep])
        extra = {"more_failed": len(failed) - keep} if keep < len(failed) else {}
        per = limit
        while per >= 160:  # below this a failure text is too short to show its cause
            bounded = {test: bounded_failure_text(message, per) for test, message in shown.items()}
            text = json.dumps({**summary, "failed": bounded, **extra})
            if len(text) <= limit:
                return text
            per = int(per * 0.85)
    return json.dumps({"event": summary.get("event"), "more_failed": len(failed)})[:limit]


def tool_schemas(ledger: bool):
    def schema(name, properties, required):
        return {"type": "function", "function": {"name": name, "description": name,
            "parameters": {"type": "object", "properties": properties,
                           "required": required, "additionalProperties": False}}}
    S = lambda d: {"type": "string", "description": d}
    A = lambda d: {"type": "array", "items": {"type": "string"}, "description": d}
    out = [
        schema("list_files", {"path": S("relative directory"), "depth": {"type": "integer"}}, []),
        schema("read_file", {"path": S("relative path"), "start": {"type": "integer"},
                             "end": {"type": "integer"}}, ["path"]),
        schema("grep", {"pattern": S("regex"), "glob": S("file glob")}, ["pattern"]),
        schema("edit_file", {"path": S("path"), "old": S("unique old text"),
                             "new": S("replacement")}, ["path", "old", "new"]),
        schema("create_file", {"path": S("path"), "content": S("file contents")}, ["path", "content"]),
        schema("delete_file", {"path": S("path")}, ["path"]),
        schema("undo_last_edit", {}, []),
        schema("run_tests", {"selector": S("optional pytest selector")}, []),
        schema("run_scenario", {"name": S("scenario stem")}, ["name"]),
        schema("plan", {"steps": A("stage plan")}, ["steps"]),
        schema("declare_stage_done", {"summary": S("stage result")}, ["summary"]),
    ]
    if ledger:
        out += [
            schema("ledger_add", {"kind": S("feature|decision|constraint|deferred"),
                                  "text": S("requirement")}, ["kind", "text"]),
            schema("ledger_link", {"id": S("requirement id"), "tests": A("test ids"),
                                   "symbols": A("code symbols")}, ["id"]),
            schema("ledger_set_status", {"id": S("requirement id"),
                                         "status": S("status"),
                                         "superseded_by": S("replacement id")}, ["id", "status"]),
            schema("ledger_note", {"id": S("requirement id"),
                                   "text": S("<=200 characters")}, ["id", "text"]),
            schema("task_add", {"req": S("requirement id"), "text": S("task")}, ["req", "text"]),
            schema("task_update", {"id": S("task id"), "state": S("todo|doing|done")}, ["id", "state"]),
        ]
    return out
