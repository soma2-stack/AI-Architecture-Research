# Experiment 014 — generated tables

Late cut = state read at `max(write+1, T-8)`; early cut = right after the differing write. Eligible = changed-slot prediction correct on both original histories. Switch = changed-slot prediction after the transplant equals the donor's correct value. `prot`/`fast` = protected-subspace / fast-complement transplant (for the GRU: arbitrary Walsh-8 / its complement, **no protected role**). R8/R24 = random 8-d / 24-d controls (min–max over 8 bases).

## Validity gates

| model | archive reproduced exactly | stepper vs forward (max logit gap) | chunked vs uninterrupted | sham gap (max) | pairs valid |
|---|---|---:|---:|---:|---|
| `prot_success_43_29` | True | 7.2e-06 | 4.8e-06 | 1.8e-05 | True |
| `prot_success_43_43` | True | 6.0e-06 | 1.1e-06 | 5.6e-06 | True |
| `fixed005_success_43_43` | True | 1.0e-05 | 1.4e-06 | 6.6e-06 | True |
| `prot_partial_43_17` | True | 1.9e-06 | 1.9e-06 | 7.2e-06 | True |
| `prot_partial_29_29` | True | 8.9e-07 | 1.4e-06 | 6.7e-06 | True |
| `prot_failed_17_17` | True | 1.2e-06 | 4.2e-07 | 2.6e-06 | True |
| `gru32_success_43_43` | True | 4.8e-07 | 9.5e-07 | 1.4e-06 | True |

Sham deviation: the preregistered bound was 1e-5; `sham_check.json` shows the sham equals a clean run on the same batch exactly (gap 0.0) with identical predictions, and the larger gap is float32 batch-size rounding against the split-batch reference.

## Eligible fraction (changed slot correct on both original histories)

| model | role | 64 | 128 | 256 | changed-slot accuracy @64 |
|---|---|---:|---:|---:|---:|
| `prot_success_43_29` | successful learned-gate protected RNN | 100% | 100% | 97% | 100% |
| `prot_success_43_43` | successful learned-gate protected RNN (replicate) | 100% | 100% | 100% | 100% |
| `fixed005_success_43_43` | successful fixed-0.005-gate protected RNN | 100% | 100% | 95% | 100% |
| `prot_partial_43_17` | partially trained protected RNN (wv@64 42.9%) | 75% | 74% | 76% | 87% |
| `prot_partial_29_29` | partially trained protected RNN (wv@64 12.4%) | 63% | 55% | 57% | 81% |
| `prot_failed_17_17` | failed (plateau) protected RNN | 40% | 36% | 33% | 70% |
| `gru32_success_43_43` | successful GRU-32 (ordinary recurrence), reproduced | 100% | 100% | 100% | 100% |

## Late cut (primary), both layers: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 100% | 100% (100%) | 0% (100%) | 2%–32% | 68%–98% | 13% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 128 | 512 | 100% | 99% (100%) | 1% (100%) | 4%–30% | 70%–96% | 11% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 256 | 498 | 100% | 90% (98%) | 10% (99%) | 15%–31% | 69%–85% | 16% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 64 | 512 | 100% | 99% (100%) | 1% (100%) | 4%–28% | 72%–96% | 11% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 128 | 512 | 100% | 99% (100%) | 1% (100%) | 4%–25% | 75%–96% | 15% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 256 | 510 | 100% | 99% (100%) | 1% (100%) | 7%–30% | 70%–93% | 15% | protected coefficients carry usable memory (localized) |
| `fixed005_success_43_43` | 64 | 510 | 100% | 0% (100%) | 100% (100%) | 5%–15% | 85%–95% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 128 | 512 | 100% | 0% (100%) | 100% (100%) | 4%–16% | 84%–96% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 256 | 488 | 100% | 0% (99%) | 100% (97%) | 8%–27% | 73%–92% | 0% | distributed / ambiguous |
| `prot_partial_43_17` | 64 | 382 | 100% | 61% (88%) | 39% (96%) | 4%–22% | 78%–96% | 7% | distributed / ambiguous |
| `prot_partial_43_17` | 128 | 380 | 100% | 59% (88%) | 41% (95%) | 7%–23% | 77%–93% | 6% | distributed / ambiguous |
| `prot_partial_43_17` | 256 | 390 | 100% | 62% (90%) | 38% (97%) | 6%–23% | 77%–94% | 10% | distributed / ambiguous |
| `prot_partial_29_29` | 64 | 322 | 100% | 56% (89%) | 44% (70%) | 10%–31% | 69%–90% | 7% | distributed / ambiguous |
| `prot_partial_29_29` | 128 | 284 | 100% | 60% (87%) | 40% (70%) | 10%–35% | 65%–90% | 7% | distributed / ambiguous |
| `prot_partial_29_29` | 256 | 290 | 100% | 55% (90%) | 45% (66%) | 8%–31% | 69%–92% | 6% | distributed / ambiguous |
| `prot_failed_17_17` | 64 | 206 | 100% | 51% (49%) | 49% (53%) | 9%–36% | 64%–91% | 6% | distributed / ambiguous |
| `prot_failed_17_17` | 128 | 182 | 100% | 46% (55%) | 54% (47%) | 10%–38% | 62%–90% | 8% | distributed / ambiguous |
| `prot_failed_17_17` | 256 | 170 | 100% | 45% (58%) | 55% (47%) | 16%–43% | 57%–84% | 10% | distributed / ambiguous |
| `gru32_success_43_43` | 64 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–15% | 85%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 128 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–16% | 84%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 256 | 510 | 100% | 4% (99%) | 96% (98%) | 1%–20% | 80%–99% | 1% | distributed / ambiguous |

