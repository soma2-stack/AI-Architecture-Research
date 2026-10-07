# Exact multi-survivor transfer and its current gain obstruction

Codex, 2026-10-05. THEORY ONLY. New author-derived structural statements,
independent hostile review required. Primary improved-gain question: STILL OPEN.
The owner-verified multicolumn and moving-probe results are premises, not
reopened. This isolated branch starts at the verified df9ef337 checkpoint.

## 1. Contract and exact complete recurrence

Use k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
gamma=1/(1-1/sqrt(k)), c=gamma^2/k. The selected memory operator is

    O_*=C+1u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-c1^T,
    v_H^T=gamma1^T/sqrt(k).                           (1)

O_* is orthogonal; C is the open cycle shift and off-cycle identity.
Every driven tuple has two moving cycle sites and two stationary
compensators, all sharing g_i,t, with balanced states (+beta,+beta,-beta,-beta).
This makes public source/bath/front STATE schedules independent of controls.
It does not make sensitivity feedback public.

For fixed orthonormal probes V=[v_1,...,v_K], the recurrent actions
(Ev_j)f_s^T, f_s=1_l/sqrt(l), are Frobenius-orthonormal. They use ONE source
feature; physical sensitivities are sigma sqrt(l) E X_t, .0499<sigma<.051.
With realized inputs frozen when differentiating,

    X_0=0, X_t=G_t(aO_*X_t-1+V),
    L^V_0=0, L^V_t=G_t(aC L^V_t-1+V), Y_t=X_t-L^V_t. (2)

Preparation is before t=0; its recurrent forcing is zero. All histories
start from the required zero state, not from a free prepared state.

Exact premises: ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md
sections 1--5 and 9--10; ../codex_private_renewal_gamma_20261003/PROOF.md
sections 2--6; ../codex_single_block_spatial_write_20261004/PROOF.md
sections 4--8. The reviewed multicolumn and moving-probe proofs are also
dependencies. No refuted support-localization theorem is used.

## 2. Full simultaneous write matrix

Put PRIVATE K-rows J_t=u^TX_t, B_t=v_H^TX_t. On each of the four driven
rows in tuple i, Y has the same row F_i,t, exactly

    F_i,0=0, F_i,t=a g_i,t(F_i,t-1+J_t-1),
    F_i,T=a sum_(s=1)^T K_i,s J_s-1,
    K_i,s=a^(T-s) product_(v=s)^T g_i,v.              (3)

The exceptional e_1 forcing never directly reaches these unwrapped
tracks, but its contribution to J through bath/front renewal is retained.
For survivor read xi_c supported on the tuples, let b_c,i be the sum of
its four tuple coefficients. The exact C-by-K private read matrix is

    R_c,k=a sum_s (sum_i b_c,i K_i,s) J_s-1,k.        (4)

Neither the suffix entries nor the private J history are independently
selectable. Both depend on all simultaneous donor/survivor controls.

An explicit nonperturbative completion, including all front slots at
GLOBAL time and the incoming front bank from earlier stages, is

    U2=[1,e_1], W2=[u^T;v_H^T], A_t=aG_t C,
    ell_t=W2 L^V_t, b_t=W2 Y_t,
    b_t=sum_(s=1)^t W2 Phi_C(t,s) aG_s U2(ell_s-1+b_s-1),
    Phi_C(t,s)=A_t ... A_s+1.                         (5)

This finite strictly causal Volterra operator is nilpotent; its inverse
is the exact finite sum of all powers. There is no first-Householder
truncation. Alternatively the full propagator built from aG_t O_* has
norm <=a^age. Thus (2)--(5) retain full bath/front/renewal interactions.

For two finite actual histories the exact midpoint identity is

    Delta X_t=a bar G_t O_* Delta X_t-1
                    +Delta G_t(aO_*bar X_t-1+V).    (6)

Differentiating a control coordinate, when appropriate, gives

    partial_j X_N=sum_t Phi(N,t)(partial_j G_t)
                                       (aO_*X_t-1+V). (7)

The cross-response is read-by-probe-by-control, a three-index tensor.
Selecting its diagonal or its tangent rank does not certify a joint
finite-boundary section. The example below instead uses exact finite (6).

## 3. Two exact scoped failures

### 3.1 Synchronized survivor words

