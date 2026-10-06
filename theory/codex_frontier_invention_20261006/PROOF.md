# A continuously coded private spatial-write section

Codex, 2026-10-06. **Author-derived theorem, pending independent hostile
review.** Owner-reviewed historical results are premises. This document
does not change their status or the authoritative current-theory file.

## 1. Result

Let log denote the natural logarithm. For every integer n >= 10^3000 and
every public real M satisfying

    sqrt(n) <= M <= n/(log n)^12,

the existing frozen dense tanh fixed-feature family has one continuous,
injective, admissible same-endpoint history section S:B^D -> histories with

    K = floor(10^-20 M),       q = floor(K/10^9),
    D = 2q >= M/10^30,
    m = 8K floor(M/(8K)),      .99 M <= m <= M,

    T+2 < 400000 n/sqrt(m),
    mT < 400000 n sqrt(M),
    ||X_raw||_2 < 1500 sqrt(n) M^(1/4),

and, on EVERY boundary antipodal pair, actual normalized legal-query
distance > .3, hence half-margin > .15 at epsilon=.001.

Every final donor local trace is exactly public and identical between
histories. Separation lies in the private spatial response, not unmatched
local trace. No past tape is provided to a decoder.

Consequences:

* M=n^(3/4): D>=n^(3/4)/10^30, mT<400000 n^(11/8), and
  ||X_raw||<1500 n^(11/16). This gives beta=3/4 rather than 3/16.
* For every fixed beta in [1/2,1), eventually M=n^beta is permitted:
  D>=n^beta/10^30, mT=O(n^(1+beta/2)), and
  ||X_raw||=O(n^(1/2+beta/4)).
* M=n/(log n)^12: D>=n/[10^30(log n)^12],
  mT<400000 n^(3/2)/(log n)^6=o(n^(3/2)), and
  ||X_raw||<1500 n^(3/4)/(log n)^3.

The achieved polynomial-exponent supremum is 1; an Omega(n) lower bound is
NOT proved. Every fixed beta<1 is achieved with a beta-dependent onset.
For example a sufficient explicit onset for the power specialization is

    n >= 10^[max(3000, 200/(1-beta)^2)].

No superlinear result or new general energy-impossibility exponent follows.
The global superlinear bracket [1/4,3/4] and full-model bounds are unchanged.

An equivalent constructive radius tradeoff, for a budget
R_abs>=1500 n^(5/8), is

    d_F(n,.001,R_abs) >= (1/10^30) min(
        n/(log n)^12, [R_abs/(1500 sqrt(n))]^4).

Choose M equal to the displayed minimum. This is an existential lower
construction, not an upper bound or an optimality claim. At M=n^(11/16),
the dimension is >=n^(11/16)/10^30 with the SAME resource exponents
mT=O(n^(43/32)), ||X_raw||=O(n^(43/64)) as the old R=2 specialization.

The mechanism is a new *nonlinear joint control code*. The linear write
gain still loses 1/sqrt(K). We avoid sparse boundary controls, collect many
independent parameter-gradient coordinates, and pay complete row errors
once. This is not a claim that the old full-cube minimum gain improved.

## 2. Exact inherited contract and history geometry

Use k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
R0=diag(aO,I_l/(100n)), W_input=I, b=.05*1_n.
The actual dense frozen R has norm a and

    e_R=||R-R0||_op <= 4/(10^8 n^2).

The source is the autonomous sigma*1_l, with
sigma=tanh(sigma/(100n)+.05), .0499<sigma<.051, and the ONE fixed source
feature is f_s=1_l/sqrt(l). Past inputs lie in (-.5,.5)^n; legal future
preactivations lie in [.25,.75]^n. All R entries are independently
differentiated. Realized past/future inputs are held fixed.

Precisely, the inherited terminal loss is (1_n^T h_future/sqrt(n))/beta_loss,
beta_loss=max(1,||R||_F), and the recurrent group multiplier is
w_R=||R||_F/n. Both public normalization multipliers are held constant
when differentiating, as in codex_autonomous_absolute_energy_20261003,
section 1. Here beta_loss>1, so w_R/beta_loss=1/n exactly.

