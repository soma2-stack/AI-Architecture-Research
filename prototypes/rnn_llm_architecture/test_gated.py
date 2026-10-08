"""CPU correctness checks for standard PyTorch GRU/LSTM candidates."""
import pytest
import torch
from torch import nn

from prototypes.rnn_llm_architecture.gated import (
    GatedConfig, GatedLanguageModel, LSTMState,
)


def make(kind, **kwargs):
    layers = kwargs.pop("layers", 2)
    return GatedLanguageModel(GatedConfig(vocab_size=23, width=8, layers=layers,
                                          cell_type=kind, precision="float64", **kwargs))


def tensor_leaves(state):
    return tuple(x for layer in state for x in
                 ((layer.hidden, layer.cell) if isinstance(layer, LSTMState) else (layer,)))


def assert_state_close(a, b):
    assert len(a) == len(b)
    for x, y in zip(tensor_leaves(a), tensor_leaves(b)):
        torch.testing.assert_close(x, y)


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_wrapper_recurrence_matches_standard_pytorch_sequence_module(kind):
    model = make(kind, layers=1)
    cell = model.cells[0]
    if kind == "gru":
        reference = nn.GRU(8, 8, batch_first=True, dtype=torch.float64)
        reference.weight_ih_l0.data.copy_(cell.weight_ih)
        reference.weight_hh_l0.data.copy_(cell.weight_hh)
        reference.bias_ih_l0.data.copy_(cell.bias_ih)
        reference.bias_hh_l0.data.copy_(cell.bias_hh)
    else:
        reference = nn.LSTM(8, 8, batch_first=True, dtype=torch.float64)
        reference.weight_ih_l0.data.copy_(cell.weight_ih)
        reference.weight_hh_l0.data.copy_(cell.weight_hh)
        reference.bias_ih_l0.data.copy_(cell.bias_ih)
        reference.bias_hh_l0.data.copy_(cell.bias_hh)
    features = torch.randn(3, 7, 8, dtype=torch.float64)
    state, history = model.forward_features(features)
    if kind == "gru":
        expected, h_n = reference(features)
        torch.testing.assert_close(history[:, :, 0], expected)
        torch.testing.assert_close(state[0], h_n[0])
    else:
        expected, (h_n, c_n) = reference(features)
        torch.testing.assert_close(history[:, :, 0], expected)
        torch.testing.assert_close(state[0].hidden, h_n[0])
        torch.testing.assert_close(state[0].cell, c_n[0])


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_token_shapes_streaming_empty_chunk_persistence_and_reset(kind):
    model = make(kind)
    ids = torch.tensor([[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]])
    original = model.initial_state(2)
    full, final, history = model(ids, original, return_history=True)
    prefix, state = model(ids[:, :2])
    suffix, chunk_state = model(ids[:, 2:], state)
    torch.testing.assert_close(full, torch.cat((prefix, suffix), dim=1))
    assert_state_close(final, chunk_state)
    assert_state_close(original, model.initial_state(2))
    assert history.shape == (2, 5, 2, 8)

    empty, empty_state, empty_history = model(ids[:, :0], state, return_history=True)
    assert empty.shape == (2, 0, 23)
    assert empty_history.shape == (2, 0, 2, 8)
    assert all(a is b for a, b in zip(empty_state, state))

    reset_mask = torch.zeros_like(ids, dtype=torch.bool)
    reset_mask[0, 2] = True
    reset_logits, reset_state = model(ids, reset_mask=reset_mask)
    reset_suffix, reset_suffix_state = model(ids[:1, 2:])
    torch.testing.assert_close(reset_logits[0, 2:], reset_suffix[0])
    torch.testing.assert_close(reset_logits[1], full[1])
    for a, b in zip(tensor_leaves(reset_state), tensor_leaves(final)):
        # Only row 0 resets; row 1 remains the uninterrupted stream.
        torch.testing.assert_close(a[1], b[1])
    row_zero = tuple(
        LSTMState(s.hidden[:1], s.cell[:1]) if isinstance(s, LSTMState) else s[:1]
        for s in reset_state
    )
    assert_state_close(row_zero, reset_suffix_state)


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_reproducible_local_initialization_and_detached_state(kind):
    torch.manual_seed(991)
    rng = torch.get_rng_state().clone()
    a, b = make(kind), make(kind)
    assert torch.equal(rng, torch.get_rng_state())
    assert all(torch.equal(a.state_dict()[k], v) for k, v in b.state_dict().items())
    assert not torch.equal(a.embedding.weight, make(kind, seed=20261008).embedding.weight)
    state = tuple(
        LSTMState(s.hidden.requires_grad_(), s.cell.requires_grad_()) if isinstance(s, LSTMState)
        else s.requires_grad_() for s in a.initial_state(1)
    )
    detached = a.detach_state(state)
    assert all(not x.requires_grad for x in tensor_leaves(detached))


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_finite_state_gradient_chunk_boundary_reset_cutoff_and_finite_difference(kind):
    model = make(kind, layers=1)
    ids = torch.tensor([[1, 2, 3, 4]])
    base = model.initial_state(1)
    initial = tuple(
        LSTMState(s.hidden.requires_grad_(), s.cell.requires_grad_()) if isinstance(s, LSTMState)
        else s.requires_grad_() for s in base
    )

    def scalar(state):
        return model(ids, state)[0][0, -1, 3]

    value = scalar(initial)
    grads = torch.autograd.grad(value, tensor_leaves(initial))
    assert all(torch.isfinite(g).all() for g in grads)
    _, prefix_state = model(ids[:, :2], initial)
    streamed_value = model(ids[:, 2:], prefix_state)[0][0, -1, 3]
    streamed_grads = torch.autograd.grad(streamed_value, tensor_leaves(initial))
    for a, b in zip(grads, streamed_grads):
        torch.testing.assert_close(a, b)

    direction = torch.linspace(-1, 1, 8, dtype=torch.float64)[None]
    eps = 1e-6
    if kind == "lstm":
        plus = (LSTMState(initial[0].hidden + eps * direction, initial[0].cell),)
        minus = (LSTMState(initial[0].hidden - eps * direction, initial[0].cell),)
        analytic = (grads[0] * direction).sum()
    else:
        plus = (initial[0] + eps * direction,)
        minus = (initial[0] - eps * direction,)
        analytic = (grads[0] * direction).sum()
    finite_difference = (scalar(plus) - scalar(minus)) / (2 * eps)
    torch.testing.assert_close(analytic, finite_difference, atol=2e-7, rtol=1e-5)
    if kind == "lstm":
        plus_cell = (LSTMState(initial[0].hidden, initial[0].cell + eps * direction),)
        minus_cell = (LSTMState(initial[0].hidden, initial[0].cell - eps * direction),)
        finite_cell_difference = (scalar(plus_cell) - scalar(minus_cell)) / (2 * eps)
        torch.testing.assert_close((grads[1] * direction).sum(), finite_cell_difference,
                                   atol=2e-7, rtol=1e-5)

    _, state = model(ids[:, :2], initial)
    reset = torch.ones((1, 2), dtype=torch.bool)
    suffix, _ = model(ids[:, 2:], state, reset_mask=reset)
    cutoff = torch.autograd.grad(suffix.sum(), tensor_leaves(state))
    assert all(torch.count_nonzero(g) == 0 for g in cutoff)


