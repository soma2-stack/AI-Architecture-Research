# Internal proof audit

2026-10-02. This records internal verification, not independent review.

## Analytic checks

1. Same n-dependent dense model, c1/gamma1/n/epsilon.001, sourceH, metric,
   legal late queries and whole intermediate gate cube. No source-column
   independence is assumed; the real parameter projection K uses H.
2. Householder dressing makes p_f exactly eigen and physical coordinate0
   exactly zero. Formal complex notation is discharged by real projections.
3. Public Q_t is finite, not replaced without error by its infinite resolvent.
   Its early-window term is included explicitly in K_fg.
4. The spreading lemma is proved by direct Gaussian integration, exponential
   Markov and two finite nets. q=d/1,000,000 has enough slack for the stated
   union bound. No unspecified Kashin/external concentration constant remains.
5. The projected tanh is odd, continuous, bounded, has the exact zero Fourier
   moments and is injective on each parameter block. The finite gate-word
   observations are injective by the degree-F trigonometric zero count.
6. Good-coordinate count is d/1024. Tanh1>3/4 is proved from e^2>7 by a
   positive-series rational lower. c_sat=3/131072 follows from the norm2<=2
   bound, not from empirical spreading.
7. At least one y block has norm>=F^(-1/2). The L_sat scaling and division
   by4F are included. The retained L1 loss is proportional to F^(-2).
8. Re(K)'s principal part is a positive weighted cosine Gram. The perturbation
   is charged in operator norm using FNb^N. Its singular lower is only claimed
   on REAL coefficients, exactly what the real profiles provide.
9. The row-norm algebra is converted to ONE column L1 with a paid factorF.
   It is not itself claimed to be query-visible; the subsequent legal-query
   construction establishes that visibility.
10. Fourier zero moments hold after saturation/projection for all selected
    frequencies and constant. Missing node0 is charged, not treated as an
    allowed control. Every term of UDU-D_hat is displayed and bounded.
11. Accumulated twist norm includes the full finite-Q factor<=2|resolvent|,
    and both physical O factors are kept. Final Householder dressing of the
    ideal column uses its exact zero sum. Total L1 loss<=32delta n.
12. The one-step query is realized at preactivations1/4 or3/4. Its head and
    beta/group-RMS normalization are unchanged. Future query inputs are NOT
    constrained by the past raw-input cube. A parameter projection is not
    an extra allowed adjoint or loss.
13. Complex column L1 loses a factor2 to real/imaginary projections. The
    s_gate>4/25 bound and query coefficient>1/(50n) are checked rationally.
14. All even degrees cancel for antipodes. All odd orders3+ obey a combined
    absolute query bound delta^3 sqrt(n), covering cross-frequency products
    and arbitrary chronological order. No relative q_n^2 claim is used.
15. The same-endpoint reset+I cancels. Its a^2 and O^2 are already in the
    query inequality. Preparation is public and gives zero selected R credit.
16. Actual-R query perturbation is charged separately at<2e-9. The original
    dense/polynomial ledger is included conservatively at epsilon/4. Neither
    is promoted into a changed epsilon or norm.
17. F=floor(n^(1/18)) and delta=10^(-10)/F^3 give the exact final exponent
    and margin arithmetic. n0=10^504 satisfies every auxiliary size bound.
    All floors are retained in D and its n^(19/18)/20,000,000 lower.
18. The history radius is explicitly finite but width-dependent. There is
    no width-uniform radius or practical conditioning/finite-bit claim.
19. Borsuk-Ulam is applied to ONE joint sphere of boundary antipodes. The
    proof does not claim all tiny interior antipodes are epsilon-separated.
    Same finalh0 rules out a free forward-state history channel.
20. The full-model n^2--n^2 log n gap is not inferred solved. The new theorem
    must receive independent review before replacing the accepted checkpoint.

## Executable cross-checks

checks.py is independently written CPU NumPy, with one BLAS worker and no
GPU/ML runtime. It does not import Claude code or read Claude numerical JSON.
The two widths are algebra diagnostics, not asymptotic proof evaluations.
Both CHECK_RESULTS.json and CHECK_RESULTS_REPLAY_2.json report PASS.

Exact rational assertions verify c_sat/query constant, hyperbolic gate
bounds, odd-tail factor and final n0 margin. Numerical assertions verify
the finite kernel against direct recurrence, dressed eigenvector, projected
zero moments through the twist calculation, odd-order tail and actual legal
query duality. No original or failed historical evidence was overwritten.
