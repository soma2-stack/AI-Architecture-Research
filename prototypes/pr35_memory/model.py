"""Trainable engineering surrogate of PR35; NOT its frozen-tanh credit theorem."""
from __future__ import annotations
import math
import torch
from torch import nn
import torch.nn.functional as F
from prototypes.rnn_llm_architecture.candidates import CandidateConfig, CandidateLanguageModel

PAIR_VARIANTS = ("pair_shared", "pair_direct", "pair_contract", "pair_no_retain")

class BalancedPairCell(nn.Module):
    """State [fast, p, -p]. Ordinary convex-gated memory in a redundant basis.

    Shared features use a row-normalized Vandermonde, not the theorem's clipped
    saturation code. Carries and writes are differentiable. No external masks,
    event parser, labels, or oracle addresses are available to this cell.
    """
    def __init__(self, width: int, variant: str = "pair_shared"):
        super().__init__()
        if variant not in PAIR_VARIANTS or width < 8 or width % 8:
            raise ValueError("known pair variant and width divisible by 8 >=8 required")
        self.width, self.variant = width, variant
        self.latent = width // 8
        self.pairs = 2 * self.latent - 1
        self.fast = width - 2 * self.pairs
        proposal_dim = self.pairs if variant == "pair_direct" else self.latent
        self.x_fast = nn.Linear(width, self.fast)
        self.h_fast = nn.Linear(width, self.fast, bias=False)
        self.x_value = nn.Linear(width, proposal_dim)
        self.h_value = nn.Linear(self.fast, proposal_dim, bias=False)
        self.x_gate = nn.Linear(width, self.pairs)
        nn.init.constant_(self.x_gate.bias, -3.)
        nn.init.orthogonal_(self.h_fast.weight)
        if variant == "pair_direct":
            code = torch.eye(self.pairs)
        else:
            nodes = torch.linspace(-1, 1, self.pairs, dtype=torch.float64)
            code = nodes[:, None] ** torch.arange(self.latent, dtype=torch.float64)[None, :]
            code = code / code.norm(dim=1, keepdim=True)
            code = code.float()
        self.register_buffer("code", code)
        self.carry = 1 - 1 / width if variant == "pair_contract" else 1.

    def prepare(self, x):
        return self.x_fast(x), self.x_value(x), torch.sigmoid(self.x_gate(x))

    def compressed_step(self, prepared, fast, contrast):
        """Same transition using ordinary fast+contrast state (comparison oracle)."""
        drive, value, gate = prepared
        physical = torch.cat((fast, contrast, -contrast), dim=-1)
        new_fast = torch.tanh(drive + self.h_fast(physical))
        proposal = torch.tanh(F.linear(torch.tanh(value + self.h_value(fast)), self.code))
        if self.variant == "pair_no_retain":
            gate = torch.ones_like(gate)
        carried = self.carry * contrast
        new_contrast = carried + gate * (proposal - carried)
        return new_fast, new_contrast

    def step(self, prepared, h, write_mask=None):
        if write_mask is not None:
            raise ValueError("no oracle write mask supported")
        f, r = self.fast, self.pairs
        p = .5 * (h[..., f:f+r] - h[..., f+r:])
        fast, p = self.compressed_step(prepared, h[..., :f], p)
        return torch.cat((fast, p, -p), dim=-1)

    def forward(self, x, h):
        return self.step(self.prepare(x), h)

class BalancedPairLanguageModel(CandidateLanguageModel):
    """PR23 token/streaming/reset/tied-head interface, with a new cell only."""
    def __init__(self, width=32, seed=17, variant="pair_shared", vocab_size=32):
        super().__init__(CandidateConfig(vocab_size=vocab_size, width=width, layers=1,
                                        cell_type="tanh", seed=seed))
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed + 101)
            self.cells = nn.ModuleList([BalancedPairCell(width, variant)])
        self.variant = variant
