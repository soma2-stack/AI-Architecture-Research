# Multi-epoch donor transfers: finite-radius scoped obstructions

Codex, 2026-10-03. **NEW theorems, internally checked; independent review pending.** Accepted historical results are dependencies, not re-reviewed here. No new superlinear lower bound or improved constructive energy exponent is claimed.

## 1. Contract, reference objects, and scope

Use the frozen corridor definitions in the source-hash manifest. Let

    k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,
    gamma=1/(1-1/sqrt(k)), c=gamma^2/k,
    N=T+1, S=m+T+4<=d/100.

There are m four-site tuples: two moving positive cycle tracks and two stationary negative compensators. Their common gate is g_i,t in (.99,1); all other states/gates are public. Preparation is public, M_0=0, and N is the public reset. The endpoint is identical for every gate word. Assume n>=10^200 for the final finite-error theorems; intermediate estimates only require n>=10^6.

The complete reference fixed-source-feature sensitivity, including every differentiated output/parameter direction in the selected memory block, is

    M_t=G_t(a O_* M_(t-1)+I),
    L_t=G_t(a C L_(t-1)+I), H_t=M_t-L_t,
    O_*=C+1 u^T+e_1 v_H^T,
    u^T=(gamma/sqrt(k))e_(d-1)^T-c1^T,
    v_H^T=(gamma/sqrt(k))1^T.

C is the accepted open cycle shift plus off-cycle identity. O_* is orthogonal. Both ||M_t||op and ||L_t||op are <=t. The exact row renewal is

    J_t=u^T M_t, B_t=v_H^T M_t,
    V_i,t=a g_i,t(V_i,t-1+J_(t-1)),
    Z_t=a q_t(Z_(t-1)+J_(t-1)),
    F_1,t=a f_1,t(J_(t-1)+B_(t-1)),
    F_z,t=a f_z,t(F_(z-1),t-1+J_(t-1)), z>=2,
    H_t=1 Z_t+sum_i 1_(tuple_i(t))(V_i,t-Z_t)
                    +sum_(z<=t)e_z(F_z,t-Z_t).                  (1)

All V,J,B,Z,F are row vectors in parameter space, not free scalars. No Householder truncation is used. At reset, V_i,N=a q_N(V_i,T+J_T), with the same q_N and J_T for all tuples.

Reference source/node-0 responses outside this selected block are public and cancel in history comparisons. Their actual dense leakage is charged by the accepted complete fixed-feature pair bound. This is still the fixed-feature restriction; other R,W,b channels are not included.

The metric throughout is the accepted actual-query supremum

    nu(A)=(sigma sqrt(l)/n) sup_(legal Q)||A^T c_Q||2,
    .0499<sigma<.051,
    nu_1(A)=(sigma sqrt(l)a/(n sqrt(n)))
                    max_(g in [g_lo,g_hi]^r)||A^T O_*^T g||2,    (2)

with future preactivations in [.25,.75]^n, uniform head 1/sqrt(n), group factor 1/n, and every permitted future horizon >=1. The accepted front-coordinate bound is |c_Q,z|<=100/sqrt(n); the bath bound is |c_Q^T1|<=102. The exceptional adjoint is not replaced by an ordinary-coordinate bound. Complete actual/reference pair discrepancy is <=8e-9.

**Preserved correction:** the historical displayed dense-error bracket was wrong. The accepted pair charge is unchanged. The correct finite-N comparison ledger is

    e_R sigma sqrt(l)[q_f N(N-1)/n+14 N/n],
    e_R<=4/(10^8 n^2), q_f<.941.                            (3)

The earlier reconstructed number at n=10^6 was approximately 1.4e-12 in the cited comparison; the tighter horizon ledger can be smaller. No result here depends on that illustrative decimal.

## 2. Exact epoch transfer and why scalar additivity is not available

Partition 1,...,t0 into E nonempty epochs. Set A_t=a G_t O_*. On any fixed public parameter probe matrix P,

    X_t=M_t P=A_t X_(t-1)+G_t P.

For epoch e=(t_(e-1),t_e], define

    Acal_e=A_(t_e)...A_(t_(e-1)+1),
    Bcal_e=sum_(s=t_(e-1)+1)^(t_e)
                   Phi_O(t_e,s)G_s P.

