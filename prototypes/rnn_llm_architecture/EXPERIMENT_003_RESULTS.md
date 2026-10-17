# Experiment 003 — contradictory-bit distractor interference

**Status:** COMPLETE, 42/42 runs, 0 skipped, 261.6 experiment seconds.

**Scope:** supervised toy memory experiment only; this does **not** establish formal learning-credit dimension, an architecture invention, or natural-language performance.

## Main observations

1. With interference included in training, the protected family learned single tagged-bit recall under contradictory distractors: original protected **100% at delay 64**, **87.6% at delay 256** (three-seed means), random orthonormal bank **100% at both**, no-projection variant **100% at both**. GRU was ~66%, LSTM near 50% under the same 150-update schedule.
2. When trained only on benign distractors, the original protected model reached **100%** benign recall at delay 64 but fell to **71.6%** under interfering distractors and **54.8%** under all-bit distractors at that length. The task therefore really tests learned resistance to interference, not an invariant that generalizes without training.
3. The result is **not Walsh-specific or projection-dependent**: at this width/budget the random orthonormal and no-projection ablations performed as well or better. The learned timescale or gating arrangement remains a plausible alternative explanation; the exact mechanism is unresolved.
4. No experiment here establishes simultaneous independent storage of A and B, language modeling, optimizer-tuned superiority, or the mathematical learning-credit theorem. The protected model remains slower than an ordinary RNN in this reference CPU implementation.

**Next decisive task:** train on **both independent slot queries** from identical histories, measure paired correctness on A≠B cases, and compare against GRU/LSTM plus mechanism-removal controls. If that succeeds, it is more substantive evidence of selective updating than copying one tagged bit.

## Design

- Seven model variants; training regimes benign-only versus interfering-bit filler; seeds [17, 29, 43]; 150 updates at delay 64, AdamW LR 0.002, batch 16.
- Frozen held-out evaluation at delays [64, 128, 256], each with 512 examples; benign, 50%-bit interfering, and all-bit distractors.
- Labels are drawn **before** distractors, so held-out targets are matched across delays for a given test seed. Noise and conflicts remain independently generated.
- No oracle write mask is given. Last distractor bit is independent of original labelled value and near 50% accurate.

## All models and test distributions

Each cell is mean (individual seed values) among complete runs; random chance is 50%.

### Trained with benign distractors

**Frozen evaluation on benign distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 50.7% (47.9%/54.5%/49.6%) | 50.1% (50.2%/50.0%/50.0%) | 48.6% (51.6%/47.1%/47.1%) |
| near_critical_w32 | 50.5% (48.0%/51.2%/52.1%) | 49.5% (48.2%/49.8%/50.6%) | 49.9% (54.9%/50.6%/44.3%) |
| protected_w32 | 100.0% (100.0%/100.0%/100.0%) | 96.8% (100.0%/90.4%/100.0%) | 83.3% (100.0%/50.0%/100.0%) |
| gru_w32 | 66.1% (100.0%/46.3%/52.0%) | 66.9% (100.0%/50.6%/50.0%) | 66.9% (100.0%/48.6%/52.1%) |
| lstm_w32 | 50.1% (49.2%/50.2%/50.8%) | 49.5% (51.4%/47.3%/49.8%) | 50.5% (52.7%/47.7%/51.2%) |
| protected_random_w32 | 100.0% (100.0%/100.0%/100.0%) | 66.7% (100.0%/100.0%/0.0%) | 100.0% (100.0%/100.0%/100.0%) |
| protected_no_project_w32 | 100.0% (100.0%/100.0%/100.0%) | 83.4% (100.0%/50.2%/100.0%) | 83.3% (100.0%/50.0%/100.0%) |

