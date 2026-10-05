# Hostile review: arbitrary-horizon log-gap note (commit 6a54d5b)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/arbitrary_horizon_log_gap_20261001/ (PROOF.md, REPORT.md, PROVENANCE.md).
- **Supporting code:** none exists, and nothing was executed.
- **My work:** I re-derived the note from scratch and ran a numerical check of the actual family
  (check_log_gap.py, log_gap_check.json, run.log).

## Verdicts

| Claim | Verdict |
| --- | --- |
| **1. Suffix-only lookback H >= (n/2c) log n - O_(c,eps)(n)** | **VERIFIED.** The window upper bound has the same leading term, so suffix-only lookback on this family is Theta((n/2c) log n), tight up to O_(c,eps)(n). |
| **2. Same family, arbitrary horizon, O(n^2) continuous encoder** | **VERIFIED, for this near-diagonal family only.** P = 2n^2 + n counted eligibility traces (+n for h when not supplied). Continuous, online, aggregating, and uniform over all horizons and all permitted late queries. |
| **"Long lookback != large required persistent memory"** | **DEMONSTRATED, in the precise sense** that a suffix-only lookback lower bound cannot be converted into a persistent-memory lower bound. It is conceptually modest, because the family is essentially an independent-unit (diagonal) recurrence, where O(n^2) eligibility traces are classical. |

## Claim 1 audit

1. **Family.**
   - B = R0 + (eta/n) 11^T with positive diagonal R0, so B is positive definite and all off-diagonal entries are
     eta/n > 0.
   - Sherman–Morrison inverse: off-diagonal entries are negative and nonzero, diagonal entries positive.
   - R = aB/\|\|B\|\|op has \|\|R\|\|op = a exactly. \|\|R - R0\|\|op <= 2 eta, since \|a - \|\|B\|\|\| <= eta and
     a/\|\|B\|\| <= 1.
   - beta = \|\|R\|\|_F, so w_R/beta = 1/n.
2. **Two histories.** The source state is s(2/5)1 for J = ceil(n/c) steps; then h = 0 for H+1 steps.
   - The reset input x_(J+1) = -R h_J - b differs between signs, but it is NOT in the retained set
     {h_(T-H..T-1), x_(T-H+1..T)}.
   - All retained items are zeros or -b, and h_T = 0 is common.
   - Measured: the suffixes are bit-identical, and max input 0.474 < 1/2.
3. **Separation.**
   - Memory gates are 1 and the memory block is aI. The R memory-row/source-column block sums the J coherent injections
     with ages T - t, giving a^(H+1)(1 - a^J)/gamma times (kappa sigma/n) sqrt(k/n) sqrt(l).
   - 1 - a^J >= 1 - e^-1 and sqrt(kl)/n >= 1/3, so the bound is >= sqrt(n)/(20c) a^(H+1).
   - Dense transfer: product perturbation p a^(p-1) e_R, summed over all ages to 1/gamma^2, gives
     E_n = 4 sigma/(10^8 c^2 sqrt(n)).
   - Measured full half-separation >= R-block formula >= bound at every tested H (full is about 1.8x the block).
4. **Theorem.**
   - Any function of (h_T, the suffix) is identical on both histories, so sep <= 2 eps, so
     a^(H+1) <= 20c(eps + E_n)/sqrt(n).
   - Since 1/(-log(1 - c/n)) >= n/c - 1, H >= (n/2c) log n + (n/c) log(1/(20c(eps+E_n))) - O(log n). This is stronger
     than the stated "- O(n)" when 20c eps < 1.
   - Measured smallest working H (c = 1): 461, 971, 2034 at n = 64, 128, 256. Each lies between the theorem's lower
     bound (380, 807, 1707) and the window upper bound (600, 1248, 2590).
   - The per-doubling increments match (n/2c) log 2 growth. At practical n the O(n/c) term dominates the log term.
5. **Scope.** This is a lookback-LENGTH bound for summaries that carry no pre-suffix accumulator (dimension
   unrestricted). It correctly disclaims any Omega(n^2 log n) memory statement.

## Claim 2 audit

