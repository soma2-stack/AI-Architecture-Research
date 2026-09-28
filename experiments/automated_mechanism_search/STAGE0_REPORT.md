# AMS v2 — Official Stage-0 report and stop notice

**Verdict: STAGE 0 FAILED — PREREGISTRATION VALIDITY FAILURE (v2): Task-B gradient-conflict gate.**

**Stage 1 was not legally allowed and was not started.** No calibration run, candidate search or Stage-3 validation took place. Task B was not redesigned. No frozen threshold, schedule, budget or rule was changed.

- Protocol: `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` v2 (sole active protocol).
- Date: 2026-09-28.
- Machine-readable results: `runs/stage0/stage0_result.json` and `runs/stage0/manifest.json`.

## 1. What Stage 0 contains

The package is `ams/`.

| Item (owner list) | Module | Tested by |
|---|---|---|
| Typed grammar, compiler, phase availability, size limits | `grammar.py`, `interp.py` | `test_grammar.py` (31 references + 21 invalid fixtures), `test_interp_substrate.py::test_shapes` |
| Register semantics (EXAMPLE / EPISODE / RUN, read-before-write, PARAM sees new values) | `substrate.py` | `test_interp_substrate.py` |
| C1 / C2 / C3 coupling, learning-signal rule, 56-cell descriptors | `fingerprint.py` | `test_collision.py::test_coupling_and_learning_signal`, `test_search_accounting.py::test_56_cells` |
| Canonicalization, structural hashing | `canon.py` | 30 known-equivalent pairs, idempotence, online semantics preserved |
| v2 behavioural-probe verifier (blob `d5a8e0d1…`), duplicate detection | `probes.py` | corpus exists / blob / structure; tampered copy rejected; regeneration aid; rescaled / commuted variants collide |
| 26-feature fingerprint + AR-141 minimum schema | `fingerprint.py` | expected features for 19 references; schema fields |
| Known-family rejection hooks (library, disguises, matcher, K(P)) | `families.py` | 100% recall on 31 references × 5 variants; no residual in references; residual found for a novel term |
| MAP-Elites archive, generator, AE.3.5 mutation / crossover, budgets, promotion | `search.py`, `generate.py` | stub-evaluator archive test; generation cap |
| Tasks B, C\*, D, E, F, reserved A, sanity T0 | `tasks.py`, `runners.py` | exact v2 schedules and constructions; determinism |
| Metrics | `metrics.py` | retention/forgetting, half-life, return rule, SGG, AULC, S_τ, BWT, etc. |
| Parameter / state / FLOP accounting; CPU ledger and 30 CPU-h cap | `substrate.py`, `interp.py`, `accounting.py` | counters on fixtures; cap raises |
| Timeout and numerical safety | `substrate.py` | 10 crafted overflow programs; divergence guard; timeout |
| Reproducible seeds; immutable run config; manifest | `substrate.py`, `manifest.py` | bit-identical reruns; config tamper refused; seed sets disjoint (no confirmation leakage) |
| Interpreter reproduces hand-written NumPy SGD, fast weights, DFA | `substrate.py` | max abs difference < 1e-5 |

The suite has **114 tests, all passing**. Raw output: `runs/stage0/pytest.txt`.

Implementation decisions were committed and pushed **before** the gate was computed: `IMPLEMENTATION_DECISIONS.md`, commit `ee08823`.

## 2. Stage-0 checks

| Check | Result |
|---|---|
| Probe corpus exists and matches blob `d5a8e0d1d91d1d1caf5ff3cbb84f9a4c76e730c1`; 16 probes, I = 8, O = 6, 4 register slots | **PASS** |
| Regeneration aid (xorshift32, seed 20260928) | all vector/matrix fields reproduce exactly; the file does not document the scalar-field mapping (`L, dL, Lbar, tep`), so those rely on the blob hash |
| Immutable run configuration | written; sha256 in `config/run_config.json` |
| Test suite | **PASS** (114/114) |
| Detector recall on references and disguises | **PASS** (0 misses / 155 variants) |
| **Task-B gradient-conflict gate** (mean cosine of 64 paired first-layer weight gradients ≤ −0.50, every seed) | **FAIL** — 3 of 8 seeds |
| C\*, D, E, F schedules match v2 exactly | PASS (tests) |
| Profiling | ≈ 7.2 CPU-s per Tier-1 candidate, ≈ 2.4 CPU-h for 1,200 (AE exit criterion ≤ 20 s: met) |

### 2.1 Task-B gate results (`runs/stage0/taskB_gate.json`)

Rule, fixed before computation (D-TASK-B-GATE):
- model initialization of each seed (Glorot normal, D-SUB-1);
- batch-mean ½‖e‖² loss;
- gradient with respect to the first-layer weight matrix;
- 64 pairs of Task-1/Task-2 mini-batches (batch 32) sharing the same `c` draws.

| Seed | Mean cos | Min | Max | ≤ −0.50 |
|---|---|---|---|---|
| 100 | −0.5009 | −0.673 | −0.323 | yes |
| 101 | −0.4770 | −0.726 | −0.318 | no |
| 102 | −0.4639 | −0.658 | −0.321 | no |
| 103 | −0.4320 | −0.572 | −0.258 | no |
| 104 | −0.5106 | −0.642 | −0.412 | yes |
| 1000 | −0.5094 | −0.658 | −0.390 | yes |
| 1001 | −0.4255 | −0.552 | −0.274 | no |
| 1002 | −0.3511 | −0.572 | −0.135 | no |

