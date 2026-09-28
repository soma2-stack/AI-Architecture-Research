"""Prereg v7: v6 C1 / C3 unchanged, detector-aligned C2 (ams/v7gen.py), accounting, integration."""
import collections
import os
import random
import subprocess
import sys

import pytest

from ams.canon import canon, struct_hash
from ams.fingerprint import Analysis, fingerprint
from ams.generate import MAX_RETRY
from ams.grammar import MAX_DEPTH, O, Node, const, make_program, program_to_dict, reads, sexpr, typecheck
from ams.v6gen import SGD_B, SGD_W, AnchoredGen, v6_invariants
from ams.v7gen import (V7_ACT_C2, V7_TOPK_KS, ZERO_S, DetectorAlignedGen, c2_updates, route_node,
                       v7_invariants)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _slots(seed, n):
    g = DetectorAlignedGen(random.Random(seed))
    return [list(g.v6_attempts()) for _ in range(n)]


def _emitted(seed, n):
    return [(p, m) for att in _slots(seed, n) for p, m, code in att if code is None]


@pytest.mark.parametrize("cls", ("C1", "C3"))
def test_c1_c3_identical_to_v6(cls):
    """Same RNG state -> identical C1 / C3 program and v6 metadata (plus the constructor tag)."""
    g6, g7 = AnchoredGen(random.Random(21)), DetectorAlignedGen(random.Random(21))
    for _ in range(200):
        p6, m6 = g6.v6_attempt(cls)
        p7, m7 = g7.v6_attempt(cls)
        assert p6 == p7 and {k: v for k, v in m7.items() if k != "constructor"} == m6
        assert all(v6_invariants(p7, m7).values())


def test_c2_template_backbone_and_residual_scale():
    g = DetectorAlignedGen(random.Random(22))
    for _ in range(400):
        p, m = g.v6_attempt("C2")
        route = p.dW.args[1].args[0].args[1]
        assert sexpr(p.dW) == f"(add (neg (outer d_bp a)) (mul (rowscale (neg (outer d_bp a)) {sexpr(route)}) 0.1))"
        assert sexpr(p.db) == f"(add (neg d_bp) (mul (mul (neg d_bp) {sexpr(route)}) 0.1))"
        assert p.dW.args[0] == SGD_W and p.db.args[0] == SGD_B and p.update_every == 1
        assert p.dW.args[1].args[1] == const(0.1) and p.db.args[1].args[1] == const(0.1)
        assert not p.regs and p.w_eff is None and p.gain is None and p.struct is None and p.cvec is None
        assert all(v7_invariants(p, m).values()), v7_invariants(p, m)


def test_c2_routes_selector_depth_and_activity():
    g = DetectorAlignedGen(random.Random(23))
    kinds, ks, depths = collections.Counter(), collections.Counter(), collections.Counter()
    for _ in range(1500):
        p, m = g.v6_attempt("C2")
        route = p.dW.args[1].args[0].args[1]
        sel = route.args[0]
        assert reads(sel) & V7_ACT_C2
        assert m["expr_depth"] in (0, 1)
        kinds[route.op] += 1
        depths[m["expr_depth"]] += 1
        if route.op == "topk":
            assert route.attr in V7_TOPK_KS and m["k"] == route.attr
            ks[route.attr] += 1
        else:
            assert route.args[1] == const(1.0) and route.args[2] == ZERO_S and m["k"] is None
    assert abs(kinds["topk"] - kinds["where"]) < 0.1 * 1500
    assert set(ks) == set(V7_TOPK_KS) and all(abs(ks[k] - sum(ks.values()) / 3) < 0.2 * sum(ks.values()) / 3 for k in ks)
    assert set(depths) == {0, 1}


def test_c2_depth_within_frozen_limit_and_always_valid():
    for att in _slots(24, 1500):
        assert len(att) == 1 and att[0][2] is None                  # v7 proposals are valid by construction
        p, m = att[0][0], att[0][1]
        info = typecheck(p)
        assert max(info["depths"].values()) <= MAX_DEPTH and info["nodes"] <= 40


def test_every_emitted_proposal_recognized_by_unchanged_fingerprint():
    for p, m in _emitted(25, 900):
        fp = fingerprint(p)
        assert m["v6_class"] in fp["couplings"] and fp["learning_signal"]
        if m["v6_class"] == "C2":
            assert Analysis(p).c2()


