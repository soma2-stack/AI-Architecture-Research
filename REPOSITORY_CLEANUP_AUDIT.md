# Repository consolidation and artifact audit — 2026-10-04

Audit only. No historical evidence deletion, migration, branch deletion, history rewriting, or broad ignore change was performed. Machine-readable complete duplicate groups, branch commits, and sizes: [REPOSITORY_CLEANUP_DATA.json](REPOSITORY_CLEANUP_DATA.json).

## Baseline and consolidation

Exact preservation base: `d1767d0a62dba90b03fd21e512b3db0c4efcd133`. Audited research/navigation head: `501eb37647509504d69f17cc3b17b97e2b29af6d` on `cleanup/research-consolidation-20261004`. Branch ahead/behind figures below are relative to that explicit head; the subsequent audit commit adds documentation only.

Original local worktree: `C:/Users/coler/OneDrive/Desktop/ai new`. Separate cleanup worktree: `C:/Users/coler/AppData/Local/Temp/ai-research-consolidation-20261004`. Original GAS-0 changes, archival notebooks and untracked work were not staged or modified.

Gallant-bardeen original commit `d8ed873a28ed952161a461917a45a812d6253d2b` was cherry-picked as `6b618ed`, preserving author/message and all four theory files. Its notebook conflict was resolved by retaining the cleanup-base notebook bytes; no notebook edits were imported. Original commit remains on its source remote branch. This is a documented provenance deviation, not an ancestry claim.

Wonderful-fermi was not merged. Only three absent independent review folders were imported in `e339ef5`; their original blobs match exactly. Unique source commits are `3a18102` (bounded-local review), `3450fbb` (absolute-energy review), and `fd0b365` (autonomous-energy upper review). Source merge commits and notebook edits were not imported. No additional theory folder on that branch is absent after integration.

| Imported folder | Files | Bytes | Source |
|---|---:|---:|---|
| `theory/claude_multidonor_joint_section_20261004/` | 4 | 35,792 | `d8ed873a28ed952161a461917a45a812d6253d2b` |
| `theory/claude_bounded_history_radius_review_20261003/` | 17 | 62,391 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |
| `theory/claude_absolute_energy_review_20261003/` | 67 | 285,855 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |
| `theory/claude_autonomous_energy_upper_review_20261003/` | 121 | 602,008 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |

All 29 prior local theory folders, four Claude experiment-review folders, Perplexity draft/provenance, and corridor ancestry remain. Imported evidence has no new acceptance status merely because it was consolidated. Claude multidonor is CONDITIONAL as a compression theorem; Codex spatial-write and multi-donor new claims are PENDING REVIEW. Dedicated unpaired-review folder is absent; owner acceptance is the recorded basis. Grok filtered notes have owner-accepted scoped findings, not a fabricated independent-review relationship.

## Measured tracked tree and object storage

- Tracked files at audited head: **4,733**.
- Current tracked-tree blob payload: **711,382,332 bytes (678.43 MiB)**.
- Under experiments/: **645,994,893 bytes (616.07 MiB)**.
- Unique blobs in this current tree: **682,374,080 bytes (650.76 MiB)**.
- Redundant path payload from exact current-tree duplicates: **29,008,252 bytes (27.66 MiB)**, across **132** groups.

Sizes come from `git ls-tree -r -l`; they are scientific file payload, not filesystem allocation or full-history size. CRLF checkout sizes may differ. The JSON contains `git count-objects -v` for repository-wide loose/packed object storage shared by all worktrees. Packs include history and branches; current-tree totals must not be interpreted as Git-history shrink estimates.

```text
count: 673
size: 24258
in-pack: 6640
packs: 3
size-pack: 497708
prune-packable: 3
garbage: 2
size-garbage: 0
```

### Largest tracked files

