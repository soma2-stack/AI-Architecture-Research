"""Cumulative visible-test regression gate with last-green git checkpoint."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def git(workspace: Path, *args):
    return subprocess.run(["git", *args], cwd=workspace, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()


def remove_untracked(workspace: Path):
    """Remove only git-untracked files inside a private episode workspace."""
    result = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "-z"],
                            cwd=workspace, capture_output=True, check=True)
    root = workspace.resolve()
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        target = (workspace / raw.decode("utf-8")).resolve()
        if not target.is_relative_to(root) or ".git" in target.parts:
            raise RuntimeError("unsafe untracked path during rollback")
        if target.is_file():
            target.unlink()
    for directory in sorted((p for p in workspace.rglob("*") if p.is_dir() and ".git" not in p.parts),
                            key=lambda p: len(p.parts), reverse=True):
        if directory != workspace:
            try:
                directory.rmdir()
            except OSError:
                pass


def run_visible(workspace: Path, selector: str | None = None):
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.json"
        # --continue-on-collection-errors: one uncollectable file (e.g. a new test written
        # before its module exists) must not stop every other visible test from running.
        cmd = [sys.executable, "-m", "pytest", "-q", "--import-mode=importlib", "-p", "no:cacheprovider",
               "--timeout=20", "--continue-on-collection-errors",
               "--json-report", f"--json-report-file={report}"]
        cmd.append(selector or "tests")
        start = time.monotonic()
        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = str(Path(tmp) / "pycache")
        proc = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True,
                              timeout=120, env=env)
        elapsed = time.monotonic() - start
        if not report.exists():
            raise RuntimeError("pytest JSON report missing: " + proc.stderr[-1000:])
        data = json.loads(report.read_text())
        tests = {t["nodeid"]: t["outcome"] == "passed" for t in data.get("tests", [])}
        failed = {t["nodeid"]: str(t.get("call", {}).get("longrepr", ""))[:1200]
                  for t in data.get("tests", []) if t["outcome"] != "passed"}
        # Collection errors are failures too (keyed by file node id), so a broken test file is
        # reported to the agent and can never be committed as a GREEN checkpoint.
        failed.update({c["nodeid"]: str(c.get("longrepr", ""))[:1200]
                       for c in data.get("collectors", []) if c.get("outcome") == "failed"})
        return {"passed": {k for k, v in tests.items() if v}, "failed": failed,
                "all": tests, "seconds": elapsed, "returncode": proc.returncode,
                "output": (proc.stdout + proc.stderr)[-5000:]}


_PYTEST_FRAME = re.compile(r"^([^\s:]+\.py):\d+:(?: in ([A-Za-z_][A-Za-z_0-9]*))?", re.M)
_NATIVE_FRAME = re.compile(r'File "([^"]+\.py)", line \d+, in ([A-Za-z_][A-Za-z_0-9]*)')


def traceback_symbols(message: str, workspace: Path) -> list[str]:
    """Project frames in a pytest long repr (or native traceback) as dotted `module.function`
    (module-only when the frame's function is not shown). Frames outside the workspace are dropped."""
    root = Path(workspace).resolve()
    out = []
    for file, fn in _PYTEST_FRAME.findall(message) + _NATIVE_FRAME.findall(message):
        path = Path(file)
        if path.is_absolute():
            path = path.resolve()
            if not path.is_relative_to(root):
                continue
            path = path.relative_to(root)
        if ".." in path.parts:
            continue
        module = path.with_suffix("").as_posix().replace("/", ".")
        symbol = f"{module}.{fn}" if fn else module
        if symbol not in out:
            out.append(symbol)
    return out


class RegressionGate:
    def __init__(self, workspace: Path, ledger=None):
        self.workspace = Path(workspace)
        self.ledger = ledger
        self.green: set[str] = set()
        self.checkpoint = git(self.workspace, "rev-parse", "HEAD")

    def stage_start(self):
        result = run_visible(self.workspace)
        self.green = result["passed"]
        self.checkpoint = git(self.workspace, "rev-parse", "HEAD")
        return result

    def after_edit(self):
        result = run_visible(self.workspace)
        old_failures = self.green & result["failed"].keys()
        missing_green = self.green - result["all"].keys()
        diff = git(self.workspace, "diff", "--stat")
        symbols = []
        for message in result["failed"].values():
            for symbol in traceback_symbols(message, self.workspace):
                if symbol not in symbols:
                    symbols.append(symbol)
        if old_failures or missing_green:
            git(self.workspace, "reset", "--hard", self.checkpoint)
            remove_untracked(self.workspace)
            event = "REGRESSION_ROLLBACK"
        elif not result["failed"]:
            git(self.workspace, "add", "-A")
            # A no-op edit can still be GREEN; Git refuses a commit with no staged change.
            if git(self.workspace, "diff", "--cached", "--name-only"):
                git(self.workspace, "-c", "user.name=GAS0", "-c", "user.email=gas0@local",
                    "commit", "-m", "green checkpoint")
            self.checkpoint = git(self.workspace, "rev-parse", "HEAD")
            self.green = result["passed"]
            event = "GREEN"
        else:
            event = "PROGRESS"
        if self.ledger:
            self.ledger.sync_test_tags(self.workspace,
                                       result["passed"] | result["failed"].keys())
            self.ledger.gate_event(result["passed"], result["failed"], symbols, diff,
                {"commit": self.checkpoint, "green_tests": len(self.green)} if event == "GREEN" else None,
                rolled_back=event == "REGRESSION_ROLLBACK")
        return {"event": event, "result": result, "diff": diff,
                "symbols": symbols, "missing_green": sorted(missing_green)}
