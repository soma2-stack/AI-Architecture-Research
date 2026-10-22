# Independent Step 3.6 audit of PR #37

**Target:** [`18f80054576df5e9c760fb4712c8591bd3e0422e`](https://github.com/soma2-stack/AI-Architecture-Research/commit/18f80054576df5e9c760fb4712c8591bd3e0422e), draft [PR #37](https://github.com/soma2-stack/AI-Architecture-Research/pull/37). Review date: 2026-10-20/21, local overnight run. Author files are unchanged. No subagents, GPU, training, pushing, or merging.

## Executive verdict

The repaired initial-vector theorem and the exact convex representation survive. So do the cost bound and the positive-deviation averaging argument, with the boundary qualifications below. The stationary ceiling is correct for a **constant bath reference**, constant gates, constant external forcing, and zero captures. The setup should explicitly include that constant-bath assumption.

**The major new finding is a counterexample to the proposed unweighted-tail bound (10.6).** No switching is needed. In a legal zero-input history, a large population of ordinary bath rows forgets each forcing increment. Its *unweighted* forcing tail keeps accumulating. For fixed horizon `T` and increasing `n`, the ratio in (10.6) tends to

\[
\frac{\tanh^2(.05)}{2}(T-1).
\]

This defeats any universal constant in the literal **per-history** conjecture. It does not show growing retained signal, robust dimension, or a counterexample to the original memory barrier. The quantity to bound must retain the age weights from Theorem 10.1.

| Claim | Verdict | Exact scope / decisive step |
|---|---|---|
| Step 3.6 repairs | **PASS**, minor presentation defects | Complete initial-vector correction works; counting and forward coefficient repaired; negative drift and dimension withdrawal retained. |
| Theorem 7.5′ | **PASS** | Bounds (a)–(c), fixed off-cycle population, `E<=1/4`, all explicitly defined remainders. Intermediate `.6605` rounding and the counterexample's “exactness” sentence are wrong; displayed theorem constants remain safe. |
| Theorem 10.1 | **PASS** | Exact unrolling and Abel identity for arbitrary gates, arbitrary initial vector, all captures, any query. |
| Corollary 10.2 | **PASS** for its bound | Require integer `1<=W<=L`; at `W=L` the claimed *equality* of old weight is false, but the upper bound is valid. Specify the initial-vector norm. |
| Proposition 10.3 | **PARTIAL as written; PASS for frozen bath** | Its stationary algebra is valid. A nonautonomous bath, expressly permitted in the section's setup, must also be frozen. It does **not** imply (10.6). |
| Proposition 10.4 | **PASS** | Fixed population, `delta>=0`, explicit initial/capture term. Signed external forcing is allowed. This is an undamped absolute-input-budget bound. |
| §10.6 stationary implication and literal Conjecture 10.5 | **FAIL** | A stationary state does not bound its unweighted forcing primitive. Section 6 below gives both an exact scalar example and a legal-history asymptotic counterexample. |
| §10.8 proposed tail-listing implication | **PARTIAL / missing term** | At equal tails, code-dependent retention weights need not agree. This is an unproved research route, not a failed previously established theorem. |
| Growing filtered amplification from switching | **OPEN** | Not found in the targeted legal tests or the adjoint adversarial search. |
| Original dense, full-metric, linear-memory problem | **OPEN** | No new robust section, full-metric upper bound, or dimension theorem was established. |

## 1. Provenance, contract, and scope

Primary sources read: [PROOF.md](../claude_remaining_channels_20261020/PROOF.md), especially §§R2, 7, 10; [REPORT.md](../claude_remaining_channels_20261020/REPORT.md); [CHECKS.md](../claude_remaining_channels_20261020/CHECKS.md); `repairs2_check.py`, `phase2_check.py`, and `exp_pump.py` with its saved results. The two preserved audits are [Step 3](../codex_pr37_independent_audit_20261020/AUDIT.md) and [Step 3.5](../codex_pr37_step35_audit_20261020/AUDIT.md). Relevant contracts were checked in PR #31's [§0](../claude_lemma_m_bus_capacity_20261015/PROOF.md), PR #32's [§0 and two-stream derivation](../claude_lemma_m_rest_20261016/PROOF.md), and PR #35's [§0 and dense structure](../claude_dense_transfer_20261020/PROOF.md); inherited PR #27/#28 dependencies were checked through the source material and previous audit records, without reauditing all earlier theorems.

The skeleton credit is

\[
B'_t=G_t(R_0B'_{t-1}+c_tE),\qquad Y_t=UB'_t,
\quad V_t=aPY_{t-1},\quad a=1-1/n.
\]

