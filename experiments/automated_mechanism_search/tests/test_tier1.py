"""Tier-1 evaluator plumbing (shortened schedules, non-official seed 7) and scoring rules."""
import math

import pytest

from ams import tier1
from ams.canon import canon
from ams.controls import GENERIC, run_job
from ams.families import REFERENCES
from ams.grammar import M, make_program
from ams.tasks import TaskB, TaskCstar, TaskF


class SerialPool:
    def map(self, f, jobs, chunksize=1):
        return [f(j) for j in jobs]


@pytest.fixture
def short(monkeypatch):
    monkeypatch.setattr(TaskB, "n1", 50)
    monkeypatch.setattr(TaskB, "n2", 50)
    monkeypatch.setattr(TaskCstar, "schedule", (("R0", 16), ("R1", 8), ("R0", 8), ("R1", 8)))
    monkeypatch.setattr(TaskF, "n_updates", 50)
    monkeypatch.setattr(tier1, "TIER1_SEEDS", [7, 8, 9])


def test_tier1_evaluate_end_to_end(short):
    jobs = [{"task": t, "learner": m, "seeds": tier1.TIER1_SEEDS} for t in tier1.TASKS for m in GENERIC]
    res = [run_job(j) for j in jobs]
    base = tier1.compute_baselines({f"{j['task']}:{j['learner']}": r for j, r in zip(jobs, res)})
    assert set(base["best_generic"]) == set(tier1.TASKS)
    p = canon(make_program("(neg (outer d_bp a))", "(neg d_bp)", w_eff="(mul r1 0.5)",
                           regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]))
    out = tier1.evaluate(p, base, SerialPool())
    assert "q" in out and "effects" in out
    if out["q"] is not None:
        assert out["best_task"] in tier1.TASKS and isinstance(out["tier1_pass_on_best"], bool)
        assert out["cost"]["flops_ratio"] > 1.0


def _base():
    return {"best_generic": {"B": {"metric": 100.0, "T2_final_mse": 0.02},
                             "Cstar": {"metric": 14.0}, "F": {"metric": 0.84}},
            "adamw": {"B": {"mean": 100.0, "sd": 1e-9}, "Cstar": {"mean": 17.6, "sd": 4.0},
                      "F": {"mean": 0.83, "sd": 0.01}}}


def _res(task, per_seed, lr=0.1):
    runs = [(s, l) for s in (1000, 1001, 1002) for l in (1e-3, 1e-2, 1e-1)]
    per = []
    for s, l in runs:
        d = per_seed if l == lr else {**per_seed, "train_select": 99.0, "train_select_tie": 99.0}
        per.append(dict(d))
    return {"task": task, "runs": runs, "unstable": [False] * 9, "per_run": per}


def test_score_rules(monkeypatch):
    monkeypatch.setattr(tier1, "TIER1_SEEDS", [1000, 1001, 1002])
    prog = canon(REFERENCES["R12_fast_weights"])
    B = _res("B", {"forgetting": 50.0, "retention": 50.0, "T2_final_mse": 0.02, "L1_pre": 0.01, "L1_post": 0.5,
                   "L1_init": 1.4, "train_select": 0.1})
    C = _res("Cstar", {"median_hl": 7.0, "median_hl_censored": 7.0, "half_lives": [7, 7], "R1_entry_mse": [1, 1],
                       "R0_pre_shift": 0.03, "R0_after_return": 0.03, "return_ok": True, "train_select": 0.1})
    F = _res("F", {"train_acc": 0.9, "ood_acc": 0.9, "sgg": 0.0, "train_ce": 0.1, "train_select": 0.9,
                   "train_select_tie": 0.1})
    out = tier1.score(prog, {"B": B, "Cstar": C, "F": F}, _base())
    assert out["effects"]["B"] == pytest.approx(0.5)                     # (100-50)/100
    assert out["effects"]["Cstar"] == pytest.approx((14 - 7) / 14)
    assert out["effects"]["F"] == 0.0                                     # train 0.90 < 0.98 -> min(e, 0)
    assert out["tier1_gate"]["B"]                                          # 100-50 >= 2e-9
    assert out["tier1_gate"]["Cstar"]                                      # 17.6-7 = 10.6 >= 2*4
    assert out["tier1_gate"]["F"] is False                                 # constraint violated
    assert out["best_task"] == "B"                                         # tie 0.5 / 0.5 -> task order B, Cstar, F
    assert out["tier1_pass_on_best"] is True


def test_score_constraint_B_T2(monkeypatch):
    monkeypatch.setattr(tier1, "TIER1_SEEDS", [1000, 1001, 1002])
    prog = canon(REFERENCES["R12_fast_weights"])
    B = _res("B", {"forgetting": 0.0, "retention": 100.0, "T2_final_mse": 0.5, "L1_pre": 0.01, "L1_post": 0.01,
                   "L1_init": 1.4, "train_select": 0.1})
    unstable = {"error": "TIMEOUT", "runs": [], "unstable": [True] * 9}
    out = tier1.score(prog, {"B": B, "Cstar": unstable, "F": unstable}, _base())
    assert out["effects"]["B"] == 0.0 and not out["constraints"]["B"]      # refuses to learn Task 2
    assert out["effects"]["Cstar"] == -math.inf and out["best_task"] == "B"
