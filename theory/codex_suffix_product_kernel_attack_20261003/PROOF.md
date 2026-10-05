# Finite-radius width barrier for the moving-corridor suffix-product channel

Codex,2026-10-03. NEW theory, internally audited; independent hostile review
required. The accepted corridor construction is a premise, not re-reviewed.
Epsilon=.001, fixed feature, original normalized legal future queries.

## 1. Exact scope and main theorem

Use the accepted frozen model and corridor constants in
theory/codex_holding_cost_attack_20261003/PROOF.md, sections1,4,5.
In particular n>=10^6, m,T positive integers,

    S=m+T+4<=floor(n/4)/100, a=1-1/n,
    .99<g_(i,t)<1, sigma=tanh(sigma/(100n)+.05),
    A=2S, paired-site offset3S, L=m+T-1.

Rows i=1,...,m have physical columns z=A+i+j, j=1,...,T:

    K_(i,A+i+j)=a^(T-j) product_(s=j)^T g_(i,s),
    K_(i,z)=0 outside that row's support.                         (1)

All other reference sensitivity coordinates ON THIS PAIRED PARAMETER FRAME
are public. Common-endpoint histories have the same public bath/reset and
future direct-injection terms. The accepted true-model comparison has
antipodal HALF-error<4e-9. We conservatively charge pair error delta_d=8e-9.

Let

    H(B)=max_(||xi||infinity<=1)||B^T xi||2,
    P=mT, s=min(m,T), B_size=sqrt(Ps), C_Q=8.

The accepted one-step query distance is exactly alpha_n H(Delta K), with
alpha_n=sigma a^2 g_reset s_gate sqrt(2l/n)/n>=1/(200n).
The ALL-future projected query upper, including reference reset,
can be written with the explicitly checked constant below as

    d_pair(X,X')<= C_Q H(K(X)-K(X'))/n +delta_d.                 (2)

d_pair is the supremum over the ACTUAL permitted future queries, with only
the gradient projection onto this paired parameter frame retained. Future
preactivations lie in[.25,.75], head1_n/sqrt(n), group factor1/n.
It is NOT arbitrary unit adjoints, RMS visibility, or the full fixed-feature
gradient norm on other parameter directions. Equation(2) has precisely the
upper scope in the accepted predecessor. Its finite C_Q is essential.

For clarity we verify the constant, a necessary dependency of the new bound.
Let q_f=sech^2(.25)<.941. For an ordinary cycle column before wrapping,
||Oe_i-e_(i+1)||2<=6/sqrt(n), as already established. A backward legal
adjoint c_L has norm<=q_f^L. Unrolling the ordinary column gives

    |c_(L,i)|<=q_f^L(1+6L)/sqrt(n).

All final paired rows, after reset, are at least n/8 forward steps from the
exceptional column. Until then, the last inequality applies. Afterwards
||c_L||2<=q_f^L<=1/sqrt(n), since n>=10^6. Moreover
sup_(L>=0)q_f^L(1+6L)<100 (use L exp(-.06L)<=1/(.06e)).
Thus each paired adjoint coordinate is at most100sqrt(2)/sqrt(n) in
absolute value. Reference past difference after reset is
sigma sqrt(l) a g_reset times Delta K on these paired rows. Normalization
1/n gives upper coefficient

    100sqrt(2) sigma sqrt(l/n) a g_reset /n <8/n,

since sigma<.051 and l<=n. This holds for EVERY permitted future horizon
and every admitted future gate word, not a sampled frame of queries.
For zero future steps, the uniform head annihilates paired rows directly.

For the dense replacement, identical prescribed past states give past
sensitivity error<=e sigma sqrt(l)n^2. The legal normalized error is at
most e sigma sqrt(l)n. Replacing future adjoints costs at most
e L q_f^L sigma sqrt(l), using past operator norm<=sigma sqrt(l)n.
Both are far below4e-9 for n>=10^6 and e<=4/(10^8 n^2).
Taking two histories gives the conservative delta_d=8e-9 in(2). Public
future direct injections cancel at their common endpoint. No multiplicative
equivalence near a zero signal is claimed.

