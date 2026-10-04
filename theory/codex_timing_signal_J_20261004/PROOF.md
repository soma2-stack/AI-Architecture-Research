# A changing survivor set violates a uniform 1/m_s timing-row bound

Codex, 2026-10-04. **NEW theorem derivation; internal checks required and independent hostile review pending.** Accepted corridor lift, full renewal, complement damping and legal-query contract are dependencies. No historical theorem is reopened.

## 1. Definitions and exact full timing recurrence

Use n>=10^6, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
gamma=1/(1-1/sqrt(k)), c=gamma^2/k. On physical coordinates 1,...,k-1,

    O_*=C+1 u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-c1^T,
    v_H^T=gamma1^T/sqrt(k).

C shifts the open cycle and fixes the off-cycle coordinates. The complete reference fixed-feature differentiated state, with realized inputs frozen, is

    M_0=0, M_t=G_t(a O_* M_(t-1)+I),
    J_t=u^T M_t, B_t=v_H^T M_t.

Multiplication by u gives the exact recurrence

    J_t = a u^T G_t C M_(t-1)
          +a(u^T G_t1)J_(t-1)
          +a(u^T G_t e_1)B_(t-1)+u^T G_t.             (1)

The first term is transported credit, weighted by the CURRENT gates. The next two are both Householder feedback terms. The last is fresh fixed-source forcing. Preparation has M_0=0 because its preceding source is zero. Gate words specify histories; sensitivity differentiation holds raw inputs fixed. Differentiating a gate-control policy instead would be a different object.

Writing G_t=q_t I+D_t (q_t is the PUBLIC ordinary bath gate), the gate-dependent forcing in (1) is exactly

    a u^T D_t C M_(t-1)
      +a(u^T D_t1)J_(t-1)+a(u^T D_t e_1)B_(t-1)+u^T D_t. (2)

The remaining terms use q_t, C, and the public u,v_H. In particular u^T1=-gamma and u^T e_1=-c. Pair STATE sums vanish, but (2) need not vanish. All four sites of a tuple have the same positive gate; the differentiated forcing has no compensating state sign. Moving support transports the weighted rows; it does not eliminate them. J and B alone are not a closed online state: C M and its gate-weighted row sums remain necessary in (1).

The exact norm identity ||u||_2^2=2 gamma^2/k follows by expanding its one exceptional coordinate and r-1 ordinary coordinates. Orthogonality and G<=I give

    ||M_t||op <= sum_(j=0)^(t-1)a^j=n(1-a^t),
    ||J_t||_2 <= gamma sqrt(2/k)n(1-a^t)
               <2.01 min(t,n)/sqrt(n).                (3)

This is a horizon-capped version of the accepted bound. It is an upper on each entry too. A much smaller universal 1/m_s bound does NOT follow.

For the ACTUAL dense map, normalize full fixed-feature sensitivity by sigma sqrt(l) and write it as mathcal M_t=G_t(R mathcal M_(t-1)+E), mathcal M_0=0. The selected timing row is J_dense=u^T E^T mathcal M. Equation (1) for its selected rows has the additional EXACT forcing u^T E^T G_t(R-R0)mathcal M_(t-1); source/node-0 coupling is included there, not omitted. Its norm is <=||u|| e_R(t-1). Since both maps contract by a,

    ||J_dense,t-J_t||_2 <=||u|| e_R t(t-1)/2,
    e_R<=4/(10^8 n^2).                              (3a)

At the complete horizon below, this is <5*10^-6/n per history. Thus the reference entry counterexample also survives dense comparison: a pair row changes by <10^-5/n. The exact structured formulas below are reference formulas; all actual-gradient claims include this comparison or the accepted all-query charge.

## 2. An exact one-switch identity

Let m be even. Half of the m tuples are donors and half survivors. Each has two moving cycle sites and two stationary compensators. There are m donor compensator sites and m survivor compensator sites. Fix the UNIT parameter probe v with entries +1/sqrt(2m) on donor compensators, -1/sqrt(2m) on survivor compensators, and zero elsewhere.

It is zero-sum, stationary off-cycle, and O_*v=v. For L steps give ALL tuples g_H=1-n^-2. Exactly

    M_L v=kappa v,
    kappa=g_H sum_(j=0)^(L-1)(a g_H)^j.               (4)

