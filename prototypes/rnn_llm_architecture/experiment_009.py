"""Experiment 009: why two-slot memory fails — plateau, leak, or routing?

CPU-only supervised synthetic study; runs only on explicit CLI invocation.
NOT a formal robust learning-credit (D) measurement and NOT a language model
result. See EXPERIMENT_009_PLAN.md for hypotheses and falsifiers.

Task (``two_slot``): two tagged writes ``WRITE_A bit`` / ``WRITE_B bit`` in
random order, then a body of ``delay`` tokens containing benign distractors,
*unmarked* bit tokens (same token ids as values, conflicting information) and
1-3 marked updates ``WRITE_X bit`` at random positions, then ``QUERY_A`` or
``QUERY_B``. Both queries are asked of the identical prefix. Labels come from
an independent token replay: a bit token writes slot X only when the token
immediately before it is ``WRITE_X``.

Oracle write masks are **upper-bound diagnostics**: they give the protected
cell information that learned models do not receive, and are reported in a
separate table, never as an architecture result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from .learning_pilot import (BIT0, BIT1, DISTRACTOR_END, DISTRACTOR_START, QUERY_A, QUERY_B,
                             WRITE_A, WRITE_B, make_batch)
from .experiment_002 import _slot_targets, build
from .experiment_004 import _paired_inputs
from .experiment_006 import flatten_recurrent_state
from .candidates import CandidateLanguageModel, ProtectedMemoryCell
from .event_gated import (EventGatedConfig, EventGatedLanguageModel, EventGatedProtectedCell,
                          KeepGatedGRULanguageModel, ShiftState)
from .gated import GatedConfig, GatedLanguageModel, LSTMState

INITIAL_TOKENS = 4  # WRITE_x bit WRITE_y bit

# name -> (family, options). Oracle arms are diagnostics, not architectures.
VARIANTS: dict[str, dict] = {
    "protected_w32": {"family": "protected"},
    "protected_no_retain_w32": {"family": "protected"},  # slow gate forced open: protection removed
    "tanh_w32": {"family": "stock"},
    "protected_shift_w32": {"family": "event", "gate_mode": "soft", "token_shift": True},
    "protected_hard_w32": {"family": "event", "gate_mode": "hard", "token_shift": False},
    "protected_hard_shift_w32": {"family": "event", "gate_mode": "hard", "token_shift": True},
    "gru_w32": {"family": "stock"},
    "lstm_w32": {"family": "stock"},
    "gru_w24": {"family": "stock"},
    "lstm_w20": {"family": "stock"},
    "gru_keep3_w32": {"family": "keep_gru", "gate_mode": "soft", "keep_bias": 3.0},
    "gru_hard_w32": {"family": "keep_gru", "gate_mode": "hard", "keep_bias": 3.0},
    "oracle_tag_protected_w32": {"family": "protected", "oracle": "tag"},
    "oracle_route_protected_w32": {"family": "protected", "oracle": "route"},
}
ORACLE_MODES = ("tag", "route")
TRAIN_TASKS = ("two_slot", "legacy")


# --------------------------------------------------------------------------- task
def make_two_slot_batch(delay: int, batch: int, *, seed: int, unmarked_bit_rate: float = .25,
                        min_updates: int = 1, max_updates: int = 3) -> tuple[Tensor, dict]:
    """Return query-free prefixes ``[batch, 4+delay]`` and the generator's own record.

    Randomness consumed is independent of the sampled update counts, so a seed
    fully determines the batch. Labels used for training/evaluation are NOT
    taken from this record but from :func:`replay_slots`; tests cross-check.
    """
    if (type(delay) is not int or type(batch) is not int or batch < 1
            or not 1 <= min_updates <= max_updates or delay < 2 * max_updates + 1
            or not 0 <= unmarked_bit_rate < 1):
        raise ValueError("invalid two-slot task parameters")
    g = torch.Generator(device="cpu").manual_seed(seed)
    initial = torch.randint(0, 2, (batch, 2), generator=g)
    b_first = torch.randint(0, 2, (batch,), generator=g).bool()
    body = torch.randint(DISTRACTOR_START, DISTRACTOR_END, (batch, delay), generator=g)
    noise_bits = torch.randint(0, 2, (batch, delay), generator=g) + BIT0
    unmarked = torch.rand((batch, delay), generator=g) < unmarked_bit_rate
    body = torch.where(unmarked, noise_bits, body)
    counts = torch.randint(min_updates, max_updates + 1, (batch,), generator=g)
    slots = torch.randint(0, 2, (batch, max_updates), generator=g)
    values = torch.randint(0, 2, (batch, max_updates), generator=g)
    scores = torch.rand((batch, delay), generator=g)
    final = initial.clone()
    last_slot = torch.empty(batch, dtype=torch.long)
    last_value = torch.empty(batch, dtype=torch.long)
    for i in range(batch):
        k = int(counts[i])
        picks = torch.sort(torch.argsort(scores[i, :delay - k])[:k]).values
        starts = picks + torch.arange(k)  # strictly non-overlapping two-token updates
        body[i, starts] = WRITE_A + slots[i, :k]
        body[i, starts + 1] = BIT0 + values[i, :k]
        for j in range(k):
            final[i, slots[i, j]] = values[i, j]
        last_slot[i], last_value[i] = slots[i, k - 1], values[i, k - 1]
    first_slot = b_first.long()
    first = torch.stack((WRITE_A + first_slot, BIT0 + initial.gather(1, first_slot[:, None])[:, 0],
                         WRITE_A + 1 - first_slot,
                         BIT0 + initial.gather(1, (1 - first_slot)[:, None])[:, 0]), dim=1)
    prefix = torch.cat((first, body), dim=1).long()
    return prefix, {"initial": initial, "final": final, "updates": counts,
                    "last_update_slot": last_slot, "last_update_value": last_value,
                    "unmarked_bits": unmarked.sum(1)}


def marked_writes(ids: Tensor) -> tuple[Tensor, Tensor]:
    """Boolean ``[B,T]`` masks of bit tokens immediately preceded by WRITE_A / WRITE_B."""
    prev = torch.cat((torch.zeros_like(ids[:, :1]), ids[:, :-1]), dim=1)
    is_bit = (ids == BIT0) | (ids == BIT1)
    return is_bit & (prev == WRITE_A), is_bit & (prev == WRITE_B)


def replay_slots(prefix: Tensor) -> dict[str, Tensor]:
    """Reference semantics from tokens alone; independent of the generator."""
    if prefix.ndim != 2 or prefix.dtype != torch.long:
        raise ValueError("prefix must be [B,T] long")
    wa, wb = marked_writes(prefix)
    value = prefix - BIT0
    b = prefix.shape[0]
    a_val = torch.full((b,), -1, dtype=torch.long)
    b_val = a_val.clone()
    last_slot, last_value = a_val.clone(), a_val.clone()
    last_bit = a_val.clone()
    is_bit = (prefix == BIT0) | (prefix == BIT1)
    for t in range(prefix.shape[1]):
        a_val = torch.where(wa[:, t], value[:, t], a_val)
        b_val = torch.where(wb[:, t], value[:, t], b_val)
        last_slot = torch.where(wa[:, t], 0, torch.where(wb[:, t], 1, last_slot))
        last_value = torch.where(wa[:, t] | wb[:, t], value[:, t], last_value)
        last_bit = torch.where(is_bit[:, t], value[:, t], last_bit)
    if bool((a_val < 0).any() or (b_val < 0).any()):
        raise ValueError("every prefix must write both slots")
    return {"final": torch.stack((a_val, b_val), 1), "last_write_slot": last_slot,
            "last_write_value": last_value, "last_bit_value": last_bit}


def with_queries(prefix: Tensor) -> Tensor:
    """Stack identical prefixes with QUERY_A then QUERY_B: ``[2B, T+1]``."""
    b = prefix.shape[0]
    q = torch.cat((torch.full((b, 1), QUERY_A), torch.full((b, 1), QUERY_B))).long()
    return torch.cat((torch.cat((prefix, prefix)), q), dim=1)


# ---------------------------------------------------------------------- baselines
def shortcut_predictions(prefix: Tensor, *, seed: int) -> dict[str, Tensor]:
    """Rule-based predictions ``[B,2]`` from tokens; none receives labels."""
    r = replay_slots(prefix)
    b = prefix.shape[0]
    g = torch.Generator(device="cpu").manual_seed(seed)
    first_is_a = prefix[:, 0] == WRITE_A
    v1, v2 = prefix[:, 1] - BIT0, prefix[:, 3] - BIT0
    initial = torch.stack((torch.where(first_is_a, v1, v2), torch.where(first_is_a, v2, v1)), 1)
    # Sticky address: every bit token writes the most recently *named* slot.
    addr = torch.full((b,), -1, dtype=torch.long)
    sticky = torch.zeros(b, 2, dtype=torch.long)
    for t in range(prefix.shape[1]):
        tok = prefix[:, t]
        addr = torch.where(tok == WRITE_A, 0, torch.where(tok == WRITE_B, 1, addr))
        bit = ((tok == BIT0) | (tok == BIT1)) & (addr >= 0)
        for s in (0, 1):
            sticky[:, s] = torch.where(bit & (addr == s), tok - BIT0, sticky[:, s])
    return {
        "random": torch.randint(0, 2, (b, 2), generator=g),
        "last_marked_write": r["last_write_value"][:, None].expand(b, 2),
        "last_bit_token": r["last_bit_value"][:, None].expand(b, 2),
        "initial_values_only": initial,
        "sticky_address": sticky,
    }


def pair_scores(pred: Tensor, target: Tensor) -> dict:
    match = pred.eq(target)
    pair = match.all(1)
    unequal = target[:, 0] != target[:, 1]
    return {"paired_on_unequal": float(pair[unequal].float().mean()) if bool(unequal.any()) else None,
            "paired_all": float(pair.float().mean()),
            "paired_on_equal": float(pair[~unequal].float().mean()) if bool((~unequal).any()) else None,
            "slot_accuracy": [float(v) for v in match.float().mean(0)],
            "unequal_fraction": float(unequal.float().mean()),
            "unequal_count": int(unequal.sum())}


# -------------------------------------------------------------------------- models
def build_variant(name: str, seed: int) -> tuple[nn.Module, str | None]:
    if name not in VARIANTS:
        raise ValueError(f"unknown variant {name}")
    spec = VARIANTS[name]
    family = spec["family"]
    if family == "protected" or family == "stock":
        return build(name.removeprefix("oracle_tag_").removeprefix("oracle_route_"), seed), spec.get("oracle")
    if family == "event":
        cfg = EventGatedConfig(vocab_size=16, width=32, layers=2, protected_channels=8,
                               cell_type="protected", seed=seed, gate_mode=spec["gate_mode"],
                               token_shift=spec["token_shift"])
        return EventGatedLanguageModel(cfg).cpu(), None
    if family == "keep_gru":
        cfg = GatedConfig(vocab_size=16, width=32, layers=2, cell_type="gru", seed=seed)
        return KeepGatedGRULanguageModel(cfg, gate_mode=spec["gate_mode"], keep_bias=spec["keep_bias"]).cpu(), None
    raise AssertionError(family)


def oracle_write_masks(ids: Tensor, mode: str, layers: int, channels: int) -> Tensor:
    """DIAGNOSTIC ONLY: true write events from the reference replay rule.

    ``tag``: every protected channel may write only at marked value tokens (no
    slot identity). ``route``: first half of channels only at A writes, second
    half only at B writes. All other tokens are exactly closed.
    """
    if mode not in ORACLE_MODES or channels < 2:
        raise ValueError("invalid oracle mode")
    wa, wb = marked_writes(ids)
    b, t = ids.shape
    m = torch.zeros(b, t, channels)
    if mode == "tag":
        m[:] = (wa | wb)[..., None].float()
    else:
        m[..., :channels // 2] = wa[..., None].float()
        m[..., channels // 2:] = wb[..., None].float()
    return m[:, :, None, :].expand(b, t, layers, channels).contiguous()


def run_model(model: nn.Module, ids: Tensor, oracle: str | None, **kwargs):
    if oracle is None:
        return model(ids, **kwargs)
    c = model.config
    return model(ids, write_masks=oracle_write_masks(ids, oracle, c.layers, c.protected_channels), **kwargs)


def query_logits(model, ids, oracle):
    return run_model(model, ids, oracle)[0][:, -1, BIT0:BIT1 + 1]


def recurrent_state_floats(model, oracle) -> int:
    _, state = run_model(model, torch.full((1, 2), DISTRACTOR_START, dtype=torch.long), oracle)
    return int(flatten_recurrent_state(state).shape[1])


# ---------------------------------------------------------------------- evaluation
@torch.no_grad()
def evaluate_two_slot(model, oracle, delay: int, *, seed: int, histories: int,
                      chunk: int = 256, task: dict | None = None) -> dict:
    model.eval()
    prefix, record = make_two_slot_batch(delay, histories, seed=seed, **(task or {}))
    replay = replay_slots(prefix)
    target = replay["final"]
    preds = []
    for s in range(0, histories, chunk):
        part = prefix[s:s + chunk]
        lg = query_logits(model, with_queries(part), oracle)
        n = part.shape[0]
        preds.append(torch.stack((lg[:n].argmax(-1), lg[n:].argmax(-1)), 1))
    pred = torch.cat(preds)
    out = pair_scores(pred, target)
    ls = replay["last_write_slot"]
    m = pred.eq(target)
    out["last_updated_slot_accuracy"] = float(m.gather(1, ls[:, None]).float().mean())
    out["other_slot_accuracy"] = float(m.gather(1, (1 - ls)[:, None]).float().mean())
    out["predicts_same_for_both"] = float(pred[:, 0].eq(pred[:, 1]).float().mean())
    unequal = target[:, 0] != target[:, 1]
    out["paired_on_unequal_by_updates"] = {
        str(k): (float(m.all(1)[unequal & (record["updates"] == k)].float().mean())
                 if bool((unequal & (record["updates"] == k)).any()) else None) for k in (1, 2, 3)}
    out["baselines"] = {k: pair_scores(v, target)["paired_on_unequal"]
                        for k, v in shortcut_predictions(prefix, seed=seed + 7).items()}
    out["histories"] = histories
    return out


@torch.no_grad()
def evaluate_legacy(model, oracle, delay: int, *, seed: int, histories: int) -> dict:
    """Experiment 004-008 task (benign fillers, one midpoint update) for comparability."""
    model.eval()
    ids, _, meta = make_batch("selective", delay, histories, seed=seed)
    target = _slot_targets(ids[:, :-1], delay)
    lg = query_logits(model, with_queries(ids[:, :-1]), oracle)
    pred = torch.stack((lg[:histories].argmax(-1), lg[histories:].argmax(-1)), 1)
    out = pair_scores(pred, target)
    out["naive_last_write_on_unequal"] = 0.0
    return out


@torch.no_grad()
def final_states(model, oracle, prefix: Tensor, chunk: int = 256) -> Tensor:
    model.eval()
    out = []
    for s in range(0, prefix.shape[0], chunk):
        out.append(flatten_recurrent_state(run_model(model, prefix[s:s + chunk], oracle)[1]))
    return torch.cat(out)


def linear_state_probe(model, oracle, delay: int, *, seed: int, train_n: int, test_n: int,
                       transfer_delay: int, steps: int = 300) -> dict:
    """Held-out linear decodability of final A and B from the query-free state.

    The probe is extra supervised reading, not native task success. It is fit
    at the training delay and also applied unchanged at ``transfer_delay``.
    """
    xs, ys = {}, {}
    for split, d, n, s in (("train", delay, train_n, seed), ("test", delay, test_n, seed + 1),
                           ("transfer", transfer_delay, test_n, seed + 2)):
        prefix, _ = make_two_slot_batch(d, n, seed=s)
        xs[split] = final_states(model, oracle, prefix)
        ys[split] = replay_slots(prefix)["final"].float()
    mu, sd = xs["train"].mean(0), xs["train"].std(0) + 1e-5
    norm = {k: (v - mu) / sd for k, v in xs.items()}
    gen = torch.Generator().manual_seed(seed)
    w = (torch.randn(norm["train"].shape[1], 2, generator=gen) * 0.01).requires_grad_()
    bias = torch.zeros(2, requires_grad=True)
    opt = torch.optim.Adam([w, bias], lr=.05)
    with torch.enable_grad():
        for _ in range(steps):
            opt.zero_grad()
            loss = F.binary_cross_entropy_with_logits(norm["train"] @ w + bias, ys["train"]) + 1e-3 * w.square().sum()
            loss.backward()
            opt.step()
    result = {"features": int(norm["train"].shape[1])}
    with torch.no_grad():
        for split in ("train", "test", "transfer"):
            pred = ((norm[split] @ w + bias) > 0).long()
            sc = pair_scores(pred, ys[split].long())
            result[split] = {"paired_on_unequal": sc["paired_on_unequal"], "slot_accuracy": sc["slot_accuracy"]}
    result["transfer_delay"] = transfer_delay
    return result


@torch.no_grad()
def gate_diagnostics(model, oracle, delay: int, *, seed: int, histories: int = 256) -> dict | None:
    """Mean write/update gate by token class, measured on the actual forward pass.

    Protected family: slow write gate (times oracle mask when present).
    GRU family: ``1 - keep`` (the fraction of a unit that is overwritten).
    ``log_retention_per_nonwrite_token`` averages ``log(1-g)`` over non-write
    tokens; exp(512x) gives the implied surviving fraction after 512 tokens.
    """
    model.eval()
    prefix, _ = make_two_slot_batch(delay, histories, seed=seed)
    wa, wb = marked_writes(prefix)
    write = wa | wb
    is_bit = (prefix == BIT0) | (prefix == BIT1)
    classes = {"marked_value": write, "unmarked_bit": is_bit & ~write,
               "write_marker": (prefix == WRITE_A) | (prefix == WRITE_B),
               "benign_distractor": (prefix >= DISTRACTOR_START) & (prefix < DISTRACTOR_END)}
    _, _, history = run_model(model, prefix, oracle, return_history=True)  # [B,T,L,W]
    x = model.embedding(prefix)
    layers = []
    masks = None
    if oracle is not None:
        masks = oracle_write_masks(prefix, oracle, model.config.layers, model.config.protected_channels)
    for i, (cell, norm) in enumerate(zip(model.cells, model.norms)):
        if isinstance(cell, EventGatedProtectedCell):
            prev = torch.cat((torch.zeros_like(x[:, :1]), x[:, :-1]), 1) if cell.config.token_shift else None
            gate = cell.prepare(x, prev)[1]
        elif isinstance(cell, ProtectedMemoryCell):
            gate = cell.prepare(x)[1]
            if masks is not None:
                gate = gate * masks[:, :, i]
        elif isinstance(cell, nn.GRUCell):
            h_prev = torch.cat((torch.zeros_like(history[:, :1, i]), history[:, :-1, i]), 1)
            w = cell.hidden_size
            logits = (F.linear(x, cell.weight_ih[w:2 * w], cell.bias_ih[w:2 * w])
                      + F.linear(h_prev, cell.weight_hh[w:2 * w], cell.bias_hh[w:2 * w]))
            hard = getattr(cell, "gate_mode", "soft") == "hard"
            keep = (logits > 0).float() if hard else torch.sigmoid(logits)
            gate = 1 - keep
        else:
            return None
        row = {}
        for name, sel in classes.items():
            g = gate[sel]
            row[name] = {"mean": float(g.mean()) if g.numel() else None,
                         "fraction_exactly_zero": float((g == 0).float().mean()) if g.numel() else None}
        nonwrite = gate[~write].clamp(max=1 - 1e-7)
        lr = float(torch.log1p(-nonwrite).mean())
        row["log_retention_per_nonwrite_token"] = lr
        row["implied_retention_after_512_nonwrite_tokens"] = math.exp(512 * lr)
        layers.append(row)
        x = norm(history[:, :, i])
    return {"layers": layers}


def _map_state(state, fn):
    out = []
    for s in state:
        if isinstance(s, (LSTMState, ShiftState)):
            out.append(type(s)(*(fn(v) for v in s)))
        else:
            out.append(fn(s))
    return tuple(out)


def distractor_tail(length: int, batch: int, *, seed: int, unmarked_bit_rate: float = .25) -> Tensor:
    """Benign distractors and unmarked (conflicting) bits only; no marked writes."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    tail = torch.randint(DISTRACTOR_START, DISTRACTOR_END, (batch, length), generator=g)
    bits = torch.randint(0, 2, (batch, length), generator=g) + BIT0
    return torch.where(torch.rand((batch, length), generator=g) < unmarked_bit_rate, bits, tail).long()


