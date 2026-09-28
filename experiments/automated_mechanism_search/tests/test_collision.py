"""Canonicalization, structural/behavioural duplicates, v2 probe corpus verification,
fingerprints, family matcher recall, coupling eligibility (AE.6 tests 2-5)."""
import itertools
import os
import shutil

import numpy as np
import pytest

from ams import PROBE_BLOB_SHA
from ams.canon import canon, canon_hash, struct_hash
from ams.families import DISGUISES, REFERENCES, FamilyLibrary
from ams.fingerprint import Analysis, fingerprint
from ams.grammar import I, M, O, S, make_program, serialize
from ams.interp import Compiled
from ams.probes import (CORPUS_PATH, DuplicateIndex, ProbeCorpusError, ProbeRunner, cos, git_blob_sha,
                        load_corpus, regeneration_check)
from ams.substrate import DT, Net, ProgramLearner, Trainer


@pytest.fixture(scope="module")
def lib():
    return FamilyLibrary()


# ---------------------------------------------------------------- probe corpus (v2 mandatory check)

def test_probe_corpus_exists_and_matches_frozen_blob():
    assert os.path.exists(CORPUS_PATH)
    assert git_blob_sha(CORPUS_PATH) == PROBE_BLOB_SHA == "d5a8e0d1d91d1d1caf5ff3cbb84f9a4c76e730c1"
    c = load_corpus()
    assert len(c) == 16
    assert c[0]["W"].shape == (6, 8) and c[0]["a"].shape == (8,) and len(c[0]["bank"]) == 4


def test_probe_corpus_modified_copy_is_rejected(tmp_path):
    bad = tmp_path / "probes.json"
    shutil.copy(CORPUS_PATH, bad)
    with open(bad, "a") as f:
        f.write(" ")
    with pytest.raises(ProbeCorpusError):
        load_corpus(str(bad))
    with pytest.raises(ProbeCorpusError):
        load_corpus(str(tmp_path / "missing.json"))


def test_regeneration_aid_reproduces_vector_fields():
    rep = regeneration_check()
    for f in ("W", "b", "a", "d_bp", "d_fa", "e", "xi_I", "xi_O", "reg_I", "reg_O", "reg_M"):
        assert rep[f]["exact"], f


# ---------------------------------------------------------------- canonicalization

def _equivalent_pairs():
    P = make_program
    W, B = "(neg (outer d_bp a))", "(neg d_bp)"
    pairs = [
        (P(W, B), P("(add (neg (outer d_bp a)) (sub 1 1))", B)),
        (P(W, B), P("(mul (neg (outer d_bp a)) 1)", B)),
        (P(W, B), P("(neg (neg (neg (outer d_bp a))))", B)),
        (P(W, B), P(W, B, cvec="d_bp")),
        (P("(neg (outer cvec a))", "(neg cvec)", cvec="d_bp"), P(W, B)),
        (P(W, B), P(W, B, regs=[("r1", O, "RUN", "0", 0.9, "h")])),            # dead register
        (P(W, B), P("(add (neg (outer d_bp a)) (mul (outer h a) (sub 1 1)))", B)),
        (P(W, B), P("(sub (neg (outer d_bp a)) (sub W W))", B)),
        (P("(abs (abs (outer d_bp a)))", B), P("(abs (outer d_bp a))", B)),
        (P("(mul (outer d_bp a) (outer d_bp a))", B), P("(square (outer d_bp a))", B)),
        (P("(sign (square (outer d_bp a)))", B), P("(step (abs (outer d_bp a)))", B)),
        (P("(outer (nrm (nrm d_bp)) a)", B), P("(outer (nrm d_bp) a)", B)),
        (P("(outer d_bp (unit (unit a)))", B), P("(outer d_bp (unit a))", B)),
        (P("(outer (where h d_bp d_bp) a)", B), P("(outer d_bp a)", B)),
        (P("(outer (mul d_bp L) a)", B), P("(mul (outer d_bp a) L)", B)),
        (P("(rowscale (outer d_bp a) h)", B), P("(outer (mul d_bp h) a)", B)),
        (P("(add (outer d_bp a) (outer h a))", B), P("(add (outer h a) (outer d_bp a))", B)),
        (P("(mul W (outer d_bp a))", B), P("(mul (outer d_bp a) W)", B)),
        (P("(max (outer h a) (outer d_bp a))", B), P("(max (outer d_bp a) (outer h a))", B)),
        (P(W, "(mul d_bp (add 0.5 0.5))"), P(W, "d_bp")),
        (P(W, B, w_eff="r1", regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]),
         P(W, B, w_eff="r2", regs=[("r2", M, "RUN", "0", 0.9, "(outer h a)")])),
        (P("(neg (add r1 r2))", B, regs=[("r1", M, "RUN", "0", 0.9, "(outer d_bp a)"),
                                         ("r2", M, "RUN", "0", 0.5, "(outer h a)")]),
         P("(neg (add r2 r1))", B, regs=[("r2", M, "RUN", "0", 0.9, "(outer d_bp a)"),
                                         ("r1", M, "RUN", "0", 0.5, "(outer h a)")])),
        (P("(neg r1)", B, regs=[("r1", M, "EXAMPLE", "0", 0.0, "(outer d_bp a)")]), P(W, B)),
        (P("(neg r1)", B, regs=[("r1", M, "RUN", "0", 0.0, "(outer d_bp a)")]), P(W, B)),
        (P("(neg r1)", B, regs=[("r1", M, "EXAMPLE", "0", 0.5, "(outer d_bp a)")]),
         P("(neg (mul (outer d_bp a) 0.5))", B)),
        (P(W, B, gain="(add (mul b (sub 1 1)) 1)"), P(W, B)),
        (P(W, B, w_eff="(sub W W)"), P(W, B)),
        (P(W, B, struct=("reinit", "(mul b (sub 1 1))", 0.1)), P(W, B)),
        (P("(neg (outer (neg (neg d_bp)) a))", B), P(W, B)),
        (P("(mul (outer (min h d_bp) a) (dot a a))", B), P("(mul (outer (min d_bp h) a) (dot a a))", B)),
    ]
    return pairs


