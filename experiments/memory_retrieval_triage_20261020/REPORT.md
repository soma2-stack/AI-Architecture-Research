# Selective Retrieval Memory — CPU Diagnostic (2026-10-20)

## Outcome

**PASS (execution):** 24/24 training-and-evaluation configurations completed with finite losses. Four architectures were trained for 180 optimizer updates for each of 2 seeds and 2/4/8 fact counts, and tested at delays 16/64/256.

**PASS (structured recall):** Both the task-specific addressable hybrid and the existing DeltaRule baseline achieved 100% whole-record recall at every tested fact count, delay and seed.

**FAIL (distinctive hybrid advantage):** The hybrid did **not** beat DeltaRule. Both were explicitly given the WRITE/QUERY token format and used slot-indexed external memory, unlike the plain GRU and PR36 surrogate. Perfect scores in this setting do not demonstrate better general language-model architecture, better self-learned addressing, or transfer of PR35's theorem.

**FAIL (plain recurrent recall on this budget):** At delay 256, neither the GRU nor the PR36-style pair model recovered complete 8-fact records in any of 192 held-out histories across two seeds.

**INCONCLUSIVE:** Learned, unassisted address discovery; any improvement caused by attention rather than explicit addressing; longer training; scaling; generalization beyond 8 slots or 256 tokens; theorem-to-model bridge.

## Experimental contract

- Source: `experiments/memory_retrieval_triage_20261020/run.py`; raw measurements: `results.json`.
- Reused PR23 `capacity_010` training histories, exact label replay and token-query expansion. Training at body length 16; held-out tests at 16, 64 and 256 using no-write tails (respectively 0, 48, 240 tokens).
- Two seeds (17 and 29); 96 held-out histories per seed, model, fact count and delay, all fact slots queried. Two-valued independent facts, with tagged overwrite updates in the initial distractor body.
- 180 AdamW steps per model/seed/slot condition, batch 12, learning rate .002; gradient clipping 1.0. Same seeded training histories for all models within each seed and fact count.
- PyTorch CPU-only (CUDA intentionally hidden and checked unavailable), 4 intra-op threads, 1 inter-op thread; no training on GPU. Results are a deliberately inexpensive pilot, not an architecture-level significance test.
- The PR36-style `pair` cell copies its state transition from `prototypes/pr35_memory/model.py` at 472ea492, hosted on PR36. Other modules reuse the already-local PR23 code. This is a local reimplementation, not a byte-for-byte replay of PR36's full 600-step pipeline.

## Whole-record recall (%), mean of the two seeds

| Facts | Model | Delay 16 | Delay 64 | Delay 256 | Trainable parameters | Counted recurrent-state scalars / example |
|---:|---|---:|---:|---:|---:|---:|
| 2 | GRU | 42.2 | 27.1 | 23.4 | 7,488 | 32 |
| 2 | PR36 pair | 39.1 | 28.1 | 25.5 | 2,757 | 32 |
| 2 | Addressable hybrid | 100.0 | 100.0 | 100.0 | 7,499 | 56 |
| 2 | DeltaRule | 100.0 | 100.0 | 100.0 | 130 | 64 |
| 4 | GRU | 6.3 | 3.1 | 3.6 | 7,488 | 32 |
| 4 | PR36 pair | 10.9 | 7.3 | 4.7 | 2,757 | 32 |
| 4 | Addressable hybrid | 100.0 | 100.0 | 100.0 | 7,523 | 80 |
| 4 | DeltaRule | 100.0 | 100.0 | 100.0 | 130 | 128 |
| 8 | GRU | 0.5 | 0.5 | 0.0 | 7,488 | 32 |
| 8 | PR36 pair | 0.0 | 0.5 | 0.0 | 2,757 | 32 |
| 8 | Addressable hybrid | 100.0 | 100.0 | 100.0 | 7,571 | 128 |
| 8 | DeltaRule | 100.0 | 100.0 | 100.0 | 130 | 256 |

For the 8-fact/256-token condition, chance independent whole-record guessing is about 0.39%, and random bit accuracy is 50%. Observed GRU and pair bit accuracy were 49.5% and 51.2%, respectively. Rounded percentages can hide a small number of successes in other conditions; consult `results.json` for exact per-seed counts.

## What the comparison actually means

The hybrid contains a learned GRU plus a slot-indexed memory bank of 12 numbers per fact, uses WRITE-tag parsing supplied by the experiment designer, and uses attention to retrieve a slot on QUERY. The DeltaRule reference is even simpler: it directly parses write tags, stores a learned value embedding per slot, and reads the indexed slot. This second model has **no Transformer-style attention**, yet attained the same 100% recall. The inference that attention improves recall **does not follow** from the observed scores.

The comparison therefore establishes that **explicit external addressing solves this synthetic fact task much more reliably at a short budget**. It does not establish that our hybrid RNN learned to manage memory addresses on its own or is cheaper than a standard architecture at equal capability. It also does not test PR35's exact-real learning-credit theorem.

The 'state scalars' column deliberately counts only model recurrent state and slot bank, not weights, transient activations, program overhead or CPU runtime. A direct wall-time comparison is confounded by the unfused Python implementations and different mechanisms.

## Design issues / corrections for future experiments

1. **Remove the oracle-style address advantage:** learn address and write decisions from tokens with a shared, differentiable controller, then hold out token re-labelings/new slot IDs. Don't compare an explicitly parsed design against an unrestricted GRU as if they had equal information.
2. **Ablate attention:** compare the same GRU-plus-bank using direct indexed retrieval (no attention) versus content-based attention under identical token access and state budgets. Our DeltaRule result already makes attention's necessity doubtful.
3. **Charge storage honestly:** include the full external memory bank and scaling with fact count, parameter bytes, runtime and training budget. Challenge it with distractors, collisions, updates, unknown slot counts and longer no-write holds.
4. **Use PR35 faithfully or keep it separate:** PR35 studies parameter-sensitivity learning credit with common endpoints, not generic forward recall. To test a theorem-derived mechanism, specify and cost the persistent credit trace needed to carry history through identical hidden endpoints.
5. **Do not fund long training by default:** run a new model only after specifying which mechanism-level gap it addresses and the falsification criterion.

## Reproduction

From the repository root, run this script after selecting a new output filename so the recorded data are preserved:

```powershell
$env:CUDA_VISIBLE_DEVICES="-1"
python -B experiments/memory_retrieval_triage_20261020/run.py --steps 180 --batch 12 --histories 96 --seeds 17,29 --slots 2,4,8 --output experiments/memory_retrieval_triage_20261020/recheck.json
```

Existing `results.json` is protected against accidental overwriting. The script is kept as one file and imports existing PR23 modules. No new Git branch or PR was created; pre-existing audits and code were left unchanged.

## TL;DR

**What happened:** 24 cheap CPU comparisons completed. **Worked:** explicit slot-addressed memory got all tested records right. **Did not work:** GRU and PR36 pair recall remained weak, and attention showed no advantage over DeltaRule. **Learned:** the important difference was built-in write/read addressing, not a novel RNN trick. **Next:** test learned addressing with fair memory/state budgets; don't simply scale up training.
