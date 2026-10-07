# Moving-cycle probes: a telescoping obstruction for the shared common write

Codex, 2026-10-05. THEORY ONLY. All new statements are author-derived and
require independent hostile review. The accepted multicolumn theorem at
9bf66b91cc033ecae589f0b2b630acec01e58118 is a premise, not re-reviewed.
STATUS=STILL OPEN refers to other moving-probe history designs.

## 1. Scope and the two new statements

**PROVED, in the following precise scope.** Replace the stationary probes
in the accepted partitioned-donor shared-write protocol by ANY fixed
orthonormal probes supported on the moving-cycle parameter coordinates.
Keep its donor controls, survivor high-write intervals, public Walsh masks,
trace corrections, clearing, and exact reset. This substitution does not
remove the gain loss. In fact its fresh donor-axis common-read gain has the
upper bound

    sigma_min(A_cycle) <= m/(K+1) + 32000 n/m.                 (1)

A second scoped statement is stronger than a moving-only objection:
for the SAME partitioned-donor histories, replacing the probes by ANY
fixed orthonormal recurrent actions cannot remove the leading 1/sqrt(K)
loss. The complete fresh common-read row satisfies

    ||row_full||_2 <= kappa/sqrt(K+1)+32000 n/m.             (1b)

The final-stage axis bound below translates this into a necessary
Omega_epsilon(sqrt(K)n^(3/4)) duration when m~sqrt(n), provided the
explicit residual envelope is below epsilon. This is an actual-query,
finite-pair obstruction for this control family, not a universal theorem.

Here A_cycle is the K-by-K matrix whose j-th row is the complete fresh
high-versus-low response read on the one survivor mean, on the K probes;
all other donor controls are at their cube midpoints. The leading invariant
response has the sharper bound sigma_min(Q_t V) <= m/(K+1), independent
of write duration. These are upper bounds, not achieved minimum gains.
They do not identify singular values with robust dimension.

For the FULL accepted stages, every such moving-only probe matrix V has a
cube-axis antipodal pair with actual all-legal-future projected distance

    d_V <= 600000 n^(-1/4)
           + 3*10^7 (log n)n^(-3/32) + 9*10^(-9) < .001     (2)

for every integer n>=10^1000 in the accepted K,R range. Thus the inherited
radial B^(KR) section is NOT robustly certified by these moving probes.
Its COMPLETE fixed-feature section remains robust via the accepted
stationary probes; (2) is not a bound on the full gradient outside V.

A second extension covers genuine nonzero rotation eigenmode probes of
UPU, including their small stationary Householder tails. Its distance
bound adds at most

    .408 N sqrt(K)/n < 5 n^(-1/16),                         (3)

so these probes also fail the same replacement test.

No theorem excludes redesigned donor/survivor schedules, new spatial
write protocols, arbitrary mixtures with substantial stationary support,
or all possible moving-column sections. No new robust lower dimension,
superlinear construction, or energy threshold is claimed.

## 2. Premises, fixed probes, and normalization

Use the accepted definitions k=floor(n/2), l=n-k, r=k-1,
d=floor(n/4), a=1-1/n, gamma=1/(1-1/sqrt(k)), and

    O_*=C+1 u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-(gamma^2/k)1^T,
    v_H^T=gamma 1^T/sqrt(k).

O_* is orthogonal. Every feedback insertion is retained. The complete
fixed-source reference response is

    M_0=0, M_t=G_t(a O_* M_(t-1)+I), X_t=M_t V.              (4)

A probe v is FIXED in physical parameter-column coordinates. A change
v->v_t during the recurrence would change the parameter action and is not
a permissible way to accumulate its sensitivity.

Let P_c project onto selected cycle sites {1,...,d-1}, and P_o=I-P_c.
Choose any V with V^T V=I_K and P_c V=V. For example, distinct coordinate
vectors on the swept cycle tube are such probes. K<=d-1 suffices for their
existence and holds in the accepted range. They can move under O_* after
injection; they are not reselected at each time.

