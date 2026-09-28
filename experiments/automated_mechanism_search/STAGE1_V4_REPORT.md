# AMS v4 — Official Stage-1 report and stop notice

**Verdict: STAGE 1 (v4) FAILED — mandatory gate `V1_B_REP` (joint-training representability oracle).**

**Stage 2 was not legally allowed and was not started.** No candidate was generated and Stage 3 did not run. Nothing in the protocol was amended.

- Protocol: `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v4**. The v3 Stage-0 PASS carries forward.
- Operational decisions D-V4, D-S2-v4 and D-S3-v4 were committed and pushed in `0fb4be1`, **before** this run and before any candidate existed.
- Results:
  - `runs/stage1_v4/stage1_result.json` (all gates, summaries, learning-rate tables);
  - `runs/stage1_v4/raw_runs.json`;
  - `runs/stage1_v4/manifest.json` (git at start `0fb4be1`, clean).
- The v3 evidence in `runs/stage1/` is untouched.

## Gate results

All values are 5-seed means (seeds 100–104) at each method's selected learning rate.

| Gate (v4 mandatory) | Result | Values |
|---|---|---|
| M6 generic-control stability | PASS | every generic method stable on B, C\* and F |
| M2-v4 B fit (`FitReduction_B ≥ 0.95`) | PASS | SGD 0.988; SGDM 0.989; AdamW 0.989 |
| M3 B interference | PASS | Forgetting 100 / 100 / 100 pp; `L1_post > L1_pre` on every seed |
| **V1-B-REP joint oracle** (some optimizer: `RelRed_T1` and `RelRed_T2 ≥ 0.95`) | **FAIL** | see below |
| M4 F generic failure | PASS | train 1.00; OOD 0.162–0.168; SGG ≈ 83 pp |
| M5 detector | PASS | carried from the v3 Stage-0 PASS |
| M7-v4 C\* sanity | PASS | R0 MSE 0.031; R1 entry MSE 1.00 / 0.90; generic censored half-life SGD 14.0, SGDM 18.8, AdamW 17.6 (all < 64) |
| V3-F discrete synthesis | PASS | OOD 1.00 |
| V-D conditioning | PASS | natgrad `S_τ` 90 / 109 steps at κ = 1e4 / 1e6; SGD and SGDM diverge (∞) |

Recorded diagnostics (not gates under v4) repeat the v3 values:
- V1-B: GPM 93.8% forgetting; R17 and R18 100%; R13 unstable.
- V2-C\*: R12 and R13 unstable; R15 half-life 110.

### V1-B-REP detail

Setup: 1,000 updates, each with 16 + 16 fresh examples; the official clipped pipeline; learning rate selected by final-50-update training MSE.

| Optimizer | Selected learning rate | `RelRed_T1` | `RelRed_T2` | Per-seed range (T1 / T2) |
|---|---|---|---|---|
| SGD | 0.1 | **0.914** | **0.904** | 0.891–0.922 / 0.885–0.912 |
| SGDM | 0.1 | 0.883 | 0.867 | |
| AdamW | 0.1 | 0.884 | 0.859 | |

No optimizer reaches 0.95 on either task; every seed of every optimizer is below 0.95.

## Post-hoc diagnostic (not gating)

File: `runs/stage1_v4/V1_B_REP_oracle_DIAGNOSTIC.json`. This was computed after the failure and cannot pass the gate.

| Variant | `RelRed_T1` | `RelRed_T2` |
|---|---|---|
| unclipped SGD, 1,000 updates | 0.922 | 0.914 |
| unclipped SGDM, 1,000 updates (lr 0.01) | 0.920 | 0.908 |
| unclipped AdamW, 1,000 updates (lr 0.01) | 0.949 | 0.945 |
| clipped SGD lr 0.1, **2,000** updates | 0.950 | 0.945 |
| clipped SGD lr 0.1, **4,000** updates | 0.967 | 0.960 |

**Interpretation (not a verdict):**
- The fixed MLP can represent both Task-B mappings jointly, since 4,000 joint updates exceed 0.95 on both tasks.
- The frozen 1,000-update oracle budget is too short. The joint function is harder: the sign of the shared-block mapping must depend on which private block is active.
- Update clipping costs about 1–3 pp at 1,000 updates.
- The gate as frozen still fails.

## Exact stop reason

`STAGE-1 MANDATORY GATE FAILURE: V1_B_REP` (`runs/stage1_v4/stage1_result.json`).

Under v4 ("If … V1-B-REP fails, Task B is invalid and the run stops for owner review"; "Abort if any mandatory v4 control fails") and the owner instruction ("If any mandatory v4 gate fails: STOP and report it. Do not amend anything yourself."), the run stops here.

## What an owner decision would need to address

Options only; none was applied.
- Restate the oracle budget; the diagnostic suggests ≥ 2,000–4,000 updates.
- Restate the oracle threshold, e.g. ≥ 0.90.
- Or allow the oracle without clipping.

Any of these is a material change requiring a v5 amendment. Stage 1 would then rerun with `scripts/stage1_v4.py` changed only in the amended items. All other v4 gates already pass.

## Compute

- v4 Stage 1: 72.8 CPU-s.
- Diagnostic: 5.9 CPU-s.
- Cumulative ledger: **0.310 CPU-h of 30**.
- No GPU.
