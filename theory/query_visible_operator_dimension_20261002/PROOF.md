# Query-visible operator dimension at gamma=c/n

2026-10-02. Bounded theoretical attempt. **GENERAL CASE UNRESOLVED.**
New author-derived lemmas require independent hostile review. No numerical
experiment, training, architecture or other contraction regime is started.

The strongest result here is a finite-error metric obstruction: the accepted
query norm does NOT, by normalization alone, collapse the natural accumulated
operator envelope to O(r) directions. It supports r^2 robust coordinates on an
AMBIENT operator ball at c=1. No admissible history lift of that ball is proved.
Consequently this is NOT a new recurrent-memory lower bound.

## 1. Authoritative review constraints

The owner accepts theory/claude_transport_basis_review_20261002/REVIEW.md.
Preserve the fixed-profile Theta_c(n^2) theorem, exact co-moving identities,
counts, fixed-anchor counterexample and exact period-1 control. Its ordinary
aperiodic stress results show fresh misfit .66--1.0 and normalized query errors
about .10--.13. Neither a constant number of those frames nor frequent renewal
has a proved universal accuracy guarantee.

Basis renewal is NOT adopted as a reduction of the general problem. Convex
packet merging, round-robin, the fixed-anchor fit and their error-ledger targets
are not the principal representation in this stage. Old files are unchanged.
The source-history tangent diagnostic is motivation, not a finite-error theorem.

General accepted bounds remain

    Omega_c(n^2) <= d_rob(n,epsilon) <= O_c(n^2 log n).

## 2. Frozen actual model, reference, parameters and units

Use exactly the accepted rotating/dense family:

    h_t=tanh(R h_(t-1)+x_t+b), h0=0,
    theta=(R,W,b), W=I, b=(1/20)1,
    P=2n^2+n, gamma=c/n, a=1-gamma,
    k=floor(n/2), l=n-k, r=k-1, p=2n+1,
    L=max(1,ceil c), d=min(k,floor(n/(4cL))),
    R0=diag(a O,delta I_l), delta=1/(100n),
    O=U(P_d direct_sum I_(k-d))U^T, O^d=I,
    ||R||op=a, e=||R-R0||op<=4/(10^8 n^2).

U is the frozen Householder matrix. O fixes e1; its restriction O_* to
physical coordinates e2,...,ek is orthogonal of dimension r. Let E embed
that block into the n actual state coordinates. Thus

    ||R E v|| >=(a-e)||v||.

R is the already defined fully dense parameter value, not a new chosen
matrix. Every entry of R,W,b is independently differentiated. Inputs remain
in (-1/2,1/2)^n; parameter derivatives hold realized inputs fixed.

Frozen normalization and future family:

    w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b),
    Z=S D_theta, beta=max(1,||R||F), q=1/sqrt(n)1,
    epsilon=1/1000,
    C_0={all permitted effective late adjoints from h=0},
    sup_(c_q in C_0)||c_q||<=kappa_Q=a/beta<=2/sqrt(k).

At sufficiently large n beta=||R||F, hence w_R/beta=1/n EXACTLY.
The one-step input box v_i in [1/5,9/20] is permitted at h=0. It yields

    c_q(g)=R^T g/(beta sqrt(n)),
    g_i in [g_lo,g_hi],
    g_hi=sech^2(1/4), g_lo=sech^2(1/2),
    g_mid=(g_hi+g_lo)/2, s_g=(g_hi-g_lo)/2>7/100.

These inputs are an accepted subset; arbitrary unit adjoints are not substituted.
Longer allowed continuations remain in C_0. Future direct injections cancel
between actual histories at the same h and are computed exactly by a decoder.

The accepted all-history surrogate uses ACTUAL hidden states, features and gates:

    G_t=diag(1-h_t^2),
    f_t=(w_R h_(t-1),w_W x_t,w_b), ||f_t||<=C<6/5,
    Zbar_t=G_t R0 Zbar_(t-1)+G_t F_t,
    F_t Phi=Phi f_t in each independently differentiated parameter-row block.

Its actual late-query error is uniformly at most

    delta_dense=kappa_Q e C/gamma^2
               <=48/(5*10^8 c^2 sqrt(k)).             (1)

