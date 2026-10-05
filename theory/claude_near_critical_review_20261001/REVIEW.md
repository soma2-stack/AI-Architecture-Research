# Hostile review: near-critical robust credit phase diagram (commit 18be6c6)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/near_critical_credit_phase_diagram_20261001/ (PROOF.md, REPORT.md, PROVENANCE.md).
- **Supporting code:** none exists; PROVENANCE confirms no test or matrix selection was run.
- **My work:** I re-derived everything from scratch and ran one numerical check of the actual construction
  (check_construction.py, construction_check.json).

## Verdicts

| Question | Verdict |
| --- | --- |
| **1. Uniform Omega(n) lower bound** (section of dimension floor(n/2000), half-margin >= 0.002075 for all n >= 2000) | **VERIFIED.** No mathematical gap. Four formalization notes follow. |
| **2. Margin ceiling** m <= (kappa_Q C/gamma)(1-gamma)^(ceil(r/2n)-1), and its three-regime consequences | **VERIFIED.** |
| **3. Theta(n) for the constant-gap class** | **ESTABLISHED as a worst-case (existential) statement** under explicit quantifiers: fixed eps < 0.002075, gap gamma <= 1/2, class constants admitting \|\|W\|\|op = 1, B = 1/2 and RMS(b) = 1/20, the accepted delayed late-query contract, and any horizon T >= 2. Not universal per model, and not proved for strongly contractive classes (a < 1/2). |

## Lower bound, line by line

1. **Family.**
   - R = delta I + (a - delta) qq^T has eigenvalue a on q and delta on its complement. So \|\|R\|\|op = a and the gap is
     gamma = 1 - a exactly.
   - All entries of R are positive. It is invertible, R^-1 = delta^-1 I + (a^-1 - delta^-1) qq^T, and every inverse
     entry is nonzero.
   - W = I is invertible but diagonal: "dense" refers to the recurrent matrix only.
   - beta^2 = max(1, a^2 + (n-1) delta^2) < 1.0001.
   - w_W = \|\|I\|\|_F/n = 1/sqrt(n).
2. **Exact fixed h.** The pairing (v, -v, 0) gives q^T z = q^T tanh z = 0, so R h1 = delta h1. Then x1 = z - b,
   x2 = -delta h1 - b gives h1 = tanh z and h2 = tanh(0) = 0 for every u.
   - Inputs: \|x1\| < 9/20 and \|x2\| < 1/20 + delta.
   - Measured: \|h2\| <= 1e-16, max input 0.425.
3. **Held-input sensitivity.** h0 = 0 and G2 = I give S2[dW] = R G1 dW x1 + dW x2, so the raw W-gradient is
   G1 R^T c x1^T + c x2^T. Its normalized antipodal difference is formula (G).
   - G1 is even in u and cancels.
   - The b-block difference is exactly 0, and the R-block (2 dR h1) only adds.
   - The direct future injection is common at h2 = 0.
   - The holding of inputs fixed during parameter differentiation is correctly enforced.
4. **Query.** v_f = (9/20)1 gives future preactivation 1/2, inside the permitted [1/4, 3/4] box, so the query is
   realizable. kappa = sech^2(1/2) = 0.786 > 3/4, and c = kappa a q/beta.
5. **Margin arithmetic.** \|\|a G1 q z^T - delta q tanh(z)^T\|\|_F >= a(21/25)\|\|z\|\| - delta\|\|z\|\|, and
   ||G1 q|| >= 21/25 since \|z_i\| < 2/5. Then m >= (3/4)(1/2)(4/5)(83/200)(1/60) = 83/40000.
   - Every factor is n-independent; w_W \|\|z\|\| >= 1/60 is the sqrt(n) cancellation.
   - No constant grows with n.
6. **Lemma (L).**
   - The Paley–Zygmund step: E X^4 <= 3 gives p >= 3/16.
   - The Chernoff step uses lambda = log 2, with exponent -0.153 p0 N <= -p0 N/8.
   - The net size 321^r and the union exponent -279N/16000 are correct.
   - The sub-Gaussian bilinear bound and 1/4-nets give \|\|M\|\| <= 2 max_net <= 8 sqrt(N) with failure
     2e^(-7N/2).
   - The Lipschitz step: 3/25 - 9/160 = 51/800 > 1/16.
   - Total failure < 1 for N >= 1000.
   - Measured on random M: \|\|M\|\|/sqrt(N) ~ 1.0 (vs 9) and min spread 0.62–0.76 (vs 1/16).
