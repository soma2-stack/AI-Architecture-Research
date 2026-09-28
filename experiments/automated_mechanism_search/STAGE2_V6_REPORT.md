# AMS v6 — Stage-2 constructor implementation and static validation: STOP before the official search

**Verdict: the v6 static validation FAILED on coupling presence for class C2. The official v6 Stage-2 search was not started.**

- No v6 proposal was trained, T0-screened, probe-evaluated, or run on B, C\* or F.
- Search seed 2026092806 is unused.
- `scripts/stage2.py stage2_v6` refuses to start (exit 4) while `runs/v6_static_validation/validation.json` has `pass: false`.
- Nothing in v6 or the frozen pipeline was modified.

The cause is a conflict between the v6 C2 constructor and the unchanged collision/descriptor layer. It is not an implementation bug, so it cannot be fixed under the instruction "fix implementation bugs only; do not modify v6".

> **Historical clarification (added in session 19).** The owner accepted this failure as historical evidence and replaced the C2 rule in prereg **v7**: C2 became detector-aligned `topk`/`where` routing with selector depth 0–1, and the accounting rule was stated explicitly. v6 never ran a search; seed 2026092806 was first used by the official v7 Stage 2. The v6 code, configuration record and validation outputs are preserved unchanged. `stage2_v6` now also refuses to start because v6 is no longer the active protocol. See `STAGE2_V7_REPORT.md`.

## 1. What was implemented (commit `956efdf`, pushed before validation)

- **`ams/v6gen.py`, `AnchoredGen`.** A subclass of the v5 `Gen`; mutation and crossover are inherited unchanged.
  - Every proposal uses the exact R1 backbone: `dW_base = (neg (outer d_bp a))`, `db_base = (neg d_bp)`, `update_every = 1`.
  - Exactly one class is drawn uniformly per slot:
    - **C1:** one RUN register, init 0, type O or M, decay from {0.5, 0.9, 0.99}. The update is drawn at depth 1–2 and reads at least one of {a, z, h, dphi}. For M, `w_eff = (mul (tanh r1) 0.1)`; for O, `gain = (add (mul (tanh r1) 0.1) 1.0)`. Parameter updates are the backbone.
    - **C2:** an O selector drawn in the PARAM phase at depth 1–2, reading at least one of {z, h, dphi}. `g = (add (mul (tanh sel) 0.1) 1.0)`, `dW = (rowscale dW_base g)`, `db = (mul db_base g)`.
    - **C3:** one O RUN register, init 0, decay from {0.5, 0.9, 0.99}. The update is drawn at depth 1–2 and reads at least one of {z, h, dphi}. The structural operation is freeze or reinit on mask `(tanh r1)` with θ from {0.0, 0.1, 0.5}. Parameter updates are the backbone.
- **`search.map_elites(init="v6")`.** Initial and empty-archive proposals come from the constructor. After seeding, the v5 mutation and crossover machinery runs unchanged.
- **`scripts/stage2.py stage2_v6`.** Uses seed 2026092806 and is gated on the static validation.
- **`config/run_config_v6.json`.** Equals the v5 configuration plus a `stage2_v6` section (tested).
- **Implementation decisions** D-V6-1…6 (`IMPLEMENTATION_DECISIONS.md`):
  - `add(1.0, X)` is written `(add X 1.0)`, because the grammar admits only (T,T) or (T,S) operands. The function is identical.
  - Depth 1–2 means the grow-method depth argument is drawn from {1, 2}.
  - The activity-leaf requirement is a conditional draw: redraws are logged but not counted.
  - The class is held fixed across at most 10 attempts per slot, and every invalid attempt counts as generated.

## 2. Tests (full suite 167/167 passing)

- **`tests/test_v6_generator.py`** covers:
  - the exact backbone;
  - the class templates;
  - every constructor invariant on 600 proposals;
  - uniform class and sub-choices;
  - retry and budget accounting;
  - map_elites v6 initialization;
  - the constructor importing no evaluation module;
  - the first 300 v5 random programs of `runs/stage2_repair1/`, reproduced unchanged;
  - documentation of the C2 conflict and the C2 depth limit.
- **Golden collision snapshot** (`test_reference_collision_outputs_identical_to_pre_repair`): all 155 reference and disguise entries are unchanged.

## 3. Static validation (`runs/v6_static_validation/`, seed 60606, 1,000 slots, structural only)

