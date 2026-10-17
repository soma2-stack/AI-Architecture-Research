# Experiment 012 — results: initialization seed versus training-data seed

**Status: complete.** 36/36 preregistered runs (`complete`, 0 skipped, 0 failed, 0 incomplete), 3,000 updates each, 10 local
single-thread CPU workers, **745 s** wall-clock (budget 60 min; no launch was held by the memory/temperature guards; observed
board temperature ≤ 29 °C). Plan: [`EXPERIMENT_012_PLAN.md`](EXPERIMENT_012_PLAN.md), committed in `bf7d767` before the confirmatory run.
Exploratory 3 × 3 factorial per architecture on a synthetic task. **Nine runs per architecture: descriptive, not statistically
definitive, no causal mechanism established.** No novelty claim; `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

Evidence: raw per-run JSON (per-update loss, windows, checkpoints, four-delay evaluations with pattern/age/collapse counts,
baselines, hashes) and logs in [`reports/experiment_012/`](reports/experiment_012/); generated
[`tables.md`](reports/experiment_012/tables.md) (all matrices), [`summary.json`](reports/experiment_012/summary.json),
[`figures/`](reports/experiment_012/figures/) (learning curves, one 3 × 3 grid per architecture + a by-data-seed overview),
[`posthoc.json`](reports/experiment_012/posthoc.json) (post-hoc checks, labeled as such).
Regenerate: `python -m prototypes.rnn_llm_architecture.experiment_012_report prototypes/rnn_llm_architecture/reports/experiment_012`.

**Validity checks (all pass):** one training-stream hash per data seed across all architectures and init seeds; one initialization
fingerprint per (architecture, init seed); one evaluation set shared by every run; **all 12 `init == data` cells reproduce
Experiment 011's training-loss windows and stream hashes exactly** (training is deterministic, so differences between cells are real
seed effects, not run-to-run noise). Preregistered definitions: learning onset = start of the first 50-update window after which
every window averages < 0.50 loss; *plateau_only* (no onset) / *partial* (onset, whole-varied@64 < 90 %) / *success* (≥ 90 %).

## Answers to the stop-condition questions

1. **Initialization or training data?** By the preregistered orientation rule, **initialization explains more than the training
   stream**: pooled over architectures the init main effect carries 62 % of within-architecture variance in whole-varied@64 (data 18 %,
   remainder 20 %); for final training loss 56 % / 22 % / 22 %. The init share is far above chance reshuffles of the cells (0.1 % of
   5,000 relabelings reach it) whereas the data share is not (72.7 %) — orientation only, not a significance test. But the picture
   is architecture-specific: `protected` is init-driven (80 % / 7 % / 13 %), `gru24` mostly init (68 % / 23 % / 8 %), and `gru32`
   shows **neither factor consistent** (27 % / 28 % / 45 %; success only where a favourable init meets a favourable stream, i.e. an
   interaction). Because training is deterministic, the "remainder" is non-additivity (interaction), not replicate noise.
   A seed number does not map to comparable weights across architectures, so "initialization favoured" means *which random weights
   a given architecture gets*, not a shared good seed (best init: `protected` 43, `gru24` 17, `gru32` 43).
2. **Most reliable architecture:** none is reliable. `gru24` most often begins sustained learning (**8/9** runs; mean whole-varied 40.4 %)
   but only 2/9 reach success; `protected` 6/9 learned, 2/9 success (35.6 %); `gru32` 4/9, 1/9 (17.6 %); `protected_no_retain` 0/9, 0/9.
   `protected` and `gru24` are indistinguishable on success; **no protected-memory superiority is claimed.**
3. **Did removing slow retention consistently hurt?** **Yes on this task, by the preregistered rule:** `protected_no_retain` never
   began learning in any of the 9 cells (all plateau_only, final loss 0.591–0.600), never beat `protected` in any paired cell, and was worse in
   6/9 (the other 3 are cells where `protected` also stayed on the plateau). This is **task-specific evidence** at this width and budget, not proof
   that protected retention is generally superior (Experiment 009 found equal two-slot learning without retention).
4. **Did the seed-43 advantage persist once the streams were separated?** **Partly, and as an initialization effect for two
   architectures.** Init 43 gave `protected` 2 successes + 1 partial and `gru32` 1 success + 1 partial + 1 plateau (its best row in both),
   but `gru24` was *worst* with init 43 and best with init 17. The Exp 011 successes replicate on the diagonal ((43,43) for `protected` and `gru32`),
   but only 2 of the 5 successes in this experiment are those; the others are `protected` (43, data 29), and `gru24` (17, data 29) and
   (17, data 43). Across all 12 runs, init 43 yielded 3 successes (1/8 with data ≠ 43) and data 43 yielded 3 (1/8 with init ≠ 43).
   "Seed 43" is therefore not a general property of the stream or of the number.
5. **What remains unexplained** — see below.
6. Commit, tests, runtime, raw locations — see final section.

## 3 × 3 matrices: whole-varied accuracy @64 tokens (outcome, onset update). Rows = init seed, columns = data seed

**protected** (8,016 params)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.2 % (P, —) | 0.0 % (P, —) | 0.2 % (P, —) | 0.2 % |
| **29** | 25.2 % (Pa, 1900) | 12.4 % (Pa, 1200) | 39.9 % (Pa, 1300) | 25.8 % |
| **43** | 42.9 % (Pa, 1850) | **100 %** (S, 1550) | **99.5 %** (S, 2250) | 80.8 % |
| col mean | 22.8 % | 37.5 % | 46.6 % | |

**protected_no_retain** (8,016): all nine cells 0.0–0.2 % (plateau_only); every row/column mean ≤ 0.1 %.

**gru24** (8,112)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 43.1 % (Pa, 2000) | **100 %** (S, 750) | **100 %** (S, 900) | 81.0 % |
| **29** | 13.3 % (Pa, 1750) | 37.8 % (Pa, 1350) | 12.2 % (Pa, 1350) | 21.1 % |
| **43** | 0.0 % (P, —) | 42.2 % (Pa, 2200) | 15.1 % (Pa, 1650) | 19.1 % |
| col mean | 18.8 % | 60.0 % | 42.4 % | |

**gru32** (13,888)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0 % (P, —) | 12.8 % (Pa, 2850) | 0.0 % (P, —) | 4.3 % |
| **29** | 0.0 % (P, —) | 11.5 % (P, —) | 15.1 % (Pa, 2100) | 8.9 % |
| **43** | 0.2 % (P, —) | 18.3 % (Pa, 2550) | **100 %** (S, 1750) | 39.5 % |
| col mean | 0.1 % | 14.2 % | 38.4 % | |

Final-training-loss matrices, variance-share tables, per-axis tables and all other outputs are in `tables.md`.
Outcome counts over 36 runs: **18 plateau_only, 13 partial, 5 success**.

## Per-axis summaries (all four architectures, 12 runs per seed)

| seed | learned as init | success as init | learned as data | success as data |
|---:|---:|---:|---:|---:|
| 17 | 4/12 | 2/12 | 4/12 | 0/12 |
| 29 | 7/12 | 0/12 | 7/12 | 2/12 |
| 43 | 7/12 | 3/12 | 7/12 | 3/12 |

Consistency of learned/not-learned status: init rows identical across the three data seeds in 3/3 (`protected`), 3/3
(`protected_no_retain`), 2/3 (`gru24`), 0/3 (`gru32`); data columns identical in 0/3, 3/3, 2/3, 1/3. Within `protected`, init 17
never learned with any stream (3/3 plateau) and init 43 learned with every stream — success follows the initialization across
different training streams. Per-architecture column means show **data seed 17 lowest for all three learning architectures**
(22.8 %, 18.8 %, 0.1 %; 0/12 successes, 4/12 learned vs 7/12 for each other data seed, and late onsets 1750–2000 when it partially
learns). Pooled this is a weak share (18 %, indistinguishable from reshuffling), so it is a **lead for the training-stream question,
not a finding**; because the stream is shared across architectures, this cross-architecture consistency is informative for data
seeds in a way it cannot be for init seeds.

## Learning curves, plateau and onset

- **Initial convergence is the same plateau everywhere.** All 18 plateau_only runs sit at the same loss (0.578–0.600), and that loss is
  fixed by the *data seed*, not the model (≈ 0.594/0.595 for data 17, 0.591 for 29, 0.599–0.600 for 43; for `protected_no_retain` data
  seed explains 99 % of final-loss variance). They collapse to one remembered value: 97.3 % of histories get the same prediction for all
  four slots (71.6 % equal the last written value), per-slot accuracy 67.9 %, whole-varied ≈ 0.5–0.7 % at every delay; baselines on the
  same set: last-write copy 62.1 % per-slot, 0.0 % whole-varied; independent guess 49.8 % per-slot, 6.2 % whole (theory 50 % / 6.25 %).
- **Onset** (sustained loss < 0.50) ranges from update 750 (`gru24` 17/29) to 2850 (`gru32` 17/29). Typical `protected` onsets 1200–2250.
- **Partial learning** (13 runs; whole-varied 12–43 %, mean ≈ 25 %): same-prediction collapse falls to 39.8 %; most-recent-slot accuracy 88.2 % vs
  79.4 % for other slots; accuracy by last-write age: never-rewritten slots 78.2 % versus 85–89 % for recently rewritten slots.
- **Success** (5 runs): per-slot 100 %, collapse only where all four values truly agree (14.9 %), whole-varied 99.9 / 99.9 / 97.9 / 74.3 % at 64 / 128 / 256 / 512 tokens
  (same length degradation at 8× as Experiment 011).
- **Post-hoc observations** (not preregistered; `posthoc.json`): partial runs mostly settle on a *second* plateau at loss 0.403–0.419 (7 of 13), and
  **5 of 13 partial runs were still descending sharply when the budget ended** (`protected` 29/43 and 43/17, `gru24` 17/17, `gru32` 17/29 and 43/29). "Partial"
  therefore partly means "not yet finished" and the success counts are lower bounds at 3,000 updates.

## Comparison with Experiment 011

- The 12 diagonal cells are exact replays of Experiment 011's training (identical loss windows and stream hashes); outcome classes agree in
  **12/12**, and whole-varied@64 differs by ≤ 3.6 points (only because the evaluation set is now fixed instead of seed-derived).
- Experiment 011's headline — 2/12 solved, strongly seed-dependent — is reproduced. What changes is its **interpretation**: in 011 "seed 43"
  bundled initialization, stream and evaluation set. Separating them shows that success depends mostly on the initialization (within an
  architecture), partly on a favourable stream (strongly for `gru32`), and that off-diagonal cells yield additional successes (3 of the 5),
  including `gru24`, which had none in 011.
- Aggregate over all 9 cells: `gru24` 40.4 %, `protected` 35.6 %, `gru32` 17.6 % (Exp 011's three-seed means 30.3 %, 37.3 %, 38.0 %) — rankings among
  the learning architectures are unstable across seed sets, consistent with "no protected-memory superiority".

## What remains unexplained

- **Why** particular initializations succeed (no weight, spectrum or dynamics analysis was done; the factorial cannot identify a mechanism).
- Whether the init effect is a property of the initial weights, of the early optimization path, or of both; only three init seeds per architecture.
- Why the stream matters for `gru32` (and possibly why data seed 17 is poor) — streams were not inspected for curriculum properties.
- Whether the 5 still-descending partial runs and the 18 plateau runs would resolve with more updates (the 3,000 budget was fixed by design).
- Why removing slow retention removes learning entirely here when it did not in Experiment 009's two-slot task.
- The second plateau near loss 0.41 (what policy it implements) — only described, not analysed.

## Limitations

Nine runs per architecture, one run per cell (no replicates; deterministic, so the remainder is interaction not noise but cannot be split
further); only three init and three data seeds; the variance shares and permutation reference are orientation tools, not tests;
hyperparameters, width and 3,000-update budget unchanged and untuned; evaluation set fixed (512 histories, finite-sample error ≈ 1–2 points
on whole-varied); executed locally (PyTorch 2.13.0+cu130 with CUDA hidden, Python 3.11.9), no hosted replication.
The 300-update implementation pilot (six cells, outside the repository) is not part of the evidence.

Preserved: Experiments 001–011 evidence, frozen files and `AGENTS.md` are unchanged; nothing was pushed.
