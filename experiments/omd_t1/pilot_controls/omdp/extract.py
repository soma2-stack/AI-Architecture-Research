"""Blinded quotient extraction (family L), policy-agnostic.

Input: closed-loop controller trajectories only (event types, anonymized slots, controller local and
global states, scores at evictions, chosen victims, lazy dt). Nothing identifies the planted policy.

Output: a finite local-class automaton
  - classes with ranks (eviction priority; lower rank is evicted first),
  - deterministic hit transitions between classes,
  - an insert class,
  - a recency tie-break direction within equal rank,
plus an abstraction map alpha: controller local state h -> class (nearest written state), a compact
text description, and generated plain-code policy source.
"""
from __future__ import annotations

import collections
import json

import numpy as np
from scipy.spatial import cKDTree

from .config import CONFIG, EVENT_EVICT, EVENT_FILL, EVENT_HIT


# ----------------------------------------------------------------------------- trajectory helpers
def reconstruct(traj, C):
    """Rebuild h_pre (T,C,2) and dt (T,C), resident (T,C) from events and written states."""
    et, sl, hs = traj["etype"], traj["slot"], traj["hs_post"]
    T = len(et)
    h = np.zeros((C, 2), np.float32)
    t_last = np.full(C, -1, np.int64)
    res = np.zeros(C, bool)
    H = np.zeros((T, C, 2), np.float32)
    D = np.zeros((T, C), np.float32)
    R = np.zeros((T, C), bool)
    for t in range(T):
        H[t], R[t] = h, res
        D[t] = np.where(res, t - t_last, 0)
        s = int(sl[t])
        h[s] = hs[t]
        t_last[s] = t
        if et[t] in (EVENT_EVICT, EVENT_FILL):
            res[s] = True
    return H, D, R


def _key(v):
    return np.asarray(v, np.float32).tobytes()


