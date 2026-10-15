# Final independent cross-PR mathematical audit

Codex, 2026-10-15. Reviewed PR #27 at a67be6da53a539198fc82264606b88d74de67a00
and PR #28 at 3746747137bb681ceda9c0f21b19e66d264165d1, including their proofs,
verification code/results, independent audit records and responses. The unchanged
contract was checked against CURRENT_THEORY.md and the holding-cost proof's bound (20).
No restricted notebook was read or edited. No training, GPU, merge or outside contact.

**Verdict after the corrections accompanying this audit:**

* **PR #27: PASS in its stated scopes.** The fixed orthonormal K-probe theorem and
  its bath/protected/state foundations are proved. One further false auxiliary
  post-gate identity was found and corrected on PR #27 at
  [6ef95b5](https://github.com/soma2-stack/AI-Architecture-Research/commit/6ef95b5259f9a7c807c123411f37499490a4d05a).
* **PR #28: CONDITIONAL.** Theorem 2 and the abstract Theorem 3 pass; Corollaries
  3.3/3.5 have their explicit additional hypotheses. Theorem 4 is a valid implication
  from Hypothesis B in its selected parameter group and dimension range. Its imported
  foundations have now been independently checked, rather than assumed on authority.
* Hypothesis B, the logarithm-free general barrier, the general neutral-path tax,
  and the original frozen dense-tanh full-d_F strict-budget problem remain **OPEN**
  (the tax remains **CONJECTURAL**). No unconditional n^(3/2) resolution follows.

## 1. Prioritized findings and repairs

| Priority | Finding at the audited heads | Status and effect |
|---|---|---|
| 1 | PR #27 Lemma 1.3 still omitted the gate on its additive injection | **REFUTED identity; repaired.** Use c_t U G_t Ev. Theorem 1 and Theorem 4 do not depend on that misprinted additive term. |
| 1 | PR #28 section 6's claimed exact total-credit unrolling omitted the front bus delivery and used actual B without its dense residual | **REFUTED identity; repaired** for B', with both standard bus channels. Theorem 4 already includes both channels in B. |
| 2 | PR #28 still said transport cannot pass the finite front, and the front term is killed | **REFUTED exact-destruction interpretation; repaired** to conditional attenuation with nonzero leakage. Not an ingredient of Theorem 4. |
| 2 | Theorem 2 used 5.9e-4 as a lower bound for the resource ratio | **REFUTED intermediate inequality; repaired** to 1/1700. Final 1.9e-10 remains valid. |
| 2 | The comment after Lemma 3.2 claimed a matching optimality scale | **Not proved by that lemma; withdrawn.** The displayed 1/D construction and 1/sqrt(D) upper bound do not match. |
| 2 | Corollary 3.3 did not explain why time-varying public source weights preserve its use of variation | **Proof clarified without new assumptions.** Project unweighted Delta Y, not c Delta Y. The 553 conclusion survives. |
| 2 | Text after Lemma 7.2 could be read as a positive capture floor | **Not a consequence of the upper bound; repaired.** Uniform bath gates have zero capture. |
| 3 | Corollary 3.5 printed a rounded lower bound as an equality; its resource paragraph could drop the public-set assumption | **Presentation corrected.** rho^2>=.0018029 n^2, and H1 remains in force. |
| 3 | Historical section 6 still suggested a full-metric, logarithm-free completion | **MIS-SCOPED historical inference; explicitly withdrawn.** The current theorem is the selected-group logarithmic-loss implication. |

These repairs preserve the valid theorem statements and constants. None assumes B,
front destruction, public source amplitudes in Theorem 4, or a public carrying set
where Theorem 4 allows a code-dependent one. Earlier negative results are preserved
in the historical audit/response records, not rewritten as successful proofs.

### Exact counterexamples to the two residual identities

For post-gate memory credit b, O=UPU and U^2=I give

```
b_t=G_t(aO b_(t-1)+c_t Ev),
U b_t=a(UG_tU)P U b_(t-1)+c_t U G_t Ev.
```

At T=2, zero raw inputs and v=e_d, b1=0 and c2=tanh(.05)/sigma>0. The old
formula has error norm c2(1-g2[d]). For every n>=1e8 the off-cycle preactivation
is z2=.05-a gamma tanh(.05)/sqrt(k)>0, so the error is exactly c2 tanh(z2)^2>0.
At n=100000000 it is .00249513500997556. This is a reference identity counterexample
inside its mathematical scope, not a counterexample to the resource theorem.

For a local reference path p_l(t), the correct unrolling is

```
B'_T(l,:)=sum_t P_l(t)[c_t e_(p_l(t)) + a J(B'_(t-1))
            + 1_{p_l(t)=1} a gamma Sum'(B'_(t-1))/sqrt(k)],
P_l(t)=a^(T-t) prod_(s=t)^T g_(p_l(s),s).
```

The front term is nonzero even on zero-input histories: at step 2, B'_2=c2 G2 E;
at step 3 the front receives `a gamma G3(1) Sum'(B'_2)/sqrt(k)`. All factors are
positive at finite preactivations. There is no exact saturation cutoff. The new
small-size regression measures a missing-front residual above 2 in a legal zero-input
reference history and a corrected total=own+bus residual below 1.2e-14.

## 2. PR #27 foundations: independent derivations and dependency map

Theorem 4 imports **only** Lemmas 2.1–2.5 and the state comparison (3.1)–(3.2),
plus the common model constants and horizon bound. It does not use PR #27 Lemmas
1.1–1.3, a total hole-credit estimate, front destruction, or the credit cancellations
needed for the K-probe theorem. Theorem 2 additionally imports (3.3)–(3.8) for its
fixed-probe credit bound. Theorem 3 is an independent abstract variation/topology argument.

### Own injections versus bus: PROVED after repair

For x0=0, the exact row identity is

```
Ox=Sx+1_(>=1)J(x)+(gamma/sqrt(k))e1 Sum'(x),
J(x)=gamma x_(d-1)/sqrt(k)-gamma^2 Sum'(x)/k.
```

The cycle skeleton S has no wrap. The own part A satisfies
`A_t=G_t(aS A_(t-1)+c_t Ev)`; the remainder receives **both** bus terms evaluated
on the total credit. Only a cycle own path has the c_max sqrt(L) bound. Off-cycle
own credit repeats one parameter coordinate and is bounded by c_max |v_j|min(T,n).
Neither bounds accumulated total bus credit. The previous legal neutral-hole
counterexample is retained and reruns successfully.

The homogeneous post-gate ordering is a(UGU)P. The full new injection is c UGEv.
The exact Ou identity leaves nonzero O(1/sqrt(k)) leakage. The front attenuation
requires the explicit |Sum'|>=s_lo k/2 condition; a bath floor alone does not supply
that hypothesis. Positivity of all finite tanh gates and invertibility of R0 rule
out finite exact annihilation. The uniform/contrast norm identity is exact.

### Bath arithmetic and all-horizon comparison: PROVED

The virtual chain must use the **same actual global J** as the row being compared.
With rho=delta sqrt(n) its scalar error obeys

```
e_(r+1)<=a e_r+rho,
e_A<=rho(1-a^A)/(1-a)<=n rho<=4e-8/sqrt(n).
```

This is uniform in A. It does not assume the comparison bath is an independently
generated R0 history. It is distinct from the coupled-state horizon restriction below.
Summing excess by chain age, including the complete geometric tail, gives an exact
upper certificate 221.021047106976...<223 for start 1; even the larger start 1.06
has upper bound 222.531626600976...<223. These are upward-rounded arithmetic
certificates, not finite floating truncations of an infinite series.

The odd/even integer-safe bath estimate is

```
gamma<=7071/7070, (m+1)/k<=10002/99999999, n rho<=4e-12,
beta+a s >=1/20-(7071/7070)^2[224(10002/99999999)+4e-12]-3/7070
          =.027164853275575... >2399/95940 >=atanh(.025).
```

Thus the induction proves s_t>=.025. The moving-bath gap argument uses the same
time-dependent maps, not a stationary approximation. Its decrement coefficient
exceeds .29 s_lo^3, giving lifetime Lambda=450000. The protected set contains recent
drive/front descendants, has size <=(m+1)(Lambda+1), and outside it ordinary rows
have h>=.0124; hence divided-difference slopes and gates are <=q=1-.00015.

The floor applies **per history**. An antipodal protected union has up to 2m drives,
but each history still uses its own width m for the bath floor. No false application
of the bath lemma with doubled admissible width occurs in PR #28.

### State and credit comparisons: PROVED in their stated horizon ranges

At a listing zero, auxiliary state differences reset protected memory and row 0.
Initial source differences are retained unless actually listed as zero. Newly driven
sources reset using their listed actual predecessor and input differences; undriven
sources use the lambda self-map. This convention is essential to PR #28's state-only
use, which does not list all initial source states.

The local predecessor map is a partial injection, so

```
||u_(t0+s)||2<=2sqrt(n)q^s,   ||u_(t0+s)||infinity<=2q^s,
e_s<= (1+delta sqrt(n))e_(s-1)+2delta sqrt(n)q^(s-1).
```

For W<=T<=n^(3/2), `e_s<=3delta sqrt(n)/kappa`. Gate changes are controlled exactly
by `Delta g=-(h+ + h-)Delta h`, not omitted. Theorem 4 uses this only below
T<=2.5e-5 n^(3/2), safely inside that range. The short-budget K-probe error further
uses the credit listings and is <3.3e-7 by (3.5)–(3.8). The uniform auxiliary query
remainder is analytically <1.46e-11; the retained 2.1e-4 allowance is safe.
When W=T the complete inputs agree, giving identical histories exactly.

### Probes, topology and resources: PROVED with scope limitations

PR #27 fixes an orthonormal basis of a memory-row probe span, K its rank, with
1<=K<=k-1. Arbitrary probe lists cannot be counted with their unnormalized Euclidean
response norm; the old nonorthogonal counterexample is retained. Borsuk–Ulam is
applied to continuous odd listings on the boundary sphere of one continuous
common-endpoint section. It supplies a zero, not a geometrically round subsphere.

Theorem 1 uses a public coordinate **envelope** of width m. For exact common supports
this is actual peak width; a larger envelope is not automatically the smaller
pointwise support budget. Actual dense corrections and full preparation/reset count.
No support lower bound is converted to an absolute-energy lower bound.

The horizon necessity T>.001sqrt(n) follows from zero initial sensitivity, injection
norm <=sqrt(l), recurrent normalization 1/n and future adjoint norm <=1. It cannot
be applied after discarding preparation. The response matrix gives D<=nK by ordinary
Borsuk–Ulam. The corrected ratio inf y/(1.7+ln+ y)=1/1700 preserves Theorem 1's
2.9e-10 coefficient. The K-dependent logarithm and the short-budget scope of its
dimension estimate remain explicit. No growing-K or full-gradient impossibility follows.

## 3. PR #28 Theorems 2–3 and their corollaries

### Theorem 2: PROVED in the inherited K-probe scope

The soft support weights are even/continuous and positive exactly on the union of
the antipodal actual supports. Multiplying odd state/input/credit quantities by them
preserves continuity and oddness. Their zeros enforce actual equalities wherever
either history drives a coordinate, even if its nonzero amplitude is arbitrarily small.
Pre-window ancestors are indexed by their geometric path, not a fixed row number.
This covers interruptions, fresh source drives and moving schedules.

Sparse Borsuk–Ulam needs only a uniform **pointwise support count**, not a public
fixed nonzero coordinate set. A fixed s-by-M Vandermonde matrix maps every nonzero
<=s-sparse vector to a nonzero vector in R^s, giving an elementary reduction to
ordinary Borsuk–Ulam. Conditioning is irrelevant for this exact existence argument.
The listing count is

`s<=(K+2)(2m+1)(2W+Lambda+2)`.

Protected-union decay and the corrected PR #27 comparisons then apply. The exact
resource coefficient is 1/(1700*3e6)=1.960784313725...e-10>1.9e-10. Thus the final
theorem is unchanged. This theorem removes public-schedule restrictions for fixed K;
it does not remove the fixed-probe restriction.

### Theorem 3: PROVED; Corollaries 3.3 and 3.5: CONDITIONAL as stated

For a cycle own profile, each suffix product is nondecreasing with injection time,
in [0,1]. Its antipodal difference has internal variation <=2, absolute value <=1,
and zero-extended variation <=4. Project **that profile**, not the product with a
time-varying public source. For one row,

`||(I-Pi_b)Y||2^2<=b (max block oscillation)(sum block oscillations)<=8b`.

At most M intervals meet a block, so arbitrary bounded public weights and query
signs give `||sum_l nu_l c_l (Y_l-Pi_bY_l)||2^2<=8 c_max^2 nu_max^2 bMp`.
Each interval meets at most ceil(L/b)+1 global blocks. List a **single scalar per
block**; repeating block entries would give an incorrect sparse support count.

For A=rho^2/(32c_max^2nu_max^2p), b=1 is exact when A<=4L. Otherwise the largest
integer b satisfying b(L+b)<A either is >=L (at most 2p coordinates) or obeys
b>=A/(4L). This handles strict inequalities, the floor and both integer branches.
It yields

`D<=128c_max^2nu_max^2(pL)^2/rho^2+2p`.

With rho=3tau/4 and rho^2>=.0018029n^2, coefficients 8402 and 1.03e5 are safe.
Corollary 3.5 retains H1–H5, notably the public carrying set/source and the remainder
bound. Its resource statements require 8(Lambda+1)<=D<=n. The constants 1.38e-10
and 8.1e-11 survive. Arbitrary code-dependent carrying sets require Theorem 4's
separate soft listing, not an unannounced deletion of H1.

Corollary 3.3's public c_max<=1 gives ||Delta Y||>=||c Delta Y||. Applying the
unweighted variation lemma with N=553 gives `4ceil(L/553)<=n/553+4<.00181n`.
This repairs its explanation without restricting c_t to be time-constant.
The old 553F multi-query extrapolation remains uncertified and unused.

## 4. Queries, source lemma and Theorem 4

### Lemma 1.2': PROVED for every legal horizon

Keep HI=sech^2(.25) exactly and r_H=-ln HI, not the upward-rounded .0619.
The correct cutoff is Fs=ceil(ln(1.01sqrt(k))/r_H). It is 144 at n=1e8 and 8959
at n=2^1600. For F>=Fs, contraction alone gives ||nu||<=HI^F sqrt(k)<=1/1.01<1;
no long-horizon spike/wrap argument is needed.

For F<Fs<d-3, moving U-spikes stay away from rows 0 and 1. The ordinary-coordinate
recurrence has forcing .1719 HI^(F-j)+5/sqrt(k). The scalar maximum
`max_(x>=0) exp(-r_H x)(.3436+.1719x)` is <1.159, and its additive tail is <.0121.
The Householder correction therefore leaves ordinary weights <1.2. Row 0 remains
separate, positive and <=1. A fresh U-coordinate-0 spike at an intermediate gate is
moved to d-1 by P^T and is included in the moving spike set.

The new exact rational certificates enclose exp by positive Taylor sums and a full
tail, enclosing r_H between .061859 and .061860. They certify the forcing, continuous
maximum and perturbation constants without relying on printed decimals. Finite
adversarial endpoint-gate queries are additional diagnostics, not proofs for all gates.
Actual-R query weight error is <=F HI^(F-1)delta sqrt(n)<=6.4delta sqrt(n).

### Lemma 7.3: PROVED, with initialization separate

c1=Delta c1=0 exactly. After a source update, undriven coordinates are within
2lambda+delta sqrt(n) of sigma; only that step's <=m driven coordinates need the
crude 1+sigma bound. This is why persistent source initialization does not require
free preparation or public source controls. For t>=2 the amplitude remainder .41/n
is retained, and for integer m>=1 c_max<=1.0022. The two-history union gives the
161m/n bound on |Delta c|, not a one-history count.

Ordinary own source-channel coordinates are <=1.2min(T,n)max|Delta c|, giving
137m min(T,n)/sqrt(n). For fixed spike-list rows, total legal readout weight is
<=6sqrt(k): max F HI^F<5.95 and Fs/sqrt(k)<.021 cover also list rows with j>F.
Consequently the spike source channel is <.0242n^(3/4). Below the budget these
cost at most tau/16 and tau/64 respectively. The full original zero initialization
and actual source feature are preserved.

### Theorem 4: CONDITIONAL on B; no additional demonstrated proof gap

The state listing has at most N1=(2m+1)(4W+Lambda+4) entries. Carrying soft weights
are even/continuous; at their positive positions the block means vanish at a listing
zero. The weighted block estimate is pointwise and thus applies to the even cbar
at that pair, without requiring c to be public over the original section.
Off-cycle carrying rows list their entire own scalar. The integer block counts give
N2=2.32e5(pL/n)^2+2p. Fixed query spikes have per-row block count <=1.3e7 (or
<=1.8e4 for the sole one-step spike), including the round-down correction.
Before flooring, b_j/n>3.0370e-8; after flooring it is >=2e-8 at n>=1e8.

For a row outside C union E*, a protected position in [T-W',T] would imply a recent
drive/front ancestor and hence membership in C. Thus its whole suffix there is
unprotected in both histories. If there is a last protected position of age a_l,
distinct final paths can be charged to distinct starts, giving

`sum_l q^(2a_l)<=(2m+1)q^(2W')/(2kappa-kappa^2)`.

A never-protected path is **not** charged to an initial drive: its R1 part is empty,
all old injections are in R2, and recent ones are in R3. Local paths never wrap.
The R2/R3 coordinate count uses one cycle path per time offset; off-cycle repeated
injections use the geometric bound. The final certified release allowances are
1.91e-4n, .85e-4n and 4.1e-4n, totaling 6.86e-4n<tau/32.

The complete readout ledger, including the actual-R query correction, is

```
bus                         tau/4     [B, not proved]
ordinary source channel      tau/16
spike source channel         tau/64
carrying cycle block error   tau/4
spike block error            tau/8
released own content         tau/32
dense + source rows + query  <2e-7 sqrt(n)
total                       <=47tau/64+2e-7 sqrt(n)<tau.
```

Source rows and dense forcing are not silently discarded by selecting a memory
block. Actual gates, not gates from an independently regenerated history, define B'.
Both standard-coordinate bus terms remain in B. The front is not assumed zero.

### Resource conversion and its exact limitations

The dimension alternative is valid without a D<=n premise. The advertised resource
law explicitly needs **2N3<=D<=n**. The three count branches give respectively

```
mT>=4.7e-11 D sqrt(n),
mT>=5.6e-10 n sqrt(D)/(1+ln+ y/151),
mT>=5.5e-11 D sqrt(n),                  y=T/sqrt(n).
```

n sqrt(D)>=D sqrt(n) uses D<=n and is not an operator-rank theorem. The ceiling
intercepts are 1170012<1.171e6 and 1510006<1.511e6, including both window ceilings.
Monotonicity in log y gives the 900/log+y intermediate, and y<4.7e-11n in the only
remaining branch gives the weaker advertised 890/ln n. Thus, conditional on B,

`mT>=4.7e-11 D sqrt(n) min(1,890/ln n)`.

For D=Theta(n), the asymptotic conclusion is **Omega(n^(3/2)/log n)**. The finite
range n<=exp(890), where the factor equals one, cannot be used to remove the log
as n tends to infinity. All-query 2N3<=D<=n is not even feasible at n=1e8; its
explicit constants start being useful only at substantially larger n (about 5e9).

The group here is `{u f_s^T:u0=0}` with unchanged inherited normalization. The
original full d_F and omitted parameter directions are not replaced by this metric.
A projected-metric impossibility is not a full-metric impossibility: a pair can be
separated by an omitted component. No full-gradient extension is proved in this audit.

## 5. Reproduction, evidence limits, and remaining work

Python 3.11.9, NumPy 2.4.6, one CPU thread. From the PR #28 checkout:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -I theory/codex_cross_pr_final_audit_20261015/checks.py
python -I theory/codex_cross_pr_final_audit_20261015/regressions.py --pr27-root PATH_TO_PR27_CHECKOUT
```

From the PR #27 checkout:

```powershell
python -I theory/codex_pr27_repair_verification_20261015/check_full_post_gate.py
```

All assertions pass. New checks include 48 adversarial future-query cases, 480
strict integer-block choices, 2560 worst-sign weighted-profile cases, 100 adversarial
release schedules including 2763 never-protected paths, full post-gate recurrences,
and rational constant certificates. The fresh suite takes about .2 seconds; the
prior independent suites take about 7.5 seconds together. No theorem-scale dense
matrix is allocated. The previous compressed n=100000001 histories and exact
infinite-tail certificates also rerun successfully.

`results.json` and `regression_results.json` retain detailed outcomes. Historical
checkers are imported only for regression; no author implementation is imported.
The manually initialized comparison fixture is not a robust common-endpoint section;
its premise fails at step 13, which remains a negative control, not admitted evidence.
The large-n source/cutoff and small-size algebra tests have their stated scopes.
Only the analytic arguments and exact arithmetic certificates support universal
claims. Passing finite samples does not prove B or uniform antipodal separation.

**No demonstrated mathematical error remains in the repaired target arguments.**
This is an independent mathematical audit, not a formal proof-assistant certificate.
Hypothesis B has not been proved or tested as a global conjecture here. Removing
the logarithmic loss and extending the selected-group conclusion to the unchanged
full contract require separate proofs. See [HANDOFF.md](HANDOFF.md) for exact targets.
