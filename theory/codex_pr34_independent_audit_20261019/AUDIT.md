# Independent hostile audit of PR #34

Auditor: Codex. Date: 2026-10-19 (local environment date; the author's repair is dated
2026-10-20). Target: draft [PR #34](https://github.com/soma2-stack/AI-Architecture-Research/pull/34),
immutable commit **`b47eb08a281b26dc2273ee0e23ad745238e9ad2b`**, stacked on PR #33.

## Executive verdict

**PROVED:** Theorem 6.1 for the base matrix **R0**, the selected parameter group and the
specified legal-query contract. The revised front-gate induction and the second-order
inequalities support an all-size upper bound below `.3747`, independently reconstructed
here with exact rational arithmetic.

**PROVED:** the mathematical content of Corollary 6.2: the original proposed Lemma M
listing bound is **REFUTED for R0**. The combined state-plus-bus listing count is now
correct. Its explicit thresholds `10^80`, `10^100`, `10^150` pass independent certificates.
The statement that the shipped function computes a threshold for *every* finite choice
of constants is false: its search stops at exponent 399. This is a checker/API defect,
not a failure of the asymptotic refutation. A rigorous terminating fallback is supplied below.

**OPEN:** transfer of this many-direction construction to the prescribed dense matrix,
Lemma M', the unresolved operator form of M_rest, and the original dense/full-d_F
linear-dimension memory problem. This result does not settle the n^(3/2) barrier.

No counterexample to the repaired R0 construction or load-bearing majorant was found.
Two reproducible, non-load-bearing verification claims need correction. Neither requires
a stronger mathematical assumption or a weaker Theorem 6.1.

| Target | Verdict | Exact basis |
|---|---|---|
| Lemma 5.0R, on the constructed history `0 <= t <= T` | PROVED | Skeleton action, synchronous row-class induction and mass floor |
| Lemma 5.1R(a)–(d) | PROVED under its stated positive-denominator conditions | Scalar chain unrolling; window/outside split; explicit birth term |
| Lemma 5.2R(i)–(iv) | PROVED under its stated closure conditions | Difference recursion, pulse sources and carrier sums, derived below |
| Corollary 5.3 | PROVED | Sign-coherent first-order leak and norm of `J-I` |
| Proposition 5.4 | PROVED | Independent positive-polynomial rational certificate, not a grid |
| Theorem 6.1 | PROVED for R0/selected metric | Above plus exact support/endpoints and first-order constants |
| Corollary 6.2, mathematical refutation | PROVED for R0 | Combined sparse listing count and uniform bus lower bound |
| Arbitrary-constant completeness of `smallest_decade` | REFUTED | `(C0,C1,C2)=(10^200,0,0)` returns `None` |
| Pointwise checker evaluates the exact positive-gate formula | REFUTED | At `n=10^18`, `DecArith.epsg == 0` by explicit truncation |
| Original dense/full-d_F barrier; Lemma M' | OPEN | Outside the scope proved here |

## 1. Scope, evidence and independence

The full repaired [PROOF.md](sources/PROOF.md), [REPORT.md](sources/REPORT.md),
[CHECKS.md](sources/CHECKS.md), new certificate code, new structural-check code, result records
and inherited schedule were inspected. All files of the PR's target folder were extracted
directly with `git show`; [source_manifest.json](source_manifest.json) records their immutable
commit and SHA256. The source snapshots were not used as a working checkout.

Supporting definitions were checked in the prior pinned snapshots:

* PR #31 `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab`: R0, selected source credit,
  actual support, original Lemma M, distinction between U-row remainder and standard-row bus.
* PR #32 `cef12b3eb6e5a8e6dbc75904253222b57eda188c`: exact broadcast identity and two-stream
  structure. Its unproved operator claims are not assumed.
* PR #28 `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88`: Theorem 4 listing, all-query `N3`,
  selected metric, and sparse Borsuk–Ulam lemma.
* PR #33 `d6801c2bb1b311b3d132312535b87c86064d2eb9`: prior independently checked first-order
  constants and identities; its refuted all-n certificate is **not** used.

These supporting snapshots and the earlier rational scalar certificate are preserved in
[the separate PR33 audit](../codex_pr33_independent_audit_20261019/AUDIT.md).
The present audit does not recertify every historical theorem in those PRs; it checks the
premises actually used and rederives the new load-bearing estimates.

The independent implementation does **not** import `envelope_certificate.py` or its `chain`.
It forms carrier gains, solves the resulting two-variable positive feedback system, and uses
192-bit outward **binary rational** polynomial coefficients. This differs from the author's
40-digit decimal coefficient rounding and shared `chain` implementation. Formula agreement
alone would not verify dynamics; the derivation in sections 3–5 is essential.

All work is local, lightweight CPU verification. No training, GPU, GitHub comments, merges,
pushes, branch switches or edits to existing research were performed. The old PR33 audit was
already untracked at the start and remains untouched.

## 2. Findings and smallest repairs

### F1 — The threshold-search function is not complete for arbitrary constants

Location: [count_certificate.py](sources/count_certificate.py), lines 81–89; compare
PROOF.md lines 743–745.

```
for e in range(18, 400):
    ...
return None
```

Reproduction: `smallest_decade(10**200, 0, 0)` returns `None`.
For every tested exponent `e <= 399`, the available dimension lower bound is below
`10^100`, whereas the listing allowance already contains `3*10^200`.

**Classification:** REFUTED as an assertion about this function computing a threshold for
every finite triple. The mathematical existence and the three advertised concrete
thresholds survive.

**Smallest repair:** replace the bounded `for` with an unbounded increasing search (or
doubling followed by bisection). Its fixed positive Taylor partial sum of degree 400
eventually dominates a quadratic, so the exact certificate eventually succeeds.

An explicit independent fallback removes even that implementation question. Let

```
A = 1.784e17 + 3 C0 + (9/4) C1,
B = 1.187e15,
C = 1.974e12 + C2,
K = A+B+C,
u = max(8, floor(sqrt(2*161*6144*K))+1).
```

For `u >= 1`, `P_C(u) <= K u^2`, and the fourth Taylor term gives
`exp(u/4) >= u^4/6144 > 2*161*K*u^2`.
Thus `g(u)>0`, `g'(u)>0`, `g''(u)>0`; `u>=8` supplies the derivative margins.
Since `g''` increases, they remain positive for larger arguments.
Take `n1 = 10^max(18,ceil(u/2))`, using `ln 10 > 2`.
This inefficient but explicit threshold works for **every finite nonnegative triple**.
[adversarial_checks.py](adversarial_checks.py) verifies its inequalities exactly, including
the triple above. It changes no author source.

### F2 — The pointwise “exact formula” silently drops a positive term

Location: [envelope_certificate.py](sources/envelope_certificate.py), line 173:

```
self.epsg = EG0*x.exp() if x > -10**6 else Decimal(0)
```

At `n=10^18`, `x=-.05*sqrt(n/2)` is already about `-3.5355e7`.
The program therefore evaluates `epsg=0`, although
`4.009 exp(-.05 sqrt(n/2)) > 0` for every finite n. This applies to all its theorem-scale
pointwise samples, not only `10^1000`.

**Classification:** REFUTED if described as evaluation of the exact positive-gate formula.
These values are approximations obtained by dropping a tiny positive term. Agreement with
an upper envelope is not an independent mathematical certificate.

**Smallest repair:** label this deliberate truncation explicitly, or evaluate with an interval
whose lower endpoint is zero and upper endpoint is the proved positive gate envelope.
A log-domain/arbitrary-exponent representation is another option.

**Impact:** none on Proposition 5.4. Its rational certificate path keeps a strictly positive
`c_g r^-40`. Our independent all-size certificate also retains it and never makes this
truncation.

### F3 — Assertion strength and presentation

The author's main script asserts `value <= 1/2`, while the manuscript uses `.3747`.
Its actual exact rational value is below `.3747`; our script explicitly asserts that
stronger bound. Change the author's assertion to the manuscript bound to prevent regression.
This is not a false mathematical constant.

Occurrences such as `tanh(.38)^2 = .1316` should read `< .1316`; the latter is the intended
upper bound and is what the proof uses. The pulse expansion's shorthand `c` means the
appropriate common, time-dependent `c_t` coefficient, not a constant source sequence.
All those coefficients are positive, so the sign argument survives unchanged.

## 3. Front-gate lemma: independent induction

Write `s_t` for a never-driven off-cycle row, `sp_t=sum_(j>=1)h_t(j)`,
`beta=1/sqrt(k)` and `gamma=1/(1-beta)`.
Direct multiplication of the Householder matrices gives

```
J = gamma*h(d-1)/sqrt(k) - gamma^2*sp/k,
(Oh)_1 = J + gamma*sp/sqrt(k),
(Oh)_j = h_(j-1)+J       (2 <= j < d),
(Oh)_j = h_j+J           (d <= j < k),
O e0 = e0.
```

The last identity matters: the nonzero scalar state in row 0 introduces no missing field in
the other rows. The independent dynamics code applies `U(P(Uv))` directly instead of the
author's reduced action.

The induction is synchronous, not circular:

1. At time zero all rows are zero. At time one, row 1 and the bath both equal `tanh(.05)`.
2. Assume the row classes and mass floor at time t. Every undriven off-cycle bath row evolves
   by the same scalar map. Parking sets a formerly held row exactly to the next bath value.
   No pair is reused. The active pair sums exactly to zero, including a pulse.
3. A free cycle row at `t+1` has a free predecessor: the successor of the spike is the next
   driven spike. Thus monotonicity of tanh preserves `h>=s` on free cycle rows.
4. Row 1 compares with the bath through
   `gamma sp_t/sqrt(k) >= gamma(k-4)s_t/sqrt(k) >= s_t`.
5. Among rows `1,...,k-1`, removing one spike and the two active rows leaves at least `k-4`
   bath-or-above rows. Hence `sp_t >= (k-4)s_t`; the arrival state is nonnegative.

This is a statement on the defined finite history, through T. It need not assert the same
row classes after an arbitrary future control.

The bath interval used here is the inherited state bound under (H), not a consequence of
assuming the desired credit estimate. For this prescribed schedule, all imposed state
values lie in `(-1,1)`, the source is undriven and only three coordinates are controlled;
the input bounds are checked separately below.

Consequently, for `t>=1`,

```
pre_1(t+1) >= a*gamma*beta*(1-gamma*beta)*(k-4)*.025 + .05.
gamma*(1-gamma*beta) = (1-2 beta)/(1-beta)^2 >= 1-2 beta.
```

Using `a=1-1/n`,

```
pre_1(t+1) >= .025 sqrt(k) - .1/sqrt(k) - .025 sqrt(k)/n
           >= .025 sqrt(k) - .001 .
```

The omitted terms in the first inequality are **positive**, namely
`.05/n + .1/(n sqrt(k))`. At `n>=10^8` the two displayed errors sum to less than
`1.592e-5`, leaving substantial slack. Finally
`sech^2(p)<=4 exp(-2p)` and `4 exp(.002)<4.009`.

At t=1 the tiny-gate inequality is not used: `delta_1(1)=0` and `Y_0=0`.
All births are therefore either zero or carry the new gate factor.
**Lemma 5.0R passes.**

## 4. Background estimates and outside-window bookkeeping

For a fixed memory column c the exact recursion is

```
Z_t(r) = a g_t(r) Z_(t-1)(pred r) + kappa_t(r) A_t - lambda_t,
Y_t(0) = (ghat_t+gamma*S_t/k) A_t + sqrt(k)/gamma * lambda_t.
```

No row-0 own injection appears. Source injection is retained in lambda1, and `c_1=0`.
The common source is bounded by c_* and is at least `.99` from time two.

A cycle N-chain has retention at most q and summed deviation at most D_f. A birth is
`a g_1 Y_prev(0)`, so its contribution is at most `eps_g Ybar0`.
Solving the scalar arrival inequality gives the printed Q1. The arrivals relevant to the
horizon occur before the gather spike reaches `d-1`; hence they remain N-chains.

Never-held off-cycle rows give Q2. Active pairs and the spike retain at most one per step,
so their content bounds are Q2 plus at most H+1 forcings, or Q1 plus at most d forcings.
Substitution in the leakage identity gives c_fb and f_sup. The own scalar cannot exceed
`c_*(Q+H+1)`: before its hold it has bath retention, during the hold it gains at most c_* per
step, and after parking bath contraction cannot increase that upper bound.

Within I_i the own deviation is s_t^2 except for seven pulse steps; parking has zero
deviation. This gives L_in and eta_self.

Outside I_i the own deviation is **exactly zero**. The spike can contain the own-window
mass L_in and at most d outside-window forcings; the currently active other pair can
contain only its own outside-window forcings. Row 0, front, spike and pair substitution
gives precisely the displayed l_out equation and its denominator.

For another window J, summing arrival chains over J gives

```
sum_J |A| <= |J| kappa_c Q1 lhat + Q L_in + |J| Q l_out
             + |J| eps_g Ybar0 .
```

The last term is necessary and is now present. Multiplying by kappa_h and adding the
initial bath content and direct outside forcing gives eta_oth as printed.
Old held rows may retain bus credit after parking; they are not erased or ignored.
Their gate deviation becomes zero, so they do not re-enter the leakage sum, and no pair
is subsequently reactivated.

The front deviation sum D_f includes the row-1 upper bound and excludes the separately
counted held spike. Counting row 1 again in c_fb is conservative. The inherited exact
rational scalar certificate gives D_f<39.723 before rounding to39.73, and
`39.73+.1009^2+2*.1316=40.00338081<40.01`.

**Lemma 5.1R passes with its stated denominator qualifications.**

## 5. Difference recursion and independent carrier derivation

Let Delta mean plus minus minus; all gates outside the two rows of each seven-step pulse
agree exactly. Subtracting the recursion, without dropping any parameter-dependent term,
gives for r>=1:

```
Delta Z_t(r) =
 a g+_t(r) Delta Zprev(pred r) + kappa+_t(r) Delta A_t - Delta lambda_t
 + a Delta g_t(r) Zprev^-(pred r)
 + (gamma/sqrt(k)) Delta delta_t(r) A^-_t
 - (gamma^2/k^(3/2)) Delta S_t A^-_t.

Delta lambda2_t =
 (gamma a/k) sum_r [delta+_t(r) Delta Zprev(pred r)
                    + Delta delta_t(r) Zprev^-(pred r)].

Delta Y_t(0) =
 (ghat_t+gamma S+_t/k) Delta A_t
 + sqrt(k)/gamma Delta lambda_t
 + (gamma/k) Delta S_t A^-_t.
```

The first-order difference includes
`(gamma/k)[a delta+_c Delta o + a Delta delta_c o^- + c_t Delta g_c]`.
There is no Delta c_t term because R0's source is common and undriven.
Balanced *states* cancel the shared forward field; their squared states and gate differences
add rather than cancel. Thus the 14 row-step pulse count is necessary.

For pulse i',

```
sum |Delta delta| <= 14 c_s Pi_i',
sum |Delta S|     <= 14 c_s Pi_i'.
```

The source mass in a pair is bounded by
`14 c_s Pi_i' [eta+(gamma/sqrt(k))(1+2gamma/k)Q1*lhat]`.
The direct leakage source is `(gamma/k)14 c_s eta Pi_i'`.
The uniform source mass is sigmatilde_S*Pi_i', exactly as printed.
Parking/reset do not add a changed-gate source: both antipodes prescribe the same state.
Their accumulated credit differences persist in the homogeneous recursion.

### Arrival feedback

Unrolling the pre-T arrival chains gives retention Q for scalar leakage and uniform source.
For a fixed earlier time the arriving chains occupy distinct rows; summing captures uses
at most Dbar deviation mass plus the uniform contribution from at most d rows:

```
kappa_A = (gamma/sqrt(k))*Dbar*(1+gamma/2).
```

Births are bounded by
`eps_g [u1 Acal + (sqrt(k)/gamma)(Lambda+sigma_S)]`.
Hence
`Acal <= [(Q+eps_g sqrt(k))/(1-kappa_A-eps_g u1)](Lambda+sigma_S)`.
The replacement `1/gamma <= 1` is an upper relaxation, not an equality.

### Leakage carriers

The following independently derived coefficients are before solving feedback:

| Carrier | Coefficient on Lambda | Coefficient on Acal |
|---|---:|---:|
| row 1 through Y(0) | `1/sqrt(k)` | `(gamma/k)u1` |
| N-front scalar/capture forcing | `(gamma/k)D_f Q` | `(gamma/k)D_f Q (gamma/sqrt(k))u1` |
| N-front birth | `D_f eps_g/sqrt(k)` | `(gamma/k)D_f eps_g u1` |
| spike, at most d times | `(gamma/k)s_hi^2 d` | same times kappa_s |
| active pairs | `(gamma/k)2 xbar(H+1)(2+Q/H)` | `(gamma/k)2 xbar(H+1)(kappa_h+kappa_b)` |

Front-birth mass is D_f times the summed births, **not** a fixed tiny number times the entire
horizon. For active pairs, starts are H+1 apart. Bath retention at sampled starts sums to
at most `1/(1-q^(H+1)) <= 1+Q/H`; adding within-window forcing gives `2+Q/H`.
The bath-capture simplification follows from
`(1+Q/H)/Q=1/Q+1/H<=1` at H>=100.

The direct sources in the table become:

* row-1 broadcast source `(gamma/k)^2 Q1*lhat*14c_s`;
* its front-birth propagation multiplied by D_f eps_g;
* front and spike uniform source terms `(gamma/k)(D_f Q+s_hi^2 d)sigmatilde_S`;
* active-pair uniform and local pulse sources;
* direct changed-deviation leakage `(gamma/k)14c_s eta`.

These reproduce R(eta), including the factor `1+D_f eps_g`. No horizon-length factor has
been silently discarded. Summing the carrier coefficients gives a_L,a_A and
`e=a_L+a_A b_A`. Solving

```
Acal <= b_A(Lambda1+Lambda2+sigma_S),
Lambda2 <= a_L(Lambda1+Lambda2)+a_A Acal+R_src
```

gives Lemma 5.2R(iii). The spike recursion bounds its output by
`Lambda2+kappa_s Acal+sigma_S`, giving (iv) and (5.4).
In the independent code these inequalities are solved directly rather than copying the
author's eps1/Phi expressions.

First-order leakage has one sign per memory column. Therefore
`||Lambda1||_2<=a^-d ||Delta F1||_2`. The other-memory source map is J-I, with operator norm
D-1 (zero if D=1), and `||Pi||_2<=||Delta F1||_2/F*`.
This establishes Corollary 5.3 without assuming aligned sphere-coordinate signs.

## 6. Formula-by-formula certificate comparison

Every operation in the author's `chain` is covered by the following mapping. There is no
reliance on the pointwise/envelope agreement as independent evidence.

| Code quantity | Mathematical origin / audit |
|---|---|
| `u1,kc,kb,kh,ks,kA` | Broadcast factor and six capture estimates from the row classes |
| `Q1` | Solved arrival supremum; code replaces `sqrt(k)/gamma` by larger `sqrt(k)` |
| `Q2,Eeta,Epi` | Bath, active pair and spike unrollings |
| `cfb` | Exact c_fb majorant; its isolated `isk` equals `(gamma/k)sqrt(k)/gamma` |
| `fsup,lhat` | Bounded own injection and positive feedback inversion |
| `Lin,eta_self` | H+1 window, seven pulse deviations, within-window bus bound |
| `cout,lout` | Outside-window equation, including spike mass L_in |
| `Y0` | Broadcast bound with the same upward `1/gamma` relaxation |
| `eta_oth` | Other-window arrival sum, including its nonzero birth contribution |
| `bA,sS` | Summed arrival inequality and 14-step uniform source |
| `aL,aA` | Sum of the five carrier rows in section 5 above |
| `e,ie` | Positive two-variable feedback elimination; invert only when e<1 |
| `pulse,R` | Local source, direct leakage, broadcast, birth and uniform propagation |
| returned `src(eta)` | `(1+ks*bA)(aA*bA*sS+R)/(1-e)+(1+ks*bA)*sS` |
| `eps1` | Coefficient of Lambda1 after output substitution |
| `t1,t2,t3` | Corollary 5.3 with a^-d, 1/F*, and D/F* |

### Primitive envelopes and rounding

Set `r=x/x0>=1`, x=n^(1/4). The `1/k`, `sqrt(k)`, `1/sqrt(k)`, d envelopes have the
correct powers -4,+2,-2,+4. Both decimal square-root brackets are strict rational brackets.
Gamma is decreasing, so freezing its upper bound at x0 is valid.
`H+1<=40x^3+2`, `1/H<=1/(40x^3)`, and `D<=x/160` hold even across ceil/floor jumps.

For the first-order reciprocal, the floor product is at least
`(H-1)(H-14)/4 >= (40x^3-14)^2/4`.
With gamma>=1 and
`a^-(n/2+1)<=exp(1/2+3/[2(n-1)])`,
the printed `792 s_lo^2 (1-.35/x0^3)^2 x^2` denominator is correct.
The a^-d upper bound follows from `-ln(1-1/n)<=1/(n-1)`.

For c=.05/sqrt(2), replacing its denominator by the upper rational bracket decreases c,
so increases the exponential bound. If c*x0^2>=20, the derivative of
`40 log r - c*x0^2(r^2-1)` is nonpositive for r>=1.
Thus `eps_g<=c_g r^-40`. The Taylor partial sum used in c_g is a **lower** bound for exp,
so its reciprocal is an **upper** bound. Its positive terms cause no cancellation.

The author's `up` uses integer ceiling division, including its negative-shift branch.
It rounds upward for every nonnegative rational regardless of the rough digit estimate.
Polynomial addition/product preserve upper bounds. Each feedback inversion checks all
exponents <=0 and value<1 before freezing the reciprocal at x0. The final nonpositive
exponents prove the uniform bound. No monotonicity of H(n)/n is assumed.

### Independent exact results

From [independent_certificate_result.json](independent_certificate_result.json):

| Quantity, x0=31622 | Independent outward upper bound |
|---|---:|
| front closure | 5.618946472e-8 |
| background feedback c_fb | .005756272275 |
| outside feedback | .005756270545 |
| arrival closure | 8.487819599e-8 |
| difference loop e | .006422137813 |
| eps1/a^d | .008299518413 |
| Phi_self/F* | .364507299497 |
| D Phi_oth/F* | .001889196395 |
| total eps_SO | **.374696014304** |

The displayed last digits are outward decimal summaries; the JSON contains the exact
binary-rational result used in assertions. Component maximum exponents are respectively
0,-1,-1. At x0=23667 the independent bound is below `.499999392894<1/2`.
The small difference from the author's `.37469601430339283` comes from our tighter
sqrt(2) bracket and different outward rounding.

This is an all-real-x>=x0 proof, hence includes all admissible integer dimensions,
including dimensions far beyond any finite numeric grid. Separate exact integer geometry
checks covered the old rounding pair, `10^166`, `10^168`, `10^180`, `10^1000` and `10^10000`.
Those checks are supplementary; the universal argument is the envelope proof.

## 7. Theorem 6.1: legality, normalization and resources

* The schedule uses one spike and one disjoint pair at a time, including parking.
  Parking and the next hold start are one time step apart. Thus actual peak support is3;
  no tiny dense correction, reference support or additive support is substituted.
* The source is undriven. Its time-one credit is zero, and all pulses occur much later.
* The spike actually starts at row19. Its predecessor has front age17, giving input
  `<.3831`; pulse start is bounded by `.38+.0763=.4563<.5`. The other transitions,
  resets and parking satisfy the stated smaller bounds.
* Balanced pulses preserve the common field exactly at every parameter value.
  After each reset/parking, changed states agree exactly. All pairs have parked before T.
  Floating-point endpoint residuals are only checks of this algebraic equality.
* The inputs are continuous functions of theta, with fixed scheduled supports; the sphere
  includes zero, negative and mixed-sign coordinates. No discontinuous sign choice is used.
* `T=n/2` includes preparation and the final tail. `mT=1.5n`.
  `D=floor((n/4-41)/(H+1))` fits the off-cycle pairs and gives the claimed
  `D>=n^(1/4)/161`. The last parking is `T-d+39+D(H+1)<=T-2`.

The query is the fixed legal uniform one-step gate vector `HI*1`; the exact common endpoint
permits the same future input, held fixed when differentiating. The selected row-0-excluded
parameter group and normalization are inherited from PR #28. Restriction to memory columns
can only decrease this group's Euclidean readout norm. It does not authorize replacing
the full original gradient metric by the selected metric.

For every unit theta, first-order separation and the second-order certificate give

```
(1-.3747)*.0004988*.6272*400
  = 382077059/4882812500
  = .0782493816832 > .078.
```

The floor loss `(1-7/(20n^(3/4)))^2` is larger than the displayed
`(1-n^(-3/4))^2`, so the theorem's lower bound is conservative.
It exceeds `tau<=.0567n` throughout n>=10^18.

The U-row remainder Z is **not** silently identified with the standard-row bus.
On memory column c the own correction is `nu_c Delta o_T(c)`,
with `|nu_c|=a HI gamma/sqrt(k)`. Even including c_*, the asserted loose bound
`4e3 n^(3/8)` comfortably dominates its vector norm. Dividing by n makes that loss
`4e3 n^(-5/8)`, negligible already at the stated threshold and decreasing thereafter.
Hence the bus lower bound itself exceeds tau, not merely tau/4.

**Theorem 6.1 passes in precisely this R0 scope.**

## 8. Corollary 6.2: complete joint listing and all-constant quantifier

PR #28's listing includes its state, carrying-row and spike-row parts. Its counts are
nonzero-coordinate budgets for the sparse Borsuk–Ulam lemma; they need not equal the
ambient array length. Concatenating Phi and Psi adds those budgets.
It is the **sum** which must be below D.

For m=3,T=n/2:

```
W' <= (8-ln(2)/2)/kappa + 1 + (ln n)/(4kappa),
Ws=126667, p=7(W'+450000+1), L<=n/4,
N1 <=7(4(W'+Ws)+450000+4),
N2 <=(232000/16)p^2+2p,
N3 <=13000000[(.01+.5 ln n)/.0618+1].
```

These are the all-query definitions, not the smaller one-step shortcut.
The outward polynomial
`1.784e17+1.187e15*u+1.974e12*u^2`, u=ln n, dominates their sum.
Add `3C0+(9/4)C1+C2*u^2`.

Our independent rational calculation uses this **coarser** polynomial rather than calling
the author's polynomial builder. At the three advertised thresholds, lower bounds for
`(g,g',g'')` are:

| max C_i | n1 | positive g lower bound |
|---|---:|---:|
| 10^12 | 10^80 | 1.2314e17 |
| 10^18 | 10^100 | 9.0868e21 |
| 10^30 | 10^150 | 7.7116e34 |

All derivative margins are recorded in the exact-check output. They use rational lower
arguments `u1=exponent*2.302585`, rigorously below ln n1. Since g'' increases, positivity
continues for every larger n. F1 supplies a terminating general-C construction.

The domain has fixed inherited `c0=5e-5`, `mu=2.5e-5`; m=3 satisfies both width and budget
conditions well below these thresholds. The all-query state listing is continuous/odd,
and its construction does not require assuming Hypothesis B. Sparse Borsuk–Ulam therefore
gives a joint zero of `(Phi,Psi)` whenever the combined bound is below D. Theorem 6.1
supplies bus readout >tau at **every** sphere point, including that zero. A single legal
query suffices to contradict a claim about every legal query.

The resource corollary's separate restriction `2N3<=D<=n` is not needed for existence of
the listing, but also holds at these large thresholds. No D=Omega(n) premise has been
inserted into the original Lemma M quantifier.

**The mathematical Corollary 6.2 passes.** Its code-completeness phrase needs F1's repair.

## 9. Reproduction and finite checks

From this audit directory:

```
python -I independent_certificate.py
python -I independent_dynamics.py
python -I adversarial_checks.py
```

The first is an exact rational universal certificate. The second is finite numerical evidence.
The third deliberately invokes copied author functions only to reproduce their defects and
independently checks extreme integer geometry and the general-C fallback.

Author scripts were run separately from `author_runs/`:

```
python -I author_runs/envelope_certificate.py
python -I author_runs/count_certificate.py
python -I author_runs/constants_seq.py
python -I author_runs/exp_skeleton_action.py
python -I author_runs/exp_repair_checks.py 16384 700 5
```

All completed successfully. The two repaired structural cases report `all_pass=true`.
The author envelope reproduces `.37469601430339283`; its count reproduces thresholds
80,100,150. Original snapshots in `sources/` retain the submitted result files.

The independent simulator uses Householder multiplication and permutation directly at
n=8192,H=200,D=3. It tests an axis, all-equal coordinates, opposite signs and a near-zero
coordinate. For both antipodes it checks every time step:
row classes, mass floor, front-gate margin, front mass, actual input magnitude/support,
U-row recurrence and broadcast identity. It also checks the summed arrival and output
inequalities with measured source terms.

Results in [independent_dynamics_result.json](independent_dynamics_result.json):

* maximum recursion residual: `2.96e-13`;
* maximum endpoint residual: `9.22e-15`;
* minimum bath: `.0387663` (positive in these tests);
* arrival/output inequalities pass in every column, including nominally zero-coordinate columns;
* measured SO/F1 ratios `.3252`–`.3308`.

These n are below (H) and cannot certify Theorem 6.1. They are adversarial algebra and schedule
checks only. The asymptotic conclusion rests on the derivation and exact all-size certificate,
not a small-size simulation or an underflowed pointwise exponential.

## 10. Final scope and next action

The previous PR33 all-size failure is repaired without hiding its negative result, assuming
sign cancellation, or raising n to avoid a growing error term. The new gate envelope decays,
and all repeated feedback is explicitly closed.

Recommended small changes to PR34: make the arbitrary-constant threshold search terminating,
label the pointwise exponential truncation accurately, and assert `.3747` directly.
These do not require another construction or new assumptions.

The precise new conclusion is a robust selected-metric R0 family with
`D=Theta(n^(1/4))`, `m=3`, `T=n/2`, refuting the proposed original Lemma M bound for R0.
It is consistent with `mT >> D sqrt(n)`.
Neither the prescribed dense transfer nor a linear robust memory dimension follows.
The dense/full-d_F original question, Lemma M', and the remaining barrier program stay **OPEN**.
