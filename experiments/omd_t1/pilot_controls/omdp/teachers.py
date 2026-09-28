"""Planted teacher policies and the cache simulator.

A policy tracks its own bookkeeping per slot. The simulator owns the item->slot map and time.
Each policy exposes:
  reset(C); on_insert(slot, t); on_hit(slot, t); choose(t) -> victim slot (may update internal
  state, e.g. SIEVE clears visited bits and moves its hand); on_forced_evict(slot, t) (bookkeeping
  when another controller chose the victim; used to track planted abstract states along foreign
  trajectories); local_state(slot) -> planted abstract local state; spec -> planted quotient spec.
"""
from __future__ import annotations

import numpy as np

from .config import EVENT_EVICT, EVENT_FILL, EVENT_HIT


class Policy:
    name = "base"

    def reset(self, C):
        self.C = C
        self.t_last = np.full(C, -1, dtype=np.int64)
        self.resident = np.zeros(C, dtype=bool)

    def on_insert(self, slot, t):
        self.t_last[slot] = t
        self.resident[slot] = True

    def on_hit(self, slot, t):
        self.t_last[slot] = t

    def _remove(self, slot):
        self.resident[slot] = False

    def choose(self, t):
        raise NotImplementedError

    def on_evict(self, slot, t):
        """Called after choose() when the policy's own victim is evicted."""
        self._remove(slot)

    def on_forced_evict(self, slot, t):
        """Bookkeeping when an external controller evicted `slot` (the policy's choice is simulated
        first so that any side effects, such as SIEVE's scan, happen as they would have)."""
        own = self.choose(t)
        self._after_forced(own, slot)
        self._remove(slot)

    def _after_forced(self, own, slot):
        pass

    def local_state(self, slot):
        return 0


class LRU(Policy):
    name = "LRU"

    def choose(self, t):
        cand = np.where(self.resident)[0]
        return int(cand[np.argmin(self.t_last[cand])])


class LFU(Policy):
    name = "LFU"

    def reset(self, C):
        super().reset(C)
        self.count = np.zeros(C, dtype=np.int64)

    def on_insert(self, slot, t):
        super().on_insert(slot, t)
        self.count[slot] = 0

    def on_hit(self, slot, t):
        super().on_hit(slot, t)
        self.count[slot] += 1

    def choose(self, t):
        cand = np.where(self.resident)[0]
        key = self.count[cand] * (1 << 40) + self.t_last[cand]  # lexicographic (count, t_last)
        return int(cand[np.argmin(key)])

    def local_state(self, slot):
        return int(self.count[slot])


class TWOQ(Policy):
    name = "TWOQ"

    def reset(self, C):
        super().reset(C)
        self.tier = np.zeros(C, dtype=np.int64)

    def on_insert(self, slot, t):
        super().on_insert(slot, t)
        self.tier[slot] = 0

    def on_hit(self, slot, t):
        super().on_hit(slot, t)
        self.tier[slot] = 1

    def choose(self, t):
        cand = np.where(self.resident)[0]
        key = self.tier[cand] * (1 << 40) + self.t_last[cand]
        return int(cand[np.argmin(key)])

    def local_state(self, slot):
        return int(self.tier[slot])


class SIEVE(Policy):
    name = "SIEVE"

    def reset(self, C):
        super().reset(C)
        self.visited = np.zeros(C, dtype=bool)
        self.queue = []          # slots, index 0 = tail (oldest insertion), end = head (newest)
        self.hand = None         # slot id or None (null -> start at tail)
        self._pending_hand = None

    def on_insert(self, slot, t):
        super().on_insert(slot, t)
        self.visited[slot] = False
        self.queue.append(slot)

    def on_hit(self, slot, t):
        super().on_hit(slot, t)
        self.visited[slot] = True

    def choose(self, t):
        q = self.queue
        idx = q.index(self.hand) if self.hand is not None else 0
        while self.visited[q[idx]]:
            self.visited[q[idx]] = False
            idx += 1
            if idx == len(q):
                idx = 0
        victim = q[idx]
        self._pending_hand = q[idx + 1] if idx + 1 < len(q) else None
        return victim

    def on_evict(self, slot, t):
        self.queue.remove(slot)
        self.hand = self._pending_hand
        super().on_evict(slot, t)

    def _after_forced(self, own, slot):
        # own choice evicted: normal hand move; otherwise the hand stays on its own choice
        if own == slot:
            self.hand = self._pending_hand
        else:
            self.hand = own
        self.queue.remove(slot)

    def local_state(self, slot):
        return int(self.visited[slot])


