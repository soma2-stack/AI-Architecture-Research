# Corrected memory-drift diagnostic — October 20, 2026

**Status: FINISHED.** 18 read-only checkpoint evaluations completed: two hint-fade schedules, three seeds, delays 256/1024/4096. CPU six threads; no GPU; no parameter changes. The first version of this probe mistakenly included 16 training-body tokens in its reported filler region. **Do not use `false_write_probe_results.json`; it is superseded by `false_write_probe_corrected_results.json`.** The corrected code uses the actual fact-body boundary (32 tokens) and counts only the generated guaranteed no-write tail.

## Corrected averages across seeds 17/29/43

| Schedule | Delay | Mean write gate on no-write tail | Memory bank cosine similarity to end-of-body |
|---|---:|---:|---:|
| Gradual fade | 256 | 1.63% | 0.974 |
| Gradual fade | 1,024 | 1.66% | 0.895 |
| Gradual fade | 4,096 | 1.72% | 0.534 |
| Hints removed by halfway | 256 | 1.91% | 0.969 |
| Hints removed by halfway | 1,024 | 1.96% | 0.906 |
| Hints removed by halfway | 4,096 | 2.00% | 0.538 |

Cosine similarity near 1 means the bank's direction is nearly unchanged; a decrease indicates drift. This measurement captures soft memory writes during filler, not direct answer accuracy. The model's gate runs on every token, including no-write filler, and even small gate activity can accumulate over thousands of steps.

**Observed:** Longer no-write tails are associated with more bank drift, consistent with the previously measured recall degradation. Seed 43 was more stable than the other seeds, which also matches its better long-delay recall in the small sample.

**Not yet proven:** That accidental writes are the *sole* cause of forgetting. A causal intervention that disables writes only during known filler was planned, but its code-writing action was blocked. **That causal test was not run.** No claim of recovered long-horizon recall is warranted.

## Next decision

Best next experiment is the unrun, inference-only no-write-tail intervention, with the original inference path checked for exact agreement against existing outputs. If freezing filler writes restores recall, consider training a write gate that stays shut on non-write tokens *without using privileged write masks at inference*. Evaluate at 256, 1024, and 4096 tokens against the exact original weights.

Code and authoritative data: `false_write_probe_corrected.py` and `false_write_probe_corrected_results.json`. Earlier recall stress evidence: `fade_long_horizon_results.json`. Original checkpoints preserved.
