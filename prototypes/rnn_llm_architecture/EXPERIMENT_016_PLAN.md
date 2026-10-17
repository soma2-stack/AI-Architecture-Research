# Experiment 016 — is the protected-memory cell a distinctive architecture, or a known gated recurrence in a fixed orthogonal basis?

**Status: preregistered before the equivalence tests were run.** Directed by GPT-6; executed by Claude. A novelty-falsification
investigation: mathematics, verified literature, small deterministic numerical tests. No training, no new architecture.
Compute budget 15 min. `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Phase 1 — exact transition (from `candidates.ProtectedMemoryCell`, default flags of every trained model)

Per layer ℓ with width n = 32 and k = 8 protected channels. `M` (k × n) = sum-free Walsh rows / √n, `MMᵀ = I_k`; `Q = I_n − MᵀM`.
Layer input `x_t` (embedding for ℓ = 0; `LayerNorm(h⁽⁰⁾_t)` for ℓ = 1). Previous state `h = h_{t−1}`; define `c := Mh` (k) and `f := Qh` (n).

```
u   = tanh(W_x x_t + b_x + U h)                    U = h_to_candidate (no bias), slow_feedback=True  (False: U Q h)
g   = sigmoid(W_g x_t + b_g) ⊙ m_t                 m_t = optional write mask ∈ [0,1]^k; retain_slow=False ⇒ g ≡ m_t (or 1)
r   = sigmoid(W_r x_t + b_r)                       elementwise in the ORIGINAL n coordinates
c'  = c + g ⊙ (M u − c)  = (1 − g) ⊙ c + g ⊙ M u
f'  = Q [ r ⊙ f + (1 − r) ⊙ Q u ]                  (project_fast=True)
h'  = Mᵀ c' + f'                                   ⇒ M h' = c' and Q h' = f' exactly (MQ = 0)
```

**Correction to the hypothesised reduction.** The directive's `f_next = Q[r f + (1−r) u]` is **not** what the code computes: the code
projects the proposal before gating, `Q[(1−r) ⊙ Q u]`. Because the gate `r` is elementwise in the original coordinates it does not commute with `Q`;
the two forms differ by `Q[(1−r) ⊙ MᵀM u]`, which is non-zero unless `r` is constant across coordinates. Gates depend only on the layer input
(never on `h`). The proposal `u` sees the full previous state. Two layers are stacked through `LayerNorm`; the head is tied to the embedding.

**Rotated form.** Let `N` (24 × 32) be any orthonormal basis of range(Q) and `O = [M; N]` (orthogonal). In coordinates `s = O h = (c, z)`:

```
c' = (1 − g) ⊙ c + g ⊙ (M u)                               diagonal coupled ("update-gate") convex update
z' = A(x) z + (I − A(x)) (N u),   A(x) = N diag(r(x)) Nᵀ    MATRIX-valued convex update, 0 ≺ A ≺ I, symmetric
u  = tanh(W_x x + b_x + U Oᵀ s)
```

So the cell is *exactly* a gated recurrence `s' = Γ(x) s + (I − Γ(x)) O u` with block-diagonal gate `Γ = diag(1−g) ⊕ A(x)`. Hypotheses to test:

- **H-exact:** an independently written reference cell built from ordinary operations (dense matrix gate, fixed orthogonal `O`, tanh candidate)
  reproduces states, coefficients, complements, logits, parameter gradients, input gradients and write-mask behaviour.
- **H-GRU:** the cell is *not* a canonical GRU/MGU in any fixed linear state basis, because (a) canonical GRU gates are diagonal in one fixed basis,
  whereas the complement gates `A(x)` would then have to commute for all inputs; (b) the candidate is a linear map of an elementwise tanh taken in a
  different basis from the gate (`M tanh(·)`, not `tanh(M ·)`); (c) no reset gate; (d) gates ignore the state. Test (a) numerically by commutators of
  `A(x)` over real inputs of trained models.

## Phase 2 — prior art (sources verified by web search in this session)

