"""Pins the Experiment 011 audit facts to the archived raw JSON (read-only)."""
from pathlib import Path

import pytest

from prototypes.rnn_llm_architecture.audit_011 import audit

RAW = Path(__file__).parent / "reports" / "experiment_011"


@pytest.fixture(scope="module")
def result():
    return audit(RAW)


def test_all_reported_values_are_valid_fractions_and_baselines_regenerate(result):
    assert result["n_runs"] == 15 and result["n_learned"] == 12
    assert result["non_integral_accuracy_values"] == 0
    assert result["baselines_regenerated_identical"] is True
    assert set(result["stream_hashes_per_seed_unique"].values()) == {1}


def test_seventy_percent_count_depends_on_definition(result):
    assert result["per_slot_ge70_checkpoint_definition"]["count"] == 6
    assert result["per_slot_ge70_final_eval_definition"]["count"] == 7
    assert result["discordant"] == [("gru32", 29)]
    d = result["discordant_detail"]["gru32:29"]
    assert d["checkpoint_max"] < .7 <= d["final_eval"]


def test_solved_runs_and_independent_guess_baseline(result):
    assert sorted(result["solved_ge90_whole_varied_64"]) == [("gru32", 43), ("protected", 43)]
    assert abs(result["independent_guess_reported_6_9_is_whole_at_64_mean_of_3_sets"] - .069) < .0005
    assert result["independent_guess_theory"]["whole"] == 1 / 16
    assert abs(result["independent_guess_theory"]["whole_varied"] - 1 / 16) < 1e-12