If survivor words are identical and public, and their initial private
differences are zero, (3) implies

    Delta Y_surv,t=1_surv r_t.                        (8)

This is true for arbitrary simultaneous donor controls and full feedback.
Hadamard READ rotations cannot change that spatial factor. Every zero-sum
spatial read is zero. One repeated public binary mask gives only two row
words; its centered spatial response has one factor. Subsequent uniform
high gates preserve that factor.

This does NOT imply a one-dimensional parameter row r_t or D<=1: the
accepted KR construction uses K coordinates of these rows across R stages.
Unequal survivor words can escape (8), as proved in section 4.

### 3.2 The false constant-gain matched-pair construction

For disjoint equal-size donor and survivor compensator groups of p sites,
put d_j=1_Dj/sqrt(p), s_j=1_Sj/sqrt(p), v_j=(d_j-s_j)/sqrt(2).
These are orthonormal, stationary, zero-sum probes. If each donor j and
survivor j have the SAME gate word throughout,

    O_*v_j=v_j, G_t v_j=g_j,t v_j,
    M_t v_j=tau_j,t v_j, tau_j,t=g_j,t(1+a tau_j,t-1),
    Y_t e_j=0.                                       (9)

Both feedback drivers vanish exactly; the entire response is local trace.
There is nonetheless a tempting pre-correction constant gain. Let P_H
project onto zero-sum vectors on ALL 2Kp physical survivor sites. Then

    [ (P_H v_i|S)^T(P_H v_j|S) ]=I/2-11^T/(4K),
    sigma_min([P_H v_1|S,...,P_H v_K|S])=1/2.        (10)

But public final trace matching gives Delta tau_j=0, hence the final
comparison is zero. A common later mask/reset cannot revive it. If an
earlier mask breaks matched words, (9) is no longer applicable and the
new chronology requires its own analysis. Equation (10) must not be
promoted to post-correction private gain.

## 4. A genuine simultaneous nonuniform two-filter example

This is a legal finite structural example, NOT an epsilon=.001 robust
lower bound. It exhibits two independent protected PRIVATE spatial
responses with exact matching, and quantifies why their gain is insufficient.

For n>=10^6 set p=2floor(sqrt(n)/10), m=5p/2, T=4. Two donor and three
survivor cohorts each have p/2 tuples, p compensators and h=2p total sites.
Use the accepted corridor A=2(m+T+4), B=5(m+T+4); spacing
m+T+4<=d/100 holds at and above this threshold. Use v_j=(d_j-s_j)/sqrt(2),
j=1,2, where s_j is survivor cohort j's compensator indicator. This is
one orthonormal parameter space, with no new source feature.

Let

    g0=.997, gbar=.995, delta=10^-4, b=1/2000,
    d_1=gbar-b, d_2=gbar+b,
    s=(gbar-b,gbar,gbar+b).                            (11)

Step 1: donor j has g0+delta theta_j, theta in [-1,1]^2; all survivors g0.
Steps 2,3: donor j uses public d_j; survivor cohort c uses public s_c.
Step 4: survivors use public gbar; each donor uses

    g_4,j= tau_target,j/(1+a tau_3,j(theta_j)),
    tau_target,j=gbar[1+a d_j(1+a d_j(1+a g0))].       (12)

This exactly restores both donor local traces to public values. The maps
are continuous and independent. The denominator's perturbation is
a^3 d_j^2 delta theta_j, so |g_4,j-gbar|<delta. All gates are in (.994,1).
All survivor traces are public throughout. One public reset at N=5 gives
the same exact nonzero endpoint.

The whole cube has balanced tuple states, so the accepted zero-start
inverse lift applies, with every realized raw input in (-.5,.5)^n. The
source, bath and front remain public. Controls are frozen during parameter
differentiation. The whole absolute norm, including preparation, holding,
compensators, writes, both corrections, dense lift and reset, satisfies

    ||X_raw||<=2sqrt(m(4+2)+1)<4n^(1/4).              (13)

No baseline or correction is omitted. Restriction to the Euclidean B^2
is one continuous injective admissible section. It is NOT robust at the
project epsilon, as the complete-query upper below proves.

### 4.1 Exact protected response over the entire finite square

