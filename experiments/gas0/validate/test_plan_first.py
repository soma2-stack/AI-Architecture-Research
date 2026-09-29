"""Regression tests for stage-level plan-first enforcement (DEV pilot audit, 2026-09-29).

Before the fix, `run_episode` only rejected a non-plan action on call 1 of a
stage. After a malformed or rejected first call, the repaired call could be any
tool. The requirement is now a per-stage state that only an accepted plan clears.
"""
from __future__ import annotations

import json
import re
from urllib.error import URLError

import pytest

from harness.agent_loop import run_episode
from harness.tools import ToolRunner
from harness.conditions import CONDITIONS
from validate.test_tool_recovery import assistant, call, make_tiny_project

PLAN = '{"steps":["inspect","edit","verify"]}'
READ = '{"path":"tiny.py"}'
DONE = '{"summary":"{}"}'
PLAN_REMINDER = "No plan has been accepted for this stage yet"


def good(name, arguments, call_id):
    return assistant(call(name, arguments, call_id))


def truncated(name, call_id):
    return assistant(call(name, '{"path":"tiny.py","new":"cut', call_id))


def two_calls(call_id):
    return assistant(call("plan", PLAN, call_id), call("read_file", READ, call_id + "b"))


def text_only():
    return {"role": "assistant", "content": '{"name":"plan","arguments":{"steps":[]}}'}


class ScriptedClient:
    """Plays a per-stage script; once it runs out, it declares the stage done.

    Unscripted stages open with a valid plan and then declare the stage done."""

    def __init__(self, scripts=None, fail_on=()):
        self.scripts = {stage: list(items) for stage, items in (scripts or {}).items()}
        self.seen = {}
        self.prompts = {}
        self.fail_on = set(fail_on)

    def count_tokens(self, value, tools=None):
        return len(str(value).split()) + (len(str(tools).split()) if tools else 0)

    def chat(self, messages, tools, seed):
        content = messages[1]["content"]
        stage = int(re.search(r"Request stage (\d+)", content).group(1))
        index = self.seen.get(stage, 0)
        self.seen[stage] = index + 1
        self.prompts.setdefault(stage, []).append(messages)
        if (stage, index) in self.fail_on:
            raise URLError("simulated connection failure")
        script = self.scripts.get(stage, [good("plan", PLAN, f"plan-{stage}")])
        if index < len(script):
            message = script[index]
        else:
            message = good("declare_stage_done", DONE, f"done-{stage}-{index}")
        prompt_tokens = self.count_tokens(messages, tools)
        return message, {"prompt_tokens": prompt_tokens, "completion_tokens": 8,
                         "peak_context_tokens": prompt_tokens + 8, "wall_seconds": 0.001}


class RetryingClient:
    """Client-level connection recovery: a failed request is retried transparently."""

    def __init__(self, inner, failures):
        self.inner = inner
        self.failures = set(failures)
        self.retries = 0

    def count_tokens(self, value, tools=None):
        return self.inner.count_tokens(value, tools)

    def chat(self, messages, tools, seed):
        stage = int(re.search(r"Request stage (\d+)", messages[1]["content"]).group(1))
        key = (stage, self.inner.seen.get(stage, 0))
        if key in self.failures:
            self.failures.discard(key)
            self.retries += 1
            # The original attempt never produced a message; retry the same prompt.
        return self.inner.chat(messages, tools, seed)


def plan_first_script(stage):
    return [good("plan", PLAN, f"plan-{stage}")]


def run(tmp_path, client, cell="C0"):
    project = make_tiny_project(tmp_path / "project")
    out = tmp_path / "episode"
    result = run_episode(project, cell, 1, client, out, 9_000_000_000)
    return result, out


def tool_rows(out, stage):
    rows = [json.loads(line) for line in (out / f"stage{stage}.jsonl").read_text(
        encoding="utf-8").splitlines()]
    return [row for row in rows if row["type"] == "tool"]


def executed(rows):
    """Names of the actions that actually reached the tool runner."""
    return [row["name"] for row in rows if row["name"] != "format_error"]


def stage_score(out, stage):
    return json.loads((out / f"stage{stage}_score.json").read_text(encoding="utf-8"))


def assert_plan_first(out):
    for stage in range(1, 9):
        names = executed(tool_rows(out, stage))
        if names:
            assert names[0] == "plan", (stage, names)