Then EXACTLY

    X_(t0)=sum_e Acal_E...Acal_(e+1) Bcal_e.               (4)

These matrices are private functions of all gates, not public constants or independent donor signals. Mixed effects are retained in the products. For cohort c sharing a whole gate word, its private response is exactly

    V_c,T=a sum_(j=1)^T K_c,j J_(j-1),
    K_c,j=a^(T-j) product_(s=j)^T g_c,s.                  (5)

Splitting this sum into E blocks does not create E new output rows. J depends on every cohort and every earlier epoch. Identical whole words give identical V rows by induction from zero. Identical LAST gates alone do not: V_i-V_j retains earlier differences. This is the first obstruction to multiplying the accepted shared-survivor amplifier.

The Householder donor signal J is BROADCAST to every tuple. There is no freely configurable donor-to-cohort routing matrix. Different survivor gate words provide different scalar temporal filters of this same private vector stream. For an off-cycle probe p_h, the exact transfer entry at reset is

    A_c,h=a q_N[a sum_j K_c,j J_(j-1)+J_T] p_h.        (5a)

Subtracting the donor mean gives the corresponding private survivor-relative matrix. Its entries are coupled functions of the complete word.

## 3. Trace correction for arbitrary simultaneous donor prefixes

Let the donor set be fixed and nonempty. Its gates are arbitrary legal continuous functions of all section parameters through t0=T-L, where

    L=ceil(1000 log n), T>=L+1, g_L=.995.

Use g_L on donors for the following L-1 steps. Correct each last donor gate by

    kappa_i,t=g_i,t(1+a kappa_i,t-1), kappa_i,0=0,
    kappa_*=kappa(g_L;T),
    g_i,T=kappa_* /(1+a kappa_i,T-1).                    (6)

Every donor trace at T is exactly kappa_*. Corrections are independent scalar rational evaluations on their own tuple prefixes; J does not enter kappa. Thus there is no trace cross-coupling even though full credit remains coupled. The map is continuous and has positive denominator.

Writing kappa_L for the constant-g_L reference trace,

    |kappa_i,T-1-kappa_L,T-1|
        <=N(.995)^(L-1)<=2N n^-5,
    |g_i,T-g_L|<=2N n^-5.                              (7)

The second bound follows directly from (6), not by differentiating a control policy in the sensitivity recurrence. The tail estimate is analytic: log(.995)=log(1-.005)<=-.005 and (.995)^(-1)<2. Gates remain in (.994,.996), hence in the accepted lift. At all times beta=sqrt(1-g) and each tuple has exactly zero state sum. Reset remains public: endpoint equality and the accepted raw-input cube are unchanged.

For ANY two donors within ONE history, common forcing cancels in their V difference during the L-1 common steps. Using ||H_t||op<=2N and ||J_t||<=3N/sqrt(n), (7) gives

    ||V_i,N-V_j,N|| <=20 N^2 n^-5.                      (8)

Indeed their initial row difference is <=4N, the common steps reduce it to <=8N n^-5, and the last correction contributes <=12N^2 n^-5. Reset multiplies the difference by a q_N<=1. If D_N is the mean donor row, every donor is within the same bound of D_N. For two histories with equal D_N, their individual donor-row differences are <=40N^2 n^-5. The all-query donor residual is therefore at most

    epsilon_d <=816 m N^2/n^6 <=816/n^3.                (9)

This is a finite-radius estimate, uniform over all prefixes, not an infinitesimal calculation. Correction terms are included in the complete renewal and cannot be declared to erase survivor credit.

## 4. A new uniform public-front estimate

This step removes the growing T-vector front bank from the final STATIC code; it is not a causal update theorem.

Accepted bath bounds give .032<u_t<.1 and q_t<=q=.9992. Nondriven front states h_z,t are public. They satisfy h_z,t>=u_t. For row1, its preactivation exceeds the ordinary bath preactivation because B_state>=u_(t-1). For z>=2, this follows inductively from the predecessor inequality and monotonicity of tanh. Quantitatively, the public state sum is

    sum h=(r-4m)u+W, 0<=W<=1.1t.

