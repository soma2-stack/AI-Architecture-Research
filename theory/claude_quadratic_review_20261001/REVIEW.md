# Hostile review: quadratic robust section at contraction gap c/n (commit 148a387)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/gamma_c_over_n_quadratic_20261001/ (PROOF.md, REPORT.md, PROVENANCE.md).
- **Supporting code:** none exists, and no recipe was executed.
- **My work:** I re-derived the proof from scratch and ran numerical checks of the actual construction:
  - check_quadratic.py and quadratic_check.json;
  - check_formula6.py and formula6_check.json.

## Verdicts

| Question | Verdict |
| --- | --- |
| **1. Omega(n^2) lower bound** | **CORRECT.** No mathematical gap. The formalization notes are below. |
| **2. Width-independent margin** | **YES.** Half-margin >= 1323/640000 - 1e-6 > 0.002 for every n >= n0(c) and every c > 0, with no n- or c-dependence in the margin. Numerically 0.078–0.110 (38–55x). |
| **3. Truly dense** | **FORMALLY YES, SUBSTANTIVELY NO.** All entries of R and R^-1 are nonzero, every parameter is independently differentiated, and \|\|R\|\|op = 1 - c/n exactly. But the family is a perturbation of a block-diagonal "rotating memory plus near-zero source buffer" matrix, of operator norm <= 4e-8/n^2. Many entries are astronomically small (rank-one C built from integer powers). |
| **4. Rules out universal subquadratic scaling at gamma = Theta(1/n)** | **YES, as a worst-case statement** with these quantifiers: the class contains \|\|R\|\|op <= 1 - c/n, \|\|W\|\|op = 1, input bound 1/2 and RMS(b) = 1/20; the horizon budget is >= J+1 ~ n/(4c) (all longer horizons by padding, note F1); the group-RMS + beta late-query contract holds; and eps < 0.002. It is existential, not a statement about typical dense models. |
| **5. Strongest remaining weakness** | The quadratic robustness lives on a structured, near-block-orthogonal family, and depends on the contract's w_R/beta = 1/n cancellation. Numerically, at FIXED genuinely dense coupling, the margin shrinks with n. See the last section. |

## Line-by-line audit

1. **Parameters.**
   - k = floor(n/2), l = n-k, L = max(1, ceil c), d = min(k, floor(n/(4cL))), J = Ld.
   - Jc/n <= 1/4 in both the capped and uncapped cases, so a^J >= 3/4 (Bernoulli, integer J).
   - d >= n/(8cL) uncapped needs n >= 8cL; N = dl >= 1000 needs n >= 126.5 sqrt(cL); a >= 1/2 needs n >= 2c; and
     T = J+1 <= n. All of these are covered by n0(c).
   - L sqrt(d/n) >= sqrt(L/(8c)) >= sqrt(1/8) > 7/20, because L >= c.
2. **Orbit.**
   - U is the Householder reflection e1 <-> e, and O = U(P_d (+) I)U^T, so (O^T)^j q_m = sqrt(k/n) U e_{pi(j)}.
   - These d vectors are orthogonal with norm^2 k/n, and (O^T)^d q_m = q_m.
   - Measured: Gram off-diagonals <= 9e-15, norm^2 = 0.5000, return error <= 4e-14.
3. **Exact fixed h.** Equation (4) prescribes the entire hidden trajectory: memory states 0, source rows H_s, and
   h_T = 0, for any R including the dense one.
   - Source inputs: atanh(2/5) = 0.4236, plus delta(2/5) and 1/20, gives < 0.477.
   - Measured: memory states and h_T exactly 0, max input 0.474 (0.489 even with 0.05 dense coupling).
4. **Held-input sensitivity and query.** Memory gates are exactly 1 and R0 is block-diagonal, so the memory adjoint
   evolves only through a O^T.
   - The future query (v = 9/20, preactivation 1/2, kappa = sech^2(1/2)) is permitted.
   - The direct future R-injection is zero at h_T = 0.
   - Formula (6), including the L-repeat grouping B_L, matches torch autograd of the actual recurrence (inputs held
     fixed) to <= 2.5e-13 relative, at (n, c) = (256, 1), (256, 2.5) and (512, 0.5).
5. **Normalization.** w_R = \|\|R\|\|_F/n and beta = \|\|R\|\|_F (> 1 since \|\|R0\|\|_F >= a sqrt(k)), so w_R/beta = 1/n
   EXACTLY, for both models. Measured: n w_R/beta = 1.000000.