@torch.no_grad()
def perturbation_recovery(model, oracle, delay: int, *, seed: int, histories: int = 512,
                          tail: int = 64, noise: tuple[float, ...] = (0.5, 1.0)) -> dict:
    """Is the stored pair error-correcting (attractor-like) or only passively held?

    After the full prefix, add Gaussian noise scaled by ``noise`` times each state
    feature's RMS, then query either immediately or after ``tail`` additional
    distractor tokens. Recovery (after-tail accuracy above immediate accuracy)
    indicates a restoring force; a passive integrator cannot recover.
    """
    model.eval()
    prefix, _ = make_two_slot_batch(delay, histories, seed=seed)
    target = replay_slots(prefix)["final"]
    rest = distractor_tail(tail, histories, seed=seed + 1)
    _, state = run_model(model, prefix, oracle)
    flat = flatten_recurrent_state(state)
    gen = torch.Generator(device="cpu").manual_seed(seed + 2)

    def answer(st, extra):
        if extra is not None:
            _, st = run_model(model, extra, oracle, state=st)
        both = _map_state(st, lambda v: torch.cat((v, v)))
        q = torch.cat((torch.full((histories, 1), QUERY_A), torch.full((histories, 1), QUERY_B))).long()
        lg = run_model(model, q, oracle, state=both)[0][:, -1, BIT0:BIT1 + 1]
        pred = torch.stack((lg[:histories].argmax(-1), lg[histories:].argmax(-1)), 1)
        return pair_scores(pred, target)["paired_on_unequal"]

    out = {"clean_immediate": answer(state, None), "clean_after_tail": answer(state, rest), "tail": tail}
    for level in noise:
        def perturb(v):
            rms = v.square().mean(0, keepdim=True).sqrt()
            return v + level * rms * torch.randn(v.shape, generator=gen, dtype=v.dtype)
        noisy = _map_state(state, perturb)
        out[f"noise_{level}"] = {"immediate": answer(noisy, None), "after_tail": answer(noisy, rest)}
    out["state_rms"] = float(flat.square().mean().sqrt())
    return out