No approximation to the actual forward state or future dynamics is introduced.

## 3. A precise physical operator norm

For T in R^(r x r), define

    nu_0(T)=sup_(c_q in C_0)||T^T E^T c_q||_2.        (2)

This is the effect of T on the allowed adjoints. It uses their actual scale,
not unit-normalized adjoints. For a fixed nonzero raw source feature H in R^l,
consider the TRUE coupled parameter action

    K -> E T K H, K=delta R_remaining,source.

The normalized queried gradient in this selected parameter group is

    w_R (T^T E^T c_q) H^T.

Consequently its exact all-query norm is

    nu_H(T)=w_R ||H|| nu_0(T).                      (3)

H is a SHARED feature vector; parameter columns are not separately chosen by
the history. Equations (2)--(3) are operator norms on differences, not raw
matrix ranks. An algebraic operator collection needs a declared coefficient
budget before its nu-norm approximation implies a gradient-error statement.

### 3.1 Exact one-step box norm and quantitative equivalence

For (3), define Y=R E T. Then

    nu_H,box(T)=||H||/(n sqrt(n))
                    max_(g in [g_lo,g_hi]^n)||Y^T g||.

The squared Euclidean norm of Y^T g is convex in g, so its maximum on the
box is attained at a corner. Average the squared values at
g=g_mid 1+s_g s with independent uniform signs s_i. Since E[s]=0 and
E[ss^T]=I,

    E_s ||Y^T(g_mid 1+s_g s)||^2
        =g_mid^2||Y^T 1||^2+s_g^2||Y||F^2.

The maximum dominates this average. Also ||R E T||F>=(a-e)||T||F.
Together with the full-query adjoint envelope:

    lambda_H ||T||F <=nu_H,box(T)<=nu_H(T)
                                      <=Lambda_H ||T||op,             (4)
    lambda_H=s_g(a-e)||H||/(n sqrt(n)),
    Lambda_H=a||H||/n.

For H=sigma 1_l, sigma=2/5, lambda_H is Theta_c(1/n) and
Lambda_H is Theta_c(1/sqrt(n)). Neither coefficient is silently rescaled.
The full norm can be sharper than the box lower; longer futures cannot
invalidate the lower. The upper covers ALL permitted futures.

In particular the EXACT query-invisible operator space is {0}. The finite-
error question is the width/entropy of a BOUNDED reachable set in this norm;
an exact quotient of dimension O(r) does not exist. This is just the
operator-level consequence of the accepted query contract, not a new proof
of exact recurrent observability.

### 3.2 Query-average spectra are not uniform query spectra

The corner average above corresponds to the positive state weight

    V_box=R^T[g_mid^2 11^T+s_g^2 I]R/(beta^2 n).

For an operator T, the root-mean-square queried norm is

    w_R||H|| ||V_box^(1/2) E T||F <=nu_H(T).          (5)

This is a valid LOWER diagnostic; it is not equality to the maximum query
norm. Optimizing this average and treating it as a uniform error upper
would repeat the earlier proxy/contract mistake. The sign corners are
allowed queries, not extra information supplied to the learner.

## 4. Query-visible approximation dimension: three different objects

For a compact operator set K and physical accuracy eta, define its linear
query width and epsilon dimension by

    w_q^Q(K)=inf_(dim V<=q) sup_(T in K) inf_(B in V) nu_H(T-B),
    q_Q(K,eta)=min{q: w_q^Q(K)<=eta}.                (6)

This is the usual Kolmogorov-width construction in the SPECIFIED query norm.
It measures approximation directions, not parameter-space rank. For a local
patch apply it to K-M0; a history-dependent center M0 must also be counted.
Linear widths themselves are not translation invariant. Distinguish:

1. A public V approximating the UNION over all histories.
2. A history-dependent V(X) approximating the transports in one history.
3. A continuous finite-error same-endpoint sensitivity SECTION which imposes
   a lower bound on arbitrary continuous encoders.

These have different quantifiers. A history-dependent subspace itself is
not free. q arbitrary dense basis operators would cost q r^2 coordinates,
before feature coefficients. Even q=O(r) does not give a quadratic encoder
unless the basis is public or has O(r^2) total counted continuous structure.

