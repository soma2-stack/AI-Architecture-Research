# AMS v7 — detector-aligned anchored constructor: static validation, official Stage 2, Stage 3

Protocol: prereg **v7** (sole active protocol). The v3 Stage-0 PASS and the v5 Stage-1 PASS carry forward; neither was rerun. The v5 Stage-2 results (`runs/stage2/`, `runs/stage2_repair1/`) and the v6 static-validation failure (`runs/v6_static_validation/`, `STAGE2_V6_REPORT.md`) are preserved as historical evidence. No v6 search ran.

## 1. Implementation (commit `27f2e81`, pushed before validation and search)

- **`ams/v7gen.py` defines `DetectorAlignedGen`.** It subclasses the v6 constructor and overrides only C2. C1 and C3 are the v6 code; a test checks they are identical from the same RNG state.
  - **C2 construction.**
    - Selector: an O-typed PARAM-phase grammar draw at depth 0–1 that reads z, h or dphi.
    - Route: `topk(selector, k)` with k ∈ {1, 4, 8}, or `where(selector, 1, 0)`, chosen uniformly.
    - Updates: `dW = (add dW_base (mul (rowscale dW_base route) 0.1))` and `db = (add db_base (mul (mul db_base route) 0.1))`.
  - **Zero branch of the `where` route (D-V7-2).** The frozen constant set does not contain 0.0, and a literal 0.0 fails the typecheck (`bad_const`). The branch is therefore spelled `(sub 1.0 1.0)`. The unchanged canonicalizer folds it to 0, so the canonical program that the pipeline hashes, fingerprints and evaluates is exactly `where(selector, 1, 0)`; a test checks struct-hash identity.
  - **Accounting (D-V7-4).**
    - Activity redraws are conditional sampling and are not counted.
    - An instantiated program that fails validation counts as generated.
    - A request gets at most 10 attempts, with its class fixed.
- **Unchanged.** The fingerprint, collision library, canonicalizer, probes, grammar and v5 generator have no diff against `956efdf`. The 155-entry golden collision snapshot is unchanged. The suite passes (180 tests at the v7 commit, 194 with the Stage-3 runner).

## 2. Static validation — PASS (`runs/v7_static_validation/`, seed 70707, clean commit `27f2e81`)

| Requirement | Result |
|---|---|
| 1,000/1,000 emitted proposals are type-valid and within node/depth/register limits | PASS; 1,000 requests, 1,000 attempts, 0 invalid, 0 skipped |
| Learning signal; exact SGD backbone; exact templates; residual scale exactly 0.1 | PASS; 0 failures on every invariant |
| C1 recognized as C1, C2 as C2, C3 as C3 by the unchanged fingerprint | PASS; raw: C1 320/320, C2 350/350, C3 330/330 |
| Canonical form | 1 C1 coupling lost, vacuous: the update simplifies to no data leaf. Every other class is detected. |
| Uniform class sampling | PASS; 320 / 350 / 330, χ² p = 0.50. Route, k and selector-depth p-values are 0.52–0.75. |
| Invalid attempts recorded separately; redraws recorded, not counted | PASS; 0 invalid; 1,821 conditional redraws |
| No evaluation module imported during construction | PASS |

Nothing was trained, and no T0, probe, B, C\* or F run was made. The script was dry-run once, with the non-official seed 71717 and scratch output only.

## 3. Official Stage 2 (`runs/stage2_v7/`)

- **Run:** `python3 scripts/stage2.py stage2_v7`, seed **2026092806**, from clean commit `1334cca` (`git_at_start.dirty_excluding_runs = false`).
- **Unchanged:** budgets, T0, Tier-1, q, the 2σ rule, descriptors, the archive, mutation and crossover, and promotion.
- **Provenance note:** the manifest's end-of-run `git_commit` (`94e23bb`) is the Stage-3 runner commit, which was pushed during the run. It adds new files only and changes no code the running search used.
- **Tier-1 baselines** (seeds 1000–1002) are identical to the v5 runs. SGD is the best generic on every task: B forgetting 100; C\* censored half-life 12.0; F OOD error 0.82.

**Stop reason: `G_MAX`.** All 20 generations completed, and they exactly exhausted the Tier-1 budget (1,200/1,200).

| Label | Count |
|---|---|
| generated | **5,544** (of 6,000) |
| invalid | 175 |
| duplicate, syntactic | 1,621 |
| duplicate, behavioural | 1,317 |
| probe non-finite | 0 |
| pure rule (no coupling) | 66 |
| no learning signal | 124 |
| REDISCOVERY | 0 |
| REDISCOVERY_inert | 11 |
| T0 sanity evaluated | **2,230** (of 3,000) |
| T0 fail | 1,030 |
| **Tier-1 evaluated** | **1,200** (of 1,200) |
| defects | **3** (threshold > 5; the run continues) |

