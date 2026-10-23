# Experiment 009 — results: why two-slot memory failed

**Status:** complete. 75/75 preregistered local CPU runs (`complete`, 0 skipped,
0 errors, 2,256 s, 4 workers × 1 thread) plus an independent hosted
replication of all 75 runs ([GitHub Actions run 37722877885](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37722877885),
conclusion `success`, 219/219 tests passed on each of 5 hosted jobs).
Preregistration: [`EXPERIMENT_009_PLAN.md`](EXPERIMENT_009_PLAN.md), committed in
`2c61215` before any confirmatory run; the source SHA-256 hashes stored inside
the results JSON match that commit. Local suite after adding the report
generator: **221/221 tests passed** (176 pre-existing + 45 new).

**Scope:** synthetic two-slot supervised task, width-32 two-layer models.
Not a language model, not a novelty claim, and no bearing on
`D=Omega(n), mT=o(n^(3/2))`, which remains **OPEN**.

Evidence files: [raw local JSON](reports/experiment_009_results.json)
(SHA-256 `f01fefd3a43d3648b25a31e56892d38c61d1ec2f4f9a6b72a3eb374e9367dba6`) ·
[all generated tables](reports/experiment_009_tables.md) ·
[hosted per-run lines](reports/experiment_009_hosted_lines.jsonl) ·
[local stdout](reports/experiment_009_local_stdout.txt) ·
[Phase A exploratory evidence](reports/experiment_009_exploratory/README.md).
Every table below is produced by
`python -m prototypes.rnn_llm_architecture.experiment_009_report reports/experiment_009_results.json --hosted reports/experiment_009_hosted_lines.jsonl`.

## Answer

**The two-slot failure of Experiments 004–008 was not an architectural
incapacity of the protected RNN.** It had three separable causes:

1. **An optimization plateau.** Every gated model first learns "answer both
   queries with the last write" (70–99% identical answers to `QUERY_A` and
   `QUERY_B` at 250 updates; 91–98% in the protected family), a symmetric saddle in which improving the
   untouched-slot query hurts the updated-slot query (Phase A gradient cosine
   −0.61 and −0.85). The unchanged original protected model leaves it between
   500 and 750 updates in 5/5 seeds and then scores **100%** on A≠B pairs at the
   training length. Experiments 004–008 stopped at 150–350 updates — on the
   plateau.
2. **A fixed-timing training task.** The legacy generator always places the
   single update at the midpoint. Trained on it, the protected model is
   length-specific (legacy 128: 42.0%, 256: 30.3%); trained on randomized update
   positions/counts it transfers (legacy 128: 100%, 256: 91.8%) — +58 and +61.5
   points, positive in 5/5 seeds.
3. **The protected retention mechanism is not what stores the values.** The
   learned slow gates never close: layer-0 gates stay ≈0.05 on every token type
   (the `sigmoid(-3)` initialization), implied surviving fraction after 512
   non-write tokens ≤4e-11. The pair is held by recurrent dynamics. Removing
   slow retention entirely (`protected_no_retain_w32`) learns equally and
   generalizes *better* to 8× length (5/5 vs 2/5 seeds).

Slot routing/addressability was **not** the bottleneck: an oracle that only
closes gates between writes (no slot identity) solves the task, while routing
without closure did not (Phase A), and giving the gate the previous token
(`protected_shift_w32`) made 8× transfer worse (1/5 seeds).

A standard GRU solves the same task as reliably at the training length and
generalizes comparably: GRU-32 5/5 at 4×, 4/5 at 8×; parameter-matched GRU-24
5/5 at 4×, 3/5 at 8×. The protected family's best 8× results come from two
variants that *disable* its slow channels in different ways.

## Primary metric — A≠B both-correct, mean of 5 seeds (seeds ≥90%)

Trained at delay 64 (body length; total prefix 68). 32 is shorter than
training; 128/256/512 are unseen longer lengths (2×/4×/8×).

