# Repair of the two-block D=2 corridor square

Codex, 2026-10-05. **New author-derived theorem; independent hostile review required.** STATUS.md's PROVED is a derivation status, not repository ACCEPTED/VERIFIED. Historical reports are unchanged. Base: `5a9cae006494f7458446af6731aeb48124d04ade`.

## 1. Precise result and dependencies

For every integer n >= 10^200, the existing frozen dense tanh family and fixed-feature/legal-query contract admit the two-donor/two-survivor square described below. It is one continuous same-endpoint B^2 section. Every boundary antipode has actual normalized gradient **pair distance >0.009**, hence **antipodal half-margin >0.0045 > epsilon=0.001**. Full absolute input norm is <8 n^(5/8) and mT <=11 n^(5/4). This proves only D=2, not superlinear dimension, an improved superlinear energy exponent, or a complete corridor compression theorem.

The historical statement `nu >0.009` is a pair-distance bound. Calling it half-margin >0.009 would not follow from that arithmetic. The present result states both conventions explicitly.

Accepted dependencies: the moving-corridor inverse lift and absolute-energy bound; full reference Householder identity; public bath/front state bounds; complement damping; legal one-step query construction; dense pair comparison <=8e-9. These are in:

- ../codex_unpaired_corridor_sensitivity_20261003/PROOF.md, sections 1--5;
- ../codex_private_renewal_gamma_20261003/PROOF.md, sections 2, 5--10;
- ../codex_timing_signal_J_20261004/PROOF.md, section 3.1, with ../grok_timing_signal_J_review_20261004/REPORT.md.

No D=2 result, frozen-matrix spectral sign claim, disjoint-packing necessity, or later spatial-write result is a premise. The complete front is retained before bounding its influence. The bath sequence is not replaced by a constant.

## 2. Histories and the exact differentiated object

Let k=floor(n/2), l=n-k, r=k-1, d=floor(n/4), a=1-1/n,

    gamma=1/(1-1/sqrt(k)), c=gamma^2/k,
    m=4 floor(sqrt(n)/4), h=m,
    T=ceil(10 n^(3/4)), L=ceil(1000 log n), t0=T-L.

Here log is natural. There are m tuples total, each containing two moving positive cycle sites and two stationary negative compensators. Partition tuples equally into D1,S1,D2,S2. Each group has h=m physical sites. Geometry is the existing A=2(m+T+4), B=5(m+T+4), with no wrapping or contact with the exceptional front. m+T+4 <=d/100 holds on the stated n range.

Prepare exactly as in the accepted corridor, from the required public zero start. For 1<=t<=t0 set both survivor group gates to g_H=1-n^(-2), and donor i gate to

    g_i(theta_i)=g_L+(theta_i+1)(g_H-g_L)/2,
    g_L=199/200, theta in [-1,1]^2.

For t0+1,...,T-1 use g_L on both donors, retain g_H on survivors, then apply the scalar trace corrections in section 9. Reset at N=T+1 is public.

Every tuple has state (+beta,+beta,-beta,-beta), beta=sqrt(1-g). Consequently the public state bath and front gate schedules do not depend on theta. This follows from the actual inverse lift and zero-sum state pairing; it does NOT assert sensitivity cancellation. Differentiation keeps each realized raw input fixed.

For probe v1 put +1/sqrt(m) on the m/2 stationary compensator sites of D1 and -1/sqrt(m) on the m/2 compensator sites of S1; all other entries are zero. Then ||v1||=1, sum v1=0, and O_* v1=v1. v2 uses D2,S2 and is orthogonal to v1. The actual recurrent parameter probe is (E vi) f_s^T with the accepted unit source feature f_s. The complete reference sensitivity on a probe is

    x_0=0, x_t=G_t(a O_* x_(t-1)+v),
    O_*=C+1 u^T+e1 v_H^T,
    u^T=(gamma/sqrt(k))e_(d-1)^T-c1^T,
    v_H^T=(gamma/sqrt(k))1^T.                         (1)

Preparation has zero reference R-credit because its preceding source is zero. Source magnitude sigma satisfies .0499<sigma<.051 and reference physical sensitivity is sigma sqrt(l) E x_t. Node0/source leakage in the actual dense model is charged in section 11.

## 3. Exact group-plus-front reduction: the five-state model is not exact