- Archive: **35/56 cells**.
- Tier-1 records with q ≥ 0.15: 41.
- Rediscovery rate over screened programs: 3.2%.
- **Promoted: 8**, all on C\* (the per-task cap is 8): P02743, P04957, P05100, P05115, P04064, P03951, P03376, P01024.
- CPU: 7,679 CPU-s (parent self plus workers); wall 74 min.

### Defects (recorded, not repaired)

P04273, P04973 and P05189 are mutation or crossover offspring. Each raised an interpreter broadcasting `ValueError` during Tier-1 evaluation on Task F. They are recorded as `defect` and were never scored. That is below the frozen threshold (more than 5 stops the search), so the run continued and no repair was made.

### The promoted candidates (Tier-1, 3 seeds; C\* censored median half-life, SGD 12)

| Candidate | q | Couplings | Nearest family (sim) | Half-life per seed | Notable structure |
|---|---|---|---|---|---|
| P02743 | 0.496 | C1 | R21 continual backprop (0.950) | 4 / 8 / 6 | gain `1 + tanh(r1)`, where r1 = EMA₀.₅ of `exp_c(ξ_O) − r1` (noise-driven gain) |
| P04957 | 0.487 | C2, C3 | R1 SGD (0.886) | 4 / 6 / 6 | `W_eff = W + W_ep0 + …`; topk-4 row gate on dphi; reinit on normalized dphi |
| P05100 | 0.486 | C1 | R21 (0.886) | 4 / 8 / 6 | noise-driven gain (as in P02743) plus a topk-4 gate on `min(d_fa, r1)` |
| P05115 | 0.486 | C3 | R1 (0.712) | 4 / 6 / 6 | `W_eff = W + W_ep0 + amax(ξ_I)`; topk-4 on `d_bp`; reinit |
| P04064 | 0.486 | C2, C3 | R1 (0.741) | 4 / 6 / 6 | as P05115, with a `where`-based gate |
| P03951 | 0.431 | C1, C2 | R21 (0.899) | 4 / 10 / 6 | noise-driven gain plus a topk gate |
| P03376 | 0.338 | C1, C2 | R21 (0.856) | 8 / 8 / 6 | noise-driven gain plus two topk gates |
| P01024 | 0.209 | C3 | R1 (0.658) | 4 / 16 / 6 | `W_eff = W + W_ep0 + tep`; topk on e; reinit on normalized dphi |

Interpretation (not a verdict):
- The promoted set is dominated by two motifs:
  - **injected noise or reset** (a noise-driven forward gain, or unit reinitialization, close to continual backprop);
  - **effective-weight doubling** (`W + W_ep0`).
- These are 3-seed Tier-1 estimates. Stage 3 decides on 10 fresh seeds.

### Where the promotions came from (`runs/stage2_v7/summary_by_class.json`)

| Source | Proposals | Reached Tier 1 | Tier-1 q ≥ 0.15 |
|---|---|---|---|
| constructor C1 | 169 | 113 | 0 (max q −0.002) |
| constructor C2 | 155 | **0**: 79 behavioural duplicates, 67 syntactic duplicates, 9 REDISCOVERY_inert | 0 |
| constructor C3 | 157 | 87 | 1 (P00065, q 0.33; later displaced from its cell) |
| mutation / crossover offspring | 5,063 | 997 | 40 |

All 8 promotions are offspring. None of the 155 v7 C2 proposals was distinct enough to reach T0: the 10% routed residual is behaviourally too close to SGD, or to earlier proposals, on the probes.

## 4. Stage 3 (`runs/stage3_v7/`)

- **Run:** `python3 scripts/stage3.py stage2_v7 stage3_v7`, from clean commit `365b264`.
- **Runner:** frozen D-S3 / D-S3-v4 rules; the runner was committed as `94e23bb` before the promotion list was final.
- **Seeds:** fresh seeds 10000–10009, used for the first time. Every condition selects its own learning rate.
- **Jobs:** 139 (123 in phase 1, 16 resource-matched in phase 2), 0 errors. Each job ran 30 runs (10 seeds × 3 learning rates) of 448 updates.
- **Compute:** 167.6 CPU-s.

**Fresh-seed generics on C\*** (censored median half-life): SGD **21.8** (the best generic, G); AdamW 22.6; SGDM 29.2. On the Tier-1 seeds SGD scored 12.0, so the fresh-seed variance is large.

