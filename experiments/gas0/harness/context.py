"""Identical context policy for every condition."""
from __future__ import annotations

import json

WINDOW = 16384
REPLY = 1024
LEDGER = 1536


def elide(history: list[dict], keep_tool_outputs=6):
    result = [dict(m) for m in history]
    tool_indices = [i for i, m in enumerate(result) if m["role"] == "tool"]
    for i in tool_indices[:-keep_tool_outputs]:
        m = result[i]
        m["content"] = ("[elided: " + m.get("name", "tool") + " " +
                        json.dumps(m.get("arguments", {}), sort_keys=True)[:120] + "]")
    return result


def assemble(system: str, request: str, history: list[dict], ledger_view: str,
             tools: list[dict], count_tokens, latest_plan: str = ""):
    """Trim only old history; never trim system, current request, ledger or plan."""
    fixed = [{"role": "system", "content": system},
             {"role": "user", "content": "CURRENT STAGE REQUEST:\n" + request}]
    if ledger_view:
        if count_tokens(ledger_view) > LEDGER:
            raise ValueError("ledger exceeds token budget")
        fixed.append({"role": "system", "content": "PROJECT LEDGER:\n" + ledger_view})
    if latest_plan:
        fixed.append({"role": "system", "content": "LATEST PLAN:\n" + latest_plan})
    past = elide(history)
    while count_tokens(fixed + past, tools) > WINDOW - REPLY and past:
        past.pop(0)
    prompt = fixed + [{k: v for k, v in m.items()
                       if k in {"role", "content", "tool_calls", "tool_call_id"}}
                      for m in past]
    if count_tokens(prompt, tools) > WINDOW - REPLY:
        raise ValueError("fixed context exceeds usable budget")
    return prompt
