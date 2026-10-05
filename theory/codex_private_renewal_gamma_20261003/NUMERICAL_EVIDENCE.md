# Numerical evidence — support only

Two scripts were run sequentially. They import no historical certification
engine, use one process, all numerical pools1, no workers, and no CUDA.

## checks.py: 58 PASS records

- Independent C+rank-two expansion and orthogonality of O_*.
- Seven direct full M-L comparisons against ALL-orders Volterra reconstruction.
- Exact co-moving zero-sum spaces, unit fixed probe and its norm1/2 projection.
- Three full two-step complement singular norms are about .99646, .99703,
  .99653, below the theorem's conservative .99999951 bound in that algebra case.
  SVD is an IDENTITY/STABILITY CHECK, not a dimension or query-visibility proxy.
- Small reference history n=65536,m=2,T=32, early high gate .9951, low .995:
  prescribed final gate .9945971742476; exact traces agree numerically;
  public-state discrepancy <=5.56e-17; common endpoint; direct probe difference0;
  private feedback probe norm about1.78695e-6. A legal-box probe lower is
  about1.93883e-12, FAR below epsilon. Its p=3; it is NOT an equal-quantile
  counterexample. It validates only trace/renewal identities. This is not
  the official asymptotic gate choice and was not optimized.
- At n=10^200, stable192/256-bit scalar paths agree on the margin arithmetic;
  lower approximately .040311216, complement relative error1.6e-47,
  tail drift4.36886e-44, local p-expression5.05964e-21.

## corollary_checks.py: 19 PASS records

At n=10^1000 with logarithmic m,T,192/256-bit calculations agree to40 digits:

    complement error / kappa = .000301778999813654117431939786325931...
    kappa / T = .999999056942107847854941406565446380...
    scalar lower = .040311177984189317038674349129984198...

High precision alone is not outward interval certification. At huge widths
rounding enormous T to an integer cannot be audited from finite precision;
the analytic proof explicitly absorbs all floor/ceiling errors with m>=.99
times its real target and T between its target and the11-constant upper.
Stable log1p/expm1 formulas avoid catastrophic1-near1 cancellation.
The claimed theorem is based on analytical inequalities, not these numbers.

No numerical experiment attempts a joint superlinear robust section.
