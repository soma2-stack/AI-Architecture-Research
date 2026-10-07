"""Structural checks of a proof-scope sensitivity recurrence; NO training."""
import pytest
import torch

from prototypes.rnn_llm_architecture.theory_reference import (
    CreditTrace, FrozenCorridorCreditReference,
)


def test_rank_two_operator_identity_and_indexing():
    ref = FrozenCorridorCreditReference(64)
    r = ref.r
    assert (ref.k, ref.d, r) == (32, 16, 31)
    ones = torch.ones(r, dtype=torch.float64)
    e1 = torch.zeros_like(ones)
    e1[0] = 1
    expected = ref.local_transport + torch.outer(ones, ref.u) + torch.outer(e1, ref.v_h)
    assert torch.allclose(ref.operator, expected, atol=1e-15)
    assert torch.equal(ref.local_transport[0], torch.zeros(r, dtype=torch.float64))
    assert ref.local_transport[ref.d - 2, ref.d - 3] == 1
    assert ref.local_transport[ref.d - 1, ref.d - 1] == 1


def test_response_and_feedback_for_one_step():
    ref = FrozenCorridorCreditReference(32)
    gates = torch.linspace(.5, 1.0, ref.r, dtype=torch.float64)[None, :]
    trace, history = ref.scan(gates, return_history=True)
    assert isinstance(trace, CreditTrace)
    assert history.shape == (2, ref.r, ref.r)
    assert torch.equal(history[0], torch.zeros_like(history[0]))
    assert torch.allclose(trace.response, torch.diag(gates[0]), atol=0)
    assert torch.allclose(trace.J, ref.u @ trace.response, atol=1e-15)
    assert torch.allclose(trace.B, ref.v_h @ trace.response, atol=1e-15)


def test_selected_probes_agree_with_full_matrix():
    torch.manual_seed(123)
    ref = FrozenCorridorCreditReference(32)
    gates = .995 + .004 * torch.rand(5, ref.r, dtype=torch.float64)
    probes = torch.randn(ref.r, 3, dtype=torch.float64)
    full = ref.scan(gates)
    selected = ref.scan(gates, probes)
    assert torch.allclose(selected.response, full.response @ probes, atol=1e-12)
    assert torch.allclose(selected.J, full.J @ probes, atol=1e-12)
    assert torch.allclose(selected.B, full.B @ probes, atol=1e-12)


def test_zero_gates_erase_all_response():
    ref = FrozenCorridorCreditReference(32)
    gates = torch.ones((3, ref.r), dtype=torch.float64)
    gates[-1].zero_()
    trace = ref.scan(gates)
    assert torch.count_nonzero(trace.response) == 0


def test_gates_have_differentiable_reference_sensitivity():
    ref = FrozenCorridorCreditReference(32)
    gates = torch.full((3, ref.r), .99, dtype=torch.float64, requires_grad=True)
    trace = ref.scan(gates)
    (grad,) = torch.autograd.grad(trace.response.square().sum(), gates)
    assert torch.isfinite(grad).all()
    assert grad.abs().sum() > 0


@pytest.mark.parametrize("invalid", [-1, 0, 15, 16.5, True])
def test_invalid_n_rejected(invalid):
    with pytest.raises(ValueError, match="integer >=16"):
        FrozenCorridorCreditReference(invalid)


def test_invalid_schedule_and_probe_rejected():
    ref = FrozenCorridorCreditReference(32)
    gates = torch.ones((2, ref.r), dtype=torch.float64)
    with pytest.raises(ValueError, match="at least one"):
        ref.scan(gates[:0])
    with pytest.raises(ValueError, match="gates must be"):
        ref.scan(torch.ones((2, ref.r + 1), dtype=torch.float64))
    with pytest.raises(ValueError, match="lie in"):
        ref.scan(gates * 2)
    with pytest.raises(ValueError, match="device/dtype"):
        ref.scan(gates.float())
    with pytest.raises(ValueError, match="probes must be"):
        ref.scan(gates, torch.zeros(ref.r + 1, 3, dtype=torch.float64))


def test_no_trainable_parameters_or_training_loop():
    ref = FrozenCorridorCreditReference(32)
    assert list(ref.parameters()) == []
    assert all(not buffer.requires_grad for buffer in ref.buffers())