# 1. valid plan on the first call -> normal continuation
@pytest.mark.parametrize("cell", ["C0", "C1", "C2", "C3", "C4"])
def test_valid_first_plan_continues_normally(tmp_path, cell):
    client = ScriptedClient({s: plan_first_script(s) + [good("read_file", READ, f"r-{s}")]
                             for s in range(1, 9)})
    result, out = run(tmp_path, client, cell)
    for stage in range(1, 9):
        rows = tool_rows(out, stage)
        assert [row["name"] for row in rows] == ["plan", "read_file", "declare_stage_done"]
        assert "1: VALUE = 1" in rows[1]["result"]
        score = stage_score(out, stage)
        assert score["calls"] == 3 and score["format_errors"] == 0 and score["done"] is True
    assert result["resources"]["format_errors"] == 0
    # No repair turn was ever needed.
    assert not any("FORMAT ERROR" in json.dumps(p) for ps in client.prompts.values() for p in ps)


# 2. malformed first response -> repair -> non-plan action cannot bypass plan-first
@pytest.mark.parametrize("cell", ["C0", "C1", "C2", "C3", "C4"])
def test_malformed_first_then_non_plan_is_rejected(tmp_path, cell):
    script = [
        truncated("edit_file", "bad-1"),              # malformed: repaired next call
        good("list_files", "{}", "list-1"),            # the pre-fix bypass
        good("declare_stage_done", DONE, "done-early"),
        good("plan", PLAN, "plan-1"),
        good("list_files", "{}", "list-2"),
    ]
    client = ScriptedClient({1: script})
    result, out = run(tmp_path, client, cell)
    rows = tool_rows(out, 1)
    assert [row["name"] for row in rows[:5]] == [
        "format_error", "format_error", "format_error", "plan", "list_files"]
    assert rows[1]["result"]["error"] == "first action must be plan"
    assert rows[2]["result"]["error"] == "first action must be plan"
    assert all(row["plan_required"] for row in rows[:3])
    assert executed(rows)[0] == "plan"
    score = stage_score(out, 1)
    assert score["format_errors"] == 3 and score["done"] is True and score["calls"] == 6
    # Each repair turn restates the plan requirement; the rejected calls are not replayed.
    retry_prompts = client.prompts[1][1:4]
    for prompt in retry_prompts:
        assert PLAN_REMINDER in prompt[-1]["content"]
    replay = json.dumps(client.prompts[1][3])
    assert "list-1" not in replay and "done-early" not in replay and "bad-1" not in replay


# 3. malformed plan -> corrected valid plan -> normal continuation
def test_malformed_plan_then_corrected_plan(tmp_path):
    script = [
        truncated("plan", "bad-plan"),                          # invalid JSON
        good("plan", '{"steps":"not an array"}', "plan-str"),   # schema-invalid, fails in tool
        good("plan", "{}", "plan-missing"),                     # missing steps
        good("read_file", READ, "read-early"),                  # still before an accepted plan
        good("plan", PLAN, "plan-ok"),
        good("read_file", READ, "read-ok"),
    ]
    client = ScriptedClient({1: script})
    _, out = run(tmp_path, client)
    rows = tool_rows(out, 1)
    assert [row["name"] for row in rows] == [
        "format_error", "plan", "plan", "format_error", "plan", "read_file", "declare_stage_done"]
    assert "error" in rows[1]["result"] and "error" in rows[2]["result"]
    assert rows[3]["result"]["error"] == "first action must be plan"
    assert rows[4]["result"] == "plan recorded"
    assert "1: VALUE = 1" in rows[5]["result"]
    # The failed plan calls are real tool errors, so they stay in history for the model.
    later = json.dumps(client.prompts[1][3])
    assert "plan steps must be an array of strings" in later
    assert "LATEST PLAN" not in client.prompts[1][3][1]["content"]
    # Only the accepted plan is recorded as LATEST PLAN.
    assert '["inspect", "edit", "verify"]' in client.prompts[1][5][1]["content"]
    assert stage_score(out, 1)["done"] is True


# 4. multiple malformed/recovery attempts cannot bypass plan-first
def test_repeated_failures_never_clear_requirement(tmp_path):
    attempts = [
        truncated("edit_file", "b1"),
        good("read_file", READ, "n1"),
        two_calls("m1"),
        good("run_tests", "{}", "n2"),
        text_only(),
        assistant(call("run_shell", "{}", "u1")),
        good("edit_file", '{"path":"tiny.py","old":"1","new":"2"}', "n3"),
        good("declare_stage_done", DONE, "n4"),
    ]
    client = ScriptedClient({1: attempts * 4})   # 32 scripted calls, no plan ever
    _, out = run(tmp_path, client)
    rows = tool_rows(out, 1)
    score = stage_score(out, 1)
    assert score["calls"] == 30 and score["format_errors"] == 30 and score["done"] is False
    assert executed(rows) == []
    assert all(row["plan_required"] for row in rows)
    # The workspace was never edited by the rejected edit_file calls.
    assert (out / "workspace" / "tiny.py").read_text(encoding="utf-8") == "VALUE = 1\n"
    # The exhausted stage does not leak into the next one, which proceeds normally.
    assert [row["name"] for row in tool_rows(out, 2)] == ["plan", "declare_stage_done"]


