# Query calculation and conservative upper cover

This does not change or re-prove accessibility, observability, or the accepted
finite-error lower theorem. It supplies two calculations used in this audit.

## Exact maximization formula for the permitted finite-head family

At equal hidden endpoints, the future parameter-injection terms cancel. The
gradient difference after the allowed next step is DeltaS^T c, with normalized
c = R^T gamma / (sqrt(n) beta), beta = max(1, ||R||F). The gate vector gamma
ranges independently over [sech^2(3/4), sech^2(1/4)]^n because W is invertible
and the future-input convention permits every preactivation in that box.

For fixed DeltaS, the norm of the linear function of gamma is convex. With all
other coordinates fixed, its value at an interior coordinate is no greater
than the greater value at the two endpoints, by convexity. Repeating this in
all n coordinates proves that its maximum equals the maximum at the 2^n
vertices. This is an exact algebraic reduction, not a numerical optimizer.
The stored float64/decimal evaluations of these vertex norms are numerical.
No high-precision midpoint is labeled an outward certificate.

## Uniform coordinate enclosure on the declared history cube

The initial state and sensitivity are zero and parameters remain frozen.
For each history step, define the nonnegative rational majorant

M_(t+1)[i,p] = sum_j abs(R[i,j]) M_t[j,p] + I_t[i,p].

For a parameter owned by row i, the injection is bounded by 1 for an R entry
or bias, and by abs(x0[t,j])+1 for a W entry; it is zero at other rows. This
follows directly from abs(tanh)<=1, abs(tanh')<=1 and the declared raw-history
coordinate bounds. Induction gives abs(S_T[i,p])<=M_T[i,p]. Independent systems
use only their supported coordinates; dense systems use all nP coordinates.
Multiply by an upward interval bound for the unchanged parameter-group RMS
scale to obtain coordinate bounds B_l in the physical normalized metric.

For the permitted query c, ||c||2 <= ||R||F / beta <= 1. Consequently query
distance is at most the Frobenius distance between normalized sensitivities.
Partition each coordinate interval [-B_l,B_l] into

N_l = max(1, ceil(B_l sqrt(D) / epsilon))

equal cells. The outward upper bound for sqrt(D) only makes cells smaller.
Each cell has side <= 2epsilon/sqrt(D); the product-cell Frobenius diameter
is <= 2epsilon. Two points in the same cell cannot have query distance
greater than 2epsilon. Therefore every strictly distinguishable packing has
at most product_l N_l points. The calculation uses exact rationals and
upward interval RMS/square-root enclosures.

This upper cover includes far more sensitivities than the reachable fixed-h
image. It is mathematically valid but can be hundreds or thousands of bits,
and thus fail to give a useful tightness conclusion. It is not a bound on
runtime, GPU memory, learned compression, or an asymptotic law.

## Interpretation of numerical products

An r-coordinate binary-corner grid with 2^r separated images establishes a
numerical finite packing and r bits in that grid. It does not by itself prove
global injectivity of the intervening continuous map, an r-dimensional
certified rectangular image, or the maximum robust dimension. Rotation can
distribute a few strong directions among many binary choices (a coding effect).
The report must not identify binary-grid dimension with a proven intrinsic
robust dimension. Larger local amplitudes are reported separately from the
accepted smaller products; those gains are not solely certificate slack.
