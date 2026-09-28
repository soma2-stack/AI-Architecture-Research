"""Collision pipeline (D-COLL-1), MAP-Elites archive (AE.3.2) and the frozen search loop
(AE.3.4 with prereg v2 budgets).  Evaluators are injected so the machinery is unit-testable
without running benchmarks."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from .canon import canon, struct_hash
from .families import FamilyLibrary
from .fingerprint import COUPLING_SUBSETS, CREDIT_CLASSES, Analysis, fingerprint
from .generate import MAX_RETRY, P_CROSS, Gen, valid
from .grammar import GrammarError, Program, program_to_dict, serialize
from .probes import DuplicateIndex, finite

N_GEN_MAX = 6000
N_SANITY_MAX = 3000
N_TIER1_MAX = 1200
N_PROMOTE_MAX = 20
N_INIT = 200
OFFSPRING = 50
G_MAX = 20
PATIENCE = 5
ELITE_GAIN = 0.02
Q_MIN = 0.15
PER_TASK_MAX = 8
N_CELLS = len(COUPLING_SUBSETS) * len(CREDIT_CLASSES) * 2   # 56


class BudgetExhausted(Exception):
    pass


@dataclass
class Record:
    pid: str
    raw: dict
    label: str
    canonical: Optional[dict] = None
    struct_hash: Optional[str] = None
    beta_hash: Optional[str] = None
    fingerprint: Optional[dict] = None
    descriptor: Optional[Tuple[int, int, int]] = None
    family: Optional[dict] = None
    detail: Optional[dict] = None
    quality: Optional[float] = None
    tier1: Optional[dict] = None

    def to_json(self) -> str:
        d = dict(self.__dict__)
        return json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))


class Pipeline:
    """try_add of AE.3.4 with the v2 sec. 12 rejection wording."""

    def __init__(self, library: FamilyLibrary, sanity: Callable[[Program], Dict],
                 tier1: Callable[[Program], Dict], log: Optional[Callable[[Record], None]] = None):
        self.lib = library
        self.runner = library.runner
        self.sanity = sanity
        self.tier1 = tier1
        self.dups = DuplicateIndex()
        self.hashes: Dict[str, str] = {}
        self.log = log or (lambda r: None)
        self.counts = {"generated": 0, "invalid": 0, "dup_syntactic": 0, "dup_behavioral": 0,
                       "probe_nonfinite": 0, "pure_rule": 0, "no_signal": 0, "REDISCOVERY": 0,
                       "REDISCOVERY_inert": 0, "sanity_evaluated": 0, "sanity_fail": 0,
                       "tier1_evaluated": 0, "tier1_unstable": 0, "tier1_error": 0}
        self.rediscovery_by_family: Dict[str, int] = {}
        self.archive: Dict[Tuple[int, int, int], Record] = {}
        self.records: List[Record] = []

    def _emit(self, rec: Record):
        self.records.append(rec)
        self.log(rec)

    def try_add(self, raw: Program) -> Optional[Record]:
        if self.counts["generated"] >= N_GEN_MAX:
            raise BudgetExhausted("N_GEN_MAX")
        self.counts["generated"] += 1
        pid = f"P{self.counts['generated']:05d}"
        rawd = program_to_dict(raw)
        code = valid(raw)
        if code is not None:
            self.counts["invalid"] += 1
            self._emit(Record(pid, rawd, "invalid", detail={"code": code}))
            return None
        c = canon(raw)
        h = struct_hash(c)
        cd = program_to_dict(c)
        if h in self.hashes:
            self.counts["dup_syntactic"] += 1
            self._emit(Record(pid, rawd, "dup_syntactic", cd, h, detail={"of": self.hashes[h]}))
            return None
        b = self.runner.beta(c)
        if not finite(b):
            self.counts["probe_nonfinite"] += 1
            self._emit(Record(pid, rawd, "probe_nonfinite", cd, h))
            return None
        bh = DuplicateIndex.exact_key(b)
        d = self.dups.find(b)
        if d is not None:
            self.counts["dup_behavioral"] += 1
            self._emit(Record(pid, rawd, "dup_behavioral", cd, h, bh, detail={"of": d[0], "cos": d[1], "how": d[2]}))
            self.hashes[h] = d[0]
            return None
        self.hashes[h] = pid
        self.dups.add(pid, b)
        fp = fingerprint(c)
        if not fp["couplings"]:
            self.counts["pure_rule"] += 1
            fam = self.lib.nearest(c)
            self._emit(Record(pid, rawd, "pure_rule", cd, h, bh, fp, family=fam))
            return None
        if not fp["learning_signal"]:
            self.counts["no_signal"] += 1
            self._emit(Record(pid, rawd, "no_signal", cd, h, bh, fp))
            return None
        b_all = self.runner.beta_all(c)
        fam = self.lib.match(c, b_all)
        k, kinfo = self.lib.decompose(c)
        residual = struct_hash(k) != h
        if fam is not None and not residual:
            self.counts["REDISCOVERY"] += 1
            self.rediscovery_by_family[fam["family"]] = self.rediscovery_by_family.get(fam["family"], 0) + 1
            self._emit(Record(pid, rawd, "REDISCOVERY", cd, h, bh, fp, fp["descriptor"], fam))
            return None
        if not residual:
            # every term is a known-family term (composite of families)
            self.counts["REDISCOVERY"] += 1
            self.rediscovery_by_family["composite"] = self.rediscovery_by_family.get("composite", 0) + 1
            self._emit(Record(pid, rawd, "REDISCOVERY", cd, h, bh, fp, fp["descriptor"],
                              {"family": "composite", "how": "K(P)=P"}))
            return None
        bk = self.runner.beta(k)
        from .probes import cos
        sim_k = cos(b, bk)
        if sim_k >= 0.99:
            self.counts["REDISCOVERY_inert"] += 1
            self._emit(Record(pid, rawd, "REDISCOVERY_inert", cd, h, bh, fp, fp["descriptor"],
                              fam or self.lib.nearest(c, b_all), detail={"cos_P_KP": sim_k, "K": program_to_dict(k)}))
            return None
        if self.counts["sanity_evaluated"] >= N_SANITY_MAX:
            raise BudgetExhausted("N_SANITY_MAX")
        self.counts["sanity_evaluated"] += 1
        s = self.sanity(c)
        if not s.get("pass"):
            self.counts["sanity_fail"] += 1
            self._emit(Record(pid, rawd, "sanity_fail", cd, h, bh, fp, fp["descriptor"],
                              self.lib.nearest(c, b_all), detail=s))
            return None
        if self.counts["tier1_evaluated"] >= N_TIER1_MAX:
            raise BudgetExhausted("N_TIER1_MAX")
        self.counts["tier1_evaluated"] += 1
        t1 = self.tier1(c)
        q = t1.get("q")
        label = "TIER1_EVALUATED"
        if t1.get("error"):
            self.counts["tier1_error"] += 1
            label = "tier1_error"
        elif q is None:
            self.counts["tier1_unstable"] += 1
            label = "tier1_unstable"
        rec = Record(pid, rawd, label, cd, h, bh, fp, fp["descriptor"], self.lib.nearest(c, b_all),
                     detail={"K": program_to_dict(k), "K_info": kinfo, "cos_P_KP": sim_k}, quality=q, tier1=t1)
        rec.raw_program = raw  # type: ignore[attr-defined]
        self._emit(rec)
        if q is not None:
            cell = tuple(fp["descriptor"])
            cur = self.archive.get(cell)
            if cur is None or q > cur.quality:
                self.archive[cell] = rec
        return rec


def map_elites(pipe: Pipeline, rng: random.Random, progress: Optional[Callable[[str], None]] = None) -> Dict:
    """AE.3.4 loop.  Returns stop reason and per-generation stats."""
    gen = Gen(rng)
    stats = []
    progress = progress or (lambda s: None)
    try:
        while pipe.counts["tier1_evaluated"] < N_INIT:
            pipe.try_add(gen.program())
        progress(f"init done: {pipe.counts}")
        stale = 0
        for g in range(1, G_MAX + 1):
            before_cells = set(pipe.archive)
            before_q = {k: v.quality for k, v in pipe.archive.items()}
            target = pipe.counts["tier1_evaluated"] + OFFSPRING
            while pipe.counts["tier1_evaluated"] < target:
                if not pipe.archive:
                    pipe.try_add(gen.program())
                    continue
                elites = list(pipe.archive.values())
                A = rng.choice(elites)
                for _ in range(MAX_RETRY):
                    if rng.random() < P_CROSS:
                        child = gen.crossover(A.raw_program, rng.choice(elites).raw_program)
                    else:
                        child = gen.mutate(A.raw_program)
                    if valid(child) is None:
                        break
                    pipe.counts["generated"] += 1          # invalid retries count as generated
                    pipe.counts["invalid"] += 1
                    if pipe.counts["generated"] >= N_GEN_MAX:
                        raise BudgetExhausted("N_GEN_MAX")
                pipe.try_add(child)
            new_cells = set(pipe.archive) - before_cells
            gain = max([pipe.archive[k].quality - before_q.get(k, -np.inf) for k in pipe.archive
                        if k in before_q] + [0.0])
            stats.append({"generation": g, "new_cells": len(new_cells), "max_elite_gain": gain,
                          "occupied": len(pipe.archive), "counts": dict(pipe.counts)})
            progress(f"gen {g}: {stats[-1]}")
            stale = 0 if (new_cells or gain >= ELITE_GAIN) else stale + 1
            if stale >= PATIENCE:
                return {"stop": "PATIENCE", "generations": stats}
        return {"stop": "G_MAX", "generations": stats}
    except BudgetExhausted as e:
        return {"stop": str(e), "generations": stats}


def select_promotions(pipe: Pipeline) -> List[Record]:
    """AE.5.6 / D-S2-4."""
    elig = [r for r in pipe.archive.values()
            if r.quality is not None and r.quality >= Q_MIN and r.tier1.get("tier1_pass_on_best")]
    elig.sort(key=lambda r: (-r.quality, r.family["sim"] if r.family else 0.0))
    out, per_task = [], {}
    for r in elig:
        t = r.tier1["best_task"]
        if per_task.get(t, 0) >= PER_TASK_MAX:
            continue
        out.append(r)
        per_task[t] = per_task.get(t, 0) + 1
        if len(out) >= N_PROMOTE_MAX:
            break
    return out