THEOREM1 (finite-radius corridor-channel barrier). For each fixed PUBLIC
n,m,T and corridor placement satisfying the conditions above, define

    p=max(1,ceil(2 C_Q B_size/(n epsilon))),
    k_quant=m(p-1), epsilon=.001.                              (3)

There is a continuous static encoding of the entire reachable kernel family
into k_quant real coordinates such that equal codes imply

    d_pair(X,X')<=epsilon+delta_d<2epsilon.                     (4)

Consequently any ONE continuous section of a D-dimensional closed ball
whose EVERY boundary antipodal pair has d_pair>2epsilon satisfies

    D<=min(mT,k_quant)
      < (2 C_Q/epsilon) m sqrt(mT min(m,T))/n
      <= (2 C_Q/epsilon) mT/sqrt(n)
      = 16000 P/sqrt(n).                                     (5)

This is a finite-radius statement: no linearization, tangent rank, packing,
or separate-axis inference. In particular

    P=o(n^(3/2)) implies D=o(n),
    D=omega(n) requires P=omega(n^(3/2)).                      (6)

Thus the requested superlinear section at mT=o(n^(3/2)) cannot exist in
THIS projected suffix-product channel. It does not rule out information in
unpaired/other sensitivity channels of the same histories or other histories.

## 2. Product geometry and exact inverse

Write row entries as k_(i,j), suppressing their physical column shift. Since
0<a g_(i,j)<1,

    0<k_(i,1)<...<k_(i,T)<1,
    k_(i,j)=a g_(i,j) k_(i,j+1) for j<T,
    g_(i,T)=k_(i,T),
    g_(i,j)=k_(i,j)/(a k_(i,j+1)) for j<T.                    (7)

Hence the product map is one-to-one. The image is NOT the full monotone row
ball: the ratios must be in the admitted gate range. We use a SUPERSET of
the image only for an upper approximation, never as a reachable lower.

For baseline g0 and z_(i,s)=log(g_(i,s)/g0),

    log(k_(i,j)/k0_j)=sum_(s=j)^T z_(i,s),
    k0_j=a^(T-j)g0^(T-j+1).                                  (8)

The difference of adjacent log-suffix coordinates recovers z exactly.
The Jacobian in gate coordinates has entries k_(i,j)/g_(i,s) when s>=j,
and0 otherwise. Its determinant is

    a^(T(T-1)/2) product_(s=2)^T g_(i,s)^(s-1)>0.             (9)

Rows vary independently in the reference gate prescription; their physical
column supports overlap. No query treats those overlapping entries as
independently selectable parameter columns.

Let C_T have entries1_(s>=j). Its exact singular values are

    sigma_l(C_T)=1/[2sin((2l-1)pi/(4T+2))], 1<=l<=T.         (10)

Indeed C_T^-1 is the upper bidiagonal first-difference matrix. Its transpose
times itself is tridiagonal with first diagonal1, other diagonals2, and
offdiagonals-1. Solving that recurrence with the two endpoint conditions
gives eigenvalues4sin^2((2l-1)pi/(4T+2)). These Euclidean values DESCRIBE
the triangular geometry; they are not robust dimension counts.

For all gates in[g_-,g_+] subset(0,1), k_min=g_-(a g_-)^(T-1) bounds the
exponential derivative below. Pointwise mean value gives finite-pair
Euclidean control by k_min C_T, but k_min may decay exponentially. Even
good cumulative-sum conditioning does not remove the legal1/n query scale.
Strict monotonicity and bounded range, rather than the smallest singular
value, will supply the stronger uniform finite-radius upper.

## 3. Direct legal-query norm and staggered supports

For any real matrix E with the same staggered row supports,

    ||E||F <= H(E) <=sqrt(s)||E||F.                          (11)

Lower: choose independent uniform signs xi_i. Then
E||E^Txi||2^2=||E||F^2, so at least one allowed sign witness attains it.
Upper: every column meets at most s=min(m,T) rows. Cauchy at EACH column
gives |sum_i xi_i E_(i,z)|^2<=s sum_i E_(i,z)^2. Sum over columns.
This explicitly bounds the worst permitted sign supremum; it does not
replace that supremum by RMS. The support factor is stronger than a generic
sqrt(m) Frobenius upper when T<m.

Equivalently, exact norm duality gives

    H(E)=max_(||v||2<=1) sum_i |sum_z E_(i,z)v_z|.            (12)

Both xi and the unit parameter test v can adapt to the antipodal pair under
the SAME future query for its two members. Our upper holds for all of them.

If every supported entry is approximated to error<=h, then

    H(E)<=h sqrt(mT min(m,T))=h B_size.                     (13)

No assumption about independence/cancellation of entries is used.

## 4. A continuous nonharmonic quantile code

For each row k_1<...<k_T, form the continuous piecewise-linear strictly
increasing function f:[0,T+1]->[0,1] through

    (0,0),(1,k_1),...,(T,k_T),(T+1,1).

For ell=1,...,p-1, store the UNIQUE position

    tau_ell=f^-1(ell/p).                                    (14)

Endpoints tau_0=0,tau_p=T+1 are public, not stored. Positions tau_ell are
strictly increasing; this is m(p-1) persistent SNAPSHOT coordinates.

Continuity of the encoder: at every admitted row, all linear slopes are
positive. The unique inverse position moves continuously when row values
vary, including when a target crosses a knot. For a sequence of rows
converging to an admitted row, their f converge uniformly; any subsequential
limit of the inverse positions solves the same strict inverse equation,
whose solution is unique. Compactness of[0,T+1] gives convergence. Compose
with the continuous product map and any continuous section. No uniform
condition number across widths or finite-precision claim is needed.

Decode using the piecewise-linear f_hat through

    (tau_ell,ell/p), ell=0,...,p,

and set k_hat_j=f_hat(j). Between adjacent tau knots, BOTH f and f_hat lie
in the SAME level interval[ell/p,(ell+1)/p]. Therefore, over the ENTIRE row,

    |f(t)-f_hat(t)|<=1/p,
    |k_j-k_hat_j|<=1/p.                                    (15)

For p=1, store nothing and use f_hat(t)=t/(T+1); the same bound holds.
Outside each physical row support keep exactly zero. All constants are
uniform over the complete admitted gate range and finite radius. Nonlinear
exponentiation is already included in f, with no Taylor remainder to pay.

Equations(13),(15) give

    H(K-K_hat)<=B_size/p.                                   (16)

If two kernels have the same code, the SAME K_hat decodes both, whence
H(K-K')<=2 B_size/p. From(2),(3), this proves(4), including the dense pair
ledger. Residual public reference coordinates cancel, as do common-endpoint
direct future injections. No invisible residual is assumed for another
parameter frame.

The code is STATIC: it does not provide an O(k_quant) causal update from
these inverse positions alone. Repeated interpolation after a gate update
would require a separate horizon-uniform error analysis. We make NO
low-dimensional online-encoder theorem from this representation.

## 5. Topological finite-error dimension step

Suppose Phi:B^D->admitted common-endpoint histories is continuous and every
antipodal pair Phi(y),Phi(-y), ||y||2=1, has d_pair>2epsilon. Compose Phi
with the quantile encoder, giving a continuous map B^D->R^k_quant.

If D>k_quant, restrict to S^(D-1). Borsuk-Ulam supplies y,-y with equal
codes: pad the target with zeros to R^(D-1) if necessary. Equation(4) gives
d_pair(Phi(y),Phi(-y))<=epsilon+8e-9<.002, a contradiction.
Therefore D<=k_quant. Also the exact gate word is a continuous encoding
in mT coordinates and determines this prescribed history; the same argument
gives D<=mT. This is an upper by continuous encoding, not a raw-rank lower.
No injectivity assumption on the section is needed for these upper bounds.
It also bounds the Borsuk-Ulam robust width of the entire reachable set.

Since p=max(1,ceil(Q)), Q=2 C_Q B_size/(n epsilon)>0, always p-1<Q,
including Q an integer and p=1. Thus

    k_quant < (2 C_Q/epsilon) m sqrt(Ps)/n.

Because s<=T and m<=n,

    m sqrt(Ps)/n <=m sqrt(mT^2)/n
                  =P sqrt(m)/n <=P/sqrt(n).                (17)

This proves all inequalities(5),(6). The exact integer dimension bound(3)
is often smaller than its asymptotic simplification.

## 6. Haar, signed blocks, ramps, and the exponent region

For a unit Euclidean Haar vector on a temporal interval b=2h (h entries
positive, h negative), its cumulative suffix vector has EXACT squared norm

    ||C_T psi||2^2=(b^2+2)/12.                              (18)

This follows by summing two triangular sequences:
[sum_(v=1)^h v^2+sum_(v=1)^(h-1)v^2]/(2h).
Coarse intervals gain O(b); fine intervals do not. After exponentiation,
all resulting reachable rows still satisfy(7), so the finite-radius quantile
upper applies to ANY joint Haar/dyadic, Walsh, step, ramp, saturated or
nonlinear code. Separate-axis gains and cumulative singular values cannot
overrule(5). This is stronger than rejecting just one Haar amplitude rule.

Let m=n^mu,T=n^tau, effective per-row section count r=n^rho, D~mr.
Physical corridor budgets require mu,tau<=1 (and small coefficients at a
boundary). Log injectivity permits r<=T, but finite-error theorem requires

    mu+rho <= [3mu+tau+min(mu,tau)]/2-1,                    (19)

in any proposed power-law robust family, with fixed epsilon/C_Q. Ceiling
effects are included by the exact bound and do not add a hidden m term.
If tau<=mu, (19) is rho<=mu/2+tau-1, and robust superlinearity forces

    mu+tau >2-mu/2 >=3/2.

If mu<=tau, (19) is rho<=mu+tau/2-1. Superlinearity requires
2mu+tau/2>2; under mu+tau<3/2 and mu<=tau, its left side is <15/8<2.
Therefore the requested exponent feasibility region is EMPTY for this
channel. The simpler(17) also proves this for non-power slowly diverging D/n.

This does not assert the upper count is achievable; no new robust lower
section is constructed in this stage.

## 7. Physical energy and endpoint bookkeeping

All new admitted gate words still obey the accepted corridor lift:

    beta_(i,t)=sqrt(1-g_(i,t)) in(0,.1),
    two cycle copies +beta, two off-cycle compensators -beta,
    public preparation beta_(i,0), source at sigma.

Every combination has exact zero private selected sum, an autonomous
public bath, and the public simultaneous reset. Endpoint independence is
automatic for all the nonharmonic codes considered here. The complete
actual raw-input norm remains bounded ABOVE by

    ||X||2<=2sqrt(m(T+2)+1).                                (20)

All dense corrections are counted; there is no discarded public baseline.
No modified head, future-query cube, input cube, endpoint contract or model.

IMPORTANT: (20) is an UPPER. A lower on mT alone does NOT establish a lower
on the actual input norm of every corridor history. Only in the accepted
near-zero schedules with beta_max->0,T=o(n), whose actual holding cost is
Theta(mT), does(6) imply R_abs=omega(n^(3/4)) for D=omega(n).
For more autonomous, nearly zero-cost active gate schedules a separate
input-energy/visible-width relation would be needed. Do not promote the
coordinate-time barrier to a general energy theorem.

Likewise this static approximation does not bound arbitrary causal memory
for every history or the full fixed-feature gradient. Different private
parameter channels can remain observable outside this paired frame.

## 8. Conclusions and the next exact question

The desired product-kernel section with D=omega(n) and mT=o(n^(3/2)) is
REFUTED, in its explicitly stated legal projected-channel metric. The
quantile argument is global finite-radius and includes every admitted
nonharmonic code. It does not reopen the accepted harmonic lower or turn a
method failure into a universal RNN claim.

Best constructive exponent for full fixed-feature d_F remains3/4, with
accepted Omega(n log n) at O(n^(3/4)(log n)^(3/2)). General necessary edge
remains1/4; threshold bracket[1/4,3/4] and full-model n^2--n^2 log n gap
are unchanged. No bits/VRAM/practical-width/training/architecture inference.

Following independent review, the specific next attack is to characterize
query-visible PRIVATE sensitivity outside the paired parameter frame of
these same low-cost corridors. That is not included in this task and is
not silently assigned the product-kernel upper.
