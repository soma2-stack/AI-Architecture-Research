# Shared spatial writes with several parameter probes

Codex, 2026-10-05. THEORY ONLY. New author-derived partial theorem;
independent hostile review required. The verified single-block theorem,
D=2 repair, complete corridor lift, and dense/query ledgers are premises.
Historical files and CURRENT_THEORY.md are unchanged.
The no-dilution question remains open.

## 1. Precise new result

Let n be any integer at least 10^1000. Let K,R be integers with

    K>=1, 2<=R<=floor(log2(n)/8), K 2^R<=n^(3/16).             (1)

There is one admissible continuous B^(KR) section using one physical
survivor block, the same R public Walsh masks for every probe, one reset,
one exact common nonzero endpoint, and the unchanged fixed-source-feature
legal-query contract. Its actual boundary antipodal pair distance is
>.012; its half-margin is >.006 at epsilon=.001.

Set

    m=2^(R+1)K floor(sqrt(n)/(2^(R+1)K)),
    t_e=ceil(10 sqrt(K) 2^(R-e) n^(3/4)), e=1,...,R,
    L_d=ceil(1000 log n),
    L_mask=ceil(2000 log n),
    L_clear=100000 ceil(n/m) ceil(log n),
    T=sum_e t_e+R(L_mask+L_clear), N=T+1.

Then

    D=KR,
    T+2<11 sqrt(K) 2^R n^(3/4),
    mT<11 sqrt(K) 2^R n^(5/4),
    ||X||_2<7 K^(1/4) 2^(R/2) n^(5/8).                      (2)

Every raw input is counted, including preparation, modulation, corrections,
clearing, dense inverse lift, and reset. There are R shared write stages,
not KR stages, and just one common survivor support.

The positive result PAYS a sqrt(K) duration cost for a 1/sqrt(K) write
gain. It does not prove the requested no-dilution version, D=omega(n),
an improved superlinear energy exponent, or a complete-corridor upper.

For example R=2 and K=floor(n^(3/16)/4) give

    D>=n^(3/16)/3,
    mT<22 n^(43/32),
    ||X||_2<10 n^(43/64).                                   (3)

At R=floor(log2(n)/8), one can instead take
K=floor(n^(3/16)/2^R); this gives D=Theta(n^(1/16) log n).
Uniformly over (1), mT<11 n^(45/32)=o(n^(3/2)).
These lower energy exponents are NOT lower energy thresholds for
superlinear memory: every dimension here is sublinear in n.

Dependency map (no historical proof is modified):

- ../codex_single_block_spatial_write_20261004/PROOF.md:
  co-moving Walsh geometry, public masks, clear protocol, exact trace
  correction, endpoint/reset and all-history norm.
- ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md:
  sections 1--5 for the full fixed-feature recurrence and rank-two
  feedback; sections 9--10 for the actual query and complete dense ledger.
- ../codex_private_renewal_gamma_20261003/PROOF.md:
  sections 5--6 for public gate caps and complete complement damping.
- ../codex_d2_time_varying_repair_20261005/PROOF.md:
  sections 5--7 for the chronological positive-coordinate mechanism and
  geometric full-front comparison; the extension to K groups is derived
  explicitly below.
- Recent leverage results are negative guidance only. No all-physical-
  support localization or support-only packing law is used.

## 2. What a parameter-column probe means here

Keep the accepted source feature f_s=1_l/sqrt(l), l=n-floor(n/2).
The source trajectory is sigma 1_l, .0499<sigma<.051.
The complete reference fixed-feature operator satisfies

    M_0=0,
    M_t=G_t(a O_* M_(t-1)+I_r), a=1-1/n, r=floor(n/2)-1.      (4)

A column probe v in R^r means the recurrent-parameter action
delta R=(Ev)f_s^T. Its Frobenius norm is ||v||_2; its physical
sensitivity is sigma sqrt(l) E M_t v. These are columns of M,
indexed by recurrent output-row coordinates, NOT K new independent
source features. No input-weight probes are needed.

