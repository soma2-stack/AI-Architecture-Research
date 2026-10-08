# Experiment 016 — results: the protected-memory cell is an exactly reducible gated recurrence; no distinctive property survives

**Status: complete.** Mathematics, verified literature, deterministic numerical tests. No training. Compute ≈ 20 s for the full
analysis (`equivalence_016.py`) plus the test suite. Plan, derivation and thresholds: [`EXPERIMENT_016_PLAN.md`](EXPERIMENT_016_PLAN.md),
committed in `ce56df0` before the grid was run. Evidence: `reports/experiment_016/equivalence.json`; reference implementation
[`reference_016.py`](reference_016.py) (written from the equations, not by calling the original); tests `test_reference_016.py`.
`D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## 1. Exact transition (Phase 1)

For each layer, with Walsh masks `M` (8 × 32, `MMᵀ = I`), `Q = I − MᵀM`, `c = Mh`, `f = Qh`, layer input `x` (embedding, or LayerNorm of layer 0's state):

```
u  = tanh(W_x x + b_x + U h)            g = sigmoid(W_g x + b_g) ⊙ m      r = sigmoid(W_r x + b_r)
c' = (1 − g) ⊙ c + g ⊙ M u
f' = Q [ r ⊙ f + (1 − r) ⊙ Q u ]        h' = Mᵀ c' + f'
```

- **The hypothesised reduction `f' = Q[r f + (1−r) u]` is not exact.** The code gates the *projected* proposal; the two differ by `Q[(1−r) ⊙ MᵀM u]`
  (test: > 1e-3 on random inputs, while the projected form matches to < 1e-12). Every other part of the hypothesis holds: `c' = (1−g)c + g P u` with `P = M`,
  and `u` depends on the complete previous state (`slow_feedback=True`; with `False` it sees only `Q h`).
- **Rotated form (exact).** With `N` an orthonormal basis of range(Q) and `O = [M; N]`, the state `s = O h = (c, z)` evolves as
  `s' = Γ(x) s + (I − Γ(x)) O u` with `Γ(x) = diag(1 − g(x)) ⊕ N diag(r(x)) Nᵀ` — a gated convex recurrence whose gate is diagonal on the 8 protected
  coordinates and a **dense, symmetric, input-dependent matrix** on the 24 complement coordinates. Gates read only the layer input, never the state.
- Optional mechanisms are accounted for: `write_mask` multiplies `g`; `retain_slow=False` sets `g = m` (or 1); `project_fast=False` breaks the block form
  (complement leaks into `Mh`) and is the only configuration the reference does not cover (no trained model uses it); two layers interact only through `LayerNorm`.

## 2. Functional equivalence (Phase 3) — preregistered thresholds met

`RotatedGatedReference` implements the rotated form with ordinary operations (two linear gates, a tanh candidate, a fixed orthogonal `O`, an explicit
`N diag(r) Nᵀ` matrix gate) and copies the original's parameters. Grid: 3 random initialisations, the trained `prot_success_43_29` and `fixed005_success_43_43`,
and a `no_retain` model × batch 1/3/8 × length 1/7/40 × masks none/random(30 % closed)/all-closed × float64/float32 = **324 cases**:

| quantity (worst case over the grid) | float64 | float32 |
|---|---:|---:|
| logits | 8.0e-14 | 1.9e-5 |
| full recurrent states (every step, both layers) | 9.8e-15 | 3.8e-6 |
| protected coefficients | 6.9e-15 | 1.9e-6 |
| fast complement | 1.0e-14 | 3.6e-6 |
| parameter gradients (relative) | 1.8e-14 | 4.1e-6 |
| input-feature gradients (relative) | 7.2e-15 | 5.1e-6 |
| identical set of gradient-free (dead) parameters | yes (all cases) | yes |

The float64 comparison re-derives the masks exactly (`±1/√32`) in both copies; with the stored float32-rounded masks the float64 gap is ≤ 1.8e-6, entirely due to
the masks being orthonormal only to ≈ 6e-8 in float64. **Causal interventions:** Experiment 015's mid-continuation `S`-zeroing and Experiment 014's late protected
twin transplant, applied to the reference in its own coordinates, give **identical predictions** on 128 histories for both trained models (logit gap ≤ 3.5e-5, float32).

**Closed-write invariant** (float64, trained layer-1 cell, channel closed by `m = 0`): coefficient drift 2.2e-16 (original) / 0.0 (reference); `∂c/∂h` equals the
mask row to 5.6e-17; gradient into every cell parameter through the closed channel ≤ 5.6e-17. The invariant is a property of the equations, which the reference
preserves exactly.

