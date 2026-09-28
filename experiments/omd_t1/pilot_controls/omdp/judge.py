"""Unblinded judge: compare an extracted family-L automaton with the planted policy's quotient
semantics (criteria J1-J5 in CONFIG['judge']). Run only after extraction outputs are hashed."""
from __future__ import annotations

import collections

import numpy as np

from . import extract as X
from . import teachers
from .config import CONFIG, EVENT_EVICT

MIN_OBS = 20


def judge(extraction, planted, ext_trajs, reqs, teacher_trajs, cfg=CONFIG):
    """ext_trajs: controller closed-loop trajectories used for extraction (etype, slot per stream);
    reqs: the request arrays of those streams; teacher_trajs: teacher runs on the same streams."""
    C = cfg["C"]
    res = {"planted": planted, "criteria": {}, "pass": False}
    if extraction.get("status") != "COMPACT RULE" or extraction.get("rule") is None:
        res["reason"] = "extractor emitted NO COMPACT RULE"
        return res
    spec = teachers.PLANTED_SPEC[planted]
    rule = extraction["rule"]
    rank = {int(k): v for k, v in rule["rank"].items()}
    succ = {int(k): v for k, v in rule["on_hit"].items()}
    if spec["kind"] == "queue_hand":
        res["reason"] = ("planted semantics use an insertion-order queue with a global hand; the "
                         "extracted family-L rule has no relational/pointer state")
        res["criteria"] = {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False}
        return res
    # correspondence counts over resident slots at eviction events of the extraction data
    cont = collections.defaultdict(collections.Counter)
    for tr, req in zip(ext_trajs, reqs):
        _, hist = X.shadow(rule, tr["etype"], tr["slot"], C)
        local, _ = teachers.track(planted, req, C, tr["etype"], tr["slot"])
        ev = np.where(tr["etype"] == EVENT_EVICT)[0]
        for t in ev:
            for s in range(C):
                if hist[t, s] >= 0:
                    cont[int(hist[t, s])][int(local[t, s])] += 1
    mapping, purity = {}, {}
    for c, cnt in cont.items():
        m, n = cnt.most_common(1)[0]
        mapping[c], purity[c] = m, n / sum(cnt.values())
    big = [c for c in cont if sum(cont[c].values()) >= MIN_OBS]
    top = max(rank, key=lambda c: (rank[c], c)) if rank else None
    # J1 purity (LFU: the top class of a saturating chain may hold a count tail >= its minimum)
    j1 = {}
    for c in big:
        if spec["kind"] == "counter" and c == top and succ.get(c, c) == c:
            kmin = mapping[c]
            tail = sum(n for k, n in cont[c].items() if k >= kmin) / sum(cont[c].values())
            j1[c] = tail >= 0.99
        else:
            j1[c] = purity[c] >= 0.99
    # J2 transitions
    j2 = {}
    for c in big:
        if c not in succ or succ[c] not in mapping:
            continue
        a, b = mapping[c], mapping[succ[c]]
        if spec["kind"] == "counter":
            j2[c] = (b == a + 1) or (succ[c] == c and c == top)
        else:
            j2[c] = spec["hit"].get(a) == b
    # J3 ranks consistent with planted order; recency oldest-first
    j3_pairs = []
    for i in big:
        for k in big:
            if i >= k:
                continue
            a, b = mapping[i], mapping[k]
            pr = (spec["rank"][a], spec["rank"][b]) if spec["kind"] == "classes" else (a, b)
            if pr[0] == pr[1]:
                ok = rank[i] == rank[k] or (spec["kind"] == "counter" and top in (i, k))
            else:
                ok = (rank[i] < rank[k]) == (pr[0] < pr[1])
            j3_pairs.append(ok)
    j3 = all(j3_pairs) and rule["recency"] == spec["recency"]
    # J4 insertion
    j4 = mapping.get(rule["insert_class"]) == spec["insert"]
    # J5 behaviour along the teacher's own trajectories
    agree, n = 0, 0
    for tt in teacher_trajs:
        pred, _ = X.shadow(rule, tt["etype"], tt["slot"], C)
        ev = tt["etype"] == EVENT_EVICT
        agree += int(np.sum(pred[ev] == tt["slot"][ev]))
        n += int(ev.sum())
    j5v = agree / max(n, 1)
    res["criteria"] = {"J1": bool(all(j1.values())), "J2": bool(all(j2.values())), "J3": bool(j3),
                       "J4": bool(j4), "J5": bool(j5v >= 0.995)}
    res["detail"] = {"mapping": {int(k): int(v) for k, v in mapping.items()},
                     "purity": {int(k): round(float(v), 6) for k, v in purity.items()},
                     "class_obs": {int(c): int(sum(cont[c].values())) for c in cont},
                     "J1_per_class": {int(k): bool(v) for k, v in j1.items()},
                     "J2_per_class": {int(k): bool(v) for k, v in j2.items()},
                     "J3_pairs_checked": len(j3_pairs), "J5_teacher_agreement": j5v,
                     "J5_evictions": n}
    res["pass"] = all(res["criteria"].values())
    if not res["pass"]:
        res["reason"] = "failed " + ",".join(k for k, v in res["criteria"].items() if not v)
    return res