With the ORIGINAL unit source f_s=1_l/sqrt(l), the actual recurrent actions
are (E v_j)f_s^T. Their Frobenius inner products are delta_ij. Physical
reference sensitivity is sigma sqrt(l) E X_t, .0499<sigma<.051. There
are no new source features, no extra group-normalization factors, and no
additional history energy from selecting probes.

The exact reference query metric on V is

    nu_V(Delta M)=(sigma sqrt(l)/n)
                   sup_(legal Q) ||V^T Delta M^T c_Q||_2.   (5)

Legal Q includes EVERY future horizon L_Q>=1 and every preactivation in
[.25,.75]^n, with realized future inputs frozen for differentiation. Head
is 1_n/sqrt(n); recurrent group-RMS factor is 1/n. All direct future terms
cancel at the common actual endpoint. We use ||c_Q||<=q_f<.941, and the
accepted all-horizon 100/sqrt(n) coordinate envelope ONLY on the final
protected corridor support far from the terminal boundary. We do not use
the refuted all-physical-support localization principle.

Dependencies: ../codex_multicolumn_spatial_write_20261005/PROOF.md,
sections 2--3, 5--9 and the geometrically restricted end of section 10;
../codex_private_renewal_gamma_20261003/PROOF.md, sections 5--6;
../codex_single_block_spatial_write_20261004/PROOF.md, sections 4--7;
../codex_unpaired_corridor_sensitivity_20261003/PROOF.md, sections 1--5,
9--10. The D=2 proof and recent leverage proofs are context; their cone
and reducing-subspace proofs are not redone or needed for a new sign claim.

## 3. One complete fresh axis comparison

There are m tuples. The first m/2 are donors, partitioned into K equal
sets; the last m/2 are survivors. On each tuple there are two moving cycle
sites A+i+s,B+i+s, and two stationary compensators. Let S_s be all 2m
physical survivor sites, D_j,s the 2m/K physical sites in donor group j.
The two cycle track tubes are disjoint and do not wrap or meet the front.
The ordering of donor subgroups within the first half is immaterial below.

During a fresh write of length t, hold survivors at g_H=1-n^(-2).
Compare donor j at g_H against g_L=.995, with all other donors at
(g_H+g_L)/2<.9992. Public bath/front gates keep their actual changing
schedules. Both responses start at zero for this fresh comparison.

Let H_s^+ be the zero-sum subspace supported on S_s union D_j,s,
and H_s^- the zero-sum subspace supported on S_s. They reduce their
respective complete O_*/G chronology. On them the gate is scalar g_H;
all remaining gates are <=.9992. The inherited FULL two-step complement
bound therefore gives, on any unit forcing/probe,

    x_t^+ = x_t^(+,H) + e_t^+, ||e_t^+||<=16000 n/m,
    x_t^- = x_t^(-,H) + e_t^-, ||e_t^-||<=16000 n/m.         (6)

The larger high set only strengthens the same bound. This is a full
orthogonal reducing-space estimate, not a first-feedback truncation.
It includes the exceptional front, bath, terminal mode and all renewals.

Put w_s=1_(S_s)/sqrt(2m). Its H_s^- projection is ZERO. Transporting w_t
back inside H^+ gives the exact row, at injection time s,

    q_j,s = 1_(S_s)/((K+1)sqrt(2m))
                - K 1_(D_j,s)/((K+1)sqrt(2m)).             (7)

Indeed Pi_(H^+_s) w_s = w_s - sqrt(2m)/(2m+2m/K)
(1_(S_s)+1_(D_j,s)), which is (7). Co-moving zero-sum transport is
isometric; its transpose on this subspace reverses the same shift.
Writing lambda=a g_H, the EXACT leading survivor row is consequently

    w_t^T(x_t^+-x_t^-)
      = [g_H sum_(s=1)^t lambda^(t-s) q_j,s^T] v + eta_j v,
    ||eta_j||_2 <= 32000 n/m.                             (8)

This formula holds for any fixed v; restriction to moving columns is
made only after (8). The whole q_j,s includes stationary sites. Its
stationary half is the part that grows like kappa. It is excluded for
P_c v=v, rather than declared negligible in the complete model.

