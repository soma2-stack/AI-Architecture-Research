# Post-withdrawal long-delay memory stress test (2026-10-20)

**FINISHED:** six read-only evaluations of the saved models from `faded_guidance_weights.pt`. No retraining, no GPU, six CPU threads. Evaluated eight binary facts with matched held-out histories. Data source: `fade_long_horizon_results.json`.

## Complete-record recall: 32 histories per seed/arm

| Hint schedule | 256 tokens | 1,024 tokens |
|---|---:|---:|
| Gradually fade hints | 83.3% | 65.6% |
| Remove hints halfway | 70.8% | 65.6% |

These averages use 32 held-out histories per seed, not the earlier 96-histories pilot; small sample differences explain the discrepancy between 70.8% here and 68.4% previously. Seeds 17, 29, 43 were unchanged.

The additional **4,096-token** stress check included only seed 17 and 16 histories per schedule: gradual fade 1/16 (6.3%), halfway removal 0/16 (0%). The sample is too small to generalize to all seeds, but it shows that long-horizon reliability cannot be assumed from a 256-token result.

## Memory causality

At 1,024 tokens, zeroing the bank or replacing selective read attention with uniform attention destroyed almost all whole-record recall in these saved models. This establishes that successes depend on learned selective external memory. It does **not** prove the bank remains stable for arbitrarily long no-write gaps.

## Interpretation and next small check

The main new bottleneck is **memory persistence**, not just address assignment: some successfully addressed facts are lost after long distractor tails. The soft memory-write gate updates on every token and can potentially overwrite stored values on ostensibly no-write filler. Measure per-token false write-gate activation and bank drift on no-write tails using the saved checkpoints, before trying any architectural modification. No additional training until the cause is isolated.

Reproduction script: `fade_long_horizon.py`; evidence: `fade_long_horizon_results.json`. CPU 6 threads only, prior files preserved.
