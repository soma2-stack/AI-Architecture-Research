# Learned Memory Addressing Pilot — October 20, 2026

## Verdict

**PASS — runnable neural memory controller.** All 6 CPU training runs completed at 240 updates, with no nonfinite loss. No GPU was used (CUDA hidden and checked). Four CPU threads.

**PARTIAL — learned memory operations.** The controller was **not given token-ID if/else parsing, write-address labels, or correct-slot supervision**. It used trainable embeddings, a GRU state, a differentiable write gate, learned key-to-slot probabilities, memory-value encoding, and learned query attention. End-of-sequence answer loss supplied the only training target. It achieved strong recall in some conditions, and the four-fact diagnostic showed higher write-gate values on actual marked writes than on other tokens in both seeds.

**FAIL — reliable eight-fact memory.** At 256 tokens the learned model recovered 0/96 complete 8-fact records in seed 17 and 25/96 in seed 29 (0% and 26.0%). It has not solved reliable eight-fact recall. Its best results also depended materially on random seed. No architectural breakthrough or general-language memory claim.

## Protocol

- Source: `learned_address.py`; raw results: `learned_results.json`.
- CPU PyTorch; 4 intra-op threads, 1 inter-op thread, no GPU.
- Two seeds: 17 and 29.
- Fact counts: 2, 4, 8; two values per fact. 240 optimizer updates, 12 histories per update, AdamW rate .003.
- Evaluated on 96 newly seeded held-out histories per condition, at task delays 16, 64 and 256 tokens; delayed histories append filler/noise **without legal writes**, with all fact slots queried separately. Data generation and label replay use the existing PR23 `capacity_010` implementation, matching the earlier triage screen's evaluation seeds and protocol apart from training budget.
- The neural forward path does **not** branch on `WRITE_START`, `VALUE_START`, `QUERY_START`, or slot indices. The token parser in `gate_probe` runs **only after training** to score whether the learned gate responded to marked writes. The architecture is nevertheless given the task's fixed *number* of memory slots and knows the final position is the query; it has not learned an unbounded store or general token parser.
- Baselines in `results.json` were trained at **180 updates**, and some use privileged addressing. Those prior results are illustrative, **not** a budget-matched fair contest against these 240-update runs.

## Results: whole-record accuracy (%)

| Facts | Seed | Delay 16 | Delay 64 | Delay 256 | Marked write gate / other gate |
|---:|---:|---:|---:|---:|---|
| 2 | 17 | 100.0 | 100.0 | 100.0 | .468 / .437 |
| 2 | 29 | 90.6 | 65.6 | 45.8 | .698 / .052 |
| 4 | 17 | 100.0 | 100.0 | 86.5 | .774 / .005 |
| 4 | 29 | 41.7 | 39.6 | 43.8 | .675 / .041 |
| 8 | 17 | 3.1 | 2.1 | 0.0 | .311 / .098 |
| 8 | 29 | 18.8 | 17.7 | 26.0 | .832 / .205 |

Averages across both seeds at delay 256:

| Facts | Complete recall | Per-fact bit accuracy |
|---:|---:|---:|
| 2 | **72.9%** | 86.5% |
| 4 | **65.1%** | 91.1% |
| 8 | **13.0%** | 75.7% |

The model uses 32 GRU state scalars plus 12 memory values per configured fact: 56, 80, and 128 recurrent/bank scalars for 2, 4, and 8 facts, respectively. It has 11,831–11,903 trainable parameters depending on slot count, more than the earlier hard-coded hybrid. These are not matched-cost comparisons.

## What this establishes

The learned gate, key projection and readout can be optimized from only the answers in some short synthetic fact-memory tasks. In both four-fact runs, gates at real marked writes were notably higher than at other token transitions (0.774 vs 0.005 and 0.675 vs 0.041). However, that gate metric is a post-hoc correlation: it does **not** by itself establish that every correct answer depended on memory, that address assignment was correct, or that the model generalized to unseen token meanings.

Two seeds and 96 held-out histories per condition are preliminary. The 2-fact first-seed result was perfect, but the second seed retained only 45.8% at delay 256. Eight-fact complete recall remained poor in both runs. The model does not surpass the original task-specific DeltaRule oracle, which reached 100% in the prior (privileged addressing) study.

## Next smallest useful experiment

1. **Causal memory ablation:** Evaluate the same trained weights with the memory bank erased, or with query keys permuted, to confirm that good predictions truly rely on the learned bank.
2. **Mechanism/optimization diagnosis:** Look at learned write gates on overwrites, read-key separation and repeated-address collisions, especially in failed 8-fact cases.
3. **Fair and budgeted controls:** Compare a learned parser without the external bank, and this model with direct versus attention retrieval, using the same updates, parameter/state budgets and random seeds.
4. Only then consider a small preregistered training extension or stronger controllers. Do not equate a tiny synthetic success with PR35's exact-real credit theorem.

## Reproduction (new output filename)

```powershell
python -B experiments/memory_retrieval_triage_20261020/learned_address.py --steps 240 --seeds 17,29 --slots 2,4,8 --histories 96 --output experiments/memory_retrieval_triage_20261020/learned_recheck.json
```

`learned_address.py` will refuse to overwrite an existing result JSON file. Original files and earlier triage records were preserved; no PR, branch or worktree created.

**TL;DR:** It is possible for this controller to *learn* useful write/read behavior from answer supervision, but it is seed-sensitive and far from reliably remembering eight facts. **PASS for a partial proof of concept, FAIL for a dependable learned memory system.**
