# Filtered timing: complete-query upper bounds and the missing packing premise

Codex, 2026-10-05. New author derivation, pending independent review.
D=2 is accepted by the owner and is not reconsidered. This folder does not
change any accepted historical theorem. The general packing problem is STILL OPEN.

## 1. Scope, conventions, and dependencies

We study only the frozen moving-corridor fixed-source-feature channel.
n >= 10^6, a=1-1/n, l=n-floor(n/2), .0499<sigma<.051,
N=T+1 includes the public reset. Source preparation precedes time 1 and
has zero recurrent-parameter forcing. All realized inputs are frozen when
differentiating. The source state is sigma times the all-ones vector
throughout these N steps. Both histories have the same exact actual endpoint.

Dependencies: ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md,
sections 1--5, 8--10 and 12; ../codex_private_renewal_gamma_20261003/PROOF.md,
sections 3--4 and 10; the corridor construction in
../codex_holding_cost_attack_20261003/PROOF.md.
We use their accepted lift, public schedule, ordinary-coordinate adjoint
bound and dense comparison. We do not use the disputed packing conclusion.

For the reference selected-memory operator,

    M_0=0, M_t=G_t(a O_* M_{t-1}+I_r),
    O_*=C+1_r u^T+e_1 v_H^T, J_t=u^T M_t,
    nu(A)=(sigma sqrt(l)/n) sup_legal Q ||A^T c_Q||_2.       (1)

The supremum includes EVERY permitted future horizon L_Q>=1.
The head is 1_n/sqrt(n); group normalization is exactly 1/n.
q_f=sech^2(.25)<.941 and ||c_Q||_2<=q_f^{L_Q}<=q_f.
Reference-to-actual complete pair-distance charge is <=8e-9.
The stronger bounds in section 4 below are derived directly for the
ACTUAL dense recurrence, so those bounds need no dense charge.

Three meanings of packet must be separated:

* A gate-modification window: the two gate words differ only during I.
  The resulting difference includes changes to transport of ALL older credit.
* An injection-age window: the contribution of fresh feature forcings at
  times in I, including their ENTIRE subsequent transport.
* A final output-supported component: a matrix whose output rows really
  vanish outside an explicitly specified set S.

These are different objects. A local gate window need not be output-supported,
nor confined to the fresh forcings injected in that window.

## 2. Exact suffix-filter identity and finite-error difference

For a tuple row, including all Householder renewals in J,

    V_{i,t}=a g_{i,t}(V_{i,t-1}+J_{t-1}), V_{i,0}=0,
    w_{i,j}=a^{T-j+1} product_{s=j}^T g_{i,s},
    V_{i,T}=sum_{j=1}^T w_{i,j} J_{j-1}.                  (2)

J and V are ROW VECTORS in parameter-coordinate space, not scalars.
Equivalently w=aK for the historical K=a^{T-j} product g.
There is no further factor a in the sum if w is defined as in (2).

