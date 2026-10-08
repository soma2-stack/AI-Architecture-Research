# Experiment 015 — generated tables

Layer-1 edits; eligible recipients (original target prediction correct; twin donors: both twins correct). Target accuracy = target slot correct for the recipient's own history. `S` = designated 8-d subspace (GRU: arbitrary Walsh-8, no protected role), `C` = its 24-d complement.

## Validity

| model | archive exact | stepper = Exp 014 stepper (max gap) | sham gap (same batch) | pairs valid |
|---|---|---:|---:|---|
| `prot_success_43_29` | True | 0.0e+00 | 0.0e+00 | True |
| `prot_success_43_43` | True | 0.0e+00 | 0.0e+00 | True |
| `fixed005_success_43_43` | True | 0.0e+00 | 0.0e+00 | True |
| `gru32_success_43_43` | True | 0.0e+00 | 0.0e+00 | True |
| `prot_failed_17_17` | True | 0.0e+00 | 0.0e+00 | True |
| `prot_partial_43_17` | True | 0.0e+00 | 0.0e+00 | True |

## Verdicts

| model | role | model verdict | cells supported / contradicted / inconclusive |
|---|---|---|---|
| `prot_success_43_29` | successful learned-gate protected RNN | **inconclusive** | 6 / 0 / 3 |
| `prot_success_43_43` | successful learned-gate protected RNN (replicate) | **inconclusive** | 6 / 0 / 3 |
| `fixed005_success_43_43` | successful fixed-0.005-gate protected RNN | **contradicted** | 0 / 9 / 0 |
| `gru32_success_43_43` | successful GRU-32 (ordinary recurrence), reproduced | **contradicted** | 0 / 9 / 0 |
| `prot_failed_17_17` | failed (plateau) protected RNN | **inconclusive** | 0 / 0 / 9 |
| `prot_partial_43_17` | partially trained protected RNN (wv@64 42.9%) | **inconclusive** | 0 / 0 / 9 |

## Answers to the preregistered questions

- Q1_removal_selectively_destroys_recall: **inconclusive**
- Q2_rescue_recovers: **supported**
- Q3_exceeds_matched_random: **inconclusive**
- Q4_more_than_one_network: **inconclusive**
- Q5_fixed_gate_counterexample_to_architectural_necessity: **supported**

## Every cell (eligible recipients)