7. **Deterministic specification.** Fixing a maximal 1/160-separated net first, then enumerating sign matrices
   and certifying the two strict conditions by outward arithmetic, terminates for every n >= 2000. The positive
   probability is computed for that fixed net (size <= 321^r). Covering of the net is decidable (real-algebraic),
   but astronomically expensive. Existence alone already suffices for the existential lower bound.
8. **Borsuk–Ulam.** The section is continuous on the sphere and h2 = 0 is supplied. If k < r, an antipodal pair
   shares memory, giving distance <= 2eps < 2m. Correct; for r = 1 it reduces to k >= 1.
9. **Uniformity in gap.** Nothing uses a beyond a in [1/2, 1). Measured margins at a = 1/2, 1 - 1/(2n) and
   1 - 1/(2n^2) are 22–105x the bound at n = 2000–6000.

### Formalization notes (do not affect validity)

- **N1 (horizon).** The theorem is stated at horizon T = 2. It extends to every T >= 2 by prefixing x_t = -b, which
  keeps h = 0. The prefix sensitivity reaches S_T through R G1 R, which is identical for +/-u because G1 is even, so
  it cancels. This remark is needed before comparing with the horizon-uniform upper bounds.
- **N2 ("explicit").** The family is computably specified (exhaustive certified search), not closed-form, as the
  proof itself says.
- **N3 (constants).** The dimension constant 1/2000 and margin 0.002075 are very conservative (true margins are about
  25–100x larger). The theorem only starts at n >= 2000; below that r = 0.
- **N4 (scope in a).** The margin scales like a^2, so a >= 1/2 is used. For strongly contractive classes the proof
  gives nothing. Small-R families need no sensitivity memory at all for delayed heads (old THEORY section 6).

## Margin ceiling

- **Error bound.** e_H = kappa_Q C a^H/gamma, with \|\|c\|\| <= \|\|R\|\|op/beta = kappa_Q and the tail
  sum C a^H/(1-a).
- **Encoder.** The 2Hn store (h_(T-H..T-1), x_(T-H+1..T), h_T supplied) is the one from my previous review.
- **Borsuk–Ulam.** H = ceil(r/2n) - 1 gives 2Hn < r, so m <= e_H. Correct.
- **Arithmetic.** For r = nP the exponent is n^2 + ceil(n/2) - 1. Correct.

| Gap regime | Consequence |
| --- | --- |
| gamma = Theta(1) | quadratic O(e^(-cn)), cubic O(e^(-cn^2)) |
| gamma = Theta(1/n) | cubic O(n e^(-cn)); quadratic ceiling O(n), nonrestrictive |
| gamma = Theta(1/n^2) | cubic ceiling O(n^2), nonrestrictive |

These are correct. The necessary condition "gamma n^2 must not dominate log(kappa_Q C/(eps gamma))" follows from
(1-gamma)^k <= e^(-gamma k), and the authors correctly decline to call 1/n^2 a sharp threshold. The table's upper
column is also correct: 2nH is O(n) at gamma = Theta(1), O(n^2 log n) at Theta(1/n), and capped by nP at Theta(1/n^2).

## Is Theta(n) established for the constant-gap class?

Yes, in the worst-case sense. Fix eps in (0, 83/40000) and a class with \|\|R\|\|op <= a_max (a_max in [1/2, 1)),
\|\|W\|\|op <= w (w >= 1), \|x_j\| <= B (B >= 1/2) and RMS(b) <= b_* (b_* >= 1/20).

| Direction | Bound |
| --- | --- |
| Upper (every model in the class) | k_eps <= 2nH = O(n log(1/eps)/gamma) |
| Lower (the specified member) | k_eps >= floor(n/2000) at every horizon T >= 2 (N1) |

So the worst case over the class is Theta(n), with constant ratio up to about 4000 H.

What it does NOT establish:
- that every model in the class needs Omega(n): it does not, for example high-stable-rank R or small R;
- matching eps-dependence: the log(1/eps) factor is open;
- anything for a_max < 1/2.

## Strongest remaining weakness

The lower family has one slow mode and horizon 2. Its robust dimension comes entirely from the last two inputs and does
not grow as gamma shrinks. So the near-critical regimes (gamma = Theta(1/n), Theta(1/n^2)) remain wide open between
Omega(n) and O(n^2 log n) or O(n^3).

Its margin also depends on beta staying bounded, which means low Frobenius norm R. As the authors note, high-stable-rank
dense R dilutes the normalized delayed head like 1/sqrt(n). That is the main structural obstacle any superlinear
construction under this query contract must overcome.

Evidence: check_construction.py and construction_check.json in this directory (n = 2000, 2001, 4000, 6000; three gap
regimes; a few CPU-minutes; no GPU). Codex's files were not modified.
