# Age-preserving transport bases after the failed convex merger

2026-10-02. Bounded theory stage. New author-derived lemmas require independent
hostile review. No experiment, architecture or new contraction regime.

**The general arbitrary-aperiodic problem remains OPEN.** The unconditional
positive theorem below covers arbitrary scalar modulation of a fixed non-scalar
gate SHAPE, with arbitrary source features and additional independent-row gates.
It is not an upper bound for arbitrary changing gate ratios. Different
continuous moving-basis encoders are defined and their residuals characterized.
The fixed-anchor/fixed-ridge co-moving version is then falsified as a universal
solution by an admissible single-pulse history. No logarithmic lower follows.

## 1. Review constraints, provenance and unchanged contract

The hostile review of theory/query_weighted_moment_merger_20261001/ verifies
its centered-covariance identity, query-error ledger and state counts. It
rejects mass-weighted convex transport merging and round-robin as a general
solution. Period-1 non-scalar gates already defeat that representation, whereas
the accepted Floquet encoder represents them exactly with quadratic state.

The earlier description of the open problem as a constant-packet ledger target
is superseded. It was a sufficient condition for one representation, not a
reduction of the general problem. Neither that representation nor its scheduling
policy is used below. The reviewed numerical failures are inherited evidence;
they were not rerun or rewritten in this stage.

There is an additional review qualification: the old future-query heredity
equation requires the prefixed transition to belong to the permitted FUTURE
family. The accepted future preactivation box need not include every admissible
PAST step. No such heredity assumption is used here. All accuracy statements use
the actual allowed adjoints and their accepted norm bound.

Use the SAME actual tanh family and all independently differentiated parameters:

    h_t=tanh(R h_(t-1)+W x_t+b), h0=S0=0,
    P=2n^2+n, Z_t=S_t D_theta,
    gamma=c/n, a=1-gamma,
    k=floor(n/2), l=n-k, L=max(1,ceil c),
    d=min(k,floor(n/(4cL))), delta=1/(100n),
    R0=diag(a O,delta I_l), O^d=I, O orthogonal,
    W=I, b=(1/20)*1, ||R||op=a,
    e=||R-R0||op<=4/(10^8 n^2).

O is the accepted Householder-conjugated rotation. Actual input histories stay
in (-1/2,1/2)^n; realized inputs are held fixed in parameter derivatives.

Keep frozen group weights and permitted late scalar-head queries:

    w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b),
    q=1/sqrt(n)*1, beta=max(1,||R||F), epsilon=1/1000,
    ||c_q||<=kappa_Q=a/beta<=2/sqrt(k) for large n.

The accepted transfer uses ACTUAL states, gates and features:

    G_t=diag(1-h_t^2),
    f_t=(w_R h_(t-1),w_W x_t,w_b) in R^p, p=2n+1,
    F_t phi=w_R phi_R h_(t-1)+w_W phi_W x_t+w_b phi_b,
    Zbar_t=G_t R0 Zbar_(t-1)+G_t F_t,
    ||F_t||op<=C<6/5,
    delta_dense=kappa_Q e C/gamma^2
               <=48/(5*10^8 c^2 sqrt(k)).             (1)

Only PAST credit is approximated. Future direct parameter injections are
computed exactly from true current h and the permitted continuation. Forward
prediction is actual, not the surrogate. True h costs n extra coordinates if
not supplied. Public model constants are uncounted; history-dependent bases,
coefficients, gate profiles, traces, clocks and ledgers are counted.

As before, a theorem using this O would initially cover this rotating family,
not every dense R satisfying the same norm gap. General class bounds remain

    Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

## 2. Isolate the easy row without weakening the query contract

The accepted O has O e1=e1 and e1^T O=e1^T. Consequently the physical coordinates
e2,...,ek form an invariant orthogonal subspace. Diagonal gates preserve it too.
Write r=k-1 and O_* for the restriction to that subspace. O_* is orthogonal
and O_*^d=I. This split is public, not learned or detected from a history.

Retain exact SURROGATE eligibilities for e1 and all l source rows. Each needs p
numbers and uses actual full f_t:

    E_1,t=G_t,11 [a E_1,t-1+f_t^T],
    E_source,i,t=G_t,ii [delta E_source,i,t-1+f_t^T].   (2)

Their parameter row groups are disjoint. These updates do not omit R/W/b
features, gate history or dense leakage; (1) transfers to the actual model.

On the remaining block, let Psi in R^(r x p) concatenate the independently
differentiated R/W/b parameter rows. Its feature injection is Psi f_t. The
exact surrogate recurrence there is the linear parameter map

    Zbar_*,t phi=a G_*,t O_* Zbar_*,t-1 phi
                         +G_*,t Psi f_t.             (3)

Every f_t is the actual shared feature tuple of the SAME trajectory. Individual
parameter perturbations are arbitrary when evaluating the linear map, but
histories do not control the parameter columns independently.

## 3. Exact quadratic theorem for a fixed projective gate profile

