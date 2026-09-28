"""The frozen OMD-PILOT-1 instrument: a slot-equivariant lazy recurrent cache controller (JAX, float32).

State: h (C, 2) local per slot, g (1,) global. Four shared event networks (one tanh hidden layer of
width 16): S (score), F_hit, F_ins, F_g. Only the touched slot and g change on an event.
"""
from __future__ import annotations

import os

os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from .config import CONFIG, EVENT_EVICT, EVENT_FILL, EVENT_HIT, EVENT_NOOP  # noqa: E402

H = 16
NET_SHAPES = {"S": (5, 1), "F_hit": (5, 2), "F_ins": (1, 2), "F_g": (7, 1)}
SMALL_OUT = {"F_hit", "F_g"}


def init_params(seed: int):
    rng = np.random.default_rng(seed)
    p = {}
    for name, (din, dout) in NET_SHAPES.items():
        w2_scale = (0.1 if name in SMALL_OUT else 1.0) / np.sqrt(H)
        p[name] = {"W1": (rng.standard_normal((din, H)) / np.sqrt(din)).astype(np.float32),
                   "b1": np.zeros(H, np.float32),
                   "W2": (rng.standard_normal((H, dout)) * w2_scale).astype(np.float32),
                   "b2": np.zeros(dout, np.float32)}
    return jax.tree_util.tree_map(jnp.asarray, p)


def n_params(p) -> int:
    return int(sum(np.size(x) for x in jax.tree_util.tree_leaves(p)))


def _mlp(q, x):
    return jnp.tanh(x @ q["W1"] + q["b1"]) @ q["W2"] + q["b2"]


def phi(dt):
    dt = jnp.asarray(dt, jnp.float32)
    return jnp.stack([jnp.log1p(dt) / 8.0, dt / 1024.0], -1)


def score(p, h, g, dt):
    """h (C,2), g (1,), dt (C,) -> scores (C,)."""
    C = h.shape[0]
    x = jnp.concatenate([h, jnp.broadcast_to(g, (C, 1)), phi(dt)], -1)
    return _mlp(p["S"], x)[:, 0]


def f_hit(p, hi, g, dti):
    x = jnp.concatenate([hi, g, phi(dti)])
    return hi + _mlp(p["F_hit"], x)


def f_ins(p, g):
    return _mlp(p["F_ins"], g)


def f_g(p, g, is_hit, is_evict, hs, dts):
    x = jnp.concatenate([g, jnp.stack([is_hit, is_evict]).astype(jnp.float32), hs, phi(dts)])
    return g + _mlp(p["F_g"], x)


def choose(S, dt, resident):
    """Deterministic argmin with the frozen tie-break: min S, then larger dt, then lower index."""
    Sm = jnp.where(resident, S, jnp.inf)
    m = jnp.min(Sm)
    cand = resident & (Sm == m)
    dtc = jnp.where(cand, dt, -1.0)
    cand2 = cand & (dtc == jnp.max(dtc))
    return jnp.argmax(cand2)


def _event_update(p, h, g, etype, slot, dt_slot):
    """Apply one event's lazy update. Returns (h_new, g_new, h_slot_new)."""
    hs = h[slot]
    is_hit = etype == EVENT_HIT
    is_ev = etype == EVENT_EVICT
    is_fill = etype == EVENT_FILL
    zero2 = jnp.zeros(2, jnp.float32)
    hs_in = jnp.where(is_fill, zero2, hs)
    dts_in = jnp.where(is_fill, 0.0, dt_slot)
    g_new = f_g(p, g, is_hit, is_ev, hs_in, dts_in)
    h_hit = f_hit(p, hs, g, dt_slot)
    h_ins = f_ins(p, g_new)
    h_slot_new = jnp.where(is_hit, h_hit, h_ins)
    noop = etype == EVENT_NOOP
    h_slot_new = jnp.where(noop, hs, h_slot_new)
    g_new = jnp.where(noop, g, g_new)
    return h.at[slot].set(h_slot_new), g_new, h_slot_new


