# Route 7A: a uniform finite-stage diameter bound for the un-cleared trace-neutral candidate

Date: 2026-10-07. Independent GPT-6 investigation.
**Research status: PARTIAL / PENDING INDEPENDENT REVIEW.** The main target is OPEN. Do not update CURRENT_THEORY.md.

## Exact target and scope

This investigates Astra's trace-neutral donor gate family (25), from
[\`astra_route7a_reservoir_20261007/PROOF.md\`](../astra_route7a_reservoir_20261007/PROOF.md), sections 11.1–12.

We assume the inherited fixed-source, reduced reference recurrence
\[
M_0=0,\qquad M_t=G_t(x)\bigl(a O_* M_{t-1}+I\bigr),\quad
a=1-1/n,\quad \|O_*\|_{2\to2}=1,\quad 0<G_t\le I.
\]
Every private gate difference occurs **only** at the first and third donor steps of one of R three-step stages, on the four balanced tuple coordinates for each donor group. Precharge, public survivor captures, waiting, and final common reset use the same public gates in both histories. This is the candidate's stipulated public bath/front model, NOT a theorem for arbitrary private survivor schedules, history-dependent observers, or a new source feature.

Write \(\varepsilon=10^{-4}\), \(g_*=0.9975\), and \(x=(x_{j,i})\in[-1,1]^{R K}\). At the first step \(d_1=g_*+\varepsilon x_{j,i}\); the middle donor gate is \(g_H\). For the third gate write the exact formula in the archive as
\[
d_3(x)=g_*\frac{A+B g_*}{A+B(g_*+\varepsilon x)},
\qquad A,B>0,
\]
where \(A,B\) depend on the stage's **public incoming local trace** \(\tau\), \(a\), and \(g_H\), but not on the private control. (For example, \(A=1+a g_H\), \(B=a^2g_H(1+a\tau)\).) This formula matches the final local scalar trace **exactly** across histories. It is not a reset of the complete \(J,B,H\) feedback state.

## New scoped bound (elementary but uniform)

Set
\[
L_*=\Bigl(\frac{g_*}{g_*-\varepsilon}\Bigr)^2
=1.000200531408\ldots.
\]

**Lemma 1 (third-gate Lipschitz property).** For any \(x,y\in[-1,1]\), any \(A,B>0\),
\[
|d_3(x)-d_3(y)|\le L_*\varepsilon|x-y|.
\]
Proof: differentiate. With \(z=A/B\ge0\), the derivative divided by \(\varepsilon\) is bounded by
\(g_*(z+g_*)/(z+g_*-\varepsilon)^2\).
It decreases in \(z\ge0\) and has maximum \(g_*^2/(g_*-\varepsilon)^2\). The mean-value theorem completes the proof. The first-gate Lipschitz constant is exactly \(\varepsilon\).

**Lemma 2 (complete reference feedback cannot amplify a gate difference faster than its horizon budget).** For any two legal schedules with the same initial state and public \(O_*\),
\[
\|\Delta M_N\|_{\rm op}\le N\sum_{t=1}^{N}\|\Delta G_t\|_{\rm op}.
\]
Proof: exact difference identity
\[
\Delta M_t=aG_t(x)O_*\Delta M_{t-1}
+\Delta G_t\bigl(aO_*M_{t-1}(y)+I\bigr).
\]
As \(\|M_{t-1}(y)\|_{\rm op}\le t-1\), both \(aO_*\) and the gate are contractions, hence
\(\|\Delta M_t\|\le \|\Delta M_{t-1}\|+t\|\Delta G_t\|\).
Sum over time. This includes full \(J,B\) renewal implicitly; no Born truncation or fictitious reset is used.

**Theorem (full-control-cube diameter).** Under the above hypotheses, for any \(x,y\in[-1,1]^{RK}\),
\[
\sum_t\|\Delta G_t\|_{\rm op}\le
\varepsilon(1+L_*)\sum_{j=1}^R\max_i|x_{j,i}-y_{j,i}|
\le 2\varepsilon(1+L_*)R.
\]
The repeated four-site coordinates do not contribute a \(\sqrt K\) factor to the diagonal operator norm.

For even n and \(\sigma<0.051,\ \ell=n/2\), the **actual legal-future supremum in the fixed-source reference metric** is bounded by the unrestricted unit-adjoint supremum:
\[
\nu_{\rm ref}(M_N(x)-M_N(y))
\le\frac{\sigma\sqrt\ell}{n}\|\Delta M_N\|_{\rm op}
\le1.45\times10^{-5}\frac{N}{\sqrt n}R.
\tag{A}
\]
If \(N\le C_T\sqrt{nR}\),
\[
\boxed{\nu_{\rm ref}(M_N(x)-M_N(y))
\le1.45\times10^{-5}\,C_T R^{3/2}.}
\tag{B}
\]
For \(C_T\le1\) and \(R\le26\), (B) is at most \(0.00192233<0.002\), for **every pair in the entire control cube**. Under the inherited dense-model pair comparison, its \(o(1)\) correction is also below the residual gap for all sufficiently large admissible n at each such fixed R. This kills the claimed 0.002 robust fixed-feature margin in this restricted finite-stage and duration regime. It does **not** imply asymptotic impossibility when \(R\to\infty\).

**Additional restriction for the natural unit-Euclidean control sphere.** If the control family is the unit sphere \(\|x\|_2=1\) with antipodes \(x,-x\), Cauchy–Schwarz across stages gives
\(\sum_j\|x_j-(-x_j)\|_\infty\le2\sqrt R\). Thus
\[
\nu_{\rm ref}(M_N(x)-M_N(-x))
\le1.45\times10^{-5}C_T R.
\tag{C}
\]
At \(C_T\le1\), (C) is below .002 for \(R\le137\). **Do not apply (C) to an arbitrary continuous legal section:** the controls could range over the whole cube with Euclidean radius as large as \(\sqrt{RK}\). Use (B) there.

Both bounds concern complete \(\Delta M_N\), so they are also upper bounds for the feedback component only when that component is considered **with its full counterpart**, not a bound on \(\Delta H_N=\Delta M_N-\Delta L_N\) individually by subtraction. No claim about a generic reader for \(H\) alone is made.

## Checks, not a legal construction

- Directly assembled the archived open-cycle-plus-rank-two \(O_*\) at n=1024 and 2048; \(\|O_*^TO_*-I\|_F\) rounds to zero (floating-point) and largest singular value is 1.
- Evaluated the scalar three-step compensation at \(\tau=0,1,32,10000\), \(x\in\{-1,0,1\}\); final local trace error zero to printed precision, and third gates remain in \([0.99740003,0.99759999]\).
- Ran a **structural surrogate** retaining the entire rank-two \(J,B\) recurrence and the local \(\Delta H=M-L\), with moving four-site donor tuples, public balanced capture masks, public all-high bath/front gates, and no low-donor clear. It is **not** a verified lifted admissible frozen-tanh history; small n also violates extreme asymptotic spacing/width thresholds. This test can diagnose algebra and amplitude, not legal-query width.
- At n=1024, m=3, precharge \(L=\lceil\sqrt{nR}\rceil\), R=1/2/3/4: the finite-difference \(\Delta H\) Frobenius Jacobian on 3R controls has full numerical column rank, but its first/last singular values are respectively (0.000329/0.000324), (0.000503/0.000368), (0.000626/0.000437), (0.000724/0.000491). For ONE sampled maximally Frobenius-exposed antipodal control direction, the unit-adjoint-scaled query ceiling is \(5.95\cdot10^{-7}, 9.00\cdot10^{-7}, 1.11\cdot10^{-6}, 1.29\cdot10^{-6}\).
- At n=2048, m=4, R=2, L=65, singular-value extremes were 0.000500/0.000359; sampled direction unrestricted-adjoint ceiling \(6.28\cdot10^{-7}\). A sampled direction does not certify the worst case or any robust sphere.

Numeric Jacobian full rank is **not** robust memory dimension. The tested public masks have only 2m survivor sites and are not the large-scale distinguished Walsh family. All public non-donor gates are set to 1 in this surrogate, not to the exact chronological frozen bath/front schedule. No numerical amplitude is promoted to a full-model theorem.

## What is STILL OPEN

The bound (B) increases like \(R^{3/2}\), so it does not address the intended diverging \(R\sim\log\log n\) regime. Route 7A without a final clear remains **OPEN**; possible feedback recycling, actual legal-query observability, and robust antipodal separation remain unproved. The factorized right parameter support and local trace neutrality alone do not settle the RNN target.

**Next falsifiable obligation:** Find a better-than-\(R^{3/2}\) all-control-cube upper for the exact trace-neutral multi-stage feedback **or** construct a legal, continuously parametrized antipodal sphere with a uniform 0.002 query lower bound, including full bath/front and dense correction. First isolate whether the growing-\(R\) feedback channel's actual legal adjoints can read more than the public unit-adjoint operator estimate.

No edits to CURRENT_THEORY.md; status PARTIAL/PENDING REVIEW.
