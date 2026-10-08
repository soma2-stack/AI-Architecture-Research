# Route 7A: exact rank-two feedback, legal future-query optimization and spectrum

Date 2026-10-07; author GPT-6. **Status: EXPERIMENTAL / PARTIAL / PENDING REVIEW.** The target \(D=\Omega(n)\) at \(mN=o(n^{3/2})\) is OPEN.

## 0. Executive finding

The verified *local-direct* bound from [gpt6_route7a_growing_R_local_20261007](../gpt6_route7a_growing_R_local_20261007/) leaves \(H_N=M_N-L_N\) as the unresolved source of robust memory. I computed the entire inherited reference rank-two \(O_*=C+\mathbf1u^T+e_1v_H^T\) feedback in a **finite structural surrogate** and optimized selected legal *future* query gate words. The tested feedback remains weak, even at \(R=128\). At a fixed optimized future query the derivative over \(mR\) private controls exhibits around \(m\) dominant singular directions, rather than \(mR\); much weaker queries can yield more directions.

**These are negative finite-size diagnostics, not a full frozen-tanh obstruction.** The simulations make no inference about a global supremum over all legal future queries, nonlinear robust sections, or \(R\to\infty\).

## 1. What was implemented and validated

For arbitrary vector \(v\), the reference recurrence can be applied matrix-free:
\[
M_t v=G_t(aO_*M_{t-1}v+v),\quad M_0v=0,
\]
and its exact transpose:
\[
M_N^Tc=\sum_{t=1}^{N} G_t\,w_t,\quad w_N=c,\quad w_{t-1}=aO_*^TG_tw_t.
\]
Both retain **all \(J_t=u^TM_t\) and \(B_t=v_H^TM_t\) renewal terms**. Replacing \(O_*\) by \(C\) produces \(L\); subtracting yields \(H\). In local validation for \(n=4096,R=4,m=4\), \(O_*\) preserved a random vector norm to printed precision, and direct forward/transpose pairings agreed to relative error \(2.80\times10^{-16}\) (full) and \(2.87\times10^{-15}\) (local).

The one-step legal future gate word \(g\in[g_{\rm lo},g_{\rm hi}]^{k-1}\), with \(g_{\rm lo}=\mathrm{sech}^2(.75)\), \(g_{\rm hi}=\mathrm{sech}^2(.25)\), gives the **exact restricted reference adjoint**
\[
c_1(g)=\frac a{\sqrt n} O_*^Tg.
\]
I maximized the observable reference expression \(\frac{\sigma\sqrt{\ell}}n \|\Delta M_N^Tc_1(g)\|_2\) by multi-start extreme-vertex ascent. If \(z=\Delta M_N^Tc_1(g)\), the ascent uses the direction
\[
\nabla_g\|z\|_2^2=\frac{2a}{\sqrt n}O_*\,\Delta M_N\,z.
\]
Because \(g\mapsto \|z\|^2\) is convex, choosing the vertex maximizing its tangent plane produces a nondecreasing candidate in exact arithmetic. Local optimization is **not proof of the global box maximum**.

The multi-step future test instead composes \(c_Q=(aO_*^TG_1)\cdots(aO_*^TG_L)\mathbf1/\sqrt n\) for lengths \(L=1,2,4,8\), updating each legal gate vector by its exact coordinatewise objective gradient. Only 2–3 rounds and 3 restarts were tested. There is no assertion that longer legal futures never help.

### Structural model limitations (crucial)

- \(n=4096\) or 8192 (far below the admitted asymptotic legal geometry); \(m=4,8,16\), much smaller than the target \(m\asymp n/R\).
- Public front/bath gates are replaced by 1, not their actual chronological frozen-tanh gates.
- Survivor captures are a small toy repeating mask, not the distinguished non-repeating Walsh construction.
- Gate amplitudes satisfy the scalar three-step trace-neutral formula and four-site replication, but no explicit globally admissible inverse-lift history or same exact endpoint was constructed in this computation.
- Legal future gate vectors \(g\) are in the allowed one-step memory-coordinate box, but the **history** is only a surrogate. Thus these are reference numerical objective values, not guaranteed realized legal fixed-feature query distances.
- The selected future gate words and private control contrasts are not exhaustive and cannot certify an upper on \(\sup_Q\).

## 2. Optimized legal one-step query: full \(\Delta M_N\)

Fixed surrogate \(n=8192,m=16\). Private controls were all \(+1\) versus all \(-1\) over \(R\) stages. The full reference \(O_*\) was propagated exactly, and future legal one-step gates were optimized with six random restarts plus the all-low and all-high starts, up to 12 vertex updates.

| R | Precharge L | N | Best found reference full-M query | Previous generic full-cube bound |
|---:|---:|---:|---:|---:|
| 4 | 182 | 195 | \(2.3787173\times10^{-8}\) | \(1.2495903\times10^{-4}\) |
| 16 | 363 | 412 | \(1.5955720\times10^{-7}\) | \(1.0560640\times10^{-3}\) |
| 64 | 725 | 918 | \(1.1386784\times10^{-6}\) | \(9.4122984\times10^{-3}\) |
| 128 | 1024 | 1409 | \(2.8278379\times10^{-6}\) | \(2.8893090\times10^{-2}\) |