Let D_k contain the m/K stationary compensator sites of donor group k.
Let S_c contain the m stationary survivor compensator sites.
Define disjoint unit vectors

    d_k=1_(D_k)/sqrt(m/K), s=1_(S_c)/sqrt(m),
    w_k=d_k-s/sqrt(K), W=[w_1,...,w_K],
    P=1_K 1_K^T/K,
    H=I_K-(1-1/sqrt(2))P, V=WH.

Exactly,

    W^T W=I_K+P, H^2=I_K-P/2, V^T V=I_K.                    (5)

Every v_k=Ve_k is stationary, zero-sum, and O_*v_k=v_k.
The actual parameter tensors (Ev_k)f_s^T are Frobenius-orthonormal.
They share the same source feature, donors, and survivors. Simultaneously,

    X_0=0, X_t=G_t(aO_*X_(t-1)+V).                           (6)

Selecting K columns introduces no extra 1/K group normalization.

The unit witness b_j=w_j/sqrt(1+1/K)=Va_j has ||a_j||_2=1.
It is positive on D_j, negative on S_c, zero elsewhere. Its positive
and negative sums are P_j and -P_j with

    P_j=sqrt(m/(K+1)).                                      (7)

Although b_j are not orthogonal, they lie in the orthonormal probe space.
A scalar read on b_j is bounded by the full K-probe gradient norm.

Literal orthogonal SOURCE directions do not multiply (4).
For source-supported orthonormal f_k, forcing amplitudes are
sigma(1_l^T f_k), whose squared sum is <=sigma^2 l.
Directions perpendicular to 1_l have zero reference forcing.
The autonomous source has one feature direction; that observation does
not bound all recurrent output-row parameter directions.

## 3. Joint histories and exact trace independence

Split m tuples into m/2 donors and m/2 survivors. Split donors into K
equal groups, each with m/(2K) tuples, hence h_D=2m/K physical sites.
The one survivor support has h_S=2m sites.
Label survivor tuples equally by b in {0,1}^R; each label occurs
m/2^(R+1) times. All four sites of a tuple have its label.

Use the accepted two moving tracks and stationary compensators, with
S_geom=m+T+4, A=2S_geom, B=5S_geom. The accepted zero-start inverse
lift realizes every gate word. Tuple states are
(+beta,+beta,-beta,-beta), beta=sqrt(1-g), with exact state sum zero.
Thus bath/front/source schedules are independent of EVERY donor control.
This does not assert sensitivity cancellation.

Use the KR-dimensional cube theta=(theta_(k,e)).
In stage e, donor group k has gate

    g_(k,e)=g_L+(theta_(k,e)+1)(g_H-g_L)/2,
    g_L=.995, g_H=1-n^(-2),

for t_e-L_d early steps. During the next L_d-1 steps all donors use
g_L. Survivors remain uniformly g_H throughout the write.
At the last donor step, correct each group separately.

If tau_0 is its public incoming local trace, run g_L for t_e steps
from tau_0 to obtain tau_target, and set

    g_last,k=tau_target/(1+a tau_prev,k).                    (8)

The scalar recurrence tau_next=g(1+a tau_prev) makes the final trace
exactly tau_target. Induction makes every stage-start trace public.
Corrections depend only on the corresponding current-stage coordinate,
not on earlier controls or another donor group.

All traces are <=N; (.995)^(L_d-1)<2n^(-5). Hence

    |g_last,k-g_L|<=2N n^(-5), .994<g_last,k<.996.             (9)

A simultaneous diagonal correction has op norm equal to its largest
entry, not the sum over K groups. Comparing two corrections costs
<=8N^2 n^(-5) in a unit-probe response.

Next apply the public bit-e mask for L_mask steps: survivor g_H on
chi_e=(-1)^(b_e)=+1, g_L on chi_e=-1; donors low. Restore every
survivor g_H and every donor g_L for L_clear steps.
Only after all R stages apply the public reset.

