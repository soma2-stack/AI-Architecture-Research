# Independent experimental audit — 2026-10-20

**Verdict: the saved-model accuracy numbers are reproducible; gains are conditional, and there is no established PR #35/36 architecture advantage.** One new inference-only experiment identifies a causal retention failure.

## Resume / status
- Lens: falsify accuracy, supervision, retention and theorem-transfer claims.
- Stage: completed source/JSON/checkpoint audit and one paired inference intervention.
- Strongest surviving finding: learned external memory helps in some runs; explicit training guidance improves fixed-vocabulary recall; filler writes cause part of the long-delay degradation.
- Closed: the old ambiguous-remapping forgetting interpretation; autonomous-discovery interpretation of guided scores; correlation-only interpretation of filler drift for the tested failing checkpoints.
- Unresolved: learning to close gates without oracle inference masks, seed reliability, cost-matched architecture comparisons, and faithful learning-credit-to-prediction mechanisms.
- Exact next action: preregister an answer-supervised learned-persistence control using fresh untouched test seeds and equal budgets. No new training was launched in this audit.

## Important findings

| Finding | Verdict | Evidence / scope |
|---|---|---|
| Reported saved-model inference accuracy | **PASS** | 159 selected checkpoint/evaluation checks agree with rounded JSON accuracies within 5.01 e-6. |
| Saved checkpoint integrity | **PASS** | 9 containers, 117 model states, 85 distinct parameter states; all finite and loaded with strict shapes, CPU and weights-only loading. |
| Original ambiguous remapping as a forgetting test | **FAIL** | Identical input/query symbols demand conflicting answers. Independent check found 126 contradictory labels among 32 histories x 8 queries. Its old-task decline is not a valid forgetting measurement. The existing retraction is correct. |
| Corrected task-identified evaluator | **PASS** | Old queries 14..21 and new queries 32..39 are disjoint; independently parsed history labels and shifted targets agree. Before/after scores reproduced. |
| Corrected test is the same old permutation with identity added | **FAIL** | Old query j denotes write(j-3)%8; corrected new query j denotes write(j+3)%8. This changes the permutation as well as adding task identity. Neither mapping is internally wrong, but results are not same-mapping replications. |
| Guidance improves this synthetic task | **PASS, conditional** | Eight-fact whole recall: original 18.4%, answer-only shared 53.5%, guided alignment+diversity 84.0% across three seeds. |
| Reliable / general shared-address improvement | **FAIL as a universal claim** | Sharing improves eight facts but reduces four-fact recall from 62.5% to 31.9%. Eight-fact shared seed scores 18.8%,41.7%,100%. |
| Guided / faded results demonstrate autonomous discovery | **FAIL** | They received explicit WRITE_i-to-QUERY_i semantic matching during training. Removing hints later does not remove that training history. |
| Rehearsal preserves old mapping | **PASS within this protocol** | Guided start: old recall 1.0% new-only versus 62.2% rehearsal. Unguided start:1.4% versus 51.4%. |
| Rehearsal comparison has equal new-task exposure | **FAIL** | Same 240 updates and 5,760 total histories; new-only sees 5,760 new histories, rehearsal 2,880 new+2,880 old. It measures a fixed-total-budget tradeoff, not an equal-new-data effect. |
| First drift probe measures only false filler writes | **FAIL; superseded** | Original snapshot at token 16 precedes the end of the 32-token eight-fact body, so it includes intended writes. Corrected script uses boundary 32 and delay-16 tail tokens. |
| Filler writes contribute causally to forgetting | **PASS for tested checkpoints** | New matched frozen-tail intervention rescues long-delay records while changing no parameters or GRU states. |
| Writes on final query are the main cause | **FAIL on these cases** | Query-write-only removal changes no whole-record success counts in all 18 checkpoint/horizon conditions. Small bit-prediction differences remain possible. |
| Filler writes explain every failure | **FAIL** | Even frozen-tail recall remains 53/96 or 52/96 in several eight-fact checkpoints. Address/value/readout limitations remain. |
| New architectural advantage or PR #35 theorem validation | **INCONCLUSIVE / unsupported** | No cost-matched superiority or theorem credit metric is measured. No mathematical claim is invalidated by these neural results. |

## What the numbers establish

