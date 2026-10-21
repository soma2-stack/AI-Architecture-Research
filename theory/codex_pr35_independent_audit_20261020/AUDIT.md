# Independent adversarial audit of PR #35

Auditor: Codex. Date: **2026-10-20**. No subagents used.

Target: [PR #35](https://github.com/soma2-stack/AI-Architecture-Research/pull/35), immutable commit
**`b984ef9347219d62db4dfd39f8f2e263317c9a33`**.

## Executive verdict

**The principal dense-transfer and cube-root theorems survive independent review.**
Theorem 6.1D, Corollary 6.2D, Lemma 9.1, Theorem 9.2 and Corollaries 9.3–9.4 are
**PROVED in their stated mathematical scopes**, with the qualifications below concerning
sharpness and exact-real coding. No fatal error in either principal construction was found.

There are **demonstrably false auxiliary statements**: Proposition 7.2 equates a scheduled
support envelope with actual support, its arbitrary-alpha wording does not justify the
quantitative perturbation bound it invokes, and the prose overextends gate/range facts to
arbitrary eta. These require correction. The principal proofs also explicitly invoke the
separately verified lemmas under the prescribed matrix, so they do not depend on those
overextensions. A downward-rounded certificate summary should be corrected as well.

The strongest defensible result is an exact-real, continuous antipodal robust family for
both R0 and the **prescribed** dense matrix, with

```
D = floor(floor(n^(1/3))/2400),  m <= 3,  T=n/2,  mT <=1.5n,
4 divides n,  n>=10^16.
```

Its selected, full fixed-feature, and full group-RMS gradient pair distances exceed the
required threshold. Original Lemma M is refuted for this dense contract, including the
combined state-plus-bus listing. The original **D=Omega(n) at mT=o(n^(3/2))** problem
remains **OPEN**. Practical finite-precision memory is not established.

## Status table

| Claim | Verdict | Basis / qualification |
|---|---|---|
| Exact prescribed all-ones perturbation and normalization | **PROVED** | Independent inverse-vector and normalization calculation, section 2 |
| Lemma 2.1D: locality/endpoints | **PROVED** | Exact zero-sum induction, all pulse/reset/parking transitions |
| Lemmas 2.2D–2.3D: support, legality, bath/front | **PROVED for prescribed coupling** | Common field, source comparison and same gap bounds |
| Lemma 3.1D, G1–G8 | **PROVED** | The skeleton credit uses a, while forward comparisons use a'=alpha a |
| Lemma 3.2D | **PROVED for prescribed normalization** | Same-gate recurrence subtraction and geometric credit bound |
| Theorem 6.1D / Corollary 6.2D | **PROVED** | Dense errors sublinear; combined listing count unchanged |
| Proposition 5.1, lower transfer to full metrics | **PROVED** | Same units, orthonormal projection, frozen normalization |
| Proposition 6.1, one-step generic merging | **PROVED under common support-envelope hypothesis** | Rank argument; not a multi-step obstruction |
| Proposition 7.2, structural induction | **PROVED with support <= envelope** | Same locality induction |
| Proposition 7.2, actual-support equality | **REFUTED as written** | Add a redundant bath target; same actual inputs, larger envelope |
| Arbitrary-alpha use of the 3 eta perturbation estimate | **REFUTED** | alpha=.6, eta=0 gives nonzero D3 but a claimed zero bound |
| General quantitative transfer beyond prescribed normalization | **OPEN as stated** | Its proof lacks the normalization/perturbation hypotheses; not used here |
| Lemma 9.1, saturation guarantee | **PROVED** | Full-spark singular-value contradiction |
| Theorem 9.2 | **PROVED under exact-real continuous-antipodal contract** | Fresh universal rational certificate, all phases fit |
| Corollary 9.3 | **PROVED** | Exact combined counts at 10^63 and10^78 |
| Corollary 9.4 | **PROVED at m=3,T=n/2, for the first-order listing task** | Borsuk–Ulam plus imported scoped listing upper bound |
| General-width / arbitrary-budget sharpness extrapolation | **OPEN** | Concurrent-pair interference is not proved |
| Injectivity of clipped code as a global chart | **REFUTED if asserted** | Explicit two-point collision; not required by robust antipodal contract |
| Practical finite-precision implementation | **OPEN** | Already D=89 forces code gain >10^50 |
| Original linear-memory strict-budget question | **OPEN** | Cube-root dimension is sublinear |

## 1. Evidence, source coverage and reproduction

The full [PROOF.md](sources/theory/claude_dense_transfer_20261020/PROOF.md),
[REPORT.md](sources/theory/claude_dense_transfer_20261020/REPORT.md),
[CHECKS.md](sources/theory/claude_dense_transfer_20261020/CHECKS.md), certificates, helper and
verification scripts, and numerical records were inspected. Supporting contracts were
checked in PRs #28, #29, #31, #32 and the PR34 files inherited at this commit.
The 67 immutable snapshots are recorded in [source_manifest.json](source_manifest.json).
PR29's proof is pinned at `2e46b02d61b8b2cc713546461d1232b578690b8f`; PR28's at
`0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88`. Their quantitative conclusions are not assumed
merely because they bear previous review labels.

New independent scripts, with **no imports from author or earlier audit modules**:

* [independent_certificate.py](independent_certificate.py): reconstructs the second-order
  carrier system, single-monomial rational majorants, floors, fit, dense errors and robustness.
* [independent_code.py](independent_code.py): full-spark determinants, 90-digit saturation
  checks and an exact conditioning lower bound at D=89.
* [independent_dense.py](independent_dense.py): explicit dense dynamics, integer-exact
  Householder orthogonality, high-precision normalization, full backpropagation and
  counterexamples to auxiliary generalizations.
* [independent_counts.py](independent_counts.py): independent combined listing polynomial,
  threshold certificates and symbolic support/noninjectivity counterexamples.

Run from this directory:

```
python -I independent_certificate.py
python -I independent_code.py
python -I independent_dense.py
python -I independent_counts.py
```

Author scripts were separately run from the sibling folders under `author_runs/`, preserving
relative imports without touching originals:

```
python -I author_runs/claude_dense_transfer_20261020/skeleton_certificate.py
python -I author_runs/claude_dense_transfer_20261020/constants_dense.py
python -I author_runs/claude_dense_transfer_20261020/count_skeleton.py
python -I author_runs/claude_dense_transfer_20261020/exp_skeleton.py 1024 50 2
python -I author_runs/claude_lemma_m_three_memory_20261019/envelope_certificate.py
```

The large stored simulations and the 256-dimensional multiprecision matrix run were inspected
but not repeated. New CPU checks were small and targeted. No training or GPU computation.

## 2. Prescribed matrix: independent all-n identification

The original recipe in `gamma_c_over_n_quadratic_20261001/PROOF.md` section7 chooses the
first admissible power vectors, then the first admissible eta_j, and rescales by operator norm.
It does not permit choosing a convenient replacement dense matrix.

Let beta=1/sqrt(k), gamma=1/(1-beta). From U1=sqrt(k)e0 and the cycle orientation,

```
R0^-1 1 = ((sqrt(k)e_(d-1)+gamma w)/a,  1_source/lam),
1^T R0^-1 = ((sqrt(k)e_1+gamma w)^T/a,  1_source^T/lam).
```

Memory entries are `1/a` at row0, `(sqrt(k)-gamma/sqrt(k))/a` at the distinguished row,
and `-gamma/(a sqrt(k))` otherwise. Source entries are100n. All are nonzero in the
theorem's entire domain. Therefore the first admissible power base is **t=1** for both
vectors, giving exactly C=11^T/n.

The original finite avoidance argument suffices to establish an admissible j. One can
also check directly that j=0 works throughout n>=200 here. With k>=100, every nonzero
entry of O has magnitude at least gamma^2/k: the remaining small positive coefficient
is `gamma/sqrt(k)-gamma^2/k`, which is at least gamma^2/k when sqrt(k)>=3.
Thus no old negative matrix entry is cancelled by eta/n. All old zero entries become
nonzero. For the inverse, write u=R0^-1 1 and v^T=1^T R0^-1. Then

```
B^-1=R0^-1 -(eta/n) u v^T /[1+(eta/n)1^T R0^-1 1].
```

The memory contribution to the denominator's sum is zero, and its source contribution
is50n^2. The denominator is therefore positive and greater than1.
Also max|u_i|,max|v_j|<=100n. Each inverse correction has magnitude

```
<= (eta/n)(100n)^2 <= 10^-4/n,
```

whereas every old nonzero inverse entry has magnitude at least2/n. No such entry vanishes;
old inverse zeros become nonzero because u_i v_j never vanishes. This verifies the actual
first-candidate recipe, rather than only a different member of the perturbation family.

Finally `B e0=a e0+(eta/n)1`, so ||B||>a for eta>0. With ||B||<=a+eta,

```
alpha=a/||B|| in [1-2eta,1),  ||R||=a,
R-R0=(alpha-1)R0+alpha eta qq^T,
||R-R0||<=3eta,  q=1/sqrt(n).
```

The prescribed eta is positive and <=10^-8/n^2. All forward and credit derivatives concern
independent entries of this fixed R; alpha is not redifferentiated as a function of R.

For the independent n=512 check, sqrt(k)=16 makes U and O rational. An integer expansion
checks `Oint*Oint^T=3600^2 I` exactly. Operator normalization was computed at80 digits
using the three-dimensional invariant space of B^T B spanned by uniform memory, its
O^T image, and uniform source. Its matrix is

```
diag(a^2,a^2,lam^2)
 +eta/2 * [[0,a,lam],[a,0,a],[lam,a,2lam]]
 +eta^2/2 * [[1,0,1],[0,0,0],[1,0,1]].
```

This avoids trying to infer contract-size normalization corrections from an ordinary
double-precision SVD. The resulting alpha is `.99999999999999044459...` and all dense
entries are nonzero. These numerical values support, but do not replace, the all-n algebra.

## 3. Exact locality, sparse actual inputs, and G1–G8

### 3.1 All transitions

The identity

```
Rh=alpha R0 h +(alpha eta/n)(1^T h)1
```

is exact. At a pulse, the two changed off-cycle coordinates have opposite state differences;
their sum is zero. Since they are off cycle and have no arrival coordinate, J(Delta h)=0.
Thus `R Delta h=alpha a Delta h`, supported on that same pair.

On pulse continuation the pair is driven again. Immediately after its seventh pulse
step it is reset to zero. It remains common through the rest of its hold, is parked at
the common bath, and is never reused. The next pair starts one time step after parking.
Induction covers preparation, first pulse, pulse continuation, reset, parking, transitions
between memories and the final tail. Undriven memory/source rows see identical fields.
The endpoint equality is mathematical equality, not a tolerance-based conclusion.

Inputs are defined **only** on the driven rows by
`atanh(target)-(R hprev+b)`. Undriven rows take their autonomous next state and actual
input zero. A dense *reference* correction is neither used nor counted. At most one
spike and one pair are controlled, so actual support is at most3 at every time and every
parameter. The full preparation and final tail are included in T=n/2.

### 3.2 Which state estimates need small coupling

Exact locality and endpoint equality do not need small eta. The *range, gate, source
and credit bounds do*. For the prescribed eta and alpha, the forward recurrence is the
same scalar skeleton with a'=alpha a and common bias `.05+phi_t`, |phi_t|<=eta.

The bath and above-bath comparisons use a'<=a<=1. A direct schedule-specific bootstrap
can be used: at one time there is at most one free front row of each age, and the
excess over the bath is bounded by the geometric sum Q=1600. Hence
`(k-4)s<=sp<=(k-1)s+1600`. With the common bias changed by at most eta, the bath
preactivation remains near .05, inside the bounds required for [.025,.1009].

Row1's bound differs from PR34 by at most
`2eta*.025 sqrt(k)+eta`. At n>=10^8 this, together with the old errors, is below .001;
the eta*sqrt(k) term decreases as n^(-3/2), so it is not frozen at its n=10^8 eta and
then incorrectly allowed to grow. The same n-dependent front gate follows.

The undriven source differs from its R0 scalar trajectory by at most
`[eta+(1-alpha)lam]/(1-lam)`, which gives at most21eta after division by sigma.
Thus c1=0 and `.99<=c_t<=1+10^-12` from time2. It remains common between all coded
histories. Monotonicity of the actual dense source is not required or assumed.

Input legality follows from the bath identity
`a'J+.05+phi=atanh(s_t)-a's_(t-1)` and the same gap comparison. Spike start uses
age17 and the bound .3831; first pulse uses .38+.0763=.4563. Resets and parking
obey their smaller bounds. These controls are strictly inside the past-input cube.

### 3.3 Gate-fact audit

| Fact | Independent justification |
|---|---|
| G1 | Zero-sum locality above; differences only in the current pulse pair |
| G2 | Spike state exactly0, so gate exactly1 |
| G3 | Targets give hold1/pulse1-v^2; parking at bath gives delta0 |
| G4 | Free chains stay above bath; never-held/parked off-cycle rows equal bath |
| G5 | Dense front estimate with a' and tiny common bias; time1 birth exception retained |
| G6 | Dense bath bootstrap; common to all parameters |
| G7 | Gap contraction is no weaker with a'<=a; the full front deviation sum remains <=39.73 |
| G8 | Undriven common source and the contraction comparison above |

The reference **credit** recurrence B' still contains **a**, not a'. This is intentional:
it is defined with R0 and the actual gates. All own/skeleton estimates use a. Only
the forward-state and gate comparisons use a'. No coefficient a has been incorrectly
substituted for a' in the actual dense credit recurrence.

## 4. Dense credit, readout, and full metrics

Subtracting the same-gate recurrences gives, exactly,

```
D_t=G_t[R D_(t-1)+(R-R0)B'_(t-1)],  D_0=0.
```

Since ||R0||=||R||=a and ||G||<=1, each column of B' and B has norm at most
`c_* sum a^j<=c_* n`. Thus

```
||D_T(:,c)|| <= T*3eta*c_* n <=1.5e-8*c_*,  T=n/2.
```

This includes all n state rows, source feedback and row0 leakage. Gate differences
between R0 dynamics and dense dynamics are not discarded: both B and B' here use
the *same actual dense* gates and source credit. Lemma3.1D justifies the subsequent
analysis of those gates.

For nu_R=R^T g and nu=R0^T g,

```
nu_R^T Delta B = nu^T Delta B' +nu^T Delta D +(nu_R-nu)^T Delta B,
||nu_R-nu||<=3eta HI sqrt(n).
```

On q tracked columns, `||Delta D||_F<=3e-8 c_* sqrt(q)` and
`||Delta B||_F<=2c_* n sqrt(q)` (2.1 is a harmless upper relaxation).
For q=D=O(n^(1/4)) these yield the stated3e-9 n^(5/8) bound. For q=r<=n^(1/3)/1200
they yield an independent coefficient below8.30e-10 on n^(2/3), hence below the
printed3e-9 bound. Both errors are sublinear compared with the order-n margin.

The bus used by Lemma M is the **R0-skeleton standard-row bus**, not the entire dense
gradient and not merely transformed Z. The own correction is explicitly subtracted.
It is <=4e3 n^(3/8) for the old construction, and <=20n^(1/3) for the coded one.
The tiny c_* factor is absorbed using a gamma c_*<2. These terms remain below the
available margin uniformly above the stated thresholds.

### Metric derivation

Use the original frozen weights
`w_R=||R||_F/n`, `beta=max(1,||R||_F)`, `q_head=1/sqrt(n)`.
For n in the theorem domain, beta=||R||_F>1. The orthonormal parameter probes are
`e_r f_s^T`, with ||f_s||=1. Frozen-input differentiation gives

```
<Delta grad_R L,e_r f_s^T>
  =(sigma sqrt(l)/(beta sqrt(n))) Delta Bfull_T(:,r)^T nu_R.
```

The direct future injection cancels because the endpoint and source state are common.
Multiplication by w_R gives precisely `sigma sqrt(l)/(n sqrt(n))`, the declared
fixed-feature normalization. Orthogonal projection cannot increase Frobenius norm,
and the full group-RMS vector contains this weighted R block. Lower bounds therefore
transfer to the full fixed-feature and full R/W/b metrics in exactly these units.

For clarity, the fully unmasked credit uses injection I: `Bfull_t=G(R Bfull_prev+c_t I)`.
The selected credit is Bfull*E. Their columns r>=1 agree. Proposition5.1 should use
different symbols when discussing the newly included r=0 direction; a selected-E
column0 is zero and is not that direction's true full credit. This notation does
not impair any lower bound, which restricts to the memory columns r>=1.

This is only a lower-bound implication. An upper bound for selected memory does
not bound either larger metric from above.

Independent n=512 direct-matrix runs gave projection-identity errors below1e-15,
column credit correction below1.34e-10, endpoint residual below1e-15 and support3.
The full R-gradient was computed over independent matrix entries by backpropagation,
not by differentiating the prescribed matrix recipe. These are finite algebra checks,
outside the theorem's bath/dimension regime.

## 5. Saturation code: validity, conditioning and meaning

For any D-row submatrix M_I, singular-value minimality gives
`||M_I theta||>=sigma_min(M_I)` for ||theta||=1. Put
`delta_*=min_I sigma_min(M_I)/sqrt(D)>0`, `L=1/delta_*`.
If D coordinates were strictly unsaturated, each would satisfy |(M theta)_i|<delta_*, so

```
||M_I theta||<sqrt(D)delta_*<=sigma_min(M_I)<=||M_I theta||.
```

This contradiction proves at least r-D+1 exactly saturated coordinates. Equality at
the clipping boundary counts as saturation; strict/weak inequalities are used correctly.
Vandermonde determinants are products of distinct node differences, so every required
submatrix is nonsingular. All matrices/constants are finite for each fixed n.
Clipping is continuous and odd, including at +/-1. No differentiability is needed.

The new amplitudes are dependent across pairs, but that is harmless here. Every pair
still balances its two physical states; all common fields and source states remain
independent of theta. First-order column c depends only on that pair's amplitude.
The interference bounds use absolute pulse sizes Pi(|z_c|), not probabilistic independence
or derivatives with respect to theta. Frozen parameter differentiation does not
differentiate the code M or the input controller.

### The code is not a globally injective chart

For D=2,r=3, nodes(-1,0,1), the defined gain is about2.288245611. The distinct unit
directions `(1,0)` and `(99/101,20/101)` both clip to `(1,1,1)`.
Thus they give the same history. This would refute an *additional* claim of global
injectivity. It does **not** refute the actual continuous-antipodal memory lower bound:
composition with any continuous encoder still gives the required Borsuk–Ulam collision
between theta and -theta. Those antipodes map to opposite codes and have the proved
separation. It should not be described as uniformly separating all distinct directions.

### Exact-real, not practical finite precision

The conditioning is serious already at the minimum claimed dimension D=89. Take the
polynomial with roots at the first D-1 of the 2D-1 equispaced nodes and normalize its
coefficient vector. On the first D rows, all evaluations but the last vanish; the last
node is0. If p0 is its constant coefficient and c its coefficient vector,

```
sigma_min(M_I)<=|p0|/||c||,
L>=sqrt(D)||c||/|p0|>=max_j|c_j|/|p0|>10^50.
```

The last inequality is an exact rational computation in `independent_code.py`.
The minimum is over exponentially many submatrices; computing or representing the
chosen L at scale is not a practical construction supplied by this PR. The theorem
contract has no bound on code Lipschitz constant, public preprocessing cost or
precision in one real input coordinate. Under that contract this is allowed.
It does not establish finite-precision robustness to control/parameter-generation errors.

Finite90-digit checks at D=2,3,4 covered basis directions, singular directions and
directions orthogonal to D-1 selected rows. They reached the minimum predicted saturation
counts2,3,4. Determinant nonvanishing was checked exactly. These finite tests supplement,
not establish, the universal singular-value argument.

## 6. Modified schedule and first-order aggregation

Write N=floor(n^(1/3)), D=floor(N/2400), r=2D-1 and H=250N^2.
Do not confuse the section dimension D with the number r of memory columns/pairs.
The original schedule/lemmas may be used with any number of disjoint sequential pairs
that fits; they do not require amplitudes to lie on S^(r-1). Each z_c lies in[-1,1].

At least j=D pairs saturate. On those columns
`|Delta F1(c)|>=F*Pi(1)`. The Euclidean norm across **orthogonal physical parameter
columns** gives `||Delta F1(C)||>=F*Pi(1)*sqrt(j)`. There is no scalar sign sum that can
cancel, and no Vandermonde condition-number factor belongs in this gradient norm.

For H>=100 there are floor(H/2) pre-pulse hold steps, seven pulse steps and ceil(H/2)-7
post-pulse hold steps. The original sign-coherent first-order proof only needs
`tanh(.38)^2<1/7`, common positive source c_t, and these gate facts. It therefore
applies to each coded pair without modification.

Let y=n^(1/12), y0=21. Then

```
H+1<=250y^8+1,
H>=250y^8(1-y0^-4)^2,
r<=y^4/1200,
D>= (y^4-2401)/2400.
```

The full timing cost satisfies

```
r(H+1)/n +41/n <=250/1200+1/(1200y0^8)+41/y0^12
                         <.208333333334 <1/4.
```

So `r(H+1)<=d-41`, every pair fits, last parking is at most T-2, and both first and
last pulses have all seven steps inside their holds. No extra simultaneous pair is
hidden in the fit. Exact cube-root/floor checks covered n=10^16, cube-boundary and
D-jump neighbors, 10^63,10^78,10^166 and10^1000. The resource is the complete peak
width times horizon, not additive support substituted for that measure.

## 7. Independent second-order and all-size certificate

### Why importing the bound chain is legitimate

The exact difference recursion for one column contains

```
Delta Z_t(r)=a g+_t(r)Delta Zprev(pred r)+kappa+_t(r)Delta A-Delta lambda
 +a Delta g_t(r)Zprev^-(pred r)
 +(gamma/sqrt(k))Delta delta_t(r)A^-
 -(gamma^2/k^(3/2))Delta S_t A^-.
```

The changed gates are confined to14 row-steps per pulse. Reset and parking cause no
new changed-gate source; credit generated earlier persists and is carried by the
homogeneous recursion. The common broadcast coordinate contains the additional
`(gamma/k)Delta S*A^-` term. All these sources remain in the new certificate.

The background arrival bound includes the row1 birth `eps_g Ybar0`. Outside a column's
own window, its own gate deviation is zero; the printed l_out bound retains its
own-window mass L_in on the spike. The eta_oth estimate includes the nonzero birth
mass over another writing window. Parked rows retain credit but have delta0 and are
not reused. These statements depend on window geometry, not on the dimensionality
or statistical independence of the amplitude vector.

The leakage coefficients on (Lambda,Acal), rederived by carrier, are:

| Carrier | On Lambda | On Acal |
|---|---|---|
| row1/broadcast | 1/sqrt(k) | (gamma/k)u1 |
| front forcing | (gamma/k)D_f Q | (gamma/k)D_f Q(gamma/sqrt(k))u1 |
| front births | D_f eps_g/sqrt(k) | (gamma/k)D_f eps_g u1 |
| spike | (gamma/k)s_hi^2 d | same times kappa_s |
| active pairs | (gamma/k)2*xbar*(H+1)*(2+Q/H) | (gamma/k)2*xbar*(H+1)*(kappa_h+kappa_b) |

The `1+Q/H` factor comes from bath contents sampled at pair starts H+1 apart; adding
within-window forcing gives2+Q/H. There is still only one active pair, so no missing
concurrency factor is introduced. Summing gives a_L,a_A. With
`Acal<=b_A(Lambda1+Lambda2+sigma_S)`, solve the resulting two-variable positive feedback
system; its loop gain is e=a_L+a_A b_A. Direct pulse, uniform and broadcast/birth sources
are all kept. The output bound is `Lambda2+kappa_s*Acal+sigma_S`.

For the vector of r columns, the other-pair sum is J_r-I_r, whose norm is r-1<=r.
This is the place where the new **r**, not section dimension D, must appear. The code
sets `Dm` to r and the independent certificate does likewise. The bound
`||Pi||<=||Delta F1||/F*` is columnwise and remains true for the clipped code.

### New primitive exponents

The independent implementation represents each bound by one monomial C*(y/y0)^p,
rounding C upward to176-bit binary rationals. This is different from the author's
sums of monomials and decimal rounding. Addition chooses the larger power; multiplication
adds powers. Denominator inversion is allowed only for nonpositive power and coefficient<1.
No author chain implementation is imported.

The new powers of 1/k,sqrt(k),1/sqrt(k),d,H+1,1/H,r are respectively
`-12,+6,-6,+12,+8,-8,+4`. The inverse F* has power-4. Indeed, gamma>=1 and
`floor(H/2)(ceil(H/2)-7)>=(H-14)^2/4` give

```
F* >= .495*250^2*s_lo^2*(1-y0^-4)^4*(1-14/Hlo)^2*y^4/e2,
e2>=exp(1/2+3/[2(n0-1)]).
```

This matches the author's coefficient and direction of every floor relaxation.
The front exponential is bounded by positive `c_g*(y/y0)^-40`, since the derivative
of `40log(y/y0)-c(y^6-y0^6)` is nonpositive once c*y0^6>=40/6. The exponential's
Taylor partial sum is used as a **lower** bound before taking its reciprocal.

### Independent universal results

For every real y>=21, hence every permitted integer n>=10^16:

| Quantity | Independent rational upper bound (decimal summary) |
|---|---:|
| front closure | 6.551153895e-7 |
| background feedback | .005767098105 |
| outside-window feedback | .005767077881 |
| arrival closure | 9.895985481e-7 |
| second-order loop e | .006443770901 |
| first error component | .008327974060 |
| own-pair source component | .370502190177 |
| other-pair source component | .001804094211 |
| total eps_SO | **<.380634258447 <.3807** |

The final component powers are0,-4,-4. All feedback denominators stay positive for
every larger y. Thus rounding jumps or dimensions beyond any sampled grid cannot
invalidate this majorant. The JSON includes the exact rational final coefficient.

### Robustness coefficient

Use sqrt(j)>=y^2/49*(1-2401/y0^4), because sqrt(2400)<49 and sqrt(1-t)>=1-t.
The squared hold factor supplies `(1-y0^-4)^4` and its printed seven-step correction.
Using the **printed** error allowance .3807, the independent rational lower bound is

```
(1-.3807)*.0004988*.6272*(125^2/49)
 *(1-2401/y0^4)*(1-y0^-4)^4*(1-7/[125(y0^4-1)^2])^2
 > .06101738006667 > .0610.
```

All loss factors improve at larger y. This proves the uniform lower bound, rather
than relying on a pointwise evaluation at n=10^16. Subtracting either the dense
correction3e-9 n^(2/3), or the skeleton own correction20n^(1/3), still leaves more
than tau<=.0567n throughout the stated domain.

This establishes Theorem9.2 for R0, the actual prescribed dense readout, and Lemma M's
skeleton-bus object. These are separate quantities and were not interchanged.

## 8. Combined listing counts and sharpness

Theorem4's all-query state listing is used with
`N3=1.3e7 F_s`, not merely the one-step shortcut. Its nonzero-coordinate count, together
with the proposed bus listing, is bounded by

```
P_C(u)=a0+a1*u+a2*u^2+3C0+(9/4)C1+C2*u^2,
a0<1.784e17, a1<1.187e15, a2<1.974e12, u=ln n.
```

An independent reconstruction from W',Ws,p,L and F_s confirms these coefficients.
The required count is the **sum** |Phi|+|Psi|. The dimension lower bound for the coded
section is `exp(u/3)/2400-2`. Exact positive Taylor lower bounds certify g,g',g''>0 at
the stated thresholds, where g is this dimension lower bound minus P_C.
Because g'' increases, the inequality holds for all larger n.

Independent g lower margins at the rational starting arguments are:

| max C_i | threshold | positive lower margin |
|---|---:|---:|
| 10^12 | 10^63 | 3.6014469216e15 |
| 10^18 | 10^78 | 9.4041152940e21 |

The old quarter-root thresholds10^80 and10^100 also recheck. For arbitrary fixed
constants, exponential growth beats the same quadratic, giving a finite threshold.
No original Lemma M hypothesis requires D=Omega(n). The width and budget hypotheses
hold well below these count thresholds. Sparse Borsuk–Ulam then yields a **joint** zero.
There the uniform legal query's skeleton-bus readout remains >tau, contradicting tau/4.
This proves Corollaries6.2D and9.3 in the prescribed dense contract.

For Corollary9.4, a sparse odd listing with fewer than D nonzero coordinates has a
zero on the parameter sphere. At that zero the gather readout is >tau and at most
`1.3807*||first-order readout||`, so the first-order part is
`>tau/1.3807>.72tau`. This contradicts the stated residual target. The public schedule
satisfies the public-support hypothesis of PR31's matching first-order listing upper
bound. At m=3,T=n/2 its other polynomial terms are constant while its off-cycle term
is O(n^(1/3)). Hence this **listing order on that resource ray and that channel** is sharp.

It is not an upper bound on all gradient-memory capacity. It does not prove the
general-width law, nor a lower construction for every arbitrary m,T. Those require
additional analysis; the concurrent-pair row-class/feedback proof is explicitly open.

## 9. Demonstrated defects and minimal corrections

### F1 — Proposition7.2 overstates the scope of its reusable principle

**Location:** primary PROOF.md:461–479; support equality at471.

The structural induction is valid, but actual support need not equal the cardinality
of a chosen scheduled envelope. Add a never-held off-cycle bath row to each S_t,
targeting its natural next bath state. P1/P2 remain true, its actual input is exactly
`atanh(tanh(pre))-pre=0`, and the original actual support remains3 while the envelope
has size4. **The equality is REFUTED.** Replace it with `actual support<=max|S_t|`.

Also, the quantitative part invokes the3eta perturbation estimate after wording its
first part for **every** alpha,eta. For alpha=.6,eta=0,
`R-R0=-.4R0`, so ||R-R0|| is not bounded by3eta=0. Already on the first three undriven
steps, for an off-cycle credit column c,

```
D3=G3(R-R0)G2*c2*e_c !=0,
```

since c2>0, all finite gates are positive and R0 is invertible. The independent
n=512 computation gives ||D3||=.3971033308899, against a3eta-based bound0.
This refutes the generalized perturbation estimate; the stated proof cannot justify
an arbitrary-alpha quantitative transfer principle.

**Minimal correction:** explicitly require the prescribed normalization/smallness
conditions, or state bounds using the actual ||R-R0||, ||R|| and actual source maximum.
The principal dense theorems already impose the prescribed conditions and cite
Lemmas2.1D–3.2D directly. Their proof is not repaired by this audit and does not need
the false generalization. Do not reuse Proposition7.2 quantitatively outside that scope.

### F2 — All-eta invariance is not an all-eta gate/range theorem

**Location:** PROOF.md:280–292, summary/status line595; matching REPORT/CHECKS language.

Locality/endpoints remain exact for any eta, but the front/range/source conclusions
do not. Here is a counterexample with n in the state-lemma size range:
take n=10^8, eta=100, alpha=a/||R0+100qq^T||. The first step is h1=tanh(.05)1.
Using alpha<=1/99, sqrt(k)<7072 and tanh(.05)<.05,

```
pre_1(2) <= .05+(.05*7072+5)/99 <3.673,
claimed front lower >= .025*7071-.001 =176.774.
```

Both inequalities are checked as exact rationals. This is deliberately **outside the
prescribed eta bound**: it refutes the blanket all-eta prose, not Lemma2.3D under
its actual prescribed-matrix hypotheses. Independently, n=512,eta=100 gives front
preactivation .107786887 versus the claimed .399 bound.

**Minimal correction:** say exact locality, zero-sum cancellation and endpoint equality
hold for arbitrary coupling; preserve gate/range and robust-readout assertions only
under their proved small-coupling hypotheses. Successful stress samples are finite
evidence, not a universal extension.

### F3 — Certificate summary rounds downward

**Location:** PROOF.md:543 and CHECKS.md skeleton-certificate row.

The exact author certificate value at y0=21 is .38063425844753235..., greater than
.38063. Reporting that certificate as an upper bound .38063 rounds in the wrong
direction. Use `.38064` or the theorem's `.3807`.

This does not demonstrate a counterexample to the sharper actual eps_SO function:
an upper certificate larger than .38063 cannot refute that separate inequality.
It does show the **reported certificate value** does not establish the displayed
rounded-down number. Theorem9.2 uses .3807 and passes independently with slack.

### F4 — Precision and sharpness descriptions need their explicit scope

`exp_skeleton.py:code_matrix` obtains delta_* through NumPy singular values. Its
description as an **exact** delta_* is inaccurate; those are finite-precision
approximations with no outward singular-value certificate. Similarly, a printed
zero at60 digits is not by itself proof of exact equality. The algebraic locality
and singular-value arguments are the proofs; the scripts are numerical evidence.

Keep the constant-width sharpness claim tied to m=3,T=n/2 and the first-order
listing task. Do not promote Remark9.5's broader rate or practical capacity into
a theorem. Define Bfull separately from Bfull*E in Proposition5.1's notation.

The primary RESUME.md is also behind section9: it still lists closing the
quarter-root-to-sharp-rate gap as a next action and says tiny eta matters only
for the gradient, not states. Update those navigation statements after the
mathematical scope corrections; otherwise a researcher could repeat work
already completed by the saturation theorem.

## 10. What was tested, and confidence limits

The independent all-size rational checks passed, including feedback closure,
the actual .3807 error allowance, the stronger .0610 margin, fit and dense/own
corrections. The sampled integer tests include the first admissible n and
cube/floor jumps, but the universal conclusion rests on exponents and rational
majorants, not those samples.

The independent saturation calculations use exact determinants and90-digit
singular calculations at D=2,3,4; the all-D guarantee rests on the mathematical
singular-value proof. The D=89 gain lower bound is exact rational arithmetic.

The independent dense simulations at n=512 verify frozen-input full-gradient
normalization, actual three-coordinate support, common endpoints, and the dense
credit/readout decomposition. Such n violate the theorem's dimension and bath
regime; their measured separations are not theorem-scale claims or counterexamples.

Author certificates were reproduced separately. The small author saturation
run produced15 cases with at least D saturated coordinates, support3 and tiny
endpoint residuals. Its negative small-n bath is explicitly outside(H).
No large experiment was needed to repeat stored plots or tables.

This audit is not a formal proof-assistant verification. All results rely on the
specified exact-real arithmetic model, frozen normalization, continuous encoder
contract and legal-future preactivation convention. No claim is made for a
bounded-precision implementation, a generic dense matrix, or an upper bound on
the full metric. These limitations do not constitute additional assumptions
inserted into the proofs: they are the original contracts and the result's scope.

## 11. Defensible conclusion and next objective

Opus extended the construction to the actual prescribed dense matrix and proved
a cube-root continuous-antipodal learning-credit lower family at constant peak
input width. The combined listing contradiction genuinely refutes original Lemma M
under this dense contract. The normalization transfer supplies lower bounds in
the full fixed-feature and full group-RMS metrics without changing their weights.

It is gradient/learning-credit memory, not distinct forward states: all endpoint
states are identical. It separates antipodes uniformly, not every pair of nearby
parameter vectors. It is an exact-real existence result with severe coding
conditioning, not a practical training or numerical-memory demonstration.

Correct the auxiliary principle and stress/precision wording before treating them
as reusable results. For the original linear-memory problem, the next high-value
objective is a bound or counterexample for the remaining centered/second-order
bus channels under the full query contract. Concurrent-pair analysis could clarify
the barrier-scale boundary, but the present single-pair sharpness result does not
settle the full mechanism family or produce linear dimension below that boundary.

The original **D=Omega(n), mT=o(n^(3/2))** question remains **OPEN**.

All audit files are separate. Existing research, prior audits, restricted notebooks
and AGENTS.md were preserved. No commits, pushes, merges, rebases or external contacts.
