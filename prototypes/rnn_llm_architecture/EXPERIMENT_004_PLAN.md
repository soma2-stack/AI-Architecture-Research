# Experiment 004 — train two independent slot queries from identical histories

**Status:** prespecified, bounded controlled-training implementation;
results pending. No change to theory or previous experimental evidence.

## Motivation and question

Experiment 002 failed genuine selective updating under the old *single*
random final query: protected model paired A+B exact accuracy at 64 tokens
was **42.3%**, below the 50% naive last-value paired shortcut, and just
**0.7% on A≠B** histories. We should not accept general claims of
"selective memory" from that task. But the training signal itself only
supervised one query per history; the model might need more explicit
feedback for both slots before concluding the architecture cannot learn
this kind of memory.

**Question:** With direct, balanced supervision of both A and B from
identical initial/update histories, which recurrent architecture first
learns to maintain both values independently? This is an optimization-
and data-protocol test, **not** a proof of extra memory capacity.

## Prespecified protocol

- Reuse the verified synthetic two-slot task generator from Experiment 001;
  its initial A/B order, updated slot, update value and two original values
  are all independently randomized. At query time no answer value is given.
- Duplicate each source history into two examples with **identical
  prefixes**, one final `QUERY_A`, the other final `QUERY_B`. Label each by
  replaying actual writes from the source tokens, independently of the
  generator's original one-query label.
- Train with average cross-entropy across **both queries**. This removes
  the old 75%-per-query training shortcut of always reporting the last
  written bit. No oracle write mask is provided to protected RNN.
- Evaluate frozen models on *counterfactual identical-prefix pairs*.
  Report paired exact accuracy, A≠B paired accuracy, updated/untouched
  slot accuracy, and naive last-write paired baseline (approximately 50%).
- Train only at delay 64; freeze and evaluate at delays 64, 128, 256.
- Compare nine variants: standard, near-critical, protected, GRU, LSTM
  width 32; GRU width 24 and LSTM width 20 (close to protected 7,504
  parameters); protected random orthonormal bank and no-projection
  ablations. Seeds 17/29/43, **27 configurations**.
- Each run: 240 AdamW optimizer updates, 16 independent histories per
  batch duplicated into 32 query examples, LR .002, clip norm 1.0.
  Held-out: 512 paired histories per seed/delay, disjoint from training.
- Stop at **540 seconds global experiment time**, GitHub Actions
  **18-minute job limit**, CPU only. Report incomplete/skipped runs
  explicitly, with original run order. No large language-model training.
- Run full architecture and new objective suite before training.
- No architecture implementation changes or historical result edits.

## Statistical and architectural caveats

Training on both queries changes supervision, not RNN architecture.
If this fixes selective recall, compare the mechanism-removal variants
and ordinary GRU/LSTM controls; no novelty follows from improved training.
A 240-step single-LR result is not an optimized general comparison.
Matching parameter count by width does not match compute or internal
state semantics. Three seeds do not establish generality.

The goal `D=Ω(n), mT=o(n^(3/2))` remains **OPEN**, and this test has
no bearing on the exact frozen dense-tanh legal-query theorem contract.
