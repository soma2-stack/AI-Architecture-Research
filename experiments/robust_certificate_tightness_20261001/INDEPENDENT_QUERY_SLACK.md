# Structural query-margin slack in the independent control

This calculation changes no archived constants or certificates. It is a separate
tightness diagnostic and possible stronger lower calculation on the SAME boxes.

In independent recurrence, every parameter column p is owned by one state row
i(p). Its sensitivity vanishes in every other row. The recurrence preserves
this support from S_0=0. Parameter-group RMS normalization preserves the zeros.
For every supported difference, the squared query norm is therefore

||DeltaS^T c||^2 = sum_p c_(i(p))^2 DeltaS_(i(p),p)^2.

The diagonal recurrent coefficients are positive. For the accepted positive
gate box, every summand is nondecreasing in every gate gamma_i. Thus the exact
query maximum occurs at the all-high-gate vector. No query optimization or
discarding of supported residual coordinates is necessary.

In particular choose the permitted all-equal gate gamma_i=7/8. Define
d_i = (7/8) R_ii / (sqrt(n) beta). For any full supported difference,

D_C >= sqrt(sum_p d_(i(p))^2 DeltaS_(i(p),p)^2).

For an existing projection functional ell,

|DeltaPsi| <= sqrt(sum_p ell_p^2 / d_(i(p))^2) D_C

by Cauchy-Schwarz. Hence a valid projection margin is

mu_structured = (7/8) /
  (sqrt(n) beta sqrt(sum_p ell_p^2 / R_(i(p),i(p))^2)).

This inequality includes EVERY supported residual difference; it only excludes
structurally impossible off-owner entries. It is valid jointly for every saved
projection: D_C >= max_i mu_structured_i |DeltaPsi_i|. The all-equal 7/8 gates
are in the already accepted preactivation/gate family. Evaluate this expression
with outward CPU intervals and exact rational projections, then apply the old
packing formula to the unchanged accepted rho values. Keep these new diagnostic
lower counts separate from the historical Level-A counts and numerical packs.

This is not an accessibility/observability re-proof, architecture proposal, or
claim about dense sensitivities. Dense parameter columns lack this support,
so the same weighted-coordinate identity does not apply to them.