The principal report tables agree with their JSON sources to displayed precision. Replaying checkpoints strengthens this beyond recomputing means from JSON: 99 ordinary model/condition checks at body 256, 48 old/new before/after task-identified checks, and 12 post-remapping checks reproduced. Forty-four requests reuse identical checkpoint/data computations; these are not independent replications.

The original 24-run triage did not save its checkpoints. Its arithmetic, code and protocol can be checked, but its historical predictions cannot be independently reconstructed from saved weights. The original six learned-address runs likewise have no own checkpoint file; identically trained causal reruns corroborate their numbers. Historical update counts are recorded in scripts/JSON, not independently proved by optimizer snapshots; training was not rerun.

Repeated controls are substantial: e.g. the 17/two-fact causal baseline, shared-study baseline, collision-study original and alignment-study original have identical saved tensors. Counting them as four independent discoveries would be wrong. There are only three seed values in the later studies. All original input files are fingerprinted in the audit JSON.

**What was independently learned:** the original learned-address controller and shared-projection arm use end-task answer cross-entropy without a WRITE/QUERY parser or matching labels in forward prediction. Their memory operations work in some seeded cases. The controller is still given the number of bank slots and a final query position.

**What used extra help:** the initial hard-addressed hybrid and DeltaRule have grammar/address parsing at inference; both obtain 100% on the original triage, so attention necessity is not established. Alignment-only and combined guidance use true write/query correspondences during training. Diversity-only uses the known query-symbol set and an auxiliary coverage loss, though it has no write/query pairing labels. Faded-guidance models inherit early privileged semantic supervision. New task query embeddings are copies of pretrained old-query embeddings, not unseen-vocabulary zero-shot learning.

The combined guided eight-fact scores are 100%,52.1%,100%; the mean 84.0% is real but hides a weak seed. Gradual fading gives 100%,49.0%,100%, or 83.0% mean on the original set. The final 240-update controls are more informative than comparisons with the earlier 180-update GRU/pair triage. Memory-bank capacity and parameter counts differ from plain GRU/pair, so those comparisons do not isolate architecture quality at equal resource cost.

No answer leakage into the learned forward function was found. Historical train and evaluation seed sets are disjoint. However, the same 96-history evaluation streams were repeatedly used while choosing new mechanisms; they are effectively development/validation sets, not an untouched final test. Pilot source/version hashes and per-example predictions were generally absent before this audit. Those are provenance limitations, not evidence of fabricated measurements.

## The one independent experiment

**Question:** Is long-delay failure caused by soft writes during supposedly idle filler, or by the final query update / some other persistent-state failure?

Frozen saved weights: three seeds 17/29/43, gradual-fade and halfway-removal schedules, eight facts, body lengths 256/1024/4096. Every checkpoint/horizon has 96 fresh histories and four paired inference modes. The fresh seed formula is 5000000000+seed*100003+8*197+chunk_start*677. These streams were not used in the earlier pilots.

The first 32 tokens contain actual writes and updates. The remaining delay-16 history tokens are guaranteed to contain no WRITE tags. The tail-only mode freezes bank updates in that region, but allows the original final-query write. The query-only mode changes only that final update. Both modes together freeze both regions. Learned parameters, read attention and GRU state are unchanged in all modes; no correct answers are supplied. The boundary is known from the generator, so the freeze is explicitly an **oracle diagnostic**, not a learned or generally deployable improvement.

Query-free history states are shared across slot queries for efficiency. Against the original full forward, all 159 reproductions agree; six additional native 4096-token checks cover every tested checkpoint. Their maximum logit discrepancy is 5.13 e-06, with identical sampled predictions. All four arms receive exactly the same histories and zero training updates. Original file hashes were checked again after all execution.

| Schedule | Body length / guaranteed no-write tail | Normal whole recall | Freeze tail only | Freeze query only | Freeze both |
|---|---|---:|---:|---:|---:|
| linear_fade | 256 / 240 | 84.4% | 85.1% | 84.4% | 85.1% |
| linear_fade | 1024 / 1008 | 60.8% | 85.1% | 60.8% | 85.1% |
| linear_fade | 4096 / 4080 | 35.8% | 85.1% | 35.8% | 85.1% |
| fade_by_half | 256 / 240 | 69.1% | 70.5% | 69.1% | 70.5% |
| fade_by_half | 1024 / 1008 | 62.5% | 69.8% | 62.5% | 69.8% |
| fade_by_half | 4096 / 4080 | 36.5% | 69.8% | 36.5% | 69.8% |

