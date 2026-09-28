# AMS v8 — robust C\* metric and confirmation funnel: implementation, official Stage 2, confirmation

Protocol: prereg **v8** (sole active protocol).
- The v3 Stage-0 PASS and the v5 Stage-1 PASS carry forward; neither was rerun.
- v7 is final historical evidence: 8 promotions, all NEGATIVE in Stage 3 (`STAGE2_V7_REPORT.md`). It was not rerun, and the `stage2_v7` script now refuses to start because v7 is no longer the active protocol.
- No v7 candidate outcome was used to set any v8 value; all v8 thresholds are the frozen prereg values.

**Outcome:**
- The official v8 Stage 2 filled 42/56 cells.
- **0 of 42 archive elites passed the frozen 8-seed confirmation funnel.** No candidate was promoted.
- **Stage 3 did not run**, and the locked seeds 30000–30009 remain untouched.
- By the owner's rule, this is a **negative result for the v8 robust-metric anchored search design**, not evidence that no mechanism exists.

## 1. Implementation (commit `46947c4`; decisions D-V8-1…9)

- **C\* AULC** (`metrics.adaptation_area` / `adaptation_aulc`), exactly as frozen:
  - `A_e = mean_{k=4,8,…,64} max(MSE_R1(e+k) − 0.05, 0) / max(MSE_R1(e) − 0.05, 1e-8)`;
  - `A_C = ½(A_256 + A_384)`.
  - `run_C` records it per run, alongside the unchanged half-life, which is now diagnostic only.
- **Tier-1 on seeds 5000–5002** with the C\* effect `(m_G − m_P) / max(m_G, 1e-8)`. Unchanged: the return constraint (≥ 2/3) and the AdamW 2σ gate, now on AULC. The fast archive is exploration only; no fast promotion file is written.
- **Confirmation funnel** (`ams/confirm.py`, `scripts/stage2_confirm.py`):
  - every occupied cell's elite is evaluated on its frozen fast best task over seeds 6000–6007, against generics recomputed once per task on the same seeds;
  - `q_confirm = e_confirm − the recorded cost penalty`;
  - eligibility needs: stable, task constraint (C\*: return on ≥ 6/8 seeds), q_confirm ≥ 0.15, AdamW 2σ, and ≥ 6/8 paired wins over the best generic;
  - promotion takes eligible elites by descending q_confirm, at most 8 per task and 20 in total.
- **Stage-3 v8 profile** (`stage3.configure("v8")`), implemented and unit-tested but never run: locked seeds 30000–30009; C\* Gate 3 on AULC (m_P ≤ 0.5·m_G, return ≥ 8/10, Holm, bootstrap); **KF(P)**, the exact nearest known-family reference, used for Gates 4a/4b, with the old K(P) recorded as a diagnostic.
- **Seed lock:** `runners._runs` refuses seeds 30000–30009 unless the official Stage 3 unlocks them.
- **Repairs:**
  - The gate mutation's `where` zero is now spelled `(sub 1.0 1.0)` in `V8Gen`, and canonicalizes to `where(sel, 1, 0)`. Historical generators keep the old literal, so their traces replay.
  - N_GEN_MAX is checked before every anchored or offspring candidate is constructed. A regression test shows constructed = counted = the cap; the v7 path built one uncounted candidate.
- **Unchanged:** the grammar, canonicalizer, fingerprint, collision library, probes, T0, B, F, descriptors, mutation and crossover probabilities, LR grid, cost penalty and budgets. The collision-layer files have no diff against `956efdf`.

## 2. Pre-search validation — PASS (`runs/v8_presearch_validation/validation.json`, clean `5606002`)

| Check | Result |
|---|---|
| Full test suite | 213 passed |
| 155-entry collision golden snapshot | unchanged |
| v7 C1/C2/C3 constructor | the v8 generator reproduces all 1,000 stored v7 static-validation proposals exactly; 0 invariant failures; every class recognized |
| Gate-mutation zero and exact-cap regressions | pass |
| AULC hand-constructed tests | pass: no adaptation = 1, linear adaptation = 0.46875, worsening > 1, floors, averaging |
| Offline replay of stored v7 *generic* C\* curves (SGD / SGDM / AdamW; no candidate data) | finite and bit-deterministic: 29, 29 and 27 stable runs; AULC 0.29–1.63 |
| Seed separation; Stage-3 lock | disjoint; 30000–30009 refused by the runner; unused in every recorded manifest |
| Active protocol | v8, seed 2026092808 |

Two earlier validation runs failed only because my own validation script misparsed the pytest summary line; every pytest return code in them was 0. Both are kept: `validation_initial_parser_bug.json` and `validation_rerun_qq_no_summary.json`. The parser was fixed, the fix committed, and the validation rerun from a clean tree.

## 3. Official Stage 2 (`runs/stage2_v8/`)

