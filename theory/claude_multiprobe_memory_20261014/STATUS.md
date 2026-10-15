# Status — claude_multiprobe_memory_20261014

Final cross-PR audit of PR #27 a67be6d / PR #28 3746747:
[AUDIT.md](../codex_cross_pr_final_audit_20261015/AUDIT.md),
[research handoff](../codex_cross_pr_final_audit_20261015/HANDOFF.md).
The imported foundations now pass independent verification; PR #27's remaining
gated-injection identity was corrected at 6ef95b5. This branch corrects 1/1700,
the historical front delivery, finite attenuation, and auxiliary overstatements.
All target theorem coefficients and assumptions are preserved.

Independent repair of `b66b12d`, with [verification and reproduction](../codex_pr28_repair_verification_20261014/VERIFICATION.md).

| Item | Current status |
|---|---|
| Original problem: linear D at mT=o(n^(3/2)) | **OPEN**, unchanged |
| Parameter group | Explicit `d_F,E`: `{u f_s^T:u_0=0}`, dimension n-1; full unmasked group not covered |
| Exact spike cutoff / all legal future horizons | **PROVED in stated scope**; exact `-ln(HI)` cutoff, long-query norm cap, short-query non-spike bound 1.2 |
| Theorem 2 | **PROVED** in the inherited fixed orthonormal K-probe scope; its PR #27 premises now independently checked |
| Theorem 3 | **PROVED** for its public intervals, public weights and stated variation/readout bounds |
| Cor. 3.5 | **CONDITIONAL** on H1-H5; coefficients 8402 / 1.03e5; resource conclusion requires `3,600,008<=D<=n` |
| Lemmas 7.1–7.2 | **PROVED** within the explicitly selected group; exact bus identities and capture upper bound |
| Lemma 7.3 | **PROVED in stated scope** after explicit c_1=0, later source estimate, and corrected .0242 spike cap |
| Theorem 4 | **CONDITIONAL** on Hypothesis B and declared PR #27 background premises; verified repaired argument; resource range `2 N_3<=D<=n` |
| Theorem 4 asymptotic consequence | `Omega(n^(3/2)/log n)` for linear D; no logarithm-free asymptotic obstruction asserted |
| Hypothesis B | **OPEN**, untouched by this repair |
| Cor. 3.3 | One-step bound **CONDITIONAL** including c_max<=1; historical 553 F extension unverified and unused |
| Historical concrete-design calculations | Scoped analysis, not a universal bus impossibility theorem |

The prior failed constants and counterexamples are retained in `REVIEW_RESPONSE.md`
and the independent verification record. `AGENTS.md`, notebooks and original theorem
records outside this PR's own index row remain untouched.

**Exact next action.** Investigate the full accumulated-bus kernel inequality in
the research handoff, then the old-profile approximation target for removing the log.
Hypothesis B requires separate future research. No proof attempt for B was made here.
