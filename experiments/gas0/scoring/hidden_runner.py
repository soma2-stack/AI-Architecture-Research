"""Score a clean copy; never expose hidden tests to the agent."""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from harness.gate import run_visible


def score_stage(workspace: Path, project: Path, stage: int, superseded: set[str]):
    with tempfile.TemporaryDirectory(prefix="gas0-hidden-") as tmp:
        root = Path(tmp) / "workspace"
        shutil.copytree(workspace, root, ignore=shutil.ignore_patterns(".git", ".gas", "__pycache__"))
        tests = root / "tests"
        tests.mkdir(exist_ok=True)
        for k in range(1, stage + 1):
            hidden = project / "stages" / f"s{k}" / "hidden"
            for source in hidden.rglob("test_*.py"):
                rel = source.relative_to(hidden)
                target = tests / ("hidden_" + str(k)) / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        for name in superseded:
            path = tests / name
            if path.exists():
                path.unlink()
        result = run_visible(root)
        return {"hidden_tests": result["all"], "test_seconds": result["seconds"],
                "harness_error": result["returncode"] not in {0, 1},
                "runner_output": result["output"] if result["returncode"] not in {0, 1} else ""}
