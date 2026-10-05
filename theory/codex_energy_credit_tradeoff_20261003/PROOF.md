# Absolute energy versus query-visible credit: new stage

Codex, 2026-10-03. NEW author-derived results, requiring independent hostile
review. The owner-accepted absolute-energy upper and all historical lower
proofs are premises. None is reopened or edited. No architecture claim.

## 1. Contract and notation

Use the frozen family in the accepted autonomous-energy proof:

    k=floor(n/2), l=n-k, d=floor(n/4), r=k-1,
    a=1-1/n, lambda=1/(100n), b0=1/20,
    R0=diag(a O,lambda I_l), O=U(P_d direct_sum I)U,
    ||R||op=a, e=||R-R0||op<=4/(10^8 n^2), W=I.

Start at zero; every raw past input coordinate must be in (-1/2,1/2).
The budget is the norm of ALL concatenated raw past inputs, including public
preparation, drive, pulse and reset. There is no excluded baseline.
Future preactivations remain in [1/4,3/4]^n, the head is 1_n/sqrt(n),
and the frozen recurrent-group normalization divided by the loss scale is
exactly 1/n. Actual future injections cancel only at a common endpoint.

The target d_rob needs a scope. Write d_F for continuous credit memory in a
one-public-source-feature class, and d_all for the complete normalized
gradient contract. Lower sections below use a single public source vector
per section, never independently selectable source columns. They also lower
bound the larger actual-gradient problem. A theorem on their projected
recurrent gradient does not constitute a new full-model upper/lower law.
Forward state, when needed online, contributes another n coordinates.

The new autonomous localized section uses H=sigma 1_l, where
sigma=tanh(lambda sigma+b0). This is one fixed feature, but its amplitude
is NOT the old H=(2/5)1_l. The short harmonic section retains the old H.
All group scales, epsilon=1/1000, parameters and future queries are unchanged.
Public preparation has source alpha_t H with known 0<=alpha_t<=1.

The accepted certificate is used as supplied:

    delta_0 <= (L_n+H_R)/sqrt(n),
    L_n=O(log n), H_R=O(1+R_abs^2).

It rules out every positive robust credit section when R_abs=o(n^(1/4)).
At R_abs=C n^(1/4) it gives a constant, coefficient-dependent ceiling;
it is not an existence result and need not be informative at larger budgets.

## 2. Off-cycle pair channels and cheap public preparation

Use zero-based memory indices. Select disjoint pairs i_j,j_j outside the
latent cycle and define psi_j=(e_i_j-e_j_j)/sqrt(2), embedded in the actual
state. These are orthonormal, are in the selected recurrent block, and

    O psi_j=psi_j.

Whenever the two coordinates of each pair have the same gate, the reference
sensitivity acting on psi_j stays exactly on psi_j. This holds with arbitrary
public gates elsewhere. It gives an invariant scalar credit channel per
PAIR of physical coordinates, not a claim about one isolated physical row.

Let h_ref be the autonomous fixed point of R0, and mu its common off-cycle
coordinate. The accepted reference equations give, for n>=10^6,

    1/40 < mu < 1/8, sigma>499/10000, sigma<1/20+1/(100n).

For the upper bound on mu, the root equation gives
a c_H^2 S/k <= b0+a c_H/sqrt(k), while S>=(k-d)mu and k-d>=k/2.
Thus mu<=2(b0+c_H/sqrt(k))/a<1/8. Here c_H=1/(1-1/sqrt(k)).
The bound on sigma follows from sigma>=tanh(.05)>.0499.

Use a public R0 zero-input burn-in of B=O(log n) steps, followed by the exact
landing input R0(h_ref-z_B), with norm <=.01. The accepted radial inequality
applies to the reference fixed point as well. To realize this REFERENCE path
with the ACTUAL R, add -(R-R0)h_previous to each raw input. The concatenated
norm of this correction is <=e sqrt(n(B+1))=o(1). Every coordinate remains
in the past input cube. The source trajectory is scalar, known and monotone.
All of this input is counted. Reference sensitivities on every psi_j are
nonnegative scalars times psi_j; their public initial scalar is at most n.

