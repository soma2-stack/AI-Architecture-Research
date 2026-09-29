"""Focused regression tests from the VPS quality/validity review (2026-09-29)."""
from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

import pytest

from harness.agent_loop import build_components
from harness.context import REPLY, WINDOW, assemble
from harness.gate import RegressionGate, traceback_symbols
from harness.ledger import Ledger, _fit
from harness.llm_client import LlamaClient
from harness.tools import tool_schemas


def words(value, tools=None):
    return len(str(value).split()) + (len(json.dumps(tools).split()) if tools else 0)


def _repo(tmp_path, files):
    ws = tmp_path / "ws"
    for rel, text in files.items():
        (ws / rel).parent.mkdir(parents=True, exist_ok=True)
        (ws / rel).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
    subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=GAS0", "-c", "user.email=gas0@local", "commit", "-qm", "s"],
                   cwd=ws, check=True)
    return ws


GAME = {
    "game/__init__.py": "",
    "game/combat.py": "def apply_poison(hp):\n    return max(1, hp - 1)\n",
    "tests/test_combat.py": ("from game.combat import apply_poison\n\n"
                             "# req: R2.1\n"
                             "def test_poison_floor():\n    assert apply_poison(1) == 1\n\n"
                             "def test_poison_hits():\n    assert apply_poison(5) == 4\n"),
}


# ---------------------------------------------------------------- C: factor isolation
@pytest.mark.parametrize("cell,has_ledger,has_gate,coupled", [
    ("C0", False, False, False), ("C1", True, False, False), ("C2", False, True, False),
    ("C3", True, True, False), ("C4", True, True, True)])
def test_factor_isolation(tmp_path, cell, has_ledger, has_gate, coupled):
    ws = _repo(tmp_path, GAME)
    condition, ledger, gate, runner, schemas = build_components(cell, ws, tmp_path / "out")
    names = {s["function"]["name"] for s in schemas}
    assert (ledger is not None) == has_ledger == ("ledger_add" in names)
    assert (gate is not None) == has_gate
    if gate is not None:
        assert (gate.ledger is not None) == coupled
        if coupled:
            assert gate.ledger is ledger
    if ledger is not None:
        assert ledger.coupled == coupled
    assert len(tool_schemas(False)) == 11 and len(tool_schemas(True)) == 17


def test_c3_stays_model_mediated(tmp_path):
    ws = _repo(tmp_path, GAME)
    _, ledger, gate, runner, _ = build_components("C3", ws, tmp_path / "out")
    rid = ledger.add("decision", "poison never kills", 2)
    gate.stage_start()
    result = runner.run("edit_file", {"path": "game/combat.py", "old": "max(1, hp - 1)", "new": "hp - 1"}, 2)
    assert result["event"] == "REGRESSION_ROLLBACK" and "failed" in result  # raw gate evidence to the model
    assert ledger._req(rid)["tests"] == [] and ledger.data["failures"] == []  # no programmatic writes
    ledger.set_status(rid, "VERIFIED")  # the model may still manage the ledger itself
    assert ledger._req(rid)["status"] == "VERIFIED"


# ---------------------------------------------------------------- C4 gate -> ledger, rollback consistency
def test_c4_verification_and_rollback_consistency(tmp_path):
    ws = _repo(tmp_path, GAME)
    _, ledger, gate, runner, _ = build_components("C4", ws, tmp_path / "out")
    rid = ledger.add("decision", "poison never kills", 2)
    gate.stage_start()
    # a kept green edit links the tagged test and verifies the requirement
    ok = runner.run("edit_file", {"path": "game/combat.py", "old": "def apply_poison(hp):",
                                  "new": "def apply_poison(hp):  # floor at one"}, 2)
    assert json.loads(ok["notice"])["event"] == "GREEN"
    req = ledger._req(rid)
    assert req["tests"] == ["tests/test_combat.py::test_poison_floor"] and req["status"] == "VERIFIED"
    # a breaking edit is rolled back: workspace restored, status NOT downgraded, lesson recorded
    bad = runner.run("edit_file", {"path": "game/combat.py", "old": "max(1, hp - 1)", "new": "hp - 1"}, 2)
    assert json.loads(bad["notice"])["event"] == "REGRESSION_ROLLBACK"
    assert "max(1, hp - 1)" in (ws / "game/combat.py").read_text()
    assert ledger._req(rid)["status"] == "VERIFIED"
    failure = next(f for f in ledger.data["failures"] if f["test"].endswith("test_poison_floor"))
    assert failure["req_ids"] == [rid] and "tests.test_combat" in failure["tb_symbols"]
    # Check the project-relative path in the ledger's canonical POSIX form.
    scope = {path.replace("\\", "/") for path in runner.edit_scope}
    assert "FAILURE" in ledger.view(scope, words)  # edit scope = game/combat.py
    assert runner.last_edit is None  # undo cannot resurrect the rolled-back edit