POLICIES = {"LRU": LRU, "LFU": LFU, "SIEVE": SIEVE, "TWOQ": TWOQ}

# Planted quotient specifications used by the (unblinded) judge.
PLANTED_SPEC = {
    "LRU": {"kind": "classes", "insert": 0, "hit": {0: 0}, "rank": {0: 0}, "recency": "oldest_first"},
    "LFU": {"kind": "counter", "insert": 0, "recency": "oldest_first"},
    "TWOQ": {"kind": "classes", "insert": 0, "hit": {0: 1, 1: 1}, "rank": {0: 0, 1: 1},
             "recency": "oldest_first"},
    "SIEVE": {"kind": "queue_hand", "insert": 0, "recency": "insertion_queue_with_global_hand"},
}


def make(name):
    return POLICIES[name]()


def simulate(policy_name, req, C, record_local=True):
    """Autonomous teacher run. Returns a dict of event arrays."""
    pol = make(policy_name)
    pol.reset(C)
    return _run(req, C, lambda t: pol.choose(t), pol, record_local)


def _run(req, C, decide, pol, record_local, forced=False):
    T = len(req)
    items = np.full(C, -1, dtype=np.int64)
    where = {}
    t_last = np.full(C, -1, dtype=np.int64)
    etype = np.zeros(T, dtype=np.int8)
    slot = np.zeros(T, dtype=np.int16)
    dt = np.zeros((T, C), dtype=np.float32)
    resident = np.zeros((T, C), dtype=bool)
    local = np.zeros((T, C), dtype=np.int64) if record_local else None
    hits = 0
    for t in range(T):
        x = int(req[t])
        res = items >= 0
        resident[t] = res
        dt[t] = np.where(res, t - t_last, 0)
        if record_local:
            local[t] = [pol.local_state(s) if res[s] else -1 for s in range(C)]
        if x in where:
            s = where[x]
            etype[t], slot[t] = EVENT_HIT, s
            pol.on_hit(s, t)
            hits += 1
        elif not res.all():
            s = int(np.argmin(res))  # lowest free slot
            etype[t], slot[t] = EVENT_FILL, s
            items[s] = x
            where[x] = s
            pol.on_insert(s, t)
        else:
            s = int(decide(t))
            etype[t], slot[t] = EVENT_EVICT, s
            if forced:
                pol.on_forced_evict(s, t)
            else:
                pol.on_evict(s, t)
            del where[int(items[s])]
            items[s] = x
            where[x] = s
            pol.on_insert(s, t)
        t_last[slot[t]] = t
    return {"etype": etype, "slot": slot, "dt": dt, "resident": resident, "local": local,
            "hits": hits, "T": T}


def track(policy_name, req, C, etype, slot):
    """Track the planted policy's abstract local states and its own would-be victims along a
    foreign trajectory (given event types and slots). Returns (local[T,C], own_choice[T] or -1)."""
    pol = make(policy_name)
    pol.reset(C)
    T = len(req)
    local = np.full((T, C), -1, dtype=np.int64)
    own = np.full(T, -1, dtype=np.int64)
    for t in range(T):
        for s in np.where(pol.resident)[0]:
            local[t, s] = pol.local_state(s)
        e, s = int(etype[t]), int(slot[t])
        if e == EVENT_HIT:
            pol.on_hit(s, t)
        elif e == EVENT_FILL:
            pol.on_insert(s, t)
        elif e == EVENT_EVICT:
            snap = _snapshot(pol)
            own[t] = pol.choose(t)
            _restore(pol, snap)
            pol.on_forced_evict(s, t)
            pol.on_insert(s, t)
    return local, own


def _snapshot(pol):
    d = {}
    for k, v in pol.__dict__.items():
        d[k] = v.copy() if isinstance(v, (np.ndarray, list)) else v
    return d


def _restore(pol, snap):
    for k, v in snap.items():
        setattr(pol, k, v.copy() if isinstance(v, (np.ndarray, list)) else v)


def teacher_forced_agreement(policy_name, req, C, etype, slot):
    """Fraction of evictions on a given trajectory where the planted policy (tracked along it)
    would have chosen the same victim."""
    _, own = track(policy_name, req, C, etype, slot)
    ev = etype == EVENT_EVICT
    return float(np.mean(own[ev] == slot[ev])) if ev.any() else 1.0
