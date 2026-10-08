# Experiment 006 — frozen-state storage versus retrieval

**Status:** 24/24 completed, 0 skipped; authoritative GitHub Actions CPU run using **PyTorch 2.14.1+cpu**, [workflow #37715859355](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37715859355). All **164/164 repository prototype tests passed**.
**Tested source commit:** `bf80125cbcc5b71b3d1fc81034e2dfb0971df7fd` · **raw JSON SHA-256:** `1eff943e4f5c33da4a5a2b6523ae4dcba4a2f8278932225c720caa20d5e86cbd`.
**CPU runtime:** 202.9 seconds (one CPU thread; no GPU or Sol usage). The same 24-run script independently completed on a local CPU PyTorch 2.10.0 environment in 265.9 seconds; the exact values vary slightly by runtime, while the main qualitative pattern persists.

## Scientific question and caveat

Experiment 005 archived performance metrics but no trained model checkpoints. This run recreated its train schedule (200 AdamW updates, batch 16, LR .002, clipping 1) and used **two independently trained diagnostic readers** of frozen query-free recurrent states. Reader training is additional supervised learning, **not** native task success. Neither a successful probe nor an unsuccessful probe is a formal proof about memory capacity or robust credit dimension.

Compare all models and all three seeds, at both training delays 16 and 64; evaluate A and B when their **final values differ**. Native readout is the original token-prediction head. Probes must output two independent bits from the same state, with no answer/query tokens. Last-write shortcut gets 0% on different-valued histories; two independently random guessed bits yield approximately 25% correct pairs.

## Primary held-out scores (%) on unequal final A/B values

| Trained delay | Architecture | Native head | Post-update MLP | Final linear | Final MLP | Untrained final MLP |
|---|---|---:|---:|---:|---:|---:|
| 16 | Protected | 19.9% | 97.4% | 66.4% | 89.9% | 40.4% |
| 16 | State-gated protected | 20.9% | 97.9% | 66.6% | 89.0% | 40.4% |
| 16 | GRU | 2.9% | 91.8% | 48.3% | 59.9% | 11.7% |
| 16 | LSTM | 1.3% | 73.8% | 14.0% | 19.5% | 15.1% |
| 64 | Protected | 3.4% | 80.1% | 23.2% | 41.0% | 16.4% |
| 64 | State-gated protected | 0.7% | 80.1% | 25.1% | 42.9% | 16.4% |
| 64 | GRU | 7.9% | 59.4% | 18.5% | 23.5% | 32.0% |
| 64 | LSTM | 2.7% | 50.9% | 22.5% | 30.7% | 29.7% |

## Seed-by-seed audit (%)

| Trained delay | Variant | Seed | Native unequal | Frozen final linear | Frozen final MLP | Untrained MLP |
|---|---|---:|---:|---:|---:|---:|
| 16 | Protected | 17 | 40.0 | 94.5 | 98.0 | 69.9 |
| 16 | Protected | 29 | 4.8 | 42.1 | 80.0 | 26.0 |
| 16 | Protected | 43 | 15.0 | 62.5 | 91.7 | 25.2 |
| 16 | State-gated protected | 17 | 43.3 | 92.7 | 95.7 | 69.9 |
| 16 | State-gated protected | 29 | 4.4 | 42.9 | 78.0 | 26.0 |
| 16 | State-gated protected | 43 | 15.0 | 64.1 | 93.4 | 25.2 |
| 16 | GRU | 17 | 4.5 | 32.9 | 45.9 | 20.3 |
| 16 | GRU | 29 | 4.0 | 24.0 | 42.3 | 7.3 |
| 16 | GRU | 43 | 0.2 | 88.2 | 91.5 | 7.4 |
| 16 | LSTM | 17 | 0.0 | 10.4 | 15.4 | 19.1 |
| 16 | LSTM | 29 | 4.0 | 17.9 | 34.7 | 12.3 |
| 16 | LSTM | 43 | 0.0 | 13.6 | 8.3 | 13.8 |
| 64 | Protected | 17 | 3.8 | 24.3 | 50.3 | 17.3 |
| 64 | Protected | 29 | 0.4 | 25.0 | 43.4 | 17.7 |
| 64 | Protected | 43 | 5.9 | 20.4 | 29.3 | 14.3 |
| 64 | State-gated protected | 17 | 0.4 | 28.0 | 63.6 | 17.3 |
| 64 | State-gated protected | 29 | 1.3 | 32.1 | 42.8 | 17.7 |
| 64 | State-gated protected | 43 | 0.4 | 15.2 | 22.4 | 14.3 |
| 64 | GRU | 17 | 0.0 | 19.7 | 18.9 | 26.0 |
| 64 | GRU | 29 | 23.6 | 13.1 | 20.7 | 33.4 |
| 64 | GRU | 43 | 0.0 | 22.8 | 30.9 | 36.6 |
| 64 | LSTM | 17 | 0.0 | 23.7 | 26.2 | 22.1 |
| 64 | LSTM | 29 | 8.1 | 23.6 | 33.0 | 38.6 |
| 64 | LSTM | 43 | 0.0 | 20.0 | 33.1 | 28.5 |

## Interpretation

**Evidence for a retrieval bottleneck at 16 tokens:** Protected native 19.9% versus frozen-state MLP 89.9%; state-gated native 20.9% versus MLP 89.0%. GRU native 2.9% versus MLP 59.9%. A state reader can recover information the existing token head is not learning to use. This is **not unique** to protected memory.

**Evidence for decodability loss across the distractor tail:** Protected 64-token post-update MLP 80.1%, versus final 41.0%; state-gated 80.1% versus 42.9%. Same labels and held-out examples, so this supports declining recoverability through the tail. It does **not** prove information is erased; more powerful readers may recover it.

**Trained-versus-random-state probe control:** The same-seed untrained protected MLP recovers 40.4% (delay16) and 16.4% (delay64), versus the trained-state MLP at 89.9% and 41.0%. This supports a trained-representation contribution in these conditions. The untrained model still receives additional supervised **probe** fitting.

**Probe generalization gap:** Protected 64-token final MLP training 52.7%, held-out 41.0%; at 16 tokens training 94.6%, held-out 89.9%. The long-delay task remains unsolved; stronger probes or longer recurrent-model training may change this result.

**State-gated comparison:** Results remain seed-dependent. State-gated final MLP 42.9% versus protected 41.0% at delay64; native state-gated 0.7% versus protected 3.4%. This is not convincing evidence that adding state-conditioned gates solved the two-slot task.

## Controls and limitations

- All 24 recurrent trainings are **new deterministic reproductions**, not the exact original model checkpoints from Experiment 005. Source model wrappers and baseline state equations unchanged. CPU environment version may alter bitwise reproducibility versus hosted runs; never mix without labeling.
- Same model training examples per seed/delay/step and identical held-out histories across models; probe training examples are independently generated. Data standardization uses probe-training features only.
- Probe training adds new trainable parameters: 4-output linear head or two-layer 64-unit MLP; the original native head did **not** get the same reader training. Therefore this is a diagnostic, not a fair architecture-quality comparison.
- Recurrent feature vectors concatenate both layers; LSTM concatenates **both hidden and cell state**, so feature width differs between architectures. No oracle writing, answers, or query identity are provided as probe input.
- Models remain very small, with only 200 optimizer updates and three seeds. The tasks are synthetic and are not general language understanding. Trainable-parameter matching, wall-clock matching, and much longer model training are not established here.
- On unequal A/B pairs a simple last-write rule cannot solve both, but reader training can exploit task-specific structure; the held-out split prevents direct example reuse, not all possible distribution shortcuts.
- This experiment does not test the formal claim `D=Omega(n), mT=o(n^(3/2))`, which remains **OPEN**.

## Recommended next hypothesis (NOT YET RUN)

Test whether training the **native model** with a stronger A/B-addressed readout or an auxiliary latent-state retrieval loss can close the gap **without sacrificing long-horizon storage**, using longer distractor tails and matched compute controls. This should be treated as a separate future experiment after approval; do not auto-launch a sweep.

## Reproduction

See [`EXPERIMENT_006_PLAN.md`](EXPERIMENT_006_PLAN.md) and [`experiment_006.py`](experiment_006.py) for exact parameters and output refusal-to-overwrite protection. The main artifact is [`reports/experiment_006_results.json`](reports/experiment_006_results.json).