def test_where_route_zero_spelling_canonicalizes_to_where_1_0():
    """The legal `(sub 1.0 1.0)` spelling yields exactly the canonical program of the specified
    where(selector, 1, 0) (built with an internal 0.0 constant, which generated programs may not use)."""
    g = DetectorAlignedGen(random.Random(26))
    n = 0
    while n < 150:
        p, m = g.v6_attempt("C2")
        if m["route"] != "where":
            continue
        n += 1
        sel = p.dW.args[1].args[0].args[1].args[0]
        spec_route = Node("where", (sel, const(1.0), const(0.0)))
        dW, db = c2_updates(spec_route)
        spec = make_program(sexpr(dW), sexpr(db))
        typecheck(spec, internal=True)
        assert struct_hash(canon(p)) == struct_hash(canon(spec, check=False))
    with pytest.raises(Exception):                                 # the literal 0.0 is not a legal constant
        typecheck(make_program("(neg (outer d_bp a))", "(add (neg d_bp) (mul (mul (neg d_bp) (where z 1.0 0.0)) 0.1))"))


def test_uniform_primary_class():
    c = collections.Counter(att[0][1]["v6_class"] for att in _slots(27, 3000))
    assert all(900 <= c[k] <= 1100 for k in ("C1", "C2", "C3")), c


def test_retry_accounting_counts_invalid_instantiated_programs(monkeypatch):
    """A validation failure of an instantiated program counts as generated and is retried (class
    fixed, <= 10 attempts); activity redraws are not counted."""
    import ams.search as S
    import ams.v7gen as V7
    pipe = _FakePipe()
    g = DetectorAlignedGen(random.Random(28))
    orig = V7.c2_updates
    calls = {"n": 0}

    def flaky(route):                                              # first 3 C2 instantiations are oversize
        calls["n"] += 1
        dW, db = orig(route)
        if calls["n"] <= 3:
            deep = dW
            for _ in range(4):
                deep = Node("neg", (deep,))
            return deep, db
        return dW, db

    monkeypatch.setattr(V7, "c2_updates", flaky)
    while calls["n"] < 4:
        S._v6_slot(pipe, g)
    inv = [r for r in pipe.records if r.label == "invalid"]
    assert len(inv) == 3 and all(r.detail["code"] == "oversize" and r.detail["v6"]["v6_class"] == "C2" for r in inv)
    assert pipe.counts["generated"] == len(pipe.added) + 3 == len(pipe.construction)
    assert [r.detail["v6"]["attempt"] for r in inv] == [1, 2, 3]
    assert g.redraws >= 0 and pipe.counts["invalid"] == 3                # redraws never reach the counters


def test_slot_skipped_after_ten_invalid_attempts(monkeypatch):
    import ams.search as S
    import ams.v7gen as V7
    pipe = _FakePipe()
    g = DetectorAlignedGen(random.Random(29))
    monkeypatch.setattr(V7, "c2_updates", lambda route: (Node("neg", (Node("neg", (Node("neg", (Node("neg", (
        Node("add", (SGD_W, Node("mul", (Node("rowscale", (SGD_W, route)), const(0.1))))),)),)),)),)), SGD_B))
    monkeypatch.setattr(g, "v6_class", lambda: "C2")
    S._v6_slot(pipe, g)
    assert pipe.counts["generated"] == MAX_RETRY == pipe.counts["invalid"] and not pipe.added


def test_constructor_imports_no_evaluation_module():
    code = ("import sys, random; sys.path.insert(0, %r)\n"
            "from ams.v7gen import DetectorAlignedGen\n"
            "g = DetectorAlignedGen(random.Random(0))\n"
            "[list(g.v6_attempts()) for _ in range(300)]\n"
            "bad = [m for m in ('ams.tasks','ams.runners','ams.tier1','ams.substrate','ams.probes',"
            "'ams.controls','ams.families','ams.metrics','ams.interp','ams.search','ams.canon',"
            "'ams.fingerprint') if m in sys.modules]\n"
            "print(bad)") % HERE
    assert subprocess.check_output([sys.executable, "-c", code], text=True).strip() == "[]"


class _FakePipe:
    def __init__(self):
        import ams.search as S
        self.S = S
        self.counts = collections.Counter()
        self.records, self.construction, self.added = [], {}, []

    def _emit(self, rec):
        self.records.append(rec)

    def try_add(self, p):
        self.counts["generated"] += 1
        self.added.append(p)


def test_map_elites_v7_init_uses_detector_aligned_constructor(monkeypatch):
    import ams.search as S
    from ams.families import FamilyLibrary
    monkeypatch.setattr(S, "N_GEN_MAX", 30)
    pipe = S.Pipeline(FamilyLibrary(), lambda p: {"pass": False}, lambda p: {"q": None})
    out = S.map_elites(pipe, random.Random(30), init="v7")
    assert out["stop"] == "N_GEN_MAX" and pipe.counts["generated"] == 30 == len(pipe.construction)
    for r in pipe.records:
        meta = pipe.construction[r.pid]
        assert meta["constructor"] == "v7" and r.raw["update_every"] == 1
        assert "(neg (outer d_bp a))" in r.raw["dW"] and "(neg d_bp)" in r.raw["db"]
        if r.label not in ("invalid", "dup_syntactic", "dup_behavioral", "probe_nonfinite"):
            assert meta["v6_class"] in r.fingerprint["couplings"] or r.label == "pure_rule"
