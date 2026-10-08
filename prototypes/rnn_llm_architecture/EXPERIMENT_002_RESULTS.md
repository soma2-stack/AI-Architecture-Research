# Experiment 002 — prespecified length-transfer / selective-memory controls

**Status:** COMPLETE, 66/66 scheduled runs recorded; 0 skipped/incomplete; 406.5 seconds (experiment process only).

**Evidence:** recorded from the GitHub Actions CPU artifact of the complete experiment. This is a bounded pilot, **not proof** of model superiority, a learning-credit theorem, or language-model ability.

## Main observations and falsifications

1. **Strongest positive observation:** protected Walsh-memory candidate learned the training-delay-64 binary copy task to **100% in all three seeds**, while the standard/GRU/LSTM baselines stayed near 50% with the same 150-step budget. With *frozen* trained weights, protected scored **100% at delay 256 in seeds 17 and 43**, but **50% in seed 29**: longer-length generalization is seed-dependent, not reliable.
2. **The specific projection mechanism did not prove necessary:** removing the fast-state re-projection scored **97.1% mean at delay 256** versus **83.3% for the original**. A random orthonormal memory basis also reached **100% at training delay 64**; Walsh specificity has not been established. These are three-seed observations, not proof that projection/retention is useless.
3. **Selective memory negative result:** the original protected model achieved **42.3% exact paired A+B accuracy at delay 64**, below the approximately **50.1% naive last-written-value paired baseline**. On **A≠B cases it solved both queries just 0.7% of the time**. Its apparent overall selective performance should **NOT** be described as reliable two-slot selective memory. At delay 256, paired accuracy fell to **34.0%**, with zero on A≠B pairs.
4. **Efficiency caveat:** protected median CPU training plus evaluation took **8.17 seconds/run**, vs **6.33 for GRU width 32** and **6.60 for LSTM width 32**; CPU timings are specific to this sequential reference implementation, not production fused kernels or equal-compute comparisons.

**Verdict:** This protocol supports further investigation of learned **single-bit long-delay recall** under this limited training schedule. It does **not** establish two-slot selective storage, a Walsh-specific advantage, necessity of the protected projection, or practical LLM superiority. The cleanest next falsification is to put contradictory bit tokens among distractors and require learning to ignore them; the existing benign filler cannot test interference from competing memory writes.

## Protocol

- Training: 11 variants × 2 tasks × 3 seeds; 150 AdamW optimizer updates, training delay 64, batch 16, fixed LR 0.002, clipping 1.0.
- Evaluation: frozen weights at delays 64, 128, 256, 512 held-out examples/condition/seed. Training/evaluation example streams are disjoint; corresponding models see matched examples.
- Three seeds and one learning rate do not establish optimized convergence or statistical generality.
- Trained recurrent architecture 4 (mathematical reference) remains excluded: no token adapter is defined.

## Delayed binary recall — frozen length transfer

Mean (individual seed results). Chance 50%; training delay 64 only.

| Variant | trainable parameters | delay 64 | delay 128 | delay 256 |
|---|---:|---:|---:|---:|
| tanh_w32 | 4864 | 49.7% (46.3%/50.4%/52.5%) | 49.7% (50.2%/48.0%/51.0%) | 48.6% (46.1%/49.2%/50.6%) |
| near_critical_w32 | 2816 | 49.8% (49.4%/48.8%/51.2%) | 48.8% (47.7%/48.6%/50.2%) | 48.4% (46.3%/48.4%/50.6%) |
| protected_w32 | 7504 | 100.0% (100.0%/100.0%/100.0%) | 83.3% (100.0%/50.0%/100.0%) | 83.3% (100.0%/50.0%/100.0%) |
| gru_w32 | 13376 | 50.8% (51.4%/48.8%/52.3%) | 51.2% (53.1%/47.5%/53.1%) | 50.7% (50.4%/50.4%/51.4%) |
| lstm_w32 | 17600 | 48.8% (50.2%/47.9%/48.2%) | 50.8% (52.3%/47.5%/52.7%) | 50.7% (50.6%/49.6%/51.8%) |
| gru_w24 | 7728 | 48.6% (48.2%/48.6%/49.0%) | 51.9% (54.5%/47.7%/53.5%) | 49.0% (48.6%/49.2%/49.2%) |
| lstm_w20 | 7160 | 48.6% (47.5%/50.4%/47.9%) | 51.6% (51.8%/46.9%/56.1%) | 49.8% (48.2%/49.2%/52.0%) |
| lstm_forget_w32 | 17600 | 50.7% (51.2%/51.2%/49.8%) | 50.5% (53.1%/46.9%/51.6%) | 50.6% (50.2%/50.6%/51.0%) |
| protected_random_w32 | 7504 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 83.3% (50.0%/100.0%/100.0%) |
| protected_no_project_w32 | 7504 | 100.0% (100.0%/100.0%/100.0%) | 100.0% (100.0%/100.0%/100.0%) | 97.1% (100.0%/91.4%/100.0%) |
| protected_no_retain_w32 | 7504 | 83.3% (100.0%/100.0%/50.0%) | 83.3% (100.0%/100.0%/50.0%) | 83.3% (100.0%/100.0%/50.0%) |

