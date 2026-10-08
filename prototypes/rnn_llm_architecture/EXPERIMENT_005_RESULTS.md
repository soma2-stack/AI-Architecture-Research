# Experiment 005 — state-conditioned slow-write gate

**Hosted CPU status:** `complete`; 30/30 configurations started; 0 skipped.

All results below are measured from the bounded 200-update synthetic paired-query pilot, **not** a formal learning-credit or language-model test. Models were trained separately at delay 16 or 64 and were evaluated at the trained delay and 2x/4x delay with frozen weights.


## Verdict — state gating did not resolve independent two-slot memory

The **prespecified intervention failed to establish consistent improvement** over the input-only protected RNN. On the primary unequal-valued both-slot metric, the three-seed mean changed **19.0% → 20.3%** at training delay 16 (**+1.3 percentage points**, but **2 of 3 seeds regressed**) and **2.6% → 0.9%** at training delay 64 (**−1.7 points**, with **2 of 3 seeds regressing**). At 64, the state-conditioned gate still performs extremely poorly at recalling both *different* values simultaneously.

The state-conditioned random-orthonormal variant reached **26.4%** on unequal pairs at delay 16, but scores varied markedly by seed (**44.0%, 6.6%, 28.4%**); at delay 64 it fell to **2.4%**. This does **not** support Walsh-specific advantage or robust improvement from state conditioning. GRU reached 7.1% at delay 64 but also failed to reliably learn the task under this training budget. All variants are still far from successful independent long-delay storage.

All **30/30** conditions completed **200 updates each**, with no skipped trials, in **181.4 seconds** of experiment runtime on GitHub-hosted CPU PyTorch 2.14.1. The hosted repository suite passed **156/156 CPU tests**. [Source run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37714510923).

**Do not promote** nonzero state-gate weights (which merely show gradient updates), high overall pair accuracy on equal-valued items, or single-bit recall as evidence of two-slot selective memory. A plausible next question is whether independently addressable slot-specific writable state, content-conditioned routing, or a longer controlled learning schedule is required, but **no follow-up experiment was launched**.

## Primary: both slots correct when A and B differ

This metric defeats the naive always-repeat-last-written-bit shortcut (which obtains zero both-correct on unequal cases). Chance for both independent random bits is 25% overall; on unequal-bit examples a fixed constant answer to both slots has 0%.

| Train delay | Variant | Seeds complete | Unequal both-correct | Overall both-correct | Updated | Untouched | Parameters |
|---:|---|---:|---:|---:|---:|---:|---:|
| 16 | protected_w32 | 3 | **19.0%** | 60.4% | 89.9% | 69.7% | 7,504 |
| 16 | state_gated_w32 | 3 | **20.3%** | 60.6% | 90.0% | 70.0% | 8,016 |
| 16 | state_gated_random_w32 | 3 | **26.4%** | 63.5% | 94.7% | 68.4% | 8,016 |
| 16 | gru_w32 | 3 | **3.0%** | 52.9% | 87.3% | 63.5% | 13,376 |
| 16 | lstm_w32 | 3 | **2.1%** | 35.3% | 57.9% | 59.9% | 17,600 |
| 64 | protected_w32 | 3 | **2.6%** | 51.4% | 84.4% | 65.4% | 7,504 |
| 64 | state_gated_w32 | 3 | **0.9%** | 50.6% | 87.8% | 62.4% | 8,016 |
| 64 | state_gated_random_w32 | 3 | **2.4%** | 51.3% | 90.0% | 60.4% | 8,016 |
| 64 | gru_w32 | 3 | **7.1%** | 24.2% | 49.2% | 48.7% | 13,376 |
| 64 | lstm_w32 | 3 | **1.6%** | 23.0% | 49.4% | 47.6% | 17,600 |

## Seed-level primary comparison

| Delay | Seed | Protected input-only | Protected state-conditioned | Δ state − input | State-conditioned random bank | GRU | LSTM |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 16 | 17 | 36.1% | 41.7% | +5.6 pp | 44.0% | 4.0% | 0.0% |
| 16 | 29 | 5.4% | 5.0% | -0.4 pp | 6.6% | 5.0% | 6.2% |
| 16 | 43 | 15.6% | 14.4% | -1.2 pp | 28.4% | 0.0% | 0.0% |
| 64 | 17 | 4.8% | 0.8% | -4.0 pp | 4.4% | 0.0% | 0.0% |
| 64 | 29 | 0.8% | 1.2% | +0.4 pp | 2.8% | 21.3% | 4.8% |
| 64 | 43 | 2.2% | 0.7% | -1.5 pp | 0.0% | 0.0% | 0.0% |

