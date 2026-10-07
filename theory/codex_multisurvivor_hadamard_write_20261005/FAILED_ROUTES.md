# Failed routes: first failed step

2026-10-05. New Codex analysis; historical accepted results unchanged.

1. **Synchronized groups plus Hadamard reads — FAILED in scope.**
   Exact private survivor response is 1 r^T; zero-sum spatial reads vanish.
   Rotating reads cannot make K spatial factors. This does not imply r is
   a one-coordinate parameter vector or D<=1.
2. **Perfectly matched pairs — FAILED as private write.** Pre-correction
   Gram I/2-11^T/(4K) has minimum gain 1/2, but Mv_j=tau_j v_j and private
   H v_j=0. Matching final traces makes the comparison zero. The invalid
   inference is to call this pre-correction gain persistent private gain.
   Breaking matching with an earlier mask lies outside this argument.
3. **Unequal four-step public filters — structural SUCCESS, robust FAILED.**
   Exact determinant is positive after trace matching/reset. Actual pair
   is nevertheless <.47991/sqrt(n)<.002. Nonzero rank/gain is not a robust
   dimension theorem. Two responses are not counted as two robust dimensions.
4. **Lengthen an all-low filter bank — FAILED in scope.** All memory gates
   <=.9992 imply complete sensitivity <1250 before reset, regardless of
   length. A claimed Theta(T) asymptotic gain in that subclass is false.
   Histories retaining near-critical sites are not covered.
5. **Affine simultaneous Hadamard gate code — FAILED as no-dilution mask.**
   A normalized row has norm sqrt(K/C), forcing lambda<=w sqrt(C/K)/2 on
   B^K. The exact minimum state gain is <=a kappa w/(2sqrt(K)); full cube
   legality gives 1/K. Separate normalization per control is the invalid
   step. Nonlinear codes and new temporal histories remain open.
6. **Disjoint cohorts are free space — FAILED as bookkeeping.** At fixed
   total support, per-cohort witness uses sqrt(h/K), not sqrt(h). Keeping
   h0 sites per cohort costs K h0 sites. This is not an all-query upper.
7. **Choose arbitrary private forcing J — FAILED as exact construction.**
   J is coupled to all filters through the full renewal. A good filter
   matrix for a freely prescribed external J is not a legal donor write.
8. **Infer a universal rank-one theorem from one rank-one insertion — FAILED.**
   Chronologically distinct rank-one broadcasts have different left and
   right factors; their sum need not have rank one. The exact two-filter
   example demonstrates this even with public survivor words and traces
   matched. No global robust-dimension obstruction follows from that rank.
9. **Change a gain exponent and announce an improved beta — CONDITIONAL.**
   No improved robust gain was established. Front/bath, simultaneous idle
   controls, masks, rounding, trace independence, endpoint and full norm
   must still be proved. The reviewed beta=3/16 remains; no global upper
   or optimality claim follows.
10. **One initial pulse plus public near-critical filtering — FAILED in scope.**
    Nonexpansive propagation bounds the initial complete sensitivity difference
    by 2delta. Exact final correction has entry difference <=2delta/[(T-1)rho_0]
    because the positive trace has T-1 injection terms. Its full forcing charge
    stays O(delta), so actual pair <.312delta/sqrt(n)+8e-9. The false step is
    assigning a Theta(T) gain to a single write without new private forcing.
    Repeated donor control is outside this obstruction.