def test_canon_known_equivalent_pairs_share_hash():
    pairs = _equivalent_pairs()
    assert len(pairs) >= 30
    for k, (p, q) in enumerate(pairs):
        assert canon_hash(p) == canon_hash(q), (k, serialize(canon(p)), serialize(canon(q)))


def test_canon_idempotent():
    for name, p in REFERENCES.items():
        c = canon(p)
        assert serialize(canon(c, check=False)) == serialize(c), name


def _online_weights(prog, steps=15, seed=2):
    net = Net(4, 3, [seed])
    tr = Trainer(net, ProgramLearner(prog, clip=True), [0.05], check_memory=False)
    tr.set_episodes(None); tr.episode_start()
    rng = np.random.default_rng(4)
    for t in range(steps):
        tr.step(rng.standard_normal((1, 1, 4)).astype(DT), rng.standard_normal((1, 1, 3)).astype(DT))
    return np.concatenate([w.ravel() for w in net.W])


def test_canon_preserves_online_semantics():
    """canon(P) and P produce the same training trajectory online (B = 1)."""
    progs = [p for p, _ in _equivalent_pairs()] + [q for _, q in _equivalent_pairs()] + list(REFERENCES.values())
    for p in progs:
        if any(r.init == "noise" for r in p.regs) or "xi" in serialize(p):
            continue
        a, b = _online_weights(p), _online_weights(canon(p))
        assert np.max(np.abs(a - b)) < 1e-4, serialize(p)


# ---------------------------------------------------------------- behavioural duplicates

def test_rescaled_and_commuted_variants_are_behavioural_duplicates(lib):
    r = lib.runner
    for name, p in REFERENCES.items():
        b0 = r.beta(canon(p))
        for dn in ("rescale", "reorder"):
            b1 = r.beta(canon(DISGUISES[dn](p)))
            assert cos(b0, b1) >= 0.999, (name, dn)


KNOWN_SAME_BEHAVIOUR = {frozenset(x) for x in [("R1_SGD", "R19_forward_hard_routing"), ("R1_SGD", "R24_loss_shaping"),
                                               ("R19_forward_hard_routing", "R24_loss_shaping"),
                                               ("R4_rmsprop_adam", "X5_adamw_like"),
                                               ("R9_hebbian", "R22_forward_forward")]}


def test_distinct_references_not_duplicates(lib):
    """AE test 3: known-distinct pairs do not collide.  Documented probe blind spots
    (scale-invariant modulation, topk k >= probe dim, Adam/AdamW) are listed explicitly."""
    B = {k: lib.runner.beta(p) for k, p in lib.canon.items()}
    idx = DuplicateIndex()
    n_ok = 0
    for a, b in itertools.combinations(B, 2):
        same = cos(B[a], B[b]) >= 0.999 or idx.exact_key(B[a]) == idx.exact_key(B[b])
        if frozenset((a, b)) in KNOWN_SAME_BEHAVIOUR:
            continue
        assert not same, (a, b)
        n_ok += 1
    assert n_ok >= 30


def test_duplicate_index():
    idx = DuplicateIndex()
    v = np.arange(10.0)
    idx.add("A", v)
    assert idx.find(v * 3)[0] == "A"
    assert idx.find(v[::-1]) is None


# ---------------------------------------------------------------- families

def test_family_matcher_recall_on_references_and_disguises(lib):
    for name, p in REFERENCES.items():
        m = lib.match(canon(p))
        assert m is not None and m["family"] == name, name
        for dn, d in DISGUISES.items():
            m = lib.match(canon(d(p)))
            assert m is not None, (name, dn)


