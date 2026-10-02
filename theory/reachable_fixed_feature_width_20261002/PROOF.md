# Finite-radius query width of reachable fixed-feature credit

2026-10-02. Bounded theoretical attempt, following the completed diagnostic.
**A joint linear-dimensional lower section is proved below. The general
linear-versus-superlinear reachable width remains OPEN.** These are new
author-derived arguments for independent hostile review, not reviewed results.
No new numerical witness search, experiment, architecture, or theorem review
is performed. Historical theory and diagnostic artifacts remain unchanged.

## 1. Scope, premises, and two different notions of width

Keep the accepted actual dense tanh family, c=1, gamma=1/n, epsilon=1/1000,
endpoint h=0, group-RMS normalization, and permitted future losses. Use ONE
public raw source vector H=(2/5)1_l, constant at all interior times. No source
column is independently injected or varied. Inputs remain in (-1/2,1/2)^n.

The completed experiment is motivation only:
experiments/fixed_feature_reachable_operator_20261002/REPORT.md. Its tangent
counts, separately visible axes, and sampled antipodes are not premises of a
dimension proof. The construction here is analytic; no history is optimized.

For an actual selected-source operator B in R^(n x r), define

    nu(B)=w_R ||H||_2 sup_(xi in C_0) ||B^T xi||_2.                 (1)

C_0 is the ACTUAL permitted effective late-adjoint family from h=0. Thus
nu(B1-B2) is the worst-query distance of selected normalized gradients.
This is not an RMS contract or an arbitrary-unit-adjoint replacement.

Let K_n be the family of such operators from admissible coupled histories
with the required endpoint. There are two different questions:

* Linear approximation width: the least dimension of a PUBLIC linear
  operator subspace approximating K_n to accuracy epsilon in (1).
* Continuous credit dimension: the least number of continuous real memory
  coordinates encoding a history, with a decoder answering EVERY permitted
  selected-source gradient query to uniform absolute error epsilon. No
  discarded-history replay or external history tape is allowed.

A jointly robust section gives a lower bound on the second quantity by the
accepted antipodal theorem. It is not enough to count tangent directions.
An upper bound for one of these notions does not automatically supply a
counted, continuously updated online encoder for the other.

The strongest bounds obtained here, for all integers n>=200, are

    floor(n/8) <= continuous fixed-feature credit dimension <= (k-1)^2,
    k=floor(n/2).                                               (2)

The upper in (2) concerns credit at the fixed endpoint. An online realization
also retains up to n actual forward-state coordinates while the history
arrives. The selected-source credit count is r^2, not full R/W/b credit.
The same order bounds hold for the linear operator approximation dimension.
In particular (2) does NOT prove an O(n) or O(n polylog n) upper.

## 2. Frozen model and units

Use the accepted definitions, with n>=200:

    a=1-1/n, k=floor(n/2), l=n-k, r=k-1, d=floor(n/4),
    delta=1/(100n),
    U=I-2ww^T/(w^T w), w=e1-1_k/sqrt(k),
    O=U(P_d direct_sum I_(k-d))U^T,
    R0=diag(a O, delta I_l),
    ||R||op=a, e=||R-R0||op<=4/(10^8 n^2),
    h_t=tanh(R h_(t-1)+W x_t+b), h0=0,
    W=I, b=(1/20)1, theta=(R,W,b), P=2n^2+n.

R is the previously specified fully dense matrix family; it is not replaced
by R0 in the actual forward computation. All parameter entries are independently
differentiated. The operator bound above is an accepted sufficient property of
that frozen dense recipe. No new matrix parameters are selected here.

O fixes physical e1. E is the n x r coordinate embedding of memory coordinates
2,...,k; O_* is the corresponding r x r orthogonal restriction. Thus R0 E=a E O_*.

    w_R=||R||F/n, w_W=1/sqrt(n), w_b=1/20,
    beta=max(1,||R||F), q=1_n/sqrt(n), loss=q^T h/beta.

