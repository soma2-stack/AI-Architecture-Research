"""Fixed slow-write-gate controls: only the gate output changes; everything else is the original protected model."""
import math

import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_010 as c10
from prototypes.rnn_llm_architecture import capacity_012 as c12
from prototypes.rnn_llm_architecture import capacity_013 as c13


def small13(**kw):
    base = dict(steps=6, batch=4, delay=8, eval_delays=(8, 16), eval_histories=32, checkpoint_every=3,
                checkpoint_histories=32, loss_window=2, max_wall_seconds=60)
    base.update(kw)
    return c13.Config(**base)


def small12():
    return c12.Config(steps=6, batch=4, delay=8, eval_delays=(8, 16), eval_histories=32, checkpoint_every=3,
                      checkpoint_histories=32, loss_window=2, max_wall_seconds=60)


@pytest.mark.parametrize("name", ["protected", "protected_no_retain"])
def test_training_loop_reproduces_experiment_012_bit_for_bit(name):
    a = c13.run_one(name, 29, 43, small13(), float("inf"))
    b = c12.run_one(name, 29, 43, small12(), float("inf"))
    assert a["loss_per_step"] == b["loss_per_step"] and a["loss_windows"] == b["loss_windows"]
    assert a["init_fingerprint_sha256"] == b["init_fingerprint_sha256"]
    assert a["training_stream_sha256"] == b["training_stream_sha256"]
    assert a["eval"]["16"]["per_slot"] == b["eval"]["16"]["per_slot"]


def test_fixed_gate_of_one_is_exactly_forced_overwrite():
    a = c13.run_one("protected_fixed_1", 17, 29, small13(), float("inf"))
    b = c13.run_one("protected_no_retain", 17, 29, small13(), float("inf"))
    assert a["loss_per_step"] == b["loss_per_step"]
    assert a["eval"]["16"]["pred_pattern_counts"] == b["eval"]["16"]["pred_pattern_counts"]


def test_fixed_controls_share_initial_weights_and_only_kill_the_gate():
    ref = c10.build("protected", 4, 2, 43)
    for name, g in (("protected_fixed_0474", c13.SIGMOID_MINUS_3), ("protected_fixed_005", .005)):
        m = c13.build(name, 43)
        assert c12.init_fingerprint(m) == c12.init_fingerprint(ref)
        assert c13.live_parameter_count(m) == 8016 - 528 == c13.live_parameter_count(c10.build("protected_no_retain", 4, 2, 43))
        x = m.embedding(c10.generator_batch(4, 2, 8, 3, seed=2))
        drive, write, fast = m.cells[0].prepare(x)
        d0, w0, f0 = ref.cells[0].prepare(x)
        assert torch.equal(drive, d0) and torch.equal(fast, f0)
        assert torch.all(write == g) and write.shape == w0.shape
    assert c13.live_parameter_count(ref) == 8016
    assert abs(c13.SIGMOID_MINUS_3 - 1 / (1 + math.exp(3))) < 1e-15 and round(c13.SIGMOID_MINUS_3, 4) == 0.0474


def test_coefficient_update_equation_is_unchanged():
    m = c13.build("protected_fixed_005", 17)
    cell = m.cells[0]
    torch.manual_seed(0)
    x, h = torch.randn(5, 32), torch.randn(5, 32)
    prep = cell.prepare(x)
    out = cell.step(prep, h)
    old = cell.read_protected(h)
    proposal = torch.tanh(prep[0] + cell.h_to_candidate(h))
    proposed = cell.read_protected(proposal)
    coeff = old + .005 * (proposed - old)
    assert torch.allclose(cell.read_protected(out), coeff, atol=1e-6)


def test_weight_snapshots_and_validation(tmp_path):
    cfg = small13(save_weights_at=(0, 6), jobs=(("protected", 17, 17),))
    r = c13.execute(cfg, tmp_path / "r.json", tmp_path / "w")
    row = r["runs"][0]
    assert [s["step"] for s in row["saved_weights"]] == [0, 6]
    m = c13.build("protected", 17)
    m.load_state_dict(torch.load(tmp_path / "w" / row["saved_weights"][1]["file"]))
    e = c12.evaluate(m, 16, seed=c12.eval_seed(16), histories=32)
    assert e["per_slot"] == row["eval"]["16"]["per_slot"]
    assert len(c13.Config().jobs) == 18
    for bad in (dict(jobs=(("gru24", 1, 1),)), dict(save_weights_at=(99,))):
        with pytest.raises(ValueError):
            small13(**bad)
    with pytest.raises(ValueError):
        c13.fix_slow_gate(c10.build("protected_no_retain", 4, 2, 1), .1)
