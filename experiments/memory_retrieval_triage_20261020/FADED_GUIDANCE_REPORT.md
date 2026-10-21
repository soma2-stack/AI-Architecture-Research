# Training-hint withdrawal pilot (2026-10-20)

**FINISHED:** 18/18 new CPU-only training runs across seeds 17, 29, 43 and 2/4/8 binary facts. Six intra-op CPU threads, GPU disabled, 240 updates per run, same seeded training histories and evals as earlier comparisons.

## Mean complete-record recall at 256-token delay

| Facts | Shared, no guidance | Always guided | Gradually fade guidance | Remove by halfway |
|---:|---:|---:|---:|---:|
| 2 | 80.9% | 100.0% | **100.0%** | **100.0%** |
| 4 | 31.9% | 83.7% | 83.0% | **84.7%** |
| 8 | 53.5% | **84.0%** | 83.0% | 68.4% |

Averages over three seeds, 96 independent held-out histories per seed/condition; correct means all facts queried correctly.

### Interpretation

The gradual fade schedule almost matched always-on training guidance, including eight-fact recall: 83.0% versus 84.0%. Removing hints halfway was less reliable with eight facts. Individual seeds remain variable: gradual fade eight-fact complete-record scores were 100.0%, 49.0%, 100.0%; halfway removal was 57.3%, 47.9%, 100.0%.

These fade schedules **do not demonstrate autonomous discovery** of the WRITE/QUERY relationship. Both received the true token pairing during early training; the first schedule applied gradually declining guidance until near the last update, and the second turned it off halfway. **No guidance at evaluation** was true of every earlier supervised condition as well. The useful result is *retention after reducing or ending training-time hints*, not learning the relation unaided.

The 8-fact learned memory bank costs 12 values per configured fact plus a 32-wide GRU, and tests cover fixed binary tags at delays up to 256 only. Seed count is three; no broad generalization claim and no PR35 theorem validation.

### Evidence and reproduction

- `faded_guidance.py`, `faded_guidance_results.json` and `faded_guidance_weights.pt`: two withdrawal schedules, all 18 complete runs.
- `write_read_alignment_results.json` and `alignment_seed43_results.json`: always-on and no-guidance controls.
- No existing models or results were overwritten. CPU-only six threads; wall time 220.89 seconds.

**Recommended next small falsification:** test the saved faded models at longer no-write horizons (1024 and 4096 tokens), and erase the bank on selected histories to verify whether memory—not recency shortcuts—is responsible. This is a read-only diagnostic using existing checkpoints.
