# AMS v5 — Official Stage-1 PASS, Stage-2 search, and stop notice

## 1. Stage 1 (v5): PASS

Source: `runs/stage1_v5/`, run from commit `bd50231`. The code was committed; the manifest's dirty flag comes only from the script-written `config/run_config_v5.json`.

All mandatory v5 gates pass. Values are 5-seed means (seeds 100–104):

| Gate | Result |
|---|---|
| M2-v4 | FitReduction 0.988 / 0.989 / 0.989 |
| M3 | Forgetting 100 / 100 / 100 pp; `L1_post > L1_pre` on every seed |
| **V1-B-REP (exactly 4,000 updates)** | SGD (lr 0.1): 0.967 / 0.960; SGDM (lr 0.01): 0.958 / 0.952; AdamW (lr 0.01): 0.970 / 0.964. All three ≥ 0.95 on both tasks. |
| M4 | train 1.00; OOD 0.162–0.168; SGG ≈ 83 |
| M5 | carried from the v3 Stage 0 |
| M6 | PASS |
| M7-v4 | half-life 14.0 / 18.8 / 17.6 < 64; R0 MSE 0.031; entry MSE 1.00 / 0.90 |
| V3-F | 1.00 |
| V-D | natgrad 90 / 109 steps; SGD / SGDM ∞ |

Diagnostics only: V1-B and V2-C\* are as in v3/v4.

## 2. Stage 2: search began and was stopped by a frozen stop condition

Source: `runs/stage2/`, run from commit `be4b73f` (clean). The files are:
- `records.jsonl.gz`: all 5,782 programs, each with raw form, canonical form, label, fingerprint, descriptor, β hash, nearest family and details;
- `counts.json`;
- `archive.json`;
- `promotions.json`;
- `baselines_tier1.json`;
- `progress.log`;
- `manifest.json`.

Tier-1 generic baselines (seeds 1000–1002): the best generic is SGD on every task.

| Task | SGD metric | AdamW mean ± sd |
|---|---|---|
| B | Forgetting 100 | 100 ± 0 |
| C\* | censored half-life 12.0 | 21.3 ± 6.1 |
| F | OOD error 0.82 | 0.829 ± 0.009 |

**Stop reason:** `implementation defects > 5` (D-S2v4-2, committed in `0fb4be1` before the search; it operationalizes prereg §15, "implementation/canonicalization tests are unreliable"). The search stopped at 5,782 generated programs, still in the random-initialization phase.

### Counts (all generated programs)

| Label | Count | Share of generated |
|---|---|---|
| invalid (typing / size) | 1,966 | 34.0% |
| duplicate, behavioural | 46 | 0.8% |
| duplicate, syntactic | 0 | 0 |
| probe non-finite | 0 | 0 |
| **pure update rule** (no C1/C2/C3; logged as optimizer/local-rule rediscovery) | **2,884** | 49.9% |
| no learning signal | 516 | 8.9% |
| REDISCOVERY (family match without residual) | 0 | 0 |
| REDISCOVERY_inert (residual behaviourally inert) | 0 | 0 |
| sanity evaluated (T0) | 364 | 6.3% |
| **sanity fail** (NEGATIVE: does not learn T0 to ≤ 0.5 × trivial) | **364** | 6.3% |
| Tier-1 evaluated | **0** | 0 |
| defect (implementation exception) | **6** | 0.1% |

Derived figures:
- Rediscovery rate over screened programs: 2,884 / 3,764 = **76.6%**. All are pure-rule logs; there were no family matches with coupling.
- NEGATIVE (sanity) count: 364.
- Archive occupancy: **0/56**.
- Promoted: **none**.
- Stage 3: **not reached**.

### Root cause of the six defects

The same bug caused all six (P01515, P01523, P02385, P04354, P05662, P05782). In the K(P) non-family-residual decomposition (`families.strip_gates`), a `where(x, y, w)` gate is neutralized by replacing it with its positive branch `y`. When `y` is a legal scalar (S) broadcast branch, this changes the subtree's type, and re-simplification raises a typing error.

The failure is a crash, not a silent mislabel. The six programs are recorded as `defect` and were never evaluated. The Stage-0 tests did not cover `where` gates with scalar branches inside decomposed terms.

The likely fix (not applied; it would need an owner decision to rerun Stage 2) is to replace such a gate with a type-preserving broadcast of the branch, e.g. `add(0@T, y)`, instead of `y`.

## 3. Interpretation (not a verdict)

- **The search never left initialization.** No random program passed the frozen AE sanity filter (T0: final-50-step online MSE ≤ 0.5 × the running-mean predictor), so the Tier-1 queue stayed empty.
  - Among the 364 sanity failures, the best reached 0.60 × trivial; the median was 0.76 ×.
  - 141 of them diverged or failed to learn at every learning rate, which triggered the AE.3.6 early stop.
  - The filter itself is sound: SGD, k-WTA, continual-backprop and DFA references pass it. Fast-weight-type couplings fail because of the output-layer Hebbian instability found in Stage 1.
