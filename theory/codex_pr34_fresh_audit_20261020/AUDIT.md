# Fresh independent mathematical audit of PR #34

**Date:** 2026-10-20. **Auditor:** Codex. **Overall verdict: VALID in its explicitly stated R0 scope.**

Target: [draft PR #34](https://github.com/soma2-stack/AI-Architecture-Research/pull/34),
commit **`39af3a97dab0c20628c837e2b72da8c7e70a4e3d`**.
The proof was challenged independently; the earlier Codex verdict was not used as a premise.
No decisive mathematical error or counterexample to the claimed R0 refutation was found.

## Verdicts

| Claim | Verdict | Supporting step |
|---|---|---|
| Balanced locality, common endpoints, width-three legality | **PROVED** | Exact skeleton action and sparse state-setting schedule, section 2 below |
| First-order lower bound, Lemma 4.2 | **PROVED** | Positive pulse polynomials and rational scalar certificates, section 3 |
| Front-gate induction, Lemma 5.0R | **PROVED** | Simultaneous row-class/mass induction; an independent bath bootstrap is given below |
| Background estimates, Lemma 5.1R | **PROVED** with its stated denominator conditions | Chain unrolling, leakage supremum, outside-window closure, section 4 |
| Difference estimates, Lemma 5.2R | **PROVED** with its stated closure conditions | Exact difference identities and carrier accounting, section 5 |
| Proposition 5.4 | **PROVED** | Fresh exact-rational single-monomial majorant; uniform ratio below .3747 |
| Theorem 6.1 | **PROVED for R0 and the selected d_F,E** | Uniform sphere lower bound, legal fixed query, complete mT accounting |
| Corollary 6.2 | **PROVED for R0** | Combined sparse listing count; arbitrary fixed constants; joint zero |
| Original proposed Lemma M, specialized to R0 | **REFUTED** | The joint zero still has bus readout greater than tau |
| Two latest checker fixes | **PROVED to resolve the reported defects** | Positive gate retained; unbounded threshold search succeeds, including C0=10^200 |
| Dense transfer of this many-direction construction | **OPEN** | Gates, credit perturbation and dense readout need their own uniform proof |
| Original dense/full-d_F, D=Omega(n), strict mT problem | **OPEN** | This construction has only D=Theta(n^(1/4)) |

The exact equality `tanh(.38)^2=.1316` printed in PROOF.md:316 is **REFUTED as written**:
the left side is approximately .131556707. The intended upper inequality is true and is
what the proof uses. This is an editorial error, not a failed theorem.

## 1. Coverage, provenance and independence

The full target PROOF.md, REPORT.md and CHECKS.md, the certificate scripts, verification
scripts, saved results, and the supporting definitions from PRs #28, #31 and #32 were read.
PR #33 supplies the construction's history, but its failed first-version all-size claim is
not a premise. The latest commit changes only two checkers and their JSON records; its
mathematical proof is unchanged from `b47eb08`.

Immutable snapshots are in [sources](sources/), with 41 path/commit/SHA256 records in
[source_manifest.json](source_manifest.json). In particular:

* [Target proof](sources/theory/claude_lemma_m_three_memory_20261019/PROOF.md).
* [Target report](sources/theory/claude_lemma_m_three_memory_20261019/REPORT.md).
* [Target checks](sources/theory/claude_lemma_m_three_memory_20261019/CHECKS.md).
* [PR31 definitions and original Lemma M](sources/theory/claude_lemma_m_bus_capacity_20261015/PROOF.md).
* [PR32 two-stream structure](sources/theory/claude_lemma_m_rest_20261016/PROOF.md).
* [PR28 selected metric and listing](sources/theory/claude_multiprobe_memory_20261014/PROOF.md),
  pinned at `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88` because that folder is absent from
  the target branch's root tree.

Four fresh independent scripts were written. None imports the author or earlier audit modules:

1. [independent_all_size.py](independent_all_size.py): exact rational **single-monomial**
   bounds, different from the author's polynomial-envelope implementation.
2. [independent_scalar.py](independent_scalar.py): rational special-function enclosures,
   first-order constants, front mass, and a self-contained bath bootstrap.
3. [independent_counts.py](independent_counts.py): combined listing polynomial, count
   thresholds and exact integer geometry.
4. [independent_frozen_query.py](independent_frozen_query.py): explicit UPU matrix,
   frozen-input finite differences, actual support and endpoint checks.

The argument below, rather than agreement between related code implementations, justifies
the dynamical inequalities. Author scripts were run separately from copies in `author_runs/`.

## 2. Architecture, legality and the front-gate induction

### 2.1 Exact routing and locality

Put k=n/2, d=n/4, a=1-1/n, beta=1/sqrt(k), gamma=1/(1-beta),
`U=I-gamma*w*w^T`, `w=e0-1/sqrt(k)`, and `O=UPU`.
The permutation reads predecessor d-1 in row0, predecessor0 in row1, j-1 in row j
for 2<=j<d, and itself off cycle. Direct multiplication gives

```
O e0 = e0,
J(h) = gamma*h(d-1)/sqrt(k) - gamma^2*sum_(j>=1)h(j)/k,
(Oh)_1 = J + gamma*sum_(j>=1)h(j)/sqrt(k),
(Oh)_j = h(j-1)+J       (2<=j<d),
(Oh)_j = h(j)+J         (d<=j<k).
```

Two active off-cycle states are +v and -v. Their sum is zero for every parameter, so
their change preserves J exactly. All other forward states are common by induction.
The pair is reset to zero and later parked at the common bath value. Consequently it
cannot leave a parameter-dependent forward state behind. Every pair is parked before T.
This proves exact common endpoints by algebra, not by small floating-point residuals.

The physical row0 state is decoupled; its nonzero bias does not feed other memory rows.
Physical row0 credit is zero under the selected row0-excluded group. This does **not**
mean the transformed credit coordinate Y(0) is zero: the latter is explicitly retained
in the birth and broadcast equations.

### 2.2 Simultaneous induction, including the bath premise

Lemma 5.0R is at PROOF.md:400–446. Over the defined history 0<=t<=T:

* free cycle rows are at least the bath;
* inactive off-cycle rows equal the bath;
* the active pair sums to zero;
* the spike is zero and the arrival row is nonnegative.

A free row's predecessor cannot be the previous spike: that spike's successor is the
next driven spike. Row1 compares with the bath using
`gamma*sp/sqrt(k)>=s`, since `sp>= (k-4)s` and `(k-4)/sqrt(k)>=1`.
Counting the k-1 nonzero-index rows, with at most one spike and two active rows,
then gives `sp >=(k-4)s`. This uses time-t premises to establish time-(t+1) conclusions;
it does not assume the desired front bound at the same step.

The bath floor/ceiling can also be verified directly here, avoiding reliance on previous
reviewers of the more general bath lemmas. For a front-chain excess y-s>=0, while the bath
is in [.025,.1009],

```
next_gap <= (1-.025^2)*gap.
```

There is at most one front row of each age. Each initial excess is <=1. Initial chains
with no row1 birth have zero excess. Thus the total free-front excess is <=Q=1600.
The held spike and balanced pair only reduce the mass relative to bath rows. Therefore

```
(k-4)s <= sp <= (k-1)s + 1600.
```

At time1 all initially undriven rows equal tanh(.05), which lies inside the claimed interval.
Using a<=1, gamma<=1/(1-1/7071) and k>=5e7, the next bath preactivation is between

```
.05 -(gamma^2-1)*.1009 - gamma^2*1600/k  >= .04993944578,
.05 +gamma/sqrt(k) +4 gamma^2*.1009/k    <= .05014145080.
```

The lower endpoint exceeds atanh(.025), and the upper endpoint is below .1009;
tanh maps this interval inside [.025,.1009]. This closes the bath and row-class
induction simultaneously for this schedule. Previous-state gap bounds establish the
next bath bound, and then the next gaps; no circular floor argument is required.
The rational inequalities are checked in `independent_scalar.py`.

Now, for t>=1,

```
pre_1(t+1) >= a gamma beta(1-gamma beta)(k-4)*.025 + .05.
gamma(1-gamma beta)=(1-2beta)/(1-beta)^2 >=1-2beta.
```

It follows that

```
pre_1(t+1) >= .025 sqrt(k) -.1/sqrt(k) -.025 sqrt(k)/n
           >= .025 sqrt(k) -.001.
```

The removed algebraic terms are positive. The actual error majorant at n=1e8 is
<1.592e-5. Since `sech^2(p)<=4 exp(-2p)` and `4 exp(.002)<4.009`, the printed
`eps_g(n)=4.009 exp(-.05 sqrt(n/2))` is valid.
At t=1 the tiny gate is not assumed: `delta_1(1)=0`, `Y_0=0` and the birth is zero.

### 2.3 Actual inputs and schedule transitions

Inputs on the prescribed driven set are `x_t(r)=atanh(h_t(r))-(R0 h_(t-1)+b)_r`;
all other actual inputs are exactly zero. No inverse-matrix correction is used.

The scalar common field satisfies
`aJ+.05=atanh(s_t)-a s_(t-1)`, whose absolute value is <=.0763.
The initial spike position is row19, predecessor row18 with age17, giving input
<=.383038075<.3831. Pulse start costs at most `.38+.0763=.4563<.5`.
Later pulse steps, reset and parking have the stated smaller bounds.
These are strict past-input cube bounds; no uniform future input cube is imposed
in this contract. Legal future queries have preactivations in [.25,.75].

At most one spike and one pair are driven at a time. Parking occurs one time step
before the next pair's hold, so peak actual support is3. The full horizon is T=n/2,
including preparation and tail. Hence mT=1.5n. The construction extends continuously
from the sphere to the unit ball, since each pulse amplitude is a continuous function
of its coordinate. Its exact endpoint is parameter-independent throughout that ball.

## 3. First-order separation

For a memory column c off cycle, the own scalar obeys
`o_t=g_t(c)(a o_(t-1)+c_t)`. The source c_t is common, nonnegative, bounded by c_*,
and at least .99 for t>=2. All writing windows occur long after time2.

For z>=0, write x_+=v(z)^2, x_-=v(-z)^2 and e_t=o^-_t-o^+_t>=0.
The seven pulse leakage terms are nonnegative because

```
x(1-x)^w is increasing for x<1/(w+1), w<=6,
0<=x_-<=x_+<tanh(.38)^2<1/7.
```

The expansion's source coefficients may depend on time; they are common in the two
histories and positive, which is all this sign argument needs. During the post-pulse
hold, e decays by a and the leakage deviation is s_t^2>=.025^2. Summing gives

```
Delta F1(c_i) >= F* Pi(z_i),
F*=(gamma/k) a^(2d+1)*.99*.025^2*floor(H/2)*(ceil(H/2)-7),
Pi(z)=(1-v(-z)^2)^7-(1-v(z)^2)^7.
```

No adverse pulse term is dropped. Outside the writing window, Delta lambda1 is zero.
Its sign within the window gives
`Lambda1 <=a^-d |Delta F1|` columnwise, with no cancellation assumption across columns.

Fresh exact-rational Taylor enclosures and monotone cells certify:

| Scalar quantity | Independent bound |
|---|---:|
| Pi(z)/z on (0,1] | >.6272833001966545 |
| pulse Lipschitz coefficient c_s | <.333006850213779 |
| complete front deviation mass | <39.722286275897 |
| corrected spike-start input | <.383038074414 |
| first-order readout coefficient c_R | >.000498854912480 |

The front mass uses 800 outward gap iterates and an **infinite geometric tail**;
the tail is not dropped. Pi on [0,.1] uses a derivative lower bound, and on [.1,1]
uses 2000 monotone endpoint intervals. Numerical sampling alone is not used for
any universal scalar inequality.

## 4. Rechecking Lemma 5.1R

The exact transformed remainder recursion, PROOF.md:377–383, is

```
Z_t(r)=a g_t(r) Zprev(pred r)+kappa_t(r) A_t-lambda_t,
Y_t(0)=(ghat_t+gamma S_t/k) A_t+(sqrt(k)/gamma)lambda_t.
```

For cycle N-chains, retention sums to <=Q. The sum of direct capture weights is
<=kappa_c; the birth at row1 is at most eps_g*Ybar0. Thus

```
Amax <= kappa_c Amax + Q*lhat
        +eps_g*(u1*Amax+(sqrt(k)/gamma)*lhat).
```

Solving proves Q1. Before T, arrival chains have not encountered the unique gather
spike: the two diagonals meet only at the final arrival after T. Never-held bath rows
give Q2; an active pair adds at most H+1 capture/leak forcings; the spike at most d.
Substitution of row1, front, spike and active-pair contents in the exact leak gives
c_fb. The own scalar is <=c_*(Q+H+1), including before and after its hold.

Within I_i there are H+1 time indices, seven pulse steps and a zero-deviation parking
step. The printed L_in safely bounds that sum. For times outside I_i, delta_t(c)=0;
the spike can retain the window mass L_in, whereas every other active pair has only
outside-window direct forcing. This yields the stated l_out denominator and numerator.

In another window J the arrival sum is

```
sum_J |A| <= |J| kappa_c Q1*lhat +Q*L_in +|J|Q*l_out +|J|eps_g*Ybar0.
```

The explicit birth term is present. Multiplying by kappa_h, adding initial bath
content and direct leakage gives eta_oth exactly as printed. Parked rows may retain
credit, but their deviation delta is zero and they are never reused. That persistent
credit is not incorrectly declared erased.

All these are conditional algebraic bounds until their denominators are certified;
section6 certifies those conditions over the entire required dimension range.

## 5. Rechecking Lemma 5.2R and every source term

Subtracting the two exact recursions gives, with plus gates as the homogeneous system,

```
Delta Z_t(r)=a g+_t(r) Delta Zprev(pred r)+kappa+_t(r)Delta A-Delta lambda
  +a Delta g_t(r) Zprev^-(pred r)
  +(gamma/sqrt(k))Delta delta_t(r) A^-
  -(gamma^2/k^(3/2))Delta S_t A^-.

Delta lambda2=(gamma a/k) sum_r[delta+_t(r)Delta Zprev(pred r)
                              +Delta delta_t(r)Zprev^-(pred r)].

Delta Y_t(0)=(ghat+gamma S+/k)Delta A+(sqrt(k)/gamma)Delta lambda
             +(gamma/k)Delta S*A^-.
```

The own-source difference includes `c_t Delta g_c`; there is no Delta c_t for R0.
Balanced forward states cancel the field, but their **gate differences add**.
Each seven-step pulse occupies fourteen row-steps. Consequently

```
sum_pulse |Delta delta| <=14 c_s Pi,
sum_pulse |Delta S| <=14 c_s Pi.
```

The local pair forcing is bounded by
`14c_s Pi [eta+(gamma/sqrt(k))(1+2gamma/k)Q1*lhat]`.
Direct changed-deviation leakage is `(gamma/k)14c_s eta Pi`.
The spatially uniform forcing is the printed sigma_S.
Reset/parking produce no new changed-gate source because the prescribed states agree;
all prior credit difference continues in the homogeneous recursion.

### Carrier accounting

In the following table the coefficients act on total leakage mass Lambda and total
arrival mass Acal before feedback is eliminated:

| Carrier | On Lambda | On Acal |
|---|---|---|
| row1/broadcast | 1/sqrt(k) | (gamma/k)u1 |
| front forced contents | (gamma/k)D_f Q | (gamma/k)D_f Q (gamma/sqrt(k))u1 |
| front births | D_f eps_g/sqrt(k) | (gamma/k)D_f eps_g u1 |
| held spike | (gamma/k)s_hi^2 d | previous coefficient times kappa_s |
| sequential active pairs | (gamma/k)2*xbar*(H+1)*(2+Q/H) | (gamma/k)2*xbar*(H+1)*(kappa_h+kappa_b) |

The front birth propagates along **one** front chain, whose total deviation is <=D_f.
It is not counted afresh at every horizon step. A source in a future pair is sampled
at starts H+1 apart; the bath retention sum is
`1/(1-q^(H+1))<=1+Q/H`. With in-window forcing this gives `2+Q/H`.
The simplification `(1+Q/H)kappa_b/Q<=kappa_b` is valid for H>=100.

The corresponding direct source masses are exactly:

* broadcast: `(gamma/k)^2 Q1*lhat*14c_s`;
* front birth from that broadcast: its D_f eps_g multiple;
* front/spike uniform source: `(gamma/k)(D_f Q+s_hi^2 d)*sigmatilde_S`;
* active-pair uniform and local sources;
* direct leakage: `(gamma/k)14c_s eta`.

These are all the terms of R(eta). In particular the factor `1+D_f eps_g` is justified.
Summing the carrier gains gives a_L and a_A. The arrival sum satisfies

```
Acal <=b_A(Lambda1+Lambda2+sigma_S),
b_A=(Q+eps_g sqrt(k))/(1-kappa_A-eps_g u1),
kappa_A=(gamma/sqrt(k))Dbar(1+gamma/2).
```

For a fixed earlier time the distinct arrivals occupy distinct rows, so the ordinary
deviation sum is <=Dbar and the uniform capture sum involves at most d rows. This is
the origin of the gamma/2 factor; no factor of d or H has been lost.

Solving these two positive scalar inequalities gives the printed eps1 and Phi. The
output is bounded by `Lambda2+kappa_s*Acal+sigma_S`. The other-memory source map is
J-I and has norm D-1 for D>=2, or zero for D=1, always <=D. Thus the vector estimate
works for arbitrary mixed-sign sphere coordinates, including zero coordinates.

## 6. Uniform certificate: independent derivation and implementation

### Primitive bounds

Let x=n^(1/4), r=x/x0>=1. Use the exact integer rounding bounds
`H+1<=40x^3+2`, `1/H<=1/(40x^3)`, `D<=x/160`.
The exact F* lower bound is obtained from

```
floor(H/2)(ceil(H/2)-7) >=(H-1)(H-14)/4 >=(40x^3-14)^2/4,
gamma>=1,
a^-(n/2+1)<=exp(1/2+3/[2(n-1)]).
```

This gives precisely the printed reciprocal coefficient 792. Also
`a^-d<=exp(1/4+1/[4(n-1)])`.
For c=.05/sqrt(2),
`r^40 exp(-c*x0^2*(r^2-1))<=1` when c*x0^2>=20. The positive Taylor sum T20
is a lower bound for the exponential, so the reciprocal used in c_g is an upper bound.
Thus `eps_g<=c_g*r^-40` with c_g>0 throughout the proof.

### New certificate, independent of author and earlier audit code

`independent_all_size.py` uses just **one monomial** C*r^p for each intermediate
quantity. Addition replaces two powers by their larger power and adds their coefficients.
Multiplication adds powers. Coefficients are rounded upward to binary rationals.
An inverse feedback denominator is bounded at r=1 only after checking its power <=0
and coefficient <1. This is a positive-majorant proof, not a numeric grid.

The carrier gains are assembled from section5's table, and the two scalar feedback
inequalities are solved directly. No author `chain`, `Phi`, envelope class or previous
audit implementation is imported.

At x0=31622 the exact final bound is

```
1095237676811160468471582176218434650997798105261
 /2923003274661805836407369665432566039311865085952
 < .3747.
```

Numerical summaries of these rational certificates are:

| Quantity | Independent upper bound |
|---|---:|
| front closure | 5.618946472e-8 |
| background feedback | .005756272275 |
| outside-window feedback | .005756270545 |
| arrival closure | 8.487819599e-8 |
| difference loop e | .006422137813 |
| first error component | .008299518413 |
| own-memory source component | .364507299497 |
| other-memory source component | .001889196395 |
| total | **.374696014304** |

The component powers are 0,-1,-1, so their bounds cannot grow for larger r.
At x0=23667 the same method gives `<.499999392894<1/2`.
The different last digits from the author's output reflect our tighter sqrt(2)
bracket and different rounding; both are outward upper certificates.

Every formula in the author chain has been checked against sections4–5:
Q1,Q2,Eeta,Epi are contents; cfb and fsup are the sup-leak closure;
Lin,eta_self are the own-window estimates; cout,lout,Y0,eta_oth are the outside-window
estimates; bA is arrival feedback; sS is uniform source; aL,aA are carrier sums;
e,ie eliminate feedback; pulse,R are direct sources; src is the solved output source;
eps1,t1,t2,t3 are the vector norm conversion. The replacements of sqrt(k)/gamma by
sqrt(k) are upward relaxations because gamma>=1.

The author's rational `up` uses ceiling integer division in both shift branches.
Its approximate digit count cannot turn upward rounding into downward rounding.
All its feedback inversions check nonpositive exponents. No pointwise monotonicity of
rounded H or D is used. The extreme dimensions are covered by this argument even
when direct floating-point simulation or ordinary exponentials are impossible.

## 7. Theorem 6.1 and metric normalization

The chosen fixed-feature parameter group is exactly PR28's row0-excluded group
`{u f_s^T:u0=0}`, with its declared normalization. Restricting its readout to memory
columns gives a valid lower bound for that group's norm. R0's memory-column source
rows carry zero credit; physical row0 credit is also zero.

For the uniform legal query `g=HI*1`, direct Householder algebra gives

```
nu^T B_T(:,c)=a*HI*sqrt(k)*Z_T(d-1,c),  c off cycle.
```

This is the selected-gradient expression with the actual R0 gates. The future input
can realize preactivation .25 at the common endpoint; it is fixed during differentiation.
The legal-future preactivation constraint differs from the past-input cube. Applying
the past cube to the future query would change the contract.

For every sphere point, ||Pi||>=.6272 and the relative error bound gives a readout
coefficient at least

```
(1-.3747)*.0004988*.6272*400
 =382077059/4882812500
 =.0782493816832 >.078.
```

The floor loss is no worse than `(1-n^(-3/4))^2`. Thus the raw readout exceeds
`.078n(1-n^(-3/4))^2`, whereas `tau<=.0567n`.
Under PR28 normalization this is a pair distance greater than .002, giving robustness
at epsilon=.001. It is not a statement using unnormalized gradients instead of the
selected metric.

The standard-row bus is not identified with transformed Z. Subtracting the own
readout costs at most `a*HI*gamma*c_*(Q+H+1)*sqrt(D)/sqrt(k)`.
Since `a*gamma*c_*<2` in this domain, the printed loose bound `4e3*n^(3/8)` follows.
Its ratio to n decreases as n^(-5/8), and the remaining bus readout is still >tau
already at n=10^18. This explicitly addresses the tiny c_* factor omitted from the
intermediate line PROOF.md:733.

The integer dimension bound also holds uniformly. For x>=31622,

```
D > x/160 -1 -(x/80+41)/(40x^3+2)
  > x/160 -1.001 >= x/161.
```

The pair indices fit and the last parking time is at most T-2. The exact integer
checks include the old H-jump pair, 10^166,10^168,10^180 and10^1000.

## 8. Corollary 6.2 and arbitrary fixed constants

The source statement of original Lemma M quantifies over **every** legal section in
the width/budget regime; it does not require D=Omega(n). The construction is therefore
in its R0-specialized domain. It has m=3 and mT=1.5n, below mu*n^(3/2) at all relevant
n for the inherited fixed mu=2.5e-5 and c0=5e-5.

For the all-query listing, not merely the one-step shortcut,

```
W' <=(8-ln2/2)/kappa+1+(ln n)/(4kappa), Ws=126667,
p=7(W'+450000+1), L<=n/4,
N1<=7(4(W'+Ws)+450000+4),
N2<=232000*p^2/16+2p,
N3<=13000000[(.01+.5 ln n)/.0618+1].
```

The last bound uses r_H=2ln cosh(.25)>.0618. Exact rational inequalities certify
the log/exponential constants. The resulting quadratic coefficients are below
`1.784e17`, `1.187e15`, `1.974e12`.
Adding the proposed bus listing adds `3C0+(9/4)C1+C2*(ln n)^2`.

For every fixed triple, exponential growth n^(1/4) beats this quadratic in ln n.
More explicitly put `g(u)=exp(u/4)/161-P_C(u)`.
Rational positive Taylor lower bounds give g,g',g''>0 at the declared threshold;
g'' increases, so g remains positive for **all** larger arguments.
The fresh independent script certifies the thresholds 10^80,10^100,10^150 for maximum
constants 10^12,10^18,10^30, and 10^826 for (10^200,0,0).

The relevant dimension budget is the combined number of potentially nonzero listing
coordinates: `|Phi|+|Psi|<D`. This is now exactly what is used. Sparse Borsuk–Ulam
applies: a generic projection into that many coordinates is injective on every one
of the finitely many coordinate support subspaces; applying ordinary Borsuk–Ulam
after projection produces a zero of the original concatenated listing.
This avoids assuming the listing's ambient dimension equals its sparsity count.

At the joint zero, Theorem6.1's bound holds because it holds at **every** sphere
point. Its legal uniform query produces bus readout >tau, contradicting a required
bound tau/4 for every legal query. No zero of just one listing is substituted for a
joint zero. The resource conversion's extra restriction `2N3<=D<=n` is not needed
to construct this listing; it also holds at the count thresholds if required.

## 9. Latest checker fixes and remaining editorial notes

### Fixed: arbitrary-constant search

`count_certificate.py:81–100` now uses doubling and bisection. The old cutoff at399
is gone. The regression returns826 for C0=10^200 and confirms825 fails its particular
degree400 certificate. Independent exact bounds confirm that826 is a valid threshold.

Termination does not require an exact exponential implementation. The degree400
positive Taylor lower polynomial eventually dominates P_C and its derivative tests
for every fixed finite input triple. The passing predicate is also monotone here:
after subtracting the quadratic, the test polynomials have a negative low-degree
coefficient prefix and a positive higher-degree suffix, hence at most one positive
root. This justifies the bisection independently of the comment about the true g.

### Fixed: zeroed front gate

`envelope_certificate.py:174–182` now uses the positive upper bound
`c_g*(31622^4/n)^10` and asserts positivity. All23 saved adversarial samples pass,
including n=10^166,10^168,10^180,10^300,10^1000. They no longer silently set this
gate term to zero. The script explicitly describes the pointwise run as a consistency
test, not an exact gate evaluation or the universal proof.

### Remaining minor recommendations

1. **PROOF.md:316:** replace `tanh(.38)^2=.1316` with `<.1316`. No constant changes.
2. **PROOF.md:681–682:** update the older pointwise description to mention the rational
   gate upper bound and high-precision approximations, matching the fixed script header.
3. **PROOF.md:732–733:** state `a*gamma*c_*<2` before dropping c_* in the looser
   intermediate own bound. This supplies the missing one-line justification without
   changing the final `4e3*n^(3/8)` constant.
4. **envelope_certificate.py:327:** assert `val<=Fraction('.3747')`, not merely1/2.
   The actual exact value passes; this would guard the coefficient actually used
   by Theorem6.1 against future regressions.

These are low-priority presentation/verification-strength matters. They do not leave
an unresolved load-bearing inequality in the present R0 argument.

## 10. Computational evidence, reproduction and limitations

From this audit directory:

```
python -I independent_all_size.py
python -I independent_scalar.py
python -I independent_counts.py
python -I independent_frozen_query.py
```

The first three use exact rational comparisons for their universal or finite scalar
assertions. Float values in JSON are summaries, not the basis of the assertions.
The last is numerical evidence only. It constructs U,P,R explicitly and saves
the original controls before perturbing parameters, so it cannot accidentally
differentiate a parameter-dependent reset controller.

Small cases n=512,1024 cover odd/even H, a mixed-sign direction and a near-axis
direction. With the direct future injection included, the frozen-input gradient
**difference** agrees with the analytic readout within2.1e-8. The uniform-query
identity residual is below3.2e-13. Actual peak support is3; common-endpoint residuals
are below7.1e-16. These sizes are outside(H), and their numerical separation/interference
does not constitute either a theorem-scale proof or a theorem-scale counterexample.

The finite-difference checker initially used an overly large central-difference step;
its truncation error failed the requested tolerance. Step refinement and Richardson
extrapolation reduce it with the expected convergence. This was a numerical-check
resolution issue, not a correction to the research proof. The saved final script
records both the raw and extrapolated errors.

Author scripts rerun separately:

```
python -I author_runs/envelope_certificate.py
python -I author_runs/count_certificate.py
python -I author_runs/constants_seq.py
python -I author_runs/exp_skeleton_action.py
python -I author_runs/exp_repair_checks.py 16384 700 5
```

All passed. Both structural histories at n=16384 report all_pass=true. The exact
author envelope reproduces .37469601430339283, all23 pointwise tests retain a positive
gate, and the count regression reproduces826. Scripts and results are preserved
separately from immutable source snapshots.

Confidence limits:

* This is a mathematical/source audit with computer-assisted rational checks, not a
  formal proof-assistant development or a machine-verified transcription of every line.
* No theorem-scale forward trajectory was simulated; the dimensions are astronomical.
  Universal claims rely on the proved majorants, not extrapolation from simulation.
* All unrelated results in the supporting PRs were not re-audited. The directly used
  matrix/metric/listing definitions were checked, and construction-specific bath,
  first-order scalar and feedback estimates were independently established here.
* No dense many-direction transfer or full-gradient normalization theorem is certified.

## 11. Meaning and next research objective

This proves a real mechanism in the specified **learning-credit** metric: a single
moving gather path collects sequential off-cycle leakage from disjoint memory
columns, allowing growing antipodally separated credit directions at constant
peak input width. The forward endpoint is identical, so this is not ordinary
retrievable hidden-state memory. It makes no claim of a practical onset at small n,
a new computational primitive, or a trained model advantage.

The precise result is `D=Theta(n^(1/4))`, `m=3`, `T=n/2`, `mT=1.5n`, for R0 and the
declared selected group. In particular `mT >> D sqrt(n)`, so the proposed stronger
barrier-compatible Lemma M' is not contradicted. The original dense/full-d_F
linear-dimension problem remains OPEN.

The next bounded objective should be a **uniform dense-transfer lemma for this
entire section**, preserving sparse actual inputs, exact common endpoints and the
sphere-uniform margin. It must derive the dense bath/front bounds, replace a by the
actual scaled coefficient where appropriate, bound actual-credit versus R0-skeleton
credit with the same actual gates, and charge the additional dense readout term.
A perturbation bound for only one direction or one finite dimension would not suffice.
That is a useful next theorem; it is not proved in this audit. Achieving D=Omega(n)
within strict little-o budget is a separate and substantially stronger objective.

All existing research, notebooks and governance files were preserved. Nothing was
committed, pushed, merged or sent to external researchers. All audit output is inside
this separate directory.
