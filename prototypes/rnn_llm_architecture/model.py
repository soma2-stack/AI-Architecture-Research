"""Small, untrained recurrent language-model architectures for controlled research.

These cells are engineering surrogates, NOT the exact frozen dense-tanh legal-query
constructions or proofs in theory/CURRENT_THEORY.md. No training is performed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import torch
from torch import Tensor, nn
import torch.nn.functional as F


@dataclass(frozen=True)
class RNNConfig:
    vocab_size: int = 8192
    width: int = 256
    layers: int = 2
    cell_type: str = "protected"  # "tanh", "near_critical", or "protected"
    protected_channels: int = 8

    def __post_init__(self) -> None:
        for name in ("vocab_size", "width", "layers"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"{name} must be an integer")
        if self.vocab_size < 2 or self.width < 2 or self.layers < 1:
            raise ValueError("vocab_size>=2, width>=2, and layers>=1 are required")
        if self.cell_type not in ("tanh", "near_critical", "protected"):
            raise ValueError("cell_type must be tanh, near_critical, or protected")
        if self.cell_type == "protected":
            if (not isinstance(self.protected_channels, int)
                    or isinstance(self.protected_channels, bool)):
                raise ValueError("protected_channels must be an integer")
            if self.width & (self.width - 1):
                raise ValueError("protected cell requires a power-of-two width")
            if not 1 <= self.protected_channels <= self.width // 2:
                raise ValueError("protected_channels must be 1..width/2")


class TanhCell(nn.Module):
    """Trainable dense tanh recurrence (ordinary baseline)."""

    def __init__(self, width: int) -> None:
        super().__init__()
        self.x_to_h = nn.Linear(width, width)
        self.h_to_h = nn.Linear(width, width, bias=False)
        nn.init.orthogonal_(self.h_to_h.weight)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        return torch.tanh(self.x_to_h(x) + self.h_to_h(h))


class NearCriticalTanhCell(nn.Module):
    """Frozen orthogonal recurrence with ||W||_2=1-1/width at initialization.

    This is a near-critical *surrogate*, not the specified dense corridor.
    Input weights and bias remain trainable; recurrent matrix is frozen.
    """

    def __init__(self, width: int) -> None:
        super().__init__()
        self.x_to_h = nn.Linear(width, width)
        q, _ = torch.linalg.qr(torch.randn(width, width))
        self.register_buffer("recurrent", (1.0 - 1.0 / width) * q)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        return torch.tanh(self.x_to_h(x) + F.linear(h, self.recurrent))


def sum_free_walsh_bank(width: int, channels: int) -> Tensor:
    """Orthonormal Walsh characters with odd-parity indices (XOR sum-free)."""
    if (not isinstance(width, int) or isinstance(width, bool)
            or width < 2 or width & (width - 1)):
        raise ValueError("width must be a power of two >= 2")
    if not isinstance(channels, int) or isinstance(channels, bool):
        raise ValueError("channels must be an integer")
    labels = [i for i in range(1, width) if i.bit_count() % 2 == 1]
    if not 1 <= channels <= len(labels):
        raise ValueError("invalid channel count")
    positions = torch.arange(width, dtype=torch.long)
    rows = []
    for label in labels[:channels]:
        # Character (-1)^(popcount(label & position)).
        signs = [1.0 if (label & int(pos)).bit_count() % 2 == 0 else -1.0
                 for pos in positions]
        rows.append(torch.tensor(signs, dtype=torch.float32) / width**0.5)
    return torch.stack(rows)


class ProtectedCell(nn.Module):
    """RNN with a fixed Walsh-projected slow subspace and fast complement.

    Total recurrent state remains width coordinates; no external memory bank.
    Both slow and fast gates are trainable. Orthogonal masks are structural,
    but do NOT guarantee protection under nonlinear recurrent dynamics.
    """

    def __init__(self, width: int, channels: int) -> None:
        super().__init__()
        self.register_buffer("masks", sum_free_walsh_bank(width, channels))
        self.x_to_candidate = nn.Linear(width, width)
        self.h_to_candidate = nn.Linear(width, width, bias=False)
        self.slow_gate = nn.Linear(width, channels)
        self.fast_gate = nn.Linear(width, width)
        nn.init.constant_(self.slow_gate.bias, 3.0)
        nn.init.constant_(self.fast_gate.bias, 1.0)
        nn.init.orthogonal_(self.h_to_candidate.weight)

    def read_protected(self, h: Tensor) -> Tensor:
        """Return per-channel coefficients without consuming a time step."""
        return F.linear(h, self.masks)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        proposal = torch.tanh(self.x_to_candidate(x) + self.h_to_candidate(h))
        old_coeff = self.read_protected(h)
        write_coeff = self.read_protected(proposal)
        retention = torch.sigmoid(self.slow_gate(x))
        coeff = retention * old_coeff + (1 - retention) * write_coeff

        old_fast = h - F.linear(old_coeff, self.masks.T)
        write_fast = proposal - F.linear(write_coeff, self.masks.T)
        fast_retention = torch.sigmoid(self.fast_gate(x))
        mixed_fast = fast_retention * old_fast + (1 - fast_retention) * write_fast
        # A coordinate-wise fast gate can leak into the Walsh subspace.
        # Project it back out so read_protected(h_new) == coeff exactly.
        mixed_coeff = self.read_protected(mixed_fast)
        new_fast = mixed_fast - F.linear(mixed_coeff, self.masks.T)
        return F.linear(coeff, self.masks.T) + new_fast


class RNNLanguageModel(nn.Module):
    """Autoregressive next-token logits; forward supports chunked streaming.

    The model intentionally contains no data loader, optimizer, trainer, RL,
    generation/decoding loop, or collector. Hidden states persist between chunks
    only if the caller explicitly supplies the returned state.
    """

    def __init__(self, config: RNNConfig) -> None:
        super().__init__()
        self.config = config
        w = config.width
        self.embedding = nn.Embedding(config.vocab_size, w)
        if config.cell_type == "tanh":
            factory = lambda: TanhCell(w)
        elif config.cell_type == "near_critical":
            factory = lambda: NearCriticalTanhCell(w)
        else:
            factory = lambda: ProtectedCell(w, config.protected_channels)
        self.cells = nn.ModuleList([factory() for _ in range(config.layers)])
        self.norms = nn.ModuleList([nn.LayerNorm(w) for _ in range(config.layers)])
        self.final_norm = nn.LayerNorm(w)
        nn.init.normal_(self.embedding.weight, std=w ** -0.5)

    def initial_state(self, batch_size: int, *, device=None, dtype=None) -> tuple[Tensor, ...]:
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        p = self.embedding.weight
        return tuple(torch.zeros(batch_size, self.config.width,
                                 device=p.device if device is None else device,
                                 dtype=p.dtype if dtype is None else dtype)
                     for _ in self.cells)

    @property
    def trainable_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(
        self,
        input_ids: Tensor,
        state: Sequence[Tensor] | None = None,
        *,
        return_history: bool = False,
    ):
        if (not isinstance(input_ids, Tensor) or input_ids.ndim != 2
                or input_ids.dtype != torch.long or input_ids.shape[0] < 1
                or input_ids.shape[1] < 1):
            raise ValueError("input_ids must be a nonempty [batch, time] int64 tensor")
        if input_ids.device != self.embedding.weight.device:
            raise ValueError("input_ids and model parameters must be on the same device")
        batch, timesteps = input_ids.shape
        if state is None:
            memory = list(self.initial_state(batch))
        else:
            if len(state) != self.config.layers:
                raise ValueError("state must have one tensor per layer")
            if any(not isinstance(s, Tensor) for s in state):
                raise ValueError("state must contain tensors")
            if any(s.shape != (batch, self.config.width) or s.device != input_ids.device
                   or s.dtype != self.embedding.weight.dtype for s in state):
                raise ValueError("state tensors must match [batch, width], device, and model dtype")
            memory = list(state)
        embedded = self.embedding(input_ids)
        logits, history = [], []
        for t in range(timesteps):
            x = embedded[:, t, :]
            for i, (cell, norm) in enumerate(zip(self.cells, self.norms)):
                memory[i] = cell(x, memory[i])
                x = norm(memory[i])
            # Tied output embedding: avoids an extra large vocab projection matrix.
            logits.append(F.linear(self.final_norm(x), self.embedding.weight))
            if return_history:
                history.append(torch.stack(memory, dim=1))
        output = (torch.stack(logits, dim=1), tuple(memory))
        if return_history:
            return (*output, torch.stack(history, dim=1))
        return output