**Equivalence to a general gated cell versus the canonical GRU.** The cell equals a general gated recurrence exactly; it is **not** a canonical GRU in any fixed linear
state basis: (a) the complement gates do not commute across real inputs (normalised commutator max 0.008–0.036, median 0.001–0.009; > 1e-6 threshold), so no
basis makes all of them diagonal; (b) the candidate is `M tanh(·)` (gate and nonlinearity act in different bases); (c) no reset gate; (d) gates ignore the state.
These are parameterisation differences; none is a claimed or demonstrated capability (see §4).

## 3. Prior art (Phase 2; all sources located and confirmed by web search in this session)

| needed property | closest established mechanisms | reproduces it? |
|---|---|---|
| 1. protected-state transition `c' = (1−g)c + g P u` | GRU update gate ([Cho et al. 2014](https://arxiv.org/abs/1406.1078)); coupled input–forget gate ([Greff et al., LSTM: A Search Space Odyssey](https://arxiv.org/abs/1503.04069)); minimal gated unit ([Zhou et al. 2016](https://arxiv.org/abs/1603.09420)); leaky-integrator ESN ([Jaeger et al. 2007](https://www.ai.rug.nl/minds/uploads/leakyESN.pdf)) for fixed `g` | **yes, exactly** in the protected coordinates (coupled convex gate; the fixed linear readout `M` of the candidate is a parameterisation) |
| 2. exact retention when the write gate is closed | LSTM with forget = 1 / input = 0 (constant error carousel); GRU with hard-masked update gate; Skip RNN binary state-copy gate ([Campos et al. 2017](https://arxiv.org/abs/1708.06834)); Clockwork RNN inactive modules ([Koutník et al. 2014](https://arxiv.org/abs/1402.3511)); Phased LSTM closed time gate ([Neil et al. 2016](https://arxiv.org/abs/1610.09513), approximately, small leak) | **yes**; in this model it too requires an *external* mask — the learned sigmoid gate is never exactly closed |
| 3. long-timescale memory | slow units ([Mozer, NIPS 1991](https://papers.nips.cc/paper_files/paper/1991/hash/53fde96fcc4b4ce72d7739202324cd49-Abstract.html)); gate-bias ("chrono") initialisation ([Tallec & Ollivier 2018](https://arxiv.org/abs/1804.11188)), which is what `b_g = −3` amounts to; unitary/orthogonal RNNs ([Arjovsky et al.](https://arxiv.org/abs/1511.06464)); gated orthogonal units ([Jing et al.](https://arxiv.org/abs/1706.02761)); LRU ([Orvieto et al. 2023](https://arxiv.org/abs/2303.06349)) | **yes** (and Exp 012/013: a GRU learned four-slot memory at least as often) |
| 4. selective subspace updates | block-partitioned state (Clockwork modules); delta-rule fast weights writing along key directions ([Schlag et al. 2021](https://arxiv.org/abs/2102.11174)); gated delta rule with non-diagonal, input-dependent transitions ([Yang et al. 2024](https://arxiv.org/abs/2412.06464)) | **yes** for fixed orthogonal subspaces (a change of coordinates); the dense complement gate is closest to the non-diagonal input-dependent transitions of the delta-rule family, though not identical to them |
| 5. Exp 014–015 causal behaviour | the reference cell (exact); GRU-32 held the same memory in layer 1 without a privileged subspace; the fixed-gate protected model did not use its protected subspace | **yes** — identical predictions under the same interventions; localisation is a training outcome, not an architectural guarantee |
| 6. state and resources | GRU-32 (32-d state, 13,888 params); input-only gates as in selective SSMs ([Mamba](https://arxiv.org/abs/2312.00752)) and other parallelisable recurrences; FastGRNN-style lightweight gating ([Kusupati et al. 2018](https://arxiv.org/abs/1901.02358)) | **yes**: same state size, comparable cost (below) |

## 4. Resources and invariants (Phase 4)

| | protected (as implemented) | rotated reference | GRU-24 | GRU-32 |
|---|---:|---:|---:|---:|
| parameters (total model) | 8,016 (formula `vn + L(3n²+nk+4n+k) + 2n` matches) | 8,016 | 8,112 | 13,888 |
| live parameters | 8,016 (7,488 with fixed gate or `retain_slow=False`) | same | 8,112 | 13,888 |
| recurrent state per layer | 32 | 32 | 24 | 32 |
| input-only MACs / token / layer (parallel over time) | 2,304 | 2,304 | 1,728 | 3,072 |
| sequential recurrent MACs / token / layer | 2,816, of which 1,792 are projections | 22,656 explicit matrix gate (4,608 if applied as `N(r⊙Nᵀz)`) | 1,728 | 3,072 |
| CPU forward, batch 64 × 72 tokens, 1 thread | 17.6 ms | 30.3 ms | 8.2 ms | 8.1 ms |
| gates depend on state | no | no | yes | yes |

Hard invariants and whether ordinary decompositions keep them:

1. **Closed channel ⇒ exact coefficient retention and identity gradient path.** Kept exactly by the reference; kept by any convex-gated cell (GRU/MGU/CIFG-LSTM) whose gate on
   those coordinates is hard-masked, in whatever fixed basis the coordinates are defined. **Not distinctive** (the project's own architecture report already recorded
   that this invariant "has an ordinary orthogonal-coordinate implementation").
2. **Block separation `M h = c`.** A coordinate partition in the rotated basis; kept by the reference by construction. **Not distinctive.**
3. **Walsh-specific features.** Odd-parity Walsh rows are orthogonal to the all-ones vector, so inter-layer LayerNorm centring cannot move protected coefficients
   (true of any subspace ⟂ 1); pairwise sum-free labels do not prevent cubic aliasing (recorded earlier in `ARCHITECTURE_REPORT.md`); random orthonormal masks preserve
   the main invariant. **No Walsh-specific guarantee.**
4. **Non-commuting projected complement gate.** A real exact difference from a canonical GRU, but an unintended by-product of projecting a coordinate gate; its
   commutators are small (median ≈ 1e-3) and no property depending on it has been claimed or observed.

No property was found that is lost when the protected mechanism is replaced by its closest established decomposition: the decomposition *is* the mechanism, with
the same state, the same invariants and similar cost, and the established gated cells reproduce each claimed capability.

## 5. Decision (Phase 5)

**Classification: a useful organisation of known recurrent mechanisms — and, for the "protected memory" component specifically, an existing mechanism with
different terminology.** The protected coefficients are a coupled (GRU-update-style) input-gated convex memory on a fixed orthonormal subspace, with an optional hard
mask; the fast complement is a gated convex memory whose coordinate gate is projected into that subspace's complement; both share one tanh candidate. No single
standard cell has exactly these equations (because of the projected, non-commuting complement gate and the `M tanh(·)` candidate), which is why it is not
labelled a pure renaming overall. It is **not** a potentially novel computational primitive (every operation is standard and the reduction is exact), and **not** a
potentially distinctive architecture (no stated property is lost under the ordinary decomposition, and Experiments 012–015 found no advantage over GRUs).

| claim | status | exact property / falsifiable test |
|---|---|---|
| new computational primitive | **contradicted** | exact equation-level reduction to standard gated operations (324/324 cases ≤ 1e-13) |
| protected subspace gives an invariant unavailable to gated RNNs | **contradicted** | the closed-write invariant is reproduced exactly by a hard-masked convex gate in the rotated basis |
| Walsh basis confers a guarantee | **contradicted** | random orthonormal masks keep the invariant; cubic aliasing exists |
| the cell is literally a canonical GRU | **contradicted** | non-commuting complement gates, `M tanh` candidate, no reset gate, input-only gates |
| non-commuting projected complement gate matters functionally | **inconclusive / untested** | replace `N diag(r) Nᵀ` by a commuting (diagonal-in-`N`) gate and compare learning and memory under the Exp 012 protocol; no evidence motivates running it |
| positive memory results (Exp 011–015) | **retained** | as findings about training outcomes of a gated RNN family (layer-1 memory; localisation in learned-gate successes; necessity for maintenance), not as architecture novelty |

**Recommendation:** close this prototype direction as a novelty candidate; do not benchmark it further. Preserve Experiments 009–015 as negative/neutral evidence
and as a tested intervention toolkit (exact steppers, pair construction, transplant/removal controls) reusable for future candidates.

## Remaining uncertainty

The literature check targets the closest mechanisms and confirms their existence and core ideas from primary pages; it is not an exhaustive priority search,
and exact equations of some cited cells (e.g., Phased LSTM's leak, SRU's gate) were not re-derived here. The non-commuting complement gate is the only exact
structural difference from canonical cells; it is unclaimed and untested. Local execution; earlier evidence, frozen files and `AGENTS.md` unchanged; nothing pushed.
