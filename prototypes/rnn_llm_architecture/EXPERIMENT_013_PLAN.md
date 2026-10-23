# Experiment 013 — learned slow-write gate versus fixed write rate

**Status: Phases 1–2 done (audit and exploratory diagnostics); Phase 3 preregistered here before its confirmatory runs.**
Directed by GPT-6; engineering by Claude. No new architecture. No novelty or formal learning-credit claim.
`D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Question

Experiment 012 found `protected` learned four-slot recall in 6/9 cells (2 successes) and `protected_no_retain` in 0/9. Which
property is responsible: (1) retaining state at all instead of overwriting, (2) a slow fixed write rate, (3) *learned,
input-dependent* write gates, or (4) something else in the recurrent dynamics?

## Phase 1 — mechanistic audit (code inspection + autograd; established facts)

Evidence: `audit_013.py` → [`reports/experiment_013/audit_phase1.json`](reports/experiment_013/audit_phase1.json).

Protected update in each of the 2 layers (`ProtectedMemoryCell.step`), with Walsh masks `M` (8 × 32, rows orthonormal to
6e-8), coefficients `c = M h`, layer input `x_t` (token embedding in layer 0; normalized layer-0 state in layer 1):

```
p_t   = tanh(W_x x_t + b + U h_{t-1})                      # proposal (slow_feedback=True: feeds back full h)
g_t   = sigmoid(W_g x_t + b_g)        in (0,1)^8           # slow write gate; depends on x_t only, not on h
r_t   = sigmoid(W_r x_t + b_r)        in (0,1)^32          # fast retention gate, b_r = +1  (≈ 0.73 at init)
c_t   = c_{t-1} + g_t ⊙ (M p_t − c_{t-1})                  # = (1−g_t)⊙c_{t-1} + g_t⊙M p_t
f_t   = Π⊥[ r_t ⊙ Π⊥h_{t-1} + (1−r_t) ⊙ Π⊥p_t ]            # Π⊥ = I − MᵀM (project_fast=True)
h_t   = Mᵀ c_t + f_t
```

- **`retain_slow=False`** replaces `g_t` by 1, so `c_t = M p_t`: the 8 protected coefficients become a memoryless tanh
  readout of the current proposal. The 24-dimensional fast complement keeps its own input-gated leaky retention.
  `sigmoid(W_g x + b_g)` is still computed but discarded, so **`slow_gate` (2 × (32·8 + 8) = 528 parameters) receives no
  gradient** (verified by autograd): allocated 8,016, **live 7,488**. `protected`: 8,016 live. GRU-24 8,112, GRU-32 13,888 (all live).
- `protected` and `protected_no_retain` have **identical initial weights** for each seed (fingerprints equal), so the
  Experiment 012 pairing is a clean mechanism ablation, but it removes four things at once: retention itself, the slow time
  constant, input dependence and learnability of the gate, and 528 trainable parameters. **It cannot isolate the benefit of
  learning the gate.** The fixed-gate controls below remove only the last two.
- At initialization the gate is **not** a constant `sigmoid(−3) = 0.0474`: `W_g` is Xavier-initialized, so layer-0 gates
  range 0.025–0.084 across task tokens. A fixed 0.0474 control equals the initial *bias*, not the initial gate function.
- **Relation to known mechanisms:** the coefficient update is a coupled input/forget (convex) gate — the GRU update gate, the
  LSTM with coupled input–forget gate, or a leaky integrator with input-dependent rate — restricted to a fixed orthonormal
  8-dimensional subspace and without a reset gate. The fast complement is likewise a GRU-style convex update. With a fixed g
  it is a leaky-integrator / echo-state-style fixed time constant on that subspace. Nothing in the coefficient equation is
  beyond standard gated recurrence; the distinctive parts are the fixed Walsh subspace split and its projections.
- Experiment 012 streams: the three data seeds have essentially the same aggregate statistics (mean marked rewrites 1.996–
  1.999 per history; 87.5–87.7 % varied; 57.8–57.9 % of slots never rewritten), so aggregate composition does not explain the
  data-seed differences.

## Phase 2 — diagnostics on reproduced weights (EXPLORATORY)

Experiment 012 saved no weights. Seven runs were re-trained deterministically with snapshots at 0–3,000 updates
(`protected` 17/17, 17/43 plateau; 29/29, 43/17 partial; 43/29, 43/43 success; `protected_no_retain` 43/43). **All
3,000 per-update losses and every evaluation metric match Experiment 012 exactly.** Diagnostics: `diagnose_013.py` →
`reports/experiment_013/diagnostics_phase2.json`; results summarized in `EXPERIMENT_013_RESULTS.md`. These results do not alter the Phase 3 design,
which is fixed by the directive.

## Phase 3 — fixed-retention controls (preregistered)

| | condition | slow-write gate | live params | source |
|---|---|---|---:|---|
| A | `protected` (learned, input-dependent) | `sigmoid(W_g x + b_g)` | 8,016 | Experiment 012 runs, reused (determinism verified on 6 cells) |
| B | `protected_fixed_0474` | constant `sigmoid(−3)` = 0.047426 | 7,488 | **new** |
| C | `protected_fixed_005` | constant 0.005 | 7,488 | **new** |
| D | `protected_no_retain` (forced overwrite) | constant 1 | 7,488 | Experiment 012 runs, reused |

B and C (`capacity_013.py`) are built from the exact `protected` model of the same init seed and replace only the gate output of
`prepare()`; the recurrent operator, masks, feedback, fast gate, width, optimizer and coefficient equation are unchanged
(tests: g = 1 reproduces D bit-for-bit; A's loop reproduces Experiment 012 bit-for-bit; the coefficient update is checked
against the equation above). Matrix: init seeds 17, 29, 43 × data seeds 17, 29, 43 → **18 new runs**, 3,000 updates,
lr 0.002, batch 12, clip 1.0, Experiment 012 training streams and the identical fixed evaluation histories (512 per delay)
at 64/128/256/512 tokens. Full learning curves, per-slot/whole/whole-varied accuracy, age-of-last-write accuracy, runtime,
live parameters; weights saved at 0 and 3,000 updates for diagnostics. ≈ 10 workers, per-run wall cap 1,800 s.

**Pilot:** 2 cells (one per condition), 300 updates, to validate wiring and project runtime. If the projected wall time
for all 18 runs exceeds the remaining training budget (60 min total for Experiment 013 including the ≈ 5 min Phase 2 reproduction),
stop and report — no conditions are dropped after outcomes are seen.

### Outcome definitions (unchanged from Experiment 012)

Onset = start of the first 50-update window after which every window mean loss < 0.50; plateau_only / partial / success
(success = onset and whole-varied@64 ≥ 90 %), ranked plateau_only < partial < success.

### Comparison rules (fixed now)

For two conditions X, Y compared cell by cell (same init and data seed):

- **X outperforms Y** if X has a higher outcome class in ≥ 4 of 9 paired cells and a lower one in ≤ 1, **and** X's mean
  whole-varied@64 exceeds Y's by ≥ 20 points.
- **X and Y comparable** if neither outperforms the other and |learned count difference| ≤ 1 and |success count difference| ≤ 1.
- Otherwise **inconclusive**.

Interpretation:

1. *Learned input-dependent writing is necessary* is supported only if A outperforms **both** B and C. Even then, alternative
   explanations must be checked first: A has 528 more trainable parameters, and its initial gate function differs from B's constant.
2. *Fixed retention is sufficient* if B or C is comparable to A or outperforms it ⇒ "the adaptive-write hypothesis is unsupported by this experiment".
3. *Retention per se matters* if B or C outperforms D.
4. *Stronger retention prevents updating* if B outperforms C **and** C's accuracy on rewritten slots is below its accuracy on never-rewritten slots
   (age-of-last-write breakdown); *stronger retention helps* if C outperforms B.
5. Initialization dependence under fixed gates is reported with the Experiment 012 axis summaries (descriptive only).
6. No architecture-level advantage is claimed from one seed, from unequal parameter budgets, or from the synthetic task alone.

## Out of scope

Experiment 014, new architectures, GPU, changes to `main`, `AGENTS.md`, PR #23, Experiments 001–012 code or evidence.
Committed locally, **not pushed**, pending GPT-6 review.

## Reproduction

```
powershell -NoProfile -File "E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1" -Module capacity_013 -Workers 10 -ShardArg jobs `
  -ShardValues <arch:init:data,...> -ExtraArgs "--steps 3000 --save-weights-at 0,3000 --weights-dir <dir>" -MaxWallSeconds 1800 -Run
python -m prototypes.rnn_llm_architecture.experiment_013_report <exp013 confirm dir> <exp012 dir>
```
