# Step 3.5 independent audit — PR #37

**Audited commit:** [`c48640db6b677d52d109827d6d53bb0e2f005acf`](https://github.com/soma2-stack/AI-Architecture-Research/commit/c48640db6b677d52d109827d6d53bb0e2f005acf). Previous audit target: `ac759bb3561fe0de6cf2553282d8ebee04018226`.

Codex, 2026-10-20. Independent worktree; no subagents, GPU, training, pushes, merges, or changes to Claude's files or the previous audit. Every file in this new directory is audit material. The numerical experiments are R0 experiments; they are not silently substituted for a dense full-metric construction.

## Executive verdict

**Overall: PARTIAL.** The original audit findings were substantively repaired. The new **off-cycle deficit-cost theorem** and **zero-initial-content heterogeneous bounds** survive. The new section also contains demonstrated errors: the nonzero-initial readout extension, the exact dense drift identity, and the interpretation of a positive integral as positive total drift. Its universal per-column dimension argument is not a valid consequence of Borsuk–Ulam.

| Item | Verdict | Exact scope/result |
|---|---|---|
| A1: R2 own-leak/injection split | **PASS** | Absolute budgets are separated; the old zero-budget counterexample is retained; no bound on the whole bus follows. |
| A1: repaired D3 | **PASS** | Damped initial mean and initial contrast are explicitly retained; small query caps apply only to nonspike rows. |
| A1: M_F envelope, Lemma 2.1 quantifier, ledger scopes | **PASS** | Continuous-envelope argument is valid; admissible tolerance and arrival offset are stated; centered F-step coefficient bounds remain OPEN. |
| A1: Lemma R constants and terminal F-step case | **PASS** | Independently certified tighter constants; no new dependency failure found. |
| Theorem 7.3, off-cycle statement | **PASS** | If the cumulative gate deficit is at most eps, at least `(H-eps/kappa)/(Lam+1)` actual inputs occur in the stated expanded interval. Retention means unforced local propagation, not a ratio of replenished full credit. |
| Theorem 7.3, cycle addendum | **PARTIAL** | Front starts before I must be charged; the printed `1+H/d` count can undercount in the expanded window. |
| Corollary 7.4(a) | **PASS in inherited theorem scopes** | Sparse scheduling does not evade protected-set arguments that already quantify over those schedules. No unconditional full-metric barrier is imported. |
| Corollary 7.4(b), universal finite factor saving | **FAIL as stated** | The eps correction and boundary drives cannot be dropped. A one-step 99.7%-retention example needs zero drives. The large-H, fixed-eps constant-factor conclusion is valid. |
| Theorem 7.5, zero initial content | **PASS** | Exact recurrence, spread estimate and composite constants pass. All explicit `Y_src`, `R_e` and Q terms remain; they are not proved small or own-credit controlled. |
| Theorem 7.5, nonzero initial content | **PARTIAL overall; readout extension FAILS literally** | The modified first aggregate bound passes; the readout bound omits initial content. A legal `n=1e8, m=1, T=3, E=Q=0` counterexample violates it by a factor 1.503865. |
| Lemma 7.2, R0 identity and lower bound on I | **PASS** | Exact integral identity; `I>=1.6e-6` under the specified slow-bath conditions. |
| Lemma 7.2, prescribed dense identity | **FAIL as written** | Forward coefficient is `alpha*a`, not a. This is an exact algebraic defect, however small the perturbation. |
| Universal positive forward drift in §§7–8 / REPORT | **FAIL** | A legal slowly falling bath gives retainer drift `-2.41761456e-6` while I remains positive. |
| Symmetric-reset leakage and `beta H^(3/2)` cost | **PASS as stated numerical/approximate mechanism; OPEN as a universal law** | Independently reproduced the positive examples. The fourfold deficit calculation is a linear-drift, large-period approximation. |
| §8's necessary per-column dimension condition | **FAIL** | Robust Euclidean dimension does not require D coordinates above `tau/sqrt(D)` at every point. Query-dependent responses make column counting even less justified. |
| Strongly heterogeneous retention ceiling / original full-metric problem | **OPEN** | E7 found no unbounded amplification, but finite tests do not prove a ceiling or a memory barrier. |

## 1. Evidence and contract

Read the changed proof, CHECKS, REPORT, STATUS, `repairs_check.py`, `exp_resets.py`, saved results and the copied previous audit. Rechecked relevant dependencies rather than rerunning all passed research: PR #27's actual protected-set proof at `c987408`, PR #31's bath/deviation and protected-set formulation, PR #28's inherited query/listing definitions, and PR #35's explicit dense forward coefficient. Source hashes are recorded separately.

The contract remains: zero initialization; actual past inputs in `(-.5,.5)^n`; original R0 or prescribed dense R; source feature and selected mask E unchanged; legal future gates in `[LO,HI]`; realized inputs frozen in parameter derivatives; peak **actual** support m and full-horizon **mT**. The original selected-to-full implication is a **lower-bound** inclusion. None of the estimates below supplies a full-gradient upper bound.

## 2. A1 — repairs to the previous audit

The original legal example is independently reproduced in [previous_independent_checks.py](previous_independent_checks.py), copied to this new directory so its outputs do not overwrite the old audit. At `n=1e8`, an off-cycle pair is neutral initially, pulsed to `(+.2,-.2)` versus `(0,0)` at time 2, and reset to the shared bath at time 3. It has exact common endpoints, `m=2,T=3`, and inputs below .253. The old own-leak budget is exactly zero, but the injection-generated readout is `5.20023165147574e-6`.

The replacement R2 does not claim that this is bounded by the old budget. It separates

\[
S'_j=aS_j+\sum_t|\delta_t(j)|c_t
\]

and compares only the own-leak component with its corresponding first-order **upper-budget scale**. The light-column argument explicitly pays for the new injection and has factor
`(2.33/HI)(1+1/900002)<2.479<2.5`. This passes. The actual signed first-order signal may cancel, and the full bus still has uncontrolled terms.

D3 now writes the initial mean, initial contrast and forcing-acquired term separately. Subtracting the damped baseline cures the exact rational diagnostic from the earlier audit. The M_F continuous envelope, tolerance restriction and arrival offset are also repaired correctly. T8 is charged, and the one-step centered estimates are not declared all-F estimates.

The tightened constants also pass **exact rational** checks in `independent_claims.py`: a rational enclosure for the square roots and positive Taylor enclosures for exp give one-step response below `2.26959`, F-step response below `2.32957`, and the own correction below `1.3335e-4 tau`. The previous passed identities were not extensively reaudited.

The author's `repairs_check.py` and `constants_mf.py` were run from separate copies under `author_checks/`; all assertions pass. Those runs are comparison evidence, not the independent argument.

## 3. A2 — retention cost

### 3.1 The off-cycle theorem passes

For `g_t in (0,1]`,

\[
\prod_{t\in I}g_t\le\exp\{-\sum_{t\in I}(1-g_t)\}.
\]

Thus unforced local retention `prod(ag_t)>=exp(-eps)` implies the claimed deficit condition. The converse implication is **not** claimed or needed: a small deficit does not by itself lower-bound the product by the same exponential. Nor does a large final **replenished** credit imply local retention.

By PR #27 Lemma 2.5, every off-cycle position with `g>1-kappa` belongs to the drive step or to at most Lam following positions started by a drive in that same row. The reference never-driven chain is bath-sized and has gate deficit above kappa; the dense comparison preserves the protected-set conclusion. This counting argument is per realized history and does not require a code-independent public schedule.

At most `eps/kappa` of the H positions can be unprotected. Each actual nonzero input in the expanded interval covers at most `L=Lam+1=450001` positions. Therefore

\[
N_i\ge\max\left(0,\left\lceil\frac{H-\mathrm{eps}/\kappa}{L}\right\rceil\right).
\]

The printed weaker real-valued bound follows. It applies to periodic, staggered, nonperiodic and heterogeneous controls. It does not establish a particular optimal reset frequency or an energy lower bound. Inputs before I, but within its Lam-step lookback, count; the charge is not necessarily paid inside I itself.

### 3.2 Finite corollary and cycle boundary qualifications

At `n=1e8`, take an entirely autonomous history and `I={3}`, `H=1`, `eps=.003`. Its unforced local retention is approximately `.9975048568094`, exceeding `exp(-.003)=.9970044955034`, with **zero** actual inputs. Theorem 7.3 correctly gives a negative, hence vacuous, lower bound. The claim in Corollary 7.4(b) that every reset strategy saves at most factor L compared with continuous driving is not a universal finite statement: a positive continuous cost divided by zero is not bounded by L.

For fixed eps and `H -> infinity`, the theorem does give `N_i>=H/L-O(1)`. That is the valid asymptotic constant-factor conclusion for **near-exact local retention**. It is not a theorem about all useful memory mechanisms.

The cycle addendum needs the same boundary care for **front starts** as for drives. For `d=25000000`, `Lam=450000`, take

- I from `25225002` through `50000001`, length `H=24775000`;
- expanded interval from `24775002` through `50000001`;
- front passages at `25000001` and `50000001`.

There are two relevant front starts, whereas `1+H/d=1.991`. If “front passages” means only passages inside I, the earlier front-chain protection is uncharged. A safe count over the expanded window is `1+floor((H+Lam-1)/d)`. This is a boundary/count issue in the addendum, not a refutation of the off-cycle cost theorem.

## 4. A3 — Theorem 7.5

### 4.1 Zero initial content: independent derivation

Put `r_i=1-g_i`, `sigma=sum_H Y_i`, `omega=max_(i,l)|Y_i-Y_l|`, and `q=gamma/sqrt(k)`. Subtracting the common leak and injection in two retainer rows gives exactly

\[
Y'_i-Y'_l=ag_i(Y_i-Y_l)+(g_i-g_l)(aY_l+qv_0).
\]

Since the off-cycle set is fixed and the selected column is outside it,

\[
\omega_t\le\omega_{t-1}+\eta_t\max_H|Y_{t-1}|+q\eta_t|v_t(0)|.
\]

Summing the exact row recursion gives precisely the proposed aggregate perturbation

\[
\rho_t=-a(1-\gamma P/k)\sum_{i\in H}r_iY_{t-1}(i).
\]

All actual capture changes remain in e; their **differences across retainers** are covered by Q. No additional own injection occurs because `j notin H`. The off-cycle cardinality ensures `|1-gamma P/k|<=1` in this domain. Consequently

\[
|\rho_t|\le\eta_t\sum_H|Y_{t-1}|,
\quad\omega_{\max}\le e^E(EM/P+Q),
\]

for zero initial contents, and

\[
M(1-E-E^2e^E)\le Y_{src}+R_e+EP e^E Q.
\]

This derivation includes repeated feedback for the whole interval: M is a supremum over all its intermediate times.

The exact rational certificate at `E=1/4`, using monotonicity of the positive expressions, gives

| Expression | Certified upper/lower value |
|---|---:|
| `1-E-E^2 exp(E)` | `>= .669748411457016...` |
| reciprocal | `<=1.493097979620` |
| `exp(E)/(1-E-E^2 exp(E))` | `<=1.917175755437 < 1.494*1.284` |
| `1+E exp(E)` | `<=1.321006354172 <1.33` |
| `exp(E)` | `<=1.284025416688 <1.29` |

Although `exp(.25)>1.284`, the **combined** first-bound constants have enough slack. This is not a rounding refutation. The resulting two zero-initial inequalities pass.

`heterogeneous_identity.py` independently compares the recurrence with full matrix multiplication and tests all explicit terms for arbitrary gates, including signed nonzero initial content outside the retainers: maximum aggregate residual `1.14e-13`, and no spread or zero-initial bound violation. These small-size operator checks are not asserted to be realizable histories or universal proofs.

### 4.2 Legal counterexample to the nonzero-initial readout extension

Location: [`PROOF.md:1005`](https://github.com/soma2-stack/AI-Architecture-Research/blob/c48640db6b677d52d109827d6d53bb0e2f005acf/theory/claude_remaining_channels_20261020/PROOF.md#L1005).

Use **R0, n=100000000, P=1, m=1, T=3**, column j off the cycle, and a different off-cycle retainer i. Inputs are zero through time 2; at time 3 set only row i to zero. Analyze `I=(2,3]`. Then its gate is exactly 1, hence **E=Q=0**, but the retainer already contains column-j credit.

Let `b2=c2*g2(j)`. Exactly `B2=b2 e_j`, so

\[
\sigma_2=Y_2(i)=-\gamma b2/k\ne0.
\]

At time 3, compute the exact physical column `B3=G3(aO b2 e_j+c3 e_j)` and transform by U. A legal one-step query with HI on i and LO elsewhere has `A=|chi_i|`. The independent calculation gives:

| Quantity | Value |
|---|---:|
| Initial `sigma_2` | `-1.99529190666808e-8` |
| Final `sigma_3` | `-3.99030305148533e-8` |
| `sigma_3-Lambda sigma_2` | `-1.99501116486976e-8` |
| Actual `|chi_i Y_3(i)|` | `1.37038590726032e-8` |
| Printed readout bound after the stated replacement | `9.11242517010156e-9` |
| Violation factor | **1.50386519689** |

The sole input is `-.04999291581023`, strictly legal. Sources remain undriven. The witness is inside (H), the smaller S4 width domain, and the resource budget. This is a single-history lemma counterexample, not a robust memory section or a refutation of the original barrier.

[interval_witnesses.py](interval_witnesses.py) encloses the expressions with outward interval arithmetic. It scales credits by the positive source normalization sigma to avoid approximating its fixed point; both sides have the same scale. The intervals for actual and claimed readout are disjoint by more than `2.29e-10` in that scale. The failure is not a numerical-precision suspicion.

The new first aggregate bound, with its initial-mean and initial-spread additions, survives. The second bound cannot become a statement about the **total** readout merely by replacing sigma on its right-hand side. It must include the initial readout, or explicitly subtract a correctly defined initial evolution.

If “replace sigma” was intended to modify only the first display, that must be stated, and the second display still needs its initial-spread term. At the recurrence level, a zero-sum initial contrast `(z,-z)` with E=Q=0 survives as `a^L(z,-z)` while its aggregate sigma remains zero; a contrast query reads it. That is an algebraic initial-data diagnostic, not an additional claimed legal-history construction. The legal three-step witness above tests the literal replacement instruction; neither interpretation supplies the currently missing general initial-vector readout argument.

One safe correction to the total-readout estimate is

\[
|\chi_H^TY_T|\le A\{1.33(M_*+|\sigma_{t1}|)+1.29P(\omega_{t1}+Q)\},
\quad M_*:=\max_t|\sigma_t-\Lambda_t\sigma_{t1}|.
\]

This follows from the same spread estimate with initial omega retained. It is a proposed repair, not the statement audited. Alternatively restrict both displays to zero initial content. Repaired D3 itself remains valid.

### 4.3 What near-homogeneity does not imply

E bounds the **cumulative maximum deficit from gate 1**, not just differences between gates. A homogeneous but persistently leaky set may have large E. Joining/leaving a dynamically redefined set would require boundary terms; the theorem assumes a fixed physical set and only permits its gates to change.

The bootstrap denominator stays positive up to approximately `.52778886`; above that, this proof fails to close. This number is a limitation of this estimate, not an amplification threshold or a theorem that larger E is impossible.

The theorem still contains `R_e`, Q, and the peak **full transformed source credit**. Calling it an unqualified own-sized ceiling drops obligations. In particular it does not establish that full source credit is linear in that source's own drive cost when bus feedback is allowed.

Actual E also depends on the interval and startup. Independent reproduction of the author's symmetric-period-256 run gives E about **.82035** from time 500, but **.14492** from the source pulse. Its qualification cannot be inferred from the period alone. Starting later also requires treating the initial contents correctly.

## 5. A4 — drift and symmetric leakage

### 5.1 R0 identity passes; the exact dense statement does not

For R0, putting `beta'=atanh(s_next)-a*s` and integrating `sech^2=1-tanh^2` gives exactly

\[
y_{next}-y_{pred}=(s_{next}-s)+(1-a)(s-y_{pred})+I.
\]

The stated subinterval proof also gives the lower bound on **I**. A rational certificate using `tanh z>=z-z^3/3` proves the claimed `1.6e-6` margin under the slow-bath and floor assumptions.

For the prescribed dense matrix the actual forward coefficient is **a′=alpha*a**, as PR #35 explicitly states. The correct identity replaces a by a′ and uses `beta'_actual=atanh(s_next)-a′*s`. At a legally reset state `y_pred=0`, the actual next preactivation exceeds the one in Lemma 7.2 by

\[
(1-\alpha)a s>0.
\]

This is strictly positive for the **prescribed** matrix: `||R0+eta 11^T/n||>=a+eta/n>a`, so its normalization satisfies `alpha<1`. No convenient alternative dense matrix was selected. The error is tiny, but an exact identity cannot omit it. Keep **a** in the R0-skeleton credit theorems; the required replacement concerns forward state drift, not a wholesale change of the model.

### 5.2 Positive I is not positive total drift

The interpretation at line 1101 and in REPORT drops `s_next-s`. “Slow” here permits a negative bath increment as large as .001, vastly greater than `1.6e-6`.

A legal **n=1e8, m=5000, T=3** example:

1. All inputs zero at time 1.
2. At time 2 set 4999 off-cycle rows to **.49**, and one other off-cycle retainer to **0**.
3. At time 3 use zero inputs.

It has source rows undriven, maximum input `.486067402791<.5`, and m exactly at (H)'s allowed limit. The resulting quantities are

\[
s_2=.04995132641106,\quad s_3=.04990741064150,
\]
\[
s_3-s_2=-4.3915769561\,10^{-5}>-.001,\quad
I=4.1497655483\,10^{-5}>1.6\,10^{-6},
\]
\[
y_2=0,\quad y_3-y_2=-2.4176145647\,10^{-6}<0.
\]

The interval certificate verifies all signs, legality and strict inequalities. Thus the R0 identity and positive-I bound pass, but the **universal positive forward-drift reading fails**. It also defeats §7.6's numerical premise that instantaneous field cancellation necessarily needs width much larger than `c0*n`. It does not show cancellation can be sustained cheaply over a long memory interval.

For long intervals the existing **telescoped** bath identity is the appropriate starting point:

\[
\sum_t\beta'_t=(s_{end}-s_{start})+
\sum_t[\operatorname{atanh}(s_{t+1})-s_{t+1}]+(1-a')\sum_t s_t.
\]

The floor controls its long-time average, not every increment. This is already related to PR #31's telescoped-field observation; it should not be presented as a new pointwise theorem.

### 5.3 The symmetric-reset advantage is real finite evidence, not a universal cost theorem

In a steady scalar bath define `F(y)=tanh(a*y+beta')` and `beta=F(0)`. Exactly,

\[
F(y)-y-\beta=-(1-a)y-a\int_0^y\tanh^2(az+\beta')\,dz.
\]

An explicit local error bound is
`(1-a)|y|+a|y|(a|y|+|beta'|)^2`. This quantifies what the linear-drift approximation neglects; a varying bath adds further errors.

For the linear samples `y_r=y0+beta*r`, `r=0,...,R-1`, exact average deficits are

- zero target: `beta^2*(R-1)*(2R-1)/6`;
- optimal discrete target `-beta*(R-1)/2`: `beta^2*(R^2-1)/12`;
- author's target `-beta*R/2`: `beta^2*(R^2+2)/12`.

The familiar 1/3 and 1/12 coefficients are their large-R limits. Neither exactly fourfold improvement nor a universal `beta H^(3/2)` cost law is proved by these approximations.

Nevertheless, [reset_law_checks.py](reset_law_checks.py) reproduces the author's nonlinear-network results with an independent implementation, using the published target beta as an input:

| n=65536, P=2048 | Independent centered readout | m | mT |
|---|---:|---:|---:|
| continuous hold | 48.072788248803 | 2050 | 10865000 |
| zero reset, R=64 | 47.680141503396 | 34 | 180200 |
| symmetric reset, R=64 | 47.962897403461 | 34 | 180200 |
| symmetric reset, R=256 | 46.352986171478 | 10 | 53000 |
| symmetric reset, R=1024 | 26.997902151873 | 4 | 21200 |

All five agree with the saved author results within `4.2e-13`. The approximate loss reductions around 3.6× / 3.5× are supported for these cases. Their interpretation as **ANALYSIS + NUMERICAL** is appropriate. Claims that these calculations exclude every new asymptotic law are not established.

## 6. Additional issue: dimension cannot be inferred from equal-strength columns

Locations: §§7.5 and 8.1, especially line 1091.

The assertion that every robust D-dimensional memory needs D columns each above `tau/sqrt(D)` under one query does not follow from Borsuk–Ulam or from the existence of saturation codes. For example, the continuous odd embedding

\[
f(\theta)=\frac{1.1\tau}{\sqrt2}(\theta,\theta),\quad\theta\in S^{D-1},
\]

has norm `1.1 tau` everywhere. At `theta=(1,...,1)/sqrt(D)`, **all 2D coordinates** are below `tau/sqrt(D)`. At a coordinate vector only two are nonzero, regardless of D. A sufficient saturated construction is not a necessary structure of every robust section.

With query-dependent responses even the number of parameter columns is not a general topological dimension bound: an abstract single-column response `r_g(theta)=C*g^T theta`, with g in the legal gate box, has `sup_g |r_g(theta)|>=C*(HI-LO)/2` on the entire sphere. This is a counterexample to the proposed **algebraic inference**, not a claimed realization by legal histories. Proving realizability is precisely the research problem.

Accordingly, the source-hold and `beta*n^(7/4)` estimates may describe the specified equal-strength, independently coded construction family. They do not establish universal necessary costs. The explicit open status of the original problem is correct and must be preserved.

## 7. E7 — strongly heterogeneous retention

### Method and controls

[e7_independent.py](e7_independent.py) imports no author research modules. It uses an exact equivalence-class reduction before the first cycle wrap: front descendants form an expanding prefix; other never-driven rows share the bath; off-cycle retainer rows are grouped **only when their complete control histories coincide**. Each group carries an integer physical-row count. The method propagates the exact original R0 equations with float64 arithmetic, not a small-eta or large-n approximation.

[validate_reduction.py](validate_reduction.py) compares against an independent full-vector implementation built from two Householder maps and a permutation. Six cases, including a bipolar source, agree within `7.4e-14` in readout, with matching actual support counts, width, source peaks and input bounds. A previous full-vector n=65536 reset control agrees within `1.6e-12`. Algebraic exactness of the reduction is separate from finite-precision agreement.

The experiment uses H=1800 source activity, a seven-step balanced pulse, an exact reset, gap 3000, and **T=5300** including warmup. There are also bipolar tests with a balanced pulse in history + early and history − later, challenging cancellation with a sign-changing source-credit difference. Other physical controls are identical between histories. Zero-sum off-cycle source differences cannot enter any other hidden row; reset gives exact common endpoints mathematically.

Families: no-retainer control, continuous holes, symmetric period-64 resets, zero period-1024 resets, mixed periods/targets, held targets from -.4 to .4, alternating strong/weak states, hole/free duty cycles, intermittent anti-holes and joining/releasing cohorts. Actual inputs are computed from target state minus the true forward preactivation and counted whenever nonzero. **mT**, additive support and retainer drive counts are distinct fields in the result files.

The centered raw learning-credit readout is optimized exactly over the one-step legal gate box for one selected column. We separately measure peak `|Delta O_source|`, peak `|Delta Y_source|`, full source magnitudes and retainer-only readout. The query is implemented from the common endpoint by future preactivations .25/.75 and held fixed under differentiation. A one-column result is not a robust D-dimensional memory.

### Results

**66 main/control configurations** were run, plus five reset-law reproductions and the small full-vector validation cases. The main/control runs used about 90 summed elapsed seconds; each process used one BLAS thread, with at most two such processes concurrent. Maximum actual input magnitude was `.473648860<.5`.

Matched retainer density `P/n=1/32`, outside the theorem's (H) domain because of n/width, but legal architecture histories:

| Schedule | n=32768, P=1024 | n=65536, P=2048 | n=262144, P=8192 |
|---|---:|---:|---:|
| continuous hold control | .06191979 | .06470274 | .06688783 |
| mixed periods / targets | .03091996 | .03143950 | .03184299 |
| strong held targets | .01972363 | .02082588 | .02170595 |
| alternating strong / weak | .00033286 | .00017114 | .00008238 |
| duty cycle | .05913697 | .06144188 | .06321325 |
| intermittent anti-holes | .05311048 | .05562493 | .05760429 |
| turnover / releases | .00910131 | .00890432 | .00875911 |

Entries are centered readout / peak `|Delta O_source|`; normalizing by peak `|Delta Y_source|` gives similar values and is recorded separately. Some values rise modestly over this finite grid. That is not evidence of **unbounded** growth; no tested heterogeneous family beats the homogeneous control here. This is not an exhaustive search.

The strong-target, alternating and anti-hole runs have post-pulse cumulative maximum deficits near **624**, with substantial actual differences between gates. Mixed periods have E around **7–8**; period-1024 resets around **5–6**. These are actual measured deficits, not the linear-drift formula. Duty-cycle E varies near .25–.30, illustrating that crossing the proof threshold need not produce a physical transition.

The exact reduction also permits finite tests **inside (H)** and the small-constant budget:

| Schedule | n=1e8, P=2048 | n=1e12, P=20480000 |
|---|---:|---:|
| hold control | .00007385 | .00007351 |
| mixed periods | .00003234 | .00003199 |
| strong targets | .00001507 | .00001472 |
| alternating strong/weak | .00000035 | .00000010 |
| duty cycle | .00007062 | .00007028 |
| anti-holes | .00005508 | .00005474 |
| turnover | .00000815 | .00000780 |

Here `P/n=2.048e-5`, all actual widths are below `5e-5*n`, sources are undriven, schedules are public, and **every run** has `mT<=2.5e-5*n^(3/2)`. For example the hold controls have mT `10865000` and `108544010600`; the corresponding ratios to `n^(3/2)` are about `1.0865e-5` and `1.08544e-7`. Virtual multiplicities are counted as actual physical inputs, not as one input per class.

Bipolar-source tests likewise found no growing advantage: hold ratios at n=65536 / 262144 were `.0221329 / .0224156`, anti-hole ratios `.0182649 / .0185051`, both below their matched controls; the (H)-domain n=1e8 ratios were much smaller. All raw results, E values and resource costs are saved.

**Conclusion:** no mechanism with an unbounded readout-to-source gain was found. Strongly heterogeneous retention remains **OPEN**, not refuted. These selected one-column tests do not establish an upper bound in the full metric. Large virtual n values are finite numerical checks, not an all-size certificate. The optional PR #35 construction reset test was not run; correcting the proved gaps takes priority over extending that construction experimentally.

## 8. Reproduction, preservation and next step

Run from this audit worktree:

```powershell
$env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:OMP_NUM_THREADS='1'
python theory/codex_pr37_step35_audit_20261020/independent_claims.py
python theory/codex_pr37_step35_audit_20261020/interval_witnesses.py
python theory/codex_pr37_step35_audit_20261020/heterogeneous_identity.py
python theory/codex_pr37_step35_audit_20261020/validate_reduction.py
python theory/codex_pr37_step35_audit_20261020/reset_law_checks.py
python theory/codex_pr37_step35_audit_20261020/e7_independent.py --series finite
python theory/codex_pr37_step35_audit_20261020/e7_independent.py --series contract
python theory/codex_pr37_step35_audit_20261020/e7_independent.py --series bipolar
python theory/codex_pr37_step35_audit_20261020/e7_independent.py --series controls
python theory/codex_pr37_step35_audit_20261020/previous_independent_checks.py
python -I theory/codex_pr37_step35_audit_20261020/author_checks/repairs_check.py
python -I theory/codex_pr37_step35_audit_20261020/author_checks/constants_mf.py
```

Python 3.11.9, NumPy 2.4.6, mpmath 1.3.0. `claim_results.json` contains the rational and 90-digit checks; `interval_results.json` contains outward counterexample certificates. The `e7_*.json` files contain numerical experiments. `source_manifest.json` and `verification_manifest.json` record source/output hashes and preservation checks. No statement in this audit converts numerical agreement into a universal proof.

**Recommended next mathematical work:** first repair the nonzero-initial readout extension and the dense coefficient, and distinguish I from total drift. Then target a query-aware heterogeneous-retention estimate with the **entire initial vector**, nonautonomous bath field and all capture terms present. Use the telescoped bath identity and the existing protected-set cost rather than a false pointwise positive drift. The unresolved step is controlling `P omega`, Q, other forcing and query-dependent heavy-column time profiles without assuming source credit is only own credit. A further sweep of continuous holes would add little; a new experiment should change those specific obligations.

The established finite efficiency gain and the valid zero-initial theorem should be preserved. **No audited result changes the established asymptotic memory-capacity scaling. No universal asymptotic exclusion follows from §8's dimension argument either.** The original prescribed-dense, full-metric robust linear-memory question at `mT=o(n^(3/2))` remains **OPEN**.