Every gate lies in (.994,1). All actual past inputs obey the inherited
(-.5,.5)^n cube. Every realized input is FROZEN when differentiating;
the inverse-lift policy is not differentiated. The prescribed reference
states are realized exactly in the actual dense model. Reset gives the
same complete nonzero endpoint for every cube point.

For span V, L_N V is public: all donor compensator traces are matched
and survivor compensator schedules are public. Final probe comparisons
therefore lie in the private H_N=M_N-L_N channel.
No moving-cycle parameter columns are implicitly selected.

## 4. New load-bearing lemma: all idle donors jointly controlled

Consider a fresh unit response to b_j from zero during an early write.
Put t0=t_e-L_d and
kappa=g_H sum_(s=0)^(t0-1)(a g_H)^s.
Let omega_S=1_(S_t)/sqrt(h_S).

If donor j is matched high, the complete fresh response is
EXACTLY kappa b_j for every idle donor gate choice, since its stationary
zero-sum support is all high. Its survivor mean is

    beta_match=-kappa P_j/sqrt(h_S).                         (10)

If donor j is low and every idle donor is high, the high set has size

    h_H=4m-2m/K.

Its exact co-moving zero-sum space is reducing. Since h_H>=2m, the
reviewed two-step proof gives the same complement bound 16000n/m.
Therefore

    x_low=kappa Proj_(high zero-sum)b_j+e, ||e||<=16000n/m,
    beta_low-beta_match
       >=kappa P_j sqrt(h_S)/h_H-16000n/m
       >=.35 kappa/sqrt(K)-16000n/m.                         (11)

The exact coefficient is K/[(2K-1)sqrt(2(K+1))].
Its lower >=1/(2sqrt(2K)) follows from
4K^3 >= (2K-1)^2(K+1)=4K^3-3K+1.
It remains to prove all other idle controls cannot worsen this bound.

### 4.1 Exact group reduction, with the front retained

Put k_model=floor(n/2), gamma=1/(1-1/sqrt(k_model)), c=gamma^2/k_model.
Let z_k be donor-group averages, z_S the survivor average, Z the far
ordinary bath value. Define

    w_k=c h_D, w_S=c h_S, w_b=gamma-4mc,
    sum_i w_i=gamma, S_w=w^T z,
    rho_t=-c sum_(z=1)^N(F_(z,t)-Z_t).

The exact observed group recurrence is

    z_t=aD_t(I-1w^T)z_(t-1)+D_t f+aD_t1 rho_(t-1),
    f_j=P_j/h_D, f_S=-P_j/h_S, f_idle=f_b=0.                 (12)

D_t contains the group gates and the ACTUAL changing public q_t.
The full exceptional front is retained by

    F_1,t=a f_1,t(J_(t-1)+B_(t-1)),
    F_z,t=a f_z,t(F_z-1,t-1+J_(t-1)), z>=2,
    Z_t=a q_t(Z_t-1+J_(t-1)),
    J=-w^Tz+rho, B=(gamma/sqrt(k_model))1^T x.

Dropping rho gives an auxiliary system, not an exact (K+2)-state closure.

IMPORTANT FRESH-STAGE INDEXING: here t is age within the new write, but
q_t and f_z,t are sampled at its GLOBAL history time. The front bank in
rho runs through ALL physical front slots 1,...,N, not just z<=t.
These slots are disjoint from every driven tuple by S_geom=m+T+4.
For slots not yet reached by the public front, f_z equals q and the
front-minus-bath difference is zero. A later fresh response can already
differ from the bath on z>t because those public gates were built by
earlier stages. The whole bank is retained. Its geometric bound below
sums all z and therefore does not restart the public front.

### 4.2 Common chronological cone for any number of idle groups

