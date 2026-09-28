# AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md

## Status

**FROZEN DESIGN v6 — STAGES 0–3 AUTHORIZED BY OWNER**

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

Version 2 was the active protocol for the first official Stage-0 implementation.

## Version 3 amendment — Task-B Stage-0 gate repair

Official v2 Stage 0 completed before any Stage-1 calibration or candidate search. The implementation passed 114/114 tests, verified the frozen behavioral-probe corpus, and achieved 100% rediscovery recall on the reference/disguise self-checks. It stopped correctly because the v2 Task-B gradient-conflict gate failed.

The v2 Task-B construction itself is retained. Across the eight predeclared calibration/search seeds, all 512 paired first-layer gradient cosines were negative, but the v2 magnitude rule (`mean cosine <= -0.50` for every seed) passed only 3/8 seeds. The pooled mean was approximately -0.459. The result also depended materially on an initialization choice that v2 had not frozen.

Because no Stage-1 training and no Stage-2/3 candidate result existed, the owner authorized this pre-search in-place repair. Git history preserves v1 and v2.

v3 makes the smallest protocol change needed:
- retain the v2 Task-B data construction, targets, schedules, metrics and promotion thresholds;
- freeze the model initialization to the already predeclared **Glorot-normal** initialization used by the official v2 Stage-0 implementation; do not switch to an initialization that looked better in the post-hoc sensitivity analysis;
- replace the arbitrary magnitude gate with a directional-consistency gate that tests the intended property: systematic negative cross-task first-layer gradient conflict;
- ratify the already predeclared Stage-1 Task-B fit/interference gates;
- ratify the deterministic `W_ep0` behavioral-probe derivation already committed before any candidate search.

All other v2 rules and the implementation decisions committed before the v2 gate remain frozen unless explicitly superseded below.

Version 3 governed the first official Stage-1 calibration.

## Version 4 amendment — Stage-1 calibration repair before search

Official v3 Stage 0 passed. Official v3 Stage 1 then stopped before any candidate search because three calibration gates failed:
- M2-B used an absolute Task-1 fit target of `L1_pre < 1e-3`, while all three generic baselines learned Task 1 by about 99% relative error reduction but plateaued near 0.016;
- V1-B required a particular existing continual-learning control to show a strong retention signature, but none of the frozen controls did so on this severe conflict construction;
- V2-C* required a fast/slow reference to beat SGD, but the frozen R12/R13 all-layer fast-weight templates diverged on the linear output layer and R15 was slower than SGD.

No Stage-2 candidate was generated or evaluated and Stage 3 did not run. The owner therefore authorized this in-place calibration amendment. Git history preserves v1-v3.

v4 **does not change**:
- the candidate grammar;
- Tasks B, C*, F generators or schedules;
- Stage-2 search budgets;
- candidate promotion thresholds;
- state/parameter/FLOP matching;
- ablations;
- rediscovery gates;
- CPU/GPU limits.

v4 changes only the pre-search calibration logic:
1. replace M2-B's unrealistic absolute fit threshold with a scale-free relative-learning requirement;
2. replace V1-B's requirement that a named continual-learning method must win with a joint-training representability oracle proving the fixed substrate can represent both Task-B mappings at once;
3. keep GPM/R17/R18/R13 as recorded Task-B known-family controls, but their failure to improve is no longer itself a stop condition;
4. demote V2-C*'s R12/R13/R15 positive-control win to a recorded diagnostic because the frozen all-layer fast-weight references are not stable positive controls on this substrate;
5. strengthen the generic C* sanity gate so at least one ordinary baseline must actually adapt within a 64-step R1 segment;
6. retain V3-F and V-D as mandatory positive-control signatures.

The official v3 Stage-0 PASS remains valid because v4 changes no Stage-0 rule or implementation. Stage 0 does not need to be rerun. Official Stage 1 must rerun under v4 before Stage 2 may begin.

Version 4 governed the second official Stage-1 calibration.

## Version 5 amendment — final Task-B representability-oracle budget repair

