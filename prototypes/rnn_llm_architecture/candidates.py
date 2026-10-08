"""Separate untrained candidates; model.py remains the frozen PR-v0 baseline.

No implicit state, optimizer, data pipeline, or weight updates. Layer-major
scans batch input projections and the tied head while retaining exact recurrence.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from .model import RNNConfig, sum_free_walsh_bank


@dataclass(frozen=True)
class CandidateConfig(RNNConfig):
    precision: str = "float32"
    seed: int = 20261007
    gap: float | None = None  # None means 1/width; never learned implicitly
    leak: float = 1.0
    operator: str = "orthogonal"  # orthogonal, householder_cycle, identity
    slow_write_bias: float = -3.0
    project_fast: bool = True
    retain_slow: bool = True
    slow_feedback: bool = True
    orthogonal_masks: bool = True
    protected_basis: str = "walsh"  # random_orthogonal tests Walsh-specific claims

    def __post_init__(self):
        super().__post_init__()
        if self.precision not in ("float32", "float64"):
            raise ValueError("precision must be float32 or float64")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError("seed must be an integer")
        if self.gap is not None and not (math.isfinite(self.gap) and 0 < self.gap < 1):
            raise ValueError("gap must be finite and strictly between zero and one")
        if self.cell_type == "near_critical":
            represented_a = torch.tensor(1-(1/self.width if self.gap is None else self.gap),dtype=getattr(torch,self.precision))
            if not 0 < represented_a < 1:
                raise ValueError("near-critical contraction gap is not representable in selected precision")
        if not math.isfinite(self.leak) or not 0 < self.leak <= 1:
            raise ValueError("leak must lie in (0,1]")
        if self.operator not in ("orthogonal", "householder_cycle", "identity"):
            raise ValueError("unknown recurrent operator")
        if not math.isfinite(self.slow_write_bias):
            raise ValueError("slow_write_bias must be finite")
        if self.protected_basis not in ("walsh", "random_orthogonal"):
            raise ValueError("unknown protected basis")
        for key in ("project_fast", "retain_slow", "slow_feedback", "orthogonal_masks"):
            if not isinstance(getattr(self, key), bool):
                raise ValueError(f"{key} must be boolean")


def initialized_linear(width: int, out: int, *, bias=True, dtype=torch.float32):
    layer = nn.Linear(width, out, bias=bias, dtype=dtype)
    nn.init.xavier_uniform_(layer.weight)
    if bias:
        nn.init.zeros_(layer.bias)
    return layer


class StandardCell(nn.Module):
    """Ordinary dense tanh, orthogonal recurrent and Xavier input initialization."""
    def __init__(self, config: CandidateConfig):
        super().__init__()
        self.x_to_h = initialized_linear(config.width, config.width, dtype=getattr(torch, config.precision))
        self.h_to_h = initialized_linear(config.width, config.width, bias=False, dtype=getattr(torch, config.precision))
        nn.init.orthogonal_(self.h_to_h.weight)

    def prepare(self, x: Tensor):
        return (self.x_to_h(x),)

    def step(self, prepared, h: Tensor, write_mask=None):
        return torch.tanh(prepared[0] + self.h_to_h(h))

    def forward(self, x: Tensor, h: Tensor):
        return self.step(self.prepare(x), h)


class NearCriticalCell(nn.Module):
    """Frozen spectral norm a, optional leaky transition; tanh may still kill credit.

