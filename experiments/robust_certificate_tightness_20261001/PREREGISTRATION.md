# Robust-certificate tightness / true-dimension gap

## Scope and frozen comparison

This is a bounded numerical geometry audit, not model training or witness search.
Eight endpoints: archived and frozen best-confirmation histories, for dense and
independent widths 3/4, horizons 22/37. Source result commit 7cb9f3d; procedural
cleanup 1e17cb8. All old artifacts are read-only. Parameters, initial state,
input-SD/parameter-RMS normalization, future head, and epsilon = 1e-3 are unchanged.

Level A is the accepted existing interval lower certificate. No old certificate
is relabeled as an upper bound. Level B is direct numerical finite point packing
on a solved fixed-h section. Level C is failed specific grids, sampled curvature,
and a rigorous but potentially useless covering upper bound. A finite vertex
packing is not a proof that the entire intervening product is injective.

## Declared local domain and numerical procedures

Use normalized history coordinates with SD = sqrt(3/32). Frozen charts use their
saved normal basis and tangent directions. Additional local bases are derived
at the SAME endpoint, never by altering the central history: SVD, query-weighted
SVD, center-curvature reordered SVD, and two seeded rotated SVD frames. Numerical
products have tangent half-widths 1/8, 1/4, 1/2, 1. Normal correction coordinates
must stay within [-1,1], and EVERY raw history coordinate remains within +/-1
of its frozen center. This larger declared local domain is distinguished from
the smaller accepted certificate boxes. Comparisons also evaluate identical
finite grids inside the accepted projection product, so domain enlargement
cannot silently be described as certificate slack.

Newton solves the hidden-state equation to 2e-12 in binary64 (maximum 18 steps).
Products use all binary corners for r=1..10. If r=10 succeeds, test r=11/12 at
its selected amplitude; no partial grid is reported as a complete product.
Save every grid failure and its closest pair. Follow successes and failures
with multiple bases. Select winners only among these declared local analyses.
An r-dimensional binary corner packing has 2^r states; r is its grid dimension,
not an upper bound on the true robust dimension.

Each endpoint also receives 2,048 Sobol tangent points in a 16-direction local
chart (clipped to available dimension), plus all successful tested grids.
Farthest-point and two seeded greedy restarts retain pairwise distances above
2.05epsilon; cap retained states at 512. Reaching that cap is censored, not a
maximum. Report selected states, coordinates, all-pair minimum separation and
closest-pair high-precision verification. No history-center search or mutation.

## Exact query geometry, numerical evaluation

Allowed future preactivations are [1/4,3/4]^n. With q=ones/sqrt(n),
beta=max(1,||R||F), effective c=R^T gamma/(sqrt(n) beta), and gamma ranging over
[sech^2(3/4),sech^2(1/4)]^n. The norm of DeltaS^T c is convex in gamma. A convex
function on a box attains a maximum at a vertex: iteratively express an interior
coordinate as a convex combination of its two endpoints. Thus all 2^n vertices
give the EXACT query-family maximization formula. Numerical evaluation of that
formula remains Level B unless outward interval verification is supplied.
The future parameter injection cancels for paired histories with equal h.

Evaluate full sensitivities, including residual coordinates. Compare exact-
formula numerical distances to the existing dual lower bound max(mu_i|DeltaPsi_i|).
CPU 60/100-decimal-point reevaluation checks critical pairs and root residuals;
it is a trusted numerical cross-check, not a finite-box theorem.

## Curvature and slack

For EACH accepted box sample 512 Sobol points, all corners where <=256, the
center, and 24 iterations of six-parent SPSA maximization of the largest
actual/certified raw Hessian ratio. This optimizes a diagnostic inside a frozen
box, not witnesses. Signed third-order sensitivity jets supply every h_yy and
S_yy entry. Store entrywise actual maxima/bound ratios, complete raw majorants,
normal-normal/normal-tangent/tangent-tangent classes, and the worst point.
Validate its maximum entry at higher CPU precision. Sampled maxima are lower
estimates of suprema. No sampled miss becomes an upper bound.

Also sample the solved fixed-h section and measure actual normal compensation,
Jacobian variation and implicit-section Hessian against the stored selected
majorants. Decompose tangent strength, compensation, global/mixed majorants,
contraction cap, amplitude, query duality, 17/8 spacing, prefix cap and interval
inflation. When contributions interact, report coupled ratios, not invented
independent multiplicative causes.

## Raw-history diagnostic

Select 32 raw SEARCH pool IDs per main width using a fixed new diagnostic seed;
same IDs for both models, no confirmation IDs, no adaptive histories. Directly
evaluate the old expensive primary proxy without spectral prefiltering. Record
the score, strategy, spectral rank in the old pool, and whether the old shortlist
missed a high primary proxy. Do not certify, replace winners, or start a new
witness campaign from these diagnostic results.

## Valid upper-bound attempt

On the raw history cube center +/-1, bound every normalized sensitivity entry
by the positive exact recurrence using |tanh|<=1, |tanh'|<=1 and bounded inputs.
Enclose RMS factors upward. A coordinate cube cover with query diameter <=
2epsilon gives a finite packing upper bound. This may be enormous; explicitly
say NO USEFUL UPPER BOUND FOUND if it cannot constrain the lower/upper gap.
Tangent singular values and numerical failures cannot replace this proof.

## Validation, resources and stopping

One CPU/BLAS worker; GPU binary64 batches <=64 for Hessian work. Hard self-imposed
limits: 60 measured CPU minutes, 60 GPU-active wall minutes, 4 GiB process RAM,
4 GiB own GPU pool; keep 4 GiB system RAM headroom. Preferred GPU <=80C; stop
GPU work above86C. Preserve partial outputs on any validity/safety failure.
Record all processes, invalid attempts, resources, hashes and precision.
Tests cover signed jets vs finite differences and CPU, fixed-h solving, exact
vertex query formula, whole-grid distances, no parameter changes and input
domain checks. No tests or compute in GAS-0.

## Frozen descriptive classification

Apply in this order after validity:
1. MODEL-DEPENDENT CERTIFICATE BIAS FOUND if independent's median numerical-
   versus-certified grid bit gain exceeds dense's by >=2 bits AND its median
   actual/dual query-distance ratio is >=2 times dense's (both witnesses/widths).
2. CERTIFICATES ARE HIGHLY CONSERVATIVE — MANY MORE ROBUST DIRECTIONS APPEAR
   NUMERICALLY if at least two endpoints yield validated complete grids with
   >=6 directions and >=3 more directions than their accepted certificate.
3. CERTIFICATES ARE MODERATELY CONSERVATIVE if any endpoint adds >=1 direction
   or >=1 bit by direct validated numerical packing on the SAME declared chart
   domain, with no useful tight upper bound.
4. CERTIFICATES ARE FAIRLY TIGHT — ROBUST CORE APPEARS SMALL only if a useful
   rigorous upper bound is within one bit of every endpoint's best lower bound.
5. Otherwise NO USEFUL CONCLUSION — UPPER/LOWER GAP REMAINS TOO LARGE.

No numerical upper claim, width law or architecture follows from these labels.
ARCHITECTURE DESIGN READY requires a useful tight upper characterization or a
reproducible validated compression structure; otherwise MORE ROBUST-DIMENSION
WORK NEEDED. No architecture is designed in this stage. Stop after report.
