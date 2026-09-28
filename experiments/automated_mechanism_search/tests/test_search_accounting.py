"""Generator/mutation validity, MAP-Elites archive and budgets with stub evaluators,
CPU ledger / cap, manifest immutability, result serialization, leakage guard."""
import json
import random

import numpy as np
import pytest

from ams import accounting, manifest
from ams.canon import canon
from ams.families import FamilyLibrary
from ams.fingerprint import COUPLING_SUBSETS, CREDIT_CLASSES
from ams.generate import Gen, valid
from ams.grammar import program_from_dict, program_to_dict, serialize
from ams.search import N_CELLS, Pipeline, Record, map_elites, select_promotions


def test_56_cells():
    assert N_CELLS == 56 and len(COUPLING_SUBSETS) == 7 and len(CREDIT_CLASSES) == 4


def test_random_programs_mostly_valid_and_typed():
    g = Gen(random.Random(0))
    progs = [g.program() for _ in range(300)]
    ok = [p for p in progs if valid(p) is None]
    assert len(ok) >= 100
    for p in ok[:50]:
        assert serialize(program_from_dict(program_to_dict(p))) == serialize(p)


def test_mutation_and_crossover_produce_valid_programs():
    g = Gen(random.Random(1))
    base = [p for p in (g.program() for _ in range(200)) if valid(p) is None][:20]
    n_valid = 0
    n = 0
    for p in base:
        for _ in range(10):
            c = g.mutate(p) if random.random() < 0.8 else g.crossover(p, random.choice(base))
            n += 1
            n_valid += valid(c) is None
    assert n_valid / n > 0.3


class StubEval:
    def __init__(self, seed=0):
        self.r = random.Random(seed)
        self.calls = 0

    def sanity(self, p):
        return {"pass": True}

    def tier1(self, p):
        self.calls += 1
        q = self.r.uniform(-0.5, 0.6)
        return {"q": q, "best_task": self.r.choice(["B", "Cstar", "F"]), "tier1_pass_on_best": q > 0.2}


@pytest.fixture(scope="module")
def lib():
    return FamilyLibrary()


def test_pipeline_and_archive_with_stub(lib, monkeypatch):
    import ams.search as S
    monkeypatch.setattr(S, "N_INIT", 15)
    monkeypatch.setattr(S, "OFFSPRING", 5)
    monkeypatch.setattr(S, "G_MAX", 3)
    ev = StubEval()
    logs = []
    pipe = Pipeline(lib, ev.sanity, ev.tier1, log=logs.append)
    out = map_elites(pipe, random.Random(3))
    c = pipe.counts
    assert c["tier1_evaluated"] == ev.calls
    assert c["tier1_evaluated"] <= 15 + 3 * 5
    total = sum(v for k, v in c.items() if k not in ("generated", "sanity_evaluated", "tier1_evaluated", "tier1_unstable", "tier1_error"))
    assert c["generated"] >= len(logs)
    # every archive entry has a descriptor matching its cell and is the best in its cell
    for cell, rec in pipe.archive.items():
        assert tuple(rec.descriptor) == cell
        same = [r for r in pipe.records if r.quality is not None and r.descriptor is not None and tuple(r.descriptor) == cell]
        assert rec.quality == max(r.quality for r in same)
    promo = select_promotions(pipe)
    assert len(promo) <= 20 and all(r.quality >= 0.15 for r in promo)
    assert len({tuple(r.descriptor) for r in promo}) == len(promo)
    for r in pipe.records[:30]:
        json.loads(r.to_json())
    assert out["stop"] in ("G_MAX", "PATIENCE", "N_GEN_MAX", "N_SANITY_MAX", "N_TIER1_MAX")


def test_generation_budget_cap(lib, monkeypatch):
    import ams.search as S
    monkeypatch.setattr(S, "N_GEN_MAX", 40)
    ev = StubEval()
    pipe = Pipeline(lib, ev.sanity, ev.tier1)
    out = map_elites(pipe, random.Random(5))
    assert pipe.counts["generated"] <= 40 and out["stop"] == "N_GEN_MAX"


def test_cpu_ledger_and_cap(tmp_path):
    p = str(tmp_path / "ledger.json")
    led = accounting.record("test", 100.0, 50.0, path=p)
    assert led["total_cpu_seconds"] == 100.0
    accounting.check_cap(0.0, path=p)
    with pytest.raises(accounting.CPUCapExceeded):
        accounting.check_cap(30 * 3600.0, path=p)


def test_config_immutable(tmp_path):
    p = str(tmp_path / "cfg.json")
    h = manifest.write_or_verify_config(p)
    assert manifest.write_or_verify_config(p) == h
    d = json.load(open(p))
    d["config"]["lr_grid"] = [0.3]
    json.dump(d, open(p, "w"))
    with pytest.raises(RuntimeError):
        manifest.write_or_verify_config(p)


