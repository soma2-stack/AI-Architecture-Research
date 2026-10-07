# Routes to linear dimension, 2026-10-06

THEORY ONLY. The coded-donor checkpoint at 5cfe9c4 is owner-reported
independently verified by Grok and Gemini. It is a premise. New results
below are author-derived and require independent review.

## The two different obstacles

The previous loss is the sufficient error estimate

    E_tail,mask/kappa <= 10^8(log n+1) sqrt(m/n)
                         + vanishing power errors.            (A)

Taking m/n<=(log n)^(-12) makes its first term O((log n)^(-5)).
The exponent 12 is conservative, not an intrinsic dimension ceiling.
But even removal of (A) does not suffice: the old duration is
Theta(n/sqrt(m)), so m=Theta(n) costs Theta(n^(3/2)). A small fixed
coefficient is not little-o. PROOF.md separates these issues.

## Candidate screen before the complete proof

Here R means number of write stages/rows, not the recurrent matrix.
Constants in schematic scaling are fixed, not width-dependent.

| Route | Mechanism | Proposed dimension | Duration / cost | Signal and main error | Disposition |
|---|---|---|---|---|---|
| 1. Capture before trace repair | One public contrast step stores the private row as zero sum; then trace-tail and clear act in its exact reducing space | Theta(m), two coded stages | T=O(n/sqrt(m)); mT=O(n sqrt(m)) | Contrast times kappa; single-step leakage O(kappa sqrt(m/n)), not log n times it | PROVED scoped construction below; wins the feasible partial result |
| 2. Weak fresh-bit multirow capture | R independent Walsh bits, contrast .005/R per one-step mask; earlier singleton coefficients stay constant instead of 2^(-R) | Candidate Theta(mR) | Axis/stage-selector certificate needs t=O(R n/sqrt(m)), T=O(R^2 n/sqrt(m)) | Capture O(kappa/R); exact protection, but stage and query losses | PROVED mask algebra; FAILED scaling for that certificate |
| 3. Cohort-local captures | R balanced pair rows on disjoint subcohorts; a later mask is identity on older pair rows | Candidate Theta(mR) | Same selector budget O(R^2 n/sqrt(m)) | Capture kappa/sqrt(R), query sqrt(m/R)/n; cohort-mean contamination remains | CONDITIONAL complete section; FAILED optimistic selector scaling |
| 4. Public rotations of stored subspaces | Rotate the stored space between writes, keeping several rows lossless | Candidate Theta(mR) | Ideally T=O(n/sqrt(m)); mT=O(n sqrt(m)) | Would need a controllable isometry from legal diagonal gates | FAILED for gate-only isometric rotation; proof below |
| 5. Hierarchical coded control blocks | Use many coded parameter blocks across temporal levels with stable private read rows | Candidate Theta(mR) | Even ideal constant-gain sequential levels cost R n/sqrt(m) | Fixed margin per level; incoming complement and simultaneous boundary remain | FAILED for the sequential selector certificate; a simultaneous version is CONDITIONAL |
| 6. Overlapping temporal/spatial code | R repeated control coordinates per donor written simultaneously into R protected rows during one interval | Target D=Theta(mR) with m=n/R | Target T=O(sqrt(nR)), mT=O(n^(3/2)/sqrt(R)) | Needs a finite-ball matrix-norm lower after trace matching, not ranks or separate temporal successes | CONDITIONAL; exact unresolved lemma, not a construction |

Routes 1 and 2 change the order and strength of the public masks; they do
not change probes or repair an illegal continuum bank. Route 3 changes
the spatial capture geometry. Route 4 seeks a different transport
operation. Route 5 changes the organization of the control ball. Route 6
requires simultaneous temporal and spatial coding, rather than R
sequential epochs counted as dimensions.

## Why route 1 wins this run

It has an exact private-row identity at one step and uses the already
reviewed zero-sum reducing space AFTER that step. All long-tail errors
then vanish in the protected read. It preserves the actual inverse lift,
trace correction, common endpoint, front chronology and normalized query.
It removes the old logarithmic restriction without an unproved transfer
matrix. It does not meet the strict linear-dimension cost target.

## Algebra for multiple protected rows without exponential mask loss

Use R balanced Walsh bits on the SAME survivor tuples. During its ONE
capture step use

    g_plus=g_H, g_minus=g_H-.005/R.

These are legal gates (>.994) for every R>=1. Put

    A_R=a(g_plus+g_minus)/2,
    B_R=a(g_plus-g_minus)/2=.0025 a/R.

A stored character containing an earlier bit is mapped exactly to
A_R xi_I+B_R xi_(I xor {e}); both characters stay zero sum. Subsequent
singletons are annihilated by its read. Uniform-high holding gives only
scalar a g_H decay. For R<=n/100, Bernoulli's inequality gives

    A_R^(R-1) >= 1 - R[(1-a)+(1-g_H)+.0025/R] > .987.

Thus survival of old singleton coefficients has no 2^R loss. The NEW
capture coefficient is O(1/R), however, and 2^R equal labels still use
physical space. This is exact mask algebra, not an Rq robust theorem.
The stage-selector proof needs kappa=Omega(R n/sqrt(m)); R writes then
cost Omega(R^2 n sqrt(m)). If D=Theta(mR)=Theta(n), this is
Omega(n^(3/2) R^(3/2)). It misses the target even before extra errors.

In the cohort-local route, xi_f is unchanged by a mask on another
cohort. But a capture also produces a BETWEEN-cohort common component;
a later mask can convert that into a later xi_e. Disjoint physical pair
rows alone do not diagonalize the COMPLETE transfer. Even an optimistic
diagonal model has new-read support suppression 1/sqrt(R) twice: in
capture and in query. Its stage-selector duration has the same R^2 cost.

## Gate-only rotations cannot be lossless

For diagonal 0<=D<=I,

    ||x||^2-||Dx||^2 = sum_i (1-D_i^2)x_i^2.

If the norm is preserved for every x in a space H, then D_i=1 wherever
some H-vector is nonzero. Consequently D is the identity on H. It
cannot implement a nontrivial lossless rotation of H. The fixed cycle
can translate H, but does not supply arbitrary controllable rotations.
This does not refute lossy, compensated or redesigned transport.

## What route 6 actually needs

Take R=ceil(log log n), m=Theta(n/R), K=Theta(m), with fixed small
allocation constants and one source feature. The missing theorem would
construct ONE B^(cKR) section using repeated simultaneous writes in
T=O(n/sqrt(m)), with common traces/endpoint and actual pair distance>.002.
That would give linear dimension and mT=O(n^(3/2)/sqrt(R))=o(n^(3/2)).
The target is NOT a matrix rank or a list of R good histories. It needs
a uniform finite-radius lower on the complete returned gradient vector,
with all R temporal controls sharing that interval. No such lemma is
proved here; none of the previously failed matched/synchronized filters
is asserted to provide it.
