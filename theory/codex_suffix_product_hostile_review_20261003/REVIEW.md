# Independent hostile review: paired suffix-product obstruction

2026-10-03. **VERDICT: VERIFIED.** The scoped obstruction survives.

Target: `theory/codex_suffix_product_kernel_attack_20261003/` at source
commit `968341f6102c3b0b452d9e1945ecad50a67f7988`. This is a new derivation
and separately implemented attack suite. It does not designate the result
owner-accepted, change its constants, or modify the original evidence.
The accepted predecessor supplies the corridor lift. Its relevant query,
support, residual and dense-comparison dependencies are audited below.

## 1. Exact strongest theorem justified

Fix PUBLIC integers n>=10^6, m,T>=1 and S=m+T+4 satisfying
S<=floor(n/4)/100, along with the accepted paired placement, preparation,
source, bath and reset. Gates are .99<g_(i,j)<1. Retain only the gradient
projection onto the specified orthonormal paired recurrent-parameter frame
for the fixed source feature. Let d_pair be the supremum of the normalized
l2 distance of these projected gradients over all permitted future queries.

Set P=mT, s=min(m,T), B=sqrt(Ps), and

    p=max(1,ceil(16000 B/n)), k=m(p-1).

Any continuous Phi:B^D -> this admitted common-endpoint history family,
with d_pair(Phi(y),Phi(-y))>.002 for every ||y||2=1, satisfies

    D <= min(mT,k) < 16000 mT/sqrt(n).

The theorem is about robust antipodal section dimension in this projected
channel. It is not an upper bound on arbitrary causal encoder state, full
fixed-feature gradients, all histories, unpaired channels, or RNN energy.
No raw rank or finite packing is used as a dimension lower bound.

## 2. Quantile continuity: the strongest direct attack

For one row, k_j=a^(T-j) product_(s=j)^T g_s, a=1-1/n. Therefore

    k_j=a g_j k_(j+1), 0<k_1<...<k_T<1.

The inequalities are STRICT on the admitted family. After adding the public
anchors (0,0),(T+1,1), every segment of the piecewise-linear interpolant f
has strictly positive slope. A stored crossing f^-1(ell/p) is unique.

Here is a genuine failure of a broader claim: rows (.5-2h,.5-h) and
(.5+h,.5+2h), h->0+, approach the same flat row (.5,.5). Their .5 crossing
positions approach 2 and 1 respectively. No choice of generalized inverse
at the limiting plateau makes both paths continuous. Thus the proof MUST
NOT be extended to arbitrary nondecreasing rows with quantile plateaus.

This counterexample does not enter the legal product family: flat adjacent
entries require a g_j=1, impossible because a<1 and g_j<1. A last flat
anchor requires g_T=1, also excluded. Nearly flat rows do not defeat ordinary
continuity at any legal row. If rows converge to a legal row, f converges
uniformly; a convergent subsequence of crossings solves the same inverse
equation. Strictness makes its solution unique. Compactness of [0,T+1]
then gives convergence of the whole sequence. This also handles a crossing
exactly at a knot. The argument needs neither a uniform inverse condition
number in n nor a finite-precision representation.

Independent 256/384-bit tests included legal slopes near 10^-30 and an exact
.5 crossing at node 61 of a T=200 row. Both-sided perturbations were
continuous. The flat extension failed as predicted, outside the theorem.

## 3. Uniform reconstruction and private coordinate count

Store only tau_ell=f^-1(ell/p), ell=1,...,p-1. The decoder has knots
(tau_ell,ell/p), including PUBLIC tau_0=0,tau_p=T+1. On each closed interval
[tau_ell,tau_(ell+1)], both f and its decoded straight line stay between
ell/p and (ell+1)/p. Thus, for EVERY time position, including endpoints,

    |f-f_hat| <= 1/p.

This proves a uniform entry bound over the complete legal family, rather
than an approximation at selected samples. Two equal codes decode to one
common row, so their supported entry difference is <=2/p.

There are exactly m(p-1) history-dependent real numbers. The level values,
two anchors, row identities, physical support, row order, n,m,T and p are
fixed public data. Ordering requires no extra bits or coordinates: crossings
are strictly ordered. No tie-breaking or interpolating slope is stored.
For p=1 the code is empty; use f_hat(t)=t/(T+1). The same entry bound <=1
remains true. History-dependent placements or horizons would not be public
under this theorem; they are not being varied here.

