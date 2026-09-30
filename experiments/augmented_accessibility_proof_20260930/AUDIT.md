# Hostile checks of the arbitrary-width argument

## Checks that could have invalidated it

1. **Only propagation spans matrices.** Avoided: sections 3 and 6 retain the
   actual deltaR*h, deltaW*u, deltab and R*S injections. The exact augmented
   differential identities are checked symbolically; full sensitivity columns
   are extracted separately.
2. **Different histories are combined without one endpoint.** Avoided by the
   forward rank-increment lemma in section 8. One selected raw prefix generator
   outside the old derivative image adds a genuinely independent last-input
   derivative to a single extended history.
3. **Illegal state-dependent control differentiation.** Coefficient extraction
   uses a finite list of constant controls; inversion of the evaluation matrix
   gives only smooth linear-combination coefficients. No derivative of a chosen
   feedback law is used in the fixed-control pullback.
4. **Parameter normalization freezes W derivatives.** W0 is only the fixed
   invertible coordinate-change matrix. All entries of W_new=W*W0^{-1} remain
   differentiated, and the induced parameter/sensitivity coordinate map is
   invertible.
5. **Bias field might disappear when Q is singular.** The expansion of the
   pullback contains separate gamma_l^{-1} terms with constant coefficients
   independent of Q. The other terms are distinct gate-ratio monomials. Thus
   the argument does not assume Q invertible.
6. **A global diffeomorphism theorem was applied to tanh.** Avoided: tanh is onto
   an open image, not all R^n. Only its everywhere nonsingular differential is
   needed for the explicit forward rank-increment lemma. The primary paper's
   stronger default hypothesis is stated as unsatisfied.
7. **A nonlinear result falsely labels the linear control full-dimensional.**
   Identity activation removes the independent gate functions. Its explicit
   bias first integral is checked; the known rank restriction remains intact.
8. **Independent recurrence should also have full cubic dimension.** Its inverse
   recurrent matrix has zero off-diagonal entries, precisely invalidating the
   column-transport premise; owner-local structural zeros remain.
9. **A theorem for arbitrary n implies the shortest known witness horizon.**
   Not claimed. The proved horizon is a loose 4d, not P+1.
10. **Schur coefficient existence is presented as an explicit determinant
    formula.** Not claimed. Section 10 proves non-identical vanishing for one
    all-width coupling family and suitable histories; the coefficient's value,
    order and a simple recurrence are still unknown.

## Outstanding verification status

The formulas and inference chain have been checked in this lane. Exact SymPy
checks are algebra checks, not a formal proof assistant or independent review.
No new certificate has been numerically sought. The previous n=2,3,4 certified
results are preserved and serve as compatible evidence, not premises from which
arbitrary-width genericity is extrapolated.

The conclusion is an existence/accessibility theorem for fully actuated dense
tanh recurrence under sufficient generic parameter conditions. The proof is
deliberately limited to this family. There is no conclusion about practical
precision, online memory lower bounds, future-loss observability, learning,
partially observed inputs, or deep-stack all-width accessibility.

Recommended next action: independent mathematical review of PROOF.md, especially
coefficient extraction, pure-bias projection, and the single-history rank
increment. Do not proceed to observability or learning experiments in this task.
