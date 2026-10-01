# Finite-error observability: conditional bounds and conditioning attacks

Status: new quantitative arguments for independent review. Accepted exact
accessibility and exact continuous-state results are premises, not reproved.
Numerical diagnostics are separate from these arguments. No architecture claim.

## 1. Computational and error model

Fix theta=(R,W,b), h and a reachable compact sensitivity family K. A past
history X produces S(X)=d h/d theta. A deterministic encoder retains M(X),
with no past replay, external tape or uncounted history-dependent buffer.
After encoding, an adversary may choose any query in the declared family.
The decoder must answer every such query with absolute error

    ||g_hat(M(X),query)-g(X,query)||_2 <= epsilon.

The error is worst case over K and queries, not average over a training
distribution. Fixed model constants and query descriptions are available to
both sides. h is fixed and may be supplied to the decoder. This lower-bound
restriction does not charge the same h twice. Encoding may depend on extra
history; a continuous local history section, supplied by the quantitative
inverse construction below, reduces it to an encoding on K when needed.

Primary gradient units are derivatives in the raw R/W/b coordinates. Primary
losses are L_c(h)=c^T h with ||c||_2<=1. Their gradient is S^T c. For a future
continuation, its direct parameter injection must also be included. At the
same starting h it is identical for both histories, hence cancels in gradient
differences. It cannot be dropped when h differs.

Relative error is a different contract:

    ||g_hat-g||_2 <= epsilon_rel ||g||_2.

Two colliding histories then require ||g1-g2||<=epsilon_rel(||g1||+||g2||)
for each query. There is no uniform conversion to an absolute contract when
gradient norms vanish, cancel, or are dominated by common future injection.
Our packing theorem uses absolute error. No practical epsilon is selected;
all conclusions state epsilon relative to explicit patch/query scales.

## 2. The query metric, exactly

For Delta=S1-S2 and unit Euclidean adjoints,

    D_unit(S1,S2)=sup_{||c||_2<=1} ||Delta^T c||_2
                =||Delta||_{2->2}.

This is the largest singular value of Delta, not its Frobenius norm and not
the rank of S. Because Delta has at most n singular values,

    ||Delta||_F/sqrt(n) <= D_unit(S1,S2) <= ||Delta||_F.

For a general normalized family C, D_C is a seminorm of the difference. If
all ||c||<=1 and C contains a Euclidean ball c0+r_c B_2, then

    r_c ||Delta||op <= D_C <= ||Delta||op.

Proof of the lower bound: for any unit u, c0+r_c u and c0-r_c u belong to C.
The difference of their gradient differences is 2r_c Delta^T u. Triangle
inequality implies that at least one has norm >=r_c||Delta^T u||. Optimize u.
The center need not be zero. Exact span alone supplies no positive uniform
r_c. A low-dimensional adjoint span of dimension r observes only the rP
quotient; its orthogonal-column differences are invisible as before.

## 3. One-step fixed-head quantitative observability

Let q=1/sqrt(n) times the all-ones vector, ||q||=1, with a fixed scalar linear
terminal head. Put a=Rh+Wv+b, G=diag(sech^2(a_i)). Divide the loss by the
constant beta=max(1,||R||_F) evaluated at the frozen model; beta is not
differentiated as a function of theta. The selected future inputs and loss
coefficients are also held constant when differentiating parameters. Then
the effective adjoint is

    c(v)=R^T G q / beta,
    D_v c=R^T diag(-2 q_i sech^2(a_i) tanh(a_i)) W / beta.

For a_i in [a0,a1], 0<a0<a1<infinity,

    sigma_min(D_v c) >= alpha
       = sigma_min(R) sigma_min(W)
         min_i |q_i| * 2 sech^2(a1) tanh(a0) / beta >0.

This bound is local and uniform on that preactivation box, not on all
possible inputs. In this audit a0=1/4, a1=3/4. Because W is invertible,
the corresponding compact future-input region is precisely

    v=W^{-1}(a-Rh-b), a in [1/4,3/4]^n.

Its inputs can be outside the archived past-input range. No claim is made
for an application that prohibits this region. Inside the box, gamma_i=
sech^2(a_i) independently covers an interval. Its half-width is

    m_gamma=(sech^2(1/4)-sech^2(3/4))/2.

The adjoint image contains a ball of radius

    r_c = sigma_min(R) min_i|q_i| m_gamma / beta.

