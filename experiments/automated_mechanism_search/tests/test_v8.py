"""Prereg v8: C* normalized adaptation AULC, gate-mutation zero repair, exact N_GEN_MAX boundary,
unchanged v7 constructor, seed separation / Stage-3 lock, v8 Tier-1 scoring, confirmation funnel,
Stage-3 v8 profile (AULC Gate 3, KF(P) Gate 4)."""
import collections
import gzip
import json
import math
import os
import random

import numpy as np
import pytest

from ams import confirm as CF
from ams import metrics as MX
from ams import stage3 as S3
from ams import tier1
from ams.canon import canon
from ams.generate import MUTATION_P, Gen, valid
from ams.grammar import program_to_dict, sexpr
from ams.runners import LOCKED_STAGE3_SEEDS, SeedLockError, _runs, run_C
from ams.tasks import TaskCstar
from ams.v7gen import ZERO_S, DetectorAlignedGen
from ams.v8gen import V8Gen

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAU = TaskCstar.tau
EV = list(range(0, 449, 4))
ENTRIES = [256, 384]


def _curve(fn):
    """MSE_R1 on the eval grid; fn(offset k from the current R1 entry) inside R1 segments."""
    out = []
    for s in EV:
        if 256 <= s <= 320:
            out.append(fn(s - 256))
        elif 384 <= s <= 448:
            out.append(fn(s - 384))
        else:
            out.append(1.0)
    return out


# ---------------------------------------------------------------------------- AULC
def test_aulc_no_adaptation_is_one():
    m = _curve(lambda k: 0.8)
    assert MX.adaptation_area(EV, m, 256, TAU) == pytest.approx(1.0)
    assert MX.adaptation_aulc(EV, m, ENTRIES, TAU) == pytest.approx(1.0)


def test_aulc_monotone_adaptation_below_one():
    E = 0.8
    m = _curve(lambda k: TAU + (E - TAU) * (1 - k / 64))           # linear decay to tau over 64 steps
    expect = float(np.mean([1 - k / 64 for k in range(4, 65, 4)]))  # = 1 - 34/64
    assert expect == pytest.approx(0.46875)
    assert MX.adaptation_aulc(EV, m, ENTRIES, TAU) == pytest.approx(expect)


def test_aulc_worsening_above_one():
    m = _curve(lambda k: 0.5 + 0.01 * k)
    assert MX.adaptation_aulc(EV, m, ENTRIES, TAU) > 1.0


def test_aulc_numerator_floor_and_entry_floor():
    m = _curve(lambda k: 0.5 if k == 0 else 0.01)                   # below tau after entry -> 0
    assert MX.adaptation_aulc(EV, m, ENTRIES, TAU) == 0.0
    m2 = _curve(lambda k: 0.04 if k == 0 else 0.05 + 1e-3)          # entry below tau -> 1e-8 floor
    assert MX.adaptation_area(EV, m2, 256, TAU) == pytest.approx(1e-3 / 1e-8)


def test_aulc_averages_the_two_entries():
    m = []
    for s in EV:
        if 256 <= s <= 320:
            m.append(0.8)                                            # first R1: no adaptation (1)
        elif 384 <= s <= 448:
            m.append(0.8 if s == 384 else TAU)                       # second R1: instant (0)
        else:
            m.append(1.0)
    assert MX.adaptation_aulc(EV, m, ENTRIES, TAU) == pytest.approx(0.5)


def test_run_C_records_aulc_consistently():
    from ams.controls import make
    r = run_C(make("SGD"), [7])
    ev, R1 = r["eval_steps"], np.array(r["R1"])
    for k, pr in enumerate(r["per_run"]):
        assert math.isfinite(pr["aulc"])
        assert pr["aulc"] == pytest.approx(MX.adaptation_aulc(ev, R1[k], ENTRIES, TAU))
        assert "median_hl_censored" in pr                           # half-life still recorded (diagnostic)


def test_v7_generic_curve_replay_is_finite_and_deterministic():
    """Offline replay of stored v7 generic C* curves (runs/stage3_v7 shared jobs); no training."""
    path = os.path.join(HERE, "runs", "stage3_v7", "jobs.jsonl.gz")
    n = 0
    for line in gzip.open(path, "rt"):
        j = json.loads(line)
        if not (j["job"]["cid"] == "shared:Cstar" and j["job"]["cond"] in ("SGD", "SGDM", "AdamW")):
            continue
        r = j["result"]
        for row, bad in zip(r["R1"], r["unstable"]):
            if bad:
                continue
            a = MX.adaptation_aulc(r["eval_steps"], row, ENTRIES, TAU)
            assert math.isfinite(a) and a == MX.adaptation_aulc(r["eval_steps"], row, ENTRIES, TAU)
            n += 1
    assert n >= 60