Official v4 Stage 1 stopped before any candidate search because the sole failing mandatory gate was V1-B-REP, the joint-training representability oracle. Every other mandatory v4 gate passed.

At the frozen 1,000-update oracle budget, the best official result (clipped SGD, lr 0.1) achieved seed-mean relative error reductions of approximately 0.914 on Task 1 and 0.904 on Task 2, below the frozen 0.95/0.95 requirement.

A post-failure diagnostic, recorded as diagnostic-only evidence, showed:
- removing clipping did not solve the 1,000-update gate;
- clipped SGD at 2,000 updates reached approximately 0.950 / 0.945, still failing Task 2;
- clipped SGD at 4,000 updates reached approximately 0.967 / 0.960, clearing the original 0.95 / 0.95 representability threshold.

The purpose of V1-B-REP is **representability**, not training-speed comparison. The owner therefore authorized one final pre-search amendment that changes only the oracle's convergence budget.

v5 changes exactly one calibration quantity:
- V1-B-REP uses **exactly 4,000 joint-training updates** instead of 1,000.

v5 explicitly retains:
- the original 0.95 relative-error-reduction threshold on both tasks;
- the official clipped update pipeline;
- SGD, SGDM and AdamW as the three oracle optimizers;
- Glorot initialization;
- the LR grid `{1e-3, 1e-2, 1e-1}`;
- 16 fresh Task-1 + 16 fresh Task-2 examples per update;
- no early stopping;
- training-side LR selection only;
- all Task-B/C*/F candidate schedules and promotion thresholds;
- all Stage-2/3 budgets, ablations, matching and novelty gates.

The v4 diagnostic result at 4,000 updates motivated the budget choice and is preserved transparently in Git history. It is not itself accepted as the official v5 gate result; v5 Stage 1 must be rerun from a clean committed implementation.

**No further Task-B calibration amendment is permitted before Stage 2.** If V1-B-REP fails under the frozen 4,000-update v5 oracle, Stage 2 remains blocked and Task B must be dropped or the pilot terminated under a separate owner decision rather than tuning this oracle again.

The accepted v3 Stage-0 PASS remains valid because v5 changes no Stage-0 rule. Official Stage 1 must rerun under v5 before Stage 2 may begin.

Version 5 governed the completed calibration and the first two Stage-2 attempts.

## v5 implementation repair record — Stage-2 `strip_gates` defect

Official v5 Stage 1 passed every mandatory gate. Stage 2 then began under the frozen search protocol and stopped at 5,782 generated programs because the precommitted implementation-defect counter exceeded five.

All six exceptions shared one implementation root cause in the non-family residual decomposition: neutralizing a legal `where` gate by returning its positive branch directly could replace a vector-typed subtree with a scalar branch, producing an ill-typed residual tree.

This is an implementation defect, not a protocol parameter or candidate result. No program reached Tier-1 benchmark evaluation and no candidate was promoted before the stop.

The repair is frozen as:
- when the positive `where` branch already has the gate's output type, return it unchanged;
- when the positive branch is scalar, preserve the gate's vector output type by broadcasting it as `add(0@T, scalar_branch)`;
- add a regression test proving scalar-branch gate stripping preserves the original type.

A Stage-2 rerun is permitted under the existing Stage-2 authorization **only** with:
- search seed `20260928`;
- the same generator;
- the same sanity filter;
- the same 6,000 generated / 3,000 sanity / 1,200 Tier-1 / 20 promoted caps;
- the same candidate thresholds, baselines and accounting rules;
- a fresh output directory/manifest so the stopped run remains intact.

Do **not** seed from known-family mutants, relax T0, enlarge the generation budget, change mutation probabilities, or otherwise tune the search based on the first run's zero-yield observation.

If the repaired exact rerun again reaches 6,000 generated programs with zero Tier-1 evaluations, record that as a **search-design negative for this frozen generator/filter configuration**, not as evidence that no mechanism exists in the grammar.