Nor does q_Q lower bound all nonlinear encoders: (6) concerns linear operator
approximation. A true continuous-state lower needs a jointly robust section,
not a statement that many matrices across incompatible histories span a space.

For reference, the standard width terminology is described in Pinkus,
*n-Widths in Approximation Theory*, Springer, 1985,
https://doi.org/10.1007/978-3-642-69894-1 . No external width theorem is needed
for the elementary perpendicular-subspace proof below.

### 4.1 Coupled-kernel dimension versus aggregate-operator dimension

For a single real history X, let q_joint(X,e) be the least dimension of a
subspace V for which one can choose Qhat_s in V whose error E_X in (11)
is at most e. This is a finite-error, feature-coupled pointwise existence
quantity. The V and Qhat can depend on the whole history in this definition;
their online realization and count are separate requirements.

There is in fact an exact O(r) pointwise aggregate representation already:

    M_j,T=sum_s f_(s,j) Q_(T,s), j=1,...,p,
    Zbar_*,T Phi=sum_(j=1)^p M_j,T Phi e_j,
    M_j,t=A_t M_j,t-1+f_(t,j) G_*,t.                (6a)

Each e_j is one of the p FEATURE coordinates of Phi, not a freely selectable
column injected by the history. Each f_(t,j) is its actual normalized feature.
Equation (6a) follows by regrouping the exact coupled injection Phi f_t.
The updates are continuous and exact for every horizon and every gate history;
all permitted query answers are exact for the surrogate. Error is delta_dense
after actual transfer. No linear-rank diagnostic is needed for this identity.

The span of the p matrices M_j has at most p=2n+1=O(r) operator directions.
It can also reproduce the coupled kernels with zero error: write F for the
p by T matrix of actual features. Vectorized aggregates equal Qmat F^T.
Take Qhatmat=Mmat(FF^T)^dagger F. Then

    Qhatmat F^T=Mmat(FF^T)^dagger FF^T=Mmat,

because Mmat=Qmat F^T vanishes on ker(F^T). All columns of Qhatmat are
combinations of the p M_j. Hence q_joint(X,0)<=p for EVERY real history.
The pseudoinverse is only an existence argument, not an online update or a
continuous basis-selection claim. Formula (6a) itself is the continuous update.

Count all of those matrices: p r^2 coordinates, plus the (l+1)p exact row
traces from the frozen protected/source split, and current h if not supplied.
This is Theta(n^3) credit state, an arrangement of exact reference RTRL, not
a new small encoder. Dense M_j are history-dependent and cannot be made free.

Thus an O(r) statement for q_joint is TRUE, but insufficient and already has
an expensive exact realization. It does not say the INDIVIDUAL transport
collection has small width, and it does not imply an O(n^2) encoder. The
nontrivial positive target must also control the finite-error structured
description of those operators (or another full encoding) with all state counted.

## 5. Normalization alone cannot hide a quadratic accumulated-operator ball

Here is the principal finite-radius theorem. Its domain is an AMBIENT envelope,
NOT a proved reachable set of histories. This limitation is part of the claim.

Take c=1, n sufficiently large, H=(2/5)1_l and

    K_env={M in R^(r x r): ||M||F<=R_env},
    R_env=n/4.

This ball lies inside the generic accumulated-transport norm allowance
||M||op<=1/gamma=n, because ||M||op<=||M||F<=n/4.
An allowance is not reachability: real gate products and injections need
not attain these independent coordinates.

### 5.1 Width lower in the actual query norm

If V has dimension q<r^2, choose a Frobenius-unit matrix N perpendicular
to V. For M=R_env N and every B in V,

    ||M-B||F^2=R_env^2+||B||F^2>=R_env^2.

Equation (4) gives

    w_q^Q(K_env)>=lambda_H R_env
        =s_g(a-e)(2/5)sqrt(l/n)/4.                 (7)

For a-e>.99 and sqrt(l/n)>.7, (7) is strictly greater than

    (.07)(.99)(.4)(.7)/4=.004851.                  (8)

