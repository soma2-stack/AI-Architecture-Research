# Novel write/read pair remapping: completed, 2026-10-20

**FINISHED:** 6 CPU-only adaptation runs: seeds 17/29/43, 8 binary facts, a new circular query-symbol remapping `QUERY_(i+3 mod 8) => WRITE_i`. Each run used 240 answer-loss-only adaptation updates with 12 examples per batch, six CPU threads and the GPU hidden. Evaluated on 96 held-out histories per seed and variant with a 256-token delay. Original checkpoints were preserved.

## Complete-record recall

| Start checkpoint | New mapping before adaptation | New mapping after adaptation | Old mapping after adaptation |
| --- | ---: | ---: | ---: |
| Gradually faded guidance | 0.7% | **25.0%** | 0.7% |
| Unguided shared addressing | 0.7% | **26.7%** | 1.0% |

Per seed new-pair post-adaptation, faded guidance: 6.3%, 10.4%, 58.3%. Unguided: 22.9%, 22.9%, 34.4%. Old-pair performance before adaptation: faded 100.0%, 53.1%, 100.0%; unguided 30.2%, 41.7%, 100.0%.

**CORRECTED INTERPRETATION / INVALID RETENTION CLAIM:** A query-symbol correspondence unseen in pretraining damaged retrieval before adaptation. Answer-only adaptation recovered partial new-mapping recall (25.0% faded versus 26.7% unguided complete-record recall). However, the same QUERY tokens were deliberately assigned contradictory meanings across the old and new tasks, with NO task-identity input. The model cannot determine which answer is requested for otherwise identical input histories. Therefore the observed low old-mapping recall is **not interpretable as catastrophic forgetting or interference**; that conclusion is RETRACTED. The three-seed pilot does not demonstrate a guided-pretraining advantage on new-mapping adaptation. Seed variation remains large.

**Important limitations:** All eight WRITE and QUERY symbols had appeared in pretraining, but the associations were novel; the experiment is not unseen-vocabulary generalization. The model received task-level answer feedback on the new mapping during adaptation, so it does not prove zero-shot learning or autonomous correspondence discovery. Tiny synthetic pilot, three seeds only.

**Evidence:** `novel_pair_adaptation.py`, `novel_pair_adaptation_results.json`, `novel_pair_adaptation_weights.pt`. Prior runs and checkpoints unchanged.

**Next:** First fix task identifiability by supplying an explicit task-context token (or distinct query vocabularies) whenever old and new correspondences coexist. THEN compare new-only adaptation versus interleaved rehearsal at matched updates and measure both mappings. Keep context available at training AND evaluation; otherwise dual-task recall is not identifiable. Separately, to test zero-shot mapping generalization, hold out pairings with a protocol that makes the correct relationship inferable without privileged identity labels. Do not label the original conflicting remap as a forgetting experiment.