# ---------------------------------------------------------------------------- repairs
def test_gate_mutation_zero_repair():
    assert dict(MUTATION_P) == {"point_op": 0.25, "subtree": 0.20, "leaf_swap": 0.15, "const": 0.10,
                                "register": 0.10, "rewire_forward": 0.08, "gate": 0.07, "struct": 0.03,
                                "timing": 0.02}                      # probabilities unchanged
    g8, g7 = V8Gen(random.Random(3)), DetectorAlignedGen(random.Random(3))
    codes8, codes7 = collections.Counter(), collections.Counter()
    for _ in range(200):
        p, _, _ = next(g8.v6_attempts())
        p7, _, _ = next(g7.v6_attempts())
        q8, q7 = g8.m_gate(p), g7.m_gate(p7)
        if q8.dW.op == "rowscale" and q8.dW.args[1].op == "where":
            assert q8.dW.args[1].args[2] == ZERO_S
            codes8[valid(q8)] += 1
            if valid(q8) is None:                                     # canonical == intended where(sel, 1, 0)
                from dataclasses import replace as _r
                from ams.canon import struct_hash
                from ams.grammar import Node, const
                w = q8.dW.args[1]
                spec = _r(q8, dW=Node("rowscale", (q8.dW.args[0], Node("where", (w.args[0], const(1.0), const(0.0))))))
                assert struct_hash(canon(q8)) == struct_hash(canon(spec, check=False))
        if q7.dW.op == "rowscale" and q7.dW.args[1].op == "where":
            codes7[valid(q7)] += 1
    assert codes8[None] > 0 and "bad_const" not in codes8            # v8: never bad_const
    assert set(codes7) == {"bad_const"}                              # historical v7 behaviour kept for replay


class _Spy:
    def __init__(self, monkeypatch, cls):
        self.n = 0
        for name in ("v6_attempt", "mutate", "crossover"):
            orig = getattr(cls, name)

            def wrap(selfg, *a, _orig=orig, **k):
                self.n += 1
                return _orig(selfg, *a, **k)
            monkeypatch.setattr(cls, name, wrap)


class _Stub:
    def __init__(self):
        self.r = random.Random(0)

    def sanity(self, p):
        return {"pass": True}

    def tier1(self, p):
        q = self.r.uniform(-0.5, 0.6)
        return {"q": q, "best_task": "Cstar", "tier1_pass_on_best": q > 0.2}


@pytest.fixture(scope="module")
def lib():
    from ams.families import FamilyLibrary
    return FamilyLibrary()


@pytest.mark.parametrize("cap", [7, 23])
def test_exact_cap_no_uncounted_construction(monkeypatch, lib, cap):
    import ams.search as S
    monkeypatch.setattr(S, "N_GEN_MAX", cap)
    monkeypatch.setattr(S, "N_INIT", 3)
    monkeypatch.setattr(S, "OFFSPRING", 3)
    monkeypatch.setattr(S, "G_MAX", 100)
    monkeypatch.setattr(S, "PATIENCE", 1000)
    spy = _Spy(monkeypatch, V8Gen)
    ev = _Stub()
    pipe = S.Pipeline(lib, ev.sanity, ev.tier1)
    out = S.map_elites(pipe, random.Random(11), init="v8")
    assert out["stop"] == "N_GEN_MAX" and pipe.counts["generated"] == cap
    assert spy.n == cap                                              # every constructed candidate was counted


def test_v7_path_built_one_uncounted_candidate_at_the_cap(monkeypatch, lib):
    """Documents the repaired defect: the v7 path constructs one candidate after the cap."""
    import ams.search as S
    monkeypatch.setattr(S, "N_GEN_MAX", 7)
    spy = _Spy(monkeypatch, DetectorAlignedGen)
    ev = _Stub()
    pipe = S.Pipeline(lib, ev.sanity, ev.tier1)
    S.map_elites(pipe, random.Random(11), init="v7")
    assert pipe.counts["generated"] == 7 and spy.n == 8


# ---------------------------------------------------------------------------- constructor unchanged
def test_v8_initial_constructor_identical_to_v7():
    g7, g8 = DetectorAlignedGen(random.Random(70707)), V8Gen(random.Random(70707))
    for _ in range(500):
        a7, a8 = list(g7.v6_attempts()), list(g8.v6_attempts())
        assert [(program_to_dict(p), m, c) for p, m, c in a7] == [(program_to_dict(p), m, c) for p, m, c in a8]


