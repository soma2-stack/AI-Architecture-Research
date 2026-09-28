# AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md

## Status

**FROZEN DESIGN v2 — STAGES 0–3 AUTHORIZED BY OWNER**

Date: 2026-09-28

This document is the owner-level cross-lane synthesis of:

- Claude Part AE — mechanism grammar, MAP-Elites search, coupling requirement, search budget, promotion gates;
- Codex AR-141 — collision library, fingerprint/equivalence screening, anti-cheating controls, novelty decision tree, prior-art gate;
- Cursor/Gemini Automated Search Benchmark Suite — Tasks A–F, matched baselines, ablations, metrics, effect thresholds, behavioral signatures, compute envelope.

Owner authorization to execute Stages 0–3 was given in chat on 2026-09-28.

## Version 2 amendment — pre-search validity repair

Version 1 was found invalid **before Stage 1 official calibration and before any candidate search** for two independent reasons:

1. Task B simultaneously required orthogonal task subspaces and approximately anti-aligned first-layer gradients. Those requirements are mathematically incompatible for the stated construction.
2. The 16 behavioral probe tuples were referenced but never serialized, and the random seed alone did not fully specify a reproducible corpus.

Additional underspecified items were also frozen here before search:
- Task C* regime timing and adaptation target;
- Task D's role relative to the fixed candidate substrate;
- Task E episode/query protocol;
- Task F training/update budget and stopping behavior;
- equal learning-rate tuning budget for official controls/candidates.

The owner approved an in-place amendment rather than creating another preregistration document. Git history preserves v1.

**No Stage-2 candidate results existed when this amendment was made.** Earlier local calibration drafts/replays are diagnostic only and are not official preregistration evidence.

Version 2 is now the sole active protocol. Stages 0–3 remain authorized under v2; Stage 0 must restart against this amended specification. No further material protocol changes are authorized after official Stage 1 begins unless another explicit owner amendment is recorded.

---

# 1. Research question

> Can a bounded automated search discover a learning-dynamics mechanism with a reproducible matched advantage that is not equivalent to a known optimizer, loss, schedule, local learning rule, or established architecture?

A positive benchmark result is **not** sufficient for novelty.

A candidate can become an architecture candidate only after:

1. matched empirical advantage;
2. mechanism-removal evidence;
3. optimizer-decoupling evidence;
4. state/parameter/FLOP matching;
5. syntactic + behavioral + structural rediscovery screening;
6. fresh prior-art search;
7. confirmation on fresh seeds and task instances.

---

# 2. Fixed mechanism substrate

Use Claude Part AE's exact typed grammar as the implementation authority.

The pilot substrate is fixed:

- two-hidden-layer MLP;
- hidden width = 32;
- tanh hidden activations;
- float32;
- one shared mechanism program applied across layers;
- online examples;
- at most 4 persistent registers;
- at most 2 matrix registers;
- register lifetimes: EXAMPLE, EPISODE, RUN;
- at most 40 AST nodes total;
- expression depth at most 5;
- at most one structural operation;
- numerically safe forms for division/log/sqrt/exp;
- no evolved learning rate;
- no outer meta-learning loop.

The grammar compiles mechanisms into:

`STATE -> FORWARD -> CREDIT/LOCAL SIGNAL -> STATE UPDATE -> PARAMETER UPDATE`

The exact leaves, operators, state-update semantics, clipping rules, program order, constants and typing rules are frozen to Claude Part AE.

## 2.1 Architecture-level coupling requirement

A generated program is eligible for the architecture search only if it contains at least one of Claude's three coupling classes:

- **C1 — state -> forward:** learned state modifies effective weights or forward gain;
- **C2 — activity-routed credit:** activity-dependent masks/gates control which parameters receive updates;
- **C3 — structural operation:** a data-dependent structural freeze/reinitialization action.

Pure update rules with none of C1–C3 are logged as optimizer/local-rule rediscoveries and are not promoted as architecture candidates.

The program must also contain a real learning signal.

---

# 3. Excluded search families

The generator must not intentionally instantiate ordinary versions of:

- SGD / momentum / Nesterov / Adam / RMSProp / Adagrad;
- natural gradient / K-FAC / Shampoo;
- mirror descent / exponentiated gradient;
- proximal or projected-gradient families;
- PCGrad / OWM / GPM / EWC;
- ordinary eligibility traces;
- Hebbian / Oja / STDP-style rules;
- ordinary three/four-factor plasticity;
- feedback alignment / direct feedback alignment;
- target propagation;
- synthetic gradients;
- predictive coding;
- equilibrium propagation;
- Forward-Forward;
- ordinary fast weights;
- differentiable plasticity;
- learned optimizers / MAML-style meta-learning;
- standard test-time training/memory;
- DEQ / fixed-point learning;
- neural-ODE/adjoint mechanisms;
- residual/highway paths;
- ordinary recurrence/gating;
- attention;
- ordinary MoE routing;
- Cascade-Correlation / ART-style constructive growth;
- standard loss shaping or schedule-only changes.

Known components may occur inside a larger candidate, but the candidate's measured advantage must be attributable to a **non-family residual**.

---

# 4. Canonicalization and rediscovery gate

Before benchmark evaluation, every program passes the collision pipeline.

## Level A — symbolic/syntactic equivalence

Use Claude Part AE's canonicalizer:

- type checking;
- temporary inlining;
- dead-code elimination;
- constant folding;
- fixed-point rewrite simplification;
- commutative operand sorting;
- canonical register renaming;
- structural hashing.

Algebraically equivalent programs are deduplicated.

## Level B — behavioral equivalence

Use the **serialized v2 behavioral probe corpus**:

`experiments/automated_mechanism_search/config/behavioral_probes_v2.json`

Git blob SHA at freeze time:

`d5a8e0d1d91d1d1caf5ff3cbb84f9a4c76e730c1`

The serialized JSON is authoritative. Regeneration is only a verification aid.

The corpus contains exactly 16 probes with fixed dimensions:
- input-like vector dimension `I = 8`;
- output-like vector dimension `O = 6`;
- matrix dimension `M = 6 x 8`;
- four register-bank slots per probe, each containing frozen I/O/M values.

The corpus also freezes synthetic read-only credit/error leaves, loss scalars, noise leaves, episode clock, parameters, bias and input values.

The deterministic regeneration procedure is stored inside the JSON and uses:
- unsigned 32-bit `xorshift32`;
- seed `20260928`;
- exact field order recorded in the file;
- integer modulo mapping to signed decimal values;
- rounding to 8 decimal places.

Implementations must first verify the checked-in corpus exists and matches the expected Git blob before running behavioral deduplication.

For each candidate:
1. execute the canonical one-step behavioral probe evaluator on all 16 frozen tuples;
2. collect forward output, normalized parameter update, normalized bias update and normalized register-state changes;
3. concatenate them in probe order;
4. use Claude Part AE's frozen normalization/similarity rule for duplicate detection.

A seed by itself is **not** accepted as the behavioral corpus.

Near-identical update trajectories are treated as rediscoveries even when source expressions differ.

## Level C — structural fingerprint
## Level C — structural fingerprint

Use the merged fingerprint schema:

- Claude's 26 AST-derived features;
- Codex AR-141's known-family signatures and state/update organization features.

The screen must capture at minimum:

- global/local gradient use;
- fixed feedback;
- transpose dependence;
- momentum;
- second moment;
- eligibility state;
- fast weights;
- fast/slow state;
- activation-dependent updates;
- input-dependent routing;
- normalization;
- projection;
- fixed-point behavior;
- parameter birth/reinitialization/freezing;
- test-time updates;
- meta-learned updates;
- persistent state lifetime;
- forward-pass dependence on learning state.

## Level D — prior-art gate

Any empirically surviving candidate receives a fresh literature search.

It cannot be promoted if substantially the same:

- architecture;
- state organization;
- update rule;
- learning dynamic;
- or mechanism/property pairing

already exists.

Finite trace/code novelty is never sufficient evidence of architecture novelty.

---

# 5. Search algorithm

Use **MAP-Elites quality-diversity search** as specified in Claude Part AE.

Why:

- novelty/diversity is required, not only score maximization;
- a single benchmark optimum would strongly favor rediscovery;
- elites are distributed across coupling, credit-source and state-complexity niches.

Freeze Claude Part AE's 56-cell descriptor map before execution.

## Search budget

Hard maximum:

