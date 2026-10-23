# Experiment 012 — generated tables

36 runs recorded, 0 skipped, incomplete: none. Rows = initialization seed, columns = training-data seed. `whole-varied@64` on the fixed evaluation set (512 histories). Outcome classes: P = plateau_only, Pa = partial, S = success. Descriptive only; 9 runs per architecture.

## protected — 3 × 3 matrices

Whole-varied@64 (outcome, onset step), row mean | column means below

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.2% (P, —) | 0.0% (P, —) | 0.2% (P, —) | 0.2% |
| **29** | 25.2% (Pa, 1900) | 12.4% (Pa, 1200) | 39.9% (Pa, 1300) | 25.8% |
| **43** | 42.9% (Pa, 1850) | 100.0% (S, 1550) | 99.5% (S, 2250) | 80.8% |
| column mean | 22.8% | 37.5% | 46.6% | |

Final training loss (mean of last five 50-update windows)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.595 | 0.591 | 0.599 | 0.595 |
| **29** | 0.406 | 0.413 | 0.281 | 0.367 |
| **43** | 0.247 | 0.000 | 0.213 | 0.153 |
| column mean | 0.416 | 0.335 | 0.364 | |

Sum-of-squares shares (whole-varied): init 80%, data 7%, remainder (interaction + noise) 13%; (final loss): init 86%, data 3%, remainder 11%. Rows with identical learned/not-learned status across data seeds: 3/3; columns: 0/3. Learned cells 6/9, success cells 2/9.

## protected_no_retain — 3 × 3 matrices

Whole-varied@64 (outcome, onset step), row mean | column means below

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **29** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **43** | 0.0% (P, —) | 0.0% (P, —) | 0.2% (P, —) | 0.1% |
| column mean | 0.0% | 0.0% | 0.1% | |

Final training loss (mean of last five 50-update windows)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.595 | 0.591 | 0.599 | 0.595 |
| **29** | 0.595 | 0.591 | 0.600 | 0.595 |
| **43** | 0.594 | 0.591 | 0.599 | 0.595 |
| column mean | 0.595 | 0.591 | 0.599 | |

Sum-of-squares shares (whole-varied): init 25%, data 25%, remainder (interaction + noise) 50%; (final loss): init 1%, data 99%, remainder 1%. Rows with identical learned/not-learned status across data seeds: 3/3; columns: 3/3. Learned cells 0/9, success cells 0/9.

## gru24 — 3 × 3 matrices

Whole-varied@64 (outcome, onset step), row mean | column means below

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 43.1% (Pa, 2000) | 100.0% (S, 750) | 100.0% (S, 900) | 81.0% |
| **29** | 13.3% (Pa, 1750) | 37.8% (Pa, 1350) | 12.2% (Pa, 1350) | 21.1% |
| **43** | 0.0% (P, —) | 42.2% (Pa, 2200) | 15.1% (Pa, 1650) | 19.1% |
| column mean | 18.8% | 60.0% | 42.4% | |

Final training loss (mean of last five 50-update windows)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.362 | 0.000 | 0.000 | 0.121 |
| **29** | 0.412 | 0.403 | 0.417 | 0.411 |
| **43** | 0.594 | 0.226 | 0.419 | 0.413 |
| column mean | 0.456 | 0.210 | 0.279 | |

Sum-of-squares shares (whole-varied): init 68%, data 23%, remainder (interaction + noise) 8%; (final loss): init 52%, data 30%, remainder 18%. Rows with identical learned/not-learned status across data seeds: 2/3; columns: 2/3. Learned cells 8/9, success cells 2/9.

## gru32 — 3 × 3 matrices