For fixed input, ||dh'/dh|| <= 1-leak+leak*a. This is a cell bound;
the inter-layer LayerNorm and tied head have separate Jacobians.
"""
    def __init__(self, config: CandidateConfig):
        super().__init__()
        w = config.width
        dtype = getattr(torch, config.precision)
        self.x_to_h = initialized_linear(w, w, dtype=getattr(torch, config.precision))
        self.a = 1 - (1/w if config.gap is None else config.gap)
        self.leak = config.leak
        if config.operator == "orthogonal":
            q, r = torch.linalg.qr(torch.randn(w, w, dtype=dtype))
            q = q * torch.where(r.diag() < 0, -1., 1.)[None, :]
        elif config.operator == "identity":
            q = torch.eye(w, dtype=dtype)
        else:
            # U P U; known Householder-conjugated cyclic permutation.
            v = torch.full((w,), -1/math.sqrt(w), dtype=dtype)
            v[0] += 1
            u = torch.eye(w, dtype=dtype) - torch.outer(v, v)/(1-1/math.sqrt(w))
            p = torch.roll(torch.eye(w, dtype=dtype), shifts=1, dims=0)
            q = u @ p @ u
        self.register_buffer("recurrent", self.a*q)

    def prepare(self, x: Tensor):
        return (self.x_to_h(x),)

    def step(self, prepared, h: Tensor, write_mask=None):
        proposal = torch.tanh(prepared[0] + F.linear(h, self.recurrent))
        return h + self.leak*(proposal-h)

    def forward(self, x: Tensor, h: Tensor):
        return self.step(self.prepare(x), h)


class ProtectedMemoryCell(nn.Module):
    """Walsh coefficients plus projected fast complement, in n coordinates.

write_mask=0 freezes a coefficient including its gradient path, up to roundoff.
Open channels can still interfere through the nonlinear proposal. Ablations
are explicit flags and cease to carry the corresponding structural guarantee.
"""
    def __init__(self, config: CandidateConfig):
        super().__init__()
        w, c = config.width, config.protected_channels
        self.config = config
        bank = sum_free_walsh_bank(w, c).sign().to(getattr(torch, config.precision))/math.sqrt(w)
        if config.protected_basis == "random_orthogonal":
            bank = torch.linalg.qr(torch.randn(w,c,dtype=getattr(torch,config.precision)),mode="reduced")[0].T
        if not config.orthogonal_masks and c > 1:
            bank[1] = (bank[1]+.25*bank[0])/math.sqrt(1.0625)
        self.register_buffer("masks", bank)
        self.x_to_candidate = initialized_linear(w, w, dtype=getattr(torch, config.precision))
        self.h_to_candidate = initialized_linear(w, w, bias=False, dtype=getattr(torch, config.precision))
        nn.init.orthogonal_(self.h_to_candidate.weight)
        self.slow_gate = initialized_linear(w, c, dtype=getattr(torch, config.precision))
        self.fast_gate = initialized_linear(w, w, dtype=getattr(torch, config.precision))
        nn.init.constant_(self.slow_gate.bias, config.slow_write_bias)
        nn.init.constant_(self.fast_gate.bias, 1.)

    def read_protected(self, h: Tensor):
        return F.linear(h, self.masks)

    def synthesize(self, coefficients: Tensor):
        return F.linear(coefficients, self.masks.T)

    def complement(self, h: Tensor):
        return h-self.synthesize(self.read_protected(h))

    def prepare(self, x: Tensor):
        return self.x_to_candidate(x), torch.sigmoid(self.slow_gate(x)), torch.sigmoid(self.fast_gate(x))

    def step(self, prepared, h: Tensor, write_mask=None):
        drive, write, fast_retention = prepared
        old = self.read_protected(h)
        feedback = h if self.config.slow_feedback else self.complement(h)
        proposal = torch.tanh(drive+self.h_to_candidate(feedback))
        proposed = self.read_protected(proposal)
        if not self.config.retain_slow:
            write = torch.ones_like(write)
        if write_mask is not None:
            if (write_mask.shape != old.shape or write_mask.dtype != h.dtype
                    or write_mask.device != h.device or not torch.isfinite(write_mask).all()
                    or ((write_mask < 0) | (write_mask > 1)).any()):
                raise ValueError("write_mask must match coefficients, with finite values in [0,1]")
            write = write*write_mask
        coefficients = old+write*(proposed-old)
        fast = fast_retention*(h-self.synthesize(old)) + (1-fast_retention)*(proposal-self.synthesize(proposed))
        if self.config.project_fast:
            fast = self.complement(fast)
        return self.synthesize(coefficients)+fast

    def forward(self, x: Tensor, h: Tensor, *, write_mask=None):
        return self.step(self.prepare(x), h, write_mask)


class CandidateLanguageModel(nn.Module):
    """Shared token interface; empty chunks, per-example resets and explicit detach.

