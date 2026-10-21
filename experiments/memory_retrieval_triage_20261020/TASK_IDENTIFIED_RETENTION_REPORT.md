# Task-identified retention experiment — 2026-10-20

**FINISHED: 12/12 runs, exit code 0** (414.172 s). Three seeds (17, 29, 43); two starting checkpoints (faded-guidance and unguided shared-addressing); two adaptation regimes (new-only versus old/new rehearsal). Eight binary facts, 256-token delay, 96 held-out histories per condition, 240 updates, 24 generated histories per update, six CPU threads, no GPU.

## Why this fixes the previous test
The earlier remapping reused the same query symbols with contradictory meanings and no task identification, so its old-task decline could not be interpreted as forgetting. In this corrected test, original query symbols 14..21 refer to original write slots, whereas distinct new symbols 32..39 refer to shifted write slots. Both tasks can coexist without ambiguous answers; no explicit write/query pair labels are supplied during adaptation. New symbols' embeddings start as copies of old query embeddings. This is not novel-vocabulary or zero-shot generalization.

## Whole-record recall at 256-token delay (three-seed mean)
| Starting checkpoint | Adaptation | Old mapping BEFORE | Old mapping AFTER | New mapping AFTER |
|---|---|---:|---:|---:|
| Faded guidance | New only | 84.4% | 1.0% | 26.7% |
| Faded guidance | Old/new rehearsal | 84.4% | 62.2% | 25.3% |
| Unguided shared | New only | 59.4% | 1.4% | 24.3% |
| Unguided shared | Old/new rehearsal | 59.4% | 51.4% | 13.5% |

New-mapping baseline before adaptation averaged about 1% whole-record recall. A whole record is counted correct only when all eight queried bits are right. Source precision is 96 histories per seed/arm and three seeds; rounded means.

## Verdict
**PASS:** With distinct task-identifying query tokens, rehearsal substantially preserves old recall during answer-supervised adaptation. Without rehearsal, old recall falls nearly to zero. With the guided starting model, rehearsal costs little new recall (26.7% vs 25.3%). With unguided starting model, it reduces new recall from 24.3% to 13.5%.

**LIMITATIONS:** These are three-seed, synthetic, fixed-token experiments. A/B have distinct query-token vocabularies, adding eight learnable embeddings (256 parameters) to each model. Rehearsal spends half the adaptation examples on old tasks; new-only sees twice as many new-task examples at the same total examples/updates. Previous guided pretraining used privileged matching labels, though adaptation here uses only answer CE. This does not prove fully autonomous addressing, zero-shot pair generalization, or any PR35 theorem claim.

## Evidence
- `task_identified_retention.py`: task-separated adaptation and matched training protocol.
- `task_identified_retention_results.json`: all 12 completed runs.
- `task_identified_retention_weights.pt`: saved adapted checkpoints.

## Next discriminating test
With fixed total examples and update budget, compare old/new ratios (0%, 25%, 50%, 75% old) under at least three seeds, preserving identical evaluation streams. Include per-bit and whole-record recall, memory-bank erasure checks, and a clearly separate unseen-vocabulary test if generalization remains the goal. Do not mislabel new query-to-fact associations as new underlying facts.
