"""Stepper equivalence, pair validity, transplant algebra, sham/positive controls and metric bookkeeping for Experiment 014."""
import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_010 as c10
from prototypes.rnn_llm_architecture import capacity_013 as c13
from prototypes.rnn_llm_architecture import intervene_014 as iv

BUILDERS = {"protected": lambda: c13.build("protected", 17), "fixed": lambda: c13.build("protected_fixed_005", 29),
            "gru32": lambda: c10.build("gru32", 4, 2, 43)}


@pytest.fixture(scope="module", params=sorted(BUILDERS))
def model(request):
    m = BUILDERS[request.param]()
    m.eval()
    return m


def small_pairs(delay=24, n=16):
    return iv.build_pairs(delay, n)


def test_pairs_differ_in_exactly_one_stored_value_and_labels_match_replay():
    for delay in (24, 64):
        P = iv.build_pairs(delay, 64)
        v = iv.validate_pairs(P)
        assert v["histories_differ_in_exactly_one_token"] and v["exactly_one_label_differs"]
        assert v["differing_label_is_changed_slot"] and v["identical_write_locations"]
        assert torch.equal(c10.replay(P.tok_a, 4, 2), P.y_a) and torch.equal(c10.replay(P.tok_b, 4, 2), P.y_b)
        assert set(P.slot.tolist()) == {0, 1, 2, 3}
        for mode in ("early", "late"):
            c = P.cuts(mode)
            assert (c > P.pos).all() and (c <= P.T).all()
        assert (P.cuts("late") >= P.cuts("early")).all()
    seeds = {iv.PAIR_SEED_BASE + d for d in iv.DELAYS}
    train = {c13.c12.training_seed(s, t) for s in (17, 29, 43) for t in range(3000)}
    assert not seeds & train and all(s != c13.c12.EVAL_BASE + d for s in seeds for d in (64, 128, 256, 512))


def test_stepper_matches_forward_and_chunked_inference(model):
    P = small_pairs()
    v = iv.verify_stepper(model, P.tok_a, k=10)
    assert v["max_abs_logit_diff_stepper_vs_forward"] < 1e-4
    assert v["max_abs_logit_diff_chunked_vs_uninterrupted"] < 1e-4
    assert v["max_abs_state_diff_stepper_vs_forward_state"] < 1e-4


def test_sham_preserves_output_and_full_transplant_equals_donor_run(model):
    P = small_pairs()
    n = P.tok_a.shape[0]
    cut = P.cuts("late")
    ra, rb = iv.staged_run(model, P.tok_a, record=True), iv.staged_run(model, P.tok_b, record=True)
    idx = torch.arange(n)
    ha, hb = ra["nat"][idx, cut - 1], rb["nat"][idx, cut - 1]
    sham = iv.staged_run(model, P.tok_a, cut, iv.transform("sham", (0, 1), ha, ha, None))
    assert (sham["logits"] - ra["logits"]).abs().max() < 1e-5
    full = iv.staged_run(model, P.tok_a, cut, iv.transform("full", (0, 1), ha, hb, None))
    assert (full["logits"] - rb["logits"]).abs().max() < 1e-4        # recipient with donor's complete state behaves as the donor
    assert (full["final"] - rb["final"]).abs().max() < 1e-4


def test_transform_algebra():
    rand = iv.random_projectors()
    for Pm in rand + [iv.walsh_projector()]:
        assert torch.allclose(Pm, Pm.T, atol=1e-6) and torch.allclose(Pm @ Pm, Pm, atol=1e-5) and abs(float(Pm.trace()) - 8) < 1e-4
    g = torch.Generator().manual_seed(0)
    hr, hd = torch.randn(10, 2, 32, generator=g), torch.randn(10, 2, 32, generator=g)
    P = rand[0]
    sub = iv.transform("sub", (0,), hr, hd, P)
    assert torch.allclose(sub[0] @ P, hd[:, 0] @ P, atol=1e-5)                   # donor's component inside S
    assert torch.allclose(sub[0] - sub[0] @ P, hr[:, 0] - hr[:, 0] @ P, atol=1e-5)  # recipient's outside S
    assert torch.equal(sub[1], hr[:, 1])                                          # untouched layer
    comp = iv.transform("comp", (1,), hr, hd, P)
    assert torch.allclose(comp[1] @ P, hr[:, 1] @ P, atol=1e-5) and torch.allclose(comp[1] - comp[1] @ P, hd[:, 1] - hd[:, 1] @ P, atol=1e-5)
    noise = iv.transform("noise", (0, 1), hr, hd, P, torch.Generator().manual_seed(1))
    for l in (0, 1):
        assert torch.allclose(((noise[l] - hr[:, l])).norm(dim=1), ((hd[:, l] - hr[:, l]) @ P).norm(dim=1), atol=1e-4)
        assert torch.allclose((noise[l] - hr[:, l]) @ P, noise[l] - hr[:, l], atol=1e-5)    # displacement stays inside S