def test_v6_config_markers():
    from ams import PROTOCOL_VERSION
    from ams.runners import ORACLE_UPDATES, V5_ORACLE_UPDATES
    assert PROTOCOL_VERSION == "AMS-prereg-v6"
    c = manifest.RUN_CONFIG
    assert c["protocol"] == "AMS-prereg-v6" and c["substrate"]["init"] == "glorot_normal"
    g = c["taskB_stage0_gate_v3"]                                           # v3 Stage-0 gate carries forward
    assert g["seed_mean_cos_lt"] == 0.0 and g["frac_pairs_negative_min"] == 0.90 and g["pairs_per_seed"] == 64
    s1 = c["stage1_v5"]
    assert s1["M2_v4_fit_reduction_min"] == 0.95 and s1["V1_B_REP"]["rel_err_reduction_min"] == 0.95
    assert s1["V1_B_REP"]["updates"] == 4000 and s1["V1_B_REP"]["batch"] == [16, 16] and s1["V1_B_REP"]["final"]
    assert s1["V1_B_REP"]["optimizers"] == ["SGD", "SGDM", "AdamW"]
    assert set(s1["diagnostic_only"]) == {"V1_B", "V2_Cstar"} and "V1_B_REP" in s1["mandatory"]
    assert V5_ORACLE_UPDATES == 4000 and ORACLE_UPDATES == 1000             # v4 script behaviour preserved
    assert manifest.CONFIG.endswith("run_config_v6.json")
    assert c["lr_grid"] == [1e-3, 1e-2, 1e-1] and c["seeds"]["stage1"] == [100, 101, 102, 103, 104]
    v6 = c["stage2_v6"]                                                     # v6 changes only the initial constructor
    assert v6["search_seed"] == 2026092806 and v6["max_construction_attempts"] == 10
    assert v6["decays"] == [0.5, 0.9, 0.99] and v6["expr_depths"] == [1, 2] and v6["C3_thetas"] == [0.0, 0.1, 0.5]
    assert v6["static_validation"]["seed"] not in (2026092806, 20260928)
    assert c["budget"]["generated"] == 6000 and c["budget"]["tier1"] == 1200 and c["budget"]["promoted"] == 20
    assert c["thresholds"]["B_forgetting_pp"] == 40 and c["thresholds"]["C_hl_reduction"] == 0.5


def test_v5_config_record_unchanged():
    import hashlib
    d = json.load(open(manifest.CONFIG_V5))
    assert d["config"]["protocol"] == "AMS-prereg-v5" and "stage2_v6" not in d["config"]
    assert hashlib.sha256(json.dumps(d["config"], sort_keys=True).encode()).hexdigest() == d["sha256"]
    v5, v6 = dict(d["config"]), dict(manifest.RUN_CONFIG)
    v5.pop("protocol"), v6.pop("protocol"), v6.pop("stage2_v6")
    assert v5 == v6                                                         # nothing else changed in v6


def test_stage1_v5_script_uses_4000_updates():
    import os
    src = open(os.path.join(os.path.dirname(manifest.CONFIG), "..", "scripts", "stage1_v5.py")).read()
    assert '{"kwargs": {"updates": V5_ORACLE_UPDATES}} if t == "Bjoint"' in src
    assert 'OUT = os.path.join(HERE, "runs", "stage1_v5")' in src


def test_v4_config_record_unchanged():
    import hashlib
    d = json.load(open(manifest.CONFIG_V4))
    assert d["config"]["protocol"] == "AMS-prereg-v4" and d["config"]["stage1_v4"]["V1_B_REP"]["updates"] == 1000
    assert hashlib.sha256(json.dumps(d["config"], sort_keys=True).encode()).hexdigest() == d["sha256"]


def test_v3_config_record_unchanged():
    import hashlib
    d = json.load(open(manifest.CONFIG_V3))
    assert d["config"]["protocol"] == "AMS-prereg-v3"
    assert hashlib.sha256(json.dumps(d["config"], sort_keys=True).encode()).hexdigest() == d["sha256"]


def test_v2_config_record_unchanged():
    import hashlib, os
    d = json.load(open(manifest.CONFIG_V2))
    assert d["config"]["protocol"] == "AMS-prereg-v2"
    assert hashlib.sha256(json.dumps(d["config"], sort_keys=True).encode()).hexdigest() == d["sha256"]


def test_seed_sets_disjoint_no_confirmation_leakage():
    s = manifest.RUN_CONFIG["seeds"]
    sets = [set(v) for v in s.values()]
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            assert not (sets[i] & sets[j])
    assert max(s["tier1"] + s["stage1"] + s["sanity"]) < min(s["stage3"] + s["tier3"])