Whole-varied@64 (outcome, onset step), row mean | column means below

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0% (P, —) | 12.8% (Pa, 2850) | 0.0% (P, —) | 4.3% |
| **29** | 0.0% (P, —) | 11.5% (P, —) | 15.1% (Pa, 2100) | 8.9% |
| **43** | 0.2% (P, —) | 18.3% (Pa, 2550) | 100.0% (S, 1750) | 39.5% |
| column mean | 0.1% | 14.2% | 38.4% | |

Final training loss (mean of last five 50-update windows)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.594 | 0.488 | 0.599 | 0.560 |
| **29** | 0.594 | 0.578 | 0.419 | 0.530 |
| **43** | 0.594 | 0.448 | 0.004 | 0.349 |
| column mean | 0.594 | 0.505 | 0.341 | |

Sum-of-squares shares (whole-varied): init 27%, data 28%, remainder (interaction + noise) 45%; (final loss): init 27%, data 34%, remainder 39%. Rows with identical learned/not-learned status across data seeds: 0/3; columns: 1/3. Learned cells 4/9, success cells 1/9.

## Pooled variance partition (within architecture)

| outcome | init share | data share | remainder (interaction + noise) | between-architecture share of total | orientation rule |
|---|---:|---:|---:|---:|---|
| whole_varied_64 | 62% | 18% | 20% | 22% | initialization favoured |
| final_loss | 56% | 22% | 22% | 30% | initialization favoured |

Permutation reference (whole_varied_64, orientation only, NOT a significance test): in 5000 random relabelings of the 9 cells per architecture, 0.1% reach an init share ≥ observed and 72.7% a data share ≥ observed.

Permutation reference (final_loss, orientation only, NOT a significance test): in 5000 random relabelings of the 9 cells per architecture, 0.4% reach an init share ≥ observed and 61.3% a data share ≥ observed.

## Per-axis summaries across all four architectures (12 runs per seed)

| seed | learned as init seed | success as init seed | learned as data seed | success as data seed |
|---:|---:|---:|---:|---:|
| 17 | 4/12 | 2/12 | 4/12 | 0/12 |
| 29 | 7/12 | 0/12 | 7/12 | 2/12 |
| 43 | 7/12 | 3/12 | 7/12 | 3/12 |

Seed 43: successes with init=43: 3/12 (of which with data≠43: 1/8); with data=43: 3/12 (of which with init≠43: 1/8); diagonal (43,43) successes: ['gru32', 'protected'].

## Retention: `protected_no_retain` vs `protected`, paired by (init, data)

| init | data | protected | no_retain | wv protected | wv no_retain |
|---:|---:|---|---|---:|---:|
| 17 | 17 | plateau_only | plateau_only | 0.2% | 0.0% |
| 17 | 29 | plateau_only | plateau_only | 0.0% | 0.0% |
| 17 | 43 | plateau_only | plateau_only | 0.2% | 0.0% |
| 29 | 17 | partial | plateau_only | 25.2% | 0.0% |
| 29 | 29 | partial | plateau_only | 12.4% | 0.0% |
| 29 | 43 | partial | plateau_only | 39.9% | 0.0% |
| 43 | 17 | partial | plateau_only | 42.9% | 0.0% |
| 43 | 29 | success | plateau_only | 100.0% | 0.0% |
| 43 | 43 | success | plateau_only | 99.5% | 0.2% |

No-retain worse in 6/9 cells, better in 0/9, equal class in 3/9 → preregistered 'consistently worse' = **True**.

## Reliability by architecture

| architecture | params | runs | learned (onset) | success | mean whole-varied@64 | onset range | mean final loss | mean train s |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| protected | 8016 | 9 | 6/9 | 2/9 | 35.6% | 1200–2250 | 0.372 | 209 |
| protected_no_retain | 8016 | 9 | 0/9 | 0/9 | 0.0% | — | 0.595 | 200 |
| gru24 | 8112 | 9 | 8/9 | 2/9 | 40.4% | 750–2200 | 0.315 | 158 |
| gru32 | 13888 | 9 | 4/9 | 1/9 | 17.6% | 1750–2850 | 0.480 | 139 |

