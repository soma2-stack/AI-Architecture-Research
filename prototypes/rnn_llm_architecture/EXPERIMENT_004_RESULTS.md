# Experiment 004 — dual-query supervision of independent memory slots

**Status:** COMPLETE; 27/27 runs recorded, 0 incomplete/skipped, 271.8s experiment runtime.

**Scope:** Two-slot supervised synthetic benchmark only; NOT an exact robust credit-D theorem or evidence of natural-language understanding.

## Primary outcomes

- The original protected RNN achieved **51.7%** both-slot exact accuracy at training delay 64, only approximately the naive **50%** last-value shortcut, and just **3.3%** both correct on A≠B. The updated-slot answer was **89.0%**, while untouched-slot answer was **61.5%** (three-seed means): learning to output the latest overwritten value is **not** learning two independent memory slots.
- Random orthonormal basis scored **50.8%** paired and no-projection **51.2%**, again challenging Walsh/projection specificity. Ordinary GRU/LSTM controls stayed near **25% random paired accuracy** after this schedule.
- At frozen test delay 256, original protected paired accuracy fell to **27.8%**; random basis **33.1%**; no projection **35.4%**. Successful two-slot selective memory and length transfer remain **NOT ESTABLISHED**.
- Training objective now explicitly supervised A+B together, so the result is stronger negative evidence than Experiment 002's single-query training, but the 240-update budget and unchanged LR can still be insufficient. There is no evidence that the architectures are fundamentally incapable of the task.

**Mechanistic lead:** the current protected candidate uses an input-only slow-write gate. It cannot directly condition the *write-gate decision* on the recurrent state that knows which slot was last requested. A state-conditioned gate analogous to a GRU-style update gate is a sensible next controlled architectural variant, not an established new primitive.

## Protocol

- 9 variants × 3 seeds; 240 optimizer updates at delay 64, AdamW LR 0.002, 16 distinct histories/batch cloned for both final queries.
- Frozen weights at test delays [64, 128, 256], 512 held-out history pairs per delay/seed; per-seed examples shared across architectures and both query branches.
- A and B each receive cross-entropy supervision on identical prefixes; no oracle protected write masks.
- **Naive last-value rule:** approximately 50% exact two-slot accuracy, **0%** exact on A≠B histories; do not use overall one-query accuracy as evidence.
- Original Experiment 002 used a single random query per source history and only 150 updates. A cross-experiment improvement cannot be attributed solely to dual supervision because training length also differs.

## Exact same-prefix both-slot accuracy

Mean (each seed separately in parentheses). Not all evaluated pairs have differing target values.

| Variant | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 24.5% (27.0%/24.2%/22.5%) | 26.9% (27.3%/26.8%/26.6%) | 25.1% (26.4%/25.6%/23.2%) |
| near_critical_w32 | 25.5% (25.6%/25.2%/25.6%) | 26.8% (28.7%/25.6%/26.2%) | 25.7% (26.4%/26.8%/23.8%) |
| protected_w32 | 51.7% (55.7%/51.4%/48.0%) | 29.5% (26.4%/28.1%/34.0%) | 27.8% (24.0%/25.6%/33.8%) |
| gru_w32 | 25.5% (27.0%/24.2%/25.2%) | 25.7% (27.3%/26.8%/22.9%) | 24.8% (26.4%/25.6%/22.5%) |
| lstm_w32 | 25.3% (27.0%/24.2%/24.6%) | 26.4% (27.3%/26.8%/25.2%) | 24.5% (26.4%/25.6%/21.7%) |
| gru_w24 | 25.8% (27.0%/24.2%/26.4%) | 25.6% (27.3%/26.8%/22.7%) | 25.3% (26.4%/25.6%/23.8%) |
| lstm_w20 | 24.9% (27.0%/24.2%/23.4%) | 26.6% (27.3%/26.8%/25.6%) | 25.0% (26.4%/25.6%/23.0%) |
| protected_random_w32 | 50.8% (51.6%/51.8%/49.2%) | 31.8% (29.1%/38.1%/28.1%) | 33.1% (42.6%/30.5%/26.4%) |
| protected_no_project_w32 | 51.2% (54.1%/51.8%/47.7%) | 43.1% (49.6%/35.4%/44.3%) | 35.4% (38.9%/27.0%/40.4%) |

