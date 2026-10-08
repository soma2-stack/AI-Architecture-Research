# Experiment 008 — short-to-long curriculum, fixed and shuffled controls

**Status:** complete — 36/36 full conditions; 0 skipped. CPU/PyTorch 2.14.1+cpu; elapsed 372.0s.

This was a bounded task-specific study, **not** proof of a new model architecture, general language-model superiority, or robust learning-credit dimension. The theorem `D=Omega(n), mT=o(n^(3/2))` remains OPEN.

## Verdict — no evidence that the curriculum solves two-slot memory

The primary hypothesis **did not pass** in this bounded experiment. At held-out delay **128**, protected memory scored **1.8%** unequal-pair correctness with increasing-length curriculum versus **2.6%** with shuffled training on the identical examples and length counts (three-seed mean). GRU was **4.1% versus 3.8%** and LSTM **1.7% versus 1.1%**. Those small, mixed differences are not compelling evidence for curriculum order.

Nearly all approaches remained **far below the ~25% unequal-pair independent-guess baseline** because the trained heads often produced the same recently written value for both slots; a last-write shortcut scores **0% on unequal pairs**, even if it scores ~50% overall. Protected curriculum's **47.9%** overall pair correctness at 128 tokens is below the measured **51.0%** naive last-write baseline. At 256 tokens, protected curriculum scored **0.0%** on unequal pairs.

One outlier matters for interpretation: fixed128 LSTM's **10.5% mean at 128 tokens** came from **0.0%, 0.0%, and 31.4%** over seeds 17, 29, 43, while its overall pair score was only **24.6%**. Do not label that a reproducible improvement.

This does not show curriculum training can never work. It shows **this specific monotone 60-step/stage schedule**, with 240 updates, batch 16, the existing model/readout, and three seeds, did not fix the long-delay independent A/B memory weakness. The result is more consistent with insufficient usable selective storage/readout than with a readily solved schedule-only issue.

## Primary endpoint: both slots correct when A≠B

Three-seed mean held-out accuracy if all three were complete; otherwise means are labeled with observed n. Random independent guessing ≈25%, copying last write =0% for unequal pairs.

| Model | Schedule | 16 | 64 | 128 | 256 | Seeds |
|---|---|---:|---:|---:|---:|---:|
| protected_w32 | curriculum | 0.8% | 1.5% | 1.8% | 0.0% | 3/3 |
| protected_w32 | shuffled | 3.0% | 1.6% | 2.6% | 2.7% | 3/3 |
| protected_w32 | fixed64 | 0.5% | 0.2% | 2.8% | 3.5% | 3/3 |
| protected_w32 | fixed128 | 0.3% | 0.0% | 0.0% | 0.0% | 3/3 |
| gru_w32 | curriculum | 4.3% | 3.7% | 4.1% | 2.0% | 3/3 |
| gru_w32 | shuffled | 4.8% | 4.7% | 3.8% | 2.7% | 3/3 |
| gru_w32 | fixed64 | 0.3% | 0.5% | 0.8% | 1.8% | 3/3 |
| gru_w32 | fixed128 | 0.0% | 0.0% | 0.0% | 0.0% | 3/3 |
| lstm_w32 | curriculum | 1.3% | 0.5% | 1.7% | 0.3% | 3/3 |
| lstm_w32 | shuffled | 0.5% | 0.8% | 1.1% | 0.8% | 3/3 |
| lstm_w32 | fixed64 | 0.0% | 0.0% | 0.3% | 0.3% | 3/3 |
| lstm_w32 | fixed128 | 13.9% | 9.4% | 10.5% | 10.4% | 3/3 |

## Paired curriculum versus shuffled, held-out A≠B accuracy

This is the **most controlled** order effect: same training lengths, same underlying examples, equal updates and equal nominal token exposure. Positive differences favor curriculum.