The **computed** response grows, while the generic theorem upper becomes uninformative; the computed values are still below the required \(0.002\) margin by roughly three orders of magnitude at \(R=128\). The gap between optimizer and upper is not evidence that the global maximum is equally small.

## 3. Optimized H-only readout and control Jacobian

For a **single fixed future query** \(g\) selected to maximize the all-positive/all-negative \(H\) response, form the finite-difference Jacobian whose \(mR\) columns are
\[
J_{(j,i)}=\frac{\sigma\sqrt\ell}{n}
\frac{H_N(x+\tfrac12 e_{ji})^T c_1(g)-H_N(x-\tfrac12e_{ji})^Tc_1(g)}{1}
\quad\text{at }x=0.
\]
These columns are a finite difference rather than an exact differential, but the control dependence is smooth. The Jacobian is mapped into the parameter coordinate output \(\mathbb R^{k-1}\). The singular-value ratios and stable ranks below are diagnostic of **one fixed query only**, not the supremum over queries available separately for each antipodal pair.

At \(n=8192,m=4\):

| R | Control count mR | Top singular value | Smallest singular value | Stable rank | Number >10% of top |
|---:|---:|---:|---:|---:|---:|
| 4 | 16 | \(1.2308\times10^{-9}\) | \(1.80\times10^{-12}\) | 3.965 | 4 |
| 16 | 64 | \(4.8378\times10^{-9}\) | \(1.75\times10^{-12}\) | 3.985 | 4 |
| 32 | 128 | \(9.3905\times10^{-9}\) | \(1.54\times10^{-12}\) | 3.993 | 4 |

At \(n=4096,m=8\), \(R=4,16\) gives 32 and 128 controls, respectively. Stable ranks are 7.839 and 8.000; exactly 8 singular values exceed 10% of the top. For \(m=8,R=16\), top singular value \(9.8307\times10^{-9}\). The leading \(m\) values are comparable but the remainder is much smaller.

This is evidence of an **amplitude/independence tradeoff** in this surrogate: control stage count rises, but at one query the number of sizable linearized directions does not rise correspondingly. **It is not a proof of \(D\le m\)**. Finite Jacobian rank is neither continuous robust width nor a uniform bound over all future queries. The \(R=64,n=8192,m=4\) Jacobian run exceeded its time limit; no data or verdict is claimed for that run.

## 4. Longer future queries

The coordinate-ascent search over legal future gate words was performed for \(n=4096,m=8,R=16\) and \(n=8192,m=16,R=64\), with 1, 2, 4 and 8 future steps.

| R | 1 step, full M | 2 steps, full M | 4 steps, full M | 8 steps, full M |
|---:|---:|---:|---:|---:|
| 16 | \(2.2404\times10^{-7}\) | \(2.1558\times10^{-7}\) | \(1.9974\times10^{-7}\) | \(1.7132\times10^{-7}\) |
| 64 | \(1.1387\times10^{-6}\) | \(1.0833\times10^{-6}\) | \(9.8543\times10^{-7}\) | \(8.1379\times10^{-7}\) |

The H-only optimized values were within a few percent of full M, consistent with H carrying most of the *tested* response. **These are local-search values**, not a monotonicity theorem in future length. The \(R=128\) multi-step run also exceeded its time limit and supplied no result.

## 5. Multiple queries illustrate rather than settle the tradeoff

A separate artificial calculation stacks a few different one-step query outputs. This is **not one admissible future query**; it diagnoses which directions different observers expose. For \(n=4096,m=4,R=16\), an all-high one-step query yields normalized linearized top value \(2.01\times10^{-11}\) and stable rank 26.1, whereas a stack containing two randomly chosen gate words yields normalized top \(3.30\times10^{-9}\) and stable rank 7.6. The larger-amplitude measurement has fewer sizable directions in this example, even though the full numerical rank may remain high. Different choices of stacking weights or queries change this comparison; it is not a model-wide law.

## 6. Mathematical status and next exact obligation

**No new theorem ruling out feedback \(H_N\) has been proved.** The previous verified \(L_N\) estimate remains intact. This experiment supplies a matrix-free tool for a better targeted next step.

The highest-value next test is to replace the toy chronological bath/front gates and capture masks with the **exact legally lifted history** from the accepted corridor framework, validate the same-endpoint state, and calculate the full \(H_N\) metric under optimized legal queries. To establish a positive result, one must additionally construct a continuous section \(S^{D-1}\) with \(D=\Omega(n)\), all antipodes separated by >0.002, and \(mN=o(n^{3/2})\); a singular-value screen at finite n is not sufficient.

To establish a negative result, derive a universal robust-width/code inequality for complete \(H_N\) over the legal future-query family, not merely a selected-query spectral bound.

**Recommended action:** do not yet promote a negative theorem from these numerical spectra. First stress-test legality and query optimization; then attack the exact feedback width. The claim that Route 7A is OPEN survives.
