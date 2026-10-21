# Independent Step 3.7 audit — PR #37

**Exact target:** [`1a8203e2ced0a68017f27e507c1a92c4fb9c91ad`](https://github.com/soma2-stack/AI-Architecture-Research/commit/1a8203e2ced0a68017f27e507c1a92c4fb9c91ad), [draft PR #37](https://github.com/soma2-stack/AI-Architecture-Research/pull/37). Date: 2026-10-21. Independent worktree; no subagents, GPU, training, author-file edits, pushes, or merges.

## Executive verdict

**Theorem 11.3 survives independent mathematical verification.** The adjoint sliding box is valid even at `eps*P=1`, with zero or very small gates and anti-holes, provided the bath reference is nonnegative and below one. The theorem bounds variation of the *normalized external forcing*, retaining initial and capture costs. It does not bound variation by computational cost or establish a memory-dimension theorem.

Two literal assertions need correction:

1. **Corollary 11.5's signed-monotone extension is false.** For `phi=(-1,+1)`, `V(phi)=3`, not at most `2 max|phi|=2`. The correct general factor is three; factor two suffices for monotone forcing with constant sign. The constant-forcing **and constant-bath** corollary passes.
2. **Increasing the size ratio alone does not make the staircase attain the bound exactly.** At fixed settle parameter 8, a finite equilibration error remains. Joint limits in hierarchy, settling time, and system size can make the operator construction arbitrarily close to the variation ceiling. At fixed `n`, long stages eventually lose memory through `a<1`.

The main experimental advance is positive but limited: an independently implemented, physically fitting legal staircase with **matched normalized external forcing** does realize amplification. Population L1 gain is `2.316x` for two stages and `3.044x` for three. A legal one-step query's retainer contribution reaches `2.012x` and `2.533x` its peak-forcing ceiling scale. Exact common endpoints follow algebraically from balanced pairs and resets. These are **finite numerical findings for one column**, not a robust dimension theorem. Their normalized selected-gradient signals are approximately `2e-12` at `n=1e12`.

| Target | Verdict | Qualification |
|---|---|---|
| Repairs from Step 3.6 | **PASS** | Targeted inspection confirms withdrawals and scope repairs; earlier audits were not repeated wholesale. |
| C1: Lemma 11.2 | **PASS in the section's positive-reference scope** | Its isolated assumption list and CHECKS summary omit the necessary lower bound on `rhat`. Negative references give a counterexample. |
| C2: Theorem 11.3; Cor. 11.4 | **PASS** | Exact adjoint/Abel proof; no extra multiplier `P` or `T` outside the stated norms and variation. |
| Cor. 11.5 | **PARTIAL** | Constant `Fext` **and bath**: PASS. Signed-monotone factor two: FAIL. |
| C3: Proposition 11.6 | **PARTIAL as worded** | Finite operator gains independently interval-certified; unbounded peak gain and asymptotic tightness require explicit joint parameter limits. Published `.9` largest-group mass does not fit the physical off-cycle block. |
| Staircase `O(log n)` discussion | **PARTIAL / scoped analysis** | Fixed geometric group ratio already gives a logarithmic cardinality limit. The resource derivation needs its stated retention premises and does not constrain all mechanisms. |
| C4: Proposition 11.7 | **PASS** | Exact split and Gamma/variation bound, common query; nonzero initial/capture terms retained. Different queries require an additional terminal term. |
| Example E | **PASS as a raw population functional** | Numbers reproduced independently. `chi=1` is not the claimed one-step legal off-cycle query; actual legal-query values are also reported below. Dense persistence has a perturbation argument. |
| Specific Theorem 4 joint zeros controlling Gamma | **OPEN** | Example E is not at those zeros. Small forcing difference is not zero forcing difference. |
| C5: legal staircase | **PARTIAL, positive numerical result** | Legal matched-endpoint histories realize amplification at large virtual `n`. No universal legal construction theorem, robust section, or linear-dimensional memory claim. |
| C6: Gamma versus input cost | **PARTIAL** | A rigorous gate-energy and square-root-time bound passes. A natural horizon-free input-difference bound is refuted. A dimension-useful bound in terms of actual `mT` remains OPEN. |
| Original dense, full-fixed-feature, `D=Omega(n)` at `mT=o(n^(3/2))` | **OPEN** | No complete proof or counterexample under that contract. |

## 1. Sources and mathematical contract

Read [PROOF.md](../claude_remaining_channels_20261020/PROOF.md) §§R3, 11 and their dependencies, [REPORT.md](../claude_remaining_channels_20261020/REPORT.md), [CHECKS.md](../claude_remaining_channels_20261020/CHECKS.md), `filtered_check.py`, its outputs, and the targeted repair records. Definitions of the credit, source feature, metric, dense recipe, and protected-set scope were cross-checked against the inherited contract and the three earlier independent audits. Those audits are preserved; earlier passed results are used only in their verified scopes.

The physical model remains `h_t=tanh(R h_(t-1)+x_t+.05)`, zero initialized, `|x|<.5`. The resource is **peak actual input support times complete horizon**, not additive support. The prescribed dense matrix obeys `R=alpha(R0+eta*11^T/n)`, `eta<=1e-8/n^2`, `||R||=a=1-1/n`, and `||R-R0||<=3 eta`.

The scalar-column population equation is

\[
y_t=M_ty_{t-1}+F_t^{ext}\mathbf1+c_t^{cap},\qquad
M_t=\operatorname{diag}(r_t)-\epsilon\mathbf1(r_t-\hat r_t\mathbf1)^T,
\]

where `r=a*g`, `rhat=a*ghat`, `eps=gamma/k>0`. The vector denoted `c` in §11 is **capture**, not the scalar source-feature coefficient also called `c` elsewhere. All outside-population contributions, including injection and front effects, belong to `Fext`. That force may itself depend on the full recurrent history. The theorem is a pathwise bound; it does not prove that force is exogenous or cheap to specify.

Physical off-cycle populations satisfy `P<=k/2-1`, stronger than `eps*P<=1` in the abstract operator theorem. `P<k/gamma` and `eps*P<=1` are not literally equivalent at equality; the lemma genuinely extends to the equality boundary.

## 2. C1 — independent sliding-box derivation

Let `p` be the terminally propagated adjoint, `pi=sum p_i`, `M=max(0,max p_i)`, `m=min(0,min p_i)`. One step is

\[
p_i'=r_ip_i-\epsilon(r_i-\hat r)\pi.
\]

If `0<=eps*P<=1`, then `m<=eps*pi<=M`. Direct subtraction gives

\[
M-\epsilon(1-\hat r)\pi-p_i'
\ge(1-r_i)(M-\epsilon\pi)\ge0,
\]

\[
p_i'-[m-\epsilon(1-\hat r)\pi]
\ge(1-r_i)(\epsilon\pi-m)\ge0.
\]

For `0<=rhat<=1`, the proposed upper endpoint is nonnegative and the lower endpoint nonpositive, so clipping at zero preserves both inequalities. Backward summation yields

\[
S_t=\sum_{u>t}\epsilon(1-\hat r_u)\pi_u\in[m_T,M_T],
\quad p_i^{(t)}\in[m_T-S_t,M_T-S_t].
\]

In particular `||p^(t)||inf<=Rchi=M_T-m_T<=2A`. This argument uses neither homogeneous nor stationary gates. The population operator need not have nonnegative entries; the proof is an interval argument for the adjoint, not positivity of `M_t`.

**Scope corrections.** Section 11 explicitly assumes `rhat in (0,1)`, which is sufficient. The isolated Lemma 11.2 list says only `rhat<=1`, and CHECKS claims only `rhat<1`: those literal weaker lists are false. With `P=1,eps=1,p=1,r=1,rhat=-1`, `p'=-1`; its clipped maximum is zero but the claimed upper bound is `-1`. This is outside the section's intended positive-bath scope and does not refute the RNN theorem. State `0<=rhat<1` explicitly. Likewise `eps*P>1` fails: `P=2,eps=.6,p=(1,1),r=(0,0),rhat=.5` gives next clipped maximum `.6` versus claimed `.4`.

[operator_audit.py](operator_audit.py) checks 561 backward steps in 72 independently generated exact rational cases, including equality `eps*P=1`, exact zero gates, `1e-12` gates, anti-holes, varying baths, signed queries, initial content and captures. The row interval, accumulated box, and adjoint identities hold exactly. Boundary `rhat=0` is included. Negative-reference and excessive-population failures are explicitly labeled outside the valid scope.

## 3. C2 — variation ceiling and corollaries

Unrolling the actual population equation gives exactly

\[
\chi^Ty_T=p^{(t_1)T}y_{t_1}
 +\sum_t\pi_tF_t^{ext}+\sum_t p^{(t)T}c_t^{cap}.
\]

The normalization must use the same history and bath as the adjoint:

\[
\phi_t=F_t^{ext}/[\epsilon(1-\hat r_t)].
\]

Since `eps*(1-rhat_t)*pi_t=S_(t-1)-S_t`, summation by parts yields

\[
\sum_t\pi_tF_t^{ext}
=\phi_{t_1+1}S_{t_1}+\sum_{t=t_1+1}^{T-1}(\phi_{t+1}-\phi_t)S_t.
\]

There is no omitted terminal term: `S_T=0`. The sliding box proves the displayed Theorem 11.3 with coefficient `A=max(M_T,-m_T)` and remainder coefficient `Rchi`. Taking `chi=sign(y_T)` proves the filtered L1 form. Corollary 11.4 follows by subtracting the individually retained initial and capture terms, each bounded by `A` times its L1 input budget.

**No hidden multiplicative P or T appears in this proof.** However, `V(phi)` and the explicit L1 initial/capture norms can depend on both. Summing a per-row result while forgetting multiplicities would be incorrect; the independent grouped simulator retains exact integer counts throughout.

### Corollary 11.5: what passes and what fails

- Constant `Fext` **and constant bath** give constant `phi`; the transient bound passes for arbitrary time-varying heterogeneous gates and anti-holes. Constant `Fext` alone is insufficient when the denominator varies. The main PROOF statement includes both assumptions; REPORT's shorter “constant forcing” summary should too.
- The signed-monotone claim is false:

  \[
  \phi=(-1,+1),\quad V(\phi)=|-1|+|1-(-1)|=3>2\max|\phi|.
  \]

  Generally, for monotone signed `phi`, `V<=3 max|phi|`; factor two holds if the sign is fixed. This is not merely a loose certificate: the two-stage operator staircase with monotone `phi` from `-C` to `+C` produces gain above two. A physically fitting abstract population also does so.

The author's complete `filtered_check.py` was rerun unmodified from an audit-local copy with its original helper copied beside it. It passed and reproduced all outputs; elapsed time was about 473 seconds, at most four BLAS threads. Passing these tests does not repair the false monotone inequality, which the script never asserts.

## 4. C3 — staircase reconstruction, certificates and limits

The independent calculation does not call Claude's staircase function. Constant stages are first evaluated by binary doubling of a matrix/geometric-series pair. A second implementation uses closed scalar mean/contrast equations with **60-digit outward intervals**.

For one stage, let `N` be the number of holders, `m` their weighted mean, `b=eps*(a-rhat)*N`, `lambda=a-b`, and `m*=f/(1-lambda)`. Then

\[
m_L=m_*+\lambda^L(m_0-m_*),\quad
y_i(L)=a^L[y_i(0)-m_0]+m_L\quad(i\text{ held}).
\]

An unheld bath class obeys

\[
y_i(L)=\hat r^Ly_i(0)+(1-a)m_*\frac{1-\hat r^L}{1-\hat r}
-b(m_0-m_*)\frac{\lambda^L-\hat r^L}{\lambda-\hat r}.
\]

These formulas independently include bath content before joining, finite stage settling, `a<1`, and integer group sizes. For the published square dimension, `eps`, `a`, `rhat`, counts and lengths are rational; interval exponentiation encloses the large powers without simulating the horizon.

| K | Interval-certified gain / peak phi, rho=20, n=2e12 |
|---:|---:|
| 1 | 2.808254852189018 |
| 2 | 4.616985516496961 |
| 3 | 6.425288604378827 |
| 4 | 8.233505471731290 |
| 5 | 10.03993203246116 |
| 6 | 11.81110700661175 |
| 7 | 13.04157155895864 |
| 8 | 13.04841730586371 |

At `K=3,rho=200`, gain is `6.932631928316740`, or `.99037598976` of variation. The floating doubled-matrix evaluation drifts from the interval result by about `2e-5` at `K=8`; that is numerical conditioning over a huge horizon, not a theorem violation. Published coarse values pass.

### Required qualifications

1. **Physical population.** Published `eps*N_K=.9` and `rho=20` give total mass about `.9474`, exceeding the physical off-cycle capacity of about `.5`. This is permitted by the abstract theorem but is not that original RNN population. Rescaling the largest mass to `.4` fixes the capacity issue and retains similar gains. For example, the independent `.4` calculation gives about `2.80827` at `K=1` and `6.42532` at `K=3`.
2. **Fixed-n saturation.** The first-stage length grows exponentially in K. At K=8 the horizon is about `9.60e13`, much larger than `n=2e12`; attenuation `a^T` prevents indefinite growth. Larger K requires larger n. An independent physically fitting interval example at `n=2e24,K=10` gives gain `19.08349850425`.
3. **Fixed settling error.** The statement “ratio tends to 1 as rho grows” needs a settling-time limit too. In the ideal `a->1`, K=1, rho->infinity limit, with largest mass `b=.9` and settle 8, put `q=exp(-8)` and `q1=(1-.9*.0025)^3556`. The gain tends to

   \[
   3-2q-2q_1+(1-.9)q q_1=2.998664846178466\ldots,
   \]

   whose ratio to three is `.999554948726...`, strictly below one. [asymptotic_checks.py](asymptotic_checks.py) encloses this outwardly. Integer stage rounding is included in `q1`.

**What is defensible asymptotically:** for each fixed K, take sufficient hierarchy, sufficient settling, and n large enough that all counts are positive integers and `T/n` is negligible. Old classes then retain their signed contents while each dominant new class takes almost the entire common-mode swing. The first class carries approximately C and the K new classes approximately 2C each. This verifies the ideal limiting mechanism and rules out a universal peak-only operator bound. It is not an all-K theorem at the fixed published dimension or an automatic legal forward realization.

### O(log n) cost discussion

For fixed geometric ratio `rho>1`, positive integer sizes already force `rho^K<=N_K=O(n)`, so this fixed family has `K=O(log n)` regardless of budget. The resource calculation additionally assumes a hypothetical realization that maintains the claimed near-unit gates, includes the full first-stage/preparation time in T, and legitimately applies the protected-set lemma. That lemma has a small-width premise; the published continuous-hold widths violate it. A rigorous cost argument must split off the already-wide case before invoking the lemma in the small-width case. This is a fixable scoped analysis, not a proved universal logarithmic amplification ceiling. No result here restricts nongeometric or different mechanisms to logarithmic gain.

## 5. C4 — kernels, queries and legal Example E

Applying the exact adjoint identity to both histories proves the displayed forcing/kernel/initial/capture split. Duhamel's formula for the same force under two operators gives

\[
K=\sum_s p_+^{(s)T}(\Delta r_s\odot z_{s-1})
-\epsilon\sum_s\pi_s^+(\Delta r_s-\Delta\hat r_s\mathbf1)^Tz_{s-1}.
\]

The first part is at most `Rchi*Gamma`; the second is Theorem 11.3 with normalized force `psi`. The stated crude variation bound follows from `V(psi)<=2 sum|psi|`. This proof keeps bath differences. It also keeps the complete initial and capture terms outside K, as required.

For **different** terminal queries add `(chi_plus-chi_minus)^T y_minus_T` after doing the split with common `chi_plus`. Matched endpoints and one common frozen legal future query give a common chi, so the proposition's scope is appropriate. Independent numerical tests include different queries and verify this extra term; the proposition does not claim it can be dropped.

### Independent Example E reproduction

The new class simulator uses two balanced retainer classes, explicit cycle-front transport, and no imported author module. At `n=16384,T=3000,P=2000`:

| Quantity | Independent value |
|---|---:|
| raw population-sum readout difference | -2039.315908455118 |
| forcing-difference term | 79.58007798626248 |
| kernel term | -2100.181421801755 |
| capture term | -18.71456463962241 |
| Gamma | 6413.507447126573 |
| kernel bound | 9071.093254135058 |
| actual peak width, both histories | 2001 |
| full mT | 6003000 |
| maximum actual input | .4483740331444822 |

Both histories drive exactly the same rows and times. One holds the retainers at zero; the other holds equal numbers at `+.38` and `-.38`. The differences are zero-sum off-cycle vectors, which remain confined to those rows. The final common target zero resets them exactly. Floating-point endpoint agreement is only a diagnostic, not the equality proof.

**Metric qualification:** `chi=1` on the population is a raw functional, not the one-step legal off-cycle weight (whose bound is about `.3435` in the relevant regime). The theorem allows arbitrary chi, so the identity remains valid. A valid legal gate-box query gives retainer contribution `535.16894`; the same query's **full selected-column** readout is `-678.45116`, normalized magnitude `.00146282`. These are different quantities. No robust D-dimensional section follows.

At `n=1e8` the same fixed P,T example satisfies the small-width and small-budget conditions; the kernel term is `-.56587135`, with forcing term about `-1.1e-8`. This verifies persistence of the phenomenon, but not uniform own-sized strength at fixed population as n grows.

### Prescribed dense recurrence

The endpoint argument remains exact for the prescribed rank-one dense recipe: the difference vectors have zero sum, so `R Delta h=alpha R0 Delta h`. Actual inputs on the same driven set are recomputed from the desired targets; no dense inverse correction or hidden support is used.

[dense_bounds.py](dense_bounds.py) uses the actual recipe's bound `eta<=1e-8/n^2`, not a convenient replacement matrix. For fixed sparse target histories, projection onto controlled targets and tanh contraction give `d_t<=3 eta*t*sqrt(n)`. With `c<=2,sigma>=.049`, the skeleton-column error is bounded by

\[
E_B\le12\eta\sqrt n\sum_{t=1}^Tt^2+100\eta\sum_{t=1}^Tt.
\]

For Example E, two-history population-readout error is at most `.04638`. A deliberately loose pure-response perturbation bound, using measured `max|Fext|<.01`, bounds kernel change by `275.39`, so the large kernel contribution persists. The raw actual-dense full-query perturbation bound is `.13191`. These are exact rational **perturbation calculations around the numerical reference history**; the entire reference trajectory has not been interval-enclosed. They establish substantial perturbative slack, not a new universal dense-memory theorem.

### What listing zeros do and do not imply

The algebra refutes dropping K merely because forcing or tails agree. Listing every gate difference and bath difference would force Gamma=0, but costs many coordinates. Equal public support alone does not force equal kernels.

Example E has **nonzero** forcing difference and has not been placed at Theorem 4's complete joint listing zero. Thus it does not prove that those particular zeros cannot control Gamma, nor prove a dimension lower bound for a kernel listing. That remains OPEN. The exact identity specifies the missing obligation; it does not solve it.

## 6. C5 — a legal matched-forcing staircase

### Design and why it differs from the author's unsuccessful pulse test

Use common nested off-cycle holds and a balanced source pair `(j,j')`. Before holding stages, the source pair is held at zero to accumulate ordinary source credit. During each stage choose the two source-pair gates so that the **measured complete normalized external forcing difference** is exactly a prescribed level `+/-100`, alternating between stages. This includes front effects and injection; it is not matching only the source's own credit.

At each step the current front/bath gates and previous credit are known. Writing the source-pair contribution as

\[
F_h^{ext}=-\epsilon(A_hg_h+B_h),\quad
A_h=V_h(j)+V_h(j')+c_{source},
\]

where B contains the front term minus `ghat*(V(j)+V(j'))`, start with both source gates one and reduce only the appropriate history's gate to solve

\[
A_+g_+-A_-g_-+B_+-B_-=-(1-a\hat g)\phi_{target}.
\]

Then set the physical source states to `(+sqrt(1-g_h),-sqrt(1-g_h))`. All implemented gates remain in `(0,1]`, with minimum about `.9997`. Exact zero-sum balance makes the bath and population forward states common. The final source reset gives exactly common endpoints. Inputs are constructed offline at the nominal model and frozen under differentiation; no derivative of this control-design computation is included.

This uses small continuous source modulations rather than short high-amplitude pulses. It avoids the enormous normalized-forcing spikes in the author's test. The whole preparation and stage horizon counts in mT.

### Results

| n | stages | T | physical P | mT / n^(3/2) | L1 / max Delta phi | legal retainer readout / (A max Delta phi) |
|---:|---:|---:|---:|---:|---:|---:|
| 1e8 | 2 | 27775 | 20997030 | .583193 | 2.315760 | 2.011900 |
| 1e12 | 2 | 27775 | 209999703016 | .00583274 | 2.315916 | 2.012238 |
| 1e12 | 3 | 64951 | 216666360253 | .01407270 | 3.044170 | 2.533122 |

For the three-stage case:

- actual peak width `m=216666360255`, including the source pair;
- full `mT=14072696764922505`;
- inputs below `.057683`;
- forcing-level matching error below `5.9e-9` in floating arithmetic;
- population L1 difference `304.4170`, versus variation `500.000064`;
- kernel term zero because population gates are common; Gamma zero;
- signed capture contribution about `2.12e-5`;
- selected full-column response to the same legal retainer-optimized query has magnitude `69.4441`, normalized `2.4532e-12`.

**This is a legal numerical realization of constant-factor staircase amplification**, not merely an arbitrary operator run. It is not an interval-certified complete construction theorem. Three smaller full-vector replays independently verify state/credit transport, external forcing, inputs, endpoints, and the legal query calculation, with errors around `1e-12` or less. The reduction retains the entire unwrapped cycle front; it does not truncate relaxed rows or approximate a large array by a short one.

These wide runs are outside `(H)`'s small-width premise; Theorem 11.3 itself does not require that premise. All controlled groups fit the actual off-cycle block. An initial attempted three-stage parameter choice exceeded that block and was rejected by the simulator before execution; the final largest mass `.3` gives total mass about `.4333`, which fits.

For the `n=1e12` two-stage run, rational dense perturbation bounds give population-readout error below `7.9e-7` and uniform Delta-phi error below `.000639` when replaying the same physical targets under the prescribed dense recurrence. Balance and input sparsity remain exact. This supports dense persistence with a large margin, subject to the stated numerical-reference limitation. We did not silently simulate a different dense matrix.

**Capacity limitation.** Level 100 and the horizon are fixed in these comparisons, so normalized signal decays like `1/n`. The large width also multiplies **all** preparation time. Raising source credit to order n would require correspondingly longer preparation; it cannot be counted at the earlier narrow width separately. No robust sphere section or growing family of independent directions was constructed. The observed improvement from K=1 to K=2 does not establish an all-K legal gain law.

## 7. C6 — rigorous upper bound and an obstruction to input-difference normalization

### A valid bound for the original prescribed dense recurrence

Tanh is 1-Lipschitz and `||R||=a`. With `d_t=||h_t^+-h_t^-||_2`,

\[
d_t\le a d_{t-1}+\|\Delta x_t\|_2,
\quad \|\Delta r_t\|_2\le2a d_t.
\]

Consequently, putting `Z2=max ||z_(t-1)||_2`,

\[
\Gamma\le2a\sum_t\|z_{t-1}\|_2\sum_{v\le t}a^{t-v}\|\Delta x_v\|_2
\le2a Z_2\min(T,n)\sum_v\|\Delta x_v\|_2.
\]

This is rigorous and includes common-field propagation, all coordinates and relaxations. Since the union of two actual supports has size at most 2m, `||Delta x_v||_2<=sqrt(2m)` gives a crude resource-related upper bound. It is far too weak to yield the desired listing or dimension bound. The bath-difference part has the analogous estimate using `|Delta rhat_t|<=2a d_t`.

The last bath estimate requires the reference gates to come from the same actual bath coordinate (or a separately controlled comparison). It is not available for two arbitrarily chosen nonautonomous references. The Gamma estimate itself has no such extra premise.

### Stronger bound: gate-difference energy

A sharper independent inequality removes the linear horizon factor. For scalar preactivations `u>v`, let `d=u-v`, `h=tanh(u)-tanh(v)`, and `g(s)=sech^2(s)`. Weighted Cauchy--Schwarz gives

\[
[g(u)-g(v)]^2\le\left(\int_v^u(1-g)\right)
\left(\int_v^u\frac{(g')^2}{1-g}\right)
=4(d-h)\int_v^u g^2\le4(d-h)h\le2(d^2-h^2).
\]

The quotient at zero uses its continuous extension. Summing over physical coordinates and times, writing `q_t=R Delta h_(t-1)+Delta x_t`, and telescoping the state energy gives, for common initialization,

\[
\sum_t\|\Delta g_t\|_2^2
\le2\sum_t(\|q_t\|_2^2-d_t^2)
\le2\left(\sum_t\|\Delta x_t\|_2\right)^2.
\]

For the last inequality, `sum(a^2 d_(t-1)^2-d_t^2)<=0`, and `d_(t-1)<=sum_(v<t)||Delta x_v||_2`; the cross terms plus squared inputs are bounded by the square of the total input norm. Arbitrary common maintenance inputs cancel from the preactivation difference, so they do not invalidate this proof.

Thus, with `L_delta=sum||Delta x_t||_2`,

\[
\boxed{\Gamma\le\sqrt2\,a L_\Delta
\left(\sum_t\|z_{t-1}\|_2^2\right)^{1/2}
\le\sqrt{2T}\,a L_\Delta Z_2.}
\]

This is valid for the original prescribed dense recurrence, as well as R0, independently of public supports and protected sets. It is a rigorous upper bound, **not** a completed cost/dimension theorem: the response's spacetime energy still needs control. [energy_bound.py](energy_bound.py) independently stress-tests the scalar inequality at 90-digit precision and the vector telescoping/weighted Gamma bound in 40 contractive recurrences. These tests support the analytic derivation; the proof is the displayed calculation.

### No universal horizon-free bound using only differences of inputs

Consider the natural candidate

\[
\Gamma\le C\, Z_\infty\sum_t\|\Delta x_t\|_1,
\quad Z_\infty=\max_{t,i}|z_t(i)|.
\]

This was **not** asserted by Claude; it is an independently tested C6 candidate. It is false with a universal C.

Hold a source row at zero in both histories. Hold two off-cycle retainers at zero in history plus. At one step put the minus retainers at `(+u,-u)`. Afterward apply **the same maintenance inputs** to both histories for `H=floor(1/u^2)` steps, then reset both to zero. The minus pair obeys `v_(t+1)=tanh(a'v_t)` with exact opposite signs, while the plus pair stays zero. All other forward states agree, including for the prescribed dense matrix. Only the initial kick and terminal reset differ in input:

\[
\sum_t\|\Delta x_t\|_1=2\operatorname{atanh}(u)+2a'v_{last}\le5u\quad(0<u\le.1).
\]

Actual peak width is three and the full cost is `3*(warm+H+1)`, because common maintenance inputs count.

For a rigorous asymptotic obstruction, first fix u,H and let n grow. The bath tends to `s0=tanh(.05)`, source coefficient is one after initialization, and the scaled minus pure response `w_t=-k z_t` obeys during the retention interval

\[
w_t=(1-v_t^2)w_{t-1}+f_t,
\quad f_t=1+s_0^2(t-2),\quad v_{t+1}=\tanh v_t.
\]

Population feedback is lower order because P=2. Front contributions vanish in this fixed-time limit, by the same explicit finite-front induction used for the earlier autonomous example; here the extra controlled rows are finite and their sum difference is zero.

For `u<=.1`, `tanh v>=v-v^3/3` and Bernoulli's inequality imply `v_t>=2u/3` through H steps. Products of `1-v_t^2` over at most H steps are at least `(1-u^2)^H>1/3`. For H sufficiently larger than the fixed warm-up, the last half of the positive response is at least a fixed fraction of its terminal peak: using only the last H/4 forcing terms gives `w_t>=w_T/192`. Thus

\[
\Gamma/Z_\infty\ge c H u^2\ge c'>0,
\]

where constants are independent of u. Dividing by the input-difference sum gives a lower bound of order `1/u`. Take n sufficiently large after each fixed u,H; this is not an unjustified simultaneous limit. The same argument applies as `a'=alpha*a->1` in the prescribed dense recipe. Exact endpoints, legal small inputs and actual support remain satisfied.

Finite checks at `n=1e12`:

| u | T | mT | Gamma / (Zinf sum input-difference L1) |
|---:|---:|---:|---:|
| .1 | 131 | 393 | 2.62 |
| .05 | 431 | 1293 | 3.99 |
| .025 | 1631 | 4893 | 6.44 |
| .0125 | 6431 | 19293 | 11.28 |

The absolute gradient signals are tiny; this is a counterexample to an auxiliary normalization, not a memory-capacity improvement. It does **not** refute a bound that charges actual maintenance cost mT. The protected-set theorem cannot replace that cost by only times at which the two histories' inputs differ.

For this two-row family, the input L1 versus L2 and response infinity versus L2 norms differ only by fixed factors. Its `1/u` growth with `T~1/u^2` shows why a time/response-energy factor such as the square-root-time factor in the valid bound cannot simply be deleted.

Likewise per-history normalized forcing variation cannot be bounded purely by input cost with no baseline term: the zero-input autonomous history already has nonzero variation. A centered/difference bound may avoid that simple obstruction, but must still handle kernel variation and retained source credit. A sharp, useful Gamma or variation bound in terms of actual cost remains OPEN.

## 8. Verification, reproducibility and preservation

Independent code:

- [operator_audit.py](operator_audit.py): exact rational box/Abel tests, independent kernel tests, binary stage evaluator and closed-form outward interval staircase certificates.
- [legal_class.py](legal_class.py): exact unwrapped class reduction, independent Example E, small-input Gamma counterexample, matched-forcing legal staircase.
- [full_crosscheck.py](full_crosscheck.py): full physical Householder/permutation replay, with independent input and query calculations. Complementary optimal retainer queries can tie; both actual full-query values are checked rather than treating a floating tie as an identity failure.
- [dense_bounds.py](dense_bounds.py): exact rational perturbation bounds using the prescribed matrix's guaranteed eta bound.
- [asymptotic_checks.py](asymptotic_checks.py): outward fixed-settling limit and elementary retention/input-budget inequalities.
- [energy_bound.py](energy_bound.py): independent scalar and vector checks of the proved gate-energy and Gamma inequalities.
- [verify_records.py](verify_records.py): source hashes, result consistency, prior-audit preservation and link checks.

Run from the isolated worktree root, with Python, NumPy and mpmath:

```powershell
$a='theory/codex_pr37_step37_audit_20261021'
python -I "$a/operator_audit.py"
python -I "$a/asymptotic_checks.py"
python -I "$a/energy_bound.py"
python -I "$a/legal_class.py" --part kernel
python -I "$a/legal_class.py" --part cost
python -I "$a/legal_class.py" --part stair
python -I "$a/full_crosscheck.py"
python -I "$a/dense_bounds.py"
python -I "$a/verify_records.py"
```

Independent scripts set one BLAS thread. The copied unmodified author script sets four; its full A--F run completed successfully. Its source and helper are copied under `author_comparison/`, so its output-writing behavior cannot modify the research originals. The final three legal staircase runs took approximately 136 seconds in total; the kernel/cost runs and exact checks are small. No large dense arrays at virtual n=1e12 were allocated. The entire cycle prefix is explicit, with only identical off-cycle classes compressed by integer multiplicity.

All results, stdout, and hashes are stored in this directory. Exact rational identities and outward interval certificates are distinguished from floating simulations and analytic asymptotic arguments. Dense perturbation certificates explicitly state their dependence on numerical reference margins. No prior audit, proof, notebook, AGENTS.md, or unrelated workspace file was edited. Nothing was committed, pushed or merged.

## 9. Recommended next task

1. Preserve Theorem 11.3 and Proposition 11.7. Correct the signed-monotone constant, positive-bath scope list, staircase limit wording, and legal-query interpretation of Example E.
2. Independently review the matched-forcing source-control construction, then determine its all-K resource and source-preparation costs. It realizes the qualitative legal amplification missing from Claude's short-pulse test, but has not shown a useful dimension law.
3. Pursue a **cost-aware kernel/forcing listing theorem** that combines the proved gate-energy inequality with a bound on `sum_t ||z_(t-1)||_2^2`, charging common maintenance and source-credit magnitude. Keep bath differences and captures separate. State exactly which odd public quantities vanish at a joint zero and what controls the remaining products. A per-column amplitude bound cannot replace a robust operator/dimension argument across queries and columns.

The original target remains OPEN: robust `D=Omega(n)` directions, exact common endpoints, full fixed-feature gradient metric, prescribed dense recurrence, and `mT=o(n^(3/2))` must all hold in one construction or obstruction. None of the results above supplies that complete conclusion.