| Model | Delay | Seedwise (curriculum−shuffled), percentage points | Mean, pp |
|---|---:|---|---:|
| protected_w32 | 16 | 17: -6.8; 29: +1.6; 43: -1.5 | -2.2 (3 seeds) |
| protected_w32 | 64 | 17: -0.8; 29: -1.6; 43: +2.2 | -0.1 (3 seeds) |
| protected_w32 | 128 | 17: -2.3; 29: -0.8; 43: +0.8 | -0.8 (3 seeds) |
| protected_w32 | 256 | 17: -7.3; 29: +0.0; 43: -0.9 | -2.7 (3 seeds) |
| gru_w32 | 16 | 17: +0.8; 29: -0.8; 43: -1.5 | -0.5 (3 seeds) |
| gru_w32 | 64 | 17: +0.0; 29: -1.6; 43: -1.5 | -1.0 (3 seeds) |
| gru_w32 | 128 | 17: +0.0; 29: +0.8; 43: +0.0 | +0.3 (3 seeds) |
| gru_w32 | 256 | 17: +0.0; 29: -2.3; 43: +0.0 | -0.8 (3 seeds) |
| lstm_w32 | 16 | 17: +0.0; 29: -0.8; 43: +3.0 | +0.7 (3 seeds) |
| lstm_w32 | 64 | 17: +0.0; 29: -2.4; 43: +1.5 | -0.3 (3 seeds) |
| lstm_w32 | 128 | 17: +0.0; 29: -3.2; 43: +5.0 | +0.6 (3 seeds) |
| lstm_w32 | 256 | 17: +0.0; 29: -2.3; 43: +0.9 | -0.5 (3 seeds) |

## Aggregate and shortcut checks

Overall both-correct scores can look deceptively good because a last-write heuristic scores about 50% when final values are equal. Primary conclusions MUST use the A≠B stratum and per-seed signs.

| Model | Schedule | 128 overall both-correct | 128 naive last-write | Updated bit correct | Untouched bit correct |
|---|---|---:|---:|---:|---:|
| protected_w32 | curriculum | 47.9% | 51.0% | 82.6% | 61.3% |
| protected_w32 | shuffled | 46.6% | 51.0% | 70.2% | 69.3% |
| protected_w32 | fixed64 | 34.2% | 51.0% | 50.5% | 67.1% |
| protected_w32 | fixed128 | 37.2% | 51.0% | 50.0% | 73.4% |
| gru_w32 | curriculum | 53.0% | 51.0% | 88.2% | 63.9% |
| gru_w32 | shuffled | 52.9% | 51.0% | 87.2% | 65.0% |
| gru_w32 | fixed64 | 33.9% | 51.0% | 64.8% | 51.7% |
| gru_w32 | fixed128 | 25.8% | 51.0% | 49.3% | 51.2% |
| lstm_w32 | curriculum | 32.8% | 51.0% | 54.9% | 59.6% |
| lstm_w32 | shuffled | 25.4% | 51.0% | 48.0% | 51.8% |
| lstm_w32 | fixed64 | 25.3% | 51.0% | 48.8% | 50.7% |
| lstm_w32 | fixed128 | 24.6% | 51.0% | 48.2% | 51.3% |

## Resource fairness and limitations

- Each completed condition used the same batch size and number of optimizer updates. Curriculum and shuffled have exactly the same length histogram and per-length training samples, with different temporal order. Three seeds are too few for a general claim.
- Fixed64 and fixed128 use different total numbers of training tokens from curriculum and each other; this is an update-matched, **not token/FLOP/runtime-matched**, control.
- All models have width 32 and two recurrent layers, but different parameter counts and per-token compute.
- Training is fully supervised, same 2-query synthetic A/B task throughout; no real language modeling, no unbounded-length test, and no theoretical D proof.
- Every held-out score here came from the fixed seed `seed+1_000_000` and 256 independent histories. Unequal-pair counts fluctuate with random labels, and A/B may be equal.
- This is a hypothesis test of **training schedule**, not evidence that the Walsh masks or projection are individually necessary. Earlier ablations already challenge those claims.