## Late cut (primary), layer 0 only: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_29` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_29` | 256 | 498 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 256 | 510 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 64 | 510 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–1% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 256 | 488 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 64 | 382 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 128 | 380 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 256 | 390 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 64 | 322 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 128 | 284 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 256 | 290 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_failed_17_17` | 64 | 206 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_failed_17_17` | 128 | 182 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–1% | 0% | evidence insufficient to localize |
| `prot_failed_17_17` | 256 | 170 | 1% | 0% (100%) | 1% (100%) | 0%–1% | 1%–1% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 256 | 510 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |

## Late cut (primary), layer 1 only: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 100% | 100% (100%) | 0% (100%) | 2%–32% | 68%–98% | 11% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 128 | 512 | 100% | 99% (100%) | 0% (100%) | 4%–30% | 70%–96% | 12% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 256 | 498 | 100% | 90% (98%) | 10% (99%) | 15%–31% | 68%–85% | 13% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 64 | 512 | 100% | 99% (100%) | 1% (100%) | 4%–28% | 72%–96% | 12% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 128 | 512 | 100% | 99% (100%) | 1% (100%) | 4%–25% | 75%–96% | 12% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 256 | 510 | 100% | 99% (100%) | 1% (100%) | 7%–30% | 70%–93% | 14% | protected coefficients carry usable memory (localized) |
| `fixed005_success_43_43` | 64 | 510 | 100% | 0% (100%) | 100% (100%) | 5%–14% | 85%–95% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 128 | 512 | 100% | 0% (100%) | 100% (100%) | 4%–16% | 83%–96% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 256 | 488 | 100% | 0% (99%) | 100% (97%) | 7%–27% | 73%–92% | 1% | distributed / ambiguous |
| `prot_partial_43_17` | 64 | 382 | 100% | 61% (88%) | 39% (96%) | 4%–23% | 78%–96% | 9% | distributed / ambiguous |
| `prot_partial_43_17` | 128 | 380 | 100% | 59% (88%) | 41% (95%) | 7%–23% | 78%–93% | 7% | distributed / ambiguous |
| `prot_partial_43_17` | 256 | 390 | 100% | 62% (90%) | 38% (97%) | 6%–23% | 77%–94% | 9% | distributed / ambiguous |
| `prot_partial_29_29` | 64 | 322 | 100% | 56% (88%) | 44% (70%) | 10%–31% | 69%–89% | 10% | distributed / ambiguous |
| `prot_partial_29_29` | 128 | 284 | 100% | 60% (87%) | 40% (71%) | 10%–36% | 65%–89% | 10% | distributed / ambiguous |
| `prot_partial_29_29` | 256 | 290 | 100% | 55% (89%) | 45% (66%) | 8%–31% | 69%–92% | 8% | distributed / ambiguous |
| `prot_failed_17_17` | 64 | 206 | 100% | 51% (49%) | 49% (54%) | 9%–36% | 64%–91% | 9% | distributed / ambiguous |
| `prot_failed_17_17` | 128 | 182 | 100% | 46% (55%) | 53% (48%) | 10%–38% | 61%–90% | 7% | distributed / ambiguous |
| `prot_failed_17_17` | 256 | 170 | 99% | 45% (58%) | 55% (47%) | 16%–43% | 57%–84% | 9% | distributed / ambiguous |
| `gru32_success_43_43` | 64 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–15% | 85%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 128 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–16% | 84%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 256 | 510 | 100% | 4% (99%) | 96% (98%) | 1%–20% | 80%–99% | 1% | distributed / ambiguous |

