"""CPU structural, streaming and gradient tests for Experiment 009 event-gated variants."""
import pytest
import torch

from prototypes.rnn_llm_architecture.candidates import CandidateConfig, CandidateLanguageModel
from prototypes.rnn_llm_architecture.event_gated import (
    EventGatedConfig, EventGatedLanguageModel, EventGatedProtectedCell, KeepGatedGRULanguageModel,
    ShiftState, StraightThroughGRUCell, straight_through_step)
from prototypes.rnn_llm_architecture.gated import GatedConfig, GatedLanguageModel

CONFIGS = [("soft", False), ("soft", True), ("hard", False), ("hard", True)]


def config(mode="hard", shift=False, seed=17, precision="float64"):
    return EventGatedConfig(vocab_size=16, width=32, layers=2, protected_channels=8, cell_type="protected",
                            seed=seed, precision=precision, gate_mode=mode, token_shift=shift)


def original(seed=17, precision="float64"):
    return CandidateLanguageModel(CandidateConfig(vocab_size=16, width=32, layers=2, protected_channels=8,
                                                  cell_type="protected", seed=seed, precision=precision))


def test_straight_through_forward_is_exact_step_and_backward_is_sigmoid_slope():
    z = torch.tensor([-3., -1e-9, 0., 1e-9, 2.], dtype=torch.float64, requires_grad=True)
    g = straight_through_step(z)
    assert g.tolist() == [0., 0., 0., 1., 1.]
    g.sum().backward()
    s = torch.sigmoid(z.detach())
    torch.testing.assert_close(z.grad, s * (1 - s))


@pytest.mark.parametrize("shift", [False, True])
def test_soft_variants_match_original_protected_model_at_initialization(shift):
    base, new = original(), EventGatedLanguageModel(config("soft", shift))
    ids = torch.randint(0, 16, (3, 12))
    a, ha = base(ids)
    b, hb = new(ids)
    torch.testing.assert_close(a, b, atol=0, rtol=0)
    for x, y in zip(ha, hb):
        torch.testing.assert_close(x, y.hidden if shift else y, atol=0, rtol=0)
    assert new.trainable_parameters == base.trainable_parameters + (2 * 32 * 8 if shift else 0)


def test_all_variants_copy_original_seeded_weights():
    base = original(seed=29)
    for mode, shift in CONFIGS:
        new = EventGatedLanguageModel(config(mode, shift, seed=29))
        for name, p in base.state_dict().items():
            torch.testing.assert_close(new.state_dict()[name], p, atol=0, rtol=0)


@pytest.mark.parametrize("mode,shift", CONFIGS)
def test_chunked_streaming_equals_full_sequence(mode, shift):
    model = EventGatedLanguageModel(config(mode, shift))
    ids = torch.randint(0, 16, (2, 11))
    full, state = model(ids)
    left, mid = model(ids[:, :4])
    right, end = model(ids[:, 4:], mid)
    torch.testing.assert_close(full, torch.cat((left, right), 1), atol=1e-12, rtol=1e-12)
    for x, y in zip(state, end):
        for u, v in zip(x if shift else (x,), y if shift else (y,)):
            torch.testing.assert_close(u, v, atol=1e-12, rtol=1e-12)
    if shift:
        assert all(isinstance(s, ShiftState) for s in state)


@pytest.mark.parametrize("shift", [False, True])
def test_reset_mask_restarts_hidden_and_previous_input(shift):
    model = EventGatedLanguageModel(config("hard", shift))
    ids = torch.randint(0, 16, (2, 9))
    reset = torch.zeros(2, 9, dtype=torch.bool)
    reset[:, 5] = True
    with_reset, _ = model(ids, reset_mask=reset)
    fresh, _ = model(ids[:, 5:])
    torch.testing.assert_close(with_reset[:, 5:], fresh, atol=1e-12, rtol=1e-12)


def test_hard_gate_values_are_binary_and_closed_coefficients_are_invariant():
    cfg = config("hard", True)
    cell = EventGatedProtectedCell(cfg)
    with torch.no_grad():
        cell.slow_gate.bias.fill_(-50.)  # every channel closed for any bounded input
    coeff = torch.randn(3, 8, dtype=torch.float64)
    h = cell.synthesize(coeff)
    prev = torch.zeros(3, 32, dtype=torch.float64)
    for _ in range(300):
        x = torch.randn(3, 32, dtype=torch.float64)
        gate = cell.prepare(x, prev)[1]
        assert set(gate.unique().tolist()) <= {0.0, 1.0}
        h = cell(x, h, previous=prev)
        prev = x
    # The gate multiplies the write by exactly zero; only projection read-back roundoff remains.
    torch.testing.assert_close(cell.read_protected(h), coeff, atol=1e-12, rtol=1e-12)


@pytest.mark.parametrize("mode,shift", CONFIGS)
def test_gradients_are_finite_and_reach_gate_parameters(mode, shift):
    model = EventGatedLanguageModel(config(mode, shift))
    ids = torch.randint(0, 16, (4, 10))
    loss = model(ids)[0][:, -1, 2:4].logsumexp(-1).sum()
    loss.backward()
    for cell in model.cells:
        assert torch.isfinite(cell.slow_gate.weight.grad).all()
        assert float(cell.slow_gate.weight.grad.abs().sum()) > 0
        if shift:
            assert float(cell.previous_to_gate.weight.grad.abs().sum()) > 0
    assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)


def test_soft_shift_cell_matches_numerical_gradient():
    cfg = config("soft", True)
    cell = EventGatedProtectedCell(cfg)
    with torch.no_grad():
        cell.previous_to_gate.weight.normal_(0, .1)
    x = torch.randn(2, 32, dtype=torch.float64, requires_grad=True)
    prev = torch.randn(2, 32, dtype=torch.float64, requires_grad=True)
    h = torch.randn(2, 32, dtype=torch.float64, requires_grad=True)
    assert torch.autograd.gradcheck(lambda a, b, c: cell(a, c, previous=b), (x, prev, h))


def test_keep_gated_gru_soft_zero_bias_equals_stock_gru():
    cfg = GatedConfig(vocab_size=16, width=32, layers=2, cell_type="gru", seed=17, precision="float64")
    stock = GatedLanguageModel(cfg)
    same = KeepGatedGRULanguageModel(cfg, gate_mode="soft", keep_bias=0.0)
    ids = torch.randint(0, 16, (3, 10))
    torch.testing.assert_close(stock(ids)[0], same(ids)[0], atol=1e-10, rtol=1e-10)
    assert same.trainable_parameters == stock.trainable_parameters


def test_hard_keep_gate_copies_hidden_state_exactly():
    cell = StraightThroughGRUCell(32, 32, gate_mode="hard", keep_bias=50.0, dtype=torch.float64)
    cell.shift_keep_bias()
    h = torch.randn(2, 32, dtype=torch.float64)
    out = h
    for _ in range(100):
        out = cell(torch.randn(2, 32, dtype=torch.float64), out)
    assert torch.equal(out, h)


def test_invalid_configurations_rejected():
    with pytest.raises(ValueError):
        EventGatedConfig(width=32, cell_type="tanh")
    with pytest.raises(ValueError):
        config(mode="sparse")
    with pytest.raises(TypeError):
        EventGatedLanguageModel(CandidateConfig(width=32, cell_type="protected"))
    with pytest.raises(ValueError):
        KeepGatedGRULanguageModel(GatedConfig(cell_type="lstm"))
    model = EventGatedLanguageModel(config("hard", True))
    with pytest.raises(ValueError):
        model(torch.randint(0, 16, (2, 3)), state=original().initial_state(2))
