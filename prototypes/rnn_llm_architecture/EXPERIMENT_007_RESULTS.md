# Experiment 007 — query-aware retrieval, frozen versus joint

**Status:** 18/18 conditions recorded, 0 skipped, status `complete`.
**Environment:** CPU-only PyTorch 2.14.1+cpu, Python 3.12.15; 315.1s total. [Hosted GitHub Actions run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37717052321).
**Tested source commit:** `c3439162824a074e21ef884dec23c1329d32cf58`. **Raw JSON SHA256:** `45aa209fe2ed42d038c4352633de4eacfc2823b85b96065ffb9c5ffef83af619`.

## Prespecified held-out primary metric

Percentage of examples with **both A and B answered correctly when final values differ**. Two independently guessed bits yield approximately 25%; a last-write shortcut predicts both the same and receives 0% on unequal cases. Three training seeds 17/29/43; matched examples across model conditions.

| Trained delay | Model | Native at 200 | Native +150 | Frozen top +150 | Frozen all +150 | Joint all +150 |
|---:|---|---:|---:|---:|---:|---:|
| 16 | Protected (3 seeds) | 19.0% | 86.9% | 76.3% | 83.5% | 58.0% |
| 16 | GRU (3 seeds) | 3.0% | 34.5% | 44.4% | 41.9% | 41.7% |
| 16 | LSTM (3 seeds) | 2.1% | 3.2% | 6.9% | 15.1% | 6.1% |
| 64 | Protected (3 seeds) | 2.8% | 2.1% | 21.0% | 30.8% | 3.3% |
| 64 | GRU (3 seeds) | 7.1% | 0.1% | 11.1% | 10.7% | 9.4% |
| 64 | LSTM (3 seeds) | 1.6% | 0.0% | 11.5% | 11.6% | 2.1% |

## Outcome and interpretation

**The short-horizon native reader was undertrained, not permanently incapable.** For protected memory at delay 16, the native original-token readout rose from **19.0%** unequal-pair accuracy at the original 200 updates to **86.9%** after 150 further updates, versus frozen all-state **83.5%** and joint readout **58.0%**. Across seeds, the native 350-update scores were **100.0%, 60.6%, 100.0%**. Thus the previous native-versus-probe gap is not by itself evidence that a new decoder architecture was required; additional ordinary training closed most of it at this short delay.

**Long-horizon selectivity remains unsolved.** At training delay 64, protected native continuation remained **2.1%**, joint all-state readout **3.3%**, frozen top-state **21.0%**, and frozen all-state **30.8%** on different A/B values. The all-state head beat the native one but only modestly exceeded the approximately **25%** independent-guess baseline, with three individual seed scores **38.2%, 24.5%, 29.9%**. Therefore added readout access reveals some remaining information, but has not solved selective retention.

**Joint training did not consistently dominate.** At delay 16 it was **100.0%, 0.0%, 74.0%** over protected seeds: extremely initialization-dependent. At delay 64 it was **9.2%, 0.4%, 0.4%**. This implementation's joint decoder uses unstandardized state features while frozen decoders standardize their fixed training features; the two arms therefore do not isolate co-training cleanly. The negative result does not rule out better jointly trained readouts or schedules.

**A possible length-curriculum clue, not a confirmed improvement:** protected joint-all trained at length **16** and evaluated without updates at length **64** averaged **44.5%** unequal-pair correctness, whereas jointly trained from scratch at length **64** averaged **3.3%**. Those are separate trained conditions, not a length-curriculum experiment, but they motivate a small, controlled 16-to-64 curriculum *if separately authorized*.

**Overall:** Experiment 007 supports short-length optimization as a major part of the native-readout gap and persistent long-horizon state/retrieval difficulty. It does not establish a new primitive or a competitive general-purpose language-model architecture.

## Length transfer (frozen, without further training)

Held-out unequal-pair accuracy after testing at 2× and 4× the original training delay.

