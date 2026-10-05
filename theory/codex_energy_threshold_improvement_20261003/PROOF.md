# Balanced short packets with bounded joint profiles

Codex, 2026-10-03. NEW DERIVATION, internally checked; independent hostile review
required. The accepted 7/8 packet is a premise and is preserved byte-for-byte.
This proof concerns fixed-feature continuous credit d_F in the frozen dense
tanh family and actual normalized future queries. No architecture claim.

## 1. Result and exact scope

THEOREM A. For every integer n >= 10^200 and every integer

    2 <= F <= n^(1/20),

the SAME frozen dense tanh family has one continuous admitted closed-ball
history section, starting at zero and ending exactly at zero, with

    D >= n F / 10^7,
    sup_y ||X(y)||_2 <= 4*10^7 n^(3/4) F^(9/4),
    every boundary antipodal legal-query half-distance > .9997 > .001.

The norm counts ALL raw preparation, interior, source, and reset inputs.
The section is injective; all combinations in its ball are admitted.

For F=floor(log n), this proves

    d_F = Omega(n log n),
    R_abs = O(n^(3/4) (log n)^(9/4)).                 (1)

For any fixed 0<beta<=1/20 and sufficiently large n, F=floor(n^beta)
gives

    d_F >= n^(1+beta)/(2*10^7),
    R_abs <=4*10^7 n^(3/4+9 beta/4).                 (2)

In particular beta=1/45 gives exponent 4/5 and dimension Omega(n^(46/45));
beta=1/27 gives exponent 5/6 and dimension Omega(n^(28/27)). Thus the new
construction strictly improves 7/8. The infimum power-energy exponent
within this proved family is 3/4. It is attained with a diverging logarithmic
dimension factor, but not with a positive power beta in formula (2).

IMPORTANT: the old INTERMEDIATE GATE SUBBOX is NOT preserved. Model weights,
raw-input cube, source H, query family, normalization, epsilon and endpoint
are preserved. Gate deficits here are adapted to packet duration, and are
larger than O(1/n). The all-admitted-history contract permits them; their
actual tanh/input admissibility is proved below rather than imported from
the old weak-gate-box lift lemma.

## 2. Frozen model and accepted packet losses

Use

    k=floor(n/2), l=n-k, d=floor(n/4), r=k-1,
    a=1-1/n, lambda=1/(100n), b_model=(1/20)1_n,
    U=I-gamma_U w w^T, w=e0-1_k/sqrt(k),
    gamma_U=1/(1-1/sqrt(k)), P=P_d direct_sum I_(k-d),
    O=UPU, R0=diag(aO,lambda I_l), W=I,
    ||R||op=a, e=||R-R0||op<=4/(10^8 n^2), H=(2/5)1_l.

Let E:R^r->R^k insert a zero at memory coordinate 0, and O_*=E^T O E.
Since Oe0=e0, this selected subspace is invariant and O_* is orthogonal.
M_t is the r-by-r reference credit map defined by
S_t[delta R]=||H|| E M_t p for delta R=(E p)H^T/||H||, with the source
rows zero. Physical probes p_j below have node0 zero and are identified
with E^T p_j when used in this selected recurrence.

All entries of R,W,b remain independently differentiated. Inputs realized
by inverse lift are held fixed for those derivatives. Future preactivations
are in [1/4,3/4]^n; head 1_n/sqrt(n), loss scale max(1,||R||F), and accepted
R-group weight divided by loss scale equals EXACTLY 1/n. Future raw inputs
may realize that box and are not constrained by the past-input cube.

The accepted old packet ledger was

    10^-18 delta T^2/(n^(3/2)F^5)
       -100 delta T^2/n^2 -delta^3 T^4/n^(7/2)-4*10^-9. (3)

Its F^5 losses were: shared word factor F^-1, resolvent F^-1, column selection
F^-1, and bounded-profile L1 guarantee F^-2. Its squared absolute input
cost was Theta(nT). At fixed true gate variation O(1/n), even the universal
degree-one query upper is O(T^2/n^(3/2)); a fixed signal needs T=Omega(n^(3/4)).
This explains why merely increasing the OLD fixed-box amplitude cannot beat
7/8 with the same full-width holding cost. No general impossibility is inferred.

