# Experiment 001 — Small supervised recurrent-memory pilot

**Status:** pilot harness and tests committed; trainable-architecture training
results are **NOT YET VERIFIED** until a run executes on the actual PR code.
This file is not a research-theorem record. It contains no claim about formal
robust credit dimension or model superiority.

## Scientific question

Can the experimental protected-memory RNN **learn** delayed recall and
selective overwrite at equal width and, later, under matched resources,
compared with standard tanh RNN, near-critical RNN, GRU and LSTM?

Our sixth architecture (full frozen-corridor mathematical reference) has no
arbitrary-token trainable adapter and **is excluded from training**.
The open `D=Omega(n), mT=o(n^(3/2))` theorem is a separate question.

## Task definitions

- **Delayed binary recall:** one balanced binary input at token zero,
  independently random distractors, and a final query token. The answer is
  evaluated only at the query. Distractor tokens exclude the bit tokens.
- **Selective overwrite:** initialize A/B in a randomized order, present
  independently random distractors, overwrite exactly one named slot,
  continue distractors, then query randomly chosen A or B. Held-out reports
  split updated-slot and untouched-slot accuracy. The full answer is never
  embedded in the query. No oracle protected-model write masks are supplied.

Both tasks use synthetic CPU tensors, fixed explicit generators and separate
train/evaluation seed families. Chance for the final balanced binary label is
about 50%. A naive **last-write-value** shortcut is approximately 75% on the
selective task and is reported explicitly; a model scoring 60–70% could still
be exploiting that shortcut. Compare updated and untouched query strata;
do not interpret greater-than-chance aggregate accuracy alone as learned
selective memory. Task token conventions live in `learning_pilot.py`.

## Run (explicit authorization required; execution does train weights)

From the checkout root in the prepared CPU environment:

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
experiments/automated_mechanism_search/.venv/bin/python -m pytest \
  -o addopts= -q -p no:cacheprovider \
  prototypes/rnn_llm_architecture/test_learning_pilot.py
```

Minimal all-five smoke (one task, short delay, one seed):

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
experiments/automated_mechanism_search/.venv/bin/python \
  -m prototypes.rnn_llm_architecture.learning_pilot \
  --output /tmp/exp001-five-smoke.json \
  --models tanh,near_critical,protected,gru,lstm \
  --tasks delayed --delays 16 --seeds 17 \
  --steps 10 --batch 8 --eval-batch 128 --max-wall-seconds 240
```

The optional full bounded matrix is 5 models x 2 tasks x 2 delays x 2 seeds,
100 updates/configuration. It is **not automatically executed** by import or
repository setup. `--max-wall-seconds 1200` is a global execution guard, not
a guaranteed completion target. Output uses exclusive file creation to prevent
overwriting evidence. If the budget is reached, JSON records completed and
skipped conditions; do not silently fill gaps.

A branch-local [GitHub Actions workflow](../../.github/workflows/rnn-exp001-cpu.yml)
attempts the CPU unit suite and a smaller 12-step five-model/two-task smoke
on push or explicit workflow dispatch. **No GitHub Actions result should be
reported unless a real run appears.** CI minute consumption is bounded by a
per-job 18-minute timeout.

## Fairness, limits, and falsification

- All models see identical examples for each corresponding seed and update.
  Evaluation uses a fixed disjoint seed stream for each condition.
- Identical width, layers, optimizer family, learning rate, batch and steps
  are **not** parameter-matched. Different model sizes and computation counts
  must be reported. A later independently authorized pilot should repeat with
  matched budgets from `comparison_configs.json`.
- Same fixed learning rate may disadvantage some architectures. A later
  matched learning-rate selection study is essential.
- No seed-aware tuning, early cherry-picking, pretrained weights, special
  write masks, datasets or RL.
- Report accuracy/loss by **condition and seed**, training time, and
  deterministic duplicate-run checks; do not announce a winner from a
  very short optimization pilot or rank architectures by a single gradient norm.
- Near-chance results after 10–100 steps are inconclusive: an optimization
  failure or difficult task is not a theoretical impossibility.
- Protected Walsh bank invariance may also hold for ordinary orthogonal
  memories. Only learnt selectivity with fair baselines, controls and ablations
  could establish an empirical architectural advantage.
- No result tests the whole-ball legal-query separation required by the
  robust learning-credit theorem.

## Status / provenance

On the authoring environment (Python 3.13, CPU PyTorch 2.10) the **six new
standalone harness tests** passed using a toy model for the training smoke.
This validates generator logic and basic optimizer plumbing only; it does
**not** exercise the five repository model implementations, and should not
be conflated with the prior reported 127 architecture tests.

The full actual-repository suite and real five-model CPU training matrix
require the PR checkout or a successful CI job. Until then, label them
**NOT RUN/NOT VERIFIED**.