Compare theta to 0. Let j_j=Delta J_1,j. Only donor j's first gate changed:

    j_j=-c sqrt(p/2) delta theta_j.
    Delta J_2,j=a(d_j+eta_2) j_j,
    eta_2=u^T G_2 1-(sqrt(k)/gamma)u_1 G_2,11.       (14)

Indeed Delta B_1,j=-(sqrt(k)/gamma)j_j; the second term in eta_2 is
exactly the exceptional-front feedback. All public bath/front/terminal
and cohort gates contribute to u^T G_2 1. No term is discarded.

Set Pi=I_3-11^T/3. Directly from (3), at step 4,

    Pi Delta F_4,j=a^3 gbar j_j[Pi s^2+(d_j+eta_2)Pi s]. (15)

The remaining a gbar Delta J_3,j is common across survivors and is killed
ONLY AFTER applying Pi. J_3 was not truncated or assumed small. The donor
correction at step 4 changes J_4, not the forcing J_3 in survivor rows.

With z=(-1,0,1), w=(1,-2,1)/3,

    Pi s=bz, Pi s^2=2gbar bz+b^2w,
    z dot w=0, ||z||=sqrt(2), ||w||=sqrt(2/3).       (16)

Normalize these patterns on the h physical sites of each cohort to get
two unit overlapping zero-sum reads xi_1,xi_2. The reset has common
survivor gate q_N>.98, uniform reset feedback vanishes under Pi, and local
cycle transport is exact. The COMPLETE protected response relative to 0 is

    A diag(theta_1,theta_2),
    A=-a^4 q_N gbar c delta p
       [sqrt(2)b(2gbar+d_1+eta_2) sqrt(2)b(2gbar+d_2+eta_2)
        sqrt(2/3)b^2             sqrt(2/3)b^2].      (17)

Local survivor differences are zero because their words/traces are public.
Donor reset-transmitted terms are outside the read support or uniform on
it. Future O_* maps these protected patterns isometrically. All formulas
are finite identities on the WHOLE square; antipodes give 2A diag(theta).

For the inner matrix B in (17),

    |det B|=(2/sqrt(3))b^3|d_1-d_2|>0,
    ||B||_op<=20b,
    sigma_min(A)>delta p b^2|d_1-d_2|/(20n)>0.       (18)

The bounds use |eta_2|<5, from ||u||<3/sqrt(n), and
a^4 q_N gbar c>1/n for n>=10^6. Thus the two spatial responses really
are independent after correction/reset. Their gain is tiny, not Theta(T).

### 4.2 Actual legal queries and the fixed-error failure

The complete normalized metric is

    nu_V(Delta M)=(sigma sqrt(l)/n)
                      sup_legal Q ||V^T Delta M^T c_Q||. (19)

It includes arbitrary permitted future horizon. Head is 1/sqrt(n),
preactivation box [.25,.75], recurrent group factor 1/n, realized inputs
frozen. The common endpoint cancels direct future terms.

Put a chosen protected xi on its NEXT-time survivor support after reset.
Two one-step queries use gates g_mid +/-s_gate xi/||xi||_infinity,
s_gate=(sech^2(.25)-sech^2(.75))/2>.17, equal off support. These gates
correspond to legal preactivations. The SAME chosen query is applied to
both histories. The two-query triangle inequality proves

    nu_V>=sigma sqrt(l)a s_gate/(n sqrt(n))
                    ||Delta X_N^T O_*^T xi||/||xi||_infinity. (20)

This is a valid lower, not an all-query upper. On theta in the Euclidean
unit boundary, the larger of the two row reads of 2A diag(theta) is
>=sqrt(2)sigma_min(A), and ||xi_j||_infinity<=1/sqrt(h). The resulting
reference lower is >.008sqrt(h)sigma_min(A)/n, tending to zero.
Dense error may exceed it; NO actual finite-epsilon lower is claimed.

The accepted COMPLETE short-packet theorem gives the decisive ACTUAL upper,
for every pair in this family and every legal future horizon:

    pair distance <.095982(T+1)/sqrt(n)
                   =.47991/sqrt(n)<.002, n>=10^6.    (21)

Therefore these modes do not supply robust D=2 at epsilon=.001. This is
not a tangent-rank construction promoted to dimension.

## 5. Two complete subclass query obstructions