## 4. Exact moving read matrix and zero moment on EACH track

Let q_j,s^c=P_c q_j,s. It has coefficient

    b_S=1/((K+1)sqrt(2m)) on m/2 survivor sites PER track,
    b_D=-K/((K+1)sqrt(2m)) on m/(2K) donor sites PER track.

Thus EACH track has zero total sum, not just the pair of tracks together:

    (m/2)b_S+(m/(2K))b_D=0,
    ||q_j,s^c||_2^2=1/(2(K+1)).                           (9)

Let P denote the public cycle permutation in the full d-coordinate
cycle, and extend q by zero to its missing node0. All the indicated
translates lie away from node0/terminal in the allowed history geometry.
Then q_j,s^c=P^(s-1) q_j,1^c. The complete leading K-by-cycle matrix is

    Q_t[j,:]=g_H sum_(s=1)^t lambda^(t-s)(q_j,s^c)^T,
    A_lead=Q_t V,
    sigma_min(A_lead)^2=lambda_min(V^T Q_t^T Q_t V).        (10)

The last identity computes the exact gain for any chosen square K-probe
read matrix. It is a gain definition, not a robust lower bound.
Rows correspond to different axis endpoint comparisons, not simultaneous
linearization of a nonlinear section. Finite amplitude is already in (8).

The zero sums in (9) admit a discrete primitive b_j:

    q_j,1^c=(I-P^(-1))b_j.

On each track choose the primitive to vanish outside its length-m tuple
interval. Its coordinate magnitude is at most the total positive mass

    m/[2(K+1)sqrt(2m)].

All negative donor sites precede the positive survivor sites; arbitrary
ordering of donor groups does not change this cumulative bound. With two
tracks, each of length at most m,

    ||b_j||_2 <= m/[2(K+1)].                              (11)

No inversion of an ill-conditioned matrix and no future query data is
needed. This is an exact spatial primitive of a finite profile.

## 5. Geometric telescoping: increasing write length cannot recover kappa

For any isometry A and 0<lambda<=1, the identity

    sum_(u=0)^(t-1) lambda^u A^u(I-A)b
      = b-lambda^(t-1)A^t b
          -(1-lambda)sum_(u=1)^(t-1)lambda^(u-1)A^u b      (12)

is exact. The absolute sum of coefficients on the right is exactly 2,
including lambda=1. Hence its norm is <=2||b||, with no t loss.

Applying (12) with A=P^(-1), and factoring the isometry P^(t-1),
gives from (10)--(11)

    ||Q_t[j,:]||_2 <= m/(K+1),                            (13)
    sigma_min(Q_t V) <= ||Q_t V||_F/sqrt(K) <= m/(K+1).

The ordinary triangle inequality also gives

    ||Q_t[j,:]||_2 <= kappa/sqrt(2(K+1)),
    kappa=g_H sum_(u=0)^(t-1)lambda^u.

One may take the MINIMUM of this bound and (13). For unrestricted
parameter columns, (7) has ||q_j,s||_2=1/sqrt(K+1), so (8) gives (1b)
for the ENTIRE reference parameter-column row. This is independent of
V, its stationary/moving split, or any re-orthogonalization. In the
accepted range the complementary residual relative to kappa/sqrt(K)
is vanishing. The accepted stationary probes nearly attain this norm
budget, within a constant. They are not bypassed by a different basis.

Combining with (8), the full fresh read matrix has each row bounded by
m/(K+1)+32000n/m, which proves (1), using sigma_min<=||A||_F/sqrt(K).
Frobenius norm is used here ONLY for a matrix minimum-gain upper. It is
not substituted for the permitted-query metric or robust dimension.

For m~sqrt(n), t>=10n^(3/4), K<=n^(3/16), and kappa>=.998t,

    sqrt(K) sigma_min(A_cycle)/kappa
      <= [m sqrt(K)/(K+1)+32000 n sqrt(K)/m]/(.998t)
      =O(n^(-1/4)+n^(-5/32)) ->0.                         (14)

