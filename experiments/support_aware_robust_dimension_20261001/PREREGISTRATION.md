# Support-aware robust continuous dimension

Frozen before official calculations. Source checkpoint: 915d007. Only the eight
existing dense/independent archived/confirmation endpoints at n=3,T=22 and
n=4,T=37. Old files are read-only. No new history, width, architecture, training,
GAS-0 operation, prior theorem review, or epsilon change.

## Contract and definitions

epsilon=1/1000, unchanged input SD sqrt(3/32), frozen parameter-group RMS,
q=ones/sqrt(n), beta=max(1,||R||F), future preactivations [1/4,3/4]^n.
Independent query distance is the exact supported weighted Euclidean norm at
the all-high gate. Use the reviewed 7/8-gate lower enclosure for certification.
Dense distance is the maximum of the permitted gate-box vertex query norms;
the accepted interior frame supplies a rigorous residual-safe lower bound.

An r-dimensional EPSILON-ESSENTIAL continuous section means a continuous
fixed-h lift of a projection box, whose opposite boundary points have query
distance >2epsilon. This implies that a continuous no-replay encoder in fewer
than r real coordinates cannot answer all allowed queries to epsilon. It is
not a statement that any r-dimensional infinitesimal chart is useful at epsilon,
nor that the true global robust dimension is at most r.

For normalized projection coordinates z_i in [-1,1], require
D >= max_i b_i |z_i-z'_i|, b_i=mu_i*rho_i, with b_i>epsilon on every retained
axis. Then m=min(b_i)/sqrt(r) is a Euclidean lower Lipschitz constant. A
certified upper derivative bound gives M. Borsuk-Ulam applies to the boundary
of the cube via radial identification with S^(r-1); opposite points have
max|z_i|=1, so the antipodal test uses min(b_i), not m. This is a new
dimension-oriented consequence of accepted product geometry, not a repeat of
the isotropic theorem. finite states/bits and continuous r are reported separately.

## Frozen systematic procedure

1. Apply the dimension lemma to every accepted product, using reviewed
   support-aware margins for independent recurrence. Evaluate sub-products
   at fractions 1,3/4,1/2,1/4. A shrink can improve curvature but cannot by
   itself increase a fixed product's observable range.
2. At the SAME histories construct deterministic fixed-center charts with up
   to eight existing types of SVD history directions. Two output projection
   rules: accepted finite-frame Gram dual; for independent only, supported
   diagonal-R weighted Gram dual. No history optimization. Rationalize all
   basis/projection constants at 128 bits before interval evaluation.
3. Test prefixes r=1..8, tangent amplitudes 1/2,1/4,1/8,1/16,1/32,1/64,
   equal and sigma/sigma1 profiles, equal normal half-width multiplier 1.
   Recompute entire simultaneous HH/HS mixed bounds, hidden contraction,
   fixed-h curvature and selected inverse-product certificate at 192 bits.
   Keep accepted contraction cap3/4 and target fraction9/10. Reject boxes
   exceeding raw-history +/-1. No optimization of constants after failures.
   Compute every scheduled trial, subject to the resource stop. Rank successes
   lexicographically by epsilon-essential dimension, minimum retained margin,
   then smaller amplitude. Failures are method failures, not upper bounds.
4. Recompute the selected best new chart at 256 bits, with its rational
   preconditioners fixed. Include ALL mixed derivatives. If it fails, do not
   relabel it certified; fall back only to already valid accepted products.
5. Numerical scale diagnostic in the selected certified section only: 257
   deterministic Sobol points plus corners (corners capped at r<=8), solve
   H=0 and projection targets using CPU Newton. Distances are the unchanged
   full permitted query metric. Farthest-point packing with three fixed
   starts at separation 0.5,1,2,4 times the primary collision scale 2epsilon.
   Slopes are numerical and censored by sampling, not dimension proofs.
   No secondary epsilon experiment or new-history promotion.

## Bounds, classifications, controls

Prove global upper/lower Lipschitz constants on accepted and new sections with
interval center derivatives, whole-box Hessian bounds and exact rational
Neumann matrices. Retain structural dimension ceilings D=63/144 dense and
15/24 independent, but do not call them useful epsilon-specific upper bounds.
Inspect uniform tails only if existing bounds justify a smaller upper cover;
otherwise report NO USEFUL ROBUST-DIMENSION UPPER BOUND FOUND.

Classification: Very small if completed reliable certificates give maximum
r<=3; Moderate if 4<=maximum r<=8; Large if r>=9 (not reachable under this
eight-prefix pilot); Finite-state large/continuous unresolved if the required
finite-radius checks cannot be established; No useful certificate if none
has r>=1. These describe achieved LOWER certificates, not maximal dimensions.
Architecture gate remains MORE ROBUST-DIMENSION WORK NEEDED unless a useful
upper bound or a reproducible uniform compression structure is actually proved.

## Validity and resources

Tests before official runs: support query identity, residual-safe dual margin,
cube antipodes, scale/epsilon criterion, Neumann inverse positivity, upper
derivative accounting, frozen input hashes, CPU enforcement, deterministic
basis and matching normalization. Check selected interval certificates at192/256.
Invalid arithmetic/NaN/parameter mutation/source changes halt interpretation.

One CPU/BLAS worker; CPU-first because widths<=4 and interval work dominates.
No GPU workload planned; numerical diagnostics also fit CPU. Maximum measured
CPU3600s, RAM4GiB, free RAM>=4GiB, free disk>=2GiB. Preserve partial trials
on resource stop; no threshold changes. Record every process, failures,
CPU/wall/RAM, seeds, hashes, ranks, amplitudes, constants and discarded axes.
Use development seed9910100 and diagnostic seed9910101; no outcome-selected seeds.
Stop after report/commit/push. No architecture, Stage C or AMS v10.