Assume the remaining actual past gates satisfy

    G_*,t=g_t D, 0<g_t<=1,
    D diagonal, positive, max_i D_ii=1, fixed within a history. (4)

g_t may be arbitrarily aperiodic. D need not commute with O_*. Source gates,
the e1 gate, actual features and allowed future queries are unrestricted.
This is a restriction on gate RATIOS, not an assumption of constant gates.

D can be saved from the first transition as
G_*,1/max_i G_*,1,ii. Its r coordinates are counted. Membership in (4) is not
detected by a discontinuous equality test: at later times always use
g_t=max_i G_*,t,ii. Those formulas extend continuously off (4), where exactness
is not asserted.

Set the history-dependent but then fixed generator and injection basis

    B=a D O_*, B_j=B^j D, j=0,...,r-1,
    det(z I-B)=z^r+sum_(j=0)^(r-1) chi_j z^j.

Save T in R^(r x p), initially zero. T_j denotes row j, and decode

    L_D(T) phi=sum_j B^j D Psi T_j^T.                (5)

Rows T_j are feature coefficient vectors. The basis is implicit in the saved D
and public O_*. No r separate r by r transports are stored. No convex average
of age-dependent transports is taken.

At a new step use

    T'_0=g_t [f_t^T-chi_0 T_(r-1)],
    T'_j=g_t [T_(j-1)-chi_j T_(r-1)], 1<=j<r.        (6)