This is WORSE than the stationary kappa/sqrt(K) target. All constants
and the exact finite bound are (1); (14) only interprets it. Increasing
t with m fixed does not increase the leading cycle row (13).

Why an honest moving eigenmode does not circumvent this identity: a fixed
Fourier vector sees the translated q profile at its phase, but q's zero
moment contributes the factor (1-exp(i omega)), cancelling the long
geometric resolvent. A time-dependent v_s chosen to track q_j,s instead
would defeat (12), but would not be one fixed parameter action.

## 6. Whole inherited protocol: incoming credit, masks and corrections

Now use EXACTLY the accepted public m,t_e,L_d,L_mask,L_clear,T,N and the
same whole cube. Choose an axis (j,e): its two histories have theta_(j,e)
=+1 versus -1 and all other controls zero. The earlier histories agree;
all later gates agree by the accepted exact trace independence.

Before the selected stage, on ANY unit probe the identical incoming
survivor zero-sum component evolves identically and cancels. Its incoming
complement has operator norm at most

    B_0=16000n/m+N n^(-6).

Two propagated incoming complements cost <=2B_0. Thus at the end of the
early write, for the whole V-row of survivor common read,

    ||beta_early||_2 <= m/(K+1)+64000n/m+2N n^(-6).          (15)

The survivor DIFFERENCE is constant on all four sites of all survivor
tuples. Its fixed forcing cancels between histories; its only additional
source is the broadcast J difference. This remains true for nonconstant
forcing entries of V. Incoming survivor zero-sum credit cancels, not
because its original magnitude was small but because it reduces exactly.

Throughout the entire history ||M_t V||_op<=t<=N, so a two-history response
has operator norm <=2N. For the common low tail, the exact mean equation is
beta^+=a g_H(beta+sqrt(2m)Delta J). The complete J satisfies
||Delta J||_2<=3||Delta X||_op/sqrt(n). Norm contraction gives the
conservative tail/mask drift charge

    24N(L_d+L_mask)sqrt(10m/n).                            (16)

For clarity the mask calculation uses the two half means: beta_+ and
beta_- obey a g_+/- (beta_+/- +sqrt(m)Delta J) at EACH step. Their initial
values are beta/sqrt(2). The homogeneous protected read after L_mask is
beta[(a g_H)^L_mask-(a g_L)^L_mask]/2, of norm <=||beta||; summing the
broadcast driver of both halves is bounded by (16). All Householder
renewals, including earlier front slots, remain in the exact Delta J.
No common-cone sign assumption is used for moving forcings.

The last donor gates are the accepted analytic trace corrections,
.994<g_last<.996, with simultaneous perturbation norm bounded by their
maximum entry. The inherited pair response charge <=8N^2 n^(-5) is
included below. The corrections preserve the exact stage-independent
later word and common endpoint. They do not change the survivor gate
at the same step. After masking and clearing,

    Delta X=xi_e r_e^T+E,
    ||r_e||_2 <= B_move,
    B_move=m/(K+1)+64000n/m+2N n^(-6)
              +24N(L_d+L_mask)sqrt(10m/n)+8N^2 n^(-5),
    ||E||_op<=2N n^(-6).                                  (17)

The complete complementary difference contracts through the shared clear;
fresh forcing is identical and cancels. No discarded private forcing is
hidden in E. This statement is on responses, not an assertion that the
hidden state or sensitivity was reset to zero.

All later stages have identical words. The stored xi_e follows the exact
Walsh transformation simultaneously on all V columns; it remains zero
sum, supported on the same survivors, with spatial norm <=1. Thus at the
final reset the ideal difference is zeta_e r_e^T, with ||zeta_e||<=1,
and the propagated E still has norm <=2N n^(-6). No R-factor is needed
for this single AXIS comparison. It suffices to falsify a proposed
whole-boundary lower bound on the inherited section.

## 7. Actual all-query upper, dense comparison, and all-width envelope

The protected final support has 2m ordinary rows, far from the terminal
cycle boundary. For ALL legal future Q the accepted geometric envelope
there gives

    |c_Q^T zeta_e| <=100 sqrt(2m)/sqrt(n).