The exact actual sensitivity is compared with the R0 sensitivity using the
SAME prescribed actual gates and public source path. The accepted geometric
transfer proof with 0<=alpha_t<=1 gives

    ||B_actual-B_reference||op<=e n^2

when B acts on the unscaled memory-side parameter vector K H. Its legal-query
error is <=a ||H|| e n, and the extra one-step query-side replacement costs
<=||H||e. Below a conservative total half-margin deduction 4*10^(-9) is used.
Prescribing reference states is NOT differentiating the inverse input lift:
each realized input history is held fixed for parameter differentiation.

## 3. A rigorous single-channel witness at O(sqrt(n)) energy

After the preparation, select one off-cycle pair. Keep all other reference
states at h_ref. For u in [-1,1], hold both pair states at

    c(u)=(1-u)mu/2+(1+u)sqrt(1/(20n))/2

for T=4n steps. Then land exactly back at the SAME h_ref with one reset.
Realize each state by x_t=atanh(h_t)-R h_previous-b0 1.
At u=-1 the hold is the autonomous state; at u=1 the pair is near-critical.
The interpolation is continuous on the whole closed interval.

Reference hold inputs are bounded uniformly: on the pair,
atanh(c)-a c lies between 0 and atanh(mu)-a mu; the common rank correction
is O(mu/k). Other rows have magnitude O(mu/sqrt(n)). Preparation and reset
pair inputs are bounded by .13. All inputs are strictly in the cube, including
the o(1) actual-R correction. A crude full-energy bound is R_abs<=2 sqrt(n)
for all sufficiently large n, uniformly in u.

On psi, reference credit follows M_next=g(a M+1). The critical gate is
g_c=1-1/(20n). Since M_pre>=0,

    M_critical >= g_c[1-(a g_c)^(4n)]/(1-a g_c) > .93 n.

The autonomous hold has g_mu=1-mu^2 and

    M_autonomous <=n exp(-4n mu^2)+1/mu^2 <=1601

for n>=10^6. Thus the difference is >.92 n for these widths. The common
reset multiplies this scalar difference by a g_mu, and its new injection
is identical for both histories.

Choose ONE actual one-step future with preactivation 1/4 on the first pair
coordinate and 3/4 on the second. Put
s_gate=(sech^2(1/4)-sech^2(3/4))/2>.17. Projection onto the unit-Frobenius
parameter direction psi H^T/||H|| gives antipodal half-margin

    >= (.92/2) a^2 g_mu sigma s_gate sqrt(2l/n)-4*10^(-9)
     > .003 > epsilon.

This proves a genuine one-dimensional continuous section with a common
endpoint and O(sqrt(n)) FULL absolute energy. It does not prove that this is
the optimal threshold among all histories.

For a rational certificate of s_gate>.17, the accepted positive-series
estimates give cosh(1/4)<129/125 and cosh(3/4)>2651/2048. Consequently
[(125/129)^2-(2048/2651)^2]/2>17/100. No fitted query constant is used.

## 4. What the scalar hold actually optimizes

For the preceding pair channel, let c=sqrt(z/n), T=kappa n, and define
B_mu=atanh(mu)-a mu. The common holding input on each pair coordinate tends
to -B_mu; B_mu>=mu^3/3>0. Reference bath corrections have squared norm O(1/n)
per step. Initial and final corrections have O(1) energy. Hence

    R_abs^2 = 2 B_mu^2 kappa n + O(1)+o(n),
    M_critical/n -> [1-exp(-(1+z)kappa)]/(1+z).

For the stated one-step query the asymptotic half-margin is

    m(kappa,z)=sigma_infty s_gate(1-mu_infty^2)/2
               *[1-exp(-(1+z)kappa)]/(1+z)

Here mu_infty=sigma_infty=tanh(b0). To see the reference limit, its cycle
coordinates lie above mu and satisfy sum_cycle(v_i-mu)<=1/mu^2<=1600.
Insert S=r mu+O(1) into the accepted root equation Phi(B)=0, using
c_H=1+O(n^(-1/2)). It becomes atanh(mu)-b0=O(n^(-1/2)); hence the asserted
limit. Also lambda->0 gives the source limit. In particular
B_mu->b0-tanh(b0)>0. The finite-n witness does not depend on this limit.
The bracket decreases with z>=0.
Near-zero depth z=0 is therefore optimal at the leading order for this
constant-hold schedule; fixed positive z does not save its leading energy.
Taking T=o(n) makes THIS projected scalar signal vanish; T much larger than
n increases energy after its signal has saturated. The useful scale is T=Theta(n).
O(1) ramp/landing steps do not change the leading energy exponent.

