# Write/read alignment pilot — October 20, 2026

## Verdict

**PASS as a diagnostic of supervised addressing; NOT a proof of autonomous memory or a novel architecture.**

18/18 train/evaluate runs completed on the owner's desktop in 216.812 seconds using six CPU intra-op threads, one inter-op thread, and no GPU. The three variants used identical train/eval histories, 240 AdamW updates and 96 held-out histories per delay/seed/fact count.

The **guided_align** variant tied write/read address projections and added two training-only penalties:
1. *Paired-token guidance*: identify that WRITE_i and QUERY_i refer to the **same** fact slot, and train their soft address distributions to agree. This is privileged semantic supervision, not information discovered from answer-only learning.
2. *Address diversity*: discourage the QUERY soft address distributions from using the same memory slot.

The original model and untutored shared-address model **did not receive** these training hints. No hardcoded token-ID parsing or true addresses were fed into the model's prediction function at evaluation. The performance gain cannot be attributed specifically to alignment alone because alignment and diversity were added together.

## 256-token whole-record recall (%)

Means of two held-out seeds (17, 29), each with 96 histories. A whole record succeeds only if *every fact* is answered correctly.

| Facts | Original | Shared only | Guided alignment + diversity |
|---:|---:|---:|---:|
| 2 | 72.9 | 71.4 | **100.0** |
| 4 | 65.1 | 35.9 | **75.5** |
| 8 | 13.0 | 30.2 | **76.0** |

Eight-fact guided performance by seed: **100.0%** (seed 17) and **52.1%** (seed 29). Eight-fact untutored shared: 18.8% and 41.7%. The performance is promising but variable.

The guided model's **eight write/read token pairs mapped to matching destination slots in both seeds**. However, seed 29 used only seven unique destinations for eight facts, which coincides with imperfect recall. The value of distinct read/write destinations can differ from one example to another because writing is soft and recurrent state can contribute.

## Limitations

- Training guidance disclosed the identity correspondence between WRITE_i and QUERY_i for all configured fact slots. The experiment tests whether added known structure improves a trainable mechanism; it does **not** show an AI learning that relation independently.
- Exactly two training seeds and a tiny synthetic fixed vocabulary; no token-identity transfer, open-domain retrieval, or scaling evidence.
- Small benchmark, 2/4/8 binary facts; maximum delay 256; not a real-world language-model quality evaluation.
- The original and shared model results match earlier six-thread controls, so this experiment adds a new supervised-training condition rather than a new independent control mechanism.
- Guided penalty adds compute during training, and external memory scales with number of facts; equal update count does not mean equal total computational cost.
- This does not validate or refute PR #35's learning-credit theorem and is not evidence for an architectural speed or resource advantage.

## Files and reproducibility

- `write_read_alignment.py` — exact CPU-only, six-thread matched protocol and guided objective.
- `write_read_alignment_results.json` — raw data, all 18 runs, complete=true.
- `write_read_alignment_weights.pt` — saved weights for all trained models.
- Previous files untouched, no new Git branch/PR.

## Next discriminating tests

**First:** run a third predeclared seed and a causal memory-bank ablation on the guided model. This tests reliability and whether high scores depend on stored memory. **Then:** compare alignment-only versus diversity-only versus both, without changing time/labels, to isolate which extra hint improves recall. More training on the current failure alone is not the best investment.

**TL;DR:** Adding explicit write/query correspondence during training raised eight-fact long-delay recall from 13.0% (original) or 30.2% (untutored sharing) to 76.0% average. It is a useful mechanistic diagnosis, not an autonomous-memory breakthrough.