## 3. A quotient-spreading lemma with explicit constants

Let A denote the real orthogonal projection onto the constant and the cosine/
sine spatial modes used by the packet. Its rank is h=2F+1. Put P_perp=I-A and
q=floor(d/10^6). Assume d>=2*10^6 and

    h log(1+512 sqrt(d)) <= d/200.                    (4)

LEMMA B. There is a public d-by-q matrix B with range in ker A such that
for all y,

    ||By||2 <=2||y||2,
    inf_(v in range A)||By-v||1 >=sqrt(d)||y||2/8.     (5)

Proof. Take a d-by-q matrix G of independent standard Gaussians and set
B=P_perp G/sqrt(d). For fixed unit y, the chi-square exponential moment at
1/4 gives Pr(||Gy||2>3sqrt(d)/2)<=exp(-9d/16)2^(d/2)<exp(-d/5).
A 1/4-net of size <=9^q, followed by the usual norm extension factor 4/3,
gives ||G||op<=2sqrt(d) except with probability <=9^q exp(-d/5).

For ANY deterministic shift v, each coordinate of Gy-v, for fixed unit y,
has Gaussian density at most 2/5. Consequently Pr(|(Gy-v)_i|>=1/2)>3/5,
uniformly in v_i. Let J count coordinates whose absolute value is >=1/2.
Independence and exponential Markov at log(3/2) give
Pr(J<d/2)<[(2/5+(3/5)(2/3))sqrt(3/2)]^d=(24/25)^(d/2)<exp(-d/50).
Thus ||Gy-v||1>=d/4 except on an event of probability <exp(-d/50).

Use a 1/64-net of the unit y sphere, size <=129^q, and a sqrt(d)/64-net of
the radius-4d ball in range A, size <=(1+512sqrt(d))^h. Outside the preceding
bad events, extensions from these nets lose at most d/32+d/64 in L1, so

    ||Gy-v||1 >=13d/64 >d/8.

It suffices to cover this v ball: a minimizing v has residual no greater
than ||Gy||1<=2d, hence ||v||2<=2d+2sqrt(d)<=4d. A minimizer exists by
coercivity on the finite-dimensional subspace. The union failure probability
is at most

    9^q exp(-d/5)
      +129^q(1+512sqrt(d))^h exp(-d/50)
    <= exp(-d/10)+exp(-d/100)<1,

using log9<3, log129<5, q<=d/10^6 and (4). Therefore one G succeeds.
Finally distance to range A is unchanged by removing A Gy, so dividing by
sqrt(d) gives (5), first on unit y and then by homogeneity. QED.

For clarity the norm-duality identity used below is

    inf_(v in range A)||z-v||1
      =max_{s in ker A, ||s||infinity<=1} z^T s.       (6)

The <= direction follows from s^Tv=0 and L1/L-infinity duality. For equality,
support the closed unit ball of the L1 quotient by range A at z/dist(z,A).
Finite-dimensional separating-hyperplane duality supplies a supporting
linear functional; it annihilates range A and has dual norm <=1. Its
coordinate representative s gives equality. Equivalently this is the
primal/dual pair of the finite linear program minimizing sum_i t_i subject
to -t_i<=z_i-v_i<=t_i, v in range A. Both optima are attained. There is no
reachability assumption about an ambient operator ball in this lemma.

## 4. One bounded, odd, injective profile map

Define the continuous strictly convex entropy on [-1,1]

    phi(s)=[(1+s)log(1+s)+(1-s)log(1-s)]/2,
    phi(0)=0, phi(+/-1)=log2, phi'(s)=atanh(s).

Let K={s in ker A: ||s||infinity<=1}, and use the SAME public scale
L=128sqrt(dF) for every harmonic. For each block y_j define

    s_j(y_j)=argmax_{s in K}
              [L(By_j)^T s-sum_i phi(s_i)].           (7)

No block is normalized by its own norm, nor given an independent gate budget.
The full domain is ONE closed unit ball in R^(qF). The maximizer in (7) is
unique by strict convexity. It is continuous: any convergent parameter
sequence has compact subsequences of optimizers, each limiting to the
unique optimizer. Symmetry gives s_j(-y_j)=-s_j(y_j).

