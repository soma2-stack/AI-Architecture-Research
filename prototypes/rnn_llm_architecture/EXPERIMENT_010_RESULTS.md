# Experiment 010 — capacity screening results

**Coverage:** 60 recorded runs, 0 skipped; **59 finished all 800 updates, 1 time-limited at 586** (delta-rule, 8 slots × 2 values, seed 43). All five GitHub jobs succeeded. Exploratory **800-update screening**, not an architecture capacity theorem or converged training.

All accuracy numbers below use held-out query histories. Primary `whole_varied` requires all slots correct when final values differ. Random independent whole-memory chance is `(1/values)^slots`; on a varied-only stratum it may differ.

| Slots | Values | Model | completed seeds | per-slot @64 | whole-varied @64 | whole-varied @256 | Mean steps |
|---:|---:|---|---:|---:|---:|---:|---:|
| 2 | 2 | `delta_rule` | 3/3 | 100.0% | 100.0% | 100.0% | 800 |
| 2 | 2 | `gru24` | 3/3 | 100.0% | 100.0% | 99.5% | 800 |
| 2 | 2 | `protected` | 3/3 | 91.8% | 67.7% | 67.2% | 800 |
| 2 | 2 | `protected_no_retain` | 3/3 | 74.2% | 2.8% | 3.8% | 800 |
| 4 | 2 | `delta_rule` | 3/3 | 100.0% | 100.0% | 100.0% | 800 |
| 4 | 2 | `gru24` | 3/3 | 64.6% | 0.6% | 0.0% | 800 |
| 4 | 2 | `protected` | 3/3 | 63.9% | 0.3% | 0.0% | 800 |
| 4 | 2 | `protected_no_retain` | 3/3 | 65.8% | 0.3% | 0.9% | 800 |
| 4 | 4 | `delta_rule` | 3/3 | 100.0% | 100.0% | 100.0% | 800 |
| 4 | 4 | `gru24` | 3/3 | 47.3% | 0.3% | 0.0% | 800 |
| 4 | 4 | `protected` | 3/3 | 46.4% | 0.0% | 0.3% | 800 |
| 4 | 4 | `protected_no_retain` | 3/3 | 43.6% | 0.3% | 0.0% | 800 |
| 8 | 2 | `delta_rule` | 2/3 | 100.0% | 100.0% | 100.0% | 729 |
| 8 | 2 | `gru24` | 3/3 | 57.1% | 0.0% | 0.0% | 800 |
| 8 | 2 | `protected` | 3/3 | 60.5% | 0.0% | 0.0% | 800 |
| 8 | 2 | `protected_no_retain` | 3/3 | 60.7% | 0.0% | 0.0% | 800 |
| 8 | 4 | `delta_rule` | 3/3 | 100.0% | 100.0% | 100.0% | 800 |
| 8 | 4 | `gru24` | 3/3 | 34.1% | 0.0% | 0.0% | 800 |
| 8 | 4 | `protected` | 3/3 | 39.1% | 0.0% | 0.0% | 800 |
| 8 | 4 | `protected_no_retain` | 3/3 | 36.5% | 0.0% | 0.0% | 800 |

## Interpretation

- All learned models receive the same token stream; GRU-24 approximates, but does not exactly match, protected-model trainable parameters.
- The delta-rule reference has **structurally decoded addresses and exact event-based writes**, an advantage unavailable to generic RNNs. Treat it separately, not as a fair learned architecture baseline.
- Low scores after only 800 updates **cannot establish capacity failure**: Experiment 009 showed strong optimization plateaus often lasting >500–750 updates.
- This is not evidence for the formal dense-tanh `D=Omega(n),mT=o(n^(3/2))` conjecture.


## Provenance

- [GitHub Actions run 37727194566](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37727194566), source commit `eb71064d`, CPU PyTorch `2.14.1+cpu`. Each of five sharded jobs passed the full prototype test suite before training.
- `reports/experiment_010_screen.json` contains all 60 run records, 5 source-file SHA-256 hashes, and the partial-run record. Raw shard ZIPs remain in the GitHub Actions artifacts.
- No claims that an 800-update failure establishes a model capacity limit. Longer controlled training is required; the structured delta reference knows the event grammar and is not a parameter-matched generic RNN.
