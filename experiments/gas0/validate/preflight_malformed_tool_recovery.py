"""Synthetic malformed-tool recovery check against the active Qwen3.5 template.

Requires the pinned local llama.cpp server on 127.0.0.1:8088. No benchmark
project content is read or used; tool results are synthetic and never executed.
"""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "gas0"))

from experiments.gas0.harness.agent_loop import SYSTEM, _one_action, _repair_message  # noqa: E402
from experiments.gas0.harness.context import REPLY, WINDOW, assemble  # noqa: E402
from experiments.gas0.harness.llm_client import LlamaClient  # noqa: E402
from experiments.gas0.harness.tools import tool_schemas  # noqa: E402


BASE_URL = "http://127.0.0.1:8088"
MODEL_ALIAS = "qwen3.5-9b-q6k"
REQUEST = (
    "Synthetic recovery check only. Do not inspect or modify any real files. "
    "After planning, call read_file with the exact synthetic path "
    "synthetic-recovery-only.txt. The harness will return a synthetic result."
)


def _schema_for(schemas, name):
    return next(tool["function"]["parameters"] for tool in schemas
                if tool["function"]["name"] == name)


def _validate_arguments(args, schema):
    if not isinstance(args, dict) or schema.get("type") != "object":
        raise AssertionError("tool arguments must be a JSON object")
    required = schema.get("required", [])
    if any(key not in args for key in required):
        raise AssertionError("tool arguments omit a required property")
    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False and any(key not in properties for key in args):
        raise AssertionError("tool arguments contain an unsupported property")
    for key, value in args.items():
        kind = properties[key].get("type")
        valid = {
            "string": lambda item: isinstance(item, str),
            "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
            "array": lambda item: isinstance(item, list),
        }.get(kind)
        if valid is None or not valid(value):
            raise AssertionError(f"tool argument {key!r} has invalid type")
        if kind == "array" and properties[key].get("items", {}).get("type") == "string":
            if any(not isinstance(item, str) for item in value):
                raise AssertionError(f"tool argument {key!r} must contain only strings")


def _call(client, schemas, history, latest_plan):
    messages = assemble(SYSTEM, REQUEST, history, "", schemas,
                        client.count_tokens, latest_plan=latest_plan)
    user_index = next(i for i, item in enumerate(messages) if item["role"] == "user")
    if any(item["role"] == "system" for item in messages[user_index + 1:]):
        raise AssertionError("post-user system message in recovery context")
    prompt_tokens = client.count_tokens(messages, schemas)
    if prompt_tokens > WINDOW - REPLY:
        raise AssertionError(f"recovery context exceeds fixed usable budget: {prompt_tokens}")
    message, usage = client.chat(messages, schemas, seed=1)
    name, args = _one_action(message, schemas)
    if len(message.get("tool_calls") or []) != 1:
        raise AssertionError("model did not return exactly one structured call")
    _validate_arguments(args, _schema_for(schemas, name))
    return messages, message, name, args, prompt_tokens, usage


def main():
    client = LlamaClient(BASE_URL, MODEL_ALIAS, timeout=300)
    schemas = tool_schemas(False)
    bad_message = {
        "role": "assistant",
        "content": "",
        "tool_calls": [{
            "id": "injected-truncated-call",
            "type": "function",
            "function": {"name": "edit_file", "arguments":
                         '{"path":"synthetic-only.txt","new":"TRUNCATED_CANARY'},
        }],
    }
    history = []
    try:
        context_per_slot = client.check_context(16384)
        template_renders_tools = client._template_renders_tools(schemas)
        if not template_renders_tools:
            raise RuntimeError("active model template does not render the GAS-0 tool schemas")
        active_template = client._get("/props").get("chat_template", "")
        active_template_sha256 = hashlib.sha256(active_template.encode("utf-8")).hexdigest()
        try:
            _one_action(bad_message, schemas)
            raise AssertionError("injected malformed call unexpectedly parsed")
        except ValueError as exc:
            parse_error = str(exc)
        history.append(_repair_message())
        if "TRUNCATED_CANARY" in json.dumps(history):
            raise AssertionError("malformed tool call leaked into replay history")

        _, response1, name1, args1, tokens1, usage1 = _call(
            client, schemas, history, latest_plan=""
        )
        if name1 != "plan":
            raise AssertionError(f"repair retry did not produce the required plan call: {name1}")
        call1 = response1["tool_calls"][0]
        history.extend([
            {"role": "assistant", "content": response1.get("content") or "",
             "tool_calls": response1["tool_calls"]},
            {"role": "tool", "tool_call_id": call1["id"], "name": name1,
             "arguments": args1, "content": json.dumps({"result": "synthetic plan recorded"})},
        ])

        latest_plan = json.dumps(args1["steps"], ensure_ascii=False)
        _, response2, name2, args2, tokens2, usage2 = _call(
            client, schemas, history, latest_plan=latest_plan
        )
        if name2 != "read_file" or args2 != {"path": "synthetic-recovery-only.txt"}:
            raise AssertionError(f"tool-result continuation mismatch: {name2} {args2!r}")

        report = {
            "model": "Qwen3.5-9B Q6_K",
            "synthetic_only": True,
            "runtime": "llama.cpp b11193 / commit 4e7481175",
            "model_alias": MODEL_ALIAS,
            "context_tokens_per_sequence": context_per_slot,
            "parallel_tool_calls": False,
            "active_template_renders_tools": template_renders_tools,
            "active_template_sha256": active_template_sha256,
            "injected_failure": {
                "type": "truncated JSON arguments",
                "rejected_by_one_action": True,
                "error": parse_error,
                "raw_invalid_call_in_replay": False,
                "synthetic_tool_result_created": False,
                "safe_repair_turn_present": True,
            },
            "recovery": {
                "repair_call_name": name1,
                "repair_arguments_valid": True,
                "next_call_name": name2,
                "next_call_arguments_valid": True,
                "one_structured_call_per_response": True,
                "tool_result_continuation": True,
                "prompt_tokens": [tokens1, tokens2],
                "completion_tokens": [usage1["completion_tokens"], usage2["completion_tokens"]],
                "peak_context_tokens": max(
                    tokens1 + usage1["completion_tokens"],
                    tokens2 + usage2["completion_tokens"],
                ),
            },
            "template_invalid_history": False,
            "http_500": False,
            "apply_template_failure": False,
            "passed": True,
        }
    except HTTPError as exc:
        report = {
            "model": "Qwen3.5-9B Q6_K",
            "synthetic_only": True,
            "passed": False,
            "http_500": exc.code == 500,
            "failure": f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:1200]}",
        }
    except Exception as exc:
        report = {
            "model": "Qwen3.5-9B Q6_K",
            "synthetic_only": True,
            "passed": False,
            "http_500": False,
            "failure": f"{type(exc).__name__}: {exc}",
        }

    output = ROOT / "experiments" / "gas0" / "analysis" / "qwen35_malformed_recovery_preflight_20260929.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
