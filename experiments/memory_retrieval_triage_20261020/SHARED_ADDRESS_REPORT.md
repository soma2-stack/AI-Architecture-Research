# Shared Write/Read Addressing: Paired CPU Test (2026-10-20)

## Verdict

**FINISHED: 12/12 CPU runs completed.** The shared-address model improved eight-fact recall but reduced four-fact recall. **MIXED, NOT A GENERAL ADVANCE.**

This experiment tested whether using one trainable projection for both writing and reading solves the address collisions discovered in `address_diagnostic.json`. The control retained separate trainable write/read projections. Both received identical tasks, training budgets, evaluation sets, and six-thread CPU settings. No token-ID parser, write mask, oracle target address, or GPU was used.

## Whole-record recall after 256-token delay

Mean across seeds 17 and 29 (96 held-out histories per seed):

| Facts | Separate read/write (control) | Shared read/write | Change |
|---:|---:|---:|---:|
| 2 | 72.9% | 71.4% | -1.6 percentage points |
| 4 | 65.1% | 35.9% | -29.2 percentage points |
| 8 | 13.0% | 30.2% | +17.2 percentage points |

Seed-level 8-fact accuracy was 0.0% and 26.0% in the control, versus 18.8% and 41.7% with sharing. At four facts, sharing changed 86.5% to 26.0% in seed 17, and 43.8% to 45.8% in seed 29.

## Resources and fairness

- Models: original `LearnedMemoryRNN` versus the same architecture with `model.read_key = model.write_key`. Both learn from the final answer loss.
- Train: 240 updates/model, batch 12, AdamW 0.003, 1.0 gradient clipping, identical seeded data stream.
- Eval: 16/64/256 token delays, 96 held-out histories per model/seed/fact condition.
- CPU: 6 intra-op threads, 1 inter-op thread, CUDA disabled and checked; total experiment wall time 145.515 seconds.
- Trainable parameters: control 11,831–11,903 versus shared 11,435–11,507. This differs because projection weights are tied, so the new model has approximately 396 fewer trainable parameters.
- The state bank scales with configured number of facts: 32 GRU coordinates plus 12 per memory slot. This is not a fixed-memory-cost model as fact count grows.

## Research interpretation

Sharing keys improves some harder eight-slot cases without manually programming addresses, but does not prevent training failure and is markedly worse for four-slot recall on one seed. It is not supported as a universal replacement for independent projections; there are only two training seeds.

Earlier causal tests (`CAUSAL_REPORT.md`) established that the better-performing original learned model uses its memory bank, but other runs can rely on shortcuts. The earlier address probe (`address_diagnostic.json`) documented write/read collisions. This experiment indicates that simply tying read and write address encoders does not reliably repair both collision and optimization problems.

## Files and integrity

- `shared_address_sixthreads.py` — reproducible paired comparison code.
- `shared_address_sixthreads.json` — all 12 detailed results; `complete: true`.
- `shared_address_sixthreads.pt` — saved model weights for all twelve training runs.

**Next narrowly scoped experiment:** examine collisions in the shared-model checkpoints and test an address-separation/coverage objective on the eight-fact task only, with frozen evaluation protocol and matched controls. Preserve failed runs and use at least three seeds before claiming improvement. Do not scale training blindly or infer a PR35 theorem benefit.

## Completed post-training address audit

A separate **read-only** diagnostic was run after the comparison; source and raw measurements are in `shared_address_probe.py` and `shared_address_probe.json`. No additional training was performed.

- **Eight facts, seed 17:** Control mapped eight query tokens to only **3** unique memory destinations; shared model used **6**. The count of same-tag write/read destination matches rose from **0/8** to **5/8**.
- **Eight facts, seed 29:** Control used **7** distinct query destinations; shared model used **8**, and write/read matches rose from **5/8** to **7/8**.
- **Four facts, seed 17:** Control used **4** distinct query destinations, while the shared model used only **2**, explaining an important possible contributor to its severe accuracy drop.

These argmax diagnostics are suggestive, not a full causal proof: soft addresses may distribute mass over several slots, and recurrent/other state can contribute. Combined with the paired held-out tests, however, they show that key sharing changes address collisions and can either help or hurt recall.

**Updated next step:** evaluate a mechanism designed to prevent multiple facts from collapsing into the same read destination. Any auxiliary access to true WRITE/QUERY token IDs or address labels must be declared as an additional inductive advantage, not compared as fully self-learned addressing.