## Selective updating — *same-prefix* counterfactual paired queries

Each sample evaluates **both** possible final query tokens for an identical history. The pair counts as correct only if both slot values are correct. The naive always-last-written-bit baseline scores approximately 50% paired; aggregate one-slot accuracy of 75% on the old task is misleading.

### Test delay 64

| Variant | both correct | updated slot | untouched slot | both correct, A≠B | naive last-write both |
|---|---:|---:|---:|---:|---:|
| tanh_w32 | 25.7% (22.7%/30.1%/24.4%) | 50.9% (50.8%/52.1%/49.8%) | 51.7% (48.6%/55.1%/51.4%) | 9.0% (19.3%/7.6%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |
| near_critical_w32 | 28.0% (28.5%/27.0%/28.5%) | 52.0% (51.0%/49.6%/55.5%) | 53.3% (55.3%/51.8%/52.9%) | 9.1% (11.6%/6.0%/9.7%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_w32 | 42.3% (39.1%/50.8%/36.9%) | 59.3% (54.5%/74.8%/48.6%) | 75.1% (72.3%/75.4%/77.5%) | 0.7% (2.0%/0.0%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |
| gru_w32 | 25.5% (26.6%/26.8%/23.2%) | 50.3% (50.0%/50.8%/50.2%) | 50.7% (51.2%/52.3%/48.6%) | 0.9% (2.0%/0.8%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |
| lstm_w32 | 26.6% (28.1%/27.1%/24.4%) | 50.8% (51.0%/51.8%/49.8%) | 51.6% (51.8%/51.6%/51.4%) | 1.9% (5.2%/0.4%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |
| gru_w24 | 27.2% (27.0%/27.3%/27.3%) | 51.6% (50.0%/52.1%/52.7%) | 51.9% (52.5%/50.2%/52.9%) | 4.6% (0.0%/4.8%/9.0%) | 50.1% (51.4%/51.4%/47.7%) |
| lstm_w20 | 26.2% (27.0%/27.1%/24.4%) | 50.1% (50.0%/50.6%/49.8%) | 52.1% (52.5%/52.3%/51.4%) | 0.0% (0.0%/0.0%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |
| lstm_forget_w32 | 26.5% (27.0%/26.6%/26.0%) | 50.0% (50.0%/50.6%/49.4%) | 53.3% (52.5%/52.3%/55.1%) | 1.1% (0.0%/0.4%/3.0%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_random_w32 | 45.9% (51.0%/48.4%/38.3%) | 72.2% (76.8%/84.0%/55.9%) | 68.8% (73.2%/60.2%/72.9%) | 0.8% (0.4%/1.2%/0.7%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_no_project_w32 | 41.5% (49.6%/40.0%/34.8%) | 60.2% (78.7%/52.1%/49.8%) | 72.5% (68.9%/76.6%/71.9%) | 0.1% (0.0%/0.0%/0.4%) | 50.1% (51.4%/51.4%/47.7%) |
| protected_no_retain_w32 | 34.6% (38.9%/40.4%/24.4%) | 50.5% (49.8%/52.0%/49.8%) | 68.6% (77.0%/77.5%/51.4%) | 0.3% (0.8%/0.0%/0.0%) | 50.1% (51.4%/51.4%/47.7%) |

### Test delay 128

| Variant | both correct | updated slot | untouched slot | both correct, A≠B | naive last-write both |
|---|---:|---:|---:|---:|---:|
| tanh_w32 | 24.9% (27.0%/25.0%/22.7%) | 50.4% (51.4%/49.8%/50.0%) | 50.7% (53.1%/49.8%/49.2%) | 9.7% (23.4%/5.7%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| near_critical_w32 | 25.5% (25.8%/25.8%/24.8%) | 51.3% (49.8%/51.6%/52.5%) | 50.9% (52.0%/50.4%/50.4%) | 9.3% (11.9%/6.9%/9.1%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_w32 | 32.6% (37.1%/26.8%/33.8%) | 48.6% (48.2%/49.4%/48.0%) | 67.0% (75.2%/52.1%/73.6%) | 0.0% (0.0%/0.0%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| gru_w32 | 25.3% (26.6%/25.8%/23.4%) | 50.5% (50.4%/51.0%/50.0%) | 50.0% (50.8%/48.4%/50.8%) | 1.2% (2.4%/1.2%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| lstm_w32 | 25.2% (27.7%/25.2%/22.7%) | 50.7% (52.0%/50.0%/50.0%) | 50.3% (52.9%/48.8%/49.2%) | 2.1% (6.0%/0.4%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| gru_w24 | 23.8% (27.3%/22.9%/21.3%) | 49.7% (52.1%/50.4%/46.5%) | 49.1% (51.8%/46.1%/49.4%) | 4.0% (0.0%/3.7%/8.3%) | 49.6% (50.8%/52.0%/46.1%) |
| lstm_w20 | 25.1% (27.3%/25.2%/22.7%) | 50.9% (52.1%/50.6%/50.0%) | 49.6% (51.8%/47.9%/49.2%) | 0.0% (0.0%/0.0%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| lstm_forget_w32 | 24.7% (27.3%/25.2%/21.7%) | 49.5% (52.0%/50.4%/46.3%) | 49.5% (51.8%/48.0%/48.6%) | 1.7% (0.0%/0.4%/4.7%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_random_w32 | 37.2% (42.8%/34.4%/34.4%) | 55.3% (72.7%/42.6%/50.6%) | 69.5% (61.7%/74.8%/71.9%) | 0.4% (0.8%/0.0%/0.4%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_no_project_w32 | 32.1% (36.1%/26.8%/33.4%) | 51.8% (57.0%/49.4%/48.8%) | 62.7% (63.9%/52.1%/72.1%) | 0.1% (0.4%/0.0%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |
| protected_no_retain_w32 | 32.9% (36.7%/39.5%/22.7%) | 50.3% (50.4%/50.4%/50.0%) | 66.1% (73.0%/76.2%/49.2%) | 1.3% (2.4%/1.6%/0.0%) | 49.6% (50.8%/52.0%/46.1%) |

### Test delay 256

| Variant | both correct | updated slot | untouched slot | both correct, A≠B | naive last-write both |
|---|---:|---:|---:|---:|---:|
| tanh_w32 | 26.0% (27.5%/26.0%/24.6%) | 51.6% (53.3%/54.3%/47.3%) | 50.4% (52.0%/48.2%/51.0%) | 8.8% (23.2%/3.2%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |
| near_critical_w32 | 24.5% (26.4%/24.0%/23.0%) | 50.8% (51.2%/53.7%/47.5%) | 48.2% (48.8%/45.9%/50.0%) | 9.0% (13.4%/6.5%/7.2%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_w32 | 34.0% (37.9%/25.6%/38.7%) | 50.3% (51.8%/46.3%/52.9%) | 66.7% (73.6%/53.1%/73.4%) | 0.0% (0.0%/0.0%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |
| gru_w32 | 25.5% (25.6%/24.4%/26.4%) | 51.8% (50.6%/52.1%/52.7%) | 48.2% (50.2%/45.3%/49.0%) | 0.7% (2.0%/0.0%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |
| lstm_w32 | 25.3% (26.2%/25.2%/24.6%) | 49.7% (50.4%/51.6%/47.3%) | 50.1% (51.8%/47.5%/51.0%) | 1.8% (5.1%/0.4%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |
| gru_w24 | 25.3% (26.4%/23.4%/26.2%) | 50.7% (50.4%/52.5%/49.2%) | 50.8% (52.0%/46.7%/53.7%) | 4.3% (0.0%/4.0%/8.8%) | 51.0% (50.4%/51.8%/51.0%) |
| lstm_w20 | 25.7% (26.4%/26.2%/24.6%) | 50.5% (50.4%/53.7%/47.3%) | 49.9% (52.0%/46.9%/51.0%) | 0.0% (0.0%/0.0%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |
| lstm_forget_w32 | 24.6% (26.2%/25.6%/22.1%) | 50.8% (50.2%/53.5%/48.6%) | 48.2% (52.0%/46.3%/46.3%) | 0.9% (0.0%/0.0%/2.8%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_random_w32 | 33.4% (24.6%/36.7%/38.9%) | 52.6% (44.1%/62.3%/51.4%) | 63.4% (55.7%/59.0%/75.6%) | 0.8% (0.8%/1.2%/0.4%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_no_project_w32 | 30.3% (26.6%/25.6%/38.7%) | 49.3% (50.6%/46.3%/51.2%) | 60.1% (52.1%/53.1%/75.0%) | 0.1% (0.0%/0.0%/0.4%) | 51.0% (50.4%/51.8%/51.0%) |
| protected_no_retain_w32 | 32.7% (37.9%/35.7%/24.6%) | 48.8% (51.8%/47.5%/47.3%) | 65.6% (73.6%/72.3%/51.0%) | 0.0% (0.0%/0.0%/0.0%) | 51.0% (50.4%/51.8%/51.0%) |

## Model-size and CPU-training-time tradeoffs

Median of complete per-run CPU training plus evaluation times, and measured trainable parameter counts. Different widths have different representation capacity.

| Variant | Width | Parameters | Median seconds/run |
|---|---:|---:|---:|
| tanh_w32 | 32 | 4864 | 2.28 |
| near_critical_w32 | 32 | 2816 | 2.73 |
| protected_w32 | 32 | 7504 | 8.17 |
| gru_w32 | 32 | 13376 | 6.33 |
| lstm_w32 | 32 | 17600 | 6.60 |
| gru_w24 | 24 | 7728 | 6.04 |
| lstm_w20 | 20 | 7160 | 5.90 |
| lstm_forget_w32 | 32 | 17600 | 6.47 |
| protected_random_w32 | 32 | 7504 | 7.98 |
| protected_no_project_w32 | 32 | 7504 | 7.26 |
| protected_no_retain_w32 | 32 | 7504 | 8.07 |

## Boundaries / interpretations

- All outcomes are specific to short synthetic binary-memory tasks and one fixed training schedule. Raw inputs are tokens, but no natural language is trained.
- Equal-width and roughly parameter-near GRU/LSTM runs are shown separately; this is **not** compute-matched nor hyperparameter-tuned learning.
- A model can succeed at recall but fail at selective overwrite. Do not combine scores into one winner.
- The pair metric exposes trivial latest-value use; a more intelligent shortcut may still exist. Paired correctness above the naive baseline needs replication and targeted falsification.
- Removing protected projection or retention changes the architecture. Ablations isolate contributions only under these fixed training conditions.
- Longer evaluation delays do not guarantee the same examples across lengths; these are independent seeded draws of the same generating distribution.
- Report exact per-seed outcomes; no p-values or theorem claims with three seeds.
- Formal `D=Ω(n), mT=o(n^(3/2))` remains **OPEN**.

## Provenance

Input JSON contains the complete machine-readable per-run evidence. Runner reports Python 3.12.14, PyTorch 2.14.1+cpu. The output is a generated summary, not a replacement for the raw observations.
