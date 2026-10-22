# Experiment 010 — GRU-32 completion

**Execution status:** COMPLETED — INCONCLUSIVE at the original 800-update screening scope.  
**Practical advantage finding:** FAIL — this run did not show GRU-32 improving the primary metric over the existing learned baselines.  
**Architecture/capacity conclusion:** INCONCLUSIVE — the preregistered plan explicitly says this short screen cannot establish a capacity limit.

## Scope and provenance

The owner authorized only the missing original GRU-32 arm: five task shapes `(slots, values) = (2,2), (4,2), (8,2), (4,4), (8,4)`, seeds `17, 29, 43`, 800 updates per run, batch 12, evaluation batch 128, learning rate 0.002, training delay 64, and held-out delays 64 and 256. The original [plan](https://github.com/soma2-stack/AI-Architecture-Research/blob/eb71064db54285d5b4d0007413b6769aadba24f1/prototypes/rnn_llm_architecture/EXPERIMENT_010_PLAN.md) defines `whole_varied` as the primary metric and identifies this budget as a screen, not a convergence test. No pretrained weights, task labels beyond the original supervised task, oracle masks, or additional guidance were used.

The successful [Actions run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39718795692) used workflow commit [`15b4cae`](https://github.com/soma2-stack/AI-Architecture-Research/commit/15b4cae53dc818f2bd7fe58663ef715793c2c2b4), whose parent is the exact original source revision [`eb71064`](https://github.com/soma2-stack/AI-Architecture-Research/tree/eb71064db54285d5b4d0007413b6769aadba24f1). Only the one-off workflow was added; scientific source files were unchanged. All five task shards passed the original suite (231 tests per shard) before training. Every one of the 15 run records reports `status=complete`, `steps=800`, and zero skipped conditions. The data-generation code uses the original deterministic training seeds and disjoint evaluation seeds (`seed + 8,000,000 + delay`); the same task/seed evaluation histories are used across model variants.

The runner used Python 3.12.15, PyTorch 2.14.1+cpu, one CPU thread per shard, and `cuda_available=false`. Five shards ran concurrently; no GPU was used. The JSON-reported model runtime totaled 746.368 CPU-seconds across 15 runs (49.758 seconds/run on average; range 37.955–62.587 seconds). End-to-end workflow wall time was 4 minutes 19 seconds. Each GRU-32 had 13,888 trainable parameters. No model checkpoint was emitted by this screen; the raw per-run JSON is preserved below.

A first attempt at the newer PR23 head, run [`39718510169`](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39718510169), failed in unrelated tests because that revision expected an unavailable plot and checkpoint. All five jobs failed before the GRU-32 training step, so it contributed zero experimental conditions and is excluded. The successful rerun above checked out the original source revision, avoiding those later unrelated tests.

## Results

Each cell below gives the held-out `whole_varied` accuracy for seeds `17 / 29 / 43`, followed by the unweighted mean across those three seed runs. Values are percent. Each run evaluates 128 histories; `whole_varied` is conditional on histories whose final slot values are not all identical.

| Task `(slots, values)` | Delay 64: seeds; mean | Delay 256: seeds; mean |
|---|---:|---:|
| `(2,2)` | `100 / 100 / 0`; **66.67** | `100 / 100 / 1.64`; **67.21** |
| `(4,2)` | `0 / 0 / 0.90`; **0.30** | `0 / 0 / 2.70`; **0.90** |
| `(4,4)` | `0 / 0 / 0.79`; **0.26** | `0 / 0 / 0`; **0** |
| `(8,2)` | `0 / 0 / 0`; **0** | `0 / 0 / 0`; **0** |
| `(8,4)` | `0 / 0 / 0`; **0** | `0 / 0 / 0`; **0** |

Across the 15 task/seed runs, the equal-weight macro-mean of `whole_varied` was **13.45% at delay 64** and **13.62% at delay 256**. The corresponding existing 800-update results come from [the original CI run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37727194566) and its [results report](https://github.com/soma2-stack/AI-Architecture-Research/blob/192df629e060def0983c4e85f70c4dd01b15b6a0/prototypes/rnn_llm_architecture/EXPERIMENT_010_RESULTS.md):

| Learned model | Parameters | Macro `whole_varied` at 64 | At 256 |
|---|---:|---:|---:|
| GRU-32 (this completion) | 13,888 | 13.45% | 13.62% |
| Protected model | 8,016 | 13.60% | 13.49% |
| GRU-24 | 8,112 | 20.17% | 19.89% |

The macro mean weights each task/seed run equally, matching the plan's condition-level comparison. GRU-32 is approximately tied with the protected model and below the smaller, approximately parameter-matched GRU-24. GRU-32 has about 1.71× the parameters of GRU-24, so this is not a parameter- or compute-matched comparison for GRU-32. At eight slots it achieved **0/6** complete varied-record recalls at each delay, despite mean per-slot accuracy of 62.24%/60.32% on `(8,2)` and 41.83%/38.61% on `(8,4)` at delays 64/256. Individual fields were often partly correct, but the complete records were not recovered.

The task-structured delta-rule reference reached 100% in the original matrix after the separately authorized seed-43 replay. It has explicit event/address parsing unavailable to the learned generic RNNs; it is not a fair learned-model win or evidence of an autonomous architecture advantage.

## Disposition

All 75 original model/task/seed conditions are now complete at the registered 800-update screen: the original 60-condition matrix (including the separately documented seed-43 completion) plus these 15 GRU-32 conditions. The screen found no GRU-32 improvement and no reliable complete recall beyond the easiest task. Since the plan has no single pass threshold and explicitly warns against interpreting an 800-update failure as a capacity limit, the full experiment is **COMPLETED — INCONCLUSIVE** for the broader capacity and architecture questions. Do not extend or repeat this protocol without new owner authorization.

## Raw results and integrity

These five files are the unmodified JSON outputs downloaded from the successful workflow artifacts. Each reports three unique seeds, the task-specific configuration, CPU-only environment, 800 updates per run, and `status=complete`.

| Task | Raw JSON | SHA-256 |
|---|---|---|
| `(2,2)` | [rnn-exp010-gru32-2x2.json](rnn-exp010-gru32-2x2.json) | `89e4dc4531361725699348c4f2153ff8f379703fce37299f42eb0ce9c09241df` |
| `(4,2)` | [rnn-exp010-gru32-4x2.json](rnn-exp010-gru32-4x2.json) | `9f4ae21076aeabe60b8edd6f90f7ad0f1a0d1f090fc9979a87bcd8c58fbb012f` |
| `(4,4)` | [rnn-exp010-gru32-4x4.json](rnn-exp010-gru32-4x4.json) | `9ebf366f8d520cb4b6a207909d6c63735ab2b5be4a73939f1e1eea68f9e79adf` |
| `(8,2)` | [rnn-exp010-gru32-8x2.json](rnn-exp010-gru32-8x2.json) | `c31af29dba38410435ae89642a808b5e9987f439cde6dd205ebfac79c9708691` |
| `(8,4)` | [rnn-exp010-gru32-8x4.json](rnn-exp010-gru32-8x4.json) | `c56f82fe7c0741ffcb43934bbca31ff70d1ee77573e79c2229ded798ae9e84bb` |

The Actions artifacts also include a tarball of the exact tested source for each shard; the pinned source commit above remains the canonical code reference.