Legal-query visibility of this scalar mode cannot be replaced by an arbitrary
unit adjoint. An off-cycle column satisfies ||(O-I)e_i||<=5/sqrt(n).
Let q_f=sech^2(1/4)<1. Backward propagation from the flat head through L legal
future steps yields, on an off-cycle coordinate,

    |p_L,i| <= q_f^L(1+5L)/sqrt(n),

by the off-cycle column identity and ||p_j||<=q_f^j. Thus the actual allowed
reference adjoint projection on psi is O(1/(beta sqrt(n))) uniformly in L.
After multiplication by w_R ||H|| this chosen scalar channel has visibility
O(|Delta M|/n), not O(|Delta M|/sqrt(n)). Dense transfer adds o(1).

This is a matching exponent statement ONLY for the projected scalar hold
mechanism. It is not an upper for all parameter projections of the history,
all ramps, every single-coordinate excursion, or the full history class.
The global one-direction exponent remains in [1/4,1/2]. No witness at
C n^(1/4), or at n^(1/3), has been proved here.

### 4A. Why a single isolated row in a stationary bath cannot use a short hold

This additional NECESSITY calculation applies to ONE controlled off-cycle
physical row, all other reference coordinates held at h_ref, a constant
near-zero hold, and O(1) ramp/reset steps. It bounds the whole selected
fixed-feature gradient difference, not merely its psi projection. It is not
an upper for a moving or freely evolving bath.

Append O(log n) public autonomous-reference settling steps to the cheap
preparation if necessary. With q=1-(1/40)^2, the all-autonomous reference
sensitivity then has norm <=2/(1-q), uniformly in subsequent time. These
settling steps require only the already counted tiny dense correction.
Only the controlled row i can have a gate above q during the hold.

For this off-cycle row, both the outside row and column of O have norm
rho<=5/sqrt(n); equality of their norms follows from orthogonality and the
common diagonal entry O_ii. Propagate a raw legal-query adjoint backward
through the hold. Write u_t=|p_t,i| and V_t=||p_t,outside||. The legal future
and common reset give u_0<=C_Q/sqrt(n), V_0<=1. At every past step,

    u_(t+1)<=u_t+rho*q*V_t,
    V_(t+1)<=q*V_t+rho*u_t.

Consequently

    max_(t<=T) u_t <=u_0+rho*q*V_0/(1-q)
                     +rho^2*q*T*max_(t<=T)u_t/(1-q).

For T<=n(1-q)/(50q), the last coefficient is <=1/2, so max u_t<=C/sqrt(n).
Subtract the autonomous sensitivity recurrence. Its only new forcing is
on row i, with row-vector norm bounded by
C_0=1+2/(1-q), because its public reference sensitivity is bounded. Pairing
each forcing with the backward legal adjoint proves

    selected query distance <=C' T/n,

using ||H||=sigma sqrt(l) and the unchanged factor 1/n. Thus T=o(n) has
vanishing entire selected credit signal. A fixed-epsilon hold needs
T=Omega_epsilon(n), whether or not its critical gate is exactly 1.

During a near-zero hold the controlled actual state differs from the actual
autonomous fixed point by at least m/2=1/100 for large n. The ACCEPTED
global state-energy inequality gives

    (1/100)sqrt(max{0,T-L_n}) <=1+10000 R_abs.

Since L_n=O(log n), such a visible hold needs R_abs=Omega_epsilon(sqrt(n)).
O(1) ramp/reset perturbations of a bounded public reference sensitivity add
only O(1/n) visible signal and cannot avoid this conclusion. Dense sensitivity
transfer adds o(1). This rigorously excludes n^(1/4) and n^(1/3) for this
isolated-row stationary-bath mechanism. The pair witness supplies the same
energy exponent for one robust credit direction. A globally optimal isolated
row witness or arbitrarily changing bath is still unresolved.