- **6,000** programs generated;
- **3,000** programs passing basic sanity checks;
- **1,200** programs receiving Tier-1 benchmark evaluation;
- **20** candidates maximum promoted to matched validation.

Stop earlier if the compute cap is reached.

Mutations/crossover, invalid-program handling and candidate selection follow Claude Part AE.

---

# 6. Benchmark allocation

The six Cursor/Gemini microbenchmarks remain part of the validation library, but the search must not directly optimize all six.

This avoids overfitting the grammar to a broad aggregate benchmark score.

## 6.1 Primary search triad

### Search Task B — Interference / retention (v2 construction)

The v1 orthogonal-subspace construction is retired because it made the requested first-layer gradient conflict impossible.

Use this frozen overlapping-subspace construction instead.

#### Input decomposition

Ambient dimension: `D = 32`.

Partition coordinates into:
- shared block `C = {0..7}` (8 dimensions);
- Task-1 private block `P1 = {8..19}` (12 dimensions);
- Task-2 private block `P2 = {20..31}` (12 dimensions).

For each paired sample:
- draw `c ~ N(0, I_8)`;
- draw `p1 ~ N(0, I_12)`;
- draw `p2 ~ N(0, I_12)`;
- Task 1 input: `x1 = [c, p1, 0]`;
- Task 2 input: `x2 = [c, 0, p2]`.

The nonzero private block implicitly identifies the task, so the two mappings are jointly representable; the task does not require contradictory labels for an identical complete input.

#### Targets

For each benchmark seed, deterministically generate fixed matrices:
- `A_c in R^(4x8)`;
- `A_1 in R^(4x12)`;
- `A_2 in R^(4x12)`;

from `numpy.random.Generator(numpy.random.PCG64(seed))`, standard normal, then row-normalize each matrix.

Targets:
- `y1 = A_c c + 0.10 A_1 p1`;
- `y2 = -A_c c + 0.10 A_2 p2`.

The shared component therefore pushes the two tasks in opposing directions while the private blocks keep the joint mapping identifiable.

#### Training protocol

- batch size: 32;
- Task 1: exactly 500 parameter-update steps;
- Task 2: exactly 500 parameter-update steps;
- no Task-1 training examples are replayed during Task 2;
- held-out Task-1 and Task-2 evaluation sets: 256 samples each, generated from separate deterministic streams;
- evaluate every 25 update steps;
- no early stopping.

#### Stage-1 validity gates

At the frozen model initialization, before training:
- form 64 paired Task-1/Task-2 mini-batches from the same shared `c` draws;
- compute first-layer gradient vectors under the same generic MLP;
- mean cosine similarity must be **<= -0.50**.

After official baseline calibration:
- each generic baseline must fit Task 1 to its preregistered training threshold;
- Task-2 training must produce measurable Task-1 degradation rather than zero interaction.

If either condition fails, Task B is invalid and the run stops for owner review.

#### Metric

Let:
- `L1_init` = held-out Task-1 MSE before Task-1 training;
- `L1_pre` = held-out Task-1 MSE immediately before Task-2 training;
- `L1_post` = held-out Task-1 MSE after Task-2 training.

Define clipped retention:

`Retention_B = 100 * clip(1 - (L1_post - L1_pre) / max(L1_init - L1_pre, 1e-8), 0, 1)`.

Define forgetting:

`Forgetting_B = 100 - Retention_B`.

Promotion threshold:
- at least **40 percentage points less forgetting** than the best generic optimizer baseline;
- `Retention_B >= 80%`;
- Task-2 final MSE must be no worse than **1.25x** the best generic baseline's Task-2 final MSE, preventing "retention by refusing to learn."

### Search Task C* — Recurring-regime adaptation (v2 frozen schedule)

Use scalar regression with no explicit regime/boundary input.

Input:
- `x ~ Uniform[-pi, pi]`.

Regimes:
- `R0: y = sin(x)`;
- for each benchmark seed draw once:
  - `omega1 ~ Uniform[1.4, 1.8]`;
  - `phi1 ~ Uniform[pi/3, 2pi/3]`;
- `R1: y = sin(omega1*x + phi1)`.

Frozen online schedule:
- R0a: 256 update steps;
- R1a: 64 update steps;
- R0b: 64 update steps;
- R1b: 64 update steps.

No task ID, regime ID, boundary bit, reset signal or segment counter is exposed to the candidate.

