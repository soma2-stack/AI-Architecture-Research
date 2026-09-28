# AMS v2 — Implementation decisions (fixed before any Stage-0 gate or Stage-1 run)

Authority: `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v2** (sole active protocol), then Claude Part AE (implementation authority for grammar, canonicalizer, probes rule, search, gates).

This file lists **only** choices that the frozen documents leave open, or where two frozen texts must be reconciled.

- Each item was fixed and committed **before** any of the following:
  - the Task-B gradient-conflict gate was computed;
  - any Stage-1 control was trained;
  - any candidate was evaluated.
- Nothing here changes a v2 threshold, budget, schedule, stop condition or promotion rule.
- Where a choice could favour candidates, the conservative option is taken.

Git history of this file is the evidence of timing.

**Pre-gate observations disclosed before this commit** (collision-library self-checks only; no task, training or gate result had been computed):

- all 31 references and 124 disguised variants are flagged as rediscoveries;
- 7 of 465 reference pairs collide at the family threshold (listed in D-COLL-3);
- the regeneration aid reproduces all vector/matrix corpus fields.

---

## D-GEN — general

- **D-GEN-1. Package.**
  - Location: `experiments/automated_mechanism_search/ams/`.
  - Results: `runs/<stage>/`, all machine-readable (JSON / JSONL / CSV).
  - Notebooks are not written by code.
- **D-GEN-2. Precision.** Substrate float32. Behavioural probes float64 (the probe corpus is a float64 JSON; float64 avoids spurious overflow in the hash).
- **D-GEN-3. CPU only.** `CUDA_VISIBLE_DEVICES=""`. No GPU library is imported.
  - Workers: at most `min(3, nproc - 1)`, run at `nice 10`.
  - Cumulative CPU time (user + sys, parent + children) goes to `runs/cpu_ledger.json`.
  - Hard stop at 30 CPU-h.

## D-SEED — seeds and random streams

- **D-SEED-1.** Every random stream is `numpy.random.Generator(PCG64(SeedSequence([seed, stream_id])))`.
  - Stream ids:
    - model init 7001;
    - fixed feedback 7002 (+100·layer);
    - reinit 7003;
    - noise (xi, noise-init registers) 7004;
    - task streams 1–9 (per task).
  - Exception: the literal v2 text for the Task-B matrices is `Generator(PCG64(seed))`, used directly for `A_c, A_1, A_2`.
- **D-SEED-2. Seed sets (disjoint).**

  | Use | Seeds |
  |---|---|
  | Stage-1 calibration | 100–104 (5 seeds) |
  | Stage-2 Tier-1 search | 1000–1002 (3 seeds; identical for every candidate and every baseline, paired) |
  | Stage-2 sanity filter T0 | 500 |
  | Stage-3 Tier-2 fresh validation | 10000–10009 (10 seeds, AE.5.10 `fresh_seeds: 10`; satisfies v2 "≥ 5") |
  | Stage-3 Tier-3 locked confirmation | 20000–20009 |

  - Task instances are functions of the seed, so these seed sets are also fresh task instances.
  - Search code has no access to seeds ≥ 10000. A leakage assertion checks this.
- **D-SEED-3.** Learning rates of the same seed share initialization, data order and noise (paired).

## D-SUB — substrate semantics (AE.1 under v2 mini-batches)

- **D-SUB-1. Architecture.**
  - MLP `[d_in, 32, 32, d_out]`, tanh hidden, identity output.
  - Glorot-normal weights, `std = sqrt(2/(fan_in+fan_out))`; biases 0.
- **D-SUB-2. Loss.**
  - Regression: per-example loss `L = ½‖ŷ−y‖²`, so `d_bp(out) = e = ŷ−y`. Reported MSE = mean over outputs and examples.
  - Classification (Task F, `d_out = 2`): softmax cross-entropy with `e = p − onehot(y)`.
- **D-SUB-3. Batch semantics.** v2 fixes batch 32 for B and F; C* and T0 are online (batch 1). The program is evaluated per example.
  - ΔW and Δb are batch means.
  - RUN / EPISODE register update: `r ← mix(r, mean_batch(v), λ)`.
  - EXAMPLE registers stay per-example temporaries. This matches canonical inlining.
  - STRUCT mask: `step(mean_batch(E_O) − θ)`.
  - Leaf `L` is the per-example loss.
  - `dL = L − (previous step's batch-mean loss)`, 0 on the first step.
  - `Lbar` is the running mean (λ = 0.99) of batch-mean losses **before** the current step; the first step uses the current batch mean.
- **D-SUB-4. Protocol steps.**
  - One protocol step = one mini-batch (B, F) or one example (C*, T0).
  - `update_every = k` applies the mean of the last k step-deltas every k steps.
  - Data exposure is identical for all methods.
  - STRUCT runs every 100 protocol steps, after the parameter update of that step.
- **D-SUB-5. Leaves.**
  - `d_bp` is backpropagated through `W_eff` and `g`, both treated as constants (no derivative of W_eff / g with respect to `a`).
  - `e` is zero at hidden layers.
  - `d_fa = e` at the output layer and `B_l e` at hidden layers, with `B_l ~ N(0, 1/d_out)` fixed.
  - `xi_I`, `xi_O`: fresh N(0, 0.01²) per example. "N(0, 0.01)" is read as standard deviation 0.01, which matches the corpus xi magnitude.
  - The same noise sample is visible in FORWARD and later phases of a step. Noise is 0 at evaluation.
  - Noise-initialized registers use the same N(0, 0.01²).
- **D-SUB-6. Phase availability.**
  - FORWARD: `a, W, b, W_ep0, tep, xi_I, xi_O`, registers (old values).
  - CREDIT adds: `z, h, dphi, d_bp, d_fa, e, L, dL, Lbar`.
  - STATE adds `cvec`. STATE right-hand sides see old register values.
  - PARAM and STRUCT see the updated registers.
- **D-SUB-7. Episodes.**
  - Task B provides its boundary at step 500, because the required GPM control needs it. At the boundary: EPISODE registers reset, `W_ep0 ← W`, and `tep` = steps since task start / 500.
  - Tasks without boundaries (C*, F, T0) have `tep = 0`, `W_ep0 =` W at run start, and EPISODE registers never reset. C* must expose no boundary or segment information (v2).
- **D-SUB-8. Update application** (identical for candidates and official controls; v2 §8 "clipping").
  - Rescale each layer's ΔW to Frobenius norm ≤ 1.
  - Clip Δb to [−1, 1].
  - Apply `W += η·ΔW`.
- **D-SUB-9. Guards** (AE.3.6, v2 §12).
  - A run is marked unstable at the first occurrence of any of:
    - NaN/Inf loss;
    - EMA(0.9) of batch-mean loss after step 10 exceeding 10 × the mean loss of the first 10 steps;
    - ‖W‖_F > 1e4, or non-finite parameters (checked every 50 steps).
  - Unstable runs stop updating.
  - A (method, LR) configuration with any unstable seed is excluded from LR selection.
  - Memory: worker RSS > 512 MB → OUT_OF_BOUNDS.
  - Timeout: CPU time of a candidate's vectorized evaluation of one task > 120 s × number of seeds → TIMEOUT.
- **D-SUB-10. STRUCT.**
  - `reinit` resamples the incoming weights of masked units from the init distribution; bias unchanged.
  - `freeze` zeroes the ΔW rows of masked units until the next STRUCT evaluation.

## D-OPS — operators

- **D-OPS-1.** `amax(x) = max|x|`.
- **D-OPS-2.** `topk(x,k)` is a 0/1 mask of the k largest values along the vector axis; all ones when k ≥ n.
- **D-OPS-3.** `sigmoid(x) = ½(1 + tanh(x/2))`.
- **D-OPS-4. Typing.** Binary operands are `(T,T)` or `(T,S)` (AE); `(S,T)` is ill-typed.
- **D-OPS-5. Depth.** A leaf has depth 0. Expression depth is the number of operator levels (≤ 5).
- **D-OPS-6. Node count.** Slot templates (`W +`, `clip`, `mix`, `step(·−θ)`) are not counted as nodes.

## D-CANON — canonicalizer (AE.2.1)

- **D-CANON-1. EXAMPLE registers with init 0/1 are inlined.**
  - Reads in FORWARD / CREDIT / STATE see the reset value.
  - Reads in PARAM / STRUCT see `λ·init + (1−λ)·v`.
  - This applies only when `v` reads no persistent register.
  - Noise-init EXAMPLE registers stay registers, because the grammar has no fresh-noise leaf of every type.
- **D-CANON-2. `cvec` is a temporary** (v2 Level A "temporary inlining").
  - It is always inlined into STATE right-hand sides.
  - It is inlined into PARAM / STRUCT only when it reads no register. PARAM would otherwise see new register values.
- **D-CANON-3. Rewrite rules.**
  - Rules: exactly the AE.2.1 list, plus constant folding.
  - Folding is restricted to dimension-independent cases.
  - `mix(r,v,0)→v` fires only when `r` is read in PARAM / STRUCT alone, and `v` reads no register.
  - `topk(x,k≥n)→1` is vacuous on this substrate (hidden width 32 > 8), so it is not applied.
  - Under mini-batching, `mix(r,v,0)→v` moves the batch reduction. All evaluation uses canonical programs, so the canonical form defines the semantics. Equivalence tests run online (B = 1).
- **D-CANON-4. Commutative sorting.** Operands of `add, mul, max, min, dot` are sorted by s-expression when their types are equal; mixed `(T,S)` stays in that order.
- **D-CANON-5. Register renaming.** By first use, in the order `w_eff, gain, cvec, dW, db, struct`, then register updates breadth-first. Renaming and sorting iterate to a fixpoint.
- **D-CANON-6. Hashes.**
  - Structural hash: sha256 of the canonical JSON.
  - Abstract template hash (family templates): constants, decays, `update_every` and register names are abstracted.

## D-PROBE — Level B (v2 corpus)

- **D-PROBE-1. Corpus verification.** Before any behavioural deduplication, the code verifies that `config/behavioral_probes_v2.json`:
  - exists;
  - has git blob `d5a8e0d1d91d1d1caf5ff3cbb84f9a4c76e730c1`;
  - is schema `AMS-BEHAVIOR-PROBES-V2`;
  - has 16 probes, I = 8, O = 6, and four register slots.

  The corpus is never regenerated as a substitute. The xorshift32 replay is a verification aid only. It reproduces all vector/matrix fields exactly. The corpus does not document the mapping for the scalar fields `L, dL, Lbar, tep`, so those rely on the blob hash.
- **D-PROBE-2. `W_ep0` is not a corpus field.** For probe k it is defined as the `W` of probe (k+1) mod 16. This is deterministic, derived only from the frozen corpus, and keeps anchor terms informative. The omission is reported to the owner.
- **D-PROBE-3. One-step evaluator.**
  - One tanh layer: FORWARD, CREDIT, STATE, PARAM.
  - `d_bp, d_fa, e, L, dL, Lbar, xi, tep` come from the corpus.
  - The canonical register k starts from bank slot k with the value of its type.
  - β = per probe `[h, unit(vec ΔW), unit(Δb), unit(Δr_slot1..4) zero-padded to 48]`, concatenated in probe order.
  - Duplicate: `round(β,6)` identical or cos ≥ 0.999 with any earlier accepted program.
- **D-PROBE-4. Family behavioural match** (AE.2.4): cos(β(P), β(R)) ≥ 0.99, maximised over injective assignments of P's registers to bank slots.
  - "Inert extras" are registers that never reach FORWARD / PARAM / STRUCT, and DCE removes them. A read register is never treated as inert.
  - STRUCT events and gates with k ≥ probe dimension are not visible in one-step probes. This is a frozen-design limitation and is reported.

## D-COLL — collision pipeline order (AE.3.4 with v2 §12 wording)

- **D-COLL-1. Pipeline order.** Each stage rejects on the condition shown; the rejection label follows the arrow.
  1. typecheck → `invalid`;
  2. canon;
  3. duplicate check (struct hash, then β) → `dup_syntactic` / `dup_behavioral`;
  4. coupling check (C1/C2/C3) → `pure_rule`, logged as REDISCOVERY-optimizer/local-rule;
  5. learning signal → `no_signal`;
  6. family match:
     - (syntactic / template / behavioural) **and** K(P) = P (no non-family residual) → `REDISCOVERY`;
     - otherwise, if β(P) ≈ β(K(P)) (cos ≥ 0.99), the residual is inert → `REDISCOVERY_inert`;
  7. sanity filter T0;
  8. Tier-1.
- **D-COLL-2. K(P)** (nearest known-family decomposition; AE.2.5 erratum: K(P) and P−R are the same object and are implemented once). Starting from P with `cvec` expanded:
  - Keep every top-level additive term of ΔW, Δb and W_eff whose abstract form equals a term of some reference slot.
  - Terms whose gates (`topk`, `where`) wrap a family term keep the family term, with the gate neutralized to 1.
  - Drop other terms.
  - Keep `g` and STRUCT only when they equal a reference template.
  - Registers whose update is not a reference template become inert (held at init).
  - K(P) is then canonicalized.
- **D-COLL-3. Reference library.**
  - Contents: R1–R24 of AE.2.4 plus 7 expressible AE.10 extras (AdaGrad-approx, anti-Hebbian, e-prop-like, neuromodulated Hebbian, AdamW-like, Nesterov-like, weight perturbation).
  - Disguises: operand reordering, update rescaling, inert extra register, register renaming.
  - Pre-commit self-check:
    - 100% of references and disguises are flagged as rediscoveries;
    - 3 rescaled disguises are attributed to a behaviourally identical family;
    - reference pairs colliding at 0.99: R1~R19, R1~R24, R19~R24, R4~X5, R9~R10, R9~R22, R10~R22.

## D-TASK — task generators (v2 §6)

- **D-TASK-B. Task B.**
  - Matrices: `A_c (4×8), A_1 (4×12), A_2 (4×12)` drawn in that order from `Generator(PCG64(seed)).standard_normal`, then each row normalized to unit L2 norm.
  - Streams:
    - training (stream 1): each step draws 32 fresh `(c, p)` for the current task;
    - held-out Task-1 set (stream 2): 256 samples;
    - held-out Task-2 set (stream 3): 256 samples;
    - gate (stream 4): 64 pairs × 32 samples with shared `c` and independent `p1`, `p2`.
  - Evaluation every 25 steps, including step 0.
    - `L1_init` = step 0;
    - `L1_pre` = step 500;
    - `L1_post` = step 1000.
- **D-TASK-B-GATE. Stage-0 conflict gate.**
  - Computed at the model initialization of each seed.
  - Gradient: the batch-mean ½‖e‖² loss, differentiated with respect to the **first-layer weight matrix** only (bias excluded).
  - For each of the 64 pairs, take the cosine between the Task-1 and Task-2 gradients.
  - The gate passes iff the mean over the 64 pairs is ≤ −0.50 **for every seed** in calibration {100..104} ∪ search {1000..1002}.
  - Stage-3 seeds are checked the same way when they are first used.
- **D-TASK-C. Task C\*.**
  - Scalar input `x ~ U[−π, π]` (stream 1).
  - `ω1 ~ U[1.4, 1.8]` and `φ1 ~ U[π/3, 2π/3]` drawn once per seed (stream 5).
  - Online schedule: R0 256, R1 64, R0 64, R1 64 steps (448 total).
  - Evaluation grid: `linspace(−π, π, 128)` for both regimes, every 4 steps including step 0.
  - Half-life for an R1 entry at step s:
    - `MSE_entry` = R1 MSE evaluated at step s;
    - the half-life is the first k ∈ {4, 8, …, 64} with `MSE_R1(s+k) ≤ (MSE_entry + 0.05)/2`;
    - it is 0 if `MSE_entry ≤ 0.05`;
    - it is +∞ if never reached.
  - Median of the two entries; the median of {x, ∞} is ∞.
  - Return check: `MSE_R0(384) ≤ max(1.10·MSE_R0(256), MSE_R0(256) + 0.01)`.
  - For averaging across seeds only, ∞ is censored at 128 (2 × segment). Raw values are stored.
- **D-TASK-F. Task F.**
  - Features 0–19 are uniform bits, with `y = x0⊕x1⊕x2`.
  - `x3` is set equal to `y` for **exactly** 90 of the 100 training examples and **exactly** 100 of the 1000 OOD examples (exact counts, positions random).
  - Streams: train set (stream 1), OOD set (stream 2), batch sampling with replacement (stream 3).
  - 500 updates at batch 32. Evaluation of the full train and OOD sets every 25 steps. Final metrics at step 500.
- **D-TASK-D. Task D.**
  - `Q` from `numpy.linalg.qr` of a standard-normal 32×32 matrix (stream 6), with signs fixed by `diag(R) > 0`.
  - `Λ = geomspace(1, κ, 32)`.
  - `θ0 ~ N(0, I)` (stream 7).
  - Exact gradients; 1000 steps; `S_τ` = first step with L ≤ 1e−4 (Cursor Task-D threshold).
  - Diverged if L > 10·L0.
  - Methods: SGD, SGDM, AdamW (standard, unclipped), and natural-gradient-like damped Newton `Δ = −(H + 1e−3 I)^{-1} g`.
  - Candidates are never run on D (v2 §6.2).
- **D-TASK-E. Task E** (reserved; finalists only).
  - Input:
    - symbol one-hot (5);
    - state one-hot (5);
    - phase flags (binding / distractor / query);
    - 5 noise dims.
  - Binding steps present `(symbol, state)`, with the target = that symbol.
  - Distractor steps show random noise with a random label.
  - The query step shows a symbol with the query flag; the target = the symbol bound to `g(s)`.
  - Each episode is an online stream, and the learning mechanism must carry the binding.
  - 128 episodes per seed, balanced query states, `L ∈ {10, 50, 200}`.
  - Also reports slow-rule accuracy on canonical successor queries.
- **D-TASK-A. Task A** (reserved; finalists only). Cursor generator: `d = 16`, `T ∈ {100, 250, 500, 1000}`, trigger at `t1 ∈ [1, 10]`, `k = 4` bits, query at `T`. On the feed-forward substrate, only register state can carry the bit.
- **D-TASK-T0. Sanity filter** (AE Stage 1b).
  - Online linear teacher: `d_in = 8`, `d_out = 2`, noise σ = 0.1, 300 steps, seed 500.
  - All three v2 learning rates run vectorized. v2 §7.1 fixes the learning-rate grid, so AE's single lr = 0.03 is replaced by the grid.
  - Pass iff some learning rate is stable and its final-50-step online MSE ≤ 0.5 × the running-mean predictor's MSE over the same steps.
  - Early stop at 50% of steps when loss ≥ trivial (AE.3.6) applies to T0 only.

## D-LR — equal learning-rate budget (v2 §7.1)

- **D-LR-1. Grid.** Every method (official controls, known-family controls, candidates, ablations, matched baselines) uses `η ∈ {1e−3, 1e−2, 1e−1}`, selected per (method, task) by a training-side metric averaged over seeds, among configurations with no unstable seed.
  - B: minimize the mean online training MSE over the last 50 steps of Task 1 plus the same over the last 50 steps of Task 2.
  - C\*: minimize the mean online training squared error over all 448 steps.
  - F: maximize full-train-set accuracy at step 500; ties go to lower train cross-entropy.
  - D: minimize final loss.

  Held-out, OOD and confirmation data never select hyperparameters.
- **D-LR-2. Other hyperparameters.** None are tuned:
  - SGDM β = 0.9;
  - AdamW (0.9, 0.999, 1e−8, weight decay 0.01, no decay on biases);
  - GPM energy threshold 0.97, with the SGD base.

## D-CAL — Stage-1 gates

**Mandatory gates.** Any failure stops the run.

- **M1 (Stage 0).** The Task-B conflict gate (D-TASK-B-GATE).
- **M2. B fit.** For each of SGD, SGDM and AdamW at its selected learning rate, the mean over seeds of held-out `L1_pre` must be < 1e−3.
  - This is the only preregistered Task-1 training threshold (Cursor Task B: "achieving MSE < 10⁻³").
- **M3. B interference.** Each generic baseline must show:
  - mean `Forgetting_B ≥ 10` pp; and
  - `L1_post > L1_pre` in every seed.
- **M4. F failure.** Each of SGD, SGDM and AdamW at its selected learning rate, as a mean over seeds at step 500, must have:
  - train accuracy ≥ 98%;
  - OOD accuracy ≤ 25%;
  - SGG ≥ 75 pp.
- **M5. Detector.** The Stage-0 test suite passes, including 100% rediscovery recall on all references and disguised variants.
- **M6. Controls run.** Every generic method has at least one stable learning rate on each of B, C\* and F.

**Known-family expected signatures.** Stop per v2 §15 on failure. The thresholds are AE.5.5 V1–V3 (AE's benchmark-validity checks), mapped to the v2 tasks.

- **V1-B.** At least one of {GPM, R17 EWC/SI, R18 k-WTA, R13 fast/slow} must:
  - reduce mean `Forgetting_B` by ≥ 15% relative to SGD; and
  - have Task-2 final MSE ≤ 1.1 × SGD's.
- **V2-C\*.** At least one of {R12 fast weights, R13 fast/slow, R15 three-factor} must reduce the seed-mean censored R1 half-life by ≥ 10% relative to SGD.
- **V3-F.** Discrete synthesis (minimal XOR-of-≤3-bits hypothesis consistent with the training set; Cursor "Discrete Synthesis") must reach OOD accuracy ≥ 95%.
- **V-D.** The natural-gradient-like control must have `S_τ ≤ 1/3 · min(S_τ(SGD), S_τ(SGDM))` at κ ∈ {1e4, 1e6}, with ∞ counted as failing for SGD / SGDM.

**Recorded, not gating.** v2 states no gate for these, and AE's V4 is superseded by v2's fixed seed counts:
- AdamW and the fast-weight columns of the Cursor signature matrix;
- the C\* task's adaptation problem size;
- unclipped generic baselines (diagnostic);
- AE V4 seed coefficient of variation.

**C\* task sanity (mandatory, M7).** The best generic baseline must satisfy both:
- `MSE_R0(256) < 0.25` (half of Var[sin x] = 0.5) — R0 was learned;
- R1 entry MSE > τ_C = 0.05 at both entries — there is something to adapt.

## D-S2 — Stage-2 search (AE.3 with v2 budgets)

- **D-S2-1. Tier 1.**
  - Tasks B, C\* and F; seeds 1000–1002; three learning rates each. Learning rate selected by D-LR.
  - Best generic baseline per task: the best of SGD / SGDM / AdamW at their selected learning rates on the same seeds, computed once before the search.
- **D-S2-2. Effects.** Metrics are oriented so that lower is better.

  | Task | Effect | Constraint (if violated, `e ← min(e, 0)`) |
  |---|---|---|
  | B | `e_B = (F_gen − F_P)/max(F_gen, 1)` | `T2_final_P ≤ 1.25 · T2_final_gen` |
  | C\* | `e_C = (hl_gen − hl_P)/max(hl_gen, 4)` on censored seed means | return check holds in ≥ 2 of 3 seeds |
  | F | `e_F = (err_gen − err_P)/max(err_gen, 0.01)` with `err = 1 − OOD acc` | train acc ≥ 98% |

  Quality: `q = max_t e_t − 0.05·log2(FLOPs_P/FLOPs_SGD) − 0.05·log2(1 + state_P/params)` (AE.3.3).
- **D-S2-3. Tier-1 minimum effect** (v2 §11 "must exceed a preregistered minimum effect"; Cursor Tier 1). On task t, the candidate must:
  - improve on AdamW's seed-mean metric by ≥ 2 × AdamW's seed standard deviation (floor 1e−9); and
  - satisfy that task's constraint.
- **D-S2-4. Stage-3 promotion** (AE.5.6).
  - q ≥ 0.15;
  - the Tier-1 minimum effect holds on the promoted task (argmax e_t);
  - at most 1 per cell, 8 per task, 20 in total;
  - ordered by q, with ties broken toward lower maximum similarity to the library.
- **D-S2-5. Random programs.**
  - Generation: typed grow method, depth 2–4.
  - Random programs are generated and screened until 200 Tier-1 evaluations exist (AE N_INIT).
  - Then up to 20 generations of 50 Tier-1-evaluated offspring, with patience 5 and crossover p = 0.2.
  - Budget caps: 6000 generated / 3000 sanity-evaluated / 1200 Tier-1.
  - Mutation probabilities: AE.3.5.
  - Invalid offspring are retried ≤ 10 times; retries count as generated.
- **D-S2-6. Records.**
  - Every generated program is logged with its raw form, canonical form (if valid), label, fingerprint, descriptor, β hash and metrics.
  - Negatives are kept.

## D-S3 — Stage-3 matched validation

- **D-S3-1. Setup.**
  - Seeds 10000–10009 with fresh task instances. Each condition selects its learning rate by D-LR on these seeds (equal budget).
  - The candidate is evaluated on its promoted task.
- **D-S3-2. Conditions.**

  | Condition | Definition |
  |---|---|
  | P | the candidate |
  | A1 | coupling cut: C1 `w_eff` / `g` → none; C2 gates → 1; C3 STRUCT → none |
  | A2 | persistent registers zeroed at the B switch, at every C\* regime entry, and every 100 steps in F |
  | A3 | persistent registers replaced at the same times by Gaussian noise of equal standard deviation |
  | A4 | `update_every` flipped 1 ↔ 8 |
  | A5a | P's ΔW fed through SGDM |
  | A5b | P's ΔW fed through AdamW moments (P∘Adam) |
  | A6 | best generic with k = ⌈FLOPs_P / FLOPs_gen⌉ updates per batch (compute-matched) |
  | A7 | best generic with hidden width widened until params ≥ P's params + persistent state floats (capacity-matched) |
  | K(P) | residual removed |

  Controls: SGD, SGDM, AdamW, and the task control (GPM for B; R12 / R13 for C\*).
- **D-S3-3. Decision.** Uses the v2 §6.1 promotion thresholds against the best generic on fresh data, plus the AE.4 gates:
  - gate 3: one-sided paired Wilcoxon, Holm-corrected over promoted (candidate, task) pairs, α = 0.05, bootstrap 95% CI (10,000 resamples) excluding 0;
  - gate 4: effect drops ≥ 50% under K(P) and under A1; P beats K(P) by ≥ τ/2;
  - gate 5: A5b keeps ≥ 50% of the effect against AdamW;
  - gate 6: beats A6 and A7 by the task threshold; FLOPs ≤ 3× SGD;
  - Cursor A1: Welch p < 0.01 degradation;
  - Cursor A7: reject if within 5%.
- **D-S3-4. Labels.** The strongest label this lane may assign is **POSSIBLE ARCHITECTURE CANDIDATE — CROSS-LANE AUDIT REQUIRED**, and only when every automated gate passes. Otherwise the label is one of:
  - `INTERESTING EMPIRICAL MECHANISM — NOVELTY AUDIT REQUIRED`;
  - `REDISCOVERY`;
  - `NEGATIVE`.

## D-ACC — accounting

- **D-ACC-1.** Parameters: Σ(o·i + o).
- **D-ACC-2.** Persistent state floats: non-EXAMPLE registers, plus `W_ep0` if read, plus scalar loss statistics if read. Controls:
  - SGDM: +P;
  - AdamW: +2P;
  - GPM: Σ(n_in+1)².
- **D-ACC-3.** FLOPs per example.
  - Analytic cost model over the compiled op list:
    - elementwise = size;
    - outer / scale = o·i;
    - matvec = 2·o·i;
    - norm / dot = 2n;
    - nrm = 5n;
    - unit = 3n;
    - topk = n·⌈log2 n⌉.
  - Plus substrate forward (2oi+3o) and, if `d_bp` is read, backward (2oi+2o) per layer above the first.
  - Plus update application.
  - STRUCT cost is amortized over 100 steps.

---

# v3 amendment and Stage-1/2 operational clarifications (session 14)

Committed **before** the v3 Stage-0 gate was computed and **before** any Stage-1 training.

- The only result visible at this point is the published v2 Stage-0 outcome:
  - Task-B cosines: all 512 negative; 3/8 seeds at ≤ −0.50; pooled −0.459;
  - Stage 0 otherwise passed.
- Nothing in this section changes a threshold, schedule, budget or rule of the v3 preregistration.
- Items marked **clarification** resolve an ambiguity in an earlier D-item in the direction the earlier text most naturally reads.

## D-V3 — v3 protocol changes (owner amendment `91bb7d8`)

- **D-V3-1. Task-B gate.** `D-TASK-B-GATE` and gate `M1` are superseded. The v3 gate:
  - Gradient: first-layer weight gradient of the batch-mean ½‖e‖² loss at the Glorot-normal initialization of each seed (unchanged).
  - Seeds: 100–104 and 1000–1002.
  - Pairs: 64 per seed, sharing `c` (unchanged).
  - The gate passes iff:
    - (1) every one of the 8 seed-level mean cosines is < 0; **and**
    - (2) at least 90% of the 512 individual cosines are < 0.
  - No magnitude threshold.
- **D-V3-2. Ratified by v3.** Glorot-normal initialization (D-SUB-1), `W_ep0` probe derivation (D-PROBE-2), and gates M2 / M3.
- **D-V3-3. Run configuration.** The v3 run configuration is written to `config/run_config_v3.json`. `config/run_config.json` is kept unchanged as the v2 record.
- **D-V3-4. Output locations.** Official Stage-0 output: `runs/stage0_v3/`. Stage-1 output: `runs/stage1/`.

## D-S1 — Stage-1 clarifications

- **D-S1-1. Official generic controls** are SGD, SGDM and AdamW run through the substrate update pipeline, with clipping (D-SUB-8) identical to candidates.
  - The same three methods without clipping run as recorded diagnostics only; they never enter a gate or a selection.
  - Known-family program controls (R12, R13, R15, R17, R18) are canonical reference programs run through `ProgramLearner`.
  - GPM is the D-LR-2 native control.
- **D-S1-2. Learning-rate selection.** Stage 1 uses seeds 100–104, the grid {1e-3, 1e-2, 1e-1}, and the D-LR-1 selection rule. All "seed-mean" quantities below are means over these 5 seeds at the selected learning rate.
- **D-S1-3. Best generic baseline** (clarification of D-S2-1 / D-CAL M7). Among SGD / SGDM / AdamW at their selected learning rates, it is the one with the lowest seed-mean task metric:

  | Task | Metric |
  |---|---|
  | B | Forgetting_B |
  | C\* | censored median R1 half-life |
  | F | OOD error |

  Ties go to the first of (SGD, SGDM, AdamW).
- **D-S1-4. M2 / M3 / M4 / M6.** Exactly as in D-CAL and v3. M3's `L1_post > L1_pre` must hold on each of the 5 seeds.
- **D-S1-5. M7** (clarification). For the best generic C\* baseline:
  - seed-mean `MSE_R0(256) < 0.25`; and
  - seed-mean R1 entry MSE > 0.05 at the first entry (step 256) **and** at the second (step 384).
- **D-S1-6. V1-B.** Pass iff some control in {GPM, R17, R18, R13} has, at its own selected learning rate, both:
  - seed-mean `Forgetting_B ≤ 0.85 ×` SGD's seed-mean `Forgetting_B`; and
  - seed-mean Task-2 final MSE ≤ 1.1 × SGD's.

  SGD here is the clipped official SGD at its selected learning rate.
- **D-S1-7. V2-C\*.** Pass iff some control in {R12, R13, R15} has a seed-mean censored R1 half-life ≤ 0.9 × SGD's.
- **D-S1-8. V3-F.** Discrete synthesis (D-TASK-F) on each calibration seed must reach a seed-mean OOD accuracy ≥ 0.95.
- **D-S1-9. V-D.** For each method and κ:
  - the selected learning rate minimizes seed-mean final loss among learning rates with no diverged seed;
  - `S_τ` is the seed-mean `S_τ` at that learning rate, or ∞ if any seed never reaches τ;
  - a method with no non-diverged learning rate has `S_τ = ∞`.

  The gate passes iff, for κ ∈ {1e4, 1e6}, `S_τ(natgrad)` is finite and `S_τ(natgrad) ≤ min(S_τ(SGD), S_τ(SGDM)) / 3`, with ∞/3 = ∞.
- **D-S1-10. M5.** Read from the official v3 Stage-0 result: test suite pass and detector recall 100%.
- **D-S1-11. Stop rule.** Any failed mandatory gate (M2–M7, V1-B, V2-C\*, V3-F, V-D) stops the run before Stage 2. Recorded-only items never stop it.

## D-T1 — Tier-1 evaluator clarifications (Stage 2)

- **D-T1-1. Baselines.**
  - Official generic baselines on the Tier-1 seeds 1000–1002 are computed once, after Stage 1 passes and before the first candidate is evaluated. They use the same selection rule.
  - The best generic per task follows D-S1-3 on these seeds.
  - AdamW's seed-level metrics feed the D-S2-3 gate.
- **D-T1-2. Evaluation.**
  - A candidate is evaluated on B, C\* and F, each with 3 seeds × 3 learning rates vectorized, and the learning rate selected per task by D-LR-1.
  - A task with no stable learning rate gets `e_t = −∞` and cannot be the promoted task.
  - If all three tasks lack a stable learning rate, the result is `tier1_unstable` (NEGATIVE: unstable).
  - A timeout or out-of-memory condition gives `tier1_error`.
- **D-T1-3. Per-seed metrics.**
  - B: `Forgetting_B`.
  - C\*: censored median half-life.
  - F: `1 − OOD accuracy`.

  Effects and constraints follow D-S2-2, using seed means.
  - The C\* return check "holds in ≥ 2 of 3 seeds".
  - The F constraint uses seed-mean train accuracy ≥ 0.98.
- **D-T1-4. Cost terms in q.** FLOPs and state are measured on the Task-B substrate `[32, 32, 32, 4]`.
  - `FLOPs_SGD` is the R1 reference program on the same substrate.
  - params = 2,276.
- **D-T1-5. Tier-1 minimum effect** (D-S2-3). On task t:
  - AdamW's seed metrics give mean `m_A` and sample standard deviation `s_A` (ddof = 1; floor 1e-9);
  - pass iff `m_A − m_P ≥ 2·s_A` and task t's constraint holds.
- **D-T1-6. Promotion** (D-S2-4). The promoted task is `argmax_t e_t`.
- **D-T1-7. Parallelism and CPU accounting.**
  - The three task evaluations of a candidate run in a pool of 3 worker processes at `nice 10`. Candidates are processed sequentially, which preserves AE.3.4 archive semantics.
  - Each worker returns its own process-CPU delta. Parent plus worker CPU is appended to the ledger after every 25 Tier-1 evaluations.
  - The cap check (30 CPU-h cumulative) runs before every Tier-1 evaluation.
- **D-T1-8. Search RNG.** `random.Random(20260928)` drives generation, mutation and parent choice. The search log is `runs/stage2/records.jsonl` (every generated program, including invalid ones and negatives).

---

# v4 amendment: operational decisions (session 15)

Committed **before** the official v4 Stage-1 run and before any Stage-2 candidate was generated. Visible at this point: the published v3 Stage-0 PASS and the v3 Stage-1 results (M2, V1-B and V2-C\* failed; all other gates passed). Nothing here changes a v4 threshold, schedule, budget or rule.

## D-V4 — Stage-1 v4 logic (owner amendment `478f590`)

- **D-V4-1. M2-v4.** For each of SGD, SGDM and AdamW at its selected learning rate:
  - `FitReduction_B = 1 − L1_pre / max(L1_init, 1e-8)`, computed per seed;
  - the gate passes iff the seed-mean is ≥ 0.95 for all three methods.

  M3 is unchanged.
- **D-V4-2. V1-B-REP joint-training representability oracle** (validity-only; never a candidate baseline).
  - Setup: seeds 100–104; Glorot initialization; exactly 1,000 updates.
  - Batches: each update draws 16 fresh Task-1 then 16 fresh Task-2 examples from the seed's Task-B training stream (stream 1; order `c, p` per task, Task 1 first). There are no episode boundaries and no early stopping.
  - Learning rate: chosen from {1e-3, 1e-2, 1e-1} to minimize the seed-mean of (mean Task-1 training MSE + mean Task-2 training MSE) over the final 50 updates, computed on the 16-example halves.
  - Evaluation: both frozen held-out sets (256 each) at step 0 and step 1,000. `RelRed_k = 1 − MSE_k(1000) / MSE_k(0)`.
  - **Optimizer (clarification; v4 does not name one).** The oracle is an existence proof of representability, so it runs with each official generic optimizer: SGD, SGDM and AdamW, through the clipped official pipeline. Each selects its own learning rate by the rule above.
  - **V1-B-REP passes iff at least one of the three optimizers has seed-mean `RelRed_1 ≥ 0.95` and seed-mean `RelRed_2 ≥ 0.95` at its selected learning rate.** All three are recorded.
- **D-V4-3. M7-v4.**
  - D-S1-5 is unchanged.
  - In addition, at least one of SGD, SGDM or AdamW must have a seed-mean censored median R1 half-life < 64 at its selected learning rate. Because censoring maps ∞ to 128, this also requires the value to be finite.
- **D-V4-4. Diagnostics.** V1-B (GPM, R17, R18, R13) and V2-C\* (R12, R13, R15) are computed exactly as in v3 and recorded as diagnostics.
- **D-V4-5. Mandatory v4 gates.**
  - M2-v4, M3, V1-B-REP, M4, M5, M6, M7-v4, V3-F and V-D.
  - M5 is read from the accepted v3 Stage-0 PASS (`runs/stage0_v3/`), which carries forward under v4.
- **D-V4-6. Files.**
  - Run configuration: `config/run_config_v4.json`.
  - Output: `runs/stage1_v4/`.
  - The v3 files (`runs/stage1/`, `config/run_config_v3.json`) are preserved unchanged.

## D-S2-v4 — Stage-2 execution details (unchanged rules; operational)

- **D-S2v4-1. Probe compilation.** Probe-evaluator compilation is cached per program. This is performance only; the numbers are identical.
- **D-S2v4-2. Implementation-defect stop.** An uncaught Python exception inside candidate evaluation is an implementation defect. More than 5 such exceptions stop the search ("repeated numerical instability indicates a grammar/compiler defect"). Numerically unstable candidates are ordinary NEGATIVE (unstable) outcomes and are counted, not stopped on.
- **D-S2v4-3. Leakage.**
  - Every seed used in Stage 2 is asserted to be < 10000.
  - Stage-3 seeds (10000–10009) and Tier-3 seeds (20000–20009) are never generated during Stage 2.
- **D-S2v4-4. Records.** The full search state is written to `runs/stage2/`:
  - `records.jsonl`: every program, with its raw form, canonical form, label, fingerprint, descriptor, β hash, family and Tier-1 metrics;
  - `archive.json`;
  - `counts.json`;
  - `promotions.json`;
  - `baselines_tier1.json`;
  - `manifest.json`.

## D-S3-v4 — Stage-3 decision details (fixed before any Stage-2 result)

For each promoted candidate on its promoted task t, the conditions of D-S3-2 are run on seeds 10000–10009 (10 seeds), each selecting its learning rate by D-LR-1.

- **Metric orientation (lower is better).**
  - B: Forgetting_B.
  - C\*: censored median R1 half-life.
  - F: OOD error.
- **Promotion thresholds** (v2 §6.1, against the best generic G at its selected learning rate, both on the same seeds).

  | Task | Requirement |
  |---|---|
  | B | `F_G − F_P ≥ 40` pp; seed-mean Retention_P ≥ 80; `T2_P ≤ 1.25 · T2_G` |
  | C\* | `hl_P ≤ 0.5 · hl_G`; the return check holds in ≥ 8/10 seeds |
  | F | seed-mean train accuracy ≥ 0.98; SGG_P ≤ 15 pp; `err_P ≤ err_G − 0.10` ("material OOD improvement" ≡ ≥ 10 pp absolute OOD gain) |

- **Gates.**
  - **Gate 1 — stable.** No unstable seed at the selected learning rate.
  - **Gate 2 — learns above trivial.**
    - B: Task-2 final MSE ≤ 0.5 × the Task-2 held-out target variance.
    - C\*: `MSE_R0(256)` ≤ 0.25.
    - F: train accuracy ≥ 0.80.
  - **Gate 3 — threshold and statistics.** The task threshold holds, **and** the one-sided paired Wilcoxon test (per-seed metric of G minus P, 10 seeds) is significant after Holm correction over all promoted (candidate, task) pairs (α = 0.05), **and** the bootstrap 95% CI (10,000 resamples) of the per-seed difference excludes 0.
    - Robustness add-on: each evolved constant (register decays, `c` constants, `k`, θ) is perturbed to its neighbouring set values one at a time. At least 70% of perturbations must retain ≥ 50% of the effect `Δ = m_G − m_P`.
  - **Gate 4 — ablations.**
    - (a) Under K(P) the effect drops by ≥ 50%: `Δ_K ≤ 0.5·Δ`.
    - (b) P beats K(P) by at least half the task threshold. The threshold τ is 40 pp for B, `0.5·hl_G` for C\* and 0.10 for F.
    - (c) Under A1 (coupling cut) the effect drops by ≥ 50%.
    - Cursor A1 check: Welch p < 0.01 that A1 is worse than P.
  - **Gate 5 — optimizer swap.** Under A5b (P∘AdamW), `Δ_{A5b vs AdamW} ≥ 0.5·Δ_{P vs AdamW}`. A5a (SGDM) is recorded.
  - **Gate 6 — resource matching.** P beats A6 (compute-matched) and A7 (capacity-matched) by at least the task threshold τ. P's FLOPs ≤ 3 × SGD's. Cursor A7 check: reject if A7's metric is within 5% of P's.
  - **Known-control comparison (v4 §7).**
    - B: strongest stable of {GPM, R17, R18, R13}.
    - C\*: strongest stable of {R12, R13, R15}.
    - The gate requires seed-mean better than that control plus one-sided Wilcoxon p < 0.05 (uncorrected).
    - If no stable control exists, it is recorded as N/A.
    - F has no stable learned known control. Discrete synthesis is a non-matched reference and is recorded.
  - **A2 / A3 / A4.** Recorded. When P has persistent registers, the top label additionally requires the effect to drop ≥ 50% under A2 or A3.
- **Labels.**
  - Gate 1 or 2 fails → **NEGATIVE** (unstable / no learning).
  - Gate 3 fails → **NEGATIVE** (no preregistered matched advantage on fresh data).
  - Gate 4(a) or 4(b) fails → **REDISCOVERY** (the effect is carried by known-family components).
  - Otherwise, if any of gate 4(c), the Cursor A1 check, gate 5, gate 6, the Cursor A7 check, the known-control comparison, the robustness add-on or the A2/A3 requirement fails → **INTERESTING EMPIRICAL MECHANISM — NOVELTY AUDIT REQUIRED**.
  - All pass → **POSSIBLE ARCHITECTURE CANDIDATE — CROSS-LANE AUDIT REQUIRED** (maximum label).
- **Tier 3.** Reserved Tasks A and E, and a locked confirmation on seeds 20000–20009, run only for candidates with the maximum label.

---

# v5 amendment (session 16)

Committed before the official v5 Stage-1 run.

- **D-V5-1.** V1-B-REP uses exactly **4,000** joint-training updates (`runners.V5_ORACLE_UPDATES`). This value is passed explicitly by `scripts/stage1_v5.py`.
  - Unchanged from D-V4-2: the ≥ 0.95 / 0.95 thresholds, the SGD / SGDM / AdamW "any optimizer" rule, clipping, Glorot initialization, the learning-rate grid, seeds 100–104, the 16 + 16 batches, and training-side selection over the final 50 updates.
  - `runners.ORACLE_UPDATES` stays 1,000, so `scripts/stage1_v4.py` still reproduces the v4 evidence.
- **D-V5-2. Files.**
  - Output: `runs/stage1_v5/`.
  - Configuration: `config/run_config_v5.json`.
  - The v3 and v4 files are preserved.
- **D-V5-3. Finality.** The 2,000- and 4,000-update results in the v4 diagnostic are **not** used as the v5 result. If the v5 oracle fails, the run stops. No further oracle change is made.
- **D-V5-4. Carried forward.** Stage-2 and Stage-3 rules are unchanged: D-T1, D-S2-v4 and D-S3-v4, as committed in `0fb4be1`.

---

# Stage-2 implementation repair 1 (session 17; owner-authorized; v5 protocol unchanged)

- **D-R1-1. The single repair.** `families.strip_gates` neutralizes `where(x, y, w)` by returning `y` when `y` already has the type of the `where` expression. Otherwise it returns the type-preserving broadcast `add(0@T, y)`, where T is the `where` expression's type. This happens only for a scalar positive branch, which the grammar permits.
  - The owner-account commit `1932379` provides this change on `main`. It is adopted unchanged.
  - Nothing else in gate stripping, K(P), canonicalization, probes, fingerprints, the generator or evaluation changed.
- **D-R1-2. Regression evidence** (`tests/test_repair1.py`; the suite is 150 tests, all passing):
  - Each of the six recorded defects (P01515, P01523, P02385, P04354, P05662, P05782) raises its recorded typing error under the pre-repair rule, and decomposes without error under the repaired rule. Every stripped expression keeps its original type.
  - Direct scalar-branch fixtures cover O and I vectors, including inside `outer(…)`.
  - Same-type branches behave as before.
  - A matrix-typed `where` is illegal in the frozen grammar, so no matrix case exists.
  - Golden snapshot: `tests/fixtures/reference_golden_pre_repair.json` was computed with the pre-repair code (`9dd8a5e`) for all 31 references × 5 variants. It records canonical form, struct and abstract hashes, fingerprint, β hash, K(P), K(P) info and family match. All 155 entries are identical after the repair.
  - The committed owner test (`test_strip_gates_preserves_type_for_scalar_where_branch`) called `serialize()` on an expression node, which raised. Only the test was changed, to use `sexpr()`.
- **D-R1-3. Rerun.** `scripts/stage2.py stage2_repair1` writes to `runs/stage2_repair1/` and refuses to overwrite an existing run. It uses the same seed (20260928), generator, budgets, filters, baselines rule, effects, q, archive and stop conditions. The first stopped run in `runs/stage2/` is preserved unchanged.
- **D-R1-4. Expected trace relation.** During random initialization, the search RNG is consumed only by program generation; screening, T0 and probes use their own streams. The raw-program sequence should therefore be identical to the first run's for all 5,782 programs, and only the labels of the six formerly defective programs can differ. Divergence would begin after the initialization phase, if Tier-1 evaluations fill the archive.