## 5. Many localized channels without a costly bath drive

Here is the bath control omitted by a naive independent-row calculation.
Let s pairs be clamped to zero, with 4*10^6<=s<=eta n, eta=10^(-12).
There are enough off-cycle pairs since their number is asymptotic n/8.
There is a public clamped reference fixed point p with zero on those pairs,
source H, and EVERY other memory coordinate >=1/40.

Proof: use the accepted scalar-reference root equations with the same cycle,
but omit these 2s off-cycle coordinates from S(B). At B_m=atanh(1/40)-a/40,
the original negative Phi bound remains valid because S has only decreased.
At B=b0, Phi has sign of c_H(r-2s)/sqrt(k)-1, which is positive here.
The intermediate-value proof gives B_p in (B_m,b0), and all unclamped
coordinates exceed 1/40. The clamp control at this fixed point is -B_p on
every clamped coordinate and zero elsewhere.

Compare p with h_ref by the accepted global radial secant inequality:

    ||p-h_ref|| <=10000 B_p sqrt(2s)<=500 sqrt(2s).

After one clamp step from h_ref, let the UNCLAMPED bath evolve freely under
R0 while keeping the pairs at zero. The radial inequality on unclamped
coordinates relative to p gives

    ||v_t-p|| <=kappa^t 500 sqrt(2s), kappa=10000/10001.

The outside part of a clamped off-cycle row has norm <=5/sqrt(n), using
J=c_H h_(d-1)/sqrt(k)-c_H^2 sum_selected h/k. Therefore its required clamp
input B_t satisfies

    |B_t|<= B_p+2500 sqrt(2s/n)<.06.

The first clamp costs at most .13 per clamped coordinate. No public drive
is discarded: ONLY these clamp inputs and the tiny actual-R corrections
are used during the hold. The actual correction outside the pairs is also
charged to the full energy. This bound is why s may be proportional to n
with a sufficiently small public proportionality constant, rather than
being capped at sqrt(n) by a forced stationary bath.

## 6. A joint localized multi-channel lower and its energy law

Let D=floor(s/1000). Use the accepted bounded-spread lemma to select a PUBLIC
sign matrix A in {+1,-1}^(s x D) such that

    v(y)=tanh(A y), ||v(y)||2>=sqrt(s)/16 for ||y||2=1,
    |v_j(y)|<1, v(-y)=-v(y).

No matrix search is executed. Its existence proof and deterministic finite
specification are the previously established bounded-spread lemma; it depends
only on s, not on a credit certificate. The map is continuous and injective.

Clamp for T=ceil(1000 n/sqrt(s)) steps, so T<=n. Follow with a ONE-step pulse
whose pair states are

    (+sqrt(.11+.05 v_j(y)), -sqrt(.11+.05 v_j(y))).

Then reset the pair states to zero. At both steps let the bath take its public
autonomous reference update. All pairs have zero sum at the pulse. Consequently
R0 maps their variations to the pairs themselves: the bath and final endpoint
are exactly independent of y. For the actual R prescribe that SAME reference
trajectory by inverse lift. All histories have a common public endpoint;
it need not be h_ref or the old zero endpoint.

Reference pulse inputs are at most atanh(.4)+.06<.484; reset inputs are at
most .4+.06=.46. The actual-R corrections are o(1) in each coordinate.
Thus the whole ball, every preparation/hold/pulse/reset, is admitted.

On each psi_j the public pre-pulse scalar satisfies

    M_pre >=(1-a^T)/(1-a)>=T/2.

The pulse gate is 1-.11-.05 v_j, exactly affine in v; the reset gate is 1.
For a fixed legal one-step query taking the high/low gates on every pair,
projection onto the ORTHONORMAL parameter directions psi_j H^T/||H|| gives
the boundary antipodal half-margin

    >= .05 a^3 sigma s_gate sqrt(2l/n) [T/(2n)] ||v(y)||2
          -4*10^(-9)
    >= .05 a^3(.0499)(.17) T sqrt(s)/(32n)-4*10^(-9)
     > .01 > epsilon.

