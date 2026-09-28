"""Supervised teacher imitation (teacher-forced truncated BPTT, Adam, fixed LR)."""
from __future__ import annotations

import time

import jax
import jax.numpy as jnp
import numpy as np

from . import instrument as ins
from .config import CONFIG, EVENT_EVICT, EVENT_NOOP


def pad_windows(tr, bptt):
    """Split a teacher trajectory into windows of `bptt` events, padding the last one with no-ops."""
    T = tr["T"]
    nw = -(-T // bptt)
    P = nw * bptt - T
    C = tr["dt"].shape[1]
    et = np.concatenate([tr["etype"].astype(np.int32), np.full(P, EVENT_NOOP, np.int32)])
    sl = np.concatenate([tr["slot"].astype(np.int32), np.zeros(P, np.int32)])
    dt = np.concatenate([tr["dt"], np.zeros((P, C), np.float32)])
    rs = np.concatenate([tr["resident"], np.zeros((P, C), bool)])
    return [tuple(jnp.asarray(a[i * bptt:(i + 1) * bptt]) for a in (et, sl, dt, rs)) for i in range(nw)]


def evaluate_tf(p, tr):
    """Teacher-forced full-sequence mean CE and victim agreement."""
    C = tr["dt"].shape[1]
    _, out = ins.tf_rollout(p, ins.init_carry(C), jnp.asarray(tr["etype"], jnp.int32),
                            jnp.asarray(tr["slot"], jnp.int32), jnp.asarray(tr["dt"]),
                            jnp.asarray(tr["resident"]))
    ev = tr["etype"] == EVENT_EVICT
    loss = np.asarray(out["loss"])[ev]
    agree = np.asarray(out["victim"])[ev] == tr["slot"][ev]
    return {"ce": float(loss.mean()), "agreement": float(agree.mean()), "n_evict": int(ev.sum())}


def _adam(p, g, m, v, k, cfg):
    b1, b2 = cfg["betas"]
    lr, eps = cfg["lr"], cfg["eps"]
    m = jax.tree_util.tree_map(lambda m_, g_: b1 * m_ + (1 - b1) * g_, m, g)
    v = jax.tree_util.tree_map(lambda v_, g_: b2 * v_ + (1 - b2) * g_ * g_, v, g)
    mh = jax.tree_util.tree_map(lambda m_: m_ / (1 - b1 ** k), m)
    vh = jax.tree_util.tree_map(lambda v_: v_ / (1 - b2 ** k), v)
    p = jax.tree_util.tree_map(lambda p_, a, b: p_ - lr * a / (jnp.sqrt(b) + eps), p, mh, vh)
    return p, m, v


def _clip(g, max_norm):
    norm = jnp.sqrt(sum(jnp.sum(x * x) for x in jax.tree_util.tree_leaves(g)))
    scale = jnp.minimum(1.0, max_norm / (norm + 1e-12))
    return jax.tree_util.tree_map(lambda x: x * scale, g), float(norm)


def train(tr, seed, cfg=CONFIG, cpu_guard=None, max_passes=None, log=None):
    tc = cfg["training"]
    C = cfg["C"]
    p = ins.init_params(seed)
    assert ins.n_params(p) <= cfg["instrument"]["param_cap"]
    m = jax.tree_util.tree_map(jnp.zeros_like, p)
    v = jax.tree_util.tree_map(jnp.zeros_like, p)
    wins = pad_windows(tr, tc["bptt"])
    k = 0
    history = []
    best = None
    passes = tc["max_passes"] if max_passes is None else max_passes
    for ep in range(passes):
        t0 = time.time()
        carry = ins.init_carry(C)
        losses, norms = [], []
        for w in wins:
            (loss, carry), grads = ins.window_grad(p, carry, *w)
            carry = jax.tree_util.tree_map(jax.lax.stop_gradient, carry)
            grads, gn = _clip(grads, tc["grad_clip_global_norm"])
            k += 1
            p, m, v = _adam(p, grads, m, v, k, tc)
            losses.append(float(loss))
            norms.append(gn)
        ev = evaluate_tf(p, tr)
        rec = {"pass": ep + 1, "train_window_loss_mean": float(np.mean(losses)),
               "grad_norm_median": float(np.median(norms)), **{"train_" + a: b for a, b in ev.items()},
               "wall_s": round(time.time() - t0, 3)}
        history.append(rec)
        if log:
            log(rec)
        if not np.isfinite(ev["ce"]):
            break
        if best is None or ev["ce"] < best[0]:
            best = (ev["ce"], ep + 1, jax.tree_util.tree_map(lambda x: x, p))
        if cpu_guard is not None:
            cpu_guard()
    if best is None:
        best = (float("nan"), 0, p)
    return best[2], {"history": history, "selected_pass": best[1], "selected_train_ce": best[0],
                     "n_params": ins.n_params(p), "updates": k}