Resets apply BEFORE each token and cut its earlier state gradient. Without
reset/detach gradients cross chunk boundaries. The caller owns persistence.
"""
    def __init__(self, config: CandidateConfig):
        super().__init__()
        self.config = config
        # Reproducible local initialization without disturbing caller CPU RNG.
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(config.seed)
            w = config.width
            self.embedding = nn.Embedding(config.vocab_size, w, dtype=getattr(torch, config.precision))
            nn.init.normal_(self.embedding.weight, std=w**-.5)
            cell = {"tanh": StandardCell, "near_critical": NearCriticalCell,
                    "protected": ProtectedMemoryCell}[config.cell_type]
            self.cells = nn.ModuleList(cell(config) for _ in range(config.layers))
            self.norms = nn.ModuleList(nn.LayerNorm(w, dtype=getattr(torch, config.precision)) for _ in self.cells)
            self.final_norm = nn.LayerNorm(w, dtype=getattr(torch, config.precision))

    @property
    def trainable_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def initial_state(self, batch_size: int, *, device=None, dtype=None):
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        p = self.embedding.weight
        return tuple(torch.zeros(batch_size, self.config.width,
                                 device=p.device if device is None else device,
                                 dtype=p.dtype if dtype is None else dtype) for _ in self.cells)

    @staticmethod
    def detach_state(state: Sequence[Tensor]):
        return tuple(s.detach() for s in state)

    def forward(self, input_ids: Tensor, state=None, *, return_history=False,
                reset_mask: Tensor | None = None, write_masks: Tensor | None = None):
        p, c = self.embedding.weight, self.config
        if (not isinstance(input_ids, Tensor) or input_ids.ndim != 2
                or input_ids.dtype != torch.long or input_ids.shape[0] < 1
                or input_ids.device != p.device):
            raise ValueError("input_ids must be [positive batch,time] int64 on model device")
        b, t = input_ids.shape
        if state is None:
            state = self.initial_state(b)
        if (len(state) != c.layers or any(not isinstance(s, Tensor) or s.shape != (b,c.width)
                or s.dtype != p.dtype or s.device != p.device for s in state)):
            raise ValueError("state must match layers, batch, width, dtype and device")
        if reset_mask is not None and (reset_mask.shape != (b,t) or reset_mask.dtype != torch.bool
                                      or reset_mask.device != p.device):
            raise ValueError("reset_mask must be [batch,time] bool on model device")
        if write_masks is not None and (c.cell_type != "protected" or
                write_masks.shape != (b,t,c.layers,c.protected_channels)):
            raise ValueError("write_masks require protected [batch,time,layers,channels]")
        if t == 0:
            output = (p.new_empty(b,0,c.vocab_size), tuple(state))
            return (*output, p.new_empty(b,0,c.layers,c.width)) if return_history else output
        x, last, histories = self.embedding(input_ids), [], []
        for i,(cell,norm) in enumerate(zip(self.cells,self.norms)):
            prepared = cell.prepare(x)
            h, sequence = state[i], []
            for j in range(t):
                if reset_mask is not None:
                    h = torch.where(reset_mask[:,j,None], torch.zeros_like(h), h)
                mask = None if write_masks is None else write_masks[:,j,i]
                h = cell.step(tuple(v[:,j] for v in prepared), h, mask)
                sequence.append(h)
            raw = torch.stack(sequence, dim=1)
            x = norm(raw)
            last.append(h)
            if return_history:
                histories.append(raw)
        output = (F.linear(self.final_norm(x), p), tuple(last))
        return (*output, torch.stack(histories, dim=2)) if return_history else output
