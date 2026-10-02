# Age-preserving transport representation: partial theoretical advance

2026-10-02. **GENERAL ARBITRARY APERIODIC CASE STILL OPEN.**

The convex merger is rejected as a general representation. Its verified
covariance identity, error ledger and counts remain preserved. The earlier
constant-packet target is not a reduction of the general problem. New proofs
below are author-derived and need independent hostile review.

## 1. Strongest theorem obtained

For the accepted rotating/dense family at gamma=c/n and epsilon=1e-3, arbitrary
scalar modulation of a FIXED NON-SCALAR gate profile has an exact quadratic
surrogate encoder, hence uniformly epsilon-correct actual gradient answers at
sufficiently large n. Gate strengths, source histories, source gates and the
protected independent-row gate may vary arbitrarily and aperiodically.

On the remaining memory block let

    r=k-1, k=floor(n/2), l=n-k, p=2n+1,
    G_*,t=g_t D, max(D)=1, D positive diagonal,
    B=a D O_*, a=1-c/n.

Store feature coefficients T in R^(r x p), representing

    L_D(T) phi=sum_(j=0)^(r-1) B^j D Psi T_j^T.

The characteristic-polynomial recurrence advances EACH age mode and adds the
actual current feature tuple. It does not average transports. This is exact
for every horizon under the profile restriction. Its actual late-query error is

    delta_dense <=48/(5*10^8 c^2 sqrt(k)).

The one-step delayed implementation also handles an arbitrary terminal gate,
including the hostile review's final reset, without assuming that reset is a
permitted future query. Its exact persistent count is

    K_shape,delay=2n^2+3n+k+1,

plus n if true current h is not supplied. The undisplaced core count is
2n^2+n+k. The restricted shape class contains the accepted quadratic lower
section, so its arbitrary-horizon worst-case scaling is Theta_c(n^2).

**This is a restricted-class theorem, not the universal arbitrary-gate upper.**
Changing relative gate entries is not scalar modulation of one shape.

## 2. Primary general representation: co-moving frame plus forcing refit

The examined general proposal retains ONE co-moving transport Q, ONE saved first
profile D, a fixed-in-that-history generator B=a D O_*, and its age coefficient
matrix T. It never convexly averages Q or rebases old feature coefficients onto
the current generator. At each new transition:

    Qraw=A_t Qprev B^-1, s=||Qraw||op, Q=Qraw/s,
    Tprop=s J_B Tprev, A_t=a G_*,t O_*.

This transports ALL previously decoded credit exactly:

    Q L_D(Tprop)=A_t Qprev L_D(Tprev).

Only the FRESH injector G_*,t is fitted into the basis

    C_j=Q B^j D.

A scalar aligned predictor followed by a continuous regularized matrix
least-squares correction produces coefficients ell, alpha and residual

    Rnew=ell C0+sum_j alpha_j C_j-G_*,t,
    T=Tprop+(ell e0+alpha) f_t^T,
    f_t=(w_R h_(t-1),w_W x_t,w_b).

Unlike the convex packet merger, old-credit errors are not introduced by
scheduling or averaging. The fresh sensitivity error is exactly

    r_t phi=Rnew_t Psi f_t,
    r_t r_t^T=||f_t||^2 Rnew_t Rnew_t^T.

Thus the error covariance has no factor involving the full old-credit mass
or old moment coefficients. All gate-history variation still enters Q, A_t
and the injector. Rank loss is handled continuously by fixed positive ridge
regularization; neither an inverse of Q nor a hard basis-selection pivot is used.

## 3. Exact count and uniform error formula

With one-step delay, the general representation stores

    K_comoving,delay
      =n(2n+1)+(k-1)^2+(k-1)+(2n+1)+2.

The terms include coefficient arrays and exact row traces, Q, saved profile,
the pending feature tuple, clock and scalar error ledger. Add n for current h
when it is not supplied. Public constants are uncounted; every history-dependent
persistent coordinate is counted. Temporary decoder/Gram operations are not
persistent memory. No runtime, finite-bit or numerical stability theorem.

Use the verified ledger with

    lambda=1-gamma/2,
    W_t=[I-A_t A_t^T/lambda^2]^-1,
    nu_t=||f_t|| ||W_t^(1/2) Rnew_t||op,
    z_t=lambda^2 z_(t-1)+nu_t^2.

Every actual permitted late query satisfies

    error_T <=delta_dense+a kappa_Q sqrt(z_(T-1)).

This is horizon-uniform as an a posteriori certificate. A small uniform ledger
is NOT established for all histories. The final epsilon and group-RMS/query
units are unchanged; least-squares weights are internal error envelopes, not
a substituted average query metric.

## 4. Why the period-1 counterexample is handled