## Early cut (persistence), both layers: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 100% | 100% (100%) | 0% (100%) | 2%–27% | 73%–98% | 12% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 128 | 512 | 100% | 100% (100%) | 0% (100%) | 3%–25% | 75%–97% | 10% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 256 | 498 | 100% | 93% (98%) | 7% (99%) | 13%–26% | 74%–87% | 13% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 64 | 512 | 100% | 97% (100%) | 3% (100%) | 2%–20% | 80%–98% | 8% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 128 | 512 | 100% | 98% (100%) | 2% (100%) | 2%–19% | 81%–98% | 12% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 256 | 510 | 100% | 96% (100%) | 4% (100%) | 4%–22% | 78%–96% | 12% | protected coefficients carry usable memory (localized) |
| `fixed005_success_43_43` | 64 | 510 | 100% | 0% (100%) | 100% (100%) | 3%–15% | 85%–97% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 128 | 512 | 100% | 0% (100%) | 100% (100%) | 3%–14% | 86%–97% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 256 | 488 | 100% | 0% (100%) | 100% (97%) | 10%–20% | 80%–90% | 0% | distributed / ambiguous |
| `prot_partial_43_17` | 64 | 382 | 100% | 61% (89%) | 39% (96%) | 5%–24% | 76%–95% | 6% | distributed / ambiguous |
| `prot_partial_43_17` | 128 | 380 | 100% | 60% (89%) | 40% (96%) | 5%–26% | 74%–95% | 6% | distributed / ambiguous |
| `prot_partial_43_17` | 256 | 390 | 100% | 61% (90%) | 39% (96%) | 7%–32% | 68%–93% | 10% | distributed / ambiguous |
| `prot_partial_29_29` | 64 | 322 | 100% | 54% (90%) | 46% (70%) | 1%–45% | 55%–99% | 5% | distributed / ambiguous |
| `prot_partial_29_29` | 128 | 284 | 100% | 56% (90%) | 44% (68%) | 1%–47% | 53%–99% | 8% | distributed / ambiguous |
| `prot_partial_29_29` | 256 | 290 | 100% | 55% (91%) | 45% (70%) | 1%–44% | 56%–99% | 6% | distributed / ambiguous |
| `prot_failed_17_17` | 64 | 206 | 100% | 38% (62%) | 62% (41%) | 1%–32% | 68%–99% | 7% | distributed / ambiguous |
| `prot_failed_17_17` | 128 | 182 | 100% | 34% (66%) | 66% (37%) | 6%–30% | 70%–94% | 8% | distributed / ambiguous |
| `prot_failed_17_17` | 256 | 170 | 100% | 36% (67%) | 64% (39%) | 10%–39% | 61%–90% | 12% | distributed / ambiguous |
| `gru32_success_43_43` | 64 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–8% | 92%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 128 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–11% | 89%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 256 | 510 | 100% | 6% (99%) | 94% (99%) | 3%–17% | 83%–97% | 1% | distributed / ambiguous |

