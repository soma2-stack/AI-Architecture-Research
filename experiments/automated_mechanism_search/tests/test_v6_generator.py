"""Prereg v6: SGD-anchored initial constructor (ams/v6gen.py) and its search integration."""
import collections
import gzip
import json
import os
import random
import subprocess
import sys

import pytest

from ams.canon import canon
from ams.fingerprint import fingerprint
from ams.generate import MAX_RETRY, Gen
from ams.grammar import (M, O, GrammarError, Node, make_program, parse, program_to_dict, reads, sexpr,
                         typecheck)
from ams.v6gen import (SGD_B, SGD_W, V6_ACT_C1, V6_ACT_C23, V6_CLASSES, V6_DECAYS, AnchoredGen,
                       fast_weight, squash_gain, v6_invariants)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _slots(seed, n):
    g = AnchoredGen(random.Random(seed))
    return [list(g.v6_attempts()) for _ in range(n)]


def _valid(seed, n):
    return [(p, m) for att in _slots(seed, n) for p, m, code in att if code is None]


def test_backbone_is_exact_r1_sgd():
    from ams.families import SGD_B as RB, SGD_W as RW
    assert SGD_W == parse(RW) and SGD_B == parse(RB)
    assert sexpr(SGD_W) == "(neg (outer d_bp a))" and sexpr(SGD_B) == "(neg d_bp)"


def test_gain_templates_are_the_v6_formulas_in_legal_operand_order():
    r = Node("reg", (), "r1")
    assert sexpr(squash_gain(r)) == "(add (mul (tanh r1) 0.1) 1)"
    assert sexpr(fast_weight(r)) == "(mul (tanh r1) 0.1)"
    # the literal add(1.0, X) with a vector X is ill-typed in the frozen grammar (operands (T,T) or (T,S))
    with pytest.raises(GrammarError):
        typecheck(make_program("(neg (outer d_bp a))", "(neg d_bp)", regs=[("r1", O, "RUN", "0", 0.9, "z")],
                               gain="(add 1.0 (mul (tanh r1) 0.1))"))


def test_every_valid_proposal_satisfies_all_constructor_invariants():
    vs = _valid(1, 600)
    assert len(vs) == 600
    for p, m in vs:
        inv = v6_invariants(p, m)
        assert all(inv.values()), (m, inv, program_to_dict(p))
        assert m["expr_depth"] in (1, 2)


@pytest.mark.parametrize("cls", V6_CLASSES)
def test_class_templates(cls):
    g = AnchoredGen(random.Random(7))
    for _ in range(100):
        p, m = g.v6_attempt(cls)
        assert p.update_every == 1 and p.cvec is None
        if cls == "C1":
            (r,), (up,) = p.regs, p.reg_updates
            assert r.lifetime == "RUN" and r.init == "0" and r.decay in V6_DECAYS and r.type in (O, M)
            assert reads(up) & V6_ACT_C1
            assert p.dW == SGD_W and p.db == SGD_B and p.struct is None
            if r.type == M:
                assert sexpr(p.w_eff) == "(mul (tanh r1) 0.1)" and p.gain is None
            else:
                assert sexpr(p.gain) == "(add (mul (tanh r1) 0.1) 1)" and p.w_eff is None
        elif cls == "C2":
            assert not p.regs and p.w_eff is None and p.gain is None and p.struct is None
            g_ = p.dW.args[1]
            assert p.dW == Node("rowscale", (SGD_W, g_)) and p.db == Node("mul", (SGD_B, g_))
            sel = g_.args[0].args[0].args[0]
            assert g_ == squash_gain(sel) and reads(sel) & V6_ACT_C23
        else:
            (r,), (up,) = p.regs, p.reg_updates
            assert r.type == O and r.lifetime == "RUN" and r.init == "0" and r.decay in V6_DECAYS
            assert reads(up) & V6_ACT_C23
            assert p.dW == SGD_W and p.db == SGD_B and p.w_eff is None and p.gain is None
            assert p.struct.kind in ("freeze", "reinit") and p.struct.theta in (0.0, 0.1, 0.5)
            assert sexpr(p.struct.mask) == "(tanh r1)"


def test_uniform_primary_class_and_sub_choices():
    sl = _slots(2, 3000)
    c = collections.Counter(att[0][1]["v6_class"] for att in sl)
    assert all(900 <= c[k] <= 1100 for k in V6_CLASSES), c
    vs = [(p, m) for att in sl for p, m, code in att if code is None]
    c1 = collections.Counter(m["reg_type"] for _, m in vs if m["v6_class"] == "C1")
    assert abs(c1[O] - c1[M]) < 0.15 * sum(c1.values())
    for key, vals in (("decay", V6_DECAYS), ("theta", (0.0, 0.1, 0.5)), ("kind", ("freeze", "reinit"))):
        cc = collections.Counter(m[key] for _, m in vs if key in m)
        n = sum(cc.values())
        assert set(cc) == set(vals) and all(abs(cc[v] - n / len(vals)) < 0.2 * n / len(vals) for v in vals)


def test_class_is_held_fixed_across_retries_and_attempts_are_bounded():
    for att in _slots(3, 1500):
        assert len(att) <= MAX_RETRY
        assert len({m["v6_class"] for _, m, _ in att}) == 1
        assert all(code is not None for _, _, code in att[:-1])
        assert [m["attempt"] for _, m, _ in att] == list(range(1, len(att) + 1))