For two histories the exact identity is

    Delta V_{i,T}
      =sum_j w_{i,j} Delta J_{j-1}
       +sum_j (w_{i,j}-w'_{i,j}) J'_{j-1}.                (3)

At public reset,

    V_{i,N}=a q_N(V_{i,T}+J_T),
    Z_N=a q_N(Z_T+J_T),
    Delta(V_{i,N}-Z_N)=a q_N Delta(V_{i,T}-Z_T).           (4)

The cancellation in the last line does NOT remove the private forcing
from Delta Z_N or from the complete sensitivity.

Erasure: if the last L gates are <=g_L<1, each weight with j<=T-L
is <=g_L^L. Thus the norm of the prefix contribution to ONE filter is
at most g_L^L sum_{j<=T-L} ||J_{j-1}||. It is not an erasure theorem for
J, for the other rows, or for the complete history difference.

Flat window: if every g in the window is >=1-eta, then

    w_j/w_T=a^{T-j} product_{s=j}^{T-1} g_s,
    0<=1-w_j/w_T<=(T-j)(eta+1/n).                         (5)

Consequently V_T=w_T sum_j J_{j-1}+R with

    ||R||<=w_T T(eta+1/n) sum_j ||J_{j-1}||.              (6)

This gives one SHARED VECTOR, not one scalar sufficient statistic.
It gives one scalar only after an additional fixed-parameter-probe
restriction. A theorem about that restriction is not a complete-query theorem.

## 3. Complete reference query ledger

The exact decomposition retained by the accepted renewal proof is

    Delta H_N=1_r Delta Z_N
       +sum_i 1_tuple_i [Delta V_{i,N}-Delta Z_N]
       +sum_{z=1}^N e_z [Delta F_{z,N}-Delta Z_N].         (7)

All-legal-future estimates give

    nu(Delta H_N) <= (sigma sqrt(l)/n) [
       102 ||Delta Z_N||
       +(400/sqrt(n)) sum_i ||Delta V_{i,N}-Delta Z_N||
       +(100/sqrt(n)) sum_{z=1}^N ||Delta F_{z,N}-Delta Z_N|| ]. (8)

The full operator is Delta M_N=Delta L_N+Delta H_N.
Equation (8) is an UPPER ledger, not separately achievable maxima.
It retains the same legal query for every term before applying triangle
inequalities. No old paired 8/n coefficient is assigned to private H.

For a selected packet of h ordinary output rows with common row b^T,
nu(1_S b^T) is at most

    (sigma sqrt(l)/n) min(100h/sqrt(n), q_f sqrt(h)) ||b||. (9)

But (9) controls only that output component. It omits the bulk/front/direct
terms if it is substituted for the distance between two actual histories.
The full metric depends on all parameter directions in b, not just b v
for a chosen unit probe v.

## 4. THEOREM: exact dense, age-weighted gate-window bounds

Normalize the ACTUAL fixed-feature sensitivity by sigma sqrt(l). Allowing
all differentiated recurrent output rows, it obeys

    mathcal M_0=0,
    mathcal M_t=G_t(R mathcal M_{t-1}+I_n), ||R||=a.       (10)

Restricting differentiated rows replaces I_n by a fixed inclusion of norm
one and leaves the following proof unchanged. Preparation forcing is zero.
All forcing terms have the same constant source value. Source, node-zero,
Householder feedback, and reset transport are included in (10).

Define b_t=(1-a^t)/(1-a)<=min(t,n). Individual operator norms are <=b_t.
For a pair define

    bar G_t=(G_t+G'_t)/2, Delta G_t=G_t-G'_t,
    bar M_t=(mathcal M_t+mathcal M'_t)/2,
    A_t=R bar M_{t-1}+I_n.

Then ||A_t||<=b_t and, EXACTLY,

    Delta mathcal M_t=bar G_t R Delta mathcal M_{t-1}
                           +Delta G_t A_t.              (11)

No renewal or gate-defect expansion is truncated. Suppose differences
are confined to I=[s,e] (include every trace-correction step if necessary).
Let delta_t=max_z |g_{t,z}-g'_{t,z}| and

    d_t=max_z (g_{t,z}-g'_{t,z})^2/(1-bar g_{t,z}^2),     (12)

with 0/0 defined as 0. Gates are in [0,1]; bar g=1 implies Delta g=0.
Thus d_t is finite and d_t<=2 delta_t. If all changed gates are >=.99,
the stronger d_t<= (200/199) delta_t holds.

For EVERY actual legal future, take its adjoint c with ||c||<=q_f.
Define p_N=c and p_{t-1}=R^T bar G_t p_t. Variation of constants yields

    (Delta mathcal M_N)^T c=sum_{t in I} A_t^T Delta G_t p_t. (13)

In particular the complete ACTUAL pair distance d_actual satisfies

    d_actual <= (sigma sqrt(l)/n) q_f
                sum_{t in I} a^{N-t} b_t delta_t.        (14)

This includes all older credit affected by the changed gates.

A sharper dissipation estimate follows from

    ||p_t||^2-||p_{t-1}||^2
       >=p_t^T(I-bar G_t^2)p_t=:ell_t>=0.                (15)

Here only ||R||<=1 is required. Telescope on I to obtain
sum_{t in I} ell_t<=||p_e||^2<=a^{2(N-e)}q_f^2.
Also ||Delta G_t p_t||<=sqrt(d_t ell_t).
Cauchy--Schwarz in (13), now with a proven dissipation budget, gives

    d_actual <= (sigma sqrt(l)/n) q_f a^{N-e}
                    sqrt(sum_{t=s}^e b_t^2 d_t).         (16)

This is a finite-error bound on the complete legal-query supremum, not an
RMS substitution. Using l<=n and sigma<.051 gives coefficient <.047991/sqrt(n).
Combine (14),(16) with the unconditional pair diameter

    d_actual <=2(sigma sqrt(l)/n) q_f b_N
               <.095982 b_N/sqrt(n).                    (17)

For duration L=e-s+1 and delta_t<=delta, (16) implies

    d_actual < .047991 a^{N-e} b_e sqrt(2 L delta)/sqrt(n). (18)

If the pair distance is >2epsilon=.002, a NECESSARY condition is

    sum_{t=s}^e b_t^2 d_t
       > (2epsilon n/(sigma sqrt(l) q_f))^2 a^{-2(N-e)}
       > .001736 n a^{-2(N-e)}.                         (19)

This is a genuine time/gate-dissipation restriction. It does not supply a
support-size restriction: late gate writes may act on credit accumulated
before I, through the factor b_t. Nor does it count continuous dimensions.
Changing the source trajectory or using unequal endpoints would require
new forcing/direct-term ledgers; those are not the histories studied here.

## 5. THEOREM: spatially resolved gate-window bound, with renewal leakage

A reference ordinary column z away from the terminal d-1 satisfies

    ||(O_*-C)e_z|| <= (gamma^2+gamma)/sqrt(k)<6/sqrt(n).   (20)

The decimal in (20) is uniform, not a sample-width claim: for n>=10^6,
gamma<1.002 and sqrt(n/k)<1.415, so the coefficient is
<(1.002^2+1.002)*1.415<2.84<6.
The characteristic from each changed tuple site remains ordinary through
reset, by the corridor's no-wrap geometry. Under the midpoint past gates,
expand a propagated unit column by its FIRST departure from this
characteristic, not by the total number of feedback insertions.
Each remainder thereafter uses the full operator a bar G O_* of norm <=a.
This is an exact telescoping identity, with ALL later renewals retained.

For age v=N-t its deviation from the bare characteristic has norm
<=6v a^v/sqrt(n). Its bare endpoint is an ordinary active/reset row, whose
all-future adjoint coefficient is <=100/sqrt(n). Since ||c_Q||<=q_f,

    |p_{Q,t,z}|<=a^v(100+6q_f v)/sqrt(n).                (21)

For a support S_t of s_t changed physical sites, the sharper of the
coordinate bound and the full contraction bound gives

    Lambda(t,S_t):=sup_legal Q ||P_{S_t}p_{Q,t}||
       <=a^{N-t} min(q_f,
                    sqrt(s_t)(100+6q_f(N-t))/sqrt(n)).   (22)

Apply (13) in the reference recurrence to obtain the COMPLETE reference upper

    nu(Delta M_N) <= (sigma sqrt(l)/n)
       sum_{t in I} b_t delta_t a^{N-t}
          min(q_f, sqrt(s_t)(100+6q_f(N-t))/sqrt(n)).     (23)

For actual distances add the accepted <=8e-9 complete pair charge.
This proof is nonperturbative: norm contraction controls every path after
its first departure. It is not a first-Householder-insertion truncation.

If s_t<=h, set
W_I=sum_{t in I} b_t delta_t a^{N-t}(100+6q_f(N-t)).
Using l<=n, an actual robust pair requires

    h > [ (2epsilon-8e-9)n/(.051 W_I) ]^2.              (24)

This is one valid support/window necessity. It is MUCH weaker than the
historical h >= const n^2/T^2: a long gate window gives W_I=O(T^3)
even when delta is constant. It therefore does not establish the old
packing rate. The leakage factor cannot simply be removed; (22) would
require a NEW history-uniform past-adjoint leverage theorem to do so.
For windows with zero changes W_I=0 the pair has zero reference difference,
and cannot be robust after the dense charge.

## 6. THEOREM: fresh-injection age-window upper

For a FIXED history, the contribution of feature injections only at j in I is

    mathcal M_N^[I]
      =sum_{j in I} Phi_G(N,j)G_j,                       (25)

where Phi includes ALL dense transport and feedback. Hence for two histories

    d_actual^[I] <=2(sigma sqrt(l)/n)q_f
                        sum_{j in I} a^{N-j}
                   <.095982 |I|/sqrt(n).                (26)

A >.002 signal carried SOLELY by this difference therefore requires
sum_{j in I} a^{N-j}>.020837 sqrt(n). Disjoint injection windows supplying
separately robust scalar coordinates, with all other contributions fixed
on each coordinate-axis pair, number at most

    P < .095982 N/(2epsilon sqrt(n)).                   (27)

This is an actual all-query time-packing theorem under the stated
attribution premise. Gate-window changes generally alter the contributions
of earlier injection windows too. Thus (26) cannot be applied by equating
a donor gate epoch with its fresh-injection window. Nor is the number P
of windows a dimension bound for arbitrary vector-valued packets.

## 7. Precisely when the historical support packing can be repaired

Suppose a pair's COMPLETE reference matrix difference A=Delta M_N has
output support S, with h=|S| ordinary corridor rows and no other output
difference. Then ||A||<=2b_N and every legal adjoint satisfies
||P_S c_Q||<=100 sqrt(h)/sqrt(n). Therefore

    d_actual <=10.2 b_N sqrt(h)/n+8e-9.                 (28)

It is necessary for a robust pair that

    h > [ (2epsilon-8e-9)n/(10.2 b_N) ]^2.              (29)

This is the CORRECT upper-bound version of the historical inference,
with the explicit and indispensable complete-output-support premise.

For P scalar packets, require one joint B^P parameter family, disjoint
final ordinary supports totaling <=4m, and every coordinate-axis
antipodal difference confined to its own support. Applying (29) to those
actual boundary pairs gives

    P < 4m [10.2 b_N/((2epsilon-8e-9)n)]^2
        =O(m(T+1)^2/n^2).                              (30)

If T=O(n), mT=o(n^(3/2)), this is o(sqrt(n)). D=P ONLY for the expressly
one-scalar-per-packet section. No dimension count for arbitrary packet
families follows. Disjoint support by itself does not imply one scalar per
packet, or that all B^D boundary differences are detectable.

The inherited corridor does NOT meet the premise of (28) merely because
survivor supports are disjoint. To see this exactly, at the first interior
step M_1=G_1. At the public reset of a T=1 packet,

    M_2=G_2(a O_* G_1+I).
    For a far public bath row z and a changed ordinary tuple column w,
    (Delta M_2)_{z,w}=-a q_2 (gamma^2/k) Delta g_{1,w}.   (31)

It is nonzero although z is outside every driven survivor site. This is
an admissible, same-endpoint corridor word whenever the inherited geometric
premises hold. The public bath STATE has not changed; its credit has.
Equation (31) is an exact counterexample to the REQUIRED LOCALIZATION
PREMISE, not a fixed-epsilon counterexample to (28).

The accepted long-packet equal-code counterexample has private distance
>.03 and shows that ignoring the renewal can fail at finite error too.
It does not refute every conceivable packing inequality. No >.002
counterexample to a well-specified stronger all-query packing theorem
has been constructed in this audit.

## 8. Continuous dimension and the precise remaining statement

Neither (19), (24), nor a count of epochs is a Borsuk--Ulam dimension proof.
A complete code or a joint robust section is still required.

For the entire family, exact storage of M_N gives at most r^2 reference
credit coordinates (or the full actual matrix for exact dense storage).
The gate word has mT parameters, so any robust section factorizing through
that admitted word satisfies D<=mT: if D>mT, its boundary maps continuously
to R^(mT), and Borsuk--Ulam supplies identical antipodal words.
These inherited elementary bounds do not close the long corridor.

For the original support-packing route, the smallest missing claim is:

    A COMPLETE history-uniform, all-future adjoint leverage/localization
    estimate must control the effect of one donor packet, INCLUDING its
    induced Delta J, bath/front response and older-credit transport,
    strongly enough to replace W_I in (24) by O(T), AND a continuous
    scalar/low-coordinate packet factorization must be supplied before
    interpreting packet count as D.

These are not proved by suffix filtering. A cleaner next target is the
leverage quantity Lambda(t,S_t) in (22) for the actual corridor midpoint
gate trajectories. Prove a stronger bound using renewal sign structure,
or give an explicit legal history where the age-dependent term is necessary.
This is one focused mathematical test; no spatial-write work is used.

## 9. Conclusion

New complete finite-error upper bounds (14),(16),(23),(26) are proved here.
The historical support/time packing law is conditionally repairable via
(28)--(30), but its needed complete localization/scalar premises are absent
from the inherited construction. Unconditional D=o(sqrt(n)) remains
UNPROVED. D=2 stays accepted. The complete long corridor remains open.
No new energy exponent, global impossibility edge, or full-model result
is claimed. The [1/4,3/4] threshold bracket is unchanged.