## 4. Staggered support: independently derived, with a sharp adversary

Shift away the fixed A. Row i occupies columns i+1,...,i+T. Any column
intersects at most s=min(m,T) rows. For |xi_i|<=1,

    |sum_i E_(i,z) xi_i|^2
        <= (# supported rows in z) sum_i E_(i,z)^2
        <= s sum_i E_(i,z)^2.

Summing columns and taking the supremum gives

    H(E):=sup_(||xi||infinity<=1)||E^T xi||2 <=sqrt(s)||E||F.

This directly bounds the WORST sign query. It does not substitute an RMS
metric. An adversary with ones in a single maximally overlapping column
attains equality: H=s, ||E||F=sqrt(s). The support factor cannot be deleted
without extra restrictions, but no extra sqrt(m), sqrt(T) or overlap factor
is missing. For an entry bound h, there are at most mT nonzeros and hence

    H(E) <= h sqrt(mT s).

As a separate check, Rademacher signs have expected squared output ||E||F^2,
so ||E||F<=H(E). This lower observation is not used as a replacement norm.

## 5. ALL-legal-future coefficient: explicit dependency audit

The existing contract in
`theory/codex_autonomous_absolute_energy_20261003/PROOF.md`, section 1,
requires EACH future preactivation, at every step, to be in [.25,.75]^n.
The final head is 1_n/sqrt(n). The loss and recurrent group multipliers
cancel to the public factor 1/n, held constant in differentiation.
Thus every future gate has norm <=q=sech^2(.25)<exp(-.06), not just the last
gate. This uniform contraction is essential to the upper bound.

Raw future inputs can realize any such word from the common endpoint by
x=v-Rh-b. They are not subject to the PAST input cube. Their values are
then held fixed for parameter differentiation. Since the two histories
have the same actual endpoint and model, their future trajectories and
future direct sensitivity injections agree and cancel.

In the reference memory block, O=UPU, with
w=e_0-1_k/sqrt(k), gamma=1/(1-1/sqrt(k)), U=I-gamma ww^T. Direct expansion
on an ordinary nonwrapping cycle column yields

    ||O e_i-e_(i+1)||2 <=6/sqrt(n).

The paired rows after reset are at least d-7S-3>=n/8 forward steps from the
exception. To see why arbitrary future gates do not break the bound, set
A_j=G_j aO. For an ordinary column,

    A_j e_i = a g_(j,i+1) e_(i+1) + r_j,
    ||r_j||2 <=6q/sqrt(n), ||A_j||op<=q.

Repeatedly unroll the main path. The uniform head reads its final unit
column with magnitude 1/sqrt(n); the L error terms each cost at most
6q^L/sqrt(n). Consequently every gate word, before wrapping, obeys

    |c_(L,i)| <=q^L(1+6L)/sqrt(n).

After the n/8 travel threshold, the full norm bound ||c_L||2<=q^L already
suffices: q^(n/8)<=1/sqrt(n) for n>=10^6. Also

    sup_L q^L(1+6L) <=1+6/(.06 e) <37.788<100.

Thus each paired coordinate (c_i-c_(i+3S))/sqrt(2) has magnitude at most
100sqrt(2)/sqrt(n), uniformly in horizon and gate word. There is no
one-step-only assumption. At zero future steps the uniform head reads a
paired vector as zero.

The reference past private sensitivity after reset is
sigma sqrt(l) a g_reset times the paired embedding of Delta K. Here
sigma=tanh(sigma/(100n)+.05)<.051, l<=n, and a,g_reset<=1. Therefore

    d_reference <= [100sqrt(2) sigma sqrt(l/n) a g_reset/n] H(Delta K)
                < [7.212490/n] H(Delta K)
                < [8/n] H(Delta K).

Endpoint public terms cannot increase this difference. Our independent
Householder-cycle implementation tested high gates and two non-scalar
greedy query words at horizons 1,2,8,16,32,64 at n=10^6. These are attacks
on the envelope, not a numerical proof of the supremum.

## 6. Dense pair error: no uncharged m or T

Let e_R=||R-R0||op<=4/(10^8 n^2). Prescribed past states and hence gates are
identical under the two models, with their actual correcting inputs counted
in the accepted lift. On the selected unit-feature parameter action, the
forcing operator norm is sigma sqrt(l). Reference past norm is at most
sigma sqrt(l)/(1-a)=sigma sqrt(l)n, independently of history length.

The difference recurrence, with the same past forcing and gates, therefore
has norm <=e_R sigma sqrt(l)n^2. The normalized legal output error is at
most e_R sigma sqrt(l)n. The future Jacobian product comparison uses the
SAME actual admitted gate word on both matrices; its adjoint error is at
most L e_R q^L. Multiplying by the past norm and dividing by n costs at most
e_R L q^L sigma sqrt(l).

Hence one-history reference error is uniformly bounded by

    e_R sigma sqrt(l) [n+1/(.06 e)].

For n>=10^6 this decreases with n and is <2.041e-12, far below 4e-9. No
extra row/time factor is needed: the operator estimate already controls
all selected columns and summed chronological injections. At n=10^6 the
independent high-precision calculation with the actual sigma gives past
bound 1.99833501825e-12 and future bound 1.22524394965e-17.

Twice the per-history bound permits the conservatively stated pair ledger
8e-9. Direct future injections cancel within the actual common-endpoint
pair before making this comparison. One need not incorrectly claim that
the same raw future inputs produce identical gates in R and R0: the
comparison of linear transports is made using the same realized gate word.

## 7. Exact p arithmetic, including p=1

Write Q=16000 B/n>0. The chosen p=max(1,ceil(Q)) satisfies p>=Q and
p-1<Q, including integral Q and Q<=1. Equal codes give

    H(Delta K) <=2B/p,
    d_pair <=16B/(np)+8e-9 <=.001+8e-9 <.002.

At p=1 the inequality follows from B<=n/16000; no hidden positive
coordinate count is added. The decoded row need not be a reachable row.
It is only a common numerical reference for comparing two reachable rows.

## 8. Topology and both rectangular cases

Compose the continuous history section Phi:B^D with its continuous
k=m(p-1) coordinate code. If D>k, restrict to S^(D-1) and pad the codomain
to R^(D-1). Borsuk-Ulam gives y,-y with equal codes. Their distance is
<=.001000008<.002, contradicting even a non-strict >=.002 robust requirement.
Thus D<=k. The full gate word is also a continuous mT-coordinate code
determining this prescribed history, giving D<=mT separately. No section
injectivity assumption is needed for the upper contradiction.

Since p-1<Q,

    k <16000 m sqrt(mT min(m,T))/n.

If m<=T, the right side is 16000 m^2 sqrt(T)/n. Its ratio to
16000 mT/sqrt(n) is m/sqrt(Tn)<=1, since m<=T and m<=n.
If T<m, it is 16000 mT sqrt(m)/n<=16000 mT/sqrt(n), since m<=n.
Equivalently, min(m,T)<=T gives m sqrt(mT min(m,T))<=mT sqrt(m).
The strict first inequality is retained in either case. Therefore

    D <16000 mT/sqrt(n).

This is not an exponent guess or a ceil approximation. For p=1 the argument
gives D<=0 directly, so no positive-dimensional robust section exists.

## 9. Static versus causal, and complete channel scope

The static crossing coordinates are NOT an online update rule. Knowing a
row's inverse levels need not determine its new inverse levels under fresh
nonuniform gates. No streaming algorithm or causal state upper is proved.

This does not invalidate their use in Borsuk-Ulam: a putative robust terminal
section can be composed with ANY continuous low-dimensional test map. The
equal-code comparison rules out that geometric section irrespective of
whether the test map is implementable online. The accepted robust-section
definition has exactly that endpoint antipodal requirement. If a different
definition asks for the minimum causal state of all prefixes, the present
argument is not an upper bound for it.

On the reference paired parameter frame, the accepted moving support
preserves pairing, U acts identically on a paired vector, O shifts it, and
other reference private components do not arise. The actual dense residual
is separately bounded above. This is sufficient for the PROJECTION.
Unpaired directions and their bath/compensator sensitivities can be private
in these very histories. They are outside the theorem. Thus closure of the
paired route must not be presented as closure of the complete corridor or
the full fixed-feature target.

## 10. Energy audit and exponent-region audit

The accepted ||X||<=2sqrt(m(T+2)+1) is an UPPER. It cannot be reversed.
The new theorem implies

    D/n <=16000 mT/n^(3/2),
    D/n ->infinity => mT/n^(3/2) ->infinity.

Only an independently established actual cost ||X||^2>=c mT transfers this
to ||X||=omega(n^(3/4)). The predecessor proves such a lower in its scoped
near-zero schedules (beta_max->0,T=o(n)); not for arbitrary gates. The
target proof and report explicitly keep this distinction. No invalid energy
lower was found in the audited text.

For power laws m~n^mu,T~n^tau,r~n^rho,D~mr, the sharper count gives the
necessary exponent inequality

    mu+rho <=(3mu+tau+min(mu,tau))/2 -1.

If tau<=mu, this gives rho<=mu/2+tau-1. Superlinearity requires
mu+tau>2-mu/2>=3/2 because mu<=1.
If mu<=tau, it gives rho<=mu+tau/2-1. Superlinearity requires
2mu+tau/2>2. Under mu+tau<3/2 and mu<=tau, mu<3/4 and
2mu+tau/2=(3/2)mu+(mu+tau)/2<15/8<2. The claimed excluded region has no
feasible point. The non-power-law inequality above is stronger in scope.

## 11. Nonharmonic codes and exact product geometry

Haar, Walsh, ramps, signed blocks and saturation are covered only when
they prescribe legal gates in THIS fixed paired suffix-product family.
The quantile argument does not care about their basis or amplitude rule.
It does not cover another nonharmonic channel whose rows cease to have the
specified support and monotonicity.

With z_s=log(g_s/g0), log(k_j/k_j^0)=sum_(s>=j) z_s. Adjacent differences
invert it. The gate Jacobian is upper triangular with entries k_j/g_s for
s>=j; its determinant equals

    a^(T(T-1)/2) product_(s=2)^T g_s^(s-1)>0.

There is no conflict between injectivity and a small finite-error code.
The code is intentionally many-to-one and never purports to recover all
gate values exactly. If gates are bounded below by g_-<1, the exponential
derivative on the oldest suffix can be as small as g_-(a g_-)^(T-1). Even
without such decay, the legal query factor 1/n and the bounded monotone
range make exact rank irrelevant to a fixed-margin dimension certificate.

The cumulative first-difference formula and the Haar squared gain
(b^2+2)/12 are consistent; neither supplies a robust lower on its own.

## 12. Direct counterexample search and supporting artifact audit

The new scripts import no original machinery. Fifty-two first-pass records
and six stronger non-infinitesimal collision records passed. Equal-code
attacks covered p=1,p=3,p=9, both rectangular regimes, square supports,
exact knot crossings, near-flat legal rows, same-sign aligned errors and
sharp maximum-overlap columns.

The largest entrywise collision was .944335... at m=1,T=2400,p=1. Despite
being far from infinitesimal, its controlled all-future query distance was
<=.000335001. The strongest controlled distance in these attacks was
.000415524564 at m=2,T=900. Reordering three low gates from the start to
the end of T=64 rows, m=64,p=9, preserves the whole code exactly while
changing entries by .0291069; its controlled distance was <=.000093578518.
No attack produced >.002. These are upper-controlled numerical examples;
they are not claims to have solved each query supremum numerically.

All original supporting files were read, including the complete test script,
204 check records, source hashes and final audit. The original checks all
report PASS; their script hash matches their metadata. Their finite tests
are not an independent proof and did not regenerate adversarial multi-step
query transport. The new vector implementation supplies that additional
diagnostic, while the written derivation supplies the uniform bound.

Original proof/review/log bytes are frozen in FROZEN_INPUTS.json and checked
again at the end. The original folder is untouched.

## 13. Final verdict and next attack

**VERIFIED.** No load-bearing inequality failed within the stated domain.
The plateau counterexample fails the LEGALITY hypothesis, not the theorem.

The paired projected suffix-product route is closed for a joint robust
antipodal section with D=omega(n),mT=o(n^(3/2)). Full causal complexity,
unpaired sensitivity and a universal energy barrier remain open.

Recommended next attack: independently characterize the unpaired/private
credit left by the same low-energy histories, beginning with its exact
coupled injections and all-legal-query norm. Do not apply this monotone-row
code to those components without a separate derivation. No new research is
started by this review.
