# Repository state audit — 2026-10-06

## Snapshot

- The audited `main` checkpoint is `2689e5feb862ef8e2461367180eef9313dfe7b6e` (`origin/main`). The local `main` ref was older at `2e3ee7b3faea9c908904a8202d85e95d2d5f8985`; the cleanup branch therefore starts from the audited remote-tracking checkpoint.
- Twelve theory folders present at the newer linear-frontier checkpoint `e841ecb2f2f164f61f94c91485c8983618c6a558` were absent from audited `main`; they are imported unchanged on this branch.
- The navigation snapshot in `04_RESEARCH_STATE.md`, `theory/CURRENT_THEORY.md`, `theory/INDEX.md`, and `theory/INDEX_LEDGER.json` did not include the Oct. 5–6 frontier work.
- Recent theory branches remain distinct from `main`; see [BRANCH_CLEANUP_CANDIDATES_20261006.md](BRANCH_CLEANUP_CANDIDATES_20261006.md). This cleanup does not delete or merge branches.
- Six local finite-size experiment folders were present. Five are complete enough to preserve in this branch. The optional R20–R32 folder remains marked `RUNNING` and is excluded from the committed evidence; its source remains in the original checkout.
- `AGENTS.md` is protected and unchanged.

## Cleanup plan

1. Start `cleanup/current-state-20261006` from the audited `origin/main` checkpoint.
2. Import the twelve named theory folders from the pinned `e841ecb` checkpoint without editing their internal proof files.
3. Preserve completed experiment scripts, summaries, measured JSON, metadata/progress records, and useful plots; exclude cache files and the incomplete optional R20–R32 run.
4. Refresh the current research resume, theory hierarchy, theory index and ledger, experiment index, and README navigation using the supplied scope and review calibration.
5. Validate provenance, paths, JSON, status wording, artifact sizes, and the resulting diff; commit and push this branch only. Do not merge to `main` or delete branches.

## Provenance and scope

Theory-folder contents are restored from the pinned checkpoint above and remain byte-for-byte source content. Experiment folders are copied from the pre-existing local checkout; measured values are not regenerated or edited. The cleanup branch is prepared in a separate worktree so approximately 3.9 GB of unrelated or still-local untracked research in the original checkout remains undisturbed.

The current strict-budget frontier is recorded as `D >= n/[10^70 log log n]` with `mT=o(n^(3/2))`; the linear boundary is `D=Omega(n)` at `mT=Theta(n^(3/2))`. The main open problem remains linear dimension at strict little-o budget. Bounded-stage obstruction wording is limited to the specified donor-control family. Finite-size results are labeled numerical evidence only.