## Version 6 amendment — learnability-anchored Stage-2 generator

The repaired v5 Stage-2 rerun completed the full 6,000-program budget with:
- 0 implementation defects;
- 382 programs reaching the unchanged T0 sanity filter;
- 0/382 passing T0;
- 0 Tier-1 benchmark evaluations;
- 0/56 archive cells occupied;
- 0 promoted candidates.

The raw-program trace matched the first run through program 5,782 except for the six repaired defect labels, and the additional programs 5,783–6,000 were also rejected before Tier 1.

This is a **search-design negative for the v5 uniform random typed generator**, not a negative result about the grammar or the existence of a novel mechanism.

The owner authorizes v6 to change **only the Stage-2 initial candidate generator**. Benchmark tasks, T0, Tier-1 metrics, MAP-Elites quality, promotion thresholds, novelty screens, compute limits and Stage-3 rules remain unchanged.

### v6 initial generator: SGD-anchored architecture residuals

The first-stage candidate constructor is replaced by a learnability-anchored constructor.

Every initial proposal starts from the exact R1 SGD parameter-update backbone:

- `dW_base = neg(outer(d_bp, a))`
- `db_base = neg(d_bp)`
- `update_every = 1`

The constructor then adds exactly **one primary architecture-level coupling class**, chosen uniformly from C1, C2 and C3.

#### C1 — state -> forward

- Create exactly one persistent register of type O or M, chosen uniformly.
- Lifetime: RUN.
- Init: 0.
- Decay chosen uniformly from `{0.5, 0.9, 0.99}`.
- Its update expression is drawn from the existing typed grammar at depth 1–2 and must contain at least one activity leaf from `{a, z, h, dphi}`.
- If the register type is M:
  - `w_eff = mul(tanh(reg), 0.1)`.
- If the register type is O:
  - `gain = add(1.0, mul(tanh(reg), 0.1))`.
- Parameter updates remain exactly the SGD backbone.

#### C2 — activity-routed credit/update

- No persistent register is required.
- Draw an O-typed selector expression from the existing PARAM-phase grammar at depth 1–2.
- The selector must contain at least one activity leaf from `{z, h, dphi}`.
- Define:
  - `g = add(1.0, mul(tanh(selector), 0.1))`
  - `dW = rowscale(dW_base, g)`
  - `db = mul(db_base, g)`
- No other parameter-update modification is added in the initial constructor.

#### C3 — data-dependent structural operation

- Create exactly one O-typed persistent register.
- Lifetime: RUN.
- Init: 0.
- Decay chosen uniformly from `{0.5, 0.9, 0.99}`.
- Its update expression is drawn from the existing typed grammar at depth 1–2 and must contain at least one activity leaf from `{z, h, dphi}`.
- Parameter updates remain exactly the SGD backbone.
- Structural kind is chosen uniformly from `{freeze, reinit}`.
- Structural mask is `tanh(reg)`.
- Threshold is chosen uniformly from the existing frozen `{0.0, 0.1, 0.5}` set.

### Constructor invariants

Every v6 initial proposal must, by construction:
- be type-valid;
- satisfy the existing node/depth/register limits;
- contain a real backprop learning signal;
- contain at least one of C1/C2/C3;
- preserve the exact SGD backbone as specified above;
- remain subject to the unchanged syntactic, behavioral and structural rediscovery filters.

If an internal construction attempt is invalid because of a grammar/node-limit issue, it is retried at most 10 times and **every attempted proposal counts toward the 6,000 generated-program cap**.

The constructor must not inspect T0, B, C* or F outcomes while generating a program.

### Search evolution after initialization

The existing MAP-Elites logic is retained:
- initialization continues until 200 Tier-1 evaluations exist or a frozen budget/stop condition fires;
- after the archive is seeded, use the existing v5 mutation probabilities, crossover probability, archive semantics, patience rule and generation limits unchanged;
- offspring are not required to preserve the SGD backbone; the normal collision, T0 and Tier-1 filters decide whether they survive.

