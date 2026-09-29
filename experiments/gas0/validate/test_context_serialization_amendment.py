from __future__ import annotations

import pytest

from harness.conditions import CONDITIONS
from harness.context import LEDGER, REPLY, WINDOW, assemble, elide


def word_count(messages, tools=None):
    if isinstance(messages, str):
        return len(messages.split())
    return sum(len(str(message.get("content", "")).split()) for message in messages)


def assembled(cell, history=None, request="stage request", ledger="", plan="latest plan",
              count_tokens=word_count):
    condition = CONDITIONS[cell]
    return assemble("base GAS-0 instructions", request, history or [],
                    ledger if condition.ledger else "", [], count_tokens, plan)


def test_context_has_only_leading_system_before_current_user():
    prompt = assembled("C4", history=[
        {"role": "assistant", "content": "prior action"},
        {"role": "tool", "content": "prior result"},
    ], ledger="synthetic ledger")
    user_index = next(i for i, item in enumerate(prompt) if item["role"] == "user")
    assert prompt[0] == {"role": "system", "content": "base GAS-0 instructions"}
    assert not any(item["role"] == "system" for item in prompt[user_index + 1:])
    assert [item["role"] for item in prompt[:user_index + 1]] == ["system", "user"]


def test_cell_payload_information_access_and_order():
    c0 = assembled("C0", request="REQUEST_SENTINEL", ledger="LEDGER_SENTINEL", plan="PLAN_SENTINEL")
    c0_text = c0[1]["content"]
    assert "CURRENT STAGE REQUEST:\nREQUEST_SENTINEL" in c0_text
    assert "LATEST PLAN:\nPLAN_SENTINEL" in c0_text
    assert "PROJECT LEDGER" not in c0_text and "LEDGER_SENTINEL" not in c0_text

    for cell in ("C1", "C3", "C4"):
        prompt = assembled(cell, request="REQUEST_SENTINEL", ledger="LEDGER_SENTINEL",
                           plan="PLAN_SENTINEL")
        text = prompt[1]["content"]
        assert "CURRENT STAGE REQUEST:\nREQUEST_SENTINEL" in text
        assert "PROJECT LEDGER:\nLEDGER_SENTINEL" in text
        assert "LATEST PLAN:\nPLAN_SENTINEL" in text
        assert text.index("CURRENT STAGE REQUEST:") < text.index("PROJECT LEDGER:") < text.index("LATEST PLAN:")

    c2 = assembled("C2", request="REQUEST_SENTINEL", ledger="LEDGER_SENTINEL", plan="PLAN_SENTINEL")
    assert "LEDGER_SENTINEL" not in c2[1]["content"]


def test_optional_ledger_and_plan_sections_are_omitted_when_absent():
    prompt = assemble("sys", "request", [], "", [], word_count, "")
    assert len(prompt) == 2
    assert prompt[1]["content"] == "CURRENT STAGE REQUEST:\nrequest"


def test_ledger_budget_is_still_capped_at_1536_tokens():
    prompt = assemble("sys", "request", [], "ledger " * LEDGER, [], word_count, "plan")
    assert "PROJECT LEDGER:" in prompt[1]["content"]
    with pytest.raises(ValueError, match="ledger exceeds token budget"):
        assemble("sys", "request", [], "ledger " * (LEDGER + 1), [], word_count, "plan")


def test_context_budget_and_history_elision_are_unchanged():
    history = [{"role": "tool", "name": "read_file", "arguments": {"i": i},
                "content": "old " * 1500} for i in range(8)]
    prompt = assemble("sys", "request " * 30, history, "ledger " * 100,
                      [], word_count, "plan " * 30)
    assert word_count(prompt) <= WINDOW - REPLY
    tool_results = [item for item in prompt if item["role"] == "tool"]
    assert len(tool_results) == 8
    assert all(item["content"].startswith("[elided:") for item in tool_results[:2])
    assert tool_results[-1]["content"].startswith("old ")


def test_request_and_plan_are_not_trimmed_and_no_future_text_is_added():
    request = "STAGE_4_REQUEST_ONLY"
    plan = "STAGE_4_PLAN_ONLY"
    history = [{"role": "assistant", "content": "old " * 20000}]
    prompt = assemble("sys", request, history, "", [], word_count, plan)
    assert prompt[1]["content"] == (
        "CURRENT STAGE REQUEST:\nSTAGE_4_REQUEST_ONLY\n\nLATEST PLAN:\nSTAGE_4_PLAN_ONLY"
    )
    assert not any("FUTURE_STAGE" in str(item) for item in prompt)
    assert len(prompt) == 2
