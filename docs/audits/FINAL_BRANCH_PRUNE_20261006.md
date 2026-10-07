# Final Branch Prune Audit — 2026-10-06

Audited after the cleanup merge was pushed to `main` at `c8340fbf9b5d19942168fb7f1c67b517d5192a43`.
Commit ancestry counts below compare each ref against that `main`. A branch with zero commits ahead is fully reachable from `main`; this does not make a preservation ref disposable when the owner explicitly asked to retain it.

> **Updated after the subsequent branch-reduction pass:** the original 18-branch snapshot and first-prune record are retained below as history. The latest disposition and final count are in the final section, based on `main` at `c6c4ae1b0d4f8d614bb64a7ce0e70f48a8200970`.

## Deleted refs

| Branch | Refs deleted | Evidence |
|---|---|---|
| `cleanup/current-state-20261006` | local + remote | Cleanup tip was merged into main; no follow-up commits; content is on main. |
| `cleanup/root-docs-20261005` | remote | Tip was already contained in main; no unique commit/content. |
| `theory/corridor-research-20261003` | local + remote | Research head was already contained in main; no unique commit/content. |
| `cleanup/research-consolidation-20261004` | remote only | Zero commits ahead; ancestor of main. Local ref retained because a linked worktree still checks it out. |
| `codex/cursor-local-snapshot-20260927` | remote only | Zero commits ahead; ancestor of main. Local ref/worktree retained. |
| `codex/cursor-local-snapshot-20260927-v2` | remote only | Zero commits ahead; ancestor of main. Local ref/worktree retained. |

## Current branch classifications

