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


def test_joint_oracle_runs_and_batches_are_16_plus_16(monkeypatch):
    seen = []
    orig = TaskB._sample

    def spy(self, task, n, rng):
        seen.append((task, n))
        return orig(self, task, n, rng)

    monkeypatch.setattr(TaskB, "_sample", spy)
    before = len(seen)
    r = runners.run_B_joint(make("SGD"), [7], updates=5)
    calls = seen[before:]
    train_calls = [c for c in calls if c[1] == 16]
    assert train_calls == [(1, 16), (2, 16)] * 5
    sel = runners.select_lr(r, [7])
    s = runners.summarize("Bjoint", sel)
    assert "rel_red_T1" in s and "rel_red_T2" in s


def test_fit_reduction_summary(short):
    r = run_job({"task": "B", "learner": "SGD", "seeds": [7]})
    s = runners.summarize("B", runners.select_lr(r, [7]))
    p = runners.select_lr(r, [7])["per_seed"][0]
    assert abs(s["fit_reduction"] - (1 - p["L1_pre"] / p["L1_init"])) < 1e-12