**Frozen evaluation on interfering distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 50.1% (47.9%/52.3%/50.2%) | 50.1% (49.6%/51.2%/49.4%) | 51.4% (54.3%/50.2%/49.6%) |
| near_critical_w32 | 51.4% (50.4%/53.3%/50.4%) | 50.3% (51.0%/49.4%/50.6%) | 47.9% (46.7%/50.4%/46.5%) |
| protected_w32 | 71.6% (79.3%/66.2%/69.3%) | 68.2% (77.1%/62.5%/65.0%) | 67.0% (78.5%/54.3%/68.2%) |
| gru_w32 | 63.0% (88.9%/46.7%/53.5%) | 64.7% (88.5%/53.7%/52.0%) | 63.1% (85.9%/53.1%/50.2%) |
| lstm_w32 | 50.9% (50.0%/50.8%/52.0%) | 51.2% (51.8%/51.6%/50.2%) | 51.6% (51.8%/51.2%/51.8%) |
| protected_random_w32 | 70.5% (55.1%/86.3%/70.1%) | 55.5% (50.2%/83.4%/32.8%) | 63.9% (48.8%/80.9%/62.1%) |
| protected_no_project_w32 | 76.4% (60.2%/73.4%/95.7%) | 73.8% (55.5%/69.9%/96.1%) | 69.1% (50.4%/60.9%/96.1%) |

**Frozen evaluation on all_bits distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 44.6% (32.4%/51.6%/49.8%) | 45.5% (35.9%/50.8%/49.8%) | 45.0% (35.7%/49.4%/49.8%) |
| near_critical_w32 | 49.5% (51.2%/50.0%/47.5%) | 50.1% (49.0%/51.6%/49.6%) | 50.5% (48.6%/51.0%/52.0%) |
| protected_w32 | 54.8% (51.8%/60.0%/52.7%) | 51.6% (50.0%/53.1%/51.6%) | 51.0% (50.6%/51.2%/51.4%) |
| gru_w32 | 55.3% (66.6%/50.0%/49.4%) | 51.3% (53.7%/50.0%/50.2%) | 50.3% (50.0%/50.0%/51.0%) |
| lstm_w32 | 50.6% (51.8%/50.0%/50.0%) | 49.9% (49.6%/50.0%/50.0%) | 49.9% (49.6%/50.0%/50.0%) |
| protected_random_w32 | 61.8% (54.1%/69.9%/61.5%) | 54.5% (49.0%/69.3%/45.1%) | 56.9% (48.8%/64.5%/57.4%) |
| protected_no_project_w32 | 63.3% (55.5%/51.6%/82.8%) | 60.5% (48.2%/50.4%/82.8%) | 62.6% (51.8%/51.0%/85.2%) |

### Trained with interfering distractors

**Frozen evaluation on benign distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 49.1% (48.8%/50.2%/48.2%) | 51.3% (52.3%/51.6%/50.0%) | 50.8% (51.4%/50.4%/50.8%) |
| near_critical_w32 | 49.2% (48.8%/48.4%/50.2%) | 48.6% (48.6%/49.2%/48.0%) | 49.2% (47.5%/47.7%/52.5%) |
| protected_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 83.3% (50.0%/100.0%/100.0%) |
| gru_w32 | 66.3% (100.0%/47.9%/51.2%) | 66.8% (100.0%/50.4%/50.0%) | 68.7% (100.0%/50.4%/55.7%) |
| lstm_w32 | 50.3% (49.6%/48.4%/52.7%) | 49.2% (53.5%/46.5%/47.7%) | 51.4% (47.9%/51.0%/55.5%) |
| protected_random_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) |
| protected_no_project_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 91.7% (75.2%/100.0%/100.0%) |

**Frozen evaluation on interfering distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 49.0% (48.4%/48.2%/50.2%) | 51.4% (51.4%/53.7%/49.0%) | 49.8% (50.2%/50.8%/48.4%) |
| near_critical_w32 | 49.4% (50.4%/48.6%/49.2%) | 51.0% (52.7%/51.0%/49.2%) | 49.8% (47.1%/51.4%/51.0%) |
| protected_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 87.6% (62.7%/100.0%/100.0%) |
| gru_w32 | 66.2% (100.0%/47.3%/51.4%) | 65.7% (100.0%/48.2%/48.8%) | 66.4% (100.0%/48.4%/50.8%) |
| lstm_w32 | 51.2% (52.9%/47.3%/53.5%) | 48.8% (50.2%/48.4%/47.7%) | 49.5% (49.2%/48.4%/50.8%) |
| protected_random_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) |
| protected_no_project_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) |