Weights and beta are frozen model constants for differentiation. For n>=200,
||R||F >= a sqrt(k)-sqrt(n)e >1, so

    w_R/beta=1/n.                                              (3)

Every permitted late adjoint satisfies ||xi||<=kappa=a/beta. Use only the
accepted one-step input box v_i in [1/5,9/20] for the LOWER argument:

    xi(g)=R^T g/(beta sqrt(n)),
    g_hi=sech^2(1/4), g_lo=sech^2(1/2),
    s_g=(g_hi-g_lo)/2 >7/100.                                   (4)

The strict rational bound in (4) is an accepted query-box inequality. Longer
permitted futures are covered by the upper envelope, not discarded.

## 3. Actual coupled operator; uniform selected-source upper

For the actual parameter subblock K=delta R_(memory 2..k, source), holding each
realized input history FIXED when differentiating, the exact sensitivity is

    delta h_t=B_t K H,
    B_t=G_t(R B_(t-1)+alpha_t E), B0=0,
    G_t=diag(1-h_t^2), alpha_1=0, alpha_t=1 for t>=2.             (5)

This follows because h_(t-1),source=H at every interior step. B has ALL n state
rows and therefore includes dense leakage, return paths, and source feedback.
The injection is K H, not r*l freely selectable source values.

Define the reference using the SAME actual gates and source feature:

    M_t=G_*,t(a O_* M_(t-1)+alpha_t I_r), M0=0,
    Bbar_t=E M_t.                                              (6)

G_*,t is the restriction of G_t to memory coordinates 2,...,k. Because diagonal
gates preserve E and R0 E=a E O_*, Bbar is the R0 sensitivity with the same
coupled injection. Uniformly over history length and admissible gate histories,

    ||B_t||op, ||Bbar_t||op <=1/gamma=n,
    ||B_t-Bbar_t||op <=e/gamma^2.                               (7)

Indeed the difference recursion is

    B_t-Bbar_t=G_t R(B_(t-1)-Bbar_(t-1))
                         +G_t(R-R0)Bbar_(t-1),

and a geometric sum proves (7). Actual forward states are not approximated.
For EVERY allowed late query, (1), (3), and (7) give

    query error <=eta_n=w_R ||H|| kappa e/gamma^2
                       =a ||H|| e/(n gamma^2)
                       <=(1.6*10^-8) sqrt(l)/n <2*10^-9.        (8)

So r^2 stored entries of M, updated by (6), suffice for selected-source credit
at epsilon=1e-3 for arbitrary horizons. Add actual h (n coordinates) while
streaming; alpha is computed continuously from the previous actual source
state as H^T h_source/||H||^2. H, R, and other model constants are public. No
gate history, transport basis, or tape is hidden in the count. A future decoder
propagates the approximate initial sensitivity through ACTUAL future dynamics
and includes all known direct future injections; (8) controls the inherited
error. Those injections cancel in differences at the same endpoint.

More explicitly, with future continuation/loss Q supplied as the query, write
its selected gradient as w_R(B_T^T xi_Q)H^T+d_Q, where d_Q is the direct
future contribution determined by Q and the shared initial h=0. The decoder
uses w_R(M_T^T E^T xi_Q)H^T+d_Q. No discarded PAST is replayed. This is a
history-memory bound; transient work on a supplied future query is not bounded
here. No small-memory guarantee for newly varying future source features is
being silently added to the fixed-feature past class.

The public linear space {E M: M in R^(r x r)} also proves a linear-width upper
r^2 in metric (1). This is the existing quadratic selected-feature upper,
sharpened to its selected-source error constant, not a new generic compressor.

## 4. A stationary paired-coordinate subspace

Let

    m=floor((k-d)/2) >=floor(n/8),
    i_j=d+2j-1, j_j=d+2j, j=1,...,m,
    v_j=(e_(i_j)-e_(j_j))/sqrt(2) in R^k,
    psi_j=(v_j,0_l) in R^n, vbar_j=E^T psi_j.

