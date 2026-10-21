# From-scratch memory experiment — 2026-10-20

**FAIL at this budget: neither fresh policy learned reliable eight-fact recall. The gate-only repair policy performed worse than continued full training at the longest delay.**

Status: one fixed experiment completed; no search or budget extension. Strongest findings: causal bank use and a diagnosed addressing failure. Unresolved: reliable autonomous allocation/alignment and long-delay stability. Next action: one matched attention-sharpness curriculum test, described below.

| Claim | Verdict | Evidence |
|---|---|---|
| Earlier repair reproduced; no new oracle inputs found | **PASS, scoped** | All nine prior repaired-checkpoint conditions reproduce per-example predictions; only gate tensors changed. Earlier write/query guidance remains inherited. |
| Reliable from-scratch memory without guidance | **FAIL at 512 updates** | 0/3 seeds in either fresh arm reached the preregistered 90% complete-record threshold at OOD4080. Some facts and preservation are learned, but reliable eight-fact learning is not established. |
| Gate-repair policy beats matched full training | **FAIL** | 34.72% vs44.44% complete recall; -9.72 points. Seed changes -30.21,0,+1.04 points. |
| Successful predictions actually use the memory bank | **PASS** | OOD4080 bit accuracy drops 91.75%→51.30% for full training and89.32%→51.22% for repair; whole recall drops to1/288 each. All six fresh per-seed bit drops exceed20 points. |
| Weak guided seed caused mainly by missed-write gates | **FAIL** | Perfect event gating leaves short-delay recall62/128. Correcting the colliding write+read route yields128/128. |
| Weak guided seed has addressing interference | **PASS, diagnostic** | Distinct tokens/facts3 and5 route to the same bank location; causal interventions below. This is learned collapse, not conflicting task labels. |
| PR #35 validation / superiority over PR #36 | **INCONCLUSIVE; not tested** | No theorem metric or matched PR #36 comparison. No new architecture is claimed. |

The previous repair changed **training, not architecture**: longer idle examples plus128 gate-only updates. Both fresh arms therefore use the identical shared-projection controller immediately before that repair (not the older untied-key variant). Each separately starts randomly with seeds101/211/307, receives6,144 identical paired histories and49,152 queried examples in512 AdamW updates, lr.003, clip1. Full training updates all weights throughout; repair updates all weights for384 steps, then only the gate for128. Both reset AdamW at384. Initial weights, first384 losses/states and complete data hashes match exactly. No fresh training function loads checkpoints; guided weights are loaded only after all fresh runs finish. Equal data/update budgets are **not equal FLOPs**, because freezing deliberately reduces compute.

Each history has randomized nonoverlapping write positions, eight initial writes and eight overwrites, with at least one actual value change. Final facts are independent uniform binary values. Bodies vary48/64/80 tokens in training, followed by0/16/64/128 idle tokens. No event masks, target addresses, correspondence labels or regularizer enter either loss/forward.

All filler identities22..29 and decoy values10/11 occur in training. Training allows32 same-parity pure-filler bigrams; OOD testing uses32 opposite-parity bigrams. Their actual input-pair sets are disjoint. **These are unseen combinations, not new token identities.** Queries14..21 are also seen during training. Fresh held-out seed streams were reserved before training; the test is never used to stop or tune a run.

For the table, three seeds x96 records; every tested body ends at its final write, then exactly the stated number of irrelevant tokens. Values are **complete-record % / individual-fact %**.

| Domain; idle tokens | Full training | Gate-repair policy | Guided reference only |
|---|---:|---:|---:|
| ID; 256 | 56.60 / 94.57 | 54.51 / 94.27 | 84.03 / 98.00 |
| ID; 1,024 | 54.51 / 94.14 | 53.12 / 94.05 | 84.03 / 98.00 |
| ID; 4,080 | 45.14 / 91.84 | 35.42 / 89.28 | 84.38 / 97.96 |
| OOD; 256 | 56.94 / 94.62 | 53.82 / 94.23 | 84.03 / 98.00 |
| OOD; 1,024 | 55.90 / 94.36 | 56.60 / 94.44 | 84.03 / 98.00 |
| OOD; 4,080 | 44.44 / 91.75 | 34.72 / 89.32 | 84.03 / 98.00 |

OOD4080 correct records per seed101/211/307: full **54/96,24/96,50/96**; repair **25/96,24/96,51/96**. Similar ID failures show that unseen filler combinations alone do not explain the deficit. Guided reference uses checkpoints17/29/43: **96/96,50/96,96/96**. It inherited correspondence guidance and unrestricted filler pairs; these bigrams are not necessarily unseen to it. Its score cannot isolate the effect of guidance, initialization, data or total training.

Fresh OOD4080 gate/drift measurements (invalid includes nonwrite history tokens and query branches):