## Individual run inventory

| Model | Seed | Schedule | Updates | Estimated train tokens (without 7 special tokens/example) | Time (s) |
|---|---:|---|---:|---:|---:|
| protected_w32 | 17 | curriculum | 240/240 | 230400 | 11.3 |
| gru_w32 | 17 | curriculum | 240/240 | 230400 | 7.1 |
| lstm_w32 | 17 | curriculum | 240/240 | 230400 | 7.0 |
| protected_w32 | 17 | shuffled | 240/240 | 230400 | 11.1 |
| gru_w32 | 17 | shuffled | 240/240 | 230400 | 6.9 |
| lstm_w32 | 17 | shuffled | 240/240 | 230400 | 7.0 |
| protected_w32 | 17 | fixed64 | 240/240 | 245760 | 10.7 |
| gru_w32 | 17 | fixed64 | 240/240 | 245760 | 6.9 |
| lstm_w32 | 17 | fixed64 | 240/240 | 245760 | 7.0 |
| protected_w32 | 17 | fixed128 | 240/240 | 491520 | 24.9 |
| gru_w32 | 17 | fixed128 | 240/240 | 491520 | 14.9 |
| lstm_w32 | 17 | fixed128 | 240/240 | 491520 | 14.8 |
| protected_w32 | 29 | shuffled | 240/240 | 230400 | 10.9 |
| gru_w32 | 29 | shuffled | 240/240 | 230400 | 6.8 |
| lstm_w32 | 29 | shuffled | 240/240 | 230400 | 7.0 |
| protected_w32 | 29 | fixed64 | 240/240 | 245760 | 10.9 |
| gru_w32 | 29 | fixed64 | 240/240 | 245760 | 6.8 |
| lstm_w32 | 29 | fixed64 | 240/240 | 245760 | 6.8 |
| protected_w32 | 29 | fixed128 | 240/240 | 491520 | 23.1 |
| gru_w32 | 29 | fixed128 | 240/240 | 491520 | 13.6 |
| lstm_w32 | 29 | fixed128 | 240/240 | 491520 | 13.5 |
| protected_w32 | 29 | curriculum | 240/240 | 230400 | 10.4 |
| gru_w32 | 29 | curriculum | 240/240 | 230400 | 6.5 |
| lstm_w32 | 29 | curriculum | 240/240 | 230400 | 6.6 |
| protected_w32 | 43 | fixed64 | 240/240 | 245760 | 10.2 |
| gru_w32 | 43 | fixed64 | 240/240 | 245760 | 6.5 |
| lstm_w32 | 43 | fixed64 | 240/240 | 245760 | 6.6 |
| protected_w32 | 43 | fixed128 | 240/240 | 491520 | 22.8 |
| gru_w32 | 43 | fixed128 | 240/240 | 491520 | 13.4 |
| lstm_w32 | 43 | fixed128 | 240/240 | 491520 | 13.4 |
| protected_w32 | 43 | curriculum | 240/240 | 230400 | 10.3 |
| gru_w32 | 43 | curriculum | 240/240 | 230400 | 6.4 |
| lstm_w32 | 43 | curriculum | 240/240 | 230400 | 6.5 |
| protected_w32 | 43 | shuffled | 240/240 | 230400 | 10.3 |
| gru_w32 | 43 | shuffled | 240/240 | 230400 | 6.4 |
| lstm_w32 | 43 | shuffled | 240/240 | 230400 | 6.4 |

## Provenance

Exact raw per-seed metrics and all stage-level training-loss/length counts: [`reports/experiment_008_results.json`](reports/experiment_008_results.json).
Hosted experiment: [GitHub Actions run 37718282627](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37718282627).
This report was generated from archived runner results; no score was interpolated or replaced.
