# Status — claude_multiprobe_memory_20261014

**Type:** author theory, plus exact-identity checks. **Repository status:** PENDING
INDEPENDENT REVIEW. Repaired 2026-10-14 after the Codex and GPT-6 reviews; see
[REVIEW_RESPONSE.md](REVIEW_RESPONSE.md).

| Item | Status |
|---|---|
| Main problem `D = Omega(n)`, `mT = o(n^(3/2))`, full d_F | **OPEN** (unchanged) |
| Lemma 1.2 (row 0 and the gather row are separate exceptions) | PROVED (repaired) |
| Lemma 1.2' (all legal F-step queries) | PROVED (author) |
| Lemma 3.0 (own-injection paths end at row `d-1`; no wrap) | PROVED |
| Theorem 2 (code-dependent schedules, bounded probes, factor `< 2(1+3e-6)`) | PROVED relative to PR #27 (author) |
| Lemmas 3.1, 3.2, 3.4 and Theorem 3 (abstract chain capacity) | PROVED (author) |
| Cor. 3.5 (`8400 c^2 (pL/n)^2 + 2p`; `mT >= 1.38e-10 D sqrt n`, one-step queries) | CONDITIONAL on (H1)–(H5) |
| Cor. 3.3 (gather capacity) | CONDITIONAL |
| §7.0, Lemmas 7.1–7.3 (dense term, exact bus structure, capture budget, source channel) | PROVED (author) |
| Theorem 4 (full-d_F barrier for all schedules and legal queries) | CONDITIONAL on Hypothesis B |
| Hypothesis B (bus part `<= tau/4` at the zeros of the state-only listing) | **OPEN** |
| §4 and §6 designs (incl. bus relay) | REFUTED as routes below `n^(3/2)` (analysis) |

*Previous status (head `6ce7026`).* Cor. 3.5 was listed as PROVED with
`4300 c^2 (pL/n)^2 + 4p`, and the §6 bus-capture lemma as the only gap. Both statements are
superseded: the constants were not derivable, and the gap is now stated as Hypothesis B.

**Exact next action.** Prove or refute Hypothesis B (PROOF.md §7.5). The most promising
route is the U-path reformulation of §7.6. It would move the wrap-around transport into
chain memory, leaving the rank-two `X_t` transfers and a column-uniform piece.