For the low extreme of channel 1 let Y_D,Y_S,Y_I,Y_R be the four group sums of x_t; Y_S is the S1 sum, Y_R the S2 sum, and Y_I the idle D2 sum. Their forcings are +iota,-iota,0,0 with iota=sqrt(h)/2. The ordinary nondriven row value is Z_t, exceptional row values are F_(z,t), 1<=z<=t. Let J_t=u^T x_t, B_t=v_H^T x_t. Exact equations, including every Householder path, are

    Y_D,t=g_L[a(Y_D,t-1+h J_t-1)+iota],
    Y_S,t=g_H[a(Y_S,t-1+h J_t-1)-iota],
    Y_I,t=g[a(Y_I,t-1+h J_t-1)],
    Y_R,t=g_H[a(Y_R,t-1+h J_t-1)],
    Z_t=a q_t(Z_t-1+J_t-1),
    F_1,t=a f_1,t(J_t-1+B_t-1),
    F_z,t=a f_z,t(F_z-1,t-1+J_t-1), z>=2,
    S_tot,t=sum Y_t+(r-4h)Z_t+sum_(z=1)^t(F_z,t-Z_t),
    J_t=gamma Z_t/sqrt(k)-c S_tot,t,
    B_t=gamma S_tot,t/sqrt(k).                       (2)

These follow by summing (1): moving-cycle predecessors remain in their group, compensators are stationary, and the terminal cycle row still equals Z. The complete exact state includes the front values; Y and Z alone are not a closed exact state.

Write z=(Y_D/h,Y_S/h,Y_I/h,Y_R/h,Z), mu=ch, and

    alpha=gamma/sqrt(k)-c(r-4h)=-gamma+4mu,
    w=(mu,mu,mu,mu,-alpha), w^T1=gamma,
    rho_t=-c sum_(z=1)^t(F_z,t-Z_t).

Then J_t=-w^T z_t+rho_t. The exact five observed components satisfy

    z_t=a D(q_t)[I-1 w^T]z_t-1+D(q_t)f
                         +a D(q_t)1 rho_t-1,
    D=diag(g_L,g_H,g,g_H,q_t),
    f=(s,-s,0,0,0), s=1/(2sqrt(h)).                 (3)

The auxiliary system z^5 drops only rho, **not** q_t. Its chronological propagator is A(q_t)...A(q_s) with A(q)=a D(q)(I-1w^T). The full-front comparison is section 7, rather than an unsupported claim of exact five-dimensional closure.

## 4. The sign actually needed; corrected orientation

Let beta(g)=Y_S(t0)/sqrt(h). A matched active donor has x_match= kappa v1 exactly for every idle donor history, where

    kappa=g_H sum_(j=0)^(t0-1)(a g_H)^j.

Thus its S1 overlap is -kappa/2. The positive read gap is

    G(g)=beta(g)+kappa/2,                             (4)

not `-kappa/2-beta(g)` with a positive lower bound. In the auxiliary system it suffices to prove partial beta^5/partial g <=0 throughout [g_L,g_H], with the actual q_t held fixed. Then beta^5(g)>=beta^5(g_H). The full system will inherit a finite-error gap from this comparison; we do not claim its exact derivative has been signed.

The auxiliary derivative obeys exactly

    d_t=A(q_t)d_t-1+a(z^5_I,t-1-w^T z^5_t-1)e_I.       (5)

There is no derivative of the bath word, and the idle group has no direct probe forcing. Required: the scalar source in (5) is nonnegative and every chronological impulse e_I has nonpositive response on S1. Both facts are proved below for every changing q sequence.

## 5. Common invariant cone for the forced source

All weights w_i are positive. Put d_H=g_H and delta=gamma-1. On the theorem range w_b=-alpha>.9, delta is less than 10^(-90), and

    sum_nonH w_i(1-g_i/g_H)-delta >0.0006.            (6)

Here nonH are D1,D2,bath; their ratios are <=1. The bath alone contributes >.9*.0007, since q_t<=.9992 and g_H=1-n^-2. Equivalently sum_i w_i g_i <=g_H. These explicit bounds are extremely conservative.

Let S=w^T z^5. The cone is

    z_D>=0, z_I>=0, Z>=0, S<=0.

