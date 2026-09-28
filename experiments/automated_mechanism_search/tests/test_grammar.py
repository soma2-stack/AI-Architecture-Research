"""Typing, size limits, phase availability, serialization (AE.6 test 1)."""
import pytest

from ams.families import REFERENCES
from ams.grammar import (GrammarError, M, O, RegDecl, make_program, parse, program_from_dict,
                         program_to_dict, serialize, sexpr, typecheck)

SGD_W, SGD_B = "(neg (outer d_bp a))", "(neg d_bp)"

INVALID = {
    "dW_wrong_type": dict(dW="(outer d_bp d_bp)", db=SGD_B),               # outer(O,O)
    "db_wrong_type": dict(dW=SGD_W, db="a"),
    "binary_mismatch": dict(dW="(add (outer d_bp a) d_bp)", db=SGD_B),
    "scalar_first": dict(dW="(mul L (outer d_bp a))", db=SGD_B),          # (S,T) is ill-typed
    "bad_const": dict(dW="(mul (outer d_bp a) 0.3)", db=SGD_B),
    "bad_topk": dict(dW=SGD_W, db="(mul d_bp (topk h 3))"),
    "topk_on_M": dict(dW="(topk (outer d_bp a) 4)", db=SGD_B),
    "nrm_on_M": dict(dW="(nrm W)", db=SGD_B),
    "phase_forward_reads_dbp": dict(dW=SGD_W, db=SGD_B, w_eff="(outer d_bp a)"),
    "phase_forward_reads_h": dict(dW=SGD_W, db=SGD_B, gain="h"),
    "phase_credit_reads_cvec": dict(dW=SGD_W, db=SGD_B, cvec="(neg cvec)"),
    "cvec_undefined": dict(dW="(outer cvec a)", db=SGD_B),
    "depth6": dict(dW="(neg (neg (neg (neg (neg (outer d_bp a))))))", db=SGD_B),
    "oversize_nodes": dict(dW="(add (add (add (outer d_bp a) (outer d_fa a)) (add (outer e a) (outer h a))) "
                              "(add (add (outer z a) (outer dphi a)) (add (outer b a) (outer xi_O a))))",
                           db="(add (add (add d_bp d_fa) (add e h)) (add (add z dphi) (add b xi_O)))"),
    "unknown_register": dict(dW="(neg r7)", db=SGD_B),
    "five_registers": dict(dW=SGD_W, db=SGD_B, regs=[(f"r{k}", O, "RUN", "0", 0.9, "h") for k in range(1, 6)]),
    "three_M_registers": dict(dW=SGD_W, db=SGD_B, regs=[(f"r{k}", M, "RUN", "0", 0.9, "(outer h a)") for k in range(1, 4)]),
    "bad_decay": dict(dW=SGD_W, db=SGD_B, regs=[("r1", O, "RUN", "0", 0.95, "h")]),
    "bad_lifetime": dict(dW=SGD_W, db=SGD_B, regs=[("r1", O, "FOREVER", "0", 0.9, "h")]),
    "bad_theta": dict(dW=SGD_W, db=SGD_B, struct=("reinit", "h", 0.3)),
    "reg_update_type": dict(dW=SGD_W, db=SGD_B, regs=[("r1", O, "RUN", "0", 0.9, "a")]),
}


def test_all_references_valid_within_limits():
    for name, p in REFERENCES.items():
        info = typecheck(p)
        assert info["nodes"] <= 40, name
        assert max(info["depths"].values()) <= 5, name


@pytest.mark.parametrize("name", sorted(INVALID))
def test_invalid_fixtures_rejected(name):
    kw = dict(INVALID[name])
    with pytest.raises(GrammarError):
        typecheck(make_program(**kw))


def test_fixture_count_at_least_40():
    assert len(REFERENCES) + len(INVALID) >= 40


def test_update_every_and_struct_kind():
    p = make_program(SGD_W, SGD_B, update_every=3)
    with pytest.raises(GrammarError):
        typecheck(p)
    p = make_program(SGD_W, SGD_B, struct=("grow", "h", 0.0))
    with pytest.raises(GrammarError):
        typecheck(p)


def test_serialization_roundtrip():
    for name, p in REFERENCES.items():
        d = program_to_dict(p)
        q = program_from_dict(d)
        assert serialize(q) == serialize(p), name
    n = parse("(topk (matvec W a) 8)")
    assert sexpr(n) == "(topk (matvec W a) 8)"