## Early cut (persistence), layer 0 only: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_29` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `prot_success_43_29` | 256 | 498 | 0% | 0% (100%) | 0% (100%) | 0%–2% | 0%–5% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–1% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–1% | 0%–1% | 0% | evidence insufficient to localize |
| `prot_success_43_43` | 256 | 510 | 1% | 0% (100%) | 1% (100%) | 0%–3% | 0%–4% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 64 | 510 | 1% | 0% (100%) | 1% (100%) | 0%–0% | 0%–5% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 128 | 512 | 1% | 0% (100%) | 1% (100%) | 0%–1% | 0%–5% | 0% | evidence insufficient to localize |
| `fixed005_success_43_43` | 256 | 488 | 2% | 0% (100%) | 2% (100%) | 0%–3% | 1%–8% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 64 | 382 | 1% | 0% (100%) | 1% (98%) | 0%–1% | 0%–1% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 128 | 380 | 1% | 0% (100%) | 1% (99%) | 0%–2% | 1%–3% | 0% | evidence insufficient to localize |
| `prot_partial_43_17` | 256 | 390 | 1% | 0% (100%) | 1% (100%) | 0%–1% | 1%–1% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 64 | 322 | 5% | 1% (99%) | 3% (98%) | 1%–2% | 2%–4% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 128 | 284 | 6% | 1% (99%) | 4% (94%) | 0%–3% | 1%–4% | 0% | evidence insufficient to localize |
| `prot_partial_29_29` | 256 | 290 | 3% | 0% (100%) | 2% (99%) | 0%–1% | 1%–3% | 0% | evidence insufficient to localize |
| `prot_failed_17_17` | 64 | 206 | 14% | 0% (100%) | 13% (88%) | 0%–6% | 2%–14% | 0% | evidence insufficient to localize |
| `prot_failed_17_17` | 128 | 182 | 13% | 2% (99%) | 12% (90%) | 1%–8% | 3%–15% | 1% | evidence insufficient to localize |
| `prot_failed_17_17` | 256 | 170 | 16% | 0% (99%) | 16% (89%) | 1%–9% | 5%–17% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 64 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 128 | 512 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |
| `gru32_success_43_43` | 256 | 510 | 0% | 0% (100%) | 0% (100%) | 0%–0% | 0%–0% | 0% | evidence insufficient to localize |

## Early cut (persistence), layer 1 only: switch rate toward the donor's value (eligible pairs), unchanged-slot agreement in parentheses

| model | delay | n elig | full | prot / Walsh8 | fast / Walsh-comp24 | R8 min–max | R24 min–max | noise (norm-matched) | category |
|---|---:|---:|---:|---|---|---|---|---:|---|
| `prot_success_43_29` | 64 | 512 | 100% | 100% (100%) | 0% (100%) | 2%–24% | 74%–96% | 9% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 128 | 512 | 100% | 100% (100%) | 0% (100%) | 3%–24% | 74%–96% | 10% | protected coefficients carry usable memory (localized) |
| `prot_success_43_29` | 256 | 498 | 100% | 93% (98%) | 6% (99%) | 13%–25% | 73%–85% | 13% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 64 | 512 | 100% | 97% (100%) | 1% (100%) | 2%–16% | 79%–97% | 11% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 128 | 512 | 100% | 98% (100%) | 0% (100%) | 1%–15% | 80%–98% | 9% | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | 256 | 510 | 99% | 96% (100%) | 1% (100%) | 3%–18% | 78%–95% | 9% | protected coefficients carry usable memory (localized) |
| `fixed005_success_43_43` | 64 | 510 | 99% | 0% (100%) | 99% (100%) | 5%–15% | 81%–92% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 128 | 512 | 99% | 0% (100%) | 99% (100%) | 4%–14% | 83%–92% | 0% | distributed / ambiguous |
| `fixed005_success_43_43` | 256 | 488 | 98% | 0% (100%) | 98% (97%) | 8%–22% | 74%–88% | 0% | distributed / ambiguous |
| `prot_partial_43_17` | 64 | 382 | 99% | 61% (89%) | 38% (96%) | 5%–24% | 73%–94% | 8% | distributed / ambiguous |
| `prot_partial_43_17` | 128 | 380 | 99% | 60% (89%) | 39% (97%) | 6%–28% | 70%–93% | 6% | distributed / ambiguous |
| `prot_partial_43_17` | 256 | 390 | 99% | 61% (90%) | 39% (97%) | 6%–32% | 65%–93% | 9% | distributed / ambiguous |
| `prot_partial_29_29` | 64 | 322 | 95% | 52% (91%) | 41% (73%) | 0%–45% | 46%–94% | 9% | distributed / ambiguous |
| `prot_partial_29_29` | 128 | 284 | 94% | 56% (90%) | 38% (74%) | 0%–47% | 46%–95% | 8% | distributed / ambiguous |
| `prot_partial_29_29` | 256 | 290 | 97% | 55% (92%) | 41% (72%) | 0%–43% | 49%–96% | 8% | distributed / ambiguous |
| `prot_failed_17_17` | 64 | 206 | 86% | 36% (63%) | 46% (58%) | 0%–27% | 57%–83% | 9% | distributed / ambiguous |
| `prot_failed_17_17` | 128 | 182 | 87% | 32% (68%) | 49% (53%) | 3%–24% | 57%–86% | 9% | distributed / ambiguous |
| `prot_failed_17_17` | 256 | 170 | 84% | 36% (67%) | 51% (50%) | 2%–35% | 52%–85% | 7% | distributed / ambiguous |
| `gru32_success_43_43` | 64 | 512 | 100% | 1% (100%) | 99% (100%) | 0%–7% | 90%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 128 | 512 | 100% | 1% (100%) | 98% (100%) | 0%–11% | 87%–100% | 0% | distributed / ambiguous |
| `gru32_success_43_43` | 256 | 510 | 100% | 5% (99%) | 94% (99%) | 3%–17% | 83%–97% | 0% | distributed / ambiguous |

