# Independent pulse verification and co-rotating age-profile screen

Frozen prospectively on 2026-10-02, before this directory's official outcomes.
Source context: HEAD 4a8a2dc; Claude's uncommitted handoff is hashed separately.
Historical files are read only. No imported Claude implementation or outputs.

## Contract and two phases

c=1, gamma=1/n, epsilon=1/1000. The accepted dense tanh family, raw input
cube (-.5,.5)^n, all R/W/b parameters, group-RMS weights, public source
H=.4 ones, exact terminal h=0, and actual permitted future losses are unchanged.
The selected fixed-feature group is R_(memory 2..k, source), not independently
selectable injection columns. Realized inputs are held fixed for derivatives.

Part 1 independently derives and checks the bounded-pulse cap, single-query
cap, stronger one-pulse section, and two-pulse identity. Widths are exactly
200,256,400,601,1000; dense Gaussian recipe seed 0 matches the handoff's public
numerical model recipe. CPU NumPy/SciPy is implemented here from formulas.
Constant-gate warmup uses binary affine composition, not archived sensitivities.
The 80-digit constant check is a numerical cross-check, not an interval certificate.
Required gates for Part 2: analytic verification passes, all one-pulse minima
exceed epsilon, actual fixed endpoint/input checks pass, tiny independent tests
pass. Any substantive mathematical failure stops establishment of that claim.

## Part 2: frozen histories, joint sections, and queries

Widths 200,400,1000; locked active-step lengths are the distinct values in
{2,ceil(ln n),ceil(sqrt n),floor(n/4),floor(n/2),n}. Zero-memory warmup is 3n+1
steps, followed by T active steps and a final exact zero reset. Source H is
fixed throughout every interior step.

Let U be the accepted Householder matrix and P its d-cycle in latent memory
coordinates. Latent profiles z_t have support on that cycle and sum zero.
Actual physical memory h_t=U P^(t-1) z_t. The true diagonal gates are
diag(1-h_t^2), not a fictitious conjugated diagonal gate.

For q in {1,min(T,ceil(ln n)),T}, time basis Q is the first q orthonormal DCT-II
columns. Space basis Z is a deterministic Helmert zero-sum basis with a seeded
orthogonal rotation. C is q by (d-1), ||C||F<=1: ONE joint section, dimension
q(d-1). A zero-sum alternating latent baseline has amplitude B.

Primary bounded-spread map:
 field=sqrt(T*d) Q C Z^T;
 z_t=baseline+(Pamp/2)[tanh(field_t)-mean(tanh(field_t))].
Thus every point has mean-zero profiles and coordinate perturbation <=Pamp.
This is injective as a history chart by strict monotonicity on the zero-sum
subspace; that fact does NOT prove robust credit dimension.

Two frozen strength policies:
 sustained: B=.25, Pamp=.11;
 total-budget: B=.25/sqrt(T), Pamp=.11/sqrt(T).
These remain inside the unchanged input cube for ALL joint combinations;
the physical total-history radius is reported, not silently fixed to .05.

An additional linear Euclidean-ball control is run at T=n, q=min(T,ceil ln n)
for each width/strength. Replace the map by z=baseline+A Q C Z^T, with
A=Pamp/[max_t ||Q_t|| sqrt(1-1/d)]. This controls total physical radius directly.
No axes or histories are optimized in response to outcomes.

For each section test four predeclared unit-sphere directions: two full random
coefficient matrices; a highest-retained temporal-mode rank-one direction;
a two-mode cancellation direction (or another seeded spatial direction for q=1).
Seeds derive from 620021 plus (width,T,q,strength,map). Keep every direction.
These are joint antipodes, NOT individual coordinate-axis counts.

For each antipode compute a legal one-step box-query LOWER estimate by six
starts (uniform endpoints, stationary-block pattern, three random corners),
three sign-gradient iterations, all inside the original future input box.
No RMS criterion replaces worst-case queries. The weakest sampled LOWER pair
also receives an all-permitted-query UPPER ENVELOPE from the full selected
reference operator's spectral norm and the established dense error ledger.
This upper calculation is ordinary CPU numerics, explicitly not a certificate.
No small lower estimate alone is evidence of failure under every allowed query.

The reference uses actual prescribed gates; its uniform actual-dense error is
eta=a||H||e*n. Pair lower/upper corrections are 2eta. Actual dense parameters
are still used to realize and check inputs and to evaluate future-query adjoints.
Full reference propagation and adjoint evaluation are independently cross-checked.
Store query witnesses, section coefficients, spectra, finite-radius nonlinear
response, admissibility, dissipation, and rotating-frame gate mismatch.

## Interpretation and resource stopping

Passing sampled antipodes is NOT a robust-dimension theorem. A numerically
subthreshold all-query upper envelope is failure evidence for this frozen section,
not a cap on all reachable histories. No regression fit is called asymptotic proof.
No automatically changed objective, strength, query contract, or epsilon.

CPU only, one process, BLAS/OMP maximum 4 threads; explicit CUDA exclusion.
Screen priority: all Part 1; then n200, n400, n1000 in order, T increasing,
q increasing, sustained then total-budget; linear controls last. Hard measured
CPU cap 60 minutes for this runner, checked between sections. Stop cleanly and
preserve partial coverage if reached. RAM target <6 GiB. No GPU/model server,
training, GAS-0 workload, new contraction regime, or architecture work.

Implementation debugging uses widths 12/24/32 only. Any repair is recorded;
the frozen scientific protocol/config does not change after official outcomes.
Owner's instruction to commit only after verification is respected: prospective
hash manifest rather than an initial results-free Git commit; commit final work
only after tests, records, and interpretation are internally consistent.
