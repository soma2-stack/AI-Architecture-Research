"""Standard PyTorch GRU/LSTM language-model comparison candidates.

The original and theory-inspired implementations remain separate. These
wrappers use PyTorch's reference ``nn.GRUCell`` and ``nn.LSTMCell`` operators,
the existing embedding/LayerNorm/tied-head convention, and explicit caller-
owned streaming state. They do not contain an optimizer or update parameters.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import NamedTuple, Sequence

import torch
from torch import Tensor, nn
import torch.nn.functional as F


@dataclass(frozen=True)
class GatedConfig:
    vocab_size: int = 97
    width: int = 32
    layers: int = 2
    cell_type: str = "gru"  # gru or lstm
    precision: str = "float32"
    seed: int = 20261007

    def __post_init__(self):
        for name in ("vocab_size", "width", "layers"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if self.cell_type not in ("gru", "lstm"):
            raise ValueError("cell_type must be 'gru' or 'lstm'")
        if self.precision not in ("float32", "float64"):
            raise ValueError("precision must be float32 or float64")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError("seed must be an integer")


class LSTMState(NamedTuple):
    """One layer's explicit LSTM hidden activation and cell memory."""

    hidden: Tensor
    cell: Tensor


GatedState = Tensor | LSTMState


class GatedLanguageModel(nn.Module):
    """Stacked standard GRU/LSTM with the prototype's shared token interface.

    ``forward`` accepts token IDs shaped ``[B,T]`` and optional per-layer
    state. GRU state is one ``[B,W]`` tensor per layer; LSTM state is one
    ``LSTMState(hidden, cell)`` pair per layer. Resets occur before the marked
    token and clear both LSTM components. State is returned, never cached.
    """

    def __init__(self, config: GatedConfig):
        super().__init__()
        self.config = config
        dtype = getattr(torch, config.precision)
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(config.seed)
            self.embedding = nn.Embedding(config.vocab_size, config.width, dtype=dtype)
            nn.init.normal_(self.embedding.weight, std=config.width ** -0.5)
            cell = nn.GRUCell if config.cell_type == "gru" else nn.LSTMCell
            self.cells = nn.ModuleList(
                cell(config.width, config.width, dtype=dtype)
                for _ in range(config.layers)
            )
            self.norms = nn.ModuleList(
                nn.LayerNorm(config.width, dtype=dtype) for _ in self.cells
            )
            self.final_norm = nn.LayerNorm(config.width, dtype=dtype)

    @property
    def trainable_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def initial_state(self, batch_size: int, *, device=None, dtype=None):
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        p, w = self.embedding.weight, self.config.width
        device = p.device if device is None else device
        dtype = p.dtype if dtype is None else dtype
        states = []
        for _ in self.cells:
            hidden = torch.zeros(batch_size, w, device=device, dtype=dtype)
            if self.config.cell_type == "lstm":
                states.append(LSTMState(hidden, torch.zeros_like(hidden)))
            else:
                states.append(hidden)
        return tuple(states)

    @staticmethod
    def detach_state(state: Sequence[GatedState]):
        if all(isinstance(s, Tensor) for s in state):
            return tuple(s.detach() for s in state)
        if all(isinstance(s, LSTMState) for s in state):
            return tuple(LSTMState(s.hidden.detach(), s.cell.detach()) for s in state)
        raise ValueError("state must consistently contain GRU tensors or LSTMState pairs")

    def _validate_state(self, state, batch_size: int):
        p, c = self.embedding.weight, self.config
        if not isinstance(state, (tuple, list)) or len(state) != c.layers:
            raise ValueError("state must contain one state per recurrent layer")
        for layer_state in state:
            values = ((layer_state.hidden, layer_state.cell)
                      if isinstance(layer_state, LSTMState) else (layer_state,))
            if (c.cell_type == "lstm") != isinstance(layer_state, LSTMState):
                raise ValueError("state type must match configured recurrent cell")
            for value in values:
                if (not isinstance(value, Tensor) or value.shape != (batch_size, c.width)
                        or value.dtype != p.dtype or value.device != p.device):
                    raise ValueError("state tensors must match batch, width, dtype and model device")
        return tuple(state)

    def _scan_features(self, inputs: Tensor, state, reset_mask: Tensor | None = None):
        """Run already embedded features; also used by shared cell diagnostics."""
        p, c = self.embedding.weight, self.config
        if (not isinstance(inputs, Tensor) or inputs.ndim != 3
                or inputs.shape[0] < 1 or inputs.shape[2] != c.width
                or inputs.device != p.device or inputs.dtype != p.dtype):
            raise ValueError("features must be [positive batch,time,width] on model device and dtype")
        batch, steps, _ = inputs.shape
        state = self.initial_state(batch) if state is None else self._validate_state(state, batch)
        if reset_mask is not None and (reset_mask.shape != (batch, steps)
                or reset_mask.dtype != torch.bool or reset_mask.device != p.device):
            raise ValueError("reset_mask must be [batch,time] bool on model device")
        if steps == 0:
            return (p.new_empty(batch, 0, c.width), tuple(state),
                    p.new_empty(batch, 0, c.layers, c.width))

        outputs, histories = [], []
        for t in range(steps):
            if reset_mask is not None:
                keep = ~reset_mask[:, t, None]
                if c.cell_type == "lstm":
                    state = tuple(LSTMState(torch.where(keep, s.hidden, torch.zeros_like(s.hidden)),
                                            torch.where(keep, s.cell, torch.zeros_like(s.cell)))
                                  for s in state)
                else:
                    state = tuple(torch.where(keep, s, torch.zeros_like(s)) for s in state)
            x = inputs[:, t]
            hidden_at_layers = []
            updated = []
            for cell, norm, previous in zip(self.cells, self.norms, state):
                if c.cell_type == "lstm":
                    hidden, memory = cell(x, (previous.hidden, previous.cell))
                    updated.append(LSTMState(hidden, memory))
                else:
                    hidden = cell(x, previous)
                    updated.append(hidden)
                hidden_at_layers.append(hidden)
                x = norm(hidden)
            state = tuple(updated)
            outputs.append(x)
            histories.append(torch.stack(hidden_at_layers, dim=1))
        return torch.stack(outputs, dim=1), state, torch.stack(histories, dim=1)

    def forward_features(self, inputs: Tensor, state=None, *, reset_mask=None):
        """Cell-level diagnostic interface for common real-valued scans."""
        _, state, history = self._scan_features(inputs, state, reset_mask)
        return state, history

    def forward(self, input_ids: Tensor, state=None, *, return_history=False,
                reset_mask: Tensor | None = None):
        p, c = self.embedding.weight, self.config
        if (not isinstance(input_ids, Tensor) or input_ids.ndim != 2
                or input_ids.dtype != torch.long or input_ids.shape[0] < 1
                or input_ids.device != p.device):
            raise ValueError("input_ids must be [positive batch,time] int64 on model device")
        if input_ids.numel() and (input_ids.min() < 0 or input_ids.max() >= c.vocab_size):
            raise ValueError("input_ids contain an out-of-vocabulary token")
        outputs, final_state, history = self._scan_features(
            self.embedding(input_ids), state, reset_mask
        )
        logits = F.linear(self.final_norm(outputs), p)
        return (logits, final_state, history) if return_history else (logits, final_state)