Let z^0 solve (12) with rho=0, retaining q_t.
Every weight is positive, w_b>.9, gamma-1<3/sqrt(n).
The bath deficit alone proves

    B_t-(gamma-1)>.0006,
    B_t=sum_(nonS i)w_i(1-g_i,t/g_H),
    sum_i w_i g_i,t<=g_H.                                   (13)

The cone z_k>=0 for every donor k, Z>=0, S_w<=0 is invariant.
Directly,

    S_w^+=a(g_H-sum_i w_i g_i)S_w
           +a sum_(nonS i)w_i(g_i-g_H)z_i
           +cP_j(g_j-g_H)<=0.                               (14)

An idle-gate derivative injects a(z_idle-S_w)>=0, since f_idle=0.

For a homogeneous idle impulse, normalize each step by a g_H.
Write the survivor value as -U; put r_i=z_i+U on every nonS group
and P=U+S_w=sum_nonS w_i r_i-(gamma-1)U. Exactly,

    U^+=P,
    r_i^+=d_i,t r_i+(1-d_i,t)P,
    P^+=sum_nonS w_i d_i,t r_i+[B_t-(gamma-1)]P,
    d_i,t=g_i,t/g_H.                                         (15)

All coefficients are nonnegative. An idle impulse has U=0, r_i>=0,
P=w_idle>0, so every chronological survivor response is nonpositive.
Variation of constants therefore shows that increasing any idle early
gate cannot increase beta_low^0. Its minimum is when all idle donors
are high. This uses genuine changing-q products, not frozen powers.

### 4.3 Uniform complete-front comparison, with no K multiplier

For a unit probe, ||x_t||<=t, ||u||<3/sqrt(n), ||v_H||<2.
The reviewed public front premises hold for all joint words:
.99<q_t<=.9992, f_1,t<=1/n,
0<=q_t-f_z,t<=2(.9992)^(z-1).

Subtracting the exact front and bath recurrences gives

    |F_z,t-Z_t|<=10000 z (.9992)^(z-1)t/sqrt(n),
    |rho_t|<=6*10^10 t/n^(3/2).

In ||z||_w^2=sum w_i z_i^2, I-1w^T is similar to the symmetric
I-sqrt(w)sqrt(w)^T, with eigenvalues 1 and 1-gamma.
Each D_t is a contraction. Summing the full chronological rho forcing,

    |beta_t-beta_t^0|<=10^12 t^2/n.                          (16)

There is no K factor: group weight is c times physical size, and total
weight is gamma. No exact full-front monotonicity is asserted.
Combining (11), (15), two uses of (16),

    beta_low(idle)-beta_match
       >=.35 kappa/sqrt(K)-16000n/m-2*10^12 t0^2/n.           (17)

This is a finite-amplitude comparison uniform over all idle controls.

## 5. Incoming credit, common tail, and spatial mask

The survivor zero-sum space H_surv,t is reducing during writes and clears,
independently of all donor gates. Identical incoming H_surv credit
cancels when one stage's WHOLE K-vector is changed. After a clear,
the complementary response on any unit probe in span V has norm <=

    B_0=16000n/m+N n^(-6).                                   (18)

All donors are low during clearing. This is complete two-step damping,
not a sensitivity reset. Incoming complementary comparisons cost <=2B_0.

The common low tail costs <=7 L_d sqrt(10m/n)kappa in survivor mean;
last corrections cost <=8N^2 n^(-5). The every-width envelopes below
turn (17) into

    |omega_S^T Delta x_write|>.349 kappa/sqrt(K),
    ||Delta x_write||<2.1 kappa.                             (19)

This holds if donor j is +1 versus -1, regardless of all other donor
controls in those two histories.

Before the mask, the survivor difference is constant on all h_S sites:
local forcings are equal, feedback is broadcast, and incoming complementary
rows are constant. The incoming zero-sum difference has canceled.
The same public chi_e mask thus applies to every probe column.

