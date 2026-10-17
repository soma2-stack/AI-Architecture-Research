"""Deterministic, small checks for Experiment 011 (training stream identity, baselines, bounded runs)."""
import json

import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_010 as c10
from prototypes.rnn_llm_architecture.capacity_011 import (Config, LEARNED, baselines, eval_seed, evaluate,
                                                          execute, parse_jobs, run_one, training_batch, training_seed)


def small(**kw):
    base = dict(steps=4, batch=4, delay=8, eval_delays=(8, 16), eval_histories=32, checkpoint_every=2,
                checkpoint_histories=32, loss_window=2, max_wall_seconds=60)
    base.update(kw)
    return Config(**base)


def test_training_stream_matches_experiment_010_formula():
    cfg = Config()
    for seed in (17, 29, 43):
        for step in (0, 1, 799, 2999):
            # capacity_010.run_one: seed*1_000_003+step*8191+slots*197+values
            assert training_seed(seed, step) == seed * 1_000_003 + step * 8191 + 4 * 197 + 2
    x, y = training_batch(cfg, 17, 5)
    assert torch.equal(x, c10.generator_batch(4, 2, 64, 12, seed=training_seed(17, 5)))
    assert torch.equal(y, c10.replay(x, 4, 2))


def test_eval_seeds_disjoint_from_training_seeds():
    train = {training_seed(s, t) for s in (17, 29, 43) for t in range(3000)}
    ev = {eval_seed(s, d) for s in (17, 29, 43) for d in (64, 128, 256, 512)}
    ev |= {eval_seed(s, 64) + 1 for s in (17, 29, 43)}   # checkpoint stream
    assert not train & ev


def test_identical_training_data_across_architectures():
    cfg = small()
    a = run_one("gru24", 17, cfg, float("inf"))
    b = run_one("protected", 17, cfg, float("inf"))
    assert a["training_stream_sha256"] == b["training_stream_sha256"]
    assert a["steps"] == b["steps"] == 4 and a["status"] == "complete"
    assert run_one("gru24", 29, cfg, float("inf"))["training_stream_sha256"] != a["training_stream_sha256"]


def test_baselines_match_expectations():
    x = c10.generator_batch(4, 2, 64, 512, seed=99)
    y = c10.replay(x, 4, 2)
    b = baselines(x, y, 99)
    assert abs(b["independent_guess"]["per_slot"] - .5) < .04
    assert b["last_write_copy"]["whole_varied"] == 0.0
    assert b["analytic_guess_whole"] == 1 / 16


def test_evaluate_reports_required_fields():
    model = c10.build("gru24", 4, 2, 1)
    e = evaluate(model, 16, seed=5, histories=32, with_baselines=True)
    assert {"per_slot", "whole", "whole_varied", "histories", "baselines"} <= set(e)
    assert model.training


def test_bounded_run_exclusive_output_and_partial_preservation(tmp_path):
    cfg = small(jobs=(("gru24", 17), ("protected_no_retain", 17)))
    p = tmp_path / "r.json"
    r = execute(cfg, p)
    assert r["status"] == "complete" and len(r["runs"]) == 2
    assert all(set(x["eval"]) == {"8", "16"} for x in r["runs"])
    assert len(r["runs"][0]["checkpoints"]) == 1 and r["runs"][0]["parameters"] > 0
    with pytest.raises(FileExistsError):
        execute(cfg, p)
    q = tmp_path / "t.json"
    # deadline already passed: nothing trains, every job is recorded as skipped (never silently dropped)
    r2 = execute(small(max_wall_seconds=1e-9, steps=50), q)
    saved = json.loads(q.read_text())
    assert r2["status"] == "incomplete" and saved["status"] == "incomplete"
    assert len(saved["runs"]) + len(saved["skipped"]) == len(small().jobs)
    # deadline expiring mid-training keeps the partial run and evaluates what was trained
    row = run_one("gru24", 17, small(steps=10_000), deadline=__import__("time").monotonic() + 0.5)
    assert row["status"] == "time_limit" and 0 < row["steps"] < 10_000 and "8" in row["eval"]


def test_invalid_config_and_job_parsing():
    assert parse_jobs("gru24:17,protected:29") == (("gru24", 17), ("protected", 29))
    with pytest.raises(ValueError):
        Config(jobs=(("bad", 17),))
    with pytest.raises(ValueError):
        Config(jobs=(("gru24", 17), ("gru24", 17)))
    with pytest.raises(ValueError):
        Config(steps=0)
    assert set(LEARNED) == {"protected", "protected_no_retain", "gru24", "gru32"}