Here `E=diag(0,1,...,1)` on the memory block. In particular `B'(0,:)=0` and `sum_i Y(i,:)=0`. Column `j` and the fixed population `Hs` are off-cycle, `j` is outside `Hs`. The source feature is undriven and `c_1=0` under zero initialization. The scalar row `Y(i,j)` is abbreviated `y(i)` below.

Theorems about this skeleton remain skeleton statements when actual forward gates come from the prescribed dense matrix. Dense forward states use `a'=alpha*a`; the credit recursion here continues to use `a`. Actual peak support and the whole horizon determine `mT`. None of these scalar-column bounds upper-bounds the full gradient metric or counts robust memory dimensions.

## 2. Targeted repair verification and Theorem 7.5′

### Complete initial vector

Set `r_t(i)=1-g_t(i)`, `sigma_t=sum_Hs y_t(i)`, `d_t=y_t-sigma_t/P`, and let `omega_0` be the initial spread. Direct subtraction of the row mean gives

\[
d_t=a d_{t-1}-a\{r_t\odot y_{t-1}-\overline{r_t\odot y_{t-1}}\mathbf1\}
 +(\kappa_t-\bar\kappa_t\mathbf1)V_t(0).
\]

The common forcing cancels exactly. The spread recurrence gives

\[
\omega_{\max}\le e^E\left[\omega_0+E(M_*+|\sigma_0|)/P+Q\right],
\]

and therefore

\[
Y_{\max}\le (1+Ee^E)(M_*+|\sigma_0|)/P+e^E(\omega_0+Q).
\]

Unrolling the contrast gives

\[
\|d_T-a^Ld_0\|_\infty\le2E Y_{\max}+Q.
\]

Substitute into `chi^T y_T=chibar*sigma_T+chi^T d_T`, retaining both initial terms. This proves (b) and (c). For (a), the unchanged aggregate bootstrap is

\[
(1-E-E^2e^E)M_*\le Y_{src}+R_e+(E+E^2e^E)|\sigma_0|
             +EP e^E(\omega_0+Q).
\]

The advertised combined coefficients are safe. [algebra_checks.py](algebra_checks.py) encloses `exp(1/4)` by a rational Taylor series with a rigorous positive-tail bound. It verifies the combined factors, not a rounded substitute for the exponential. Thirty independent full-operator trials with arbitrary nonzero initial vectors also check the worst query in the whole box `|chi_i|<=1` by L1 duality; worst ratios for (a),(b),(c) are `0.226944, 0.184525, 0.165927`. These trials are numerical diagnostics, not the proof.

### Two presentation errors that do not invalidate the displayed theorem

1. **PROOF line 1296:**

   `2E(1+E exp(E)) <= .6605` is false at `E=1/4`:

   \[
   2E(1+Ee^E)=0.6605031770859677\ldots>0.6605.
   \]

   Use `.660504` or `.661`. The displayed `.661` and `1.661` already dominate the exact value. Also `2E exp(E)=.6420127083438707...<.643`, so the displayed `.643` and `1.643` are valid.

2. **PROOF lines 1281–1283:** on the old `P=1,E=Q=0` counterexample, `Acq` alone is **not** the total readout. Approximate unscaled magnitudes are

   \[
   |Acq|=6.8514474963\,10^{-9},\quad
   |\bar\chi\Lambda\sigma_0|=6.8524115763\,10^{-9},\quad
   |\chi y_T|=1.3703859073\,10^{-8}.
   \]

   It is the **sum of initial mean and acquired content** that agrees with the total. Moreover `1.8226132658e-8` in `repairs2_check.py` is the older safe `1.33`-coefficient repair bound, not the displayed Theorem 7.5′(c). That displayed bound is about `2.2762110034e-8`. Both bounds exceed the actual value, but the verification record should distinguish them.

