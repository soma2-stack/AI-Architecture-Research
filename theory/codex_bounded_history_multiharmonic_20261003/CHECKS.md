# Internal check ledger

2026-10-03. New analytic result; no independent review is claimed.

## Written proof checks

1. The target radius is about public X_n(0), matching the user's explicit
   ||X(y)-X(0)|| contract. An absolute ||X|| bound is not substituted.
2. Existing profiles are used exactly, including joint delta/F and projection
   after saturation. The uniform L2 bound follows from projection norm1,
   not numerical spreading. It is used ONLY for input energy.
3. c_t has EXACT zero sum; physical omission of node0 is charged separately.
4. The shift is P v(i)=v(i-1), matching the existing eigenvalue convention.
   Cosine phase change is paid using sum f, with every F denominator retained.
5. phi is the exact square-root lift, not its linear approximation. The
   Taylor remainder is used only to bound its sum, with linear zero sum.
6. Physical p_t(0)=0. The Householder expansion includes both first-order
   terms and the quadratic rank-two term; |w^T P w| is bounded explicitly.
7. A nonzero nonlinear hidden mean is NOT assumed zero. Its norm is bounded
   by the full joint c_t energy, yielding delta^2/F^2.
8. Source/input changes from the ACTUAL dense R perturbation are counted.
   atanh movement is separated into the identity plus a bounded small part.
9. Preparation contributes0. First varying step and final reset are both
   included; interior time slots add squared norms without time cancellation.
10. Every inequality is uniform over the entire parameter ball; no selected
    axes or sampled grid is substituted for joint admissibility/radius.
11. delta and F change only public scalar rules. The old accepted query
    proof holds for arbitrary admitted sup amplitude and its size conditions.
12. All nonlinear odd terms, original epsilon/4 transfer/poly error and
    actual-R query correction2e-9 remain paid. No RMS visibility substitute.
13. Monotonicity n^(1/36)/(log n)^(1/4) requires log n>9, which holds well
    below n0. Tail exponent is -1/12, not positive or omitted.
14. n0=10^900 guarantees every floor/net/Fourier condition, not just the
    positive ledger. qF is one joint dimension; all endpoints equal0.
15. Borsuk-Ulam concerns the ONE boundary sphere. The result is not a packing,
    exact-rank or finite-bit theorem and does not multiply sources.

## Executable checks

checks.py is newly written and imports no Claude/Grok code or numerical
outputs. It uses CPU NumPy with one BLAS worker. Cases/seeds are fixed,
not searched. Profile generation at small widths is an algebra diagnostic,
not a numerical substitute for the accepted large-width spreading lemma.

The actual numerical history radius is summed across the whole frozen
diagnostic word using its exact cycle repetition, with the preparation/reset
boundaries counted separately. The mathematical proof does not rely on
float64 agreement, small-width ranks or those diagnostic radii.

All 17 Fraction/scalar comparisons and all three geometry checks pass.
Any additional replay writes a separately numbered result, never overwrites
the first run or historical project artifacts.