def test_only_c2_depth2_selectors_are_invalid_and_they_exceed_frozen_depth():
    for att in _slots(4, 1500):
        for p, m, code in att:
            if code is not None:
                assert m["v6_class"] == "C2" and code == "oversize" and m["expr_depth"] == 2
            if m["v6_class"] == "C2" and m["expr_depth"] == 2:
                assert code == "oversize"


def test_frozen_fingerprint_does_not_detect_v6_c2_soft_gate():
    """Documents the v6 / frozen-fingerprint conflict found by the static validation (D-V6-6):
    the frozen C2 detector (Part AE: gate via topk/where on activity) does not see the v6 soft gate."""
    g = "(add (mul (tanh (max dphi z)) 0.1) 1.0)"
    p = make_program(f"(rowscale (neg (outer d_bp a)) {g})", f"(mul (neg d_bp) {g})")
    assert fingerprint(p)["couplings"] == [] and fingerprint(canon(p))["couplings"] == []
    g2 = "(add (mul (tanh (topk z 4)) 0.1) 1.0)"          # incidental routing gate inside the selector
    p2 = make_program(f"(rowscale (neg (outer d_bp a)) {g2})", f"(mul (neg d_bp) {g2})")
    assert fingerprint(canon(p2))["couplings"] == ["C2"]


def test_c1_c3_couplings_detected_by_frozen_fingerprint():
    for p, m in _valid(5, 600):
        if m["v6_class"] == "C2":
            continue
        fr = fingerprint(p)
        assert m["v6_class"] in fr["couplings"] and fr["learning_signal"]


def test_constructor_imports_no_evaluation_module():
    code = ("import sys, random; sys.path.insert(0, %r)\n"
            "from ams.v6gen import AnchoredGen\n"
            "g = AnchoredGen(random.Random(0))\n"
            "[list(g.v6_attempts()) for _ in range(200)]\n"
            "bad = [m for m in ('ams.tasks','ams.runners','ams.tier1','ams.substrate','ams.probes',"
            "'ams.controls','ams.families','ams.metrics','ams.interp','ams.search') if m in sys.modules]\n"
            "print(bad)") % HERE
    out = subprocess.check_output([sys.executable, "-c", code], text=True).strip()
    assert out == "[]"


def test_v5_random_constructor_trace_unchanged():
    """The v5 `Gen.program` sequence of the official repaired rerun is reproduced (first 300)."""
    path = os.path.join(HERE, "runs", "stage2_repair1", "records.jsonl.gz")
    recs = []
    with gzip.open(path, "rt") as f:
        for line in f:
            recs.append(json.loads(line)["raw"])
            if len(recs) == 300:
                break
    g = Gen(random.Random(20260928))
    for r in recs:
        assert program_to_dict(g.program()) == r


class _FakePipe:
    def __init__(self, n_max):
        import ams.search as S
        self.S = S
        self.n_max = n_max
        self.counts = collections.Counter()
        self.records, self.construction, self.added = [], {}, []

    def _emit(self, rec):
        self.records.append(rec)

    def try_add(self, p):
        if self.counts["generated"] >= self.n_max:
            raise self.S.BudgetExhausted("N_GEN_MAX")
        self.counts["generated"] += 1
        self.added.append(p)


def test_v6_slot_counts_every_invalid_attempt_as_generated(monkeypatch):
    import ams.search as S
    pipe = _FakePipe(10 ** 6)
    monkeypatch.setattr(S, "N_GEN_MAX", 10 ** 6)
    g = AnchoredGen(random.Random(11))
    ref = AnchoredGen(random.Random(11))
    n_att = 0
    for _ in range(300):
        S._v6_slot(pipe, g)
        n_att += len(list(ref.v6_attempts()))
    assert pipe.counts["generated"] == n_att == len(pipe.construction)
    assert pipe.counts["invalid"] == len(pipe.records) == n_att - len(pipe.added)
    assert all(r.label == "invalid" and r.detail["v6"]["v6_class"] == "C2" for r in pipe.records)


def test_v6_slot_respects_generation_budget(monkeypatch):
    import ams.search as S
    monkeypatch.setattr(S, "N_GEN_MAX", 25)
    pipe = _FakePipe(25)
    g = AnchoredGen(random.Random(12))
    with pytest.raises(S.BudgetExhausted):
        for _ in range(100):
            S._v6_slot(pipe, g)
    assert pipe.counts["generated"] == 25


def test_map_elites_v6_init_uses_anchored_constructor(monkeypatch):
    import ams.search as S
    from ams.families import FamilyLibrary
    monkeypatch.setattr(S, "N_GEN_MAX", 30)
    pipe = S.Pipeline(FamilyLibrary(), lambda p: {"pass": False}, lambda p: {"q": None})
    out = S.map_elites(pipe, random.Random(13), init="v6")
    assert out["stop"] == "N_GEN_MAX" and pipe.counts["generated"] == 30
    assert len(pipe.construction) == 30 and len(pipe.records) == 30
    for r in pipe.records:
        d = r.raw
        assert d["update_every"] == 1 and "(neg (outer d_bp a))" in d["dW"] and "(neg d_bp)" in d["db"]
        assert pipe.construction[r.pid]["v6_class"] in V6_CLASSES
