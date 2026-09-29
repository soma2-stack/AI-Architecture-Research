from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.conditions import CONDITIONS
from harness.agent_loop import run_episode
from harness.context import assemble, elide
from harness.gate import RegressionGate
from harness.ledger import Ledger
from scoring.metrics import score_episode


def count(value, tools=None):
    return len(str(value).split())


def test_conditions():
    assert [(c.ledger, c.gate, c.coupled) for c in CONDITIONS.values()] == [
        (False, False, False), (True, False, False), (False, True, False),
        (True, True, False), (True, True, True)]


def test_ledger_permissions(tmp_path):
    uncoupled = Ledger(tmp_path / "c3.json", False)
    rid = uncoupled.add("decision", "never reduce HP below one", 2)
    uncoupled.set_status(rid, "VERIFIED")
    with pytest.raises(PermissionError):
        uncoupled.gate_event(set(), {}, [], "")
    coupled = Ledger(tmp_path / "c4.json", True)
    rid = coupled.add("decision", "never reduce HP below one", 2)
    with pytest.raises(PermissionError):
        coupled.set_status(rid, "VERIFIED")
    coupled.set_status(rid, "CLAIMED")
    coupled.link(rid, ["tests/test_rule.py::test_floor"], ["combat.poison"])
    coupled.gate_event({"tests/test_rule.py::test_floor"}, {}, [], "", {"commit": "x", "green_tests": 1})
    assert coupled._req(rid)["status"] == "VERIFIED"
    coupled.gate_event(set(), {"tests/test_rule.py::test_floor": "failed"}, ["combat.poison"], "+1/-1")
    assert coupled._req(rid)["status"] == "REGRESSED"
    assert coupled.data["failures"][0]["count"] == 1


def test_context_elision_and_budget():
    history = [{"role": "tool", "name": "read_file", "arguments": {"path": str(i)},
                "content": "many words " * 500} for i in range(8)]
    cropped = elide(history)
    assert cropped[0]["content"].startswith("[elided:")
    assert cropped[-1]["content"].startswith("many words")
    prompt = assemble("system", "current request", history, "", [], count, "latest plan")
    assert prompt[1]["content"].startswith("CURRENT STAGE REQUEST:")
    assert any("latest plan" in str(m) for m in prompt)


def test_gate_rolls_back_old_green_only(tmp_path):
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "tests").mkdir()
    (ws / "module.py").write_text("VALUE = 1\n")
    (ws / "tests" / "test_module.py").write_text("from module import VALUE\ndef test_old():\n assert VALUE == 1\n")
    subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
    subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=GAS0", "-c", "user.email=gas0@local",
                    "commit", "-qm", "start"], cwd=ws, check=True)
    gate = RegressionGate(ws)
    gate.stage_start()
    (ws / "module.py").write_text("VALUE = 0\n")
    assert gate.after_edit()["event"] == "REGRESSION_ROLLBACK"
    assert (ws / "module.py").read_text() == "VALUE = 1\n"
    (ws / "tests" / "test_new.py").write_text("def test_new():\n assert False\n")
    assert gate.after_edit()["event"] == "PROGRESS"
    (ws / "tests" / "test_module.py").unlink()
    assert gate.after_edit()["event"] == "REGRESSION_ROLLBACK"
    assert (ws / "tests" / "test_module.py").exists()


def test_scorer():
    manifest = {"probes": [{"introduced": i, "retired": None,
                            "tests": [f"h{i}"], "text_only": i == 2} for i in range(1, 9)]}
    rows = [{"hidden_tests": {f"h{i}": True for i in range(1, k + 1)}}
            for k in range(1, 9)]
    out = score_episode(rows, manifest)
    assert out["RPS"] == out["final"] == out["requirement_retention"] == 1


def test_fake_null_episode_logs_all_model_calls(tmp_path):
    class FakeClient:
        def __init__(self):
            self.seen = {}

        def count_tokens(self, value, tools=None):
            return len(str(value).split())

        def chat(self, messages, tools, seed):
            content = messages[1]["content"]
            request = content.split("CURRENT STAGE REQUEST:\n", 1)[1].split(
                "\n\nPROJECT LEDGER:", 1)[0].split("\n\nLATEST PLAN:", 1)[0]
            n = self.seen.get(request, 0)
            self.seen[request] = n + 1
            name = "plan" if n == 0 else "declare_stage_done"
            arguments = '{"steps":["inspect"]}' if n == 0 else '{"summary":"{}"}'
            message = {"role": "assistant", "content": "", "tool_calls": [{
                "id": f"call_{len(self.seen)}_{n}", "type": "function",
                "function": {"name": name, "arguments": arguments}}]}
            prompt = self.count_tokens(messages, tools)
            return message, {"prompt_tokens": prompt, "completion_tokens": 10,
                             "peak_context_tokens": prompt+10, "wall_seconds": 0.01}

    project = Path(__file__).resolve().parents[1] / "bench" / "dev_arena"
    out = tmp_path / "fake"
    result = run_episode(project, "C0", 1, FakeClient(), out, 7_000_000_000)
    assert result["resources"]["model_calls"] == 16
    assert result["resources"]["completion_tokens"] == 160
    assert result["resources"]["format_errors"] == 0
    assert result["RPS"] < 1
