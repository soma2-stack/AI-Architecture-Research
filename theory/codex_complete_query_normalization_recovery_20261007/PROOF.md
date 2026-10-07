# Complete legal-query normalization: source recovery record

Date: 2026-10-07. Author: Codex. Repository status: **PENDING REVIEW**.

## Recovery result

The exact derivation of the newer checkpoint
\[
\nu_{\rm actual}\le 7.213\frac{\sqrt m}{n}
\|B\Delta Y_{\rm full}\|_F+\eta,\qquad \eta<.001,
\]
was **not recovered** from the available Codex notebook, main-branch research files, or their reachable Git history. The value 7.213 and the eta claim occur in the later author report only as supplied upstream checkpoints. The preservation task prohibits rebuilding a missing derivation from memory, so this file does not assert that inequality as proved.

This note separates what the repository actually contains from what is missing. It is not a substitute proof.

## Recovered exact legal-query metric

In `theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md`, §9, lines 295–353, the repository defines the frozen fixed-feature reference pseudometric
\[
\nu(A)=\frac{\sigma\sqrt l}{n}\sup_{Q\ \rm legal}\|A^Tc_Q\|_2,
\]
and the exact one-step subfamily
\[
\nu_1(A)=\frac{\sigma\sqrt l\,a}{n\sqrt n}
\max_{g\in[g_{\rm lo},g_{\rm hi}]^r}\|A^TO_*^Tg\|_2.
\]
The report explicitly warns that the longer-query metric is not equivalent to an arbitrary unit-adjoint or operator norm. The same section gives the legal-query upper ledger
\[
\nu(\Delta H_N)\le\frac{\sigma\sqrt l}{n}\left[
102\|\Delta Z_N\|_2+
\frac{400}{\sqrt n}\sum_i\|\Delta V_{i,N}-\Delta Z_N\|_2+
\frac{100}{\sqrt n}\sum_{z=1}^N\|\Delta F_{z,N}-\Delta Z_N\|_2
\right].
\]
This recovers a decomposition into bath/common, cycle, and front differences. It is an upper ledger, not a claim that the terms' suprema are jointly attained or that channel dimensions add.

The same section recovers some component estimates: ordinary/front coordinate leakage is individually bounded by \(100/\sqrt n\) in its stated regime; a bath aggregate has its own bound \(|c_Q^T\mathbf1_r|\le102\) for legal queries with at least one future step; the complete Householder block has an exceptional terminal/bath-supported coordinate and cannot be bounded by the ordinary-coordinate estimate. Direct cycle contributions have a normalized upper below \(8H(\Delta K)/n\) after reset, while the two compensator copies contribute below \(8\|\Delta\kappa\|_2/n\). These are not yet the requested full \(B\Delta Y_{\rm full}\) normalization.

## Recovered construction and scope facts

`theory/codex_linear_dimension_frontier_20261006/PROOF.md` §3, lines 121–159, records the fixed source feature, exact recurrent sensitivity, probe bank, rank-two Householder form, and complete recurrence. §4, lines 161–194, gives the two-stage public schedule. §5, lines 196–232, gives inherited bath/front bounds and global chronology. §6, lines 234–259, gives exact trace matching after capture. §8, lines 297–341, gives the one-step capture identity and protected-row cancellation. §9, lines 343–373, gives the two-stage boundary/reset construction. §10, lines 375–409, gives an actual legal one-step query and a separate lower-bound argument. These files establish relevant construction premises, but they do not derive 7.213 or the eta<.001 complete-query upper bound.

Additional background is in `theory/codex_frontier_invention_20261006/PROOF.md` §§6–10, lines 257–554, including the group-averaged recurrence, bath/survivor comparison, full chronological front, and query normalization for that construction. `theory/codex_holding_cost_attack_20261003/PROOF.md` §§4–5, lines 139–265, contains exact inverse-lift geometry and an earlier legal-query analysis. `theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md` §§1–5 and §10, lines 9–202 and 355–397, contains fixed-input differentiation, the exact reference recurrence, common-mode/bath equations, and dense-model scope.

These are related but distinct estimates. Combining their constants into 7.213 without the original argument would be an unsupported reconstruction.

## Requested components: recovered versus missing

| Component requested | What is recovered | What is missing for the checkpoint |
|---|---|---|
| 7.213 coefficient | Exact old legal-query metric and a channel ledger, cited above. | The complete sequence of inequalities and constants that turns the final cleared \(B\Delta Y_{\rm full}\) into the coefficient 7.213. |
| \(\eta<.001\) | Older finite-error and dense-correction estimates exist in the construction proofs. | The exact terms in this checkpoint's eta, their widths/horizons, and the numerical inequality proving their sum is below .001. |
| Donor contribution | Donor/cycle terms and some post-reset bounds are explicit in the older query ledger. | The bound for all donor channels under the complete final-clear protocol, with the normalization used by \(B\Delta Y_{\rm full}\). |
| Bath contribution | The old bath aggregate estimate and the later public bath recurrence are explicit. | The exact contribution after the prescribed final public clear in this normalization and the constant charged to 7.213 or eta. |
| Front contribution | Ordinary front-coordinate leakage and full chronological front estimates are present in inherited proofs. | The exact final-clear projection and constants charged in the newer full-query upper. |
| Terminal contribution | The old report identifies terminal/bath support as an exception to coordinate dilution; the later geometry treats terminal as a bath row. | The exact cancellation, projection, or residual bound in the newer normalization. |
| Trace correction | Exact trace matching schedules and legal correction gates are described in the early-capture proof. | The full query-side estimate for all correction derivatives, not just trace equality or protected-row blindness. |
| Dense correction | Dense operator perturbation estimates are recorded in multiple construction proofs. | The precise dense term in the eta ledger for this checkpoint and its final numerical contribution. |
| Final public clear | A public clear appears in the inherited construction schedule. | The exact operator/filter action on every query channel and the derivation that makes the final bound valid after this clear. |
| Exact scope | Fixed source, legal future queries, frozen realized inputs, actual recurrent sensitivity, two-stage construction premises are documented. | A single source proof stating every hypothesis under which 7.213 and eta<.001 hold. |

## Unrecovered assertion

The implication
\[
\nu_{\rm actual}>.002\quad\Longrightarrow\quad
\|B\Delta Y_{\rm full}\|_F\ge c\,n/\sqrt m
\]
is therefore retained only as an **owner-supplied checkpoint**, not established by this recovery record. The coefficient and additive-error assertion need their original derivation before independent review can validate them.

No source file was edited in the search. No experiment was used. `CURRENT_THEORY.md` was not changed.