| Train length | Eval length | Model | Native +150 | Frozen all +150 | Joint all +150 |
|---:|---:|---|---:|---:|---:|
| 16 | 32 | Protected | 43.7% | 15.3% | 53.0% |
| 16 | 32 | GRU | 35.2% | 33.5% | 39.0% |
| 16 | 32 | LSTM | 2.1% | 11.5% | 1.5% |
| 16 | 64 | Protected | 23.0% | 7.9% | 44.5% |
| 16 | 64 | GRU | 36.1% | 28.2% | 34.5% |
| 16 | 64 | LSTM | 1.0% | 6.8% | 2.7% |
| 64 | 128 | Protected | 1.4% | 12.6% | 1.9% |
| 64 | 128 | GRU | 0.0% | 9.5% | 10.8% |
| 64 | 128 | LSTM | 0.0% | 12.3% | 1.5% |
| 64 | 256 | Protected | 0.0% | 15.3% | 0.4% |
| 64 | 256 | GRU | 0.0% | 8.0% | 12.1% |
| 64 | 256 | LSTM | 0.0% | 13.1% | 1.3% |

## Raw per-seed training-length audit

| Delay | Model | Seed | Native +150 | Frozen top | Frozen all | Joint all |
|---:|---|---:|---:|---:|---:|---:|
| 16 | Protected | 17 | 100.0% | 92.5% | 92.9% | 100.0% |
| 16 | Protected | 29 | 60.6% | 56.4% | 71.8% | 0.0% |
| 16 | Protected | 43 | 100.0% | 80.0% | 86.0% | 74.0% |
| 16 | GRU | 17 | 3.6% | 20.6% | 16.7% | 25.0% |
| 16 | GRU | 29 | 0.0% | 15.4% | 13.7% | 0.0% |
| 16 | GRU | 43 | 100.0% | 97.2% | 95.2% | 100.0% |
| 16 | LSTM | 17 | 4.4% | 3.6% | 9.5% | 14.7% |
| 16 | LSTM | 29 | 2.5% | 12.4% | 25.3% | 3.7% |
| 16 | LSTM | 43 | 2.8% | 4.8% | 10.4% | 0.0% |
| 64 | Protected | 17 | 3.2% | 24.5% | 38.2% | 9.2% |
| 64 | Protected | 29 | 0.8% | 18.5% | 24.5% | 0.4% |
| 64 | Protected | 43 | 2.2% | 20.1% | 29.9% | 0.4% |
| 64 | GRU | 17 | 0.4% | 14.5% | 8.0% | 18.1% |
| 64 | GRU | 29 | 0.0% | 3.2% | 6.4% | 6.8% |
| 64 | GRU | 43 | 0.0% | 15.7% | 17.5% | 3.4% |
| 64 | LSTM | 17 | 0.0% | 4.8% | 12.0% | 5.6% |
| 64 | LSTM | 29 | 0.0% | 7.6% | 10.0% | 0.8% |
| 64 | LSTM | 43 | 0.0% | 22.0% | 12.7% | 0.0% |

## Readout/control audit

All five treatments start from identical trained recurrence weights within each seed/model/delay. The original head at 200 updates is retained as a baseline. Native-continued and joint-all receive the *same additional synthetic training stream* and 150 updates, while the frozen readers train on a separate fixed 1024-example stream. Frozen reader training verifies recurrent model weights are **bitwise unchanged** by hash; joint training must update those weights.

The query-aware MLP gets an A/B query identity and the query-free prefix state; it never receives answer labels at inference. All-state readers concatenate two layers (and LSTM cell states), whereas the native token head reads the top layer. Thus the new readers have more parameters, more direct feature access, and different training procedures. A positive difference is evidence for a readout bottleneck, **not** a fair equal-compute architecture victory.

Unlike frozen readers, joint training can change the recurrent memory representation. The original recurrent training lasts 200 updates; the matched continuation and joint arms each add 150 updates, but their optimizer parameter sets and per-step compute differ. Frozen readers see fixed standardized features; joint readers do not standardize features. These differences limit attribution.

Only three seeds and a small synthetic binary two-slot task; no real-language perplexity, hardware speed advantage, formal robust credit dimension, or theoretical theorem is established. The main theoretical target remains OPEN: `D=Omega(n), mT=o(n^(3/2))`.

## Next decision

Review the unequal-pair scores. If frozen readers outperform the native head, the readout bottleneck persists. If joint training consistently exceeds frozen readers, co-training may help. If all decay strongly with length, storing two distinct values through interference remains open. No Experiment 008 is authorized by this report.

## Reproduction

See [`EXPERIMENT_007_PLAN.md`](EXPERIMENT_007_PLAN.md), [`experiment_007.py`](experiment_007.py), and [`reports/experiment_007_results.json`](reports/experiment_007_results.json). GitHub run #37717052321 stores the exact source snapshot.
