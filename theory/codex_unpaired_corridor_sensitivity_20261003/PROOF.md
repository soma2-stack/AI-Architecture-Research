# Unprojected corridor credit and its common-mode renewal kernel

Codex, 2026-10-03. **NEW structural theorems, pending hostile review.**
The owner accepts the preceding corridor lift and paired projected
obstruction. Neither is reopened. No exponent below 3/4 is claimed here.
This stage derives complete fixed-source-feature credit, not just the paired
frame, and isolates the remaining unpaired channel.

## 1. Frozen model, differentiation, and indexing

Use n>=10^6, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
lambda=1/(100n), b0=.05, W=I, R0=diag(aO,lambda I_l),
O=UPU, U=I-gamma ww^T, w=e0-1_k/sqrt(k), gamma=1/(1-1/sqrt(k)).
The ACTUAL frozen R has ||R||op=a and e_R=||R-R0||op<=4/(10^8 n^2).

Fix public m,T,S=m+T+4<=d/100, A=2S,B=5S. Each row i has two moving
cycle sites c_i^A(t)=A+i+t,c_i^B(t)=B+i+t and two fixed off-cycle
compensators o_i^1,o_i^2. All four gates are g_(i,t)=1-beta_(i,t)^2,
0<beta<.1. The cycle states are +beta; compensator states are -beta.
Nondriven reference states and the bath are public. All histories start at
the public zero state and have the exact same nonzero endpoint after reset.

Here t=0 is AFTER preparation; h_(-1)=0. Interior times are 1,...,T;
N=T+1 is reset. Preparation has raw input x0 and source state sigma*1_l,
where sigma=tanh(lambda sigma+.05), .0499<sigma<.051. Reset does not reset
the source; its state remains sigma*1_l. Current h0 in this indexing is not
the public zero START h_(-1).

For arbitrary independently differentiated R,W,b, holding every realized
raw input fixed, the full differential is EXACTLY

    S_t[delta theta]=G_t(R S_(t-1)[delta theta]
                         +delta R h_(t-1)+delta W x_t+delta b),
    G_t=diag(1-h_t^2), S_(-1)=0.                         (1)

Thus the R-, W-, b-block forcings are respectively delta R h_(t-1),
delta W x_t, delta b. Equivalently, for t=0,...,N,

    S_N[delta theta]=sum_t Phi_R(N,t) G_t
                        (delta R h_(t-1)+delta W x_t+delta b),
    Phi_R(N,t)=(G_N R)...(G_(t+1) R), Phi_R(N,N)=I.       (2)

Preparation R forcing is zero, but preparation W and b forcing is NOT zero.
No derivative of the inverse-lift control policy is included in (1).

For the accepted fixed feature f_s=1_l/sqrt(l), let E embed coordinates
1,...,k-1 of memory and take delta R=(Ev) f_s^T. The complete reference
sensitivity for ALL v in R^r is

    S_t[v]=sigma sqrt(l) E M_t v,
    M_0=0, M_t=G_t^m(a O_* M_(t-1)+I_r), 1<=t<=N,       (3)

where G^m is the selected memory gate restriction and O_*=E^T O E. No
paired projection is taken. The source and node-0 sensitivities for this
action are zero in R0. If the fixed-feature parameter action also includes
rows outside E, their reference source/node-0 response is public; dense
coupling is treated separately below.

## 2. Exact rank-two Householder identity

Physical memory coordinates are indexed 0,...,k-1; E excludes coordinate0.
On R^r define C by

    (Cv)_1=0,
    (Cv)_j=v_(j-1), 2<=j<=d-1,
    (Cv)_j=v_j, d<=j<=k-1.

Define PUBLIC row vectors

    u^T=(gamma/sqrt(k)) e_(d-1)^T-(gamma^2/k)1_r^T,
    v_H^T=(gamma/sqrt(k))1_r^T.

Direct expansion of UPU, not differentiation of state cancellation, gives

    O_*=C+1_r u^T+e_1 v_H^T.                            (4)

This is an exact open cycle shift, off-cycle identity and two feedback
outer products. For any credit matrix define ROW VECTORS

    J_t=u^T M_t, B_t=v_H^T M_t.                          (5)

These are history-dependent vectors in parameter-coordinate space, NOT
two scalar statistics. Each has r coordinates. Their small number of rows
does not establish a small continuous credit-memory dimension.

## 3. Exact local-plus-feedback decomposition

