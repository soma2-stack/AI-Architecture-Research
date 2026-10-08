# Experiment 006 — frozen-state storage vs retrieval diagnosis

**Status:** protocol committed before the hosted run; **completed** in [GitHub Actions #37715859355](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/37715859355), 24/24 runs, 164/164 tests passed. [Results and limitations](EXPERIMENT_006_RESULTS.md). The frozen dense-tanh learning-credit theorem remains OPEN and is not tested.

## Decision to be resolved

Experiments 004–005 found that native token-model queries usually fail when A and B hold different final bits. The prior runs saved metrics and source archives, **not trained state_dict checkpoints**, so the published training schedule must be rerun. This experiment distinguishes:

1. A **readout bottleneck**: A or B can be recovered accurately from a frozen recurrent state by a diagnostic probe even though the learned token-model head fails.
2. A **recoverability/storage issue under these probes**: neither the linear nor the small MLP probe can recover both values on held-out unequal pairs. This is **not proof that bits are absent**, because more powerful/nonlinear readers might succeed.
3. **Decodability without training**: a randomly initialized recurrent model plus a separately fitted diagnostic probe already allows similar recovery. Then strong probe accuracy alone is not evidence that supervised memory training caused storage.

## Fixed models and training

Four variants: `protected_w32`, `state_gated_w32`, `gru_w32`, `lstm_w32`; seeds `17,29,43`; delays `16,64`; **24 training conditions**. Recreate the exact Experiment 005 200 AdamW steps, batch 16, LR .002 and clip 1.0. Each model trains on paired A/B queries of the same histories, without oracle write masks. Width 32, layers 2, CPU one thread only.

Independent probe training examples: 2,048; held-out examples: 1,024 per model/seed/delay. Reproducible seeded synthetic generation, never sharing training samples with model training or probe testing. Include only prefixes **before the query token**. Targets are final A/B values reconstructed from write tokens.

For each fixed trained recurrent model, extract hidden state at (a) directly after the update bit token and (b) after all remaining distractors. Concatenate all layer states (and both LSTM hidden and cell states). Train separate **linear** and **64-unit Tanh MLP** probes for 200 AdamW updates at LR .01 with batch 128, freeze all recurrent parameters. Fit mean and standard deviation on the probe-training set only. Evaluate on held-out data; record train and held-out accuracies.

Also run both probes on **untrained** same-seed recurrence at the **final** time point, with identical probe train/eval input histories. This is a necessary control for representational information already present at initialization.

## Outcomes and interpretation

Primary: `paired_on_unequal` at the final state, using held-out data; compare native token head, frozen-state linear and MLP readers, and untrained-state probe controls **per seed**. Secondary: intermediate state vs final state, full both-slot accuracy, equal-pair accuracy, per-slot accuracy, parameter counts, training loss, runtime and incomplete conditions. A last-write predictor has **zero** accuracy on unequal-valued final pair correctness. A reader can overfit; scrutinize train-vs-held-out accuracy.

No probe is permitted access to tokens, write masks, slot targets or metadata at evaluation: only final recurrent state. Reader parameter counts are reported but reader training is **additional supervision** and the native models did not receive that probe capability. Strong probes do not establish an end-to-end language model advantage or any formal learning-credit theorem.

A native-vs-probe separation across multiple seeds would support a readout limitation. A consistent drop after post-update distractors would support retention loss across the tail. If untrained-state controls match trained-state probes, the experiment cannot attribute decodability to the learned protected memory mechanism.

## Resource bounds

CPU-only, no network datasets or GPU, 540-second hard experiment runtime. Skip and record unfinished conditions. Do not train more than the 24 stated model conditions or change existing architectures, previous experiments, `AGENTS.md` or `main`. The original full suite must pass; source hash and result JSON saved with exact environment and repository commit.

Run from repository root:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' python -m pytest \
  -o addopts= -q -p no:cacheprovider prototypes/rnn_llm_architecture

OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' python \
  -m prototypes.rnn_llm_architecture.experiment_006 \
  --output /tmp/rnn-exp006-results.json \
  --variants protected_w32,state_gated_w32,gru_w32,lstm_w32 \
  --seeds 17,29,43 --delays 16,64 \
  --train-steps 200 --train-batch 16 \
  --probe-examples 2048 --test-examples 1024 \
  --probe-steps 200 --probe-batch 128 --max-wall-seconds 540
```