[repair_certificates.py](repair_certificates.py) independently encloses the old witness and the new bound by outward intervals, scaling credits by the positive source normalization to avoid a numerical fixed-point substitution. It does not import the author's check.

### Other repairs

- Expanded-window cycle count `1+floor((H+Lam-1)/d)` is correct. The old boundary example gives `2`, not `1+H/d=1.991`.
- The finite saving-factor assertion remains withdrawn. The asymptotic fixed-error statement retains its additive boundary term.
- The dense forward identity correctly uses `a'=alpha*a`; the skeleton credit coefficient remains `a`. **One residual proof typo remains at line 955:** the contained subinterval must have length `a'*s_t/2`, not `a*s_t/2`. The stated consequence uses `a'` correctly and follows with that substitution.
- The negative-drift counterexample is reproduced by interval bounds: drift `<0`, positive integral `>1.6e-6`, inputs `<.5`. The telescoped bath identity is algebraically correct. It gives an average statement, not pointwise positive drift.
- The invalid per-column dimension necessity is explicitly withdrawn. No replacement dimension-counting assumption was smuggled into the new theorems.

## 3. Theorem 10.1: exact representation — PASS

Starting from the full post-gate transformed recursion, independently expanding `UGU` gives, for every off-cycle `i` in `Hs`,

\[
y_t(i)=a g_t(i)y_{t-1}(i)+F_t+\kappa_t(i)V_t(0),
\]

\[
F_t=-\frac\gamma k\sum_{l\ge1}\delta_t(l)V_t(l)-\frac\gamma k c_tg_t(j),
\quad \kappa_t(i)=\frac\gamma{\sqrt k}
\left(\delta_t(i)-\frac\gamma k\sum_{l\ge1}\delta_t(l)\right).
\]

All population feedback is included in `F_t`; broadcast capture remains explicit. No independent-forcing, stationarity, homogeneous-gate, or gate-sign premise is used.

Put `rho_i(u)=prod_{v=u+1}^T a*g_v(i)`. Unrolling and summing by parts gives

\[
\sum_{v=t_1+1}^T\rho_i(v)F_v
=\rho_i(t_1+1)\Psi_{t_1}
 +\sum_{u=t_1+1}^{T-1}[\rho_i(u+1)-\rho_i(u)]\Psi_u.
\]

Every coefficient is nonnegative and their sum is exactly `rho_i(T)=1`. The initial coefficient is `rho_i(t1)`, **not** the first age weight `rho_i(t1+1)`. The proof keeps these indices correctly.

For any query, triangle inequality gives

\[
\sum_u|\Lambda_u(\chi)|\le\sum_i|\chi_i|\sum_u\lambda_u(i)\le AP.
\]

Thus the theorem is valid for every claimed gate history, including anti-holes, and every legal one- or multi-step query (indeed any real `chi`), with initial and capture terms retained. It is not a bound on `Psi*` itself and is not a dimension theorem.

The independent check uses `n=32,k=16,sqrt(k)=4`, so the complete Householder and cycle matrices have rational entries. Twenty-seven row/time identities, all Abel reconstructions, positivity, and unit sums hold **exactly as fractions** with arbitrary initial content and heterogeneous gates. Small `n` is used only for algebraic identity testing. Separate full-vector numerical cross-checks of legal histories are in §8.

## 4. Corollary 10.2: age and input cost — PASS with boundary clarification

Require integer `1<=W<=L`. For `W<L`, the old weight is exactly

\[
\sum_{u<T-W}\lambda_u(i)=\rho_i(T-W).
\]

For `W=L`, the sum is empty and equals **zero**, whereas `rho_i(t1)>0`; replace the equality in PROOF line 1353 with `<=`, or split this boundary case. The advertised upper bound remains valid.

Let `N_i` count actual nonzero inputs on the row in the expanded window for the last `W` steps. The protected-set cost gives

\[
\epsilon_i=\sum_{v=T-W+1}^T(1-g_v(i))
\ge\kappa\,[W-(\mathrm{Lam}+1)N_i]^+.
\]

Therefore rows with `N_i<W/[2(Lam+1)]` have old weight at most `exp(-kappa*W/2)`. For the other rows,