Next keep survivors high but put donors at g_L=.995. At this FIRST switch,

    J_(L+1)v = c(g_H-g_L)(a kappa+1)sqrt(m/2).        (5)

This is an exact finite-amplitude identity, not a derivative or truncation. Indeed M_(L+1)v=(a kappa+1)G_(L+1)v and u=-c on these stationary columns.

Permuting compensator sites within either group commutes with O_* and EVERY G in this schedule. Therefore J has one common column value j_D on the donor compensators and one j_S on survivors. Equation (5) gives

    j_D-j_S=c(g_H-g_L)(a kappa+1).                    (6)

The public comparison history A simply continues ALL-high gates; its two group values coincide and J_A v=0. Thus the same contrast (6) holds for Delta J=J_B-J_A. At least one ENTIRE group of m entries of Delta J has magnitude >=half the right side. This survives public-center subtraction. No claim of m independent robust dimensions is made.

## 3. A persistence estimate without dropping Householder renewals

We prove persistence over a growing interval. Set

    n>=10^200,
    m=2 floor(sqrt(n)/2), L=ceil(10 n^(3/4)),
    R_short=floor(10^-6 sqrt(n/m)), s_0=ceil(1000 log n).

Keep donors low and survivors high after the switch. For all s_0+1<=s<=R_short,

    J_(L+s)v >= .0004 c kappa sqrt(m),                (7)
    max_z |(J_B-J_A)_(L+s,z)| >= 2*10^-4 kappa/n,     (8)

and (8) holds on at least m stationary compensator columns. More precisely the fixed donor-versus-survivor column CONTRAST is uniformly large throughout this interval; which absolute group is larger may depend on s.

### 3.1 Public gates and probe-specific exact balance

The accepted bath satisfies .032<u_t<.1, hence .99<q_t<=q_*=.9992. Front states are >=u_t: first-row preactivation has the additional positive Householder state sum, and ordinary front predecessors are >= the bath predecessor. The first front preactivation is >.02 sqrt(k), giving f_1,t<=4 exp(-.04 sqrt(k))<=1/n. For z>=2, mean value along tanh between preactivations >=atanh(u_t) gives

    0<=h_(z,t)-u_t<=q_*^(z-1),
    0<=q_t-f_(z,t)<=2 q_*^(z-1).                    (9)

These inequalities also follow from the full derivation in the preceding multi-donor proof; here their premises and mean-value step are stated explicitly. In particular sum_(z>=2)|f_z-q_t|<2500.

Write x_t=M_t v, Z_t for its ordinary bath row, and F_z,t for its public-front row (these are SCALARS on this one probe). At warmup end x= kappa v, so Z=F=0. The terminal cycle row equals Z throughout this no-wrap interval. Let Y_H,Y_L be sums of x over all 2m physical sites in the high and low groups respectively. Then, EXACTLY,

    Y_H,t=a g_H(Y_H,t-1+2m J_t-1 v)-g_H sqrt(m/2),
    Y_L,t=a g_L(Y_L,t-1+2m J_t-1 v)+g_L sqrt(m/2),
    Z_t=a q_t(Z_t-1+J_t-1 v),
    F_1,t=a f_1,t(J_t-1 v+B_t-1 v),
    F_z,t=a f_z,t(F_z-1,t-1+J_t-1 v), z>=2.          (10)

Cycle predecessors are the corresponding moving sites; compensators stay fixed. Each sum counts all FOUR tuple sites, including the empty-at-warmup cycle response. No feedback order is suppressed.

Directly summing the FULL x recurrence and using u^T x=gamma Z/sqrt(k)-c sum x gives the particularly useful exact balance

    J_t v = a q_t[(1-gamma)J_t-1 v+c Z_t-1]
      -c a(g_H-q_t)(Y_H,t-1+2m J_t-1 v)
      -c a(g_L-q_t)(Y_L,t-1+2m J_t-1 v)
      -c a sum_(z>=1)(f_z,t-q_t)(x_pred(z),t-1+J_t-1 v)
      -c a f_1,t B_t-1 v
      +c(g_H-g_L)sqrt(m/2).                          (11)