Define the auxiliary direct-path matrix and feedback matrix

    L_0=0, L_t=G_t^m(a C L_(t-1)+I), H_t=M_t-L_t.

Subtracting recurrences gives the exact causal triangular system

    H_0=0,
    H_t=a G_t^m C H_(t-1)
            +a G_t^m[1_r J_(t-1)+e_1 B_(t-1)].          (6)

Although (6) is linear in its forcing, J and B are computed from L+H,
so it is a coupled renewal system, not an external public forcing.
With Phi_C(t,s)=(aG_t^m C)...(aG_(s+1)^m C),

    H_t=sum_(s=1)^t Phi_C(t,s) aG_s^m
                          [1_r J_(s-1)+e_1 B_(s-1)].   (7)

Equation (7), together with (3)-(5), is an EXACT unpaired kernel including
all orders of Householder transport. It does not omit path interference.

## 4. Local kernels, four-site modes, and signed channels

For j<=t<=T put

    k_(i,j;t)=a^(t-j) product_(s=j)^t g_(i,s),
    kappa_(i,t)=sum_(j=1)^t k_(i,j;t).

The direct cycle row at c_i^A(t) has coefficient k_(i,j;t) in parameter
column c_i^A(j), and zero elsewhere; likewise for the B track. Each
compensator row is kappa_(i,t)e_(o_i)^T. Outside the active set the direct
rows are public. The chronological injections that collide at a physical
parameter column are summed; they are not independently selectable.

Use the following orthonormal OUTPUT modes on each four-site tuple:

    p_i=(e_cA-e_cB)/sqrt(2),
    o_i=(e_o1-e_o2)/sqrt(2),
    b_i=(e_cA+e_cB-e_o1-e_o2)/2,
    s_i=(e_cA+e_cB+e_o1+e_o2)/2.                        (8)

The accepted paired frame is the cycle-exchange ANTISYMMETRIC p mode
between two POSITIVE copies. It is not a positive-versus-negative state sum.
The state balance is 2 beta b_i. The first three modes have zero sum;
the last has sum2. Before wrapping, O maps each zero-sum co-moving mode
to its next-time counterpart and matched gates multiply it by g_i.

For the complete output rows of (3), the exact projected recurrences are

    p_i(t)^T M_t=g_i,t[a p_i(t-1)^T M_(t-1)+p_i(t)^T],
    o_i^T M_t=g_i,t[a o_i^T M_(t-1)+o_i^T],
    b_i(t)^T M_t=g_i,t[a b_i(t-1)^T M_(t-1)+b_i(t)^T],
    s_i(t)^T M_t=g_i,t[a s_i(t-1)^T M_(t-1)
                                  +2a J_(t-1)+s_i(t)^T]. (9)

The first three OUTPUT projections remove feedback exactly. The common
mode does not. Constant INPUT parameter modes cannot all be replaced by
their co-moving versions at each injection time; (9) does not license
selecting parameter columns separately at every step.

## 5. New common-mode kernel and an exact row-level realization

On all FOUR active rows of tuple i the feedback H_t has the SAME row
vector V_(i,t). Gates agree, initial H0=0, and the predecessor of each row
is its matching cycle/identity row. Thus

    V_i,0=0,
    V_(i,t)=a g_i,t[V_(i,t-1)+J_(t-1)],
    V_(i,T)=a sum_(j=1)^T k_(i,j;T) J_(j-1).             (10)

This is a product kernel with PRIVATE VECTOR-VALUED weights, rather than
a monotone scalar row. State signs disappear from the fixed-source forcing
but not from gates or the common sensitivity response.

Let q_t=1-u_t^2 be the public ordinary bath gate. All far, nondriven
ordinary feedback rows share a row vector Z_t satisfying

    Z_0=0, Z_t=a q_t[Z_(t-1)+J_(t-1)].                  (11)

The public exceptional front is contained in rows1,...,t. Write its
feedback rows F_(z,t) and their PUBLIC gates f_(z,t). They satisfy

    F_(1,t)=a f_(1,t)[J_(t-1)+B_(t-1)],
    F_(z,t)=a f_(z,t)[F_(z-1,t-1)+J_(t-1)], 2<=z<=t.   (12)

Every other feedback row equals Z_t. Therefore, with S_L(t)=1_r^T L_t,

    S_M(t)=S_L(t)+(r-4m-t)Z_t+4 sum_i V_(i,t)+sum_(z=1)^t F_(z,t),
    J_t=(gamma/sqrt(k))[e_(d-1)^T L_t+Z_t]-(gamma^2/k)S_M(t),
    B_t=(gamma/sqrt(k))S_M(t).                         (13)

