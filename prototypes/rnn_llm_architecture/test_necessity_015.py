"""Experiment 015 machinery: callback stepper equivalence, removal algebra, rescue identity, donor selection, pairs."""
import pytest
import torch

from prototypes.rnn_llm_architecture import capacity_010 as c10
from prototypes.rnn_llm_architecture import capacity_012 as c12
from prototypes.rnn_llm_architecture import capacity_013 as c13
from prototypes.rnn_llm_architecture import intervene_014 as iv
from prototypes.rnn_llm_architecture import necessity_015 as ne

BUILD = {"protected": lambda: c13.build("protected", 43), "gru32": lambda: c10.build("gru32", 4, 2, 43)}


@pytest.fixture(scope="module", params=sorted(BUILD))
def model(request):
    m = BUILD[request.param]()
    m.eval()
    return m


@pytest.fixture(scope="module")
def ctx(model):
    return ne.Context(model, 24, 16)


def test_pairs_fresh_valid_and_cut_order():
    P = ne.build_pairs(64, 64)
    v = iv.validate_pairs(P)
    assert v["histories_differ_in_exactly_one_token"] and v["exactly_one_label_differs"] and v["differing_label_is_changed_slot"]
    assert not torch.equal(P.tok_a, iv.build_pairs(64, 64).tok_a)            # not Experiment 014's pairs
    a, m, b = (ne.cut_times(P, t) for t in ne.TIMINGS)
    assert (a == P.pos + 1).all() and (a <= m).all() and (m <= b).all() and (b == P.T).all()
    train = {c12.training_seed(s, t) for s in (17, 29, 43) for t in range(3000)}
    used = {ne.PAIR_SEED_BASE + d for d in ne.DELAYS} | {ne.REF_SEED_BASE + d for d in ne.DELAYS}
    assert not used & train and not used & {iv.PAIR_SEED_BASE + d for d in iv.DELAYS}


def test_values_over_time_matches_replay():
    x = c10.generator_batch(4, 2, 40, 32, seed=3)
    v = ne.values_over_time(x)
    assert torch.equal(v[:, -1], c10.replay(x, 4, 2))
    assert (v[:, 0] == -1).all()


def test_callback_stepper_equals_014_stepper_and_forward(model):
    x = ne.build_pairs(24, 16).tok_a
    a, b = ne.run_events(model, x), iv.staged_run(model, x)
    assert torch.equal(a["logits"], b["logits"])
    assert iv.verify_stepper(model, x, k=10)["max_abs_logit_diff_stepper_vs_forward"] < 1e-4


def test_twin_replacement_reproduces_twin_and_rescue_identity(model, ctx):
    cut = ne.cut_times(ctx.P, "mid_continuation").repeat(2)
    twin_state = ctx.at(ctx.nat_twin, cut)
    full = ne.run_events(model, ctx.hist, [(cut, ne.LAYER, lambda h: twin_state.clone())])      # layer-1-only replacement runs
    # exact positive control: replacing BOTH layers with the twin's states reproduces the twin's run
    tw0 = ne.run_events(model, ctx.twin, record=True)["nat"][torch.arange(ctx.n), cut - 1]
    rec0 = ne.run_events(model, ctx.hist, [(cut, 0, lambda h: tw0[:, 0].clone()), (cut, 1, lambda h: tw0[:, 1].clone())])
    assert (rec0["logits"] - ne.run_events(model, ctx.twin)["logits"]).abs().max() < 1e-5
    assert full["logits"].shape == rec0["logits"].shape
    h0 = ctx.at(ctx.nat, cut)
    mu = ctx.mu[cut - 1]
    rem_then_restore = ne.run_events(model, ctx.hist, [(cut, 1, lambda h: ne.remove(h, ctx.Ps, mu)), (cut, 1, lambda h: ne.remove(h, ctx.Ps, h0))])
    assert (rem_then_restore["logits"] - ne.run_events(model, ctx.hist)["logits"]).abs().max() < 1e-5


def test_removal_algebra(ctx):
    h = torch.randn(7, 32)
    ref = torch.randn(7, 32)
    Ps = ctx.Ps
    new = ne.remove(h, Ps, ref)
    assert torch.allclose(new @ Ps, ref @ Ps, atol=1e-5) and torch.allclose(new - new @ Ps, h - h @ Ps, atol=1e-5)
    z = ne.remove(h, Ps, None)
    assert torch.allclose(z @ Ps, torch.zeros_like(h), atol=1e-5)


def test_unrelated_donors_hold_requested_value(ctx):
    cut = ne.cut_times(ctx.P, "before_query").repeat(2)
    i = torch.arange(ctx.n)
    for same in (True, False):
        donor, ok = ctx.unrelated_donor(cut, same)
        assert ok.all()
        want = ctx.lab[i, ctx.slot] if same else 1 - ctx.lab[i, ctx.slot]
        # the chosen reference state must be one of the natural states with that stored value at that time
        for b in range(0, ctx.n, 5):
            t = int(cut[b]) - 1
            matches = (ctx.ref_nat[:, t] - donor[b]).abs().sum(1) == 0
            j = int(matches.nonzero()[0])
            assert int(ctx.ref_vals[j, t, int(ctx.slot[b])]) == int(want[b])


def test_variants_and_scoring_run(model, ctx):
    cut, h0, vs = ne.removal_variants(ctx, "after_write")
    assert {"sham", "S_mean", "C_mean", "S_mean_rescue_S", "R8_mean_b7", "R8_normrand_b0", "R24_mean_b3", "full_twin"} <= set(vs)
    assert "S_mean_rescue_S" not in ne.removal_variants(ctx, "before_query")[2]
    ev, info = vs["sham"]
    res = ne.run_events(model, ctx.hist, ev)
    s = ne.score(ctx, res["logits"].argmax(-1), info)
    assert s["all"]["other_agree_with_original"] == 1.0
    assert s["all"]["target_acc"] == float(ctx.target_ok.float().mean())
    ev, info = vs["full_twin"]
    assert "donor_value_rate" in ne.score(ctx, ne.run_events(model, ctx.hist, ev)["logits"].argmax(-1), info)["all"]
    assert ctx.nn_ratio(h0, h0) == 1.0