def test_regressed_only_when_kept_workspace_fails(tmp_path):
    led = Ledger(tmp_path / "l.json", True)
    rid = led.add("feature", "x", 2)
    led.link(rid, ["t::a"], [])
    led.gate_event({"t::a"}, {}, [], "", {"commit": "c", "green_tests": 1})
    led.gate_event(set(), {"t::a": "boom"}, [], "", None, rolled_back=True)
    assert led._req(rid)["status"] == "VERIFIED"
    led.gate_event(set(), {"t::a": "boom"}, [], "", None)  # e.g. injected stage-4 bug, PROGRESS
    assert led._req(rid)["status"] == "REGRESSED"


# ---------------------------------------------------------------- A2 tag propagation
def test_tags_do_not_bleed(tmp_path):
    ws = tmp_path / "ws"
    (ws / "tests").mkdir(parents=True)
    (ws / "tests" / "test_tags.py").write_text(
        "import pytest\n\n"
        "# req: R2.1\n"
        "def test_one():\n    pass\n\n"
        "def test_unrelated():\n    pass\n\n"
        "# req: R2.2\n"
        "def helper():\n    pass\n\n"
        "def test_after_helper():\n    pass\n\n"
        "@pytest.mark.req('R2.3')\n"
        "def test_marked():\n    pass\n\n"
        "@pytest.mark.req('R2.1')\n"
        "@pytest.mark.req(\"R2.2\", \"R2.3\")\n"
        "def test_multi():  # req: R2.4\n    pass\n")
    led = Ledger(tmp_path / "l.json", True)
    for text in "abcd":
        led.add("feature", text, 2)
    ids = {f"tests/test_tags.py::{n}" for n in
           ("test_one", "test_unrelated", "test_after_helper", "test_marked", "test_multi")}
    led.sync_test_tags(ws, ids)
    tests = {r["id"]: set(t.split("::")[1] for t in r["tests"]) for r in led.data["requirements"]}
    assert tests == {"R2.1": {"test_one", "test_multi"}, "R2.2": {"test_multi"},
                     "R2.3": {"test_marked", "test_multi"}, "R2.4": {"test_multi"}}


# ---------------------------------------------------------------- A3 deferred visibility
def test_deferred_work_stays_visible(tmp_path):
    led = Ledger(tmp_path / "l.json", True)
    rid = led.add("deferred", "boss drops the vault key", 3)
    assert "UNPROTECTED " + rid in led.view(set(), words)
    led.link(rid, ["tests/test_boss.py::test_key"], [])
    for status in ("OPEN", "CLAIMED"):
        led.data["requirements"][0]["status"] = status
        assert f"DEFERRED {rid} [{status}]" in led.view(set(), words)
    led.data["requirements"][0]["status"] = "VERIFIED"
    view = led.view(set(), words)
    assert "DEFERRED" not in view and rid in view.split("VERIFIED: ")[1]


# ---------------------------------------------------------------- A1 scoped failure records
def test_traceback_symbols_from_pytest_repr(tmp_path):
    external_file = (tmp_path.parent / "x.py").resolve().as_posix()
    repr_ = ("tests/test_combat.py:3: \n_ _ _\ngame/combat.py:2: in apply_poison\n    return helper(hp)\n"
             "game/combat.py:4: ValueError\n" + external_file + ":9: in outside\n")
    assert traceback_symbols(repr_, tmp_path) == ["tests.test_combat", "game.combat.apply_poison", "game.combat"]


def test_failure_visible_only_in_scope(tmp_path):
    led = Ledger(tmp_path / "l.json", True)
    led.gate_event(set(), {"tests/test_save.py::test_roundtrip": "AssertionError"},
                   ["game.save.serialize"], " game/inventory.py | 3 ++-", rolled_back=True)
    assert "FAILURE X1" in led.view({"game/save.py"}, words)          # symbol's file
    assert "FAILURE X1" in led.view({"game/inventory.py"}, words)     # file of the reverted edit
    assert "FAILURE X1" not in led.view({"game/ui.py"}, words)
    assert "FAILURE X1" not in led.view({"game/save_ui.py"}, words)   # no prefix false match
    assert "FAILURE X1" not in led.view(set(), words)


