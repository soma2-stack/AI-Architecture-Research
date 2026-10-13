# Status — claude_shift_holonomy_audit_20261013

**Type:** independent audit of Gemini's proposal, plus new author-derived theorems for a
modified architecture. **Repository status:** PENDING INDEPENDENT REVIEW.

| Item | Status |
|---|---|
| Original strict-budget problem (frozen dense tanh) | **OPEN**, unchanged |
| Gemini: "solves the original problem" | **REFUTED as stated** (different model and metric; no reduction; Lemma 8.1) |
| Gemini: forward cancellation, Jacobian, singular values | **VERIFIED** (exact) |
| Gemini: input admissibility | **DEFECT** (`5/8 > 1/2`), repairable |
| Gemini: learning-credit theorem | Not a parameter-gradient statement. Trivial under its own unnormalized metric. **REFUTED** for its schedule under normalized metrics |
| Repaired QSR: `D = Theta(n)`, `mT = Theta(n)`, `T = Theta(sqrt n)`, tight in the nonexpansive class | **PROVED (author)**, pending review; new architecture and explicit metrics only |
| Novelty | Existing mechanism (delay line plus nonlinear port); the property is preserved by an ordinary tanh RNN (numerical ablation) |
| Neutral-path tax for the original model | **CONJECTURE** (stated, not claimed) |

**Next action.** Run an independent hostile review of PROOF.md Lemmas 5.1-5.3, Theorem 5.4
and Corollary 5.6 (see REVIEW_HANDOFF.md). For the original problem, the actionable
question is the neutral-path tax conjecture (PROOF.md section 8.3).