## Diagnostic details at delay 64

| Variant | both on A≠B | updated slot | untouched slot | naive paired shortcut |
|---|---:|---:|---:|---:|
| tanh_w32 | 8.2% (0.0%/0.0%/24.6%) | 49.0% (50.0%/49.4%/47.5%) | 49.1% (52.5%/47.7%/47.1%) | 50.1% (51.4%/51.4%/47.7%) |
| near_critical_w32 | 5.9% (3.6%/2.4%/11.6%) | 49.8% (50.6%/49.6%/49.2%) | 49.6% (49.6%/48.4%/50.8%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_w32 | 3.3% (8.8%/0.4%/0.7%) | 89.0% (93.2%/86.1%/87.7%) | 61.5% (59.8%/65.0%/59.8%) | 50.1% (51.4%/51.4%/47.7%) |
| gru_w32 | 2.7% (0.0%/0.0%/8.2%) | 49.0% (50.0%/49.4%/47.7%) | 50.8% (52.5%/47.7%/52.3%) | 50.1% (51.4%/51.4%/47.7%) |
| lstm_w32 | 14.4% (0.0%/0.0%/43.3%) | 49.3% (50.0%/49.4%/48.4%) | 49.3% (52.5%/47.7%/47.9%) | 50.1% (51.4%/51.4%/47.7%) |
| gru_w24 | 8.3% (0.0%/0.0%/25.0%) | 49.8% (50.0%/49.4%/50.0%) | 50.6% (52.5%/47.7%/51.6%) | 50.1% (51.4%/51.4%/47.7%) |
| lstm_w20 | 14.6% (0.0%/0.0%/43.7%) | 49.2% (50.0%/49.4%/48.0%) | 49.4% (52.5%/47.7%/48.0%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_random_w32 | 1.4% (0.4%/0.8%/3.0%) | 86.7% (87.9%/86.1%/85.9%) | 63.7% (63.7%/65.4%/62.1%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_no_project_w32 | 2.3% (5.6%/0.8%/0.4%) | 88.5% (89.1%/89.3%/87.3%) | 61.6% (62.3%/62.5%/60.0%) | 50.1% (51.4%/51.4%/47.7%) |

## Diagnostic details at delay 128

| Variant | both on A≠B | updated slot | untouched slot | naive paired shortcut |
|---|---:|---:|---:|---:|
| tanh_w32 | 9.3% (0.0%/0.0%/27.9%) | 49.5% (52.1%/49.4%/46.9%) | 52.6% (51.8%/52.1%/53.9%) | 49.6% (50.8%/52.0%/46.1%) |
| near_critical_w32 | 5.3% (4.0%/0.4%/11.6%) | 51.2% (52.9%/49.2%/51.6%) | 51.4% (51.8%/51.6%/51.0%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_w32 | 1.1% (2.0%/0.8%/0.4%) | 52.1% (50.2%/54.9%/51.2%) | 57.8% (53.5%/49.2%/70.7%) | 49.6% (50.8%/52.0%/46.1%) |
| gru_w32 | 2.4% (0.0%/0.0%/7.2%) | 50.7% (52.1%/49.4%/50.6%) | 51.0% (51.8%/52.1%/49.2%) | 49.6% (50.8%/52.0%/46.1%) |
| lstm_w32 | 14.0% (0.0%/0.0%/42.0%) | 49.3% (52.1%/49.4%/46.3%) | 51.4% (51.8%/52.1%/50.4%) | 49.6% (50.8%/52.0%/46.1%) |
| gru_w24 | 6.6% (0.0%/0.0%/19.9%) | 49.5% (52.1%/49.4%/46.9%) | 50.9% (51.8%/52.1%/48.8%) | 49.6% (50.8%/52.0%/46.1%) |
| lstm_w20 | 14.5% (0.0%/0.0%/43.5%) | 49.2% (52.1%/49.4%/45.9%) | 51.7% (51.8%/52.1%/51.2%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_random_w32 | 0.4% (0.8%/0.4%/0.0%) | 50.8% (32.2%/59.2%/61.1%) | 63.4% (75.8%/64.6%/49.8%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_no_project_w32 | 2.7% (5.2%/1.6%/1.4%) | 68.2% (71.3%/62.9%/70.5%) | 67.3% (74.0%/55.9%/71.9%) | 49.6% (50.8%/52.0%/46.1%) |

## Diagnostic details at delay 256

| Variant | both on A≠B | updated slot | untouched slot | naive paired shortcut |
|---|---:|---:|---:|---:|
| tanh_w32 | 8.5% (0.0%/0.0%/25.5%) | 47.4% (50.4%/46.3%/45.5%) | 52.0% (52.0%/53.1%/50.8%) | 51.0% (50.4%/51.8%/51.0%) |
| near_critical_w32 | 6.8% (4.3%/2.0%/13.9%) | 48.1% (50.8%/46.7%/46.9%) | 51.0% (50.8%/53.7%/48.6%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_w32 | 0.0% (0.0%/0.0%/0.0%) | 50.8% (49.6%/46.3%/56.6%) | 54.1% (48.0%/53.1%/61.1%) | 51.0% (50.4%/51.8%/51.0%) |
| gru_w32 | 1.6% (0.0%/0.0%/4.8%) | 48.0% (50.4%/46.3%/47.5%) | 52.0% (52.0%/53.1%/50.8%) | 51.0% (50.4%/51.8%/51.0%) |
| lstm_w32 | 13.9% (0.0%/0.0%/41.8%) | 47.2% (50.4%/46.3%/44.9%) | 51.6% (52.0%/53.1%/49.6%) | 51.0% (50.4%/51.8%/51.0%) |
| gru_w24 | 7.0% (0.0%/0.0%/21.1%) | 48.2% (50.4%/46.3%/48.0%) | 51.9% (52.0%/53.1%/50.6%) | 51.0% (50.4%/51.8%/51.0%) |
| lstm_w20 | 14.7% (0.0%/0.0%/44.2%) | 47.6% (50.4%/46.3%/46.1%) | 51.8% (52.0%/53.1%/50.4%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_random_w32 | 1.1% (2.4%/0.8%/0.0%) | 54.2% (59.4%/50.6%/52.7%) | 60.7% (74.8%/58.2%/49.0%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_no_project_w32 | 2.5% (5.1%/2.4%/0.0%) | 60.1% (63.5%/49.8%/67.0%) | 59.6% (64.1%/51.8%/63.1%) | 51.0% (50.4%/51.8%/51.0%) |

## CPU cost and parameter count

| Variant | Params | Median seconds/run (training + evaluations) |
|---|---:|---:|
| tanh_w32 | 4864 | 4.14 |
| near_critical_w32 | 2816 | 4.75 |
| protected_w32 | 7504 | 14.05 |
| gru_w32 | 13376 | 10.61 |
| lstm_w32 | 17600 | 10.96 |
| gru_w24 | 7728 | 10.10 |
| lstm_w20 | 7160 | 9.86 |
| protected_random_w32 | 7504 | 13.77 |
| protected_no_project_w32 | 7504 | 12.56 |

## Interpretive limits

- Successfully answering both queries shows learning on this synthetic memory task; it does not certify the exact mathematical robust learning-credit dimension.
- If two-slot scores remain low, a longer or LR-tuned training schedule might work; this does not establish incapacity of the architecture.
- Comparison has one LR and three seeds, not equal parameter/compute budgets across all variants and no optimized GRU/LSTM schedule.
- Walsh and projection-removal controls are required before attributing any gains to those specific structures.
- Formal target `D=Ω(n), mT=o(n^(3/2))` remains **OPEN**.

## Provenance

Python 3.12.14, PyTorch CPU 2.14.1+cpu. Source artifact and raw machine-readable JSON are preserved.