1. **Surrogate recursion.** Zbar_t = G_t R0 Zbar_(t-1) + B_t uses the ACTUAL gates and injections.
   - \|\|Zbar\|\| <= C/gamma.
   - The error obeys Delta_t = A_t Delta_(t-1) + G_t(R - R0) Zbar_(t-1), so
     \|\|Z - Zbar\|\| <= e C/gamma^2 for every horizon.
   - Query error <= kappa_Q e C/gamma^2. The future direct terms are exact from the actual h_T.
2. **Storage.** G_t R0 is diagonal and row i of B_t is supported on (R_(i,:), W_(i,:), b_i), so each row of Zbar has
   2n + 1 entries: P = 2n^2 + n traces. This is an exact realization of Zbar, with no window buffer, replay or
   uncounted factor.
   - The online update needs the actual h_(t-1) and gates, i.e. the network's own n-dimensional state: +n if h is
     not counted as supplied.
   - The map from the input stream to the traces is continuous.
3. **Error.** Codex's analytic bound is (2/sqrt(k))(4/(10^8 n^2))(6/5)(n^2/c^2) = 48/(5 x 10^8 c^2 sqrt(k)), far
   below eps.

   | Test (n = 64–256, 2,000-step random, alternating and adversarial-tail histories; two query inputs) | Result |
   | --- | --- |
   | Measured worst query error at the proof's coupling | <= 3e-12 |
   | Past-dependent part | about 0.5–1.0 |

4. **All permitted queries.** The bound only uses \|\|c_q\|\| <= a/beta, which covers multi-step and off-box
   continuations too.
5. **Near-diagonal only.** The bound needs \|\|R - R0\|\|op <= eps gamma^2/(kappa_Q C) = O_(c,eps)(n^(-3/2)). Measured
   error grows roughly linearly with the coupling and with n:

   | Coupling eta | n = 64 | n = 128 | n = 256 | Below eps? |
   | --- | ---: | ---: | ---: | --- |
   | 1e-4 | 1.1e-4 | 3.1e-4 | 8.3e-4 | yes, but approaching eps at n = 256 |
   | 1e-3 | 1.0e-3 | 3.0e-3 | 7.4e-3 | no |

   So this is an exact-diagonal result with a vanishing safety neighbourhood, not a dense-recurrence aggregation
   theorem.

## Requested checks, briefly

| Check | Finding |
| --- | --- |
| Hidden extra storage | None. |
| Uniform error over arbitrary horizons | Yes. |
| Normalization | Unchanged group RMS and beta. |
| Aggregated vs replayed | Aggregated: eligibility traces. |
| Continuity | Yes. |
| Dense assumptions | Formally dense (all R, R^-1 entries nonzero), substantively diagonal. |
| Dependence on c | The lookback bound's O-term is (n/c) log(1/(20c eps)). The encoder's error scales as 1/c^2. |

## Does it show "long lookback != large required persistent memory"?

Yes, in the following sense.
- The same family needs suffix lookback Theta((n/2c) log n), costing (n^2/c) log n for the literal 2Hn window.
- Yet it admits an arbitrary-horizon O(n^2) aggregated encoder.
- So a lookback lower bound alone can never prove an Omega(n^2 log n) memory lower bound.

Two qualifications:
1. No memory LOWER bound is given for this family. The O(n^2) is an upper bound only; the family's true requirement
   could be smaller.
2. The aggregation works because the reference propagation is diagonal. Independent-unit recurrences have classical
   exact O(n^2) eligibility traces (RTRL/e-prop style), so the separation is real but expected.

## Strongest remaining gap

The worst-case arbitrary-horizon log gap, Omega_c(n^2) <= d_rob <= O_c(n^2 log n), is untouched, and the note's tool
cannot reach the hard instances.

In the accepted rotating quadratic family (R0 = diag(aO, delta I)), general histories have history-dependent memory
gates. Then G_t aO is not diagonal, the surrogate's memory rows spread over all memory-row parameters (k x k(2n+1) =
Theta(n^3) entries), and diagonal eligibility traces do not apply.

Closing the gap needs either:
- a compression theorem for noncommuting gated products G_t R ... G_s at fixed eps under the normalized late-query
  norm; or
- a jointly robust Omega(n^2 log n) section.

Neither is attempted here, as instructed.

Evidence: check_log_gap.py, log_gap_check.json and run.log in this directory. A few CPU-minutes at <= 12 threads; no
GPU. Codex's files were not modified.
