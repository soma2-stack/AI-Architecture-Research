"""Stream separation, replication of Exp 011 on the diagonal, outcome definitions and bounded-run checks for Exp 012."""
import json
import time
from pathlib import Path

import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_010 as c10
from prototypes.rnn_llm_architecture import capacity_011 as c11
from prototypes.rnn_llm_architecture import capacity_012 as c12
from prototypes.rnn_llm_architecture.capacity_012 import (Config, analyze, eval_seed, execute, init_fingerprint, last_write_positions,
                                                          learning_onset, outcome_class, parse_jobs, run_one, training_seed)

RAW11 = Path(__file__).parent / "reports" / "experiment_011"


def small(**kw):
    base = dict(steps=6, batch=4, delay=8, eval_delays=(8, 16), eval_histories=32, checkpoint_every=3,
                checkpoint_histories=32, loss_window=2, max_wall_seconds=60)
    base.update(kw)
    return Config(**base)


def test_data_stream_formula_is_experiment_011s_and_eval_is_disjoint_and_fixed():
    for s in (17, 29, 43):
        for t in (0, 1, 2999):
            assert training_seed(s, t) == c11.training_seed(s, t)
    train = {training_seed(s, t) for s in (17, 29, 43) for t in range(3000)}
    ev = {eval_seed(d) for d in (64, 128, 256, 512)} | {c12.CHECKPOINT_EVAL_SEED}
    assert not train & ev and max(train) < c12.EVAL_BASE
    # evaluation seed takes only the delay: it cannot depend on init/data seed
    assert eval_seed.__code__.co_argcount == 1


def test_streams_are_separated():
    cfg = small()
    a = run_one("gru24", 17, 17, cfg, float("inf"))
    b = run_one("gru24", 17, 29, cfg, float("inf"))     # same init, different data
    c = run_one("gru24", 29, 17, cfg, float("inf"))     # different init, same data
    d = run_one("protected", 17, 17, cfg, float("inf"))  # different architecture, same data and init seed
    assert a["init_fingerprint_sha256"] == b["init_fingerprint_sha256"] != c["init_fingerprint_sha256"]
    assert a["training_stream_sha256"] == c["training_stream_sha256"] == d["training_stream_sha256"] != b["training_stream_sha256"]
    # evaluation histories are bit-identical across all runs (same seed per delay)
    assert a["eval"]["8"]["true_pattern_counts"] == b["eval"]["8"]["true_pattern_counts"] == c["eval"]["8"]["true_pattern_counts"]
    assert a["eval"]["8"]["baselines"]["independent_guess"] == d["eval"]["8"]["baselines"]["independent_guess"]


@pytest.mark.parametrize("name", ["gru24", "protected", "protected_no_retain"])
def test_diagonal_cell_replays_experiment_011_training_exactly(name):
    cfg12 = small(steps=8)
    cfg11 = c11.Config(jobs=((name, 17),), steps=8, batch=4, delay=8, eval_delays=(8,), eval_histories=32,
                       checkpoint_every=4, checkpoint_histories=32, loss_window=2, max_wall_seconds=60)
    r12 = run_one(name, 17, 17, cfg12, float("inf"))
    r11 = c11.run_one(name, 17, cfg11, float("inf"))
    assert r12["training_stream_sha256"] == r11["training_stream_sha256"]
    assert r12["loss_windows"] == r11["loss_windows"]
    assert r12["parameters"] == r11["parameters"]


def test_last_write_positions_consistent_with_replay():
    x = c10.generator_batch(4, 2, 40, 16, seed=5)
    y = c10.replay(x, 4, 2)
    pos = last_write_positions(x)
    assert (pos >= 0).all()
    assert torch.equal(x.gather(1, pos) - c10.VALUE_START, y)


def test_analyze_counts_are_internally_consistent():
    x = c10.generator_batch(4, 2, 40, 64, seed=9)
    y = c10.replay(x, 4, 2)
    g = torch.Generator().manual_seed(1)
    pred = torch.randint(2, y.shape, generator=g)
    a = analyze(pred, x, y)
    assert sum(v["n"] for v in a["by_last_write_age"].values()) == 64 * 4
    assert sum(v["correct"] for v in a["by_last_write_age"].values()) == int(pred.eq(y).sum())
    assert sum(a["pred_pattern_counts"]) == sum(a["true_pattern_counts"]) == 64
    assert abs(sum(a["per_slot_index"]) / 4 - a["per_slot"]) < 1e-6
    assert a["most_recently_written_slot"]["n"] + a["other_slots"]["n"] == 64 * 4
    assert a["most_recently_written_slot"]["correct"] + a["other_slots"]["correct"] == int(pred.eq(y).sum())
    same = analyze(torch.zeros_like(y), x, y)
    assert same["collapse"]["all_slots_same_prediction"] == 1.0


def test_onset_and_outcome_definitions():
    w = lambda ls: [{"step": 50 * (i + 1), "mean_loss": v} for i, v in enumerate(ls)]
    assert learning_onset(w([.69, .66, .4, .3])) == 100
    assert learning_onset(w([.69, .4, .6, .3])) == 150           # dip that does not persist is not onset
    assert learning_onset(w([.69, .66, .6])) is None
    assert learning_onset(w([.3, .3])) == 0
    assert learning_onset([]) is None
    assert outcome_class(None, .0) == "plateau_only"
    assert outcome_class(500, .5) == "partial"
    assert outcome_class(500, .95) == "success"


def test_onset_criterion_separates_experiment_011_runs():
    expected_none = {("protected", 17), ("protected_no_retain", 17), ("protected_no_retain", 29), ("protected_no_retain", 43),
                     ("gru32", 17), ("gru32", 29)}
    seen = 0
    for f in RAW11.glob("*_*.json"):
        if f.name == "run_manifest.json":
            continue
        r = json.loads(f.read_text(encoding="utf-8-sig"))["runs"][0]
        if r["reference_only"]:
            continue
        on = learning_onset(r["loss_windows"])
        assert (on is None) == ((r["variant"], r["seed"]) in expected_none), (r["variant"], r["seed"])
        seen += 1
    assert seen == 12


def test_bounded_run_exclusive_output_partial_and_validation(tmp_path):
    cfg = small(jobs=(("gru24", 17, 29), ("protected_no_retain", 29, 17)))
    p = tmp_path / "r.json"
    r = execute(cfg, p)
    assert r["status"] == "complete" and len(r["runs"]) == 2 and len(r["runs"][0]["loss_per_step"]) == 6
    assert r["runs"][0]["outcome"] in ("plateau_only", "partial", "success")
    with pytest.raises(FileExistsError):
        execute(cfg, p)
    r2 = execute(small(jobs=(("gru24", 17, 17),), max_wall_seconds=1e-9), tmp_path / "t.json")
    assert r2["status"] == "incomplete" and len(r2["runs"]) + len(r2["skipped"]) == 1
    row = run_one("gru24", 17, 17, small(steps=10_000), time.monotonic() + 0.5)
    assert row["status"] == "time_limit" and 0 < row["steps"] < 10_000 and row["outcome"].startswith("incomplete")
    assert parse_jobs("gru24:17:29,protected:43:17") == (("gru24", 17, 29), ("protected", 43, 17))
    assert len(Config().jobs) == 36
    for bad in (dict(jobs=(("bad", 1, 1),)), dict(jobs=(("gru24", 1, 1), ("gru24", 1, 1))), dict(steps=0)):
        with pytest.raises(ValueError):
            Config(**bad)