def test_protected_complement_and_coefficient_split_use_the_cells_own_masks():
    m = c13.build("protected", 17)
    h = torch.randn(5, 32)
    cell = m.cells[0]
    P = cell.masks.T @ cell.masks
    assert torch.allclose(h @ P, cell.synthesize(cell.read_protected(h)), atol=1e-5)
    assert torch.allclose(h - h @ P, cell.complement(h), atol=1e-5)
    assert torch.allclose(iv.walsh_projector(), P, atol=1e-6)      # GRU "Walsh-8" control uses the identical subspace


def test_intervention_suite_bookkeeping(model):
    P = small_pairs(24, 16)
    out = iv.intervention_suite(model, P, "late", iv.random_projectors())
    assert out["sham_max_abs_logit_diff"] < 1e-5
    names = set(out["variants"])
    assert "sham" in names and "full_both" in names and "rand8_b7_both" in names and "rand24_b0_l1" in names
    assert ("prot_both" in names) == iv.is_protected(model) and ("walsh8_both" in names) != iv.is_protected(model)
    assert len(names) == 1 + 3 + 3 * (3 + 2 * iv.N_BASES)      # sham + full + per layer-set (sub, comp, noise, 8 rand8, 8 rand24)
    full = out["variants"]["full_both"]["all"]
    assert full["switch_to_donor"] is not None
    # a full transplant must reproduce the donor's changed-slot prediction: switch == donor's original correctness
    assert out["ordered_pairs"] == 32


def test_score_metrics_on_synthetic_predictions():
    n = 8
    slot = torch.tensor([0, 1, 2, 3] * 2)
    lab_r = torch.zeros(n, 4, dtype=torch.long)
    lab_d = lab_r.clone()
    lab_d[torch.arange(n), slot] = 1
    ctx = {"slot": slot, "lab_r": lab_r, "lab_d": lab_d, "pred_r": lab_r.clone(), "eligible": torch.ones(n, dtype=torch.bool),
           "fully_eligible": torch.ones(n, dtype=torch.bool), "initial": torch.tensor([True, False] * 4)}
    post = lab_r.clone()
    post[torch.arange(n), slot] = 1                      # perfect switch, unchanged slots intact
    s = iv.score(post, ctx)
    assert s["all"]["switch_to_donor"] == 1.0 and s["eligible"]["unchanged_slots_agree_with_original"] == 1.0
    assert s["eligible_initial_write"]["n"] == 4 and s["eligible_rewritten"]["n"] == 4
    assert iv.score(lab_r.clone(), ctx)["all"]["kept_recipient_value"] == 1.0
    assert iv.wilson(8, 8)[0] > .6 and iv.wilson(0, 0) == [None, None]


def test_phase5_outputs_are_finite_and_complete(model):
    P = iv.build_pairs(24, 64)
    out = iv.phase5(model, P, iv.random_projectors())
    assert out["pairs_used"] > 5
    for key in ("memory_displacement_ratio", "random_full_space_displacement_ratio", "random_in_designated_subspace_displacement_ratio",
                "memory_displacement_ratio_protected_part", "memory_displacement_ratio_complement_part"):
        assert len(out[key]) == 2 and all(torch.isfinite(torch.tensor(r)).all() for r in out[key])
    assert set(out["interpolation"]) == {"0.25", "0.5", "0.75"}
