# AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md

## Status

**FROZEN DESIGN — NOT AUTHORIZED TO EXECUTE**

Date: 2026-09-28

This document is the owner-level cross-lane synthesis of:

- Claude Part AE — mechanism grammar, MAP-Elites search, coupling requirement, search budget, promotion gates;
- Codex AR-141 — collision library, fingerprint/equivalence screening, anti-cheating controls, novelty decision tree, prior-art gate;
- Cursor/Gemini Automated Search Benchmark Suite — Tasks A–F, matched baselines, ablations, metrics, effect thresholds, behavioral signatures, compute envelope.

No experiment is authorized by this file. Execution requires a later explicit owner instruction.

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

Use fixed preregistered probe tuples.

Compare one-step forward/update behavior and state changes after scale normalization.

Near-identical update trajectories are treated as rediscoveries even when source expressions differ.

Claude Part AE's probe seed, normalization and similarity thresholds are authoritative.

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

### Search Task B — Interference / retention

Use Cursor Task B.

Target:
- sequential conflicting learning;
- catastrophic interference;
- persistent protection of earlier knowledge.

Promotion threshold:
- at least **40 percentage points less forgetting** than the best generic optimizer baseline;
- Task-1 retention at least **80%**;
- Task-2 acquisition must remain competitive rather than solving retention by refusing to learn.

### Search Task C* — Recurring-regime adaptation

Use Cursor Task C as the base generator, modified to include Claude's stronger requirement:

- regimes may recur;
- no explicit boundary signal is supplied to the candidate.

Target:
- rapid adaptation;
- retention/recovery;
- fast/slow learning-state behavior.

Promotion threshold:
- at least **50% lower adaptation half-life** than the best generic optimizer baseline;
- no more than **5 percentage points** degradation when returning to the original regime;
- advantage must survive state/FLOP matching.

### Search Task F — Structural commitment

Use Cursor Task F.

Target:
- correct discrete invariant induction despite a strong spurious shortcut.

Validity requirement before search:
- the generic MLP + SGD/SGDM/AdamW controls must demonstrate the intended structural-generalization failure on the frozen task generator.
- If they do not, Task F is invalid and the search pauses for owner review rather than changing the task post hoc.

Promotion threshold:
- training accuracy at least **98%**;
- structural generalization gap **<= 15 percentage points**;
- material improvement over the strongest generic matched baseline on fresh OOD instances.

## 6.2 Diagnostic Task D — optimizer-confound detector

Cursor Task D is **not a primary search objective**.

It is used to identify optimizer/preconditioning rediscoveries.

If a candidate's strongest advantage is conditioning and:

- the advantage disappears against AdamW/K-FAC-like controls;
- or disappears under optimizer swap;
- or is explained by an effective preconditioner,

classify it as optimizer/preconditioner rediscovery, not a new architecture.

## 6.3 Reserved validation Tasks A and E

Tasks A and E are not used to select MAP-Elites.

They are reserved for finalists to test transfer of the discovered learning dynamic:

- A: long-range credit;
- E: fast/slow state and distractor-resistant binding.

A finalist does not need to win every reserved task. The purpose is to identify its behavioral scope and detect hidden equivalence to known families.

---

# 7. Mandatory baselines

Every evaluated candidate is compared with:

1. SGD;
2. SGD + Polyak momentum beta = 0.9;
3. AdamW;
4. target-property-specific known method.

Target-property controls follow Cursor/Gemini's suite, including appropriate families such as:

- GPM/OWM for interference;
- MAML/fast-weight-style controls for adaptation;
- K-FAC or strong normalization/adaptive-optimizer controls for conditioning diagnostics;
- constructive/discrete learners for structural commitment where matched comparison is meaningful.

---

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

## Stage 1 — calibration
Run established mechanisms and ordinary baselines.

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
- Stage 0: **NOT AUTHORIZED**;
- Stage 1: **NOT AUTHORIZED**;
- Stage 2: **NOT AUTHORIZED**;
- Stage 3: **NOT AUTHORIZED**;
- GPU confirmation: **NOT AUTHORIZED**.

Execution begins only after an explicit owner instruction authorizing the preregistered pilot.