Starting at zero it is preserved at EACH step. Indeed the three outside-high updates have nonnegative preinputs z_i-S and nonnegative direct forcing. Also

    S^+=a(g_H-sum_i w_i g_i)S
             +a sum_nonH w_i(g_i-g_H)z_i
             +mu s(g_L-g_H) <=0.                    (7)

No restriction on the signs of z_S,z_R is used. Equation (6) signs the first coefficient; the other terms have the signs displayed. Hence a(z_I-S)>=0 at every time. This proves the variational source sign without the historical unsupported forced-cone assertions.

## 6. A common POSITIVE coordinate realization of the chronological Green function

Consider a homogeneous impulse starting in D2, with both high survivor values initially zero. Those two survivor values remain equal. Divide the state after j steps by (a g_H)^j. Write the common high value as -U. The three other values are z_i, with time-dependent d_i=g_i/g_H in [0,1]. Define

    r_i=z_i+U,
    P=U+S=sum_nonH w_i r_i-delta U,
    B_t=sum_nonH w_i(1-d_i,t).

An EXACT change of coordinates gives

    U^+=P,
    r_i^+=d_i,t r_i+(1-d_i,t)P,
    P^+=sum_nonH w_i d_i,t r_i+(B_t-delta)P.         (8)

These identities are just multiplication of diag(d)(I-1w^T), not eigenvalue arguments. At the impulse, U=0, r_i>=0 and P=w_I>0. By (6), all coefficients in the last two recurrences are nonnegative for every q_t. Therefore r_i,P remain nonnegative under EVERY time-ordered product, U^+=P>=0, and the high output is nonpositive.

The four-state symmetric-high subsystem has coordinates (P,r_D,r_I,r_b). The transform is invertible for delta>0, using U=(sum w_i r_i-P)/delta. It is ill-conditioned as n grows; it is used only to prove signs, not as a finite-precision algorithm. This establishes a common order structure for the actual varying-q AUXILIARY recurrence. The unused antisymmetric high coordinate has scalar propagation and is zero for this impulse.

Combining (5), (7), (8) by variation of constants proves

    partial beta^5(g)/partial g <=0                  (9)

for all g in [g_L,g_H], every horizon, and every admitted changing bath word. In particular the transition band is covered. Powers of a frozen A(q) are never substituted for chronological products.

## 7. Quantitative comparison with the COMPLETE exceptional front

The accepted public state bounds are .032<u_t<.1, .99<q_t<=q_*=.9992, first-front gate f_1,t<=1/n, and

    0<=q_t-f_z,t<=2 q_*^(z-1), z>=2.                (10)

For clarity their mechanism is state geometry, not a credit sign assumption: the first front preactivation is >.02 sqrt(k), so sech^2 is <=4exp(-.04sqrt(k))<=1/n. Each subsequent front preactivation is at least the bath's. Mean value for tanh on that interval contracts the front-minus-bath state difference by q_*; squaring hidden values gives the gate difference in (10). The driven tracks never enter this front. These public schedules are the same for both histories.

From orthogonality in (1), ||x_t||<=t, ||u||<3/sqrt(n), ||v_H||<2. Thus |J_t|<=3t/sqrt(n), |B_t|<=2t. Geometric summation of the exact bath update gives |Z_t|<=4000t/sqrt(n). Put D_z,t=F_z,t-Z_t. Its first value has

    |D_1,t|<=5000t/sqrt(n).

For z>=2 subtraction of the two exact updates gives

    D_z,t=a f_z,t D_z-1,t-1
                  +a(f_z,t-q_t)(Z_t-1+J_t-1).

Induction with (10) yields, uniformly for all idle gates,

    |D_z,t|<=10000 z q_*^(z-1)t/sqrt(n),
    sum_z |D_z,t|<=2*10^10 t/sqrt(n),
    |rho_t|<=6*10^10 t/n^(3/2).                     (11)

The infinite geometric sum here upper-bounds the finite front: sum z q_*^(z-1)=1/(1-q_*)^2=1,562,500. Thus no growing T multiplier is discarded.

Use the weighted norm ||z||_w^2=sum w_i z_i^2. The undamped five-state matrix I-1w^T is similar to the symmetric matrix I-sqrt(w)sqrt(w)^T, whose eigenvalues are 1 and 1-gamma. Since 0<gamma<2 it has norm <=1 in this norm. Every diagonal D(q_t) has norm <=1. The true chronological five-state propagator consequently has weighted norm <=a^(t-s); no frozen eigenvectors are used.

