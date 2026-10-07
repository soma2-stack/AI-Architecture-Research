# RNN LLM architecture prototype (no training)

**Status: untrained engineering prototype / hypothesis, NOT a proved new architecture.**

This isolated folder is intended to connect the [current robust credit-memory
theory](../../theory/CURRENT_THEORY.md) to a falsifiable language-model design.
It does not alter any theory records, experiments, research-lane notebooks,
AGENTS.md, or the main README.

## Scope

Only recurrent next-token architecture, streaming state, introspection, and
CPU-only correctness checks are included. **No training script, optimizer,
dataset, synthetic experiment loop, collector, RL, generation service, GPU job,
or pretrained weights.**

## Three model variants

All have a token embedding, a configurable stack of recurrent layers, state
shape `[batch, width]` per layer, layer normalization, and a tied output head.

| Cell | Recurrence | Reason to keep |
|---|---|---|
| `tanh` | `h'=tanh(W_x x+W_h h+b)` | Ordinary trainable reference. |
| `near_critical` | `h'=tanh(W_x x+(1-1/n) Q h+b)`, frozen orthogonal `Q` | Tests the **idea** of near-critical transition persistence. Not the exact frozen dense-tanh/corridor theorem construction. |
| `protected` | One recurrent state separated into fixed orthonormal Walsh channels and their orthogonal complement; separately gated writes | Tests selective retention and multi-channel interference. Not a theorem-backed robust-credit guarantee. |

For the protected cell, let `P` be an `R x n` orthonormal Walsh bank
(`P P^T = I`) with odd-parity, pairwise XOR-sum-free labels. Let
`c=tanh(W_x x + W_h h)`, `q=P h`, `u=P c`. Then

```
q_new = sigmoid(G_s x) * q + (1-sigmoid(G_s x)) * u
f_old = h - P^T q
f_write = c - P^T u
f_mix = sigmoid(G_f x) * f_old + (1-sigmoid(G_f x)) * f_write
f_new = f_mix - P^T(P f_mix)
h_new = P^T q_new + f_new
```

The final projection is required because the coordinate-wise fast gate can
move `f_mix` into the protected Walsh subspace. The implementation removes
that component after gating so `P h_new = q_new` (up to floating-point error).

The protected bank occupies **R of the existing n state coordinates**,
not R additional n-wide states. Increasing R nevertheless changes the gate
parameter count. Fixed Walsh readout orthogonality does **not** imply low
nonlinear temporal cross-talk or stable learning credit.

### Relation to the repository research

- The [linear-dimension frontier](../../theory/codex_linear_dimension_frontier_20261006/PROOF.md)
  established **scoped** strict-budget constructions with `D=o(n)` and a
  linear boundary at `mT=Theta(n^(3/2))`. The strict-budget `D=Omega(n)`
  target is **OPEN**, not realized in this prototype.
- [Clean-mask scaling](../../experiments/finite_n_clean_mask_scaling_20261006/SUMMARY.md)
  reported low normalized cross-talk through R=16 in a specific untrained
  recurrence. That is motivation to test orthogonal channels, **not** proof
  that this LLM cell inherits that performance.
- [Recent Route 6/7A reviews](../../theory/INDEX.md) expose additional
  conditional or pending-review obstructions. No claim here resolves them.
- Exact theory involves a prescribed frozen family, admissible continuous
  histories, common endpoints, *actual legal future gradient queries*, and
  group-RMS-normalized robust separation. Token-level accuracy, raw memory
  state dimension, Walsh rank, and ordinary backpropagation are **not** D.

## Proposed evaluation gates (not executed)

1. **Architecture correctness:** shape, streaming/chunk equivalence, explicit
   reset, recurrent spectrum, mask orthogonality, gradient finiteness.
   CPU-only tests here check these basic properties.
2. **Learning-credit diagnostics:** vary sequence horizon and retain
   backpropagated gradient norms and actual future-loss sensitivity; test
   with all three cells, multiple seeds, matched parameter count / training
   FLOPs. Raw norms are diagnostics, not the formal theorem metric.
3. **Retention and interference:** delayed recall, selective overwrite,
   late retrieval after distractors, and mixed messages; vary R=2/4/8/16.
   Compare against unprotected tanh and a standard gated recurrent baseline
   of matched size before any novelty claim. Report all failures.
4. **Formal bridge, separate from LLM experiments:** implement the precise
   frozen corridor and actual legal-query normalization as a distinct
   numerical oracle, with common-endpoint and admissibility checks. An LLM
   training run cannot prove `D=Omega(n), mT=o(n^(3/2))`.
5. **Scaling / hardware:** eventually sweep n and T, record actual training
   peak VRAM, throughput, latency, and accuracy. Do not infer asymptotics
   from small widths.

Promotion requires reproducible gains under matched controls and ablations
(removing protected projection, disabling slow retention, destroying mask
orthogonality), followed by a prior-art check. This is currently a
**conceptual architecture candidate assembled from known operations**.

## Local CPU-only validation

From repository root with Python, PyTorch and pytest installed:

```bash
python -m pytest -q prototypes/rnn_llm_architecture/test_model.py
```

Example forward call (untrained output only):

```python
import torch
from prototypes.rnn_llm_architecture.model import RNNConfig, RNNLanguageModel

model = RNNLanguageModel(RNNConfig(vocab_size=128, width=64, layers=2,
                                    cell_type="protected", protected_channels=8))
ids = torch.tensor([[1, 5, 9]], dtype=torch.long)
logits, state = model(ids)
next_logits, next_state = model(torch.tensor([[7]]), state)  # stream continuation
```

**Architecture only.** Do not interpret next-token logits as a useful trained
language model until a separate approved pretraining and evaluation phase.
