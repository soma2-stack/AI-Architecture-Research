"""Phase B — causal intervention tests on reachable states of the neural controller."""
from __future__ import annotations

import numpy as np
from scipy.stats import fisher_exact

from . import extract as X
from . import teachers
from .config import CONFIG, EVENT_EVICT, EVENT_HIT
from .controller import np_choose


def _bits(a):
    return np.asarray(a, np.float32).view(np.uint32)


def _order(S, dt, a, b):
    """True if a is ordered (evicted) before b under the neural tie-break."""
    return (S[a], -dt[a], a) < (S[b], -dt[b], b)


def _ext_choose(rule, cl, t_last, t):
    rank = {int(k): v for k, v in rule["rank"].items()}
    return X.choose(cl, t_last, t, rank, rule["recency"] == "oldest_first")


def _ext_succ(rule, c):
    succ = {int(k): v for k, v in rule["on_hit"].items()}
    return succ.get(int(c), int(c))


# ---- planted policy snapshots and local-state swaps
_LOCAL_ATTR = {"LRU": None, "LFU": "count", "TWOQ": "tier", "SIEVE": "visited"}


def planted_snapshots(planted, req, C, etype, slot, times):
    pol = teachers.make(planted)
    pol.reset(C)
    want = set(int(t) for t in times)
    snaps = {}
    for t in range(len(etype)):
        if t in want:
            snaps[t] = teachers._snapshot(pol)
        e, s = int(etype[t]), int(slot[t])
        if e == EVENT_HIT:
            pol.on_hit(s, t)
        elif e == EVENT_EVICT:
            pol.on_forced_evict(s, t)
            pol.on_insert(s, t)
        else:
            pol.on_insert(s, t)
    return snaps


def planted_pair_order(planted, snap, C, a, b, t, swap):
    """True if the planted policy would evict a before b from this state (no further requests)."""
    pol = teachers.make(planted)
    pol.reset(C)
    teachers._restore(pol, snap)
    attr = _LOCAL_ATTR[planted]
    if swap and attr is not None:
        arr = getattr(pol, attr)
        arr[a], arr[b] = arr[b], arr[a]
    for _ in range(C):
        v = pol.choose(t)
        if v in (a, b):
            return v == a
        pol.on_evict(v, t)
    raise RuntimeError("pair not evicted")