The predecessor in the front sum is the actual C predecessor, with x_pred(1)=0. The first-row B term is separate; its gate-defect times J IS included in the front sum. Crucial identity gamma/sqrt(k)-cr=-gamma is used here. The coefficient 1-gamma=O(n^-1/2) is small, but the gate-weighted Y_H forcing is NOT. The last term is fresh injection, not an old-credit term.

### 3.2 Bounds for every combination in this schedule

For the short interval H=L+R_short<=2 kappa. Equation (3), conservatively, gives |J_t v|<=6 kappa/sqrt(n) and |B_t v|<=4 kappa. Equations (9)-(10), starting from zero bath/front probe response, imply

    |Z_t|<=7500 kappa/sqrt(n),
    |F_z,t|<=8000 kappa/sqrt(n).                     (12)

The high sum starts at -kappa sqrt(m/2). Its fresh forcing is negative. Using 2m R_short times the bound on |J|, and (a g_H)^R_short>=.999, gives

    Y_H,t-1+2m J_t-1 v <=-.69 kappa sqrt(m).          (13)

For s>=s_0+1, (a g_L)^(s-1)<=n^-5. Geometric summation of the low-group forcing and possible signed J gives

    |Y_L,t-1+2m J_t-1 v|
       <=kappa sqrt(m)n^-5+200 sqrt(m)
                                      +2412 m kappa/sqrt(n). (14)

We do NOT assume q_t>=g_L; that can be false. We bound the low term in absolute value. Its coefficient |g_L-q_t|<.01.

The high term in (11) is positive, at least .00047 c kappa sqrt(m), because a>.99 and g_H-q_t>=.0007. All potentially negative terms, divided by c kappa sqrt(m), sum to at most

    11/sqrt(m)+7500/sqrt(nm)
      +2.1*10^7/sqrt(nm)+4/(n sqrt(m))
      +.01 n^-5+2/kappa+24.12 sqrt(m/n).              (15)

For every n>=10^200 this is <.00007. The floor m>=.99 sqrt(n), k>=n/3, and kappa>=.998L make each displayed term decrease beyond the threshold. Also R_short>s_0+1 and R_short/n is negligible, verifying (13). The fresh term in (11) is nonnegative. This proves (7). Permutation symmetry and J_A v=0 give (8), with ample slack. Large-J persistence is established over R_short-s_0 consecutive time indices; it is not inferred from isolated peaks or tangent rank.

## 4. Equal terminal local codes, endpoint, and full energy

The preceding prefix can be extended to an equal-code, same-endpoint pair. To obtain a robust 1D section as well, use a longer switching block

    R_long=100000 ceil(n/m) ceil(log n),
    L_tail=ceil(1000 log n), T=L+R_long+L_tail.

A keeps all tuples high until t0=T-L_tail. B has all-high warmup L, then donors low throughout R_long; survivors remain high. Give BOTH donors g_L for the final L_tail-1 steps. Set A's last donor gate to

    g_A,T=g_L(1+a kappa_B,T-1)/(1+a kappa_A,T-1).       (16)

Every final donor trace matches EXACTLY; survivor words coincide. The difference before correction is <=T g_L^(L_tail-1), so .994<g_A,T<=.995. The old quantile p=1 at n>=10^200, because 16000 m sqrt(T)/n<1. Thus ALL old local quantile/trace codes match. The large-J interval occurs before the common tail, which cannot retroactively remove it.

All gates remain in (.99,1), with exact zero-sum four-site STATES. Accepted inverse lift and PUBLIC reset give the same exact nonzero endpoint for every history. The full absolute energy, including preparation/source/bath/dense lift/tail/reset, is

    ||X||_2<=2 sqrt(m(T+2)+1)<8 n^(5/8),
    mT<=11 n^(5/4), S=m+T+4<=d/100.                 (17)

This is an UPPER bound only, never an energy necessity.

## 5. Actual legal-query metric: one robust dimension, not many

Use nu(A)=(sigma sqrt(l)/n) sup_(legal Q)||A^T c_Q||_2, .0499<sigma<.051, same legal future preactivations [.25,.75]^n and head/group normalization. J alone is not a final query output.

