"""Synthetic Qwen3.5 check using the actual GAS-0 context assembler.

Run only after starting the pinned Qwen3.5 llama.cpp server on port 8088.
No benchmark project files or benchmark text are read.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import HTTPError

from jsonschema import validate as validate_schema

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "gas0"))

from experiments.gas0.harness.agent_loop import SYSTEM, _one_action  # noqa: E402
from experiments.gas0.harness.conditions import CONDITIONS  # noqa: E402
from experiments.gas0.harness.context import REPLY, WINDOW, assemble  # noqa: E402
from experiments.gas0.harness.llm_client import LlamaClient  # noqa: E402
from experiments.gas0.harness.tools import tool_schemas  # noqa: E402


BASE_URL = "http://127.0.0.1:8088"
MODEL_ALIAS = "qwen3.5-9b-q6k"
PLAN = (
    "Synthetic only: perform the six one-call tool checks in order, including recovery "
    "after the mock test error."
)
SYNTHETIC_LEDGER = (
    "DECISION R1.1 [CLAIMED]: this is synthetic ledger text only.\n"
    "CONSTRAINT R1.2 [OPEN]: no real project files may be read or changed."
)
REQUEST = (
    "This is a synthetic tool-template check. Make exactly one structured tool call per "
    "assistant turn, wait for its result, then continue to the next step. Do not call "
    "declare_stage_done until all six are complete. Steps: (1) call plan with steps "
    "array [synthetic-step-a, synthetic-step-b]; (2) call read_file with path "
    "synthetic-only.txt; (3) call run_tests with no arguments; (4) after its ordinary "
    "recoverable timeout result, call grep with pattern synthetic-marker; (5) call "
    "create_file with path synthetic-only.txt and content synthetic; (6) call "
    "undo_last_edit with no arguments. These are mock tool calls only; do not access "
    "real files, tests, or resources."
)
CHECKS = [
    ("plan", {"steps": ["synthetic-step-a", "synthetic-step-b"]}, True),
    ("read_file", {"path": "synthetic-only.txt"}, True),
    ("run_tests", {}, False),
    ("grep", {"pattern": "synthetic-marker"}, True),
    ("create_file", {"path": "synthetic-only.txt", "content": "synthetic"}, True),
    ("undo_last_edit", {}, True),
]


def context_messages(client, cell, history, request, system=SYSTEM):
    condition = CONDITIONS[cell]
    ledger = SYNTHETIC_LEDGER if condition.ledger else ""
    schemas = tool_schemas(condition.ledger)
    messages = assemble(system, request, history, ledger, schemas,
                        client.count_tokens, latest_plan=PLAN)
    user_index = next(i for i, message in enumerate(messages) if message["role"] == "user")
    if any(message["role"] == "system" for message in messages[user_index + 1:]):
        raise AssertionError("system role appears after current user message")
    content = messages[user_index]["content"]
    if not content.startswith("CURRENT STAGE REQUEST:\n" + request):
        raise AssertionError("current request changed or moved")
    if condition.ledger:
        if "PROJECT LEDGER:\n" + SYNTHETIC_LEDGER not in content:
            raise AssertionError("synthetic ledger missing from ledger cell")
        if not content.index("CURRENT STAGE REQUEST:") < content.index("PROJECT LEDGER:") < content.index("LATEST PLAN:"):
            raise AssertionError("request/ledger/plan order is wrong")
    elif "PROJECT LEDGER" in content:
        raise AssertionError("ledger leaked into C0")
    if not content.endswith("LATEST PLAN:\n" + PLAN):
        raise AssertionError("latest plan missing or changed")
    token_count = client.count_tokens(messages, schemas)
    if token_count > WINDOW - REPLY:
        raise AssertionError(f"assembled prompt exceeds fixed budget: {token_count}")
    return messages, schemas, token_count


def run_sequence(client, cell):
    history = []
    turns = []
    for index, (expected_name, expected_args, success) in enumerate(CHECKS, 1):
        messages, schemas, assembled_tokens = context_messages(client, cell, history, REQUEST)
        body = {
            "model": MODEL_ALIAS,
            "messages": messages,
            "tools": schemas,
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "temperature": 0.2,
            "top_p": 0.95,
            "seed": 1,
            "max_tokens": 512,
            "stream": False,
        }
        try:
            response = client._post("/v1/chat/completions", body)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:1200]
            raise RuntimeError(f"HTTP {exc.code} at {cell} turn {index}: {detail}") from exc
        choice = response["choices"][0]
        message = choice["message"]
        calls = message.get("tool_calls") or []
        if len(calls) != 1:
            raise AssertionError(f"{cell} turn {index}: expected one tool call; got {len(calls)}")
        name, args = _one_action(message, schemas)
        schema = next(tool["function"]["parameters"] for tool in schemas
                      if tool["function"]["name"] == name)
        validate_schema(args, schema)
        if name != expected_name or args != expected_args:
            raise AssertionError(
                f"{cell} turn {index}: expected {expected_name} {expected_args!r}; got {name} {args!r}"
            )
        turn = {
            "index": index,
            "expected_function": expected_name,
            "function": name,
            "arguments": args,
            "tool_calls_count": len(calls),
            "valid_json_and_schema": True,
            "finish_reason": choice.get("finish_reason"),
            "assembled_prompt_tokens": assembled_tokens,
            "usage": response.get("usage", {}),
        }
        history.append({"role": "assistant", "content": message.get("content") or "",
                        "tool_calls": calls})
        tool_result = ({"ok": True, "result": "synthetic success"} if success else
                       {"ok": False, "error": "synthetic recoverable tool timeout"})
        history.append({"role": "tool", "tool_call_id": calls[0]["id"],
                        "content": json.dumps(tool_result)})
        turn["mock_tool_result"] = "success" if success else "ordinary recoverable error"
        turns.append(turn)
    return {
        "turns": turns,
        "successful_tool_calls": sum(t["mock_tool_result"] == "success" for t in turns),
        "tool_error_recovery": turns[2]["mock_tool_result"].startswith("ordinary") and turns[3]["function"] == "grep",
        "all_single_structured_calls": all(t["tool_calls_count"] == 1 and t["valid_json_and_schema"] for t in turns),
        "total_prompt_tokens": sum(t["usage"].get("prompt_tokens", 0) for t in turns),
        "total_completion_tokens": sum(t["usage"].get("completion_tokens", 0) for t in turns),
        "peak_context_tokens": max((t["usage"].get("prompt_tokens", 0) +
                                     t["usage"].get("completion_tokens", 0) for t in turns), default=0),
    }


def main():
    client = LlamaClient(BASE_URL, MODEL_ALIAS, timeout=180)
    report = {
        "model": "Qwen3.5-9B Q6_K",
        "synthetic_only": True,
        "assembler_policy_sha256": "A0779B00CE6CF19DA7E1BDABB2E2A232449F6928F079DAC7FC1796F0BD8C36A5",
        "system_policy": "Actual GAS-0 SYSTEM, no benchmark content.",
        "parallel_tool_calls": False,
        "context_tokens_per_sequence": client.check_context(16384),
        "template_renders_tools": client._template_renders_tools(tool_schemas(False)),
        "condition_sequences": {},
        "http_500": False,
        "apply_template_failure": False,
    }
    try:
        # Force actual /apply-template rendering for both requested assembler shapes.
        for cell in ("C0", "C4"):
            history = [{"role": "assistant", "content": "synthetic prior plan"}]
            messages, schemas, count = context_messages(client, cell, history, "Synthetic context shape check.")
            report["condition_sequences"][cell] = {
                "initial_assemble_roles": [m["role"] for m in messages],
                "initial_assemble_tokens": count,
                "ledger_present": cell == "C4",
                "plan_present": True,
            }
            report["condition_sequences"][cell].update(run_sequence(client, cell))
    except HTTPError as exc:
        report["http_500"] = exc.code == 500
        report["failure"] = f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:1200]}"
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"
        if "apply-template" in str(exc).lower():
            report["apply_template_failure"] = True
    report["eligible"] = (
        report["context_tokens_per_sequence"] >= 16384 and report["template_renders_tools"] and
        set(report["condition_sequences"]) == {"C0", "C4"} and
        all(item.get("successful_tool_calls", 0) >= 5 and item.get("tool_error_recovery") and
            item.get("all_single_structured_calls") for item in report["condition_sequences"].values()) and
        not report["http_500"] and not report["apply_template_failure"] and "failure" not in report
    )
    output = ROOT / "experiments" / "gas0" / "analysis" / "qwen35_amended_context_preflight_20260929.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