All paired coordinates lie outside the first d latent coordinates and exclude
physical e1. They have zero coordinate sum. Hence w^T v_j=0 and

    U v_j=v_j, (P_d direct_sum I) v_j=v_j,
    O v_j=v_j, R0 psi_j=a psi_j.                                (9)

The v_j are orthonormal. More importantly EVERY linear combination of them
is fixed by O. This will prove input admissibility for the entire section,
not just its axes. The count follows since k-d>=floor(n/4), and halving and
flooring gives m>=floor(n/8).

## 5. One JOINT finite-radius, same-endpoint history section

Let u run over the CLOSED Euclidean unit ball in R^m. Set

    tau0=11/100, t0=1/20,
    z_(i_j)(u)=sqrt(tau0+t0 u_j),
    z_(j_j)(u)=-sqrt(tau0+t0 u_j),
    all other memory z coordinates=0.                         (10)

Every square root lies between sqrt(3/50) and 2/5. Thus z is smooth on a
neighborhood of the whole ball, |z_i|<=2/5, and O z=z by (9). It is NOT
necessary that z(-u)=-z(u); the gate differences will be exactly odd.

Choose N=3n. Prescribe the actual hidden trajectory

    h0=0,
    h_t=(0_k,H) for t=1,...,N+1,
    h_(N+2)=(z(u),H),
    h_(N+3)=0.                                                (11)

For each u realize it with the SAME frozen actual dense model:

    x_t(u)=atanh(h_t(u))-R h_(t-1)(u)-b.                       (12)

At the base model, substitution in the tanh recurrence proves (11) EXACTLY.
The formula defines input histories using the public frozen parameter value.
When calculating parameter sensitivities, these realized inputs are held
fixed; we do NOT differentiate (12) through theta.

For R0, every input coordinate is bounded in magnitude by

    atanh(2/5)+1/20 < 12/25=.48

or by 2/5+1/20=.45. This uses O z=z at the final reset, not a loose dense
row-sum estimate. Sources have slow-free recurrence delta; during the warmup
memory states are zero. The actual dense correction in (12) is at most

    e ||h_(t-1)|| <=(2/5)e sqrt(n) <.001.

Thus ALL combinations in (10), not just one coordinate at a time, stay strictly
inside the original input cube. Source direction H never changes; all endpoints
are the exact same h=0. This is one genuine continuous section.

### 5.1 Physical finite radius, independent of width

Compare with the center history X(0). Only the pulse input and final reset
input depend on u. For each pair the square-root difference identity gives

    ||z(u)-z(0)|| <=L_z ||u||,
    L_z=sqrt(2)t0/(sqrt(tau0-t0)+sqrt(tau0)) <31/250.

On [-2/5,2/5], atanh is (25/21)-Lipschitz. Since ||R||op=a<1,

    ||X(u)-X(0)||_(total input L2)
        <=L_z sqrt((25/21)^2+a^2) ||u|| <1/5.                  (13)

This is a NON-infinitesimal history patch of physical radius below .2, uniform
in n and measured in the same total-input L2 units as the diagnostic. It is
NOT a proof at the diagnostic's radius .05. Epsilon and gradient units have
not changed. No radius is inferred from a tangent spectrum.

## 6. Exact affine dependence of the selected sensitivity

The only history-dependent gate is the pulse. Let P_j project onto the two
physical memory coordinates of pair j. Then, in the full n-state system,

    G_p(u)=G_p(0)-t0 sum_j u_j P_j.                            (14)

Source gates at the pulse are constant, all previous gates are constant,
and the final zero reset has G_T=I. Put

    Bpre=B_(N+1), V=R Bpre+E.

Equation (5) becomes, EXACTLY for the actual dense model,

    B_T(u)=R G_p(u) V+E,
    B_T(u)-B_T(v)=-t0 R [sum_j(u_j-v_j)P_j] V.                (15)

