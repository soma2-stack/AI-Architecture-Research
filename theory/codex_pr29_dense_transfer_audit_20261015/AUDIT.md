# Independent final dense-transfer audit

Audited PR #29 at **2e46b02d61b8b2cc713546461d1232b578690b8f**, especially
PROOF.md section 2.4. Foundations checked against PR #27 c987408, PR #28
0cc0a23, CURRENT_THEORY.md, the original quadratic proof section 7, and
reachable_fixed_feature_width_20261002 section 2. Date: 2026-10-15.

## Verdict

**Theorem R_D: INCOMPLETE as literally stated. Its core counterexample to the
original selected-group Hypothesis B is independently PROVED.**

The new argument closes the earlier prescribed-matrix and actual-support gaps.
The original Hypothesis B of PR #28, whose listing has items (i)–(v), is therefore
**REFUTED under the original prescribed dense matrix**. This conclusion does not
require the additional assertion about the full-group listing introduced in
PR #29 Proposition 0.2.

The parenthetical claim that this same pair is also a zero of that **extended**
listing is not proved. It concerns an actual gradient scalar, not a state scalar.
The proof conflates them. An independent high-precision scaled construction has
a nonzero added scalar, and an exact short-history example disproves the inference
used to declare it zero. I have not established a theorem-scale counterexample to
that extra property; thus the literal theorem receives INCOMPLETE, not REFUTED.
Removing this optional assertion gives a proved dense counterexample to original B.

The displayed rounding implication `.11790 n >= 2.0826 tau` is also false, but
the stronger available bound proves the intended numerical conclusion.

| Item | Verdict |
|---|---|
| D1: identification of the prescribed matrix | **PROVED**, with a harmless n=8,9 endpoint correction to a strict inequality |
| D2: shared field and exact cancellation | **PROVED** |
| D3: actual support, state endpoint, continuity | **PROVED**, with the inherited time-1 exceptions stated explicitly |
| Transfer of Lemma E for selected reference credit | **PROVED** |
| Original listing (i)–(v) zero | **PROVED** |
| Added actual-credit scalar in Proposition 0.2 | **INCOMPLETE**; state equality does not prove credit equality |
| Theorem R_D literally including that extension | **INCOMPLETE** |
| R_D restricted to original Hypothesis B | **PROVED** |
| Original Hypothesis B, prescribed dense matrix and actual support | **REFUTED** |
| Original D=Omega(n), full-metric strict n^(3/2) question | **OPEN** |

No target PR, restricted notebook or AGENTS.md was modified. This directory is
the independent record. CPU only; no training, GPU, merge, outside contact or
Lemma M research.

## 1. Serious findings and exact corrections

### P1: equality of states does not make the extra actual-credit scalar zero

PROOF.md lines 829–830 and 845–849 include Proposition 0.2's extended listing
in the exact-zero claim. That proposition adds the odd part of the **actual full
fixed-feature** scalar B_T(0,0), for direction e0 f_s^T. It is not the redundant
zero column of the selected group E=diag(0,1,...,1).

Let b_t be that full-group column and H=R-R0. The exact recurrence is

```
b_t = G_t (R b_(t-1) + c_t e0),
b_t(0) = g_0(t) [(alpha a+alpha eta/n)b_(t-1)(0)
                +(alpha eta/n) sum_(j>=1)b_(t-1)(j)+c_t].
```

Although g_0 and c_t are common, this gives

```
Delta b_t(0) = g_0(t) [(alpha a+alpha eta/n) Delta b_(t-1)(0)
                    +(alpha eta/n) sum_(j>=1) Delta b_(t-1)(j)].       (1)
```

The last term is omitted in the listing-zero reasoning. Zero-sum **state**
differences do not imply zero-sum **credit** differences: paired +z and -z
states have the same gate, and their changed-gate credit terms can add.

