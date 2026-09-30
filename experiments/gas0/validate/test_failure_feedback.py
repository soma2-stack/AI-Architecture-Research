"""Regression tests: bounded failure feedback keeps the exception (post-fix DEV pilot, 2026-09-30).

In the post-fix DEV pilot, C4 repeated one dataclass field-order edit 24 times.
Its notice (`json.dumps(summary)[:800]`) and ledger `message_head`
(`message[:300]`) kept only the head of an import-chain traceback, so the final
`E   TypeError: ...` line was cut off. The shared `run_visible` cut (1,200
characters, head only) had the same defect in every cell, for longer tracebacks.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

import pytest

from harness.agent_loop import _init_workspace, _stage_intake, build_components
from harness.gate import _OMITTED, bounded_failure_text, run_visible
from harness.ledger import Ledger
from harness.tools import bounded_notice

DEV_ARENA = Path(__file__).resolve().parents[1] / "bench" / "dev_arena"
PY = r"C:\Users\someone\AppData\Local\Programs\Python\Python311\Lib"
EXCEPTION = "E   TypeError: non-default argument 'attack' follows default argument"


def windows_import_chain(extra_frames=8):
    """A pytest collection longrepr shaped like the pilot's, with long absolute stdlib paths."""
    lines = ["tests\\test_basics.py:1: in <module>", "    from arena import Arena",
             "arena\\__init__.py:3: in <module>", "    from .game import Arena",
             "arena\\game.py:4: in <module>", "    from . import ai",
             "arena\\ai.py:4: in <module>", "    from .model import Actor, Point, World",
             "arena\\model.py:27: in <module>", "    @dataclass", "     ^^^^^^^^^"]
    for n in range(extra_frames):
        lines += [f"{PY}\\dataclasses.py:{1000 + n}: in _process_class_{n}",
                  "    return _process_class(cls, init, repr, eq, order, unsafe_hash,"]
    lines += [f"{PY}\\dataclasses.py:545: in _init_fn",
              "    raise TypeError(f'non-default argument {f.name!r} '", EXCEPTION]
    return "\n".join(lines)


def assertion_failure():
    return ("def test_poison_floor():\n>       assert apply_poison(1) == 1\n"
            "E       assert 0 == 1\nE        +  where 0 = apply_poison(1)\n\n"
            "tests\\test_status.py:6: AssertionError")


def lines_come_from(output: str, source: str) -> bool:
    """Every kept line is a line (or the retained prefix of a line) of the source text."""
    src = source.splitlines()
    return all(line == _OMITTED or any(s.startswith(line) for s in src) for line in output.splitlines())


# 1. long tracebacks with long Windows paths keep the final exception type and message
@pytest.mark.parametrize("limit", [1200, 800, 300])
def test_long_windows_traceback_keeps_exception(limit):
    text = windows_import_chain()
    assert len(text) > 1200 and text.index(EXCEPTION) > 1200
    assert EXCEPTION not in text[:limit]          # the old head truncation lost it
    out = bounded_failure_text(text, limit)
    assert EXCEPTION in out
    assert out.startswith("tests\\test_basics.py:1: in <module>")
    assert "arena\\model.py:27: in <module>" in out   # last project frame kept


# 2. the summary stays within its bound
def test_summary_is_always_bounded():
    rng = random.Random(7)
    words = ["E   ValueError: bad", "x" * 300, f"{PY}\\a.py:1: in f", "arena\\x.py:3: in g",
             "    code()", "", "E       assert 1 == 2", "Traceback (most recent call last):"]
    for _ in range(500):
        text = "\n".join(rng.choice(words) for _ in range(rng.randint(1, 80)))
        for limit in (120, 300, 800, 1200):
            out = bounded_failure_text(text, limit)
            assert len(out) <= limit
            assert lines_come_from(out, text)


# 3. short failures are not degraded
@pytest.mark.parametrize("text", [assertion_failure(), "E   ImportError: no module", "", "x" * 1200])
def test_short_failures_unchanged(text):
    assert bounded_failure_text(text, 1200) == text
    assert bounded_failure_text(text, 1200) == text[:1200]  # identical to the old behavior


def test_cause_at_top_uses_plain_head():
    text = "E   ModuleNotFoundError: No module named 'arena.extra'\n" + "\n".join(
        f"{PY}\\importlib\\_bootstrap.py:{n}: in _find" for n in range(80))
    out = bounded_failure_text(text, 300)
    assert out.startswith("E   ModuleNotFoundError") and len(out) <= 300


# 4. no information beyond the failure text itself is exposed
def test_output_is_only_source_text_plus_marker():
    for text in (windows_import_chain(), windows_import_chain(30), assertion_failure() * 20):
        for limit in (300, 800, 1200):
            out = bounded_failure_text(text, limit)
            assert lines_come_from(out, text)
            added = set(out.splitlines()) - set(text.splitlines())
            assert added <= {_OMITTED} | {line for line in out.splitlines()
                                          if any(s.startswith(line) for s in text.splitlines())}