Every optimizer has |s_i|<1. If a coordinate is at +/-1, moving toward zero
stays in K; the entropy improvement has positive order t log(1/t), which
dominates the linear O(t) change and the finite derivatives of all interior
coordinates. This contradicts maximality. Therefore the exact stationarity
condition is

    P_perp atanh(s_j)=L By_j.                         (8)

If two optimizers agree, (8) and injectivity of B give equal y_j. Thus this
is an odd, continuous, injective map, with exact mode exclusions and a
coordinatewise bound <1 over the whole ball.

On the boundary some ||y_j||>=1/sqrt(F). Equations (5)-(6), testing (7)
against the support maximizer, give

    (By_j/||y_j||)^T s_j
      >=sqrt(d)/8-d log2/(L||y_j||) >=sqrt(d)/16.

Since ||By_j/||y_j||||2<=2,

    ||s_j||2 >=sqrt(d)/32,
    ||s_j||1 >=||s_j||2^2/||s_j||infinity >=d/1024.    (9)

This improves the old d/F^2 guarantee to Theta(d). It is optimal in order
as a profile bound since ||s_j||1<=d. It does NOT remove the shared F^-1
gate-word budget or the joint kernel/column-selection losses.

## 5. General duration-scaled gates

For an integer packet duration T, use

    nu_j=2pi j/T, f_j=nearest_integer(d j/T),
    omega_j=2pi f_j/d, 1<=j<=F,

with a fixed tie rule. Require

    T>=4, T<=d/2, 2F<T-1, FT/n<=1/200,
    zeta>delta>0, (1+zeta)T/n<=1/3,
    beta_max=sqrt((zeta+delta)/n)<=1/10,
    kappa_delta=delta T/n<=1/2.                       (10)

The projection A in sections 3-4 uses these ACTUAL spatial frequencies;
they are positive, distinct, and below d/2. Define the virtual cycle word

    c_t(i)=delta/F sum_j s_j((i+T-t) mod d)cos(nu_j(T-t)). (11)

It has |c_t(i)|<=delta, zero sum, zero Fourier moments at every omega_j,
and is odd in the whole y. It is not an independently selectable set of
parameter columns. It prescribes gates of the actual coupled tanh history.

## 6. Balanced lift: remove the large raw input at the mixing row

Physical memory coordinate 0 is kept at zero. On cycle coordinates
i=1,...,d-1 prescribe

    h_t(i)=+sqrt((zeta-c_t(i))/n).

There are at least d off-cycle coordinates because k-d>=d. Pair each of
these d-1 cycle coordinates with a distinct off-cycle coordinate, and set
the paired off-cycle state to its NEGATIVE. Its gate is identical to the
cycle gate. There remain k-2d+1 coordinates, exactly one or two. If one,
give it the public state +sqrt(zeta/n); if two, use a public plus/minus
pair. These have unmodulated gate 1-zeta/n. The source is H throughout.

Thus the selected-memory sum S_t is either sqrt(zeta/n) or zero, independent
of y and t. Every selected gate is

    G_t=(1-zeta/n)I + D_t/n,

where D_t copies c_t(i) to BOTH members of each pair, omits node0, and is
zero on the remaining public coordinates. ||D_t||op<=delta and D(-y)=-D(y).

Prepare h=(0_k,H) in one step from zero, run T interior steps, then reset
EXACTLY to h=0. Use the exact raw input at every step

    x_t=atanh(h_t)-R h_(t-1)-b_model.                 (12)

No inverse-lift derivative is taken in the sensitivity calculation.

Admissibility is a whole-ball bound. The exact reference row identity for
v_0=0 is, with tau=1/sqrt(k), cH=1/(1-tau),

    J=cH tau v_(d-1)-cH^2 tau^2 sum_selected v,
    (Ov)_1=J+cH tau sum_selected v,
    (Ov)_i=v_(i-1)+J       (2<=i<=d-1),
    (Ov)_i=v_i+J           (d<=i<=k-1).

For n>=200 and |sum_selected v|<=beta_max this proves
||Ov||infinity<1.5 beta_max. Hence interior memory inputs satisfy

    |x_t,i|<=atanh(.1)+1.5(.1)+.05+e sqrt(n)<.303<.5.