@pytest.mark.parametrize("kind", ("gru", "lstm"))
@pytest.mark.parametrize("precision", ("float32", "float64"))
def test_long_sequence_outputs_state_and_gradients_remain_finite(kind, precision):
    model = GatedLanguageModel(GatedConfig(vocab_size=23, width=8, layers=1,
                                           cell_type=kind, precision=precision))
    ids = torch.arange(1024)[None] % 23
    logits, state = model(ids)
    gradients = torch.autograd.grad(logits[0, -1, 3], model.embedding.weight)
    assert torch.isfinite(logits).all()
    assert all(torch.isfinite(x).all() for x in tensor_leaves(state))
    assert all(torch.isfinite(g).all() for g in gradients)


@pytest.mark.parametrize("kwargs", (
    {"vocab_size": 0}, {"width": 0}, {"layers": 0}, {"cell_type": "tanh"},
    {"precision": "float16"}, {"seed": True},
))
def test_invalid_gated_configuration(kwargs):
    with pytest.raises(ValueError):
        GatedConfig(**kwargs)


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_invalid_lstm_or_gru_state_and_reset_masks_are_rejected(kind):
    model = make(kind)
    ids = torch.ones(1, 2, dtype=torch.long)
    wrong_state = (torch.zeros(1, 8, dtype=torch.float64),) * 2 if kind == "lstm" else (
        LSTMState(torch.zeros(1, 8, dtype=torch.float64), torch.zeros(1, 8, dtype=torch.float64)),) * 2
    with pytest.raises(ValueError):
        model(ids, wrong_state)
    with pytest.raises(ValueError):
        model(ids, reset_mask=ids)


def test_lstm_cell_memory_is_a_separate_persistent_state_component():
    model = make("lstm", layers=1)
    ids = torch.tensor([[1, 2, 3]])
    initial = model.initial_state(1)
    changed_cell = (LSTMState(initial[0].hidden, torch.ones_like(initial[0].cell)),)
    original_logits, _ = model(ids, initial)
    changed_logits, _ = model(ids, changed_cell)
    assert not torch.allclose(original_logits, changed_logits)


@pytest.mark.parametrize("kind", ("gru", "lstm"))
def test_gradient_diagnostic_does_not_update_model_parameters(kind):
    model = make(kind)
    before = {name: value.detach().clone() for name, value in model.state_dict().items()}
    logits, _ = model(torch.tensor([[1, 2, 3]]))
    gradients = torch.autograd.grad(logits.square().mean(), tuple(model.parameters()))
    assert all(torch.isfinite(gradient).all() for gradient in gradients)
    assert all(torch.equal(before[name], value) for name, value in model.state_dict().items())