| Branch/ref | Commits ahead / behind main | Classification | Reason / action |
|---|---:|---|---|
| `main` | 0 / 0 | KEEP | Current pushed authoritative line. |
| `preserve/all-research-20261004` | 0 / 23 | PRESERVATION | Explicit preservation checkpoint; retained despite ancestry. |
| `preserve/local-theory-20261004` | 0 / 26 | PRESERVATION | Explicit preservation checkpoint; retained despite ancestry. |
| `claude/admiring-turing-cvyhm0` (remote) | 0 / 171 | KEEP | Explicitly retain unknown Claude work. |
| `claude/gallant-bardeen-ybxn57` (remote) | 1 / 32 | KEEP | Has a unique commit; retain. |
| `claude/wonderful-fermi-yx8b1e` (remote) | 5 / 40 | KEEP | Has unique commits; retain. |
| `codex/d2-time-varying-repair-20261005` | 1 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/filtered-timing-packing-repair-20261005` | 2 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/frontier-invention-20261006` | 11 / 6 | KEEP | Recent frontier provenance; linked worktree. |
| `codex/history-uniform-leverage-20261005` | 3 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/linear-dimension-frontier-20261006` | 12 / 6 | KEEP | Recent frontier provenance; linked worktree. |
| `codex/moving-probe-spatial-write-20261005` | 6 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/multicolumn-spatial-write-20261005` | 5 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/multisurvivor-hadamard-independent-20261005` | 7 / 6 | KEEP | Distinct review/provenance line; linked worktree. |
| `codex/multisurvivor-hadamard-write-20261005` | 7 / 6 | KEEP | Its relevant folder differs from main; retain original branch. |
| `codex/multisurvivor-hadamard-write-completion-20261005` (local) | 7 / 6 | KEEP | Alias at the same tip as the write branch; linked completion worktree. |
| `codex/private-complement-leverage-20261005` | 4 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/repeated-nearcritical-filter-independent-20261006` | 8 / 6 | KEEP | Recent theory provenance; linked worktree. |
| `codex/repeated-nearcritical-filter-write-20261005` (local) | 8 / 6 | KEEP | Its relevant folder differs from main; retain. |
| `gemini/time-varying-nearcritical-filter-bank-20261006` (local) | 9 / 6 | KEEP | Current original checkout; local untracked review work remains there. |
| `sol/k3-discrete-filter-comparison-20261006` | 10 / 6 | KEEP | Recent review provenance; linked worktree. |
| `cleanup/research-consolidation-20261004` (local) | 0 / 18 | SAFE TO DELETE LATER | Fully reachable from main; local linked worktree still checks it out, so left intact. |
| `codex/ams-v4-independent-verification-20260928` (local) | 0 / 260 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/ams-v6-independent-audit-20260928` (local) | 0 / 241 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/ar142-validity-audit-20260928` (local) | 0 / 285 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/automated-novelty-gate-20260927` (local) | 0 / 294 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/cursor-local-snapshot-20260927` (local) | 0 / 299 | SAFE TO DELETE LATER | Fully reachable from main; local linked worktree remains. |
| `codex/cursor-local-snapshot-20260927-v2` (local) | 0 / 293 | SAFE TO DELETE LATER | Fully reachable from main; local linked worktree remains. |
| `codex/filter-calibration-20260927` (local) | 0 / 307 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/learning-dynamics-sync-20260927` (local) | 0 / 300 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |
| `codex/native-coupling-sync-20260927` (local) | 0 / 304 | SAFE TO DELETE LATER | Fully reachable from main; linked worktree remains. |

Recent frontier branches remain even when their main-tree folder is represented, because their separate commits and review provenance remain useful. In particular, the multi-survivor write and repeated-filter-write folders are not byte-for-byte identical to main. No preservation branch, Claude branch, or unknown branch was deleted.

## Final branch counts

After pruning and fetching, GitHub has **18 branches including `main`** (the `origin/HEAD` symbolic ref is not a branch). Three remote branches were deleted in this final prune; three additional remote refs had already been deleted earlier in this hygiene task. Local refs with attached worktrees were intentionally retained rather than detaching or removing those worktrees as a side effect.

---

## Final branch-reduction pass

This pass started with the **18 GitHub branches** listed below and `main` at `c6c4ae1b0d4f8d614bb64a7ce0e70f48a8200970`. Ancestry counts are `branch..main` comparisons made before deletion. “Ahead” is the branch's unique commit count relative to main at the time of audit. The tip SHAs are the exact refs that were tagged before deletion.

| Starting remote branch | Tip SHA | Ahead | Behind | Relevant content / action |
|---|---|---:|---:|---|
| `claude/admiring-turing-cvyhm0` | `8e64c850aea05586dbbcd178f2b396f0de4ebe19` | 0 | 172 | Tip is an ancestor of main; archived exact tip, then deleted. Claude notebook was not opened. |
| `claude/gallant-bardeen-ybxn57` | `d8ed873a28ed952161a461917a45a812d6253d2b` | 1 | 33 | Multi-donor folder matches main, but its unique commit also changes `Claude_Research.md`; retained under the lane-reading rule. |
| `claude/wonderful-fermi-yx8b1e` | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` | 5 | 41 | Its two unique Claude review folders (188 files) match main byte-for-byte; archived exact tip, then deleted. No notebook change was in its unique commits. |
| `codex/d2-time-varying-repair-20261005` | `44c9e0e9090e8243f0f0030865e263cc7b21798e` | 1 | 7 | Folder exact on main; tag then delete. |
| `codex/filtered-timing-packing-repair-20261005` | `39c371452f2a025974bf0df6b6b920d7ebf91154` | 2 | 7 | Folder exact on main; tag then delete. |
| `codex/frontier-invention-20261006` | `5cfe9c40014f9bca0bf30969262e616ba97b0103` | 11 | 7 | Folder exact on main; tag then delete. |
| `codex/history-uniform-leverage-20261005` | `1992f93915a0a7995595468215af623726b6a1f7` | 3 | 7 | Folder exact on main; tag then delete. |
| `codex/linear-dimension-frontier-20261006` | `e841ecb2f2f164f61f94c91485c8983618c6a558` | 12 | 7 | Folder exact on main; tag then delete. |
| `codex/moving-probe-spatial-write-20261005` | `df9ef3379097acc1f1c0e86fa480d94bcf8321d4` | 6 | 7 | Folder exact on main; tag then delete. |
| `codex/multicolumn-spatial-write-20261005` | `9bf66b91cc033ecae589f0b2b630acec01e58118` | 5 | 7 | Folder exact on main; tag then delete. |
| `codex/multisurvivor-hadamard-independent-20261005` | `b484504b30c412d2c19820b0927f0d53008fbe96` | 7 | 7 | Shared multisurvivor folder matches main; tag then delete. |
| `codex/multisurvivor-hadamard-write-20261005` | `8db6ab1f4022ce16b4baa7c0c238dfd1ac537e9f` | 7 | 7 | Historical folder differs from main in 8 paths; exact branch tip preserved by tag before deletion. |
| `codex/private-complement-leverage-20261005` | `644d023c8a929361b5413636a9ac8325d043772d` | 4 | 7 | Folder exact on main; tag then delete. |
| `codex/repeated-nearcritical-filter-independent-20261006` | `866df3e25694b3271e7bfc31338d3bb00015511a` | 8 | 7 | Its relevant folders match main; tag then delete. |
| `main` | `c6c4ae1b0d4f8d614bb64a7ce0e70f48a8200970` | 0 | 0 | KEEP; source of truth. |
| `preserve/all-research-20261004` | `d1767d0a62dba90b03fd21e512b3db0c4efcd133` | 0 | 24 | PRESERVATION; explicitly retained. |
| `preserve/local-theory-20261004` | `74232f2d1d386db45ccd5712fc684da0d82d6733` | 0 | 27 | PRESERVATION; explicitly retained. |
| `sol/k3-discrete-filter-comparison-20261006` | `b8d17b3e1130838af4eb3f30d6b02a5109506449` | 10 | 7 | Folder exact on main; tag then delete. |

### Archive tag → original branch/ref → exact original tip

All listed tags were pushed and verified: the peeled remote tag commit equals the exact SHA shown.

