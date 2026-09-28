"""Plumbing test for every Stage-1 control on every task (shortened schedules, non-official
seed 7).  Checks only that runners, selection and summaries execute; no performance claims."""
import pytest

from ams import runners
from ams.controls import GENERIC, make, run_job
from ams.tasks import TaskB, TaskCstar, TaskF

CONTROLS = {"B": GENERIC + ("GPM", "R17_EWC_SI", "R18_kWTA_sparse_update", "R13_fast_slow", "SGD_noclip"),
            "Cstar": GENERIC + ("R12_fast_weights", "R13_fast_slow", "R15_three_factor", "AdamW_noclip"),
            "F": GENERIC + ("SGDM_noclip",)}


@pytest.fixture
def short(monkeypatch):
    monkeypatch.setattr(TaskB, "n1", 50)
    monkeypatch.setattr(TaskB, "n2", 50)
    monkeypatch.setattr(TaskCstar, "schedule", (("R0", 16), ("R1", 8), ("R0", 8), ("R1", 8)))
    monkeypatch.setattr(TaskF, "n_updates", 50)


@pytest.mark.parametrize("task", ["B", "Cstar", "F"])
def test_all_controls_run(short, task):
    for m in CONTROLS[task]:
        r = run_job({"task": task, "learner": m, "seeds": [7]})
        assert "error" not in r, (task, m, r.get("error"))
        sel = runners.select_lr(r, [7])
        s = runners.summarize(task, sel)
        assert "stable" in s
        assert r["cpu_s"] >= 0


def test_run_D_and_T0():
    r = runners.run_D("natgrad", [7], 1e4)
    assert len(r["runs"]) == 3
    t0 = runners.run_T0(make("SGD"), seed=7)
    assert "pass" in t0