Evaluation:
- fixed 128-point grid on `[-pi, pi]` for each regime;
- evaluate both R0 and R1 every 4 update steps;
- no early stopping.

Adaptation target:
- `tau_C = 0.05` MSE.

For each entry into R1, adaptation half-life is the first update index at which R1 evaluation MSE reaches the midpoint between its MSE at regime entry and `tau_C`.
If the target side of that midpoint is never reached within the 64-step segment, adaptation half-life is `+infinity`.

Promotion threshold:
- median R1 adaptation half-life across the two R1 entries is at least **50% lower** than the best generic optimizer baseline;
- after return to R0, R0 evaluation MSE after 64 steps must be no greater than `max(1.10 * MSE_R0_pre_shift, MSE_R0_pre_shift + 0.01)`;
- advantage must survive state/FLOP matching and optimizer swap.

### Search Task F — Structural commitment (v2 fixed budget)

Generator remains:
- binary input dimension `D = 20`;
- true rule `y = x0 XOR x1 XOR x2`;
- `N_train = 100`;
- train shortcut correlation `P(x3 = y) = 0.90`;
- `N_OOD = 1000`;
- OOD shortcut correlation `P(x3 = y) = 0.10`;
- true parity remains 100% valid in both sets.

Training protocol:
- mini-batch size: 32;
- exactly **500 parameter-update steps**;
- sampling with replacement from the 100-example training set;
- evaluate full train and OOD sets every 25 update steps;
- **no early stopping**;
- final promotion metrics use step 500, not the best checkpoint.

Validity requirement before Stage 2:
- official generic MLP + SGD/SGDM/AdamW controls must each achieve at least 98% train accuracy by step 500;
- their OOD accuracy must be <= 25%;
- their structural generalization gap must be >= 75 percentage points.

If those frozen validity gates do not hold, Task F is invalid and the run stops for owner review. Do not alter correlations, dataset size, model capacity or update count after seeing results.

Promotion threshold:
- final train accuracy >= **98%**;
- final structural generalization gap **<= 15 percentage points**;
- final OOD accuracy materially exceeds the strongest generic matched baseline on fresh OOD instances.

## 6.2 Diagnostic Task D — optimizer-confound detector (baseline-only in v2)

Task D is **not** a candidate-program benchmark because the frozen candidate grammar targets the two-hidden-layer MLP substrate, while the direct quadratic ravine has no compatible forward/credit interface.

Freeze Task D as a baseline/diagnostic only:

- dimension: 32;
- `H = Q Lambda Q^T`;
- `Q` from deterministic QR decomposition under the benchmark seed;
- condition numbers `kappa in {1e2, 1e4, 1e6}`;
- exactly 1,000 optimizer update steps;
- no early stopping.

Use SGD, SGDM, AdamW and K-FAC/natural-gradient-like controls where implementable.

Task D may identify optimizer/preconditioner-like behavioral signatures, but **cannot directly promote or reject a candidate program**.

If a candidate's apparent advantage elsewhere is fully explained by an effective preconditioner and disappears under optimizer controls, classify it as optimizer/preconditioner rediscovery.

## 6.3 Reserved validation Tasks A and E

Tasks A and E are not used to select MAP-Elites.

### Task A — long-range credit

Keep the existing frozen delayed-bit generator and horizon set. It is reserved for finalist characterization only.

### Task E — fast/slow state and distractor-resistant binding (v2 frozen protocol)

Slow rule:
- five latent states `0..4`;
- fixed successor function `g(s) = (s + 1) mod 5`.

Each episode:
1. sample a deterministic random permutation mapping five episode symbols to the five latent states;
2. present all five symbol/state binding examples once;
3. present `L` unrelated distractor examples;
4. query one episode symbol;
5. target is the episode symbol bound to the successor latent state `g(s)`.

Distractor lengths:
- `L in {10, 50, 200}`.

Evaluation:
- 128 independent episodes per seed;
- balanced query states;
- report query accuracy separately for each distractor length;
- also report slow-rule accuracy on canonical latent-state successor queries.

Finalists are characterized on Task E only after Tier-2 promotion. Task E does not decide MAP-Elites selection.

A finalist does not need to win Tasks A or E. They are used to establish behavioral scope and detect hidden equivalence to known families.