Use the accepted four-site corridor lift: two moving cycle sites per tuple
have state +sqrt(1-g), two stationary off-cycle compensators have the
negative state, all four gates agree. All other reference states evolve
autonomously with zero reference input. Source preparation, all driven
steps, actual dense inverse-lift corrections, and reset are counted.

Set S_geom=m+T+4, A=2S_geom, B=5S_geom as in the inherited lift. Section 10
checks S_geom<=d/100. Thus no track wraps or meets a public front slot.
The tuple state sum is exactly zero, not approximately zero. Consequently
bath/front/source schedules are independent of all donor controls.

Split m tuples into m/2 donors and m/2 survivors. Partition the donors
into K equal groups. Each donor group has m/(2K) tuples, h_D=2m/K total
sites, and m/K stationary compensator sites. The survivor has h_S=2m sites,
with m stationary sites. Its tuple labels are the four R=2 Walsh labels,
equally represented. The choice m multiple of 8K makes all allocations
integral. No separate survivor support or epoch is assigned to a probe.

The public source/bath setup, zero-start inverse lift and same-endpoint
reset are exactly those in:

* ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md, sections 1-5;
* ../codex_private_renewal_gamma_20261003/PROOF.md, sections 5-6;
* ../codex_multicolumn_spatial_write_20261005/PROOF.md, sections 2-8.

We use their local identities/estimates under the explicitly checked
geometric premises, NOT their previous K<=n^(3/16) final theorem range.
That cutoff is replaced by the new error ledger below.

## 3. Fixed orthonormal probes and the exact complete recurrence

Let d_j and s be the unit indicators of donor-j and survivor stationary
compensator sets. Put

    w_j=d_j-s/sqrt(K), W=[w_1,...,w_K], P=1_K 1_K^T/K,
    H=I-(1-1/sqrt(2))P, V=WH.

Then W^T W=I+P, H^2=I-P/2, V^T V=I. Each v_j=V e_j is stationary,
zero-sum, and O_* v_j=v_j. The recurrent actions (Ev_j) f_s^T are
Frobenius-orthonormal. They use the existing recurrent output-row columns,
not new source features or new trainable parameters.

With preparation indexed t=0 and no recurrent preparation forcing,

    X_0=0, X_t=G_t(a O_* X_(t-1)+V), 1<=t<=N=T+1.       (1)

The physical sensitivity is sigma sqrt(l) E X_t. This is the COMPLETE
fixed-feature sensitivity on span V. In particular,

    O_*=C+1_r u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-gamma^2 1_r^T/k,
    v_H^T=gamma 1_r^T/sqrt(k),
    gamma=1/(1-1/sqrt(k)).

Equation (1) retains the private K-row vectors J_t=u^T X_t and
B_t=v_H^T X_t, exceptional front, terminal row, bath, and all repeated
Householder renewals. It is not a first-renewal truncation.

Define unit witnesses b_j=w_j/sqrt(1+1/K)=V a_j. Their positive and negative
sums are P_j=sqrt(m/(K+1)) and -P_j. The exact frame upper bound is

    lambda_max[(a_i^T a_j)_(i,j)] = 2/(1+1/K) < 2,
    sum_j |a_j^T r0|^2 <= 2 ||r0||_2^2.                  (2)

Thus MANY simultaneous b_j tests lower-bound one returned K-gradient
norm. These witnesses are not being called orthogonal.

## 4. A continuous full-spark code with many saturated boundary entries

LEMMA 1. For K>=10^10 and q=floor(K/10^9), there is a fixed public real
matrix B in R^(K x q) such that

    ||B||_op <= (3/2)sqrt(K),
    every q-row minor is nonsingular,
    for every ||y||_2=1, at least K/20000 entries of B y have |(B y)_j|>=2.

Proof. Choose independent standard Gaussian entries. For fixed unit y,
(B y)_j are independent standard normals. The elementary density bound

    Pr(|Z|>=3) >= 2 exp(-8)/sqrt(2pi) > 1/5000

