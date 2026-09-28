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


def test_seed_sets_disjoint_no_confirmation_leakage():
    s = manifest.RUN_CONFIG["seeds"]
    sets = [set(v) for v in s.values()]
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            assert not (sets[i] & sets[j])
    assert max(s["tier1"] + s["stage1"] + s["sanity"]) < min(s["stage3"] + s["tier3"])