def test_notice_contains_only_summary_fields_and_is_valid_json():
    failed = {f"tests/test_{k}.py": windows_import_chain() for k in "abc"}
    notice = bounded_notice({"event": "REGRESSION_ROLLBACK", "failed": failed, "passed": 9}, 800)
    data = json.loads(notice)
    assert len(notice) <= 800
    assert set(data) <= {"event", "failed", "passed", "more_failed"}
    assert set(data["failed"]) <= set(failed)
    assert all(EXCEPTION in text for text in data["failed"].values())
    assert "hidden" not in notice


def test_notice_drops_whole_failures_before_losing_causes():
    failed = {f"tests/test_{k}.py::test_{k}": windows_import_chain() for k in "abcdefghij"}
    notice = bounded_notice({"event": "REGRESSION_ROLLBACK", "failed": failed, "passed": 3}, 800)
    data = json.loads(notice)
    assert len(notice) <= 800 and data["more_failed"] == 10 - len(data["failed"])
    assert data["failed"] and all(EXCEPTION in t for t in data["failed"].values())


def test_short_notice_unchanged():
    summary = {"event": "PROGRESS", "failed": {"tests/test_a.py::test_a": assertion_failure()},
               "passed": 4}
    assert bounded_notice(summary, 800) == json.dumps(summary)


# 5 and 7. C4 ledger failure records keep the useful line; repeats stay one consistent record
def test_ledger_failure_record_keeps_exception_and_repeats_consistently(tmp_path):
    ledger = Ledger(tmp_path / "ledger.json", coupled=True)
    failed = {"tests/test_basics.py": windows_import_chain()}
    for _ in range(3):
        ledger.gate_event(set(), failed, ["arena.model"], "arena/model.py | 5 +++++",
                          rolled_back=True)
    records = ledger.data["failures"]
    assert len(records) == 1 and records[0]["count"] == 3
    head = records[0]["message_head"]
    assert len(head) <= 300 and EXCEPTION in head
    view = ledger.view({"arena/model.py"}, lambda s: len(s.split()))
    assert f"FAILURE X1 x3 tests/test_basics.py: {head}" in view
    # A failure whose text already fits keeps the old verbatim head.
    ledger.gate_event(set(), {"tests/test_status.py::t": assertion_failure()}, [], "",
                      rolled_back=True)
    assert ledger.data["failures"][1]["message_head"] == assertion_failure()[:300]


# 1, 5 and 6 on the real pilot failure: dev_arena starter with the recorded field-order edit
def _broken_dev_arena(root: Path) -> Path:
    workspace = root / "ws"
    _init_workspace(DEV_ARENA, workspace)
    for stage in (1, 2):
        _stage_intake(DEV_ARENA, workspace, stage)
    return workspace


BAD_OLD = "    max_hp: int\n    attack: int\n"
BAD_NEW = "    max_hp: int\n    shield: int = 0\n    attack: int\n"
CAUSE = re.compile(r"TypeError: non-default argument 'attack' follows default argument")


@pytest.mark.parametrize("cell", ["C2", "C3", "C4"])
def test_recorded_dataclass_failure_is_visible_in_every_gate_cell(tmp_path, cell):
    workspace = _broken_dev_arena(tmp_path)
    _, ledger, gate, runner, _ = build_components(cell, workspace, tmp_path / "out")
    gate.stage_start()
    result = runner.run("edit_file", {"path": "arena/model.py", "old": BAD_OLD, "new": BAD_NEW}, 2)
    if cell == "C4":
        notice = result["notice"]
        assert len(notice) <= 800
        data = json.loads(notice)
        assert data["event"] == "REGRESSION_ROLLBACK"
        assert all(CAUSE.search(t) for t in data["failed"].values())
        heads = [f["message_head"] for f in ledger.data["failures"]]
        assert heads and all(CAUSE.search(h) and len(h) <= 300 for h in heads)
    else:
        # C2/C3 keep the unchanged raw summary structure (no notice, no failure records).
        assert set(result) == {"event", "failed", "passed"}
        assert result["event"] == "REGRESSION_ROLLBACK"
        assert all(CAUSE.search(t) for t in result["failed"].values())
        assert ledger is None or not ledger.data["failures"]
    # The rollback restored the checkpoint either way.
    assert BAD_NEW not in (workspace / "arena" / "model.py").read_text()


def test_old_c4_channels_lost_the_recorded_cause(tmp_path):
    """Documents the defect: the pre-fix slicing drops the cause on this exact failure."""
    workspace = _broken_dev_arena(tmp_path)
    model = workspace / "arena" / "model.py"
    model.write_text(model.read_text().replace(BAD_OLD, BAD_NEW, 1))
    failed = run_visible(workspace)["failed"]
    old_notice = json.dumps({"event": "REGRESSION_ROLLBACK", "failed": failed, "passed": 0})[:800]
    assert not CAUSE.search(old_notice)
    assert not any(CAUSE.search(message[:300]) for message in failed.values())
    assert all(CAUSE.search(message) for message in failed.values())