\[
\#\{i:N_i\ge W/[2(\mathrm{Lam}+1)]\}
\le2(\mathrm{Lam}+1)m_W(W+\mathrm{Lam})/W.
\]

The required expanded interval begins at `T-W+1-Lam` and has `W+Lam` integer positions. The author's slightly larger interval defining `m_W` is harmless: its peak bounds the peak on this subset. There is no need to count `W+Lam+1` positions in the proof.

Multiplying by `A` and the relevant tail suprema proves the stated bound. For initial content, a precise version is

\[
\left|\sum_i\chi_i\rho_i(t_1)y_{t_1}(i)\right|
\le A\|y_{t_1}\|_\infty
\{2(\mathrm{Lam}+1)m_W(1+\mathrm{Lam}/W)+Pe^{-\kappa W/2}\}.
\]

The explicit small-width assumption `(H)` and the inherited protected-set lemma matter. A large current tail can be seen by all `P` rows; only **old weighted** content receives this cost restriction. “Only near-exact retainers throughout the interval” is informal: the proof is a cumulative-deficit split with a nonzero residual, not an assertion that every surviving row was always close to a perfect hole.

## 5. Propositions 10.3 and 10.4

### Stationary heterogeneous ceiling

Freeze the bath gate `ghat` as well as the population gates, set captures to zero, and hold `Fext` constant. Write `b_i=1-a*g_i`, `s_tilde^2=1-a*ghat`, `U=sum_i 1/b_i`. Stationarity gives

\[
b_i y_i^*=F^*,\qquad
F^*=F^{ext}-\frac{\gamma a}k\sum_i(g_i-\hat g)y_i^*.
\]

Since `a*(g_i-ghat)=s_tilde^2-b_i`,

\[
F^*=\frac{F^{ext}}{1-\gamma P/k+(\gamma/k)s_{\sim}^2 U}.
\]

Every `b_i>0`; the denominator is at least `1-gamma*P/k>0`. This proves uniqueness and the ceiling. The strict final inequality requires nonzero `Fext` and a nonempty population; for `Fext=0`, use `<=` (both sides are zero).

**Scope defect:** §10 begins with a nonautonomous bath, and Prop. 10.3 only explicitly freezes `g_i` and `Fext`. If `g_i=1` and the bath alternates between two different gates, the common-mode equilibrium would have to satisfy

\[
[1-a+(\gamma aP/k)(1-\hat g_t)]y^*=F^{ext}
\]

for both bath values. With `Fext!=0` this is impossible. Thus constant bath is a necessary explicit stationarity premise, not a transient extension of the formula. The stationary result with that premise **passes**. An “adiabatic” approximation additionally needs a rate/error argument; none is proved here.

The source specialization is valid for the **source-leak forcing alone**, with captures and injection/other leaks excluded from that specialization:

\[
|F^{ext}_{source}|=(\gamma/k)a\delta_j|Y(j)|,
\quad 0\le\delta_j\le1-\hat g,
\quad a(1-\hat g)<1-a\hat g.
\]

It is not an upper bound for arbitrary `Fext` by own source credit.

### Positive-deviation averaging

At end time `v-1`, the exact representation rewrites forced row content as `Phi_(v-1)-Phibar_i`. Hence, with

`theta_v=(gamma*a/k)*sum_Hs delta_v(i)`,

\[
\Phi_v=(1-\theta_v)\Phi_{v-1}+\frac{\gamma a}k\sum_i\delta_v(i)\bar\Phi_i
       +F_v^{ext}+I_v.
\]

For nonnegative deviations the second term is a nonnegative average of older `Phi` values of total weight `theta_v`. In the physical off-cycle population, `theta_v<1`. Include the first step separately (`Phi_t1=0`, no older average); if `theta=0`, define its weighted term to be zero. This closes the small empty-average boundary omission in the written proof.

Induction with absolute values proves the stated L1 forcing-budget bound, even for sign-changing external forcing. Also `|Psi_u|<=2 max|Phi|`. Nonzero initial content and all captures enter `I_v` exactly. This passes; it does **not** bound the output by the peak of the external forcing, nor permit arbitrary changing membership without fixing a union population and accounting for its states. Anti-hole rows must stay external or lose convexity.

