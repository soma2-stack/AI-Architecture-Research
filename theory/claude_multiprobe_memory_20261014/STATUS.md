# Status — claude_multiprobe_memory_20261014

**Type:** author theory (+ autograd identity checks). **Repository status:** PENDING
INDEPENDENT REVIEW.

| Item | Status |
|---|---|
| Main problem `D = Omega(n)`, `mT = o(n^(3/2))`, full d_F | **OPEN** (unchanged) |
| Theorem 2 (code-dependent schedules, bounded probes) | PROVED (author) |
| Theorem 3 / Cor. 3.5 (chain-memory capacity) | PROVED (author) |
| Lemmas 1.1–1.3, 3.1, 3.2, 3.4 | PROVED (identities verified by autograd) |
| Cor. 3.3 (gather capacity) | CONDITIONAL |
| §4 designs | REFUTED as routes below `n^(3/2)` |
| §6 reduction of the full-d_F problem | ANALYSIS (outline) + precise open lemma |

**Exact next action.** Prove or refute the bus-capture lemma of PROOF.md §6.