- **Generator yield is very low.** Even without the defect stop, only 218 generations remained in the 6,000 budget. At the observed sanity pass rate of 0/364, it is very unlikely that the search would have reached Tier-1. The committed typed grow generator mostly produces:
  - invalid programs (34%);
  - pure rules with no architecture coupling (50%);
  - programs whose random update expressions do not descend the loss.
- **No mechanism was evaluated on the target tasks.** This run gives **no evidence for or against** a new learning-dynamics mechanism. It shows that the frozen generator / filter / substrate combination cannot seed MAP-Elites within the budget. It must not be read as the stronger negative result "no non-family mechanism exists in grammar G".

## 4. Compute

| Item | CPU |
|---|---|
| Stage 1 v5 | 88.1 CPU-s |
| Stage 2 (parent self CPU + workers) | 547 CPU-s |
| **Cumulative ledger** | **0.486 CPU-h of 30** |

- No GPU.
- Stage-1 ledger entries (v3, v4, v5) double-count worker CPU, because the parent figure includes reaped children. This errs conservatively. Stage 2 uses parent-self plus worker CPU.

## 5. What an owner decision would need to address

Options only; none was applied.
- Authorize a Stage-2 rerun with the decomposition fix, restarting the search from the same seed.
- Decide whether the search design must change so the archive can be seeded. Candidate changes:
  - seed the initial population with coupling-bearing mutants of family references rather than pure random programs;
  - relax T0;
  - enlarge the generation budget.

  Any of these is a material protocol change requiring a new amendment.

---

## 6. Implementation repair 1 and the official repaired rerun (owner-authorized; v5 protocol unchanged)

### Repair

- In `families.strip_gates`, `where(x, y, w)` now returns `y` only when `y` already has the `where` expression's type. Otherwise it returns the type-preserving broadcast `add(0@T, y)`.
- Source: owner-account commit `1932379`, adopted unchanged. No other implementation change.

### Regression evidence (`tests/test_repair1.py`; full suite 150/150 passing)

- Each of the six recorded defects (P01515, P01523, P02385, P04354, P05662, P05782) reproduces its recorded typing error under the pre-repair rule. Under the fix it decomposes, and every stripped term keeps its original type.
- Scalar-branch fixtures pass for O and I vectors, including inside `outer`. Same-type branches are unchanged. A matrix-typed `where` is illegal in the frozen grammar, so there is no matrix case.
- Golden snapshot from the **pre-repair** code (`9dd8a5e`), covering all 155 reference and disguise programs: canonical form, struct and abstract hash, fingerprint, β hash, K(P), K(P) info and family match. **All 155 are identical after the repair.**
- The owner's committed test called `serialize()` on an expression node and raised. Only the test was corrected, to use `sexpr()`.

**Frozen before the rerun.** Commit `000f237` was pushed before launch; the run manifest records git at start `000f237`, clean.

### Rerun

`scripts/stage2.py stage2_repair1`, output in `runs/stage2_repair1/`. The first stopped run in `runs/stage2/` is preserved unchanged.

| Setting | Value |
|---|---|
| Search seed | 20260928 |
| Generator, budgets, T0 filter, Tier-1 baselines, effects, q, archive, stop rules | identical to the first run |
| Tier-1 baselines | identical to the first run |

### Trace reproduction (`runs/stage2_repair1/comparison_to_stage2.json`)

- The raw-program sequence is **identical** over all 5,782 programs of the first run; there is no divergence.
- The only label changes are the six former `defect` programs, which now screen normally and are all `sanity_fail`.
- There are 0 canonical-form changes elsewhere.

### Final counts (6,000 generated)

| Label | Count |
|---|---|
| invalid | 2,053 |
| duplicate, behavioural | 50 |
| duplicate, syntactic | 0 |
| probe non-finite | 0 |
| pure rule (no C1/C2/C3; optimizer/local-rule rediscovery log) | 2,981 |
| no learning signal | 534 |
| REDISCOVERY | 0 |
| REDISCOVERY_inert | 0 |
| **reached the sanity filter** | **382** |
| sanity fail (NEGATIVE) | 382 |
| **reached Tier 1** | **0** |
| defects | **0** |

- Rediscovery rate over screened programs: 76.5%.
- Negatives: 382 (100% of sanity-evaluated).
- Best sanity result: 0.596 × trivial loss (the threshold is ≤ 0.5 ×); median 0.762 ×.
- Archive: **0/56**. Promoted: **none**. **Stage 3 was not reached.**

**Exact completion reason:** `N_GEN_MAX` — the frozen 6,000-program generation budget was exhausted during the random-initialization phase, before any program reached Tier 1.

**Conclusion (per the owner instruction; no redesign).** The frozen v5 generator and T0 sanity-filter combination failed to seed MAP-Elites within budget. This is a search-design negative, not evidence about the existence or absence of a new mechanism.

**Compute.** The rerun used 572.6 CPU-s (parent-self plus workers). The shared ledger, including Codex's independent v4 verification, stands at **0.654 CPU-h of 30**. No GPU.