Thus sum h>.03 k and |J_state|<.12 for n>=10^6, while B_state=gamma sum h/sqrt(k)>.03 sqrt(k). Row1's preactivation is at least

    .05+a(.03 sqrt(k)-.12)>.02 sqrt(k).

Consequently

    f_1,t<=4 exp(-.04 sqrt(k))<=1/n.                    (10)

For the last inequality, at n=10^6, .04 sqrt(n/3)>20>log(4n), and the difference increases for larger n. One exact bound for the logarithm is log(4*10^6)<16: e>8/3 from its first five series terms and (8/3)^16>4*10^6 by integer arithmetic. This also bounds the first reset-front gate. For z>=2, the mean-value form of tanh, with both preactivations >=atanh u_t, gives

    0<=h_z,t-u_t<=q^(z-1),
    |f_z,t-q_t|<=2 q^(z-1).                            (11)

The row1 initial bound is h_1,t-u_t<1. No averaging of queries is used.

Since sqrt(k)>=700 and gamma<=700/699<1.002 at n>=10^6, the squared norm of u is <=(gamma^2+gamma^4)/k<6.1/n<9/n. Thus ||u||2<=3/sqrt(n), ||v_H||2<=2, and ||M_t||op<=t give

    ||J_t||2<=3N/sqrt(n), ||B_t||2<=2N,
    ||Z_t||2<=3750N/sqrt(n),
    ||F_1,t||2<=3N/n.

Put R_z,t=F_z,t-Z_t. Its exact recurrence for z>=2 is

    R_z,t=a f_z,t R_(z-1),t-1
               +a(f_z,t-q_t)(Z_(t-1)+J_(t-1)).

The initial bound ||R_1,t||<=4000N/sqrt(n), followed by (11), gives

    ||R_z,t||2<=8000N z q^(z-1)/sqrt(n).

For any TWO histories, summing and using the all-legal front-coordinate bound in (2),

    nu(sum_z e_z Delta R_z,N)
       <=1.275*10^11 N/n^(3/2)
       <=3.2*10^8/sqrt(n) =: epsilon_f.                 (12)

Here N<=S<=n/400. This is negligible at n>=10^200, uniformly over all legal corridor words and over ALL legal future horizons. The exceptional B row is controlled by the tiny PUBLIC f_1, not by the false paired 8/n coefficient. Bath Z is still private and must be stored. The estimate is deliberately loose but sufficient.

## 5. Exact public right-parameter subspace for all private renewal

There is a useful further reduction without counting tangent rank. Define a public auxiliary gate word Gbar_t: replace every driven tuple's gate by the ordinary q_t; keep the public front gates. At reset Gbar_N=G_N. Let

    Lbar_0=0, Lbar_t=Gbar_t(a C Lbar_(t-1)+I),
    ellbar_s=[u^T;v_H^T] Lbar_s.

All of these are genuinely public, because the nondriven bath/front and positions are independent of the private gate word. Let U be the set of input parameter columns c_i^A(j), c_i^B(j), o_i^1,o_i^2 for 1<=j<=T and 1<=i<=m. Its size is <=4m+2T. The direct recurrence proves

    (L_t-Lbar_t) has no columns outside U.              (13)

To see this, the new forcing of L-Lbar is supported on driven rows. A cycle-row forcing at c_i(t) has parameter columns c_i(j), j<=t, because C only shifts; a compensator-row forcing has only o_i. Subsequent left multiplication cannot create a new parameter column. The reset has no new gate difference.

Let P be the PUBLIC subspace spanned by e_z, z in U, and the two rows of ellbar_s, 0<=s<N. Then

    q_P=dim P<=min(r,4m+4T+2).

Equation (13) gives J/B direct forcing rows in P. The exact finite Volterra renewal and H_0=0 imply that EVERY row of H_t is in P. This includes all insertion orders, bath, front, and reset. Choose any fixed public orthonormal basis of P. Storing a private row requires q_P coordinates, not r. The basis is public model/schedule data; the row's coordinates are all counted. This exact-real STATIC statement is not a finite-bit conditioning claim.

