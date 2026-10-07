# Local Untracked Material Audit — 2026-10-06

This is a preservation-first inventory of the original checkout at `C:\Users\coler\OneDrive\Desktop\ai new`. The attached pre-clean snapshot is [`LOCAL_UNTRACKED_INVENTORY_20261006.csv`](LOCAL_UNTRACKED_INVENTORY_20261006.csv); it records the pre-deletion file and directory inventory. Sizes below are exact bytes from filesystem enumeration, with decimal GB and binary GiB distinguished.

## Before and after

| Measure | Before cleanup | After cleanup |
|---|---:|---:|
| Non-ignored untracked files | 233 files / 62,866,522 bytes | 121 files / 2,613,017 bytes |
| Ignored files (including local environments and scientific outputs) | 8,841 files / 3,446,402,646 bytes | 6,075 files / 3,405,440,348 bytes |
| Combined untracked + ignored material | 9,074 files / 3,509,269,168 bytes | 6,196 files / 3,408,053,365 bytes |
| Combined size | 3.509 GB / 3.267 GiB | 3.408 GB / 3.173 GiB |

**Reclaimed: 101,215,803 bytes (about 101.2 MB).** This comprised 60,253,505 bytes of verified exact duplicate copies of files already committed on main, plus 40,962,298 bytes of Python bytecode and pytest caches. The original rough estimate of about 3.9 GB was larger than the measured pre-clean inventory.

## Disposition

- **Removed as exact duplicates:** six finite-size experiment folders whose path sets and every file blob matched main, plus the root `PERPLEXITY_PROOF_PACKET.txt`, whose Git blob matched its committed theory copy. The six folders were `finite_n_early_capture_20261006`, `finite_n_multistage_capture_20261006`, `finite_n_clear_scaling_20261006`, `finite_n_r8_diagnosis_20261006`, `finite_n_clean_mask_scaling_20261006`, and `finite_n_r20_r32_scaling_20261006`. The only extra files found inside those local copies were `.pyc` files.
- **Removed as cache:** 2,766 `.pyc` files and pytest cache contents under `__pycache__` / `.pytest_cache`. No research output or source script was removed.
- **Kept as completed research:** ignored scientific outputs, including `.npz` and `.pt` matrices/checkpoints, result files, plots, logs, archives, and experiment records. Large files were not removed based on age or size.
- **Kept as rebuildable but useful environment:** `experiments/robust_witness_search_20261001/.venv` (roughly 2.56 GB). It contains frozen CUDA/CuPy dependencies and is the largest source of local disk use. Its scripts and `runtime_packages.txt` support reproducibility; rebuilding it may be time-consuming, so it was retained.
- **Kept as active/current untracked theory:** `theory/grok_codex_gemini_joint_audit_20261006/`. It was not present as a committed copy and remains local.
- **Kept as GAS-0 work:** remaining untracked files are already under `experiments/gas0/analysis/.../workspace/` and `experiments/gas0/analysis/dev_pilot_qwen35_final_20260930/`. Their exact purpose and completion state were not enough to justify removal or relocation. The repository's tracked GAS-0 README and related files were untouched.
- **Kept as unknown:** 156 inventoried files / 1,342,708 bytes were classified uncertain and retained.

No active experiment, proof, report, result JSON, plot, source script, theorem file, or unknown material was deleted. Legitimate untracked research already sits under `theory/` or `experiments/`, so no historical folder was renamed or moved.

## Largest tracked files

Sizes are bytes; tracked files are on the merged main tree.

| Bytes | Path |
|---:|---|
| 46,353,716 | `experiments/fixed_feature_reachable_operator_20261002/archive/n96_random_84101.npz` |
| 46,045,186 | `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n96_driven_coherent_86101.npz` |
| 29,247,054 | `experiments/feature_revision_20260930/model_checkpoints.tar.gz` |
| 26,399,470 | `experiments/exact_online_credit_stage_b_20260930/matrices.zip` |
| 21,568,028 | `experiments/finite_n_r8_diagnosis_20261006/results.json` |
| 19,929,329 | `experiments/fixed_feature_reachable_operator_20261002/archive/n64_random_84102.npz` |
| 19,819,945 | `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n64_driven_coherent_86102.npz` |
| 17,494,399 | `experiments/finite_n_clear_scaling_20261006/results.json` |
| 15,575,412 | `experiments/endpoint_width_scaling_20260930/certificate_deep_n3_9602100_full.json` |
| 15,460,693 | `experiments/exact_online_credit_stage_b_20260930/raw_width8.jsonl` |
| 10,532,576 | `experiments/exact_online_credit_stage_b2_20260930/matrices.zip` |
| 10,532,576 | `experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/matrices.zip` |
| 10,045,826 | `experiments/robust_witness_search_20261001/spectra_search_dense_n4.npz` |
| 10,045,826 | `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n4.npz` |
| 9,680,286 | `experiments/robust_witness_search_20261001/pool_n4.npz` |
| 9,100,972 | `experiments/robust_certificate_tightness_20261001/product_dense_n4_confirmation.npz` |
| 9,002,228 | `experiments/endpoint_width_scaling_20260930/certificate_dense_n4_9602100_full.json` |
| 8,951,078 | `experiments/robust_certificate_tightness_20261001/product_dense_n4_archived.npz` |
| 8,418,117 | `experiments/automated_mechanism_search/runs/stage3_v7/jobs.jsonl.gz` |
| 8,342,843 | `experiments/exact_online_credit_stage_b_20260930/family_matrices.zip` |
| 7,546,020 | `experiments/exact_online_credit_stage_b_20260930/raw_width16.jsonl` |
| 7,460,981 | `experiments/finite_n_clean_mask_scaling_20261006/results.json` |
| 7,122,171 | `experiments/endpoint_width_scaling_20260930/certificate_deep_n3_9602100_local_base.json` |
| 7,112,809 | `theory/codex_two_pulse_corotating_20261002/single_n1000.npz` |
| 6,515,500 | `theory/codex_two_pulse_corotating_20261002/screen_1000_1000_1000_total-budget_spread.npz` |