Preparation/source holding inputs are bounded by atanh(.4)-.05+o(1)<.375;
memory/source reset inputs are also <.5. Every raw input is strictly within
the SAME old past cube. In particular full energy is bounded without a
subtracted center by

    ||X(y)||2 <(1/2)sqrt(n(T+2)) <=2sqrt(n(T+2)).     (13)

The mirror is ONLY a state-sign/gate schedule in existing coordinates; it
adds no units or parameters. Selected sensitivity injections remain the
true coupled action delta R=E p H^T/||H||, with source H fixed and all raw
inputs frozen. Off-cycle gate modulation must be paid in the credit ledger;
it is not ignored as an energy-only helper.

## 7. Joint first-order kernel at the new baseline

Put g0=1-zeta/n, b=a g0. The actual reference selected sensitivity is

    M_t=(g0 I+D_t/n)(aO_*M_(t-1)+I), M_0=0.

Preparation makes its initial sensitivity zero since the preceding source
was zero. Each harmonic probe is p_j=U v_j, v_j(i)=exp(i omega_j i)/sqrt(d)
on the latent cycle, zero elsewhere. p_j has physical node0 equal to zero,
norm one, and Op_j=exp(-i omega_j)p_j.

For the ideal virtual-cycle part of degree one,

    I_j(x)=delta exp(i omega_j x)
       /[n sqrt(d) F(1-b exp(-i omega_j))] sum_g K_jg s_g(x),
    K_jg=sum_(tau=0)^(T-1)b^tau exp(-i omega_j tau)cos(nu_g tau).

The startup term vanishes EXACTLY since sum_tau cos(nu_g tau)=0. The real
cosine Gram with unrounded nu_j is >=b^(T-1)T/2>=T/3: (10) and Bernoulli
give b^(T-1)>=1-(1+zeta)T/n>=2/3. Rounding loses at most
F pi T^2/(2d)<=8FT^2/n<=.04T. Thus ||Kx||2>=T||x||2/4 for real x.

Also

    |1-b exp(-i omega_j)|
      <=(1+zeta)/n+2pi j/T+pi/d <16j/T,

so its reciprocal is >=T/(16F). Apply this and the K bound at every row,
then use (9). The sum over rows of column-vector L2 norms is at least

    delta T^2 sqrt(d)/(65536 n F^2).

Since sum_j||I_j||1 >=sum_x||(I_j(x))_j||2, some column has

    ||I_j||1 >=delta T^2 sqrt(d)/(65536 n F^3).        (14)

This is a joint guarantee for every boundary point, not separate-axis
counting or replacement of the query metric by Frobenius visibility.

## 8. Mirror, node, twist, actual query, and nonlinear errors

Split D=D_cycle+D_mirror. The inherited exact Householder algebra is linear
in D and therefore holds at any delta: its cycle contribution differs from
the virtual-cycle action on v_j by at most 6delta/sqrt(d). On off-cycle
coordinates p_j has the constant value gamma_U/(sqrt(kd)). Consequently

    ||U D_mirror U v_j||2<=delta gamma_U/sqrt(k)
                          <=2delta/sqrt(d).

Charge both by 10delta/sqrt(d). The exact finite public Q_t acting on p_j
has magnitude <=t<=T. Summing T first-order transports gives latent L2
error <=10delta T^2/(n sqrt(d)), hence physical L1 error <18delta T^2/n.
The ideal column has zero sum. Final reset plus future produce the same
UP^2 dressing as in the accepted proof, losing at most 4delta T^2/n in L1.
Their combined L1 loss is <25delta T^2/n.

For a real physical vector z the legal one-step choice of preactivations
1/4 or 3/4 gives max_g |g^Tz|>=s_gate||z||1, s_gate>.16. A complex column
has a real or imaginary parameter projection with at least half its L1.
The unchanged normalized coefficient for signal is >=1/(50n), and for
bounding errors is <=.4/n. Thus (14) and d>=n/5 yield

    degree-one legal half-signal >=
       A delta T^2/(n^(3/2)F^3)-100delta T^2/n^2,
    A=10^-8 <1/(50*65536*sqrt(5)).                    (15)