Cayley-Hamilton proves

    L_D(T')=g_t B L_D(T)+g_t D Psi f_t.               (7)

Induction from zero gives exact equality to (3) for every horizon. All age
weights, including products of the variable scalars, remain in the coefficient
recurrence. In period-1, (5) represents sums of powers of the ACTUAL non-scalar
generator, not powers of the rotation paired with an averaged transport.

Characteristic coefficients are polynomials in B entries, so repeated
eigenvalues or a lower minimal-polynomial degree cause no rank-selection branch.
The positive normalization in (4), update (6) and source updates are continuous
on the admissible domain. A counted public clock initializes D at the first
transition; public-time branches admit continuous extensions between integer
times. Actual tanh gates at fixed n have a positive model-dependent lower bound,
so division has a continuous extension outside the reachable state domain.

### 3.1 Exact count and horizon-uniform error

    K_shape=r p+(l+1)p+r+1
           =n(2n+1)+(k-1)+1
           =2n^2+n+k.                              (8)

The terms are coefficient rows, all exact independent/source traces, saved
profile and clock. Add n for current h if needed. Powers, characteristic
coefficients, decoded gradients and work matrices are recomputed transiently.
No old history is replayed or retained outside these coordinates.

The surrogate is exact, so EVERY actual permitted late gradient has error

    error_T<=delta_dense                            (9)

uniformly in T. For fixed c and sufficiently large n, (9)<epsilon. This is
an O_c(n^2) finite-error theorem for (4), with arbitrary feature/gate variations
inside that class. Its scalar-gate subclass contains the accepted quadratic
lower section, so the restricted class has worst-case Theta_c(n^2).

This extends period-1 to arbitrary scalar modulation of a fixed non-scalar
shape. It DOES NOT cover arbitrary changes of the relative diagonal entries.
Exact-real coordinate conditioning can be poor; no bit or practical numerical
stability bound follows from (8).

### 3.2 Exact one-step delay includes a terminal reset

The review includes histories whose period-1 core ends in an arbitrary reset.
Such a reset is not itself a period-1 gate. It must not be silently assumed
to belong to the permitted future preactivation box either.

There is a causal, counted implementation for every queried prefix T whose
gates at times 1,...,T-1 satisfy (4), with an ARBITRARY admissible gate at T.
Maintain the coefficient T_core for the prefix ending one step earlier, and
keep ONE pending normalized feature tuple f_T (p coordinates). At transition
t, process the previously pending tuple f_(t-1) using the true prior state
h_(t-1), hence its actual gate and scalar, before storing f_t. At t=1 the
core is zero and D is initialized from the first actual gate as above.

At endpoint T the decoder uses the actual last gate explicitly:

    Zhat_*,T phi=a G_*,T O_* L_D(T_core) phi
                            +G_*,T Psi f_T.          (8a)

This is exact for the surrogate under the stated prefix restriction. All
source/e1 traces already include the last transition through (2). Processing
the pending tuple uses counted state, not replay of discarded input history.
There is no detector for a reset or for a final time; the ONE-step delay is
the same at every step. Public initialization is still clock-controlled.

The exact persistent count is

    K_shape,delay=K_shape+p=2n^2+3n+k+1,              (8b)

plus n if h is not supplied. Error (9) is unchanged. Thus the period-1 core
plus final reset used by the hostile review is covered without smuggling a
reset into the allowed future query family. A further arbitrary interior
profile change is not covered by this conditional theorem.

## 4. A genuinely different moving-profile representation

The following continuous algorithm is defined for ALL actual histories, but
its epsilon accuracy is not proved on all of them. It is provided as an explicit
alternative representation, not renamed convex packets.

At each step let

    g_t=max_i G_*,t,ii, D_t=G_*,t/g_t,
    B_t=a D_t O_*, A_t=g_t B_t=a G_*,t O_*,
    B_j,t=B_t^j D_t, L_t=L_(D_t).

Retain only T_(t-1), the previous D_(t-1), exact traces (2), a clock and one
error scalar. Construct the current characteristic companion J_t so that

    L_t(J_t T)=B_t L_t(T).

The prediction and its actual one-step target are

    Tpred=g_t J_t T_(t-1)+g_t e0 f_t^T,
    Y_t=A_t L_(t-1)(T_(t-1))+G_*,t Psi f_t,
    R_t=Y_t-L_t(Tpred)
       =A_t [L_(t-1)-L_t](T_(t-1)).                 (10)

R_t is the basis-INNOVATION residual. It preserves the age-dependent old
coefficients during transport. It is not a mismatch multiplied by an unrelated
sum of old features. Define matrices

    Q_j,t=A_t (B_j,t-1-B_j,t),
    R_t phi=sum_j Q_j,t Psi T_(t-1),j^T.             (11)

### 4.1 Continuous regularized refit, with no discontinuous pivots

Use the reviewed loss weighting, not a changed gradient metric:

    lambda=(1+a)/2,
    W_t=[I-A_t A_t^T/lambda^2]^-1,
    H_ij=tr(B_i,t^T W_t B_j,t),
    b_i=sum_j tr(B_i,t^T W_t Q_j,t) T_(t-1),j.       (12)

W_t is positive definite since ||A_t||<=a<lambda. It is derived from current
counted state; it is NOT an uncounted public history-dependent metric. Select
ANY fixed public xi>0, without searching against outcomes, and set

    Delta=(H+xi I)^-1 b,
    T_t=Tpred+Delta,
    r_t=L_t(Delta)-R_t.                              (13)

H is positive semidefinite. xi>0 ensures continuity even at polynomial-basis
rank degeneracies. Formula (13) minimizes

    ||L_t(Delta)-R_t||_(W_t,F)^2+xi ||Delta||F^2.      (14)

It is an orthogonal/ridge refit of COEFFICIENTS, not a convex average of
transport matrices. It retains a matrix polynomial with a different feature
coefficient for each age mode. In particular,

    ||r_t||_(W_t,F)^2+xi||Delta||F^2
                             <=||R_t||_(W_t,F)^2.  (15)

This local improvement is not a global all-query accuracy guarantee. The
criterion is a positive upper-envelope/error weight. It is not the actual
worst permitted query norm, and not a substituted RMS query contract.

If D_t=D_(t-1), (10) gives R_t=0, b=0, Delta=0 EXACTLY for every xi>0, including
singular H. Thus the refit reduces exactly to (6) on the whole fixed-shape class,
including its period-1 core. Section3.2/4.3 handles a terminal reset separately.
An unanchored ridge fit of Y_t
would instead introduce bias even in that control; that version is not used.

### 4.2 Exact residual covariance and counted state

For clarity put

    C_i=B_i,t, V_i=Delta_i, 0<=i<r,
    C_(r+j)=-Q_j,t, V_(r+j)=T_(t-1),j, 0<=j<r.

The same actual parameter-row layout in (3) gives

    r_t r_t^T=sum_(i,j=0)^(2r-1) (V_i dot V_j) C_i C_j^T. (16)

All cross terms are kept. (16) allows the loss-scaled operator residual

    nu_t^2=lambda_max(W_t^(1/2) r_t r_t^T W_t^(1/2))  (17)

to be evaluated from counted coefficients and the two profiles in transient
workspace, without retaining a full r by r p sensitivity matrix. In this family
W_t is diagonal, since O_* is orthogonal. The parameter group weights are already
in the feature coordinates; they are not adjusted by the refit.

Use the verified ledger

    z0=0, z_t=lambda^2 z_(t-1)+nu_t^2.

Here Zhat_*,t=L_t(T_t) and E_t=Zhat_*,t-Zbar_*,t satisfy

    E_t=A_t E_(t-1)+r_t.

The reviewed adjoint-energy lemma therefore gives, for all T and ALL actual
permitted future queries,

    error_T<=delta_dense+kappa_Q sqrt(z_T).          (18)

The exact persistent count is

    K_moving=r p+(l+1)p+r+2=2n^2+n+k+1,             (19)

plus n if true h is not supplied. The extra coordinate relative to (8) is z.
There are no retained transports, old gates, full tensor, Gram, inverse, or
future adjoint caches. Every profile is counted. Old/new arrays and Gram/matrix
operations are transient workspace within a step; peak workspace and runtime
are not bounded quadratically by (19).

Equation (18) is a correct a posteriori bound, not the general solution. No
uniform small z bound is established. Moment coefficients may be ill-conditioned
or amplify under a changing companion basis; xi ensures continuity, not stable
uniform accuracy. A useful policy/basis may need more than one generator, or a
different algebra altogether. The general problem is NOT reduced to proving
that this particular refit succeeds.

### 4.3 One-step delayed moving refit

The same pending-tuple construction applies to the moving refit: at time t
run (10)--(17) on the previously pending step t-1 using actual h_(t-1), then
store f_t. The core coefficient and profile now describe the prefix t-1;
decode the current memory row block through the exact final map (8a), using
that moving core rather than a fixed D core. Source/e1 traces remain current.

Persistent state costs

    K_moving,delay=K_moving+p=2n^2+3n+k+2,            (19a)

plus n if h is not supplied. The ledger measures core error at T-1. Since
||a G_*,T O_*||<=a, the all-query guarantee is

    error_T<=delta_dense+a kappa_Q sqrt(z_(T-1)).     (19b)

This protects the most recent gate/injection exactly, including an arbitrary
terminal reset. It does not prove a small ledger at earlier changing profiles.
The observed period-1 failure of convex packets is therefore not a failure of
this new representation; no experiments were run to claim more than that
algebraic boundary check.

## 5. Exact current-generator leakage: a commutator obstruction

For a positive current D write B=a D O_*. Any matrix in its injection-power span

    V_D=span{B^j D:0<=j<r}

has the property that M D^-1 is a polynomial in B and therefore commutes with B.
Consider transporting ONE previous injection with previous profile Dold:

    M=B Dold, H=Dold D^-1.

If M belongs to V_D, then B H must commute with B. B is invertible, so

    [B H,B]=B[H,B]=0 implies [H,B]=0,
    [H,B]=a D[H,O_*].                               (20)

Thus a NECESSARY condition for exact inclusion is

    [Dold D^-1,O_*]=0.                              (21)

It is not asserted sufficient when B is noncyclic. The implication uses actual
injection matrices as well as propagation, not only the algebra generated by B.

Take D=I and Dold=I-tau E_ii with 0<tau<1 and [E_ii,O_*]!=0. Then (21) fails.
No reweighting, least-squares solve, vanishing ridge parameter or full degree-r
current-power expansion can represent that transported old injection EXACTLY.
This is more than an inadequate scheduling rule: there is a component outside
the entire chosen current-generator module.

### 5.1 Coupled, admissible fixed-h realization

For sufficiently large n, d>=3 and O_* has order d, so it cannot be a real
diagonal orthogonal matrix. Select the first public coordinate i with
[E_ii,O_*]!=0; this is a deterministic symbolic model constant.

Use the original full physical indices and source coordinate j. Prescribe

    h0=0,
    h1=(0_memory, .3 e_j,source),
    h2=(.3 e_i,memory, 0_source),
    h3=0.

Actual realized inputs are x_t=atanh(h_t)-R h_(t-1)-b. At R0, memory inputs at
step2 are at most atanh(.3)-.05<.26; reset inputs are at most .3+.05=.35.
The source initial input is <.26 and later inputs are at most delta*.3+.05.
Tiny accepted dense leakage preserves the original input cube. The endpoint is
EXACTLY fixed at h=0. Parameter derivatives hold those inputs fixed.

In the selected R_*,source-j block, there is no first-step injection, the
second injection is .3 w_R Dold, and the third has no new injection because
h2,source=0. Its terminal reference transport is therefore .3 w_R a O_* Dold.
The current profile is I. Equation (20) proves that this actual coupled
parameter-block map lies outside V_I. No independent selection of parameter
columns by the history has been assumed.

This is an EXACT representation obstruction, not an epsilon lower bound.
The normalized query margin of this short example is not proved uniform in n;
its uncovered component may be below epsilon. It neither refutes a richer
quadratic encoder nor supplies an Omega(n^2 log n) jointly robust section.

The delayed decoder can postpone this particular terminal rebasing. Appending
one additional zero-state transition makes the same third-step innovation
enter its internal core refit. The lemma concerns exact polynomial-module
closure, not a quantitative failure assertion for that delayed encoder.

## 6. Why a simple moving Floquet gauge does not remove the injection problem

Suppose invertible history-dependent T_t and fixed matrices H,C transform BOTH
the propagation and parameter-row injection to scalar multiples of fixed forms:

    T_t^-1 (a G_t O_*) T_(t-1)=alpha_t H,
    T_t^-1 G_t=beta_t C, alpha_t,beta_t nonzero.       (22)

Since G_t and T_t are invertible, C must be invertible. The second equation
forces T_t=G_t C^-1/beta_t. Substitution into the first gives

    a (beta_t/beta_(t-1)) C O_* G_(t-1) C^-1
                                                  =alpha_t H,
    G_(t-1)=[alpha_t beta_(t-1)/(a beta_t)]
                         O_*^-1 C^-1 H C.           (23)

Every G_(t-1) is therefore a scalar multiple of ONE fixed matrix. In other words,
its projective shape must stay constant. This is exactly the boundary handled
in section3; arbitrary changing ratios cannot satisfy (22).

One can always absorb propagation into a cumulative transport T_t. But then
T_t^-1 G_t becomes a history-dependent full injection operator. Storing those
operators or all their feature correlations is not free. Proving hidden-state
matrix-algebra generation without handling these injections would miss (23).

This lemma does not exclude multiple generators, genuinely moving injection
bases, quotient approximations, rational bases or other continuous encoders.

## 7. Primary proposal: co-moving transport, refit ONLY the fresh injection

This avoids the old-credit rebasing in section4. Its propagation identity is
exact for ALL actual gate histories. Accuracy remains conditional because the
fresh injector need not lie in the transported injection-power module.

Initialize the same saved normalized first profile D and B=a D O_*; B is
invertible. Retain Q0=I_r and coefficient T0=0. At each step compute

    A_t=a G_*,t O_*,
    Qraw=A_t Q_(t-1) B^-1,
    s_t=||Qraw||op>0, Q_t=Qraw/s_t,
    Tprop=s_t J_B T_(t-1).                          (F1)

Decode old credit as Q_t L_D(Tprop). Cayley-Hamilton and (F1) imply

    Q_t L_D(Tprop)=A_t Q_(t-1) L_D(T_(t-1))          (F2)

EXACTLY. This does not average Q, fit old moments or discard any part of the
previous decoded credit. No separate transport for every age is stored. The
input-word order is retained in one co-moving Q; ages are retained in the
feature coefficient recurrence. Matrix inverses of Q are not used by the
encoder.

Q has norm one. Actual gates at fixed n have a positive lower bound g_floor;
therefore s_t>=sigma_min(A_t)/||B||>=g_floor. The normalizer has a continuous
extension off the admissible state domain. Q can approach rank deficiency over
long histories, but neither (F1) nor the refit below divides by its singular
values. The fixed saved D is invertible and counted. Conditioning remains an
accuracy issue, not an uncounted coordinate assumption.

### 7.1 Matrix injection refit, not transport averaging

Let the current implicit operators and reviewed loss weight be

    C_j=Q_t B^j D, j=0,...,r-1,
    W_t=[I-A_t A_t^T/lambda^2]^-1, lambda=(1+a)/2.

First project onto the scalar span of C0:

    ell_t=tr(C0^T W_t G_*,t)/tr(C0^T W_t C0),
    Enew=G_*,t-ell_t C0.

The denominator is positive: C0=Q_t D is nonzero, D has a positive model-dependent
smallest entry and ||Q_t||op=1. This scalar is an unconstrained coefficient,
not a mass, convex weight or changed gradient normalization.

Refit the remaining injector through one fixed public xi>0:

    H_ij=tr(C_i^T W_t C_j), b_i=tr(C_i^T W_t Enew),
    alpha=(H+xi I)^-1 b,
    T_t=Tprop+(ell_t e0+alpha) f_t^T,
    Rnew_t=ell_t C0+sum_j alpha_j C_j-G_*,t.          (F3)

The regularized scalar solve minimizes

    ||sum_j alpha_j C_j-Enew||_(W_t,F)^2+xi||alpha||^2.

It remains continuous at basis rank loss. Its residual satisfies

    ||Rnew_t||_(W_t,F)^2+xi||alpha||^2
                                      <=||Enew||_(W_t,F)^2. (F4)

This is a sufficient-weight fit, not equality to the actual future-query norm.
An average fit score is never substituted for uniform late-query accuracy.

The resulting decoded sensitivity obeys

    Zhat_*,t=A_t Zhat_*,t-1+G_*,t Psi f_t+r_t,
    r_t phi=Rnew_t Psi f_t,
    r_t r_t^T=||f_t||^2 Rnew_t Rnew_t^T.             (F5)

This covariance involves ONLY the current injection feature tuple. No old
moment, full old-credit tensor or old C/gamma mass enters it. All new R/W/b
injections are coupled through the actual f_t; no parameter column is selected
independently by the history. The old moments still matter through the decoded
prediction, but (F2) transports them without approximation.

### 7.2 State count and uniform a posteriori accuracy

Using the verified error ledger, compute transiently

    nu_t=||f_t|| ||W_t^(1/2) Rnew_t||op,
    z_t=lambda^2 z_(t-1)+nu_t^2.

Then EVERY horizon and permitted actual query obeys

    error_T<=delta_dense+kappa_Q sqrt(z_T).          (F6)

The counted persistent coordinates are

    K_comoving=r^2+r p+(l+1)p+r+2
              =n(2n+1)+(k-1)^2+(k-1)+2.             (F7)

These are one Q, feature coefficients, exact row traces, first profile, clock
and ledger. Add n if true h is not supplied. B, B^-1, characteristic coefficients,
C_j, Grams and residual norms are transiently recomputed from COUNTED state.
No old gates, histories, bases or gradients are cached. Runtime and temporary
workspace, including potentially dense output gradients, are not bounded here.

A one-step delayed version, precisely as in section4.3, retains one pending
f_t. It costs

    K_comoving,delay=K_comoving+p
       =n(2n+1)+(k-1)^2+(k-1)+(2n+1)+2,             (F8)

plus current h if necessary, and satisfies

    error_T<=delta_dense+a kappa_Q sqrt(z_(T-1)).     (F9)

It applies the current final gate and fresh injection exactly at the decoder.

If ||W_t^(1/2) Rnew_t||op<=eta_*/C for all t, where
eta_*=(epsilon/2)sqrt(3c/40) and delta_dense<=epsilon/2, the reviewed ledger
gives uniform actual epsilon accuracy. A discounted cumulative bound suffices
more generally. Neither statement is proved to hold for arbitrary histories.
This is an explicit finite-error certificate, not an unconditional universal
upper and not a claim that the general problem reduces to this sufficient test.

### 7.3 Boundary exactness and the injector obstruction

When G_*,t=g_t D for all t, induction gives Q_t=I and s_t=g_t. Then C0=D,
ell_t=g_t, Enew=0, alpha=0 and Rnew=0. Thus (F3) is EXACT on the whole shape
class, including period-1 non-scalar gates and scalar gates with arbitrary
strength changes. The delayed version also handles an arbitrary terminal reset,
with the old core still propagated exactly by (F2). xi creates no bias in this
control, even when H is singular.

There is a useful additional check. At the second step, with initial Q1=I,
Qraw=G_*,2 D^-1. Hence G_*,2=s_2 Q2 D, which the scalar coefficient ell_2 fits
EXACTLY. There is no injection error merely from the first profile change.

For a general later step, exact fresh fitting would require

    G_*,t in span{Q_t B^j D}, or equivalently
    Q_t^-1 G_*,t D^-1 is a polynomial in B.          (F10)

This inverse is a PROOF device only. Invertibility holds at every finite actual
trajectory, but the algorithm does not compute Q^-1.

With initial D=I, G_*,1=I, a noncommuting diagonal second gate G_*,2, and third
gate G_*,3=I, the formulas give, up to a nonzero scalar,

    Q3^-1 G_*,3=O_* G_*,2^-1 O_*^-1.

This does not commute with B=a O_* when [G_*,2,O_*]!=0. Thus (F10) fails: the
entire one-generator injection-power space cannot fit that later injection
exactly. A coupled source feature can be present at that step by prescribing
a bounded source vector at h2 and resetting h3; original input slack is the
same as in section5.1. Bias/W injections are present even without it.

Unlike a current-generator refit, this obstruction does NOT destroy strong
old credit: it creates a new bounded-feature forcing error only. No uniform
epsilon margin or logarithmic lower follows just from nonzero forcing error.
Additional/renewed operator families might fit it. Refreshing a basis must
preserve existing decoded credit, with every factor and coefficient counted;
discarding it or performing a hidden full-tensor refit is not an answer.

The unresolved finite-error theorem is therefore about joint query-visible
injector innovations and basis renewal under arbitrary gates, not convex
transport packet scheduling. Even a successful theorem here would initially
cover the accepted rotating family, not all dense R.

### 7.4 Falsification of this fixed-anchor, fixed-ridge implementation

For clarity, the algorithm (F1)--(F3) with any FIXED public xi>0 is NOT a
universal epsilon encoder. This is a mathematical method counterexample,
not an experiment or a robust-dimensional lower.

Take c=1 and n>=200 divisible by4. Then k=l=n/2, d=n/4 and r=k-1.
Use original physical memory coordinate i=k, and write e_i within the r block.
Set tau=9/100, sigma=2/5 and prescribe

    h1,mem=(3/10)e_i, h1,source=sigma*1_l,
    h_t,mem=0, h_t,source=sigma*1_l, 2<=t<=N,
    h0=h_(N+1)=0.                                   (F11)

The first remaining gate is D=I-tau E_ii (max1). All later remaining gates,
including the final reset, equal I. The actual compensating inputs stay in
the original cube: the first memory input is at most atanh(.3)-.05<.26;
the next/reset memory input is at most .3+.05=.35; source inputs are bounded
by atanh(.4)+delta*.4+.05<.477. Tiny accepted dense leakage preserves this
slack. This is ONE non-scalar event followed by scalar gates, an already
quadratically solvable boundary class. The final hidden state is exactly zero.

The fixed profile saved by the proposed method is D. Put M=D O_*, B=a M.
For every core time t>=1 its normalized co-moving frame is exactly

    Q_t=O_*^(t-1) M^(-(t-1))/b_t,
    b_t=||M^(-(t-1))||op
       >=(1-tau)^(-(t-1)/r).                        (F12)

This follows inductively from (F1). Orthogonality of O_* gives the equality
of norms; the determinant gives the lower bound since |det M|=1-tau.

Let W be ker(I-O_*) intersect e_i^perp and let Pi_W be its orthogonal projector.
Its dimension s is at least k-d-1=n/4-1. Both O_* and D are identity on W and
preserve W^perp, so

    Pi_W Q_t=Q_t Pi_W=Pi_W/b_t,
    Pi_W C_j=a^j Pi_W/b_t.                          (F13)

For t>=2, the current loss matrix is the scalar w I,
w=[1-(a/lambda)^2]^-1. Cauchy--Schwarz in the scalar predictor and
||Q D||F>=1-tau yield |ell_t|<=sqrt(r)/(1-tau). Moreover ||Enew||F<=2sqrt(r),
||C_j||F<=sqrt(r)a^j and (H+xi I)^-1 has norm<=1/xi. Therefore

    ||alpha||<=2 w r/[xi sqrt(1-a^2)],
    |ell_t+sum_j alpha_j a^j|
        <=M0:=sqrt(r)/(1-tau)+2 w r/[xi(1-a^2)].     (F14)

M0 is finite at each fixed n,xi. The effective fresh injector on W is thus
a scalar d_t Pi_W with

    |d_t|<=M0/b_t<=M0 rho^(t-1),
    rho=(1-tau)^(1/r)<1.                            (F15)

It tends to ZERO while the TRUE fresh injector on W is identity. Old credit
is propagated exactly, but the persistent ill-alignment is not repaired.

Inspect the actual R_*,source parameter group. Its first injection is zero
because h0=0. For 2<=t<=N, the source feature is H=sigma*1_l. On W the exact
reference coefficient at N is (1-a^(N-1))/gamma, whereas the encoded coefficient
vhat_N satisfies vhat_t=a vhat_(t-1)+d_t, vhat_1=0. In particular

    |vhat_N|<=M0 sum_(t=2)^N a^(N-t)rho^(t-1) ->0.   (F16)

The sum equals rho*(rho^(N-1)-a^(N-1))/(rho-a) when rho!=a, or
(N-1)a^(N-1) otherwise. Choose a FINITE N so a^(N-1)<=1/4 and the bound
in (F16)<=1/(4gamma). Such N exists for every fixed n and xi. The reference-
minus-encoded coefficient gap is then >=1/(2gamma).

The delayed encoder at final reset applies a O_* to this gap, and includes
the final new injection exactly. That injection is identical in exact and
encoded answers and cannot fix the previous error. Hence the selected raw
parameter-group error has

    Frobenius norm >=sigma sqrt(l) *a/(2gamma)*sqrt(s). (F17)

Here one may project both state and parameter-row axes onto W; other groups
cannot cancel a selected Euclidean gradient group.

Use the accepted realizable one-step future preactivation box [1/4,1/2]^n at
h=0, whose gate half-range s_g>7/100. Averaging squared query norms over its
sign corners gives the already accepted inequality D_box(Y)>=s_g||Y||F/sqrt(n).
Apply it to actual R times the normalized reference-error map divided by beta.
On memory-supported state vectors sigma_min(R|memory)>=a-e; w_R/beta=1/n.
Triangle subtraction of the accepted actual-surrogate query transfer yields

    D_actual >=s_g a(a-e) sigma sqrt(l/n) sqrt(s)/(2 n gamma)
                  -delta_dense
              >.06 >epsilon=.001.                  (F18)

For the last conservative inequality use a,a-e>.99, sqrt(l/n)>.7, sqrt(s)>=7,
s_g>.07 and delta_dense<1e-6. There is no bound on the decoded polynomial norm
hidden in this transfer: the restricted actual R lower singular value is used
before subtracting only the true-surrogate difference. Exact future direct
injections agree and cancel.

Thus even exact old-credit propagation plus a fixed positive ridge cannot be
made universal just by retaining the first generator forever. The frame becomes
bad for NEW credit on undamped stationary directions. The fixed-number-of-events
encoder handles (F11) quadratically, so this failure cannot support a logarithmic
memory lower. Refreshing the first anchor after its pulse would fix this specific
history; choosing when/how to renew under arbitrary histories remains unproved.

The counterexample is specific to the saved first-profile frame and fixed xi.
It does not rule out history-dependent regularization, multiple generators,
adaptive bases, exact eligibility on a larger invariant subspace, or every
continuous encoder with the same coordinate count.

## 8. Conditional near-shape error: its width loss is explicit

For comparison only, keep a fixed saved profile D and g_t=max G_*,t. Run the
exact section3 coefficient updates even on histories satisfying merely

    ||G_*,t-g_t D||op<=eta for every t.              (24)

The shadow sensitivity obeys propagation a g_t D O_* and injection g_t D Psi f_t,
both contractive/bounded. Its norm is <=C/gamma. Difference from (3) has residual

    (G_*,t-g_t D)[a O_* Ztilde_*,t-1+Psi f_t].

Using a+gamma=1 gives residual norm <=eta C/gamma, hence

    error_T<=delta_dense+kappa_Q eta C/gamma^2       (25)

for every horizon and every actual late query. This is a valid uniform theorem
on (24), but a deliberately conservative comparison bound, not the proposed
general solution: it pays the full old-credit norm again.

At gamma=c/n on the hard family, keeping this bound below fixed epsilon needs
eta of order epsilon c^2 n^(-3/2). Arbitrary changing gate ratios are not so
restricted. The profile result cannot be promoted to a universal quadratic upper
by silently assuming adiabatic or almost-periodic histories.

## 9. Representation routes and the remaining quantitative question

1. **Fixed polynomial / rational basis:** constant generator age structure is
   retained. A rational function of the same invertible current generator still
   commutes with it, so the obstruction (20) persists. New poles do not remove
   it unless the representation introduces a genuinely new operator family.
2. **Implicit multiple generators:** a fixed number of saved profiles and their
   power coefficient arrays still costs O(n^2). It can repair some innovations;
   a continuous selection/update and a uniform all-query approximation theorem
   remain unproved. Nothing here prescribes convex transport merging.
3. **Moving least-squares / query-weighted basis:** section4 counts every profile
   and gives the exact residual. Fit quality or an RMS probe score cannot be
   substituted for (18). A loss-weighted Frobenius objective is an upper-envelope
   objective, not equality to the permitted-query metric.
4. **Krylov recurrence:** section3 uses a recurrence in feature COEFFICIENTS, not
   stored age-specific matrices. Outside that class its missing object is the
   noncommuting injection innovation (20), not raw sensitivity rank.
5. **Exact eligibility plus compressed remainder:** (2) protects dangerous physical
   e1/source rows. Arbitrary stationary eigenvectors do not form a diagonal-gate
   invariant space; their full tensors cannot be counted as p-vectors for free.
6. **Factorizations/correlations:** near equality of sampled transports at orbit
   lag d does not bound the operator-feature innovation on all histories. A
   factorization must count its history-dependent factors and retain their
   coupling to every feature tuple, including gate-history variations.

The smallest identified remaining obstruction is a FINITE-ERROR, query-visible
closure theorem for the evolving transport/injection module. It would have to
show that components outside a counted O(n^2) moving representation can be
discarded/aggregated with a horizon-uniform epsilon error on ALL histories.
Exact closure fails for the simplest current-generator module, but that fact
alone supplies neither robust leakage at scale epsilon nor a logarithmic lower.

A potential Omega(n^2 log n) construction must encode independent noncommuting
innovations in ONE jointly robust exact-fixed-h section; all gates/features
must be admissible and coupled. It must survive group-RMS dilution and bounded
queries, with width-independent antipodal margin. The example in section5 has
one short innovation, not logarithmically many jointly robust cohorts. No such
lower construction is obtained. General bounds are unchanged.

## 10. Boundary checks, mathematical status and stop

* Scalar gates: D=I, arbitrary g_t; section3 is exact for every horizon.
* Constant period-1 non-scalar gates: fixed D, fixed g; exact companion feature
  recurrence, including arbitrary source features. The delayed decoder handles
  its terminal reset without averaging age transports.
* Fixed-period gates: the already accepted Floquet encoder remains the boundary
  result; no periodicity is imposed on the general class.
* Finite-event boundary: the saved source proves fixed b total declared events.
  The owner calls a boundary 'bounded-density'; this stage does not infer a new
  per-unit-time density theorem or reinterpret that saved proof. No new result
  below depends on resolving that wording.

Manual checks: frozen parameter-row units and injections; reference split;
companion indexing/initialization; count/continuity; target-minus-prediction
sign; Gram and weighted adjoint layout; positive ridge and zero-innovation
exactness; all covariance cross terms; residual recurrence/ledger scope;
commutator and gauge implications; exact co-moving propagation/normalization;
scalar injector alignment and regularized matrix refit; fresh-feature covariance;
fixed-anchor frame collapse, stable response and normalized-box lower estimate;
delayed decoder counts; actual coupled source history/input slack;
distinction between exact module failure and robust memory lower.

No automated tests, numerical or training experiments, GPU/CUDA or model-server
work. New proofs are not independently verified or machine-certified. Source
hashes are preserved. AGENTS, GAS-0 and historical evidence remain untouched.

Related prior art: Cayley-Hamilton/Floquet realization and weighted least squares
are established mathematics. Dynamical low-rank/model-reduction theory requires
appropriate approximability and error hypotheses; it does not supply the missing
all-history closure theorem here. See Koch--Lubich, Dynamical Low-Rank Approximation,
https://doi.org/10.1137/050639703, and Kieri--Lubich--Walach, Discretized Dynamical
Low-Rank Approximation in the Presence of Small Singular Values,
https://doi.org/10.1137/15M1026791. No external theorem is used as an unverified
shortcut, and no encoder is claimed novel.

**STOP:** arbitrary aperiodic case not solved; no logarithmic lower; no other
gamma regime or architecture work. Review the new representation and its exact
injection leakage before choosing the next proof strategy.