def phase_b(ctrl, rule, alpha, planted, req, seed, cfg=CONFIG):
    C = cfg["C"]
    M = cfg["phaseB"]["states_per_pair"]
    rng = np.random.default_rng(seed)
    out = ctrl.cl(req)
    et, sl, S_all, D, R = out["etype"], out["slot"].astype(int), out["S"], out["dt"], out["resident"]
    Hpre, Gpre = out["h_pre"], out["g_pre"]
    _, hist = X.shadow(rule, et, sl, C)
    ev_idx = np.where(et == EVENT_EVICT)[0]
    samp = np.sort(rng.choice(ev_idx, size=min(M, len(ev_idx)), replace=False))
    snaps = planted_snapshots(planted, req, C, et, sl, samp)
    rec = {"B1": [], "B2": [], "B3": [], "B4_tie": [], "B5": []}

    for t in samp:
        h, g, dt, res = Hpre[t].copy(), Gpre[t].copy(), D[t].copy(), R[t].copy()
        cl = hist[t].copy()
        t_last = (t - dt).astype(np.int64)
        S = ctrl.score(h, g, dt)
        v = np_choose(S, dt, res)
        order = sorted(range(C), key=lambda s: (S[s], -dt[s], s))
        # B1 permutation equivariance (neural bitwise; extracted exact)
        pi = rng.permutation(C)
        Sp = ctrl.score(h[pi], g, dt[pi])
        vp = np_choose(Sp, dt[pi], res[pi])
        ve = _ext_choose(rule, cl, t_last, t)
        vpe = _ext_choose(rule, cl[pi], t_last[pi], t)
        rec["B1"].append({"t": int(t), "scores_bitwise": bool(np.array_equal(_bits(Sp), _bits(S[pi]))),
                          "neural_victim": bool(pi[vp] == v), "extracted_victim": bool(pi[vpe] == ve)})
        # B2 local-state swap vs planted prediction
        others = [s for s in range(C) if s not in (v, order[1])]
        for a, b, kind in ((v, order[1], "victim_runner_up"), (v, int(rng.choice(others)), "victim_random")):
            nb = _order(S, dt, a, b)
            h2 = h.copy()
            h2[[a, b]] = h2[[b, a]]
            S2 = ctrl.score(h2, g, dt)
            na = _order(S2, dt, a, b)
            pb = planted_pair_order(planted, snaps[int(t)], C, a, b, int(t), swap=False)
            pa = planted_pair_order(planted, snaps[int(t)], C, a, b, int(t), swap=True)
            cl2 = cl.copy()
            cl2[[a, b]] = cl2[[b, a]]
            eb = _ext_pair(rule, cl, t_last, int(t), a, b)
            ea = _ext_pair(rule, cl2, t_last, int(t), a, b)
            rec["B2"].append({"t": int(t), "pair": kind, "planted_flip": bool(pb != pa),
                              "neural_flip": bool(nb != na), "extracted_flip": bool(eb != ea)})
        # B3 hit vs no-hit counterfactual on the victim and a random other resident
        u = int(rng.choice([s for s in range(C) if s != v]))
        for i in (v, u):
            hi2 = ctrl.hit(h[i], g, dt[i])
            g2 = ctrl.glob(g, True, False, h[i], dt[i])
            hh = h.copy()
            hh[i] = hi2
            dth = dt + 1
            dth[i] = 1
            vh = np_choose(ctrl.score(hh, g2, dth), dth, res)
            vn = np_choose(ctrl.score(h, g, dt + 1), dt + 1, res)
            clh = cl.copy()
            clh[i] = _ext_succ(rule, cl[i])
            tlh = t_last.copy()
            tlh[i] = t
            evh = _ext_choose(rule, clh, tlh, t + 1)
            evn = _ext_choose(rule, cl, t_last, t + 1)
            a_next = int(alpha(hi2)[0])
            rec["B3"].append({"t": int(t), "slot_kind": "victim" if i == v else "random",
                              "next_class_match": bool(a_next == clh[i]), "victim_hit_match": bool(vh == evh),
                              "victim_nohit_match": bool(vn == evn)})
        # B4 tie-break
        j = int(rng.choice([s for s in range(C) if s != v]))
        h3, dt3 = h.copy(), dt.copy()
        h3[j], dt3[j] = h[v], dt[v]
        vt = np_choose(ctrl.score(h3, g, dt3), dt3, res)
        cl3, tl3 = cl.copy(), t_last.copy()
        cl3[j], tl3[j] = cl[v], t_last[v]
        vte = _ext_choose(rule, cl3, tl3, t)
        rec["B4_tie"].append({"t": int(t), "expected": int(min(v, j)), "neural": int(vt), "extracted": int(vte)})
        # B5 targeted edit vs matched random perturbation
        u = int(rng.choice([s for s in range(C) if s != v]))
        dh = (h[v] - h[u]).astype(np.float64)
        ddt = float(dt[v] + 1 - dt[u])
        h4, dt4 = h.copy(), dt.copy()
        h4[u], dt4[u] = h[v], dt[v] + 1
        tgt = np_choose(ctrl.score(h4, g, dt4), dt4, res) == u
        th = rng.uniform(0, 2 * np.pi)
        rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        h5, dt5 = h.copy(), dt.copy()
        h5[u] = (h[u] + rot @ dh).astype(np.float32)
        dt5[u] = max(1.0, dt[u] + rng.choice([-1.0, 1.0]) * abs(ddt))
        rnd = np_choose(ctrl.score(h5, g, dt5), dt5, res) == u
        cl4, tl4 = cl.copy(), t_last.copy()
        cl4[u], tl4[u] = cl[v], t - (dt[v] + 1)
        rec["B5"].append({"t": int(t), "extracted_predicts_u": bool(_ext_choose(rule, cl4, tl4, t) == u),
                          "targeted_success": bool(tgt), "random_success": bool(rnd)})

    # B4 insertion (all insert events) and reset
    ins_idx = np.where(np.isin(et, [EVENT_EVICT, 2]))[0]
    ins_cls = alpha(out["hs_post"][ins_idx])
    ins_ok = float(np.mean(ins_cls == rule["insert_class"]))
    resets = []
    L = min(4000, len(req) // 2)
    for p0 in rng.choice(len(req) - L, size=3, replace=False):
        o = ctrl.cl(req[p0:p0 + L])
        pred, _ = X.shadow(rule, o["etype"], o["slot"], C)
        e = np.where(o["etype"] == EVENT_EVICT)[0][:64]
        resets.append({"start": int(p0), "n": int(len(e)), "match": int(np.sum(pred[e] == o["slot"][e]))})
    # summaries and gates
    b1 = all(r["scores_bitwise"] and r["neural_victim"] and r["extracted_victim"] for r in rec["B1"])
    flips = [r for r in rec["B2"] if r["planted_flip"]]
    b2 = all(r["neural_flip"] for r in flips)
    b3v = float(np.mean([r["next_class_match"] and r["victim_hit_match"] and r["victim_nohit_match"]
                         for r in rec["B3"]]))
    tie_ok = all(r["neural"] == r["expected"] and r["extracted"] == r["expected"] for r in rec["B4_tie"])
    reset_ok = all(r["n"] == 64 and r["match"] == 64 for r in resets)
    ts = sum(r["targeted_success"] for r in rec["B5"])
    rs = sum(r["random_success"] for r in rec["B5"])
    n5 = len(rec["B5"])
    _, pval = fisher_exact([[ts, n5 - ts], [rs, n5 - rs]], alternative="greater")
    summ = {
        "B1_exact": b1,
        "B2_predicted_flips": len(flips), "B2_neural_flipped": int(sum(r["neural_flip"] for r in flips)),
        "B2_pass": b2,
        "B2_noflip_consistency": float(np.mean([not r["neural_flip"] for r in rec["B2"] if not r["planted_flip"]]))
        if any(not r["planted_flip"] for r in rec["B2"]) else None,
        "B3_agreement": b3v, "B3_pass": b3v >= cfg["gates"]["phaseB_counterfactual_min"],
        "B4_insert_exact_fraction": ins_ok, "B4_reset": resets, "B4_tie_exact": tie_ok,
        "B4_pass": bool(ins_ok == 1.0 and reset_ok and tie_ok),
        "B5_targeted": f"{ts}/{n5}", "B5_random": f"{rs}/{n5}", "B5_p": float(pval),
        "B5_pass": bool(pval < cfg["gates"]["phaseB_significance_alpha"]),
    }
    summ["pass"] = bool(b1 and b2 and summ["B3_pass"] and summ["B4_pass"] and summ["B5_pass"])
    return summ, rec


def _ext_pair(rule, cl, t_last, t, a, b):
    rank = {int(k): v for k, v in rule["rank"].items()}
    old = rule["recency"] == "oldest_first"

    def key(s):
        dt = t - t_last[s]
        return (rank[int(cl[s])], -dt if old else dt, s)
    return key(a) < key(b)
