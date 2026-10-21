# Write/read alignment: third-seed results (2026-10-20)

**Status:** 27/27 configurations completed, across seeds 17, 29, and 43. CPU-only, six threads. Original data and code retained.

## Complete-record recall after 256 tokens

| Number of facts | Original | Shared-key model | Guided alignment |
|---:|---:|---:|---:|
| 2 | 81.9% | 80.9% | 100.0% |
| 4 | 62.5% | 31.9% | 83.7% |
| 8 | 18.4% | 53.5% | 84.0% |

Each mean pools three independent seeded models, with 96 held-out histories per model/condition.

For eight facts, seed-by-seed guided scores were 100%, 52.1%, and 100%. Unguided shared scores were 18.8%, 41.7%, and 100%. Results vary markedly by initialization.

**Memory ablation:** In the two earlier guided eight-fact models, setting the memory bank to zero reduced whole-record successes from 96 to 0 and from 50 to 1 (out of 96). This supports a causal memory contribution.

**Major caveat:** The guided model was taught the correspondence between WRITE and QUERY identifiers, plus a penalty against address collisions. It was not an equal-information comparison, and it did not autonomously discover those correspondences. Both guidance components were applied together.

**Next:** Isolate the two components with alignment-only, diversity-only, and combined experiments, retaining an unguided control. Avoid claims about general-language memory or PR35 theorem transfer.

Raw evidence: write_read_alignment_results.json, alignment_seed43_results.json, guided_causal_results.json. Reproduction scripts and model checkpoints are in this folder.
