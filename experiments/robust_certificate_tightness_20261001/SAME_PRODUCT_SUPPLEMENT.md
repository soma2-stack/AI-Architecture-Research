# Same-product packing diagnostic

This fixes an evaluation granularity omission in the initial implementation:
binary corners alone cannot estimate extra positions INSIDE an accepted product.
It does not change histories, axes, accepted constants, epsilon, primary
classification criteria, or the already-running primary numerical analysis.

Before this supplemental calculation, declare deterministic projection-target
lattices on the EXACT accepted boxes: 65 levels for r=1, 33 levels per coordinate
for r=2, 17 levels per coordinate for r=3. Solve the same joint hidden/projection
equations; reject failed roots or roots outside the accepted history-coordinate
box. Use complete permitted-query vertex distances, three farthest/greedy
restarts, strict 2.05epsilon spacing and a 512-state cap, unchanged from the
main analysis. No basis selection or box enlargement occurs here.

Record all pairwise minimum distances and a CPU 60-digit closest-pair
cross-check. These remain NUMERICAL LOWER ESTIMATES. This diagnostic isolates
packing/query slack from larger-domain and extra-direction effects. It is
implemented and committed before its measurements; it cannot rewrite the
frozen historical certificates or the primary results.