Also ||c||<=||R||op/beta<=1. Thus the metric comparison in section 2 applies.
The positive radius can alternatively use a rational certified conservative
sigma_min(R) bound from ||R^{-1}||_F^{-1}, if a rigorous numerical constant
is needed. Tables here evaluate spectral constants at high precision without
calling them outward certificates; the analytic inequalities are rigorous.

Width dependence is explicit: min|q_i|=1/sqrt(n). Nearly singular R/W or
large beta worsen the constants. The tanh derivative tends exponentially to
zero under saturation; D_v c also vanishes at a_i=0. Accepted invertibility
does not give a width-uniform conditioning constant.

For L future transitions, c=A1^T ... AL^T q, where Aj=Gj R at the future
trajectory, and the terminal loss gradient replaces q for a nonlinear loss.
For ||R||op<=a<1 and unit terminal gradient, ||c||<=a^L. Hence a loss family
requiring at least L future steps has D_C<=a^L||Delta||op, even if its exact
span is full. At a fixed tolerance sufficiently small query magnitudes can
make all points in a bounded K indistinguishable. No hidden-state
controllability assumption substitutes for this adjoint calculation.

## 4. An explicit compact reachable patch

The accepted archived dense certificates provide a square Jacobian J0 of
F(X)=(h,S), a dyadic inverse preconditioner M, and an outward verified bound

    ||I-M J0||_infinity <= eta0 <1.

Choose the archived input center X0 and the infinity cube ||X-X0||<=1.
Let B=max|X0|+1, H=max(1,B), a=||R||_infinity, w=||W||_infinity. The following
scalar recursions are uniform derivative bounds, with all initial values zero.
For input directions u,v of infinity norm<=1 and a single parameter coordinate,
let A bound h_X, B2 bound h_XX, C bound h_theta, D bound h_thetaX, and E bound
h_thetaXX. At each step form

    v1=a A+w, v2=a B2,
    z=a C+H, z1=a D+A+1, z2=a E+B2;
    A_new=v1,
    B2_new=2 v1^2+v2,
    C_new=z,
    D_new=2 z v1+z1,
    E_new=4 z v1^2+2(z v2+2 z1 v1)+z2.

These follow by differentiating tanh's mixed derivatives using global
|tanh'|<=1, |tanh''|<=2, |tanh'''|<=4. The R-coordinate injection uses old h,
its first/second input derivatives A,B2; W injection uses input, derivative
<=1 and second derivative zero; b injection is constant. The maxima in z1
and z2 safely bound all three. No parameter is updated. The S rows require
third derivatives of h; they are included in E. Thus

    L=max(B2_T,E_T)

bounds D^2F in the infinity-norm bilinear operator norm on the cube. All a,w,
B,H,L are rational for the archived parameters/input bounds. Let m=||M||inf
and define exactly

    r=min(1,(1-eta0)/(2 m L)),
    kappa=eta0+m L r <=(1+eta0)/2<1,
    rho=(1-eta0) r/(2m), R_K=rho/2.

For ||Z-F(X0)||inf<=rho, the map

    T_Z(X)=X+M(Z-F(X))

is a contraction with Lipschitz constant<=kappa on the r cube. It maps that
cube into itself since kappa*r+m*rho<=r. Its unique fixed point has F(X)=Z:
M is invertible because MJ0 is invertible. The fixed point depends
continuously on Z, giving a local history section. In particular,

    K={S: ||S-S(X0)||_F <= R_K}, with h=h(X0) fixed,

lies entirely inside the reachable neighborhood. It is compact, bounded and
full dimension nP. Exact rational constants and their decimal sizes are
stored per witness. This is a deliberately conservative sufficient radius.
A tiny certified R_K does NOT prove that a larger or better-conditioned
reachable region does not exist. The analysis concerns continuous controls;
the finite grid used to choose X0 is not a restriction on future perturbations.

## 5. Conditioning of accessibility and its composition

Write J=[J_h;J_S] at a witness. Since J_h has full row rank, choose N with
orthonormal columns spanning ker J_h. Then

    A_fiber=J_S N

is the derivative of sensitivity along fixed-h history tangents. It removes
the n forward-state directions before counting sensitivity modes. The local
fixed-h manifold admits this tangent by the implicit-function theorem, but a
finite straight displacement N u does not in general keep h exactly fixed.
Our spectra count tangent axes, not global displacements or bits by themselves.

Let s_i be the singular values in the declared norms. Define

    d_eff(tau)=#{i:s_i>=tau}.