All mirror residual coordinates are included. The permitted query is an
actual query chosen on the whole physical vector; it assumes no cancellation
of residual sensitivities.

Expand the exact chronological recurrence in the formal multiplier of D.
Oddness of the WHOLE gate word gives exact cancellation of every even order
between antipodes. Induction using Q_t<=T and ||D||<=delta gives

    ||Z_1||op<=delta T^2/n,
    ||Z_j||op<=delta T^2/n (delta T/n)^(j-1).

At kappa_delta<=1/2, the actual legal-query coefficient <=.3/sqrt(n) gives
the all-odd tail j>=3, including all mixed harmonics and chronology, at most

    delta^3 T^4/n^(7/2).                             (16)

It requires small accumulated defect, NOT small unscaled delta. No Taylor
linearization of tanh is substituted for the exact lift or recurrence.

The accepted dense-reference transfer applies uniformly since ||G_t||<=1,
source amplitudes are <=||H||, and ||R||=a. One can directly bound sensitivity
transfer by e||H|| n^2 and the future-side replacement by e||H|| n. Their
normalized antipodal half-error is <4*10^-9, as in the accepted packet.
All histories end at zero, so future direct parameter injections agree.

The complete NEW actual legal-query ledger is therefore

    M >= A delta T^2/(n^(3/2)F^3)
        -100delta T^2/n^2 -delta^3 T^4/n^(7/2)-4*10^-9. (17)

This is a finite-radius lower, not an exact-rank or tangent statement. The
old polynomial surrogate's epsilon/4 ledger is not silently claimed here;
the contract in Theorem A is the actual physical epsilon-query decoder.

## 9. Explicit parameters, floors, and all-width threshold

Use

    C=10^14, eta=10^-6,
    T=ceil(C sqrt(n) F^(9/2)),
    delta=eta n/[T F^(3/2)], zeta=3/20+2delta.         (18)

For n>=10^200 and 2<=F<=n^(1/20),

    T<=2C n^(29/40), T/n<=2C n^(-11/40),
    FT/n<=2C n^(-9/40)<=2*10^-31<1/200,
    (1+zeta)T/n=1.15T/n+2eta/F^(3/2)<1/3,
    (zeta+delta)/n=.15/n+3eta/[T F^(3/2)]<1/100,
    delta T/n=eta/F^(3/2)<1/2.

All packet conditions (10), T<=d/2, and 2F<T-1 follow. Fourier exclusions
and profile condition (4) hold: h<=3n^(1/20),
log(1+512sqrt(d))<=log n<=n^(1/20), and
3n^(1/10)<=n/1000<=d/200 at this threshold. q>=d/(2*10^6)>=n/10^7.
Gaussian-net existence and profile parity/injectivity therefore hold for
EVERY integer width in the theorem, not just even cycle lengths.

Substitution into (17) yields

    leading signal >=A eta C=1,
    odd tail <=2eta^3 C=2*10^-4,
    twist <=200eta C F^3/sqrt(n)<=2*10^-60,
    M>1-.0002-2*10^-60-4*10^-9>.9997.

Equations (13) and T+2<=3C sqrt(n)F^(9/2) give the stated conservative
absolute norm <=4*10^7 n^(3/4)F^(9/4). Dimension is qF>=nF/10^7.
For a fixed beta, floor(n^beta)>=n^beta/2 once n^beta>=2; combine this with
the explicit n>=10^200 threshold rather than asserting it for arbitrarily
tiny beta already at that threshold. Similarly floor(log n)>=log n/2.

The word map is injective: each transported line sees at least T-1 distinct
temporal phases, since at most one phase is omitted at node0. A nonzero
degree-F cosine polynomial has at most 2F circle zeros. Together with (8)
and the exact inverse lift this makes the history map an embedding of the
one compact ball. Every antipodal boundary pair has the margin just proved.
Borsuk-Ulam applied to a continuous encoder with fewer than qF coordinates
gives one equal-code antipodal pair; uniform epsilon=.001 answers would
then have distance <=.002, contradicting twice this half-margin. The same
lower applies to causal encoders because they must work at terminal time.
No finite-state packing is substituted for this continuous-dimension step.

