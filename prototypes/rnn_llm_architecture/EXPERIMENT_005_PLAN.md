# Experiment 005 — state-conditioned selective-write gate

**Status: preregistered CPU protocol; results pending.**

## Falsifiable question

Experiments 001–003 established trained *single tagged-bit* recall in small models, including contradictory-bit distractors. Experiments 002 and 004 found that two-slot selective overwrite remained weak and was consistent with the naive last-write shortcut. The existing protected-memory cell computes its slow write probability from input only. Here we test whether conditioning the **same slow-channel gate** on the previous hidden state improves two-slot retention, rather than assuming the improvement.

This is a **known GRU-style gating principle**, not a claim of a new primitive or the frozen dense-tanh learning-credit theorem. The comparison is an engineering experiment only.

## Candidate intervention

Baseline protected slow-channel write gate:

`w_t = sigmoid(G_x x_t)`

State-conditioned candidate:

`w_t = sigmoid(G_x x_t + G_h h_(t-1))`

The new matrix `G_h` initializes to zero. Thus the candidate exactly reproduces the original protected forward function at initialization; subsequent learning can use state-dependent gating. This intervention adds `width * protected_channels` trainable scalar weights **per layer**, so equal width is **not parameter matching**. All other cell equations, memory, token model, optimizer and training data remain the same. This is an architecture ablation; compare it with both the original protected cell and its random-basis counterpart.

## Fixed design

Five variants, three independent seeds, and two training delays:

- `protected_w32` — input-conditioned protected baseline
- `state_gated_w32` — state-conditioned slow gate (Walsh bank)
- `state_gated_random_w32` — state-conditioned slow gate with random orthonormal bank
- `gru_w32` — ordinary GRU control
- `lstm_w32` — ordinary LSTM control

Seeds: `17,29,43`; train delays: `16,64`; **30 distinct training conditions**. Each condition gets at most **200 AdamW updates**, batch size 16, LR 0.002, gradient clip 1.0, fixed synthetic data and balanced targets. Both A and B queries from a common prefix are supervised, with no oracle write masks. Test on frozen checkpoints at each training delay and at 2x/4x delay. Evaluation batch 512, independently generated from training seeds. Collect every condition, including failed seeds and stopped runs.

Resource guard: CPU-only PyTorch, one CPU thread, **540 seconds total experiment wall time** and 15-minute GitHub Actions job timeout. The resource guard can skip conditions; skipped runs must appear in the JSON artifact, and comparisons must not silently omit them. The workflow also executes all architecture and experiment CPU tests. No GPU, language pretraining, AMS Stage 0, collector or external datasets.

## Primary outcome and interpretation

Primary: **counterfactual both-slot correctness on unequal-valued histories** (`paired_on_unequal`) at the *trained delay*. This directly tests genuine independent retention. Secondary: both-slot accuracy over all examples, updated/untouched slot accuracy, transfer to 2x/4x delay, train loss, parameter counts, measured gate norm, runtimes and learning stability. Include naive last-write both-slot accuracy (~50%) and chance pair accuracy (~25%) to avoid inflated claims.

Intervention success requires improvement over the original protected model on the *unequal-valued* primary metric across multiple seeds; a one-seed improvement or a jump only on equal-valued histories is not sufficient. Even if positive, it remains a small exploratory result until independent replication, equal-parameter/compute comparisons, stronger baselines and other tasks succeed. If failure, preserve the failure and consider whether the current architecture cannot learn two independent slots.

## Reproduction

From repository root, with a compatible CPU-only PyTorch installation:

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m pytest -o addopts= -q -p no:cacheprovider prototypes/rnn_llm_architecture/

CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m prototypes.rnn_llm_architecture.experiment_005 \
  --output /tmp/rnn-exp005.json \
  --variants protected_w32,state_gated_w32,state_gated_random_w32,gru_w32,lstm_w32 \
  --seeds 17,29,43 --train-delays 16,64 \
  --steps 200 --batch 16 --eval-batch 512 --max-wall-seconds 540
```

`--output` uses exclusive creation and never overwrites prior evidence. The automatic GitHub workflow carries its own unique temporary output and uploads the machine-readable artifact even if the training command fails.

**Theory boundary:** There is no experimental inference about `D=Omega(n), mT=o(n^(3/2))`. The full mathematical reference remains untouched and untrained. The original protected and GRU/LSTM candidates remain unchanged.
