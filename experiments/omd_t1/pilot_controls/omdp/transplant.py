"""Phase C — autonomous plain-code transplant vs the neural controller and the teacher."""
from __future__ import annotations

import importlib.util

import numpy as np

from . import teachers
from .config import CONFIG, EVENT_EVICT, EVENT_FILL, EVENT_HIT
from .streams import stationary_mask


def load_plain_code(path):
    spec = importlib.util.spec_from_file_location("extracted_policy_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ExtractedPolicy


class _Adapter(teachers.Policy):
    """Drive an emitted plain-code policy through the shared simulator."""

    def __init__(self, cls):
        self.inner = cls()

    def reset(self, C):
        super().reset(C)
        self.inner.reset(C)

    def on_insert(self, slot, t):
        super().on_insert(slot, t)
        self.inner.on_insert(slot, t)

    def on_hit(self, slot, t):
        super().on_hit(slot, t)
        self.inner.on_hit(slot, t)

    def choose(self, t):
        return self.inner.choose(t)

    def on_evict(self, slot, t):
        self.inner.on_evict(slot, t)
        super().on_evict(slot, t)


def run_policy(pol, req, C):
    pol.reset(C)
    return teachers._run(req, C, lambda t: pol.choose(t), pol, record_local=False)


def shadow_policy(pol, etype, slot, C):
    """The plain-code policy's own choice at each eviction of a foreign trajectory."""
    pol.reset(C)
    own = np.full(len(etype), -1, np.int64)
    for t in range(len(etype)):
        e, s = int(etype[t]), int(slot[t])
        if e == EVENT_HIT:
            pol.on_hit(s, t)
        else:
            if e == EVENT_EVICT:
                own[t] = pol.choose(t)
                pol.on_evict(s, t)
            pol.on_insert(s, t)
    return own


class RandomEvict(teachers.Policy):
    name = "RANDOM"

    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)

    def choose(self, t):
        return int(self.rng.choice(np.where(self.resident)[0]))


def _segment_windows(segs, T, after=256):
    wins = []
    for s in segs:
        if s["type"] in ("scan", "loop"):
            wins.append((s["type"], s["start"], s["end"]))
            wins.append((s["type"] + "_after", s["end"], min(T, s["end"] + after)))
    return [w for w in wins if w[2] > w[1]]


def phase_c(ctrl, plain_cls, planted, req, segs, seed, cfg=CONFIG):
    C = cfg["C"]
    g = cfg["gates"]
    T = len(req)
    trans = run_policy(_Adapter(plain_cls), req, C)
    neural = ctrl.cl(req)
    teacher = teachers.simulate(planted, req, C, record_local=False)
    rnd = run_policy(RandomEvict(seed + 7000), req, C)
    # agreement: neural shadows the transplant's autonomous trajectory
    sh = ctrl.tf(trans["etype"], trans["slot"], trans["dt"], trans["resident"])
    ev = trans["etype"] == EVENT_EVICT
    agree = sh["victim"][ev] == trans["slot"][ev]
    stat = stationary_mask(segs, T)[ev]
    # reverse diagnostic: transplant shadows the neural autonomous trajectory
    own = shadow_policy(_Adapter(plain_cls), neural["etype"], neural["slot"], C)
    nev = neural["etype"] == EVENT_EVICT
    rev = float(np.mean(own[nev] == neural["slot"][nev]))
    hT, hN, hTe, hR = int(trans["hits"]), int(neural["is_hit"].sum()), int(teacher["hits"]), int(rnd["hits"])
    rel = abs(hT - hN) / max(hN, 1)
    gapN, gapT = hTe - hN, hTe - hT
    gap_ratio = None if gapN == 0 else gapT / gapN
    closure = (lambda h: None if hTe == hR else (h - hR) / (hTe - hR))
    # edge cases
    hit_T = trans["etype"] == EVENT_HIT
    hit_N = np.asarray(neural["is_hit"], bool)
    hit_Te = teacher["etype"] == EVENT_HIT
    edges = []
    for kind, a, b in _segment_windows(segs, T):
        rT, rN, rTe = hit_T[a:b].mean(), hit_N[a:b].mean(), hit_Te[a:b].mean()
        edges.append({"kind": kind, "start": a, "end": b, "transplant": float(rT), "neural": float(rN),
                      "teacher": float(rTe), "ok": bool(rT >= min(rN, rTe) - 0.05)})
    summ = {
        "evictions": int(ev.sum()), "overall_agreement": float(agree.mean()),
        "stationary_agreement": float(agree[stat].mean()) if stat.any() else None,
        "reverse_agreement_diagnostic": rev,
        "hits": {"transplant": hT, "neural": hN, "teacher": hTe, "random": hR},
        "rel_hit_diff": rel, "gap_neural": gapN, "gap_transplant": gapT, "gap_ratio": gap_ratio,
        "closure_vs_random_diagnostic": {"neural": closure(hN), "transplant": closure(hT)},
        "edge_windows": len(edges), "edge_failures": [e for e in edges if not e["ok"]],
        "scoring_work_O_C_per_eviction": C,
    }
    crit = {
        "overall_agreement": summ["overall_agreement"] >= g["phaseC_overall_agreement_min"],
        "stationary_agreement": summ["stationary_agreement"] is not None
        and summ["stationary_agreement"] >= g["phaseC_stationary_agreement_min"],
        "rel_hit_diff": rel <= g["phaseC_rel_hit_diff_max"],
        "gap_reproduction": gap_ratio is None or gap_ratio >= g["phaseC_gap_reproduction_min"],
        "edge_cases": not summ["edge_failures"],
    }
    summ["criteria"] = crit
    summ["pass"] = all(crit.values())
    decisions = {"transplant_etype": trans["etype"], "transplant_slot": trans["slot"],
                 "neural_shadow_victim": np.asarray(sh["victim"]).astype(np.int16),
                 "neural_etype": neural["etype"], "neural_slot": neural["slot"],
                 "teacher_etype": teacher["etype"], "teacher_slot": teacher["slot"]}
    return summ, decisions
