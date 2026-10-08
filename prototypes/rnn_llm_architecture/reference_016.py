"""Experiment 016: an independent reference implementation of the protected-memory cell as an ordinary gated recurrence.

Written from the derived equations, NOT by calling ProtectedMemoryCell. The original architecture is not modified.

State in rotated coordinates s = O h = (c, z), O = [M; N] orthogonal (N = orthonormal basis of range(I - MᵀM)):
    u  = tanh(W_x x + b_x + U h)                      (h = Oᵀ s; slow_feedback=False uses U Q h)
    g  = sigmoid(W_g x + b_g) * m                     (or a fixed constant, or 1 when retain_slow=False)
    r  = sigmoid(W_r x + b_r)
    c' = (1 - g) * c + g * (M u)                      diagonal coupled gate
    z' = A z + (I - A) (N u),  A = N diag(r) Nᵀ       dense, input-dependent, symmetric matrix gate
"""
from __future__ import annotations

import copy

import torch
import torch.nn.functional as F
from torch import nn


def complement_basis(M: torch.Tensor) -> torch.Tensor:
    """Orthonormal rows spanning range(I - MᵀM), computed in float64 then cast."""
    Md = M.double()
    Q = torch.eye(M.shape[1], dtype=torch.float64) - Md.T @ Md
    evals, evecs = torch.linalg.eigh(Q)
    N = evecs[:, evals > 0.5].T.contiguous()
    if N.shape[0] != M.shape[1] - M.shape[0]:
        raise ValueError("masks are not orthonormal")
    return N.to(M.dtype)


class RotatedGatedReference(nn.Module):
    def __init__(self, cell):
        super().__init__()
        cfg = cell.config
        if not (cfg.project_fast and cfg.orthogonal_masks):
            raise ValueError("reference covers the block-decomposable configuration (project_fast and orthonormal masks)")
        self.register_buffer("M", cell.masks.clone())
        self.register_buffer("N", complement_basis(cell.masks))
        self.W_x = copy.deepcopy(cell.x_to_candidate)
        self.U = nn.Parameter(cell.h_to_candidate.weight.detach().clone())
        self.W_g = copy.deepcopy(cell.slow_gate)
        self.W_r = copy.deepcopy(cell.fast_gate)
        self.fixed_g = getattr(cell, "_fixed_slow_write", None)
        self.retain = cfg.retain_slow
        self.slow_feedback = cfg.slow_feedback
        self.k = cell.masks.shape[0]

    @property
    def O(self):
        return torch.cat([self.M, self.N], 0)

    def to_h(self, s):
        return s @ self.O

    def to_s(self, h):
        return h @ self.O.T

    def step(self, x, s, m=None):
        h = self.to_h(s)
        fb = h if self.slow_feedback else h - (h @ self.M.T) @ self.M
        u = torch.tanh(self.W_x(x) + fb @ self.U.T)
        if self.fixed_g is not None:
            g = torch.full((x.shape[0], self.k), self.fixed_g, dtype=x.dtype)
        elif not self.retain:
            g = torch.ones(x.shape[0], self.k, dtype=x.dtype)
        else:
            g = torch.sigmoid(self.W_g(x))
        if m is not None:
            g = g * m
        r = torch.sigmoid(self.W_r(x))
        c, z = s[:, :self.k], s[:, self.k:]
        c_new = (1 - g) * c + g * (u @ self.M.T)
        A = torch.einsum("in,bn,jn->bij", self.N, r, self.N)            # [B, n-k, n-k]
        un = u @ self.N.T
        z_new = (A @ z.unsqueeze(-1)).squeeze(-1) + un - (A @ un.unsqueeze(-1)).squeeze(-1)
        return torch.cat([c_new, z_new], 1), {"A": A, "g": g, "r": r}


class ReferenceModel(nn.Module):
    """Same embedding, LayerNorms and tied head as the original (copied); cells replaced by RotatedGatedReference."""

    def __init__(self, model):
        super().__init__()
        self.embedding = copy.deepcopy(model.embedding)
        self.cells = nn.ModuleList(RotatedGatedReference(c) for c in model.cells)
        self.norms = copy.deepcopy(model.norms)
        self.final_norm = copy.deepcopy(model.final_norm)

    def forward_features(self, x, write_masks=None):
        """x [B,T,W] -> logits [B,T,V], rotated states per layer [B,T,L,W] and h-coordinate states."""
        B, T, W = x.shape
        S, H = [], []
        for l, (cell, norm) in enumerate(zip(self.cells, self.norms)):
            s = x.new_zeros(B, W)
            seq = []
            for t in range(T):
                m = None if write_masks is None else write_masks[:, t, l]
                s, _ = cell.step(x[:, t], s, m)
                seq.append(s)
            st = torch.stack(seq, 1)
            h = cell.to_h(st)
            S.append(st)
            H.append(h)
            x = norm(h)
        logits = F.linear(self.final_norm(x), self.embedding.weight)
        return logits, torch.stack(S, 2), torch.stack(H, 2)

    def forward(self, ids, write_masks=None):
        return self.forward_features(self.embedding(ids), write_masks)


def original_forward_features(model, x, write_masks=None):
    """The original CandidateLanguageModel layer loop, started from features (for input gradients). Checked against model(ids)."""
    B, T, _ = x.shape
    H = []
    for i, (cell, norm) in enumerate(zip(model.cells, model.norms)):
        prepared = cell.prepare(x)
        h = x.new_zeros(B, model.config.width)
        seq = []
        for j in range(T):
            mask = None if write_masks is None else write_masks[:, j, i]
            h = cell.step(tuple(v[:, j] for v in prepared), h, mask)
            seq.append(h)
        raw = torch.stack(seq, 1)
        H.append(raw)
        x = norm(raw)
    return F.linear(model.final_norm(x), model.embedding.weight), torch.stack(H, 2)


PARAM_MAP = {"x_to_candidate.weight": "W_x.weight", "x_to_candidate.bias": "W_x.bias", "h_to_candidate.weight": "U",
             "slow_gate.weight": "W_g.weight", "slow_gate.bias": "W_g.bias", "fast_gate.weight": "W_r.weight", "fast_gate.bias": "W_r.bias"}


def mapped_name(name: str) -> str:
    """Original parameter name -> reference parameter name."""
    if name.startswith("cells."):
        _, l, rest = name.split(".", 2)
        return f"cells.{l}.{PARAM_MAP[rest]}"
    return name
