# Isolating memory-address training hints (2026-10-20)

**FINISHED:** 18 new CPU training runs across three seeds, 2/4/8 binary facts, and two single-hint variants. Ran in 216.047 seconds with six CPU threads and the GPU disabled. Both single-hint arms used the same 240 updates, examples, and evaluation seeds as the prior shared and combined-guidance arms.

### Complete-record recall (%) after a 256-token delay

| Facts | No hint (shared keys) | Write/read pairing only | Query address diversity only | Both hints |
|---:|---:|---:|---:|---:|
| 2 | 80.9 | 100.0 | 68.1 | **100.0** |
| 4 | 31.9 | 54.2 | 77.1 | **83.7** |
| 8 | 53.5 | 62.8 | 39.2 | **84.0** |

All values are averages across seeds 17, 29, and 43; each seed tested 96 fresh held-out histories per setting. A complete-record success requires every queried fact to be right.

**Technical interpretation:** Write/read pairing alone helps more than diversity alone for eight facts, while diversity alone helps more at four facts. Both together score best overall at four and eight facts. This is a tiny three-seed pilot; individual seeds varied substantially. For eight facts, diversity-only scores were 11.5%, 6.3%, and 100.0%, and alignment-only scores were 57.3%, 31.3%, and 100.0%.

**CRITICAL CAVEAT:** Pairing-only and the combined arm used explicit training-time knowledge that WRITE_i and QUERY_i refer to the same logical fact. This is extra semantic supervision, not fully learned addressing. Diversity-only uses knowledge of the set of query-token IDs without knowing their WRITE correspondences. No privileged labels were fed into forward prediction at inference. These comparisons isolate which task-specific hints help; they do not demonstrate a general-purpose autonomous memory architecture, PR #35 theorem transfer, or equal total compute.

**Evidence:** `single_hint_ablation.py`, `single_hint_results.json`, `single_hint_weights.pt` (new single-hint arms); `write_read_alignment_results.json` and `alignment_seed43_results.json` (existing shared and combined controls).

**Next small experiment:** Train on some ID pairings and evaluate generalization to new/remapped WRITE/QUERY symbols, without training-time pairing hints for held-out IDs. Only pursue larger compute if the model learns the relation beyond memorizing supplied tag mappings.