## Model-level category (late cut; same category required at all three delays)

| model | both layers | layer 0 | layer 1 |
|---|---|---|---|
| `prot_success_43_29` | protected coefficients carry usable memory (localized) | evidence insufficient to localize | protected coefficients carry usable memory (localized) |
| `prot_success_43_43` | protected coefficients carry usable memory (localized) | evidence insufficient to localize | protected coefficients carry usable memory (localized) |
| `fixed005_success_43_43` | distributed / ambiguous | evidence insufficient to localize | distributed / ambiguous |
| `prot_partial_43_17` | distributed / ambiguous | evidence insufficient to localize | distributed / ambiguous |
| `prot_partial_29_29` | distributed / ambiguous | evidence insufficient to localize | distributed / ambiguous |
| `prot_failed_17_17` | distributed / ambiguous | evidence insufficient to localize | distributed / ambiguous |
| `gru32_success_43_43` | distributed / ambiguous | evidence insufficient to localize | distributed / ambiguous |

Cells where the integrity-first tie-break of overlapping preregistered clauses changed the label: none.

## All pairs (not only eligible), late cut, both layers — nothing hidden

| model | delay | n | full | prot / Walsh8 | fast / Walsh-comp24 | R8 max | R24 max |
|---|---:|---:|---:|---|---|---:|---:|
| `prot_success_43_29` | 64 | 512 | 100% | 100% (100%) | 0% (100%) | 32% | 98% |
| `prot_success_43_29` | 128 | 512 | 100% | 99% (100%) | 1% (100%) | 30% | 96% |
| `prot_success_43_29` | 256 | 512 | 99% | 89% (98%) | 11% (99%) | 32% | 84% |
| `prot_success_43_43` | 64 | 512 | 100% | 99% (100%) | 1% (100%) | 28% | 96% |
| `prot_success_43_43` | 128 | 512 | 100% | 99% (100%) | 1% (100%) | 25% | 96% |
| `prot_success_43_43` | 256 | 512 | 100% | 98% (100%) | 2% (100%) | 30% | 93% |
| `fixed005_success_43_43` | 64 | 512 | 100% | 0% (100%) | 100% (100%) | 15% | 95% |
| `fixed005_success_43_43` | 128 | 512 | 100% | 0% (100%) | 100% (100%) | 16% | 96% |
| `fixed005_success_43_43` | 256 | 512 | 98% | 2% (99%) | 98% (97%) | 28% | 90% |
| `prot_partial_43_17` | 64 | 512 | 87% | 58% (91%) | 42% (97%) | 29% | 84% |
| `prot_partial_43_17` | 128 | 512 | 87% | 57% (91%) | 43% (96%) | 30% | 82% |
| `prot_partial_43_17` | 256 | 512 | 88% | 59% (92%) | 41% (98%) | 29% | 83% |
| `prot_partial_29_29` | 64 | 512 | 81% | 54% (93%) | 46% (81%) | 38% | 75% |
| `prot_partial_29_29` | 128 | 512 | 78% | 55% (93%) | 45% (83%) | 42% | 72% |
| `prot_partial_29_29` | 256 | 512 | 78% | 53% (94%) | 47% (81%) | 39% | 74% |
| `prot_failed_17_17` | 64 | 512 | 70% | 51% (79%) | 49% (81%) | 44% | 67% |
| `prot_failed_17_17` | 128 | 512 | 68% | 49% (84%) | 51% (81%) | 46% | 64% |
| `prot_failed_17_17` | 256 | 512 | 67% | 48% (86%) | 52% (82%) | 48% | 61% |
| `gru32_success_43_43` | 64 | 512 | 100% | 1% (100%) | 99% (100%) | 15% | 100% |
| `gru32_success_43_43` | 128 | 512 | 100% | 1% (100%) | 99% (100%) | 16% | 100% |
| `gru32_success_43_43` | 256 | 512 | 100% | 4% (99%) | 96% (98%) | 20% | 99% |