If the archive is empty, new proposals come from the v6 anchored constructor rather than the v5 uniform random constructor.

### v6 search seed and budgets

Use search RNG seed:

`2026092806`

Budgets remain:
- max 6,000 generated;
- max 3,000 T0 sanity evaluations;
- max 1,200 Tier-1 benchmark evaluations;
- max 20 promoted candidates;
- CPU only;
- 30 cumulative CPU-hour hard cap;
- no Stage 4;
- no GPU.

### v6 implementation validity before search

Before the official v6 Stage-2 run:
- add unit tests for all three constructor classes;
- statically generate 1,000 proposals from a separate non-official test seed;
- verify type validity, node/depth/register limits, learning-signal presence, coupling-class presence and exact SGD-backbone invariants;
- do **not** evaluate those 1,000 proposals on T0 or any benchmark task;
- verify the existing reference/disguise collision golden snapshot remains unchanged.

The accepted v3 Stage-0 PASS and v5 Stage-1 PASS carry forward because v6 changes neither the grammar semantics nor any benchmark/calibration rule.

### Interpretation

A v6 positive result is still only an empirical mechanism candidate and must pass the unchanged Stage-3 ablations, resource matching, rediscovery screening and fresh prior-art review.

A v6 zero-yield or no-promotion result is a negative result for this **SGD-anchored architecture-residual search design**, not proof that no novel mechanism exists.

**Version 6 is now the sole active protocol.** Stages 0–3 remain authorized. Claude is the primary v6 search runner; Codex and Cursor/Gemini are independent implementation/result auditors and must not duplicate the full search.

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

For the probe-only `W_ep0` leaf, which is not serialized in the corpus, v3 ratifies the deterministic pre-search implementation rule:
- for probe `k`, use the serialized `W` matrix from probe `(k + 1) mod 16`.
- this derivation is part of the frozen probe evaluator and may not be changed after Stage 1 begins.

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

### Search Task B — Interference / retention (v3 gate; v2 construction retained)

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

#### Stage-0 gradient-conflict validity gate (v3)

Initialization is frozen to the official Stage-0 implementation choice:
- Glorot-normal weights with `std = sqrt(2 / (fan_in + fan_out))`;
- zero biases;
- tanh hidden activations.

Do **not** substitute LeCun, He or another initialization based on the v2 post-hoc diagnostic.

Use exactly the predeclared seed set:
- Stage-1 calibration seeds `100..104`;
- Stage-2 Tier-1 seeds `1000..1002`.

For each seed:
- form 64 paired Task-1/Task-2 mini-batches from the same shared `c` draws;
- compute the gradient of the batch-mean `0.5 * ||e||^2` loss with respect to the **first-layer weight matrix only**;
- compute the cosine between paired Task-1 and Task-2 gradients.

The v3 Stage-0 gate passes iff:
1. the mean cosine is **< 0 for every one of the 8 seeds**; and
2. at least **90% of all 512 paired gradient cosines are < 0**.

There is no additional magnitude threshold. The Stage-0 gate establishes directional conflict only; actual harmful interference is tested empirically in Stage 1.

#### Stage-1 Task-B validity gates (v4)

Using the frozen equal learning-rate grid and no early stopping:

- **B fit (M2-v4):** for each of SGD, SGDM and AdamW at its selected learning rate, define
  `FitReduction_B = 1 - L1_pre / max(L1_init, 1e-8)`.
  The seed-mean `FitReduction_B` must be **>= 0.95**. This gate asks whether Task 1 was substantially learned; it no longer demands an arbitrary absolute MSE scale.
- **B interference (M3, unchanged):** for each of SGD, SGDM and AdamW:
  - seed-mean `Forgetting_B >= 10` percentage points; and
  - `L1_post > L1_pre` on every calibration seed.