## Transfer (mean across complete seeds)

| Train delay | Tested delay | Variant | Unequal both-correct | All-example both-correct |
|---:|---:|---|---:|---:|
| 16 | 16 | protected_w32 | 19.0% | 60.4% |
| 16 | 16 | state_gated_w32 | 20.3% | 60.6% |
| 16 | 16 | state_gated_random_w32 | 26.4% | 63.5% |
| 16 | 16 | gru_w32 | 3.0% | 52.9% |
| 16 | 16 | lstm_w32 | 2.1% | 35.3% |
| 16 | 32 | protected_w32 | 8.2% | 47.9% |
| 16 | 32 | state_gated_w32 | 7.7% | 48.8% |
| 16 | 32 | state_gated_random_w32 | 15.1% | 42.6% |
| 16 | 32 | gru_w32 | 5.3% | 51.0% |
| 16 | 32 | lstm_w32 | 0.4% | 30.3% |
| 16 | 64 | protected_w32 | 2.4% | 20.9% |
| 16 | 64 | state_gated_w32 | 3.0% | 22.8% |
| 16 | 64 | state_gated_random_w32 | 0.1% | 26.4% |
| 16 | 64 | gru_w32 | 7.1% | 51.0% |
| 16 | 64 | lstm_w32 | 0.5% | 30.2% |
| 64 | 64 | protected_w32 | 2.6% | 51.4% |
| 64 | 64 | state_gated_w32 | 0.9% | 50.6% |
| 64 | 64 | state_gated_random_w32 | 2.4% | 51.3% |
| 64 | 64 | gru_w32 | 7.1% | 24.2% |
| 64 | 64 | lstm_w32 | 1.6% | 23.0% |
| 64 | 128 | protected_w32 | 0.4% | 28.6% |
| 64 | 128 | state_gated_w32 | 2.3% | 38.0% |
| 64 | 128 | state_gated_random_w32 | 0.4% | 29.0% |
| 64 | 128 | gru_w32 | 5.3% | 22.7% |
| 64 | 128 | lstm_w32 | 2.7% | 23.3% |
| 64 | 256 | protected_w32 | 0.0% | 25.0% |
| 64 | 256 | state_gated_w32 | 2.0% | 31.8% |
| 64 | 256 | state_gated_random_w32 | 0.3% | 34.2% |
| 64 | 256 | gru_w32 | 7.7% | 25.5% |
| 64 | 256 | lstm_w32 | 3.2% | 25.3% |

## Gate learning diagnostics

| Delay | Seed | State-conditioned gate L2 norms by layer | Initial loss | Final loss |
|---:|---:|---|---:|---:|
| 16 | 17 | [0.6347429752349854, 0.5322533845901489] | 1.5023 | 0.2980 |
| 16 | 29 | [0.5706369280815125, 0.4386798143386841] | 0.7835 | 0.5447 |
| 16 | 43 | [0.5536853671073914, 0.6199526190757751] | 0.9489 | 0.3047 |
| 64 | 17 | [0.6231303811073303, 0.6187267303466797] | 1.1077 | 0.3822 |
| 64 | 29 | [0.5493847727775574, 0.7326000332832336] | 0.7623 | 0.5081 |
| 64 | 43 | [0.5723035335540771, 0.6558586955070496] | 0.8364 | 0.5749 |

## Experimental limits

- These architectures were trained at the **same width, not matched trainable parameter or compute counts**; state-conditioned gating adds nR weights per layer.
- They share one fixed learning rate, step count and optimizer family, with no architecture-specific tuning or broad scaling study.
- Three seeds and synthetic two-slot tasks are insufficient for robust superiority or novelty claims.
- Gate weight L2 nonzero establishes that gradient updates occurred, not necessarily that gating learned a useful discrete write policy.
- No model has shown general selective memory or high-quality language-modeling on these experiments unless supported by the primary unequal-case scores.
- The frozen tanh theory reference is not a trainable LLM and the open D=Omega(n), mT=o(n^(3/2)) target remains OPEN.

## Complete evidence

- Raw per-condition and per-seed data: [`reports/experiment_005_results.json`](reports/experiment_005_results.json)
- Runner: [GitHub Actions Experiment 005](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37714510923)
- Original preregistered design: [`EXPERIMENT_005_PLAN.md`](EXPERIMENT_005_PLAN.md)