| Path | Bytes |
|---|---:|
| `experiments/fixed_feature_reachable_operator_20261002/archive/n96_random_84101.npz` | 46,353,716 |
| `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n96_driven_coherent_86101.npz` | 46,045,186 |
| `experiments/feature_revision_20260930/model_checkpoints.tar.gz` | 29,247,054 |
| `experiments/exact_online_credit_stage_b_20260930/matrices.zip` | 26,399,470 |
| `experiments/fixed_feature_reachable_operator_20261002/archive/n64_random_84102.npz` | 19,929,329 |
| `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n64_driven_coherent_86102.npz` | 19,819,945 |
| `experiments/endpoint_width_scaling_20260930/certificate_deep_n3_9602100_full.json` | 15,575,412 |
| `experiments/exact_online_credit_stage_b_20260930/raw_width8.jsonl` | 15,460,363 |
| `experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/matrices.zip` | 10,532,576 |
| `experiments/exact_online_credit_stage_b2_20260930/matrices.zip` | 10,532,576 |
| `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n4.npz` | 10,045,826 |
| `experiments/robust_witness_search_20261001/spectra_search_dense_n4.npz` | 10,045,826 |
| `experiments/robust_witness_search_20261001/pool_n4.npz` | 9,688,286 |
| `experiments/robust_certificate_tightness_20261001/product_dense_n4_confirmation.npz` | 9,100,972 |
| `experiments/endpoint_width_scaling_20260930/certificate_dense_n4_9602100_full.json` | 9,002,228 |
| `experiments/robust_certificate_tightness_20261001/product_dense_n4_archived.npz` | 8,951,078 |
| `experiments/automated_mechanism_search/runs/stage3_v7/jobs.jsonl.gz` | 8,418,117 |
| `experiments/exact_online_credit_stage_b_20260930/family_matrices.zip` | 8,342,843 |
| `experiments/exact_online_credit_stage_b_20260930/raw_width16.jsonl` | 7,545,890 |
| `experiments/endpoint_width_scaling_20260930/certificate_deep_n3_9602100_local_base.json` | 7,122,171 |
| `theory/codex_two_pulse_corotating_20261002/single_n1000.npz` | 7,112,809 |
| `theory/codex_two_pulse_corotating_20261002/screen_1000_1000_1000_total-budget_spread.npz` | 6,515,500 |
| `theory/codex_two_pulse_corotating_20261002/screen_1000_1000_1000_sustained_spread.npz` | 6,515,314 |
| `experiments/robust_certificate_tightness_20261001/product_independent_n4_confirmation.npz` | 5,647,649 |
| `experiments/aperiodic_gate_spectrum_20261001/results/n256_diffuse_s62102_history.npz` | 5,600,577 |

### Extension/category payload

| Extension | Bytes | MiB |
|---|---:|---:|
| `.npz` | 378,360,757 | 360.83 |
| `.json` | 123,126,635 | 117.42 |
| `.jsonl` | 88,768,031 | 84.66 |
| `.zip` | 55,844,983 | 53.26 |
| `.gz` | 47,181,808 | 45.00 |
| `.md` | 6,415,587 | 6.12 |
| `.csv` | 6,010,144 | 5.73 |
| `.py` | 3,984,322 | 3.80 |
| `.npy` | 504,024 | 0.48 |
| `.log` | 485,567 | 0.46 |
| `.png` | 324,364 | 0.31 |
| `.txt` | 250,019 | 0.24 |
| `.patch` | 111,462 | 0.11 |
| `.out` | 11,690 | 0.01 |
| `(no extension)` | 2,447 | 0.00 |

### Exact duplicate blob groups

These groups share Git object IDs and identical repository blob contents. Git already deduplicates these blobs internally. Removing a duplicate path reduces checked-out path payload; it does not save that same amount in Git history. All groups and paths are in the JSON; representative largest groups follow.