Combining this, (5), sigma<.051 and sqrt(l)<=sqrt(n),

    d_V <= 8 sqrt(m)B_move/n
             + .102 N n^(-13/2) +8e-9.                    (18)

This is a COMPLETE all-future upper for the SELECTED probes. It does not
use a chosen-witness lower, the old paired 8/n coefficient, or the
invalid global support-localization conjecture. The numerical 8 in (18)
comes independently from .051*100*sqrt(2)<8.

The accepted every-width envelopes give

    .99sqrt(n)<=m<=sqrt(n), N<11n^(29/32),
    L_d+L_mask<=3002 log n.

The first two terms in B_move cost less than 600000 n^(-1/4).
The drift contribution costs at most

    192*3002*sqrt(10) N m log(n)/n^(3/2)
        <3*10^7(log n)n^(-3/32).

The remaining terms are bounded explicitly by

    176 n^(-187/32) +7744 n^(-63/16)+1.122 n^(-179/32),

whose sum is <1e-9 on the stated range. These respectively charge the
incoming clear residue in B_move, trace correction, and full operator
clear residue. At n=10^1000, log(n)<3000 and n^(-3/32)<10^(-93),
so the drift envelope is <9*10^(-83); the first term is still smaller.
These elementary inequalities do not depend on sampled decimal widths.
Every envelope decreases for n>=10^1000, since log(n)>32/3. At that
threshold the two displayed vanishing terms sum to <1e-80. Adding the
conservative complete dense pair charge <=8e-9 proves (2).

Dense source/node0 coupling and future adjoint replacement are covered by
the inherited complete operator comparison, valid simultaneously for
all orthonormal probes. The corrected finite-N ledger is

    e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n],
    e_R<=4/(10^8 n^2), q_f<.941.

The historical erroneous display is NOT reused. No direct future term
survives the same endpoint/same-query comparison.

An axis maps to an axis under the accepted odd radial ball-to-cube map.
Since (2)<2epsilon, that pair rules out an all-boundary robustness proof
using only these selected moving-probe gradients on that section.
It does NOT rule out its accepted full-gradient robust lower bound or
another moving-probe section. No rank or parameter-count inference is
used in this finite-radius conclusion.

## 8. A probe-basis-independent dilution bound inside this history family

The same complete stage ledger (15)--(18) applies to V=I_r: all norm
estimates are operator bounds with unit forcing, independent of the number
of queried columns. Replace only its leading m/(K+1) by the unrestricted
row bound kappa_e/sqrt(K+1) from (1b). For the LAST-stage axis (j,R),
there are no later-mask losses to discuss. Thus the complete fixed-feature
actual distance obeys

    d_full(axis) <= 8 sqrt(m) kappa_R/[n sqrt(K+1)]
                      + Err(n,K,R),
    Err <= 600000 n^(-1/4)
                +3*10^7(log n)n^(-3/32)+9e-9.             (18b)

The SAME source feature, all legal future queries, full Householder
renewal and dense comparison are included. Reference source/node0 past
credit is public; its actual private leakage is in the dense charge.
This extension bounds the full fixed-feature gradient, not just V.
It still concerns this particular axis family and public stage protocol.

Whenever the displayed residual is <=epsilon and a robust section of this
specified cube/radial form requires that axis pair to exceed 2epsilon,
(18b) NECESSARILY gives

    kappa_R > epsilon n sqrt(K+1)/(8 sqrt(m)),
    t_R >= kappa_R > (1/8000)sqrt(K+1)n^(3/4),             (18c)

using epsilon=.001 and m<=sqrt(n). This does not derive a necessary
support cost from a chosen-query lower. It follows from a genuine complete
all-query UPPER and an actually required antipodal pair.

The residual proof applies on the accepted analytic envelope N<11n^(29/32)
and the inherited overheads; in particular it remains valid on reducing
the early write lengths while maintaining those overheads and trace legality.
It is not a claim for arbitrary durations beyond that envelope. The
shorter uncompensated durations O(2^(R-e)n^(3/4)), if substituted with the
same overhead protocol, therefore cannot keep a fixed margin as K grows:
the final-stage leading signal is O(1/sqrt(K)) and Err<epsilon.

