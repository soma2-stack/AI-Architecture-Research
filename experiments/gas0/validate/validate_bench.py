"""Mandatory benchmark checks. Any failure blocks model selection and pilot."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from harness.agent_loop import _stage_intake, _init_workspace
from harness.conditions import CONDITIONS
from harness.gate import run_visible
from harness.tools import ToolRunner
from scoring.hidden_runner import score_stage
from scoring.metrics import score_episode


def apply_patch(workspace: Path, path: Path):
    if path.stat().st_size:
        result = subprocess.run(["git", "apply", str(path)], cwd=workspace,
                                capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(f"patch {path}: {result.stderr}")


def required_project_shape(project: Path):
    manifest = json.loads((project / "manifest.json").read_text())
    assert manifest["stages"] == 8
    sources = list((project / "starter").rglob("*.py"))
    loc = sum(bool(line.strip()) for p in sources for line in p.read_text().splitlines())
    files = len(sources)
    assert 600 <= loc <= 1500, (project.name, "LOC", loc)
    assert 8 <= files <= 15, (project.name, "files", files)
    assert len(manifest["orientation_answers"]) >= 8
    return manifest, {"loc": loc, "files": files}


def validate_project(project: Path):
    manifest, stats = required_project_shape(project)
    with tempfile.TemporaryDirectory(prefix="gas0-val-") as tmp:
        workspace = Path(tmp) / "workspace"
        _init_workspace(project, workspace)
        stages = []
        retired = set()
        expected_ids = set()
        for stage in range(1, 9):
            request, just_retired = _stage_intake(project, workspace, stage)
            retired |= just_retired
            assert request.strip(), (project.name, stage, "missing request")
            visible_stage = project / "stages" / f"s{stage}" / "visible"
            hidden_stage = project / "stages" / f"s{stage}" / "hidden"
            if stage > 1:
                assert list(visible_stage.rglob("test_*.py")), (project.name, stage, "no visible")
                assert list(hidden_stage.rglob("test_*.py")), (project.name, stage, "no hidden")
            pre = score_stage(workspace, project, stage, retired)
            for probe in manifest["probes"]:
                if probe["introduced"] != stage or probe.get("text_only") or stage == 1:
                    continue
                assert all(not pre["hidden_tests"].get(t, False) for t in probe["tests"]), (
                    project.name, stage, probe["requirement"], "new hidden probe already passes")
            if stage == 4:
                assert (project / "stages" / "s4" / "bug.patch").exists()
                assert any(not pre["hidden_tests"].get(t, False) for p in manifest["probes"]
                           if p["introduced"] == 4 for t in p["tests"])
            if stage == 7:
                scenario = workspace / "scenarios" / "stage7.py"
                env = os.environ.copy()
                env["PYTHONPATH"] = str(workspace) + os.pathsep + env.get("PYTHONPATH", "")
                assert subprocess.run([sys.executable, str(scenario)], cwd=workspace,
                                      capture_output=True, env=env).returncode != 0, "scenario must crash before fix"
            apply_patch(workspace, project / "reference" / f"s{stage}.patch")
            if stage == 7:
                scenario = workspace / "scenarios" / "stage7.py"
                assert subprocess.run([sys.executable, str(scenario)], cwd=workspace,
                                      capture_output=True, env=env).returncode == 0, "scenario must pass after fix"
            visible = run_visible(workspace)
            assert not visible["failed"] and visible["returncode"] == 0, (
                project.name, stage, "visible", visible["failed"])
            repeated = [score_stage(workspace, project, stage, retired) for _ in range(3)]
            assert all(r["hidden_tests"] == repeated[0]["hidden_tests"] for r in repeated), (
                project.name, stage, "nondeterminism")
            hidden = repeated[0]
            if stage == 1:
                hidden["hidden_tests"].update({f"Q{i}": True for i in range(1, 9)})
            active = [p for p in manifest["probes"] if p["introduced"] <= stage
                      and (p.get("retired") is None or p["retired"] > stage)]
            for probe in active:
                for test in probe["tests"]:
                    assert hidden["hidden_tests"].get(test, False), (
                        project.name, stage, test, "reference fails hidden", hidden["hidden_tests"],
                        hidden["runner_output"])
            stages.append(hidden)
            expected_ids |= {t for p in active for t in p["tests"]}
        score = score_episode(stages, manifest)
        assert score["RPS"] == 1.0, (project.name, "oracle score", score["RPS"])
    stats.update({"visible_tests": sum(len(re.findall(r"^def test_", p.read_text(), re.M))
                                       for p in (project / "starter" / "tests").rglob("test_*.py")) +
                                  sum(len(re.findall(r"^def test_", p.read_text(), re.M))
                                      for p in (project / "stages").rglob("test_*.py")
                                      if "visible" in p.parts),
                  "hidden_tests": sum(len(re.findall(r"^def test_", p.read_text(), re.M))
                                      for p in (project / "stages").rglob("test_*.py")
                                      if "hidden" in p.parts),
                  "retention_probes": sum(bool(p.get("text_only")) for p in manifest["probes"]),
                  "stages": 8, "reference_rps": score["RPS"]})
    return stats


def validate_text_only_and_supersession(project: Path):
    manifest = json.loads((project / "manifest.json").read_text())
    for probe in manifest["probes"]:
        if not probe.get("text_only"):
            continue
        rid = probe["requirement"]
        for visible in (project / "stages").rglob("visible/test_*.py"):
            assert not re.search(r"#\s*req:\s*[^\n]*\b" + re.escape(rid) + r"\b",
                                 visible.read_text()), (project.name, rid, visible)
        assert probe["tests"], (project.name, rid, "no hidden probe")
    for stage in range(1, 9):
        path = project / "stages" / f"s{stage}" / "supersedes.json"
        if not path.exists():
            continue
        for retired in json.loads(path.read_text()):
            if retired.startswith("tests/hidden_"):
                parts = Path(retired).parts
                original_stage = int(parts[1].split("_")[1])
                assert (project / "stages" / f"s{original_stage}" / "hidden" / parts[2]).exists()
                assert any(p.get("retired") == stage and any(parts[2] in t for t in p["tests"])
                           for p in manifest["probes"]), (project.name, stage, retired)
            else:
                assert (project / "starter" / retired).exists() or any(
                    (project / "stages" / f"s{k}" / "visible" / Path(retired).name).exists()
                    for k in range(1, stage)), (project.name, stage, retired)


def validate_null_and_oracle(project: Path):
    manifest = json.loads((project / "manifest.json").read_text())
    with tempfile.TemporaryDirectory(prefix="gas0-null-") as tmp:
        root = Path(tmp)
        null = root / "null"
        oracle = root / "oracle"
        mirror = root / "mirror"
        for ws in (null, oracle, mirror):
            _init_workspace(project, ws)
        runner = ToolRunner(oracle, CONDITIONS["C0"])
        null_rows, oracle_rows = [], []
        retired = set()
        for stage in range(1, 9):
            for ws in (null, oracle, mirror):
                _, current_retired = _stage_intake(project, ws, stage)
            retired |= current_retired
            before = {str(p.relative_to(mirror)).replace("\\", "/"): p.read_text()
                      for p in mirror.rglob("*.py") if ".git" not in p.parts}
            apply_patch(mirror, project / "reference" / f"s{stage}.patch")
            after = {str(p.relative_to(mirror)).replace("\\", "/"): p.read_text()
                     for p in mirror.rglob("*.py") if ".git" not in p.parts}
            for rel in sorted(set(before) | set(after)):
                if before.get(rel) == after.get(rel):
                    continue
                if rel not in before:
                    runner.run("create_file", {"path": rel, "content": after[rel]}, stage)
                elif rel not in after:
                    runner.run("delete_file", {"path": rel}, stage)
                else:
                    runner.run("edit_file", {"path": rel, "old": before[rel],
                                             "new": after[rel]}, stage)
            nr = score_stage(null, project, stage, retired)
            orow = score_stage(oracle, project, stage, retired)
            if stage == 1:
                nr["hidden_tests"].update({f"Q{i}": False for i in range(1, 9)})
                orow["hidden_tests"].update({f"Q{i}": True for i in range(1, 9)})
            null_rows.append(nr)
            oracle_rows.append(orow)
        n = score_episode(null_rows, manifest)
        o = score_episode(oracle_rows, manifest)
        assert n["RPS"] < 1.0, (project.name, "null unexpectedly perfect")
        assert o["RPS"] == 1.0, (project.name, "harness tool oracle not perfect", o)
        return {"null_rps": n["RPS"], "tool_oracle_rps": o["RPS"]}


def main():
    root = Path(__file__).resolve().parents[1] / "bench"
    results = {}
    for p in sorted(root.iterdir()):
        if not p.is_dir() or not (p / "manifest.json").exists():
            continue
        validate_text_only_and_supersession(p)
        results[p.name] = validate_project(p)
        results[p.name].update(validate_null_and_oracle(p))
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
