"""CPU tests for the Experiment 009 task, labels, baselines, oracle isolation and runner."""
import json
import math
import time

import pytest
import torch

from prototypes.rnn_llm_architecture import experiment_009 as e
from prototypes.rnn_llm_architecture.experiment_002 import _slot_targets
from prototypes.rnn_llm_architecture.learning_pilot import (BIT0, BIT1, DISTRACTOR_END, DISTRACTOR_START,
                                                            QUERY_A, QUERY_B, WRITE_A, WRITE_B)


@pytest.mark.parametrize("delay,seed", [(7, 1), (16, 2), (64, 3), (257, 4)])
def test_generator_structure_and_replay_agree(delay, seed):
    prefix, rec = e.make_two_slot_batch(delay, 128, seed=seed)
    assert prefix.shape == (128, 4 + delay) and prefix.dtype == torch.long
    assert torch.equal(prefix[:, [0, 2]].sort(1).values, torch.tensor([[WRITE_A, WRITE_B]] * 128))
    allowed = {BIT0, BIT1, WRITE_A, WRITE_B, *range(DISTRACTOR_START, DISTRACTOR_END)}
    assert set(prefix.unique().tolist()) <= allowed
    # every WRITE is immediately followed by a value bit
    w = (prefix == WRITE_A) | (prefix == WRITE_B)
    assert not bool(w[:, -1].any())
    nxt = prefix[:, 1:][w[:, :-1]]
    assert bool(((nxt == BIT0) | (nxt == BIT1)).all())
    wa, wb = e.marked_writes(prefix)
    assert torch.equal((wa | wb).sum(1), 2 + rec["updates"])
    assert bool(((rec["updates"] >= 1) & (rec["updates"] <= 3)).all())
    r = e.replay_slots(prefix)
    assert torch.equal(r["final"], rec["final"])
    assert torch.equal(r["last_write_slot"], rec["last_update_slot"])
    assert torch.equal(r["last_write_value"], rec["last_update_value"])


def test_generator_is_seed_deterministic_and_contains_conflicting_unmarked_bits():
    a, _ = e.make_two_slot_batch(64, 64, seed=11)
    b, _ = e.make_two_slot_batch(64, 64, seed=11)
    c, _ = e.make_two_slot_batch(64, 64, seed=12)
    assert torch.equal(a, b) and not torch.equal(a, c)
    wa, wb = e.marked_writes(a)
    unmarked = ((a == BIT0) | (a == BIT1)) & ~(wa | wb)
    assert 0.15 < float(unmarked[:, 4:].float().mean()) < 0.35
    final = e.replay_slots(a)["final"]
    assert 0.3 < float((final[:, 0] != final[:, 1]).float().mean()) < 0.7


def test_replay_semantics_on_handwritten_sequence():
    d = 8
    seq = [WRITE_B, BIT1, WRITE_A, BIT0,   # A=0, B=1
           BIT1,                            # unmarked: ignored
           WRITE_A, 9, BIT1,                # WRITE not adjacent to bit: ignored
           WRITE_B, BIT0,                   # B=0
           10, BIT1]                        # unmarked
    prefix = torch.tensor([seq])
    r = e.replay_slots(prefix)
    assert r["final"].tolist() == [[0, 0]]
    assert r["last_write_slot"].tolist() == [1] and r["last_write_value"].tolist() == [0]
    assert r["last_bit_value"].tolist() == [1]
    s = e.shortcut_predictions(prefix, seed=0)
    assert s["sticky_address"].tolist() == [[1, 1]]  # shortcut treats unmarked bits as writes
    assert s["initial_values_only"].tolist() == [[0, 1]]
    with pytest.raises(ValueError):
        e.replay_slots(torch.tensor([[WRITE_A, BIT0, 9, 9]]))


def test_shortcut_baselines_have_expected_unequal_pair_scores():
    prefix, _ = e.make_two_slot_batch(64, 4096, seed=5)
    target = e.replay_slots(prefix)["final"]
    preds = e.shortcut_predictions(prefix, seed=1)
    score = {k: e.pair_scores(v, target)["paired_on_unequal"] for k, v in preds.items()}
    assert score["last_marked_write"] == 0.0 and score["last_bit_token"] == 0.0
    assert abs(score["random"] - 0.25) < 0.03
    assert score["initial_values_only"] < 0.5 and score["sticky_address"] < 0.6


def test_queries_share_identical_prefixes():
    prefix, _ = e.make_two_slot_batch(16, 5, seed=3)
    ids = e.with_queries(prefix)
    assert ids.shape == (10, 21)
    assert torch.equal(ids[:5, :-1], ids[5:, :-1]) and torch.equal(ids[:5, :-1], prefix)
    assert ids[:5, -1].eq(QUERY_A).all() and ids[5:, -1].eq(QUERY_B).all()


def test_oracle_masks_only_open_true_write_events():
    prefix, _ = e.make_two_slot_batch(32, 64, seed=8)
    wa, wb = e.marked_writes(prefix)
    tag = e.oracle_write_masks(prefix, "tag", 2, 8)
    route = e.oracle_write_masks(prefix, "route", 2, 8)
    assert tag.shape == route.shape == (64, 36, 2, 8)
    assert torch.equal(tag.amax((2, 3)).bool(), wa | wb)
    assert torch.equal(route[..., :4].amax((2, 3)).bool(), wa)
    assert torch.equal(route[..., 4:].amax((2, 3)).bool(), wb)
    with pytest.raises(ValueError):
        e.oracle_write_masks(prefix, "label", 2, 8)


