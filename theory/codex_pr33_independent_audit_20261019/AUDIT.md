# Independent audit of PR #33: three-memory / sequential off-cycle construction

Date: 2026-10-19. Auditor: Codex. Claude remains lead researcher.

Target: [PR #33](https://github.com/soma2-stack/AI-Architecture-Research/pull/33), immutable commit
`d6801c2bb1b311b3d132312535b87c86064d2eb9`.

Supporting context: PR #31 `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab`, PR #32
`cef12b3eb6e5a8e6dbc75904253222b57eda188c`, and PR #28
`0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88`. The #31 and #32 folders at the audited #33
commit compare unchanged to these supporting heads. The #28 proof was read at its own head.

## Executive verdict

**Theorem 6.1: OPEN. Corollary 6.2: OPEN.** The construction's actual robustness has not been
refuted, but the submitted proof does not establish either universal conclusion.

**REFUTED:** the assertion that the supplied coefficient `eps_SO` is at most `1/2` for every
`n >= 10^18`, the claimed eventual monotonicity, and the claimed limit of that exact formula.
At the admissible integer dimension `n = 10^166`, the formula gives
`e = 0.6313704808502767...` and `eps_SO = 2.199215479617742...`. At `10^168`, `e > 6`, and the
shipped program fails `assert e < 1`. This is a counterexample to a load-bearing certificate,
not a counterexample history to the intended memory construction.

Useful results survive. **PROVED in their R0 scope:** balanced locality, the uniform-query
identity, first-order separation, bounded-input legality after correcting the stated start-row
index, the first-order lower bound, and the exact pulse-source identities. The out-of-window
estimate in Lemma 5.1(d) can be justified by making a small omitted birth-term absorption
explicit, as done below. The second-order bootstrap is valid only where its scalar closure
conditions hold; its advertised use for every larger n is not certified.

No source proof, existing research file, restricted notebook, or AGENTS.md was edited. No branch
was switched, no commit/push/merge or GitHub review publication was performed. All new files are
inside this separate audit directory. Tests were lightweight CPU verification, not training.

## 1. Findings in priority order

### F1 — REFUTED: the universal second-order numerical bound and monotonicity

Sources: `PROOF.md:497–514`, especially 506–510; `constants_so.py:23,59–63,75`.
[Immutable proof](https://github.com/soma2-stack/AI-Architecture-Research/blob/d6801c2bb1b311b3d132312535b87c86064d2eb9/theory/claude_lemma_m_three_memory_20261019/PROOF.md#L497),
[coefficient code](https://github.com/soma2-stack/AI-Architecture-Research/blob/d6801c2bb1b311b3d132312535b87c86064d2eb9/theory/claude_lemma_m_three_memory_20261019/constants_so.py#L59).

The code defines

\[
 \varepsilon_g=4e^{-200},\quad Q=1600,\quad k=n/2,
\]
\[
 a_L=\frac{\gamma}{k}\left[\frac{\sqrt{k}}\gamma+D_fQ+
 2\bar x(H+1)(2+Q/H)+s_{hi}^2d\right]
 +\underbrace{\varepsilon_g Q\sqrt{k}}_{6400e^{-200}\sqrt{n/2}},
 \qquad e=a_L+a_A b_A.
\]

The underbraced term increases without bound. Every term here is nonnegative. Therefore `e < 1`
cannot hold for all sufficiently large n with this fixed gate majorant. Increasing `n_*` or
merely extending the finite grid cannot fix the problem.

Independent reconstruction uses exact integer H and D, not floating approximations to their
ceilings/floors. Results agree with separate calls to the author's implementation:

| n | e | eps_SO from the submitted formula |
|---|---:|---:|
| 10^18 | 0.006422105107216883 | 0.3746807476664495 |
| 10^24 | 0.005132517001545007 | 0.01810395309652888 |
| 10^40 | 0.005090409211200000 | 0.006570804672446859 |
| 10^160 | 0.005716685075850277 | 0.007382572780225337 |
| 10^164 | 0.06771841258502767 | 0.09326813283744374 |
| 10^165 | 0.2031375542869888 | 0.3273259822840471 |
| 10^166 | 0.6313704808502767 | **2.199215479617742** |
| 10^168 | 6.267891163502767... | bootstrap assertion fails |
| 10^180 | 6262800.76359317... | bootstrap assertion fails |

This failure is independently **exactly certified**, not an artifact of Decimal precision:
`interval_certificate.py` uses Fraction arithmetic and positive Taylor series with rigorous
rational tail bounds. It establishes

\[
 .6313704808502 < e(10^{166}) < .6313704808504 <1.
\]

Since all source coefficients are nonnegative, `0 < a_d < 1`, and

\[
 \varepsilon_1=\kappa_s b_A+(1+\kappa_s b_A)\frac e{1-e},
 \quad \varepsilon_{SO}\ge\varepsilon_1/a_d\ge\frac e{1-e},
\]

it follows **rigorously** that `eps_SO(10^166) > 1.7 > 1/2`. The full high-precision evaluation
is 2.199215..., but that decimal is not needed for the refutation. The same rational certificate
establishes `e(10^168) > 6`.

These n satisfy `4 | n`, the construction fits its horizon, its pairs lie inside the memory
block, and the integer D bound holds. The counterexample therefore does not leave the stated
parameter range. It concerns the coefficient formula; it does not simulate an astronomical
network or demonstrate that the actual second-order signal is large.

There is also a finite rounding counterexample to the claimed decreasing constituents:

```
n0 = 1000000000000000280   H(n0) = 1264911064067352
n1 = 1000000000000000284   H(n1) = 1264911064067353
```

Exact rational arithmetic gives `H(n1)/n1 > H(n0)/n0`. Both n are legal multiples of four.
The independently reconstructed full epsilon also increases there by approximately
`2.9373e-16` (the latter is a high-precision numerical observation). Saying that a rounding
changes H by at most one does not bound its effect or establish monotonicity.

**Consequence:** the second inequality of Theorem 6.1, via the claimed global half-error bound,
is unproved. The limit `.0066` describes a simplification that neglects the fixed exponential
term, not the asymptotic behavior of the supplied certificate.

**Smallest credible repair to investigate:** retain a genuinely n-dependent front-gate bound,
for example the form `4 exp(-.0297 sqrt(k)+.92)` in PR #32 Lemma S4, after independently checking
its premises for this construction. Alternatively exploit the exact birth/retention kernels.
Then derive the complete revised majorant and a uniform analytic envelope handling ceilings,
floors and every remaining n-dependent term. Do not simply set the fixed exponential to zero.
This audit does not supply that complete global repair.

### F2 — REFUTED count rule: separate dimension inequalities do not produce a joint zero

Source: `PROOF.md:559–574`, especially the condition in 564–567.

The conditions `|Psi| < D` and, additionally, `N_1+N_2+N_3 < D` do not imply that the
concatenation `(Phi,Psi)` has a zero. The necessary sufficient count for the Borsuk–Ulam argument
used here is

\[
 N_1+N_2+N_3+|\Psi|<D.
\]

For a proposed listing bound `B(n)=3C_0+2.25C_1+C_2 log^2 n`, one must require
`D > N_1+N_2+N_3+B(n)`, with the appropriate integer/count convention.

Exact elementary counterexample to the stated counting inference: on `S^1` (`D=2`), take
`Phi(x,y)=x` and `Psi(x,y)=y`. Both maps are odd and continuous, each has one coordinate, and
both separate counts are less than two; they have no joint zero.

The original target controls the bus at zeros of a specified Theorem-4 listing. A failure at
zeros of Psi alone is not yet its refutation. Moreover, if that listing is the all-future-query
listing, PR #28 uses `N_3=1.3e7 F_s`, not the one-step value `1.8e4`. A single legal uniform
query can violate a universal readout bound, but this does not allow changing its required
listing-zero set. The one-step variant is valid only when that is the explicitly chosen target.

For fixed constants, the correct total is still `O(log^2 n)` here, so an independently proved
unbounded family with `D ~ n^(1/4)/160` would beat it eventually. Thus this finding corrects the
finite sufficient condition and the exact listing scope; it does not itself disprove the
qualitative eventual implication. The implication remains **PROVED if** the robust family and
the corrected total-count inequality are first established. Corollary 6.2 itself remains
**OPEN**, because Theorem 6.1 has not been certified for an unbounded n range.

### F3 — REFUTED start-row description; legality survives with a corrected age estimate

Sources: `PROOF.md:241–245,273–281`; `exp_S_check.py:28–29` uses the same formula.

The definition gives

\[
 T_s=T-d+20,\qquad p_{T_s}=d-1-(T-T_s)=19,
\]

not row 20. Its predecessor is row 18, whose row-1 front age is 17, not the age-18 predecessor
used in the stated `.376` bound. The printed construction and script are consistent with each
other, but inconsistent with the row-20 description and that proof step.

With the actual indices,

\[
 \tanh^{17}(1)+\operatorname{atanh}(.1009)
 = .3830380744137302\ldots < .3831 < .4563.
\]

The rational certificate verifies the corrected upper bound. This preserves the legal input
margin. One can instead shift `T_s` forward by one to implement the described row-20 spike;
the window definition has enough terminal slack, but that is a source correction, not the
construction audited here. No illegal-input counterexample was found.

### F4 — REFUTED all-timestep front-gate statement; harmless initialization exception

Source: the row-class assertion at `PROOF.md:381`.

At zero initialization and before any scheduled drive,

\[
 h_1(1)=\tanh(.05),\quad g_1(1)=\operatorname{sech}^2(.05)
 =.9975041607715679\ldots > 4e^{-200}.
\]

The tiny gate bound starts at t=2. PR #32 Lemma S4 actually states `g_1(t+1)` for `t>=1`.
This exception does not inject an omitted initial credit: `c_1=0`, `B'_0=0`, and hence `B'_1=0`.
The t=1 birth multiplies zero. The background and difference estimates can explicitly exclude
that zero term. It does not cure F1.

### F5 — Verification assertions are weaker than the constants claimed in CHECKS.md

`constants_seq.py` asserts `Pi(z)/z >= .60` (line 72), `c_s <= .34` (76), and front mass
`<= 60` (86); these assertions do not test the manuscript's `.6272`, `.3331`, and `39.73`.
It also does not assert the displayed lower bound on `c_R`. Passing those assertions alone
would be insufficient evidence for the constants the proof uses.

This is a verification-coverage defect, **not a false constant**. Independent exact rational
interval checks certify the stronger constants used in the manuscript:

| Quantity | Independently certified conclusion | Approximate underlying bound |
|---|---:|---:|
| Pi(z)/z, all z in (0,1] | >= .6272 | .6272833001966545 (grid lower envelope) |
| c_s | <= .3331 | .3330068502137784 |
| maximum pulse square | < .1316 and < 1/7 | .1315567070368830 |
| front mass, infinite tail included | < 39.723 < 39.73 | < 39.72228636 |
| c_R | > .0004988 | .0004988549124810 |
| first-pulse input | < .4563 | < .456244522 |

The Pi certificate combines a derivative lower bound on [0,.1] with monotonicity on 2,000
intervals covering [.1,1]. Every endpoint evaluation is bounded with exact rational Taylor
remainders. The front mass uses 800 outward-rounded rational steps and an analytic geometric
bound on the entire remaining tail. It does not discard an uncertified finite-sum remainder.

## 2. Lemma 5.1(d): independent derivation and the hidden birth term

**Verdict: PROVED as a consequence of the preceding background bounds, with the birth-term
absorption below made explicit.** No counterexample to the claimed out-of-window magnitude
bound was found. This result is not a proof of the global second-order half-error claim.

Write `L_out=sup_{t notin I_i}|lambda_t|`. Use `lhat` for the global supremum. Outside the
column's own window, the parked/bath gate gives `delta_t(c)=0`. The own forcing is at most
`(gamma/k)c_*`. For the other terms in (5.2), the following bounds apply:

\[
 |Y_0|\le(1+\gamma\bar D/k)Q_1\widehat\lambda+
 (\sqrt{k}/\gamma)\widehat\lambda,
\]
\[
 |Z_{spike}|\le Q_1(1+d\kappa_s)\widehat\lambda+L_{in}+dL_{out},
\]
\[
 |Z_{active\ other\ pair}|\le[Q_2+(H+1)\kappa_hQ_1]\widehat\lambda+(H+1)L_{out}.
\]

The pair is a different, previously unused pair, because the windows including parking are
disjoint. Its initial bus is therefore a never-held bath bus. Front predecessors use
`Q_1*lhat`. Substitution into the exact leak formula gives precisely the displayed right side
of (5.1d), including `lhat/sqrt(k)` from the broadcast row and the `s_hi^2 L_in` term. Rearranging
is legitimate: `c_out=(gamma/k)[s_hi^2 d+2 xbar(H+1)]<.006` throughout n>=10^18, using
`H<=40n^(3/4)+1`. Define the proposed `l_out` by equality with `RHS/(1-c_out)`, as the code does;
a bare inequality of the form `l_out(1-c_out)<=RHS` would not characterize an arbitrary
supersolution.

There is one term not displayed in the text's arrival-window argument. For another window J,
unrolling a cycle N path gives

\[
 \sum_{t\in J}|A_t|\le |J|\kappa_c Q_1\widehat\lambda
 +Q L_{in}+|J|Q l_{out}+B_J,
\]

where `B_J` is the row-1 birth contribution. It is not mathematically zero. Its per-time bound
is

\[
 \varepsilon_g q^{d-2}[(1+\gamma\bar D/k)Q_1+\sqrt{k}/\gamma]\widehat\lambda,
 \quad q\le1-1/1600.
\]

It can be absorbed without changing the stated constants. Our rational certificate gives a
front capture-mass bound `D_f^0=39.723`, leaving `.007` below the chosen `D_f=39.73`.
Also `k q^(d-2)<=1` for all n>=10^8: the logarithm is at most
`log(n/2)-(n/4-2)/1600`, which is negative at 10^8 and decreasing thereafter.
Since `Q_1>=1` and `gamma Dbar/k<=1`, the birth term divided by
`(gamma/sqrt(k))Q_1*lhat` is at most `3 eps_g k q^(d-2) <=3 eps_g <.007`.
Use that unused mass margin in kappa_c, rather than silently dropping `B_J`.
The arrival-window estimate then has exactly the form used in eta_oth, and unrolling the
other pair for H+1 steps yields the stated eta_oth.

The D_f terminology should refer to the front contribution excluding the deliberately held
spike when a separate spike term is also used. The total deviation estimate is safe:
`39.73 + .1009^2 + 2*.1316 = 40.00338081 < 40.01`.

## 3. Lemma 5.2: exact pulse sources and conditional bootstrap

### 3.1 PROVED: source identities; balanced states do not mean balanced gate differences

For one credit column, set `Z^-_pred(r)=Z^-_(t-1)(pi^-1 r)` and take Delta=plus-minus.
The two histories have identical bath, source credit and all non-pulse gates. Subtracting the
exact U-row recurrence gives, for r>=1,

\[
 \Delta Z_t(r)=ag_t^+(r)\Delta Z_{pred}(r)+\kappa_t^+(r)\Delta A_t-\Delta\lambda_t
 +a\Delta g_t(r)Z^-_{pred}(r)
 +\frac\gamma{\sqrt{k}}\Delta\delta_t(r)A^-_t
 -\frac{\gamma^2}{k^{3/2}}\Delta S_t A^-_t.
\]

The exact bus-leak difference is

\[
 \Delta\lambda_{2,t}=\frac{\gamma a}k\sum_{r\ge1}
 [\delta_t^+(r)\Delta Z_{pred}(r)+\Delta\delta_t(r)Z^-_{pred}(r)].
\]

The broadcast row also has a direct source, not just a homogeneous coefficient:

\[
 \Delta Y_t(0)=(\widehat g_t+\gamma S_t^+/k)\Delta A_t+
 (\sqrt{k}/\gamma)\Delta\lambda_t+(\gamma/k)\Delta S_t A^-_t.
\]

The first-order source includes all changed own injections:

\[
 \Delta\lambda_{1,t}=\frac\gamma k
 [a\delta_t^+(c)\Delta o_{t-1}+a\Delta\delta_t(c)o^-_{t-1}+c_t\Delta g_t(c)].
\]

There is no Delta c_t term for R0: its undriven source block is independent of these memories.
The reset and parking remove state differences exactly; their credit differences persist in
the homogeneous Delta Z recursion. They do not create additional changed-gate forcing outside
the seven-step pulses.

Both rows of a balanced pair have the same squared amplitude, so their gate differences
**add** in Delta S. The submitted bookkeeping correctly retains this uniform source. Each
pulse has two rows and seven steps: the factor is 14, not seven and not zero.
For Pi_j=Pi(|theta_j|), the verified slope bound gives
`sum_pulse,rows |Delta g| <=14 c_s Pi_j`, and hence

\[
 \sum |\text{pair-row source}|\le14c_s\Pi_j
 [\eta+(\gamma/\sqrt{k})(1+2\gamma/k)Q_1\widehat\lambda].
\]

This is the code's `pulse`. The direct leak source is bounded by
`(gamma/k)14c_s eta Pi_j`. The uniform source has time mass at most
`(gamma^2/k^(3/2))Q_1*lhat*14c_s Pi_j` (the code's sS per Pi_j).
The broadcast direct source contributes
`(gamma/k)^2 Q_1*lhat*14c_s Pi_j` to the leak majorant; it is present in R_src.
No missing pulse, injection or reset term was found in these identities.

### 3.2 PROVED within scalar closure conditions; OPEN as the advertised all-n bound

The remaining collection is a positive-system argument, not a theorem supplied by executing
a scalar formula. Its terms can be traced as follows:

| Carrier | Coefficient on Lambda | Coefficient on Acal | Direct pulse/uniform sources |
|---|---|---|---|
| row 1 via Y(0) | 1/sqrt(k) | (gamma/k)(1+gamma Dbar/k) | (gamma/k)^2 Amax sum|Delta S| |
| front rows | (gamma/k)D_f Q | (gamma/k)D_f Q(gamma/sqrt(k))(1+gamma Dbar/k) | (gamma/k)D_f Q sigma_S |
| spike | (gamma/k)s_hi^2 d | preceding coefficient times kappa_s | preceding coefficient times sigma_S |
| all active pairs | (gamma/k)2xbar(H+1)(2+Q/H) | (gamma/k)2xbar(H+1)(kappa_h+kappa_b) | uniform sources and the summed pair pulse sources |

All entries are upper bounds; dropping factors a<=1 is safe. Bath samples at window starts
are H+1 apart. Their retention sum is at most
`1/(1-q^(H+1)) <= 1+Q/H`; adding forcing during the disjoint active windows yields `2+Q/H`.
For the capture term, `(1+Q/H)kappa_b/Q <= kappa_b` for H>=100, Q=1600. This explains the
otherwise easy-to-miss repeated-window factors.

Front birth terms must be retained during this derivation. When the submitted `e<1` condition
holds, its nonnegative term `eps_g Q sqrt(k)` implies `eps_g sqrt(k)<1/Q=.000625`.
The front birth sum is at most
`eps_g Q[(1+gamma Dbar/k)Acal+(sqrt(k)/gamma)(Lambda+sigma_S)]`.
It fits in the unused `.007` front-mass margin established above. The Acal arrival-birth term
has an additional `q^(d-2)` factor; its absorption follows from the same exponential path
estimate as in section 2 and the spare `2 eps_g Q` denominator margin. Thus birth terms need
not be assumed exactly zero.

These estimates give the code's a_L, a_A and R_src (a_L includes an extra conservative positive
front-gate term). If all denominators are positive and e=a_L+a_A b_A<1, solving

\[
 \mathcal A\le b_A(\Lambda+\sigma_S),\quad
 \Lambda_2\le a_L(\Lambda_1+\Lambda_2)+a_A\mathcal A+R_{src}
\]

is legitimate and yields the stated Phi-type coefficients. The l2 step of Corollary 5.3 is
also valid: the off-diagonal all-ones bound contributes at most D Phi_oth times ||Pi||_2.

This does **not** establish the conditions at every n, nor eps_SO<=1/2. F1 explicitly refutes
that next step. A valid source decomposition cannot rescue a scalar bootstrap whose closure
condition eventually fails.

## 4. Other results and contract accounting

| Item | Verdict and precise scope |
|---|---|
| Prop. 2.1, balanced locality | **PROVED for R0**, disjoint prescribed pairs, common resets/parking. Opposite state changes preserve the off-cycle sum and the shared field, and all other rows stay identical by induction. |
| Prop. 2.2, uniform query | **PROVED.** B'(0)=0 and source rows of a memory column are zero; `U R0^T(HI 1)=a HI sqrt(k)e_(d-1)` on that subspace. The row's own part is zero on an off-cycle column. |
| Prop. 2.3, first-order separation | **PROVED** for windows after path entry. Own arrivals and cycle-own sources on an off-cycle column vanish; L_off and W depend only on that memory. Mixed interactions are in K_bus+L_bus. |
| Lemma 4.1 | **PROVED legality/continuity/common endpoints with the corrected age-17 calculation.** Public support envelope has at most three rows, including parking. The row-20 description is false for the printed schedule. |
| Lemma 4.2 | **PROVED in (H).** The own recurrence is monotone in pulse gate. The functions x(1-x)^w increase for w<=6 because tanh(.38)^2<1/7. Nonconstant c_t merely gives nonnegative weighted injection terms. Post-pulse holding gives the displayed F*; exact scalar certificates verify Pi and c_R. |
| Lemma 5.1(d) | **PROVED as derived in section 2**, with explicit birth absorption; use equality to define l_out. |
| Lemma 5.2 / Cor. 5.3 local algebra | **PROVED under their explicit scalar closure conditions**; not a proof those conditions hold universally. The claimed universal half-error coefficient is **REFUTED**. |
| Theorem 6.1 | **OPEN.** The first-order proof and valid resource accounting survive, but the global second-order step does not. No actual trajectory counterexample established. |
| Corollary 6.2 | **OPEN.** Needs an unbounded robust family and the corrected combined listing count. Its sufficient separate-count rule is **REFUTED**. |
| Dense transfer | **OPEN**, as the PR itself says. R0 is not the prescribed fully dense matrix. |
| Original strict-budget linear-dimension/full-metric question | **OPEN**, unchanged. |

The integer geometry was independently checked with integer fourth roots:
`H=ceil_root4(40^4 n^3)` and `D=(n/4-41)//(H+1)`. For all n>=10^18,
write x=n^(1/4)>=30000. Then
`D > x/160 - 1 - (41+x/80)/(40x^3+2) > x/160 - 1.001 >= x/161`.
This proves the claimed lower bound uniformly; it does not rely on sampled rounding checks. The pairs fit since D<<n/8. More directly, last parking is
`T-d+39+D(H+1)<=T-2` with the printed Ts. The full horizon is T=n/2, including autonomous
initialization and preparation. Actual inputs outside the prescribed sparse controls are
zero for R0; no dense inverse correction is being hidden. Public envelopes count every
potentially nonzero parking/reset coordinate. Hence `m<=3`, `mT<=1.5n`; the intended peak is
three, as observed in checks. No additive-support measure was substituted.

The uniform query is legal in the inherited future-preactivation contract; future inputs are
held fixed under differentiation. The selected group is PR #28's row-0-excluded
`{u f_s^T:u_0=0}` with its declared normalization. A lower bound on the memory-column restriction
is a lower bound for that same selected normalized vector. It is not an obstruction or a
normalization theorem for the original full R/W/b gradient metric.

The own correction estimate is safe: `|nu_c|=a HI gamma/sqrt(k)` off cycle, both own credits
are nonnegative and bounded by `c_*(Q+H+1)`, and the generously stated
`4e3 n^(3/8)` bound follows. It is conditional only in its use after a robust full selected
readout has been established. A small own correction does not prove a large bus signal when
the prerequisite selected-readout lower bound is still open.

Even a repaired R0 theorem would give only `D~n^(1/4)/160` at mT=1.5n. This is compatible with
mT>=c D sqrt(n), not a refutation of the n^(3/2) barrier for D=Omega(n). The dense transfer,
Lemma M', general centered/second-order operator listings, and the logarithmic loss remain
separate questions. Do not classify the original Lemma M for the prescribed dense contract
as refuted on the basis of this incomplete R0 proof.

## 5. Reproduction and evidence

From this audit directory (Python 3.11, NumPy 2.4.6 used here):

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -I interval_certificate.py
python -I independent_checks.py
python -I run_author_checks.py
```

* `interval_certificate.py`: exact rational certificate for F1, the H/n rounding counterexample,
  and the first-order constants. Output: `rational_certificate_result.json`.
* `independent_checks.py`: independently reconstructs majorants with exact integer geometry;
  implements an explicit UPU matrix simulation, not the author's O_apply or m3sim; checks
  exact row/difference identities, pulse sources, signs, locality and readout at small sizes.
  Output: `independent_results.json`; readable full output: `independent_stdout.txt`.
* `run_author_checks.py`: copies only the author's Python files into `author_runs/` and reruns
  constants_seq, constants_so, exp_exact_checks, exp_verify_probe, the external probe, and
  exp_S_check at n=16384,H=700,D=5. It separately calls the author's coefficient routine at the
  adversarial astronomical n. Output: `author_run_results.json` and per-script stdout/stderr.
  The immutable `sources/` files are never overwritten by running these scripts.
* `provenance.json` and `source_manifest.json` pin commits and SHA-256 hashes of the inspected
  source snapshots. Read REPORT.md, CHECKS.md, all 11 Python files in the target including the
  external probe, and the committed result records. Large-n scaling records were inspected,
  not rerun as expensive simulations. Supporting #31/#32 material and #28's selected contract,
  listing and query definitions were examined independently of their status labels.

All six small author reruns exited zero. The grid values and the external-probe numbers
reproduced. The n=16384 S rerun gives actual peak support 3, endpoint residual 0 in that
implementation, and SO/F1 about .1212 or .1144 depending on theta. These finite checks do not
satisfy the theorem's n>=10^18 premise and do not prove its asymptotic bound.

Eight independent boundary cases at n=512 or 1024 included positive/negative axes, equal
coordinates, opposite signs, a near-axis direction, and a mixed-sign direction. These are
structural tests outside (H), not counterexamples to theorem-regime bounds. Maximum residuals:

| Check | Maximum residual / ratio |
|---|---:|
| U-row recurrence | 9.62e-12 |
| full difference recursion | 1.45e-11 |
| broadcast difference including direct Delta S source | 2.87e-13 |
| uniform-query identity | 6.12e-13 |
| direct changed-gate bus-leak source | 1.05e-17 |
| first-order sign violation (roundoff) | 2.33e-16 |
| endpoint difference | 5.83e-16 |
| measured pulse-source / 14-step majorant | <= .551 |
| mixed difference of first-order parts, four separate amplitude corners | 1.67e-16 |

Small matrix products were built explicitly from the reflection and permutation; their
roundoff residuals are not asserted to be exact zeros. Exactness claims above rest on algebra.
The independent arithmetic/simulation checks took seconds; the author S rerun took about
27 seconds on one CPU thread. No GPU or model training was used.

## 6. Recommended next action

Repair the n-dependent front contribution in the complete second-order bootstrap and prove
an analytic uniform envelope for all admissible integer n. Keep the exact row-0 source and
the seven-by-two pulse accounting visible. Correct the joint-listing total and use the
same Phi/query scope as the target being refuted. Correct the harmless start index and the
t=1 gate exception. Then rerun an independent audit of the resulting universal bound before
promoting Theorem 6.1 or claiming an asymptotic refutation of Lemma M. A denser numerical grid
alone cannot establish this result.

## TL;DR

The balanced sparse mechanism, its first-order signal, and the pulse bookkeeping passed.
The all-n error certificate failed with an exact supporting counterexample. Therefore the
robust theorem and Lemma-M refutation remain OPEN from the submitted proof. The original
frozen dense-tanh/full-d_F n^(3/2) problem remains OPEN.