Report absolute tau and s_i/s_1 separately. Raw input norm is total-history
Euclidean norm, not per-token RMS; doubling horizon therefore does not grant
additional input energy in this norm. Secondary input units use the known
standard deviation sqrt(3/32). Parameter-group RMS relative coordinates are
theta=theta0+diag(p_RMS) phi, so S_phi=S_theta diag(p_RMS) and
g_phi=diag(p_RMS) g_theta. The error contract changes units accordingly.
This is not a way to improve a raw-coordinate theorem.

Column-normalizing S by its observed column sizes is a different convention:
it grants larger allowable parameter perturbations in weakly sensitive columns
and can conceal the failure under examination. It is not used in the primary
analysis. Fisher-like norms additionally require a specified output distribution
and positive-definite metric; a singular Fisher metric discards directions.
They can be scientifically appropriate for a task but redefine distinguishability
and are not evidence for a universal worst-case gradient claim. Orthonormal
changes of input/sensitivity coordinates preserve the singular values and norm;
general rescalings do not. A fixed scalar input standard deviation is declared
in advance and applied to BOTH architectures. No endpoint whitening is used.

For a finite local section s(u) on a p-dimensional input-coordinate ball,
suppose its base derivative has smallest singular value tau and its derivative
differs from the base by operator norm at most ell*rho_X<tau throughout a
convex rho_X ball. Project onto the base derivative's left singular subspace.
By integration along line segments and the triangle inequality,

    ||s(u)-s(v)||_F >= (tau-ell*rho_X)||u-v||_2.

Hence queries with adjoint-ball radius r_c distinguish them by at least

    D_C(s(u),s(v)) >= r_c (tau-ell*rho_X)/sqrt(n) * ||u-v||_2.

This is the two-stage conditioning product, including a nonlinear remainder.
At the tangent level the guaranteed per-axis scale is r_c*s_i/sqrt(n).
For input radius rho_X and error epsilon, a conservative threshold is
rho_X*r_c*s_i/sqrt(n)>epsilon, before remainders. Numerical singular values
alone do not certify any chosen finite rho_X. An ellipsoidal section gives
axis-dependent packing; an isotropic lower bound uses its smallest retained
axis. No theorem here upgrades a tangent count to a practical memory bound.

## 6. Deterministic finite-state packing bound

Let an encoder have Q discrete memory states and answer all allowed queries
within absolute epsilon. If two points have the same state, the decoder
returns the same answer for any fixed query. Therefore

    D_C(S1,S2)<=2 epsilon

is necessary for a collision. A set pairwise separated by >2epsilon in D_C
requires at least that many distinct memory states. If Q<=2^b, then

    b >= log2 packing(K,D_C, separation>2epsilon).

For the Frobenius R_K ball in dimension D=nP, take delta=4epsilon sqrt(n)/r_c
(r_c=1 for the primary unit-adjoint family). A maximal Euclidean delta-separated
set covers K by delta balls. Comparing volume gives at least (R_K/delta)^D
points when R_K>delta. Euclidean separations>=delta imply D_C>=4epsilon>2epsilon.
Thus, conservatively,

    b >= max(0, D log2(r_c R_K/(4epsilon sqrt(n)))).

Round the actual number of memory states/bits upward. The right-hand side is
a real lower bound; for a specific small packing, use its integer cardinality.
Packing is finite because K is compact and the query metric is continuous.
For unit adjoints, a Frobenius epsilon cover also gives query error<=epsilon.
The standard disjoint-ball volume argument gives a covering upper estimate
(1+2R_K/epsilon)^D; a codebook decoder can store its cell index. That is an
existence rate bound, not a cheap update algorithm. For restricted head queries
normalized by beta, the same upper bound applies since D_C<=||Delta||F.

This gives D log(1/epsilon) worst-case bits asymptotically as epsilon->0 for
each fixed n and fixed positive R_K,r_c, up to constants. It does NOT give
Theta(nP) bits at a single application tolerance uniformly over widths when
R_K or r_c shrinks. A large exact dimension may provide a vacuous bound.
One must not infer a GPU byte lower bound from this mathematical codebook model.

## 7. Real coordinates are different: conditional finite-error topology

