"""DEV-pilot GPU-time cap guard for pilot runners. Not part of the harness.

The GPU-time upper bound charges each model request its wall time. The guard
starts a request only if that request's worst case still fits under the cap.
The worst case is the client's per-request timeout plus a small slack for
reading the response. llama.cpp sends a non-streaming chat completion only
when it is finished, so no byte arrives before the end: the socket timeout
ends any request that runs longer and raises an error. Every started request
is charged its measured duration, including requests that fail.

The earlier guard (`run_qwen35_c4_postfix.py`) reserved a fixed 60 s. A 75.7 s
request then overshot the cap by 12.8 s.

`cap_seconds=None` means no cumulative cap. The owner lifted the post-fix
pilot's 3-hour cap during C1. The per-request timeout and the charging stay
in force either way.
"""
from __future__ import annotations

import time

RESPONSE_SLACK_SECONDS = 5.0


class PilotBudgetExhausted(RuntimeError):
    pass


class CappedClient:
    """Forwards to the frozen client; refuses a request whose worst case could cross the cap."""

    def __init__(self, inner, cap_seconds: float | None, used_before: float = 0.0, clock=time.monotonic):
        timeout = getattr(inner, "timeout", None)
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("client needs a positive per-request timeout")
        self.inner = inner
        self.cap = None if cap_seconds is None else float(cap_seconds)
        self.used_before = float(used_before)
        self.clock = clock
        self.reservation = float(timeout) + RESPONSE_SLACK_SECONDS
        self.spent = 0.0
        self.calls = 0
        self.failed_calls = 0
        self.failed_seconds = 0.0

    def remaining(self) -> float:
        if self.cap is None:
            return float("inf")
        return self.cap - self.used_before - self.spent

    def check_context(self, minimum=16384):
        return self.inner.check_context(minimum)

    def count_tokens(self, value, tools=None):
        return self.inner.count_tokens(value, tools)

    def chat(self, messages, tools, seed, max_tokens=1024):
        if self.reservation > self.remaining():
            raise PilotBudgetExhausted(
                f"GPU cap: {self.used_before + self.spent:.3f}s used of {self.cap}s; "
                f"the next request needs a {self.reservation:.0f}s worst-case reservation")
        start = self.clock()
        try:
            message, usage = self.inner.chat(messages, tools, seed, max_tokens)
        except BaseException:
            elapsed = self.clock() - start
            self.spent += elapsed
            self.failed_calls += 1
            self.failed_seconds += elapsed
            raise
        self.spent += max(self.clock() - start, usage["wall_seconds"])
        self.calls += 1
        return message, usage

    def stats(self) -> dict:
        return {"cap_seconds": self.cap, "used_before_seconds": self.used_before,
                "reservation_seconds": self.reservation, "charged_seconds": self.spent,
                "completed_requests": self.calls, "failed_requests": self.failed_calls,
                "failed_request_seconds": self.failed_seconds}