This is one JOINT D-dimensional section, not D separately visible axes.
Reference cross-talk between these projections is exactly zero; arbitrary
actual dense leakage is paid by the uniform operator transfer above.

Full history-energy norm, including public preparation and dense correction,
is conservatively <=100 sqrt(n) s^(1/4). Endpoint correction squared energy
is O(s); clamp squared energy is O(sT)=O(n sqrt(s)). This is the source of
the power 1/4 in the cost, not a subtracted baseline.

Thus, for sufficiently large n and budgets with the displayed constraints,

    s <= min{10^(-12)n, (R_abs/[100 sqrt(n)])^4}
       => d_F >=floor(s/1000).

In asymptotic notation this yields

    d_F = Omega(min{n,R_abs^4/n^2})

whenever R_abs/sqrt(n) grows enough to exceed the fixed construction constants.
The separate single-channel witness covers an O(sqrt(n)) budget with a smaller
constant. This lower is not a matching upper, and it never yields omega(n).
It gives Omega(n^(2/3)) at R_abs~n^(2/3), and Omega(n) at R_abs~n^(3/4).
Here E(n,s), when E denotes SQUARED energy, is O(n sqrt(s)); the norm is
O(sqrt(n)s^(1/4)). The fixed-query visible margin is >.01 uniformly, dense
cross-talk is <4e-9, and the reference endpoint correction cost is O(s).

## 7. Short harmonic packets: exact removal of the startup obstruction

Use the old admitted square-root co-moving lift and source H=(2/5)1_l,
but take an integer packet length T and temporal frequencies

    nu_j=2pi j/T, f_j=nearest_integer(d j/T), omega_j=2pi f_j/d,
    1<=j<=F.

Assume n>=200, T>=4, T<=d/2, 2F+1<=d/4096, 2F<T-1, and

    F T/n <=1/200.

The f_j are positive, distinct and below d/2. Round ties by a fixed rule.
Project profiles onto the complement of the constant and these ACTUAL spatial
Fourier modes. The old Gaussian/two-net spreading proof works with any such
orthogonal modes: its rank is 2F+1, its row absolute-sum bound is <=1+2F,
and its constants are unchanged. Write q=floor(d/10^6) and use the old joint
odd saturated profiles s_j with the old c_sat=3/131072. On the unit boundary
some profile has ||s_j||1>=c_sat^2 d/(16F^2).

Define the actual physical gate defects (omit physical node zero) by

    D_t(i)=delta/F sum_j s_j((i+T-t) mod d) cos(nu_j(T-t)),
    g_t(i)=1-.15/n+D_t(i)/n, 0<delta<=.01.

Other memory gates are the old public weak gates. The old inverse-tanh lift
is admitted for every such word, and both preparation and reset are counted.
Every profile appears at T-1 or more temporal phases on each transported
spatial line (at most one phase is lost because T<d). Since T-1>2F, the word
map is injective. This is one continuous qF-dimensional closed-ball section.

For b=a(1-.15/n), the exact first-order kernel now is

    K_jg=sum_(tau=0)^(T-1) b^tau exp(-i omega_j tau) cos(nu_g tau)
             -b^T exp(-i omega_j T) sum_(tau=0)^(T-1) cos(nu_g tau).

The second sum is EXACTLY ZERO because each temporal cosine completes an
integer number of periods. No stationary-resolvent substitution, approximate
startup washout, or logarithmic warmup is used.

Let K0 use nu_j in place of omega_j. For real x, its real quadratic form is
the weighted cosine Gram form. Exact temporal orthogonality and Bernoulli give

    x^T Re(K0)x >= b^(T-1) T||x||^2/2 >=T||x||^2/3.

Indeed 1-b<=1.15/n and T<=d/2<=n/8 imply b^(T-1)>=1-1.15/8>2/3.
Rounding gives |omega_j-nu_j|<=pi/d; therefore

    ||K-K0||op<= F pi T^2/(2d) <=8 F T^2/n <=.04 T.

Thus ||Kx||>=T||x||/4 for real x. Also

    |1/(1-b exp(-i omega_j))| >= T/(8j)>=T/(8F).

For this inequality use |1-b exp(-i omega_j)|<=1.15/n+2pi j/T+pi/d,
and T<=d/2<=n/8, making the right side <8j/T.

