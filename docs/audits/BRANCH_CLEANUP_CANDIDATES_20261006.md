# Branch cleanup candidates — 2026-10-06

This is a classification only. No branch is deleted, rewritten, force-pushed, or merged by this cleanup. Ref comparisons below use the locally available `origin/main` snapshot `2689e5f`; they are not a substitute for checking the live remote before any later deletion.

## KEEP — recent frontier work; retain through consolidation review

- `cleanup/current-state-20261006` — this cleanup branch, based on `origin/main`.
- `origin/main` — protected base branch; do not merge automatically as part of this cleanup.
- `codex/d2-time-varying-repair-20261005`, `codex/filtered-timing-packing-repair-20261005`, `codex/history-uniform-leverage-20261005`, `codex/private-complement-leverage-20261005`.
- `codex/multisurvivor-hadamard-write-20261005`, `codex/multisurvivor-hadamard-write-completion-20261005`, `codex/multisurvivor-hadamard-independent-20261005`, `codex/multicolumn-spatial-write-20261005`, `codex/moving-probe-spatial-write-20261005`.
- `codex/repeated-nearcritical-filter-write-20261005`, `codex/repeated-nearcritical-filter-independent-20261006`, `codex/frontier-invention-20261006`, `codex/linear-dimension-frontier-20261006`, `sol/k3-discrete-filter-comparison-20261006`, and `gemini/time-varying-nearcritical-filter-bank-20261006`.
- Their available `origin/codex/...` and `origin/sol/...` tracking refs, where present.

These refs contain work newer than `main` or independent review/repair snapshots. Keep them until the consolidated proof folders, source hashes, and review records have been checked against their branch histories.

## PRESERVATION — retain historical preservation snapshots

- `preserve/all-research-20261004` and `origin/preserve/all-research-20261004`.
- `preserve/local-theory-20261004` and `origin/preserve/local-theory-20261004`.

Their commits are already contained in the audited `origin/main` history, but the named refs serve as explicit preservation checkpoints. Retain unless the repository owner later changes that policy.

## MERGED OR SUPERSEDED — possible later cleanup candidates

- `cleanup/research-consolidation-20261004` and `origin/cleanup/research-consolidation-20261004`.
- `origin/cleanup/root-docs-20261005`.
- `main` (local ref `2e3ee7b`, behind the audited `origin/main` at `2689e5f`).
- Older Codex support branches whose commits are contained in `origin/main`: `codex/ams-v4-independent-verification-20260928`, `codex/ams-v6-independent-audit-20260928`, `codex/ar142-validity-audit-20260928`, `codex/automated-novelty-gate-20260927`, `codex/cursor-local-snapshot-20260927`, `codex/cursor-local-snapshot-20260927-v2`, `codex/filter-calibration-20260927`, `codex/learning-dynamics-sync-20260927`, and `codex/native-coupling-sync-20260927`.
- `theory/corridor-research-20261003`, whose commits are contained in `origin/main`.

The two older cleanup refs above have no commits unique from `origin/main` in this snapshot (`cleanup/research-consolidation` is 15 commits behind; `cleanup/root-docs` is 1 commit behind). They appear safe as future deletion candidates after a live-remote check and a final unique-content check. This report does not delete them.

## UNKNOWN — preserve pending owner/research-context review

- `origin/claude/admiring-turing-cvyhm0`, `origin/claude/gallant-bardeen-ybxn57`, and `origin/claude/wonderful-fermi-yx8b1e`.
- Any newly created or remote branch not enumerated above.

These Claude refs have commits not contained in `origin/main` in the available snapshot. Their relationship to active Claude work and the protected lane-reading policy has not been established here; keep them until their provenance and purpose are confirmed.
