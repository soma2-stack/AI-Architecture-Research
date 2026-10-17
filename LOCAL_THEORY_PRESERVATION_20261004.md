# Local theory preservation, 2026-10-04

Archival/provenance task only; committing a claim does not accept or verify it. No cleanup or consolidation performed.

- Branch: `preserve/local-theory-20261004`.
- Exact base: `c682b271dd7bc98fcded9298da621c63b816ed34`.
- Evidence commit: `53d5027c88a1f4483d0f5df7e203dad39f073403`.
- Notebook commit: `8209b4bad701bf280aab57c6b9ac31ee5bf05bfb`.
- 29 folders;331 evidence files;1,798,485 original working-file bytes.
- Includes54 previously ignored evidence logs. Two bytecode caches excluded and left on disk.
- No duplicate folders or byte-identical tracked content found; no uncertain preservation classifications.
- Detailed per-file SHA-256, committed blob IDs, sizes, branch-presence checks and inventory: [JSON manifest](LOCAL_THEORY_PRESERVATION_20261004.json).

| Folder | Files preserved | Source bytes | Classification |
|---|---:|---:|---|
| `theory/claude_aperiodic_review_20261001` | 6 | 23224 | PRESERVE_COMPLETE |
| `theory/claude_causal_width_20261002` | 3 | 14371 | PRESERVE_COMPLETE |
| `theory/claude_fixed_feature_width_review_20261002` | 5 | 35804 | PRESERVE_COMPLETE |
| `theory/claude_interacting_block_20261002` | 17 | 100261 | PRESERVE_COMPLETE |
| `theory/claude_log_gap_review_20261001` | 4 | 32499 | PRESERVE_COMPLETE |
| `theory/claude_moment_merger_review_20261001` | 20 | 155616 | PRESERVE_COMPLETE |
| `theory/claude_moving_spike_remainder_20261002` | 193 | 773994 | PRESERVE_COMPLETE |
| `theory/claude_near_critical_review_20261001` | 3 | 13628 | PRESERVE_COMPLETE |
| `theory/claude_operator_dimension_review_20261002` | 3 | 24479 | PRESERVE_COMPLETE |
| `theory/claude_quadratic_review_20261001` | 5 | 27500 | PRESERVE_COMPLETE |
| `theory/claude_rotating_gate_review_20261001` | 10 | 31255 | PRESERVE_COMPLETE |
| `theory/claude_transport_basis_review_20261002` | 9 | 82476 | PRESERVE_COMPLETE |
| `theory/claude_two_pulse_additivity_20261002` | 18 | 114373 | PRESERVE_COMPLETE |
| `theory/claude_width_scaling_review_20261001` | 3 | 40116 | PRESERVE_COMPLETE |
| `theory/grok_bounded_history_radius_review_20261003` | 2 | 12775 | PRESERVE_COMPLETE |
| `theory/grok_causal_suffix_width_review_20261002` | 1 | 13639 | PRESERVE_COMPLETE |
| `theory/grok_filtered_timing_d2_20261004` | 1 | 5318 | PRESERVE_COMPLETE |
| `theory/grok_filtered_timing_d2_band_20261004` | 1 | 5431 | PRESERVE_COMPLETE |
| `theory/grok_filtered_timing_d2_monotone_20261004` | 1 | 5620 | PRESERVE_COMPLETE |
| `theory/grok_filtered_timing_one_block_20261004` | 1 | 4811 | PRESERVE_COMPLETE |
| `theory/grok_filtered_timing_width_20261004` | 1 | 7925 | PRESERVE_COMPLETE |
| `theory/grok_intermediate_gate_review_20261002` | 1 | 8147 | PRESERVE_COMPLETE |
| `theory/grok_multiharmonic_16_15_review_20261003` | 1 | 4539 | PRESERVE_COMPLETE |
| `theory/grok_multiharmonic_lower_review_20261002` | 2 | 25036 | PRESERVE_COMPLETE |
| `theory/grok_online_gate_polynomial_review_20261002` | 1 | 7446 | PRESERVE_COMPLETE |
| `theory/grok_permitted_query_reach_20261002` | 12 | 147249 | PRESERVE_AFTER_EXCLUDING_OBVIOUS_TEMP_FILES |
| `theory/grok_spike_remainder_review_20261002` | 5 | 60273 | PRESERVE_AFTER_EXCLUDING_OBVIOUS_TEMP_FILES |
| `theory/grok_sustained_weak_gate_review_20261002` | 1 | 9810 | PRESERVE_COMPLETE |
| `theory/grok_timing_signal_J_review_20261004` | 1 | 10870 | PRESERVE_COMPLETE |


## Notebook provenance

- Claude notebook: MIXED. Preserved existing theory text at original working lines12-377,390 and5313-5369 through the index. Its GAS-0 additions at378-389 and5370-5390 remain uncommitted. Working-file bytes were not rewritten.
- Codex notebook: RELATED_THEORY_PROVENANCE; all14 added lines106-119 preserved unchanged.
- GAS-0 README: UNRELATED_WORK; all97 added lines remain uncommitted and byte-identical.

## Verification

Every approved evidence path is tracked; every committed blob matches Git-filtered original input. All original working-file hashes, AGENTS.md, .gitignore and both notebook working files are unchanged. Main and corridor heads are unchanged; all prior theory paths remain. No unrelated untracked path disappeared.

## Remaining local material outside this task

The four untracked Claude experiment-review folders, the Perplexity review export, GAS-0 outputs/workspaces and GAS-0 notebook additions remain local and untouched. They require a separate preservation decision before a broad consolidation can be declared safe. The 29-folder theory preservation itself is complete.

## Exact remaining status

```text
 M Claude_Research.md
 M experiments/gas0/README.md
?? PERPLEXITY_PROOF_PACKET.txt
?? experiments/claude_8d_review_20261001/
?? experiments/claude_radial_8d_review_20261001/
?? experiments/claude_rebalanced_7d_review_20261001/
?? experiments/claude_third_order_review_20261001/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C0_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C1_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C1_dev_arena_seed1_retry_after_empty_ledger_fix/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C2_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C3_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C4_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C4_dev_arena_seed1_clean_after_plan_first_fix/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_20260929/C4_dev_arena_seed1_retry_after_empty_commit_fix/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_final_20260930/
?? experiments/gas0/analysis/dev_pilot_qwen35_postfix_20260929/C0_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_postfix_20260929/C1_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_postfix_20260929/C2_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_postfix_20260929/C3_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_pilot_qwen35_postfix_20260929/C4_dev_arena_seed1/workspace/
?? experiments/gas0/analysis/dev_smoke_c4_feedback_20260930/C4_dev_arena_seed1_stages1to3/workspace/
?? experiments/gas0/analysis/model_selection_recoveryfix_20260929/qwen35/budget_planner_seed1/workspace/
?? experiments/gas0/analysis/model_selection_recoveryfix_20260929/qwen35/dev_arena_seed1/workspace/
```

## Boundary

Do not merge this branch or start cleanup automatically. Future consolidation must retain the archived wording and distinguish historical claims from current acceptance.