# 5. connection/retry paths preserve plan-required state
def test_client_connection_recovery_preserves_requirement(tmp_path):
    inner = ScriptedClient({1: [good("read_file", READ, "after-retry"),
                                good("plan", PLAN, "plan-1")]})
    client = RetryingClient(inner, failures={(1, 0)})
    _, out = run(tmp_path, client)
    assert client.retries == 1
    rows = tool_rows(out, 1)
    assert rows[0]["name"] == "format_error"
    assert rows[0]["result"]["error"] == "first action must be plan"
    assert executed(rows) == ["plan", "declare_stage_done"]


def test_connection_failure_aborts_without_accepting_an_action(tmp_path):
    client = ScriptedClient({1: [truncated("edit_file", "bad-1")]}, fail_on={(1, 1)})
    with pytest.raises(URLError):
        run(tmp_path, client)
    out = tmp_path / "episode"
    rows = tool_rows(out, 1)
    assert [row["name"] for row in rows] == ["format_error"]
    assert not (out / "stage1_score.json").exists()


def test_tool_execution_error_before_plan_keeps_requirement(tmp_path):
    # A valid plan call whose execution fails is not an accepted plan.
    script = [good("plan", '{"steps":[1, 2]}', "p-bad"), good("grep", '{"pattern":"VALUE"}', "g"),
              good("plan", PLAN, "p-ok"), good("grep", '{"pattern":"VALUE"}', "g2")]
    _, out = run(tmp_path, ScriptedClient({1: script}))
    rows = tool_rows(out, 1)
    assert [row["name"] for row in rows[:4]] == ["plan", "format_error", "plan", "grep"]
    assert rows[1]["plan_required"] is True


# 6. a new stage resets plan-first enforcement
@pytest.mark.parametrize("cell", ["C0", "C4"])
def test_new_stage_resets_requirement(tmp_path, cell):
    scripts = {s: plan_first_script(s) for s in range(1, 9)}
    scripts[2] = [good("read_file", READ, "carry-over"), good("plan", PLAN, "plan-2")]
    scripts[5] = [truncated("edit_file", "bad-5"), good("grep", '{"pattern":"x"}', "g5"),
                  good("plan", PLAN, "plan-5")]
    client = ScriptedClient(scripts)
    _, out = run(tmp_path, client, cell)
    stage_two = tool_rows(out, 2)
    assert stage_two[0]["name"] == "format_error"
    assert stage_two[0]["result"]["error"] == "first action must be plan"
    assert [row["name"] for row in tool_rows(out, 5)[:3]] == [
        "format_error", "format_error", "plan"]
    assert_plan_first(out)


# 7. behavior after an accepted plan remains unchanged
def test_behavior_after_accepted_plan_is_unchanged(tmp_path):
    script = [
        good("plan", PLAN, "p1"),
        good("edit_file", '{"path":"tiny.py","old":"missing","new":"x"}', "e-fail"),  # tool error
        good("read_file", READ, "r1"),                  # accepted: failure did not re-arm
        truncated("edit_file", "bad-after"),            # ordinary format error
        good("grep", '{"pattern":"VALUE"}', "g1"),      # accepted after repair
        good("plan", '{"steps":["revise"]}', "p2"),     # re-planning still allowed
        good("run_tests", "{}", "t1"),
    ]
    client = ScriptedClient({1: script})
    _, out = run(tmp_path, client)
    rows = tool_rows(out, 1)
    assert [row["name"] for row in rows] == [
        "plan", "edit_file", "read_file", "format_error", "grep", "plan", "run_tests",
        "declare_stage_done"]
    assert rows[1]["result"]["error"] == "old text must match exactly once"
    assert rows[3]["plan_required"] is False
    # After an accepted plan, the repair turn is the unchanged generic text.
    repair = client.prompts[1][4][-1]["content"]
    assert repair.startswith("FORMAT ERROR") and PLAN_REMINDER not in repair
    assert '["revise"]' in client.prompts[1][6][1]["content"]
    score = stage_score(out, 1)
    assert score["format_errors"] == 2 and score["done"] is True and score["calls"] == 8


def test_plan_tool_requires_array_of_strings(tmp_path):
    runner = ToolRunner(tmp_path, CONDITIONS["C0"])
    assert runner.run("plan", {"steps": ["a", "b"]}, 1) == "plan recorded"
    assert runner.plan == '["a", "b"]'
    for bad in ("a", [1], None, {"a": 1}):
        with pytest.raises(ValueError, match="array of strings"):
            runner.run("plan", {"steps": bad}, 1)
    assert runner.plan == '["a", "b"]'