For a planned public horizon T, the accepted exact causal row-bank realization can also use this fixed right basis: mt direct kernel entries and (m+t+1) private rows of q_P coordinates. Thus one nonminimal EXACT reference credit-state count is mt+q_P(m+t+1), or r^2 through the full matrix. J/B are computed from this counted bank, not kept for free. Ordinary forward state, if needed for an online input interface, is additional and must be counted. Neither this exact bank nor the final static codes prove a universal O(n) causal encoder.

## 6. Complete fixed-survivor-class finite-error code

Partition a fixed survivor set into C public cohorts. Within each cohort all tuples share the SAME entire gate word, which may vary continuously with parameters; different cohorts may use different words. Donors may use arbitrary E-epoch prefixes and the protocol (6). Then their private rows collapse to C exact V_c,N rows plus one approximate donor mean D_N.

Use the accepted local continuous code: p-1 quantile positions per tuple plus one exact compensator trace, with

    p=max(1,ceil(16000 sqrt(mT min(m,T))/n)).

It uses mp coordinates and makes equal-code direct distance <=epsilon=.001. Append the q_P coordinates of Z_N, D_N, and V_c,N for each c. Every private coordinate is counted. The total is

    K_complete=mp+(C+2)q_P.                            (14)

With no donors omit D_N; with no cohorts omit their rows. An alternative for unrestricted gate words stores all m V rows plus Z, giving mp+(m+1)q_P. Use the smaller applicable count. Row identities, memberships, supports, Gbar, basis, endpoints, and the schedule are public and fixed independently of section parameters.

For two histories with equal code, (1), (9), (12), the accepted direct code and actual dense pair comparison give

    d_actual <=.001+epsilon_f+epsilon_d+8e-9 <.002       (15)

for every n>=10^200. This is a uniform finite-radius fiber diameter bound, not a pointwise approximation or a rank argument.

**THEOREM A (new, scoped).** Every continuous admissible robust antipodal D-ball in this fixed-survivor-class, terminal-donor-matching family, at unchanged epsilon=.001 and exact common endpoint, has

    D<=mp+(C+2)q_P,
    q_P<=min(r,4m+4T+2).

For fixed C and mT=o(n^(3/2)), this is O(n). In particular

    mp<m+16000mT/sqrt(n),                               (16)

since m min(m,T)<=nT in BOTH m<=T and T<m cases. For arbitrary fixed C, (14) is O(m+T+mT/sqrt(n)); the constants do not depend on E. Adding arbitrarily many donor epochs cannot defeat this scoped code. It is a STATIC section obstruction, not an online sufficient-memory encoder.

Proof of dimension statement: compose the continuous code with the proposed section. If D>K_complete, Borsuk-Ulam on S^(D-1) gives equal-coded antipodes. Equation (15) contradicts their required separation >.002. This uses the actual future-query norm, every allowed finite-radius combination, and strict separation. It does not use finite-state packing.

**Corollary (the two accepted cheap schedules, arbitrarily many donors/epochs).** Keep one survivor word/class, and allow arbitrary independent legal donor prefixes followed by (6). Both accepted schedules have p=1. For the main schedule, n>=10^200,

    D<=13m+12T+6 <=120 n^(3/4)+13 sqrt(n)+18 =o(n).

For the logarithmic schedule, n>=10^1000,

    D<=13m+12T+6
       <=120 n/(log n)^2+13(log n)^4+18 =o(n).          (16a)

These are complete-channel bounds for these FIXED-SURVIVOR extensions, not whole-corridor bounds. At the original one-slider boundaries the accepted margin remains positive. Cheap strong signal and small continuous dimension are compatible.

## 7. A stronger code for all stationary-compensator input directions

Now restrict differentiated parameter INPUT directions to the entire off-cycle block, not just the one probe of the accepted amplifier. This is a projection of the fixed-feature gradient vector, not a change of future-query legality or normalization. Precisely, with Pi_off the public orthogonal projection onto these parameter coordinates, use

    nu_off(A)=(sigma sqrt(l)/n) sup_(legal Q)
                             ||Pi_off A^T c_Q||2.

