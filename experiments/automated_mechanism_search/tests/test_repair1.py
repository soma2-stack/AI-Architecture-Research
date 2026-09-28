"""Stage-2 implementation repair 1 (owner-authorized, v5 frozen protocol unchanged):
families.strip_gates must preserve the type of a neutralized `where` gate.

Regression evidence: the six programs that raised typing errors ('defect') in the first
official Stage-2 run (runs/stage2/records.jsonl.gz), direct scalar-branch fixtures, and a
golden snapshot of all reference/disguise collision outputs computed with the PRE-repair code
(commit 9dd8a5e) to show the repair changes nothing else."""
import gzip
import json
import os

import pytest

from ams.canon import abstract_hash, canon, struct_hash
from ams.families import DISGUISES, REFERENCES, FamilyLibrary, strip_gates, terms
from ams.fingerprint import expand, fingerprint
from ams.grammar import (GrammarError, O, I, make_program, parse, program_from_dict, serialize, sexpr,
                         type_of, typecheck)
from ams.probes import DuplicateIndex

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFECT_PIDS = ["P01515", "P01523", "P02385", "P04354", "P05662", "P05782"]


@pytest.fixture(scope="module")
def lib():
    return FamilyLibrary()


@pytest.fixture(scope="module")
def defect_records():
    recs = {}
    with gzip.open(os.path.join(HERE, "runs", "stage2", "records.jsonl.gz"), "rt") as f:
        for line in f:
            r = json.loads(line)
            if r["pid"] in DEFECT_PIDS:
                recs[r["pid"]] = r
    return recs


def test_six_defects_are_the_recorded_ones(defect_records):
    assert sorted(defect_records) == DEFECT_PIDS
    for r in defect_records.values():
        assert r["label"] == "defect" and r["detail"]["error"].startswith("GrammarError(\"ill_typed")


def _old_strip_gates(e, rt):
    """Pre-repair rule (commit 9dd8a5e): where -> positive branch regardless of type."""
    from ams.canon import simplify, subst
    from ams.grammar import tconst

    def fn(x):
        if x.op == "topk":
            return tconst(1.0, type_of(x, rt))
        if x.op == "where":
            return x.args[1]
        return None
    return simplify(subst(e, fn), rt)


@pytest.mark.parametrize("pid", DEFECT_PIDS)
def test_old_rule_reproduces_recorded_defect(pid, defect_records, monkeypatch, lib):
    """Root cause: with the pre-repair where->branch rule, decomposition raises the recorded
    typing error on each of the six programs."""
    import ams.families as fam
    monkeypatch.setattr(fam, "strip_gates", _old_strip_gates)
    c = canon(program_from_dict(defect_records[pid]["raw"]))
    with pytest.raises(GrammarError) as ei:
        lib.decompose(c)
    assert str(ei.value).startswith("ill_typed")
    rec_msg = defect_records[pid]["detail"]["error"]
    assert str(ei.value).split("(got")[0].strip() in rec_msg


@pytest.mark.parametrize("pid", DEFECT_PIDS)
def test_defect_program_now_decomposes(pid, defect_records, lib):
    raw = program_from_dict(defect_records[pid]["raw"])
    typecheck(raw)
    c = canon(raw)
    k, info = lib.decompose(c)                                   # previously raised GrammarError
    typecheck(k, internal=True, limits=False)
    rt = c.reg_types()
    for slot, e in c.slot_exprs():
        ex = expand(c, e)
        for t in [ex] + terms(ex, rt):
            st = strip_gates(t, rt)
            assert type_of(st, rt) == type_of(t, rt), (pid, slot, sexpr(t), sexpr(st))


def test_where_scalar_branch_vector_O():
    e = parse("(where h L d_bp)")
    st = strip_gates(e, {})
    assert type_of(st, {}) == O and sexpr(st) == "(add 0@O L)"


def test_where_scalar_branch_vector_I():
    e = parse("(where a Lbar xi_I)")
    st = strip_gates(e, {})
    assert type_of(st, {}) == I and sexpr(st) == "(add 0@I Lbar)"


def test_where_same_type_branch_unchanged():
    e = parse("(where h d_bp e)")
    assert sexpr(strip_gates(e, {})) == "d_bp"                  # original semantics kept


def test_where_scalar_branch_inside_matrix_expression():
    e = parse("(outer (where h L d_bp) a)")                     # the P01523-style context
    st = strip_gates(e, {})
    assert type_of(st, {}) == "M"


def test_matrix_where_is_illegal_in_frozen_grammar():
    for dW in ("(where W W W_ep0)", "(where (outer h a) W 1)"):
        with pytest.raises(GrammarError):
            typecheck(make_program(dW, "(neg d_bp)"))


def test_reference_collision_outputs_identical_to_pre_repair(lib):
    gold = json.load(open(os.path.join(HERE, "tests", "fixtures", "reference_golden_pre_repair.json")))
    assert len(gold) == len(REFERENCES) * (1 + len(DISGUISES))
    for name, p in REFERENCES.items():
        for dn, d in [("identity", lambda x: x)] + list(DISGUISES.items()):
            c = canon(d(p))
            k, info = lib.decompose(c)
            g = gold[f"{name}|{dn}"]
            assert serialize(c) == g["canon"] and struct_hash(c) == g["struct_hash"]
            assert abstract_hash(c) == g["abstract_hash"]
            assert json.loads(json.dumps(fingerprint(c), default=str)) == g["fingerprint"]
            assert DuplicateIndex.exact_key(lib.runner.beta(c)) == g["beta_hash"]
            assert struct_hash(k) == g["K_hash"]
            assert json.loads(json.dumps(info, default=str)) == g["K_info"]
            assert json.loads(json.dumps(lib.match(c), default=str)) == g["match"], (name, dn)
