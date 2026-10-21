# Causal memory dependency test — October 20, 2026

## Verdict

**PASS: meaningful learned memory use is causally demonstrated in some runs.** All six fresh models were trained under the same 240-update task and seeds as the learned-address pilot. Evaluation-time memory bank removal, reversal, uniform attention, and recurrent-state ablation were tested on *the same model weights and held-out examples*. All six runs completed CPU-only, 4 intra-op threads, GPU disabled, in 78.515 seconds.

**INCONSISTENT: learning is not reliable across seeds and eight facts remain challenging.**

## Whole-record accuracy after a 256-token delay

| Facts | Seed | Normal | Erase bank | Reverse slots | Uniform read | Erase GRU |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 17 | 100.0% | 53.1% | 55.2% | 100.0% | 47.9% |
| 2 | 29 | 45.8% | 45.8% | 45.8% | 45.8% | 25.0% |
| 4 | 17 | 86.5% | 11.5% | 20.8% | 14.6% | 54.2% |
| 4 | 29 | 43.8% | 7.3% | 6.3% | 6.3% | 41.7% |
| 8 | 17 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 8 | 29 | 26.0% | 0.0% | 1.0% | 0.0% | 25.0% |

Each cell evaluates 96 independent held-out histories; every memory slot is queried. Accuracy is for **all** facts in a history being recalled correctly, not per-bit scores.

## Interpretation

- In both four-fact runs, removing the learned memory reduced correct whole-record recalls sharply (83 to 11; 42 to 7). Thus the bank is truly contributing information and is not just decorative.
- In the eight-fact seed 29, removing the bank reduced correct records from 25 to zero: the bank matters despite still-low absolute reliability. Seed 17 never recalled a complete 8-fact record, so the test says little about successful memory in that run.
- Two-fact seed 17 relied on both the bank and its GRU state, but uniform read attention did not hurt; the model may exploit redundant or slot-independent read information there.
- Two-fact seed 29 was unaffected by memory removal at the longest delay, despite reduced correctness when the GRU was erased. That run is not evidence of successful addressable memory.
- Uniform attention degraded four-fact and successful eight-fact performance, evidence that selective read addressing actually matters there.
- The reconstructed unmodified model logits agreed **exactly** with the original forward implementation in all evaluated cases (maximum recorded error: 0). Interventions changed only inference, not model weights.
- These are post-training interventions and cannot separate all causal interactions between the GRU and bank. They do not prove novel architecture, transfer of PR35's theory, or competitive inference resource scaling.

## Reproduction and integrity

Source: `causal_ablation.py`; committed-style measurements: `causal_results.json`; saved six model states: `causal_weights.pt`. All are saved in the existing `experiments/memory_retrieval_triage_20261020` directory. Existing files and audit folders were not modified.

Train: 240 AdamW updates, 12 histories per update, seeds 17 and 29, 2/4/8 facts. Test: 64 and 256 token delays, 96 held-out histories each. CPU only, 4 threads, no GPU. The prior pilot can be reproduced separately; these fresh weights were trained to enable causal tests because the previous pilot did not preserve checkpoints.

**Next small test:** inspect how learned WRITE tags and QUERY tags map to internal memory keys, and identify which slots collide in failed conditions. If addressing is the bottleneck, test an address-separation regularizer or slot-wise coverage loss, with the original model as the fixed-budget control. Avoid indiscriminate extra training.