An exact counterexample to that inference works at arbitrarily large n. Take
two autonomous initial steps, then change two off-cycle memory states at time 3
to a balanced pair, and reset both to the public autonomous endpoint at time 4.
Use sufficiently small amplitude so the four sparse controls are legal. The
dense field is common and all endpoint states coincide exactly. Since c1=0,

```
b_2 = c_2 g_0(2) e0.
```

If one boundary history uses gates g_mod<1 at the two time-3 modulated rows
and the other uses gate 1, then only those two rows of b3 differ. Consequently

```
Delta b_4(0)
 = -2 g_0(4) (alpha eta/n)^2 c_2 g_0(2) (1-g_mod) < 0.             (2)
```

This is exact for every eta>0. It is a counterexample to “common states imply
common B00”, not to the original listing theorem: this short example does not
claim its final own-profile listing is zero.

My independent implementation of the *written long schedule*, scaled to
n=256, ell=16, tail=12, uses the actual prescribed eta=1/(10^8 n^2) and alpha
from an independent 3-by-3 singular-value reduction. It gives

```
Delta B_T(0,0) = 2.328375735057197378166837627572288...e-31.
```

The value agrees at 80 and 110 decimal digits. In contrast, state endpoint
differences fall from about 3e-81 to 2e-111 as precision rises. Thus the credit
defect is not an endpoint roundoff artifact. These finite sizes are below the
theorem range; I do not promote this to a theorem-scale counterexample.

**Smallest correction:** remove “and of its Prop. 0.2 extension” and item (vi)
from this counterexample's zero claim. The original Hypothesis B uses only
items (i)–(v), and its refutation survives. Proving an exact zero of the added
credit scalar would require a further argument or altered section. No such
argument is needed to refute the original selected-group B.

### P2: the false rounding implication remains

PROOF.md line 833 still writes `.11790 n >= 2.0826 tau`. Put s=tanh(.05).
The prescribed normalization uses the original sigma, satisfying

```
s <= sigma <= s/(1-lambda),
tau/n = .002 sqrt(2)/sigma.
```

Therefore the ratio of .11790n to tau is asymptotically 2.08246214159..., and
even its upper bound using sigma<=s/(1-lambda) is below 2.0826 in this range.

The available **stronger** dense bound is

```
||Gamma_bus||/n >= .11791 -(1+1e-40) HI*1019/sqrt(2*n)
                 > .11790944697053530    at n>=1.5e18.
```

Its ratio to tau exceeds 2.08262900298. State this bound before rounding,
or replace the rounded implication by `.11790n > 2.082tau`.
The desired separation is established; the displayed chain is incorrect.

### P2: actual support and reference support still do not agree

PROOF.md lines 100–102 claim the readings now agree. The dense construction
correctly makes actual inputs zero off its driven set. But along its changed
dense trajectory

```
x_ref = x_actual + (R-R0) h_prev.
```

At time 2, h1=s*1 and actual input is zero everywhere. Each source coordinate
of the reference input equals

```
s [alpha eta -(1-alpha)lambda]
 >= s eta(a-lambda)/(a+eta) > 0.
```

So reference support contains all n/2 source rows, while actual support there
is zero. The new theorem's actual-support argument is valid precisely because
it does not need a reference-support identification. Delete the claimed equality.

### P3: initialization and small-n wording

D1's proof uses `1<gamma<2<k` for n>=8. At n=8,9, k=4 and gamma=2. Use
`1<gamma<=2<k`; all required inverse-image entries remain nonzero.

D3(c)'s small beta and large front-preactivation ranges apply at **t>=2**.
At t=1 beta=.05, front preactivation=.05 and c1=0. The transferred Lemma E
handles this correctly because its first incoming credit is zero. The exception
should be stated in D3 rather than left implicit.

## 2. D1: the matrix is exactly the prescribed one

The original recipe picks the first admissible integer power base separately
for the two vectors. With q_k=1/sqrt(k), gamma=1/(1-q_k), w=e0-q_k*1,