| Archive tag | Original branch/ref | Exact commit |
|---|---|---|
| `archive/codex-d2-time-varying-repair-20261005` | `codex/d2-time-varying-repair-20261005` | `44c9e0e9090e8243f0f0030865e263cc7b21798e` |
| `archive/codex-filtered-timing-packing-repair-20261005` | `codex/filtered-timing-packing-repair-20261005` | `39c371452f2a025974bf0df6b6b920d7ebf91154` |
| `archive/codex-frontier-invention-20261006` | `codex/frontier-invention-20261006` | `5cfe9c40014f9bca0bf30969262e616ba97b0103` |
| `archive/codex-history-uniform-leverage-20261005` | `codex/history-uniform-leverage-20261005` | `1992f93915a0a7995595468215af623726b6a1f7` |
| `archive/codex-linear-dimension-frontier-20261006` | `codex/linear-dimension-frontier-20261006` | `e841ecb2f2f164f61f94c91485c8983618c6a558` |
| `archive/codex-moving-probe-spatial-write-20261005` | `codex/moving-probe-spatial-write-20261005` | `df9ef3379097acc1f1c0e86fa480d94bcf8321d4` |
| `archive/codex-multicolumn-spatial-write-20261005` | `codex/multicolumn-spatial-write-20261005` | `9bf66b91cc033ecae589f0b2b630acec01e58118` |
| `archive/codex-multisurvivor-hadamard-independent-20261005` | `codex/multisurvivor-hadamard-independent-20261005` | `b484504b30c412d2c19820b0927f0d53008fbe96` |
| `archive/codex-multisurvivor-hadamard-write-20261005` | `codex/multisurvivor-hadamard-write-20261005` | `8db6ab1f4022ce16b4baa7c0c238dfd1ac537e9f` |
| `archive/codex-private-complement-leverage-20261005` | `codex/private-complement-leverage-20261005` | `644d023c8a929361b5413636a9ac8325d043772d` |
| `archive/codex-repeated-nearcritical-filter-independent-20261006` | `codex/repeated-nearcritical-filter-independent-20261006` | `866df3e25694b3271e7bfc31338d3bb00015511a` |
| `archive/sol-k3-discrete-filter-comparison-20261006` | `sol/k3-discrete-filter-comparison-20261006` | `b8d17b3e1130838af4eb3f30d6b02a5109506449` |
| `archive/claude-admiring-turing-cvyhm0` | `claude/admiring-turing-cvyhm0` | `8e64c850aea05586dbbcd178f2b396f0de4ebe19` |
| `archive/claude-wonderful-fermi-yx8b1e` | `claude/wonderful-fermi-yx8b1e` | `fd0b3656dd3b632abbcb4b6b0112edd8f6b496bc` |
| `archive/codex-repeated-nearcritical-filter-write-20261005` | local-only `codex/repeated-nearcritical-filter-write-20261005` | `fff52bbd5b029b8705967f061a5a1f3f515c8b98` |
| `archive/gemini-time-varying-nearcritical-filter-bank-20261006` | local-only `gemini/time-varying-nearcritical-filter-bank-20261006` | `eb0374622b332149cd0f67dbb492f203f67c42a0` |

The multisurvivor completion local alias pointed at the same SHA as `codex/multisurvivor-hadamard-write-20261005`; it was removed after that exact commit was verified under the archive tag. The local-only repeated-filter-write branch had distinct content and received its own tag before deletion.

### Claude branch disposition

- `claude/admiring-turing-cvyhm0`: zero commits ahead and its tip is an ancestor of main. The historical tree, including its older root map layout, remains in main's reachable history. The branch was tagged and deleted; `Claude_Research.md` was not opened.
- `claude/wonderful-fermi-yx8b1e`: its two unique review folders (`claude_absolute_energy_review_20261003` and `claude_autonomous_energy_upper_review_20261003`) were compared file-by-file by Git blob and match main exactly. Its tip was tagged and the branch deleted. Its unique commits did not include a Claude notebook edit.
- `claude/gallant-bardeen-ybxn57`: the multi-donor folder matches main exactly, but its unique commit also modifies `Claude_Research.md`. The governing lane rule says Codex must not read that notebook unless the owner explicitly changes the rule. This audit does not read or relocate that content; the branch remains as the only branch ref protecting the unique commit.

### Final state

- Starting GitHub branch count: **18**.
- Remote branches deleted in this pass: **14** (12 Codex/Sol frontier branches and the admiring/wonderful Claude branches).
- Archive tags created in this pass: **16** (14 for deleted GitHub branches plus local-only repeated-filter-write and Gemini branch checkpoints).
- Final GitHub branch count: **4** — `main`, the two explicit `preserve/*` refs, and `claude/gallant-bardeen-ybxn57`.
- No preservation branch was deleted. Main remains at `c6c4ae1b0d4f8d614bb64a7ce0e70f48a8200970`.
- Twelve clean obsolete temporary worktrees associated with archived or contained refs were removed; no dirty worktree was removed. The original `ai new` checkout and clean main checkout remain. The exact committed tip of the local Gemini branch is also archived by tag, while its intentional untracked files remain only in the original checkout.
- Old worktrees with tracked deletions or other dirty state remain untouched. The unique Gallant Claude notebook commit also remains only on its retained branch; all other frontier branch tips are now reachable from archive tags, and the reviewed folders are represented on main.