# ------------------------------------------------------------------------ training
@dataclass(frozen=True)
class Config:
    variants: tuple[str, ...] = tuple(VARIANTS)
    legacy_variants: tuple[str, ...] = ()
    seeds: tuple[int, ...] = (17, 29, 43)
    train_delay: int = 64
    eval_delays: tuple[int, ...] = (32, 64, 128, 256, 512)
    legacy_delays: tuple[int, ...] = (64, 128, 256)
    steps: int = 2000
    batch_histories: int = 16
    lr: float = .002
    grad_clip: float = 1.0
    checkpoint_every: int = 250
    checkpoint_histories: int = 256
    eval_histories: int = 512
    probe_train: int = 2048
    probe_test: int = 1024
    workers: int = 1
    max_wall_seconds: float = 3000.0

    def __post_init__(self):
        if not self.variants or len(set(self.variants)) != len(self.variants) or any(v not in VARIANTS for v in self.variants):
            raise ValueError("invalid variants")
        if len(set(self.legacy_variants)) != len(self.legacy_variants) or any(v not in VARIANTS for v in self.legacy_variants):
            raise ValueError("invalid legacy-trained variants")
        if not self.seeds or len(set(self.seeds)) != len(self.seeds) or any(type(s) is not int or s < 0 for s in self.seeds):
            raise ValueError("invalid seeds")
        if any(type(d) is not int or d < 7 for d in (self.train_delay, *self.eval_delays)):
            raise ValueError("two-slot delays must be integers >= 7")
        if any(type(d) is not int or d < 2 for d in self.legacy_delays):
            raise ValueError("invalid legacy delays")
        if any(type(v) is not int or v < 1 for v in (self.steps, self.batch_histories, self.checkpoint_every,
                                                       self.checkpoint_histories, self.eval_histories,
                                                       self.probe_train, self.probe_test, self.workers)):
            raise ValueError("counts must be positive integers")
        if any(not math.isfinite(v) or v <= 0 for v in (self.lr, self.grad_clip, self.max_wall_seconds)):
            raise ValueError("lr, clip and wall budget must be positive")


