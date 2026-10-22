# PRB-Z4 — original evidence recovered

**Recovery/integrity: PASS. Execution coverage: COMPLETE (12/12 original records). Scientific verdict: INCONCLUSIVE for a reliable general mechanism.** No model inference, training, or simulation was run. This recovers the existing experiment; it creates no new experiment or seed.

## What was recovered

The missing **n=7, m=20, seeds 1–3** records survive in an **unreachable Git blob** in the older repository at `C:\Users\coler\OneDrive\Desktop\ai new\.git`:

- Git blob: `4f9a7f4aee4b252b08f85af0d8a802f42114893c`.
- Verbatim recovered file: [z4_n7.recovered_original.jsonl](z4_n7.recovered_original.jsonl), 9,443 bytes, SHA-256 `956e261ae9ed1a7e1d95de8ec62fdb0c1f5557041ef9816ccceb1b00c40e387d`.
- Its first nine rows are **byte-identical** to the existing tracked [z4_n7.jsonl](../z4_n7.jsonl), Git blob `3376e2aed3416551533b9ec940a7e0c05176936c`. That original nine-row file is untouched. The recovered file contains all 12 unique `(m,seed)` conditions: m=10/20/35, seeds 0–3. Do not count the copied nine rows as new runs.
- A separate unreachable ten-row blob, `71476c51c7830cf3402bcb292e4d751ed8fb8e79`, is an exact prefix of the recovered twelve-row file. No associated commit containing the twelve-row blob was found among the three unreachable commits examined; **no original producer commit is invented**.

The initial reachable-history, physical-backup and Actions searches did not find these rows. The original September 27 console transcript showed the file reaching 12 rows; this justified checking unreachable Git objects rather than launching a replay. The full original payload was then preserved from the old store before any further work. No Git garbage collection, reset, deletion, or source-file modification was performed.

## Configuration, provenance and verification

[VERIFICATION.json](VERIFICATION.json) records static checks; [SEARCH_MANIFEST.json](SEARCH_MANIFEST.json) records the bounded recovery search and provenance. [ORIGINAL_CONSOLE_EXCERPTS.json](ORIGINAL_CONSOLE_EXCERPTS.json) preserves only the relevant original commands and actual tool-result output, with timestamps, tool IDs, source line numbers and the source transcript hash. No research notebook text or unrelated conversation was copied.

- The original launch explicitly ran `python z4_grad.py 7 20 1,2,3 12`, after the m10/35 seed runs. The original console at **2026-09-27T23:50:21.905Z** reports **12 rows** and four-seed summaries for all three m values. Their rounded means and per-seed held-out accuracies agree with the recovered payload.
- The original source Write, followed by its documented seed-parser correction, matches the canonical [z4_grad.py](../z4_grad.py) **exactly**: Git blob `7a9489ebf94975a8aa1894220691fb3c6f926cd5`, SHA-256 `c531e4bab23eea1800efa1072061c3749fb26cec1b3f45d978a76dc6c445956f`. The canonical source revision is [`2feeef85ff9168b844c591c961a8bd568a731f2d`](https://github.com/soma2-stack/AI-Architecture-Research/tree/2feeef85ff9168b844c591c961a8bd568a731f2d/experiments/prb); this is a source reference, not a fabricated commit for the later orphaned data.
- Original configuration: Qwen3-VL-4B-Instruct, frozen base model, CPU float32, 12 threads, n=7, 20 demonstrations, 29 held-out pairs; 100 Adam updates for each of `free` and `sinkhorn`. The original CLI does not override that 100-update default. All recovered rows contain both method payloads and ten saved loss samples per method, as the source specifies.
- Each recovered seed has the same symbols and permutation as that seed's existing m10 and m35 records. The full 12-condition grid has no duplicates; metrics are finite/in range and held-out accuracies are consistent with the original denominators. These are data-integrity/configuration checks, not new model evaluations.
- The original checkpoint/tokenizer revision and original software versions were not pinned. That remains a limitation on exact independent reproduction; it does **not** make these recovered original raw records into new measurements or invalidate their documented execution coverage.

## Actual results

| m=20 seed | Free unseen accuracy | Sinkhorn unseen accuracy |
|---:|---:|---:|
| 0 (previously available) | 6.90% | 100% |
| 1 (recovered) | 3.45% | 100% |
| 2 (recovered) | 3.45% | 100% |
| 3 (recovered) | 0% | 34.48% |
| **Four-seed mean** | **3.45%** | **83.62%** |

For comparison, the unchanged m10 four-seed means are **9.62% free / 39.74% Sinkhorn**, and m35 means are **1.79% / 80.36%**. Different m values have different demonstration and held-out sets; this is a descriptive comparison. The digit-interface and exhaustive model-as-scorer controls score 100% in all 12 records.

The m20 Sinkhorn method solved held-out rebinding for three seeds, but seed 3 reached only 34.48% held-out accuracy, 45% training accuracy and 3/7 mapping score despite full-table coherence 1.0. Coherence therefore must not be substituted for correctness. The free method fits its training pairs but transfers poorly. These recovered results support the original bounded comparison, not a new architecture, an all-seed reliable solution, or the growing-dimensional learning-credit target. No numerical preregistered PASS/FAIL threshold was found; the scientific outcome remains scoped and seed-dependent.

## Completion and next record

**PRB-Z4's original raw grid is genuinely complete: all 12 conditions now have their original evidence. No replay is needed.** Lifecycle status changes from PARTIAL to COMPLETED — INCONCLUSIVE; independent training reproduction remains unperformed. This changes the 97-record inventory to **82 completed, 6 partial, 3 stopped, 4 not run, 1 invalid, 1 missing evidence**. Original tracked files and all backups remain intact.

The next separate partial register entry is **AMS v4**: its Stage 2 was barred by the failed mandatory `V1_B_REP` gate. It must not be resumed or redesigned automatically. No work on it began here. PR42 remains open and unmerged; this recovery is submitted as a separate draft based on its branch so the master-register updates compose without losing Experiment 010's completion record.