---

# 7. Mandatory baselines---

# 7. Mandatory baselines

Every evaluated candidate is compared with:

1. SGD;
2. SGD + Polyak momentum beta = 0.9;
3. AdamW;
4. target-property-specific known method.

## 7.1 Equal hyperparameter budget

Official Stage-1 controls and candidate comparisons use the same learning-rate search budget:

`eta in {1e-3, 1e-2, 1e-1}`.

For each method, choose the learning rate only from training-side calibration metrics defined for that task. OOD/confirmation results may not choose hyperparameters.

No method receives early stopping in Tasks B, C* or F.

Any pre-v2 local calibration run that used unequal fixed learning rates or early stopping is **diagnostic only** and cannot satisfy Stage 1.

Target-property controls follow Cursor/Gemini's suite, including appropriate families such as:

- GPM/OWM for interference;
- MAML/fast-weight-style controls for adaptation;
- K-FAC or strong normalization/adaptive-optimizer controls for conditioning diagnostics;
- constructive/discrete learners for structural commitment where matched comparison is meaningful.

---

# 8. Matching and anti-cheating rules---

# 8. Matching and anti-cheating rules

A result is invalid unless controls account for:

- trainable parameter count;
- persistent-state bytes;
- cumulative FLOPs;
- number of update opportunities;
- forward/backward passes;
- initialization seeds;
- learning-rate tuning budget;
- clipping;
- normalization;
- stopping policy;
- data exposure.

Parameter counts should match within **±5%** where practical.

If exact matching is impossible, record the mismatch and construct the strongest compensating baseline.

The candidate may not win merely because it has:

- larger effective learning rate;
- extra state;
- extra compute;
- extra parameters;
- hidden lookahead;
- more data;
- extra training steps;
- a better initialization search;
- adaptive stopping;
- implicit ensembling.

---

# 9. Mandatory ablations

Every candidate promoted beyond Tier 1 must receive the seven Cursor/Gemini ablations where applicable:

1. mechanism removed;
2. persistent state zeroed;
3. persistent state randomized;
4. update timing shifted;
5. optimizer swapped;
6. state/FLOP-matched control;
7. parameter-matched control.

In addition, Claude's **non-family residual ablation** is mandatory:

> remove the part of the program not explained by its nearest known-family decomposition.

The claimed property must materially collapse.

---

# 10. Metrics

Do not collapse the experiment to one accuracy score.

Record as applicable:

- Area Under Learning Curve;
- Steps-to-Threshold;
- forgetting percentage;
- backward transfer;
- forward transfer;
- adaptation half-life;
- retention half-life;
- accuracy improvement per FLOP;
- loss improvement per update;
- stability variance;
- structural generalization gap.

Raw final accuracy is secondary to the learning-dynamics property.

---

# 11. Statistical/selection controls

## Tier 0 — implementation validity

Before search:

- grammar type checker;
- canonicalizer;
- known-family fingerprint tests;
- deterministic behavioral probes;
- benchmark generator tests.

No search begins until these pass.

## Tier 1 — search evaluation

- 3 seeds;
- fresh procedural samples;
- strict per-candidate timeout;
- candidates must exceed a preregistered minimum effect rather than merely rank first.

## Tier 2 — matched validation

For no more than 20 candidates:

- 5 seeds minimum;
- seven ablations + residual ablation;
- optimizer swaps;
- state/parameter/FLOP controls;
- fresh task instances not used in search.

## Tier 3 — confirmation

Only for candidates surviving Tier 2:

- new seeds;
- locked task generators;
- reserved Tasks A/E as applicable;
- Codex novelty audit;
- fresh literature review.

Do not repeatedly tune on the confirmation set.

---

# 12. Automatic rejection rules

Reject immediately for:

- NaN/Inf;
- loss > 10x initial loss;
- memory > 512 MB per candidate process;
- timeout > 120 s per seed in screening;
- no measurable learning;
- pure update rule with no architecture-level coupling;
- syntactic/behavioral duplicate;
- known-family fingerprint match with no non-family residual;
- result explained by extra compute/state/parameters.

---

# 13. Compute envelope

Pilot is **CPU only**.

Model scale:

- hidden width roughly 16–64;
- approximately 1e3–5e4 trainable parameters;
- batch sizes roughly 8–32 where batching is used;
- sequence lengths no larger than the frozen benchmark specification.