Independent tests include signed forcing, nonzero initial vectors, and capture, with averaging identity error `7.2e-15` or less. These are numerical checks of the independently derived identity; the positivity argument supplies the proof.

## 6. Major finding: (10.6) bounds the wrong quantity

**Location:** PROOF lines 1446–1459, especially line 1449 (“Prop. 10.3 proves (10.6) with C=1 for stationary responses”).

### Exact scalar obstruction

Choose every population gate equal to a constant bath gate: `g_i=ghat<1`. Then `delta_i=0`, there is no population feedback, and, with zero initial content and zero captures,

\[
y_t=a\hat g\,y_{t-1}+f,\qquad F_t=F_t^{ext}=f\ne0.
\]

The state is bounded by `|f|/(1-a*ghat)`, but `Psi_0=L*f`. The ratio of the proposed sides with `C=1` is

\[
\frac{P|\Psi_0|}{[k/(\gamma s_{\sim}^2)]|f|}
=\frac{\gamma P(1-a\hat g)L}{k},
\]

that is, **`gamma*P*(1-a*ghat)*L/k`**. For the exact rational case `n=200000000`, `k=100000000`, `sqrt(k)=10000`, `P=1000`, `ghat=399/400`, `L=n/2`, it is

\[
\frac{200000399}{79992000}=2.5002550130013\ldots>1.
\]

The rational script certifies this without iterating `L` steps. Any nonzero force scale, including `f=1/k`, gives the same ratio. As `L` increases the ratio is unbounded. At a stationary initial state the contradiction between a bounded state and a growing forcing primitive is just as clear, but zero initial content avoids relying on an initial-content allowance.

This scalar example diagnoses the mathematical mistake. It does not, by itself, assert an arbitrary prescribed force can be generated by a legal full recurrent history. The next construction removes that qualification.

### Legal-history counterexample family, including the prescribed dense forward model

Use **no actual inputs at any step**, start from `h_0=0`, and take an off-cycle credit column `j`. Let `Hs` consist of `P=k/2-4` other off-cycle rows. All these rows are exactly undriven bath rows; their actual gates satisfy `g_t(i)=ghat_t` and hence `delta_t(i)=0` at every `n,t`. Thus **`Fext_t=F_t` exactly** for this population. The initial credit is zero.

Here is a finite-time asymptotic derivation; all constants in the O-terms can depend on the fixed integer `T`. Take `n->infinity` through multiples of four **after fixing T**, so no cycle wrap occurs. Put `s0=tanh(.05)`, `g0=1-s0^2`.

1. At time `t<=T`, at most `t-1` cycle descendants differ from the bath; all states are bounded by one. Therefore the memory-state sum outside physical row zero is `(k-O_T(1))*s_t+O_T(1)`. The exact common skeleton field

   `J_t=gamma*s_t/sqrt(k)-gamma^2*sum_{l>=1}h_t(l)/k`

   equals `-s_t+O_T(k^-1/2)`. Induction gives `s_t->s0` for every fixed `t>=1`.

2. The front-row preactivation grows as `s0*sqrt(k)+O_T(1)`, so its gate tends to zero faster than every inverse power of `k` for `t>=2`. At `t=1`, the credit injection is zero (`c_1=0`). Source features converge to `s0` at every fixed time `>=1`; their reference normalization also converges to `s0`. Consequently `c_t->1` for `t>=2`.

3. Induct on the exact physical skeleton column: its driven column entry is `O_T(1)`; its other bulk entries are `O_T(1/k)`; its finitely many front descendants are `O_T(1/k)`; and its total physical column sum is `O_T(1)`. To verify the induction, the credit version of `J_t` is `O_T(1/k)`. The front entry before its gate is `O_T(1/sqrt(k))` and is killed by the front gate. Other rows receive their previous entry plus that common `O_T(1/k)` field and the single column injection. This also proves `V_t(0)=O_T(1/k)`.