def batch_seed(seed: int, step: int, delay: int) -> int:
    """Shared across variants for a seed: every model sees identical examples."""
    return seed * 1_000_003 + step * 8191 + delay * 17 + 909


def training_batch(task: str, seed: int, step: int, cfg: Config) -> tuple[Tensor, Tensor]:
    """Paired A/B queries on identical prefixes; labels from token replay only."""
    if task == "two_slot":
        prefix, _ = make_two_slot_batch(cfg.train_delay, cfg.batch_histories,
                                        seed=batch_seed(seed, step, cfg.train_delay))
        target = replay_slots(prefix)["final"]
        return with_queries(prefix), torch.cat((target[:, 0], target[:, 1]))
    if task == "legacy":  # Experiment 004-008 generator: one midpoint update, benign fillers
        ids, y, _ = _paired_inputs(cfg.train_delay, cfg.batch_histories,
                                   seed=batch_seed(seed, step, cfg.train_delay) + 1)
        return ids, y
    raise ValueError("unknown training task")


def train_and_evaluate(name: str, seed: int, cfg: Config, deadline: float, train_task: str = "two_slot") -> dict:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(0)
    began = time.monotonic()
    model, oracle = build_variant(name, seed)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    losses, curve, done, status = [], [], 0, "complete"
    grad_norms = []
    held_out = seed + 1_000_000
    for step in range(cfg.steps):
        if time.time() >= deadline:
            status = "wall_budget"
            break
        model.train()
        ids, y = training_batch(train_task, seed, step, cfg)
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(query_logits(model, ids, oracle), y)
        if not bool(torch.isfinite(loss)):
            status = "nonfinite_loss"
            break
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
            status = "nonfinite_gradient"
            break
        grad_norms.append(float(torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)))
        opt.step()
        losses.append(float(loss.detach()))
        done += 1
        if done % cfg.checkpoint_every == 0:
            ev = evaluate_two_slot(model, oracle, cfg.train_delay, seed=held_out + 500_000,
                                   histories=cfg.checkpoint_histories)
            curve.append({"step": done, "paired_on_unequal": ev["paired_on_unequal"],
                          "paired_all": ev["paired_all"],
                          "predicts_same_for_both": ev["predicts_same_for_both"]})
    train_seconds = time.monotonic() - began
    row = {"variant": name, "train_task": train_task, "seed": seed, "oracle": oracle, "status": status,
           "steps_requested": cfg.steps, "steps_completed": done, "complete": status == "complete",
           "parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
           "recurrent_state_floats": recurrent_state_floats(model, oracle),
           "loss_first": losses[0] if losses else None, "loss_last": losses[-1] if losses else None,
           "loss_by_50": [sum(losses[i:i + 50]) / len(losses[i:i + 50]) for i in range(0, len(losses), 50)],
           "max_grad_norm_preclip": max(grad_norms) if grad_norms else None,
           "checkpoints": curve, "train_seconds": train_seconds}
    for thresh in (.9, .99):
        hit = next((c["step"] for c in curve if (c["paired_on_unequal"] or 0) >= thresh), None)
        row[f"first_checkpoint_unequal_ge_{thresh}"] = hit
    if status in ("complete", "wall_budget") and done > 0:
        t0 = time.monotonic()
        row["two_slot"] = {str(d): evaluate_two_slot(model, oracle, d, seed=held_out, histories=cfg.eval_histories)
                           for d in cfg.eval_delays}
        row["legacy"] = {str(d): evaluate_legacy(model, oracle, d, seed=held_out, histories=cfg.eval_histories)
                         for d in cfg.legacy_delays}
        row["probe"] = linear_state_probe(model, oracle, cfg.train_delay, seed=seed + 3_000_000,
                                          train_n=cfg.probe_train, test_n=cfg.probe_test,
                                          transfer_delay=4 * cfg.train_delay)
        row["gates"] = gate_diagnostics(model, oracle, cfg.train_delay, seed=seed + 4_000_000)
        row["perturbation"] = perturbation_recovery(model, oracle, cfg.train_delay, seed=seed + 5_000_000,
                                                    histories=cfg.eval_histories)
        row["eval_seconds"] = time.monotonic() - t0
    row["elapsed_seconds"] = time.monotonic() - began
    return row