| model | delay | timing | n | original (all) | S mean | S zero | min R8 mean | min R8 norm-matched | C mean | rescue S | rescue C only | unrel. same: acc | unrel. diff: donor | twin→S donor | twin→C donor | full mean | NN ratio S / worst R8 | N1 N2 N4 N5 (N3) | verdict |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `prot_success_43_29` | 64 | after_write | 512 | 100% | 61% | 61% | 95% | 97% | 100% | 100% | 79% | 100% | 100% | 100% | 0% | 52% | 2.44 / 1.88 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 64 | mid_continuation | 512 | 100% | 62% | 61% | 94% | 96% | 100% | 100% | 80% | 100% | 99% | 100% | 0% | 50% | 4.94 / 3.19 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 64 | before_query | 512 | 100% | 84% | 78% | 94% | 94% | 100% | — | — | 100% | 97% | 100% | 0% | 50% | 4.89 / 3.21 | n n – Y (Y) | inconclusive |
| `prot_success_43_29` | 128 | after_write | 512 | 100% | 60% | 58% | 94% | 96% | 100% | 100% | 77% | 100% | 100% | 99% | 1% | 51% | 1.74 / 1.42 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 128 | mid_continuation | 512 | 100% | 57% | 58% | 93% | 94% | 100% | 100% | 76% | 100% | 99% | 99% | 1% | 50% | 5.30 / 3.37 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 128 | before_query | 512 | 100% | 82% | 75% | 93% | 92% | 100% | — | — | 100% | 95% | 98% | 2% | 50% | 5.08 / 3.29 | n n – Y (Y) | inconclusive |
| `prot_success_43_29` | 256 | after_write | 506 | 99% | 53% | 56% | 88% | 94% | 96% | 98% | 61% | 99% | 92% | 93% | 6% | 51% | 1.86 / 1.47 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 256 | mid_continuation | 506 | 99% | 51% | 56% | 87% | 92% | 95% | 99% | 59% | 98% | 92% | 93% | 7% | 51% | 4.93 / 3.27 | Y Y Y Y (Y) | supported |
| `prot_success_43_29` | 256 | before_query | 506 | 99% | 61% | 77% | 87% | 91% | 96% | — | — | 98% | 86% | 89% | 11% | 51% | 4.77 / 3.03 | Y n – Y (Y) | inconclusive |
| `prot_success_43_43` | 64 | after_write | 512 | 100% | 60% | 59% | 96% | 98% | 100% | 97% | 87% | 100% | 98% | 98% | 1% | 53% | 1.96 / 1.56 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 64 | mid_continuation | 512 | 100% | 55% | 56% | 94% | 96% | 100% | 97% | 82% | 99% | 99% | 99% | 0% | 49% | 3.30 / 2.91 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 64 | before_query | 512 | 100% | 83% | 74% | 92% | 97% | 96% | — | — | 97% | 80% | 84% | 16% | 50% | 3.25 / 2.89 | n n – n (Y) | inconclusive |
| `prot_success_43_43` | 128 | after_write | 512 | 100% | 57% | 56% | 97% | 98% | 100% | 99% | 82% | 100% | 97% | 97% | 0% | 53% | 1.50 / 1.33 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 128 | mid_continuation | 512 | 100% | 55% | 53% | 96% | 96% | 100% | 96% | 84% | 100% | 100% | 100% | 0% | 49% | 3.48 / 3.06 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 128 | before_query | 512 | 100% | 83% | 75% | 90% | 95% | 97% | — | — | 98% | 82% | 83% | 17% | 50% | 3.22 / 2.79 | n n – Y (Y) | inconclusive |
| `prot_success_43_43` | 256 | after_write | 511 | 100% | 58% | 58% | 96% | 97% | 100% | 95% | 80% | 100% | 96% | 95% | 1% | 54% | 1.43 / 1.21 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 256 | mid_continuation | 511 | 100% | 54% | 53% | 94% | 96% | 100% | 94% | 82% | 99% | 99% | 99% | 1% | 50% | 3.36 / 3.20 | Y Y Y Y (Y) | supported |
| `prot_success_43_43` | 256 | before_query | 511 | 100% | 81% | 75% | 90% | 95% | 95% | — | — | 97% | 76% | 81% | 19% | 50% | 3.20 / 2.93 | n n – n (Y) | inconclusive |
| `fixed005_success_43_43` | 64 | after_write | 512 | 100% | 100% | 100% | 96% | 100% | 53% | 100% | 100% | 100% | 0% | 0% | 99% | 54% | 1.00 / 1.69 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 64 | mid_continuation | 512 | 100% | 100% | 100% | 94% | 100% | 51% | 100% | 100% | 100% | 0% | 0% | 100% | 50% | 1.07 / 2.49 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 64 | before_query | 512 | 100% | 100% | 100% | 93% | 100% | 53% | — | — | 100% | 0% | 0% | 100% | 50% | 1.14 / 2.30 | n n – n (n) | contradicted |
| `fixed005_success_43_43` | 128 | after_write | 512 | 100% | 100% | 100% | 97% | 100% | 54% | 100% | 100% | 100% | 0% | 0% | 100% | 54% | 1.00 / 1.32 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 128 | mid_continuation | 512 | 100% | 100% | 100% | 93% | 100% | 52% | 100% | 100% | 100% | 0% | 0% | 100% | 50% | 1.25 / 2.53 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 128 | before_query | 512 | 100% | 100% | 100% | 90% | 100% | 53% | — | — | 100% | 0% | 0% | 100% | 50% | 1.32 / 2.42 | n n – n (n) | contradicted |
| `fixed005_success_43_43` | 256 | after_write | 498 | 97% | 100% | 100% | 93% | 99% | 54% | 100% | 100% | 100% | 0% | 0% | 97% | 53% | 1.03 / 1.38 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 256 | mid_continuation | 498 | 97% | 100% | 100% | 85% | 99% | 50% | 100% | 100% | 100% | 0% | 0% | 100% | 51% | 1.45 / 2.62 | n n Y n (n) | contradicted |
| `fixed005_success_43_43` | 256 | before_query | 498 | 97% | 100% | 99% | 83% | 98% | 53% | — | — | 99% | 1% | 0% | 100% | 51% | 1.58 / 2.59 | n n – n (n) | contradicted |
| `gru32_success_43_43` | 64 | after_write | 512 | 100% | 100% | 100% | 99% | 100% | 88% | 100% | 100% | 100% | 3% | 1% | 99% | 54% | 2.23 / 2.39 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 64 | mid_continuation | 512 | 100% | 100% | 100% | 96% | 100% | 85% | 100% | 100% | 100% | 3% | 0% | 100% | 52% | 3.93 / 4.93 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 64 | before_query | 512 | 100% | 100% | 100% | 98% | 100% | 80% | — | — | 100% | 2% | 0% | 100% | 50% | 3.47 / 3.30 | n n – n (n) | contradicted |
| `gru32_success_43_43` | 128 | after_write | 512 | 100% | 100% | 100% | 98% | 100% | 81% | 100% | 100% | 100% | 3% | 1% | 98% | 52% | 1.44 / 1.56 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 128 | mid_continuation | 512 | 100% | 100% | 100% | 97% | 99% | 83% | 100% | 100% | 100% | 4% | 1% | 99% | 50% | 3.87 / 4.90 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 128 | before_query | 512 | 100% | 100% | 100% | 98% | 99% | 81% | — | — | 100% | 3% | 1% | 99% | 50% | 3.42 / 3.78 | n n – n (n) | contradicted |
| `gru32_success_43_43` | 256 | after_write | 512 | 100% | 99% | 99% | 95% | 99% | 76% | 100% | 100% | 100% | 6% | 6% | 94% | 51% | 1.56 / 1.62 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 256 | mid_continuation | 512 | 100% | 99% | 98% | 94% | 98% | 81% | 99% | 100% | 99% | 8% | 6% | 94% | 50% | 3.70 / 4.36 | n n Y n (n) | contradicted |
| `gru32_success_43_43` | 256 | before_query | 512 | 100% | 98% | 100% | 94% | 98% | 82% | — | — | 98% | 6% | 3% | 97% | 50% | 3.40 / 3.89 | n n – n (n) | contradicted |
| `prot_failed_17_17` | 64 | after_write | 368 | 72% | 89% | 75% | 93% | 95% | 89% | 99% | 89% | 93% | 30% | 31% | 55% | 77% | 1.49 / 1.74 | n n Y n (n) | inconclusive |
| `prot_failed_17_17` | 64 | mid_continuation | 368 | 72% | 84% | 66% | 92% | 95% | 86% | 99% | 85% | 86% | 36% | 40% | 60% | 57% | 1.61 / 1.97 | n n Y n (n) | inconclusive |
| `prot_failed_17_17` | 64 | before_query | 368 | 72% | 88% | 58% | 96% | 95% | 90% | — | — | 87% | 33% | 39% | 60% | 50% | 1.42 / 1.78 | n n – n (Y) | inconclusive |
| `prot_failed_17_17` | 128 | after_write | 335 | 65% | 88% | 81% | 93% | 97% | 93% | 99% | 89% | 92% | 22% | 33% | 47% | 73% | 1.27 / 1.43 | n n Y n (Y) | inconclusive |
| `prot_failed_17_17` | 128 | mid_continuation | 335 | 65% | 83% | 70% | 92% | 95% | 89% | 99% | 84% | 86% | 32% | 48% | 52% | 63% | 1.73 / 2.29 | n n Y n (n) | inconclusive |
| `prot_failed_17_17` | 128 | before_query | 335 | 65% | 85% | 59% | 95% | 94% | 93% | — | — | 83% | 33% | 46% | 54% | 54% | 1.49 / 1.93 | n n – n (Y) | inconclusive |
| `prot_failed_17_17` | 256 | after_write | 357 | 70% | 89% | 78% | 91% | 95% | 87% | 97% | 90% | 92% | 25% | 36% | 59% | 71% | 1.36 / 1.46 | n n Y n (n) | inconclusive |
| `prot_failed_17_17` | 256 | mid_continuation | 357 | 70% | 86% | 68% | 91% | 94% | 88% | 98% | 88% | 89% | 31% | 38% | 62% | 61% | 1.65 / 2.20 | n n Y n (n) | inconclusive |
| `prot_failed_17_17` | 256 | before_query | 357 | 70% | 89% | 58% | 93% | 94% | 90% | — | — | 88% | 32% | 39% | 61% | 54% | 1.44 / 1.98 | n n – n (n) | inconclusive |
| `prot_partial_43_17` | 64 | after_write | 451 | 88% | 84% | 78% | 96% | 96% | 90% | 99% | 87% | 95% | 53% | 62% | 37% | 57% | 1.77 / 1.70 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 64 | mid_continuation | 451 | 88% | 85% | 77% | 97% | 97% | 88% | 99% | 87% | 94% | 57% | 62% | 38% | 51% | 2.45 / 2.48 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 64 | before_query | 451 | 88% | 80% | 74% | 96% | 96% | 85% | — | — | 93% | 57% | 60% | 40% | 50% | 2.28 / 2.37 | n n – n (n) | inconclusive |
| `prot_partial_43_17` | 128 | after_write | 444 | 87% | 84% | 80% | 95% | 96% | 90% | 98% | 88% | 96% | 50% | 61% | 39% | 59% | 1.43 / 1.35 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 128 | mid_continuation | 444 | 87% | 85% | 75% | 96% | 96% | 89% | 99% | 87% | 91% | 54% | 61% | 39% | 52% | 2.65 / 2.74 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 128 | before_query | 444 | 87% | 84% | 76% | 94% | 95% | 86% | — | — | 93% | 55% | 60% | 41% | 51% | 2.40 / 2.57 | n n – n (n) | inconclusive |
| `prot_partial_43_17` | 256 | after_write | 456 | 89% | 86% | 78% | 96% | 96% | 87% | 98% | 88% | 96% | 51% | 62% | 38% | 56% | 1.47 / 1.41 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 256 | mid_continuation | 456 | 89% | 82% | 73% | 97% | 96% | 88% | 99% | 86% | 95% | 53% | 62% | 38% | 52% | 2.64 / 2.79 | n n Y n (n) | inconclusive |
| `prot_partial_43_17` | 256 | before_query | 456 | 89% | 78% | 74% | 95% | 94% | 85% | — | — | 92% | 51% | 61% | 39% | 51% | 2.50 / 2.67 | n n – n (n) | inconclusive |