def test_references_have_no_residual(lib):
    for name, p in lib.canon.items():
        k, _ = lib.decompose(p)
        assert struct_hash(k) == struct_hash(p), name


def test_residual_detected_for_novel_term(lib):
    p = canon(make_program("(add (neg (outer d_bp a)) (outer (mul dphi (sign d_fa)) (nrm a)))", "(neg d_bp)",
                           w_eff="r1", regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]))
    k, info = lib.decompose(p)
    assert struct_hash(k) != struct_hash(p)
    assert info["dropped_terms"]
    assert struct_hash(k) == struct_hash(lib.canon["R12_fast_weights"])


EXPECTED_FEATURES = {
    "R1_SGD": {"F1_global_bp"}, "R3_momentum": {"F6_momentum"}, "R4_rmsprop_adam": {"F7_second_moment"},
    "R8_DFA": {"F4_fixed_feedback"}, "R9_hebbian": {"F19_hebbian"}, "R10_oja": {"F20_oja_decay"},
    "R12_fast_weights": {"F8_fast_weights", "F9_fast_slow"}, "R13_fast_slow": {"F9_fast_slow"},
    "R15_three_factor": {"F5_eligibility_trace", "F21_reward_modulated"},
    "R16_node_perturbation": {"F22_perturbation"}, "R17_EWC_SI": {"F23_anchor_consolidation", "F17_freezing"},
    "R18_kWTA_sparse_update": {"F13_routing"}, "R20_homeostatic_gain": {"F24_gain_modulation"},
    "R21_continual_backprop": {"F18_structural_growth"}, "R22_forward_forward": {"F2_local_objective"},
    "R23_synthetic_gradient": {"F26_credit_predictor"}, "R24_loss_shaping": {"F25_loss_shaping"},
    "R6_EG_mirror": {"F14_multiplicative_plasticity"}, "X3_eprop_like": {"F5_eligibility_trace"},
}


def test_reference_fingerprints(lib):
    for name, feats in EXPECTED_FEATURES.items():
        f = fingerprint(lib.canon[name])["features"]
        on = {k for k, v in f.items() if v}
        assert feats <= on, (name, feats - on)
        assert f["F10_fixed_point"] == 0 and f["F12_explicit_memory"] == 0 and f["F16_orthogonal_projection"] == 0


def test_codex_schema_fields_present(lib):
    need = {"global_gradient", "local_gradient", "fixed_feedback", "transpose_required", "momentum_state",
            "second_moment_state", "eligibility_state", "fast_weights", "fast_slow_state",
            "activation_dependent_update", "input_dependent_routing", "normalization", "projection",
            "fixed_point_or_root_solve", "parameter_birth_reinit_freeze", "test_time_update",
            "meta_learned_update", "persistent_state_lifetimes", "forward_depends_on_learning_state"}
    for p in lib.canon.values():
        assert need <= set(fingerprint(p)["codex"])


# ---------------------------------------------------------------- coupling eligibility

@pytest.mark.parametrize("kw,coup,signal", [
    (dict(dW="(neg (outer d_bp a))", db="(neg d_bp)"), set(), True),
    (dict(dW="(neg (outer d_bp a))", db="(neg d_bp)", w_eff="r1", regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]), {"C1"}, True),
    (dict(dW="(neg (outer d_bp a))", db="(neg d_bp)", w_eff="r1", regs=[("r1", M, "RUN", "1", 0.9, "(mul r1 1)")]), set(), True),
    (dict(dW="(neg (rowscale (outer d_bp a) (topk h 4)))", db="(neg d_bp)"), {"C2"}, True),
    (dict(dW="(neg (rowscale (outer d_bp a) (topk d_bp 4)))", db="(neg d_bp)"), set(), True),
    (dict(dW="(mul (outer d_bp a) (norm (topk h 4)))", db="(neg d_bp)"), set(), True),
    (dict(dW="(neg (outer d_bp a))", db="(neg d_bp)", struct=("freeze", "(abs h)", 0.5)), {"C3"}, True),
    (dict(dW="(neg (outer d_bp a))", db="(neg d_bp)", struct=("freeze", "b", 0.5)), {"C3"}, True),
    (dict(dW="(outer h a)", db="h", w_eff="r1", regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]), {"C1"}, False),
    (dict(dW="(mul r1 (sub Lbar L))", db="h", gain="r2", regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)"),
                                                              ("r2", O, "RUN", "1", 0.9, "(abs h)")]), {"C1"}, True),
])
def test_coupling_and_learning_signal(kw, coup, signal):
    p = canon(make_program(**kw))
    a = Analysis(p)
    assert set(a.couplings()) == coup
    assert a.learning_signal() == signal
    d = a.descriptor()
    assert (d is None) == (not coup)
    if d is not None:
        assert 0 <= d[0] < 7 and 0 <= d[1] < 4 and d[2] in (0, 1)