GRU (Cho et al., 2014, arXiv:1406.1078); LSTM and its coupled input–forget gate variant (Greff et al., "LSTM: A Search Space Odyssey",
arXiv:1503.04069); minimal gated unit (Zhou et al., 2016, arXiv:1603.09420); leaky-integrator ESNs (Jaeger et al., Neural Networks 2007);
multiple-timescale units (Mozer, NIPS 1991/92); Clockwork RNN (Koutník et al., 2014, arXiv:1402.3511); Phased LSTM time gate that holds state while
closed (Neil et al., 2016, arXiv:1610.09513); Skip RNN binary state-copy gate (Campos et al., 2017, arXiv:1708.06834); unitary RNNs (Arjovsky et al., 2015,
arXiv:1511.06464); gated orthogonal recurrent units (Jing et al., 2017, arXiv:1706.02761); FastGRNN (Kusupati et al., 2018, arXiv:1901.02358);
LRU (Orvieto et al., 2023, arXiv:2303.06349); Mamba selective SSM with input-only dependent transitions (Gu & Dao, 2023, arXiv:2312.00752);
Gated DeltaNet with non-diagonal input-dependent transitions (Yang et al., 2024, arXiv:2412.06464). Each is compared against the six capabilities in the directive.

## Phase 3 — functional-equivalence tests (thresholds fixed now)

Reference `reference_016.RotatedGatedReference` (separate file; the original is not modified), parameters copied from the original. Grid: 3 random
initialisations + the trained checkpoints `prot_success_43_29` and `fixed005_success_43_43`; batch sizes 1, 3, 8; sequence lengths 1, 7, 40; float64
(primary) and float32; write masks absent, random in [0,1], and all-zero. Compared per step and layer: full state, protected coefficients, complement,
logits, all parameter gradients, input-feature gradients.

- **Exact equivalence (float64):** every max-abs difference ≤ 1e-10 (gradients: ≤ 1e-9 relative to the gradient's max-abs). float32: ≤ 1e-4 absolute.
- **Closed-write invariant:** with `m_t = 0` the coefficient is unchanged to ≤ 1e-12 (float64) and `∂c'/∂c = I`, `∂c'/∂(W_x, U, W_g, b_g) = 0` on that channel, in both implementations.
- **Not a canonical GRU (H-GRU a):** if the normalised commutator `‖A(x)A(x') − A(x')A(x)‖_F / (‖A(x)‖_F ‖A(x')‖_F)` exceeds 1e-6 for some pair of
  real inputs, no fixed linear change of basis makes the complement gate diagonal.
- **Causal-behaviour equivalence:** the Experiment 015 mid-continuation `S_mean` removal and the Experiment 014 late protected transplant, applied to the
  reference model in its own coordinates, give the same predictions as the original on the same histories.

## Phase 4 — resources and invariants

Parameter count (formula and count), live parameters, recurrent state dimension, recurrent multiply-accumulates per token (analytic), a small CPU wall-clock
micro-benchmark (≤ 1 min), projection overhead, and the list of hard invariants with whether the ordinary decomposition preserves each.

## Phase 5 — decision rules (fixed now)

- If H-exact holds and every hard invariant is preserved by the reference (or by a known mechanism with a hard mask), the protected cell carries **no
  invariant unavailable to ordinary gated decompositions**.
- Classification: *novel primitive* only if some operation cannot be written with known operations while preserving a stated property (not expected);
  *distinctive architecture* only if a precisely stated property is lost under the closest established decomposition **and** evidence shows the property matters;
  *useful organization of known mechanisms* if exact reduction holds but the specific combination (coupled gate on a fixed subspace + matrix-gated projected
  complement + shared candidate) has no single known name; *existing mechanism with different terminology* if a single known cell already has the same equations.
- Each surviving claim must come with an exact property and a falsifiable test. If none survives, recommend closing the prototype direction, preserving
  the Experiment 009–015 memory results.

## Out of scope

Experiment 017, training, changes to `main`, `AGENTS.md`, PR #23, Experiments 001–015. Committed locally, not pushed.
