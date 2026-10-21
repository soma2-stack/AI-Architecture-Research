# Learned gate repair — independent experimental report, 2026-10-20

**Outcome: PASS for learned preservation in this benchmark; FAIL for added recall benefit from the new sparsity penalty. Recommend the simpler answer-only repair.**

## Resume / status
- Lens: isolate accidental writes without oracle inference information. Stage: completed training, fresh paired evaluation, checkpoint reload and late-write falsification.
- Strongest result: answer-only gate training repairs long-delay recall in all three starting seeds. Closed: the proposed extra penalty is necessary for that gain. Unresolved: the weak seed, distribution changes and end-to-end training reliability.
- Exact next action: matched training from scratch with writes at unpredictable positions and held-out distractor distributions; keep answer-only sparse-gate controls and separately diagnose weak-seed addressing/readout.

## What changed and why
The existing sigmoid gate always produces positive activity. Short historical training did not sufficiently penalize thousands of accumulated filler writes. I kept the architecture and forward rule unchanged and fine-tuned only the existing gate MLP. The proposed objective is answer cross entropy + 0.1 times mean gate activity, including genuine writes. Its matched control removes that penalty. Neither receives new write/no-write labels, a grammar parser, an inference boundary, or an oracle mask.

Both continuations start from the SAME gradual-fade checkpoint per seed (17/29/43), freeze every other weight, and receive identical 128 updates, 12 histories/update, eight queries/history, AdamW .003, clipping 1, and 64 idle training tokens after the 32-token write body. That is 1,536 fresh histories and 12,288 query examples per arm/seed. The saved source checkpoint is context only, with zero repair updates, so its comparison is not equal-total-training evidence. All starts inherit earlier privileged address-alignment guidance; this does not demonstrate unaided addressing discovery. The halfway-fade family was not retrained.

This is a repair using generic regularization, **not a new architecture or primitive**, and it does not validate PR #35 or beat PR #36.

## Fresh complete-record recall
Each entry requires all eight independent binary facts correct. Three seeds x 128 fresh histories, identical paired inputs across arms. The table counts exactly the stated number of idle tokens after the ordinary write body, rather than reusing the old delay parameter.

| No-write tokens | Saved source | Answer-only repair | Sparse-gate repair | Oracle: source tail frozen |
|---:|---:|---:|---:|---:|
| 256 | 82.55% (317/384) | 83.07% (319/384) | 83.07% (319/384) | 83.07% (319/384) |
| 1,024 | 59.64% (229/384) | 83.07% (319/384) | 83.07% (319/384) | 82.81% (318/384) |
| 4,080 | 32.55% (125/384) | 83.33% (320/384) | 83.07% (319/384) | 83.07% (319/384) |

The oracle is a diagnostic reference, not a competitor or a mathematical upper bound: it can harm individual records. With repaired gates, oracle recall is 318/384 (82.81%) at every horizon for both arms. The source oracle differs from the prior audit because these are new held-out records.

| Seed, at 4,080 idle tokens | Source correct /128 | Answer-only /128 | Sparse /128 | Idle gate mean: source → answer-only → sparse |
|---:|---:|---:|---:|---:|
| 17 | 2 | 128 | 128 | 0.0107467 → 5.51126e-05 → 3.53898e-05 |
| 29 | 9 | 64 | 63 | 0.0380466 → 0.00851036 → 0.00215339 |
| 43 | 114 | 128 | 128 | 0.00201784 → 6.65656e-06 → 5.04741e-06 |

At 4,080 tokens, answer-only bit accuracy is 3,007/3,072 = **97.88%**, averaging 7.831/8 facts correct; sparse is 3,006/3,072 = **97.85%**, averaging 7.828/8. Source is 2,363/3,072 = 76.92%. Both repairs retain **318/318 records that were already wholly correct at the body boundary** on this set; source retains 123/320. This is empirical conditional retention, not perfect write suppression or an indefinite guarantee.

## Verdicts and causal checks

| Finding | Verdict | Actual evidence |
|---|---|---|
| Autonomous learned preservation improves vs saved source | **PASS, scoped** | Long-delay gains in every seed: answer-only +98.44, +42.97, +10.94 percentage points. Additional training and longer training tails are disclosed. |
| Penalty adds >=10 points over matched answer-only control | **FAIL** | 83.07% versus 83.33%, a -0.26 point difference. |
| No seed loses >5 points vs matched control at any horizon | **PASS** | Largest loss 1/128 = 0.78 point, seed 29 at 4,080. |
| Penalty reduces idle integral >=50% in every seed vs control | **FAIL** | Reductions 35.8%,74.7%,24.2%. Lower activity in every seed, but only one meets the threshold. |
| Gate training reduces accidental overwriting | **PASS, scoped** | See bank drift and gate activity below; both repair arms preserve previously correct records. |
| Extra labels, different test sets, changed nongate weights explain the gain | **PASS checks against these explanations** | Fresh test input hashes match; all nongate tensors remain exactly equal; no new event labels enter either loss or learned forward. Existing address guidance is shared. |
| New penalty is causally necessary for improved recall | **FAIL** | Coefficient-zero training ablation is equally good. Restoring the original gate restores ALL original tensors and exactly original logits, locating the repair in gate learning, not establishing a penalty benefit. |
| Late legitimate writes remain possible | **PASS on the small falsification set** | Detailed counts below; weak seed remains problematic. |
| Robust new architecture / PR #35 or #36 advantage | **INCONCLUSIVE, not demonstrated** | No such matched architecture comparison was performed. |

