"""Smoke/consistency tests of the Experiment 012 analysis on a tiny synthetic factorial plus hand-checkable partitions."""
import json
from pathlib import Path

import pytest

from prototypes.rnn_llm_architecture import capacity_012 as c12
from prototypes.rnn_llm_architecture import experiment_012_report as rep

SEEDS = c12.SEEDS


def test_partition_is_exact_for_additive_and_interaction_patterns():
    additive = {(i, d): float(ix) for ix, i in enumerate(SEEDS) for d in SEEDS}      # depends only on init
    p = rep.shares(rep.partition(additive))
    assert p["init"] == pytest.approx(1.0) and p["data"] == pytest.approx(0.0) and p["remainder"] == pytest.approx(0.0, abs=1e-12)
    assert rep.verdict(p["init"], p["data"]) == "initialization favoured"
    by_data = {(i, d): float(dx) for i in SEEDS for dx, d in enumerate(SEEDS)}
    q = rep.shares(rep.partition(by_data))
    assert q["data"] == pytest.approx(1.0) and rep.verdict(q["init"], q["data"]) == "training data favoured"
    diag = {(i, d): 1.0 if i == d else 0.0 for i in SEEDS for d in SEEDS}            # pure interaction
    r = rep.shares(rep.partition(diag))
    assert r["remainder"] > .6 and rep.verdict(r["init"], r["data"]) == "neither factor consistent / unexplained"
    assert rep.shares(rep.partition({k: 1.0 for k in additive})) == {"init": 0.0, "data": 0.0, "remainder": 0.0}


def test_full_pipeline_on_tiny_factorial(tmp_path):
    cfg = c12.Config(steps=6, batch=4, delay=8, eval_delays=(8, 16, 32, 64), eval_histories=32, checkpoint_every=3,
                     checkpoint_histories=32, loss_window=2, max_wall_seconds=300)
    # eval delays must be keys "64".. for the report; use real delay names with tiny histories
    c12.execute(cfg, tmp_path / "all.json")
    runs, skipped = rep.load_runs(tmp_path)
    assert len(runs) == 36 and not skipped
    out = rep.analyze(runs, skipped, None)
    assert out["incomplete"] == [] and out["same_eval_set_all_runs"] is True
    assert set(out["stream_hash_per_data_seed"].values()) == {1}
    assert set(out["init_fingerprint_per_arch_init"].values()) == {1}
    assert out["pooled_partition_final_loss"]["verdict"]
    text = rep.md(out, runs, skipped)
    assert text.count("3 × 3 matrices") == 4 and "Retention" in text and "Seed 43" in text
    rep.main([str(tmp_path)])
    assert (tmp_path / "tables.md").exists() and (tmp_path / "summary.json").exists()
    assert (tmp_path / "figures" / "learning_curves_gru24.png").stat().st_size > 1000
    json.loads((tmp_path / "summary.json").read_text())
