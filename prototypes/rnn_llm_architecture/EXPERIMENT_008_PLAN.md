# Experiment 008 — Does a 16→32→64→128 curriculum improve two-slot memory?

**Status at preregistration:** not trained. This is an exploratory, supervised CPU study; the formal robust learning-credit target `D=Omega(n), mT=o(n^(3/2))` remains **OPEN**, and cannot be settled by this benchmark.

## Falsifiable hypothesis

Experiment 007 found that more native-head training sharply improved protected RNN unequal-value paired accuracy when training at delay 16, while training directly at delay 64 remained near chance. Hypothesis: **short-to-long training may help the model learn selective writes/readout and transfer to delay 128**, better than either keeping all training at 64/128 or intermixing the same short and long examples.

The hardest outcome is *both* values correct when the two slots end with **different values**. Chance from two independent random guesses is ~25%; always repeating the last value yields **0%** on that stratum (and ~50% overall). Report per-slot, overall paired, equal-pair, unequal-pair, loss, and the last-write heuristic alongside this primary metric. A score on the aggregate alone is insufficient.

## Precommitted design

- Models: the **unaltered** protected RNN, GRU, and LSTM (width 32, two layers, vocabulary 16); same original query-token readout, no new architecture/decoder.
- Independent seeds: `17,29,43`.
- All schedules run **240 optimizer updates** at batch 16, AdamW LR `.002`, gradient clipping `1`, on exactly the same synthetic dual-query task as Experiment 007. Two counterfactual A/B queries from an identical prefix are supervised every update; no oracle write masks.
- `curriculum`: 60 updates each at delays **16,32,64,128** in increasing order.
- `shuffled`: a deterministic random permutation of the **same multiset** of 240 delay assignments. The curriculum and shuffled conditions see the **same generated training examples for each (seed, delay, occurrence)**; ordering is the manipulated variable.
- `fixed64`: 240 updates at delay 64.
- `fixed128`: 240 updates at delay 128.
- Initial model seeds, optimizer type/hyperparameters, update count, batch size, training examples, and evaluation sets matched across conditions. The fixed-length controls **do not** have equal number of processed tokens or runtime; report both rather than calling it a compute-matched comparison.
- Train/eval seeds: sample identity is keyed by `(seed, delay, within-delay occurrence)`, independent of model and curriculum schedule. Held-out eval uses `seed+1_000_000`, with no fitting on these examples.
- Evaluate at **16,64,128,256** tokens, without further fitting, using 256 independent prefix histories at each length. Sample and seed variation is important: 3 seeds are not sufficient for a strong general architecture claim.
- Final evaluation only, to avoid human selection of best intermediate stage. Per-stage training loss/length counts are recorded for diagnostics.

There are 3 models × 3 seeds × 4 schedules = **36 conditions**. The experiment is bounded by 720 seconds of global training+evaluation time and a GitHub job timeout of 18 minutes. Every partial/skipped condition and its reason must be saved in the result JSON. No autoretry, no further sweeps, no automatic hyperparameter selection.

## Execution

```bash
python -m pytest -q -o addopts= -p no:cacheprovider prototypes/rnn_llm_architecture/
python -m prototypes.rnn_llm_architecture.experiment_008 \
  --output "$RUNNER_TEMP/rnn-exp008-results.json" \
  --variants protected_w32,gru_w32,lstm_w32 \
  --seeds 17,29,43 --schedules curriculum,shuffled,fixed64,fixed128 \
  --steps-per-stage 60 --batch 16 --eval-examples 256 \
  --max-wall-seconds 720
```

## Interpretation and limitations

- Primary direct scheduling effect: `curriculum` versus `shuffled` (identical token lengths/examples, different ordering).
- Secondary checks: curriculum versus fixed64/fixed128 (equal optimizer updates but different token exposure and throughput).
- Compare models descriptively; equal hidden width does **not** ensure equal parameters/FLOPs.
- If the curriculum improves 16 but fails 128, the longer-memory selective write problem persists. If it outperforms shuffled, replicate with more seeds and harder tasks before claiming anything general.
- All data are small, synthetic, task-specific; no language modeling or new architectural mechanism is established.
- Preserve existing experiments 001–007, repository governance, frozen baselines, `AGENTS.md`, and draft PR #23. Do not merge or touch `main`.
