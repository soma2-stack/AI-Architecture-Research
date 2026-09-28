"""Controller interface used by Phases B and C.

NeuralController wraps trained instrument parameters (jitted JAX). `generic_cl` / `generic_tf` run any
controller exposing score/hit/ins/glob step functions in plain Python; the tests use them to check the
jitted rollouts and to drive synthetic oracle controllers."""
from __future__ import annotations

import numpy as np

from . import instrument as ins
from .config import CONFIG, EVENT_EVICT, EVENT_FILL, EVENT_HIT


def np_choose(S, dt, resident):
    Sm = np.where(resident, S, np.inf)
    m = Sm.min()
    cand = resident & (Sm == m)
    dtc = np.where(cand, dt, -1.0)
    return int(np.argmax(cand & (dtc == dtc.max())))


class NeuralController:
    def __init__(self, params):
        self.p = params

    def score(self, h, g, dt):
        return np.asarray(ins.score_j(self.p, np.asarray(h, np.float32), np.asarray(g, np.float32),
                                      np.asarray(dt, np.float32)))

    def hit(self, hi, g, dti):
        return np.asarray(ins.f_hit_j(self.p, np.asarray(hi, np.float32), np.asarray(g, np.float32),
                                      np.float32(dti)))

    def ins(self, g):
        return np.asarray(ins.f_ins_j(self.p, np.asarray(g, np.float32)))

    def glob(self, g, is_hit, is_ev, hs, dts):
        return np.asarray(ins.f_g_j(self.p, np.asarray(g, np.float32), bool(is_hit), bool(is_ev),
                                    np.asarray(hs, np.float32), np.float32(dts)))

    def cl(self, req):
        return ins.to_numpy(ins.cl_rollout(self.p, np.asarray(req, np.int32)))

    def tf(self, etype, slot, dt, resident):
        C = dt.shape[1]
        _, out = ins.tf_rollout(self.p, ins.init_carry(C), np.asarray(etype, np.int32),
                                np.asarray(slot, np.int32), np.asarray(dt, np.float32),
                                np.asarray(resident, bool))
        return ins.to_numpy(out)


def generic_step(ctrl, h, g, etype, slot, dt_slot):
    """Python version of the instrument's lazy event update (same order of operations)."""
    hs = h[slot].copy()
    if etype == EVENT_HIT:
        g_new = ctrl.glob(g, True, False, hs, dt_slot)
        hs_new = ctrl.hit(hs, g, dt_slot)
    elif etype == EVENT_EVICT:
        g_new = ctrl.glob(g, False, True, hs, dt_slot)
        hs_new = ctrl.ins(g_new)
    else:
        g_new = ctrl.glob(g, False, False, np.zeros(2, np.float32), 0.0)
        hs_new = ctrl.ins(g_new)
    h = h.copy()
    h[slot] = hs_new
    return h, np.asarray(g_new, np.float32), hs_new


def generic_cl(ctrl, req, C=None):
    C = C or CONFIG["C"]
    h = np.zeros((C, 2), np.float32)
    g = np.zeros(1, np.float32) + CONFIG["instrument"]["g0"]
    items = np.full(C, -1, np.int64)
    t_last = np.full(C, -1, np.int64)
    T = len(req)
    out = {"etype": np.zeros(T, np.int8), "slot": np.zeros(T, np.int16), "is_hit": np.zeros(T, bool),
           "S": np.zeros((T, C), np.float32), "dt": np.zeros((T, C), np.float32),
           "resident": np.zeros((T, C), bool), "hs_post": np.zeros((T, 2), np.float32),
           "h_pre": np.zeros((T, C, 2), np.float32), "g_pre": np.zeros((T, 1), np.float32),
           "g_post": np.zeros((T, 1), np.float32)}
    for t, x in enumerate(req):
        out["h_pre"][t], out["g_pre"][t] = h, g
        res = items >= 0
        dt = np.where(res, t - t_last, 0).astype(np.float32)
        S = ctrl.score(h, g, dt)
        hitm = items == x
        if hitm.any():
            e, s = EVENT_HIT, int(np.argmax(hitm))
        elif res.all():
            e, s = EVENT_EVICT, np_choose(S, dt, res)
        else:
            e, s = EVENT_FILL, int(np.argmax(~res))
        h, g, hs = generic_step(ctrl, h, g, e, s, dt[s])
        if e != EVENT_HIT:
            items[s] = x
        t_last[s] = t
        out["etype"][t], out["slot"][t], out["is_hit"][t] = e, s, e == EVENT_HIT
        out["S"][t], out["dt"][t], out["resident"][t], out["hs_post"][t] = S, dt, res, hs
        out["g_post"][t] = g
    return out


def generic_tf(ctrl, etype, slot, dt, resident):
    """Python shadow rollout along a given trajectory (same outputs as instrument.tf_rollout)."""
    T, C = dt.shape
    h = np.zeros((C, 2), np.float32)
    g = np.zeros(1, np.float32) + CONFIG["instrument"]["g0"]
    out = {"victim": np.zeros(T, np.int64), "S": np.zeros((T, C), np.float32),
           "h_pre": np.zeros((T, C, 2), np.float32), "g_pre": np.zeros((T, 1), np.float32),
           "hs_post": np.zeros((T, 2), np.float32), "g_post": np.zeros((T, 1), np.float32)}
    for t in range(T):
        out["h_pre"][t], out["g_pre"][t] = h, g
        S = ctrl.score(h, g, dt[t])
        out["S"][t] = S
        out["victim"][t] = np_choose(S, dt[t], resident[t]) if resident[t].any() else 0
        s = int(slot[t])
        h, g, hs = generic_step(ctrl, h, g, int(etype[t]), s, dt[t][s])
        out["hs_post"][t], out["g_post"][t] = hs, g
    return out
