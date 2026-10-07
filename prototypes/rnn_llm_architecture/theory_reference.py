"""Frozen fixed-source credit reference from the repository's scoped corridor.

This is an executable mathematical *reference kernel*, NOT a language-model
cell, trainable model, proof of D=Omega(n), or full legal-query implementation.

Source of equations: theory/codex_unpaired_corridor_sensitivity_20261003/
PROOF.md sections 1-3, especially (3)-(5), and
theory/codex_linear_dimension_frontier_20261006/PROOF.md section 3.

The public gate schedule, balanced four-site inverse lift, preparation,
chronological bath/front, exact common endpoint, and legal future-query
normalization have NOT been implemented here. A faithful full-system
realization must add and validate them separately.
"""
from __future__ import annotations

import math
from typing import NamedTuple

import torch
from torch import Tensor, nn


class CreditTrace(NamedTuple):
    """Complete fixed-source response at an endpoint, with feedback reads."""
    response: Tensor  # [r, p], p selected parameter directions
    J: Tensor         # [p], unpaired first feedback row
    B: Tensor         # [p], unpaired second feedback row


class FrozenCorridorCreditReference(nn.Module):
    """Direct reference realization of M_t=G_t(a O_* M_(t-1)+V).

    r=floor(n/2)-1, G_t=diag(gates[t]), O_*=C+1 u^T+e_1 v_H^T.
    With V=I_r this reproduces the full reference M_t from the proof.
    With selected V, it computes M_t V in the same linear recurrence.

    This tracks *parameter sensitivity*, not the hidden state of an LLM.
    Its intermediate matrix may consume O(r*p) storage; it makes no
    credit-compression claim. Intended for small n and float64 CPU audits.
    """

    def __init__(self, n: int, *, dtype: torch.dtype = torch.float64) -> None:
        super().__init__()
        if not isinstance(n, int) or isinstance(n, bool) or n < 16:
            raise ValueError("n must be an integer >=16 for this finite reference")
        if dtype not in (torch.float32, torch.float64):
            raise ValueError("reference dtype must be float32 or float64")
        self.n = n
        self.k = k = n // 2
        self.r = r = k - 1
        self.d = d = n // 4
        self.a = 1.0 - 1.0 / n
        gamma = 1.0 / (1.0 - 1.0 / math.sqrt(k))

        C = torch.zeros(r, r, dtype=dtype)
        # Theorem coordinates j=1,...,k-1; tensor index j-1.
        for j in range(2, d):
            C[j - 1, j - 2] = 1.0
        for j in range(d, k):
            C[j - 1, j - 1] = 1.0

        ones = torch.ones(r, dtype=dtype)
        e1 = torch.zeros(r, dtype=dtype)
        e1[0] = 1.0
        e_terminal = torch.zeros(r, dtype=dtype)
        e_terminal[d - 2] = 1.0  # physical j=d-1
        u = (gamma / math.sqrt(k)) * e_terminal - (gamma**2 / k) * ones
        v_h = (gamma / math.sqrt(k)) * ones
        operator = C + torch.outer(ones, u) + torch.outer(e1, v_h)

        self.register_buffer("local_transport", C)
        self.register_buffer("u", u)
        self.register_buffer("v_h", v_h)
        self.register_buffer("operator", operator)
        self.register_buffer("identity", torch.eye(r, dtype=dtype))

    def _validate(self, gates: Tensor, probes: Tensor) -> None:
        if not isinstance(gates, Tensor) or gates.ndim != 2 or gates.shape[1] != self.r:
            raise ValueError("gates must be [time, r] with r=floor(n/2)-1")
        if gates.shape[0] < 1:
            raise ValueError("at least one recurrence step is required")
        if (not isinstance(probes, Tensor) or probes.ndim != 2
                or probes.shape[0] != self.r or probes.shape[1] < 1):
            raise ValueError("probes must be [r, positive direction count]")
        if any(t.dtype != self.operator.dtype or t.device != self.operator.device
               for t in (gates, probes)):
            raise ValueError("gates, probes, and reference buffers must match device/dtype")
        if not bool(torch.isfinite(gates).all()) or not bool(torch.isfinite(probes).all()):
            raise ValueError("gates and probes must contain only finite values")
        if bool(((gates < 0.0) | (gates > 1.0)).any()):
            raise ValueError("gates must lie in [0,1], as diag(1-h_t^2)")

    def scan(
        self,
        gates: Tensor,
        probes: Tensor | None = None,
        *,
        return_history: bool = False,
    ) -> CreditTrace | tuple[CreditTrace, Tensor]:
        """Propagate chosen fixed parameter probes through all given time steps.

        Gates are INPUT to this reference, not synthesized by the legal
        four-site control protocol. The returned history, if requested,
        includes the zero initial condition and has shape [time+1,r,p].
        """
        p = self.identity if probes is None else probes
        self._validate(gates, p)
        state = torch.zeros_like(p)
        history = [state] if return_history else None
        for g in gates.unbind(0):
            state = g[:, None] * (self.a * (self.operator @ state) + p)
            if history is not None:
                history.append(state)
        trace = CreditTrace(response=state, J=self.u @ state, B=self.v_h @ state)
        if history is not None:
            return trace, torch.stack(history, dim=0)
        return trace