The old exact ideal-column identity, with this new kernel, yields

    I_j(x)=delta exp(i omega_j x)/[n sqrt(d) F(1-b exp(-i omega_j))]
                   sum_g K_jg s_g(x).

Apply the kernel bound to the REAL profile vector at each spatial row and
then the largest-profile L1 bound. Some actual parameter column satisfies

    ||I_j||1 >=delta c_sat^2 T^2 sqrt(d)/(512 n F^5).

This is a physical L1 signal precursor, not an RMS or raw-rank argument.

## 8. Short-packet corrections and complete actual-query ledger

The old node-zero/Householder pointwise injection error is <=6delta/sqrt(d).
Use the EXACT finite source resolvent bound |Q_t p_j|<=t<=T instead of n,
and sum only T transports. After the 1/n defect factor, its accumulated
L2 error is <=6delta T^2/(n sqrt(d)), and its L1 error is <=12delta T^2/n
because k/d<=3. The final Householder dressing loses at most 4delta T^2/n
in L1: ideal entries have magnitude <=delta T^2/(n sqrt(d)) and the ideal
column has zero sum by the excluded actual spatial modes. The old two O
factors from reset and query remain present. Round up the total to

    20delta T^2/n in physical L1.

A legal one-step query uses coordinatewise preactivations 1/4 or 3/4.
For a real vector z, max_g |g^T z|>=s_gate||z||1; a complex column has a
real or imaginary parameter projection with at least half its L1 norm.
The signal coefficient is still >=1/(50n), as in the accepted proof.
The exact one-step coefficient for bounding an ERROR is <=.4/n, so the
dressing/node losses in query units are <=8delta T^2/n^2. This upper is
charged with an upper coefficient, not with the signal's lower coefficient.
The weaker round number 100delta T^2/n^2 is used below.

For chronological degree j, short-horizon induction gives

    ||Z_1||op<=delta T^2/n,
    ||Z_j||op<= (delta T^2/n)(delta T/n)^(j-1).

This uses max_{t<=T}||a O M0_t+I||<=T and a sum of at most T transports.
All odd orders j>=3 therefore have legal-query half-error bounded by

    delta^3 T^4/n^(7/2)

since delta T/n<=1/2 and the reference all-query coefficient is <=.3/sqrt(n).
This includes all mixed harmonics and chronological noncommutation.
Even degrees cancel EXACTLY because the whole gate word is odd in y.
No perturbative oddness about the autonomous endpoint is assumed here:
this packet retains the old positive square-root gate lift and ends at zero.

Actual dense transfer plus query-side correction costs <4*10^(-9). No old
polynomial approximation is needed for the actual-gradient claim. If the
archived polynomial contract is also requested, it needs its own explicitly
retained epsilon/4 ledger; we do not silently assert it in this new theorem.

Combining the above and d>=n/5 gives the conservative NEW actual half-margin

    M_packet >= 10^(-18) delta T^2/[n^(3/2) F^5]
                 -100delta T^2/n^2
                 -delta^3 T^4/n^(7/2) -4*10^(-9).       (P)

Every error in (P) has a stated origin; future direct terms cancel at the
common zero endpoint. It lower-bounds the actual legal query metric.

## 9. Full absolute packet energy and a superlinear theorem below n

The old exact four-type center energy formula remains applicable with N=T:

    E0^2=k{2b0^2+T[(atanh(sqrt(.15/n))-b0)^2+a^2(.15/n)]}
          +l{(atanh(.4)-b0)^2+T(atanh(.4)-b0-lambda*.4)^2
                    +(b0+lambda*.4)^2}.

This is the FULL center energy, not its perturbation radius. For n>=200,
E0^2<=n(T+2). The actual center correction is <=e sqrt(.16 l+T[.15k/n+.16l]).
The old lift Lipschitz bound gives the WHOLE section displacement from this
center <=3delta sqrt(T+2). Consequently

    R_abs<=2 sqrt(n(T+2))

for the displayed delta and sufficiently large n. In particular squared
absolute energy is O(nT), with source maintenance, bias cancellation,
preparation and reset all included.

