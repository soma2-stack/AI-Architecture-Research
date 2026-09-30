# Endpoint certificate — frozen before official input points

CPU-only, one worker and actual numerical thread1, float64 references. No GAS-0,
training, parameter updates, Stage C, AMS v10 or new architecture. Read Stage A/B/B2
and own/shared state; no standalone Round-5 file found, use owner's self-contained
question. Preserve all old artifacts and unrelated modified files.

## Recurrence and parameters

Width2. h0=0. One dense tanh layer: h_t=tanh(R hprev+W x_t+b), EXACT real tanh.
R=[[7,3],[-4,6]]/16; W=[[8,2],[-1,7]]/16; b=[1,-2]/64.
All10 entries independently differentiated; fixed at these rational values.
Uses the SAME smooth recurrence as B2, rational initialization for certification,
not a polynomial substitute. Continuous input space; witness points are seeded
integers uniformly[-8,8]/16 (grid only selects points, doesn't restrict derivative domain).
Official seeds9502100–04, development9501900. Input RNG NumPy PCG64(seed).
Full endpoint F=(h,vec(Dtheta h)); all20 entries can structurally be nonzero.
Dimension22, input width2, FIRST count-feasible horizon11. No shorter full-rank test.

Independent control: R=diag(3/10,9/20), same W/b;8 parameters; only8 S entries
structurally nonzero, so endpoint10; T5. Compact local rule exact by block ownership.
Shared-linear control: replace tanh by identity, both diagonal entries7/20, still
independently differentiated. Same8 parameters/support, endpoint10, T5.
Exact factors ex=sum gamma^(T-t)x_t, eh=sum gamma^(T-t)hprev, eb=sum gamma^i.
S_W=I tensor ex; S_R=diag(eh); S_b=eb I; h=W ex+b eb. At fixed T, eb constant,
so F is an affine function of4 input-dependent scalars (ex,eh). Rank<=4 exactly.
This control must not be classified as full10-dimensional.

If the single dense case has a RIGOROUS full22 minor, additionally test two dense
layers. Second R=[[6,-3],[2,7]]/16; W=[[7,-2],[3,8]]/16;b=[-1,1]/64.
Layer2 input=tanh(current layer1 h), as in B2. N4,P20,structurally supported S60;
lower-state/upper-param20 coordinates always zero. Endpoint64; T32 FIRST feasible.
E=within-layer full local sensitivities40 coordinates, h4 =>44; C=upper state
derivative w.r.t lower params20 =>64. E for each dense module is exact block-local
eligibility, not a claim of scalar-diagonal trace state. Compare base44 and full64
at SAME input; certify base/full minors if possible. No width3 or broad sweep.

## Derivatives and validity

Analytic forward mixed jets maintain h, S=Dtheta h, H=DX h, K=DX S. Multiplying a
parameter p by a state z: S=p S_z+e_p z; H=p H_z; K=p K_z+e_p H_z.
For phi=tanh: S=phi' S_z; H=phi' H_z;
K=phi' K_z+phi'' outer(S_z,H_z); phi'=1-h²,phi''=-2h phi'.
No theta optimization. Independent autograd obtains S via full frozen unroll and
J via mixed automatic differentiation; compare forward states, S and J on development
cases, then official S/J comparisons before interpreting rank. Degenerate gradients
use absolute1e-11; nondegenerate relative1e-8; Jacobian relative1e-10.
No NaN/Inf, CPU-only, parameter hashes/inputs preserved. Implementation bugs may
be repaired with affected measurements marked; no threshold tuning.

## Certification (not an ordinary float SVD)

Float64 spectra at five cutoffs, then80/160-decimal mixed jets. For square full
endpoint J use all columns; for base44 choose44 columns by deterministic pivoted
QR; verify THAT specific minor at high precision, save determinant/inverse.
Try rational dyadic interval arithmetic at256/512/768 bits, outward rounded using
Python integers. Exact rational inputs/parameters enclosed. Exponential endpoint
bounds use Taylor series of positive argument plus rigorous geometric remainder;
tanh=(exp(2z)-1)/(exp(2z)+1). Negative exp uses reciprocal. All enclosure operations
are integer floor/ceiling; no floating-point/transcendental assumption in verifier.
Require |2z|<=4, Taylor order bits+32, remainder bound
next_term/(1-x/(order+2)) for nonnegative x<=4. This is conservative and rigorous.

Rational dyadic approximate inverse M from high-precision point calculation is
only a preconditioner. Compute interval R=I-M*Jminor; if certified infinity norm<1,
Neumann series proves M*Jminor invertible, hence the selected maximal minor NONZERO.
Save all rational witness inputs/parameters, interval bounds, preconditioner integer
entries, precision, residual bound, and rerun independent certificate verifier.
High-precision determinant alone is not proof. Include rational polynomial/linear
matrix determinant unit controls, not substitute main recurrence. mpmath interval
support is experimental (official contexts documentation); avoid relying on it for
rigor. Numerical mpmath is ONLY for comparison and preconditioning.

## Sampling / stopping

All two controls at seed0, then dense official seeds in order. Stop dense point hunt
after first certified22 witness (existence goal); try deeper same seed and then next
seeds if needed. Maximum five points per case, only frozen horizons. At each point
progressive precisions; stop precision escalation on first rigorous success. No
post-result horizon/parameter adjustment. If no dense full witness, do not run deep.
Could be insufficient horizon/nonlinear invariant or numerical conditioning; don't
infer compressibility from failure. Budget1800 CPU-s including tests/imports/failed
attempts/verification/analysis; stop starting expensive jobs with90s reserve. RSS1GiB,
available RAM>=4GiB/disk>=2GiB. Whole-process CPU/RSS metered, no hidden parallel jobs.

Classification FULL-DIMENSION WITNESS FOUND ONLY when real tanh interacting full
endpoint minor rigorously certified. STRUCTURAL RANK CEILING FOUND only if an
actual invariant for the PRIMARY dense case is established, not merely a control
invariant. Otherwise INCONCLUSIVE. Deep success/failure reported separately.
No claim of universal lower bound, asymptotic scaling, utility of exact gradients,
new architecture or Stage-C authorization. Stop after this experiment.