- `b9bbe2e4bc07e83c695313121d957493d917d5f0`: 10,045,826 bytes x 2 paths. `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n4.npz`; `experiments/robust_witness_search_20261001/spectra_search_dense_n4.npz`
- `ddac0f50d4314e2663116ff40942f2ce2d088a7b`: 5,541,388 bytes x 2 paths. `experiments/antipodal_robust_dimension_20261001/frozen_dependencies/robust_certificate_tightness_20261001/inputs.json`; `experiments/robust_certificate_tightness_20261001/inputs.json`
- `e5964d97f63845718a506b2b3451a9a4c3d75f7c`: 4,417,858 bytes x 2 paths. `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n3.npz`; `experiments/robust_witness_search_20261001/spectra_search_dense_n3.npz`
- `86ec5d71d1412e95d2a9a2d4746e8891edac2c05`: 1,781,496 bytes x 2 paths. `experiments/anisotropic_robust_packing_replay_20261001/frozen_sources/certificate_dense_n3_9602100_full.json`; `experiments/endpoint_width_scaling_20260930/certificate_dense_n3_9602100_full.json`
- `23b6cd1de4f633e7c2eddea23efb36884d3d6a8f`: 1,456,884 bytes x 2 paths. `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n2.npz`; `experiments/robust_witness_search_20261001/spectra_search_dense_n2.npz`
- `34ed69de2153e1945efde2826f982e58b8d306a5`: 793,374 bytes x 2 paths. `experiments/robust_witness_search_20261001/invalid_attempt1/result_search_dense_n4.json`; `experiments/robust_witness_search_20261001/result_search_dense_n4.json`
- `3d8e76cca98622fbbfc5bf8d8441f99523dc44cc`: 730,710 bytes x 2 paths. `experiments/anisotropic_robust_packing_20260930/basis_dense_n3.json`; `experiments/anisotropic_robust_packing_replay_20261001/frozen_sources/basis_dense_n3.json`
- `93d8a8d40d8245a759ad0245c9aacf32846a8142`: 195,559 bytes x 4 paths. `experiments/radial_taylor_refinement_8d_20261001/control_bounds_192.npz`; `experiments/radial_taylor_refinement_8d_20261001/control_bounds_256.npz`; `experiments/third_order_antipodal_8d_20261001/bounds_192.npz`; `experiments/third_order_antipodal_8d_20261001/bounds_256.npz`
- `8417a5bdb9f83f1edb26af392b1209a02c76ce21`: 377,674 bytes x 2 paths. `experiments/robust_witness_search_20261001/invalid_attempt1/result_search_dense_n3.json`; `experiments/robust_witness_search_20261001/result_search_dense_n3.json`
- `59ec3f09b86f03a3ba67d0693669818dc1661057`: 159,274 bytes x 3 paths. `experiments/cleanroom_7d_interval_20261001/frozen_candidate.json`; `experiments/independent_dimension_feasibility_20261001/endpoint.json`; `experiments/rebalanced_7d_section_20261001/candidate.json`
- `524bc64cd83b475308ccd8f6e6cfb318657001bf`: 168,920 bytes x 2 paths. `experiments/rebalanced_7d_section_20261001/bounds_192.npz`; `experiments/rebalanced_7d_section_20261001/bounds_256.npz`
- `49b6820e8cd1847d070dc0f6ca8bb31a1e2c6869`: 166,886 bytes x 2 paths. `experiments/third_order_antipodal_7d_20261001/bounds_192.npz`; `experiments/third_order_antipodal_7d_20261001/bounds_256.npz`

## Artifact categories and scientific role

Filename classification below is a conservative audit heuristic, not permission to discard. Exact per-path duplicates are proved by blob identity; scientific necessity and reproducibility require workflow-specific review.

### Frozen dependencies / vendor copies

44 tracked paths, 9,539,072 bytes (9.10 MiB). Examples:

- `experiments/antipodal_robust_dimension_20261001/frozen_dependencies/robust_certificate_tightness_20261001/inputs.json`
- `experiments/anisotropic_robust_packing_replay_20261001/frozen_sources/certificate_dense_n3_9602100_full.json`
- `experiments/robust_witness_search_20261001/frozen_winners.json`
- `experiments/anisotropic_robust_packing_replay_20261001/frozen_sources/basis_dense_n3.json`
- `experiments/cleanroom_7d_interval_20261001/frozen_candidate.json`
- `experiments/claude_8d_review_20261001/cleanroom_8d/frozen_candidate.json`
- `experiments/antipodal_robust_dimension_20261001/FROZEN.json`
- `experiments/third_order_antipodal_8d_20261001/FROZEN.json`
### Invalid-attempt / retry evidence

125 tracked paths, 26,421,140 bytes (25.20 MiB). Examples:

- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n4.npz`
- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n3.npz`
- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_independent_n4.npz`
- `experiments/robust_witness_search_20261001/invalid_attempt1/phase_search_results.json`
- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n2.npz`
- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_independent_n3.npz`
- `experiments/anisotropic_robust_packing_20260930/attempts_svd.jsonl`
- `experiments/anisotropic_robust_packing_20260930/attempts_frame.jsonl`
### Archive outputs

21 tracked paths, 103,026,791 bytes (98.25 MiB). Examples:

- `experiments/feature_revision_20260930/model_checkpoints.tar.gz`
- `experiments/exact_online_credit_stage_b_20260930/matrices.zip`
- `experiments/exact_online_credit_stage_b2_20260930/corrected_single_thread/matrices.zip`
- `experiments/exact_online_credit_stage_b2_20260930/matrices.zip`
- `experiments/automated_mechanism_search/runs/stage3_v7/jobs.jsonl.gz`
- `experiments/exact_online_credit_stage_b_20260930/family_matrices.zip`
- `experiments/claude_8d_review_20261001/cleanroom_8d/exact_bounds_256.json.gz`
- `experiments/automated_mechanism_search/runs/stage2_repair1/records.jsonl.gz`
### Bulk arrays / JSONL

949 tracked paths, 467,632,812 bytes (445.97 MiB). Examples:

- `experiments/fixed_feature_reachable_operator_20261002/archive/n96_random_84101.npz`
- `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n96_driven_coherent_86101.npz`
- `experiments/fixed_feature_reachable_operator_20261002/archive/n64_random_84102.npz`
- `experiments/fixed_feature_reachable_operator_20261002/archive/supplement/n64_driven_coherent_86102.npz`
- `experiments/exact_online_credit_stage_b_20260930/raw_width8.jsonl`
- `experiments/robust_witness_search_20261001/invalid_attempt1/spectra_search_dense_n4.npz`
- `experiments/robust_witness_search_20261001/spectra_search_dense_n4.npz`
- `experiments/robust_witness_search_20261001/pool_n4.npz`

**Scientifically necessary:** accepted and failed proofs, independent review files, frozen witnesses and manifests, precision regeneration outputs, source hashes, preregistrations, repair/invalid-attempt evidence, and decisive attack/collision results. Frozen dependency copies can be part of isolated reproducibility; preserve until replacements reproduce the same bytes.

**Likely reproducible, not verified regenerated in this task:** NPZ matrices, repeated certificates, logs, and archived replay packages alongside scripts/configs. Reproducibility is only a candidate classification. Seeds, environment, source version, rounding settings and output hashes must first be checked. ZIP/GZ archives may uniquely bundle environments or evidence.

**Uncertain:** bulk JSON/JSONL/archives without complete regeneration metadata, snapshots documenting bugs/repairs, and numerical outputs whose exact producer or acceptance relationship is not explicit. Preserve and review individually. No experiment or theory script was run during consolidation.

## Three separate cleanup goals

1. **Working-tree cleanliness:** navigation and indexing can reduce confusion without removing evidence. Duplicate paths occupy checkout space but may preserve independent review provenance.
2. **Preventing future growth:** store new large regenerable arrays/checkpoints/raw streams outside normal Git, after workflow owners choose a verified artifact mechanism.
3. **Shrinking actual Git history:** deleting a currently tracked file does not remove it from historical Git objects. History rewriting/filter-repo/BFG or LFS migration of old commits would require separate explicit approval, published-history planning and backups. None was performed.

## Proposed future artifact policy — not executed

- Keep source, proofs/reports, compact checks, configs, seeds, preregistrations, hashes, manifests, and small decisive failure/success evidence in normal Git.
- Consider new giant NPZ/NPY matrices, bulk raw JSONL, large archives, checkpoints, and regenerable datasets for Git LFS, releases, or immutable artifact storage. LFS selection must account for access/quota and reproducibility.
- For every external artifact retain a small manifest with SHA256, bytes, producer script and commit, config/seed, software/precision environment, artifact URL/version, and the scientific result it supports.
- No broad `.gitignore` changes here. A later conservative proposal may ignore only reviewed generated scratch paths, `__pycache__/`, and editor temporary files; do not blanket-ignore JSON, NPZ, logs, or results, because existing certification workflows use them as evidence.
- Invalid-attempt and dependency snapshots must be individually reviewed before migration; provenance remains available even for failed results.

## Remote branch retirement audit

Ahead = commits on remote absent from audited cleanup `501eb37647509504d69f17cc3b17b97e2b29af6d`; behind = commits on audited cleanup absent from remote. SAFE TO DELETE LATER means ancestry proves zero unique commits; no branch was deleted. CONSOLIDATED for diverged Claude branches describes scientific-content coverage, not identical ancestry or notebook coverage.

| Remote branch | Head | Ahead / behind | Unique scientific material | Recommendation |
|---|---|---|---|---|
| `claude/admiring-turing-cvyhm0` | `8e64c850aea05586dbbcd178f2b396f0de4ebe19` | 0 / 152 | 0 absent scientific paths; 0 differing theory paths | **SAFE TO DELETE LATER** — All commits reachable from the audited cleanup head. |
| `claude/gallant-bardeen-ybxn57` | `d8ed873a28ed952161a461917a45a812d6253d2b` | 1 / 13 | 0 absent scientific paths; 0 differing theory paths | **CONSOLIDATED** — Unique scientific folders imported byte-identically; original commits and notebook history remain on this branch. No deletion recommendation. |
| `claude/wonderful-fermi-yx8b1e` | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` | 5 / 21 | 0 absent scientific paths; 0 differing theory paths | **CONSOLIDATED** — Unique scientific folders imported byte-identically; original commits and notebook history remain on this branch. No deletion recommendation. |
| `codex/cursor-local-snapshot-20260927` | `a1a58187f56f80b5a570dabd916c01e16385dd73` | 0 / 280 | 0 absent scientific paths; 0 differing theory paths | **SAFE TO DELETE LATER** — All commits reachable from the audited cleanup head. |
| `codex/cursor-local-snapshot-20260927-v2` | `dcea4510df75d85326455d8a31049c8c084a64bb` | 0 / 274 | 0 absent scientific paths; 0 differing theory paths | **SAFE TO DELETE LATER** — All commits reachable from the audited cleanup head. |
| `main` | `a8c5d3407580c96c32bb370f883952d2accf1c94` | 0 / 21 | 0 absent scientific paths; 0 differing theory paths | **KEEP** — Default branch and published baseline; no merge authorized. |
| `preserve/all-research-20261004` | `d1767d0a62dba90b03fd21e512b3db0c4efcd133` | 0 / 4 | 0 absent scientific paths; 0 differing theory paths | **CONSOLIDATED** — Full ancestry preserved; retain provenance branches for now. |
| `preserve/local-theory-20261004` | `74232f2d1d386db45ccd5712fc684da0d82d6733` | 0 / 7 | 0 absent scientific paths; 0 differing theory paths | **CONSOLIDATED** — Full ancestry preserved; retain provenance branches for now. |
| `theory/corridor-research-20261003` | `c682b271dd7bc98fcded9298da621c63b816ed34` | 0 / 10 | 0 absent scientific paths; 0 differing theory paths | **CONSOLIDATED** — Full ancestry preserved; retain provenance branches for now. |