For G_t=g_t D, induction gives Q=I. The aligned injector coefficient is exactly
ell=g_t; the correction and forcing residual are zero. This includes constant
period-1 non-scalar gates with arbitrary source features, and arbitrary scalar
modulation of that profile. A terminal reset is applied exactly by the delayed
decoder. The old strong credit remains intact rather than being convexly mixed.

The co-moving version also fits the first change of gate profile exactly:
after that change G_t=s Q D. Its scalar predictor reproduces this injector
without ridge bias. This is a mathematical boundary check, not a numerical run.

## 5. Obstructions found

### Current-generator-only basis

An old injector transported into the current powers has a necessary inclusion
condition

    [Dold Dcurrent^-1,O_*]=0.

A realizable coordinate gate change violates this. Even all powers up to the
full characteristic degree cannot represent that exact old injection. This
motivates carrying old transport rather than repeatedly changing its basis.

### Co-moving forcing basis

Exact fresh fitting requires

    Q_t^-1 G_t D^-1 to be a polynomial in B.

It already fails algebraically on a three-step scalar/noncommuting/scalar gate
sequence. The co-moving method preserves the old decoded credit in that case;
the unresolved error is in the new forcing. A nonzero forcing residual does
not establish a width-independent epsilon failure or a logarithmic lower.

### Simple moving-Floquet gauge

If one invertible change of coordinates simultaneously makes propagation AND
the parameter-row injector scalar multiples of fixed matrices, the gate shape
must be constant. Absorbing propagation alone into a cumulative matrix leaves
a history-dependent injector. Ignoring it would drop the actual coupled
parameter-sensitivity injections.

### Fixed-anchor implementation: analytically rejected as a general solution

A single initial non-scalar pulse, followed by scalar gates and a final reset,
defeats the specified fixed-anchor/fixed-positive-ridge implementation. Its
co-moving Q increasingly suppresses at least n/4-1 undamped stationary modes.
Old credit is transported exactly, but new credit on those modes is fitted with
coefficients tending to zero. The true accumulated new credit tends to 1/gamma.

For c=1, n>=200 divisible by4, every fixed public xi>0 admits a finite horizon
where an actual permitted query has error **>.06**, at unchanged epsilon=.001.
The proof includes determinant-based frame-collapse bounds, bounded refit
coefficients, the exact fixed-h/input construction and group-RMS/query transfer.
No numerical execution or favorable rank threshold is used.

This is a representation/renewal failure. The already accepted finite-event
encoder handles the same history in O(n^2). It does not imply a logarithmic
memory lower or exclude adaptive frames/history-dependent regularization.

## 6. Is arbitrary aperiodic gating solved?

**No.** The universal propagation/forcing identities and counts are rigorous
derivations. The examined fixed-anchor accuracy claim is falsified as general;
only the restricted fixed-shape theorem is unconditional.

The smallest remaining obstruction is a query-visible, finite-error basis-
renewal theorem: when new injections leave the transported power module, can
we introduce/refresh operator directions while retaining old observable credit,
using only O(n^2) counted state and a horizon-uniform error budget?

The ledger is only one sufficient certificate; the general problem is not
reduced to this particular frame, fit or scalar bound. Nearly singular Q and
companion-coordinate conditioning may make the fit poor. A richer algebra can
still beat this representation. Any actual dense-class theorem needs an
additional extension beyond the accepted rotating family.

No Omega(n^2 log n) section was obtained. Such a lower would require ONE jointly
robust exact-fixed-h family of independent gate/feature innovations, not ranks
or failures from incompatible histories. Group-RMS dilution, contraction and
coupled injections remain crucial. Existing general bounds are unchanged.

## 7. Boundary/provenance notes and next step

Fixed-period Floquet and the saved fixed-number-of-declared-events encoders are
preserved as accepted boundary cases. The owner calls an event boundary
'bounded-density'; the available proof states fixed b total declared events.
This stage does not expand that theorem to an unbounded event count at fixed
per-unit-time density, and the new lemmas do not depend on that wording.

The review also restricts earlier future-query heredity to actually permitted
future transitions. This stage makes no arbitrary-past-prefix heredity claim.
All-query norm/error estimates use the accepted adjoint envelope directly.

Manual algebra, units, coupling, initialization, counts, continuity, frame
normalization, weighted matrix fitting, covariance, delayed decoder and input-
domain checks only. No automated tests, numerical experiments, GPU/CUDA,
training or model-server work. Administrative CPU/wall overhead and RAM are
unprofiled. Historical proofs/results, the review, AGENTS and GAS-0 untouched.

Sources and manuscript hashes: PROVENANCE.json. Full derivations: PROOF.md.

**Single next step:** independent hostile review of the co-moving forcing-refit
identity/counts and the fixed-shape theorem before pursuing a query-weighted
basis-renewal theorem. Stop this stage; no architecture or gamma=1/n^2 work.
