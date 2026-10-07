"""CPU-only architecture checks. No learning, dataset, or optimizer is run."""
import pytest
import torch

from prototypes.rnn_llm_architecture.model import (
    NearCriticalTanhCell, ProtectedCell, RNNConfig, RNNLanguageModel,
    sum_free_walsh_bank,
)


@pytest.mark.parametrize("cell_type", ["tanh", "near_critical", "protected"])
def test_shapes_and_finite_logits(cell_type):
    torch.manual_seed(11)
    config = RNNConfig(vocab_size=37, width=16, layers=2,
                       cell_type=cell_type, protected_channels=4)
    model = RNNLanguageModel(config)
    logits, last_state, history = model(
        torch.randint(0, 37, (2, 5)), return_history=True
    )
    assert logits.shape == (2, 5, 37)
    assert len(last_state) == 2
    assert history.shape == (2, 5, 2, 16)
    assert torch.isfinite(logits).all()
    assert torch.allclose(history[:, -1, 1, :], last_state[1])


@pytest.mark.parametrize("cell_type", ["tanh", "near_critical", "protected"])
def test_streaming_matches_single_pass(cell_type):
    torch.manual_seed(12)
    config = RNNConfig(vocab_size=31, width=16, layers=2,
                       cell_type=cell_type, protected_channels=4)
    model = RNNLanguageModel(config)
    tokens = torch.randint(0, 31, (2, 7))
    full, full_state = model(tokens)
    left, h = model(tokens[:, :3])
    right, chunk_state = model(tokens[:, 3:], h)
    assert torch.allclose(full, torch.cat((left, right), dim=1), atol=1e-6)
    for a, b in zip(full_state, chunk_state):
        assert torch.allclose(a, b, atol=1e-6)


@pytest.mark.parametrize("cell_type", ["tanh", "near_critical", "protected"])
def test_gradient_flows_through_time(cell_type):
    torch.manual_seed(13)
    model = RNNLanguageModel(RNNConfig(
        vocab_size=41, width=16, layers=1, cell_type=cell_type, protected_channels=4
    ))
    ids = torch.randint(0, 41, (2, 6))
    logits, state = model(ids)
    # Analytic backwards test only; no optimizer or training step.
    grad = torch.autograd.grad(logits[:, -1, 7].sum(), model.embedding.weight)[0]
    assert torch.isfinite(grad).all()
    assert grad.abs().sum() > 0
    assert torch.isfinite(state[0]).all()


def test_near_critical_recurrent_operator():
    torch.manual_seed(14)
    width = 16
    cell = NearCriticalTanhCell(width)
    assert not cell.recurrent.requires_grad
    singular_values = torch.linalg.svdvals(cell.recurrent)
    target = 1 - 1 / width
    assert torch.allclose(singular_values, torch.full_like(singular_values, target),
                          atol=1e-5)


def test_sum_free_orthonormal_masks():
    masks = sum_free_walsh_bank(32, 8)
    assert torch.allclose(masks @ masks.T, torch.eye(8), atol=1e-6)
    cell = ProtectedCell(32, 8)
    coefficients = torch.randn(3, 8)
    state = torch.nn.functional.linear(coefficients, cell.masks.T)
    assert torch.allclose(cell.read_protected(state), coefficients, atol=1e-6)


def test_protected_state_budget_is_constant():
    a = RNNLanguageModel(RNNConfig(
        vocab_size=29, width=32, layers=2, cell_type="protected", protected_channels=4
    ))
    b = RNNLanguageModel(RNNConfig(
        vocab_size=29, width=32, layers=2, cell_type="protected", protected_channels=8
    ))
    assert len(a.initial_state(3)) == len(b.initial_state(3)) == 2
    assert all(s.numel() == 3 * 32 for s in b.initial_state(3))
    # More channels DO add gate parameters; comparison must account for this.
    assert b.trainable_parameters > a.trainable_parameters


def test_invalid_protected_width_rejected():
    with pytest.raises(ValueError):
        RNNConfig(cell_type="protected", width=30, protected_channels=4)


def test_reset_not_implicit():
    model = RNNLanguageModel(RNNConfig(
        vocab_size=37, width=16, layers=1, cell_type="protected", protected_channels=4
    ))
    x = torch.tensor([[2, 3, 4]], dtype=torch.long)
    _, last_state = model(x)
    reset = model.initial_state(1)
    assert torch.equal(reset[0], torch.zeros_like(reset[0]))
    assert not torch.allclose(last_state[0], reset[0])
