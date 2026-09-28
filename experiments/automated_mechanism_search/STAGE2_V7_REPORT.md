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

## 4. Stage 3

_Pending — filled in from `runs/stage3_v7/results.json`._