4. Deviations occur only on the finitely many front descendants. Their `V_t` coordinates are `O_T(1/k)`, except row 1's predecessor, which is `O_T(1/sqrt(k))`. Thus

   \[
   kF_t=kF_t^{ext}\longrightarrow-g_0\quad(t\ge2),\qquad F_1=0.
   \]

   On every population row, `kappa_t(i)=O_T(k^-3/2)` and the capture input is `O_T(k^-5/2)`. Even its **absolute time-and-row sum** is `O_T(k^-3/2)->0`. No neglected capture supplies the missing signal.

5. For the prescribed dense forward matrix, `a'=alpha*a->1`, the additional common forward field has size `<=eta=O(n^-2)`, and the source coefficient also converges to zero as required. The same state-sum and front-gate induction applies. The credit in (10.6) remains the same R0 skeleton with these actual dense gates. In particular undriven off-cycle rows remain exactly equal to the bath, so their deviations are still exactly zero. This is the prescribed rank-one dense recipe, not a replacement matrix.

It follows that

\[
P\Psi^*\longrightarrow\frac{g_0(T-1)}2,
\qquad
\frac{k}{\gamma s_{\sim}^2}\max_t|F_t^{ext}|
\longrightarrow\frac{g_0}{s_0^2}.
\]

For the nonautonomous bath, take the **minimum** `1-a*ghat_t` over the interval to make the proposed right side as large as possible; it has the same limit. Initial credit is exactly zero and both filtered and absolute-input capture allowances tend to zero. The ratio is therefore `s0^2*(T-1)/2`.

Since `s0>.0499` (rational exponential enclosure in `algebra_checks.py`), taking `T-1>1000*C` makes the limit exceed `1.245*C`. For sufficiently large admissible `n` the strict violation follows. This defeats **every** universal `C` in the literal per-history formulation, with either allowed forward matrix. It does not rely on a finite numerical sweep or exchange a simultaneous `T,n` limit. Even a restriction `T<=n/2` is eventually satisfied.

Actual support is zero, source rows are undriven, initialization is zero, and all `(H)` width conditions hold. If a width convention insists `m>=1`, account with `m=1`; then cost is `T` and still below the barrier for sufficiently large `n`. This is not a robust memory section: identical histories have identical endpoints and zero gradient *difference*. No claim about antipodal separation, listing zeros, or dimension follows. If a new conjecture is restricted to **differences at specific joint listing zeros**, this common-background example does not refute that new statement; that would be a different quantified conjecture requiring a precise definition.

### Finite legal checks

The independent simulator measures the actual common forcing, not a surrogate first-order pulse. The following `R0` histories have zero inputs and zero initial credit:

| n | T | P | P Psi* | C=1 scale using minimum bath complement | Ratio | Absolute capture-input budget |
|---:|---:|---:|---:|---:|---:|---:|
| 1e8 | 5300 | 24999996 | 2642.924945 | 399.789041 | 6.610799 | 2.377e-5 |
| 1e8 | 11900 | 24999996 | 5934.739473 | 399.789041 | 14.844678 | 5.608e-5 |
| 1e12 | 5300 | 249999999996 | 2642.887306 | 399.667965 | 6.612707 | 2.376e-11 |

These are finite floating-point evidence supporting the analytic family. The actual **filtered** forcing L1 content is about `199.9`, not `P*Psi*`; it stays below the stationary comparison scale. The universal refutation comes from the fixed-time derivation, not treating these floating-point numbers as interval certificates.

### Smallest useful repair

Withdraw the claimed stationary implication and the universal bound on unweighted tails. Keep Theorem 10.1. Investigate a bound on

\[
\sup_{\chi\ \mathrm{legal}}\left|\sum_u\Lambda_u(\chi)\Psi_u\right|
\]

or the equivalent filtered response, with explicit initial/capture allowances. Alternatively formulate and justify a precisely centered, age-restricted, or joint-listing-zero bound. Simply assuming a population's gates are heterogeneous does not fix the accumulating primitive.

## 7. Additional gap: equal tails do not kill unequal kernels

**Location:** PROOF lines 1524–1528, proposed route to a heavy-column listing.

If a listing makes `Delta Psi_u=0`, the forced readout difference is still

\[
\sum_u(\Lambda_u^+-\Lambda_u^-)\Psi_u
\]