The retained high half loses <=7 L_mask sqrt(10m/n)kappa in its common
projection. The erased half has magnitude <=

    2.1 kappa n^(-10)+1300 kappa sqrt(m/n).                   (20)

This follows from its exact low-gate recurrence, using
|u^T Delta x|<=3||Delta x||/sqrt(n). It retains every renewal.
Taking (retained-erased)/sqrt(2) yields

    |xi_e^T Delta x_after_mask|>.17 kappa/sqrt(K).             (21)

The subsequent clear leaves comparison residue <=2N n^(-6) in op norm;
the protected xi_e coefficient decays only by a g_H.

## 6. Cross-probe / cross-character response

In (6), J_t^V=u^TX_t and B_t^V=v_H^TX_t are K-coordinate PRIVATE
row vectors. The full recurrence retains them. They are not free
public scalar statistics.

Let xi_I denote a unit nonempty survivor Walsh character.
A fresh bit-e mask acts on every character containing an earlier bit f<e as

    xi_I -> A_e xi_I+B_e xi_(I symmetric_difference {e}),
    A_e=[(a g_H)^L_mask+(a g_L)^L_mask]/2,
    B_e=[(a g_H)^L_mask-(a g_L)^L_mask]/2.                    (22)

This identity acts on ALL parameter columns at once. Zero sum persists
through each intermediate mask step; both Householder drivers vanish.

Telescope two cube histories by R STAGES, not KR separate axes. In each
comparison the entire K-vector of one stage is changed, earlier stages
agree, and later controls agree. Trace matching makes the later gate
word independent of the changed stage.

After its clear, the stage-f comparison is

    Delta X=xi_f r_f^T+E_f, ||E_f||_op<=2N n^(-6).            (23)

The private row r_f is nonlinear and history-dependent. No affine
dependence or diagonal donor Jacobian is assumed.
After later public masks its spatial factor contains f and possibly
later bits, so every other singleton xi_e read, e!=f, is exactly zero.

For f=e its singleton coefficient is >=(a g_H)^T 2^(-(R-e)).
The public reset supplies a q_N>.98; future O_* transports the
protected character exactly. Thus, if some |theta_(j,e)|=1,

    |xi_e,future^T O_* Delta X_N a_j|
       >.16 kappa_e 2^(-(R-e))/sqrt(K)-2RN n^(-6),
    kappa_e>=.998t_e.                                        (24)

The character response is triangular. The probe response is NOT diagonal,
but a_j is a unit vector, so (24) lower-bounds the whole K-gradient norm.
Same-stage interactions are controlled by (17); cross-stage residues
number R, not KR.

## 7. One joint ball and unchanged query contract

Use the odd radial homeomorphism

    theta(y)=||y||_2 y/||y||_infinity for y!=0; theta(0)=0

from B^(KR) to the cube. Every boundary point has some
|theta_(j,e)|=1. The section is continuous and injective: different early
gates change prescribed states, hence realized inputs from the same start.
All combinations are legal and have the same exact endpoint.

For bit e, use two legal one-step preactivation patterns .25 versus .75
according to chi_e, then interchange them. They agree off the survivor
support. Put s_gate=(sech^2(.25)-sech^2(.75))/2>.17.

The same chosen query is applied to both histories; future inputs are
frozen. Head=1_n/sqrt(n), group normalization=1/n, source feature=f_s.
The two-query triangle inequality gives

    nu_V(Delta M_N)
      >=sigma sqrt(l)a s_gate sqrt(2m)/(n sqrt(n))
                     ||V^T Delta M_N^T O_*^T xi_e||_2
      >=sigma sqrt(l)a s_gate sqrt(2m)/(n sqrt(n))
                     |xi_e^T O_* Delta X_N a_j|.             (25)

This is a lower on the complete accepted
nu(A)=(sigma sqrt(l)/n) sup_legal_Q ||A^Tc_Q||_2.
The query reads the spatial mode; its returned gradient is a K-vector,
whose Euclidean norm tests a_j. It need not address a single parameter
column through a new query operation. No RMS, arbitrary adjoint, or
changed query normalization is used.