### 5.1 All-low temporal filters

If every interior selected-memory gate is <=q_c=.9992, (2) and
orthogonality give ||M_t||<1/(1-aq_c)<1250. The one public reset adds at
most one unit forcing, giving ||M_N||<1251. Every legal future adjoint,
at ANY permitted horizon, has ||c_Q||<=q_f^L<=1. Thus

    actual pair distance <128/sqrt(n)+8e-9.          (22)

It is <.002 for n>=10^12. The complete Householder/bath/front dynamics
are included. The dense charge is applied only in the accepted admitted
corridor horizon. Lengthening an all-low public filter bank does not give
Theta(T) gain. This theorem does NOT cover histories keeping some sites
near-critical, and does not close the corridor.

### 5.2 A single initial pulse cannot gain strength by waiting

This stronger scoped obstruction does NOT require low survivor gates.
Start with M_0=0. Histories may differ in donor tuple gates only at step 1,
with pair entry difference <=2delta and minimum first gate rho_0>=.994.
All gates at steps 2,...,T-1 are public and identical across histories,
but can be arbitrary legal nonuniform near-critical words. At step T
restore each donor compensator trace to its public target by the exact
formula g_T=target/(1+a tau_T-1). Assume those correction gates are legal.
Then apply the same public reset. No other private writes are allowed in
this subclass. T>=2 and the admitted corridor horizon are required.

Let P_i=a^(T-2) product_(v=2)^(T-1) g_i,v. The trace difference is exactly
Delta tau_i,T-1=P_i Delta g_i,1. Every one of the T-1 positive terms in
the direct trace is >=rho_0 P_i; hence

    tau_i,T-1 >=(T-1)rho_0 P_i,
    |Delta g_i,T|
       <=a |Delta tau_i,T-1|/(1+a min tau_i,T-1)
       <=2delta/[(T-1)rho_0].                        (22a)

The first inequality uses the legality g_T<=1 and identical targets.
It includes distinct donor words; the simultaneous diagonal norm is
the maximum entry, not a sum over donors.

At step 1, ||Delta M_1||<=2delta. Public chronological propagation is
nonexpansive, so the same bound holds until step T-1. Since ||M_t||<=t,
the entire correction-forcing difference at step T has norm at most
2delta[a(T-1)+1]/[(T-1)rho_0]. Consequently

    ||Delta M_N||<=2delta+4delta/rho_0<6.1delta,
    actual all-query pair <.312delta/sqrt(n)+8e-9.   (22b)

The public reset does not amplify the difference. Full Householder
renewals, all memory columns, arbitrary future horizons, and the dense
pair charge are included. This is a finite-pair theorem over the whole
history class, not a Jacobian approximation.

Thus even near-critical PUBLIC filter words cannot turn one small initial
write plus final trace correction into Theta(T) robust gain. The donor
control must act again during the write, or a later gate word must depend
on it in a way outside this subclass. This does not constrain the accepted
continuous donor-writing constructions, which have many private steps.

## 6. A quantitative nonperturbative word-diversity requirement

For any orthonormal V, ||X_t||<=t, ||J_t||<=3t/sqrt(n). Choose a public
comparison word g_ref,t and define F_ref by (3) using the SAME actual J.
Product telescoping and (3) prove

    ||F_i,T-F_ref,T||<=B_i,
    B_i=(3a/sqrt(n))sum_(s=1)^T(s-1)
                                  sum_(v=s)^T|g_i,v-g_ref,v|. (23)

This comparison is not a different history and does not replace J by
public forcing. A normalized cohort-mean matrix, with h_i physical sites
per cohort, is a rank-one common-word matrix plus error bounded by

    ||E||_op<=(sum_i h_i B_i^2)^(1/2).               (24)

For K>=2 output/parameter channels its minimum singular value is at most
this error. Orthonormal Hadamard read rotations cannot increase it.
If every gate difference is <=eta, then

    sigma_min<=a eta T(T^2-1)sqrt(h_total)/(2sqrt(n)). (25)

Thus a proposed cT state gain requires
eta>=2c sqrt(n)/[a(T^2-1)sqrt(h_total)]. This is a weak NECESSARY diversity
budget, not a certificate of gain or robust dimension. It does not rule
out legal near-critical unequal words. Frobenius bounds a matrix operator
error here; it is never substituted for nu or continuous dimension.