Bank cosine similarity (body to 4,080-token bank), source → answer-only → sparse:

- Seed 17: 0.2100 → 0.9998 → 0.9999; relative drift 0.9742 → 0.0325 → 0.0224.
- Seed 29: 0.5820 → 0.9217 → 0.9638; relative drift 0.8730 → 0.4942 → 0.3708.
- Seed 43: 0.8594 → 1.0000 → 1.0000; relative drift 0.6089 → 0.0042 → 0.0032.

The mean gate is write mass, not a direct norm of memory change; both are reported. For sparse seed 29, integrated idle gate activity is still 8.786 over the tail and relative bank drift is 0.371. Intended-write gate means are 0.961/0.818/0.999 in the sparse arm, versus 0.999/0.824/1.000 in answer-only. The penalty also suppresses useful writes; no perfect memory invariant exists.

## Independent reload and late-write falsification
Without further training, each model received 1,024 idle tokens, one randomly chosen fact deliberately changed to its opposite, then 256 more idle tokens. All 64 fresh records/seed and all inputs were paired. Reference replay independently checked the targets; only the test generator uses token semantics.

| Arm | Complete records, seeds 17 /29 /43 | Pooled complete recall | Newly changed fact correct |
|---|---|---:|---:|
| original | 14/64 / 23/64 / 64/64 | 101/192 (52.60%) | 191/192 (99.48%) |
| answer_only | 64/64 / 33/64 / 64/64 | 161/192 (83.85%) | 190/192 (98.96%) |
| sparse_gate | 64/64 / 34/64 / 64/64 | 162/192 (84.38%) | 188/192 (97.92%) |

Gate closure has not simply disabled all future writing. However, sparse seed 29 updates only 60/64 changed facts versus control 62/64: a possible preservation/update tradeoff, requiring more data before a firm claim. The ~50% whole-record ceiling remains even with oracle tail preservation, so it needs a separate addressing/readout investigation.

## Verification, cost and limits
- Optimized shared-prefix inference agrees with native forward: maximum long-delay logit difference 2.39e-7; pretraining gate-gradient difference <=1.50e-8. Reloaded native predictions match saved fresh predictions. No labels are inputs to learned inference.
- A small float64 check (two long histories per model/seed, 18 records total) gives identical predictions, maximum logit difference 7.23e-5. This rules out a sampled float32-only scoring artifact; it is not a numerical stability proof. Positive sigmoid leakage and longer horizons remain unresolved.
- Both models: **11,507 unique parameters**, **3,169 trainable during repair**, **46,028 bytes FP32 parameter storage**. A streaming implementation needs 160 persistent FP32 scalars (640 bytes: bank96 + GRU32 + previous embedding32), excluding transient activations. The evaluator caches prefixes/features and uses more workspace.
- Across three seeds: answer-only training **27.47 wall s /107.84 process CPU s**; sparse **27.83 wall s /109.27 CPU s**. Both have equal steps, data and trainable parameters. Gate regularization does not reduce inference operations.
- Main training/evaluation/parity run **228.36 wall s /636.92 CPU s**; independent verification **64.86 wall s /156.16 CPU s**. Total **293.22 wall s /793.08 CPU s**, excluding startup and inspection. Four intra-op threads, one inter-op thread, no worker processes or GPU.
- Verification peak working set **643.1 MiB**. The main run's Windows peak counter failed silently and returned zero; its actual peak is **unavailable**, not zero. Do not infer training peak from verification peak.
- Three warm starts on one fixed-vocabulary synthetic task are insufficient for general architectural claims. No claim of new mechanisms, larger-scale scaling, novel distractor generalization, or full end-to-end repair is established.
- All **60 original files** remain byte-identical. Original proofs, checkpoints, reports and notebooks were preserved. No GPU, external outreach or GitHub changes.

## Next recommended research step
**Use answer-only gate training as the reference.** Run one matched from-scratch experiment with unpredictable write times and unseen distractor distributions, including late updates and end-to-end gate/address learning. First inspect seed 29 addressing/readout errors cheaply; further gate penalties alone are unlikely to remove its ceiling. Reserve untouched test streams before choosing mechanisms.

## Artifacts and reproduction
- Protocol: `learned_gate_repair_protocol.md`; training/evaluation: `learned_gate_repair.py`; independent reload/falsification: `learned_gate_repair_verify.py`.
- Raw predictions, labels, full training traces, file hashes and resource records: `learned_gate_repair_results.json` and `learned_gate_repair_verification.json`.
- New saved models: `learned_gate_repair_weights.pt`, keys `{seed}_original`, `{seed}_answer_only`, `{seed}_sparse_gate`. CPU, weights-only loading; source projections remain tied in the model builder.
- Scripts refuse existing output files. To repeat the main study without overwriting, from repository root:

```powershell
python -B -c "import sys; sys.path.insert(0,'experiments/memory_retrieval_triage_20261020'); import learned_gate_repair as r; r.OUT=r.HERE/'learned_gate_repair_repeat_results.json'; r.WEIGHTS=r.HERE/'learned_gate_repair_repeat_weights.pt'; r.main()"
```