Thus a probe change cannot reduce the scoped sqrt(K) duration requirement
in THIS history family. This is not a lower bound on the actual input
norm: no energy upper is reversed. New gates, simultaneous spatially
nonuniform writes, or multiple interleaved common projections may change
the argument's premises and remain open.

## 9. Genuine rotation eigenprobes: their small stationary tail is counted

Let phi be a unit, nonzero-frequency Fourier eigenvector of the original
public d-cycle P, extended by zero outside that cycle in R^k. For a real
basis use its normalized sine and cosine partners. Sum(phi)=0. The
physical eigenprobe v=U phi satisfies

    v_0=0,
    v_z=gamma phi_0/sqrt(k) for every off-cycle z,
    ||v||=1, O_*v=e^(i omega)v                           (complex notation).

For real partners, the plane rotates rather than giving a real scalar
eigenvalue. U is orthogonal, so distinct real Fourier basis vectors yield
Frobenius-orthonormal recurrent actions with the same source. Sine modes
have phi_0=0 and are moving-only. All off-cycle tails of the cosine modes
lie in the ONE stationary all-ones off-cycle direction.

For K such orthonormal probes, |phi_0|<=sqrt(2/d) implies, for all large
n in our range,

    ||P_o V||_op <=4 sqrt(K/n).                            (19)

This is an INCLUDED tail, not a new source feature or a free baseline.
Linearity in parameter probes gives Delta M V=Delta M P_c V+
Delta M P_o V. The first part obeys (18), since ||P_c V||_op<=1;
orthonormality was not needed for that upper. The second part has full
op norm <=2N||P_o V||_op, so (5)'s generic all-query cap adds at most
.102N||P_o V||_op/sqrt(n), giving (3).

Since N<11sqrt(K)2^R n^(3/4) and K2^R<=n^(3/16), this additional charge
is <5 n^(-1/16), which is already <1e-60 at the threshold. Therefore
these genuine eigenprobes also cannot replace the accepted stationary
probe family with a robust no-dilution section on the same protocol.
The tail has rank at most one; it cannot supply K independent stationary
amplifiers by relabeling them as moving eigenprobes.

## 10. Full energy, scope ceiling, and what remains open

The histories, source, lift and endpoint are exactly the accepted ones.
Selecting parameter probes changes no physical input. Thus all actual
inputs, including zero-start preparation, donor and survivor drives,
compensators, dense inverse lift, trace matching, masks, clearing and
reset, satisfy

    ||X||<=2sqrt(m(T+2)+1)
         <7K^(1/4)2^(R/2)n^(5/8),
    mT<11sqrt(K)2^R n^(5/4).

The public bath is autonomous and no public trajectory is subtracted.
These are upper bounds and are not reversed into energy necessities.
A shared reset does not erase private credit; it is included in (17)--(18).

No new D is established on moving probes. The accepted stationary result
still provides D=KR and, for R=2, D>=n^(3/16)/3. Its polynomial exponent
is unchanged, and its whole admitted range has mT<11n^(45/32)=o(n^(3/2)).
The fixed-feature superlinear threshold remains [1/4,3/4] up to slow
factors; best superlinear construction remains Omega(n log n) at
O(n^(3/4)(log n)^(3/2)). The full-model bounds are unchanged.

Any fixed K-probe response at a common endpoint factors through nK actual
sensitivity coordinates, so its general topological ceiling is D<=nK;
that is not an achieved lower. In the unchanged cube the family has KR
controls and the inherited admissible range already makes KR=o(n).
No conclusion about arbitrary growing K,R follows outside this range.

The exact remaining lemma is not independence of translated probe rank.
It is a shared write/read operator with multiple nonzero temporal/spatial
moments, having a UNIFORM finite-radius minimum gain on one B^(KR),
without reducing each probe to the single survivor common projection (7).
A multi-survivor/Hadamard-interleaved geometry is the most useful next
candidate: its full cross-response and legal-read minimum gain must be
proved jointly and under the same absolute energy and endpoint contract.
