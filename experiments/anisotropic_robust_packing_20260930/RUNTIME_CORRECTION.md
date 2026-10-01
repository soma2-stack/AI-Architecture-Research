# Preserved interval implementation failure

The initial SVD campaign stopped after 128 recorded proposals when a broad
interval evaluation of tanh lost numerator/denominator correlation and the
subsequent curvature majorant overflowed binary64. The initial expression
(exp(2*x)-1)/(exp(2*x)+1) was enclosing, but unnecessarily allowed outputs
outside [-1,1]. It was not a reliable implementation for these larger boxes.
The partial campaign is preserved in attempts_svd_initial_interval_bug.jsonl;
its 172.9375 CPU seconds remain charged. It is not the primary result.

The correction evaluates the two interval endpoints separately, using tanh
monotonicity, and intersects with its rigorously known range [-1,1]. Taylor
evaluation may terminate once its explicitly bounded remaining tail is below
two dyadic units. The tail is still added outward. This changes no witness,
seed, axis, units, epsilon, candidate grid, threshold, or information access.

An explicit wide-interval monotonicity/range test was added. All ten tests
passed before the corrected campaign. Repeated center inverses are cached
for runtime efficiency; these are the identical checked rational matrices.
W invertibility is explicitly checked for realization of the future queries.
No earlier artifact or GAS-0 file was changed.

After both certificate campaigns and their successful 256-bit replays, the
postprocessor's first import found an archived verify.py with the same module
name because the read-only archive loader prepended its directory to sys.path.
The postprocessor stopped before producing summaries. Explicit file loading
of this stage's verify.py corrected this generic import collision. No measured
campaign was rerun or changed; five seconds of unmetered import CPU are charged
as a separate conservative estimate.
The next postprocessing attempt stopped on unsupported Fraction/mpmath
division when formatting an isotropic comparison value. Explicit conversion
fixed this output-only type error; that metered attempt remains in the ledger.
