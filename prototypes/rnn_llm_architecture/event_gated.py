"""Experiment 009 variants: exactly-closable (event-gated) memory writes; no training.

Diagnosis motivating this module (see EXPERIMENT_009_PLAN.md): the original
protected cell writes its slow coefficients with ``sigmoid`` gates. A sigmoid
is never exactly zero, so every non-write token leaks ``g`` of each protected
coefficient toward the current proposal and retention decays like
``(1-g)^T``. An oracle mask that only *closes* the gates on non-write tokens
(no slot routing) made two-slot memory trainable in an exploratory pilot.

This module tests whether a *learned* gate that can be exactly zero supplies
the same property without oracle information:

* ``gate_mode="hard"``: forward write gate is the Heaviside step
  ``1[logit > 0]``; the backward pass uses the sigmoid derivative
  (straight-through estimator). A closed coefficient receives an exactly
  zero write (re-reading it from ``h`` is exact up to projection roundoff).
* ``token_shift=True``: gate logits additionally read the previous layer
  input ``x_{t-1}`` (zero-initialized weights), so the decision to write at a
  value token can depend on the address/tag token that preceded it. The
  previous input is carried explicitly in the recurrent state.

Known prior art, NOT claimed as a new primitive: binary update gates with
straight-through gradients and exact state copying (Skip RNN, Campos et al.
2018; HM-RNN COPY operation, Chung et al. 2017; straight-through estimator,
Bengio et al. 2013) and token shift (RWKV; short causal convolutions in
H3/Mamba). ``StraightThroughGRUCell`` applies the same hard keep-gate to a
standard GRU so the protected subspace can be separated from hard gating.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, Sequence

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from .candidates import CandidateConfig, CandidateLanguageModel, ProtectedMemoryCell
from .gated import GatedConfig, GatedLanguageModel

GATE_MODES = ("soft", "hard")


def straight_through_step(logits: Tensor) -> Tensor:
    """Forward ``1[logits > 0]`` exactly; backward ``sigmoid'(logits)``."""
    soft = torch.sigmoid(logits)
    hard = (logits > 0).to(logits.dtype)
    return hard + (soft - soft.detach())


@dataclass(frozen=True)
class EventGatedConfig(CandidateConfig):
    gate_mode: str = "hard"
    token_shift: bool = False

    def __post_init__(self):
        super().__post_init__()
        if self.cell_type != "protected":
            raise ValueError("event-gated memory requires cell_type='protected'")
        if self.gate_mode not in GATE_MODES:
            raise ValueError("gate_mode must be 'soft' or 'hard'")
        if not isinstance(self.token_shift, bool):
            raise ValueError("token_shift must be boolean")


class ShiftState(NamedTuple):
    """One layer's protected hidden state plus the previous layer input."""

    hidden: Tensor
    previous_input: Tensor


class EventGatedProtectedCell(ProtectedMemoryCell):
    """Original protected recurrence; only the slow write-gate function changes.

    With ``gate_mode='soft'`` and ``token_shift=False`` this is numerically the
    original cell. The proposal, fast complement and projection are inherited.
    """

    def __init__(self, config: EventGatedConfig):
        if not isinstance(config, EventGatedConfig):
            raise TypeError("EventGatedConfig required")
        super().__init__(config)
        if config.token_shift:
            self.previous_to_gate = nn.Linear(config.width, config.protected_channels, bias=False,
                                              dtype=getattr(torch, config.precision))
            nn.init.zeros_(self.previous_to_gate.weight)

    def gate_logits(self, x: Tensor, previous: Tensor | None = None) -> Tensor:
        logits = self.slow_gate(x)
        if self.config.token_shift:
            if previous is None or previous.shape != x.shape:
                raise ValueError("token-shift gate requires previous input of the same shape")
            logits = logits + self.previous_to_gate(previous)
        return logits

    def prepare(self, x: Tensor, previous: Tensor | None = None):
        logits = self.gate_logits(x, previous)
        gate = straight_through_step(logits) if self.config.gate_mode == "hard" else torch.sigmoid(logits)
        return self.x_to_candidate(x), gate, torch.sigmoid(self.fast_gate(x))

    def forward(self, x: Tensor, h: Tensor, *, previous: Tensor | None = None, write_mask=None):
        return self.step(self.prepare(x, previous), h, write_mask)