No tracked file in this top-25 list exceeds 50 MiB.

## Largest remaining untracked / ignored files

These include ignored files because they account for most of the local footprint.

| Bytes | Path |
|---:|---|
| 668,673,536 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cublas/bin/cublasLt64_12.dll` |
| 477,564,928 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cusparse/bin/cusparse64_12.dll` |
| 287,136,768 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cufft/bin/cufft64_11.dll` |
| 283,129,856 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cusolver/bin/cusolver64_11.dll` |
| 187,460,096 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cusolver/bin/cusolverMg64_11.dll` |
| 102,518,272 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cublas/bin/cublas64_12.dll` |
| 89,899,520 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cuda_nvrtc/bin/nvrtc64_120_0.alt.dll` |
| 89,832,960 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/cuda_nvrtc/bin/nvrtc64_120_0.dll` |
| 87,359,488 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/nvjitlink/bin/nvJitLink_120_0.dll` |
| 79,197,696 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/nvidia/curand/bin/curand64_10.dll` |
| 69,007,360 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/cupy/cuda/thrust.cp311-win_amd64.pyd` |
| 46,487,169 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n96_driven_random_86102.npz` |
| 46,457,663 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n96_driven_random_86101.npz` |
| 46,354,411 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_random_84102.npz` |
| 46,353,716 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_random_84101.npz` |
| 46,343,143 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_novelty.npz` |
| 46,329,947 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_dense_84101.npz` |
| 46,316,698 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_dense_84102.npz` |
| 46,045,186 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n96_driven_coherent_86101.npz` |
| 46,026,695 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n96_driven_coherent_86102.npz` |
| 45,565,531 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_sparse_84102.npz` |
| 45,561,934 | `experiments/fixed_feature_reachable_operator_20261002/results/n96_sparse_84101.npz` |
| 44,908,032 | `experiments/robust_witness_search_20261001/.venv/Lib/site-packages/cupy/cuda/cub.cp311-win_amd64.pyd` |
| 20,051,996 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n64_driven_random_86101.npz` |
| 20,047,083 | `experiments/fixed_feature_reachable_operator_20261002/supplement_results/n64_driven_random_86102.npz` |

The only remaining files above 50 MiB in this list are the first eleven CUDA/CuPy environment files; all belong to the retained `.venv`. Exact SHA-256 comparison confirmed that the two `spectra_search_dense_n4.npz` paths are byte-identical (10,045,826 bytes). That duplicate remains in place because it is embedded in an `invalid_attempt1` provenance folder. The two `matrices.zip` files have equal lengths but different hashes, so they were not treated as duplicates.

## Rebuildability and future size

- `.pyc` and pytest caches are safe to regenerate and were removed.
- The local Python/CUDA environment can likely be rebuilt from its package metadata and experiment setup scripts, but rebuilding may take time; it remains preserved.
- `.npz`, `.pt`, `.jsonl`, `.zip`, `.gz`, logs, and plots are mixed research outputs. Some are reproducible, but no broad removal was attempted.
- Normal Git already deduplicates identical blobs across commits; removing a duplicate path from the working tree does not shrink old Git history. No history rewrite, Git LFS migration, or artifact migration was performed.
- Future normal Git content should include source, proofs, small/essential result summaries, manifests, hashes, and reproducibility metadata. Very large regenerable matrices, CUDA dependency environments, and bulky archives are candidates for separately approved artifact storage or release assets; this report makes no migration.

## Remaining local state

The original `ai new` checkout is still on the Gemini research branch and intentionally retains untracked local research. `git status --short` shows GAS-0 workspace/output paths and `theory/grok_codex_gemini_joint_audit_20261006/`; ignored local data is also retained. A separate clean `main` worktree is at `C:\Users\coler\OneDrive\Desktop\ai-new-cleanup-20261006`. Nothing was committed from the original checkout, and no experiment or theory status was changed.