```
O^T 1_k = sqrt(k)e_(d-1)+gamma w,
O   1_k = sqrt(k)e_1    +gamma w,

R0^-1 1_n = (O^T 1_k/a, 1_l/lambda),
1_n^T R0^-1 = ((O 1_k)^T/a, 1_l^T/lambda).
```

The memory entries are 1 at index 0, (k-gamma)/sqrt(k) at the exceptional
index, and -gamma/sqrt(k) elsewhere. For k>=4 none is zero. Thus t=1 really
is the first admissible integer in both selections, not a convenient replacement.
The normalized rank-one matrix is exactly C=1_n1_n^T/n.

The original finite-root argument then guarantees the selected positive eta_j
has both B=R0+eta_j C and B^-1 entrywise nonzero. Independently, in the theorem
range even j=0 works. For k>=7.5e17 the nonzero memory entries of O have magnitude
at least 1/k; the formulas follow by applying O to coordinate vectors. Their
signs cannot be canceled by eta/n. Memory inverse entries have magnitude at
least 1/(ak), while the Sherman–Morrison correction is at most

```
eta*k/(n*a^2) < 1/(ak).
```

Here the correction denominator is particularly simple:

```
1 + (eta/n) 1^T R0^-1 1 = 1 + eta*l/(n*lambda) > 1,
```

because the memory sum is zero. Base-zero inverse entries become nonzero
since both inverse-image factors are nonzero. Source diagonals remain positive:
the correction is bounded by eta/(n*lambda^2)<1/lambda. Scaling by positive
alpha preserves density and dense inverse. The prescribed first eta therefore
does not introduce an extra assumption.

For normalization, let p be the memory restriction of 1_n/sqrt(n), extended
by zero, and r=O^T p on that block. Then p^T r=0, since
1_k^T O 1_k=k e0^T P e0=0 for d>=2. The unit vector proportional to p+r gives

```
||(R0+eta C)x||^2 > a^2.
```

The cross term is strictly positive, and ||R0x||=a. Thus

```
a < ||R0+eta C|| <= a+eta,
1-2eta <= a/(a+eta) <= alpha < 1,
||R-R0|| <= (1-alpha)a+alpha eta <= 2eta <= 4eta.
```

All parameter entries are differentiated independently. The recipe defines
the frozen base values; its alpha and rank-one form do not constrain the
parameter directions used in the credit recurrence.

## 3. D2–D3: exact state cancellation and actual inputs

For every h,

```
Rh = alpha R0h + (alpha eta/n)(1^T h)1.
```

At each time every modulation has an opposite companion. For any two parameter
values their state difference has zero total sum, zero row 0 and source
coordinates, and zero coordinate d-1. On that subspace U acts trivially both
before and after P, so R Delta h=alpha a P Delta h. Its nonzero positions are
only successors of modulated rows; those successors are driven, including the
resets. All other preactivations therefore coincide. This proves the induction
from zero through preparation, arrivals, hold and tail, for all theta in [-1,1].
The shared field is independent of theta even though it changes absolute
trajectories. There is no accumulated tiny state mismatch hidden in this equality.

Define actual inputs by

```
x_t(i) = atanh(target_t(i)) -(Rh_(t-1)+b)_i   on S_t,
x_t(i) = 0                                 off S_t.
```

This is an exact definition, not a numerical threshold. There are at most ell
arrival diagonals in flight and one spike, hence actual peak support<=120001.
Targets and controls are continuous; a modulated state changes strictly with
theta, proving injectivity. All modulation is reset before the final window,
so the common endpoint is exact for every parameter value.

The forward coefficients are a'=alpha a and lambda'=alpha lambda, with a
common field bounded by eta. Writing the original mass M relative to the
memory bath s gives

```
beta'_t = .05-s_prev+epsilon'_t,
epsilon'_t = (1-a')s_prev
             +a' gamma/sqrt(k) [h_prev(d-1)-2s_prev]
             -a' gamma^2 M_prev/k + phi_t.
```

