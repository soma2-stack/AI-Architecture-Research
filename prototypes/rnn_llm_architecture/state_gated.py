"""Exploratory state-conditioned gated protected memory; no training.

A known gated-recurrence idea, NOT claimed as a new primitive or a
realization of the frozen dense-tanh robust learning-credit theorem.
Keeps the published candidate baseline intact and adds n*R gate weights
per recurrent layer for context-dependent write decisions.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from .candidates import CandidateConfig, CandidateLanguageModel, ProtectedMemoryCell


class StateGatedProtectedCell(ProtectedMemoryCell):
    """Changes write gate from sigmoid(G_x x) to sigmoid(G_x x+G_h h).

    The original proposal/fast complement and protection projection are
    unchanged. G_h initializes to zero, providing exact baseline parity
    at initialization and a clean ablation of context-dependent gates.
    """
    def __init__(self, config: CandidateConfig) -> None:
        if config.cell_type != "protected":
            raise ValueError("state-gated cell requires protected configuration")
        super().__init__(config)
        self.state_to_gate = nn.Linear(config.width,config.protected_channels,bias=False,
                                       dtype=getattr(torch,config.precision))
        nn.init.zeros_(self.state_to_gate.weight)

    def prepare(self,x:Tensor):
        # Parent version applies sigmoid in prepare; defer it until h is available.
        return self.x_to_candidate(x), self.slow_gate(x), torch.sigmoid(self.fast_gate(x))

    def step(self,prepared,h:Tensor,write_mask=None):
        drive, input_gate_logits, fast_retention=prepared
        combined_gate=torch.sigmoid(input_gate_logits+self.state_to_gate(h))
        return super().step((drive,combined_gate,fast_retention),h,write_mask)


class StateGatedProtectedLanguageModel(CandidateLanguageModel):
    """Same token/head/state interface as CandidateLanguageModel.

    Initializes the original protected model first and copies its weights
    unchanged, adding only zero-initialized state-dependent gate weights.
    """
    def __init__(self,config:CandidateConfig)->None:
        if config.cell_type!="protected":raise ValueError("protected config required")
        super().__init__(config)
        new=[]
        for original in self.cells:
            enhanced=StateGatedProtectedCell(config)
            incompatible=enhanced.load_state_dict(original.state_dict(),strict=False)
            if set(incompatible.missing_keys)!={"state_to_gate.weight"} or incompatible.unexpected_keys:
                raise RuntimeError("baseline weight migration failed")
            new.append(enhanced)
        self.cells=nn.ModuleList(new)
