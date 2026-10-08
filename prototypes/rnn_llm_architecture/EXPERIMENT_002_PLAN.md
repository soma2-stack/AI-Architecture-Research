# Experiment 002 — length transfer, fairer gated baselines, and counterfactual queries

**Status: planned/implemented; training results pending.** This is an
independent, bounded follow-up to the successful 100-step Experiment 001.
The strict robust learning-credit target `D=Omega(n), mT=o(n^(3/2))`
remains **OPEN**, and these token tasks are not formal evidence about `D`.

## Why this test is worth doing

Experiment 001 found 100% 64-token **delayed binary recall** for the
protected RNN in two seeds after 100 updates. But the comparison was
not parameter matched, omitted the better-forgetting LSTM initialization,
and did not establish longer-horizon generalization. The selective task
allows 75% accuracy via the last-write shortcut; the protected model was
weak on the updated-slot condition at delay 64. This follow-up attempts to
**falsify** claims of better learned memory with stronger controls.

## Prespecified design

- Train once at **delay 64**, independently for each of the two tasks.
- Evaluate **frozen model weights** at delays 64, 128, 256, with fixed
  disjoint held-out sets. No additional updates during evaluation.
- Models: standard, near-critical, protected, GRU, LSTM at width 32;
  parameter-closer GRU width 24 (7,728 trainable) and LSTM width 20
  (7,160 trainable), compared with protected width 32 (7,504);
  width-32 LSTM initialized with sum of forget-gate biases +1;
  protected RNN with random orthonormal bank, projection removed,
  retention removed. These make **11 variants**.
- Two tasks x 3 independent seeds (17, 29, 43) x 11 variants = **66 runs**;
  150 AdamW steps each, batch 16, LR .002, clip norm 1; fixed training
  generator seeds and identical input batches per task/seed/step.
- Counterfactual selective query: take the **identical full prefix** and
  clone it to evaluate both final `QUERY_A` and `QUERY_B` tokens. Compute
  both independent ground truths from the source tokens (no answer leak).
  Report exact **both-slot** accuracy, updated-slot accuracy,
  untouched-slot accuracy, paired score on cases where A/B final bits
  differ, and the naive last-write paired baseline.
- This counterfactual evaluation requires at most 50% pair accuracy of a
  naive always-last-written-bit rule when A/B match about half the time.
  Report both-slot score on **unequal** values to expose this shortcut.
- Tied token embeddings / head, layers, common loss and task generator are
  held fixed except for width (in the parameter-nearer controls). Width
  changes representation capacity; **these comparisons are not perfectly
  matched**. No optimized learning-rate search or compute-matched grid.
- CPU-only, no user GPU. One GitHub Actions workflow, 18min max job;
  **540 seconds experiment wall-time guard**. Incomplete jobs are retained
  and marked incomplete, never manufactured. Existing evidence not overwritten.
- Full architecture suite must pass before experiment begins.

## Reproduction and evidence

Run only from repository root and only with explicit authorization:

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
experiments/automated_mechanism_search/.venv/bin/python \
  -m pytest -o addopts= -q -p no:cacheprovider \
  prototypes/rnn_llm_architecture/test_experiment_002.py

CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
experiments/automated_mechanism_search/.venv/bin/python \
  -m prototypes.rnn_llm_architecture.experiment_002 \
  --output /tmp/rnn-experiment-002.json \
  --train-delay 64 --eval-delays 64,128,256 \
  --steps 150 --batch 16 --eval-batch 512 --max-wall-seconds 540
```

GitHub Actions evidence is uploaded by `.github/workflows/rnn-exp002-cpu.yml`.
Only independent complete runs establish pilot results, and the results
are exploratory: three seeds, one LR, limited steps, fixed toy tasks and
unmatched operations/optimization budgets do not prove superiority.

## Research guardrails

- Original architecture implementations, prior experiment, and theory
  unchanged. No Route-6 theorem claims or theoretical model training.
- No additional prompts/oracle write masks exclusive to protected model.
- No large LLM pretraining, RL, dataset downloads or owner GPU.
- Do not compare selectively reported best seeds. Preserve failed runs.
- Candidate ablations change model capability and parameterization; do
  not call them proof of mechanism necessity without matched controls.