## Strata (late cut, both layers, eligible): changed write in the initial prefix vs rewritten — switch rate (n)

| model | delay | prot initial | prot rewritten | fast initial | fast rewritten |
|---|---:|---|---|---|---|
| `prot_success_43_29` | 64 | 100% (288) | 100% (224) | 0% (288) | 0% (224) |
| `prot_success_43_29` | 128 | 99% (304) | 100% (208) | 1% (304) | 0% (208) |
| `prot_success_43_29` | 256 | 90% (276) | 89% (222) | 10% (276) | 11% (222) |
| `prot_success_43_43` | 64 | 99% (288) | 98% (224) | 1% (288) | 2% (224) |
| `prot_success_43_43` | 128 | 99% (304) | 100% (208) | 1% (304) | 0% (208) |
| `prot_success_43_43` | 256 | 99% (284) | 99% (226) | 1% (284) | 1% (226) |
| `fixed005_success_43_43` | 64 | 0% (288) | 0% (222) | 100% (288) | 100% (222) |
| `fixed005_success_43_43` | 128 | 0% (304) | 0% (208) | 100% (304) | 100% (208) |
| `fixed005_success_43_43` | 256 | 0% (268) | 0% (220) | 100% (268) | 100% (220) |
| `prot_partial_43_17` | 64 | 61% (220) | 61% (162) | 39% (220) | 39% (162) |
| `prot_partial_43_17` | 128 | 53% (218) | 67% (162) | 47% (218) | 33% (162) |
| `prot_partial_43_17` | 256 | 59% (204) | 64% (186) | 41% (204) | 36% (186) |
| `prot_partial_29_29` | 64 | 66% (164) | 46% (158) | 34% (164) | 54% (158) |
| `prot_partial_29_29` | 128 | 73% (138) | 47% (146) | 27% (138) | 53% (146) |
| `prot_partial_29_29` | 256 | 73% (134) | 40% (156) | 27% (134) | 60% (156) |
| `prot_failed_17_17` | 64 | 71% (104) | 31% (102) | 29% (104) | 69% (102) |
| `prot_failed_17_17` | 128 | 73% (86) | 22% (96) | 27% (86) | 78% (96) |
| `prot_failed_17_17` | 256 | 62% (68) | 33% (102) | 38% (68) | 67% (102) |
| `gru32_success_43_43` | 64 | 0% (288) | 1% (224) | 100% (288) | 99% (224) |
| `gru32_success_43_43` | 128 | 0% (304) | 1% (208) | 100% (304) | 99% (208) |
| `gru32_success_43_43` | 256 | 6% (284) | 2% (226) | 94% (284) | 98% (226) |

## Phase 5: perturbation stability versus memory separation (initial-prefix pairs; ratio = displacement at end / initial displacement, median)