Although histories (10)--(12) are nonlinear functions of u, the selected
sensitivity endpoint is affine in u. Equation (15) includes every mixed
combination, all dense feedback, and the tied propagation/injection. No
curvature or tangent approximation is being promoted to finite-radius proof.

For the reference, the N warmup injections give

    Mpre=sum_(s=0)^(N-1) a^s O_*^s,
    Mpre vbar_j=m_N vbar_j,
    m_N=(1-a^N)/(1-a) > (19/20)n.                             (16)

The last bound follows from a^(3n)<exp(-3)<1/20. On each pair,

    M_T(u) vbar_j=[a(a m_N+1)(1-tau0-t0 u_j)+1] vbar_j.

Thus for ANY u,v in the ball,

    (Bbar_T(u)-Bbar_T(v)) vbar_j
       =-t0 a(a m_N+1)(u_j-v_j) psi_j.                       (17)

## 7. ONE actual permitted query gives a uniform lower margin

Use the following fixed one-step future input, the same for ALL section points:

    future v_(i_j)=1/5, future v_(j_j)=9/20,
    every other future coordinate=1/5.

At h_T=0, W=I and b=(1/20)1, this produces g_(i_j)=g_hi,
g_(j_j)=g_lo. Hence

    psi_j^T g=sqrt(2)s_g,
    psi_j^T xi=(a sqrt(2)s_g+d_j)/(beta sqrt(n)),
    |d_j|<=e sqrt(n).                                        (18)

This is the ACTUAL future adjoint, using R, not R0. Its coordinates need not
be idealized and are uniformly positive in these projections for n>=200.

The selected normalized gradient is w_R(B_T^T xi)H^T. Project it onto the
orthonormal parameter directions

    Phi_j=vbar_j H^T/||H||.

Projection cannot increase Frobenius norm. Equations (3), (17), and (18) show
that the reference queried difference has norm at least

    ell_n ||u-v||,
    ell_n=t0 a(a m_N+1)||H||/(n sqrt(n))
                              *[a sqrt(2)s_g-e sqrt(n)].     (19)

Unselected parameter coordinates and state rows are NOT assumed zero. They
cannot cancel this valid orthogonal projection of the full answer.

### 7.1 Dense correction proportional to the finite displacement

A constant endpoint error would suffice for antipodes. We instead prove a
Lipschitz correction, so the whole section has a query bi-Lipschitz lower.
From (7), at the warmup endpoint,

    ||Bpre-E Mpre||op<=e n^2,
    V0=R0 E Mpre+E,
    ||V-V0||op<=e n+a e n^2,
    ||V0||op<=a n+1.

For D(u-v)=sum_j(u_j-v_j)P_j, ||D||op<=||u-v||_2. Subtracting the two
finite affine maps (15), actual minus reference, gives

    ||[B_T(u)-B_T(v)]-[Bbar_T(u)-Bbar_T(v)]||op
       <=t0 e(n+1)^2 ||u-v||.                               (20)

Using the SAME actual future adjoint (or any permitted one), its normalized
query error is at most

    zeta_n ||u-v||,
    zeta_n=t0 a ||H|| e(n+1)^2/n.                            (21)

There is no switch of physical norm. Direct future injections cancel because
all endpoints are h=0; in the R block the immediate future injection is zero.

### 7.2 Explicit strict constants

For n>=200, a^3>(49/50), m_N/n>19/20, sqrt(2l/n)>=1, and s_g>7/100. Dropping
the positive extra term in (19) yields the leading lower

    t0*(2/5)*(49/50)*(19/20)*(7/100)
       =13034/10^7=.0013034.

The negative future-R correction in (19) is at most

    t0 (n+1)||H|| e/n <10^-9,

and zeta_n<10^-9 by e<=4/(10^8 n^2), ||H||=(2/5)sqrt(l). Therefore

    nu(B_T(u)-B_T(v)) >=(ell_n-zeta_n)||u-v||,
    ell_n-zeta_n >13/10000=.0013.                            (22)

