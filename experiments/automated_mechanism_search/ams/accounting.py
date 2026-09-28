"""Resource accounting: parameters, persistent state, FLOPs, and the cumulative CPU ledger
with the 30 CPU-hour hard cap (prereg v2 sec. 13)."""
from __future__ import annotations

import json
import os
import resource
import time
from typing import Dict

from .substrate import Learner, Net, learner_flops_per_example

CPU_CAP_HOURS = 30.0
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(HERE, "runs", "cpu_ledger.json")


class CPUCapExceeded(Exception):
    pass


def self_cpu_seconds() -> float:
    """CPU of this process only (workers are accounted by their own returned deltas)."""
    s = resource.getrusage(resource.RUSAGE_SELF)
    return s.ru_utime + s.ru_stime


def process_cpu_seconds() -> float:
    s = resource.getrusage(resource.RUSAGE_SELF)
    c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return s.ru_utime + s.ru_stime + c.ru_utime + c.ru_stime


def load_ledger(path: str = LEDGER) -> Dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"cap_cpu_hours": CPU_CAP_HOURS, "entries": [], "total_cpu_seconds": 0.0}


def record(stage: str, cpu_seconds: float, wall_seconds: float, note: str = "", path: str = LEDGER) -> Dict:
    led = load_ledger(path)
    led["entries"].append({"stage": stage, "cpu_seconds": round(cpu_seconds, 3),
                           "wall_seconds": round(wall_seconds, 3), "note": note,
                           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    led["total_cpu_seconds"] = round(sum(e["cpu_seconds"] for e in led["entries"]), 3)
    led["total_cpu_hours"] = round(led["total_cpu_seconds"] / 3600.0, 5)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(led, f, indent=1)
    return led


def check_cap(extra_seconds: float = 0.0, path: str = LEDGER):
    led = load_ledger(path)
    if (led["total_cpu_seconds"] + extra_seconds) / 3600.0 >= CPU_CAP_HOURS:
        raise CPUCapExceeded(f"{led['total_cpu_seconds'] / 3600:.3f} CPU-h used")


def resources(net: Net, learner: Learner) -> Dict:
    params = net.n_params()
    state = learner.state_floats(net)
    return {"params": params, "state_floats": state, "state_bytes": 4 * state,
            "flops_per_example": learner_flops_per_example(net, learner)}