Choose

    delta=10^(-10), F=floor(log n),
    T=ceil(10^15 n^(3/4) F^(5/2)).

For all sufficiently large n, every condition in section 7 holds. The first
term of (P) is at least 100; the two variable error terms are bounded by
constants times n^(-1/2)F^5 and n^(-1/2)F^10, respectively, and tend to zero.
Floors/ceilings do not affect these conclusions (T<=2*10^15 n^(3/4)F^(5/2)
eventually). Thus M_packet>epsilon, and

    D=qF >= n floor(log n)/(10^7)

eventually, while

    R_abs=O(n^(7/8)(log n)^(5/4)).

THEOREM: the frozen dense family supports omega(n) fixed-feature robust
credit dimension at this FULL absolute energy scaling, with exact old zero
endpoint and unchanged legal queries. This is new and needs hostile review.
An explicit sufficient onset can be defined as the first integer beyond
which the displayed algebraic/monotonic inequalities and (P)>epsilon hold;
the proof is asymptotic and makes no practical-onset claim.

More generally choose any F(n)->infinity with F=o(n^(1/20)) and the same
T=ceil(10^15 n^(3/4)F^(5/2)). Then (P)'s error terms vanish, and

    d_F>=c nF, R_abs<=C n^(7/8)F^(5/4).                 (T)

Thus within this stated range the lower can be expressed as

    d_F >= c n [R_abs/(C n^(7/8))]^(4/5),

by choosing an admissible integer F no larger than that expression, with
F->infinity and F=o(n^(1/20)). This is a CONSTRUCTION bound, not equality.

For a concrete power theorem, take T=ceil(n^(4/5)), F=floor(n^(1/100)),
delta=10^(-10). Main exponent in (P) is 1/20, dressing exponent -2/5,
and odd-tail exponent -3/10. Hence for sufficiently large n,

    d_F=Omega(n^(101/100)), R_abs=O(n^(9/10)).

This supplies a simple exponent witness in addition to the sharper logarithmic
onset above. For the power ladder, any alpha>7/8 sufficiently close to it
permits omega(n); no construction at alpha<=3/4 is asserted superlinear.

### 9A. One complete cycle preserves the 16/15 power at O(n) energy

Set T=d and nu_j=omega_j=2pi j/d. The short-packet rounding conditions are
replaced by EXACT frequency equality. The startup cosine sums still vanish.
The weighted cosine Gram now satisfies

    x^T Re(K)x >= b^(d-1)d ||x||^2/2 >=d||x||^2/3,

because b^(d-1)>=1-1.15/4>2/3. The denominator bound is
|1-b exp(-i omega_j)|<=1.15/n+2pi j/d<8j/d. Thus the same ideal signal,
node/dressing, finite-Q and odd-tail derivations give (P) with T=d,
without the irrelevant condition F T/n<=1/200. Injectivity needs d-1>2F.

Choose delta=10^(-10)/F^(5/2), F=floor(n^(1/15)/10^4). For all sufficiently
large n the spreading and non-aliasing conditions hold, and d>=n/5 gives

    M_packet >= (4*10^(-20)delta/F^5-delta^3)sqrt(n)
                           -100delta-4*10^(-9)
             >= (4*10^(-30)-10^(-30))sqrt(n)/F^(15/2)
                           -100delta-4*10^(-9)
             >= 3-100delta-4*10^(-9) >epsilon.

The last step uses F<=n^(1/15)/10^4, so sqrt(n)/F^(15/2)>=10^30.
Floor losses give D=qF>=n^(16/15)/(2*10^11), while section 9's FULL energy
bound is R_abs<=2sqrt(n(d+2))=O(n). This is a NEW shorter-history theorem
for the accepted mechanism; historical proofs and their n sqrt(log n) cost
remain unchanged. The old polynomial surrogate is not asserted here.

## 10. A dimension-dependent upper by an actual counted window

This is a new consequence of the ACCEPTED energy certificate, not a re-review.
Let B_R be its bad-step count, q_g=9999/10000, and choose

    J=ceil(log(C sqrt(n)/epsilon)/[-log(q_g)]),
    H=L_n+B_R+J,

