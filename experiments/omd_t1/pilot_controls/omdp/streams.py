"""Control-excitation request streams (fixed mixture; not the T1 discovery benchmark)."""
from __future__ import annotations

import numpy as np

from .config import CONFIG

SEG_TYPES = ["uniform", "zipf", "working_set", "scan", "loop", "burst"]


def make_stream(seed: int, length: int, cfg=CONFIG):
    """Return (requests int32[length], seg_id int32[length], segments list of dicts)."""
    sc, N = cfg["stream"], cfg["N"]
    rng = np.random.default_rng(seed)
    names = list(sc["mixture"])
    probs = np.array([sc["mixture"][k] for k in names], dtype=float)
    probs /= probs.sum()
    reqs, segs = [], []
    total = 0
    while total < length:
        kind = names[rng.choice(len(names), p=probs)]
        if kind in ("uniform", "zipf", "working_set"):
            n = int(rng.integers(sc["iid_len"][0], sc["iid_len"][1] + 1))
            if kind == "uniform":
                r = rng.integers(0, N, size=n)
                info = {}
            elif kind == "zipf":
                perm = rng.permutation(N)
                w = 1.0 / np.arange(1, N + 1) ** sc["zipf_alpha"]
                r = perm[rng.choice(N, size=n, p=w / w.sum())]
                info = {"alpha": sc["zipf_alpha"]}
            else:
                ws = int(rng.choice(sc["working_set_sizes"]))
                hot = rng.choice(N, size=ws, replace=False)
                is_hot = rng.random(n) < sc["working_set_p_hot"]
                r = np.where(is_hot, hot[rng.integers(0, ws, size=n)], rng.integers(0, N, size=n))
                info = {"size": ws}
        elif kind == "scan":
            n = int(rng.integers(sc["scan_len"][0], sc["scan_len"][1] + 1))
            r = rng.choice(N, size=n, replace=False)
            info = {}
        elif kind == "loop":
            L = int(rng.integers(sc["loop_size"][0], sc["loop_size"][1] + 1))
            n = int(rng.integers(sc["loop_len"][0], sc["loop_len"][1] + 1))
            items = rng.choice(N, size=L, replace=False)
            r = items[np.arange(n) % L]
            info = {"size": L}
        else:  # burst
            n = int(rng.integers(sc["burst_len"][0], sc["burst_len"][1] + 1))
            out = []
            while len(out) < n:
                k = int(rng.integers(sc["burst_repeat"][0], sc["burst_repeat"][1] + 1))
                out.extend([int(rng.integers(0, N))] * k)
            r = np.array(out[:n])
            info = {}
        n = min(len(r), length - total)
        segs.append({"type": kind, "start": total, "end": total + n, **info})
        reqs.append(np.asarray(r[:n], dtype=np.int32))
        total += n
    req = np.concatenate(reqs)
    seg_id = np.zeros(length, dtype=np.int32)
    for i, s in enumerate(segs):
        seg_id[s["start"]:s["end"]] = i
    return req, seg_id, segs


def stationary_mask(segs, length, cfg=CONFIG):
    m = np.zeros(length, dtype=bool)
    for s in segs:
        if s["type"] in cfg["stream"]["stationary_segment_types"]:
            m[s["start"]:s["end"]] = True
    return m