Thus q_Q(K_env,1e-3)=r^2. This is FINITE error at the unchanged metric,
not infinitesimal rank or Frobenius-rank inference. At general c the same
choice R_env=n/(4c) gives .004851/c; no claim at epsilon1e-3 is made when
that lower margin is insufficient. The concrete negative calibration c=1
is already within the accepted class and diagnostic setting.

### 5.2 Continuous-coordinate consequence for this AMBIENT domain only

On the boundary of the r^2-dimensional ball, every antipodal pair satisfies

    nu_H(M-(-M))>=2lambda_H R_env>2epsilon.

A continuous encoding of THIS ABSTRACT BALL into fewer than r^2 coordinates
identifies some antipodes by the accepted Borsuk-Ulam argument. A decoder
answering every query with epsilon error would give a contradiction.
Therefore this abstract problem needs at least r^2 continuous coordinates.

THIS DOES NOT YIELD A NEW RNN LOWER BOUND. It becomes such a bound only if
one constructs a continuous admissible-history section at one actual endpoint
whose FULL sensitivity queries realize the ball with the stated margins.
An arbitrary algebraic span, an operator-norm bound, or the exact accessibility
theorem does not supply that finite radius. Actual injections outside the
chosen block and dense leakage must also be accounted for in such a lift.

### 5.3 Finite packing, not just a dimension argument

Let delta=3epsilon/lambda_H. A maximal delta-separated packing of K_env in
Frobenius norm covers that ball by delta balls. Volume comparison gives

    N >=max(1,(R_env/delta)^(r^2)).

Every distinct pair is query-separated by at least3epsilon>2epsilon.
For the constants in (8), R_env/delta>.004851/.003>1.617, so the abstract
domain has at least1.617^(r^2) distinguishable states. This illustrates a
finite-error obstruction to a METRIC-ONLY O(r) assertion; it is not a bit or
memory bound for actual reachable histories. The volume argument uses a
compact finite-dimensional ball, so a finite maximal packing exists.

## 6. A single weak transport is not a weak accumulated history

For each actual remaining-block packet

    Q_(T,s)=A_T ... A_(s+1) G_*,s,
    A_t=a G_*,t O_*,

we have ||Q_(T,s)||op<=a^(T-s). In the selected constant-feature norm:

    nu_H(Q_(T,s))<=Lambda_H a^(T-s)
                         <=(2/5)/sqrt(n).           (9)

For n>=160000, each single packet is epsilon-small, even at age zero.
It would be wrong to conclude that their sum is safely discarded.

### 6.1 One actual admissible fixed-h control demonstrates accumulation

Fix c=1, N=ceil(n), sigma=2/5. Prescribe

    h_t=(0_k,H), H=sigma1_l, 1<=t<=N+1,
    h0=h_(N+2)=0,
    x_t=atanh(h_t)-R h_(t-1)-b.

As in the frozen lower/pulse constructions, source inputs have magnitude
<.477 plus the vanishing dense perturbation; memory inputs have the same
strict slack. This is an actual trajectory, with frozen realized
inputs for derivatives and exact final h=0. The memory gates are all I.

In the selected block K=deltaR_remaining,source, there are N+1 constant
feature injections (transitions2,...,N+2). The reference aggregate is

    M=sum_(j=0)^N a^j O_*^j.

Let Pi_* be its stationary projector. At c=1,n divisible4, d=n/4 and
rank Pi_*=k-d>=n/4. Write m_N=(1-a^(N+1))/gamma>3n/5. Then

    ||M||F >=m_N sqrt(rank Pi_*).

The actual adjoint acting on this reference aggregate therefore obeys

    nu_H(M)>s_g(a-e)sigma sqrt(l/n)(3/5)sqrt(n/4).

For large n, using the same conservative constants, this exceeds

    .0058 sqrt(n).                                 (10)

Transfer from the true surrogate using (1) only subtracts delta_dense.
Discarding the whole selected past block gives an actual error at least
the bound in (10) minus that transfer; future direct R injection is zero
at h=0. Each individual packet nevertheless satisfies (9).