Terminal row d-1 is outside both private sets and front. The two moments
and (10)-(13) give an exact common-mode renewal system, INCLUDING cross-row
coupling and the bath. All quantities on the right are row vectors except
public scalar coefficients. The full private feedback is

    Delta H_t=1_r Delta Z_t
       +sum_i 1_(tuple_i(t))[Delta V_(i,t)-Delta Z_t]
       +sum_(z=1)^t e_z[Delta F_(z,t)-Delta Z_t].         (14)

The word Delta denotes the difference of TWO histories throughout (14).
No separate-axis inference is made.

One exact online realization stores the current m-by-t product array
(shared by both cycles; its row sums give the compensator traces), together
with m vectors V_i, one vector Z and t front vectors F_z. Public remaining
direct rows are supplied by the public schedule. Its explicit credit count
is at most

    m t+r(m+t+1).                                      (15)

This is a nonminimal exact upper, not O(n) and not a robust lower. J,B and
S_L are temporary computations. Ordinary forward state, if required, must
be counted separately; no hidden vectors are declared free. At reset the
last product entries are public but retaining them is harmless for the
upper. The usual full M state gives the alternative exact r^2 count.

## 6. Prefix-suffix crossover: a new nonharmonic path component

Expand the finite product of C+(O_*-C) by the number of Householder
insertions. This is an exact finite path expansion, not a convergent
small-perturbation claim. The one-insertion term is

    H_t^(1)=sum_s Phi_C(t,s) aG_s^m(O_*-C)L_(s-1).     (16)

Consider injection at time s into cycle row c_h^A(s), transport along its
active characteristic h until a Householder insertion at time j>s, then
transport on active characteristic i to T. The uniform u part has exact
coefficient

    A_(i,h,s)=-(gamma^2/k) a^(T-s)
       sum_(j=s+1)^T [product_(v=j)^T g_(i,v)]
                       [product_(v=s)^(j-1) g_(h,v)].  (17)

There is an identical formula for the B injection track. For compensator
parameter o_h, sum (17) over s because all injection times have that SAME
physical parameter column. Likewise overlapping cycle columns require
summing over (h,s) with c_h(s)=z. Other local-public paths and the e1
insertion are also present in (16); (17) is not incorrectly called the
entire parameter entry.

For h=i the sum collapses to (T-s)k_(i,s;T), times -gamma^2/k. For h!=i
it splices two different gate words. It is not one nested monotone row.
The full response includes two and higher insertions through (10)-(13).
The entries in (17) are not independent parameters.

There is a useful exact variation bound. Remove -gamma^2/k from (17) and
write the remaining positive sequence as P_s, with P_T=0. It satisfies

    P_s=a g_(h,s) P_(s+1)+f_s,
    f_s=a^(T-s)g_(h,s) product_(v=s+1)^T g_(i,v), 0<=f_s<=1.

Set d_s=(1-a g_(h,s))P_(s+1)>=0. Telescoping P_s-P_(s+1)=f_s-d_s gives
sum_s d_s=sum_s f_s-P_1. Therefore

    TV(P)=sum_s|P_s-P_(s+1)|<=2sum_s f_s-P_1<=2(T-1),
    TV(A_(i,h,.))<=2 gamma^2(T-1)/k.                    (18a)

So the first crossover is an inhomogeneous positive triangular row of
bounded variation O(T/n), not an unconstrained operator row. This does NOT
prove a small code for the COMPLETE feedback: physical columns sum multiple
(h,s) paths, compensator columns sum all ages, and higher insertions remain.

## 7. Private sensitivity really exists, despite public states

This conclusion is exact, not a tangent-rank count. Already at interior
t=1, M1=G1. At t=2,

    H2=aG2(O_*-C)G1.

For any far ordinary bath row z and ordinary parameter column w of a
tuple whose first gate varies,

    (H2)_(z,w)=-a q2(gamma^2/k)g_(i,1).                 (18)

The bath STATE is public, but this SENSITIVITY is private. T=1 followed
by public reset gives exactly the same example at the common endpoint.
Each changed tuple supplies a rank-one feedback term aG_reset r_H Delta g
on its four input columns, with
r_H=-(gamma^2/k)1_r+(gamma/sqrt(k))e1. This term is nonzero.

