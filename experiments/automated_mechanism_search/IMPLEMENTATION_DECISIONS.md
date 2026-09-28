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