Pooled mean over the 8 seeds: **−0.459**. Any aggregation (every seed, pooled, calibration seeds only: −0.477) fails the −0.50 threshold.

**Interpretation (not a verdict):**
- The overlapping shared/private construction does create substantial, consistent conflict. Every one of the 512 pairs has a negative cosine.
- The shared block has only 8 of 20 active input dimensions. The private blocks are orthogonal between tasks, and they contribute to the gradient norms but never to the inner product.
- The network's own random output at initialization also dilutes the target-driven anti-alignment.
- Together, these put the typical cosine near −0.46 rather than below −0.50.

### 2.2 Post-hoc sensitivity (DIAGNOSTIC ONLY)

File: `runs/stage0/taskB_gate_sensitivity_DIAGNOSTIC.json`.

This was computed **after** the frozen gate failed. It cannot be used to pass the gate. It is reported so the owner can judge whether the failure is robust to implementation choices that v2 left open.

| Initialization | First-layer W | W + b | All layers |
|---|---|---|---|
| Glorot normal (pre-declared) | 3/8 seeds, pooled −0.459 | 3/8, −0.460 | 0/8, −0.377 |
| LeCun normal (1/fan_in) | 7/8, −0.545 | 7/8, −0.546 | 5/8, −0.495 |
| He normal (2/fan_in) | 0/8, −0.289 | 0/8, −0.288 | 0/8, −0.153 |

- No variant passes on every seed.
- The result depends on the initialization scale: smaller output scale gives stronger anti-alignment.
- v2 says "at the frozen model initialization" but does not fix the initialization. Stage 0 froze Glorot normal (a standard choice for tanh, and the Cursor suite's "He/Xavier normal") before computing anything.

## 3. Other Stage-0 findings the owner should know

These are not stop conditions.

1. **Probe corpus omits `W_ep0`.** D-PROBE-2 derives it deterministically as probe (k+1)'s `W`. A future corpus version could serialize it.
2. **Blind spots of the frozen one-step probe** (documented in `runs/stage0/collision_selfcheck.json`):
   - STRUCT events never fire in one step;
   - `topk(·, 8)` is all-ones at probe dimensions ≤ 8;
   - per-step scalar modulation of the whole update is invisible after unit normalization (by AE design).

   At the family threshold, 7 of 465 reference pairs collide:
   - R1~R19, R1~R24, R19~R24;
   - R4~X5;
   - R9~R10, R9~R22, R10~R22.

   All are explained by these blind spots or by true near-equivalence. Recall is 100% (every reference and disguise is flagged). The effect is conservative: a C3 residual with no register, or a gate with k = 8, would be classified as `REDISCOVERY_inert` rather than evaluated. It can suppress candidates but cannot manufacture a novelty claim.
3. **Two implementation defects were found and fixed by the Stage-0 tests** before the verdict. Neither affects the Task-B gate, which uses only the task generator, the initialization and plain backprop.
   - Commutative register operands made canonical register naming order-dependent. Fixed by name-free register content signatures.
   - K(P) rebuilt kept terms from the cvec-expanded form, which altered register-phase semantics.
4. **Batch semantics.** v2 fixes mini-batches (B, F) while AE's grammar was written for online examples. D-SUB-3 fixes a consistent reading. One AE rewrite (`mix(r,v,0)→v`) moves the batch reduction, so canonical programs define the evaluated semantics (D-CANON-3).

## 4. Compute

| Item | CPU time |
|---|---|
| Ledgered Stage-0 script | 17.6 CPU-s |
| Interactive development and testing in this session | ≤ 0.25 CPU-h (upper-bound estimate, not measured) |
| **Cumulative ledger** | **0.265 CPU-h of the 30 CPU-h cap** (three Stage-0 script runs of ~17–18 CPU-s each, plus the development estimate) |

No GPU was used (`CUDA_VISIBLE_DEVICES=""`).

## 5. Exact stop reason

`PREREGISTRATION VALIDITY FAILURE (v2): Task-B first-layer gradient-conflict gate — mean cosine over 64 paired mini-batches at the frozen initialization is ≤ −0.50 on only 3 of 8 pre-declared seeds (pooled −0.459).`

Per v2 §6.1 ("If either condition fails, Task B is invalid and the run stops for owner review") and the owner instruction ("STOP and report a v2 preregistration validity failure. Do not redesign Task B"), the run stops here.

## 6. What an owner decision would need to settle

These are options only. None was chosen or applied.

- (a) Keep Task B unchanged and restate the gate, e.g. pooled mean over seeds, or ≤ −0.40.
- (b) Fix the initialization at the protocol level (e.g. LeCun normal) and state the aggregation rule. Under LeCun the diagnostic gives 7/8 seeds, pooled −0.545.
- (c) Change the construction so the shared block dominates the gradient, e.g. a larger shared block or smaller private dimensions.
- (d) Drop B from the primary triad and search on C\* and F only.

Any of these is a material protocol change and needs a recorded v3 amendment before Stage 1. The Stage-0 package is ready to rerun unchanged apart from the amended item.