This is a real finite-error control, not a claim of r^2 new independent
directions. Its gates are scalar and the accepted quadratic encoder already
handles it. It only proves why a per-operator error criterion with no joint
coefficient budget is inadequate.

## 7. The correct joint transport criterion and what is actually bounded

On the remaining reference block, concatenate the normalized independently
differentiated parameter rows into Phi in R^(r x p). EXACT past credit is

    Zbar_*,T Phi=sum_(s=1)^T Q_(T,s) Phi f_s.

For any approximate kernel collection Qhat_(T,s), the all-query error is

    E_X(Qhat)=sup_(c_q in C_0)
        ||sum_s (Q_(T,s)-Qhat_(T,s))^T E^T c_q f_s^T||F. (11)

This is the finite-error object. All f_s and gates are from the SAME actual
history X. Arbitrarily selectable parameter columns or unrelated feature
tuples are not substituted. (11) includes cancellation/correlation as it
actually occurs; a pointwise width alone does not capture it.

For a sufficient feature-uniform upper only, allow all ||f_s||<=C. The triangle
inequality then gives

    E_X<=C sup_c sum_s ||(Q_s-Qhat_s)^T E^T c||
        <=C sum_s nu_0(Q_s-Qhat_s).                  (12)

The first expression can be much sharper than the second. Neither is claimed
necessary, nor is the general problem reduced to this sufficient inequality.
Taking a supremum over independent feature tuples is only a conservative
upper; it cannot be used as a lower for the real coupled trajectory class.

Write Q_s=a^(T-s) M_s with ||M_s||op<=1. A uniform pointwise approximation
nu_0(M_s-Mhat_s)<=eta implies

    E_X<=C eta/gamma.                              (13)

Thus the SUFFICIENT uniform per-kernel tolerance is

    eta=gamma(epsilon-delta_dense)/C,

not epsilon. At gamma=c/n it is of order epsilon/n. Comparing unit transport
spectra to epsilon without this accumulation scale proves the wrong property.
An actual joint-query bound better than (13) would be welcome, but must be
proved for all real histories rather than assumed from column correlations.

### 7.1 Horizon-uniform per-history O(r log r) operator-template upper

Keep the most recent H exact kernels, set all older kernels to zero. Every
allowed query has tail error at most

    C kappa_Q sum_(age>=H) a^age
      =C kappa_Q a^H/gamma.

Set

    H=max(0,ceil(log(C kappa_Q/[(epsilon-delta_dense)gamma])
                       /[-log a])).                 (14)

For fixed c,epsilon and kappa_Q=Theta(n^-1/2), H=O_c(n log n).
The span of the H retained kernels has at most H operator directions; its
existence gives the finite-error joint approximation (11) uniformly in horizon.
If T<H use all T kernels. This is a per-history approximation statement,
not a basis-learning encoder: its potentially unstructured dense bases would
cost H r^2. The accepted window encoder instead keeps history coordinates
and computes these kernels transiently, costing O_c(n^2 log n).

Consequently a claim of Omega(r^2) simultaneously NECESSARY operator templates
within ONE history at this finite-error scale cannot hold asymptotically in
this sense: O(r log r) retained templates suffice. A family over many histories
can still have a much larger joint geometry. Changing these quantifiers is
not evidence against a robust lower bound for history encoders.

No improvement to O(r) is obtained. There are only O(log n) relevant rotation
periods in the window, but counting them does not make them independent.
Conversely their observed near-correlation does not bound the supremum in (11)
including gate-history variation. Fixed-period and fixed-profile boundaries
remain accepted; they do not impose periodic gates in (14).

## 8. An exact quadratic control despite a possibly rich operator aggregate

This is a selected-credit-block control, NOT a complete-gradient encoder.
Fix a public nonzero H in R^l. Suppose the actual source states satisfy

    h_(t-1),source=alpha_t H,

with bounded alpha_t, while remaining memory gates can be arbitrary aperiodic
ones realized by the actual model. Initialize M0=0 and update

    M_t=a G_*,t O_* M_(t-1)+alpha_t G_*,t.            (15)

Then the reference sensitivity for K=deltaR_remaining,source is exactly

    K ->E M_t K H.