After warmup, project v onto the co-moving zero-sum subspace of the high survivor sites. This public probe p_t has norm 1/2, with positive high-cycle and negative high-compensator entries. The COMPLETE switched response is

    M_B,t0 v=kappa_H(t0)p_t0+e_t0,
    ||e_t0||<=kappa n^-6+16000 n/m<.001 kappa_H(t0).  (18)

Indeed the accepted two-step complement contraction is <=1-m/(8000n); R_long gives an initial-state factor <=n^-6, and the full forced complement sums to <=16000n/m. Equation (18) is a nonperturbative resummation. A has exactly M_A,t0 v=kappa_H(t0)v.

Thus the accepted common-mode read argument applies verbatim to this NEW warm-start schedule: survivor common component at t0 exceeds .499 kappa_H(t0); the common tail and reset cost <.002 kappa_H(t0); one future O_* gives a common component >.48 kappa_H(t0). The corresponding direct L_N v cancels by the exact trace match. Two complementary LEGAL one-step gate patterns, high versus low on the survivor support and equal elsewhere, give

    nu(Delta H_N)>.0499*.99*.17*.48
                         kappa_H(t0)sqrt(m)/n>.03.    (19)

The SAME query is applied to both histories. Triangle inequality selects one of two real legal queries; no RMS or arbitrary unit-adjoint substitution is used. Dense pair charge <=8e-9 yields actual separation >.03-8e-9.

For theta in [-1,1], give donors g_L+(theta+1)(g_H-g_L)/2 ONLY in R_long, with the common warmup and tail, then set last donor gate to kappa_B,T/(1+a kappa_theta,T-1). This continuous legal correction preserves the same traces and exact endpoint over the ENTIRE interval. Consequently this is one continuous finite-radius D=1 section, with boundary half-margin >.014999996.

All m large compensator entries are a shared two-group CONTRAST of this single vector timing signal. They cannot be counted as independent dimensions. No omega(n) section or energy exponent below 3/4 for superlinear dimension follows.

## 6. Precise failure and status

For m_s=m/2 high survivor tuples, (8) implies

    m_s max_z |Delta J_(L+s,z)|
       >=10^-4 kappa m/n >= .00098 n^(1/4).          (20)

This diverges. For any fixed PUBLIC centering row, triangle inequality on A and B leaves an unbounded centered multiple too. Therefore a width-independent O(1/m_s) ENTRY bound, uniform on changing survivor sets, is FALSE. The exact first-switch identity (5) already disproves it; (7)-(8) show that it is not merely a one-step anomaly. The histories can even have equal final old local codes.

Equation (3a) preserves at least m actual selected timing entries of magnitude >=10^-4 kappa/n in the centered pair, and therefore preserves divergence after multiplication by m_s. No assumption of exact permutation symmetry of the perturbed dense matrix is made.

This does NOT refute a conditional theorem with a genuinely DIFFERENT hypothesis, for example a controlled signed time integral rather than pointwise entries. Claude's newest conditional statement was not found locally; its precise constants/norm/centering cannot be certified from the user's summary alone. The sufficient small-entry premise described in the task does not become unconditional. Complete corridor remains OPEN.

The strongest universal upper proved here is (3); it does not bound a query-weighted transfer integral tightly enough to close growing survivor schedules. The smallest next quantity is the finite-error width of the exact filtered timing matrix a q_N[a sum_j K_c,j J_(j-1)+J_T], on a fiber of local code, bath row and donor mean, with growing whole-word survivor schedules. Its observed/possible large entries still need either a joint lower or a continuous finite-error code.

## 7. Preserved dense-comparison correction and scope

Do not reuse the historical incorrect dense-error display. The accepted conservative complete pair charge <=8e-9 remains valid; the independently reconstructed illustrative comparison was about 1.4e-12 at n=10^6. A correct finite-N ledger is e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n], e_R<=4/(10^8 n^2), q_f<.941.

This work concerns the exact reference timing row and its actual fixed-feature legal-query consequence. It does not claim a generic causal encoder, all-RNN theorem, full-model strengthening, finite-bit/VRAM bound, practical onset, or energy impossibility. The accepted global exponent bracket remains [1/4,3/4], up to slow factors; best superlinear construction and full-model gap are unchanged.
