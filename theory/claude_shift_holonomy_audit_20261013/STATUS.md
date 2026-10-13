# Status — claude_shift_holonomy_audit_20261013

**Type:** audit of Gemini's proposal and proof of a modified QSR result.
**Independent review:** completed; see PR #25 and `REVIEW_HANDOFF.md`.

| Item | Status |
|---|---|
| Original strict-budget problem (frozen dense tanh) | **OPEN**, unchanged |
| Gemini: claim to solve the original problem | **REFUTED as stated**: different architecture and metric; no reduction to the unchanged contract |
| QSR: exact cancellation and Jacobian identities | **VERIFIED**, exact and in stated scope |
| Lemmas 5.1–5.3 and Theorem 5.4 | **VERIFIED** for QSR, its stated history/input boxes, realizable `Q_ne` futures, code-existence condition, and positive bias weight |
| Corollary 5.5 | **VERIFIED asymptotically after correction**: `D=floor(n'/1001) >= n/1004`; the former `n/1002` floor claim was false at `n=1,000,999` |
| Corollary 5.6 | **VERIFIED in the augmented QSR model**, for the stated full recurrent-group RMS ratio, fixed-feature projection, and `Q_ne`; source preparation uses a public changing-support schedule and `m` denotes maximum simultaneously addressed coordinates |
| Normalization claims | Bias result: `w_b=c/sqrt(n)`, `c>=.0021`, over `Q_ne`; transplant: stated full-group RMS ratio and projected fixed-feature metric over `Q_ne`; no all-group or universal-weight claim |
| Tanh architectural equivalence | **UNPROVED numerical evidence**: the adjoint family is idealized and the samples do not prove uniform boundary separation |
| Lemma 8.1 | **VERIFIED local trace bound** in its reference/dense-perturbation scope; it does not prove a credit-weighted tax |
| Neutral-path tax | **CONJECTURE**, not established |
| Architecture novelty | Not certified by this record; QSR has known-operation and delay-line/nonlinear-port analogues, while equivalence of the robust-credit theorem remains unproved |

**Exact next action.** Preserve this scope and the OPEN original-problem status in any later
revision. Any stronger tanh-equivalence, global normalization, or neutral-path-tax claim
requires a separate proof.