## Diagnostics at delay 64 pooled by outcome class

| class | runs | per-slot | all-slots-same prediction | predicts last write everywhere | most-recent slot acc | other slots acc | whole-varied by delay (64/128/256/512) |
|---|---:|---:|---:|---:|---:|---:|---|
| plateau_only | 18 | 67.9% | 97.3% | 71.6% | 73.9% | 65.9% | 0.7% / 0.6% / 0.5% / 0.5% |
| partial | 13 | 81.6% | 39.8% | 34.7% | 88.2% | 79.4% | 25.4% / 26.0% / 26.1% / 25.6% |
| success | 5 | 100.0% | 14.9% | 14.9% | 100.0% | 100.0% | 99.9% / 99.9% / 97.9% / 74.3% |

Per-slot accuracy by age of the slot's last write (queried slots pooled over runs; n in parentheses)

| class | initial_only | 1-8 | 9-16 | 17-32 | 33-64 |
|---|---:|---:|---:|---:|---:|
| plateau_only | 65.2% (21438) | 79.9% (2502) | 66.8% (2034) | 70.9% (3924) | 70.4% (6966) |
| partial | 78.2% (15483) | 89.3% (1807) | 86.2% (1469) | 85.4% (2834) | 85.7% (5031) |
| success | 100.0% (5955) | 99.9% (695) | 100.0% (565) | 100.0% (1090) | 100.0% (1935) |

## Baselines on the fixed evaluation set (empirical; analytic shown separately)

| delay | independent guess (per-slot / whole / whole-varied) | analytic guess | last-write copy |
|---|---|---|---|
| 64 | 49.8% / 6.2% / 6.9% | 50.0% / 6.2% / 6.2% | 62.1% / 14.8% / 0.0% |
| 128 | 50.0% / 4.7% / 4.5% | 50.0% / 6.2% / 6.2% | 64.4% / 13.3% / 0.0% |
| 256 | 49.4% / 5.3% / 5.4% | 50.0% / 6.2% / 6.2% | 63.1% / 13.9% / 0.0% |
| 512 | 50.4% / 5.9% / 5.9% | 50.0% / 6.2% / 6.2% | 62.9% / 13.9% / 0.0% |

## Stream / initialization identity checks

Distinct training-stream hashes per data seed (must be 1): {17: 1, 29: 1, 43: 1}.
Distinct init fingerprints per (architecture, init seed) (must be 1): {1}. Same evaluation set for all runs: True.

## Diagonal cells vs Experiment 011 (same init and data seed)

| architecture | seed | loss windows identical | stream identical | wv@64 Exp 011 (seed-specific eval) | wv@64 Exp 012 (fixed eval) | outcome 011 → 012 |
|---|---:|---|---|---:|---:|---|
| gru24 | 17 | True | True | 41.2% | 43.1% | partial → partial |
| gru24 | 29 | True | True | 34.2% | 37.8% | partial → partial |
| gru24 | 43 | True | True | 15.6% | 15.1% | partial → partial |
| gru32 | 17 | True | True | 0.0% | 0.0% | plateau_only → plateau_only |
| gru32 | 29 | True | True | 14.0% | 11.5% | plateau_only → plateau_only |
| gru32 | 43 | True | True | 100.0% | 100.0% | success → success |
| protected | 17 | True | True | 0.0% | 0.2% | plateau_only → plateau_only |
| protected | 29 | True | True | 12.7% | 12.4% | partial → partial |
| protected | 43 | True | True | 99.1% | 99.5% | success → success |
| protected_no_retain | 17 | True | True | 0.0% | 0.0% | plateau_only → plateau_only |
| protected_no_retain | 29 | True | True | 0.0% | 0.0% | plateau_only → plateau_only |
| protected_no_retain | 43 | True | True | 0.0% | 0.2% | plateau_only → plateau_only |