Legal one-step gate boxes have interior. Since O_* is invertible and
finite-time reset gates are positive, some permitted query sees this
nonzero reference term. This proves exact query visibility, NOT visibility
above epsilon or a width-independent robust section. Actual dense credit
is handled by the uniform comparison below, not by assuming all small
reference terms exceed that comparison error.

## 8. Reset and full energy ledger

Reset has PUBLIC G_N, not zero G_N. Consequently

    M_N=G_N(a O_* M_T+I),
    V_(i,N)=a q_N[V_(i,T)+J_T],
    Z_N=a q_N[Z_T+J_T].                                 (19)

The common forcing J_T cancels in V_i,N-Z_N, but neither feedback nor
old credit is erased. Direct cycle entries are a q_N k_(i,j;T), plus the
public new injection q_N. Compensator trace is a q_N kappa_i,T+q_N.

All gates in this stage belong to the SAME accepted lift, with beta=sqrt(1-g),
paired +beta/-beta states, public bath and common reset. The complete actual
history cost remains the accepted UPPER

    ||X||2<=2sqrt(m(T+2)+1).                             (20)

No public input center is subtracted. No energy lower is inferred from (20).

## 9. ACTUAL legal-query metric and channel coefficients

Every future preactivation is in [.25,.75]^n; future raw controls realize
these preactivations and are then frozen for differentiation. Let
q_f=sech^2(.25), g_lo=sech^2(.75), g_hi=q_f. For L>=1 let c_Q be the
UNNORMALIZED reference effective adjoint of head1_n/sqrt(n), restricted
to E. Define the exact reference fixed-feature pseudometric

    nu(A)=(sigma sqrt(l)/n) sup_(legal Q)||A^T c_Q||2.   (21)

Its one-step subset is EXACTLY

    nu_1(A)=(sigma sqrt(l)a/(n sqrt(n)))
               max_(g in [g_lo,g_hi]^r)||A^T O_*^T g||2. (22)

There is no RMS replacement or arbitrary unit-adjoint assumption. Longer
queries are retained in (21). ||c_Q||<=q_f^L gives a valid uniform upper
nu(A)<=sigma sqrt(l)||A||op/n, not an equivalence to the operator norm.
For the decimal bounds below, cosh(1/4)>1+(1/4)^2/2=33/32 proves
q_f<1024/1089<941/1000 exactly; numerical agreement is not the proof.

Ordinary active and front rows are far from wrapping, and off-cycle rows
do not wrap. The accepted leakage argument applies individually to these
rows: |c_Q,z|<=100/sqrt(n). For the FULL Householder block it does not apply
globally, since it also has terminal-row/bath support. For instance the
legal all-high one-step query has

    c_(d-1)=a g_hi[ sqrt(k)+1-gamma ]/sqrt(n)>.66
    at n>=10^6.                                        (23)

This directly forbids a universal 100/sqrt(n) coordinate dilution bound.
It does not prove the reachable private operator can exploit that row with
many independent finite-margin degrees.

The uniform bath has its own structure:

    O_*1_r=sqrt(k)e1-(gamma/sqrt(k))1_r.

After the first future step the main term is an ordinary near-origin
column; its all-horizon bound and the remainder's full norm give
|c_Q^T1_r|<=102 for all L>=1. Before wrapping use the same q_f^L(1+6L)
envelope as for ordinary columns; after n/8 steps use q_f^L sqrt(r)<=1.
For zero future steps this bath bound is FALSE; L>=1 is the accepted contract.

Using (14), the following all-legal-query upper is therefore valid:

    nu(Delta H_N) <=(sigma sqrt(l)/n){
        102||Delta Z_N||2
       +(400/sqrt(n)) sum_i||Delta V_i,N-Delta Z_N||2
       +(100/sqrt(n)) sum_(z=1)^N||Delta F_z,N-Delta Z_N||2 }. (24)

The exact metric remains (21); (24) is an upper ledger, not a claim that
those maxima are independently attainable or that channel dimensions add.
For direct cycle contributions of BOTH copies combined, the normalized
upper is <8H(Delta K)/n after reset. For both compensator copies it is
<8||Delta kappa||2/n. Balanced output modes (9) also admit legal complementary
one-step queries, since their next-time sign patterns fit the gate box and
O^T transports them back exactly. Common mode queries must retain J and
the bath/front terms, not assume residual cancellation.

## 10. Dense perturbation and full R,W,b scope