For a CONTINUOUS encoding E:K->R^k, finite bits are not assumed. A useful
finite-error counterpart is Borsuk-Ulam, not the exact injectivity theorem.
If k<D, restrict E to the boundary S=S0+R_K u, ||u||F=1. Borsuk-Ulam on
the (D-1)-sphere yields E(S0+R_K u)=E(S0-R_K u) for some u (pad the target
with zeros if k<D-1). But their query distance is at least

    2 r_c R_K/sqrt(n).

They cannot both have error<=epsilon if epsilon<r_c R_K/sqrt(n). Therefore
under continuity and this scale assumption, k>=D. The decoder need not be
continuous for this collision argument. For an encoder on history, compose
with the continuous local history section from section 4.

At larger tolerances this argument no longer enforces D coordinates. Tiny
variation in discarded directions can fit entirely within the error budget.
Discontinuous finite codebooks violate continuity and are instead bounded in
BITS. Counting coordinates of unbounded-precision real numbers alone gives
no finite-state bound: one real can encode a discrete code index. A buffer of
k coordinates each limited to b0 bits has at most 2^(k b0) states, so packing
bounds k*b0. These are separate models, not interchangeable conclusions.

## 8. Strong conditioning failures permitted by the exact hypotheses

1. Future gate contraction: section 3 gives exponential attenuation a^L for
contractive R and delayed normalized terminal queries. Full exact span is
compatible with arbitrarily weak finite-margin separation.

2. Nearly independent dense recurrence: start with distinct nonzero diagonal
R0 and consider R(t)=R0+t C with generic dense C. For all sufficiently small
nonzero t outside isolated exceptional values, R(t), W are invertible and all
R(t) inverse entries nonzero. At t=0, all non-owner sensitivity entries vanish
for diagonal parameters, but in the DENSE parameterization off-diagonal R
parameters are also differentiated: their injections need not vanish. One
must NOT use the independent parameter-restricted dimension as a rank ceiling
for this dense t=0 model. The correct failure attack instead uses continuity
of any particular small coupling-dependent mode, or the delayed-loss bound,
not an unsupported assertion that all dense sensitivity modes vanish at t=0.

3. Scaling and parameterization: replace theta by lambda*phi. Gradient
queries in phi units are multiplied by lambda. An absolute epsilon contract
is not invariant to that reparameterization. Raw units or an externally
justified metric must be fixed before claims of robustness.

4. Numerical witnesses: full endpoint or fixed-h singular spectra can have
many tiny singular values even with an exact nonzero maximal minor. This
is evidence about those histories, not a universal upper bound on robust
dimension across all histories. Widths2/3/4 and their different minimal
horizons do not isolate width from horizon. No exponential-in-n theorem
is inferred from three witnesses.

5. Explicit strongest all-width scale counterexample: set R=delta*A, W=I,
where A=I-11^T/(n+1), delta>0. Every exact-theorem assumption holds for every
delta>0; every R/W/b entry is still differentiated independently, not only
delta. Since ||R||op=delta, all normalized terminal adjoints after at least
L steps have norm<=delta^L. On any bounded sensitivity patch with diameter
2R_K, D_C<=2R_K*delta^L. Choose delta small enough that this is<=2epsilon.
The full sensitivity family then cannot enforce a nontrivial packing lower
bound at that epsilon using only those delayed losses. A constant code with
representative S0 even attains error<=R_K*delta^L, accounting separately for
the common direct future injection. This is a rigorous counterexample to a
uniform fixed-error conclusion from the accepted qualitative assumptions.
It does not apply when immediate arbitrary unit hidden losses are allowed.

## 9. Independent recurrence comparison

For owner-local diagonal recurrence, parameters are diagonal R (n), dense W
(n^2) and b (n): P_ind=n^2+2n. State i depends only on its own parameter group.
Its supported sensitivities have exactly P_ind scalar coordinates; including
h gives P_ind+n. Restrict queries/norms identically. On an open supported
Frobenius patch the preceding metric, packing and Borsuk-Ulam arguments give
the same formulas with D=P_ind, not nP_ind. Owner queries distinguish the
nonzero rows. Compact exact traces therefore need only O(P_ind) entries.

The matched controls here use identical n, past X, T, W and b; diagonal R
uses the archived recipe. Parameters are fewer, so this is a structural
control, not a parameter-matched capability experiment. At each width compare
the SAME absolute thresholds, input norm and query normalization. It is not
automatic that dense recurrence has more robust modes merely because its
exact supported dimension is higher. No independent patch radius is borrowed
from the dense certificate.

## 10. Approximation escape routes

