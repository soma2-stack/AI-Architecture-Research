# Manual derivation audit

2026-10-02. Written algebraic checks only; no automated test/experiment.

1. **Fixed contract:** c1, gamma1/n, epsilon.001, original R/W/b, source H,
   group-RMS and actual permitted future preactivation family unchanged.
   The adjoint norm is used only for upper estimates; the lower supplies one
   actual legal query. No raw rank, SVD/RMS, packing or separate-axis claim.
   Weak deficits refer to G_*, the memory restriction; public source gates
   remain .84. A full-state near-identity condition would be incompatible.
2. **Indexing:** global first source-establishment step has alpha=0 and zero
   selected credit. Local weak steps1..N all have alpha=1. There are N weak
   steps plus preparation/reset. The final reset gate is I and adds I to M;
   it is not silently treated as a positive-gap gate. An earlier prefix is
   separately bounded, never silently reset without the error (8).
3. **Whole cube lift:** hidden=signed sqrt(z/n), fixed source and endpoint;
   atanh inverse uses the actual frozen R. The defining input dependence on
   public R is not included in theta derivatives. All gate words, including
   all mixed section combinations, fit the past cube by a uniform input bound.
4. **Elementary amplitude bounds:** atanh(.4)<.424 follows from its first
   three odd-power terms plus tail x^7/[7(1-x^2)], x=.4. The small memory
   atanh is <.036. Reference memory propagation is at most1/(2sqrt2), source
   propagation .4/(100n), and dense correction <1e-8; thus |input|<.48.
5. **Old credit:** product norms <=[a(1-z_minus/n)]^N, and N>=4n log n.
   Multiplying n by A_n a yields the exponent1/2-4(1+z_minus)=-37/10.
   Fresh injections are retained independently of that fading result.
6. **Pair support:** physical k-vectors are explicitly converted to r-vectors
   with E^T. Paired zero-sum NC vectors are O_* eigenvectors with eigenvalue1.
   Equal-pair diagonal gates preserve their lines and orthogonal complements;
   therefore the scalar recurrence is exact, not just its projected tangent.
7. **Time count:** log n>3 for n>=200 (e<3 gives e^3<27<200), so N>12n+1.
   The constant-tail prefix is nonempty, and its eligibility is public>=0.
8. **Radius:** square-root difference denominator is >=sqrt(.05)+sqrt(.15).
   The paired norm coefficient <.24/sqrt(n), e.g. sqrt(.05)>.22,
   sqrt(.15)>.38 and sqrt2<1.42 suffice. The first changed input has only
   current-state variation, subsequent J-1 inputs include previous-state
   propagation, and the final reset includes only propagation. Using J=12n,
   n>=200, (10)-(11) give radius<2 for the ENTIRE ball.
9. **Derivative sign:** differentiation of b(z)^J p_pre adds nonnegative
   magnitude to -p'_J. Fresh scalar derivative is exactly sum(j+1)b^j/n.
   Its geometric tail is b^J[1+J(1-b)], not an omitted old-history term.
10. **Rational margin constants:** 1-b<=(5/4)/n, b^J<=exp(-12), J=12n;
    (5/2)^12>16000 gives 16exp(-12)<.001. Thus the derivative exceeds
    (.999)(16/25)n>.63n. No width-dependent numerical fitting is involved.
11. **Actual query:** preactivation pair.25/.5 from the common zero endpoint
    means future input.2/.45 with W=I,b=.05. Actual xi=R^T g/(beta sqrt n).
    R0 pair eigenvalue a plus dense error e_R gives (15). Projection onto
    orthonormal Phi_j cannot increase or cancel the full gradient discrepancy.
12. **Antipodal lower:** ||u-(-u)||=2; a^2>.99 and sqrt(2l/n)>=1. The
    rational principal half-margin is .00174636. Dense future half-loss
    <=e_R||H||<2e-9 and accepted past half-loss eta<2e-9 leave >.00174.
    This is whole-sphere finite separation, not tangent accuracy.
13. **Scoped exact encoder:** constant tail depends on u alone; full actual
    affine powers give B_end without a saved history. Count u, optional clock
    and actual current h; no history-dependent matrix is made public. This
    is a subclass upper, not a general aperiodic result.
14. **Ordered-word coefficients:** D/n directly perturbs the injection in
    order1 and propagation at every higher order. Summing the homogeneous
    recursion exactly restores G(aO M+alpha I) at each time. No products
    are commuted or averaged.
15. **Truncation constants:** 1-b=(1+a z0)/n, C_n=Delta/[n(1-b)^2],
    q_n=aDelta/[n(1-b)]<1 because z0>Delta. The order1 forcing is at most
    Delta/[n(1-b)]; geometric propagation gives C_n. Each higher order
    costs factor q_n. The tail is C_n q_n^p/(1-q_n), uniform in horizon.
16. **Error allocations:** after the reset multiply tail by a. Add eta once
    and the inherited-old error (zero for preparation). p_n yields total
    <=epsilon/4. A proxy decoder error<=3epsilon/4 suffices for epsilon;
    proxy antipodal half-margin>5epsilon/4 survives a half-loss<=epsilon/4.
17. **No fake reduction:** the explicit polynomial is on reachable gate
    words. Its first-order term alone is insufficient under the present
    uniform tail bound. Offline nonlinear width and online continuous counted
    encoding are distinguished. Degree is not memory, and norm-bound failure
    is not a lower theorem or proof that compression is impossible.
18. **Preservation:** old experiments/reviews/chart outputs and other notebooks
    are read-only. Current research pointers are prepended; historical records
    remain. No new architecture, learning, other gap regime or GAS-0 action.

All stated scoped algebraic arguments pass this manual audit. This is not an
independent hostile review. The arbitrary aperiodic question remains open.
