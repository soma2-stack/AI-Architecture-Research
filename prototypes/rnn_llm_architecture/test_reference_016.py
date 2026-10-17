"""Exact equivalence of the protected cell to the independently written rotated matrix-gated reference (Experiment 016)."""
import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_013 as c13
from prototypes.rnn_llm_architecture import equivalence_016 as eq
from prototypes.rnn_llm_architecture import necessity_015 as ne
from prototypes.rnn_llm_architecture.reference_016 import ReferenceModel, complement_basis


@pytest.mark.parametrize("arch,seed", [("protected", 0), ("protected", 7), ("protected_fixed_005", 3), ("protected_no_retain", 5)])
@pytest.mark.parametrize("mask", ["none", "random", "zeros"])
def test_exact_equivalence_float64(arch, seed, mask):
    model = c13.build(arch, seed)
    ids = torch.randint(0, 32, (3, 9), generator=torch.Generator().manual_seed(seed))
    r = eq.compare(model, ids, mask, torch.float64, seed)
    for k in ("logits", "state", "protected_coefficients", "fast_complement"):
        assert r[k] <= 1e-10, (k, r[k])
    assert r["param_grad_rel"] <= 1e-9 and r["input_grad_rel"] <= 1e-9 and r["dead_params_same"]
    if mask == "none":
        assert r["features_path_vs_model_forward"] <= 1e-12


def test_original_float32_masks_explain_the_float64_residual():
    r = eq.compare(c13.build("protected", 1), torch.randint(0, 32, (2, 20)), "random", torch.float64, exact_masks=False)
    assert 1e-12 < r["logits"] < 1e-5 and r["replaced_mask_rounding_error"] is None


def test_float32_close():
    r = eq.compare(c13.build("protected", 1), torch.randint(0, 32, (2, 20)), "random", torch.float32)
    assert r["logits"] <= 1e-4 and r["state"] <= 1e-4


def test_complement_basis_is_orthonormal_and_complementary():
    M = c13.build("protected", 0).cells[0].masks.double()
    N = complement_basis(M)
    O = torch.cat([M, N])
    assert torch.allclose(O @ O.T, torch.eye(32, dtype=torch.float64), atol=1e-12)
    assert torch.allclose(M @ N.T, torch.zeros(8, 24, dtype=torch.float64), atol=1e-12)


def test_directive_reduction_is_not_exact_but_projected_form_is():
    """f' = Q[r f + (1-r) u] (hypothesised) differs from the implementation's Q[r f + (1-r) Q u] unless r is constant."""
    model = c13.build("protected", 2).double()
    eq.exact_masks_(model)
    cell = model.cells[0]
    g = torch.Generator().manual_seed(1)
    x, h = torch.randn(5, 32, generator=g, dtype=torch.float64), torch.randn(5, 32, generator=g, dtype=torch.float64)
    out = cell.step(cell.prepare(x), h)
    M = cell.masks
    Q = torch.eye(32, dtype=torch.float64) - M.T @ M
    u = torch.tanh(cell.x_to_candidate(x) + cell.h_to_candidate(h))
    r = torch.sigmoid(cell.fast_gate(x))
    f = h @ Q
    exact = (r * f + (1 - r) * (u @ Q)) @ Q
    hypothesised = (r * f + (1 - r) * u) @ Q
    assert (out @ Q - exact).abs().max() < 1e-12
    assert (out @ Q - hypothesised).abs().max() > 1e-3


def test_closed_write_invariant_and_noncommuting_gates():
    inv = eq.closed_write_invariant()
    assert inv["original_closed_channel_drift"] < 1e-12 and inv["reference_closed_channel_drift"] < 1e-12
    assert inv["dc_closed_dh_equals_mask_row"] < 1e-12 and inv["closed_channel_param_grad_max"] < 1e-12
    com = eq.commutators()
    assert all(v["normalized_commutator_max"] > 1e-6 for m in com.values() for v in m.values())


def test_reference_event_stepper_matches_original_without_events():
    model = c13.build("protected", 4)
    ids = torch.randint(0, 32, (5, 15))
    a = ne.run_events(model, ids)["logits"]
    b = eq.ref_run_events(ReferenceModel(model), ids, [])
    assert (a - b).abs().max() < 1e-5
