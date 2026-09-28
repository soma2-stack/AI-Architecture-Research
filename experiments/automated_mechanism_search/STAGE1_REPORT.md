# AMS v3 — Official Stage-1 report and stop notice

**Verdict: STAGE 1 FAILED — mandatory gates `M2_B_fit`, `V1_B` and `V2_Cstar` failed.**

**Stage 2 was not legally allowed and was not started.** No candidate program was generated or evaluated, and Stage 3 did not run. No protocol element was changed, and no control was retuned.

- Protocol: `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v3**.
- Official Stage 0 (v3) **passed** first (`runs/stage0_v3/`):
  - directional Task-B gate: 512/512 paired cosines negative;
  - 118/118 tests.
- Gates and operational rules are `IMPLEMENTATION_DECISIONS.md` D-CAL and D-S1, committed in `fa5fc00` **before** Stage 1 ran.
- Results: `runs/stage1/stage1_result.json` (gates, summaries, learning-rate selection tables), `runs/stage1/raw_runs.json` (all curves) and `runs/stage1/manifest.json`. The manifest's git at start is `75e9ed1` (clean).

## Setup

- Calibration seeds 100–104.
- Learning-rate grid {1e-3, 1e-2, 1e-1}, selected per (method, task) on training-side metrics only (D-LR-1).
- No early stopping on B, C\* or F.
- Official generic controls are SGD, SGDM and AdamW with the same update clipping as candidates. Unclipped versions ran as recorded diagnostics only.

## Gate results

| Gate | Result | Values (seed means at the selected learning rate) |
|---|---|---|
| M6 controls run | PASS | every generic method stable on B, C\* and F |
| **M2 B fit** (`L1_pre < 1e-3`) | **FAIL** | SGD 0.0172; SGDM 0.0163; AdamW 0.0158 |
| M3 B interference (Forgetting ≥ 10 pp; `L1_post > L1_pre` every seed) | PASS | Forgetting 100 / 100 / 100; `L1_post` ≈ 4.0–4.1 vs `L1_init` 1.42 |
| M4 F failure (train ≥ 98%, OOD ≤ 25%, SGG ≥ 75) | PASS | train 1.00 / 1.00 / 1.00; OOD 0.162 / 0.165 / 0.168; SGG 83.8 / 83.5 / 83.2 |
| M5 detector | PASS | from v3 Stage 0 |
| M7 C\* sanity (best generic = SGD) | PASS | `MSE_R0(256)` 0.031; R1 entry MSE 1.00 and 0.90 |
| **V1-B** (some retention control: Forgetting ≤ 0.85 × SGD **and** T2 MSE ≤ 1.1 × SGD) | **FAIL** | see below |
| **V2-C\*** (some fast/slow control: half-life ≤ 0.9 × SGD) | **FAIL** | see below |
| V3-F discrete synthesis OOD ≥ 95% | PASS | 1.00 on all 5 seeds (finds x0⊕x1⊕x2) |
| V-D natural-gradient `S_τ ≤ min(SGD, SGDM)/3` at κ ∈ {1e4, 1e6} | PASS | natgrad 89.8 / 108.6 steps; SGD and SGDM diverge at every learning rate (∞) |

V1-B detail. SGD's reference is Forgetting 100.0, T2 MSE 0.0130.

| Control | Forgetting | T2 MSE | Outcome |
|---|---|---|---|
| GPM (θ = 0.97, SGD base) | 93.8 | 0.615 | fails both conditions |
| R17 EWC/SI | 100.0 | 0.0137 | fails forgetting |
| R18 k-WTA | 100.0 | 0.051 | fails both |
| R13 fast/slow | — | — | unstable at every learning rate |

V2-C\* detail. SGD's censored half-life is 14.0 updates.

| Control | Result |
|---|---|
| R12 fast weights | unstable at every learning rate (diverges at step 11) |
| R13 fast/slow | unstable at every learning rate |
| R15 three-factor | half-life 110.4 (∞ on 4/5 seeds) |

## Interpretation (not a verdict)

1. **M2.** In 500 batch-32 updates the generic MLP fits Task 1 to held-out MSE ≈ 0.016, which is R² ≈ 0.984. It does not reach the preregistered 1e-3. This holds with or without clipping, since unclipped SGD gives 0.0172.
2. **V1-B.** Task B's shared-block conflict is severe: Task 2 drives Task-1 MSE to about 3× its initial value. GPM at its pre-declared energy threshold 0.97 still leaks enough to forget 94%, and it learns Task 2 poorly (MSE 0.61). The EWC-type (R17) and k-WTA (R18) templates give no protection.
3. **V2-C\*.** The fast-weight control failures come from the frozen design, not from a code defect (`runs/stage1/fast_weight_instability_DIAGNOSTIC.json`, post-hoc).
   - The single program is applied to all three layers.
   - At the identity output layer, the Hebbian register `r ← mix(r, outer(h = z, a), 0.9)` feeds back without bound: |r| goes from 0.006 to about 600 in 10 steps, and the loss reaches ≈ 1e7.
   - Register dynamics do not involve η, so every learning rate diverges.
   - The benchmark therefore has no working fast-weight positive control on this substrate.
4. **The passing parts show the pipeline itself behaves as intended:**
   - F's spurious-shortcut failure is strong (OOD ≈ 16%, SGG ≈ 83 pp), and discrete synthesis solves F perfectly;
   - the D conditioning diagnostic separates curvature control from first-order methods;
   - C\* has a real re-adaptation problem (entry MSE ≈ 1).

## Exact stop reason

`STAGE-1 MANDATORY GATE FAILURE: M2_B_fit, V1_B, V2_Cstar` (`runs/stage1/stage1_result.json`).

Under v3 (§6.1: "If … any Stage-1 Task-B gate fails, Task B is invalid and the run stops for owner review"), v3 §15 and the owner instruction, the run stops here.

## What an owner amendment would need to address

These are options only. None was applied.

- **M2.** Restate the Task-1 fit threshold (e.g. relative to `L1_init`, or R² ≥ 0.95), or change the budget.
- **V1-B.**
  - Accept that no available retention control shows its signature on this construction.
  - Or name a different positive control or threshold (for example, a GPM energy threshold as a preregistered constant).
  - Or reduce the conflict strength.
- **V2-C\*.**
  - Specify how fast-weight controls apply on the linear output layer (e.g. hidden layers only, or bounded output activity).
  - Or drop the positive-control requirement for C\*.

Any of these is a material change, which requires a v4 amendment before Stage 1 is rerun. The Stage-0 and Stage-1 code would rerun unchanged apart from the amended items.

## Compute

- Stage 1: 66.5 CPU-s (parent plus 3 workers).
- Cumulative ledger: **0.288 CPU-h of 30**.
- No GPU.