def test_v7_static_validation_proposals_reproduced_by_v8_generator():
    rows = [json.loads(l) for l in gzip.open(os.path.join(HERE, "runs", "v7_static_validation", "proposals.jsonl.gz"), "rt")]
    g = V8Gen(random.Random(70707))
    got = []
    while len(got) < len(rows):
        for p, m, code in g.v6_attempts():
            got.append(program_to_dict(p))
    assert got == [r["raw"] for r in rows]


# ---------------------------------------------------------------------------- seeds
def test_seed_separation_and_stage3_lock():
    v8 = __import__("ams.manifest", fromlist=["RUN_CONFIG"]).RUN_CONFIG["stage2_v8"]
    sets = {"fast": set(tier1.V8_TIER1_SEEDS), "confirm": set(CF.CONFIRM_SEEDS), "stage3": set(v8["stage3_seeds"]),
            "sanity": {500}, "stage1": set(range(100, 105)), "v7_tier1": {1000, 1001, 1002},
            "v7_stage3": set(range(10000, 10010)), "tier3": set(range(20000, 20010))}
    names = list(sets)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            assert not (sets[names[i]] & sets[names[j]]), (names[i], names[j])
    assert set(v8["stage3_seeds"]) == set(LOCKED_STAGE3_SEEDS)
    for s in LOCKED_STAGE3_SEEDS:
        with pytest.raises(SeedLockError):
            _runs([s], (0.1,))
    assert _runs([5000], (0.1,)) == [(5000, 0.1)]


# ---------------------------------------------------------------------------- v8 fast Tier-1 scoring
def _cres(aulc_seeds, ret=(True, True, True), seeds=(5000, 5001, 5002), lr=0.1):
    runs = [(s, l) for s in seeds for l in (1e-3, 1e-2, 1e-1)]
    per = []
    for s, l in runs:
        i = seeds.index(s)
        d = {"aulc": aulc_seeds[i], "median_hl_censored": 12.0, "median_hl": 12.0, "return_ok": ret[i],
             "R0_pre_shift": 0.05, "R1_entry_mse": [0.5, 0.5], "train_select": 0.1 if l == lr else 9.0}
        per.append(d)
    return {"task": "Cstar", "runs": runs, "unstable": [False] * len(runs), "per_run": per}


def test_v8_tier1_cstar_effect_and_gates():
    base = {"best_generic": {"B": {"metric": 100.0, "T2_final_mse": 0.02}, "Cstar": {"metric": 0.6},
                             "F": {"metric": 0.8}},
            "adamw": {"B": {"mean": 100.0, "sd": 1e-9}, "Cstar": {"mean": 0.62, "sd": 0.05}, "F": {"mean": 0.8, "sd": 0.01}}}
    unstable = {"runs": [], "error": "x"}
    tr = {"B": unstable, "F": unstable, "Cstar": _cres([0.3, 0.3, 0.3])}
    from ams.canon import canon as C
    from ams.families import REFERENCES
    out = tier1.score(C(REFERENCES["R1_SGD"]), tr, base, cm="aulc", seeds=[5000, 5001, 5002])
    assert out["effects"]["Cstar"] == pytest.approx((0.6 - 0.3) / 0.6)
    assert out["tier1_gate"]["Cstar"] is True                        # 0.62 - 0.3 >= 2 * 0.05
    tr["Cstar"] = _cres([0.3, 0.3, 0.3], ret=(True, False, False))   # return 1/3 < 2/3 -> effect capped at 0
    out = tier1.score(C(REFERENCES["R1_SGD"]), tr, base, cm="aulc", seeds=[5000, 5001, 5002])
    assert out["effects"]["Cstar"] == 0.0 and out["tier1_gate"]["Cstar"] is False
    assert tier1.effect("Cstar", 12.0, 8.0, "hl") == pytest.approx(4 / 12)   # v7 formula unchanged


# ---------------------------------------------------------------------------- confirmation funnel
def _base_confirm():
    return {"best_generic": {"Cstar": {"method": "SGD", "metric": 0.6, "seed_metric": [0.6] * 8},
                             "B": {"method": "SGD", "metric": 100.0, "seed_metric": [100.0] * 8, "T2_final_mse": 0.02},
                             "F": {"method": "SGD", "metric": 0.8, "seed_metric": [0.8] * 8}},
            "adamw": {"Cstar": {"mean": 0.62, "sd": 0.02}, "B": {"mean": 100.0, "sd": 1e-9}, "F": {"mean": 0.8, "sd": 0.01}}}