Compared with the old bootstrap its extra bound is at most 3eta. The independent
interval bound at n0 is |epsilon'|<1.270083e-9<1.4e-9; the old bath interval,
front-chain comparison, gate sums, and input-amplitude slack all survive.
Using a'<=1 strengthens the front-excess upper comparison. The front lower
bound survives alpha>=1-2eta with substantial slack. Every input is below
.4732+1e-40<.5, including starts, modulation transitions and resets.

The source is common across parameters. If sigma is the original fixed point,
the upper comparison fixed point with bias .05+eta satisfies

```
sigma_plus-sigma <= eta/(1-lambda) <= 1.01eta,
c_t <= 1+1.01eta/sigma < 1+1e-40.
```

For the lower bound, t>=1 source states are at least tanh(.05-eta), while
sigma<=tanh(.05)/(1-lambda). Hence c_t>=1-lambda-eta/tanh(.05)>1-1e-12 for
t>=2. At t=1, c1=0. This supplies the lower estimate that D3 only asserts.

The complete horizon and peak resource are unchanged. At n0,
T=375000000000599046 and mT/n<=30000.250000047925. Smooth ceiling envelopes
give the same budget for all larger qualifying n. No preparation, reset, or
tail step is omitted.

## 4. Credit transfer, query and numerical bounds

The distinction between forward dynamics and reference credit is essential:

```
forward:          h_t=tanh(Rh_prev+x_t+b),          a'=alpha a,
reference credit: B'_t=G_t(R0 B'_(t-1)+c_t E),      transport coefficient a,
actual credit:    B_t =G_t(R  B_(t-1)+c_t E),       ||R||op=a.
```

Thus using the original a in Lemma E is correct. It is the coefficient of
B', which is exactly the reference object appearing in original B. It is not
an unacknowledged replacement of the forward coefficient a'.

Actual gates still have all the properties used in the independent E proof:
exact hole/modulation gates, zero off-cycle deviations from the common bath,
the same bath/front bounds, and common c_t. Scaling the injection-linear
majorant by cmax scales all own norms, its supersolution and E_Y; no new
transport term appears in B'. The earlier rational certificate is preserved.

At the final time, every reference own profile agrees: no modulated point
can lie on a final local path, and the common source sequence weights both
profiles equally. Source-row reference credit differences are zero. Hence
the uniform one-step R0 query reads exactly the selected-group bus:

```
Gamma_bus = a HI sqrt(k) Delta(UB'_T)(d-1,:).
```

This is not an identification of the entire actual dense gradient with bus
content. For D_t=B_t-B'_t, with actual gates held the same,

```
D_t=G_t[R D_(t-1)+(R-R0)B'_(t-1)],
||B'_t||F <= cmax sqrt(n)/(1-a) = cmax n^(3/2),
||D_T||F <= ||R-R0|| cmax n^(5/2) <=4e-8 cmax sqrt(n).
```

These follow from geometric sums for every finite horizon. Antipodal
subtraction supplies the factor 2. The actual one-step weights obey

```
||nu_R||<=sqrt(n),
||nu_R-nu|| <= ||R-R0|| HI sqrt(n),
||nu_R^T Delta D_T|| <=8.1e-8 n,
||(nu_R-nu)^T Delta B'_T|| <1e-7.
```

The final independent interval lower bounds are

```
bus/n    > .11790944697053530,
actual/n > .11790936597053530,
bus/tau  > 2.08262900298,
.11789n/tau > 2.08228551206.
```

The bus error fraction decreases with n; the dense-credit error fraction has
a uniform upper bound. Eta and the source excess also decrease.
These bounds cover the minimum n and the asymptotic regime. They use the
previous independently verified E_Y<1019, not extrapolation of small-n runs.

For original listing items (i)–(iii), window inputs/states, J, Sum', c and
the t0 states all agree. For (iv)–(v), every odd own profile at T vanishes;
arbitrary even soft weights and block projections preserve zero. The added
actual-credit scalar is the separate unresolved assertion described in (1).

