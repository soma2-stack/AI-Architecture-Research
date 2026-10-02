# Manual proof audit

2026-10-02. These are mathematical checks, not machine tests or independent
review. No new numerical experiment was run. Every new lemma remains available
for hostile review.

## Paired finite-radius section

1. The frozen rotation is unchanged. Each paired vector has zero coordinate
   sum and support outside the first d coordinates; therefore it is fixed by
   the Householder, the cyclic/direct-sum matrix, and O. This holds for ALL
   combinations, avoiding a dense row-sum input bound.
2. All source coordinates equal the same public H throughout the interior;
   alpha1=0 and all later injections use alpha=1. N=3n warmup injections end
   at time N+1, the pulse is N+2, and the exact reset is N+3.
3. The pulse squared amplitudes are in [.06,.16] over the entire Euclidean
   unit ball. Its paired signs preserve rotation stationarity. All realized
   inputs, including the dense correction and reset, stay strictly in the
   original cube. No hidden task or gate metadata is supplied.
4. Formula x=atanh(h)-R hprev-b is used only to define histories at the frozen
   base parameter. Parameter sensitivities hold the realized x fixed.
5. Physical history changes occur in TWO input steps only. The total L2
   radius is bounded by L_z sqrt((25/21)^2+a^2)<.2 uniformly in n. This is
   NOT the diagnostic's .05 radius.
6. Actual G_p(u) is exactly affine in u; all other gates/injections are
   independent of u. Therefore B_T(u)=R G_p(u)(R Bpre+E)+E is an exact affine
   endpoint map, with all actual state rows included.
7. Warmup selected Bpre is bounded by n. The reference map agrees on the
   stationary paired subspace; m_N/n>.95. The dense sensitivity error is
   bounded in operator norm by e n^2, not omitted from the argument.
8. The future inputs .2 and .45 are ACTUALLY permitted and yield the accepted
   gate endpoints. The same one-step query works for every point. Its
   effective adjoint uses ACTUAL R and frozen beta.
9. Projecting normalized gradients onto vbar_j H^T/||H|| is an orthonormal
   parameter-group projection. Residual gradient entries are not discarded
   before comparison or assumed unable to change.
10. w_R/beta=1/n exactly at these widths. The leading lower constant is
    13034/10^7; the two correction terms are each <1e-9. The final strict
    Lipschitz lower>.0013 exceeds epsilon=.001 with uniform slack.
11. Boundary antipodes are separated by>.0026. The continuous lower invokes
    the accepted antipodal theorem on ONE jointly admissible sphere. It
    does not combine histories/queries that cannot coexist in a section.
12. The patch is m-dimensional and affine in its SELECTED operator. This
    does not mean the complete sensitivity, all histories, or all feature
    tuples have dimension m.

## Uniform upper and finite variation ledger

13. The reference uses ACTUAL G and H. Difference recurrence uses R on the
    old error and (R-R0) on reference B. Geometric sums give e/gamma^2.
    Late error includes w_R, ||H||, and kappa; r^2 credit entries and n
    forward-state entries are counted, without an age tape or free basis.
14. Exact finite Duhamel uses Vtilde_s=R Btilde_(s-1)+alpha_s E, so parameter
    injection and old-credit transport remain coupled. It applies at each
    common finite horizon, with no commutation or infinitesimal assumption.
15. Adjoint telescoping uses ||R^T Gp||<=a||Gp||. The inequality includes
    both uniform contraction and gate dissipation.
16. Gamma^dagger is zero on its kernel. The extra P_kernel term is retained
    when only one of the two histories has a gate equal to one. Without
    that term, the finite discrepancy bound would be false.
17. The block operator norm is sqrt(||sum A_s A_s^T||op), not a sum of
    individually optimized query norms. All-query kappa is an upper
    envelope, not an RMS replacement. No small tail or dimension count
    follows without a further uniform reachable-family estimate.

## Explicit non-results

No ambient operator ball is asserted reachable. No tangent, ordinary rank,
finite sampled sphere, or period correlation is converted to a dimension
theorem. No O(n) upper, robust superlinear lower, full logarithmic-gap closure,
finite-bit bound, practical memory/learning claim, or architecture is obtained.