For fixed-feature credit, identical prescribed states give the exact
comparison recurrence between actual and reference sensitivity

    Delta B_t=G_t[R Delta B_(t-1)+(R-R0)B_(t-1)^ref].   (25)

Forcing is identical. Its operator bound is sigma sqrt(l); contraction
gives ||B^ref||<=sigma sqrt(l)n and comparison <=e_R sigma sqrt(l)n^2.
After group normalization and legal future-adjoint replacement, each
history has error <=e_R sigma sqrt(l)[n+1/(.06e)]<4e-9. Thus

    |d_fixed_actual(X,X')-nu(M_N(X)-M_N(X'))|<=8e-9.     (26)

This bound covers the COMPLETE fixed-feature operator, not just paired
columns. Future direct injections cancel at the actual common endpoint.

For FULL parameter sensitivity (1), split the reference state as
h_t=h_t^pub+sum_i 2 beta_i,t b_i(t), where the public state has zeros on
the four driven sites and agrees elsewhere. Its private part sums to zero.
Then the recurrent forcing has a public-feature term AND
sum_i 2 beta_i,t delta R b_i(t). This signed beta injection is absent only
in the accepted fixed-source-feature restriction, not in the full R block.

At interiors the reference raw input on a tuple is

    x_ref,tuple=-(b0+aJ_state,pub)1_tuple
                 +2[atanh(beta_i,t)-a beta_i,t-1]b_i(t).

Here J_state,pub is the scalar PUBLIC state bath term, distinct from the
PRIVATE sensitivity row vector J_t. Reset input on that tuple is
a u_T 1_tuple-2a beta_i,T b_i(N). Source preparation and holding are public.
Actual inputs include -(R-R0)h_(t-1) on ALL rows. Thus W forcing also has
signed private inputs and dense corrections; b forcing is public constant
but its propagation gates and transports are private. They do not cancel
merely because the state sum does.

For full parameter comparisons, a W surrogate using actual x_t has identical
forcing; using x_ref instead adds the explicitly known forcing
delta W[-(R-R0)h_(t-1)]. These blocks are not silently assigned (26)'s
fixed-feature constant or promoted to new d_F lower bounds. Formula (2)
accounts for every component exactly. A full-model robust result would
require a separate normalized joint-section proof.

## 11. What the local quantile code DOES extend to

Store the accepted quantile positions of each local product row, together
with kappa_i,T=sum_j k_i,j as one exact real per row. This is a continuous
STATIC code of dimension

    k_local=m(p-1)+m=m p,
    p=max(1,ceil(16000sqrt(mT min(m,T))/n)).              (27)

Equal codes make BOTH direct cycle copies close in (21) by <=epsilon
and make direct compensator differences zero. The extra m scalar traces
do not create superlinear dimension. It follows by Borsuk-Ulam that any
section whose antipodal distinction is carried solely by this local direct
metric satisfies

    D<=m+k_quant <m+16000mT/sqrt(n).                    (28)

This is NOT a bound on the full M=L+H. Also H output cancellation under
balanced modes is exact, but output algebra alone does not substitute an
arbitrary output projection for the actual legal-query supremum.

For completeness: a row that is the difference of TWO legal monotone
product rows has total variation <=2. Encoding the two inverse-level lists
gives entry error <=2/p and equal-code pair error <=4/p. If its projected
query upper really is C/n times the same staggered H norm, choosing
p>=4C sqrt(mT min(m,T))/(n epsilon) gives an analogous O(mT/sqrt(n))
static section obstruction. Nonmonotonicity of such a difference alone
does not escape. This lemma does not assert that (10)'s private vector
weights or the crossover (17) meet those hypotheses.

The FIRST missing property for H is not simply a minus sign. Its weights
J_(j-1) are private r-vectors coupled to the ENTIRE gate word; they are not
public bounded scalar weights. Its output also has bulk/front support.
Thus the old scalar entry reconstruction and staggered H bound do not
control this feedback by themselves.

## 12. New complete-corridor short-packet obstruction

THEOREM (full fixed-feature short packet). For every accepted corridor word,
the ACTUAL sensitivity operator has norm <=sigma sqrt(l) sum_(j=0)^(N-1)a^j
<=sigma sqrt(l)N, directly from (1), ||R||op=a, ||G||<=1 and the identical
fixed-source forcing. Preparation forcing is zero. Every actual legal
future adjoint has norm <=q_f^L<=q_f<.941. Therefore every pair has

    d_fixed_actual <=2 sigma sqrt(l) q_f N/n
                   < .095982 N/sqrt(n).               (29)