The dimension theorem below requires EVERY boundary antipodal pair to exceed .002 in the actual version of THIS projected metric. A section that is only robust in the full metric while nu_off is small is not covered.

For the two compensators in tuple i, v=e_o1-e_o2 has zero sum, O_*v=Cv=v, and G_t v=g_i,t v. Thus M_t v=L_t v=kappa_i,t v and H_t v=0. Similarly, the difference of ANY two ordinary off-cycle coordinates is annihilated by H, since their gates are both q_t. Therefore the private off-cycle parameter quotient is EXACTLY contained in the public (m+1)-dimensional space spanned by normalized pair sums and the ordinary off-cycle all-ones vector. No individual antisymmetric compensator direction contains private renewal.

Store all m traces and the (m+1) off-cycle quotient coordinates of each V_i,N and Z_N. This code uses

    K_off=m+(m+1)^2=m^2+3m+1.                          (17)

It works for EVERY legal gate word: no common tail, survivor equivalence, or small number of epochs is needed. Equal codes make the off-cycle direct matrix equal and all non-front private rows equal. Remaining actual pair error is <=epsilon_f+8e-9<.002. Consequently:

**THEOREM B (new, scoped).** A robust section whose entire guaranteed antipodal distinction is in the stationary/off-cycle fixed-feature parameter block satisfies D<=m^2+3m+1. Under (6) and C survivor classes, the sharper code is

    D<=m+(C+2)(m+1).                                  (18)

For the accepted m~sqrt(n) family, (17) is O(n), even with arbitrarily many independently changing survivor words. For the accepted m~(log n)^4 family it is O((log n)^8)=o(n). This rules out widening THOSE families to omega(n) using their stationary-compensator amplifier alone. It does NOT rule out using their additional moving cycle parameter columns jointly. Nor does it rule out m>>sqrt(n).

In the fixed-one-survivor-class protocol the off-cycle bound improves to 4m+3, irrespective of E. This is O(sqrt(n)) for the main schedule and O((log n)^4) for the logarithmic schedule.

This is a coordinate-code upper proof, not the invalid inference 'matrix rank equals robust dimension.' The front error and actual-query upper are essential to the finite-error conclusion.

## 8. Cohort query geometry and normalization

For a pure cohort response A=sum_c w_c,N X_c, let h_c be the number of physical sites in cohort c and w_c=1_(cohort c)/sqrt(h_c). All supports are far from the exceptional front/terminal row. The exact next-time common-mode overlap is

    B_cd=w_c,N+1^T O_* w_d,N
         =delta_cd-c sqrt(h_c h_d),
    B=I-c vv^T, v_c=sqrt(h_c).                         (19)

Since sum h_c<=4m and m<=n/400, ||u|| bounds imply 1-c sum h_c>.97 at n>=10^6. Thus the public read-frame itself is well-conditioned. It does NOT establish good conditioning of the gate-to-credit transfer matrix.

Put s_gate=(g_hi-g_lo)/2>.17, b=diag(sqrt(h_c)). The legal pair of one-step patterns g_center +/- s_gate sum_c xi_c 1_(cohort c at N+1), xi_c=+/-1, applied identically to both histories, proves

    nu(A)>=sigma sqrt(l)a s_gate/(n sqrt(n))
                        max_(xi in {+/-1}^C)||X^T B b xi||2
          >=sigma sqrt(l)a s_gate/(n sqrt(n))
                          sqrt(h_min)(1-c sum h_c)||X||F. (20)

The last step is the expectation identity for a Rademacher sign witness; at least one LEGAL query attains the lower bound. This does not replace the supremum with RMS. Cross-channel residuals, when present, must be subtracted using the actual norm; they do not vanish by assertion.

Splitting fixed total support into C equal independent row modes introduces sqrt(h_min)=sqrt(h_total/C), a 1/sqrt(C) factor in this uniform Frobenius lower certificate. A largest-cohort-only certificate also loses across the C row modes. No normalized query gives free independent readout of E*C amplitudes. Aligned responses may be stronger, but alignment is not independent dimension. This is the second failed naive multiplicative argument.

