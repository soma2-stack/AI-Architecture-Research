# Written algebraic checks

2026-10-02. This is a manual proof audit, not an automated test report or
independent certification. No new numerical experiment was run.

1. Scope: only the verified online polynomial and its Grok review are used.
   n>=200, c=1, gamma=1/n, epsilon=1/1000, source, normalization, gate cube,
   preparation/reset exceptions and actual future queries are unchanged.
2. The public degree-zero recursion gives the same Q_t and tied D_t Q_t/n
   injection in every comparison. Source columns are not independently chosen.
3. `q_n=2a/(20+3a)<1/11` follows from `19a<20`. Consequently
   `1+1/(1-q_n)<21/10`; no rounded decimal is used to establish the bound.
4. The projection pi_m commutes with update-and-reproject because the
   triangular transition only transfers degree j-1 into j. Public forcing
   is in degree 1, and never requires a deleted higher degree.
5. The sum of operator norms contracts by b+u_n=b_max for homogeneous
   triangular differences, including the final truncated boundary. The
   actual supremum nu_n is retained; its operator upper is used only for
   sufficient safe bounds, never as an equality or a robust lower.
6. The m_n integer rule is capped safely at p because the verified frozen
   tau_n<=epsilon/4 is already below delta=3epsilon/4. m=0 gives the public
   code when its bound is enough. Increasing the degree later is not free.
7. The ell_n/t0 rule handles ell_n>N (only the initial zero cut), ell_n=0
   (the whole window negligible), and exact equality at delta0 correctly.
8. Initial erasure includes all mixed old and fresh credit already present
   at the cut. Shared future forcing cancels in the suffix difference.
   Nonexpansiveness applies to common admitted gate symbols.
9. Common gate symbols are not incorrectly equated with common raw inputs
   when actual and shadow current h differ. Both lifted words are legal
   and reset to the same endpoint; actual h is kept and counted separately.
10. The full chronological hierarchy in section5 is a finite-history proof
    device, not hidden persistent storage. Its C_n q_n^(j-1) envelope is
    preserved under homogeneous continuation because b+u_n/q_n=1.
11. The lifted carrier's order-h contribution is bounded by chronological
    placements binom(L,h). The binomial probability upper is valid without
    commutation and also when h>L, where the contribution is zero.
12. At lambda=1 the two full homogeneous carriers start with the same F
    and follow the same products. Only their tails differ after truncation.
    Public and new future forcing cancel, rather than being charged twice.
13. Exact budget arithmetic:
    `epsilon/8+21epsilon/40=13epsilon/20<3epsilon/4`;
    adding the accepted epsilon/4 actual ledger gives 9epsilon/10;
    `epsilon/16+21epsilon/40=47epsilon/80<3epsilon/4`.
14. The auxiliary Y code uses r^2 scalars, not Y plus the full polynomial
    hierarchy. Public M0/Q, static constants, workspace and final output
    are excluded under the accepted contract. Adaptive history-dependent
    factors would count if introduced. A non-public clock costs one scalar.
15. The offline compact-cover weights have a positive denominator on R_t.
    Continuity follows from the continuous seminorm. Convex interpolation
    and the affine decoder give its error bound. This is not an online
    update, and the full jet needed to evaluate weights is not free.
16. Projection absorption proves uniform error by induction only if its
    exact identity and explicit continuous coordinate maps are present.
    It is not asserted for the offline interpolant or for a Cn map.
17. The robust lower uses the accepted joint section and buffered polynomial
    antipodal margin. A decoder collision would bound pair distance by
    2delta=0.0015, below the accepted distance >0.00298. Exact-realization
    rank, separate axes and finite-state counts are not substituted.
18. Reference M is a continuous causal prefix statistic. No exact identity
    M=f(Z_t) is proved here, and no impossibility of such an identity is
    asserted. The literal finite-jet causal width and its implementation
    count are stated separately without rejecting the accepted ordinary
    reference-memory upper.
19. No Cn realization, omega(n) robust section, whole fixed-feature Theta(n),
    full-model gap closure or architecture claim is made. No new gate regime,
    GPU experiment, server work or historical evidence modification follows.