unless those weights also agree (or this term is bounded independently). The gates, retention weights, and potentially the legal-query weights depend on the history. Public support schedules alone do not equate them.

For example, in a two-step scalar recurrence with zero initial content/capture and identical forcing `(F_1,F_2)=(1,0)`, all tails agree. Taking last-step propagation factors `.9` and `.5` produces forced contents `.9` and `.5`. The missing difference is `.4`. These are permissible contraction factors; this is an algebraic counterexample to the inference, **not a claimed legal robust-section construction**. The author's own exact representation exposes the missing term. A valid listing route must list or control kernel variation and capture variation too. This does not invalidate Cor. 10.2's per-history inequality.

## 8. Adversarial experiments and independent implementation

### Legal recurrent histories

[b6_legal.py](b6_legal.py) implements an exact symmetry-class reduction before the first cycle wrap. It extends the method in our previous audit, without importing any author module. It propagates the cycle-front prefix explicitly and groups off-cycle rows only by identical complete control histories. Integer multiplicities represent physical rows, not rescaled surrogate neurons. Virtual `n=1e12` is cheap because only the front prefix and at most sixteen off-cycle classes are stored.

Twenty-seven cases include:

- held controls, bath controls, anti-hole controls at `+/- .38`;
- rapid smooth gate modulation, delayed switches, unequal start ages, mixed reset targets and duty cycles;
- source differences that change sign (pulses in different histories) and longer alternating pulse trains;
- complete histories from zero, plus interval diagnostics beginning at time 500 with nonzero initial credit;
- `n=65536,1e8,1e12`, `T=5300` and `11900`, controlled populations up to `20480000` rows, and large undriven bath populations for the tail test.

Actual peak support, every nonzero input, additive support, and complete `mT` are recorded. Twenty-one cases satisfy both `(H)` and `mT<=2.5e-5*n^(3/2)`; six `n=65536` cases are deliberately below the theorem's dimension cutoff and are structural controls. Exact counts are in [b6_legal_results.json](b6_legal_results.json).

The balanced source pair differs by a multiple of `e_j-e_j'`, which has zero sum and is an off-cycle eigenvector of `O` with eigenvalue one. Common controls elsewhere and exact resets give exact common endpoints algebraically. The full-vector floating-point gaps, up to `9.4e-16`, test implementation agreement; they are not the proof of equality. The numerical experiments use `R0`; the dense statement in §6 is analytic. We do not claim a full-metric dense experimental section.

Every final one-step query is optimized over the legal gate box and frozen when differentiated. The reported centered one-column readout removes the terminal gather spike and retains the correct own subtraction. It is neither the whole gradient nor a robust dimension measurement.

An initial audit-script trial tried a direct `.4 -> -.4` physical target switch, which required input magnitude `.82369` and was **rejected** by the input-legality assertion. The final delayed-switch schedule interpolates over twenty steps; no illegal run is counted as evidence. Final recorded inputs are below `.381`.

Illustrative matched results (`centered readout / peak |Delta Y(source)|`):

| n / controlled P | hold | anti-switch | duty |
|---|---:|---:|---:|
| 65536 / 2048 | .02213467 | .00707766 | .02142794 |
| 1e8 / 2048 | 2.16812e-5 | 5.59580e-6 | 2.10757e-5 |
| 1e12 / 20480000 | 2.14480e-5 | 5.36446e-6 | 2.08421e-5 |

The density-matched `1e8 -> 1e12` comparison does not show growing gain. The longer alternating train at `1e8,P=2048` gives `6.26737e-5` for hold and `1.56763e-5` for anti-switch. This is finite evidence against these particular switching designs, not a universal transient ceiling.

[validate_b6.py](validate_b6.py) separately constructs the full Householder reflection and permutation and propagates every physical memory coordinate at `n=4096`. Six full-vector cases compare actual forcing, external forcing, input counts and query optima. Maximum forcing discrepancy is below `5.1e-15`, query discrepancy below `2.0e-14`, and support/additive counts agree. These small cases verify the algebraic reduction, not theorem-scale memory performance.

### Adversarial bounded-forcing operator search