- **B representability oracle (V1-B-REP):** the same two-hidden-layer MLP must be able to represent both frozen Task-B mappings when replay/interleaving is allowed:
  - same calibration seeds and Glorot initialization;
  - same LR grid `{1e-3, 1e-2, 1e-1}`;
  - exactly **4,000 updates**;
  - batch size 32 with exactly 16 Task-1 and 16 Task-2 fresh examples in every update;
  - no early stopping;
  - LR selected by the mean of Task-1 and Task-2 training MSE over the last 50 updates;
  - on held-out sets, both Task-1 and Task-2 must achieve seed-mean relative error reduction **>= 0.95** against their own initialization MSE.

The representability oracle is a benchmark-validity control only. It is not an eligible baseline for candidate promotion because it receives replay from both tasks.

GPM, R17, R18 and R13 remain recorded known-family Task-B controls and remain eligible as relevant matched controls when stable, but their failure to reduce forgetting is **not** a Stage-1 stop condition under v4.

If the v3 Stage-0 directional-conflict gate, M2-v4, M3, or V1-B-REP fails, Task B is invalid and the run stops for owner review. Under v5, V1-B-REP is the frozen 4,000-update oracle and may not be amended again before search.

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

#### Stage-1 C* calibration rule (v4)

The generic C* sanity gate is mandatory:
- the best generic baseline must learn R0 to seed-mean `MSE_R0(256) < 0.25`;
- seed-mean R1 entry MSE must exceed `tau_C = 0.05` at both entries;
- at least one of SGD/SGDM/AdamW must have a **finite seed-mean censored R1 adaptation half-life < 64 updates**, demonstrating measurable adaptation within an R1 segment.

R12 fast weights, R13 fast/slow and R15 three-factor remain recorded known-family diagnostics. Their failure to beat SGD does **not** stop Stage 1 under v4. Unstable controls remain recorded as unstable and may not be used as a matched denominator.

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

Target-property controls follow Cursor/Gemini's suite where they are stable and compatible with the substrate, including appropriate families such as:

- GPM/OWM-style controls for interference;
- stable fast/slow or three-factor controls for adaptation;
- K-FAC or strong normalization/adaptive-optimizer controls for conditioning diagnostics;
- constructive/discrete learners for structural commitment where matched comparison is meaningful.

For Task B Stage-3 matching, use the strongest stable relevant control among GPM/R17/R18/R13 in addition to the generic baselines.

For Task C* Stage-3 matching, use the strongest stable relevant control among R12/R13/R15. A control that is unstable on the frozen task is recorded but is not used as the comparison denominator.

The joint-training Task-B representability oracle is validity-only and is never a candidate baseline because it receives replay unavailable to candidates.

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

- a **mandatory v4 benchmark/calibration validity control** fails;
- mandatory positive-control signatures V3-F or V-D fail;
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

Because v3 supersedes the failed v2 Task-B Stage-0 gate, official Stage 0 must be rerun under v3. The v2 114-test result remains valid implementation evidence, but the v3 gate result must be newly recorded before Stage 1.

## Stage 1 — calibration

Run established mechanisms and ordinary baselines **under v5**.

The v3 and v4 Stage-1 runs are preserved as calibration evidence. Neither authorized Stage 2 because their then-mandatory gates failed.

Purpose:
- validate tasks;
- validate mandatory v5 benchmark controls;
- record known-family behavioral signatures;
- validate effect metrics;
- validate equivalence detector.

Mandatory v5 gates include:
- M2-v4 Task-B relative fit;
- M3 Task-B interference;
- V1-B-REP joint-training representability oracle;
- Task-F generic failure;
- C* generic sanity including finite adaptation within a segment;
- detector/implementation validity;
- generic-control stability;
- V3-F;
- V-D.

R12/R13/R15 C* positive-control wins and GPM/R17/R18/R13 Task-B retention wins are recorded diagnostics, not mandatory v5 stop gates.

Abort if any mandatory v5 control fails. V1-B-REP must use exactly 4,000 updates; do not retune it.

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

The v6 protocol, CPU-only execution rule, and 30 CPU-hour hard cap remain binding. Any further material protocol change, any GPU use, or any larger follow-up run requires separate owner authorization.
