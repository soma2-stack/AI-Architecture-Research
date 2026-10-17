# Experiment 012 — initialization seed versus training-data seed

**Status: preregistered before the confirmatory run.** Directed by GPT-6; engineering by Claude. A controlled
factorial on the unchanged four-slot binary task. No architecture, width, optimizer or hyperparameter is modified.
No novelty claim. `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Phase 0 — audit of Experiment 011 (completed before this plan)

Commit `7e378c6`; details in the audit addendum of [`EXPERIMENT_011_RESULTS.md`](EXPERIMENT_011_RESULTS.md) and
[`reports/experiment_011_audit/audit_011.json`](reports/experiment_011_audit/audit_011.json). Summary: all reported values match
the raw JSON; "6 vs 7 runs ≥ 70 % per-slot" is two definitions (6 by 250-update checkpoint, 7 by final evaluation; the
difference is `gru32` seed 29: 68.2 % best checkpoint, 71.9 % final); the 6.9 % independent-guess figure is an *empirical*
mean over three 256-history evaluation sets (theory 6.25 %); and **in Experiment 011 one seed number set the initialization, the
training stream and the evaluation histories simultaneously**, which is exactly the confound this experiment removes.

## Question

Why do some models suddenly learn four-slot memory while others stay near the plateau?
H1 initialization dependence · H2 training-data dependence · H3 interaction of the two.

## Design

Three independent random streams (`capacity_012.py`):

| stream | controls | values |
|---|---|---|
| `init_seed` | model initialization only (`config.seed` → `torch.manual_seed` inside `fork_rng`) | 17, 29, 43 |
| `data_seed` | training stream only (same formula as Exp. 011: `seed·1,000,003 + step·8191 + 4·197 + 2`) | 17, 29, 43 |
| evaluation | **one fixed** held-out set per delay, `100,000,000 + delay`; independent of both seeds and shared by every model | — |

Full 3 × 3 crossing of init × data seeds for each of `protected`, `protected_no_retain`, `gru24`, `gru32` = **36 learned runs**,
3,000 updates each, training delay 64, batch 12, AdamW lr 0.002, clip 1.0. All architectures sharing a `data_seed` receive
the byte-identical training stream. Evaluation at 64, 128, 256, 512 tokens on **512** histories per delay. Checkpoint
evaluation every 250 updates (128 fixed histories, delay 64). `init == data` cells replay Experiment 011's training
trajectory exactly (verified in the pilot and by test); only their evaluation set differs (fixed, not seed-derived).
The explicit-address delta-rule reference is not rerun (not needed for this question).

Implementation validation pilot (done; 300 updates, six cells, outside the repository): diagonal cells reproduce Exp. 011
loss windows bit-for-bit; shared data seed ⇒ identical stream hash across architectures; shared (architecture, init
seed) ⇒ identical initialization fingerprint; ≈ 18–23 s per 300 updates ⇒ ≈ 5 min per full run ⇒ 36 runs on 10 workers
≈ 20–30 min, inside the 60-minute budget. **No run is extended, repeated or dropped on the basis of its outcome.**

## Outcome definitions (fixed before the confirmatory run; calibrated only on Experiment 011's curves)

- **Learning onset** = number of updates completed before the first 50-update window from which *every* later window's mean
  training loss is below **0.50** (sustained to the end of training; `learning_onset()`). Experiment 011: all stuck windows
  ≥ 0.553, all learners stayed < 0.483 after first crossing. Dips that do not persist do not count.
- **Outcome class** (per run, using the fixed evaluation set at delay 64):
  - **plateau_only** — initial convergence only: no sustained onset (last-write-style plateau, loss ≈ 0.55–0.70);
  - **partial** — onset reached but whole-varied accuracy < 90 %;
  - **success** — onset reached and whole-varied accuracy ≥ 90 %.
  Runs that do not complete (`time_limit`, non-finite loss/gradient) are labelled `incomplete:<reason>` and reported.
- Collapse diagnostics: fraction of histories where all four slot predictions are identical, and where all four equal
  the most recent written value (overall and varied-only).

## Measurements per run

Whole-memory, whole-varied and per-slot accuracy at four delays; per-slot-index accuracy; training loss at every
optimizer update (plus 50-update windows); 250-update checkpoints; onset; outcome class; predicted/true 4-bit pattern
histograms; accuracy by age of each slot's last write (`initial_only`, 1–8, 9–16, 17–32, 33–64, 65–128, 129–256, 257+) and
for the most recently written slot versus the others; independent-guess and last-write baselines (empirical **and**
theoretical values reported separately); parameters; wall/CPU time; initialization fingerprint; training-stream SHA-256.

## Analysis plan (descriptive; fixed in advance)

1. For each architecture a **3 × 3 matrix (init seed rows × data seed columns)** of whole-varied@64, outcome class, onset
   and final training loss (mean of the last five 50-update windows); row (init) and column (data) means beside each matrix.
2. **Variance partition** of whole-varied@64 and of final training loss: within each architecture, sums of squares for the
   init main effect, data main effect and the remainder (interaction **plus** run-to-run noise — with one run per cell they
   cannot be separated); pooled across architectures, plus the share between architectures. Orientation rule: *initialization
   favoured* if pooled init share ≥ 0.30 and ≥ 2 × data share; *training data favoured* if the reverse; otherwise
   *neither factor consistent / unexplained*. A large remainder is reported as interaction-or-noise, not as evidence of H3.
3. **Consistency counts:** per architecture, rows (and columns) in which all three cells share the same learned/not-learned
   status; across architectures, the learned rate for each data seed (12 runs) and each init seed (12 runs).
4. **Seed-43 question:** learned/success rates for init = 43 versus data = 43 versus the other seeds, pooled and per architecture.
5. **Retention:** paired by (init, data) cell, `protected_no_retain` vs `protected`; "consistently worse" only if never
   better in outcome class and worse in ≥ 5 of 9 cells.
6. **Reliability** per architecture: learned rate, success rate, mean whole-varied, onset spread.
7. **Comparison with Experiment 011** on the 12 diagonal cells (training identical; outcomes under the fixed eval set).
8. A permutation reference (random relabeling of the 9 cells within each architecture) is given only for orientation and is
   **not** a significance claim. With 9 runs per architecture no statistically definitive or causal claim is made.

## Interpretation rules (from the directive)

Success following init across data streams ⇒ initialization promising. Success following data seed across inits ⇒ investigate
the training stream/curriculum. Neither consistent ⇒ "effect remains unexplained". Protected ≈ GRU ⇒ no protected-memory
superiority claim. Consistent harm from removing retention ⇒ task-specific evidence only.

## Out of scope

Experiment 013, any new architecture, GPU use, changes to `main`, `AGENTS.md`, PR #23 or Experiments 001–011. Results
are committed locally on this branch and **not pushed** pending GPT-6 review.

## Reproduction

```
powershell -NoProfile -File "E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1" -Module capacity_012 -Workers 10 `
  -ShardArg jobs -ShardValues <arch:init:data,...> -ExtraArgs "--steps 3000" -MaxWallSeconds 1800 -Run
python -m prototypes.rnn_llm_architecture.experiment_012_report prototypes/rnn_llm_architecture/reports/experiment_012
```