def _tf_step(p, carry, ev):
    h, g = carry
    etype, slot, dt, resident = ev
    S = score(p, h, g, dt)
    victim = choose(S, dt, resident)
    logits = jnp.where(resident, -S, -jnp.inf)
    lse = jax.scipy.special.logsumexp(logits)
    is_ev = etype == EVENT_EVICT
    loss = jnp.where(is_ev, lse + S[slot], 0.0)
    h_new, g_new, hs_new = _event_update(p, h, g, etype, slot, dt[slot])
    out = {"loss": loss, "victim": victim, "S": S, "h_pre": h, "g_pre": g, "hs_post": hs_new,
           "g_post": g_new}
    return (h_new, g_new), out


def init_carry(C):
    return (jnp.zeros((C, 2), jnp.float32), jnp.zeros((1,), jnp.float32) + CONFIG["instrument"]["g0"])


@jax.jit
def tf_rollout(p, carry, etype, slot, dt, resident):
    """Teacher-forced / shadow rollout along a given trajectory."""
    return jax.lax.scan(lambda c, e: _tf_step(p, c, e), carry, (etype, slot, dt, resident))


def _window_loss(p, carry, etype, slot, dt, resident):
    carry2, out = jax.lax.scan(lambda c, e: _tf_step(p, c, e), carry, (etype, slot, dt, resident))
    n = jnp.maximum(jnp.sum(etype == EVENT_EVICT), 1)
    return jnp.sum(out["loss"]) / n, carry2


window_grad = jax.jit(jax.value_and_grad(_window_loss, has_aux=True))


def _cl_step(p, carry, x):
    h, g, items, t_last, t = carry
    resident = items >= 0
    dt = jnp.where(resident, (t - t_last).astype(jnp.float32), 0.0)
    hitm = items == x
    is_hit = jnp.any(hitm)
    full = jnp.all(resident)
    S = score(p, h, g, dt)
    victim = choose(S, dt, resident)
    etype = jnp.where(is_hit, EVENT_HIT, jnp.where(full, EVENT_EVICT, EVENT_FILL))
    slot = jnp.where(is_hit, jnp.argmax(hitm), jnp.where(full, victim, jnp.argmax(~resident)))
    h_new, g_new, hs_new = _event_update(p, h, g, etype, slot, dt[slot])
    items = jnp.where(is_hit, items, items.at[slot].set(x))
    t_last = t_last.at[slot].set(t)
    out = {"etype": etype.astype(jnp.int8), "slot": slot.astype(jnp.int16), "S": S, "dt": dt,
           "resident": resident, "h_pre": h, "g_pre": g, "hs_post": hs_new, "g_post": g_new,
           "is_hit": is_hit}
    return (h_new, g_new, items, t_last, t + 1), out


@jax.jit
def cl_rollout(p, req):
    C = CONFIG["C"]
    h, g = init_carry(C)
    carry = (h, g, jnp.full((C,), -1, jnp.int32), jnp.full((C,), -1, jnp.int32), jnp.int32(0))
    _, out = jax.lax.scan(lambda c, x: _cl_step(p, c, x), carry, jnp.asarray(req, jnp.int32))
    return out


# jitted single-step helpers for interventions
score_j = jax.jit(score)
f_hit_j = jax.jit(f_hit)
f_ins_j = jax.jit(f_ins)
f_g_j = jax.jit(f_g)
choose_j = jax.jit(choose)


def to_numpy(tree):
    return jax.tree_util.tree_map(lambda x: np.asarray(x), tree)


def params_to_lists(p):
    return jax.tree_util.tree_map(lambda x: np.asarray(x).tolist(), p)


def params_from_lists(d):
    return jax.tree_util.tree_map(lambda x: jnp.asarray(np.asarray(x, np.float32)), d,
                                  is_leaf=lambda x: isinstance(x, list))
