"""Named learner factories (picklable by name) for official controls and candidates, plus
parallel job execution with per-worker CPU accounting (D-T1-7)."""
from __future__ import annotations

import os
import time
from typing import Callable, Dict, Optional

from .canon import canon
from .families import REFERENCES
from .grammar import Program, program_from_dict
from .substrate import GPM, SGD, SGDM, AdamW, Learner, ProgramLearner

GENERIC = ("SGD", "SGDM", "AdamW")


def make(name: str, program: Optional[dict] = None) -> Callable[[], Learner]:
    """Factory for a learner by name.  'P' = candidate program (dict form)."""
    if name == "SGD":
        return lambda: SGD(clip=True)
    if name == "SGDM":
        return lambda: SGDM(clip=True)
    if name == "AdamW":
        return lambda: AdamW(clip=True)
    if name == "SGD_noclip":
        return lambda: SGD(clip=False)
    if name == "SGDM_noclip":
        return lambda: SGDM(clip=False)
    if name == "AdamW_noclip":
        return lambda: AdamW(clip=False)
    if name == "GPM":
        return lambda: GPM(clip=True)
    if name in REFERENCES:
        prog = canon(REFERENCES[name])
        return lambda: ProgramLearner(prog, name=name)
    if name == "P":
        prog = program_from_dict(program)
        return lambda: ProgramLearner(prog, name="P")
    raise ValueError(name)


def run_job(job: Dict) -> Dict:
    """Worker entry: job = {task, learner, seeds, program?, kwargs?}.  Returns the runner
    result with 'cpu_s' (this process's CPU for the job)."""
    from . import runners
    t0 = time.process_time()
    f = runners.RUNNERS[job["task"]]
    res = f(make(job["learner"], job.get("program")), job["seeds"], **job.get("kwargs", {}))
    res["cpu_s"] = time.process_time() - t0
    res["learner"] = job["learner"]
    return res


def init_worker():
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        os.nice(10)
    except OSError:
        pass
