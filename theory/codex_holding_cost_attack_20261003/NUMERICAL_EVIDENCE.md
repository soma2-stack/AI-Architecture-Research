# Numerical evidence, kept separate from proof

No witness search. All numerical work is CPU only and supports/falsifies
formulas; numerical agreement is not a rigorous nonzero or interval certificate.

## First path: NumPy identities and mpmath scalar ledger

checks.py / checks_result.json: 61 recorded checks pass. Scalar parameter
cases n=10^200,10^240, F=2,floor(log n),10^floor(log10(n)/16), use exact
rational arithmetic plus 240/320 binary-bit calculations. The all-width
range is justified analytically, not by sampling its endpoints.

At n=8192,m=8,T=32,F=2, reference raw input maxima .0595686113.
Three prescribed parameter samples have total squared norms
10.39723745,10.39707629,10.39699199 in the ORIGINAL zero-bath preparation
identity test. This first test is preserved; the cheaper autonomous
preparation is checked in the separate path below.

Common endpoint, private support and all 33 public-bath comparisons pass.
Projected query identity discrepancy: 3.09662e-21. One tested actual
normalized query distance is 3.20540e-10, far BELOW epsilon; no finite-error
dimension is asserted for these small sanity cases. Ordinary column leak
.0224478 is below the conservative .0662913 cap.

High-precision source accounting yields:

    old E^2/(nT) = .0710567615174115579961983298...
    old source fraction = .982408429918471539724...
    autonomous E^2/(nT) = .00125
    new/old norm coefficient = .13263321635822777662...

## Separate pure mpmath list-arithmetic path

checks_autonomous_preparation.py / corresponding result JSON: 13 checks
pass, n=400,m=2,T=6, at 240 and 320 bits. Uses the new zero-input bath
preparation and two full nonlinear inverse-lift histories.

    full reference energy squared: .06055079788831 / .06002941963209
    maximum raw input: .09332836397013
    common endpoint error: displayed 0 at both precisions
    maximum product-kernel error at 240 bits: 2.264e-72
    maximum query identity error at 240 bits: 3.274e-77

Energy and query coefficients agree to all 60 displayed digits. These are
ordinary high-precision calculations without explicit outward error bounds,
labeled HIGH-PRECISION NUMERICAL. Theorems rest on written exact identities
and analytic inequalities, not these samples.

No numerical scaling fit, robust-dimension count or additional epsilon
analysis was performed. GPU usage zero; total mathematical CPU 3.34375s.
