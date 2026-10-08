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

## Fourth theory-faithful design path (new; incomplete)

See [THEORY_BLUEPRINT.md](THEORY_BLUEPRINT.md) for the complete
architecture plan, exact contract boundaries, and open components.
[theory_reference.py](theory_reference.py) adds a CPU-oriented,
untrained reference implementation of the source's selected
fixed-feature credit recurrence, with
[test_theory_reference.py](test_theory_reference.py) checking its algebra.
**This fourth path is NOT a fourth runnable token-prediction cell yet.**
It does not implement the full frozen dense-tanh legal-query protocol,
the Route-6 construction, or the unsolved strict-budget theorem.
The original three runnable variants remain unchanged as frozen baselines.

## Five token-model variants and one mathematical reference

All have a token embedding, a configurable stack of recurrent layers, state
shape `[batch, width]` per layer, layer normalization, and a tied output head.

| Cell | Recurrence | Reason to keep |
|---|---|---|
| `tanh` | `h'=tanh(W_x x+W_h h+b)` | Ordinary trainable reference. |
| `near_critical` | `h'=tanh(W_x x+(1-1/n) Q h+b)`, frozen orthogonal `Q` | Tests the **idea** of near-critical transition persistence. Not the exact frozen dense-tanh/corridor theorem construction. |
| `protected` | One recurrent state separated into fixed orthonormal Walsh channels and their orthogonal complement; separately gated writes | Tests selective retention and multi-channel interference. Not a theorem-backed robust-credit guarantee. |
| `gru` | Standard `torch.nn.GRUCell` reset/update-gated recurrence | Established gated baseline with one `[B,W]` persistent state per layer. |
| `lstm` | Standard `torch.nn.LSTMCell` input/forget/output-gated recurrence | Established gated baseline with separate `[B,W]` hidden and cell tensors per layer. |

GRU/LSTM token wrappers use the same embedding, layer-normalization placement,
tied output head, explicit streaming state, reset-mask convention, and hidden
history shape as the other candidates. An LSTM state is represented as
`LSTMState(hidden, cell)` per layer; both values are preserved across chunks,
detached together, and cleared together on reset. PyTorch's stock cell
initializers run inside a local seeded RNG scope, so model construction is
reproducible without consuming the caller's random stream.

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
   with all five token models, multiple seeds, matched parameter count / training
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

## Implemented architecture-development expansion

The original files above are preserved as frozen source controls. Four
separate current paths, implemented scope, actual CPU results, fair resource
counts, criticism and next-phase recommendations are documented in
[ARCHITECTURE_REPORT.md](ARCHITECTURE_REPORT.md). See
[LIMITATIONS.md](LIMITATIONS.md) for evidence calibration and open research.

* `candidates.py`: improved standard, near-critical and protected token models.
* `gated.py`: standard PyTorch GRU and LSTM token models.
* `full_reference.py`: exact established forward operators, balanced histories,
  early capture/trace repair, complete unpaired renewal and legal-query oracle.
* `validation.py`: shared cell/token diagnostics, fair configurations and measured resource inventory.
* `comparison_configs.json`: equal-width and trainable-parameter-matched configurations, plus isolated ablations.
* `reports/`: actual CPU test and diagnostic records.

```bash
python -m pytest -q prototypes/rnn_llm_architecture
python -m prototypes.rnn_llm_architecture.validation --output /tmp/rnn-validation.json
```

These commands run CPU architecture checks without training. The fourth
path remains a mathematical reference; missing robust-section and token
adapter obligations explicitly raise rather than fabricate implementations.

## Experiment 001 (first authorized CPU learning pilot)

[Method and task limitations](EXPERIMENT_001.md) ·
[Measured 40-condition report](EXPERIMENT_001_RESULTS.md) ·
[Complete per-seed results](reports/experiment_001_results.json) ·
[GitHub Actions evidence](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37710011831)

The protected model learned 64-token delayed binary recall in both 100-step
seeds; GRU/LSTM/ordinary controls were near chance at **that bounded budget**.
Selective overwrite remains much weaker and admits a last-write shortcut.
No parameter-matched training, general-language evaluation, or formal-D
theorem evidence was obtained. Keep these tasks and claims separate.

## Experiment 002 results

[Experiment plan](EXPERIMENT_002_PLAN.md) · [Full results and negative findings](EXPERIMENT_002_RESULTS.md) · [66-run raw JSON](reports/experiment_002_results.json) · [Hosted CPU evidence](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37710980507)

The protected model learned one-bit delayed recall at 64 tokens and often transferred to 128/256 tokens, but **not in every seed**. A no-projection ablation did just as well or better at the longest test length; Walsh-specific advantage has not been established. Counterfactual **both-slot** accuracy remained below a last-write shortcut on selective updating. Formal robust learning-credit dimension remains **OPEN**.

## Experiment 003 results

[Protocol and scope](EXPERIMENT_003_PLAN.md) · [Complete report](EXPERIMENT_003_RESULTS.md) · [All 42 runs](reports/experiment_003_results.json) · [GitHub-hosted evidence](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37712102670)

At 64-token training, the protected family learned single tagged-bit memory in the presence of competing bit tokens. The original protected cell averaged 87.6% on 256-token interference, while random-orthonormal and no-projection variants both reached 100% at that tested length. This does **not** establish Walsh-specific or projection-specific benefit, independent two-slot storage, token-model generality or formal learning-credit dimension.

## Experiment 004 results

[Protocol](EXPERIMENT_004_PLAN.md) · [Full per-seed analysis](EXPERIMENT_004_RESULTS.md) · [All 27 raw runs](reports/experiment_004_results.json) · [Hosted CPU run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37712871182)

Training both independent slot queries from the same prefix improved the protected model's updated-slot answer, **but not exact two-slot storage**. Its mean both-slot success at training length 64 was 51.7%, versus roughly 50% naive last-write; only 3.3% when A≠B. It fell to 27.8% both-slot success at 256 tokens. The next architecture hypothesis is a state-conditioned slow-write gate; these results do **not** establish new theoretical D or a unique mechanism.