With (24), m>=.99sqrt(n), l>=n/2, the main reference pair signal exceeds

    .0499*.99*.17*.16*.998*10*.994=.013329736668864.            (26)

Cross-stage query charge <1e-9; COMPLETE dense pair charge <=8e-9.
The dense comparison is an op-norm statement for the entire fixed-feature
operator and therefore holds simultaneously for K projections.
Actual pair >.012, half-margin >.006.

Direct future terms cancel at the common actual endpoint.
Borsuk--Ulam on S^(KR-1) contradicts any continuous encoder with fewer
than KR counted coordinates: equal encoded antipodes cannot answer a
common legal query with error .001 when pair distance >.012.
This establishes joint finite-error robust dimension, not a rank count.

## 8. Full energy, dense ledger, and ceilings

The FULL actual history satisfies the accepted upper

    ||X(theta)||_2<=2sqrt(m(T+2)+1)
                <7 K^(1/4)2^(R/2)n^(5/8).

No public input center is subtracted. The only new operation is different
simultaneous donor-group gates; no extra tuple, mask stage, or reset is used.

Preserve the corrected finite-N dense pair display

    e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n],
    e_R<=4/(10^8 n^2), q_f<.941.                             (27)

It is negligible under (1), certainly <=8e-9. The old erroneous display
is not reused. Node0/source leakage and future adjoint replacement are
included in the inherited COMPLETE comparison.

For any fixed K actions, the actual final sensitivity matrix has nK
real entries. At a common endpoint, every past-credit response on those
probes factors through it. A section separated entirely by those probes
therefore has D<=nK by Borsuk--Ulam. This is a topological ceiling, not
an achieved lower or a full fixed-feature bound.
Our particular history family has KR controls, so its own history-
parameter ceiling is D<=KR; the new lower attains that ceiling.

## 9. Explicit monotone every-width envelopes

For every integer n>=10^1000, (1) implies

    .99sqrt(n)<=m<=sqrt(n),
    K<=n^(3/16), sqrt(K)2^R<=n^(5/32),
    N<11n^(29/32), R<=log(n)/(8log 2).

The rounding loss in m is <2n^(-5/16).
Clear/mask/rounding overhead is <=30000 sqrt(n)(log n)^2, smaller
than sqrt(K)2^R n^(3/4), proving (2). The geometry ratio to d/100 is <=

    401[n^(-1/2)+11n^(-3/32)+4/n]<1.

Bernoulli yields kappa_e>=.998t_e and
(a g_H)^T>=1-22n^(-3/32)>.999.
The complete two-step clear factor is <=n^(-6).

Normalize all additive write/mask errors by kappa_e/sqrt(K).
Conservative bounds are:

    fresh plus incoming complement:
      6000n^(-1/4)+3N n^(-6)/(9.98n^(3/4));

    full-front comparison:
      4*10^13 n^(-1/16);

    common-tail read drift:
      25000(log n)n^(-5/32);

    high-half mask drift:
      50000(log n)n^(-5/32);

    erased-half remainder:
      3n^(-9)+1300n^(-5/32);

    trace corrections:
      100n^(-63/16);

    cross-stage query charge:
      2R n^(-179/32)<1e-9.

Each of the first six is <1e-6 at the threshold, and decreases thereafter.
Log-power envelopes decrease once log n exceeds their elementary
power/exponent ratio. These leave slack in .35 -> .349 -> .17 -> .16.
The bath deficit and gamma-1<3/sqrt(n) prove (13).
The reset gives a q_N>.98 on the protected support.

The old local quantile code even has p=1, since its argument is <=

    16000sqrt(11)n^(-3/64)<1.

The local traces are exact, but private differences remain large.
No refuted support-localization claim is used anywhere.

## 10. Exact scoped gain dilution