def test_only_named_oracle_arms_receive_oracle_information():
    for name in e.VARIANTS:
        model, oracle = e.build_variant(name, 17)
        assert (oracle is not None) == name.startswith("oracle_")
        assert all(torch.isfinite(p).all() for p in model.parameters())


def test_parameter_and_state_accounting():
    expected = {"protected_w32": (7504, 64), "protected_hard_shift_w32": (8016, 128),
                "gru_w32": (13376, 64), "lstm_w32": (17600, 128), "gru_w24": (7728, 48),
                "lstm_w20": (7160, 80), "oracle_tag_protected_w32": (7504, 64)}
    for name, (params, floats) in expected.items():
        model, oracle = e.build_variant(name, 3)
        assert sum(p.numel() for p in model.parameters()) == params
        assert e.recurrent_state_floats(model, oracle) == floats


def test_event_variants_start_from_protected_weights():
    base, _ = e.build_variant("protected_w32", 29)
    for name in ("protected_shift_w32", "protected_hard_w32", "protected_hard_shift_w32"):
        model, _ = e.build_variant(name, 29)
        for k, v in base.state_dict().items():
            assert torch.equal(model.state_dict()[k], v)


def test_training_batches_are_shared_and_labelled_by_replay():
    cfg = e.Config(steps=1)
    ids, y = e.training_batch("two_slot", 17, 4, cfg)
    ids2, y2 = e.training_batch("two_slot", 17, 4, cfg)
    assert torch.equal(ids, ids2) and torch.equal(y, y2)
    n = ids.shape[0] // 2
    final = e.replay_slots(ids[:n, :-1])["final"]
    assert torch.equal(y, torch.cat((final[:, 0], final[:, 1])))
    lids, ly = e.training_batch("legacy", 17, 4, cfg)
    t = _slot_targets(lids[:n, :-1], cfg.train_delay)
    assert torch.equal(ly, torch.cat((t[:, 0], t[:, 1])))
    with pytest.raises(ValueError):
        e.training_batch("other", 17, 0, cfg)


@pytest.mark.parametrize("name", ["protected_hard_shift_w32", "gru_hard_w32", "lstm_w20", "oracle_tag_protected_w32"])
def test_short_training_run_records_complete_finite_evidence(name):
    cfg = e.Config(variants=(name,), steps=4, checkpoint_every=2, checkpoint_histories=16, eval_delays=(7, 16),
                   legacy_delays=(8,), eval_histories=32, probe_train=64, probe_test=32)
    row = e.train_and_evaluate(name, 17, cfg, time.time() + 120)
    assert row["complete"] and row["steps_completed"] == 4 and len(row["checkpoints"]) == 2
    assert all(math.isfinite(v) for v in row["loss_by_50"])
    assert set(row["two_slot"]) == {"7", "16"} and set(row["legacy"]) == {"8"}
    assert row["two_slot"]["16"]["baselines"]["last_marked_write"] == 0.0
    assert row["probe"]["transfer_delay"] == 4 * cfg.train_delay
    json.dumps(row)


def test_wall_budget_marks_run_incomplete():
    cfg = e.Config(variants=("tanh_w32",), steps=5, eval_delays=(7,), legacy_delays=(8,), eval_histories=8,
                   probe_train=16, probe_test=8)
    row = e.train_and_evaluate("tanh_w32", 17, cfg, time.time() - 1)
    assert row["status"] == "wall_budget" and not row["complete"] and row["steps_completed"] == 0


def test_config_validation_and_no_overwrite(tmp_path):
    with pytest.raises(ValueError):
        e.Config(variants=("protected_w32", "protected_w32"))
    with pytest.raises(ValueError):
        e.Config(legacy_variants=("not_a_model",))
    with pytest.raises(ValueError):
        e.Config(eval_delays=(3,))
    out = tmp_path / "r.json"
    out.write_text("{}")
    with pytest.raises(FileExistsError):
        e.execute(e.Config(), output=out)
    with pytest.raises(ValueError):
        e.make_two_slot_batch(4, 2, seed=0)


def test_distractor_tail_has_no_marked_writes_but_has_conflicting_bits():
    tail = e.distractor_tail(200, 16, seed=4)
    wa, wb = e.marked_writes(tail)
    assert not bool((wa | wb).any())
    assert not bool(((tail == WRITE_A) | (tail == WRITE_B)).any())
    assert bool(((tail == BIT0) | (tail == BIT1)).any())


@pytest.mark.parametrize("name", ["protected_w32", "protected_hard_shift_w32", "lstm_w20", "oracle_tag_protected_w32"])
def test_perturbation_diagnostic_clean_branch_matches_full_sequence_evaluation(name):
    model, oracle = e.build_variant(name, 5)
    p = e.perturbation_recovery(model, oracle, 16, seed=9, histories=64, tail=8, noise=(0.5,))
    full = e.evaluate_two_slot(model, oracle, 16, seed=9, histories=64)
    assert p["clean_immediate"] == full["paired_on_unequal"]
    assert set(p["noise_0.5"]) == {"immediate", "after_tail"}