This is verified directly by the real coupled injector alpha_t K H. The
coefficient alpha_t is read continuously as
H^T h_(t-1),source/||H||^2 from the actual forward state. There is no history
membership detector. The same formula is continuous off the restricted
source class, where accuracy is not promised.

Count r^2 persistent credit coordinates; add n for current h if not supplied.
If H is supplied once by the history rather than fixed publicly, count l more
and handle its first initialization continuously as a separate restricted
interface. The theorem here uses public H and needs no such extra convention.
Equation (1) transfers the selected normalized gradient to the true dense
model with uniform delta_dense error, for features within the frozen bound C.

All permitted late queries for THIS parameter group are covered, including
arbitrary allowed future gates. Constant non-scalar and period-1 past gates
are included. The full matrix sum retains transported ages exactly; it is
not convex averaging of packet transports. Actual varying source FEATURE
DIRECTIONS and other R/W/b injections are not covered by (15).

This explains a conceptual limitation of target B: even an admissible family
of r^2 robust OPERATOR coordinates would establish only quadratic storage
for this one correlated-feature block. It would not establish the additional
log n in COMPLETE credit memory. More feature/age directions must be jointly
independent and robust after their actual coupling to the same gates.

The corresponding limitation of target A is symmetric: O(r) approximating
operator directions do not imply O(n^2) online state unless their bases and
coefficients have a counted, continuous, no-replay realization and (11) has
a horizon-uniform accuracy guarantee. Neither direction is an automatic
reduction of the original memory problem.

## 9. When a query-composed singular spectrum could become valid evidence

Here is a rigorous translation criterion, not a new numerical calculation.
Let an admissible same-endpoint history chart u->X(u) define its FULL normalized
sensitivity Z(u), on a convex ball B_R in R^s. Let

    Q(Z)=function [c_q -> Z^T c_q],
    ||Q(Z)||=sup_(c_q in C_0)||Z^T c_q||.

Choose finitely many actually permitted queries c_j and weights w_j>=0 with
sum_j w_j=1. The linear stacked map

    B(Z)=(sqrt(w_j) Z^T c_j)_j

satisfies ||B(Z)||_2<=||Q(Z)||. This produces a legitimate lower singular-
value diagnostic; it does not produce a uniform error upper. Mixed residual
coordinates must be retained unless a valid parameter-group projection is used.

Assume the finite chart satisfies

    ||Q(Z(u)-Z(v)-DZ(0)(u-v))||<=L_R ||u-v||,
    sigma_min(B DZ(0))>=s_min>L_R.                 (16)

Then by the triangle inequality and the frame lower bound,

    ||Q(Z(u)-Z(v))||>=(s_min-L_R)||u-v||            (17)

throughout the WHOLE ball. A sufficient way to prove the first inequality is
to bound the query-norm derivative variation sup_w||Q(DZ(w)-DZ(0))||_(2->Q)
by L_R and integrate along the segment. This includes mixed curvature.
No ordinary SVD is being treated as a certificate without that translation.

If (s_min-L_R)R>epsilon, antipodal separation exceeds2epsilon and the accepted
topological argument gives an s-dimensional continuous-memory lower. For
transfer from a reference map to actual queries, subtract twice the uniform
endpoint error from pair distances, or subtract delta_dense from half-margins.
Reachability, exact fixed h, all actual gate/input couplings and a finite
radius R must be independently established.

Conversely an upper bound needs a supremum over ALL permitted queries;
failure of one finite frame or one tangent spectrum cannot establish it.
A numerical high correlation at a single history does not prove uniform
L_R, a reachable chart radius, or the encoder continuity/state count.

## 10. Proof attempts, what fails, and what is still unproved

### 10.1 Exact quotienting

The operator query kernel is zero by (4). Thus an exact query-invisible
linear subspace cannot discard r^2-O(r) directions. Approximate invisibility
is possible only relative to a declared finite radius and coefficient budget.
The accepted exact observability theorem is not rerun.

### 10.2 Normalization alone