def _job(args):
    task, name, seed, cfg_dict, deadline = args
    cfg = Config(**{k: tuple(v) if isinstance(v, list) else v for k, v in cfg_dict.items()})
    try:
        return train_and_evaluate(name, seed, cfg, deadline, task)
    except Exception as exc:  # preserve failures as evidence, never silently drop
        return {"variant": name, "train_task": task, "seed": seed,
                "status": f"error: {type(exc).__name__}: {exc}", "complete": False}


def source_hashes() -> dict:
    here = Path(__file__).resolve().parent
    return {p: hashlib.sha256((here / p).read_bytes()).hexdigest()
            for p in ("experiment_009.py", "event_gated.py", "candidates.py", "gated.py", "learning_pilot.py")}


def execute(cfg: Config, *, output: Path, progress: Path | None = None) -> dict:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    began = time.monotonic()
    deadline = time.time() + cfg.max_wall_seconds
    report = {"status": "running", "config": asdict(cfg),
              "environment": {"torch": torch.__version__, "python": platform.python_version(),
                              "device": "cpu", "cuda_visible": os.environ.get("CUDA_VISIBLE_DEVICES"),
                              "cpu_count": os.cpu_count(), "workers": cfg.workers,
                              "threads_per_worker": 1},
              "sources_sha256": source_hashes(),
              "scope": "synthetic two-slot supervised CPU study; oracle arms are upper-bound diagnostics; NOT formal D",
              "runs": [], "skipped": []}
    jobs = ([("two_slot", v, s, asdict(cfg), deadline) for s in cfg.seeds for v in cfg.variants]
            + [("legacy", v, s, asdict(cfg), deadline) for s in cfg.seeds for v in cfg.legacy_variants])
    try:
        ctx = mp.get_context("spawn")
        with ctx.Pool(cfg.workers, maxtasksperchild=1) as pool:
            for row in pool.imap_unordered(_job, jobs):
                report["runs"].append(row)
                if progress is not None:
                    with progress.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(row) + "\n")
                two = row.get("two_slot", {})
                print(json.dumps({"done": len(report["runs"]), "of": len(jobs), "task": row["train_task"],
                                  "variant": row["variant"],
                                  "seed": row["seed"], "status": row["status"],
                                  "unequal_by_delay": {d: v["paired_on_unequal"] for d, v in two.items()},
                                  "seconds": round(row.get("elapsed_seconds", 0), 1)}), flush=True)
        order = list(cfg.variants) + list(cfg.legacy_variants)
        report["runs"].sort(key=lambda r: (TRAIN_TASKS.index(r["train_task"]), cfg.seeds.index(r["seed"]),
                                           order.index(r["variant"])))
        report["status"] = "complete" if all(r.get("complete") for r in report["runs"]) and len(report["runs"]) == len(jobs) else "incomplete"
    finally:
        report["elapsed_seconds"] = time.monotonic() - began
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--progress", type=Path)
    p.add_argument("--variants", default=",".join(VARIANTS))
    p.add_argument("--legacy-variants", default="")
    p.add_argument("--seeds", default="17,29,43")
    p.add_argument("--train-delay", type=int, default=64)
    p.add_argument("--eval-delays", default="32,64,128,256,512")
    p.add_argument("--legacy-delays", default="64,128,256")
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--lr", type=float, default=.002)
    p.add_argument("--checkpoint-every", type=int, default=250)
    p.add_argument("--checkpoint-histories", type=int, default=256)
    p.add_argument("--eval-histories", type=int, default=512)
    p.add_argument("--probe-train", type=int, default=2048)
    p.add_argument("--probe-test", type=int, default=1024)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--max-wall-seconds", type=float, default=3000)
    a = p.parse_args(argv)
    ints = lambda s: tuple(int(x) for x in s.split(",") if x)
    cfg = Config(variants=tuple(x for x in a.variants.split(",") if x),
                 legacy_variants=tuple(x for x in a.legacy_variants.split(",") if x), seeds=ints(a.seeds),
                 train_delay=a.train_delay, eval_delays=ints(a.eval_delays), legacy_delays=ints(a.legacy_delays),
                 steps=a.steps, batch_histories=a.batch, lr=a.lr, checkpoint_every=a.checkpoint_every,
                 checkpoint_histories=a.checkpoint_histories, eval_histories=a.eval_histories,
                 probe_train=a.probe_train, probe_test=a.probe_test, workers=a.workers,
                 max_wall_seconds=a.max_wall_seconds)
    r = execute(cfg, output=a.output, progress=a.progress)
    print(f"Experiment 009: {r['status']}; runs={len(r['runs'])}; seconds={r['elapsed_seconds']:.1f}")


if __name__ == "__main__":
    main()
