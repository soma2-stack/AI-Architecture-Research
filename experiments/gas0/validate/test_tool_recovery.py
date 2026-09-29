from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from harness.agent_loop import _one_action, run_episode
from harness.tools import tool_schemas


def call(name, arguments, call_id="call-1"):
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": arguments},
    }


def assistant(*calls):
    return {"role": "assistant", "content": "", "tool_calls": list(calls)}


def test_one_action_rejects_truncated_json_arguments():
    message = assistant(call("edit_file", '{"path":"x.py","new":"cut'))
    with pytest.raises(ValueError, match="valid JSON"):
        _one_action(message, tool_schemas(False))


def test_one_action_rejects_unsupported_tool_name():
    message = assistant(call("run_shell", "{}"))
    with pytest.raises(ValueError, match="unsupported tool"):
        _one_action(message, tool_schemas(False))


def test_one_action_rejects_multiple_tool_calls():
    message = assistant(call("plan", '{"steps":[]}'), call("run_tests", "{}", "call-2"))
    with pytest.raises(ValueError, match="one tool call"):
        _one_action(message, tool_schemas(False))


def test_one_action_accepts_one_valid_structured_call():
    message = assistant(call("plan", '{"steps":["inspect"]}'))
    assert _one_action(message, tool_schemas(False)) == ("plan", {"steps": ["inspect"]})


def make_tiny_project(root: Path):
    starter = root / "starter"
    (starter / "tests").mkdir(parents=True)
    (starter / "tiny.py").write_text("VALUE = 1\n", encoding="utf-8")
    (starter / "tests" / "test_smoke.py").write_text(
        "from tiny import VALUE\n\ndef test_value():\n    assert VALUE == 1\n",
        encoding="utf-8",
    )
    for stage in range(1, 9):
        package = root / "stages" / f"s{stage}"
        package.mkdir(parents=True)
        (package / "request.md").write_text(f"Request stage {stage}.", encoding="utf-8")
    manifest = {
        "orientation_answers": {f"q{i}": f"a{i}" for i in range(1, 9)},
        "probes": [
            {"introduced": stage, "retired": None, "tests": [f"hidden_{stage}"], "text_only": False}
            for stage in range(1, 9)
        ],
    }
    (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return root


class RecoveringFakeClient:
    def __init__(self):
        self.seen = {}
        self.recovery_prompt = None

    def count_tokens(self, value, tools=None):
        return len(str(value).split()) + (len(str(tools).split()) if tools else 0)

    def chat(self, messages, tools, seed):
        content = messages[1]["content"]
        request = content.split("CURRENT STAGE REQUEST:\n", 1)[1].split("\n\n", 1)[0]
        stage = int(re.search(r"stage (\d+)", request).group(1))
        index = self.seen.get(stage, 0)
        self.seen[stage] = index + 1

        if stage == 1 and index == 2:
            self.recovery_prompt = messages

        has_ledger = any(schema["function"]["name"] == "ledger_add" for schema in tools)
        if index == 0:
            message = assistant(call("plan", '{"steps":["inspect"]}', f"plan-{stage}"))
        elif stage == 1 and index == 1:
            # Deliberately truncated just like the recorded 1,024-token failures.
            message = assistant(call(
                "edit_file", '{"path":"tiny.py","new":"RAW_MALFORMED_CANARY', "bad-1"
            ))
        elif stage == 1 and index == 2 and has_ledger:
            message = assistant(call(
                "ledger_add", '{"kind":"feature","text":"recovery test"}', "ledger-1"
            ))
        else:
            message = assistant(call("declare_stage_done", '{"summary":"{}"}', f"done-{stage}"))

        prompt_tokens = self.count_tokens(messages, tools)
        return message, {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": 12,
            "peak_context_tokens": prompt_tokens + 12,
            "wall_seconds": 0.001,
        }


@pytest.mark.parametrize("cell", ["C0", "C1", "C2", "C3", "C4"])
def test_malformed_call_is_logged_repaired_and_not_replayed(tmp_path, cell):
    project = make_tiny_project(tmp_path / "project")
    client = RecoveringFakeClient()
    out = tmp_path / "episode"

    result = run_episode(project, cell, 1, client, out, 9_000_000_000)

    # The bad response consumed one of the ordinary model-call slots; the next
    # call repaired it, and all eight stages finished without another call path.
    expected_calls = 18 if cell in {"C1", "C3", "C4"} else 17
    assert result["resources"]["model_calls"] == expected_calls
    assert result["resources"]["format_errors"] == 1
    assert result["resources"]["tool_calls"] == expected_calls
    stage_one = json.loads((out / "stage1_score.json").read_text(encoding="utf-8"))
    assert stage_one["calls"] == (4 if cell in {"C1", "C3", "C4"} else 3)
    assert stage_one["format_errors"] == 1
    assert stage_one["done"] is True

    raw_lines = (out / "stage1.jsonl").read_text(encoding="utf-8").splitlines()
    raw_rows = [json.loads(line) for line in raw_lines]
    bad_model = next(row for row in raw_rows if row.get("type") == "model" and row["call"] == 2)
    assert "RAW_MALFORMED_CANARY" in json.dumps(bad_model["message"])
    bad_tool = next(row for row in raw_rows if row.get("type") == "tool" and row["call"] == 2)
    assert bad_tool["name"] == "format_error"
    assert bad_tool["result"].get("error")

    # The retry prompt contains a safe repair turn, while the invalid assistant
    # tool call and any fabricated tool result are absent from replay history.
    replay = client.recovery_prompt
    assert replay is not None
    assert any(
        item.get("role") == "user" and "previous tool call was invalid" in item.get("content", "")
        for item in replay
    )
    assert "RAW_MALFORMED_CANARY" not in json.dumps(replay)
    assert not any(
        item.get("role") == "assistant"
        and any(c.get("id") == "bad-1" for c in item.get("tool_calls", []))
        for item in replay
    )
    # All replayed assistant tool calls are single, complete calls paired with
    # their actual tool response; the invalid call exists only in JSONL audit.
    for item in replay:
        if item.get("role") == "assistant" and item.get("tool_calls"):
            assert len(item["tool_calls"]) == 1
            assert item["tool_calls"][0].get("id") != "bad-1"