## 10. Delta maximum and optimized general F frontier

PROVED, for this method's sufficient ledger. With the old zeta=.15 gate box,
true variation must obey |D_t|<=.1; increasing a symbol called delta cannot
change that physical bound. The positive all-memory lift additionally has
a mixing-row term Theta(sqrt(zeta)), so growing zeta fails the past cube.
The balanced mirror removes the latter obstruction exactly.

For the new lift the admissible, useful effective amplitude is limited by

    zeta>delta, zeta+delta<=n/100,
    (1+zeta)T/n<=1/3,
    delta T/n<=1/2,
    (delta T/n)^2 F^3 <= a chosen constant times A.    (19)

The last is the odd-tail/leading-signal comparison. Choosing zeta=.15+2delta,
the asymptotically active sufficient limit is

    delta_max = Theta(n/[T F^(3/2)]),

with a small explicit constant. This is not the optimal admissible amplitude
of every history, only the maximum order supported by (17) with a positive
uniform margin. Dense transfer and exact reset impose no further exponent.
Node/twist needs F^3/sqrt(n) small, independently of delta. Kernel rounding
needs FT/n small, and profile existence needs F log n/n small.

The ten amplitude obligations, with no omitted physical constraint, are:

| Obligation | Sufficient condition / deduction in this construction |
|---|---|
| Positive square-root lift | zeta-delta=.15+delta>0 |
| Inverse tanh defined | max memory magnitude<=.1, source magnitude=.4 |
| Physical gate range | 0<1-(zeta+delta)/n<=G<=1-(zeta-delta)/n<1 |
| Past raw-input cube | Balanced sum gives ||Ov||infinity<1.5 beta_max, hence |x|<.5 |
| Node/Householder/mirror | Charge 100delta T^2/n^2; relative cost <=100F^3/(A sqrt(n)) |
| Dense transfer | ||G||<=1 and ||R||=a give uniform <4e-9 legal half-error |
| Higher odd orders | kappa^2 F^3 small compared with A |
| Accumulated defect | kappa<=1/2 and (1+zeta)T/n<=1/3 |
| Exact common endpoint | Raw reset (12) attains zero and itself stays in the cube |
| Legal-query margin | Coefficient >=1/(50n); ledger (17) must exceed epsilon |

These are jointly sufficient constraints, not a claim that each majorant
is a necessary physical limit. The resulting delta_max is the useful order
of amplitude under this stated proof ledger; a global admissibility maximum
without these sufficient restrictions has not been computed.

Write kappa=delta T/n. The signal-minus-odd-tail part of (17) is

    T/sqrt(n) [A kappa/F^3-kappa^3].

Its maximum over positive kappa is

    [2 A^(3/2)/(3sqrt(3))] T/[sqrt(n)F^(9/2)],
    kappa*=sqrt(A/3) F^(-3/2).                        (20)

Thus this proof family needs T=Omega_epsilon(sqrt(n)F^(9/2)), and the chosen
rule attains that scaling. With Theta(nT) squared holding cost it gives

    D >=c nF, R_abs<=C_E n^(3/4)F^(9/4),
    D >=c n [R_abs/(C_E n^(3/4))]^(4/9),              (21)

for admissible diverging integer F; the latter is a constructive bound,
not equality or a universal upper. For example F=o(n^(1/11)) meets rounding
asymptotically, the weaker twist and profile conditions also follow, and
(18) proves the same formula eventually. The explicit all-width theorem
uses the conservative F<=n^(1/20) subrange. A boundary F=c_F n^(1/11)
also needs the small-coefficient rounding check and is not needed here.

Keeping the OLD profiles would replace F^3 by F^5. The same balanced lift
and amplitude optimization then give T=Theta(sqrt(n)F^(15/2)) and
R_abs=O(n^(3/4)F^(15/4)). Thus the n-exponent improvement comes from the
duration-scaled amplitude plus balanced lift. The new profile lemma improves
the polylog/Pareto factor from 15/4 to 9/4. Spreading alone at fixed box
amplitude improves F factors but leaves the infimum n exponent 7/8.

## 11. Full-width energy, other routes, and impossibility side