For unit transports normalization can make every packet epsilon-small by (9).
That does not bound a sum, as the admissible control (10) shows. At the natural
accumulated allowance normalization leaves the ambient ball fully visible
by (7)--(8). Therefore a proof that normalization ALONE forces O(r) effective
operator directions is false for that envelope. It must use restrictions of
the actual gate semigroup, simultaneous feature coupling and history geometry.

### 10.3 Low-rank or query-weighted SVD

The accepted low-row-rank truncation counterexample is preserved. An average
query Gram/SVD is only a lower diagnostic as in (5),(16); it cannot certify
a uniform upper by itself. A query-norm width of the actual finite set at
the accumulation-aware tolerance remains a valid target, with no guarantee
of a cheap or continuous basis realization. No new algorithm benchmark ran.

### 10.4 Algebraic r^2 span and finite-radius lower

The algebra can generate r^2 exact directions while the admissible variation
of most of them is below the finite-error scale. The artificial ball theorem
does not resolve whether admissible product words generate that radius.
Positive diagonal gates, tanh realization, contraction, product age and the
shared feature tuple couple all columns. A radius for one direction at a time
does not give a simultaneous r^2-dimensional same-endpoint section.

Even an actual r^2 operator section would not by itself yield Omega(n^2 log n):
the constant-feature control (15) already stores an arbitrary aggregate
matrix in r^2 coordinates. A logarithmic lower needs ONE joint section with
extra independently observable feature/age coordinates, not a union of r^2
operator witnesses from different histories or repeated age-band counts.

### 10.5 Period correlations

Rotations have a public finite period; gates need not. Repeated phases can
aggregate exactly in the accepted scalar/profile/Floquet classes. For general
aperiodic gates, showing that transported operators differ little on AVERAGE
does not control (11) after coefficients and future queries are selected.
No norm bound on that full residual sum was found. Convex packets and fixed-
anchor renewal are not repurposed under a different name.

## 11. Strongest conclusion and smallest remaining mathematical obstruction

The finite-error operator metric is now specified with all physical weights.
It has no exact invisible subspace; it can retain r^2 robust directions on
a bounded accumulated-operator envelope. It also makes individual bounded
transports weak while a real accumulated history remains strongly visible.
These are finite-error statements, not tangent-rank conclusions.

For ACTUAL admissible arbitrary aperiodic histories, the coupled aggregates
have p=O(r) exact operator directions by (6a), but storing them costs cubic
state. No O(r) individual-kernel approximation with a quadratic counted
continuous online description, or jointly robust Omega(r^2) same-endpoint
operator section, was obtained. Per-history O(r log r) sufficient retained
templates and the accepted O(n^2 log n) window encoder remain available.
General Omega_c(n^2) to O_c(n^2 log n) memory bounds are unchanged.

The smallest new geometric question is the accumulation-aware finite-radius
width of the ACTUALLY REACHABLE coupled kernel family under (11). An O(r)
width plus counted continuous recursive structure would be sufficient for
one route to the upper; it is not a necessary representation theorem. A
negative route needs a continuous admissible fixed-h lift of many independent
operator innovations with width-independent joint query margin, followed
by a separate proof that additional feature/age blocks cannot aggregate.

The task is stopped at this partial theoretical result. Recommended next
theorem: prove or refute a horizon-uniform JOINT query-norm width bound for
the reachable coupled kernels, at the budget-adjusted scale in (11)--(14),
including gate-history variations. Do not pursue single-frame renewal as
a reduction. No other gap regime, architecture or learning stage is begun.

## 12. Checks, provenance and resources

Manual checks: frozen group multipliers; actual-query box and adjoint envelope;
source-feature coupling; sign average and uniform norm inequalities; finite-
radius width/packing proof; exact accumulation/history indexing; source input
slack, fixed-h reset and dense transfer; tail exponent; counted basis state;
matrix-eligibility control; finite chart/query-frame/remainder inequalities.
New derivations require independent hostile review; no machine proof claim.

No automated tests, tensor/SVD experiments, GPU/CUDA, model-server work,
training or scientific compute workload ran. Administrative CPU/wall time
and RAM were not profiled. Only manuscript, hashing, Git and literature
operations were performed. AGENTS, other notebooks, historical evidence and
GAS-0 are untouched. Source and manuscript hashes are in PROVENANCE.json.
