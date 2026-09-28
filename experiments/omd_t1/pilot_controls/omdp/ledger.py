"""CPU accounting for OMD-PILOT-1.

Two ledgers:
- the pilot ledger (results/cpu_ledger_pilot.json), which enforces the 1.0 CPU-hour pilot cap;
- the shared project ledger (experiments/automated_mechanism_search/runs/cpu_ledger.json).

Every measured piece of work (development tests included) is appended to both."""
from __future__ import annotations

import json
import os
import resource
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PILOT_LEDGER = os.path.join(HERE, "results", "cpu_ledger_pilot.json")
SHARED_LEDGER = os.path.join(REPO, "experiments", "automated_mechanism_search", "runs", "cpu_ledger.json")
PILOT_CAP_HOURS = 1.0
PROJECT_BEFORE_HOURS = 5.12737


class PilotCapExceeded(Exception):
    pass


def cpu_seconds() -> float:
    """CPU of this process and all waited-for children."""
    s = resource.getrusage(resource.RUSAGE_SELF)
    c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return s.ru_utime + s.ru_stime + c.ru_utime + c.ru_stime


def _load(path, cap):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"cap_cpu_hours": cap, "entries": [], "total_cpu_seconds": 0.0}


def _append(path, cap, entry):
    led = _load(path, cap)
    led["entries"].append(entry)
    led["total_cpu_seconds"] = round(sum(e["cpu_seconds"] for e in led["entries"]), 3)
    led["total_cpu_hours"] = round(led["total_cpu_seconds"] / 3600.0, 5)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(led, f, indent=1)
    return led


def pilot_used_seconds() -> float:
    return _load(PILOT_LEDGER, PILOT_CAP_HOURS).get("total_cpu_seconds", 0.0)


def record(stage: str, cpu_s: float, wall_s: float, note: str = ""):
    entry = {"stage": stage, "cpu_seconds": round(cpu_s, 3), "wall_seconds": round(wall_s, 3),
             "note": note, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _append(PILOT_LEDGER, PILOT_CAP_HOURS, entry)
    shared = dict(entry, stage="omd_pilot1_" + stage)
    return _append(SHARED_LEDGER, 30.0, shared)


def check_cap(in_process_cpu_s: float = 0.0, margin_s: float = 0.0):
    used = pilot_used_seconds() + in_process_cpu_s + margin_s
    if used >= PILOT_CAP_HOURS * 3600.0:
        raise PilotCapExceeded(f"pilot CPU {used / 3600:.4f} h would reach the 1.0 h cap")
    return used


class Measured:
    """Context manager that measures CPU/wall of a block and records it in both ledgers."""

    def __init__(self, stage: str, note: str = ""):
        self.stage, self.note = stage, note

    def __enter__(self):
        self.c0, self.w0 = cpu_seconds(), time.time()
        check_cap()
        return self

    def elapsed_cpu(self):
        return cpu_seconds() - self.c0

    def __exit__(self, *exc):
        record(self.stage, cpu_seconds() - self.c0, time.time() - self.w0,
               self.note + ("" if exc[0] is None else f" [ended with {exc[0].__name__}]"))
        return False