| model | delay | layer | memory ratio | random full-space ratio | random in-subspace ratio | memory ÷ random-full | separation / natural spread | sub-criteria met (≥.25 / ≥10× / ≥.10) | τ median α=.25/.5/.75 | P(predict B) α=.25/.5/.75 | near-endpoint fraction | preregistered label |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| `prot_success_43_29` | 64 | 0 | 0.00299 | 0.0514 | 0.00356 | 0.1x | 0.00779 | n/n/n | 0.25/0.50/0.75 | 0.01/0.47/1.00 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_29` | 64 | 1 | 0.88 | 0.359 | 0.488 | 2.5x | 0.628 | Y/n/Y | 0.25/0.50/0.75 | 0.01/0.47/1.00 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_29` | 128 | 0 | 0.000456 | 0.00861 | 0.000592 | 0.1x | 0.0015 | n/n/n | 0.25/0.50/0.75 | 0.03/0.44/0.98 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_29` | 128 | 1 | 0.786 | 0.328 | 0.393 | 2.4x | 0.619 | Y/n/Y | 0.25/0.50/0.75 | 0.03/0.44/0.98 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_29` | 256 | 0 | 1.64e-05 | 0.000213 | 1.53e-05 | 0.1x | 5.6e-05 | n/n/n | 0.25/0.50/0.75 | 0.18/0.48/0.78 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_29` | 256 | 1 | 0.672 | 0.23 | 0.349 | 2.9x | 0.586 | Y/n/Y | 0.25/0.50/0.75 | 0.18/0.48/0.78 | 0.00/0.00/0.00 | collapsing (separation not preserved) |
| `prot_success_43_43` | 64 | 0 | 0.00417 | 0.0403 | 0.00206 | 0.1x | 0.00938 | n/n/n | 0.23/0.49/0.77 | 0.02/0.53/0.95 | 0.06/0.00/0.04 | collapsing (separation not preserved) |
| `prot_success_43_43` | 64 | 1 | 0.969 | 0.406 | 0.511 | 2.4x | 0.642 | Y/n/Y | 0.23/0.49/0.77 | 0.02/0.53/0.95 | 0.06/0.00/0.04 | collapsing (separation not preserved) |
| `prot_success_43_43` | 128 | 0 | 0.000838 | 0.00745 | 0.000375 | 0.1x | 0.00235 | n/n/n | 0.23/0.51/0.77 | 0.03/0.51/0.97 | 0.05/0.00/0.04 | collapsing (separation not preserved) |
| `prot_success_43_43` | 128 | 1 | 0.939 | 0.3 | 0.444 | 3.1x | 0.671 | Y/n/Y | 0.23/0.51/0.77 | 0.03/0.51/0.97 | 0.05/0.00/0.04 | collapsing (separation not preserved) |
| `prot_success_43_43` | 256 | 0 | 3.51e-05 | 0.00025 | 1.52e-05 | 0.1x | 0.000108 | n/n/n | 0.23/0.50/0.77 | 0.10/0.49/0.94 | 0.05/0.00/0.03 | collapsing (separation not preserved) |
| `prot_success_43_43` | 256 | 1 | 0.801 | 0.27 | 0.336 | 3.0x | 0.668 | Y/n/Y | 0.23/0.50/0.77 | 0.10/0.49/0.94 | 0.05/0.00/0.03 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 64 | 0 | 0.00695 | 0.408 | 0.00446 | 0.0x | 0.0199 | n/n/n | 0.24/0.50/0.76 | 0.06/0.50/0.96 | 0.02/0.00/0.03 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 64 | 1 | 0.787 | 0.646 | 0.0047 | 1.2x | 0.6 | Y/n/Y | 0.24/0.50/0.76 | 0.06/0.50/0.96 | 0.02/0.00/0.03 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 128 | 0 | 0.00534 | 0.325 | 0.00316 | 0.0x | 0.0185 | n/n/n | 0.24/0.50/0.76 | 0.04/0.46/0.93 | 0.04/0.00/0.05 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 128 | 1 | 0.723 | 0.514 | 0.00359 | 1.4x | 0.599 | Y/n/Y | 0.24/0.50/0.76 | 0.04/0.46/0.93 | 0.04/0.00/0.05 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 256 | 0 | 0.00345 | 0.178 | 0.00185 | 0.0x | 0.0129 | n/n/n | 0.23/0.50/0.77 | 0.09/0.43/0.83 | 0.06/0.00/0.01 | collapsing (separation not preserved) |
| `fixed005_success_43_43` | 256 | 1 | 0.656 | 0.376 | 0.00237 | 1.7x | 0.488 | Y/n/Y | 0.23/0.50/0.77 | 0.09/0.43/0.83 | 0.06/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 64 | 0 | 0.00679 | 0.0486 | 0.00326 | 0.1x | 0.0154 | n/n/n | 0.24/0.50/0.75 | 0.17/0.50/0.77 | 0.00/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 64 | 1 | 0.832 | 0.302 | 0.224 | 2.8x | 0.547 | Y/n/Y | 0.24/0.50/0.75 | 0.17/0.50/0.77 | 0.00/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 128 | 0 | 0.00142 | 0.00896 | 0.000574 | 0.2x | 0.00371 | n/n/n | 0.24/0.50/0.76 | 0.26/0.58/0.79 | 0.02/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 128 | 1 | 0.768 | 0.254 | 0.181 | 3.0x | 0.592 | Y/n/Y | 0.24/0.50/0.76 | 0.26/0.58/0.79 | 0.02/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 256 | 0 | 6.71e-05 | 0.000356 | 2.36e-05 | 0.2x | 0.000188 | n/n/n | 0.24/0.50/0.76 | 0.24/0.52/0.81 | 0.03/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_43_17` | 256 | 1 | 0.801 | 0.22 | 0.162 | 3.6x | 0.665 | Y/n/Y | 0.24/0.50/0.76 | 0.24/0.52/0.81 | 0.03/0.00/0.01 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 64 | 0 | 0.00643 | 0.0416 | 0.00653 | 0.2x | 0.0158 | n/n/n | 0.24/0.50/0.76 | 0.29/0.56/0.69 | 0.15/0.00/0.10 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 64 | 1 | 0.491 | 0.311 | 0.302 | 1.6x | 0.324 | Y/n/Y | 0.24/0.50/0.76 | 0.29/0.56/0.69 | 0.15/0.00/0.10 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 128 | 0 | 0.000573 | 0.00501 | 0.000959 | 0.1x | 0.00148 | n/n/n | 0.24/0.51/0.77 | 0.34/0.51/0.70 | 0.17/0.00/0.20 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 128 | 1 | 0.439 | 0.241 | 0.23 | 1.8x | 0.352 | Y/n/Y | 0.24/0.51/0.77 | 0.34/0.51/0.70 | 0.17/0.00/0.20 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 256 | 0 | 7.43e-06 | 4.35e-05 | 7.56e-06 | 0.2x | 1.96e-05 | n/n/n | 0.23/0.49/0.75 | 0.35/0.49/0.66 | 0.22/0.00/0.15 | collapsing (separation not preserved) |
| `prot_partial_29_29` | 256 | 1 | 0.406 | 0.19 | 0.2 | 2.1x | 0.373 | Y/n/Y | 0.23/0.49/0.75 | 0.35/0.49/0.66 | 0.22/0.00/0.15 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 64 | 0 | 0.0027 | 0.0342 | 0.00332 | 0.1x | 0.0054 | n/n/n | 0.24/0.50/0.77 | 0.37/0.48/0.57 | 0.07/0.00/0.14 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 64 | 1 | 0.302 | 0.191 | 0.122 | 1.6x | 0.485 | Y/n/Y | 0.24/0.50/0.77 | 0.37/0.48/0.57 | 0.07/0.00/0.14 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 128 | 0 | 0.000177 | 0.0024 | 0.000253 | 0.1x | 0.000381 | n/n/n | 0.22/0.49/0.77 | 0.45/0.55/0.62 | 0.10/0.00/0.05 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 128 | 1 | 0.263 | 0.131 | 0.0963 | 2.0x | 0.496 | Y/n/Y | 0.22/0.49/0.77 | 0.45/0.55/0.62 | 0.10/0.00/0.05 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 256 | 0 | 7.03e-07 | 1.41e-05 | 1.59e-06 | 0.0x | 1.56e-06 | n/n/n | 0.23/0.50/0.77 | 0.46/0.50/0.56 | 0.08/0.00/0.10 | collapsing (separation not preserved) |
| `prot_failed_17_17` | 256 | 1 | 0.216 | 0.105 | 0.0816 | 2.1x | 0.449 | n/n/Y | 0.23/0.50/0.77 | 0.46/0.50/0.56 | 0.08/0.00/0.10 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 64 | 0 | 1.12e-07 | 7.15e-08 | 4.86e-08 | 1.6x | 2.38e-07 | n/n/n | 0.25/0.50/0.76 | 0.00/0.49/1.00 | 0.01/0.00/0.01 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 64 | 1 | 1.05 | 0.36 | 0.16 | 2.9x | 0.636 | Y/n/Y | 0.25/0.50/0.76 | 0.00/0.49/1.00 | 0.01/0.00/0.01 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 128 | 0 | 0 | 0 | 0 | 0.0x | 0 | n/n/n | 0.24/0.50/0.76 | 0.00/0.47/1.00 | 0.03/0.00/0.03 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 128 | 1 | 1.03 | 0.305 | 0.131 | 3.4x | 0.619 | Y/n/Y | 0.24/0.50/0.76 | 0.00/0.47/1.00 | 0.03/0.00/0.03 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 256 | 0 | 0 | 0 | 0 | 0.0x | 0 | n/n/n | 0.25/0.51/0.76 | 0.08/0.55/0.91 | 0.02/0.00/0.06 | collapsing (separation not preserved) |
| `gru32_success_43_43` | 256 | 1 | 0.876 | 0.256 | 0.116 | 3.4x | 0.587 | Y/n/Y | 0.25/0.51/0.76 | 0.08/0.55/0.91 | 0.02/0.00/0.06 | collapsing (separation not preserved) |