The upper is also uniform over the WHOLE ball and ALL permitted queries:
||V||op<=a n+1=n, so (15) and w_R kappa=a/n imply

    nu(B_T(u)-B_T(v)) <=t0 a^2 ||H|| ||u-v||.                (23)

This upper may grow like sqrt(n); no width-independent upper Lipschitz constant
is asserted. The positive LOWER in (22) is width independent and is what the
finite-error dimension lower needs. A single legal query proves it; neither
an RMS visibility assumption nor an ambient operator ball is involved.

## 8. Genuine joint dimension consequence

On ||u||=1, (22) gives

    nu(B_T(u)-B_T(-u))/2 >.0013>epsilon.

For any continuous history encoder with fewer than m real coordinates,
composition with the section (10)--(12) maps the boundary S^(m-1) into R^k,
k<m. By the already accepted antipodal theorem, some u,-u share memory.
The decoder must give the same answer to the fixed query in section 7, but
the two true answers are more than 2epsilon apart. They cannot both have
error <=epsilon. Hence at least m>=floor(n/8) credit coordinates are necessary.
The antipodes are u,-u in the section's parameter sphere. Physical histories
X(u)-X(0) need not be odd or straight; the accepted topological argument requires
continuity of the section, not linearity of its embedding in history space.

The SELECTED operator patch itself is an affine m-dimensional set by (15)
and has rank m by (22). Thus m coordinates also encode this particular patch
exactly. This does not upper-bound the union of arbitrary gate histories.
The construction uses one nonscalar pulse; it is not evidence that arbitrarily
many nonscalar events can be summarized by m coordinates.

For the linear-width question, project the fixed-query outputs onto Phi_j.
The affine patch centered at u=0 contains, in this m-dimensional output space,
a ball of radius ell_n-zeta_n>epsilon. Any public operator subspace of
dimension <m has fixed-query projected image of dimension <m. A perpendicular
output direction proves that it cannot approximate the whole patch to epsilon.
This lower is distinct from, and does not replace, the continuous argument.

## 9. Finite gate-dissipation ledger, with the coupled source retained

The accepted adjoint energy inequality can be combined with an exact finite
gate-difference identity. This supplies a more precise unresolved object than
"gate damage times the full old-credit norm"; it does NOT finish a width upper.

Take any TWO actual histories of the same length T in the fixed-source class,
with gates G_s, Gtilde_s and operators B_s, Btilde_s. Let

    DeltaG_s=G_s-Gtilde_s,
    Vtilde_s=R Btilde_(s-1)+alpha_s E,
    p_T=xi, p_(s-1)=R^T G_s p_s.

Then the exact finite Duhamel identity is

    (B_T-Btilde_T)^T xi
          =sum_(s=1)^T Vtilde_s^T DeltaG_s p_s.               (24)

It is not a tangent formula. Each Vtilde includes the real old credit AND the
current shared-feature injection; the controls are never made independent of
that trajectory. For actual ||R||op=a, telescoping yields

    (1-a^2) sum_s ||p_s||^2
       +a^2 sum_s ||Gamma_s p_s||^2 <=||xi||^2,
    Gamma_s=(I-G_s^2)^(1/2).                                 (25)

Indeed ||R^T G_s p_s||^2<=a^2||G_s p_s||^2. No commutation or scalar-gate
assumption is used. This is the known energy budget, not a new claim that
such a budget by itself bounds continuous dimension.

Let P_s project onto ker Gamma_s; let dagger denote the diagonal generalized
inverse (zero on that kernel). Define the r x n matrices

    A_s=Vtilde_s^T DeltaG_s Gamma_s^dagger,
    D_s=Vtilde_s^T DeltaG_s P_s,
    L_A=||sum_s A_s A_s^T||op^(1/2),
    L_D=||sum_s D_s D_s^T||op^(1/2).