[switching_adjoint.py](switching_adjoint.py) tests the isolated population operator, **not legal histories**. For each four-class schedule it enumerates all sixteen terminal L1 dual signs, back-propagates adjoints, and chooses the exact worst sign of a bounded external force at every step. This is stronger than testing a few selected source pulses within that subsystem.

Twenty-seven cases use `gamma*P/k=.02,.25,.49`, horizons 8000, fixed bath, fixed heterogeneous controls, fast/delayed switching, staggered ages, mixed periods, and random block patterns. The largest filtered L1 response divided by the stationary comparison ceiling is `0.99994072`; the largest **raw-tail** ratio is `18.63734`. Forward reconstruction attains the calculated adjoint optimum. This again separates a poor tail bound from actual retained amplification.

No new robust dimension scaling is demonstrated. The positive filtered results and the unweighted-tail counterexample are compatible.

## 9. Reproduction and evidence strength

From the isolated worktree root, with Python 3.11, NumPy and mpmath:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
$audit='theory/codex_pr37_step36_audit_20261020'
python -I "$audit/algebra_checks.py"
python -I "$audit/repair_certificates.py"
python -I "$audit/b6_legal.py"
python -I "$audit/validate_b6.py"
python -I "$audit/switching_adjoint.py"
python -I "$audit/verify_records.py"
```

`algebra_checks.py` supplies exact rational identities and constant enclosures plus explicitly labeled numerical tests. `repair_certificates.py` supplies outward interval witnesses. `b6_legal.py`, full-vector validation and adjoint search are numerical experiments; their raw JSON and stdout are saved beside the scripts. The legal-history asymptotic counterexample is a mathematical argument, cross-checked by those experiments.

The author's unmodified scripts were also executed separately from copies in `author_comparison/` so that their output-writing behavior did not modify the source folder:

```powershell
python -I "$audit/author_comparison/repairs2_check.py"
python -I "$audit/author_comparison/phase2_check.py"
```

Both pass and reproduce the published values. The latter's worst 7.5′ ratios are `.0450527,.1832737,.1793450`, row/representation residuals below `9e-14`, stationary direct-solve discrepancy `4.95e-9`, and positive-deviation identity discrepancy `9.68e-14`. These passing scripts do **not** test (10.6). Also `phase2_check.py` caps its nominal population size at 3000, so its advertised sampling “up to .99*k/gamma” does not actually exercise that limit at large `n`; the denominator proof, not that sampling, covers the boundary.

[verification_manifest.json](verification_manifest.json) records source and audit SHA-256 hashes, 27 legal cases (21 within both `(H)` and the small resource budget), 27 isolated-operator cases, six full-vector validation cases, and resolved relative links. All 58 files copied from the two earlier audits agree with their preserved worktrees, either byte-for-byte or solely after CRLF/LF normalization. Git has no tracked or staged diff at the target commit; only this new audit directory is untracked. Author scripts in the comparison directory are byte-identical to the target originals. No author's proof, earlier audit, governance file, or research notebook was edited.

The final legal-history batch recorded 68.4 seconds of elapsed time on this host, using one BLAS thread; exact per-case times are in the JSON. The adjoint batch took about two seconds. The author comparison includes its original 2000 direct stationary solves and is materially more expensive than the independent algebra checks. No large model or dense theorem-scale array was simulated.

## 10. Recommended next research task

1. Correct the small presentation errors, explicitly freeze the bath in the stationary proposition, withdraw the false stationary-to-(10.6) inference, and record the autonomous-background counterexample.
2. State the next conjecture directly for the **filtered, query-weighted** forced response with explicit initial and capture norms. Test bath-only and sign-changing-source controls before investigating a new switch schedule. A tail bound that fails on zero-input autonomous histories should not guide capacity research.
3. Keep the cross-history kernel term in any listing proof. If code-dependent kernels are to be compressed, specify exactly which quantities are listed and how their joint zero controls the remaining product. Only then ask about an operator-norm or robust-dimension bound across columns and queries.

The largest discovery here is a distinction: an accumulated forcing primitive is not retained memory. The exact representation survives, but its very loose supremum cannot be replaced by the proposed damped tail ceiling. Nothing in this audit settles `D=Omega(n)` with `mT=o(n^(3/2))` in the original prescribed dense, full-gradient contract.