uses the two intervals [3,4] and [-4,-3]. Chernoff's Bernoulli bound gives

    Pr[#{j: |(B y)_j|>=3}<K/10000] <= exp(-K/40000).

Take a 1/1000-net of S^(q-1), of size at most 2001^q. Independently, the
Gaussian square-moment formula with exponent 1/10 gives

    Pr[||B y||_2^2 > (81/64)K]
      <= exp[-81K/640 + (K/2)log(5/4)] < exp(-K/100).

A 1/4-net of size at most 9^q then proves ||B||_op<=1.5sqrt(K).
The union of the two failure probabilities is less than 1 for K>=10^10
and q<=K/10^9. Any q Gaussian rows are independent almost surely, and
there are only finitely many such minors.

For an arbitrary boundary y, choose net point y0 with distance<=.001.
The norm bound gives sum_j |[B(y-y0)]_j|^2 <= (9/4)K*10^-6. Fewer than
(9/4)K*10^-6 entries can change by more than 1. Therefore at least
K/10000-(9/4)K*10^-6 > K/20000 entries retain magnitude>=2. This proves
the uniform statement, rather than a sampled-direction statement. QED.

Define clip(x)=max(-1,min(1,x)) and

    F(y)_j = clip((B y)_j/2), y in B^q.                   (3)

This map is odd and continuous. It is INJECTIVE: at any y, at most
(9/16)K entries have |(B y)_j|>=2, so at least (7/16)K rows are strictly
unsaturated. If F(y')=F(y), those rows give B_j y'=B_j y. More than q
such rows are available and any q are independent, so y'=y. Saturation
does not store hidden sign/order/tie data.

For y=(y_1,y_2) in B^(2q), put

    z_e = ||y||_2 y_e / max(||y_1||_2,||y_2||_2) if y!=0,
    z_1=z_2=0 if y=0;   theta_e=F(z_e).                   (4)

The first map is an odd homeomorphism onto the product of two q-balls.
Its inverse is y=max_e||z_e||_2 * z/||z||_2 (and 0 at 0).
On every boundary point at least one z_e is on S^(q-1), so at least
K/20000 controls in that ONE stage are exactly +1 or -1. All stage
controls coexist in one B^(2q). B is a public design constant for the
history section; it does not alter the frozen RNN or hide past storage.

## 5. Full schedules, legal corrections, and common endpoint

Set C0=100000 and

    t_e=ceil(C0 * 2^(2-e) n/sqrt(m)), e=1,2,
    L_d=ceil(1000 log n), L_mask=ceil(2000 log n),
    L_clear=100000 ceil(n/m) ceil(log n).

Let T=sum_e(t_e+L_mask+L_clear). Prepare once and reset once.
Set g_L=.995, g_H=1-n^-2. In the first t_e-L_d donor steps, group j uses

    g_j,e=g_L+(theta_j,e+1)(g_H-g_L)/2.

Survivors use g_H. During the next L_d-1 steps all donors use g_L.
At the last step correct donor j separately:

    g_last,j = tau_target/(1+a tau_prev,j),
    tau_next = g(1+a tau_prev).                           (5)

Here tau_target is the public trace obtained by using g_L throughout this
stage from its public incoming trace. The correction is continuous,
strictly legal, and exact. As in the inherited proof,

    |g_last,j-g_L|<=2N n^-5, .994<g_last,j<.996.

This holds simultaneously; a diagonal correction has operator norm equal
to its maximum entry, not K times that entry. The pair-response charge is
at most 8N^2 n^-5. Later stage gates do not depend on earlier controls.

After each write use the public bit-e survivor mask for L_mask steps:
g_H on chi_e=+1, g_L on chi_e=-1, donors low. Then restore all survivors
high, donors low, for L_clear steps. All four sites of a tuple use the
same mask. The whole-ball inverse lift uses the actual frozen R and
x=atanh(h)-R h_prev-b. This produces the prescribed states exactly, but
is NOT differentiated as a control policy. The final public reset puts
every driven coordinate at the same public ordinary state u_N. All bath,
front, node-0, and source coordinates were already public. Hence the
entire actual endpoint is identical, with protected reset gate q_N>.98.

All donor compensator traces match exactly by (5), survivor direct paths
are public, and L_N V is public. Thus the final comparison on V is a
comparison of H_N=M_N-L_N, the PRIVATE channel. The code is injective
as a history section: distinct theta values change an early prescribed
state, and identical actual inputs from a common start cannot do that.

## 6. Fresh auxiliary comparison without a hidden sqrt(K) front charge

For group averages z=(z_1,...,z_K,z_S,Z), put c=gamma^2/k,

    w_j=c h_D, w_S=c h_S, w_b=gamma-4mc, sum_i w_i=gamma.

The EXACT complete group recurrence for a fresh unit probe is

    z_t=aD_t(I-1 w^T)z_(t-1)+D_t f+aD_t1 rho_(t-1),    (6)
    rho=-c sum_(z=1)^N(F_z-Z).

The sum runs through every GLOBAL front slot. Public q_t and f_z,t are
sampled at global time, not restarted at each write. For b_j,
f_j=P_j/h_D, f_S=-P_j/h_S, other f_i=0.
Dropping rho defines an auxiliary comparison, not the actual dynamics.
Here "fresh" means the zero-initial forced component in the exact linear
sensitivity decomposition. It does not reset the actual history, public
front or incoming sensitivity. The other component is retained in the
incoming-credit charge in section 6.3.

The inherited chronological cone, valid for changing q_t, says the
auxiliary survivor response for donor j low is minimized when every idle
donor is high. Its premises are w_b>.9, q_t<=.9992, g_H>.99, and

    sum_nonS w_i(1-g_i/g_H) > gamma-1.                    (7)

They follow here from the bath deficit alone. For completeness, let
S_w=w^Tz. The invariant cone is z_nonS>=0 and S_w<=0. For a homogeneous
positive idle impulse use U=-z_S, r_i=z_i+U, P0=U+S_w. After division
by a g_H,

    U^+=P0,
    r_i^+=d_i r_i+(1-d_i)P0,
    P0^+=sum_nonS w_i d_i r_i+[B_def-(gamma-1)]P0,
    d_i=g_i/g_H, B_def=sum_nonS w_i(1-d_i).

All coefficients are nonnegative, so increasing idle gates cannot
increase the low donor's survivor value. This is chronological, not
frozen spectral reasoning. A matched-high b_j response is exactly
kappa b_j regardless of idle gates, where

    t0=t_e-L_d, kappa=g_H sum_(s=0)^(t0-1)(a g_H)^s.

### 6.1 New auxiliary residual bound

We need calibration in the auxiliary system WITHOUT charging one front
error to each coordinate. In weighted coordinates z'=diag(sqrt(w)) z,
the auxiliary transport is aD_t R_hat, R_hat=I-r_w r_w^T,
r_w=(sqrt(w_i))_i. Its eigenvalues are 1 and 1-gamma; its norm<=1.

With donor j low and all idle donors high, the high zero-sum subspace is
reducing. Its total weight is

    w_H=c(4m-2m/K) >= 3cm >= 6m/n > gamma-1,

and w_H<.01. In its orthogonal complement write x=beta v_High+z_out,
where v_High=r_H/sqrt(w_H). Put q0=r_w^T x and
y=P_out R_hat x=z_out-r_out q0. Since w_out=gamma-w_H<=1,

    beta=[(1-w_out)q0-r_out^T y]/sqrt(w_H),
    ||x|| <= 2|q0|+2||y||/sqrt(w_H),
    ||x||^2 <= 8 q0^2+8||y||^2/w_H.

All outside gates are <=.9992. Therefore, for every chronological q_t,

    ||x||^2-||D_t R_hat x||^2
       >=(2-gamma)q0^2+(1-.9992^2)||y||^2
       >=(w_H/6000)||x||^2.

The auxiliary complementary transport contracts by at least w_H/12000
per step. Group-projected unit forcing has weighted norm<=sqrt(c);
converting the survivor read back multiplies by 1/sqrt(c). Thus its
forced complementary read is <=12000/w_H<=2000n/m. We use 16000n/m
conservatively.

Its high zero-sum projection gives the same exact calibration coefficient
as the inherited physical projection. Consequently, if control j is
+1 in one history and -1 in the other, regardless of their other controls,
the fresh auxiliary survivor row r^0 obeys

    |r^0 a_j| >= .35 kappa/sqrt(K)-16000n/m.             (8)

The sign is fixed by which endpoint is low. The exact positive coefficient
is K/[(2K-1)sqrt(2(K+1))] >=1/(2sqrt(2K))>.35/sqrt(K).

### 6.2 Aggregate the coordinate comparisons first

For the stage furnished by (4), at least K/20000 coordinates are full
endpoint comparisons. All their tests concern the SAME row vector r^0.
Equation (2) and (8), plus K/m<=2*10^-20, give

    ||r^0||_2
      >= [ .35 kappa -16000 sqrt(K)n/m ]/200
      > .00174 kappa.                                    (9)

Here kappa>=.998 C0 2^(2-e)n/sqrt(m); the fractional calibration loss
16000 sqrt(K)n/(m kappa) is <3*10^-11. This is a finite endpoint
comparison, not a Jacobian or an axis-only claim.

### 6.3 Charge the complete front ONCE in row norm

For ANY unit v in span V, the fresh full response has norm<=t. The verified
global front bounds give

    |F_z,t-Z_t|<=10000 z (.9992)^(z-1) t/sqrt(n),
    |rho_t|<=6*10^10 t/n^(3/2).

Here is also a direct vector-norm justification of this use of those
bounds. At least n/4 ordinary bath rows have the same fresh response Z,
so ||Z||_2<=2t/sqrt(n), while ||J||_2<=3t/sqrt(n) and ||B_t||_2<=2t.
There is no parameter forcing on a front slot. The first front has gate
<=1/n, giving ||F_1-Z||_2<=10t/sqrt(n). For z>=2 the exact difference
recurrence is

    F_z,t-Z_t = a f_z,t(F_(z-1),t-1-Z_(t-1))
             +a(f_z,t-q_t)(Z_(t-1)+J_(t-1)).

With r_bath=.9992, induction bounds its norm by
10 z r_bath^(z-1)t/sqrt(n), certainly by the displayed 10000 bound.
Summing ALL z uses sum z r_bath^(z-1)=(1-r_bath)^(-2), with c<3/n,
and proves the stated rho bound. The argument applies to the complete
K-vector of each row because ||X_t||_op<=t. It does not assume physical
support localization and includes front slots made by earlier stages.

Weighted auxiliary transport is contractive for every changing D_t.
Summing the forcing in (6), and converting the survivor read, gives
|beta_t(v)-beta_t^0(v)|<=10^12 t^2/n. Taking the SUP over unit v
therefore proves the ROW-NORM bound

    ||r-r^0||_2 <= 2*10^12 t0^2/n.                       (10)

There is no sqrt(K) factor in (10). The complete front is not assumed
monotone or zero. All renewal paths are retained in the actual response
and controlled by this full-propagator comparison.

After the previous public clear, an incoming complementary response has
operator norm at most B0=16000n/m+N n^-6. The identical incoming protected
survivor component cancels. Charging 2B0 ONCE, equations (9)-(10) give
the actual survivor common-row difference before the low tail

    ||r_write||_2 > .00173 kappa.                        (11)

The envelopes in section 10 justify this slack for every admitted width.

## 7. Full-vector tail, mask, clear, and stage separation

The complete fresh pair has operator norm<=2t0, and the incoming charge
gives a bound <=3kappa. In a common public tail, this norm cannot increase.
Since ||u||<3/sqrt(n), every step of the survivor mean changes from its
scalar a g_H transport by at most

    sqrt(h_S)||u^T Delta X||_2 <= 13 kappa sqrt(m/n).

This is a bound on the K-vector, not K individually charged components.
The legal last trace correction adds at most 8N^2 n^-5 in full operator
norm. Both local traces are then equal; this does not erase the private
survivor mean.

During the public mask, the retained high-half common coefficient is
(a g_H)^L_mask r_write/sqrt(2), with row-norm drift bounded by
20 L_mask kappa sqrt(m/n). The erased half obeys its exact low-gate
recurrence including the SAME private J. Summing that recurrence bounds
its coefficient by 3kappa n^-10+2000kappa sqrt(m/n). Subtracting halves
and dividing by sqrt(2) produces the protected Walsh row. Thus all tail,
mask, and correction losses together can conservatively be charged by

    10^8(log n+1) kappa sqrt(m/n)
       +8N^2 n^-5+3kappa n^-10+2N n^-6.                 (12)

This is <10^-6 kappa in our range. Scalar a g_H decay is included below.
Consequently the stage's protected singleton row has norm>.0008kappa
after the mask and clear.

The exact survivor zero-sum reducing space ensures clear homogeneous
decay only by a g_H on this row. Its complementary error is <=2N n^-6.
For the later fresh Walsh bit, the exact character identity is

    xi_I -> A_e xi_I+B_e xi_(I symmetric_difference {e}),
    A_e=[(a g_H)^L_mask+(a g_L)^L_mask]/2,
    B_e=[(a g_H)^L_mask-(a g_L)^L_mask]/2.

An earlier bit remains present; singleton reads from different write
stages therefore annihilate each other's protected terms. Telescope by
the TWO whole stages. The earlier histories in each comparison agree,
and later controls agree, because (5) makes incoming traces public.
No KR-axis telescope or replay tape is used.

Including both possible later masks, all scalar decay, q_N>.98 reset,
and the <=4N n^-6 cross-stage row error, the dominant coded stage e gives

    ||xi_e,future^T O_* Delta X_N||_2
       > .0005 kappa_e 2^(-(2-e)).                       (13)

Every inequality applies to arbitrary boundary y; the choice of e is
made from its coded stage norm. The histories remain a single family.

## 8. Actual permitted query and finite-error topology

Take the two legal one-step preactivation patterns .25/.75 according to
chi_e on the survivor support, interchanging them in the other pattern
and agreeing off that support. The same chosen future input applies to
both histories because the actual endpoint is identical. Future inputs
are frozen. Put s_gate=(sech^2(.25)-sech^2(.75))/2>.17.

With head 1_n/sqrt(n), the accepted recurrent group/loss factor 1/n,
the one source feature f_s, and V orthonormal, the two-query triangle
inequality gives the complete reference metric lower bound

    nu(Delta M_N)
      >= [sigma sqrt(l) a s_gate sqrt(2m)/(n sqrt(n))]
           ||xi_e,future^T O_* Delta X_N||_2.             (14)

No parameter-column query operation, independent cohort normalization,
or arbitrary replacement adjoint is introduced. A gradient returned by
one actual query contains all K projections; its Euclidean norm permits
(14). Projection cannot increase the complete gradient norm.

Using (13), kappa_e>=.998 C0 2^(2-e)n/sqrt(m), l>=n/2 and a>.999,
the reference pair distance is greater than

    .0499 * .999 * .17 * .0005 * .998 * 100000 > .4.      (15)

The inherited complete dense pair-comparison charge, valid also for these
K projections and the same legal witnesses, is

    e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n], q_f<.941,       (16)

and is <=8e-9 here. It includes node-0/source leakage and actual future
transport. The previously corrected erroneous dense display is NOT used.
Direct future forcing cancels at the common actual endpoint. Thus every
actual antipodal pair has distance >.3, with ample slack in (15).

Borsuk-Ulam on S^(D-1) contradicts a continuous past encoder using fewer
than D counted coordinates: equal encoded antipodes would return the same
answer to the chosen common legal query, hence have pair distance<=.002
if both errors were<=.001. Equation (15) contradicts this. The proof is
finite-radius over the entire boundary, not exact rank, packing, or a
local linearization.

## 9. Complete absolute energy and resource ledger

All histories satisfy the inherited FULL bound

    ||X_raw||_2 <= 2sqrt(m(T+2)+1)
                  <1500 sqrt(n) M^(1/4).                 (17)

Preparation, source initialization, moving holds, donor writes, survivor
holds/masks, compensators, exact trace corrections, common reset and
actual dense inverse lift are included. Autonomous reference background
uses zero reference input; its small actual dense correction is included,
not declared free. No public input center is subtracted. The public code
only chooses existing legal simultaneous gates, so adds no control step.

There are 4m driven tuple coordinates per interior step, K existing
orthonormal recurrent directions, one source feature, two mask/write
stages, and ONE reset. Source preparation uses the inherited public
initialization. The temporary public design matrix B has Kq entries;
it is a constant defining the section, not history-dependent storage or
another differentiated parameter group.

For M<=n/(log n)^12, mT<400000 n^(3/2)/(log n)^6, so the coordinate-time
budget is genuinely little-o of n^(3/2). Norm (17) is an UPPER bound
and is never reversed into an energy impossibility theorem.

## 10. Explicit every-width envelopes

All quantities below hold for every n>=10^3000, not sampled widths.
Put L=log n>=3000 log 10>6900. Rounding gives

    K>=.5*10^-20 M, K/m<=2*10^-20, .99M<=m<=M,
    D>=M/10^30, m>=.99sqrt(n), m/n<=L^-12.

The schedule overhead is at most 500000(n/m)(L+1). Dividing it by
C0 n/sqrt(m) gives <=5(L+1)/sqrt(m), so
T+2<4C0 n/sqrt(m). In particular N/n<410000 n^(-1/4).
Geometry follows from 401[L^-12+410000 n^(-1/4)+4/n]<1.
The bath induction has |C_n|<.05 and its front forcing<.012, proving
.99<q_t<=.9992, first-front gate<=1/n, front-above-bath ordering, and
0<=q_t-f_z,t<=2(.9992)^(z-1), at GLOBAL times.

Bernoulli's inequality gives kappa_e>=.998t_e and
(a g_H)^T>.999. The clear two-step bound gives factor<=n^-6.
The relevant normalized losses are bounded as follows:

    auxiliary calibration inside (9): <3*10^-11;
    full front row charge / kappa: <5*10^17 n^(-1/4);
    incoming complementary charge / kappa: <n^(-1/4);
    tail and mask row charge / kappa:
       <2*10^8 / L^5 <10^-6;
    correction and clear residues / kappa: <n^-2;
    two-stage cross-read charge / kappa: <n^-4.

The second, third, fifth and sixth bounds are much below 10^-6 at the
threshold. The logarithmic bound decreases for all larger n. All powers
are decreasing; powers times log n decrease because L exceeds their
derivative thresholds. These envelopes leave slack in
.00174 -> .00173 -> .0008 -> .0005. Also N<n/400, so (16) is far below
8e-9. This closes all asymptotic, floor, chronology, and dense conditions.

## 11. Scope, novelty, and exact limits

The construction remains the existing dense tanh family. Its new operation
is mathematical control coding, not a new neural architecture. It differs
from probe-only substitution, passive filters, or fixed-compensator
widening of a scalar donor amplifier: many private tests coexist on the
SAME stage, every donor trace is matched, and a uniform finite-ball code
forces enough full donor tests to combine in the actual gradient norm.

It does not contradict the old probe-only axis obstruction. Our dimension
2q is smaller than the full 2K cube by a fixed factor; this lower-dimensional
coded ball avoids its weak sparse boundary axes. The linear write matrix
can retain its 1/sqrt(K) gain. No universal dilution theorem is asserted.

Within this fixed R=2, K=Theta(m) protocol the constructed dimension is
O(m). With m=o(n) it is sublinear, even in the near-linear logarithmic
specialization. Thus no D=omega(n), Omega(n), new superlinear energy
threshold, bit/VRAM statement, or full-model improvement is proved.

Hostile reviewers should primarily attack: (i) the simultaneous signed
endpoint comparisons in (8); (ii) the new auxiliary complement calibration;
(iii) the fact that (10) and (12) are operator/row bounds for arbitrary
unit probes and incur no sqrt(K); (iv) the clipped full-spark ball and its
uniform boundary count; and (v) the continued validity of the whole lift
when m grows beyond sqrt(n) under the displayed geometric envelopes.
