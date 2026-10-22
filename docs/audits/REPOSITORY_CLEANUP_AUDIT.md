# Repository engineering cleanup — 2026-10-21

**Current record: PARTIALLY CLEANED, final owner decision pending.** This is an execution
record, not another scientific audit. [Machine-readable inventory and hashes](REPOSITORY_CLEANUP_DATA.json)
are under `current_cleanup_20261021`; older JSON fields and the October 4 report below
remain historical snapshots. The [claim register](../CLAIM_REGISTER.md) remains the
scientific authority. The research freeze and original OPEN target are unchanged.

## Completed engineering

- Refreshed GitHub main at `b56a8ae486826928f2b45ace7e866bdfa03c4e07` (PR38 merged); inspected all 24 remote branches and 15 open PRs individually.
- Inventoried all 371 Git references across three repositories, 83 distinct tracked trees, 6,192 paths and 6,460 path/blob versions; also 22 embedded GAS-0 replay repositories. No historical checker was run.
- Preserved 94,583 physical files (17,557,327,934 logical bytes) in 13,733 hash-verified content blobs (5,674,878,774 bytes), plus 25 verified portable Git bundles. No source-copy errors or missing roots. Five audit/checkpoint samples were restored and hash verified.
- Backup: `E:\AI-Architecture-Research-preservation\cleanup-20261021`. Manifest SHA-256 `484ea076bcbfbcdd056d96298861d9bd4ad4def3a4d23c01c161503a233cd915`. `preserve_repository.py restore --root <original-root> --destination <new-empty-root>` restores file bytes; use `git bundle clone` for portable history and `git worktree repair` for relocated linked checkouts. Backup includes raw Git metadata, reflogs, ignored checkpoints, environments and embedded workspaces.
- Renamed divergent local main to `preserve/local-main-20261021`, published all its history and 448 local-only files plus 12 checkpoints at [`41f1c80dc87d38f4e5ee9f962ff4ddba40a4d12a`](https://github.com/soma2-stack/AI-Architecture-Research/commit/41f1c80dc87d38f4e5ee9f962ff4ddba40a4d12a). It retains all 107 commits absent main, including 13 absent every previous remote branch. No scientific history was merged into main.
- Created a clean local main at GitHub main, imported the other two repositories' refs into recovery namespaces, and archived nine stale local branch names transactionally. Three working branch names remain: main, this review branch and the local-evidence preservation branch.
- Archived 40 ignored/generated entries (including an embedded workspace), removed 22 verified empty directories, and left the canonical E: checkout clean. No unique raw file was discarded.
- Relocated seven inactive checkouts into the external archive, repaired Git links, detached and locked linked archives. Six E: audit checkouts are locked **in place** because NTFS lacks Delete permission. The owner-attached Desktop clone is retained pending its final retirement decision.
- Copied 17 existing independent audit folders / 573 files verbatim from pinned Git objects, including PR24/26/27/28/29/31/33/34/35/37 and the Route7A conditional audit. Frozen sources, checkers and raw artifacts are preserved as evidence; copying conveys no new proof verdict.
- Added raw-byte .gitattributes protection for all 17 copied audit folders; 54 artifacts contain CRLF that must not be normalized.
- Moved three historical root documents to docs/history, repaired six relative file links in the Codex archival notebook without changing prose, and repaired the missing Gemini audit target by preserving the original folder.
- Corrected stale PR descriptions #23, #27, #28, #29 and #30 using existing evidence. PR34–37 heads and scientific contents were not changed.

## File, duplicate and large-artifact decisions

GitHub baseline: **5,065 files, 774,121,553 bytes**, including 3,879 experiment files
and 1,149 theory files. All original paths/objects are recorded in the JSON. Every
baseline file remains at the same path or one of the three recorded history renames;
only navigation/maintenance data and six notebook link targets are edited.

The review tree adds 573 original audit artifacts; this is preservation, not evidence
of new research. Root documents fall from eight to five. The baseline has no tracked
Python caches, virtual environments, OS junk or temporary `.pyc/.tmp/.bak` files.

**All 136 exact-duplicate groups / 254 extra copies / 29,055,108 bytes are retained
with explicit reasons in the JSON.** Largest groups are invalid-run records, frozen
inputs and independent review copies. Equal bytes do not erase those roles. Distinct
named parameter outputs are not silently coalesced. Large `.npz`, zipped matrices and
checkpoint archives remain at their historical paths; no Git/LFS history rewrite or
external artifact migration is authorized. The ignored Desktop environment is captured
in the verified local backup and included in the retirement approval scope.

`.github/CODEOWNERS`, `.devcontainer/devcontainer.json`, AGENTS.md, primary scientific
sources and all original proof/result binaries remain unchanged. Local prototypes and
memory-triage records are preserved on the archival branch; they are not promoted to
verified architecture results. Directory and file-purpose labels are engineering
inventory, not a re-audit of every historical proof.

## Immutable audit-source link context

The 167 layout-dependent relative references inside preserved audits/source snapshots are
kept verbatim. The JSON field `immutableAuditLinkResolution` maps each to a verified
SHA-pinned GitHub target in its original repository layout, or explicitly labels a
later archival target. This supplies navigation without editing original audits or
importing their primary unmerged scientific sources. It does not extend any verdict
to a later revision. Active repository links are checked separately.

## Every remote branch

Ahead means commits absent pinned main, not exclusive scientific contribution.
Stack dependencies, exclusive counts, exact source paths and current versus historical
PR base SHAs are in the JSON. ARCHIVE is a disposition, not proof refutation.

| Branch | Inspected head | Disposition | Ahead main | Evidence / limit |
|---|---|---|---:|---|
| astra/private-survivor-independent-20261008 | `6297b112bcd7f0bea312a98cc81ecd956127825b` | ARCHIVE | 2 | No open PR. PARTIAL/INCONCLUSIVE comparison; fixed-gap echo conditional author theorem PENDING; weak echo OPEN. Cited main register Route7A table. Preserve 26 branch-added files, no rerun. |
| claude/dense-transfer-20261020 | `61163c58bf835c52874025272c8fa1f155bce974` | KEEP | 10 | KEEP draft, partly independently verified with later-source limitation; no merge |
| claude/gallant-bardeen-ybxn57 | `d8ed873a28ed952161a461917a45a812d6253d2b` | ARCHIVE | 1 | No open PR. Unique d8ed873 multi-donor joint-section author derivations; REPORT explicitly requires independent review, no exponent below3/4 proved, conditional H_TM unclosed. Preserve 4 scientific files plus index historical delta; do not upgrade author PROVED. |
| claude/hypothesis-b-bus-20261015 | `f05694454956edab849ebe7d1858131eaca4174c` | CONSOLIDATE | 5 | PROPOSE CLOSE after verified refutation and original audit artifacts are archived |
| claude/lemma-m-bus-capacity-20261015 | `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab` | CONSOLIDATE | 2 | KEEP stack anchor until later-stack archival resolution; no direct merge |
| claude/lemma-m-rest-20261016 | `cef12b3eb6e5a8e6dbc75904253222b57eda188c` | ARCHIVE | 3 | KEEP stack anchor until dependent PRs archived; no direct merge |
| claude/lemma-m-sequential-repair-20261020 | `d620d015057c4026a1c2c31c3828df570bc9fb3b` | KEEP | 8 | KEEP draft; preserve exact audits; no scientific merge authorized |
| claude/lemma-m-three-memory-20261019 | `d6801c2bb1b311b3d132312535b87c86064d2eb9` | ARCHIVE | 4 | KEEP stack anchor until PR34–35/37 resolution; later PROPOSE CLOSE as superseded/refuted |
| claude/multiprobe-memory-20261014 | `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88` | ARCHIVE | 6 | PROPOSE CLOSE as retired conditional route, preserving audited foundations |
| claude/narrow-capture-hub-20261013 | `c9874081461139373a276efeb47394d50781c0e3` | CONSOLIDATE | 13 | PROPOSE CLOSE after scoped result and audits archived |
| claude/neutral-path-tax-20261013 | `e13311b1d4d6d7ea227f7c9caa1931636cb55502` | ARCHIVE | 1 | PROPOSE CLOSE as wrong-budget route after source+negative audit preserved |
| claude/remaining-channels-20261020 | `f7931ad3b0237e295571dfb48860a1338f8a2fa9` | KEEP | 15 | KEEP draft as audited PARTIAL/OPEN archive; repeatC5 withdrawn; no scientific merge |
| claude/shift-holonomy-audit-20261013 | `d899895aab81b36a3128a375ae2238b08f73f4af` | CONSOLIDATE | 2 | PROPOSE CLOSE after coordinated QSR+independent-review archival consolidation |
| codex/claim-register-20261021 | `1433bee0a518923600f8cf94d4eeea5224e65f7d` | ARCHIVE | 0 | PR38 merged asb56a8ae; branch tree identical main and0ahead. Redundant branch eligible owner-approved eventual deletion, retain exact commit reference. |
| codex/pr24-independent-hostile-review | `50bb5ffabf33b28099238acb6440cb1a349079e3` | CONSOLIDATE | 1 | PROPOSE CLOSE after byte-preserving review-folder consolidation alongside PR24 |
| codex/pr35-trainable-balanced-memory-20261020 | `bbc16f6224e254dc6a326ff1e283cf792b25e990` | ARCHIVE | 62 | PROPOSE CLOSE after full negative evidence/checkpoint provenance indexed; no rerun |
| codex/route7a-long-window-20261008 | `075c5ffdb0c08a37245260c55df401654761bc96` | CONSOLIDATE | 1 | 6 branch-added audit files. Existing Gemini audit at075c5ff verifies conditional donor code/combinedD=o(n) only with imported premises,fixedb=.05,W>=88006,n>=exp(exp(4.8e6)); finite<=1e6,W<=64 not applicable/refuted. Preserve audit verbatim; no simulation. |
| docs/claude-research-handoff-20261015 | `afb6f3c5d09f0ffbaba23aca1dfa2db4fb73b347` | ARCHIVE | 1 | PROPOSE CLOSE as superseded navigation after SHA indexed |
| gemini/astra-route7a-feedback-audit-20261008 | `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9` | ARCHIVE | 0 | Already ancestor of main;0ahead. Scoped conditional feedback audit remains in main, not a universal result. Eligible redundant branch retirement after preserving reference. |
| gemini/pr26-neutral-hole-audit-20261013 | `2f3a3d248e02306408195312f3ca258ac8b357e8` | CONSOLIDATE | 2 | Contains PR26 plus2 independent audit files REVIEW.md,indep_sim.py. Independently rejects required peak-width budget. Additive byte-preserving audit consolidation safe; no author-branch merge. |
| main | `b56a8ae486826928f2b45ace7e866bdfa03c4e07` | KEEP | 0 | Canonical GitHub authority atb56a8ae; PR38 merged. Do not blindly add107 local-main commits. |
| preserve/all-research-20261004 | `d1767d0a62dba90b03fd21e512b3db0c4efcd133` | ARCHIVE | 0 | Already ancestor of main;0ahead. Historical preservation provenance intact, no automatic merge/deletion. |
| preserve/local-theory-20261004 | `74232f2d1d386db45ccd5712fc684da0d82d6733` | ARCHIVE | 0 | Already ancestor of main;0ahead. Historical local-theory evidence preservation intact, no automatic merge/deletion. |
| prototype/rnn-llm-architecture-v0-20261007 | `192df629e060def0983c4e85f70c4dd01b15b6a0` | ARCHIVE | 57 | PROPOSE CLOSE after preserved source and negative records are indexed |

New archival branch `preserve/local-main-20261021` retains unique local work without
scientific acceptance; `codex/repository-cleanup-20261021` carries this engineering
review. Neither authorizes research. No remote branch has been deleted.

## Every open scientific PR

No scientific PR has been merged or closed by this pass. Independent review scope
is narrower than branch contents; stacked heads do not automatically contain newer
lower-PR audit-preservation commits. This is why audits are preserved independently.

| PR | Disposition | Contribution | Existing review scope | Proposed owner resolution |
|---|---|---|---|---|
| [#23](https://github.com/soma2-stack/AI-Architecture-Research/pull/23) | ARCHIVE | Finite protected-cell copy-task successes and later memory/equivalence investigations; reusable GRU/LSTM harness. | C01 VERIFIED finite task; C02 REFUTED novelty; October21 audits. Initially inspected body had obsolete 127-tests/untrained wording; corrected during this cleanup. | PROPOSE CLOSE after preserved source and negative records are indexed |
| [#24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24) | CONSOLIDATE | Repaired modified quadratic-shift recurrence result, separate from original dense-tanh contract. | C03 REFUTED transfer to original target; C04 VERIFIED scoped QSR through PR25 review including n/1004 correction. | PROPOSE CLOSE after coordinated QSR+independent-review archival consolidation |
| [#25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25) | CONSOLIDATE | Independent hostile QSR review, rational identities and rounding counterexample. | C04 VERIFIED within scoped modified QSR model, original target OPEN. | PROPOSE CLOSE after byte-preserving review-folder consolidation alongside PR24 |
| [#26](https://github.com/soma2-stack/AI-Architecture-Research/pull/26) | ARCHIVE | Neutral-hole Householder broadcast candidate and finite numerical checks. | C05 REFUTED peak-width budget: m about n/2,T about n/4 => mT about n²/8, not summed support. | PROPOSE CLOSE as wrong-budget route after source+negative audit preserved |
| [#27](https://github.com/soma2-stack/AI-Architecture-Research/pull/27) | CONSOLIDATE | Fixed-K selected-subspace/public-schedule resource inequality. | C06 VERIFIED within listed assumptions; final PR27 repair audit plus cross-PR audit on PR28; no full-gradient barrier. | PROPOSE CLOSE after scoped result and audits archived |
| [#28](https://github.com/soma2-stack/AI-Architecture-Research/pull/28) | ARCHIVE | Multi-probe ingredients and conditional Theorem4. | C07 PARTIAL: Theorem4 implication survives but original B is refuted by PR29; no unconditional barrier. | PROPOSE CLOSE as retired conditional route, preserving audited foundations |
| [#29](https://github.com/soma2-stack/AI-Architecture-Research/pull/29) | CONSOLIDATE | R0 and prescribed-dense counterexamples to original Hypothesis B; scoped structure. | C08 REFUTED original B with independent R0+dense audits; C09 extended full-group Proposition0.2 OPEN. | PROPOSE CLOSE after verified refutation and original audit artifacts are archived |
| [#30](https://github.com/soma2-stack/AI-Architecture-Research/pull/30) | ARCHIVE | Root handoff/documentation only. | C10 REFUTED independent-result interpretation; main claim register supersedes status. Initially inspected body incorrectly said dense audits were not committed; corrected during this cleanup. | PROPOSE CLOSE as superseded navigation after SHA indexed |
| [#31](https://github.com/soma2-stack/AI-Architecture-Research/pull/31) | CONSOLIDATE | First-order gather/two-channel listing; incomplete higher-order scope. | C11 VERIFIED within scope via October21 evidence and PR37 audit history; M_rest open. | KEEP stack anchor until later-stack archival resolution; no direct merge |
| [#32](https://github.com/soma2-stack/AI-Architecture-Research/pull/32) | ARCHIVE | Two-stream bus structure/contraction and partial operator reduction. | C12 PARTIAL; full M_rest not closed. | KEEP stack anchor until dependent PRs archived; no direct merge |
| [#33](https://github.com/soma2-stack/AI-Architecture-Research/pull/33) | ARCHIVE | Three-memory probe plus original sequential quarter-root construction. | C13 REFUTED universal second-order certificate at extreme n; later PR34 repair separately scoped. | KEEP stack anchor until PR34–35/37 resolution; later PROPOSE CLOSE as superseded/refuted |
| [#34](https://github.com/soma2-stack/AI-Architecture-Research/pull/34) | KEEP | Repaired R0 quarter-root theorem plus two original independently preserved audit records. | C14 VERIFIED at39af3a97; C15 narrow final f515e48 PASS for Lemma5.0R/Prop5.4 via separate comparison; C31 audit availability verified. | KEEP draft; preserve exact audits; no scientific merge authorized |
| [#35](https://github.com/soma2-stack/AI-Architecture-Research/pull/35) | KEEP | Prescribed-dense cube-root exact-real construction and original audit provenance. | C16 VERIFIED atb984ef9 only; aa47ca5 auxiliary corrections PENDING exact-revision review; C16a different certificate scopes; C17 practical interpretation REFUTED. | KEEP draft, partly independently verified with later-source limitation; no merge |
| [#36](https://github.com/soma2-stack/AI-Architecture-Research/pull/36) | ARCHIVE | Trainable balanced-pair surrogate,123 matched600-update runs; no registered control advantage. | C18 REFUTED advantage, C19 REFUTED theorem-falsification interpretation; 3,000-update proposal WITHDRAWN. | PROPOSE CLOSE after full negative evidence/checkpoint provenance indexed; no rerun |
| [#37](https://github.com/soma2-stack/AI-Architecture-Research/pull/37) | KEEP | Remaining channels Steps3–3.7 with preserved independent audits and documentation repairs. | C20 theorem VERIFIED audited bath assumptions; C21 signed-monotone REFUTED; C22–24 PARTIAL operator/legal/dimension distinction; common-query identity passes, kernel bound OPEN. | KEEP draft as audited PARTIAL/OPEN archive; repeatC5 withdrawn; no scientific merge |

## Every local checkout

The canonical local working repository is **E:\AI-Architecture-Research**. Its main
tracks GitHub main; the separate cleanup worktree is the sole active review checkout.
Other linked archives are detached/locked; the standalone atlas archive and Desktop
legacy clone retain their original raw work. All original refs and dirty/ignored file
records are in the verified snapshot; all original commit IDs are retained.

| Original checkout | Disposition | Current location |
|---|---|---|
| `C:\Users\coler\AppData\Local\Temp\ai-atlas-review` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\02-ai-atlas-review` |
| `C:\Users\coler\AppData\Local\Temp\ai-ch` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\04-ai-ch` |
| `C:\Users\coler\AppData\Local\Temp\ai-dt` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\05-ai-dt` |
| `C:\Users\coler\AppData\Local\Temp\ai-m3r` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\06-ai-m3r` |
| `C:\Users\coler\AppData\Local\Temp\ai-memory-freeze` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\07-ai-memory-freeze` |
| `E:\AI-Architecture-Research-PR34-checkers` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR34-checkers` |
| `E:\AI-Architecture-Research-PR35-checkers` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR35-checkers` |
| `E:\AI-Architecture-Research-PR37-audit` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR37-audit` |
| `E:\AI-Architecture-Research-PR37-step35-audit` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR37-step35-audit` |
| `E:\AI-Architecture-Research-PR37-step36-audit` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR37-step36-audit` |
| `E:\AI-Architecture-Research-PR37-step37-audit` | ARCHIVE IN PLACE | `E:\AI-Architecture-Research-PR37-step37-audit` |
| `C:\Users\coler\.codex\worktrees\pr24-hostile-review\ai new` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\14-ai new` |
| `C:\Users\coler\AppData\Local\Temp\ai-m3` | ARCHIVE | `E:\AI-Architecture-Research-preservation\cleanup-20261021\checkouts\15-ai-m3` |
| `E:\AI-Architecture-Research` | KEEP canonical; clean main matches GitHub | `E:\AI-Architecture-Research` |
| `C:\Users\coler\AppData\Local\Temp\AI-Architecture-Research-claim-register` | KEEP until cleanup review/merge is resolved | `C:\Users\coler\AppData\Local\Temp\AI-Architecture-Research-claim-register` |
| `C:\Users\coler\OneDrive\Desktop\ai new` | ARCHIVE pending approval; owner-attached legacy clone, all raw work and environment backed up; refs imported into canonical repository | `C:\Users\coler\OneDrive\Desktop\ai new` |

## Engineering verification

**PASS (repository integrity; not a new proof audit).** The independent helper checked
all 573 source blobs/modes, all 5,065 baseline-file dispositions, three exact moves,
six link-only notebook edits, all branch/PR/checkout dispositions, the five corrected
live PR descriptions and all 167 immutable-context link mappings. No scientific
claim was upgraded. The parent additionally verified 36,696 relocated physical data
files against the preservation snapshot, 371 original refs / 86 distinct ref objects,
566 relative file targets and 83 SHA-pinned project targets. Missing active link
targets: **0**. All thirteen archived checkout heads match their inspected revisions.
Maintenance whitespace checks pass; original audit CRLF/trailing whitespace remains
verbatim. The claim register, AGENTS.md, other lane notebooks, CODEOWNERS and
development-container configuration retain their baseline Git blobs.

The machine record contains both verification results and a complete current-file
inventory reconstructed from preservation accounting plus explicit documentation
overrides. Its own Git hash is supplied by the containing commit rather than a
self-referential checksum. Validation scripts used file/Git/JSON operations only;
no scientific checker, experiment, training or proof-development process was run.

## Single consolidated owner approval required

All non-destructive preparation is complete in this review branch. These operations
are deliberately **not reported as completed**:

1. Approve and merge the documentation/evidence/organization cleanup PR; do not merge
   scientific PR34–37. Fast-forward canonical local main only after that merge.
2. Close PRs **#23, #24, #25, #26, #27, #28, #29, #30, #31, #32, #33, #36** after preserving their
   scoped evidence; their remote source histories remain available. Keep #34, #35 and
   #37 open and frozen. Closing does not label all their auxiliary claims false.
3. Delete only the four already-merged remote refs listed below, after checking their
   exact heads again. Their commits are ancestors of main; no open PR depends on them.
   - `codex/claim-register-20261021` at `1433bee0a518923600f8cf94d4eeea5224e65f7d`.
   - `gemini/astra-route7a-feedback-audit-20261008` at `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9`.
   - `preserve/all-research-20261004` at `d1767d0a62dba90b03fd21e512b3db0c4efcd133`.
   - `preserve/local-theory-20261004` at `74232f2d1d386db45ccd5712fc684da0d82d6733`.

4. Retire the fourteen legacy checkout copies listed in the JSON (seven relocated,
   six locked in place and the Desktop legacy clone), and retire the cleanup worktree
   after an approved merge. Preserve the external snapshot, Git bundles and archival
   history branch. Scoped NTFS Delete permission repair is required for the owned E:
   archive/audit directories; no research-folder ACL has been changed in preparation.

No unique data, remote scientific branch, scientific PR or main merge is removed or
resolved implicitly. Until owner approval and successful application/verification of
those operations, the repository is **PARTIALLY CLEANED**, not FULLY CLEANED.

---

## Historical October 4 execution record (preserved below)

# Repository consolidation and artifact audit — 2026-10-04

Audit only. No historical evidence deletion, migration, branch deletion, history rewriting, or broad ignore change was performed. Machine-readable complete duplicate groups, branch commits, and sizes: [REPOSITORY_CLEANUP_DATA.json](REPOSITORY_CLEANUP_DATA.json).

## Baseline and consolidation

Exact preservation base: `d1767d0a62dba90b03fd21e512b3db0c4efcd133`. Audited research/navigation snapshot: `501eb37647509504d69f17cc3b17b97e2b29af6d` on `cleanup/research-consolidation-20261004`. Branch ahead/behind figures and local-worktree validation below are relative to that explicit snapshot. Later commits correct audit wording and scientific-status/navigation claims after independent review; they do not retroactively extend the snapshot-specific local validation to the final PR head.

Original local worktree: `C:/Users/coler/OneDrive/Desktop/ai new`. Separate cleanup worktree: `C:/Users/coler/AppData/Local/Temp/ai-research-consolidation-20261004`. Original GAS-0 changes, archival notebooks and untracked work were not staged or modified.

Gallant-bardeen original commit `d8ed873a28ed952161a461917a45a812d6253d2b` was cherry-picked as `6b618ed`, preserving author/message and all four theory files. Its notebook conflict was resolved by retaining the cleanup-base notebook bytes; no notebook edits were imported. Original commit remains on its source remote branch. This is a documented provenance deviation, not an ancestry claim.

Wonderful-fermi was not merged. Only three absent independent review folders were imported in `e339ef5`; their original blobs match exactly. Unique source commits are `3a18102` (bounded-local review), `3450fbb` (absolute-energy review), and `fd0b365` (autonomous-energy upper review). Source merge commits and notebook edits were not imported. No additional theory folder on that branch is absent after integration.

| Imported folder | Files | Bytes | Source |
|---|---:|---:|---|
| `theory/claude_multidonor_joint_section_20261004/` | 4 | 35,792 | `d8ed873a28ed952161a461917a45a812d6253d2b` |
| `theory/claude_bounded_history_radius_review_20261003/` | 17 | 62,391 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |
| `theory/claude_absolute_energy_review_20261003/` | 67 | 285,855 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |
| `theory/claude_autonomous_energy_upper_review_20261003/` | 121 | 602,008 | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |

All 29 prior local theory folders, four Claude experiment-review folders, Perplexity draft/provenance, and corridor ancestry remain. Imported evidence has no new acceptance status merely because it was consolidated. Claude multidonor is CONDITIONAL as a compression theorem; Codex spatial-write and multi-donor new claims are PENDING REVIEW. Dedicated unpaired-review folder is absent; owner acceptance is the recorded basis. A post-consolidation independent audit found that the Grok `D=2` monotonicity completion has an unresolved time-varying-propagator proof gap and that the filtered-timing disjoint-packing necessity is inferred from a lower bound in the wrong direction. Current navigation now marks those theorem claims pending rather than established; historical Grok reports remain unchanged.

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

Snapshot results: [CONSOLIDATION_VALIDATION.json](CONSOLIDATION_VALIDATION.json) checks head `501eb37647509504d69f17cc3b17b97e2b29af6d`. All preservation, link, ancestry, original-worktree hash/status, and audited-head checks passed for that snapshot. Later documentation/status-correction commits were reviewed through GitHub but were not rerun through the original local-worktree validation harness, so this file does not claim final-head validation. Git reported two zero-sized garbage/temp entries during object inventory; these were left untouched. No Git garbage collection or pruning was performed.