For clarity, the normalization loss is also real in a simple PURE-CHANNEL norm example: take orthogonal input rows R_c=A e_c and equal support h_c=H/C. The accepted all-legal ordinary-coordinate bound gives nu(sum_c 1_c R_c)<=5.1 A H/(n sqrt(C)). This example need not be reachable and is not a lower construction; it only refutes a claim of free independent cohort readout from the query geometry alone.

## 9. What is not solved

Legal epoch count can be as large as T-L, with C<=m_survivor. Neither is a robust dimension. A fixed-probe output has at most r continuous coordinates irrespective of epochs; proving a large one-probe signal cannot refute O(n).

An explicit JOINT admissible candidate is obtained by taking theta in the Euclidean ball B^(m_d E), public epoch boundaries, and g_i,t=.995+.001 theta_i,e on donor i during epoch e. Use (6) afterward; survivor words are public or cohort-shared continuous functions in the legal box. This is a continuous injective map into histories: distinct prefixes give distinct positive beta and hence distinct realized states/inputs from the same start. All combinations are legal, the endpoint is common, and the full energy bound holds. It is NOT a robust lower theorem. When m_d E exceeds (14), a boundary antipodal collision is proved by (15). This directly attacks the whole ball, rather than checking coordinate axes.

For off-cycle transfer, a necessary power region for a target D~n^delta is

    delta<=mu+chi, chi<=mu, delta>1,
    mu+tau<3/2, tau>=1/2.

Thus mu>1/2 and chi>1-mu are necessary for superlinearity from this block. An E-by-C one-amplitude-per-epoch/cohort protocol also has delta<=eta+chi, eta<=tau. For an epoch that satisfies the accepted half-high configuration, inherited complement can be reduced by a factor eta_settle using the SUFFICIENT duration

    d_cert=2 ceil((8000n/m) log(1/eta_settle)).

The factor two is essential: the accepted rate is per TWO steps. A protocol that allocates at least d_cert steps to each settled epoch has E<=floor((T-L)/d_cert)=O(mT/[n log(1/eta_settle)]). This is a cost of that sufficient certificate, not a universal packing obstruction or a necessary physical damping time. The necessary exponent region remains nonempty; for example mu=.65,tau=.75,chi=.39,eta=.39 is not ruled out. No finite-radius minimum gain is proved there.

For the COMPLETE channel, (14) additionally requires delta<=chi+max(mu,tau) whenever the direct-code term is sublinear and C has power growth. In the main schedule this forces chi>1/4 for a superlinear target, and such a target must use moving cycle input directions because (17) already caps the stationary block at O(n). In the logarithmic schedule, C=O((log n)^2) still gives a complete O(n) code; escaping it requires faster cohort-count growth and moving cycle novelty, not merely many donor epochs. These are necessary constraints, not a construction.

The exact missing statement is the robust antipodal width of the reachable COHORT-RESOLVED MATRIX of private row responses

    Vcal(g)=[V_c,N(g)-D_N(g)]_c,

on a fiber fixing the local direct code, bath Z_N, and donor D_N, in the actual induced metric (2). The matrix must be generated by the full renewal (1),(4),(5), not an ambient matrix ball. Growing C can escape Theorem A; m>>sqrt(n) or moving cycle columns can escape Theorem B. A true lower needs a uniform boundary gain after the full nonlinear integral transfer, not independent epoch counts. A true upper must compress this remaining matrix to O(n) coordinates. Neither is proved here.

## 10. Energy and final status

All proposed gate words preserve the accepted full raw-input bound

    ||X||2<=2sqrt(m(T+2)+1),

including preparation, every step, corrections, reset, source, and dense lift. The code does not remove any physical history energy. This is an UPPER bound only. No energy lower is deduced from mT.

The best positive corridor section remains the accepted 1D section, half-margin>.014999996, at mT<=11n(log n)^2 and ||X||<8sqrt(n)log n (or the accepted main family). No new joint D=omega(n) section is established. The best GLOBAL constructive exponent remains 3/4 with log power3/2; general threshold bracket [1/4,3/4] and full-model gap are unchanged. The complete moving corridor is still open, but its fixed-class multi-epoch extension and the small-m stationary-compensator amplifier are now bounded by explicit finite-error static codes.