At the 4096 condition, the guaranteed no-write tail contains 4,080 tokens:

| Schedule | Seed | Normal correct records | Tail frozen | Query frozen |
|---|---:|---:|---:|---:|
| linear_fade | 17 | 0/96 | 96/96 | 0/96 |
| linear_fade | 29 | 10/96 | 53/96 | 10/96 |
| linear_fade | 43 | 93/96 | 96/96 | 93/96 |
| fade_by_half | 17 | 0/96 | 53/96 | 0/96 |
| fade_by_half | 29 | 13/96 | 52/96 | 13/96 |
| fade_by_half | 43 | 92/96 | 96/96 | 92/96 |

For gradual fade, freezing the tail raises mean whole recall from 35.8% to 85.1% (+49.3 points). For halfway withdrawal it raises 36.5% to 69.8% (+33.3 points). This localizes a material causal failure to tail-time bank updates. It does not establish a new architecture or recovery by an autonomous learned gate.

The strict criterion written before execution required at least 20 percentage-point rescue in **every** seed at 4096. **That criterion FAILS:** seed 43 already scores 96.9%/95.8% normally, so its gain is only 3.1/4.2 points. This ceiling limitation is retained rather than changing the rule after seeing results. The narrower causal contribution is directly supported by the paired rescues in the failing checkpoints. Some records are also harmed (e.g. one halfway/seed 29 record); the intervention is not universally beneficial record by record.

## Relationship to PR #35 and PR #36

These external-memory controllers are not the balanced-pair learning-credit construction. PR #35 separates parameter sensitivities after deliberately identical hidden endpoints; these experiments measure ordinary forward recall using a growing slot bank. No such common-endpoint construction, credit trace, legal-query gradient metric, or theorem-size regime is tested here. Neural recall gains neither validate nor refute that theorem.

The local pair baseline copies PR #36's transition, but uses a shorter local pipeline/budget and is not a full reproduction of that PR. The successful learned-memory and guided models do not use that paired cell. Their improvements cannot be attributed to PR #35 or PR #36. They do provide useful engineering evidence about learned addressing, privileged guidance and accidental overwrites in ordinary external-memory systems.

## Ranked next three priorities

1. **Learn persistence without an oracle inference mask.** Target filler-time false writes first. Train/evaluate a small learned or constrained write gate, with an answer-only control and all extra labels/regularizers disclosed. Require fresh long-delay records, overwrite fidelity and comparable cost. Do not report this audit's frozen-tail scores as achieved by the current autonomous controller.
2. **Establish a fair, reliable learned-addressing gain.** Compare original/shared controllers and guided/unguided controls at matched update/data budgets; report total bank storage, parameters, runtime and plain GRU/LSTM or other ordinary-memory baselines. Reserve a new untouched test generator/seed set; separate initialization from data-seed variability. The present three-seed results are descriptive, not a general superiority finding.
3. **Repair retention/generalization comparisons before extending them.** Keep task IDs, use the same permutation direction in corrected replications, add multiple random permutations, and include an equal-new-exposure control alongside the existing fixed-total-budget rehearsal test. If a PR #35 bridge is proposed, define and charge its explicit learning-credit state before running it; keep it separate from these recall claims.

## Evidence and reproduction

- Script: [independent_audit.py](independent_audit.py).
- All input SHA256 s, checkpoint digests, exact fresh intervention counts,159 replay comparisons and six long-parity checks: [independent_audit_results.json](independent_audit_results.json).
- Original scripts, JSON, checkpoints and reports were preserved; no proofs, other lanes, branches or saved models were edited. No GPU, training, external contact, or extra experiment folder.
- CPU resources for audit/replay/intervention plus targeted long-parity validation: **186.7 wall seconds**, **974.6 process CPU seconds**, six intra-op and one inter-op thread. Runtime excludes initial source inspection and Python/Torch startup.
- Full fresh rerun from repository root, using a new output file:

```powershell
python -B experiments/memory_retrieval_triage_20261020/independent_audit.py --output experiments/memory_retrieval_triage_20261020/independent_audit_recheck.json
```

Existing outputs are refused. The --validate-existing mode rechecks only 4096-token native-forward parity and refreshes validation metadata on the selected audit output; it does not rerun training or all prior inference conditions. The saved source hashes distinguish initial execution from the added native-parity validation and final output/help CLI.