Subtracting (3) from its rho=0 counterpart, using sqrt(gamma)<2, gives

    ||z_t-z^5_t||_w<=1.2*10^11 t^2/n^(3/2),
    |beta_t-beta^5_t|<=10^12 t^2/n.                  (12)

The second bound uses sqrt(h)/sqrt(mu)=1/sqrt(c)<=sqrt(n). This is a uniform finite-amplitude comparison on the whole gate square. It charges every front/Householder insertion, not a perturbative insertion truncation. At t0<=11n^(3/4) its error relative to kappa is <2*10^13 n^(-1/4), hence far below 10^(-30) on n>=10^200.

## 8. Endpoint of the comparison and the uniform early read

At g=g_H, the high set is D2 union S1 union S2, with 3h physical sites. Its co-moving zero-sum space is exactly invariant under O_* and G. The projection p_t of v1 onto that space has S1 overlap -1/3; therefore

    x_t(g_H)=kappa_H(t)p_t+e_t,
    ||e_t||<=16000n/m.                              (13)

This uses the accepted two-step complement-damping proof, not a frozen-q approximation. With high-support size 3m, its leakage satisfies ell^2>=3m/k>=6m/n; the same squared-norm proof gives two-step contraction at least m/(8000n), so the conservative 16000n/m forcing sum still applies. All other selected gates are <=.9992, even on the public front. The complement forcing norm is <=1.

It follows that beta(g_H)>=-kappa/3-16000n/m. Applying (9), then (12) twice, gives the REQUIRED full-system comparison, without asserting full exact monotonicity:

    beta(g)+kappa/2
      >= kappa/6-16000n/m-2*10^12 t0^2/n.            (14)

This holds for every g in [g_L,g_H] and the actual public bath/front sequence. Bernoulli and t0=T-L give kappa>=.998T. Both error terms in (14), divided by kappa, sum to <10^-30 at n>=10^200. This is a finite-radius uniform bound, not a Jacobian dimension inference.

## 9. Trace corrections and the terminal tail

For each donor group independently, after L-1 common g_L steps define

    kappa_target=kappa(g_L;T),
    g_last(theta_i)=kappa_target/(1+a kappa_theta_i,T-1).

The scalar trace recurrence kappa_t=g_t(1+a kappa_t-1) proves exact final matching. Prefix traces lie between the all-low and all-high traces; hence

    0<=kappa_theta,T-1-kappa_low,T-1
            <=T (.995)^(L-1)<=12 n^(-17/4),
    .994<g_last<=.995,
    |g_last-g_L|<=12 n^(-17/4).                      (15)

These corrections are continuous in both coordinates and have no cross-coupling: local compensator traces use their own gate word. Their effect on full credit is not assumed to vanish. Changing one history's last gate costs at most 144 n^(-7/2) on a unit probe; two histories cost at most 288 n^(-7/2). The gate is common to all four sites of that donor tuple, so balanced state pairing remains exact.

For any square boundary antipode, select a channel whose theta_i is +/-1. Its two early histories are matched and low, while its idle donor gates can be different. The matched probe response is independent of the idle gate; (14) bounds the low response for EVERY idle gate. Thus their early read has the uniform positive gap (14).

Both donors then have identical g_L gates until the last correction. The full homogeneous difference is contracted by aG O_*. For w_t=1_(S_i(t))/sqrt(m),

    w_t^T O_* w_t-1=1-cm,
    ell^2=1-(1-cm)^2<=6m/n.

The per-step read drift is at most [(1-ag_H)+cm+ell]||Delta x||. Here 1-ag_H<=2/n<=ell and cm<=ell. Before the last correction ||Delta x||<=2t0<2.01kappa, so the whole common tail costs at most 7L ell kappa. Put

    E_early=16000n/m+2*10^12t0^2/n,
    eta=288 n^(-7/2).

Thus the final interior read and norm obey

    |beta_T| >= kappa/6-E_early-7L ell kappa-eta,
    ||Delta x_T|| <2.02kappa.                       (16a)

The public reset has gate q_N>.99 on the co-moving survivor support. Orthogonality gives the EXACT row identity

    w_(t+1)^T O_* = (1-cm) w_t^T + r_t^T,
    ||r_t||=ell.