Unique commit lists, absent paths, differing theory paths and all local branch heads are recorded in the JSON. Differing older theory blobs are not automatically new science. Claude notebook conflicts and omitted branch notebook edits mean source branches should be kept until owner provenance review. Remote main may be stale relative to research, but it remains the published baseline.

## Consistency and validation

- `Stage: Not started` replaced only in current-state navigation. Older dated “current” claims remain in historical reports/map below the additive checkpoint.
- Every theory directory appears once in INDEX and the structured ledger; current links resolve.
- Base scientific files are blob-identical; only the two authorized navigation files were changed among pre-existing paths. Governance and all three giant notebooks are unchanged.
- The old SHARED_RESEARCH_MAP bytes remain as an exact suffix after the additive checkpoint.
- Exact imported source blobs, preserved local theory paths and four review folder trees were checked. Corridor `c682b27` is an ancestor.
- Original worktree dirty/untracked status and file hashes are compared before push; original main and audited remote branch heads are checked.

The cleanup branch is for owner review. No merge to main is authorized. Independent scientific review of the pending spatial-write theorem is a separate next task.

Actual pre-push results: [CONSOLIDATION_VALIDATION.json](CONSOLIDATION_VALIDATION.json). All preservation, link, ancestry, original-worktree hash/status, and audited-head checks passed. Git reported two zero-sized garbage/temp entries during object inventory; these were left untouched. No Git garbage collection or pruning was performed.
