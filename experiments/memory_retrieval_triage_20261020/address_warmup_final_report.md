# Final address-allocation experiment

**PASS for the preregistered mean-improvement comparison; reliable performance across initializations remains INCONCLUSIVE.** One fixed six-run test; no follow-up optimization.

Only the training softmax sharpness changed: fixed beta8 versus beta1→8 over128 updates, then8. Both evaluate at8. Same11,507-parameter architecture, seeds101/211/307, examples, optimizer/reset and512 full-training updates. No pretrained initialization, extra supervision, masks or address assignments.

| Idle tokens | Fixed8: complete /fact accuracy | Warmup: complete /fact accuracy |
|---:|---:|---:|
| 256 | 164/288 (56.94%) / 94.62% | 239/288 (82.99%) / 97.87% |
| 4,080 | 128/288 (44.44%) / 91.75% | 242/288 (84.03%) / 98.00% |

| Seed | Long recall fixed→warmup (/96) | Write collision pairs fixed→warmup | Distinct write slots fixed→warmup | Read/write matches fixed→warmup |
|---:|---:|---:|---:|---:|
| 101 | 54→50 | 1→1 | 7→7 | 7→7 |
| 211 | 24→96 | 1→0 | 7→8 | 8→8 |
| 307 | 50→96 | 1→0 | 7→8 | 7→8 |

Long recall change **+39.58 points**; short recall change **+26.04 points**. Total dominant write collision pairs: **3→1**. The preregistered pooled/per-seed short-harm and paired-seed consistency thresholds passed. Nevertheless, seed101 remains a failure: short recall fell56/96→47/96 (-9.38 points), and long recall54/96→50/96 (-4.17 points). The short decline is just inside the predeclared10-point per-seed threshold; do not hide it behind the pooled gain. Only2/3 candidate initializations achieved reliable eight-fact recall.

Allocation is measured at the same evaluation sharpness, including full soft probabilities, overlap and per-query errors in raw JSON. Dominant collisions are not a rank/capacity proof. Both collision-free candidate runs scored96/96 at both delays; the candidate with an unresolved collision/misaligned read remained near50%. With the bank zeroed, candidate long-delay fact accuracy is51.48%, versus98.00% normally. This supports bank-dependent gains associated with improved allocation. Temperature also changes optimization of gates, values and readout, so allocation is not isolated as the sole causal mediator.

| Seed/arm | Soft write-pair overlap | Valid /invalid gate | Bank cosine at4080 | Zero-bank fact accuracy at4080 |
|---|---:|---:|---:|---:|
| 101/fixed8 | 0.03619 | 0.8740/0.126746 | 0.8983 | 51.95% |
| 101/warmup1to8 | 0.03629 | 0.8739/0.000016 | 1.0000 | 52.47% |
| 211/fixed8 | 0.03755 | 0.8195/0.093604 | 0.8117 | 51.17% |
| 211/warmup1to8 | 0.00044 | 0.9999/0.000052 | 0.9999 | 50.00% |
| 307/fixed8 | 0.03747 | 0.8695/0.000186 | 0.9964 | 50.78% |
| 307/warmup1to8 | 0.00049 | 0.9993/0.000107 | 0.9998 | 51.95% |

Limits: three seeds,96 records/seed/horizon, one small synthetic binary task. Same previously inspected held-out benchmark as the prior run; not an untouched external test. Evaluation filler bigrams are absent from training, but token identities are familiar. All neural inference is beta8 with no parser/oracle. Zero-bank is an inference diagnostic, not a trained baseline. No claim about PR #35, PR #36 or a new architecture.

Checks: paired initial/data hashes agree; baseline predictions reproduce the prior full-training benchmark; native inference and native head-input bank ablation agree with saved predictions. Full-gradient checks at beta1 and8 pass. All **76 pre-existing files** remain byte-identical.

Resources: **6 training runs,512 updates each**,4 intra-op threads,1 inter-op thread,no GPU/workers. End-to-end experiment **320.11 wall seconds /1215.61 process CPU seconds**, for startup/training/evaluation/verification (wall time includes startup; CPU measurement begins after imports). Peak process working set **770.5 MiB**. Hard599-second watchdog and cooperative570-second limit; no retries.

**Recommendation: preserve this bounded result without claiming a breakthrough. No additional training is authorized in this turn; return to independent mathematical auditing.**

Status: experiment complete; allocation lane stopped for now. Unresolved: robustness, isolation of the optimization mechanism and any broader architecture significance. Next work: mathematical auditing, not another allocation test.

Artifacts: [protocol](address_warmup_final_protocol.md), [script](address_warmup_final.py), [raw traces/predictions/checks](address_warmup_final_results.json), [new weights](address_warmup_final_weights.pt). The script refuses existing outputs. Prior code/checkpoints/reports/proofs/notebooks remain intact; no PR or outreach.

Mathematical-audit handoff: the latest locally tracked Claude proof revision is `origin/claude/dense-transfer-20261020` at `aa47ca5`, after the prior independent review of `b984ef9`. Its proof/scope/precision corrections are the next read-only audit target. This experiment issues no new theorem verdict; local tracking refs may lag GitHub.