Hence beta_N=a q_N[(1-cm)beta_T+r_T^T Delta x_T]. Since a q_N>.98, the reset and one future O_* together give

    |w_(T+2)^T O_* Delta x_N|
      >= .98 |beta_T|-2(cm+ell)2.02kappa
      >= [.98/6]kappa-E_early-(7L+9)ell kappa-eta
      > .16 kappa.                                 (16b)

The first inequality uses ||Delta x_N||<=||Delta x_T|| and bounds both leakage terms in absolute value. Direct new forcing cancels in the pair; it is not omitted individually.

Explicit sufficiency: E_early/kappa<10^-30,
(10L+20)sqrt(6m/n)<10^-30, and eta/kappa<10^-30. All hold at 10^200 and decrease thereafter. The leading retained factor is .98/6>.1633, leaving ample room above .16. Reset carries private credit; it is not treated as erasure.

## 10. One ball, same endpoint, full absolute energy

The continuous gate square, including (15), stays in the accepted corridor range (.994,1). The existing inverse lift is applied with every actual raw input counted; no policy derivative is taken. Paired states guarantee the same public bath/source and the same exact reset endpoint for all theta. Each history starts from the required zero state, with full norm

    ||X(theta)||<=2 sqrt(m(T+2)+1)<8 n^(5/8),
    mT<=11n^(5/4).                                  (17)

This includes preparation, source/bath, interior steps, trace correction, reset and dense lift. A public baseline is not subtracted.

For y in B^2 use the odd homeomorphism theta(y)=||y||_2 y/||y||_infinity for y!=0, theta(0)=0. Its boundary has max|theta_i|=1. Every point gives one jointly legal history, and antipodes map to opposite square points. The controls are injective during the early window. The whole section is continuous and finite-radius. The argument uses the ENTIRE boundary, not separately good axes.

## 11. Actual normalized legal-query distance

For the selected survivor block use two legal one-step preactivation patterns, differing only by .25 versus .75 on S_i(T+2). Let s_gate=(sech^2(.25)-sech^2(.75))/2>.17. The same two queries are available for both histories; future inputs are realized from the common endpoint and then frozen.

The difference between these two query readouts, followed by the triangle inequality, gives

    nu_reference(Delta M_N)
      >= sigma sqrt(l) a s_gate sqrt(m)/(n sqrt(n))
                |w_(T+2)^T O_* Delta x_N|
      > (.0499*.99*.17/sqrt(2)) *.16 kappa sqrt(m)/n
      >.0093.                                      (18)

For the last inequality kappa>=9.98n^(3/4), sqrt(m)>.994n^(1/4), and sqrt(2)<1.415 suffice. This is the worst permitted-query supremum, bounded below by genuinely permitted witnesses, not RMS visibility or an arbitrary unit adjoint. Projection onto the FIXED unit parameter probe is a legitimate lower on the normalized gradient group norm.

The dense comparison for the entire pair is <=8e-9, giving actual pair distance >.0093-8e-9>.009. All future direct terms cancel because current endpoints agree. Thus every boundary antipode has half-margin >.0045>.001. Borsuk--Ulam applied to any continuous memory code of fewer than two coordinates would yield equal encoded antipodes, contradicting this pair gap under the accepted error contract. This establishes the scoped D=2 lower.

## 12. Spectral sign corrections and limits

For a frozen rank-one matrix A=D+r sig^T with b_i=sig_i r_i<0, the secular f(lambda)=sum b_i/(lambda-d_i) satisfies

    f'(lambda)=-sum b_i/(lambda-d_i)^2>0,
    Im f(x+iy)=-y sum b_i/((x-d_i)^2+y^2)
               =+y sum |b_i|/((x-d_i)^2+y^2).

The historical negative derivative and negative imaginary signs are wrong. Across adjacent poles the relevant branch increases from -infinity to +infinity, not decreases in the reverse direction. Residues also need their common negative left-right normalization. NONE of that spectral argument is used by this repair. The overlap orientation is independently corrected in (4).

What remains unproved: exact monotonicity of the full front-inclusive beta(g); necessity of the historical disjoint-packing cap; any third dimension, growing-dimensional/superlinear extension, or complete-corridor compression. The claimed >.009 half-margin interpretation is not proved; the pair-distance claim is. The new D=2 derivation, especially (8), (11)--(12), and the tail/query factors, needs independent hostile review before repository acceptance.
