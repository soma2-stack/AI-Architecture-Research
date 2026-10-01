# Post-certificate sensitive numerical checks

These checks are supporting numerical validation, not additional certificates
or witness selection. The independent interval outputs were already committed
as f8ce4dd. No bound, basis, amplitude or selection changes are permitted.

Recompute the two tight entries identified in the independent review:
HH3[1,0,0,0] and HS[11,0,0]. Use a separate signed univariate chain-rule
calculation in mpmath at 90 decimal digits, across all 2^11 sign corners of
the frozen box, plus its center. Cross-check the maximizer at 120 digits.
This checks the actual hidden third derivative and normalized bias sensitivity
second derivative, not a majorant engine. Corners need not maximize curvature;
failure to exceed the bound is numerical supporting evidence only.

Independently solve the original fixed-h equations for face 1's midpoint
antipodes at 90 and 120 decimal digits. Reconstruct supported sensitivities
and the frozen preconditioned output. Compare the actual projection difference
with the rigorously certified face-1 lower bound. Numerical root residuals
do not constitute interval certification. This is not a new history search.

Re-run the same synthetic development tests under a resource monitor, saving
new results separately; do not overwrite the original test record.