with a fixed sufficiently large C for the normalized R/W/b injection bound.
For any last H steps, at most L_n are unclassified initial steps and at most
B_R are bad. The actual chronological transport has norm <=q_g^J.
Before that window the general normalized sensitivity norm is <=C0 n,
and the legal adjoint norm is <=2/sqrt(n). Dropping that older sensitivity
therefore costs <=2 C0 sqrt(n)q_g^J<=epsilon. If the history is shorter,
retain it in full with public zero padding.

The accepted continuous causal window implementation stores the last H actual
states and raw inputs, 2nH coordinates, and the true current state if needed.
It reconstructs the retained-window sensitivity; it reads no discarded
history. These are counted private coordinates, not a free past replay.
Thus in this frozen family under the absolute-energy promise,

    d_all <= O(n[1+R_abs^2+log(n/epsilon)]),

capped by the accepted general O(n^2 log(n/epsilon)) recent-window upper.
In a one-source-feature class it is also capped by the accepted r^2 reference
credit store (with its dense error ledger), giving

    d_F <= min{r^2, C_epsilon n[1+R_abs^2+log(n/epsilon)]}.  (U)

The ZERO-credit certificate supersedes (U) whenever delta_0<=epsilon, in
particular when R_abs=o(n^(1/4)) at fixed epsilon. This is a dimension-dependent
upper but is not sharp and does not exclude superlinearity above that scale.
It uses continuous real coordinates and legal-query transport, not bit counts
or matrix rank as a robustness surrogate.

## 11. Efficiency, failed schedules, and the remaining gaps

Use I=D/R_abs^2 for the dimension lower realized by a JOINT section.
For localized spread-pulse channels, D=Theta(s), R_abs^2=O(n sqrt(s)),
so achieved efficiency is Omega(sqrt(s)/n). This improves as channels are
shared, reaching Omega(n^(-1/2)) at s=Theta(n). A straight Euclidean gate
ball misses the sqrt(s) boundary amplitude and only gives energy O(ns).

For short harmonic packets, D=Theta(nF), R_abs^2=O(n^(7/4)F^(5/2)),
so achieved efficiency is Omega(n^(-3/4)F^(-3/2)). These ratios are section
lower efficiencies, not universal maxima per joule or finite-bit capacities.

Closed/failed approaches:

* n^(1/4) off-cycle hold: its projected channel needs T=Theta(n) and its
  holding drive has nonzero constant size. It supplies no witness at this budget.
* Forcing a stationary autonomous bath while clamping s rows: the exceptional
  row needs O(s/sqrt(n)) input and leaves the cube for large s. The FREE,
  controlled-clamp bath in sections 5-6 resolves this particular obstruction.
* Multiplying separately visible axes: invalid. Sections 6 and 7 construct
  whole balls and prove every boundary antipode, with full coupling charged.
* Using old low spatial frequencies in a short packet: the temporal Gram
  becomes nearly singular when T/n is small. Rounded, widely spaced actual
  spatial frequencies and EXACT temporal periods remove this loss.
* Sparse packets separated by autonomous relaxation: a constant autonomous
  gap erases old carriers; packet margins cannot just be added for free.
* Subtracting source or bias drive: forbidden and not used. The harmonic
  theorem explicitly pays nT squared energy.
* A weak-gate packet T=o(n^(3/4)) with delta bounded and this ledger cannot
  certify even one profile: its main bound delta T^2/n^(3/2) tends to zero.
  This is a limitation of THIS weak-gate proof, not a general impossibility.

Remaining rigorous exponent brackets, at fixed epsilon:

    first robust direction: necessary alpha>=1/4; possible alpha=1/2;
    superlinear dimension: necessary alpha>=1/4;
                           possible alpha=7/8 with polylog energy.

Neither n^(1/4) sharpness nor a matching d_rob law is established. Numerical
results are recorded separately and cannot close either interval. Recommended
next attack: a query-visible, spatially localized transport upper that charges
the actual off-cycle adjoint visibility and rounded-cycle packet transport,
rather than paying all bad time steps with a global operator norm. A proof
that omega(n) requires alpha>3/4, or a packet below 7/8, would narrow the
remaining superlinear gap. Independently hostile-review the NEW packet and
clamped-bath lemmas before adopting these as accepted project checkpoints.