6. **Margin.**
   - Orthogonal v_s give \|\|sum_s v_s H_s^T\|\|_F^2 = sum_s \|\|v_s\|\|^2 \|\|H_s\|\|^2, which yields (7).
   - a^d B_L >= L a^(Ld) >= 3L/4, and \|\|H\|\|_F >= sqrt(dl)/40 from the accepted spread lemma (measured
     min \|\|H\|\|_F/sqrt(dl) ~ 0.25, against 1/40).
   - sqrt(k/n) >= 3/5 and sqrt(l/n) >= 7/10.
   - Product: (9/16)(1/40)(3/5)(7/20)(7/10) = 0.0020671875 (capped case: 0.00354).
   - It is joint over every boundary antipode. Other gradient blocks only add in Euclidean norm.
7. **Section dimension.** r = floor(dl/1000) >= dl/2000, which is >= n^2/10000 (capped) or >= n^2/(32000 cL), so
   Omega_c(n^2). The constant scales like 1/(c ceil c); the margin does not.
8. **Density transfer.**
   - Rank-one C with positive power vectors; the finite root counts for B and for B^-1 (Sherman–Morrison, denominator
     bounded away from 0 by eta/delta < 1) are correct, with 2n^2 + 1 candidates against <= 2n^2 bad values.
   - Rescaling to \|\|R\|\|op = a gives e_R <= 2a eta/(a - eta) <= 4 eta.
   - The trajectory and gates are identical across models by (4). Telescoping over norm-<=1 factors gives
     \|\|g_R(R) - g_R(R0)\|\|_F <= (2/5) n^(3/2) e_R < 1e-6. Correct.
9. **Borsuk–Ulam.** The lift is continuous in u, h_T = 0 is shared, and one permitted query separates. So k < r
   forces a shared memory and distance <= 2eps < 2m. Correct.

### Formalization notes (do not affect validity)

- **F1 (horizon).** The section needs histories of length T = J+1 ~ n/(4c), and no quadratic lower bound is possible
  at horizons T = o(n), since 2Tn exact storage suffices. To claim "arbitrary horizon", add the padding remark: prefix
  x_t = -b keeps h = 0, and the prefix sensitivity propagates through gates that are even in u (memory gates 1,
  source gates 1 - H_s^2), so it cancels between antipodes.
- **F2.** "Explicit" means a computable specification (exhaustive sign-matrix search, finite integer t search,
  finite eta list); for real c it is existence only. This is as the proof states.
- **F3.** Density is not needed for the class lower bound at all. The class is defined by norm bounds, and R0 itself is
  a member under full independent differentiation. Section 7 only adds an all-entries-nonzero property.

## Comparison with the upper bounds

- **Arbitrary horizon.** With kappa_Q <= 1, H = ceil(log(kappa_Q C/(eps gamma))/(-log(1-gamma))) = O_c(n log n), so
  d_rob <= 2nH = O_c(n^2 log n). Together with the lower bound (horizons >= n/(4c)+1, via F1), this gives
  Omega_c(n^2) <= d_rob <= O_c(n^2 log n). Correct; the log gap is open.
- **Constructed horizon T = J+1 <= n/(4c)+1.** The universal 2Tn exact store (states and inputs, no discarded replay)
  gives O_c(n^2), so Theta_c(n^2) holds at that horizon. Correct.
- **Consistency.** The same-gap margin ceiling is nonrestrictive for r ~ n^2/(32000 cL): exponent about
  n/(64000 cL), so (1 - c/n)^that ~ 1. There is no conflict.

## Strongest remaining weakness

1. **Knife-edge structure.** The proof's dense family is within 4e-8/n^2 (operator norm) of block-diagonal
   "memory rotation (+) delta I". Numerically, with genuinely dense random coupling of FIXED operator norm e, the margin
   is unaffected at e = 1e-3 and still large at e = 1e-2 (0.049–0.085). But at e = 0.05 it decays with width:

   | n | Margin at e = 0.05 |
   | ---: | ---: |
   | 256 | 0.045 |
   | 512 | 0.034 |
   | 1024 | 0.024 |

   That is consistent with orbit drift ~ J e = Theta(n e). The theorem is therefore an existence statement for
   specially structured near-critical recurrences. It is not evidence that generic dense models at gap c/n carry
   quadratic robust credit.
2. **Contract dependence.** The entire margin sits in the R memory-row/source-column block and relies on
   w_R/beta = 1/n. Under per-entry or beta-free units the conclusion is untested; the proof notes this itself.
3. **Open log factor.** At arbitrary horizons the log n gap is open, and the lower bound needs horizon Theta_c(n).

Evidence: check_quadratic.py and quadratic_check.json (n = 256–1024, c in {0.5, 1, 2.5}, couplings 0 to 0.05);
check_formula6.py and formula6_check.json. A few CPU-minutes at <= 12 threads; no GPU. Codex's files were not modified.
