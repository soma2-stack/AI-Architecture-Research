# Independent audit of the proposed Hypothesis B counterexample

Auditor: Codex. Date: 2026-10-15.

Audited commits:

- [PR #29, c19ec9b51e0865e332cf1f933582bc94be718160](https://github.com/soma2-stack/AI-Architecture-Research/pull/29/commits/c19ec9b51e0865e332cf1f933582bc94be718160).
- [PR #27, c9874081461139373a276efeb47394d50781c0e3](https://github.com/soma2-stack/AI-Architecture-Research/commit/c9874081461139373a276efeb47394d50781c0e3).
- [PR #28, 0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88](https://github.com/soma2-stack/AI-Architecture-Research/commit/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88).

No target PR, research notebook, or AGENTS.md was modified. No GPU, training, merge,
or outside contact. Independent code is in this directory. Author code was run only
from byte-identical copies in `author_comparison/`. Its hashes and the clean target
worktree states are in `scope_and_provenance.json`.

## Executive verdict

**The quantitative counterexample is PROVED for its explicitly stated R=R0 system.**
I independently derived all six inequalities of Lemma E, certified a nonnegative
majorant with exact rational arithmetic, enclosed the transcendental constants with
outward-rounded intervals, and obtained `E_Y < 1018.375 < 1019`. The endpoint,
listing-zero, coherent-arrival and one-step-query arguments work in that system.
I found no counterexample to this scoped mathematical result.

**The claim of a counterexample under the unchanged original frozen dense-family
contract is INCOMPLETE.** The proof explicitly chooses R=R0. This matrix is not the
original final dense matrix. Satisfying the perturbation norm bound is not the same
as using that fixed matrix. The proposed reference-support convention is also not
the actual-support definition in the audited PR #27/#28 accounting. The ordinary
dense inverse lift does not fix this: it violates the narrow actual-support budget.

These two statements must not be collapsed:

1. **Hypothesis B over the broad class described only by the displayed norm
   inequalities, including R0: REFUTED.** In that interpretation the counterexample
   is in the domain and its D=1 is legitimate.
2. **Hypothesis B restricted to the original prescribed fully dense R, with actual
   input support: still OPEN on the evidence audited here.** PR #29 has not supplied
   the needed sparse actual-input realization for that fixed R.

Thus the requested unchanged-contract certification is **INCOMPLETE**, not a
refutation of the intended dense counterexample. This is a model-domain gap, not
a failure of Lemma E. If the intended question is expressly the broader norm-ball
formulation of B, the answer is **PROVED counterexample / REFUTED B**.

The original linear-dimension, full-metric, strict `mT=o(n^(3/2))` question remains
**OPEN** under either interpretation. D=1 does not resolve it. Lemma M and removal
of the logarithmic loss remain **OPEN**.

## 1. Prioritized findings

### P1: the R0 counterexample does not preserve the original fixed dense matrix

References: PR #29 PROOF.md lines 76–95 and 198; PR #27's section 0 accounting;
PR #28's section 0 and section 7.5; CURRENT_THEORY.md's scope/contract;
`theory/gamma_c_over_n_quadratic_20261001/PROOF.md`, section 7; and
`theory/codex_holding_cost_attack_20261003/PROOF.md`, sections 1 and 3.

The inherited final matrix is a prescribed fully dense perturbation followed by
normalization. The foundational construction expressly says that its block matrix
is **not yet dense**, and defines its final matrix by

```
R = alpha (R0 + eta C),     alpha = a/||R0+eta C||op,     eta > 0.
```

In contrast, Theorem R sets R=R0, including exactly zero memory/source cross blocks.
The norm bound `||R-R0|| <= 4e-8/n^2` permits this limiting matrix but does not
identify it with the original fixed family. The broad norm-ball theorem statements
and the narrower inherited frozen-family contract therefore require separate verdicts.

The two input notions are exactly related by

```
x_actual,t = x_ref,t - (R-R0) h_(t-1).
```

Small norm does not imply small support. Here is an explicit obstruction to using
that lift to certify the requested width. Consider the original construction's
positive rank-one choice `C=11^T/n`; for the large dimensions in question its
power-vector selection can take the all-ones vectors (the required inverse images
are nonzero). Write `lambda=1/(100n)`. At the second, still-autonomous reference step,
`h_1=tanh(.05)1` and `x_ref,2=0`. Every source coordinate of the actual input is

```
x_actual,2(j) = -tanh(.05) [alpha eta - (1-alpha) lambda].
```

Since `||R0+eta C|| <= a+eta`,

```
alpha eta-(1-alpha)lambda
 = alpha(eta+lambda)-lambda
 >= eta(a-lambda)/(a+eta) > 0.
```

Consequently at least `l=n/2` coordinates are actually driven already at step 2.
This is greater than `c0 n=5e-5 n`. Tiny positive eta does not help. This calculation
is exact; `check_scope.py` verifies the rational sign at the threshold n.

It disproves the **claimed transfer/accounting shortcut**, not the possibility of
some other sparse dense-R construction. A proof using sparse inputs and altered
autonomous trajectories could still work, but it is not in the audited argument.

The correction is to state the R0 result with that scope, or supply an actual-support
dense-R realization and redo the affected state, source, credit and listing-zero
estimates. Do not change the support definition to repair this gap.

### P2: a false numerical chain, with an available correction

REPORT.md line 68 and REVIEW_RESPONSE.md lines 100–101 infer

```
.11790 n >= 2.0826 tau.
```

This is false. With `t=tanh(.05)`, the source fixed point obeys
`t <= sigma <= t/(1-lambda)`. For even n,

```
tau/n = .002 sqrt(2)/sigma,
.11790 / (.002 sqrt(2)/t) = 2.08246214159136... .
```

Even the upper ratio obtained using `sigma<=t/(1-lambda)` is below 2.0826 throughout
the stated n range. The **stronger available inequality does imply the desired ratio**:

```
||Gamma||/n >= .11791 - .00000056 = .11790944,
.11790944 / (.002 sqrt(2)/t) > 2.08262887986631.
```

Therefore use `.11790944 n > 2.0826 tau` before rounding, or retain `.11790 n` and
state `>2.082 tau`. This presentation error does not invalidate the R0 theorem.

### P2: bath rows can receive capture and leakage

PROOF.md line 170 says bath rows (`delta_i=0`) neither capture nor leak. The exact
identity immediately above it says otherwise. At such a receiving row,

```
capture_i = -gamma^2 q^3 (sum_j delta_j) V0,
leak_i    = -gamma q^2 sum_j delta_j Vj,       q=1/sqrt(k).
```

For an exact algebraic example take k=16, gamma=4/3, ghat=3/4, delta_3=1/4 and
all other deviations zero. At the bath row i=2:

- For `V=e0-e4`, the capture is `-1/144`.
- For `V=e3-e4`, the leak is `-1/48`.

Both V have zero coordinate sum, as required for the credit transport identity.
These are counterexamples to the claimed algebraic consequence, not new history
constructions. The corrected statement is that bath **source** rows make no
`delta_j Vj` contribution; bath **receivers** can receive the uniform corrections.
E1–E6 retain these terms, so their derivation is unaffected.

### P2: finite front attenuation is not exact destruction

PROOF.md line 191 calls the wrap channel dead; the summary/report repeat this.
For every finite preactivation, `sech^2(z)>0`. The term `g_1 a Y_prev(0)` is therefore
not identically zero. The correct assertion is exponential attenuation. The
`g1max B0` and `g1max B0-` terms in E1/E4 do account for it. My certificate keeps a
strictly positive bound `g1max/q <= 10^-230`, rather than replacing it by zero.

### P2: a generic dense merge is not a universal dense merge

Remark 0.1 correctly derives
`Delta x_t=-R Delta h_(t-1)` when the states merge, but its transition from
“generically every coordinate” to “case (A) covers every section” is unsupported.

For `R=alpha(R0+eta 11^T/n)` and distinct off-cycle memory indices i,j,
`v=e_i-e_j` satisfies `R v=alpha a v`. Set

```
h_1(theta) = tanh(.05) 1 + z theta v,
x_2(theta) = -alpha a z theta v.
```

The second state is independent of theta. Both input steps have support at most
two and are legal for sufficiently small z. Thus a fully dense matrix can admit a
sparse exact merge. This example makes no robustness claim; it refutes the purported
inference from density and injectivity alone. The original robust-section question
is not answered by that inference.

### P3: the comparison scripts use two more arrivals than the proof

The mathematical construction ends arrivals at `T-W_tail-2 J_M-2`, rounded for
even cardinality. `exp_drift_capture.py:50` uses `T-wsim-2 J_M`. Its importing
simulation scripts therefore test a schedule with two extra arrivals. This is
distinct from the earlier predictor off-by-one that was repaired.

My implementation uses the proof's endpoint and still passes. This discrepancy
does not disprove the theorem; it limits the claimed exact correspondence of the
author's simulations with its written schedule.

### P3: two minor bookkeeping corrections

`120001*.2501 = 30012.2501`, so the stated intermediate bound `T<=.2501n` alone
does not imply `mT<=30012n`. The claimed 30012 bound is nevertheless true using the
actual T formula: at n0 the upper ratio is below `30000.250000048`, and the continuous
ceiling envelope divided by n decreases. The looser 30013 bound in Step 4 is also safe.

In Proposition 0.2, `<4.1e-8` bounds one history's extra-column leakage, so the
antipodal difference costs `<8.2e-8 sqrt(n)` in readout, not `<4.1e-8 sqrt(n)`.
The displayed final ledger `47 tau/64 + 3e-7 sqrt(n)` still covers this. Adding one
scalar to the count also preserves the advertised resource coefficient: the strict
coefficient margins in PR #28 absorb `1-2/D` for `D>=36000` (checked exactly in
`check_certificate.py`). This remains a conditional statement, not a full-gradient
obstruction or a proof of B.

## 2. Exact contract audit, scoped to R0

| Requirement | Result |
|---|---|
| Zero initialization | PROVED: all states and credit start at zero; `c_1=0`. |
| Source feature | PROVED: the same unit source feature; no dimension-dependent renormalization. |
| Past cube | PROVED: every prescribed input is below .4732 in absolute value. |
| Actual support | PROVED for R0: at most ell+1=120001. Not transferred to the fixed dense R. |
| Full horizon | PROVED: T includes preparation, all arrivals, hold, tail and resets; no interval is free. |
| Continuous section | PROVED: targets and inverse inputs are continuous on [-1,1]; finite horizon implies finite radius. |
| Common exact endpoint | PROVED for R0 for every theta, not merely for the two endpoints of the parameter interval. |
| Listing zero | PROVED for R0: all odd listed states/inputs/source amplitudes and final own profiles vanish at theta=1. |
| D=1 in B's listing domain | PROVED: the resource corollary's `2N3<=D<=n` is not an assumption of the listing or B. |
| Legal query | PROVED: choose future preactivation .25 in every coordinate, giving gate HI. |
| Normalization | PROVED: the inherited scale is `sigma sqrt(l)/(n sqrt(n))`; no selected-group rescaling. |
| Full metric | No large-dimension conclusion: separation in a normalized projection only supplies a D=1 lower section in larger groups. |

For R0 the source scalar follows the autonomous lambda-contraction from zero to
sigma. Thus `0<=c_t<=1` and `c_t>=1-lambda^(t-1)`, which proves the claimed
`c_t>=1-1e-12` for t>=3 without an initialization exception hidden in a sum.

The balanced modulation states at each time have opposite signs, equal magnitudes,
and lie strictly before row d-1. Their state-sum difference and their end-row
difference are exactly zero. Their successors remain driven. Induction therefore
gives common J, common Sum', common source states, and common states everywhere
except the presently modulated positions. All modulation is reset well before the
final window. The selected feature is never redefined.

The largest input is the start of the spike, following the sixth front-chain value.
The independent upper is `.472107471739898...`. The first modulation uses at most
`.45+beta`, later modulation at most `.45-a tanh(.45)+beta`, and reset at most
`a tanh(.45)+beta`. These bound every interior theta, not just the antipodes.

At n0=1.5e18 the exact integer data are

```
W_tail = 479014,
T      = 375000000000599046,
|A|    = 374999999999520962,
mT/n  <= 30000.250000047924079364.
```

The bound on `W_tail` by its continuous expression plus one proves the uniform
budget for all larger n divisible by four. Actual ceiling-valued fractions need
not literally be monotone at every integer jump; their smooth upper envelopes
are sufficient.

For the listing window, `W <= (27+.25 ln n)/kappa+2 <= W_tail-3`. Every differing
input and state is earlier than t0=T-W. A modulated position (r,t) on an arrival
diagonal ending at t_A has final local index

```
r + T-t = d-1 + T-t_A > d-1.
```

Consequently it is on no final local own-profile path. The off-cycle own profiles
and source amplitudes are common as well. All odd parts in listing items (i)–(v)
vanish, irrespective of soft weights or chosen block lengths. The extra scalar
in Proposition 0.2 vanishes too.

No Borsuk–Ulam invocation is needed to *find* this particular zero. A low-dimensional
section may have a zero even when dimension counting does not force one. Rejecting
the construction just because D=1 would be incorrect.

The uniform one-step query is realized by the common raw future input
`.25*1-R0 h_T-b`. It is held fixed under differentiation. The future preactivation
restriction is satisfied; it must not be replaced with the past input-cube restriction.

## 3. Independent derivation of the exact credit identities

All the following algebra is for the selected group, R0, and memory parameter columns.
Source-column differences are zero for this construction. Put `q=1/sqrt(k)` and
`gamma=1/(1-q)`. The useful block entries of U are

```
U_0j = U_j0 = q,
U_ij = delta_ij - gamma q^2,       i,j>=1.
```

Since B'(0,:)=0, `sum_i Y_i=0` for Y=UB'. The same is true of `V=aPY_prev`.
Writing `delta_i=g_i-ghat`, the standard-coordinate pre-gate credit at row i>=1 is

```
(UV)_i = V_i + gamma q V_0.
```

Thus, directly from `Y=UG(UV+cE)`,

```
Y_0 = ghat V_0 + q sum_j delta_j V_j
      + gamma q^2 (sum_j delta_j) V_0 + c q gvec,

Y_i = g_i V_i
      + gamma q (delta_i-gamma q^2 sum_j delta_j) V_0
      - gamma q^2 sum_j delta_j V_j
      + c g_i e_i - gamma q^2 c gvec.                    (A)
```

These reproduce Lemma 1.2 and the broadcast identity, including the gates on
injection. Replacing g0 by ghat is legitimate precisely because selected credit
row 0 remains zero for R0. It is not legitimate for arbitrary actual dense credit.

Uniform F-step query weights satisfy

```
U nu_F = (ag)^F (P^T)^F U1 = (ag)^F sqrt(k) e_(d-F),   1<=F<=d-1.
```

Also, from the same block entries,

```
Sum'(B') = sqrt(k) Y_0,
J(B')    = gamma q (Y_(d-1)-Y_0).
```

Lemmas 1.1–1.3 are therefore PROVED in their stated reference-credit scope.

**Important distinction:** define the local own profile O by the standard skeleton
recursion and put Z=Y-O. If D_bus=B'-O is the standard-coordinate bus, generally
`Z != U D_bus`. In fact `U D_bus=Z+(I-U)O`. The estimates of Lemma E concern Z,
not a separately identified physical bus row. At the final antipodes `Delta O_T=0`,
so `Delta Y_T=U Delta D_bus,T`; this is exactly what is needed to conclude that
the final readout is entirely bus content. No intermediate identification is needed.

## 4. Lemma E: term-by-term verification

Use the author's six suprema, taken over the *whole* finite history. Let

```
A  = O_D + zeta,            A- = O_h + zeta-,
L_D = B0 + Sigma zeta + nu_N O_D + mu (O_h+zeta-) + w,
L_- = B0- + Sigma (O_h+zeta-).
```

The two A bounds exclude the final time: the spike reaches d-1 only at T, and
arrivals read at time t are from t-1<T. This prevents an omitted large final-spike
term or a circular A bound.

### 4.1 Geometry and scalar budgets

Each non-spike local path has at most ell held/modulated positions and at most
seven changed gates. It cannot have passed through a held spike position: the
spike continues on its own nonbranching diagonal all the way to T. Outside its
drive interval, such a path is a bath or front-chain path. Consequently its
weighted forcing lifetime is bounded by

```
Lambda <= ell + 1/s_lo^2 <= 120401.
```

The independent front comparison uses

```
z_1=1,   z_(r+1)=(1-s_lo^2)tanh(z_r).
```

The exact tanh addition formula proves the comparison when the bath is positive.
An induction closes positivity and the bath interval: the resulting mass bound
gives `|epsilon_t| <= 1.270083e-9`, and the next bath state stays within `1.5e-9`
of tanh(.05). At t=1 the bath is exactly tanh(.05), so there is no circular
assumption of a settled initial state.

The outward-rounded comparison gives

```
sum z_r                         < 51.652224,
sum_(r>=2) z_r(z_r+2s_hi)       < 11.811647,
|M|                             < 6064.104 < 6350.
```

This yields both instantaneous and per-diagonal gate-deviation sums. The front
is counted separately by 1, not incorrectly included in the 11.82 wake budget.

```
Sigma <= 1 + 11.82 + (ell+1)s2 + 8*.1756 < 314,
Dbar  <= 1 + 11.82 + (ell-7)s2 + 7*.1756 < 314,
mu    <= 8*.1780 = 1.424,
mu_d  <= 7*.1780 = 1.246,
w     <= sqrt(8)*.1780 < .50347.
```

The more precise interval sums give Sigma<313.726943 and Dbar<313.531376.

Own-profile columns on a cycle path are distinct. Squaring their coefficients,
the held portion contributes at most ell and the unheld portion contributes at
most `ghat_max^2/(1-ghat_max^2)`. Hence

```
O_h < 346.698121 < 346.70,
O_D <= (1-sech(.45)^14) O_h < 258.783976 < 258.79.
```

The own differences are supported only on rows d-10,...,d-1: modulation starts
at offsets 8 and 9 on the paired arrivals. In a leakage sum, rows reading an own
difference therefore lie in d-9,...,d-1. At most eight have a modulated gate and
the remaining one has a hole gate, giving

```
nu_N <= 8*.1756+.0024959 = 1.4072959 < 1.41.
```

The long spike's own norm is at most `sqrt(k/2+194)`. The 194 allowance safely
covers its short prefix through row 6. No other long-lived own path is hidden
inside the non-spike O_h bound.

### 4.2 E1: non-spike difference

Subtract the local own recursion from (A). The remaining forcing consists of
capture, leakage and the column-spread injection. Antipodal subtraction also
produces changed capture, changed leakage, and `(Delta g_i)a Z_prev^-` transport.

Unrolling the non-spike path gives exactly the following conservative ledger:

| Contribution | Upper bound in E1 |
|---|---|
| Entry through front row 1 | `g1max B0` |
| Receiving-row capture deviations | `gamma q Dbar A` |
| Uniform capture correction | `gamma^2 Sigma Lambda q^3 A` |
| Changed receiving capture | `gamma q mu_d A-` |
| Changed uniform capture | `gamma^2 mu Lambda q^3 A-` |
| Leak reading the broadcast mode at j=1 | `gamma Lambda q^2 B0` |
| Leak reading the preceding spike | `gamma Lambda q^2 s2 S` |
| Other non-spike bus differences | `gamma Lambda q^2 Sigma zeta` |
| Only the near-arrival own differences | `gamma Lambda q^2 nu_N O_D` |
| Changed leak coefficient times full minus credit | `gamma Lambda q^2 mu(O_h+zeta-)` |
| Changed column-spread injection | `gamma Lambda q^2 w` |
| Changed local transport | `mu_d zeta-` |

Their sum is E1. At time 1 the front gate is not tiny, but its incoming credit is
zero; using g1max for subsequent entry terms therefore loses nothing. The reset
terms are included in the changed-gate and injection accounting; no derivative of
the chosen control is taken, because actual raw inputs are frozen when differentiating.

**E1: PROVED for the R0 construction.**

### 4.3 E2: broadcast difference

Subtract the first line of (A). Its leading term is bounded by A. The deviation
sum reads the front/broadcast mode, the spike, other bus rows, near-arrival own
differences, and full minus contents at changed gates. These contribute
`q(L_D-w+s2 S)`. The uniform capture correction contributes
`gamma q^2(Sigma A+mu A-)`; injection contributes qw. Thus

```
B0 <= A + q(L_D-w+s2 S) + gamma q^2(Sigma A+mu A-) + qw.
```

This is E2, including broadcast feedback. Off-cycle rows have delta=0, so they
are not omitted deviation sources; their parameter columns remain in the vector
norms and injections. **E2: PROVED.**

### 4.4 E3: spike difference over the full hold

The spike gate is 1 in both histories. Its own term in the leakage sum combines
with transport, producing

```
tr_t = a(1-gamma s_t^2/k),
kap_t = gamma a q(s_t^2-gamma q^2 sum_j delta_j),
|Delta kap_t| <= gamma^2 mu q^3.
```

The remaining leak sum excludes this spike row, so it is bounded by `L_D` without
the `s2 S` term. The initial own difference at `(6,Ts-1)` is zero. There are
`d-7<=k/2` steps. Discarding attenuation (not summation!) gives

```
S <= zeta + (k/2)[gamma q(s2+gamma Sigma q^2) A
                  + gamma^2 mu q^3 A- + gamma q^2 L_D].
```

This is E3. In particular the O(1/k) forcing is multiplied by k/2; it has not been
dismissed as a small per-step error. **E3: PROVED.**

### 4.5 E4 and E5: full minus-history contents

For full minus contents, replace the near-arrival difference bound by
`Sigma(O_h+zeta-)`, retain the front and spike contributions, and use
`||c gvec||<=sqrt(k)`. There are no changed-coefficient terms. The same path
unrolling and broadcast identity give

```
zeta- <= g1max B0- + gamma q(Dbar+gamma Sigma Lambda q^2) A-
         + gamma Lambda q^2(L_-+s2 S-) + gamma Lambda q,

B0- <= A- + q(L_-+s2 S-) + gamma q^2 Sigma A- + 1.
```

The last 1 in E5 is the norm of `c q gvec`, not an assumed nonzero initial source.
These are E4/E5. **Both PROVED.**

### 4.6 E6: full minus spike

Separate its local own profile, bounded by `sqrt(k/2+194)`, from the incoming
non-spike remainder at row 6. Capture, the remaining full-content leak, and
the column-spread injection then give

```
S- <= sqrt(k/2+194) + zeta-
      + (k/2)[gamma q(s2+gamma Sigma q^2) A- + gamma q^2 L_- + gamma q].
```

This is E6. Counting the own profile separately is conservative when the
spike self-leak has already been folded into tr_t: the extra attenuation only
decreases its positive coefficients. **E6: PROVED.**

### 4.7 Exact rational majorant certificate and all-n extension

I constructed the unscaled right sides above, then applied the diagonal scaling
`X=(zeta/q, B0, qS, zeta-/q, B0-, qS-)`. This avoids merely transcribing the author's
scaled implementation. All matrix coefficients are nonnegative.

At k0=7.5e17, use the rational upper bound

```
q <= 288675134594813 / 250000000000000000000000,
gamma <= 1/(1-q),
sqrt(1/2+194q^2) <= .707106781186548,
g1max/q <= 10^-230.
```

The first and third assertions are checked by exact rational squaring. The last
follows from `log(4 sqrt(k))- .0996 sqrt(k)` at k0 and its decreasing derivative.
Solving `(I-M)x*=b+10^-7 1` by exact rational elimination gives approximately

```
x* = (368086.362610241, 258.791232492016, .322958256780074,
      229772.851744825, 347.704484388523, 1.63983453170820).
```

Every coordinate of `x*-(b+Mx*)` is **exactly 1/10000000** in the rational certificate.
Furthermore

```
max_i (Mx*)_i/x*_i < .778063 < 1.
```

This proves rho(M)<1 without relying on a floating-point eigenvalue. Finiteness of
the original horizon and nonnegativity then give `X<=(I-M)^(-1)b<=x*`.

After scaling, the coefficients are nonnegative polynomials in q, gamma, the
displayed square root, and `g1max/q`. Each decreases with n in this range. Thus
the same certificate covers every qualifying n>=n0, not just a numerical sample.

## 5. Main term, final error and bus identification

For each column `r_j=d-1-j`, `10<=j<=ell-1`, the injection precedes every modulation
of either member of the paired arrival. There are exactly seven changed gates:

```
Delta O_(t_A)(d-1,r_j)
 = -[1-sech(.45)^14] c_(t_A-j) a^j.
```

The coefficient in brackets lies in
`[.7464245122961768330087424591816148522804905209994021896443807,
  .7464245122961768330087424591816148522804905209994021896443817]`.
All these column contributions are negative. Every capture coefficient used in
the main term is positive since `s_lo^2-gamma Sigma/k>0`. All transport factors
are positive. Hence coherence across arrivals and across the selected 119990
columns is genuine, not an unjustified norm-of-sum lower bound.

The independent interval calculation of the conservative coefficient is

```
HI * modulation * (1-gamma*s2*.5002) * .7785
   * (s_lo^2-gamma*314/k) * .249999 * (1-1e-12) * sqrt(119990)
 > .11791179996531860 > .11791.
```

Here `.7785` follows from `log(1-1/n)>=-1/(n-1)` and the full T+ell+2 exponent.
The proof's arrival count lower bound includes parity loss. Earlier source terms
are actually far beyond time 3, so using `1-1e-12` is safe.

The exact spike unrolling separates initial content, all own captures, all bus
captures, changed capture coefficients, leakage and column-spread injection.
No own difference exists at a non-arrival time. The conservative accumulated
error pieces at n0 are:

| Piece | Upper bound, before final query amplification |
|---|---:|
| Initial non-spike difference | .000426 |
| All arrival bus errors | 459.357917 |
| Changed capture coefficients | .000000286 |
| Front/broadcast leakage | 129.400001 |
| Other non-spike bus leakage | .066731 |
| Near-arrival own leakage | 182.446951 |
| Changed-gate full-content leakage | 246.850590 |
| Column-spread injection | .251736 |

Using the exact combined expression rather than individually rounded table
entries gives `E_Y <=1018.374346201866 <1019`. Every contribution is bounded
with worst-case alignment over all `<=k/2` steps. There is no cancellation
assumption about the errors.

The uniform query gives

```
Gamma = a HI sqrt(k) Delta Y_T(d-1),
||Gamma|| >= .11791 n - HI*1019 sqrt(n/2)
          >= .11790944 n > 2.0826 tau.
```

The error/n bound is `5.530294646947e-7` at n0 and decreases as n grows. The
rounded `.11790n` lower bound also holds, subject to the ratio correction in finding 2.

Every final standard-coordinate own profile agrees. Source and row-0 credit
differences vanish for R0. Therefore the entire selected-group Gamma is exactly
the bus readout that B bounds, not merely a large component of total credit
mistakenly attributed to the bus.

This establishes the R0 counterexample for every qualifying n. It does not
establish the dense actual-input transfer discussed in finding 1.

## 6. Independent CPU checks and reproducibility

Run from this directory with Python 3.11+, numpy and mpmath:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -I check_certificate.py
python -I check_intervals.py
python -I check_dynamics.py
python -I check_scope.py
```

`check_scope.py` also verifies the local pinned worktrees and byte-identical
author-script copies; its path constants are environment-specific. The other
three scripts are self-contained and portable. No independent implementation
imports an author module.

- `certificate_results.json`: exact rational supersolution, matrix, slacks,
  weighted matrix norm, independently reconstructed scalar constants.
- `interval_results.json`: outward-rounded 60-digit enclosures, with an explicit
  geometric tail for the 20000-step scalar comparison sequence.
- `dynamics_results.json`: eight dense-matrix simulations at n=192,256,384,512;
  different widths, tails, interior antipodes, reversed signs, and amplitudes.
- `scope_and_provenance.json`: exact support argument, source hashes, target
  worktree checks, and comparison-run records.

The independent simulations explicitly form U P U, rather than using the author's
fast O application. They verify the exact row/broadcast identities, the leading
arrival columns, own-difference support, raw-input realization, final own-profile
equality, query identity and complete spike decomposition. Maximum absolute
residuals were below 4.4e-12; leading arrival columns agreed within 9.5e-16.
Endpoint discrepancies were at floating-point roundoff. Exact equality is proved
by balance and induction above, not by these residuals.

All six inequalities hold with independently measured small-n constants. The
maximum LHS/RHS was below .66. These runs do **not** use theorem-scale bath
constants at small n and do **not** extrapolate the finite-size signal to n0.
The amplitude-.49 stress case has an input .502714, outside the legal cube;
it is labeled an algebraic stress test, not a legal counterexample. The .45
runs remain below .463. The sign reversal and interior theta tests preserve
the schedule's balance.

The author's scripts were separately run from `author_comparison/`:

```powershell
python -I constants_check.py
python -I exp_identities_u.py
python -I exp_error_bounds.py 512 1024
python -I exp_spike_decomposition.py 512 1024
python -I exp_drift_capture.py 4096:16
```

Their constant assertions and reported inequalities passed. The drift run gave
`Gamma/tau=.0585939805`, endpoint error `<1.9e-16`, and no changed gate on a final
own path. This supports exact mechanics, not a theorem-scale refutation. The
two-arrival schedule discrepancy remains documented rather than silently fixed.

Meaningful compute consisted of small CPU matrix recurrences, scalar interval
iterations, and a 6-by-6 rational solve; no large-n state was allocated. The
independent scripts take seconds on this machine, and the comparison runs took
under a minute with one BLAS thread.

## 7. Research implications and next action

The first next action is **scope repair**, not a declaration that the original
frozen dense problem has been resolved. Preserve the valid R0 result and its
new coupled error proof. Then either explicitly state that B is being tested
over the enlarged norm-ball class, or construct sparse actual inputs for the
prescribed dense R while proving an exact common endpoint and listing zero.
For the rank-one dense completion, balanced modulation may help because its
state differences can annihilate the rank-one perturbation. Autonomous baseline
trajectories would still change; their effect on source amplitudes, gates,
credit and the final zero must be proved. The dense inverse lift is not a
support-preserving solution. This audit does not supply that new construction.

Once the scope is explicit, the R0 result does justify examining **dimension**
rather than asserting a uniformly small bus magnitude. The family has one
parameter and a large coherent aggregate. Its signal norm is not a lower bound
on robust memory dimension. A one-coordinate listing can already separate
the two boundary parameters of a one-dimensional ball.

Lemma M remains OPEN. A useful next bounded investigation is to characterize
the query-visible aggregate

```
sum_t rho_t kap_t O_(t-1)(d-1,:)
```

for a public spike schedule, and ask for a continuous odd low-support listing
whose zero controls the residual under every legal query. Any eventual general
argument must also control full-content leakage when m is comparable to or
larger than sqrt(n), code-dependent schedules, and undriven near-neutral paths.
The present construction does not test those issues. No proof of Lemma M is
attempted here.

Finally, “no magnitude bound can rescue the route” is too broad. What the R0
counterexample defeats is the universal tau/4 bound at **every** listing zero
in the class containing this D=1 section. It does not refute a dimension-qualified
bound, an existence-of-a-good-zero statement for sufficiently large D, or a
bound for a narrower dense-R class. Such statements would need their own proof.

**TL;DR:** the repaired six-inequality error analysis passes, and the R0 bus signal
is rigorously large. Several prose/numerical statements need small corrections.
The unchanged frozen dense-family / actual-support transfer has not been proved.
Resolve that scope issue before labeling B refuted under the original contract.
The original n^(3/2) question, Lemma M and the logarithmic-loss question remain OPEN.