**Known controls:** R12 and R13 are unstable on these seeds, so R15 (128) is the strongest stable control.

| Candidate | m_P | Return OK | Threshold (≤ 10.9 and ≥ 8/10) | Wilcoxon p | Holm (8 pairs) | Bootstrap 95% CI of G − P | **Label** |
|---|---|---|---|---|---|---|---|
| P02743 | 18.0 | 5/10 | fail | 0.406 | no | [−4.0, 14.6] | **NEGATIVE** |
| P04957 | 12.4 | 5/10 | fail | 0.070 | no | [1.6, 17.8] | **NEGATIVE** |
| P05100 | 23.0 | 8/10 | fail | 0.766 | no | [−6.2, 3.6] | **NEGATIVE** |
| P05115 | 17.0 | 3/10 | fail | 0.008 | no (0.008 > 0.05/8) | [2.0, 8.0] | **NEGATIVE** |
| P04064 | 17.0 | 3/10 | fail | 0.008 | no | [2.0, 8.0] | **NEGATIVE** |
| P03951 | 23.8 | 7/10 | fail | 0.812 | no | [−6.6, 2.6] | **NEGATIVE** |
| P03376 | 26.4 | 3/10 | fail | 0.921 | no | [−13.6, 7.4] | **NEGATIVE** |
| P01024 | 22.6 | 6/10 | fail | 0.125 | no | [−13.0, 7.0] | **NEGATIVE** |

All eight pass gate 1 (stable) and gate 2 (R0 MSE at step 256 ≤ 0.25). **All eight fail gate 3** — the preregistered threshold, Holm-corrected Wilcoxon and bootstrap requirement — and so are labelled **NEGATIVE: no preregistered matched advantage on fresh data.**
- P05115 and P04064 behave identically on C\*. Their gates differ only through the error leaf `e`, which is zero in hidden layers.
- The closest candidate, P04957, has seed-mean half-life 12.4 against the required ≤ 10.9, and only 5/10 seeds pass the return check against the required 8.

**Diagnostic conditions** (recorded in `results.json`; they do not affect the labels, which gate 3 already decides):
- **Resource-matched G is much worse than SGD.** A6 (compute-matched SGD, k = 2 or 3 updates per batch) has half-life 61.6 or censored; A7 (capacity-matched SGD, hidden 33–47) is 24.0–27.2.
- **A4** (`update_every` flipped to 8) is unstable for 7 of 8 candidates and censored (128) for P03376.
- **A5a / A5b** (P through SGDM / AdamW) are mostly worse than P.
- **K(P) limitation (frozen decomposition, observation only).** For every candidate whose dW term is gated, the frozen K(P) drops the whole gated term instead of stripping the gate, because the stripped form does not match a family template. K(P) then has `dW = 0`, cannot learn (half-life 128), and makes gates 4a/4b pass trivially. Only P02743, whose dW is plain SGD, has a meaningful K(P); it equals SGD (21.8).
- Tier 3 is not required: no candidate carries the maximum label.

## 5. Outcome

- **v7 is the first AMS design to seed the archive.** It filled 35/56 cells with 1,200 Tier-1 evaluations and 8 promotions.
- **No promoted candidate survived Stage 3. Final labels: 8 × NEGATIVE.** 0 INTERESTING, 0 REDISCOVERY, 0 POSSIBLE ARCHITECTURE CANDIDATE.
- By the owner's classification, this is a **negative result for the v7 detector-aligned SGD-anchored search design** at the matched-validation stage. The C\* half-life gains selected on 3 Tier-1 seeds did not replicate on 10 fresh seeds.
- It is not evidence that no novel mechanism exists in the grammar.

Interpretation (not a verdict):
- **Selection on noise.** Tier-1 C\* scores rest on 3 seeds, and the censored half-life is a coarse, high-variance metric (per-seed values of 4–128). MAP-Elites selected on that noise: 40 of the 41 q ≥ 0.15 records are offspring that mainly add noise injection, reinitialization or `W + W_ep0` weight doubling.
- **Constructor proposals.** The v7 C2 proposals never became distinct candidates, and C1 never reached q > 0. The constructor mainly served to seed the archive; mutation produced everything that was promoted.

## 6. Compute

| Item | CPU |
|---|---|
| v7 static validation (plus one scratch dry run) | 6.5 CPU-s |
| Official Stage 2 | 7,678.6 CPU-s |
| Official Stage 3 | 167.6 CPU-s |
| **Shared ledger total** | **2.838 CPU-h of 30** |

No GPU. No Stage 4.