def _s(metric_seeds, ret=8):
    return {"stable": True, "seed_metric": metric_seeds, "metric": float(np.mean(metric_seeds)), "return_ok_count": ret}


def test_confirmation_eligibility_rules():
    b = _base_confirm()
    good = CF.assess("Cstar", _s([0.2] * 8), b, 0.01)
    assert good["eligible"] and good["q_confirm"] == pytest.approx((0.6 - 0.2) / 0.6 - 0.01) and good["paired_wins"] == 8
    assert not CF.assess("Cstar", _s([0.2] * 5 + [0.9] * 3), b, 0.01)["eligible"]            # 5/8 wins
    assert not CF.assess("Cstar", _s([0.2] * 8, ret=5), b, 0.01)["eligible"]                 # return 5/8
    assert CF.assess("Cstar", _s([0.2] * 8, ret=6), b, 0.01)["eligible"]                     # return 6/8 ok
    assert not CF.assess("Cstar", _s([0.55] * 8), b, 0.01)["eligible"]                       # q < 0.15
    assert not CF.assess("Cstar", _s([0.2] * 8), b, 0.6)["eligible"]                         # penalty -> q < 0.15
    b2 = _base_confirm(); b2["adamw"]["Cstar"]["sd"] = 0.3
    assert not CF.assess("Cstar", _s([0.2] * 8), b2, 0.01)["eligible"]                       # AdamW 2 SD gate
    assert not CF.assess("Cstar", {"stable": False}, b, 0.01)["eligible"]
    bB = CF.assess("B", {**_s([40.0] * 8), "T2_final_mse": 0.024}, b, 0.0)
    assert bB["eligible"] and bB["constraint_ok"]
    assert not CF.assess("B", {**_s([40.0] * 8), "T2_final_mse": 0.5}, b, 0.0)["eligible"]   # T2 constraint


def test_confirmation_selection_order_and_caps():
    cands = [{"pid": f"P{i:05d}", "task": "Cstar", "eligible": True, "q_confirm": 0.2 + 0.01 * i, "family_sim": 0.5}
             for i in range(12)]
    cands += [{"pid": "PB", "task": "B", "eligible": True, "q_confirm": 0.9, "family_sim": 0.5},
              {"pid": "PX", "task": "F", "eligible": False, "q_confirm": 5.0, "family_sim": 0.5}]
    sel = CF.select(cands)
    assert [c["pid"] for c in sel][0] == "PB" and len([c for c in sel if c["task"] == "Cstar"]) == 8
    assert all(c["eligible"] for c in sel) and "PX" not in [c["pid"] for c in sel]
    qs = [c["q_confirm"] for c in sel]
    assert qs == sorted(qs, reverse=True)


# ---------------------------------------------------------------------------- Stage-3 v8 profile
def test_stage3_v8_profile_uses_aulc_and_kf(monkeypatch):
    S3.configure("v8")
    try:
        assert S3.STAGE3_SEEDS == list(range(30000, 30010)) and S3.CM == "aulc" and S3.GATE4_REF == "KF"
        assert S3.event_steps("Cstar") == {256, 320, 384}
        assert S3.nearest_family_program("R1_SGD") == canon(__import__("ams.families", fromlist=["REFERENCES"]).REFERENCES["R1_SGD"])
        st = lambda m, **k: {"stable": True, "metric": float(np.mean(m)), "seed_metric": list(m), "return_ok_count": 10,
                             "R0_pre_shift": 0.05, "hl_censored_seeds": [12.0] * 10, **k}
        S = {"P": st([0.2] * 10), "SGD": st([0.6] * 10), "SGDM": st([0.7] * 10), "AdamW": st([0.65] * 10),
             "K": {"stable": False}, "KF": st([0.6] * 10), "A1": st([0.6] * 10), "A5b": st([0.3] * 10),
             "A6": st([0.6] * 10), "A7": st([0.6] * 10)}
        d = S3.pre_decide("Cstar", S, False, 1.0)
        assert d["gate4_reference"] == "KF" and d["threshold_ok"]                 # 0.2 <= 0.5 * 0.6
        assert d["gate4a_K_drops_half"] and d["gate4b_P_beats_K_by_half_tau"]    # evaluated on KF(P)
        S["KF"] = st([0.25] * 10)                                                # KF(P) keeps the effect
        d = S3.pre_decide("Cstar", S, False, 1.0)
        assert not d["gate4a_K_drops_half"]                                      # K(P)=unstable is NOT used
        assert S3.label(d, True) == "REDISCOVERY"
        assert d["diagnostic_half_life_P"] == 12.0
    finally:
        S3.configure("v7")
