# Protected-memory RNN prototype — closure summary (2026-10-08)

**Disposition: suspended, not deleted.** All code, raw evidence, negative results and frozen files remain in place. This summary covers
Experiments 009–016 (Experiments 001–008 are documented in their own result files). It does not claim that every possible extension of the
idea has been mathematically ruled out, and it does not touch the separate formal learning-credit theory (`D=Omega(n),mT=o(n^(3/2))` remains OPEN).

## 1. What the prototype demonstrated

- **The two-slot failure (Exps 004–008) was an optimisation plateau,** not incapacity: the unchanged protected model leaves a "last-write" saddle after 500–750 updates (Exp 009).
- **Four binary slots are learnable but unreliable within 3,000 updates.** 2 of 12 learned runs succeeded in Exp 011. In Exp 012, 5/36 succeeded, 13 partially learned, and 18 stayed on the plateau. Success is dominated by the **initialization seed** (62 % of within-architecture variance, with clear architecture-specific interaction); the training-data seed contributes less.
- **Retention matters on this task.** Forced overwrite never learned four slots (0/9). A slow fixed write rate of 0.005 recovered most learning (4/9 learned), and the fixed rate equal to the initial gate bias failed (1/9) (Exps 012–013).
- **Where the memory lives (Exps 014–015, exact causal interventions on saved checkpoints):** the value is read from layer 1 only; layer 0 carries nothing at read time.
  - In the two learned-gate successes (both init 43), layer 1's eight protected coefficients are **sufficient**: transplanting them transfers the stored value 99–100 % (random 8-d subspaces ≤ 32 %).
  - During the continuation they are also **necessary**: removing them gives chance recall, random removals don't, and restoring them rescues recall 94–100 %.
  - At the read-out instant they are dominant but not strictly necessary.
- **The intervention toolkit is reliable.** Every reconstruction reproduced archived losses and evaluations bit-for-bit, and all steppers were checked against `forward` and chunked inference.

## 2. What Experiments 009–016 falsified or weakened

| claim | status | evidence |
|---|---|---|
| slow retention is what stores the two slots | weakened | Exp 009: gates never close; recurrent dynamics hold the pair |
| protected RNN outperforms a GRU | not supported | Exps 011–012: GRU-24 learned at least as often (8/9 learned, 2/9 success vs 6/9, 2/9) |
| learned input-dependent writing is necessary | unsupported | Exp 013: learned gate ≈ slow fixed rate (inconclusive); no consistent token selectivity |
| memory held in stable attractor basins | abandoned | Exp 014: contraction was a layer-0 artefact; layer-1 memory is a slowly decaying continuum; no basin snapping |
| the architecture relies on its protected store | contradicted | Exp 015: the successful fixed-gate model does not use it at all; GRU needs no 8-d subspace |
| new primitive / unique invariant / Walsh-specific guarantee | contradicted | Exp 016: exact reduction (below); closed-write invariant reproduced by ordinary hard-masked gating |

## 3. Exact known-mechanism reduction (Exp 016)

Per layer, with orthonormal Walsh rows `M` (8×32), `O = [M; N]` orthogonal and `s = O h = (c, z)`:

```
u  = tanh(W_x x + b + U h)
c' = (1 − g) ⊙ c + g ⊙ M u                 g = sigmoid(W_g x + b_g) ⊙ m      (coupled GRU-style update gate)
z' = A z + (I − A) N u,  A = N diag(r) Nᵀ  r = sigmoid(W_r x + b_r)           (matrix-valued convex gate)
```

An independent reference written with ordinary gated operations matches states, coefficients, complements, logits, parameter and input gradients and write-mask
behaviour in 324/324 cases (float64 ≤ 1e-13). It is a general gated recurrence, not literally a canonical GRU (non-commuting complement gates, `M tanh` candidate,
no reset gate, input-only gates), but none of these differences carries a claimed or demonstrated capability.

## 4. Why the prototype is suspended

The repository's standard requires a new primitive or an architectural property that the ordinary decomposition loses. Neither survived:
- the mechanism reduces exactly to known gated operations;
- every invariant is preserved by that decomposition;
- the localisation of memory in the protected store is a training outcome contradicted by a successful model of the same architecture;
- no advantage over GRUs was observed.

Further benchmarking would accumulate results for an existing mechanism.

## 5. Open uncertainties

- The non-commuting projected complement gate is the only exact structural difference from canonical cells; it is unclaimed and untested.
- Seeds are few: all localisation evidence comes from two models sharing init seed 43. Only one synthetic task was used (4 slots × 2 values), at width 32 and up to 3,000 updates.
- Runs left mid-descent at the budget (5/13 partial in Exp 012) might have succeeded with more updates.
- Why particular initialisations succeed is unexplained (one candidate marker, initial perturbation gain, was falsified).
- At the read-out instant, a weak complement trace exists whose role is not characterised.
- No language-modelling-scale test was run, and no hosted replication of Exps 011–016.

## 6. Reusable technical lessons

1. **Mechanistic reduction before benchmarking.** Write an independent reference cell from the derived equations and test exact equivalence (states, gradients, masks) early.
   Most of Exps 011–015 would have been framed differently had Exp 016 come first.
2. **Preregistration with mechanical decision rules** (and recording tie-breaks or misnamed labels instead of reinterpreting them) kept conclusions honest when results were mixed.
3. **Separate random streams** (initialisation, data, evaluation) from the start; Exp 011's single seed confounded all three.
4. **Bit-exact reproducibility** (deterministic CPU, stream hashes, init fingerprints, reconstruction checks) made saved-checkpoint analysis trustworthy.
5. **Causal intervention protocol:**
   - twin histories differing in one token;
   - transplants and removals at several timings;
   - dimension- and magnitude-matched random-subspace controls;
   - natural-state resampling, not only mean or zero ablation;
   - rescue, and an off-distribution measure.
   Analyse layer by layer before any whole-network claim.
6. **Pitfalls met:**
   - float32-stored orthonormal masks are not orthonormal in float64;
   - batch-size-dependent float rounding in sham controls;
   - perturbation measures taken in a layer that holds no memory;
   - a launcher bug with single shards.

Code entry points (unchanged): `candidates.py`, `capacity_010.py`…`capacity_013.py`, `intervene_014.py`, `necessity_015.py`, `reference_016.py`, `equivalence_016.py`; local launcher
`E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1`.