The pass criteria were fixed in the script docstring before the first run, which was made from clean commit `956efdf`. The recorded `validation.json` comes from clean commit `6331de4`, which differs only in the scope of check 6.

| Check | Result |
|---|---|
| Constructor invariants on all 1,000 valid proposals: type-valid, node/depth/register limits, `update_every` 1, no cvec, backprop signal in dW, exact SGD backbone, exact class template | **PASS** (0 failures on each) |
| Every slot valid within 10 attempts | **PASS** (1,258 attempts; 258 invalid, all C2 `oversize`) |
| Learning signal, frozen fingerprint, raw and canonical | **PASS** (1,000 / 1,000) |
| **Intended coupling present, frozen fingerprint, raw proposal** | **FAIL**: C1 347/347, **C2 53/338**, C3 315/315 |
| **Canonical coupling loss explained only by canonicalization** | **FAIL**, because of C2. C1 347/347 and C3 313/315 detected; 3 losses are vacuous dependences such as `(sub h h)` that the canonicalizer removes. |
| Uniform class choice | **PASS**: slots C1 347, C2 338, C3 315; χ² p = 0.44 |
| Sub-choices (reported) | C1 type M 188 / O 159 (p = 0.12); C1 decay p = 0.54; C3 decay p = 0.69; kind p = 0.46; θ p = 0.41 |
| No evaluation module imported during construction | **PASS**: none of tasks, runners, tier1, substrate, probes, controls, families, metrics, interp or search |

Check-6 note: the first run measured the whole process instead of the construction phase. It flagged only `ams.interp`, which the unchanged canonicalizer imports for constant folding during the checks. That output is kept as `validation_initial_check6_whole_process.json`. The check was rescoped to the construction phase (`6331de4`) and the validation rerun from a clean tree. The proposals are byte-identical, and only check 6 changed.

### The C2 conflict

- Prereg §2.1 and the frozen Part AE define C2 in the implementation as a `topk`/`where` gate on activity applied to ΔW. The fingerprint (`Analysis.c2`), the collision pipeline's coupling check and the MAP-Elites descriptor all use this definition, and all are frozen.
- The v6 C2 gate `1 + 0.1·tanh(selector)` contains no `topk`/`where`. It is detected only when the randomly drawn selector happens to contain an activity-reading `topk`/`where` (53 of 338).
- **286 of 338 C2 proposals (84.6%; 28.6% of all proposals) have no coupling at all after canonicalization.** The unchanged pipeline would log them as `pure_rule` and never screen them, so the C2 class would effectively not be searched.
- Constructor invariants "contain C1, C2, or C3" and "pass through the unchanged … rediscovery filters" therefore cannot both hold for C2.

### Secondary observation (handled by the frozen retry rule; not a blocker)

- A depth-2 C2 selector makes `dW` depth 6, over the frozen `MAX_DEPTH` of 5.
- All 258 invalid attempts are of this kind. They count toward the generated budget: about 0.76 extra generated per C2 slot. Realized C2 selectors are always depth 1.

## 4. What an owner decision would need to address

Options only; none was applied.

1. Amend the v6 C2 constructor so the gate is one the frozen detector recognizes: an activity-selected `topk` or `where` gate on ΔW, as in the frozen C2 definition. Choose a selector depth that keeps `dW` within depth 5.
2. Amend the frozen C2 detector so it also counts soft activity-dependent multiplicative gates on ΔW. This changes the collision and descriptor layer, so the golden snapshot and the v5 trace equivalences would need to be rechecked.
3. Search only C1 and C3, or knowingly accept C2 proposals being logged as `pure_rule`. This is a different design from frozen v6.
4. Optionally, confirm or override D-V6-4: the activity-leaf redraws are not counted as generated. There were 2,018 redraws for 1,000 proposals. If they counted, the initial phase would consume about 3.3 generated units per proposal instead of 1.26.

With an amended C2, only the constructor would change. The run command is `python3 scripts/stage2.py stage2_v6`, after the static validation passes.

## 5. Compute

- Static validation: 10.3 CPU-s over four structural runs (the initial run, the check-6 rerun, and two clean-tree reruns). Test runs were negligible and are not ledgered.
- Shared ledger: **0.657 CPU-h of 30**.
- No GPU. No training, T0, probe or benchmark evaluation of any v6 proposal.