The actual future input `.25*1-Rh_T-b` is common and realizes gates HI. It
is frozen when differentiating. Its legal preactivation contract is satisfied;
it is not subject to the past input-cube bound. Normalization stays exactly
sigma sqrt(l)/(n sqrt(n)); sigma is not silently replaced by the new source
trajectory or its comparison fixed point.

D=1 is permitted: B is asserted at every zero of the original listing,
and this is an explicitly exhibited zero. The resource corollary's
2N3<=D<=n restriction is not part of B's listing domain. The actual selected
pair distance exceeds 2epsilon, so this is a robust one-dimensional section.
Projection into the original larger gradient metric preserves this positive
separation, without supplying a large-dimensional section or any obstruction
for that full metric.

## 5. Independent checks and reproduction

Run in this directory:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -I check_matrix.py
python -I check_transfer_bounds.py
python -I check_dense.py
```

- `check_matrix.py`: exact Fractions at n=8,9,18,32,50,72, direct U P U,
  inverse-image formulas, first eta density and Sherman–Morrison inverse.
- `check_transfer_bounds.py`: outward-rounded 70-digit intervals for the
  dense bath/source shifts, errors, final constants and false rounding chain.
  It reuses only the previous **independent** rational E certificate, not an
  author module. Its location is the adjacent prior audit directory.
- `check_dense.py`: independent reflection/permutation implementation, exact
  prescribed alpha reduced to a 3-by-3 eigenproblem, actual sparse controls,
  state comparisons and the omitted full-group column at 80 and 110 digits.

For the alpha reduction, let f=k/n, g=l/n. On orthonormal memory-mean,
rotated-memory-mean and source-mean axes, B^T B is exactly

```
diag(a^2,a^2,lambda^2) + eta(r q^T+q r^T)+eta^2 q q^T,
q=(sqrt(f),0,sqrt(g)), r=(0,a sqrt(f),lambda sqrt(g)).
```

Its largest eigenvalue gives the actual alpha. Remaining singular values
are a or lambda; the displayed largest eigenvalue exceeds a^2. No convenient
approximate alpha is substituted in the positive cases.

For an adversarial right factor, changing one weight at a modulated coordinate
produces an endpoint defect about 1.61887e-16 already with contract-sized eta
at n=256. It is outside the prescribed matrix class, and is an expected failure
of cancellation, not a counterexample to R_D. The prescribed uniform factor
has endpoint differences at the working-precision floor; exact equality is
proved by induction, never inferred from those residuals.

Author `exp_dense_transfer.py` and `constants_check.py` were separately run
from byte-identical copies in `author_comparison/`; their outputs passed.
Their scaled schedule still uses two additional arrivals compared with the
written construction. My independent schedule uses the proof's endpoint.

Results: `matrix_results.json`, `transfer_bound_results.json`,
`dense_results.json`. Exact identities and rational sign checks are distinct
from outward interval certificates and finite numerical evidence. The scaled
B00 test is evidence of the omitted feedback, not a theorem-scale disproof
of the long schedule's added zero claim.

## 6. Research handoff

The smallest outstanding correction is editorial/mathematical scope: retain
the proved original Hypothesis B refutation, remove the unsupported assertion
about Proposition 0.2's extra actual-credit scalar, fix the ratio chain, and
state the time-1 exceptions and distinct input supports correctly.

If the stronger extended-listing zero is desired, equation (1) is the exact
missing condition. It needs an actual proof or a modified balanced section;
state balance alone cannot provide it. That work is optional for refuting
original B.

After these corrections, the appropriate next research question concerns
robust bus dimension. This audit does not begin Lemma M research. A large
D=1 coherent signal leaves the D=Omega(n), full-metric n^(3/2) question OPEN.
The logarithmic loss and the neutral-path cost issue remain separate and OPEN.