PROVED: this construction still has Theta(nT) squared cost. H=.4*1_l
requires source holding raw input atanh(.4)-.05-lambda*.4, bounded below
by .3, on l>=n/2 coordinates. All dense source corrections are o(1).
Therefore source cost alone is >=c nT. No source drive is subtracted.

Replacing H by its autonomous scalar equilibrium sigma eliminates reference
source holding cost and changes the legal signal by a constant. It would
not remove the active memory holding cost: states here tend uniformly to
zero while b=.05, so all selected memory raw inputs tend to -.05, except
finite boundary transitions. Thus the nT order remains. This alternative
source amplitude is not used in Theorem A.

FAILED, constant autonomous bath for the active cycle: its gate gap is
uniformly positive, so the first failing packet inequality is
b^(T-1)>=2/3, and the growing Q_t/resolvent is lost. Autonomous gaps cannot
preserve the T^2 carrier signal by an unchanged proof.

CONDITIONAL, sparse/moving active support or vanishing active fraction:
the first missing identity is Q_t p_j=sum_{s<t}(b lambda_j)^s p_j.
Nonuniform baseline gates no longer commute with O. Neither dimension sF
nor a T^2 signal may be inserted into (21) without a replacement joint
kernel and all-query ledger. Fixed positive active fractions change constants
only; no proved reduction of nT is claimed here.

NO NEW GENERAL IMPOSSIBILITY EXPONENT. The accepted radial/bad-step proof
still gives zero-credit query error O((log n+R_abs^2)/sqrt(n)); it rules out
positive robust margin at R_abs=o(n^(1/4)). The normalization and actual
query geometry are unchanged, but the new construction does not sharpen
that bound. A query-weighted Gramian can bound query magnitudes, yet a
raw spectrum, metric packing or finite rank does not give a continuous
causal-coordinate cap.

The first unresolved upper-side inequality would be a uniform approximation
of ALL reachable credit operators by a continuously selectable O(n)-state
observable quotient at a stronger energy scale. The moving legal-adjoint
spike can overlap history-dependent low-gate rows; the energy estimate
counts at most O(R_abs^2) such time steps but supplies no uniform bound on
their jointly observable quotient dimension. No new alpha>1/4 follows.

Updated sufficient/necessary threshold bracket for superlinear fixed-feature
robust credit: the necessary exponent remains 1/4; sufficient exponent is
now 3/4 with (log n)^(9/4), or any slightly larger power with a positive
power superlinear dimension via (2). This is a bracket, not a sharp phase
transition. The full-model n^2--n^2 log n gap is unchanged.

An exact obstruction to one tempting upper-bound step is worth isolating.
LEMMA C (legal spike leverage). For a legal one-step future with constant
preactivation 1/4, let g=sech^2(1/4). Its reference current adjoint on the
memory block is c=a g O^T 1_k/sqrt(n). Since U1_k=sqrt(k)e0 and
P^T e0=e_(d-1),

    c_(d-1)=a g [sqrt(k)-gamma_U/sqrt(k)]/sqrt(n)
           -> g/sqrt(2)>0.                           (22)

Indeed Ue_(d-1) has that diagonal entry after multiplying by sqrt(k).
Dense replacement changes this adjoint by at most e. This is an ACTUAL
permitted query, not an arbitrary unit adjoint. Thus a uniform bound
max_i |c_i|<=C/sqrt(n), independent of width, is false. It can hold for
off-cycle coordinates, but cannot charge ALL gate-damage rows with the
off-cycle dilution. Equation (22) identifies the first failed inequality
in that proposed stronger energy-only upper. It does not itself construct
a high-dimensional reachable section or disprove other upper methods.

## 12. Review targets and limitations

Review NEW items only: shifted-Gaussian quotient spreading (section 3),
entropy profile injectivity and boundary L1 (4), physical mirror and input
cube (6), off-cycle mirror credit correction (8), large-delta accumulated
odd-tail control (8), and explicit all-width parameter arithmetic (9).

The lower is fixed-feature, continuous real state, finite-error, absolute
past input energy, and the actual normalized query contract. It is not
generic RNN capacity, finite bits, VRAM, runtime, training efficiency or a
practical-onset claim. Old accepted proofs/reviews remain unchanged.
