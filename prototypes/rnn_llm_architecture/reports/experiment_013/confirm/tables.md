# Experiment 013 — generated tables

A and D are Experiment 012 runs (reused); B and C are new. Rows = init seed, columns = data seed. whole-varied@64 on the fixed Experiment 012 evaluation set (512 histories). P = plateau_only, Pa = partial, S = success. Descriptive; 9 runs per condition.

## Summary

| cond | model | slow-write gate | live / allocated params | learned | success | mean wv @64 / @128 / @256 / @512 | mean per-slot@64 | mean train s |
|---|---|---|---:|---:|---:|---|---:|---:|
| A | `protected` | learned gate | 8,016 / 8,016 | 6/9 | 2/9 | 35.6% / 36.2% / 35.2% / 26.4% | 81.9% | 209 |
| B | `protected_fixed_0474` | fixed g = sigmoid(-3) = 0.0474 | 7,488 / 8,016 | 1/9 | 0/9 | 3.7% / 3.7% / 3.9% / 3.5% | 69.1% | 309 |
| C | `protected_fixed_005` | fixed g = 0.005 | 7,488 / 8,016 | 4/9 | 1/9 | 23.1% / 22.0% / 18.2% / 13.0% | 76.9% | 273 |
| D | `protected_no_retain` | forced overwrite (g = 1) | 7,488 / 8,016 | 0/9 | 0/9 | 0.0% / 0.0% / 0.0% / 0.1% | 67.6% | 200 |

## A: learned gate — 3 × 3 (whole-varied@64, outcome, onset)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.2% (P, —) | 0.0% (P, —) | 0.2% (P, —) | 0.2% |
| **29** | 25.2% (Pa, 1900) | 12.4% (Pa, 1200) | 39.9% (Pa, 1300) | 25.8% |
| **43** | 42.9% (Pa, 1850) | 100.0% (S, 1550) | 99.5% (S, 2250) | 80.8% |
| col mean | 22.8% | 37.5% | 46.6% | |

Variance shares (whole-varied): init 80%, data 7%, remainder 13%. Learned by init seed: {17: 0, 29: 3, 43: 3}. Accuracy@64 never-rewritten slots 79.9%, rewritten slots 84.6%.

## B: fixed g = sigmoid(-3) = 0.0474 — 3 × 3 (whole-varied@64, outcome, onset)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **29** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **43** | 0.0% (P, —) | 33.3% (Pa, 1800) | 0.0% (P, —) | 11.1% |
| col mean | 0.0% | 11.1% | 0.0% | |

Variance shares (whole-varied): init 25%, data 25%, remainder 50%. Learned by init seed: {17: 0, 29: 0, 43: 1}. Accuracy@64 never-rewritten slots 66.6%, rewritten slots 72.6%.

## C: fixed g = 0.005 — 3 × 3 (whole-varied@64, outcome, onset)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **29** | 0.2% (P, —) | 12.4% (Pa, 1550) | 39.0% (Pa, 2800) | 17.2% |
| **43** | 47.0% (Pa, 1200) | 9.6% (P, —) | 100.0% (S, 1300) | 52.2% |
| col mean | 15.7% | 7.3% | 46.3% | |

Variance shares (whole-varied): init 46%, data 28%, remainder 26%. Learned by init seed: {17: 0, 29: 2, 43: 2}. Accuracy@64 never-rewritten slots 74.2%, rewritten slots 80.7%.

## D: forced overwrite (g = 1) — 3 × 3 (whole-varied@64, outcome, onset)

| init \ data | 17 | 29 | 43 | row mean |
|---|---|---|---|---:|
| **17** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **29** | 0.0% (P, —) | 0.0% (P, —) | 0.0% (P, —) | 0.0% |
| **43** | 0.0% (P, —) | 0.0% (P, —) | 0.2% (P, —) | 0.1% |
| col mean | 0.0% | 0.0% | 0.1% | |

Variance shares (whole-varied): init 25%, data 25%, remainder 50%. Learned by init seed: {17: 0, 29: 0, 43: 0}. Accuracy@64 never-rewritten slots 65.3%, rewritten slots 70.8%.

## Paired comparisons (preregistered rule)

| X vs Y | X higher class | X lower class | mean wv@64 X − Y | learned X/Y | success X/Y | verdict |
|---|---:|---:|---:|---|---|---|
| A vs B | 6 | 0 | +31.9 pts | 6/1 | 2/0 | A outperforms B |
| A vs C | 2 | 0 | +12.5 pts | 6/4 | 2/1 | inconclusive |
| B vs D | 1 | 0 | +3.7 pts | 1/0 | 0/0 | comparable |
| C vs D | 4 | 0 | +23.1 pts | 4/0 | 1/0 | C outperforms D |
| B vs C | 1 | 4 | -19.4 pts | 1/4 | 0/1 | inconclusive |
| A vs D | 6 | 0 | +35.6 pts | 6/0 | 2/0 | A outperforms D |

## Preregistered interpretation flags

- 1_learned_gate_necessary (A outperforms both B and C): **False**
- 2_fixed_retention_sufficient (B or C comparable to or better than A): **False**
- 3_retention_per_se_matters (B or C outperforms D): **True**
- 4a_stronger_retention_prevents_updating (B>C and C rewritten < initial-only): **False**
- 4b_stronger_retention_helps (C outperforms B): **False**