Budget:

- expected search cost: approximately **6–8 CPU-hours**;
- **hard cap: 30 CPU-hours total** for Stages 0–3;
- no GPU use;
- no larger follow-up run;
- no automatic extension of the budget.

Parallel execution may reduce wall-clock time, but accounting is in cumulative CPU-hours.

Any GPU or larger-scale confirmation requires a separate owner authorization.

---

# 14. Outcome labels

Every searched mechanism ends in exactly one of:

### REDISCOVERY
Equivalent or substantially identical to a known optimizer, rule, loss, schedule, or architecture.

### NEGATIVE
Valid distinct program, but no preregistered matched advantage.

### INTERESTING EMPIRICAL MECHANISM
Distinct under current screens and shows a reproducible property advantage, but architecture novelty is not established.

### ARCHITECTURE CANDIDATE
May be used only after:

- Tier-2 matched validation;
- mechanism/residual ablations;
- optimizer decoupling;
- resource matching;
- Tier-3 confirmation;
- Codex equivalence audit;
- fresh prior-art review;
- cross-lane agreement that the property is architectural.

No automated system may label its own output a new architecture.

---

# 15. Global stop conditions

Stop the search immediately if:

- benchmark validity controls fail;
- known-family controls do not show their expected behavioral signatures;
- Task F does not create the preregistered baseline structural-generalization failure;
- implementation/canonicalization tests are unreliable;
- the 30 CPU-hour cap is reached;
- repeated numerical instability indicates a grammar/compiler defect;
- confirmation data have accidentally leaked into search.

The protocol may not be silently modified after search results are visible.

Any material protocol change requires a new preregistration version.

---

# 16. Promotion decision tree

For each apparent winner:

1. Did it execute stably?
2. Did it learn?
3. Did it exceed the frozen effect threshold on fresh data?
4. Did mechanism removal erase the effect?
5. Did non-family residual removal erase the effect?
6. Did it survive optimizer swap?
7. Did it beat state/parameter/FLOP-matched controls?
8. Is it syntactically distinct from the collision library?
9. Is it behaviorally distinct?
10. Is its architecture/state organization structurally distinct?
11. Did it survive locked confirmation?
12. Did fresh prior-art search fail to find the same mechanism?

If any required answer is no, do not call it an architecture candidate.

---

# 17. Execution stages

## Stage 0 — compiler and validity tests

Implement only the grammar, canonicalizer, fingerprinting, known-family unit cases and benchmark generators.

Stage 0 must additionally verify:
- the checked-in behavioral probe corpus exists and matches blob `d5a8e0d1d91d1d1caf5ff3cbb84f9a4c76e730c1`;
- the Task-B overlapping-subspace construction satisfies the frozen gradient-conflict gate;
- Tasks C*, D, E and F match the v2 fixed schedules exactly.

Because v1 was invalidated before official Stage 1, all official Stage-0 evidence must be regenerated under v2.

## Stage 1 — calibration

Run established mechanisms and ordinary baselines **from the v2 implementation**.

Earlier pre-v2 calibration replays are not official evidence.

Purpose:
- validate tasks;
- validate behavioral signatures;
- validate effect metrics;
- validate equivalence detector.

Abort if controls do not behave as preregistered.

## Stage 2 — automated search
Run the frozen MAP-Elites search within the candidate and compute budgets.

## Stage 3 — matched validation
Evaluate no more than 20 promoted mechanisms using fresh seeds, ablations and matched controls.

## Stage 4 — larger confirmation
Not authorized by this preregistration.

Requires a separate owner decision.

---

# 18. Authorization state

As of this commit:

- protocol design: COMPLETE;
- GitHub consolidation: COMPLETE;
- Stage 0: **AUTHORIZED**;
- Stage 1: **AUTHORIZED**;
- Stage 2: **AUTHORIZED**;
- Stage 3: **AUTHORIZED**;
- GPU confirmation: **NOT AUTHORIZED**.

Owner authorization for Stages 0–3 was given in chat on 2026-09-28.

The v2 protocol, CPU-only execution rule, and 30 CPU-hour hard cap remain binding. Any further material protocol change, any GPU use, or any larger follow-up run requires separate owner authorization.