# ----------------------------------------------------------------------------- micro-clusters
def micro_clusters(points, resolution):
    """Grid quantization at `resolution` x robust range per dimension, then union of occupied
    8-neighbour cells. Returns labels, scale."""
    P = np.asarray(points, np.float64)
    lo, hi = np.quantile(P, 0.001, axis=0), np.quantile(P, 0.999, axis=0)
    scale = np.maximum(hi - lo, 1e-6)
    cells = np.floor((P - lo) / (scale * resolution)).astype(np.int64)
    uniq, inv = np.unique(cells, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    index = {tuple(c): i for i, c in enumerate(uniq)}
    parent = list(range(len(uniq)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, c in enumerate(uniq):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                j = index.get((c[0] + dx, c[1] + dy))
                if j is not None:
                    ra, rb = find(i), find(j)
                    if ra != rb:
                        parent[ra] = rb
    roots = np.array([find(i) for i in range(len(uniq))])
    _, lab = np.unique(roots, return_inverse=True)
    return lab[inv], scale


# ----------------------------------------------------------------------------- graph utilities
def _scc(nodes, adj):
    """Iterative Tarjan. adj: dict node -> iterable of nodes. Returns dict node -> component id."""
    index, low, onstack, comp = {}, {}, set(), {}
    stack, counter, cid = [], [0], [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(adj.get(root, ())))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        onstack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onstack.add(w)
                    work.append((w, iter(adj.get(w, ()))))
                    advanced = True
                    break
                elif w in onstack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    onstack.discard(w)
                    comp[w] = cid[0]
                    if w == v:
                        break
                cid[0] += 1
    return comp


def _levels(le, lt, soft=()):
    """le: dict (a,b)->weight for a<=b observations; lt: dict (a,b)->weight for strict a<b.
    Contradictory cycles (a strict edge inside a strongly connected component) are broken by
    removing, per offending component, its lightest internal edges (hard evidence only). Then soft
    strict edges (simplicity prior from hit transitions: a hit moves to a higher rank) are added in
    the given order, skipping any that would contradict the evidence. Returns (level per node,
    removed weight, n_components, n_soft_used) or (None, ...) if contradictions exceed 2%."""
    le, lt = dict(le), dict(lt)
    total = sum(le.values())
    removed = 0
    nodes = sorted({a for a, _ in le} | {b for _, b in le} | {a for a, _ in soft} | {b for _, b in soft})
    for _ in range(500):
        adj = collections.defaultdict(list)
        for (a, b) in le:
            adj[a].append(b)
        comp = _scc(nodes, adj)
        bad_comps = {comp[a] for (a, b) in lt if comp[a] == comp[b]}
        if not bad_comps:
            break
        internal = collections.defaultdict(list)
        for e, w in le.items():
            if comp[e[0]] == comp[e[1]] and comp[e[0]] in bad_comps:
                internal[comp[e[0]]].append((w, e))
        for c, lst in internal.items():
            wmin = min(w for w, _ in lst)
            for w, e in lst:
                if w == wmin:
                    removed += w
                    del le[e]
                    lt.pop(e, None)
        if removed > 0.02 * total:
            return None, removed, 0, 0
    else:
        return None, removed, 0, 0
    adj = collections.defaultdict(list)
    for (a, b) in le:
        adj[a].append(b)
    comp = _scc(nodes, adj)
    ncomp = max(comp.values()) + 1 if comp else 0
    cadj = collections.defaultdict(dict)
    for (a, b) in le:
        ca, cb = comp[a], comp[b]
        if ca != cb:
            cadj[ca][cb] = max(cadj[ca].get(cb, 0), 1 if (a, b) in lt else 0)
    order = _topo(ncomp, cadj)
    reach = [0] * ncomp  # bitset of components reachable from c (excluding c)
    for c in reversed(order):
        r = 0
        for d in cadj.get(c, {}):
            r |= reach[d] | (1 << d)
        reach[c] = r
    used = 0
    for a, b in soft:
        ca, cb = comp[a], comp[b]
        if ca == cb or (reach[cb] >> ca) & 1:
            continue
        if cadj[ca].get(cb) == 1:
            continue
        cadj[ca][cb] = 1
        add = reach[cb] | (1 << cb)
        for u in range(ncomp):
            if u == ca or (reach[u] >> ca) & 1:
                reach[u] |= add
        used += 1
    order = _topo(ncomp, cadj)
    lev = {c: 0 for c in range(ncomp)}
    for c in order:
        for d, w in cadj.get(c, {}).items():
            lev[d] = max(lev[d], lev[c] + w)
    return {n: lev[comp[n]] for n in nodes}, removed, ncomp, used


def _topo(n, cadj):
    indeg = [0] * n
    for c in cadj:
        for d in cadj[c]:
            indeg[d] += 1
    order, q = [], [c for c in range(n) if indeg[c] == 0]
    while q:
        c = q.pop()
        order.append(c)
        for d in cadj.get(c, {}):
            indeg[d] -= 1
            if indeg[d] == 0:
                q.append(d)
    assert len(order) == n, "condensation is not acyclic"
    return order


# ----------------------------------------------------------------------------- extraction
def _observations(trajs, C, mc_of):
    """Ordering observations: list of (mc_a, mc_b, dt_a, dt_b) meaning a is ordered before b."""
    obs = []
    for tr in trajs:
        H, D, R = tr["_H"], tr["_D"], tr["_R"]
        for t in np.where(tr["etype"] == EVENT_EVICT)[0]:
            S = tr["S_ev"][tr["_evpos"][t]]
            dt = D[t]
            order = sorted(range(C), key=lambda s: (S[s], -dt[s], s))
            mcs = [mc_of[_key(H[t, s])] for s in range(C)]
            pairs = [(order[0], j) for j in order[1:]]
            low = order[:4]
            pairs += [(low[i], low[k]) for i in range(1, 4) for k in range(i + 1, 4)]
            for a, b in pairs:
                obs.append((mcs[a], mcs[b], dt[a], dt[b]))
    return obs


def _constraints(obs, direction):
    le, lt = collections.Counter(), collections.Counter()
    same_viol = 0
    for a, b, da, db in obs:
        consistent = (da > db) if direction == "oldest_first" else (da < db)
        if a == b:
            same_viol += 0 if consistent else 1
            continue
        le[(a, b)] += 1
        if not consistent:
            lt[(a, b)] += 1
    return le, lt, same_viol


def extract(trajs, cfg=CONFIG):
    C = cfg["C"]
    ex = cfg["extraction"]
    # 1. written states and micro-clusters
    written, wkeys = [], []
    for tr in trajs:
        H, D, R = reconstruct(tr, C)
        tr["_H"], tr["_D"], tr["_R"] = H, D, R
        evpos = np.full(len(tr["etype"]), -1)
        evidx = np.where(tr["etype"] == EVENT_EVICT)[0]
        evpos[evidx] = np.arange(len(evidx))
        tr["_evpos"] = evpos
        m = np.isin(tr["etype"], [EVENT_HIT, EVENT_EVICT, EVENT_FILL])
        written.append(tr["hs_post"][m])
    W = np.concatenate(written).astype(np.float32)
    Wu, inv = np.unique(W, axis=0, return_inverse=True)
    res = ex["micro_cluster_resolution"]
    lab, scale = micro_clusters(Wu, res)
    while lab.max() + 1 > ex["max_micro_clusters"] and res < 0.1:
        res *= 2.0
        lab, scale = micro_clusters(Wu, res)
    mc_of = {_key(Wu[i]): int(lab[i]) for i in range(len(Wu))}
    n_mc = int(lab.max()) + 1

    # 2. transitions
    succ = collections.defaultdict(collections.Counter)
    ins_c = collections.Counter()
    for tr in trajs:
        H = tr["_H"]
        for t in range(len(tr["etype"])):
            e, s = int(tr["etype"][t]), int(tr["slot"][t])
            post = mc_of[_key(tr["hs_post"][t])]
            if e == EVENT_HIT:
                succ[mc_of[_key(H[t, s])]][post] += 1
            elif e in (EVENT_EVICT, EVENT_FILL):
                ins_c[post] += 1
    modal = {a: c.most_common(1)[0][0] for a, c in succ.items()}
    soft = [(a, b) for w, a, b in sorted(((w, a, b) for a, cnt in succ.items() for b, w in cnt.items()),
                                          key=lambda x: (-x[0], x[1], x[2]))]

    # 3. ordering constraints (hard evidence) + soft hit-transition prior, recency direction
    obs = _observations(trajs, C, mc_of)
    best = None
    for direction in ("oldest_first", "newest_first"):
        le, lt, sv = _constraints(obs, direction)
        lev, removed, ncomp, n_soft = _levels(le, lt, soft)
        if lev is None:
            continue
        viol = removed + sv
        if best is None or viol < best[0]:
            best = (viol, direction, lev, removed, sv, ncomp, n_soft)
    if best is None:
        return _fail("ordering contradictions exceed 2% of observations in both recency directions",
                     None)
    viol, direction, lev, removed, same_viol, ncomp, n_soft = best

    # 4. classes: Moore refinement of levels by successor class, then don't-care merges
    key = {m: (lev[m] if m in lev else "U") for m in range(n_mc)}
    cls = _relabel(key)
    for _ in range(50):
        changed = False
        for _inner in range(50):
            newkey = {m: (cls[m], cls[modal[m]] if m in modal else None) for m in range(n_mc)}
            new = _relabel(newkey)
            if len(set(new.values())) == len(set(cls.values())):
                break
            cls, changed = new, True
        cls, merged = _merge_dont_care(cls, lev, modal, n_mc)
        if not changed and not merged:
            break
    cls = _relabel(cls)
    n_cls = len(set(cls.values()))
    if n_cls > ex["max_classes"]:
        return _fail(f"{n_cls} classes exceed max_classes", locals())

    # class-level tables
    size = collections.Counter(cls[m] for m in range(n_mc))
    class_level = {}
    for m in range(n_mc):
        if m in lev:
            class_level.setdefault(cls[m], collections.Counter())[lev[m]] += 1
    point_class = np.array([cls[int(l)] for l in lab])
    centroid = {c: Wu[point_class == c].mean(0) for c in set(cls.values())}
    rank = {}
    leveled = [c for c in class_level]
    for c in set(cls.values()):
        if c in class_level:
            rank[c] = int(class_level[c].most_common(1)[0][0])
        else:  # never observed at an eviction: rank of the nearest leveled class
            if leveled:
                d = [np.sum(((centroid[c] - centroid[k]) / scale) ** 2) for k in leveled]
                rank[c] = int(class_level[leveled[int(np.argmin(d))]].most_common(1)[0][0])
            else:
                rank[c] = 0
    csucc_counts = collections.defaultdict(collections.Counter)
    for a, cnt in succ.items():
        for b, w in cnt.items():
            csucc_counts[cls[a]][cls[b]] += w
    csucc = {c: cnt.most_common(1)[0][0] for c, cnt in csucc_counts.items()}
    succ_det = {c: cnt.most_common(1)[0][1] / sum(cnt.values()) for c, cnt in csucc_counts.items()}
    ins_counts = collections.Counter()
    for m, w in ins_c.items():
        ins_counts[cls[m]] += w
    insert_class = ins_counts.most_common(1)[0][0]
    insert_det = ins_counts[insert_class] / sum(ins_counts.values())

    rule = {"family": "L", "classes": sorted(int(c) for c in set(cls.values())),
            "rank": {int(c): int(r) for c, r in rank.items()},
            "on_hit": {int(c): int(s) for c, s in csucc.items()},
            "insert_class": int(insert_class), "recency": direction,
            "tie_break": "lower slot index"}
    # 5. validation on the extraction data: extracted rule shadowing the controller trajectories
    agree = []
    for tr in trajs:
        pred, _ = shadow(rule, tr["etype"], tr["slot"], C)
        ev = tr["etype"] == EVENT_EVICT
        agree.append(float(np.mean(pred[ev] == tr["slot"][ev])))
    n_ev = [int((tr["etype"] == EVENT_EVICT).sum()) for tr in trajs]
    pooled = float(np.dot(agree, n_ev) / max(sum(n_ev), 1))
    accepted = pooled >= ex["acceptance_min_agreement"]

    abstraction = {"scale": scale.tolist(), "points": Wu, "point_class": point_class}
    out = {
        "status": "COMPACT RULE" if accepted else "NO COMPACT RULE",
        "rule": rule,
        "description": describe(rule),
        "stats": {"n_written_unique": int(len(Wu)), "n_micro_clusters": n_mc,
                  "micro_cluster_resolution_used": res, "n_classes": n_cls,
                  "n_ordering_observations": len(obs), "ordering_violations_removed": int(removed),
                  "same_cluster_recency_violations": int(same_viol), "n_rank_components": int(ncomp),
                  "n_soft_transition_edges_used": int(n_soft), "n_soft_transition_edges": len(soft),
                  "class_sizes_micro_clusters": {int(c): int(n) for c, n in size.items()},
                  "hit_transition_determinism": {int(c): round(float(v), 6) for c, v in succ_det.items()},
                  "insert_determinism": round(float(insert_det), 6),
                  "validation_agreement_per_stream": agree, "validation_agreement_pooled": pooled},
    }
    return out, abstraction


def _relabel(key):
    ids = {}
    return {m: ids.setdefault(k, len(ids)) for m, k in sorted(key.items(), key=lambda kv: kv[0])}


def _merge_dont_care(cls, lev, modal, n_mc):
    """Merge classes whose differences are unobserved (successor unknown, or no level)."""
    members = collections.defaultdict(list)
    for m in range(n_mc):
        members[cls[m]].append(m)

    def level_of(c):
        ls = {lev[m] for m in members[c] if m in lev}
        return ls.pop() if len(ls) == 1 else (None if not ls else "mixed")

    def succ_of(c):
        ss = {cls[modal[m]] for m in members[c] if m in modal}
        return ss.pop() if len(ss) == 1 else (None if not ss else "mixed")

    info = {c: (level_of(c), succ_of(c), len(members[c])) for c in members}
    target = {}
    by_size = sorted(info, key=lambda c: -info[c][2])
    for c in by_size:
        lc, sc, _ = info[c]
        if c in target:
            continue
        for d in by_size:
            if d == c or d in target or info[d][2] < info[c][2]:
                continue
            ld, sd, _ = info[d]
            lvl_ok = lc is None or (lc == ld and lc != "mixed")
            suc_ok = sc is None or (sc == sd and sc != "mixed")
            if lvl_ok and suc_ok and (lc is None or sc is None):
                target[c] = d
                break
    if not target:
        return cls, False
    return {m: target.get(cls[m], cls[m]) for m in range(n_mc)}, True


def _fail(reason, loc):
    return {"status": "NO COMPACT RULE", "reason": reason, "rule": None, "description": reason,
            "stats": {}}, None


# ----------------------------------------------------------------------------- plain-code semantics
def shadow(rule, etype, slot, C):
    """Run the extracted rule's class tracking along a given trajectory; return (predicted victim at
    each eviction event or -1, classes[T,C] pre-event)."""
    rank, succ = rule["rank"], rule["on_hit"]
    rank = {int(k): v for k, v in rank.items()}
    succ = {int(k): v for k, v in succ.items()}
    ic, old = rule["insert_class"], rule["recency"] == "oldest_first"
    cl = np.full(C, -1, np.int64)
    t_last = np.full(C, -1, np.int64)
    T = len(etype)
    pred = np.full(T, -1, np.int64)
    hist = np.zeros((T, C), np.int64)
    for t in range(T):
        hist[t] = cl
        e, s = int(etype[t]), int(slot[t])
        if e == EVENT_EVICT:
            pred[t] = choose(cl, t_last, t, rank, old)
        if e == EVENT_HIT:
            cl[s] = succ.get(int(cl[s]), int(cl[s]))
        elif e in (EVENT_EVICT, EVENT_FILL):
            cl[s] = ic
        t_last[s] = t
    return pred, hist


def choose(cl, t_last, t, rank, old):
    best, bk = -1, None
    for s in range(len(cl)):
        if cl[s] < 0:
            continue
        dt = t - t_last[s]
        k = (rank[int(cl[s])], -dt if old else dt, s)
        if bk is None or k < bk:
            best, bk = s, k
    return best


def describe(rule):
    classes, rank, succ = rule["classes"], rule["rank"], rule["on_hit"]
    rank = {int(k): v for k, v in rank.items()}
    succ = {int(k): v for k, v in succ.items()}
    rec = "oldest" if rule["recency"] == "oldest_first" else "newest"
    if len(classes) == 1:
        return (f"Single local class: insertion and hits do not change it. Evict the resident with the "
                f"{rec} last access.")
    # chain detection
    path, c, seen = [], rule["insert_class"], set()
    while c not in seen:
        seen.add(c)
        path.append(c)
        c = succ.get(c, c)
    chain = (len(path) == len(classes) and all(rank[path[i]] < rank[path[i + 1]] for i in range(len(path) - 1))
             and succ.get(path[-1], path[-1]) == path[-1])
    if chain:
        return (f"Saturating counter with {len(path)} levels: insertion sets level 0, each hit adds 1 "
                f"up to level {len(path) - 1}. Evict the lowest level; ties by the {rec} last access.")
    tr = ", ".join(f"{c}->{succ.get(c, c)}" for c in classes)
    rk = ", ".join(f"{c}:{rank[c]}" for c in classes)
    return (f"Finite automaton with {len(classes)} local classes; insert -> {rule['insert_class']}; "
            f"hit transitions {tr}; eviction by minimum rank ({rk}), ties by the {rec} last access.")


PLAIN_CODE_TEMPLATE = '''"""Plain-code policy emitted by the blinded OMD-PILOT-1 extractor for controller {codename}.
{description}
No neural network, no controller state: only per-slot class ids and last-access times."""

RANK = {rank}
ON_HIT = {on_hit}
INSERT_CLASS = {insert_class}
OLDEST_FIRST = {oldest}


class ExtractedPolicy:
    name = "extracted_{codename}"

    def reset(self, C):
        self.cls = [-1] * C
        self.t_last = [-1] * C

    def on_insert(self, slot, t):
        self.cls[slot] = INSERT_CLASS
        self.t_last[slot] = t

    def on_hit(self, slot, t):
        self.cls[slot] = ON_HIT.get(self.cls[slot], self.cls[slot])
        self.t_last[slot] = t

    def choose(self, t):
        best, bk = -1, None
        for s, c in enumerate(self.cls):
            if c < 0:
                continue
            dt = t - self.t_last[s]
            k = (RANK[c], -dt if OLDEST_FIRST else dt, s)
            if bk is None or k < bk:
                best, bk = s, k
        return best

    def on_evict(self, slot, t):
        self.cls[slot] = -1
'''


def plain_code(rule, codename, description):
    return PLAIN_CODE_TEMPLATE.format(
        codename=codename, description=description,
        rank=json.dumps({int(k): v for k, v in rule["rank"].items()}).replace('"', ""),
        on_hit=json.dumps({int(k): v for k, v in rule["on_hit"].items()}).replace('"', ""),
        insert_class=rule["insert_class"], oldest=rule["recency"] == "oldest_first")


class Alpha:
    """Abstraction map h -> extracted class (nearest written state in scaled coordinates)."""

    def __init__(self, abstraction):
        self.scale = np.asarray(abstraction["scale"], np.float64)
        pts = np.asarray(abstraction["points"], np.float64) / self.scale
        self.tree = cKDTree(pts)
        self.cls = np.asarray(abstraction["point_class"])

    def __call__(self, h):
        h = np.atleast_2d(np.asarray(h, np.float64)) / self.scale
        _, i = self.tree.query(h)
        return self.cls[i]