## 7. Affine Hadamard gate coding: a different scoped loss

Suppose C equal cohorts carry one public common response
kappa 1_C/sqrt(C), and one multiplicative spatial write uses
g(theta)=g_mid1+lambda H theta. H has K orthonormal zero-sum Hadamard
columns with entries +/-1/sqrt(C); the gate interval has width w.
On the FULL Euclidean unit ball, exact legality requires

    sup_theta|(H theta)_c|=sqrt(K/C),
    |lambda|<=w sqrt(C/K)/2.                         (26)

The centered control-to-spatial matrix is a kappa lambda H/sqrt(C),
whose minimum gain is <=a kappa w/(2sqrt(K)). For the FULL independent
cube, the row l1 maximum is K/sqrt(C), giving <=a kappa w/(2K).

This is an exact finite single affine multiplicative-write statement.
It is not a bound for nonlinear saturation or arbitrary chronological
histories. The accepted radial cube section must not be charged a false
Euclidean boundary loss. Conversely a ball-only gate amplitude cannot be
used while claiming full cube legality.

## 8. Masks, physical allocation and query costs

An established channel pattern multiplied by a nonempty old Walsh bit
is still zero-sum under later fresh-bit masks, provided all bit labels
have equal multiplicities WITHIN EACH channel cohort. Exact evolution is
the inherited xi_I -> A_e xi_I+B_e xi_(I symmetric_difference {e}).
This requires at least 2^R tuple labels per cohort. It preserves a proven
write; it does not establish a new simultaneous minimum gain.

K disjoint cohorts at fixed total support h have per-cohort witness
coefficient sigma sqrt(l)a s_gate sqrt(h/K)/(n sqrt(n)), rather than
the full-support sqrt(h) coefficient. This is a CHOSEN-WITNESS cost,
not an all-query upper. Keeping h0 sites per cohort costs K h0 actual
sites. A Hadamard rotation preserves singular values; rotated read
patterns still need their infinity-normalized legal query checked.

For arbitrary redesigned stage lengths, masks and clears,

    T=sum_e(t_e+L_e+C_e), physical driven sites=4m,
    ||X_raw||<=2sqrt(m(T+2)+1).                       (27)

No K is hidden in m or T. Public bath/source are actually autonomous,
and every preparation/control/correction/reset input is included.
This is an energy UPPER and is not reversed into an energy necessity.
With K fixed probes, the response factors through nK actual sensitivity
coordinates: D<=nK is only a scoped topological ceiling, not an achieved lower.

## 9. The retained checkpoint and one remaining lemma

New author structural statements are (4)--(6), (8)--(10), the legal finite
two-filter example (11)--(18), the complete low-gate query upper (22),
word-diversity bound (23)--(25), and affine budget (26). None proves a
robust K-independent or K^(-alpha), alpha<1/2, protected write.

No new robust D/beta is established. The reviewed lower stays D=KR at
n>=10^1000, K2^R<=n^(3/16); R=2 gives D>=n^(3/16)/3. Its actual pair>.012,
half-margin>.006, mT<11sqrt(K)2^R n^(5/4), full norm<7K^(1/4)2^(R/2)n^(5/8)
remain. The whole admitted range has mT<11n^(45/32)=o(n^(3/2)).
Global superlinear Omega(n log n) at O(n^(3/4)(log n)^(3/2)), bracket
[1/4,3/4], and full-model Omega_c(n^2)--O_c(n^2 log n) are unchanged.

Use the corrected dense formula e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n],
e_R<=4/(10^8 n^2), or accepted charge <=8e-9 in its regime. Do not reuse
the old erroneous display or infer that our tiny reference lower beats it.

The remaining constructive lemma is ONE question: do legal PUBLIC
near-critical survivor words, coupled to simultaneous donor controls,
make the complete finite-antipodal matrix (4) have K protected independent
spatial reads of gain >=c kappa K^(-alpha), alpha<1/2, uniformly in all
idle controls, with exact public traces, common endpoint and later
Walsh-mask survival? A valid answer must give one ball with ACTUAL query
distance>.002, not a rank count. Low fixed-rate filters and one affine
Hadamard mask cannot do this. General nonuniform chronology is STILL OPEN.