class EventGatedLanguageModel(CandidateLanguageModel):
    """Protected token model with event-gated cells and explicit streaming state.

    Construction first builds the original seeded protected model and copies its
    weights, so every variant starts from the same parameters as
    ``protected_w32`` for a given seed; token-shift weights start at zero.
    State per layer is a tensor, or ``ShiftState`` when ``token_shift``.
    """

    def __init__(self, config: EventGatedConfig):
        if not isinstance(config, EventGatedConfig):
            raise TypeError("EventGatedConfig required")
        super().__init__(config)
        cells = []
        for original in self.cells:
            cell = EventGatedProtectedCell(config)
            result = cell.load_state_dict(original.state_dict(), strict=False)
            expected = {"previous_to_gate.weight"} if config.token_shift else set()
            if set(result.missing_keys) != expected or result.unexpected_keys:
                raise RuntimeError("protected weight migration failed")
            cells.append(cell)
        self.cells = nn.ModuleList(cells)

    def initial_state(self, batch_size: int, *, device=None, dtype=None):
        base = super().initial_state(batch_size, device=device, dtype=dtype)
        if not self.config.token_shift:
            return base
        return tuple(ShiftState(h, torch.zeros_like(h)) for h in base)

    @staticmethod
    def detach_state(state: Sequence):
        return tuple(ShiftState(s.hidden.detach(), s.previous_input.detach())
                     if isinstance(s, ShiftState) else s.detach() for s in state)

    def _check_state(self, state, batch: int):
        p, c = self.embedding.weight, self.config
        if not isinstance(state, (tuple, list)) or len(state) != c.layers:
            raise ValueError("state must contain one entry per layer")
        for s in state:
            if c.token_shift != isinstance(s, ShiftState):
                raise ValueError("state type must match token_shift configuration")
            for v in (s if isinstance(s, ShiftState) else (s,)):
                if (not isinstance(v, Tensor) or v.shape != (batch, c.width)
                        or v.dtype != p.dtype or v.device != p.device):
                    raise ValueError("state tensors must match batch, width, dtype and device")
        return tuple(state)

    def forward(self, input_ids: Tensor, state=None, *, return_history=False,
                reset_mask: Tensor | None = None, write_masks: Tensor | None = None):
        p, c = self.embedding.weight, self.config
        if (not isinstance(input_ids, Tensor) or input_ids.ndim != 2
                or input_ids.dtype != torch.long or input_ids.shape[0] < 1
                or input_ids.device != p.device):
            raise ValueError("input_ids must be [positive batch,time] int64 on model device")
        b, t = input_ids.shape
        state = self.initial_state(b) if state is None else self._check_state(state, b)
        if reset_mask is not None and (reset_mask.shape != (b, t) or reset_mask.dtype != torch.bool
                                       or reset_mask.device != p.device):
            raise ValueError("reset_mask must be [batch,time] bool on model device")
        if write_masks is not None and write_masks.shape != (b, t, c.layers, c.protected_channels):
            raise ValueError("write_masks must be [batch,time,layers,channels]")
        if t == 0:
            output = (p.new_empty(b, 0, c.vocab_size), tuple(state))
            return (*output, p.new_empty(b, 0, c.layers, c.width)) if return_history else output
        x, last, histories = self.embedding(input_ids), [], []
        for i, (cell, norm) in enumerate(zip(self.cells, self.norms)):
            layer_state = state[i]
            h = layer_state.hidden if c.token_shift else layer_state
            previous = None
            if c.token_shift:
                previous = torch.cat((layer_state.previous_input[:, None], x[:, :-1]), dim=1)
                if reset_mask is not None:
                    previous = torch.where(reset_mask[..., None], torch.zeros_like(previous), previous)
            prepared = cell.prepare(x, previous)
            sequence = []
            for j in range(t):
                if reset_mask is not None:
                    h = torch.where(reset_mask[:, j, None], torch.zeros_like(h), h)
                mask = None if write_masks is None else write_masks[:, j, i]
                h = cell.step(tuple(v[:, j] for v in prepared), h, mask)
                sequence.append(h)
            raw = torch.stack(sequence, dim=1)
            last.append(ShiftState(h, x[:, -1]) if c.token_shift else h)
            x = norm(raw)
            if return_history:
                histories.append(raw)
        output = (F.linear(self.final_norm(x), p), tuple(last))
        return (*output, torch.stack(histories, dim=2)) if return_history else output


class StraightThroughGRUCell(nn.GRUCell):
    """PyTorch GRU equations with an optional hard (straight-through) keep gate.

    ``h' = (1-z) * n + z * h`` as in ``nn.GRUCell``. ``keep_bias`` is added to
    the update-gate bias so that ``z`` starts near one (copy), mirroring the
    protected cell's ``-3`` write bias. With ``gate_mode='hard'`` a unit with
    ``z=1`` copies its value bit-exactly.
    """

    def __init__(self, input_size: int, hidden_size: int, *, gate_mode: str = "hard",
                 keep_bias: float = 3.0, dtype=torch.float32):
        if gate_mode not in GATE_MODES:
            raise ValueError("gate_mode must be 'soft' or 'hard'")
        super().__init__(input_size, hidden_size, dtype=dtype)
        self.gate_mode = gate_mode
        self.keep_bias = float(keep_bias)

    def shift_keep_bias(self):
        w = self.hidden_size
        with torch.no_grad():
            self.bias_ih[w:2 * w] += self.keep_bias

    def forward(self, x: Tensor, h: Tensor | None = None) -> Tensor:
        if h is None:
            h = x.new_zeros(x.shape[0], self.hidden_size)
        gi = F.linear(x, self.weight_ih, self.bias_ih)
        gh = F.linear(h, self.weight_hh, self.bias_hh)
        i_r, i_z, i_n = gi.chunk(3, dim=-1)
        h_r, h_z, h_n = gh.chunk(3, dim=-1)
        r = torch.sigmoid(i_r + h_r)
        logits = i_z + h_z
        z = straight_through_step(logits) if self.gate_mode == "hard" else torch.sigmoid(logits)
        n = torch.tanh(i_n + r * h_n)
        return (1 - z) * n + z * h


class KeepGatedGRULanguageModel(GatedLanguageModel):
    """Same seeded weights as ``GatedLanguageModel`` GRU plus keep-bias shift."""

    def __init__(self, config: GatedConfig, *, gate_mode: str = "hard", keep_bias: float = 3.0):
        if config.cell_type != "gru":
            raise ValueError("keep-gated wrapper requires a GRU configuration")
        super().__init__(config)
        cells = []
        for original in self.cells:
            cell = StraightThroughGRUCell(config.width, config.width, gate_mode=gate_mode,
                                          keep_bias=keep_bias, dtype=getattr(torch, config.precision))
            cell.load_state_dict(original.state_dict(), strict=True)
            cell.shift_keep_bias()
            cells.append(cell)
        self.cells = nn.ModuleList(cells)
