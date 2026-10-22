# Independent audit of PR #37

Target: [`ac759bb3561fe0de6cf2553282d8ebee04018226`](https://github.com/soma2-stack/AI-Architecture-Research/commit/ac759bb3561fe0de6cf2553282d8ebee04018226), stacked on PR #35 `aa47ca5`.
Auditor: Codex, 2026-10-20. No subagents. CPU only, one BLAS thread per process. Original research files were not edited. This directory contains the independent work and copies of the author's checkers used for comparison.

## Executive verdict

**Overall: PARTIAL.** The main new operator identity, its response bound, and the F-step first-order listing argument survive. The broad descriptions of the 2.5× comparison and homogeneous-retention ceiling require corrections. There is no demonstrated counterexample to the original memory barrier, and no proof of that barrier here.

| Claim | Verdict | Independently defensible conclusion |
|---|---|---|
| Proposition R1 | **PASS** | Exact creation formula for off-cycle columns of the actual-gate R0 skeleton, propagated by the true contracting map. |
| Lemma R | **PASS** | The displayed dimension-dependent response estimate; constants 2.27 / 2.33 in the smaller S4 domain, using S4's dimension-dependent bound. The terminal F-step case also needs the inherited nonspike-weight estimate, spelled out below. |
| Corollary R2, displayed inequality with `S'_j` | **PASS** | All-order bound on precisely the specified creation component. |
| Corollary R2's comparison with the old `S_j` / an actual first-order readout | **FAIL as written** | `S'_j` is not `S_j`. A legal, common-endpoint example below has `S_j=0` and a nonzero contribution from the newly included injection. A bound against a signed, possibly vanishing, actual first-order readout does not follow either. |
| Lemma 2.1 | **PARTIAL** | Its argument requires the negative-capture condition listed in its body; the opening quantifier “any `tau'`” does not include that restriction. Theorem M_F uses an admissible tolerance. The near-column offset should explicitly refer to the **arrival** endpoint `d-1`. |
| Theorem M_F | **PASS within stated scope, with a nonfatal proof correction** | The stated listing count and `14 tau/256` bound on the first-order **spike-row** channel, for public envelopes, undriven sources, `n>=1e10`. Replace the false monotonicity assertion about the ceiling by the continuous upper-envelope argument actually used in the checker. |
| Lemma D | **PASS** | Exact one-step homogeneous-set identity. Its interpretation as a scalar damping recursion needs a hole set moving with the permutation and avoiding row 0. |
| Corollary D2 | **PASS within its explicit restrictions** | A bound on source forcing relative to the **damped initial condition**, plus the displayed negative-deviation and remainder terms. Its source content is `Y(j)`, not automatically `O(j)`. |
| Corollary D3 | **PARTIAL** | Identical increments and the weighted-sum reduction pass. The final ceiling needs a zero initial common component or subtraction of the correctly damped baseline. The small numerical values of `A` require nonspike/centered rows. No general own-credit ceiling follows without further control. |
| Lemma 1.3 | **PASS in the inherited below-budget Theorem 4 scope** | The cited bounds are linear in an arbitrary weight cap; an exact rational upper certificate gives `<0.000133346 tau < 1.4e-4 tau`. |
| Proposition 1.1 / nine-term identities | **PASS after disambiguating notation** | Use the own profile in the first display, not `Y=UB'`. The transformed bus identity and all nine path terms hold. |
| Table 1.2, interpreted as nineteen independently bounded terms for every F | **PARTIAL** | It is a useful ledger, not literally nineteen additive summands. The inherited centered coefficient bounds are one-step bounds; their F-step extension is not proved by citing S2. The own-correction allocation must also be charged. |
| Universal heterogeneous-retention ceiling; relay resource law; C3; M_rest; full-metric upper bound | **OPEN** | Finite tests and channel-specific estimates do not prove these statements. |

## 1. Contract and evidence reviewed

Read the target's complete `PROOF.md`, `REPORT.md`, `CHECKS.md`, `STATUS.md`, all four Python scripts and their saved results. Supporting material:

- PR #28 at `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88`: §0, Lemma 1.2′, Lemma 3.4, Lemma 7.3, and Theorem 4, particularly the listing, arbitrary-weight residual estimates and release argument. The original path is absent from this stacked checkout; an exact `git show` copy is preserved under `sources/`.
- PR #31's `claude_lemma_m_bus_capacity_20261015/PROOF.md`: (H), M1, B, C, G1–G4, the nine-term identity and all four parts of Theorem M; its constant checker.
- PR #32's `claude_lemma_m_rest_20261016/PROOF.md`: S0–S6, the two-stream representation, coefficient split, front bound and homogeneous-retention experiments; `colsim.py` and `exp_retention_leak.py` were inspected, not used by the independent implementation.
- PR #35 at the inherited corrected base: contract, actual-input convention, dense skeleton/credit distinction, selected-to-full lower bounds and the scope of the cube-root construction. No new claim against that construction was established by this audit.

The model remains `h_t=tanh(R h_(t-1)+x_t+.05 1)`, `h_0=0`, with actual past inputs in the open cube, peak support `m`, complete horizon `T`, cost **mT**. The selected credit has injection mask `E=diag(0,1,...,1)`. The skeleton `B'` uses R0 and the actual gates and source; it is distinct from actual dense credit `B`. Future preactivations lie in `[.25,.75]`; their physical inputs are not subject to the past-input cube. Realized past and future inputs are frozen when taking parameter derivatives.

These are not upper bounds on the full gradient metric. The dense theorem's selected-to-full **lower-bound** inclusion does not reverse direction.

## 2. Proposition R1 and Lemma R

### 2.1 Exact creation, independently derived

Write `o_t=O_t(j)` for one off-cycle column and `q=gamma/sqrt(k)`. Since `P e_j=e_j`, `U e_j=e_j+q w`, `U w=-w`, and `o_t=g_j(a o_(t-1)+c_t)`, subtraction of `o_t e_j` from the exact transformed credit gives

\[
Z_t=M_tZ_{t-1}+q\{[a\delta_t(j)o_{t-1}+c_tg_t(j)]w
                         +ao_{t-1}U\Delta_t w\},\qquad
M_t=UG_tUaP.
\]

No zero-sum hypothesis on `Z` is used in propagating it. `||M_t||<=a` because U and P are orthogonal and every gate is in `(0,1]`. This is different from treating the shortened row formula as an operator on an unconstrained bus.

The independent full-matrix checks use arbitrary gates, including strong negative deviations, nonzero bus column sums, held off-cycle sets, and more than a cycle of transport. R1's largest absolute residual was `4.87e-14`; the general row formula's was `4.98e-14`. These checks corroborate the algebra, not its universal quantifiers.

### 2.2 Response to w

For `Phi^U=U Phi^st U`, exactly

\[
\chi^T\Phi^Uw=\nu^T\Phi^{st}(u-e_0),\quad
\Phi^{st}e_0=\Big(\prod ag_0\Big)e_0,\quad
Ou=e_1+q w.
\]

Thus, if `t<T`,

\[
|\chi^T\Phi^U(T,t)w|
\le |\nu_0|+\|\nu\|_2\left(g_1(t+1)+q\|w\|_2\right).
\]

Using `|nu_0|<=HI`, `||nu||<=HI sqrt(k)` gives the one-step formula; using `|nu_0|<=1`, `||nu||<=HI^F sqrt(k)<=HI sqrt(k)` gives its F-step version. Arbitrary subsequent relay/feedback gates are included by the contraction, not dropped term by term.

At `t=T`, the one-step formula follows directly from the legal gate box. For an F-step query, the inherited estimate supplies
`|chi^T w|=|chi_0-u^T chi|<=1.18+1=2.18` when `F<F_s`, and contraction gives a bound below 2 when `F>=F_s`. This fills the terminal case not written explicitly in §3.2's F-step proof.

**All-size caution.** The fixed shorthand `g_1<=exp(-207)` alone does not imply a uniform numerical bound after multiplication by `sqrt(k)` for unbounded n. Use S4's stronger estimate

\[
g_1(t+1)\le4e^{-0.0297\sqrt{k}+0.92}\quad(t\ge1).
\]

For `x=sqrt(k)>=sqrt(5e7)`, `x exp(-.0297x)` decreases. The resulting worst-case response bounds are

- one step: rational upper certificate `< 2.269585040 < 2.27`;
- all F: rational upper certificate `< 2.329570191 < 2.33`.

The corresponding 90-digit endpoint evaluations, with the exact square root rather than the coarse rational enclosure, are 2.26958462638 and 2.32956977758.

S4 controls gates from time **2**, which suffices because the first propagation after a creation at `t>=1` is at `t+1>=2`. No claim of front saturation at the zero-initialization step is needed.

The S4 lower-mass arithmetic can also be checked directly: set `x=sqrt(k)`, so `gamma=x/(x-1)` and the front multiplier is `(x-2)/(x-1)^2`. The mass lower bound is `sp >= .014857982 x^2-.025`. Since `x>=7071`, the factor `a(1-1/(x-1)^2)` loses much less than the gap between `.014857982` and `.01485`, and the remaining negative terms are below `.01`. This yields the stated `.01485x-.46` preactivation bound for all sizes.

The independent operator stress test used 200 gate histories, 16 propagation steps each, F=1–8, including front gates `1e-30`, strong anti-holes, and nonsaturated fronts. It tested the explicit gate-dependent bound rather than applying the S4 numerical constant outside its domain. No violation was found.

## 3. Priority finding: what the 2.5× comparison does and does not prove

Location: target `PROOF.md:448–472`, especially `459–461`; related broad descriptions in its Summary and REPORT.

The displayed inequality for

\[
S'_j=\sum_t|\delta_t(j)|(ao_{t-1}+c_t)
\]

is valid. Triangle inequality applied to the response bound proves exactly that. But Theorem M(d)'s budget is

\[
S_j=\sum_t|\delta_t(j)|o_{t-1}.
\]

There is a new contribution `sum |delta| c_t`. Its omission is not a rounding issue.

### 3.1 Legal, exact-common-endpoint counterexample to identifying those budgets

Take **n=100000000**, R0, off-cycle pair `j,j'`, and **T=3, m=2, mT=6**. Sources are undriven and every support set is public. This lies in both (H) and S4's smaller width domain.

1. At time 1, use zero inputs everywhere. Consequently `c_1=0` and `o_1=0`.
2. At time 2, set the pair to `(+.2,-.2)` in history + and `(0,0)` in history −. Other inputs are zero.
3. At time 3, set both pair coordinates in both histories to the same undriven bath value `s_3`.

Balanced differences are supported on an off-cycle pair and have zero sum; `O(e_j-e_j')=e_j-e_j'`. All other coordinates are exactly common at every step, and the reset makes the complete endpoints exactly equal. Actual input magnitudes are below `.253` (computed maximum `.252725487874`), not merely below the bound up to numerical tolerance. Use the uniform legal one-step query `g=HI 1` from that common endpoint.

The pulse can be interpolated continuously by `v(theta)=.1(1+theta)` on the closed interval `[-1,1]`, with pair `(v,-v)`, so this is not an isolated illegal history pair. It is not claimed to be a zero of Phi or a robust section at the research threshold. R2's advertised comparison is for every history, so neither property is needed to test it.

For both histories,

\[
S_j=0:
\quad \delta_1(j)=0,\quad o_1=0,\quad\delta_3(j)=0.
\]

However, their source-specific **new-injection** creation differs at time 2 by

\[
\Delta\xi^{\rm source}_2=-.04\,q c_2 w.
\]

Its readout at time 3 is

\[
-.04\,q c_2\,\chi^TM_3w\ne0.
\]

The independent 90-digit evaluation gives `chi^T M_3 w = -.919149760425...` and contribution `5.2002316514757e-6`. Nonzero is also analytic: in physical coordinates the row-0 term of `(O^T 1)^T G_3(Ou-e0)` is `g_0(1/sqrt(k)-1)`, with `g_0>.97`; the possible positive terms sum to less than `.00015`, and the other terms are nonpositive. Thus the response is strictly negative, bounded away from zero. The failure does not depend on floating-point precision.

This is **not** a counterexample to the displayed `S'_j` inequality: `S'_j` is positive. It is not a claim that the entire first-order channel vanishes: the W-injection part does not. It specifically refutes replacing `S'_j` by the **old own-leak budget S_j**, as the quoted reading does.

### 3.2 Smallest repairs, not applied to Claude's files

- State the existing theorem as a bound against **S′**, an absolute creation budget, not against the actual signed first-order signal.
- Alternatively split the own-leak creation `q a delta o w` from the modulated injection `q c delta w`. For the former alone, the bound `2.33 a q S_j` is proved and is `<2.5` times the corresponding first-order **upper-budget scale** `HI a q S_j`. This still is not a bound on the complete bus or on a possibly canceled direct readout.
- Keep the common forcing and `U Delta w` own-spread term explicit. R1 shows exactly why the latter is not covered by the response-to-w argument.

The unlisted-light-column consequence can retain its conservative 2.5 factor, but needs an extra line. With `L=450001` and integer `N_j>=1`,

\[
ao_{t-1}+c_t\le (2L+1)c_*N_j,
\]

so its comparison to the old **envelope calculation**, rather than its actual S_j value, costs

\[
\frac{2.33}{HI}\left(1+\frac1{2L}\right)<2.479<2.5.
\]

The threshold is reduced by `2.5^(2/3)` if the old light-column residual is to be maintained; the listed heavy-column count increases accordingly. This verifies the useful consequence with the missing injection explicitly paid for. It does not list a heavy column's whole query-dependent time profile.

## 4. Common-mode damping: exact identity versus ceiling

Location: target `PROOF.md:312–387`.

### 4.1 What passes

Summing the full Y-row recurrence over a homogeneous set gives exactly Lemma D. In particular the contribution from members of H is

\[
\left(g_H-\frac{\gamma|H|\delta_H}{k}\right)\sum_{i\in H}v_t(i).
\]

For holes moving with the permutation, avoiding row 0, this is `a(1-mu_t) sigma_(t-1)` with `mu_t=gamma |H| s_t^2/k`. In the actual bath range `0<=mu_t<1`. Fixed off-cycle hole sets meet these transport conditions.

For the positive-deviation source forcing, `gamma |H| delta_j^+/k<=mu_t`, and

\[
\sum_u\mu_u\prod_{v>u}(1-\mu_v)=1-\prod_u(1-\mu_u)\le1.
\]

Factors a only decrease the sum. Negative deviations and all other forcing must remain in the explicit remainders. Thus D2's displayed inequality passes. Notice that its source is the **full transformed credit** `y(j)=Y(j)`, not the local own scalar. Dropping that distinction would make a circular upper-bound argument.

### 4.2 D3's missing initial-condition term

D2 controls

\[
\sigma_T-\Lambda\sigma_{t_1},\quad
\Lambda=a^{T-t_1}\prod(1-\mu_t).
\]

D3 instead defines its acquired part using `sigma_T-a^(T-t1) sigma_(t1)`. These differ by

\[
a^{T-t_1}\left[\prod(1-\mu_t)-1\right]\sigma_{t_1}.
\]

This term is absent from its claimed ceiling. For an exact rational recurrence diagnostic, take `a=1-10^-8`, `mu=10^-8`, `sigma_initial=10`, ten steps and zero subsequent source and remainder forcing. The purported acquired part is

\[
10[((1-10^{-8})^2)^{10}-(1-10^{-8})^{10}]
 =-9.9999985500001\ldots\times10^{-7},
\]

while the new source peak is zero. This demonstrates the algebraic inference error. It is an example in the stated pure-forcing recurrence, **not** a constructed legal full-credit history with all other physical forcing absent. No such full-history counterexample is claimed here.

The correct forcing-acquired readout subtracts **Lambda** times the initial common component. Equivalently assume that component is initially zero; then D2 gives the intended bound. If an undamped baseline is retained, add the displayed initial-condition term.

There are two additional scope requirements:

- `j notin H` is essential, as the proof recognizes: direct injection otherwise breaks identical increments.
- `A=max_(i in H)|chi_i|` is always the appropriate factor. Its quoted `.3435` / `1.18` values apply to **centered/nonspike** rows, not a homogeneous set containing an amplified gather row.

Neither D2 nor D3 proves a universal bound for heterogeneous retainers, anti-hole compensation, captured arrivals, or the full own-plus-bus source feedback. Marking the entire relay mechanism “refuted” is too broad. The source component in §3 is controlled; the rest remains open.

## 5. F-step first-order listing

Location: target `PROOF.md:203–294`.

I reconstructed the proof from the content bounds of PR #31, rather than treating an F-step query as a one-step query.

- Every final cycle row `d-f` has its own path `p_t=d-f-(T-t)`, but its captures receive the **same** broadcast arrival stream `aY_(t-1)(d-1)`. Unrolling does not replace that arrival profile by the gather row's own profile.
- Monotonicity and variation of the arrival profiles remain G1–G2. The positive gate deviation is bounded by `s_hi^2`. The negative-capture telescoping G4 applies along any such path.
- Singleton near listings have zero residual, so they really do scale to an arbitrarily reduced tolerance without inheriting the fixed near-block error.
- For far-short arrivals, adding `ceil(2 ln r/kappa)` contributes at least the needed `r^-1` decay. For far-long arrivals the squared cutoff scales by `r^2`.
- The BV listing count scales by `r^2`; the light off-cycle cutoff by `r^(-2/3)`, hence count by `r^(2/3)`. The ceiling in `N0=max(1,ceil(x))` is used in the correct direction: unlisted integer counts are **strictly below x**.
- Public support envelopes and undriven sources are indispensable to these bounds. The listed quantities depend on the history but their indexing sets do not.

For clarity, near-column offsets in this argument must be `d-1-r_column`, measured from the **arrival own-profile endpoint**, regardless of final f. The phrase “row's path end” at line 214 is ambiguous and should be replaced with that definition. The constants below use the arrival offset, as the inherited far-arrival proof does.

The per-row residual ledger is exactly

\[
0+1/64+1/256+1/256+1/64+1/64=14/256.
\]

With `tau'=tau/sqrt(F_s)`, concatenating all `F_s-1` listings and applying Cauchy–Schwarz gives

\[
\left\|\sum_{f\in Sp}\chi_{d-f}\Delta F1_f\right\|
\le HI\sqrt{k}\sqrt{F_s}\max_f\|\Delta F1_f\|
\le14\tau/256.
\]

The listings are concatenated **jointly**; separate zeros are not being combined. They are query-independent and odd continuous maps. At `F>=F_s`, the exceptional spike set is empty; this does **not** say the whole first-order centered readout vanishes.

### 5.1 Exact constants and a false monotonicity sentence

`independent_math.py` uses rational Taylor enclosures for exp to bound HI. It clears fractional powers in the off-cycle coefficient inequality, and uses a rational upper bound for the short-arrival exponential. The critical results are:

| Quantity | Independent bound | Required bound |
|---|---:|---:|
| Far-long coefficient `c_l` | `< 38962380.072` | `38970000` |
| BV coefficient `c_b` | `< 807233.471` | `810000` |
| Combined quadratic count coefficient | `< 1.722067697e15` | `1.73e15` |
| Off-cycle coefficient | cube-cleared exact rational inequality passes | `1.4e8` |
| Far-short residual / n after the tolerance shift | `<1.563e-59 / r` | `.0566/(256 r)` |
| Negative-capture requirement at n=1e10 | needed `5357.846`; available `7419.180` | passes |

The printed rounded summaries are not the certificate: the inequalities in the script use exact rational values, except the explicitly labeled high-precision diagnostics.

The sentence at line 276, “n/F_s is increasing,” is **false** because F_s is a ceiling. Exact permitted integer dimensions give:

| n | F_s | n/F_s |
|---:|---:|---:|
| 11785591396 | 182 | 64755996.68131868 |
| 11785591400 | 183 | 64402138.79781421 |

This does not invalidate M_F. Use

\[
F_s\le f(n)=1+\frac{\log(1.01\sqrt{n/2})}{r_H}.
\]

Since `f'(n)=1/(2 r_H n)` and `f(n)>1/(2r_H)`, **n/f(n)** increases for every n in the stated domain. Consequently `n/F_s>=n/f(n)>=1e10/f(1e10)`. This is the valid continuous-envelope argument in the code.

Finally, Lemma 2.1's opening quantifier should incorporate its body condition
`HI gamma 1.26 c_* sqrt(n) r <= .0566 n/256`. The proof does not certify arbitrary tiny tau′ without it. Its actual use with `r=sqrt(F_s)` satisfies that condition. No counterexample to Theorem M_F was found.

## 6. Own correction and the nineteen-item ledger

### 6.1 Lemma 1.3

The PR #28 dependencies do permit arbitrary weights with a cap:

- Lemma 3.4's coordinate Cauchy–Schwarz estimate explicitly uses only `nu_max`.
- Lemma 7.3(c)'s coordinate sums multiply an arbitrary cap; it does not require a realizable query.
- The release estimates bound the coordinate sums before inserting the weight cap, so the result is linear in that cap too.
- Spike blocks have a guaranteed reference cap at least HI through the last listed index, since `1.01 HI^Fs sqrt(k)>=HI`. Thus the uniform replacement weight can be charged against that same block error.

At n=1e8, the worst coefficient is

\[
\frac{2.18\gamma/\sqrt{k}}{1.2}\frac{23}{64}
 +\frac{2.18\gamma/\sqrt{k}}{HI}\frac18
 =0.000133344353432\ldots<0.00014.
\]

It decreases with n. These are the inherited **below-budget** Theorem 4 estimates, including its source/release premises; this is not an unrestricted-horizon upper bound obtained solely from (H).

### 6.2 Exact identities and presentation limits

The unambiguous own/bus identity is

\[
\nu^T\Delta(B'-O)=\chi^T\Delta Z+(\chi-\nu)^T\Delta O.
\]

The first display of Proposition 1.1 should therefore use `sum_l nu_l Delta O_l`, or explicitly define a distinct **unit-source own profile** whose Hadamard product with the time-indexed c is O. In §0, Y already means `UB'`; inserting that Y into `Delta(c(.)Y_l)` is not the identity. The proof's intended PR #28 own-profile notation is recoverable, but the overload should be removed.

The independently implemented dense-matrix reference gives maximum absolute errors:

- nine-term reconstruction of rows `d-1` through `d-6`, over more than four cycle lengths: `2.07e-14`;
- exact bus transform for F=1,2,3,7,12: `5.00e-15`.

The ledger includes the own correction; source and dense errors; all six first-order path terms; two feedback terms and front entries; and the two-stream centered decomposition. No missing term was found in these **identities**. Items T17–T19 are scope obligations, not additional summands.

However:

1. S2 is explicitly a **one-step coefficient theorem**. Line 104 and the table cannot simply reuse its numerical `.3435 sqrt(k)+203` bath coefficient as an all-F result. The exact two-stream identity is linear in chi and transfers to F steps; the coefficient estimates must then be rederived with the actual multi-spike set and weight caps. This does not invalidate M_F, which does not use that centered bound, and does not close the open centered channel.
2. The table's “non-bus `31/64`” and final `47/64` totals omit the newly separately charged T8 if the rest-of-bus allocation excludes it. Either keep T8 inside the bus budget, or write a total at most `47/64+0.00014`, plus the displayed small errors. Another option is to bound the combined own readout with chi directly: `nu^T Delta O+(chi-nu)^T Delta O=chi^T Delta O`, and establish the same inherited ordinary/spike caps for that vector. The existing slack remains ample; the displayed itemized allocation needs one of these explanations.
3. Front entries are not exactly zero. To make all-size negligibility claims, retain S4's exponential in sqrt(n), not its fixed `exp(-207)` shorthand.

## 7. Independent E4 experiment

### 7.1 Implementation and legality

`retention_probe.py` imports no author modules. It applies O via **two explicit Householder maps and a permutation**, simulates the forward memory block, and separately evolves an undriven source scalar. It evolves the +/− credit columns with their actual gates, subtracts the local own scalar, then optimizes the **one-column centered readout exactly over the legal one-step gate box**. A scalar box optimum is the maximum of the two sign-selected corners; no heuristic alternating optimizer is required.

The retained test signal is one selected parameter column. These measurements do not claim an operator-norm supremum for every column or every F. We record both transformed centered readout and standard-row total bus readout; neither is silently identified with the other.

Schedule:

- warmup 499 zero-input steps; source pair held from time 500 for H=1800 steps;
- balanced `(+tanh(.38),-tanh(.38))` seven-step pulse at the midpoint in history +, zero pair in history −;
- exact reset to zero immediately after the pulse, continuing the hold;
- release, then gap 3000; total horizon **T=5300**;
- common retainer controls, with homogeneous, staggered starts, staggered stops, duty-cycled hole/free schedules, or 25% balanced anti-holes ramped to absolute state .4;
- additional round-robin single-reset schedules, periods 64 and 256, and no-retainer / one-retainer controls.

The paired differences sum to zero, and a balanced off-cycle pair is an eigenvector of O with eigenvalue 1. Therefore no difference enters another hidden coordinate; after reset all hidden states coincide **exactly**. The implementation uses the shared baseline trajectory and inserts the paired pulse's actual local preactivation correction when checking inputs. Credit evolution still uses both distinct gate histories.

Actual controls are `x_i=atanh(target_i)-(aOh+.05)_i`, not a reference-support convention. Every scheduled nonzero is counted, and peak support times the **entire** horizon is reported separately from additive support. The largest observed input magnitude across all 19 runs is `<.380441`. Queries are implemented by physical future inputs producing preactivations .25/.75 from the common endpoint, and are frozen for differentiation.

All post-release bath gate-integral diagnostics exceed 6.9; the release gap actually suppresses the source's free relaxation. It does not make the final own difference exactly zero, and that residual is explicitly reported.

**Scope warning:** these are legal R0 structural tests at n=16384,65536,262144. They are outside the theorem's `n>=1e8` hypothesis; many widths also exceed `(H)`'s small-width cap. The broad probes' costs are nowhere near the specified small-constant theorem budget. They are not counterexamples to a theorem in that domain. No dense simulation or high-dimensional robust section was claimed.

### 7.2 Results

All entries below are the optimal **one-column centered readout divided by peak absolute own-credit difference**.

| n | Retainers P | Schedule | Ratio |
|---:|---:|---|---:|
| 16384 | 512 | homogeneous | .05700180 |
| 16384 | 512 | staggered starts | .05311862 |
| 16384 | 512 | staggered stops | .02526200 |
| 16384 | 512 | duty cycle | .05647292 |
| 16384 | 512 | anti-holes | .04897031 |
| 65536 | 2048 | homogeneous | .06470274 |
| 65536 | 2048 | staggered starts | .05977113 |
| 65536 | 2048 | staggered stops | .02553123 |
| 65536 | 2048 | duty cycle | .06382996 |
| 65536 | 2048 | anti-holes | .05613344 |
| 262144 | 2048 | homogeneous | .02469513 |
| 262144 | 2048 | staggered stops | .00859859 |
| 262144 | 2048 | duty cycle | .02439177 |
| 262144 | 2048 | anti-holes | .01918586 |

The fixed-P comparison from n=65536 to 262144 decreases; the matched density comparison between the two smaller n increases slightly. Neither supports an unbounded gain. This is a short, structured adversarial search, not an optimization over all heterogeneous histories. The universal ceiling remains **OPEN**.

Controls at n=65536:

- P=0: ratio `.000242128`, m=2;
- P=1 homogeneous: `.000247002`, m=3;
- P=128 duty cycle: `.006390767`, m=66.

### 7.3 Useful positive observation: retain with sparse resets

At n=65536, P=2048, all with the same H and T:

| Schedule | Centered readout | Ratio to peak | Actual peak m | mT |
|---|---:|---:|---:|---:|
| continuous holds | 48.07279 | .06470274 | 2050 | 10865000 |
| one reset / 64 steps, staggered phases | 47.68014 | .06417426 | 34 | 180200 |
| one reset / 256 steps, staggered phases | 42.01433 | .05654846 | 10 | 53000 |

Thus period-64 retains about **99.2%** of this signal with about **60× smaller mT**; period-256 retains about **87.4%** with **205× smaller mT**. This is a meaningful finite efficiency finding, and it argues against estimating retention cost solely by holding every retainer continuously. Periodic redriving was already explored in PR #32; this result extends that mechanism with deliberately staggered support and **peak-width** accounting. It is not a new computational primitive or a demonstrated new asymptotic memory law.

At this n, `tau>=3709.3`, whereas these one-column readouts are below 49. They do not constitute a robust section at the required threshold, much less linear-dimensional memory. Whether sparse redriving changes an asymptotic resource constant or law requires proof and a dimension-aware construction; no such claim follows from this table.

## 8. Reproduced author checks and independent evidence

All three author's verification scripts were executed from copies under `author_runs/`, with one BLAS thread; original outputs were not overwritten.

| Check | Reproduced result |
|---|---|
| `constants_mf.py` | all assertions pass; `c_l=3.89624e7`, BV `2.0341e14`, off-cycle `1.3178e8`, ledger `14/256` |
| `ledger_check.py` | nine-term relative residual <=`3.58e-15`; F-step identity <=`1.17e-14`; D absolute residual <=`2.85e-13` |
| `lemma_r_check.py` | R1 relative residual <=`2.50e-13`; max w-response `.940000506`; max ratio to explicit bound `.728675` |

The author's `exp_relay.py` and saved v2 outputs were inspected, but the full relay sweep was not rerun. It would add substantial repetitive work after the independent E4 tests at the requested larger n. E5's two-Hp, large-Hg sweep and optional E6 on the specific S_K construction were **not run**. They remain optional finite tests; the independent ledger test already includes F-step algebra through F=12, but is not mislabeled as E6 on S_K.

Independent records:

- [independent_math.py](independent_math.py), [math_results.json](math_results.json): exact rational coefficient inequalities, high-precision diagnostics, the legal S-versus-S′ example, ceiling jump and D3 recurrence diagnostic.
- [independent_ledger.py](independent_ledger.py), [ledger_results.json](ledger_results.json): physical full-matrix reference, all path terms, F-step transform and adversarial gate operators.
- [retention_probe.py](retention_probe.py), [retention_results.json](retention_results.json), [retention_large.json](retention_large.json), [retention_resets.json](retention_resets.json): 19 executed E4 configurations and actual-support resource records.
- `source_manifest.json` records target source hashes and the historical PR #28 source. `verification_manifest.json` records audit-output hashes and preservation checks.

Reproduce from the audit worktree:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python theory/codex_pr37_independent_audit_20261020/independent_math.py
python theory/codex_pr37_independent_audit_20261020/independent_ledger.py
python theory/codex_pr37_independent_audit_20261020/retention_probe.py
python theory/codex_pr37_independent_audit_20261020/retention_probe.py --large
python theory/codex_pr37_independent_audit_20261020/retention_probe.py --resets
python -I theory/codex_pr37_independent_audit_20261020/author_runs/claude_remaining_channels_20261020/constants_mf.py
python -I theory/codex_pr37_independent_audit_20261020/author_runs/claude_remaining_channels_20261020/ledger_check.py
python -I theory/codex_pr37_independent_audit_20261020/author_runs/claude_remaining_channels_20261020/lemma_r_check.py
```

Python 3.11.9, NumPy 2.4.6, mpmath 1.3.0. The large E4 set consumed roughly five minutes of elapsed run time in total; the smaller/reset sets roughly two minutes. These were targeted recurrence tests, not model training. Some independent processes overlapped, each with one BLAS thread, staying below four total BLAS threads.

## 9. Research handoff

1. Correct the R2 comparison and distinguish source-specific **creation budget**, pure own-leak component, and actual signed first-order readout. Preserve R1, Lemma R and the displayed S′ bound.
2. State D3 with a zero initial common component or its damped baseline, nonspike retainers and explicit remainder/source-credit scope. Do not use its present wording to kill heterogeneous retention or full feedback.
3. Correct the ceiling monotonicity sentence, qualify Lemma 2.1's tolerance, disambiguate the arrival offset and own-profile notation, and charge the small own-correction allocation.
4. The best next focused mathematical question is an input-cost-aware bound for **heterogeneous, sparsely redriven retention**. Start from the exact dynamics with a bound that permits joins, leaves, anti-hole periods and nonzero initial content, and account for actual peak support. The round-robin data make this more informative than another continuous-hold sweep. Proving only a common-mode ceiling will not settle the query-dependent heavy-column temporal profiles or the own-spread term.
5. Heavy-column listing, `U Delta w` capture, cycle-source relays, code-dependent public-envelope replacement, driven sources and full-metric upper bounds remain separate obligations. Do not declare them resolved by the response-to-w contraction or by finite experiments.

**Original problem:** robust `D=Omega(n)` learning-gradient memory with `mT=o(n^(3/2))` in the original full metric remains **OPEN**. The existing cube-root lower construction and the refutations of earlier overstrong bus/listing claims are preserved. This audit neither proves a new barrier nor refutes the original one.