- Truncated SVD: a rank-r sensitivity approximation has worst unit-query
  error exactly ||S-S_r||op=sigma_(r+1)(S). Its storage is roughly r(n+P+1).
  This concerns a snapshot S spectrum, not the endpoint Jacobian spectrum.
  An efficient closed online update needs additional analysis; repeated
  compression errors can accumulate.
- A randomized sketch may approximate selected/independent queries with
  high probability. Pointwise, average or fixed-before-randomness guarantees
  are not the deterministic worst-case/all-late-queries contract. A realized
  sketch satisfying that contract on K still obeys packing. Uniform operator
  error or subspace assumptions must be supplied, not presumed from JL alone.
- UORO/KF-RTRL provide stochastic estimates (including unbiased versions),
  not deterministic uniform epsilon bounds. Variance and rare deviations are
  genuine scope changes. They can be useful without refuting our theorem.
- Truncated RTRL: if ||A_t||op<=a<1 and ||B_t||op<=B, omitting injections
  older than H steps produces a tail <=B*a^H/(1-a), hence bounded query error.
  This is a rigorous sufficient escape in contractive systems; H depends on
  epsilon. Saturation may shrink this tail while also reducing useful credit.
- Kronecker/shared-factor/local approximations exploit distributions or
  exact architecture restrictions; their error must be measured in the
  declared query norm. Dense support need not imply high metric entropy.
- Learned compression/sufficient statistics can achieve small error if K
  or the query family is low-dimensional at that tolerance. Performance
  on an average task distribution is not uniform worst-case correctness.
- BPTT/checkpointing/reversible recomputation retain/replay past information;
  total history-dependent state/tape and recomputation must be counted. They
  lie outside the discarded-history model, not outside mathematics.

## 11. Worst-case rate-distortion formulation

Define R_wc(epsilon)=ceil(log2 minimum number of deterministic memory states
supporting uniform query error<=epsilon on K). Each cell must have D_C diameter
<=2epsilon; an epsilon-net with representative answers suffices. Consequently

    log2 packing(K,D_C, >2epsilon) <= R_wc(epsilon)
      <= ceil(log2 covering(K,D_C, epsilon)).

The lower display may be rounded as appropriate for integer rates. Decoder
outputs need not be sensitivities; the cell-diameter argument still applies.
This is deterministic metric entropy, a worst-case rate-distortion-style
problem. Shannon rate-distortion needs a source probability law and expected
distortion; neither is authorized by the current experiment.

## 12. Architecture relevance and remaining obligation

A width-uniform patch radius and query margin at fixed meaningful epsilon,
with many accessible axes, would establish a material memory/credit target.
Superlinear robust dimension could still matter. If robust dimension stays
O(P), the exact cubic endpoint count may be practically weak. A controllable
interaction-versus-credit-memory frontier is a design target, not a discovered
architecture. We establish none of these across arbitrary widths here.

The rigorous outcome is conditional finite-bit and continuous finite-error
bounds, plus an explicit demonstration that the qualitative hypotheses alone
cannot provide fixed-error robustness uniformly over allowed models/losses.
Archived spectra are empirical conditioning diagnostics. They neither prove
global robust collapse nor identify a learning advantage. Independent review
and a justified perturbation/loss/error scale remain necessary before any
architecture or learning work.

## References used for scope, not as substitutes for the derivations

- Karol Borsuk (1933), original antipodal theorem, Fundamenta Mathematicae20,
  177-190, DOI10.4064/fm-20-1-177-190. Publisher record:
  https://www.impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/20/0/93008/drei-satze-uber-die-n-dimensionale-euklidische-sphare
- Roman Vershynin, High-Dimensional Probability, section on nets, covering
  and packing numbers. Author's draft:
  https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-1.pdf
  Web PDF fetch failed; the volume arguments needed here are given in full.
- Tallec and Ollivier, UORO, https://arxiv.org/abs/1702.05043
- Halko, Martinsson and Tropp, randomized matrix approximation,
  https://arxiv.org/abs/0909.4061
- Mujika, Meier and Steger, KF-RTRL, https://arxiv.org/abs/1805.10842
- Menick et al., SnAp, https://arxiv.org/abs/2006.07232
- Shalev-Merin (2026 preprint), empirical sparse gradient transport,
  https://arxiv.org/html/2603.15195v1 . Its task-adaptation evidence is a
  relevant warning against assuming exact credit storage is practically
  necessary; it does not assert our uniform frozen-parameter gradient contract.