# ---------------------------------------------------------------- A4 budget fitting equivalence and cost
def _old_fit(lines, count, budget):
    out = []
    for line in lines:
        if count("\n".join(out + [line])) > budget:
            break
        out.append(line)
    return len(out)


def test_budget_fit_matches_linear_and_is_cheap():
    rng = random.Random(0)
    for _ in range(300):
        lines = [" ".join("w" * rng.randint(1, 6) for _ in range(rng.randint(1, 40)))
                 for _ in range(rng.randint(0, 60))]
        budget = rng.randint(1, 600)
        chars = lambda s: len(s) // 4  # noqa: E731
        for counter in (words, chars):
            assert _fit(lines, counter, budget) == _old_fit(lines, counter, budget)
    calls = []
    counter = lambda s: calls.append(1) or words(s)  # noqa: E731
    _fit(["alpha beta gamma"] * 64, counter, 100)
    assert len(calls) <= 8


# ---------------------------------------------------------------- B1 collection errors
def test_uncollectable_new_test_does_not_blind_or_trip_gate(tmp_path):
    ws = _repo(tmp_path, GAME)
    gate = RegressionGate(ws)
    start = gate.stage_start()
    assert len(start["passed"]) == 2
    (ws / "tests" / "test_inventory.py").write_text("from game.inventory import Bag\n\ndef test_bag():\n    assert Bag()\n")
    event = gate.after_edit()  # test written before its module: keep it, not a regression
    assert event["event"] == "PROGRESS" and "tests/test_inventory.py" in event["result"]["failed"]
    assert len(event["result"]["passed"]) == 2
    (ws / "game" / "combat.py").write_text("def apply_poison(hp:\n")  # syntax error breaks green tests
    assert gate.after_edit()["event"] == "REGRESSION_ROLLBACK"
    assert "max(1, hp - 1)" in (ws / "game" / "combat.py").read_text()


def test_gate_never_green_with_collection_error(tmp_path):
    ws = _repo(tmp_path, {"tests/test_new.py": "from missing import x\n\ndef test_x():\n    assert x\n"})
    gate = RegressionGate(ws)
    gate.stage_start()
    (ws / "tests" / "test_new.py").write_text("from missing import x\n\ndef test_x():\n    assert x  # still\n")
    assert gate.after_edit()["event"] == "PROGRESS"


# ---------------------------------------------------------------- B3 token accounting, B4 neutral errors
class _FakeServer(LlamaClient):
    def __init__(self, renders_tools):
        super().__init__("http://x", "m")
        self.renders_tools = renders_tools

    def _post(self, path, body):
        if path == "/apply-template":
            text = " ".join(m["content"] for m in body["messages"])
            if self.renders_tools and body["tools"]:
                text += " " + " ".join(t["function"]["name"] for t in body["tools"])
            return {"prompt": text}
        return {"tokens": str(body["content"]).split() + (["<bos>"] if body.get("add_special") else [])}


def test_tool_schema_counted_once():
    msgs = [{"role": "user", "content": "a b c"}]
    tools = tool_schemas(True)
    exact = _FakeServer(renders_tools=True)
    assert exact.count_tokens(msgs, tools) == 3 + len(tools) + 1
    fallback = _FakeServer(renders_tools=False)
    assert fallback.count_tokens(msgs, tools) == 3 + 1 + len(json.dumps(tools, ensure_ascii=False).split())


def test_context_never_exceeds_usable_budget():
    rng = random.Random(1)
    tools = tool_schemas(True)
    for _ in range(50):
        history = [{"role": "tool" if i % 2 else "assistant", "name": "read_file", "arguments": {},
                    "content": "tok " * rng.randint(10, 3000)} for i in range(rng.randint(0, 40))]
        prompt = assemble("sys", "req " * 200, history, "ledger " * rng.randint(0, 1500), tools, words, "plan")
        assert words(prompt, tools) <= WINDOW - REPLY


def test_condition_neutral_errors(tmp_path):
    led = Ledger(tmp_path / "l.json", True)
    rid = led.add("feature", "x", 2)
    with pytest.raises(PermissionError) as err:
        led.set_status(rid, "VERIFIED")
    assert "C4" not in str(err.value) and "C" + "3" not in str(err.value)
