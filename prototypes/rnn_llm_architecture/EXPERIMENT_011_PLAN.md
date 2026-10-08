# Experiment 011 — does a longer training budget solve four binary memory slots?

**Status: preregistered before the confirmatory run.** Controlled optimization-versus-capacity
screen. It does not propose or modify any architecture and makes no novelty claim. The formal
`D=Omega(n),mT=o(n^(3/2))` question remains OPEN. Executes on the owner's local CPU (launcher
`E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1`), not GitHub Actions.

## Question (fixed; not to be changed after seeing results)

Experiment 010 stopped at 800 updates, where all learned models scored ≈0% whole-memory accuracy on
4 slots × 2 values. Experiment 009 showed 2-slot plateaus lasting 500–750 updates. **Does extending
the training budget to 3,000 updates let the existing recurrent architectures learn four independent
binary memory slots?** Low accuracy after insufficient training is not evidence of a capacity limit.

## Task (unchanged from Experiment 010)

`capacity_010` generator, replay labels, models and optimizer are imported unchanged: 4 slots, 2
values; every slot initialized in random order, 64 body tokens with 25 % decoy VALUE tokens, 1–3
randomized marked rewrites per history; one query per slot from the same prefix. AdamW lr 0.002,
clip 1.0, batch 12 histories (×4 queries), width-32 two-layer models.

## Conditions

| Group | Model | Parameters | Role |
|---|---|---:|---|
| learned | `protected` (original protected RNN) | 8,016 | primary |
| learned | `protected_no_retain` (no slow retention) | 8,016 | primary |
| learned | `gru24` (≈ parameter-matched GRU) | 8,112 | primary |
| learned | `gru32` (equal width GRU) | 13,888 | optional, included |
| reference | `delta_rule` (explicit-address, grammar-aware) | 130 | **separate reference only**; never counted as a fair learned comparison |

Seeds **17, 29, 43** (paired). For a given seed every model receives the byte-identical training
stream (training seed depends only on seed and step; SHA-256 of the full stream is stored per run
and tested) and the identical held-out evaluation histories. Model initialization uses the same seed.
Architecture definitions are not altered.

## Procedure and decision rules (fixed in advance)

1. **Pilot** (done, seed 17, 400 updates, all five models; scratch outputs outside the repository):
   timing ≈ 25 s / 400 updates; stream hashes identical across models; all learned models still on
   the plateau (loss 0.65–0.70, whole-varied ≈ 0 %). The pilot cannot rank any condition.
2. **Extension decision:** because every learned condition is unresolved at 400 updates and the full
   budget is cheap (≈ 4 min per run), *all* learned runs go to **3,000 updates** — no pruning by pilot
   outcome, to avoid selection bias. The reference model is also run to 3,000 for completeness.
3. **Confirmatory run:** 15 runs (5 models × 3 seeds), ≈ 10 single-thread workers (one run per
   worker; measured best throughput 10–12 workers), `--max-wall-seconds` 1,800 per run.
   Total experiment budget **60 minutes**; if exceeded, partial results are preserved with
   `status` recorded and the limitation reported. No re-runs with altered settings.
4. **Evaluation** on held-out histories (256 each, disjoint seeds, same for every model): delays
   **64, 128, 256, 512** tokens (training delay 64), reporting all-slot exact accuracy (`whole`),
   `whole_varied` (histories whose final values are not all equal) and per-slot accuracy.
5. **Tracking:** mean training loss per 50-update window; held-out delay-64 accuracy every 250
   updates (128 histories); parameter counts; wall and CPU time; training token positions.
6. **Controls on the same evaluation histories:** independent-guess baseline (analytic per-slot ½,
   whole 1/16; empirical guess also stored) and last-written-value copy baseline.
7. **Definitions.** *Solved at length L*: seed `whole_varied` ≥ 90 % at delay L. Condition "solves
   four-slot recall" only if ≥ 2 of 3 seeds are solved at delay 64. A "plateau exit" is the first
   checkpoint with held-out per-slot ≥ 70 % at delay 64. *Protected outperforms GRU* only if
   protected's mean `whole_varied` at delay 64 exceeds `gru24`'s by ≥ 10 points **and** is higher in ≥ 2/3
   paired seeds; the difference is otherwise reported as inconclusive. With three seeds these are
   descriptive screens, not significance tests.
8. **Failure handling:** `time_limit`, non-finite loss/gradient or skipped jobs are recorded, never
   dropped. Failure to learn within 3,000 updates is reported as "not learned within the budget",
   not as a capacity limit.

## Out of scope

No new architecture, no Experiment 012, no GPU (all modules are CPU-only; benchmarks showed CPU
multi-worker is ≈ 6.5× faster than CUDA for these small RNNs), no changes to `main`, `AGENTS.md`,
Experiments 001–010 or PR #23.

## Reproduction

```
powershell -NoProfile -File "E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1" -Module capacity_011 -Workers 10 `
  -ShardArg jobs -ShardValues <variant:seed,...> -ExtraArgs "--steps 3000" -MaxWallSeconds 1800 -Run
python -m prototypes.rnn_llm_architecture.experiment_011_report prototypes/rnn_llm_architecture/reports/experiment_011
```
