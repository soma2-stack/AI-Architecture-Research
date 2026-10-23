# Experiment 001 — first bounded supervised learning results

**Status:** GitHub-hosted CPU run **SUCCESS**, 40/40 complete; 100 optimizer updates/condition. **Exploratory only.**
GitHub Actions run: [#37710011831](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37710011831).
The complete machine-readable evidence is [experiment_001_results.json](experiment_001_results.json), extracted unchanged from that run’s uploaded artifact.

## Procedure

- Models: improved standard, near-critical, protected, GRU, LSTM; **full theoretical reference is excluded** because it is not a token LLM.
- Conditions: two tasks × delays 16/64 × seeds 17/29 × five models = 40 training runs.
- Width 32, two layers, protected channels 8, vocabulary 16, batch 16, 100 updates, AdamW LR 0.002, gradient clipping 1.0.
- Held-out: 512 independently generated examples per task/delay/seed; same held-out set and same training batches across all five models for a given condition.
- CPU PyTorch 2.14.1+cpu. All 133 architecture+pilot unit tests passed in the hosted job; no GPU, dataset download, pretrained weights or RL.
- 81.96 seconds in the experiment process (excluding dependency installation and unit tests); **not a wall-clock training comparison on the owner’s hardware**.

## Held-out accuracy after 100 updates

Each cell reports seed 17 / seed 29 (mean). Chance-level accuracy is about 50%.

| Model | Delayed 16 | Delayed 64 | Selective 16 | Selective 64 |
|---|---:|---:|---:|---:|
| tanh | 100.0% / 100.0% (100.0%) | 50.8% / 48.6% (49.7%) | 72.3% / 74.2% (73.2%) | 49.6% / 52.1% (50.9%) |
| near_critical | 92.4% / 65.0% (78.7%) | 46.1% / 51.4% (48.7%) | 66.4% / 62.5% (64.5%) | 51.4% / 50.0% (50.7%) |
| protected | 100.0% / 100.0% (100.0%) | 100.0% / 100.0% (100.0%) | 75.2% / 76.4% (75.8%) | 65.8% / 63.5% (64.6%) |
| gru | 100.0% / 100.0% (100.0%) | 48.6% / 52.5% (50.6%) | 74.4% / 72.7% (73.5%) | 50.6% / 48.2% (49.4%) |
| lstm | 100.0% / 54.1% (77.1%) | 48.0% / 50.8% (49.4%) | 47.1% / 49.2% (48.1%) | 49.6% / 48.8% (49.2%) |

## What the outcomes support — and do not support

- **Delayed recall at 64 tokens:** protected achieved 512/512 held-out answers for each of the two seeds; all four other models were near chance after the **same 100-update budget**. This is evidence of fast learnability for this *specific small synthetic task*, not a robust-memory theorem or a global superiority claim.
- **Delayed recall at 16 tokens:** standard, protected and GRU reached 100% for both seeds; near-critical and LSTM varied by seed.
- **Selective overwrite at 64 tokens:** protected averaged 64.6%, higher than the other trained models (about 49–51%) but **below a naive last-written-value predictor** (~75–77.5%). It has not shown reliable selective updating.
- **Selective overwrite at 16 tokens:** protected averaged 75.8%, approximately matching the 75% last-value shortcut; this is not sufficient to claim the model maintains both slots independently.
- The protected cell uses an externally controlled coefficient projection structure, but **no oracle write masks were given in these learning runs**. Learned gates and model weights are jointly optimized.

### Selective task by query stratum

An updated-slot query asks for the recent overwrite; an untouched-slot query asks the network to retain the other slot. The original task design allows a shortcut by always predicting the last written value. Stratified metrics are therefore essential.

| Delay | Model | Seed | Updated slot | Untouched slot | Last-write shortcut |
|---|---|---:|---:|---:|---:|
| 16 | tanh | 17 | 89.5% | 56.1% | 75.0% |
| 16 | tanh | 29 | 71.1% | 76.8% | 74.6% |
| 16 | near_critical | 17 | 76.6% | 56.8% | 75.0% |
| 16 | near_critical | 29 | 77.2% | 50.4% | 74.6% |
| 16 | protected | 17 | 77.8% | 72.7% | 75.0% |
| 16 | protected | 29 | 77.6% | 75.4% | 74.6% |
| 16 | gru | 17 | 82.3% | 67.0% | 75.0% |
| 16 | gru | 29 | 83.6% | 63.6% | 74.6% |
| 16 | lstm | 17 | 48.4% | 45.8% | 75.0% |
| 16 | lstm | 29 | 51.3% | 47.5% | 74.6% |
| 64 | tanh | 17 | 46.6% | 52.2% | 75.0% |
| 64 | tanh | 29 | 53.9% | 50.0% | 77.5% |
| 64 | near_critical | 17 | 53.8% | 49.3% | 75.0% |
| 64 | near_critical | 29 | 52.9% | 46.6% | 77.5% |
| 64 | protected | 17 | 53.8% | 76.3% | 75.0% |
| 64 | protected | 29 | 58.9% | 69.0% | 77.5% |
| 64 | gru | 17 | 51.7% | 49.6% | 75.0% |
| 64 | gru | 29 | 46.8% | 50.0% | 77.5% |
| 64 | lstm | 17 | 47.1% | 51.8% | 75.0% |
| 64 | lstm | 29 | 47.5% | 50.4% | 77.5% |

### Fairness and efficiency caveats

Equal width **does not** mean equal trainable parameters, compute or wall time. Counts and observed per-run elapsed seconds in this exact pilot:

| Model | Trainable parameters | Median CPU seconds per 100-update run |
|---|---:|---:|
| tanh | 4,864 | 0.87 |
| near_critical | 2,816 | 1.03 |
| protected | 7,504 | 3.16 |
| gru | 13,376 | 2.46 |
| lstm | 17,600 | 2.45 |

Only **two** seeds and one 512-example held-out draw were used per condition. LR and initialization were not tuned per architecture. A 100-step schedule is biased toward models that learn early; GRU/LSTM may catch up with sufficient updates, a different forget-gate initialization, or tuned LR. The protected model is not necessarily the most efficient: here its recurrent forward/backward implementation was slower per run than the standard and GRU models.

No strong claims about information capacity, robust topological learning-credit dimension, theoretical novelty, generic LLM quality, long-run training convergence, or superiority over optimized LSTM/GRU are justified.

## Next cheapest falsification tests (not yet executed)

1. Test longer delays (128/256) and unseen delay generalization after training at 16/64, with more seeds.
2. Compare approximately parameter-matched and compute-matched controls, including separate matched LR selection and well-initialized LSTM forget gates.
3. Design a selective task where last-written-value heuristics do not beat chance or report counterfactual paired probes. Require both updated and untouched slot success.
4. Test protected-channel mechanism-removal ablations and substitute a random orthogonal bank, with identical budgets.
5. Preserve the exact theoretical reference separately; the target `D=Omega(n), mT=o(n^(3/2))` remains **OPEN**.

**No additional runs are inferred or fabricated.** Training evidence belongs to GitHub Actions run #37710011831; the source artifact was also downloaded and the complete prototype suite independently rerun in a separate CPU runtime (133 passes), though that runtime used PyTorch 2.10 rather than the hosted 2.14.1.
