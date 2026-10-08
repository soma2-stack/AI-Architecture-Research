# Experiment 007 — query-aware memory retrieval (bounded CPU pilot)

**Scientific question:** Did earlier poor A/B accuracy reflect a weak token readout, or an inaccessible state? Does additional **joint** training with a query-conditioned decoder help at length 64, including cases in which A and B differ?

No result in this experiment measures formal robust learning-credit dimension. The open conjecture `D=Omega(n), mT=o(n^(3/2))` remains unaffected.

## Precommitted comparisons

- Architecture candidates: original protected RNN, standard GRU and LSTM, no changes to their cells. Width 32, two layers, vocabulary 16, same fixed seeds `17,29,43` and train delays `16,64`.
- **Pretrain:** identical Experiment 005/006 two-query task, 200 updates, AdamW LR .002, batch 16, gradient clipping 1. Same per-step synthetic data seed formula as Experiment 006.
- **Native-200:** unchanged baseline token head before extra training.
- **Native-continued:** cloned pretrained model; another 150 steps with the original paired-query token head and the same per-step data stream as joint training. This controls for additional optimization (though not identical parameters/FLOPs).
- **Frozen-top:** train a 64-hidden-unit MLP decoder + query embedding to decode A or B using *only* the highest layer hidden state, with no recurrent updates. 1024 separate seeded examples, 150 decoder steps, LR .01, batch 64. Freeze and verify the recurrent weights are bitwise unchanged.
- **Frozen-all:** identical head and training data but state includes all layers; LSTM also includes its cell memories. Train-feature standardization only, applied unchanged to held-out examples. Parameter count differs due to input width.
- **Joint-all:** clone the same pretrained model and train recurrent model and all-state addressed decoder together for 150 updates on the **same seed stream as native-continued**; no oracle write gates. LR .002 recurrent, LR .01 decoder, clipping 1. Unlike the frozen readers the joint decoder inputs are not standardized, so direct equality of optimizers or compute must not be assumed.

The MLP gets a learned A/B query embedding and must return independent two-class predictions for **both queries from the same query-free prefix**. It never receives true values, labels, or the future query token as input, and neither branch uses a slot-specific oracle write gate. The head receives task-specific decoder supervision, and this is not an equal-parameter or equal-compute architecture ranking.

## Evaluation

Held-out data seed `seed+1_000_000` is disjoint from both native training and frozen-head training seeds. Evaluate at the trained length and **2× and 4× length transfer** without new optimizer updates. Report both-correct paired accuracy, both-correct on unequal A/B values **as primary metric**, both-correct on equal values, per-slot accuracy, loss, and parameter counts. Trivial last-write behavior yields **zero both-correct on unequal A/B values**; two independent random guesses yield approximately 25%. Document deviations and their uncertainty over only three seeds.

## Resource and reproducibility constraints

Run CPU-only, 1 CPU thread, PyTorch 2.14.1+cpu in GitHub Actions. No dataset downloads, CUDA, stage0, RL, full LLM pretraining, PR merge, historical edits, or additional experiments. Job maximum 15 minutes; experiment guard 540 seconds. Record incomplete runs, preserve raw JSON with one exclusive-create output path, fail clearly on nonfinite values, retain the exact tested source snapshot and all new tests. Do not overwrite earlier runs.

If the global time budget is reached, mark status `budget_limited`, keep completed seeds and disclose missing comparisons. The experiment is exploratory and too small to claim a general neural architecture advantage.

## Execution

```
python -m prototypes.rnn_llm_architecture.experiment_007 \
  --output "$RUNNER_TEMP/rnn-exp007-results.json" \
  --variants protected_w32,gru_w32,lstm_w32 \
  --seeds 17,29,43 --delays 16,64 \
  --pretrain-steps 200 --additional-steps 150 \
  --batch 16 --head-examples 1024 --head-batch 64 \
  --eval-examples 512 --max-wall-seconds 540
```

**Decision gate:** On completion, preserve the full evidence and report whether the new reader improves *unequal-pair* recall. Do not begin Experiment 008 without a separate request.
