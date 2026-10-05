# Private-complement leverage

**Verdict: REFUTED** for the proposed bound over every ordinary physical
support. The failure occurs at age one.

A legal all-high one-step future query has an exceptional adjoint entry
greater than 0.66 at terminal-cycle coordinate d-1. One backward application
of the cycle shift moves that entry to ordinary coordinate d-2. This
coordinate lies outside the corridor tuples and therefore in the
tuple-common/private complement. The accepted reset gate there is greater
than 0.99. Rank-two Householder corrections at d-2 are only O(1/sqrt(n)),
and the dense correction is negligible. Consequently
\[
\Lambda_\perp(N-1,\{d-2\})>.64
\]
for n at least 10^6, while the proposed scale is \(C/\sqrt n\).

This does **not** contradict the accepted packing-repair estimate on its
actual changed-gate support, which stays far from the terminal row. It also
does not settle an age-independent bound restricted to those corridor
supports. No unconditional packet or continuous-dimension limit follows.

The reference complement recurrence remains the full vector recurrence
with two rank-one feedback terms; no closed low-dimensional aggregate
system was found. The exact recurrence, constants, common endpoint, query
legality, dense correction, and scope distinction are recorded in PROOF.md.

Recommendation: move next to independent review of
codex_single_block_spatial_write_20261004, while preserving the narrower
corridor-packing question as open. If packing resumes, formulate its leverage
claim only for actual gate-change supports satisfying the no-wrap geometry.

No numerical experiment was run.
