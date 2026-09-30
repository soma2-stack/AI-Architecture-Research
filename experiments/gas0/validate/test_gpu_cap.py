"""CPU/mock tests for the DEV-pilot GPU-time cap guard (analysis/gpu_cap.py)."""
from __future__ import annotations

import json
import random
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from analysis.gpu_cap import RESPONSE_SLACK_SECONDS, CappedClient, PilotBudgetExhausted
from harness.llm_client import LlamaClient


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class TimedFakeClient:
    """Each request takes the next scripted duration; one that exceeds the timeout raises."""

    def __init__(self, clock, durations, timeout=300):
        self.clock = clock
        self.durations = list(durations)
        self.timeout = timeout
        self.requests = 0

    def chat(self, messages, tools, seed, max_tokens=1024):
        self.requests += 1
        duration = self.durations.pop(0)
        if duration > self.timeout:
            self.clock.now += self.timeout
            raise socket.timeout("timed out")
        self.clock.now += duration
        return {"role": "assistant"}, {"wall_seconds": duration, "prompt_tokens": 1,
                                       "completion_tokens": 1, "peak_context_tokens": 2}


def test_reservation_is_timeout_plus_slack():
    clock = FakeClock()
    capped = CappedClient(TimedFakeClient(clock, []), 10_800, clock=clock)
    assert capped.reservation == 300 + RESPONSE_SLACK_SECONDS


def test_request_refused_without_calling_server_when_worst_case_does_not_fit():
    clock = FakeClock()
    inner = TimedFakeClient(clock, [10.0])
    capped = CappedClient(inner, 1_000, used_before=1_000 - 304.9, clock=clock)
    with pytest.raises(PilotBudgetExhausted):
        capped.chat([], [], 1)
    assert inner.requests == 0 and capped.spent == 0


def test_recorded_overshoot_case_is_now_refused():
    # Previous guard: 10,727.2 s used, 60 s reservation -> allowed a 75.7 s call.
    clock = FakeClock()
    inner = TimedFakeClient(clock, [75.687])
    capped = CappedClient(inner, 10_800, used_before=10_727.119, clock=clock)
    with pytest.raises(PilotBudgetExhausted):
        capped.chat([], [], 1)
    assert inner.requests == 0


@pytest.mark.parametrize("trial", range(20))
def test_charged_time_never_exceeds_cap(trial):
    rng = random.Random(trial)
    clock = FakeClock()
    # Durations up to and beyond the timeout, including 75.7 s-style outliers.
    durations = [rng.choice([rng.uniform(1, 40), rng.uniform(40, 300), 400.0]) for _ in range(500)]
    inner = TimedFakeClient(clock, durations)
    used_before = rng.uniform(0, 5_000)
    capped = CappedClient(inner, 10_800, used_before=used_before, clock=clock)
    while True:
        try:
            capped.chat([], [], 1)
        except PilotBudgetExhausted:
            break
        except socket.timeout:
            continue
    assert used_before + capped.spent <= 10_800
    assert capped.remaining() < capped.reservation


def test_failed_request_time_is_charged():
    clock = FakeClock()
    capped = CappedClient(TimedFakeClient(clock, [1_000.0, 5.0]), 10_800, clock=clock)
    with pytest.raises(socket.timeout):
        capped.chat([], [], 1)
    assert capped.failed_calls == 1 and capped.failed_seconds == 300 and capped.spent == 300
    capped.chat([], [], 1)
    assert capped.spent == 305 and capped.calls == 1


def test_client_without_timeout_is_rejected():
    class NoTimeout:
        timeout = None
    with pytest.raises(ValueError):
        CappedClient(NoTimeout(), 100)


class _SlowHandler(BaseHTTPRequestHandler):
    delay = 3.0

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        time.sleep(self.delay)
        body = json.dumps({"choices": [{"message": {"role": "assistant"}}], "usage": {}}).encode()
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except OSError:
            pass

    def log_message(self, *args):
        pass


def test_real_client_timeout_bounds_a_silent_request():
    """A non-streaming request that sends no bytes is cut off at the client timeout."""
    server = HTTPServer(("127.0.0.1", 0), _SlowHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        client = LlamaClient(f"http://127.0.0.1:{server.server_port}", "mock", timeout=0.5)
        capped = CappedClient(client, 100)
        start = time.monotonic()
        with pytest.raises(OSError):   # socket.timeout / URLError(timeout)
            capped.chat([{"role": "user", "content": "x"}], [], 1)
        elapsed = time.monotonic() - start
        assert elapsed < 0.5 + RESPONSE_SLACK_SECONDS
        assert capped.failed_calls == 1 and 0.4 < capped.spent < capped.reservation
    finally:
        server.shutdown()
        server.server_close()


def test_no_cumulative_cap_still_charges_and_times_out():
    clock = FakeClock()
    inner = TimedFakeClient(clock, [100.0] * 200 + [1_000.0])
    capped = CappedClient(inner, None, used_before=50_000, clock=clock)
    for _ in range(200):
        capped.chat([], [], 1)
    assert capped.spent == 20_000 and capped.remaining() == float("inf")
    with pytest.raises(socket.timeout):
        capped.chat([], [], 1)
    assert capped.failed_seconds == 300
    assert capped.stats()["cap_seconds"] is None
