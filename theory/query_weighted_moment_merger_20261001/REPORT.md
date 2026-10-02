# Uniform aperiodic merger: partial theorem and a repaired method obstruction

2026-10-01. **PARTIAL THEORETICAL ADVANCE — ARBITRARY APERIODIC GATES STILL OPEN.**

New author-derived lemmas require independent hostile review. The accepted
diagnostic and all earlier theory/evidence are preserved. No new experiment.

## Strongest theorem obtained

An explicit continuous, no-replay streaming encoder with m transport/moment
packets has an exact centered merger-error covariance and a horizon-uniform
finite-error ledger. These results account for every gate, feature and history
variation; they are not source-only, tangent or RMS statements.

For a mass-weighted merger, write

    r_t=-(Q1-Q2) M_v,
    v=(1-alpha)f1-alpha f2,
    alpha=mu1/(mu1+mu2).

The parameter-row layout gives, for EVERY actual late query c_q,

    ||r_t^T c_q||^2
       =c_q^T Delta Q K(v) Delta Q^T c_q,
    K(v)=sum_(j,l) (V_j dot V_l) O^(j-l).

Only d cyclic feature autocorrelations determine K. This retains the coupled
transport--feature association. For a separately mass-weighted coherent feature
channel, its stationary component cancels before the transport mismatch acts;
one heterogeneous tuple mass does not automatically cancel every subchannel.
The estimate does not multiply gate damage by the full old-credit norm. When
merging a fresh injection into old credit,

    ||r_t||op<=2 min(mu_old,mu_new)||Delta Q||op<=4C,

independent of old C/gamma mass. This improves that residual estimate, but it
does not by itself give epsilon accuracy after arbitrarily many merges.

## Exact memory count

With k=floor(n/2), l=n-k, d the accepted rotation period and p=2n+1:

    K_m=m[k^2+d p+1]+l p+2.

This includes every Q, feature moment, packet mass, source eligibility, clock
and scalar error ledger. Add n if exact current h is not supplied. Decoded dense
sensitivities and current covariance/eigenvalue evaluations are transient; no
history-dependent matrix/basis is retained for free. Public model constants
are uncounted as agreed. No runtime or finite-precision claim.

For fixed m this is O_c(n^2) persistent coordinates. **Its uniform epsilon
accuracy is conditional, not proved for arbitrary gates.**

## Uniform error bound

Choose public lambda=(1+a)/2=1-gamma/2 and define the loss weighting of the
actual surrogate memory Jacobian A_t=a G_t O. D_t depends on current gates;
it is recomputed from counted state, not retained as a free public constant:

    D_t=diag(sqrt(1-(a/lambda)^2 G_t,ii^2)),
    nu_t^2=lambda_max(
       D_t^-1 Delta Q K(v) Delta Q^T D_t^-1),
    z0=0, z_t=lambda^2 z_(t-1)+nu_t^2.

Then for EVERY horizon and EVERY permitted actual future continuation:

    gradient error <= delta_dense+kappa_Q sqrt(z_T),
    delta_dense <=48/(5*10^8 c^2 sqrt(k)).

This follows by rescaling the actual past adjoint, telescoping its dissipated
energy, then vector Cauchy--Schwarz. No hypothetical future query is stored.
D is an internal proof/error metric; the FINAL gradient epsilon is unchanged.

A sufficient width-independent condition, when delta_dense<=epsilon/2, is

    nu_t <= (epsilon/2)sqrt(3c/40) at every step.

At c=1, this is .0001369306394 in the LOSS-SCALED residual units, not a new
gradient epsilon. A discounted average bound on z suffices more generally.
We have NOT proved that constant m can enforce either bound on all histories.

## A real failure of the simplest merger, and its cheap repair

The accepted rotating reference has an exactly independent physical mode e1.
On the ACTUAL dense model prescribe an exact-fixed-h history with:

* c=1, gamma=1/n unchanged;
* first memory h=1/sqrt(n), hence gate a=1-1/n;
* a strictly varying tiny second-memory coordinate, making gates genuinely
  non-scalar, aperiodic and noncommuting;
* source vector -(.4)*1 early and +(.4)*1 in the last approximately n ln2 steps;
* exact zero endpoint and compensating inputs inside the original cube.

The one-packet shared moments discount source signs by a^age and nearly cancel.
The exact independent-mode credit discounts by a^(2 age) and does not cancel.
The actual permitted uniform one-step future input .45*1 exposes error **>.048**
for n>=200, versus epsilon=.001. This is an analytic method counterexample,
not a numerical witness or a new parameter family. The n^2 prefix length is a
horizon choice; gamma remains 1/n, not 1/n^2.

