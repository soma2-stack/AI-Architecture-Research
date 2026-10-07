# Final Branch Prune Audit — 2026-10-06

Audited after the cleanup merge was pushed to `main` at `c8340fbf9b5d19942168fb7f1c67b517d5192a43`.
Commit ancestry counts below compare each ref against that `main`. A branch with zero commits ahead is fully reachable from `main`; this does not make a preservation ref disposable when the owner explicitly asked to retain it.

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