- **Run:** `python3 scripts/stage2.py stage2_v8`, seed **2026092808**, from clean `297369e`. Constructor v8; C\* metric AULC; fast seeds 5000–5002.
- **Fast baselines** (seeds 5000–5002): SGD is best on every task. B forgetting 100; C\* AULC 0.416 (AdamW 0.416 ± 0.109); F OOD error 0.793.
- **Stop reason: `G_MAX`.** 20 generations, which exactly used the Tier-1 budget (1,200).

| Label | Count |
|---|---|
| generated | 4,413 (of 6,000) |
| invalid | 45 |
| duplicate, syntactic / behavioural | 1,245 / 976 |
| pure rule / no signal | 76 / 101 |
| REDISCOVERY / REDISCOVERY_inert | 0 / 9 |
| T0 evaluated / fail | 1,961 / 761 |
| **fast Tier-1 evaluated** | **1,200** |
| defects | 2 (below the stop threshold) |

- **Archive:** 42/56 cells.
- **Compute:** 7,745 CPU-s.
- **Defects:** P03104 and P04262 are offspring that raised the same interpreter broadcasting `ValueError` on Task F as the 3 v7 defects. They were recorded and not repaired.
- **By source** (`summary_by_class.json`):
  - constructor C1: 172 proposals, 98 reached Tier 1, max fast q 0.028;
  - constructor C2: 188 proposals, 0 reached T0 (all duplicates or inert, as in v7);
  - constructor C3: 179 proposals, 102 reached Tier 1, max fast q 0.071;
  - offspring: 3,874 proposals, 998 reached Tier 1, max fast q 0.342, 7 records with fast q ≥ 0.15.

## 4. Confirmation funnel (`runs/stage2_v8_confirm/`, seeds 6000–6007, clean `8c5af23`)

- **Scale:** 42 candidates (one per occupied cell) plus 9 generic baseline jobs; 51 jobs, 0 errors, 24 runs each; 421 CPU-s.
- **Confirmation generics:**
  - B: SGD 100.
  - C\*: SGD AULC 0.400 (AdamW 0.441 ± 0.072).
  - F: SGDM 0.827 (AdamW 0.828 ± 0.039).
- **Frozen best tasks of the elites:** B 29, F 8, C\* 5. Most B elites have zero effect on every task, so B wins the frozen tie-break by task order.

**Result: 0 / 42 eligible. Promoted: none.** Every elite fails q_confirm ≥ 0.15; the maximum is 0.063. The other failures overlap:

| Failed requirement | Elites |
|---|---|
| task constraint | 34 |
| AdamW 2σ gate | 32 |
| ≥ 6/8 paired wins over G | 29 |

Top fast elites and their confirmation:

| Candidate | Task | q_fast | q_confirm | m_P / m_G (AULC) | Paired wins | Return (need ≥ 6/8) | AdamW 2σ | Fails because |
|---|---|---|---|---|---|---|---|---|
| P03974 | C\* | 0.342 | −0.051 | 0.213 / 0.400 | 8/8 | **5/8** | pass | the return constraint caps the effect at 0 |
| P03912 | C\* | 0.217 | −0.014 | 0.326 / 0.400 | 7/8 | 5/8 | fail | return; AdamW |
| P03911 | C\* | 0.206 | 0.063 | 0.370 / 0.400 | 5/8 | 6/8 | fail | q < 0.15; wins; AdamW |
| P04215 | C\* | 0.198 | −0.010 | 0.327 / 0.400 | 7/8 | 3/8 | fail | return; AdamW |

Interpretation (not a verdict):
- **P03974 has the only large confirmation-seed effect.** Its uncapped AULC effect is 0.467, winning on all 8 seeds. Its mechanism is `W_eff = W + W_ep0`: the forward pass adds the constant initial weights, since C\* has no episode boundaries. Its `freeze` operation never triggers (`tanh(r1) ≤ 0` always).
- It re-adapts faster within R1 but fails the frozen R0 return condition on 3/8 seeds. That is a stability/plasticity trade-off, which the frozen protocol correctly does not count as an effect.
- **The funnel did what v8 designed it to do.** The four C\* elites with fast q ≈ 0.2–0.34 did not survive 8 fresh seeds under the unchanged constraints.

## 5. Stage 3

**Not run: no confirmation-eligible candidate.** Seeds 30000–30009 were never evaluated: no `runs/stage3_v8/` exists, and the runner lock refuses them. The v8 Stage-3 profile, including KF(P), is implemented and unit-tested only.

## 6. Outcome and compute

- Final: **0 promotions; 0 Stage-3 labels; 0 INTERESTING; 0 POSSIBLE ARCHITECTURE CANDIDATE.**
- By the owner's rule, this is a negative result for the **v8 robust-metric anchored search design**.
- CPU: pre-search validation 74 CPU-s; Stage 2 7,745 CPU-s; confirmation 421 CPU-s. **Shared ledger: 5.13 CPU-h of 30.** No GPU. No Stage 4.
