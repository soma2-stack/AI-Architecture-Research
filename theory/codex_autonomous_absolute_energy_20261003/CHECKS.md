# Internal checks and compute

27 checks in ARITHMETIC.json, 10 in ZERO_DECODER_ARITHMETIC.json and 6 in
FULL_GROUP_ARITHMETIC.json: 43 pass.
The scripts refuse to overwrite their result files.

The first record preserves the valid INTERMEDIATE public-template error
calculation, including its weaker constants. The second separately evaluates
the final zero-credit theorem. No output was overwritten when the argument
was simplified.

Exact rational checks cover the reference fixed-point sign test, dense
transfer, secant-contraction constants, convolution gains and error-onset
exponents. Independent vector calculations check the selected UPU row identity
at n=200 and 2000. Fixed-point iteration at those same small widths is only
numerical reference evidence, below the new theorem's n>=10^6 threshold.

Negative small-width minima are retained: -0.11760216435074086 at n200 and
-0.0022257110610129443 at n2000. These do not refute a theorem scoped to
n>=10^6; nor are they discarded to make a positive-coordinate claim look
uniform at practical widths.

Scalar evaluations at 80/120 decimal precision agree in all saved 45-digit
values and integer ceiling counts. They are not promoted to outward-interval
certificates. All-width conclusions are analytic, using explicit inequalities
and the exact model, and do not depend on measured numerical minima or spectra.

Main arithmetic CPU .171875s, peakRAM36,921,344 bytes. Final scalar arithmetic
CPU rounded to 0s at timer resolution, peakRAM21,807,104 bytes. Wall times are
saved in the JSON records. No CUDA/GPU, local inference, model server, training,
history search, parameter tuning or architecture work.

No scientific repair or failed inequality occurred. Unsuccessful text-anchor
patches were atomic and changed no file; they were retried against the actual
draft text. The stronger theorem is an algebraic simplification, not a change
of epsilon, query normalization, endpoint family or official candidate.