The sqrt(K) price is real for this partitioned-donor common-write route.

Consider one fresh stage with donor j high versus low, all idle donor
controls theta=0. Their gate (g_H+g_L)/2 is below .9992, so both endpoint
histories satisfy the complete complement-damping premises.
High sets have sizes h_S+h_D and h_S, respectively.

Let Pi_plus, Pi_minus be their zero-sum projections. The leading K-probe
response difference is kappa(Pi_plus-Pi_minus)V, with op-norm error
<=32000n/m. Its survivor common row is EXACTLY

    omega_S^T kappa(Pi_plus-Pi_minus)V
      =-kappa sqrt(h_S)sqrt(m/K)/(h_S+h_D)
                          [e_j^T+(1/K)1_K^T]H.

Using H^2=I-P/2, its Euclidean norm is

    kappa/sqrt(2(K+1)).                                     (28)

This is an axis-antipodal comparison of the simultaneous donor cube.
Even combining ALL K gradient coordinates retains 1/sqrt(K) gain.
Orthogonalizing the probes does not remove it.

The common trace tail, public mask, and clear turn that common row into
a protected spatial row without amplification in probe space. Front,
tail and complementary errors obey the vanishing envelopes above.
The reviewed all-future ordinary-coordinate bound
|c_Q,z|<=100/sqrt(n) on its final protected support gives

    nu_V(axis pair)
      <=20 kappa sqrt(m)/(n sqrt(K))
            +o(kappa sqrt(m)/(n sqrt(K)))+8e-9.              (29)

This bounds the rank-one protected read and charges the clear residue
in full op norm. It does not assume localization of general sensitivities.
At the old uncompensated duration O(n^(3/4)) with fixed R and m~sqrt(n),
the leading upper is O(1/sqrt(K)); it eventually loses the fixed margin.
In applying this observation to unextended durations, require the same
vanishing-error conditions, e.g. K2^R<=n^(3/16).

For clarity, the ordinary-query envelope used here is ONLY for the
final protected support, far from the terminal-cycle boundary; it is
not a cap for all ordinary physical rows. Its cycle sites are at most
6S_geom<.06d, hence more than n/8 before the terminal boundary; its
other sites are stationary
off-cycle. For a forward characteristic starting at one such site,
before L=n/8 each first departure has norm at most 6/sqrt(n).
The exact first-departure sum retains the complete subsequent
propagator and gives

    |c_Q,z| <= q_f^L(1+6L)/sqrt(n) <100/sqrt(n).

For L>=n/8, use the full norm cap q_f^L<100/sqrt(n).
Every future gate word is allowed in this estimate. This does not
reuse the refuted all-physical-support complement cap or exclude later
Householder renewals.

This is scoped to the selected probe space and this history family.
It does not refute another donor code, moving-cycle probes, a different
joint section, or signals in columns outside V.

## 11. Uniform-donor collapse and the exact remaining question

If all donors have one common gate word, any zero-sum stationary
donor-compensator probe d obeys exactly

    M_t d=tau_D,t d, tau_D,t=g_D,t(1+a tau_D,t-1).

O_*d=d and feedback vanishes. Final trace matching gives Delta M_N d=0.
Thus comparisons on the whole donor-compensator input subspace are
determined by its ONE donor-mean response; orthogonal donor contrasts
do not multiply the uniform-control result. This is an exact quotient
statement, not raw rank as robust dimension.

Nonuniform donor groups escape the collapse but pay (28).
The remaining stronger lemma is one precise minimum-gain question:

Does some legal shared donor history family and fixed orthonormal
stationary or moving-cycle probe matrix V admit a one-ball KR-control
minimum gain of order kappa per protected spatial read, rather than
kappa/sqrt(K), with this same survivor block and no K-dependent duration?

No such family, nor a universal impossibility theorem, is proved here.
Complete corridor and global superlinear bracket [1/4,3/4] remain open;
the full-model gap is unchanged.
