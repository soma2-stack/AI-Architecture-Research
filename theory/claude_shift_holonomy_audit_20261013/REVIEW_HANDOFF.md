# Review handoff: shift-holonomy audit

**What to review.**

* The audit verdicts on Gemini's claims: [REPORT.md](REPORT.md), sections I-IV.
* The author-derived theorems for the repaired architecture: [PROOF.md](PROOF.md),
  Theorems 1.3, 1.4, 4.4 and 5.4, Lemmas 1.2, 5.1, 5.2, 5.3 and 8.1, and Corollaries 4.5,
  5.5 and 5.6.

**Do not read** `docs/notebooks/Codex_Research.md` or `docs/notebooks/Cursor_Research.md`
for this review; everything needed is in this folder. The original contract is summarized
in `../CURRENT_THEORY.md`.

**Scope warning.** These theorems concern a different architecture (QSR) under explicitly
defined metrics. They do not bear on the frozen dense tanh problem, which stays OPEN. A
review that "verifies" them must not upgrade the original problem's status.

## Highest-value attack points

1. **Lemma 5.1 index bookkeeping.**
   * Check the block placement `beta(T, qR+r+1) = R+1-r` (and `1` for `r = R`).
   * Check the reduction `(S^T)^(2R-s) = (S^T)^(R-s)`.
   * Check the summation `sum_(t <= qR) (S^T)^(qR-t) = q (J_R (x) I_m)`.

   `checks.py: closed_form_delta` implements the same formula, and section F compares it
   with the actual recurrence.
2. **Lemma 5.2.** Check that the `k`-th future input gates block `R+1-k` of `lambda_T`.
   This pairing (the `r`-th future input with the `r`-th written block) is what the
   sign-aligned query exploits.
3. **Theorem 5.4, sign-query inequality.** Verify
   `P - (1-rho_f) N >= (rho_f/2)(P + N)` when `P >= N`, and the Cauchy-Schwarz step
   `sqrt(sum_i ||Dz_i||_1^2) >= ||Dz||_1/sqrt(m)`.
4. **Window bound.** Verify `||sum_s (S^T)^(R-s) delta_s|| <= R ||Dz||_2/sqrt(n)` from
   `0 <= mu <= n^(-1/2)`.
5. **Lemma 5.3 constants.** Check each of the following:
   * Paley-Zygmund `3/16` from `E X^4 <= 3`;
   * Hoeffding `exp(-N/128)` for a deficit of `N/16`;
   * net size `241^D` at `delta = 1/120`;
   * operator norm `<= 5.06 sqrt(N)` (`1/4`-nets, `2e^(-N)` failure);
   * transfer count `16 ||G||^2 delta^2 < N/16`;
   * final probability `< 1` for `N >= 520`.

   Alternative: substitute Codex's reviewed Lemma 1 from
   `../codex_frontier_invention_20261006/PROOF.md`.
6. **Theorem 4.4 and the definition of `Q_ne` and `A_ne`.** Is "fixed uniform head plus
   future gates in `[0,1]`" a fair analog of the original legal family? Theorem 4.4 needs
   nonexpansive dynamics. Section 6 shows that expansive histories break it.
7. **Corollary 5.6 (transplant).**
   * Check `w_W/beta = 1/n_tot` for `W_full = [[S,K],[0,I]]`.
   * Check the projection formula `n_tot^(-1) sum_t (f_s^T s_(t-1)) lambda_t^mem` (checks
     K: autograd `2e-17`).
   * Check the preparation-window bound.
8. **Lemma 8.1.** Is it correctly scoped to `R_0 = diag(aO, delta I)`? Its interpretation
   (section 8.2) is labeled as interpretation. The neutral-path tax (section 8.3) is a
   conjecture.
9. **Novelty (section 7).** Is the tanh ablation (numerical) enough to classify QSR as an
   existing mechanism, or does a written proof need to be required?

## Reproduction

    cd theory/claude_shift_holonomy_audit_20261013
    python -I checks.py

Requirements: numpy, torch (CPU). The run takes about 25 s. Every internal assertion must
pass, and `checks_result.json` is rewritten. Compare against the committed copy; values
are deterministic for the fixed seed up to BLAS-level floating differences of order
`1e-15`.

## Suggested verdict vocabulary

For each of Theorems 1.3, 1.4, 4.4, 5.4, Corollaries 5.5 and 5.6, and Lemmas 5.1, 5.2,
5.3 and 8.1, use one of:

* VERIFIED IN STATED SCOPE
* PROOF GAP (precise location)
* COUNTEREXAMPLE
* MIS-SCOPED