| Arm | Params | State floats | 32 | 64 | 128 | 256 | 512 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `protected_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 94.4% (4/5) | 84.2% (2/5) |
| `protected_no_retain_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.9% (5/5) | 96.5% (5/5) |
| `protected_shift_w32` | 8,016 | 128 | 100.0% (5/5) | 100.0% (5/5) | 99.9% (5/5) | 83.6% (1/5) | 67.1% (1/5) |
| `protected_hard_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.0% (5/5) |
| `protected_hard_shift_w32` | 8,016 | 128 | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) |
| `tanh_w32` | 4,864 | 64 | 0.1% (0/5) | 0.2% (0/5) | 0.1% (0/5) | 0.0% (0/5) | 0.1% (0/5) |
| `gru_w32` | 13,376 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.5% (5/5) | 92.1% (4/5) |
| `lstm_w32` | 17,600 | 128 | 80.2% (4/5) | 80.6% (4/5) | 80.6% (4/5) | 70.7% (2/5) | 51.8% (1/5) |
| `gru_w24` | 7,728 | 48 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.1% (5/5) | 90.0% (3/5) |
| `lstm_w20` | 7,160 | 80 | 90.6% (4/5) | 90.5% (4/5) | 90.0% (4/5) | 83.9% (3/5) | 70.9% (1/5) |
| `gru_keep3_w32` | 13,376 | 64 | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 79.8% (4/5) | 72.3% (2/5) |
| `gru_hard_w32` | 13,376 | 64 | 3.0% (0/5) | 1.7% (0/5) | 2.2% (0/5) | 1.8% (0/5) | 1.3% (0/5) |

**Upper-bound diagnostic, not an architecture** (true write events supplied):
`oracle_tag_protected_w32` 100.0% (5/5) at every length.

**Rule baselines on the same held-out histories:** random 23.5–25.6%; last
marked write 0%; last bit token 0%; initial values only 37.4–40.2%; sticky
address (unmarked bits written to the last named slot) 32.8–46.1%. Every
solved run is far above all of them; `tanh_w32` and `gru_hard_w32` are below
random because they give the same answer to both queries.

Per-seed values at 512 (17/29/43/59/71): protected 100/57.7/100/83.3/79.8;
no-retain 100/96.0/99.6/94.6/92.1; hard 100/95.2/100/100/100; GRU-32
96.6/100/74.6/95.3/94.0; GRU-24 100/100/70.4/100/79.4. The single failed
`protected_hard_shift_w32` seed (29) scored 0% at every length. Full per-seed
tables: [`reports/experiment_009_tables.md`](reports/experiment_009_tables.md).

## Plateau, then escape

Mean held-out A≠B both-correct at the training length, by update:

| Arm | 250 | 500 | 750 | 1000 | 1250 | 1500 | 1750 | 2000 | same answer to A and B, 250 → final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `protected_w32` | 1.4% | 39.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 98.0% → 50.5% |
| `protected_no_retain_w32` | 3.7% | 38.8% | 60.2% | 60.7% | 96.5% | 100.0% | 100.0% | 100.0% | 91.1% → 50.5% |
| `protected_shift_w32` | 3.4% | 78.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 95.1% → 50.5% |
| `protected_hard_w32` | 1.8% | 21.2% | 33.6% | 71.5% | 80.7% | 80.1% | 100.0% | 100.0% | 97.1% → 50.5% |
| `protected_hard_shift_w32` | 2.2% | 20.1% | 41.0% | 60.0% | 60.0% | 65.3% | 80.0% | 80.0% | 95.8% → 60.4% |
| `gru_w32` | 4.5% | 87.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 92.3% → 50.5% |
| `gru_w24` | 7.9% | 25.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 81.8% → 50.5% |
| `lstm_w32` | 10.6% | 7.1% | 1.1% | 14.2% | 40.8% | 51.5% | 79.2% | 80.2% | 76.3% → 59.3% |
| `lstm_w20` | 13.9% | 12.3% | 1.4% | 18.2% | 35.2% | 60.6% | 80.1% | 89.4% | 69.7% → 55.7% |
| `gru_keep3_w32` | 0.3% | 1.2% | 0.2% | 0.8% | 34.5% | 40.2% | 41.8% | 80.0% | 98.8% → 60.4% |
| `oracle_tag_protected_w32` (diagnostic) | 42.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 77.7% → 50.5% |

50.5% "same answer" at the end is correct behaviour: it is the fraction of
held-out histories with A=B. Median first checkpoint ≥90%: oracle 500, GRU-32
500, protected 750, GRU-24 750, no-retain 750, hard 1000, LSTM-32 1500,
LSTM-20 1500. A retention prior (`gru_keep3_w32`, keep-gate bias +3) *slowed*
GRU learning and left one seed on the plateau.

## Training task: legacy fixed-timing versus randomized

Evaluated on the Experiment 004–008 generator (one update at the midpoint,
benign fillers), A≠B both-correct:

| Model | Trained on | legacy 64 | legacy 128 | legacy 256 | two-slot 64 | two-slot 256 |
|---|---|---:|---:|---:|---:|---:|
| `protected_w32` | randomized two-slot (5 seeds) | 100.0% | 100.0% | 91.8% | 100.0% | 94.4% |
| `protected_w32` | legacy (5 seeds) | 100.0% | 42.0% | 30.3% | 11.3% | 11.1% |
| `gru_w32` | randomized two-slot (5 seeds) | 100.0% | 100.0% | 100.0% | 100.0% | 99.5% |
| `gru_w32` | legacy (5 seeds) | 80.7% | 80.8% | 73.1% | 33.2% | 18.5% |

With 2000 updates even legacy training solves legacy 64 (protected 5/5), so the
legacy task was learnable; what it teaches does not transfer in length. The
two-slot columns for legacy-trained models are a distribution shift (they never
saw unmarked bits or multiple updates) and are shown only for completeness.

## How the memory is held

| Arm | Layer | mean write gate: marked value / unmarked bit / WRITE / distractor | exact-zero on distractors | implied retention after 512 non-write tokens |
|---|---:|---|---:|---:|
| `protected_w32` | 0 | 0.049 / 0.049 / 0.055 / 0.046 | 0.00 | 1.3e-11 |
| `protected_w32` | 1 | 0.176 / 0.102 / 0.219 / 0.107 | 0.00 | 6.4e-31 |
| `protected_no_retain_w32` | 0 / 1 | gate is overridden to 1 (no retention) | — | — |
| `protected_hard_w32` | 0 | 0 / 0 / 0 / 0 (never opens) | 1.00 | 1 (channels unused) |
| `protected_hard_w32` | 1 | 0.205 / 0.384 / 0.162 / 0.434 | 0.57 | 0 |
| `gru_w32` (overwrite fraction `1-z`) | 0 | 0.563 / 0.555 / 0.614 / 0.533 | 0.00 | 9.5e-179 |
| `oracle_tag_protected_w32` | 0 / 1 | 0.071, 0.193 at marked values; 0 elsewhere | 1.00 | 1 |

(The no-retain row is by construction; the report generator shows the
unused sigmoid values.) Findings:

- In no learned model does the "protected" write gate close. Layer-0 gates of
  the original cell never leave their initialization and are identical for
  A-writes, B-writes, unmarked bits and distractors, as §3.1 of the plan
  predicts for input-only gates. Layer 1 learns at most ≈10× contrast
  (seeds 59/71: 0.22 at marked values vs 0.02 on distractors), still far from
  closure.
- GRUs overwrite about half of every unit at every token and still recall
  both values 512 tokens later; the stored pair must therefore be re-created
  by the recurrent map each step — a self-sustaining (attractor-like) code,
  not a held coefficient.
- `protected_hard_w32` never opens its layer-0 gates in any seed: its layer-0
  slow subspace is permanently zero, an accidental structural ablation, and its
  layer-1 channels are either fully overwritten or exactly held. Both variants
  that remove slow *leaky* integration — hard (as described) and no-retain
  (always fully overwritten) — transfer to 8× in 5/5 seeds, while the original
  soft leaky channels (time constant ≈20 tokens) transfer in 2/5. This is a
  correlation across three variants, not an isolated causal test.
- With token shift, 3 of 5 hard-gated seeds (29, 59, 71) learned an **exact
  tag gate** in layer 0 — exactly one of 8 channels opens only at marked value
  tokens and is exactly closed elsewhere — i.e. the oracle's pattern, found by
  learning. It did not make learning faster (H5) and seed 29 still failed.

**Frozen-state linear probes** agree with native readout: fit at 64 and applied
unchanged at 256, 90.6% (protected), 99.9% (no-retain), 100% (hard), 99.0%
(GRU-32). No hidden-but-unread memory was found in solved models.

**State-perturbation test** (noise added to the whole recurrent state after the
last write; query immediately or after 64 more distractor tokens, A≠B
both-correct, solved seeds): at 0.5×RMS the protected family, GRUs and the
oracle stay ≥98% with or without the tail (LSTMs 88–97%); at 1.0×RMS accuracy
falls to 72–93% immediately and does not recover within 64 tokens (changes
after the tail −6.5 to +1.5 points; protected 92.7% → 91.7%, GRU-32 93.4% →
86.9%, oracle 90.5% → 90.2%). The preregistered H4 rule (tail ≥ immediate and ≥90% at 0.5×)
is computed below, but 0.5× noise barely damages any model, so the rule mostly
measures ±1-point noise: **H4 is inconclusive as designed.** The data show
wide basins, not active recovery.

## Preregistered decisions (computed by `experiment_009_report.py`)

- **H1 (budget/plateau): SUPPORTED.** `protected_w32` solves 64 in 5/5 seeds;
  A≠B at 250 updates: 0.9%, 0.0%, 3.9%, 0.8%, 1.5%.
- **H2 (fixed-timing task): SUPPORTED.** Legacy-task A≠B, randomized-trained
  minus legacy-trained `protected_w32`: 128 → +58.0 points (5/5 seeds
  positive); 256 → +61.5 points (5/5).
- **H3 (protected retention unused): SUPPORTED.** No-retain solves 64 in 5/5
  (protected 5/5); max implied 512-token retention over solved protected runs
  and layers 4.3e-11.
- **H4 (error-correcting memory):** rule outcome SUPPORTED for protected,
  hard, hard+shift, GRU-24 and the oracle; NOT SUPPORTED for no-retain, shift,
  GRU-32, LSTM-32, LSTM-20, keep-bias GRU. Treated as **inconclusive** (ceiling
  effect, above).
- **H5 (learned exact closure ≈ oracle): FALSIFIED** for both hard variants:
  reached 90% by the oracle median + 250 updates (= 750) in 1/5 (hard) and 2/5
  (hard+shift) seeds. Hard gating did, however, give the best 8× transfer
  (5/5), for the structural reason above.
- **H6 (descriptive), seeds solved at 64 / 512:** protected 5/2; no-retain 5/5;
  shift 5/1; hard 5/5; hard+shift 4/4; tanh 0/0; GRU-32 5/4; LSTM-32 4/1;
  GRU-24 5/3; LSTM-20 4/1; keep-bias GRU 4/2; hard-keep GRU 0/0. By the
  preregistered descriptive rule no-retain and hard are "better" than GRU-32
  (5/5 vs 4/5 at 512, equal at 64) — a one-seed difference over 5 seeds, **not
  statistically meaningful**. The original protected cell is worse than GRU at
  8× (2/5 vs 4/5).

## Hosted replication and numerical sensitivity

Same code, seeds and configuration on GitHub-hosted CPUs (torch 2.14.1+cpu
wheel, Python 3.12) versus local (torch 2.14.1+cu130 wheel executing on CPU,
Python 3.13):

| Arm | Solved 64 local / hosted | Solved 512 local / hosted | Mean abs. diff | Seed-runs whose solved status differs |
|---|---:|---:|---:|---:|
| protected, no-retain, shift, hard, tanh, GRU-32, GRU-24, keep-bias GRU, hard-keep GRU, oracle, both legacy arms | identical counts | identical counts | 0.0–1.8 pp | 0 |
| `lstm_w32` | 4 / 4 | 1 / 1 | 1.9 pp | 1 |
| `protected_hard_shift_w32` | 4 / 5 | 4 / 4 | 19.1 pp | 1 (seed 29 failed locally, solved hosted) |
| `lstm_w20` | 4 / 3 | 1 / 1 | 17.0 pp | 2 (seed 17 solved locally, 72% hosted) |

All conclusions above hold in both environments. Floating-point differences
between PyTorch builds change the *outcome* of individual seeds only for arms
that escape the plateau late or erratically (LSTMs, hard+shift); conclusions
that rest on one such seed are fragile.

## Comparison with earlier experiments (A≠B both-correct, original protected model)

| Experiment | Updates | Task | Delay 64 | Longer |
|---|---:|---|---:|---|
| 004 | 240 | legacy, dual query | 3.3% | 256: 0.0% |
| 005 | 200 | legacy | 2.6% | 256: 0.0% |
| 007 | 200 + 150 | legacy | 2.1% | 256: 0.0% |
| 008 | 240 (curriculum) | legacy | 1.5% | 128: 1.8% |
| **009** | **2000** | randomized, conflicting unmarked bits, 1–3 updates | **100% (5/5)** | 256: 94.4% (4/5); 512: 84.2% (2/5) |
| 009 legacy-trained | 2000 | legacy | legacy 64: 100% (5/5) | legacy 128: 42.0%; 256: 30.3% |

Experiment 008's curriculum allotted 60 updates per stage; the plateau lasts
≈500–750 updates, which explains that negative result without implying that
curricula never help.

## What changed (all isolated; originals untouched)

- `event_gated.py`: `EventGatedProtectedCell`/`EventGatedLanguageModel`
  (straight-through Heaviside slow gate; optional previous-input gate term
  carried in `ShiftState`), `StraightThroughGRUCell`/`KeepGatedGRULanguageModel`.
  All start from the exact seeded weights of the original models; soft/no-shift
  is bit-identical to `protected_w32`.
- `experiment_009.py`: randomized two-slot task with independent replay labels,
  shortcut baselines, oracle masks (diagnostic only), learning curves, length
  transfer, legacy evaluation, probes, gate statistics, perturbation test,
  multiprocess runner with wall cap and exclusive-create output.
- `experiment_009_report.py`: read-only table and decision renderer.
- Tests: `test_event_gated.py`, `test_experiment_009.py`, `test_experiment_009_report.py`
  (45 new tests; the last checks that the committed JSON regenerates the
  committed tables exactly).
- Workflow: `.github/workflows/rnn-exp009-cpu.yml` (per-seed hosted replication).

## Classification under AGENTS.md

- **Event-gated variants (hard straight-through gate, token shift, hard-keep
  GRU): not novel / existing mechanism** — Skip RNN, HM-RNN COPY, the
  straight-through estimator, RWKV token shift, H3/Mamba short convolutions.
- **Protected memory as an architecture candidate on this task:** the
  mechanism-removal test fails the "material difference" gate — removing slow
  retention preserves the capability and improves 8× transfer, and the learned
  model does not use gate-closure retention. No architectural property of the
  protected cell was shown to survive decomposition here.
- **"Explicitly addressed protected memory"** was deliberately not built: the
  diagnostics place the bottleneck in closure and optimization, not in
  addressing (routing-only oracle failed, closure-only oracle succeeded, token
  shift did not help). Its closest prior art is addressed slot memory (NTM;
  Recurrent Entity Networks) and key–value delta-rule memory (fast-weight
  programmers, DeltaNet); with two slots there is nothing for it to fix.

## Theory boundary

The hard gate's straight-through gradient is a surrogate, closed channels give
exact identity Jacobian blocks, token shift enlarges the state beyond `n`, and
all weights are trained — so none of the frozen dense-tanh legal-query
assumptions apply to the new variants. Nothing here bears on
`D=Omega(n), mT=o(n^(3/2))`; it remains **OPEN**, and no historical theorem
claim was changed.

## Unresolved

- **Learnable exact closure.** The oracle shows what exact closure buys (5/5 at
  every length; fastest learning). Gates that start closed under a
  straight-through estimator mostly never open (layer 0 in 7 of 10 hard runs).
  Whether a gate that starts open, or anneals from soft to hard, can learn the
  oracle's pattern reliably is untested.
- **Why the original's soft slow channels hurt 8× transfer** is a correlation
  across variants, not an isolated test.
- **Capacity.** Two binary slots fit easily in a 32-dimensional attractor code.
  Whether attractor memory degrades with more slots or larger value alphabets —
  where gate-closure memory could plausibly matter — is unknown.
- **Error correction** (H4) needs a stronger perturbation design.
- 5 seeds, one width, one learning rate, synthetic task only.

## Recommended Experiment 010 (not run)

**Capacity scaling of attractor versus closure memory.** Same randomized task
generalized to K ∈ {2, 4, 8} independently updated slots and 2- or 4-valued
contents at fixed width 32 (plus width 64 for the best arm), training budget
set from this experiment's learning curves (≈3,000–4,000 updates), lengths 1×–8×.
Arms: `protected_w32`, `protected_no_retain_w32`, GRU-32 and parameter-matched
GRU, a key–value delta-rule memory baseline (prior art for addressed
overwrite), `tag` and `route` oracles as upper bounds, and one learnable
exact-closure gate that starts open (soft-to-hard annealing). Primary metric:
all K slots correct on histories whose final values are not all equal.
Decisive question: at what K does learned recurrent memory fall below the
oracle, and does any learnable closure mechanism close that gap? If learned
models match the oracle up to K=8, protected memory has no remaining
engineering role on this task family and the line should be closed.

## Resources

CPU only. Local: 4-core container, 4 workers × 1 thread, 2,256 s for 75 runs.
Hosted: 5 jobs, 381–901 s per study step. Phase A diagnostics and pilots used
roughly one additional CPU-hour (estimated from per-run timings). No GPU, no
external data, no changes to `main`, `AGENTS.md`, earlier experiments or other
research lanes.