**Frozen evaluation on all_bits distractors**

| Model | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|
| tanh_w32 | 49.4% (49.8%/49.8%/48.6%) | 50.2% (50.0%/52.1%/48.4%) | 48.4% (48.4%/49.4%/47.5%) |
| near_critical_w32 | 49.0% (47.7%/51.4%/47.9%) | 48.4% (48.2%/48.4%/48.6%) | 48.6% (47.9%/45.7%/52.3%) |
| protected_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 99.8% (99.4%/100.0%/100.0%) |
| gru_w32 | 66.6% (99.8%/49.4%/50.6%) | 65.8% (99.6%/48.4%/49.4%) | 65.4% (96.5%/49.2%/50.6%) |
| lstm_w32 | 49.7% (49.4%/48.8%/51.0%) | 49.1% (49.4%/48.2%/49.6%) | 49.3% (49.0%/48.4%/50.4%) |
| protected_random_w32 | 100.0% (100.0%/100.0%/100.0%) | 99.9% (100.0%/100.0%/99.6%) | 100.0% (100.0%/100.0%/100.0%) |
| protected_no_project_w32 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) |

## Cross-regime comparison at training delay 64

Accuracy when evaluated on **interfering** distractors, comparing training regimes. This is a matched-input indication of whether the architecture can learn to ignore competing bit tokens.

| Model | benign-trained | interfering-trained | difference (percentage points) |
|---|---:|---:|---:|
| tanh_w32 | 50.1% (47.9%/52.3%/50.2%) | 49.0% (48.4%/48.2%/50.2%) | -1.2 |
| near_critical_w32 | 51.4% (50.4%/53.3%/50.4%) | 49.4% (50.4%/48.6%/49.2%) | -2.0 |
| protected_w32 | 71.6% (79.3%/66.2%/69.3%) | 100.0% (100.0%/100.0%/100.0%) | +28.4 |
| gru_w32 | 63.0% (88.9%/46.7%/53.5%) | 66.2% (100.0%/47.3%/51.4%) | +3.2 |
| lstm_w32 | 50.9% (50.0%/50.8%/52.0%) | 51.2% (52.9%/47.3%/53.5%) | +0.3 |
| protected_random_w32 | 70.5% (55.1%/86.3%/70.1%) | 100.0% (100.0%/100.0%/100.0%) | +29.5 |
| protected_no_project_w32 | 76.4% (60.2%/73.4%/95.7%) | 100.0% (100.0%/100.0%/100.0%) | +23.6 |

## Model resources

| Model | Trainable parameters | Median elapsed seconds per run (including evaluation) |
|---|---:|---:|
| tanh_w32 | 4864 | 2.45 |
| near_critical_w32 | 2816 | 2.87 |
| protected_w32 | 7504 | 8.60 |
| gru_w32 | 13376 | 6.63 |
| lstm_w32 | 17600 | 6.81 |
| protected_random_w32 | 7504 | 8.58 |
| protected_no_project_w32 | 7504 | 7.69 |

## Critical scientific limitations

- This is only three seeds, one optimizer and one training budget. Failure to learn may reflect short optimization or suboptimal hyperparameters.
- All variants are evaluated under the same task distribution and input sequences per seed; equal width is still not equal compute.
- A single tagged bit is **not** the same as storing two independent, selectively updated slots. Experiment 002 showed a significant two-slot failure.
- Benign-to-interfering transfer is an explicit distribution shift. Interfering-trained success is learned task selectivity but **not** proof of unique protected mechanisms.
- If the no-projection or random-basis controls match the proposed protected cell, they challenge the necessity/specificity of projection and Walsh structure.
- These results cannot prove or disprove `D=Ω(n), mT=o(n^(3/2))`, which remains **OPEN**.

## Provenance

GitHub-hosted CPU; Python 3.12.14, PyTorch 2.14.1+cpu. Original machine-readable artifact is stored alongside this report.