It refutes the specified one-packet product decoder, not all decoders of that
state and not all quadratic encoders. Exact reference e1 eligibility costs
only p=2n+1 coordinates and fixes this failure at every horizon, up to the
already bounded actual dense transfer.

The resulting hybrid state count is

    K_m,hybrid=m[(k-1)^2+d p+1]+(l+1)p+2,

plus n if h is not supplied. The same error ledger applies to the remaining
block. The larger stationary eigenspace is not closed under arbitrary diagonal
gates, so the one-row repair cannot be copied to every eigenvector for free.

## Is the arbitrary-aperiodic problem solved?

**No.** What is now controlled rigorously is the error of a proposed merge,
including centered feature covariance, an exact independent-mode repair, and
all future query propagation. What remains is the number and policy of merges.

For the hybrid method, the smallest unproved sufficient statement is:

There exists m(c,epsilon) independent of n and horizon, with a continuous causal
merge policy, such that on every admissible actual history

    sup_T z_T <=[(epsilon-delta_dense)/kappa_Q]^2.

The target ledger bound is of order epsilon^2 n on this family. Selected orbit
correlations do not imply it. A naive norm bound supplies only O_c(sqrt(n))
gradient error, which is useless for fixed epsilon as n grows. RMS/probe metrics
do not permit discarding future-visible residuals uniformly.

Future-query invisibility itself is hereditary: prepending an admissible input
maps every later adjoint into the current allowed family, so propagating an
already uniformly invisible residual cannot make it reappear. The unresolved
problem is controlling the accumulated NEW centered merger errors, not a free
amplification of previously discarded uniformly invisible directions.

## Can this support an Omega(n^2 log n) lower?

Not yet. The one-packet failure has an O(n)-coordinate repair. Failing a
sufficient ledger can be conservative, and failure of any packet policy is
not a continuous-memory lower bound. A logarithmic lower still requires one
jointly robust, exact-fixed-h section with independent nonstationary covariance
directions, realizable gates/features and a width-independent margin. No such
section or general obstruction to all quadratic encoders was obtained.

Even a successful hybrid theorem would initially cover the accepted rotating
family. A universal theorem for all dense R needs an additional argument;
the family's public rotation must not be silently imposed on the whole class.

## What was tried, without promoting diagnostics to proof

| Route | Rigorous advance / outcome | Remaining limitation |
|---|---|---|
| Centered transport--feature merger | Exact query covariance, d autocorrelations; full old mass removed from fresh-merge residual estimate | Repeated centered covariance not uniformly bounded |
| Scalar normalization of transport | Continuous bounded Q; arbitrary gates/features included; scalar-memory history merges exactly | Non-scalar associations remain |
| Loss-weighted adjoint energy | Horizon-uniform scalar error ledger with all future queries | Constant packet count satisfying epsilon ledger unproved |
| Common-feature stationary cancellation | Exact annihilation before mismatch, using that channel's mass | Heterogeneous channels do not automatically share it |
| One-packet merger | Explicit real fixed-h failure >.048 | Method-specific, cheaply repaired |
| Independent-mode eligibility hybrid | Exact repair with p counted coordinates | Remaining gated block still noncommuting |
| Approximate future-query quotient | Previously uniformly invisible residuals stay invisible under a common future prefix | No small recursive chart or total merger budget follows |
| Low-rank/sketch/balancing shortcuts | Existing results do not establish the needed deterministic uniform policy | Random/average guarantees, fixed templates or trajectory spectra insufficient |

## Validation, resources and records

New proof steps were manually checked for injection coupling, group weights,
cyclic indexing, covariance sign/factors, PSD, stationary cancellation, mass
positivity, continuous updates, decoder residual recurrence, adjoint rescaling,
telescoping, dense transfer, explicit counterhistory/domain/reset, and counts.
They are author-derived and require independent review; no new automated tests,
formal theorem-prover verification, numerical experiments or certificates.

No meaningful experimental CPU or GPU workload was launched. Ordinary document,
shell and literature-search overhead and RAM are unprofiled. GPU/CUDA unused;
no model server, training, architecture work, gamma=1/n^2 or GAS-0 action.

Files: PROOF.md (complete derivations), REPORT.md, PROVENANCE.json and local
.gitattributes for stable evidence bytes. Only Codex's resume and the shared
state map are updated; historical proofs/results and independent notebooks
are preserved. Existing theory bounds remain

    Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

**Single next step:** independently review the covariance/ledger/counterexample,
then target the continuous bounded-packet ledger theorem on the repaired block.
Do not infer a universal encoder or start architecture work from this partial
result. STOP this theory stage.