| Seed /policy | Valid gate | Invalid gate | Bank cosine | Relative bank drift | Body-correct records still correct |
|---|---:|---:|---:|---:|---:|
| 101 /Full training | 0.8740 | 0.126746 | 0.8983 | 0.4484 | 42/50 |
| 101 /Gate-repair policy | 0.8738 | 0.126500 | 0.8130 | 0.5834 | 20/52 |
| 211 /Full training | 0.8195 | 0.093604 | 0.8117 | 0.5874 | 20/58 |
| 211 /Gate-repair policy | 0.8193 | 0.094077 | 0.7543 | 0.6600 | 21/59 |
| 307 /Full training | 0.8695 | 0.000186 | 0.9964 | 0.1030 | 50/50 |
| 307 /Gate-repair policy | 0.8707 | 0.000173 | 0.9902 | 0.1200 | 31/55 |

All six fresh final models have only **seven distinct dominant write addresses**; seeds101/307 also have one dominant write/read mismatch. Argmax counts are not a formal rank/capacity proof. Idle gate activity is not itself a forgetting rate: e.g.seed101 routes most idle write mass into bank2, which has no dominant fact write. Per-bank accumulated writes and initial-content survival coefficients are provided in the extra checks. Some correctly guessed body records also change at long delay; conditional record retention is not a direct information-capacity measure.

After1024 idle tokens, one fact is deliberately flipped, then256 more idle tokens. OOD results,192 records/arm:

| Policy | Complete records | Updated fact correct | Other seven bits correct |
|---|---:|---:|---:|
| Full training | 88/192 | 184/192 | 1243/1344 |
| Gate-repair policy | 104/192 | 185/192 | 1262/1344 |
| Guided reference | 164/192 | 191/192 | 1316/1344 |

The models can accept many late writes; that does not rescue reliable complete records. Removing the bank is an inference ablation, not a trained GRU baseline.

**Weak guided seed29:** facts3 and5 have write-address cosine0.99988 and share dominant slot7; their reads also point there. Exactly62/128 short histories have equal values for those facts: all62 succeed, and none of the66 unequal cases do. Post-hoc oracle diagnostics, with unchanged weights and the same inputs:

| Diagnostic | Complete records /128 |
|---|---:|
| Normal |62|
| Perfect write/no-write gating |62|
| Reroute only fact5 writes into unused bank1 |62|
| Reroute only its read |46|
| Reroute both its write and read |128|

This localizes the short-delay ceiling to colliding storage/retrieval, rather than a wrong token meaning or missed writes alone. The colliding gates average0.338/0.342 versus roughly0.98 for other facts, but perfect gates do not fix the ceiling. These oracle routing interventions are diagnostic only and enter neither fresh arm. Long-delay leakage is a separate additional failure.

**Verification and cost:** native/optimized forward error <=4.48e-8 before training; all-parameter gradient error <=2.24e-8. Reloaded native long-delay predictions match (maximum logit discrepancy2.39e-7); an independent native head-input hook reproduces zero-bank predictions. Late-update targets, all reported counts and hashes reconstruct. No GPU; four intra-op threads, one inter-op thread, no workers. All67 pre-existing files remain byte-identical.

| Fresh policy; three seeds | Training wall seconds | Process CPU seconds |
|---|---:|---:|
| Full training | 164.30 | 647.23 |
| Gate-repair policy | 146.69 | 577.34 |

Audit + training/evaluation + two verification passes: **547.78 wall seconds /1922.56 process CPU seconds**, excluding startup/inspection. Peak process working set **768.6 MiB**; this includes runtime/workspace, not just the model. Both models have11,507 parameters (46,028 FP32 bytes) and160 persistent streaming scalars (640 bytes, excluding workspace); repair trains3,169 parameters in its last stage. No architecture or general capacity advantage follows from these numbers.

**Single next experiment:** test one fixed **softmax attention sharpness warmup,1→8 over the first128 updates**, against constant8, with full end-to-end answer-only training and the same512-update budget/data. Keep inference at8. The hypothesis is that early sharp routing traps duplicate addresses; test whether warmup reduces collisions and improves complete-record recall without correspondence labels. This is a proposed optimization test, not a claimed fix. Do not extend gate-only training blindly.

Evidence: [fixed protocol](memory_from_scratch_protocol.md), [implementation](memory_from_scratch.py), [audit/reproductions](memory_from_scratch_audit.json), [all training traces and predictions](memory_from_scratch_results.json), [new weights and384-step states](memory_from_scratch_weights.pt), [native verification](memory_from_scratch_verification.json), [independent checker](memory_from_scratch_check.py), [routing/ablation/late-update checks](memory_from_scratch_extra_checks.json). Raw results retain all per-query counts, gate integrals, ID/OOD late results and file hashes.

Execution from repository root (each phase refuses an existing corresponding output):
```powershell
python -B experiments/memory_retrieval_triage_20261020/memory_from_scratch.py --phase audit
python -B experiments/memory_retrieval_triage_20261020/memory_from_scratch.py --phase run
python -B experiments/memory_retrieval_triage_20261020/memory_from_scratch.py --phase verify
python -B experiments/memory_retrieval_triage_20261020/memory_from_scratch_check.py
```
The existing outputs are preserved; a future rerun needs explicitly new output paths. No training beyond the fixed protocol, GitHub PR, external contact, proof edit or notebook edit was performed. Stop this experiment here.