If N=T+1<=.020sqrt(n), the right side is <=.00191964<.002.
Consequently NO positive-dimensional robust antipodal section can exist
in the COMPLETE fixed-feature corridor channel at those horizons. This
is an actual worst-query upper, not RMS visibility. It includes all
common-mode feedback and the ACTUAL dense dynamics exactly; it needs no
additive dense comparison charge. The reference bound ||M_N||op<=N agrees.

The same short-packet proof also covers fixed-source-feature parameter
actions on ALL n output rows: their injection operator still has norm
sigma sqrt(l). No uncounted source/node-0 channel escapes that time bound.

This proves the necessary time scale T=Omega(sqrt(n)) for any fixed-margin
section in this mechanism. It does not close longer packets or strengthen
the global energy impossibility exponent. The energy upper is not reversed.

## 13. Exponent region and the first failed lower route

The exact gate word has mT continuous coordinates, so any robust section
has D<=mT. For m~n^mu,T~n^tau,r_profile~n^rho,D~mr_profile, necessary
conditions for a new complete-channel construction include

    rho<=tau, tau>=1/2, mu+rho>1, mu+tau<3/2,
    mu,tau<=1.                                         (30)

This region is NOT empty; e.g. (.4,.8,.7) passes these necessary tests.
The local-direct channel further obeys (28) and cannot furnish the target.
No new inequality closing the complete region is proved.

A naive lower using only (17) fails at the FIRST tail-control step. A
specific absolute-value iteration estimate charges feedback by mT/k:
(13) contains the term -(4gamma^2/k)sum_i V_i in J. In the maximum row-vector
norm its one-step reinjection into (10) has bound4gamma^2 m/k; summing T
steps gives the sufficient bound4gamma^2 mT/k. Requiring THIS bound to be
below a small constant is incompatible with any robust
section D=omega(n), since D<=mT requires mT/n->infinity. This is a METHOD
failure, not a bound on the true nonperturbative system. Whole common-mode
resummation via (10)-(13) is required. No raw m-by-m matrix count or visible
axis count certifies a joint robust section.

## 14. One precise remaining finite-error problem

Let E_local be (27). Define, at the fixed PUBLIC parameters, the conditional
feedback diameter in the ACTUAL reference query metric

    Gamma_(n,m,T)=sup_{legal g,g': E_local(g)=E_local(g')}
                       nu(H_N(g)-H_N(g')).             (31)

All endpoints and public schedules are the same. There is no separate
normalization of query vectors. A sufficient COMPLETE-channel theorem is

    Gamma_(n,m,T)<=epsilon-2(8e-9).                    (32)

Indeed equal codes then have full distance <=epsilon+Gamma+8e-9<2epsilon;
Borsuk-Ulam gives D<=m+k_quant, excluding superlinearity at subcritical mT.
Thus an all-sequence Gamma=o(1) bound at mT=o(n^(3/2)) would close this route.

We do NOT prove (32). The available crude uniform bound
Gamma<=.204N/sqrt(n), from ||H||<=||M||+||L||<=2N, is useless once
N>>sqrt(n). The row ledger (24) is sharper structurally but its renewal
vectors have no proved finite-error bound sufficient for (32).

Failure of (32) would NOT itself prove a superlinear robust section;
conditional diameter is not continuous dimension. The exact full remaining
lower target is the Borsuk-Ulam robust width of the ONE reachable family
M_N(g), metric (21), generated by (10)-(13), with mT=o(n^(3/2)). A valid
positive proof must control every antipodal pair after all feedback orders.

## 15. Conclusion

STRUCTURAL SUCCESS: pairing cancels state and some derivative modes, but
there is a nonzero PRIVATE common-mode sensitivity reservoir, including
private bath rows, reset-transmitted feedback and prefix-suffix crossovers.
The accepted paired theorem does not compress this reservoir.

PARTIAL NEGATIVE SUCCESS: balanced/direct modes admit the extended local
code; complete fixed-feature packets of length T+1<=.020sqrt(n) cannot
meet the robust threshold. No positive omega(n) section or complete long-
packet obstruction is proved. Best constructive energy exponent remains
3/4, log power3/2; general threshold bracket[1/4,3/4] and full-model gap
are unchanged. Next: bound or refute (32) using the exact common-mode renewal
system, WITHOUT a small-mT/n Born truncation. Stop this stage.