Because DeltaG is diagonal and commutes with Gamma and P,

    Vtilde_s^T DeltaG_s p_s=A_s Gamma_s p_s+D_s p_s.

The block-matrix Cauchy-Schwarz inequality and (25) give the HORIZON-UNIFORM
finite-difference implication

    nu(B_T-Btilde_T)
       <=w_R||H|| kappa [L_A/a+L_D/sqrt(1-a^2)].              (26)

This bound uses operator Gramians of the finite, source-weighted discrepancy,
not sum_s ||Vtilde_s|| multiplied by a gate norm. It is a true upper for ALL
permitted queries, although using kappa can still be quite conservative.
The kernel term is necessary: a gate can equal one in the first history and
be smaller in the other, so dividing by gate dissipation alone would be invalid.
If DeltaG vanishes on every such kernel, L_D=0.

An epsilon-small bound on the right of (26) is sufficient for a finite query
collision/approximation bound. No uniform small L_A/L_D or low-dimensional
family of them is proved. In particular (26) is NOT a continuous encoder.

## 10. Why this does not dispose of the weak mixed tail

1. The new section proves that a LINEAR number of joint directions is genuine,
   not only separately visible. It is located in paired stationary modes and
   uses one pulse. It neither realizes nor kills the diagnostic's mixed tail.
2. Adjoint energy (25) is per query. Bounding each query and then summing
   worst-case contributions across directions can lose a width factor. A
   supremum over queries is not interchangeable with a sum of suprema.
3. The old source-weighted credit Vtilde in (24) can be large even when each
   gate defect is small. Source Gramians in (26) retain that coupling but do not
   make it small. The exact paired section already contains old credit of
   order n before its pulse. A dissipation-only counting argument misses it.
4. Gamma_s^dagger can be large for weak gates; when a gate has no loss, the
   D_s term is required. Dropping these cases would exclude allowed histories.
5. Rotations separated by d steps coincide only without intervening gate
   defects (or in the accepted structured special cases). Exact correlation
   in an experiment does not bound every finite-radius multigate remainder.
6. Numerical strong cutoffs and weak tails give no uniform finite coefficient
   budget on ONE admissible section. Likewise an ambient r^2 ball cannot be
   substituted for that missing lift.

No O(n), O(n polylog n), or superlinear jointly robust result for the GENERAL
reachable fixed-feature family has been established in this attempt.

## 11. Consequences and smallest remaining obstruction

The strongest new theorem is the explicit n>=200 fixed-feature patch with
m>=floor(n/8), physical history radius<.2, exact h=0, and query lower
Lipschitz constant>.0013. It improves a separately visible-axis diagnostic
to a true continuous finite-radius lower, without extending it to a new
numerical width or modifying any accepted theorem.

For arbitrary aperiodic admissible histories the bounds are still only

    Omega(n) <= fixed-feature continuous query dimension <= O(n^2).

The full credit problem remains Omega_c(n^2) to O_c(n^2 log n). Even a fixed-
feature O(n) result would need compatible, counted simultaneous feature
summaries to supply the full quadratic encoder. A superlinear one-feature
section alone would not establish a logarithmic factor in full credit: a
single r x r selected operator already costs O(n^2), and many different
feature/history sections cannot be added as independent dimensions.

The smallest remaining mathematical obstruction is a UNIFORM finite-radius,
worst-query bound on the jointly varying mixed transported-credit remainder
for arbitrary gate words. Equation (26) specifies a source-weighted finite
error test, but its Gramians have no proved O(n)-width or controlled tail.
Resolving that requires either a finite-error reachable-set width estimate
including gate variations, or a superlinear jointly admissible antipodal
section. No constant-packet, basis-renewal, RMS, raw-rank, or ambient-ball
reduction is asserted.

No architecture, learning, gamma=1/n^2, finite-bit, VRAM, conditioning,
or practical performance claim follows. Stop at this theory stage.
