# AI Architecture Research Atlas

Snapshot: 2026-10-17 (consolidated local archive). This is a cross-branch navigation and status archive, not a fresh proof of every historical result. “Verified” always means verified only in the stated scope. Numerical agreement, even at high precision, is not a universal theorem. The original frozen dense-tanh learning-credit problem remains **OPEN**.

Start new work at [RESEARCH_START_HERE.md](../RESEARCH_START_HERE.md). For saved experiment protocols, numerical outcomes, prototype studies, negative runs, duplicates, and run-status limits, see [EXPERIMENT_HISTORY.md](EXPERIMENT_HISTORY.md). The atlas remains the canonical theorem/branch index.

## 1. Research goals and original mathematical problem

The project seeks a genuinely new computational primitive or architecture whose important state transitions, guarantees, learning behavior, information flow, or resource law are not preserved by an ordinary decomposition. General computability or Turing-machine simulation does not by itself decide architectural novelty. See the repository governance and lane method documents for the discovery standard.

The central mathematical problem is the frozen dense-tanh recurrent system under its original prescribed dense recurrent matrix, zero initialization, original full fixed-feature gradient metric $d_F$, legal future-query contract, and resource measure. The target is a robust continuous $D=\Omega(n)$ section with one exact common endpoint and uniform boundary-antipodal separation greater than (0.002), while peak actual input support $m$ times the complete history horizon $T$ is $o(n^{3/2})$. This target is not established. It must not be silently replaced with a modified architecture, a selected parameter group, a numerical sample, or a different cost model.

Contract reminders:

- $m$ is the maximum number of nonzero **actual** input coordinates at any one time and at any section parameter. Every nonzero value counts, however small. It is not a sum of supports over time, nor a reference-support convention.
- The budget is the bounding-box product $mT$, with the full history horizon. Preparation, holding, routing, reset, and tail are included. Additive coordinate-time is a different accounting.
- Inputs and parameterizations are fixed while taking the gradient. Do not differentiate an input-routing or correction policy.
- The legal future-query preactivation range is $[0.25,0.75]$; it is not the past-input cube.
- A selected group of weights, the full fixed-feature group, and the original full $d_F$ metric are distinct claims. Query families and normalization must be stated with each bound.
- Public schedules/envelopes, code-dependent schedules, and private gates are different assumptions.
- A common endpoint must be exact where the theorem requires exact equality. Approximate floating-point agreement is not exact equality.
- QSR (quadratic shift recurrence), diagonal/reference skeletons such as $R_0$, and other altered recurrences are not the original prescribed dense-tanh architecture.

### NEW DISCOVERY CHECK

1. Search this atlas for the proposed idea and its synonyms.
2. Compare the exact assumptions, equations, mechanism, legal query family, and resource accounting.
3. Check whether an independent counterexample, correction, or superseding result already exists.
4. State precisely what the proposed result adds and which established record it does not duplicate.
5. Only then consider extended proof work or a permitted experiment.

## 2. Quick discovery lookup

| New idea or keyword | Previously investigated? | Result | Where to look | What remains new? |
|---|---|---|---|---|
| gated recurrence, GRU equivalence, retention gate | Yes: prototype PR23 Experiments 009–016 | Exact transition/gradient equivalence to a general gated recurrent cell in 324 cases; no unique architecture property found | [Prototype record](https://github.com/soma2-stack/AI-Architecture-Research/tree/192df629e060def0983c4e85f70c4dd01b15b6a0/prototypes/rnn_llm_architecture); PR #23, `192df629` | A materially different native guarantee or resource law not preserved by that cell |
| QSR, quadratic shift, neutral holes, credit broadcast | Yes: PR24–26 | QSR robust theorem verified in its modified architecture; neutral-hole broadcast principle verified in a narrow route; original tanh equivalence unproved | `claude_shift_holonomy_audit_20261013/`; `claude_neutral_path_tax_20261013/`; PR #24–26 | A proof under the unchanged prescribed dense-tanh contract; neutral-path tax remains conjectural |
| neutral path tax, neutral holding, gate deficit | Yes: PR24 Lemma 8.1, PR26 audit | One-step unweighted trace-deficit statement verified in displayed reference model; global credit-weighted tax not proved | PR #24 `d899895`; PR #25 review `50bb5ff`; PR #26 `e13311b` | A cumulative, credit-weighted inequality under exact original assumptions |
| Householder relay, dense twist, signed relay | Yes: PR26 and Oct 2026 corridor records | Exact algebraic relays and finite-stage cases; no universal robust $D=\Omega(n)$ construction | `claude_neutral_path_tax_20261013/`; `codex_single_block_spatial_write_20261004/` | Uniform legal-query gain across a full continuous section under strict $mT$ |
| bus feedback, gathered credit, bus-captured memory | Yes: PR27–29, PR31 | Hypothesis B's selected-group bus bound refuted by PR29 at $D=1$; this does not imply large robust dimension | PR #27–29, `c987408`, `0cc0a23`, `f056944`; PR #31 `35cdb7a` | Capacity/dimension theorem for gathered information, beyond a large scalar signal |
| distributed memory, bath cancellation, reservoir/bath floor | Yes: PR27–32 and earlier Route 7A/7B | Several scoped bath identities/floors verified; complete moving-corridor and unrestricted operator listing remain open | `theory/INDEX.md`; PR27 audit; PR31 audit; PR32 `STATUS.md` | Close remaining public/private, off-cycle, multi-step, and full-metric gaps without changing the contract |
| front saturation, protected set, protected Walsh mask | Yes: finite-N experiments and PR27–32 | Exact/small-size algebra and some fixed-K public-schedule bounds verified; finite masks do not imply asymptotic dimension | `experiments/finite_n_*`; PR #27, #31 | A uniform asymptotic capacity law under actual support and complete horizon |
| centered retention, centered channel, zero-sum modulation | Yes: Codex corridor work and PR32 | Some centered identities are scoped; PR32 centered channel/resource law is author analysis awaiting independent audit | `codex_single_block_spatial_write_20261004/`; PR #32 | Independently prove operator-width/credit bound for the full legal query family |
| gather channel, first-order gather, off-cycle listing | Yes: PR31 | Corrected first-order gather listing theorem proved in its stated scope; not the full bus or all multi-step queries | PR #31 `35cdb7a`, `codex_pr31_repair_audit_20261016/` | Prove or refute `M_rest` and connect listing control to full $d_F$ |
| multi-step future queries, exact cutoff | Yes: PR28 | Corrected cutoff is (F_s=\lceil \ln(1.01\sqrt{k})/r_H\rceil), (r_H=-\ln H_I); scoped query bound is verified | PR #28 `0cc0a23`, cross-PR audit | Expand to new query families only with a complete operator/error proof |
| Hypothesis B, source-channel counterexample, dense transfer | Yes: PR29 | Refuted for the selected-group reference-skeleton bus statement under the original prescribed dense matrix; $D=1$ | PR #29 `f056944`; audit folders in PR #29 | No need to repeat the refutation; robust dimension and full-$d_F$ conclusions remain separate |
| Lemma M, bus capacity, log-free bound | Yes: PR31 | First-order gather listing bound independently checked; full Lemma $M_{rest}$ is open/unaudited | PR #31 audit; PR #32 | Resolve the exact missing off-cycle/operator-norm inequalities |
| robust antipodal code, Borsuk–Ulam, sign matrices | Yes: PR24–28 and Oct 1 finite-N work | Scoped QSR theorem and some conditional section bounds verified; random-code estimates are not transferable across architectures | PR24 proof/review; PR28 proof/review; `experiments/third_order_antipodal*` | Prove a section for the original model with its full resource and query contract |
| absolute history energy, exponent (1/4)–(3/4) | Yes: Sep/Oct theory folders | Scoped fixed-feature norm exponent bracket survives; it is not a squared-energy exponent and not the final dimension theorem | `theory/CURRENT_THEORY.md`; `theory/INDEX.md` | Improve the exponent or derive a robust dimension result without conflating norm and energy |
| moving corridor, moving probe, multi-donor, repeated writes | Yes: many Oct 2–8 folders | Several constructions/obstructions are family-specific; no complete corridor theorem | Codex notebook; `theory/INDEX.md`; source index below | Handle jointly changing cohorts and parameter information with uniform section control |
| time-varying near-critical filters, K=3/4, growing K | Yes: PR branches/local-only commits | Some scoped results; one literal K=3 discrete word refuted; growing-K and selected repairs await review | `gemini_time_varying_nearcritical_filter_bank_20261006/`; source index; local-only commit list | Exact legal schedules and a uniform asymptotic result |
| query-weighted moment merger, round-robin packet schedule | Yes | General solution claim refuted; auxiliary covariance/error identities remain useful | `claude_moment_merger_review_20261001/` | A different aggregation mechanism with a proved legal-query guarantee |
| Lemma U / dependent Walsh labels | Yes | Claimed constant 2 is false for dependent labels; corrected bound (2\sqrt2) and scoped Theorem B-F constant 8 | `claude_lemma_u_repair_20261007/`; `gemini_lemma_u_repair_audit_20261007/` | Sharpen constants under additional valid assumptions, or prove sharpness |
| fixed-anchor basis renewal, arbitrary aperiodic gates | Yes | Reduction refuted; exact fixed-profile results survive | `claude_transport_basis_review_20261002/` | New treatment of genuinely time-varying gate products |
| private renewal Gamma, D=1 scalar bus signal | Yes | Scoped cheap scalar signal verified; says nothing by itself about $D=\Omega(n)$ | `codex_private_renewal_gamma_20261003/`; PR29 | A dimension/capacity argument; avoid treating amplitude as independent memory |
| dynamic internal data structures / runtime-created types | Broadly searched in Cursor lane | 103 primitive/interface/learning-dynamics candidates killed under its recorded novelty screen; not a universal proof that no architecture exists | `docs/notebooks/Cursor_Research.md`, resume; PR history #1–22 | A precisely specified candidate that survives prior art and decomposition tests |
| automated mechanism search, AMS, GAS-0 | Yes: PR7–16, PR19–20 | Search/harness design and recorded negative runs; no new architecture promoted | `experiments/automated_mechanism_search/`; `experiments/gas0/` | Only a screened candidate with matched evidence, not another unmotivated batch |
| original (n^{3/2}) barrier, log loss | Yes | Full high-dimensional claim remains OPEN; PR28 conditional theorem had a log loss and its premise Hypothesis B was later refuted | PR27–29; PR30 handoff | A new proof under original full metric; a D=1 bus refutation is insufficient |

## 3. Established theorems and independently verified results

Each entry below is a result record, not a blanket endorsement of every statement in its source folder.

### F-01 — General gated-cell equivalence in prototype

**Claim and scope.** The prototype recurrence was compared against an ordinary general gated recurrent cell with matched state, masks, and parameterization. Across 324 tested cases, transitions, gradients, and masks agreed to float64 error at most (10^{-13}). This is an exact algebraic/implementation equivalence for that prototype mechanism, supported by exhaustive finite cases; it is not a theorem about every architecture called “gated RNN.” The prototype is not canonical GRU, but no non-preserved architectural property was identified.

**Status: NUMERICALLY VERIFIED; architecture novelty not established.** Evidence: PR #23, commit `192df629e060def0983c4e85f70c4dd01b15b6a0`, Experiments 009–016 under `prototypes/rnn_llm_architecture/`. No later result supersedes it. Matters as a novelty filter; repeating the same equivalence test is redundant unless the state transition changes.

### F-02 — QSR robust antipodal theorem

**Claim and exact scope.** In the modified quadratic shift recurrence, the theorem assumes $n=mR$, $1 ≤ D ≤ n/1001$, $n-D ≥ 520$, the stated $q=193$ zero-input accumulation followed by $R$ writes and $R$ cancels, input cube $[-0.5,0.375]$, exact common endpoint 0, and the legal $Q_{ne}$ future family. The PR24 sign-code argument gives a continuous section and uniform antipodal separation under its stated positive-bias assumptions. The finite-size dimension is $D=floor(n'/1001) ≥ n/1004$ in the corrected range; the older $n/1002$ statement was false at $n=1,000,999$. The bias-group claim uses $w_b=c/sqrt(n)$ with $c ≥ .0021$ over $Q_{ne}$. A separate augmented fixed-feature statement uses only its stated full-group RMS/projected fixed-feature metric over $Q_{ne}$; neither is a universal all-group/all-query claim or the original full $d_F$ theorem. For resources, $R=floor(sqrt(n))$, $m=floor(n/R)$, $n'=mR$, and $T=195R$, so $mT ≤ 195n$ directly from $m ≤ n/R$; at most $2n' ≤ 2n$ coordinate-times are nonzero and $||X||_2 ≤ (5/8)sqrt(n)$. Source preparation uses a public changing-support schedule. The theorem does not supply a fixed $m$-coordinate input router.

**Status: VERIFIED IN STATED QSR SCOPE.** Lemmas 5.1–5.4 and corrected Corollaries 5.5–5.6 were independently checked in PR #25. Evidence: PR #24 commit `d899895aab81b36a3128a375ae2238b08f73f4af`; hostile review PR #25 `50bb5ffabf33b28099238acb6440cb1a349079e3`; `theory/claude_shift_holonomy_audit_20261013/` and `theory/codex_pr24_hostile_review_20261013/`. It does not solve the original architecture problem. Repeating the same QSR proof is redundant; proving a contract-preserving reduction would be new, but remains absent.

### F-03 — Local neutral trace-deficit lemma

**Claim and scope.** In the displayed frozen reference block $R_0=diag(aO, delta I_l)$, with $O$ orthogonal, $W=I$, and $b=.05 1$, if memory coordinate $i$ has $x_t(i)=0$ and $|h_t(i)| ≤ eta ≤ .01$, then

$$
(Oh_{t-1})_i ≤ -(.05 - atanh(eta))/a < -.0399.
$$

Let $N_t$ count memory coordinates $j$ with zero input and $|h_t(j)| ≤ .01$. Then

$$
∑_{j∈mem}(1-g_{t-1}(j)) = ||h_{t-1}^{mem}||_2^2 ≥ .00159 N_t,
$$

where $g=1-h^2$. The source reports that the operator norm of dense perturbation $R-R_0$ is at most $4/(10^8 n^2)$, changing the constant by less than $10^{-7}$ in its stated setting. This is a one-step, unweighted gate deficit. It is not cumulative parameter-credit tax and not an impossibility theorem for the neutral route or original problem.

**Status: VERIFIED IN STATED LOCAL SCOPE; any global neutral-path tax is CONJECTURAL.** Evidence: PR #24, `d899895`; independent PR #25 review `50bb5ff`; exact statement in `claude_shift_holonomy_audit_20261013/PROOF.md`. Repeating the one-step algebra is redundant; deriving a cumulative credit-weighted inequality is new and unproved.

### F-04 — PR27 fixed-K public-schedule probe theorem

**Claim and scope.** For the fixed-$K$ public-schedule probe family and exact assumptions in the repaired PR27 proof, the verified lower bound is
\[
mT\ge \frac{2.9\times10^{-10}D\sqrt n}{(K+2)(1+\ln K)}.
\]
Repairs correctly distinguish own-injection credit from incoming bus credit, use post-gate transport ordering (a(UGU)P), treat attenuation conditionally rather than as exact destruction, preserve nonzero front/cycle-wrap transport, correct bath-floor/all-horizon arithmetic, and use orthonormal probes with the declared parameter group. It is not a bound for arbitrary code-dependent schedules or growing $K$, and it does not automatically become a full-$d_F$ theorem.

**Status: VERIFIED IN STATED FAMILY.** Evidence: PR #27 `c9874081461139373a276efeb47394d50781c0e3`, repair verification `codex_pr27_repair_verification_20261015/FINAL_CROSS_PR_ADDENDUM.md`, and final cross-PR audit. No contradiction found in the listed repairs. Repeating the fixed-K proof is redundant; expanding its family is new.

### F-05 — PR28 Theorems 2–3 and corrected query cutoff

**Claim and scope.** Theorem 2 (soft sparse listing) and Theorem 3 (variation/topology) are verified under their stated assumptions. Corollary 3.5 is conditional on H1–H5, including a public carrying set/source/remainder and (8(\Lambda+1)\le D\le n). The exact multi-step cutoff is
\[
F_s=\left\lceil\frac{\ln(1.01\sqrt{k})}{r_H}\right\rceil,\qquad r_H=-\ln H_I,
\]
and its query-tail bound was checked. Theorem 4 explicitly requires (2N_3\le D\le n) and, if Hypothesis B holds, gives the scoped conditional bound
\[
mT\ge4.7\times10^{-11}D\sqrt n\,\min\!\left(1,\frac{890}{\ln n}\right).
\]
The logarithmic factor is part of the theorem; this is not a log-free (\Omega(n^{3/2})) result.

**Status: VERIFIED / CONDITIONAL as labeled.** Evidence: PR #28 `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88`, `codex_pr28_repair_verification_20261014/`, and `codex_cross_pr_final_audit_20261015/`. The exact theorem remains logically valid as an implication conditional on its premise; the premise below is refuted, so this route does not yield an unconditional lower bound. Repeat only if assumptions or query scope materially change.

### F-06 — PR29 refutation of selected-group Hypothesis B

**Claim and scope.** Theorem R_D transfers the $R_0$ counterexample to the exact prescribed dense matrix in the original contract. The deterministic recipe gives $R = alpha(R_0 + eta 11^T/n)$; balanced modulations satisfy $1^T Delta h = 0$, so the rank-one shared field cancels exactly. Sparse driven inputs are used directly, with actual support bounded by 120001, not a dense inverse correction. For every qualifying $n ≥ 1.5×10^{18}$ divisible by four, the construction has $D=1$, actual width $m≤120001$, and $mT≤2.5×10^{-5} n^{3/2}$. The audited lower bounds are $||Gamma_bus||/n > 0.11790944697$ and actual dense readout $>0.11790936597 n$; using the unrounded bound gives the required ratio $>2.0826 tau$. The earlier rounded display $0.11790n ≥ 2.0826 tau$ was false.

**Status: PROVED; Hypothesis B REFUTED in its exact selected-group scope.** The earlier $R_0$ Lemma E was independently verified, then dense-transfer equalities, actual support, endpoint/listing zero, and constants were audited. Evidence: PR #29 `f05694454956edab849ebe7d1858131eaca4174c`, dense transfer audit `codex_pr29_dense_transfer_audit_20261015/`, independent audit `codex_pr29_independent_audit_20261015/`; predecessor counterexample commit `2e46b02d61b8b2cc713546461d1232b578690b8f`. This refutes a scalar selected-group bus hypothesis at $D=1$; it does not prove or refute the original target $D=\Omega(n)$ under full $d_F$.

### F-07 — PR31 first-order gather listing theorem

**Claim and scope.** The corrected proposition M1, nine-term decomposition, bath floor/ceiling/gap, variation budget, and first-order gather listing are independently verified for $n≥10^8$ divisible by four, actual support $m≤5×10^{-5}n$, undriven source, one-step legal queries, and a public support envelope of width at most $m$ for the off-cycle term. The listed bound is

$$
|Psi_M| ≤ 9.1×10^5 + 9.7×10^{14}(mT/n)^2 + 1.4×10^8(mT)^{4/3}/n + 4,
$$

with first-order residual at most $30 tau/256$. The corrected source uses ceilings (including $N_0=max(1,ceil(x))$), cutoff 1,800,004, coefficient $3.897×10^7$, count less than $7.6×10^{14}$, centered bound .3435, and corrected BV block rounding. It does not prove the full bus theorem, all query lengths, full $R/W/b$ metric, or $M_{rest}$.

**Status: VERIFIED IN STATED SCOPE.** Evidence: PR #31 `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab`; independent repair audit `codex_pr31_repair_audit_20261016/AUDIT.md`. Repeating first-order arithmetic is redundant; higher-order/full-operator extension remains open.

### F-08 — Earlier fixed-feature and absolute-history bounds

**Claim and scope.** The indexed pre-PR24 results include a near-critical quadratic robust-dimension bracket $Omega_c(n^2)≤d_{rob}≤O_c(n^2 log n)$ for arbitrary horizon (with a finite $O(n)$-horizon quadratic match); a fixed-feature absolute-history norm exponent bracket $[1/4,3/4]$ up to specified slow/polylog factors; local-radius lower bounds in their stated regimes; an absolute-history superlinear packet; and scoped absolute-energy upper bounds when legal credit vanishes for the studied frozen biased family. A later strict-budget early-capture result gives $D≥n/(10^{70} log log n)$ only in its admissible regime, and the linear boundary occurs at $mT=Theta(n^{3/2})$. These are not the same theorem and norm is not squared energy.

**Status: VERIFIED / ACCEPTED IN STATED SCOPES as individually recorded; no blanket transfer.** Evidence and exact source summaries: `theory/CURRENT_THEORY.md` (2026-10-06 snapshot) and 106 unique source folders cataloged below, especially `codex_linear_dimension_frontier_20261006/`. Existing statuses preserve reviewer calibration, including mixed evidence and inherited-premise caveats. These results matter as current baselines; repeating without a changed assumption is redundant.

## 4. Author-proved claims awaiting independent verification

### A-01 — PR32 Lemma $M_{rest}$ and two-stream operator listing

PR32 reports author proofs for the two-stream formula (all rows/orders/queries), no-amplification lemma, retention, front saturation, and operator-norm reduction, plus small numerical identities. The centered-channel resource law (D\sim(mT/(6.2sn))^2) is labeled analysis. The bath identity/leak example is numerical at (n=65536). The complete $M_{rest}$ operator listing and multi-step/full-(R/W/b) extension remain **OPEN / NOT INDEPENDENTLY AUDITED**. Do not inherit PR31’s one-step result as proof of these claims.

Sources: PR #32 `cef12b3eb6e5a8e6dbc75904253222b57eda188c`, `claude_lemma_m_rest_20261016/STATUS.md` and `REPORT.md`. No need to rerun the finite identities as if they closed the proof; the missing object is the uniform operator/error estimate.

### A-02 — Newer Oct 4–8 moving-corridor constructions

Codex notebooks and theory folders report single-survivor spatial writes, changing-survivor timing rows, multi-donor joint sections, trace-neutral feedback compression, and private survivor capture. Some exact row identities and bounded subfamilies are internally checked or independently reviewed; the strongest newer joint results are often marked hostile-review-pending, conditional, or scoped. In particular, no full moving-corridor theorem gives the original $D=\Omega(n)$, (mT=o(n^{3/2})) result. Treat the status in each folder and `theory/INDEX.md` separately; the Codex notebook is a research record, not a status authority.

Sources include `codex_single_block_spatial_write_20261004/`, `codex_multi_donor_joint_section_20261003/`, `codex_timing_signal_J_20261004/`, `astra_route7a_long_window_20261008/`, `astra_route7a_feedback_compression_20261008/`, and `gpt6_private_survivor_capture_20261008/`; current-main paths are listed in the source index. Do not repeat an identical construction; first identify which proof premise or schedule class is new.

### A-03 — PR32 numerical identities

PR32 reports residuals around (5.6\times10^{-13}), (6.2\times10^{-15}), and (1.1\times10^{-14}), alongside one (n=65536) bath example. These are finite numerical checks, not universal estimates. Source: PR #32 `cef12b3`; `REPORT.md`. Any asymptotic claim still needs a symbolic proof or a certified interval argument covering its full domain.

### A-04 — Notebook-level candidate interpretations

Claude’s notebook retains historical 2026-10-02 harmonic/saturated-section ideas, including an (\Omega(n^{7/6}))-style suggestion explicitly marked likely/interim at that time. Later consolidated theory records changed the active status. Codex’s notebook contains October 4–8 results that are explicitly partial or awaiting hostile review. Cursor’s notebook records a negative-space search and AMS validations. These are provenance and candidate records, not current theorem statements; consult the dated source and later review before reuse.

## 5. Open lemmas, hypotheses, and conjectures

| ID | Open claim | Exact missing statement / scope | Why it remains open | Best source / repeat guidance |
|---|---|---|---|---|
| O-01 | Original frozen dense-tanh strict-budget memory problem | Prove $D=\Omega(n)$ at (mT=o(n^{3/2})) for original prescribed matrix, (h_0=0), full $d_F$, exact common endpoint and uniform legal-query antipodal separation; or prove a valid obstruction | No result listed here establishes this contract. PR29 only refutes selected-group Hypothesis B at $D=1$ | `CURRENT_THEORY.md`; PR27–32; pursue only with an exact full-contract proof path |
| O-02 | Remove logarithmic loss from conditional lower bound | Upgrade scoped (\Omega(n^{3/2}/\log n)) to (\Omega(n^{3/2})), or provide a counterexample under the same assumptions | Log-free control of query/operator variation and source/carrying code is missing; do not strengthen assumptions to conceal it | PR28 cross-PR audit; research handoff PR30 |
| O-03 | Lemma $M_{rest}$ / second-order gather capacity | Uniformly bound the complete off-cycle and multi-step operator/readout, including the stated two-stream terms and all legal query lengths | PR31 proves first-order listing only; PR32 is author-proved and unaudited; resource conversion is not established universally | PR32 `STATUS.md`, `REPORT.md`; continue by proving the exact missing operator inequality |
| O-04 | Full moving-corridor theorem | A single jointly admissible continuous code, uniform over all boundary points, with legal-query gain, exact endpoint and strict $mT$ budget | Separate axes, finite radius, scalar signal, or schedule-specific results do not make a complete robust section | Codex theory folders and `theory/INDEX.md`; do not count probes as independent dimensions without a rank/code proof |
| O-05 | Cumulative credit-weighted neutral-path tax | Turn the local (.00159N_t) unweighted deficit into the required cumulative credit bound across preparation/hold/reset | Lemma 8.1 is local and unweighted; interactions and credit propagation are not bounded by it | PR24 proof/review; explicitly conjectural, not an established route obstruction |
| O-06 | Public changing-support preparation routing | Provide an explicit router/embedding with bounded peak actual support for QSR source preparation, or state resource theorem only for public changing-support support schedules | Current QSR resource claim counts maximum simultaneously addressed support and relies on changing support across times; it does not provide fixed $m$-coordinate routing | PR24–25; no claim of a fixed router |
| O-07 | Growing-$K$ time-varying filter banks and repaired D2 | Close full time-ordered product sign/packing arguments for variable gates with a necessary complete-query signal upper bound | Existing power-of-frozen-matrix sign proof does not establish changing-(q_t) sign; visibility lower bound alone does not imply packing upper bound | `theory/INDEX.md`; historical notes remain proof gaps |
| O-08 | Spatial-write joint extensions | Uniform legal-query gain and shared subcritical cost when multiple modes/columns coexist on the same survivor patterns | Walsh reuse can break zero-sum protection; old writes can lose gain; current best joint result reaches only logarithmic D in one scope | `codex_single_block_spatial_write_20261004/`; no multiplication of separate-axis results |
| O-09 | Full-$d_F$ dense listing zero beyond selected group | Establish every listed quantity is zero for the full original metric at the constructed endpoint | The optional stronger PR29 proposition remains OPEN; selected-group Hypothesis B refutation is enough only for that hypothesis | PR29 audit; do not expand its conclusion |
| O-10 | Architecture novelty | Show a property not preserved by ordinary decomposition, with prior-art screen and falsifiable evidence | Mathematical construction alone is not architecture novelty; prototype gate mechanism reduces to ordinary general gated recurrence | `AGENTS.md`, `docs/notebooks/`, PR23 evidence |

Hypothesis B itself is **REFUTED**, not open, in its exact selected-group reference-skeleton bus formulation by PR29. This does not close O-01 or O-02.

## 6. Refuted claims and verified counterexamples

### X-01 — Hypothesis B selected-group bus bound

The claim that the selected-group bus readout is always bounded by the specified (\tau/4) scale is refuted by PR29’s legal $D=1$ construction. Its exact dense-transfer cancellation is (R\Delta h=\alpha R_0\Delta h) because (mathbf1^T\Delta h=0); exact actual support and listing-zero claims were separately checked. Scope is Hypothesis B only. No implication to $D=\Omega(n)$ follows.

### X-02 — Original QSR solution claim

Any claim that PR24’s QSR theorem solves the original frozen dense-tanh problem is refuted as a scope transfer. The recurrence, normalization/query family, and preparation-routing assumptions differ. The QSR theorem itself remains valid in QSR; its failure to solve the original problem is not a refutation of its internal theorem.

### X-03 — Neutral-path tax as a proved global obstruction

The one-step trace-deficit lemma is verified, but the global “neutral-path tax” conclusion is **not proved**. Any manuscript statement treating that cumulative tax or a universal neutral-holding impossibility as theorem is overstated. Keep it CONJECTURAL.

### X-04 — PR26 “one neutral path per direction” principle

The exact Householder/hole calculations show a single neutral path can broadcast query-visible credit to (Theta(n)) coordinates in the scoped construction. Thus that proposed general principle is false. The robust linear-dimensional counterexample/theorem H remains unproved: no uniform held-window perturbation estimate; random-code saturation was not an all-boundary proof; resource cost (m_{peak}\approx n/2), (T\approx n/4), so (mT\approx n^2/8), outside the strict budget.

### X-05 — Query-weighted moment merger as a general solution

The proposed convex transport averaging / round-robin packet solution is refuted in general. Auxiliary covariance and error identities remain useful and should not be deleted. Source: `claude_moment_merger_review_20261001/`; current scoped status in `theory/INDEX.md`.

### X-06 — Lemma U constant 2 for dependent labels

The claimed bound (le2) is false for dependent Walsh labels; a verified example exceeds (2.0039), with reported examples near (2.0346) and (2.0746). The corrected universal bound is (2\sqrt2), yielding scoped (D-q\le8(\Lambda/s)^2), not the earlier factor 4. This correction does not settle the full problem.

### X-07 — Fixed-anchor basis renewal as a reduction for arbitrary aperiodic gates

That reduction is refuted; fixed-profile encoder results survive in their own family. It cannot be reused as a proof for arbitrary time-varying gate sequences.

### X-08 — False implications to avoid

- A $D=1$ bus signal is not a high-dimensional robust memory code.
- A visibility lower bound is not a packing upper bound.
- A numerical success at finite (n) is not an asymptotic capacity theorem.
- A one-step query result is not a multi-step query theorem.
- A selected group is not the full gradient metric.
- Additive support-time is not peak-width times complete horizon.
- A modified architecture theorem is not a result for the original frozen dense-tanh system.

## 7. Numerical experiments and measured findings

| ID | Experiment / measured result | Evidence class and limit | Source |
|---|---|---|---|
| N-01 | Prototype two-slot training often plateaus; four binary slots learned unreliably (2/12 success in Exp011; 5/36 in Exp012, plus partial runs) | Finite seeded optimization outcomes; not incapacity proof | PR23 prototype Experiments 009–016 |
| N-02 | Slow fixed retention mattered more than learned gate in the tested runs: overwrite 0/9, slow fixed rate .005 4/9, initial gate bias 1/9 | Finite run result; seed-sensitive | PR23 prototype folder |
| N-03 | Layer1 held the read-time memory in tested successful two-gate runs; 8D projection sufficient and continuation-intervention necessary in those specific models | Model-specific intervention, not general architecture theorem | PR23 Exp014/015 |
| N-04 | Prototype recurrence/cell differences at most (10^{-13}) float64 across 324 cases | Strong finite exact-implementation check; algebraic equivalence is scoped to tested parameter/state family | PR23 Exp016 |
| N-05 | PR26 exact small-size values for neutral-hole route around .00245–.00253; total table values .0144 at n=16k, .0072 at64k, .0051 at128k | Numerical evidence; background/control can cancel; no all-boundary proof | PR26 theory/audit folder |
| N-06 | Finite protected Walsh-mask tests through R=16; sum-free masks pass the tested 0.1% cross-talk target, alias-prone masks fail at R=8,12,16 | Finite-N only; at n=2048 independent labels limited to six dimensions and matched run only at R=4 | `experiments/finite_n_clean_mask_scaling_20261006/`, `finite_n_r20_r32_scaling_20261006/` |
| N-07 | PR29 exact-rational/majorant certificate for the six-variable Lemma E system gives (E_Y<1018.375<1019) | Computer-assisted certificate for the stated recurrence/majorant plus exact algebra; not a substitute for checking transfer assumptions | PR29 `constants_check.py`, independent audit folder |
| N-08 | PR31 structural/numeric checks include nine-term decomposition, bath floor, BV constants and residual (le30\tau/256) | Independent symbolic derivations plus lightweight checks in the stated one-step regime | `codex_pr31_repair_audit_20261016/AUDIT.md` |
| N-09 | PR32 reports residuals (5.6\cdot10^{-13}, 6.2\cdot10^{-15}, 1.1\cdot10^{-14}) and an (n=65536) bath example | Numerical only; not independent and not an asymptotic proof | PR32 `REPORT.md` |
| N-10 | Cursor AMS benchmark gates, reruns, and OOD outcomes were audited, including v7 8 candidate promotions with all 8 negative and v8 0/42 confirmed | Search-process results for preregistered synthetic tasks; no general theorem and no architecture promoted | `experiments/automated_mechanism_search/`, `automated_mechanism_search_v9/`, `docs/notebooks/Cursor_Research.md` |
| N-11 | Finite-size robust-code, 7D/8D, radial, antipodal, endpoint, support-aware and witness-search experiments | Each records tested dimensions/parameters and failures; none alone proves the universal boundary theorem | All `experiments/` families indexed below; use `experiments/INDEX.md` for six finite-N protected-channel suites |
| N-12 | GAS-0 reproducibility harness and generated workspace artifacts | Harness/provenance and pipeline validation, not evidence of new architecture | `experiments/gas0/`; 17 local untracked generated workspaces are outside tracked branch history |

## 8. Failed approaches and why they failed

- **Ordinary gated-cell novelty:** exact equation/gradient equivalence preserved the prototype behavior, so the original architectural distinction was not demonstrated.
- **QSR-to-tanh transfer:** proved QSR results do not transfer without a separate equivalence theorem. Tanh preservation is unproved numerical evidence; idealized adjoints and sampled boundaries do not certify all-boundary legal queries.
- **Neutral-path global tax:** local trace deficit does not control cumulative credit, changed gate weights, or all transport paths. Keep the global claim conjectural.
- **PR26 random saturated code:** sampled success and exact algebra did not produce uniform held-window/all-boundary estimates; resource product was quadratic scale.
- **Convex moment merger / round robin:** counterexample invalidates the general claimed solution while leaving auxiliary estimates intact.
- **Fixed-anchor renewal:** does not handle arbitrary aperiodic, time-varying gates.
- **Dependent-label Lemma U:** orthogonality premise failed for dependent labels; the constant required repair.
- **D2 time-varying filter completion:** signs for powers of frozen (A(q)) do not prove signs for products with changing (q_t); spectral sign typos and a missing necessary packing inference remain historical gaps.
- **Disjoint-packing inference from visibility:** a lower bound on visibility alone does not supply an upper bound on the complete query signal/support; claimed necessity was not established.
- **Growing filter bank:** evidence includes time-varying/growing-$K$ dilution and one legal K=3 discrete-word counterexample. Do not generalize those to all filters.
- **Uniform small private renewal / pointwise timing bound:** refuted in recorded families because many large entries can form one coherent contrast. Integrated/query-weighted alternatives remain open.
- **Separate-axis spatial modes:** do not combine into one (B^R) section unless cross-mode trace independence, triangular reads, and one shared resource budget are proved.
- **Treating bus amplitude as dimension:** PR29 gives a scalar bus counterexample; it does not evade a high-dimensional robust-memory bound.
- **Treating “additive support” as m:** violates the original peak-width-times-horizon contract when supports move or are dense at different times.
- **Treating PR32 as audited:** author report and small numerical checks do not close $M_{rest}$.

## 9. Overlapping or rediscovered results

| Mechanisms | Relationship | What is actually shared | What remains distinct / duplicate judgement |
|---|---|---|---|
| PR24 QSR neutral holes ↔ PR26 neutral-hole/Householder relay | Related | Both use gate-neutral coordinates and query-visible credit | QSR modifies the recurrence and has a uniform sign-code theorem; PR26’s relay uses its own dense/Householder algebra and lacks a robust strict-budget section. Not duplicates. |
| PR27 protected probes ↔ PR28 multi-step queries | Direct dependency, not duplicate | PR28 imports protected-set/bath/state comparison ingredients and adds sparse-listing/variation/query-cutoff arguments | PR27 is fixed-K public-schedule bound; PR28 Theorem4 is conditional on Hypothesis B and has an explicit dimension range. |
| PR28 Theorem4 ↔ PR29 bus counterexample | Direct logical interaction | PR28's conditional lower route assumes Hypothesis B; PR29 refutes that premise | The conditional implication may be mathematically correct, but it yields no unconditional conclusion after its premise fails. |
| PR29 bus feedback ↔ PR31 gather channel | Related, materially different | Both study gathered/bus-carried selected-group credit and source effects | PR29 refutes a scalar bus-cap bound at D=1; PR31 bounds a first-order gather listing in a scoped source/query family. A large signal and a capacity bound are different questions. |
| PR31 first-order gather ↔ PR32 M_rest | Exact extension target | PR32 starts from the same bath/two-stream/gather framework | PR31 independently verifies first order only; PR32’s higher-order operator listing is not yet audited. Do not call it established by inheritance. |
| Householder relay ↔ bus feedback ↔ centered channel | Related mechanism family | Dense transport can move or expose credit through coherent directions | Different operators, source assumptions, and query scopes. A shared word like “bus” does not imply same theorem. |
| Bath cancellation / reservoir floor ↔ protected-set front saturation | Related proof components | Both bound what remains after captured/protected components are removed | Separate decompositions and hypotheses; reusing one bath lemma requires checking the exact gate schedule and parameter group. |
| Finite clean Walsh masks ↔ asymptotic spatial writes | Evidence informs construction, not proof | Same character/aliasing concerns | Finite R and finite n do not prove all-boundary or asymptotic separation. |
| Private renewal Gamma ↔ Hypothesis B counterexample | Related but not equivalent | Both exhibit a cheap D=1 scalar readout | PR29 is an exact prescribed-dense transfer with contract checks; earlier Gamma records have their own reference/schedule scope. Neither proves D linear. |
| Original (n^{3/2}) question ↔ PR29 B refutation | Different quantifiers | Both use bus/captured credit | B is selected-group and quantified even at D=1; original target asks D=Omega(n) in full metric. The refutation leaves the original open. |
| PR23 learned gate ↔ modern QSR shift architecture | Not an identified reduction | Both use gates/recurrent state | PR23 reduces to a general gated cell; QSR has a different mathematical recurrence. No novelty equivalence follows solely from shared gating. |
| Old theory index ↔ current PR24–32 | Status refinement | Same repository problem and vocabulary | `CURRENT_THEORY.md`/`INDEX.md` snapshot is 2026-10-06 and predates most PRs here. Later audits supersede only the exact overlapping claims; preserve other old records. |
| Local PR29 audit copies ↔ tracked PR29 audits | Exact duplicate | Same 22- and 27-file trees, byte-identical excluding cache files | Two untracked local copies were checked against PR29 head; do not count them as separate findings. |
| Codex joint audit local folder ↔ spatial-write/early-capture frontier | Related, later bounded result | Multi-column spatial writing and protected support | Local-only audit reported (D\ge n^{3/16}/3) for extreme (n\ge10^{1000}), (R=2), pair (>.012), (mT=o(n^{3/2})); later main frontier records stronger (D\ge n/(10^{70}\log\log n)) in an admissible regime. The former is not identical, and its specific bound is superseded for current best lower bound. |

### Explicit rediscovery links found during consolidation

These records share algebra or vocabulary but are not interchangeable results.

- **Oct 3 private renewal → Oct 4 multi-donor transfer → PR32 two-stream readout.** The Oct 3 [renewal derivation](codex_private_renewal_gamma_20261003/RENEWAL_DERIVATION.md) writes `O_* = C + U2 W2`, with `U2=[1,e1]` and two `r`-coordinate row vectors `J=u^T M` and `B=v_H^T M`; its `2×2` Volterra kernel is an output-channel kernel, not a two-coordinate or `2r`-coordinate online state. The Oct 4 [multi-donor proof](claude_multidonor_joint_section_20261004/PROOF.md) gives `H_N = Σ_s [β_s S_L(s−1)^T + ε_s ρ_(s−1)^T]` and, after applying a fixed parameter probe `v`, two scalar input sequences `S_L(s−1)^T v` and `ρ_(s−1)^T v` through fixed spatial vectors. PR32 [Proposition S1](claude_lemma_m_rest_20261016/PROOF.md) instead expresses a query readout as `χ^T Z_T = Σ_t [C_t(χ)a_t − R_t(χ)lhat_t]`, using two common vector-valued time streams and query-dependent scalar weights. The common substrate is the rank-two Householder correction `O_*−C = 1u^T + e_1 v_H^T`; the renewed variables, output, and scope differ. This is a related family, not an exact duplicate or proof transfer.
- **PR31 Theorem M → PR32 Proposition S1.** PR32 identifies the nine-term PR31 formula as the `χ=e_(d−1)` specialization of S1, split into own and bus components. See [PR31 proof](claude_lemma_m_bus_capacity_20261015/PROOF.md), its [independent repair audit](codex_pr31_repair_audit_20261016/AUDIT.md), and [PR32 proof](claude_lemma_m_rest_20261016/PROOF.md). PR31 is independently verified only in its first-order stated scope; PR32's broader S1/M_rest package remains author-proved or unaudited as labeled in A-01. Algebraic specialization does not verify the higher-order resource bound.
- **PR26/PR29 coherent readout ↔ PR32 Lemma S0 contraction.** These are not contradictory. S0 bounds Euclidean state-norm amplification for its stated transition; PR26/PR29 concern coherent or query-visible readout/credit. A large scalar or replicated bus signal can coexist with contraction and does not imply robust memory dimension.
- **PR32 bath-block draft correction.** The PR32 [proof](claude_lemma_m_rest_20261016/PROOF.md) records its own discarded `Theta(n)` and `O(sqrt(k))` bath-gain claims and replaces them with the stated bound `<= .3435 sqrt(k) + 203`; its [checks](claude_lemma_m_rest_20261016/CHECKS.md) report a column-restricted `n=65536` contrast `X=2797` but query readouts `8.5` and `28.6` for `H=1000` and `H=4000`. The example is finite numerical evidence, and the replacement theorem remains unaudited. Do not revive either discarded draft claim.
- **Oct 4 Codex spatial writes ↔ Oct 4 Claude multi-donor transfer.** The [single-block spatial-write proof](codex_single_block_spatial_write_20261004/PROOF.md) claims an internally checked, hostile-review-pending joint Walsh-masked `B^R` section with `R<=floor(log2(n)/8)`, `n>=10^200`, and explicit `2^R` duration cost; its best dimension is logarithmic. The [multi-donor proof](claude_multidonor_joint_section_20261004/PROOF.md) studies exact transfer, parameter-side confinement, and a conditional code barrier, and constructs no `omega(n)` section. Both use the four-site corridor and rank-two Householder substrate, but objectives and conclusions differ; neither validates the other's theorem.
- **Finite Walsh masks ↔ Oct 4 spatial-write proof.** The clean-mask experiments pass only over their tested finite range (through `R=16`). They diagnose aliasing and inform design; they do not certify the all-boundary constants or extreme-size theorem in the Oct 4 proof.

### Duplicate-detection rules

Treat two results as exact duplicates only if the state transition, assumptions, equations, quantified inputs/queries, resource accounting, and conclusion match. Shared terminology or a common rank-one/bus/bath component makes them related, not identical. A later stronger bound supersedes an earlier one only on the intersecting domain; preserve narrower results and counterexamples.

## 10. Unresolved research directions

1. **Original high-dimensional strict-budget problem.** Seek one exact common-endpoint continuous section for the unchanged frozen dense-tanh system and full $d_F$, with uniform legal-query antipodal separation and (mT=o(n^{3/2})). Any route must control the full parameter metric and actual support; the PR29 scalar bus construction is insufficient.
2. **Logarithmic loss.** For the current scoped lower-bound route, identify the exact inequality where query-family/operator variation or carrying-code size introduces (log n). A proof must remove it without silently shrinking the legal future family or adding a stronger public-schedule assumption; a counterexample must satisfy the same contract.
3. **Lemma $M_{rest}$.** Independently audit PR32’s two-stream formula and derive the missing uniform bound on every off-cycle/multi-step component, then check the integer resource conversion and final error budget. PR31’s verified first-order gather result is a starting lemma, not a proof of the extension.
4. **Joint protected spatial writes.** Find a shared continuous code with fresh modes and uniform all-boundary reads while charging one $mT$; explicitly test how later masks erase or alias earlier modes.
5. **Preparation routing.** For changing-support source preparation, either construct a legal fixed-width routing map with exact support accounting and fixed differentiation inputs, or state the theorem only in the public changing-support model.
6. **Novel architecture candidates.** Follow AGENTS.md’s novelty assay. A candidate must state its operation/state transition and identify a guarantee or learning/resource property lost under the strongest ordinary decomposition. The Cursor negative-space scan and PR23 equivalence are useful filters, not proof that no candidate exists.

## 11. Chronological history of discoveries

- **2026-09-27–28, PRs #1–6:** initial Claude/Codex/Cursor research syncs on learning dynamics, native coupling, and benchmark design. Cursor’s novelty screen later classified 103 candidates with zero survivors in its recorded classes. PRs #1–6 are merged.
- **2026-09-28–30, PRs #7–16:** AMS/grammar-gap candidate search and benchmark/harness repairs. AMS v7 promoted eight candidates, all eight were negative in fresh seeds; AMS v8 confirmed 0/42. No candidate promoted. This is a search-protocol result, not proof of no new architecture.
- **2026-10-01, PRs #17–18:** OMD-0 screened 18 target families; T1 retention survived its initial hostile review. OMD pilot phase A failed; no broader OMD-1 discovery search was authorized. Preserve as methodological/negative evidence.
- **2026-10-01–06, historical theory expansion:** near-critical quadratic dimensions, fixed-feature/absolute-history exponents, local-radius bounds, harmonic and multiharmonic constructions, online credit, protected sets, bath/source decompositions, and numerous review/counterexample folders. Current canonical legacy status is `theory/CURRENT_THEORY.md` and `theory/INDEX.md` (snapshot 2026-10-06).
- **2026-10-06, preservation branches/local-only commits:** time-varying filter banks, compensated spatial writes, moving-probe gain, all-support complement leverage, history-uniform corridor leverage, filtered timing packing, and D2 time-varying repair. Nine additional reachable commits were unique to local branch refs; see Coverage. Their source files are otherwise in existing indexed theory folders or explicitly marked pending/refuted.
- **2026-10-07–08, Route 7A/7B and corridor work:** public reservoir/recent-capture codes, un-cleared donor feedback compression, route-specific width bounds, Lemma U repair, and joint spatial-write constructions. Some components received independent scoped reviews; complete moving-corridor theorem stayed open.
- **2026-10-13, PRs #24–26:** modified QSR robust theorem and hostile audit; repaired QSR-to-original scope; neutral-hole/Householder analysis. PR24 theorem survives in QSR; global neutral tax remains conjectural; PR26 did not establish a strict-budget linear-dimensional counterexample.
- **2026-10-14, PRs #27–28:** fixed-K protected-probe foundation repairs and conditional multi-probe Theorem 4. Integer/cutoff/error fixes made; Hypothesis B remained a premise and Theorem4 retained (2N_3\le D\le n). The conditional route cannot produce an unconditional result once its premise is refuted.
- **2026-10-15, PRs #29–30:** exact dense transfer refuted selected-group Hypothesis B; handoff separated the scalar bus result from high-dimensional capacity and opened Lemma M.
- **2026-10-15–16, PRs #31–32:** first-order gather listing corrected and independently audited; higher-order $M_{rest}$ published but unaudited. The high-dimensional original problem and logarithmic-loss question remain open.

## 12. Full source index and coverage

The tables generated below list every accessible branch, every PR head, all 123 theory collections across the union of refs, and all 46 experiment collections. Main-branch theory records retain their existing indexed summary and relative source link. Theory folders absent from main use an immutable commit-pinned GitHub tree link. The old `theory/INDEX.md` has 108 rows for 106 unique source folders because two recovery rows are duplicated verbatim; this atlas lists each source folder once. `experiments/INDEX.md` indexes six finite-N protected-channel suites, not all experiment families.

### Canonical navigation and lane records

| Source | Role and recorded status | Coverage note |
|---|---|---|
| [`README.md`](../README.md) | Mission, original problem framing, and repository entry point | Read as contract context; mathematical statuses defer to scoped proof/review records. |
| [`AGENTS.md`](../AGENTS.md) | Governance and novelty standard | Read-only; not modified. |
| [`CURRENT_THEORY.md`](CURRENT_THEORY.md) | Authoritative consolidated legacy snapshot dated 2026-10-06 | Predates most PRs #24–32; later scoped audits override only claims they explicitly review. |
| [`INDEX.md`](INDEX.md) | 108 legacy status rows covering 106 unique main-branch theory folders | Two recovery rows duplicate verbatim; this atlas de-duplicates the folder list and preserves the source index. |
| [`experiments/INDEX.md`](../experiments/INDEX.md) | Entry to six finite-N protected-channel suites | Does not index all experiment collections; all 46 are listed in this atlas. |
| [`EXPERIMENT_HISTORY.md`](EXPERIMENT_HISTORY.md) | Saved empirical evidence across all 46 experiment collections, including outcomes, scope, duplicates, and non-runs | Distinguishes numerical results from proofs and lists coverage limits. |
| [`Claude_Research.md`](../docs/notebooks/Claude_Research.md) | Claude lane research notebook; historical top resume points to 2026-10-02 material | Resume is stale relative to PR24–32; use dated theory folders and later audits for status. |
| [`Codex_Research.md`](../docs/notebooks/Codex_Research.md) | Codex lane research notebook; top resume includes 2026-10-04 corridor results | Notebook records mix accepted, scoped, pending-review, and interim findings; do not promote a resume claim without its review/source. |
| [`Cursor_Research.md`](../docs/notebooks/Cursor_Research.md) | Cursor/Gemini lane: negative-space screen, 103 candidates, AMS protocol/results | Zero survivors applies to that recorded candidate set and screen, not all possible architectures. |


**Coverage boundary.** Snapshot 2026-10-17: 32 original local branch tips, 18 GitHub branch heads, and PR heads #1–32 (22 merged, 10 open, none closed), totaling 82 branch/PR snapshot refs plus symbolic `origin/HEAD`. Their reachable union contains 495 distinct commits and 5,585 tracked paths before the new research entry-point page; the consolidated tree includes that full path union plus `RESEARCH_START_HERE.md`. The union contains 123 theory folders, 46 experiment collections, and one prototype suite with 16 numbered experiments. A complete external bundle captured 176 refs and 507 reachable commits at backup time; `git bundle verify` and an independent bare clone matched all original local tips, remote heads, and PR heads. Local recovery refs are `refs/archive/local/<branch>`, `refs/archive/remote-heads/<branch>`, and `refs/archive/pr-heads/<number>`. Shared paths with divergent historical blobs retain the `origin/main` snapshot in the consolidated tree, except the explicitly curated archive navigation/status edits; branch-only files are included from a containing archived tree. Other historical blobs remain recoverable from the integration commit parents and verified bundle.

This is not a line-by-line re-proof of every historic proof. Older status claims were cross-checked against the 2026-10-06 `CURRENT_THEORY.md` and `INDEX.md`; detailed recent PRs #23–32 and their listed proof/audit/verification records were read and compared. The three long lane notebooks were inspected for their top resume/current-status blocks and selected navigation/status passages, not read line-by-line; notebook prose not indexed in theory folders may therefore be absent from the curated finding IDs. All 46 experiment collections are path-indexed, but their scripts, raw data, and generated workspaces were not all opened or rerun. The primary checkout had 20 untracked paths: 17 generated GAS-0 workspaces were not exhaustively inspected; two local PR29 audit copies were byte-identical to tracked PR29 audit trees (22 and 27 non-cache files); one local-only joint audit was reviewed at summary level. The joint audit reported Codex multi-column frontier VALID in scope and Gemini filter-bank result PARTIAL; its (n^{3/16}/3) construction is older/weaker than the later (n/(10^{70}\log\log n)) admissible-regime result. A deleted `PERPLEXITY_WRITE_TEST.md` create/edit/delete sequence was found in historical commits and classified as a non-research test artifact. These limitations are preserved rather than described as complete coverage.

The atlas contains 42 curated finding IDs (8 established/scoped, 4 author-proved or awaiting audit, 10 open, 8 refuted, and 12 numerical/experimental records), cross-referenced to 108 legacy index rows and 123 distinct theory folders. These counts identify archive records; one folder can contain multiple claims, so they are not a claim that the research contains only 42 findings. No model training or new experiment was run. The validation pass after authoring independently regenerates branch, PR, commit, source-folder, and experiment-folder counts; checks every source link and PR hash against the fetched refs; and checks whitespace. No proofs, experiments, notebooks, or governance files are modified by this archive.

### Pull-request inventory (all accessible PRs)

At the 2026-10-17 snapshot, PR head commits are pinned locally as `refs/archive/pr-heads/<number>` for #1–32; the exact SHA for each is listed below. Remote PR branches were not changed.


| PR | Title | State | Date | Head branch | Head commit |
| --- | --- | --- | --- | --- | --- |
| [#1](https://github.com/soma2-stack/AI-Architecture-Research/pull/1) | Merge latest Claude research checkpoint | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `ad32b9b7b99d739f95f17a99fa652857e67048ca` |
| [#2](https://github.com/soma2-stack/AI-Architecture-Research/pull/2) | Merge Claude calibration re-audit | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `f91df88b5cbba25722e0759dff2fc6e1d775f35f` |
| [#3](https://github.com/soma2-stack/AI-Architecture-Research/pull/3) | Merge Claude native-coupling research round | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `939653d89572f8178b1952df9a978bef09113ae5` |
| [#4](https://github.com/soma2-stack/AI-Architecture-Research/pull/4) | Sync latest Cursor learning-dynamics research | MERGED | 2026-09-28 | `codex/cursor-local-snapshot-20260927` | `a1a58187f56f80b5a570dabd916c01e16385dd73` |
| [#5](https://github.com/soma2-stack/AI-Architecture-Research/pull/5) | Merge Claude learning-dynamics research | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `baedbce6a9b1d54756b72d298404bd57b8cfc327` |
| [#6](https://github.com/soma2-stack/AI-Architecture-Research/pull/6) | Sync Cursor benchmark-suite design | MERGED | 2026-09-28 | `codex/cursor-local-snapshot-20260927-v2` | `dcea4510df75d85326455d8a31049c8c084a64bb` |
| [#7](https://github.com/soma2-stack/AI-Architecture-Research/pull/7) | Merge Claude automated-search protocol design | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `3617547d324f2a929918ebe352bb10ea4442155a` |
| [#8](https://github.com/soma2-stack/AI-Architecture-Research/pull/8) | Merge AMS v2 Stage-0 implementation and validity report | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `ef635b12045f574adcf4a0b7c3056c8f95954fbe` |
| [#9](https://github.com/soma2-stack/AI-Architecture-Research/pull/9) | Merge AMS v3 Stage-0 pass and Stage-1 calibration stop | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `68cc330e8cdf23958f51aa285ca8dee0116170fe` |
| [#10](https://github.com/soma2-stack/AI-Architecture-Research/pull/10) | Merge AMS v4 Stage-1 oracle stop and diagnostics | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `1ca7fc2f520ce7a177d9dff7653fddbab6537821` |
| [#11](https://github.com/soma2-stack/AI-Architecture-Research/pull/11) | AMS v5 Stage-1 pass, Stage-2 defect stop, and exact repair rerun | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `9dd8a5e409e6c61551179eb3610a80fc84ec09d9` |
| [#12](https://github.com/soma2-stack/AI-Architecture-Research/pull/12) | Merge AMS v5 repaired Stage-2 zero-yield result | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `deaa05d661beebf811635b23c41acd056d9d909d` |
| [#13](https://github.com/soma2-stack/AI-Architecture-Research/pull/13) | AMS v7 Stage 2 complete: static validation PASS, 8 promoted (all C*) | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `ec27e353ab658ea3f68ab53f53a06841a120474d` |
| [#14](https://github.com/soma2-stack/AI-Architecture-Research/pull/14) | Merge AMS v8 complete result: 0/42 confirmed, no promotions | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `d8d6761d047046a1338749c1f6fd8c8466a9e964` |
| [#15](https://github.com/soma2-stack/AI-Architecture-Research/pull/15) | Merge post-v8 grammar-gap audit | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `8325d3c9bf33ba4d7d909fb6736e7d02b4c6ec35` |
| [#16](https://github.com/soma2-stack/AI-Architecture-Research/pull/16) | Merge GG2 closure and close grammar-expansion path | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `1acd16d1157d989a8ae25168a8b3dc8f628b29e6` |
| [#17](https://github.com/soma2-stack/AI-Architecture-Research/pull/17) | Merge OMD-0 target screening | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `5747359ee4be16a04ef2fdc66ace1c3500fc4399` |
| [#18](https://github.com/soma2-stack/AI-Architecture-Research/pull/18) | Merge OMD-PILOT-1 Phase A failure evidence | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `a03b88717579df0157aa1b6a61f672cc59602b86` |
| [#19](https://github.com/soma2-stack/AI-Architecture-Research/pull/19) | Add GAS-0 Verified Project State design | MERGED | 2026-09-28 | `claude/admiring-turing-cvyhm0` | `da390e858ff2ff1acb356c98820c36e9053effe4` |
| [#20](https://github.com/soma2-stack/AI-Architecture-Research/pull/20) | GAS-0 VPS harness quality/validity fixes | MERGED | 2026-09-29 | `claude/admiring-turing-cvyhm0` | `8e64c850aea05586dbbcd178f2b396f0de4ebe19` |
| [#21](https://github.com/soma2-stack/AI-Architecture-Research/pull/21) | Consolidate research state and repository navigation | MERGED | 2026-10-05 | `cleanup/research-consolidation-20261004` | `5a9cae006494f7458446af6731aeb48124d04ade` |
| [#22](https://github.com/soma2-stack/AI-Architecture-Research/pull/22) | Clean up repository root documentation | MERGED | 2026-10-05 | `cleanup/root-docs-20261005` | `755d16fc7319cb73c6c0433b2638df3a2326410b` |
| [#23](https://github.com/soma2-stack/AI-Architecture-Research/pull/23) | Develop six untrained RNN architecture paths and CPU comparisons | OPEN | 2026-10-07 | `prototype/rnn-llm-architecture-v0-20261007` | `192df629e060def0983c4e85f70c4dd01b15b6a0` |
| [#24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24) | Audit shift-holonomy recurrence; scope verified QSR result; original problem OPEN | OPEN | 2026-10-13 | `claude/shift-holonomy-audit-20261013` | `d899895aab81b36a3128a375ae2238b08f73f4af` |
| [#25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25) | Independent hostile review of PR24: QSR theorem survives; rounding and scope corrections | OPEN | 2026-10-13 | `codex/pr24-independent-hostile-review` | `50bb5ffabf33b28099238acb6440cb1a349079e3` |
| [#26](https://github.com/soma2-stack/AI-Architecture-Research/pull/26) | Neutral-path tax test: Householder hub-broadcast candidate (exact lemmas + numerics; tax and main problem still OPEN) | OPEN | 2026-10-14 | `claude/neutral-path-tax-20261013` | `e13311b1d4d6d7ea227f7c9caa1931636cb55502` |
| [#27](https://github.com/soma2-stack/AI-Architecture-Research/pull/27) | Audited K-probe barrier: repair credit scopes, constants and horizon proof; main problem OPEN | OPEN | 2026-10-14 | `claude/narrow-capture-hub-20261013` | `c9874081461139373a276efeb47394d50781c0e3` |
| [#28](https://github.com/soma2-stack/AI-Architecture-Research/pull/28) | Repair multi-probe bounds: exact query cutoff and scoped conditional Theorem 4 | OPEN | 2026-10-14 | `claude/multiprobe-memory-20261014` | `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88` |
| [#29](https://github.com/soma2-stack/AI-Architecture-Research/pull/29) | Hypothesis B refuted: drift capture by the gather spike; exact bus structure; Lemma M isolated (pending review) | OPEN | 2026-10-15 | `claude/hypothesis-b-bus-20261015` | `f05694454956edab849ebe7d1858131eaca4174c` |
| [#30](https://github.com/soma2-stack/AI-Architecture-Research/pull/30) | Consolidated handoff: Claude PR24–29 results and Codex audits | OPEN | 2026-10-15 | `docs/claude-research-handoff-20261015` | `afb6f3c5d09f0ffbaba23aca1dfa2db4fb73b347` |
| [#31](https://github.com/soma2-stack/AI-Architecture-Research/pull/31) | Lemma M: first-order gather capacity theorem; corrected bus-listing target; Lemma M_rest open (pending audit) | OPEN | 2026-10-15 | `claude/lemma-m-bus-capacity-20261015` | `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab` |
| [#32](https://github.com/soma2-stack/AI-Architecture-Research/pull/32) | Lemma M_rest: two-stream bus structure, no amplification, operator-norm reduction, centered channel (pending audit) | OPEN | 2026-10-16 | `claude/lemma-m-rest-20261016` | `cef12b3eb6e5a8e6dbc75904253222b57eda188c` |

### GitHub branch head snapshot (18; captured 2026-10-17)

Remote branches are unchanged. The exact fetched snapshot is pinned locally under `refs/archive/remote-heads/<branch>`.

| Remote branch | Commit | Local recovery ref |
| --- | --- | --- |
| `astra/private-survivor-independent-20261008` | `6297b112bcd7f0bea312a98cc81ecd956127825b` | `refs/archive/remote-heads/astra/private-survivor-independent-20261008` |
| `claude/gallant-bardeen-ybxn57` | `d8ed873a28ed952161a461917a45a812d6253d2b` | `refs/archive/remote-heads/claude/gallant-bardeen-ybxn57` |
| `claude/hypothesis-b-bus-20261015` | `f05694454956edab849ebe7d1858131eaca4174c` | `refs/archive/remote-heads/claude/hypothesis-b-bus-20261015` |
| `claude/lemma-m-bus-capacity-20261015` | `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab` | `refs/archive/remote-heads/claude/lemma-m-bus-capacity-20261015` |
| `claude/lemma-m-rest-20261016` | `cef12b3eb6e5a8e6dbc75904253222b57eda188c` | `refs/archive/remote-heads/claude/lemma-m-rest-20261016` |
| `claude/multiprobe-memory-20261014` | `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88` | `refs/archive/remote-heads/claude/multiprobe-memory-20261014` |
| `claude/narrow-capture-hub-20261013` | `c9874081461139373a276efeb47394d50781c0e3` | `refs/archive/remote-heads/claude/narrow-capture-hub-20261013` |
| `claude/neutral-path-tax-20261013` | `e13311b1d4d6d7ea227f7c9caa1931636cb55502` | `refs/archive/remote-heads/claude/neutral-path-tax-20261013` |
| `claude/shift-holonomy-audit-20261013` | `d899895aab81b36a3128a375ae2238b08f73f4af` | `refs/archive/remote-heads/claude/shift-holonomy-audit-20261013` |
| `codex/pr24-independent-hostile-review` | `50bb5ffabf33b28099238acb6440cb1a349079e3` | `refs/archive/remote-heads/codex/pr24-independent-hostile-review` |
| `codex/route7a-long-window-20261008` | `075c5ffdb0c08a37245260c55df401654761bc96` | `refs/archive/remote-heads/codex/route7a-long-window-20261008` |
| `docs/claude-research-handoff-20261015` | `afb6f3c5d09f0ffbaba23aca1dfa2db4fb73b347` | `refs/archive/remote-heads/docs/claude-research-handoff-20261015` |
| `gemini/astra-route7a-feedback-audit-20261008` | `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9` | `refs/archive/remote-heads/gemini/astra-route7a-feedback-audit-20261008` |
| `gemini/pr26-neutral-hole-audit-20261013` | `2f3a3d248e02306408195312f3ca258ac8b357e8` | `refs/archive/remote-heads/gemini/pr26-neutral-hole-audit-20261013` |
| `main` | `f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c` | `refs/archive/remote-heads/main` |
| `preserve/all-research-20261004` | `d1767d0a62dba90b03fd21e512b3db0c4efcd133` | `refs/archive/remote-heads/preserve/all-research-20261004` |
| `preserve/local-theory-20261004` | `74232f2d1d386db45ccd5712fc684da0d82d6733` | `refs/archive/remote-heads/preserve/local-theory-20261004` |
| `prototype/rnn-llm-architecture-v0-20261007` | `192df629e060def0983c4e85f70c4dd01b15b6a0` | `refs/archive/remote-heads/prototype/rnn-llm-architecture-v0-20261007` |

### Original local branch tips (32; snapshot 2026-10-17)

All original local tips are pinned under `refs/archive/local/<branch>` and in the verified external bundle.

| Original local branch | Commit | Recovery ref |
| --- | --- | --- |
| `astra/private-survivor-independent-20261008` | `f7eeff01a12c08d7229de36e9b457f3acd445138` | `refs/archive/local/astra/private-survivor-independent-20261008` |
| `claude/hypothesis-b-bus-20261015` | `f05694454956edab849ebe7d1858131eaca4174c` | `refs/archive/local/claude/hypothesis-b-bus-20261015` |
| `claude/lemma-m-bus-capacity-20261015` | `35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab` | `refs/archive/local/claude/lemma-m-bus-capacity-20261015` |
| `claude/lemma-m-rest-20261016` | `cef12b3eb6e5a8e6dbc75904253222b57eda188c` | `refs/archive/local/claude/lemma-m-rest-20261016` |
| `claude/multiprobe-memory-20261014` | `0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88` | `refs/archive/local/claude/multiprobe-memory-20261014` |
| `claude/narrow-capture-hub-20261013` | `c9874081461139373a276efeb47394d50781c0e3` | `refs/archive/local/claude/narrow-capture-hub-20261013` |
| `claude/neutral-path-tax-20261013` | `e13311b1d4d6d7ea227f7c9caa1931636cb55502` | `refs/archive/local/claude/neutral-path-tax-20261013` |
| `claude/shift-holonomy-audit-20261013` | `d899895aab81b36a3128a375ae2238b08f73f4af` | `refs/archive/local/claude/shift-holonomy-audit-20261013` |
| `codex/ams-v4-independent-verification-20260928` | `7771fa8f1680ee734e0980f4e2e22fa8068f539d` | `refs/archive/local/codex/ams-v4-independent-verification-20260928` |
| `codex/ams-v6-independent-audit-20260928` | `0b726b0465845d5addb159e3e882cf5eeb2114be` | `refs/archive/local/codex/ams-v6-independent-audit-20260928` |
| `codex/ar142-validity-audit-20260928` | `c5d3d2eef606bdd3b98e1a6edc7027bd3428b815` | `refs/archive/local/codex/ar142-validity-audit-20260928` |
| `codex/automated-novelty-gate-20260927` | `33fa190989f7cfade70f18a993f9ec4f98fa1003` | `refs/archive/local/codex/automated-novelty-gate-20260927` |
| `codex/cursor-local-snapshot-20260927` | `a1a58187f56f80b5a570dabd916c01e16385dd73` | `refs/archive/local/codex/cursor-local-snapshot-20260927` |
| `codex/cursor-local-snapshot-20260927-v2` | `dcea4510df75d85326455d8a31049c8c084a64bb` | `refs/archive/local/codex/cursor-local-snapshot-20260927-v2` |
| `codex/filter-calibration-20260927` | `03e99111efc0fe7522758b874214b39668424295` | `refs/archive/local/codex/filter-calibration-20260927` |
| `codex/learning-dynamics-sync-20260927` | `2d733ab30c0a7c57c0d253d9311ef9b10c334dec` | `refs/archive/local/codex/learning-dynamics-sync-20260927` |
| `codex/native-coupling-sync-20260927` | `7c938599c65b9d0cc04a76313c7a427e342f4ed6` | `refs/archive/local/codex/native-coupling-sync-20260927` |
| `codex/pr24-independent-hostile-review` | `50bb5ffabf33b28099238acb6440cb1a349079e3` | `refs/archive/local/codex/pr24-independent-hostile-review` |
| `codex/route7a-feedback-compression-20261008` | `1249c3c74347b205abd61dc09eceaa616d40135c` | `refs/archive/local/codex/route7a-feedback-compression-20261008` |
| `codex/route7a-long-window-20261008` | `075c5ffdb0c08a37245260c55df401654761bc96` | `refs/archive/local/codex/route7a-long-window-20261008` |
| `gemini/astra-route7a-feedback-audit-20261008` | `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9` | `refs/archive/local/gemini/astra-route7a-feedback-audit-20261008` |
| `gemini/checkpoint-recovery-audit-20261007` | `007fb25e7679a4874572cc5f4f2bbf0b507509d3` | `refs/archive/local/gemini/checkpoint-recovery-audit-20261007` |
| `gemini/gpt6-route7a-audit-20261007` | `da72532c8a01d0df66dcbc9a6e4756a0719949c9` | `refs/archive/local/gemini/gpt6-route7a-audit-20261007` |
| `gemini/growing-R-route7a-audit-20261007` | `127eb79af4866368192dbf27d7f6086adac02659` | `refs/archive/local/gemini/growing-R-route7a-audit-20261007` |
| `gemini/lemma-u-repair-audit-20261007` | `e2900e7706a3a2784466f95d044c483835f88dab` | `refs/archive/local/gemini/lemma-u-repair-audit-20261007` |
| `gemini/pr26-neutral-hole-audit-20261013` | `2f3a3d248e02306408195312f3ca258ac8b357e8` | `refs/archive/local/gemini/pr26-neutral-hole-audit-20261013` |
| `gemini/route7a-audit-20261007` | `aa72c30351f23f0d5344c7268105847a558ba916` | `refs/archive/local/gemini/route7a-audit-20261007` |
| `gemini/route7b-audit-20261007` | `a4538b27c76df7d7d7ba94b7645ddf3274c190f9` | `refs/archive/local/gemini/route7b-audit-20261007` |
| `gemini/time-varying-nearcritical-filter-bank-20261006` | `eb0374622b332149cd0f67dbb492f203f67c42a0` | `refs/archive/local/gemini/time-varying-nearcritical-filter-bank-20261006` |
| `main` | `f1fa85d976bc205f77d7fac101a975be001ded54` | `refs/archive/local/main` |
| `preserve/all-research-20261004` | `d1767d0a62dba90b03fd21e512b3db0c4efcd133` | `refs/archive/local/preserve/all-research-20261004` |
| `preserve/local-theory-20261004` | `74232f2d1d386db45ccd5712fc684da0d82d6733` | `refs/archive/local/preserve/local-theory-20261004` |

### Theory collection index (all branches)

One row per distinct theory folder (123 total). Main links are repository-relative. Off-main links pin the exact source tree commit. Existing 2026-10-06 index descriptions are retained where available; newer off-main records are explicitly scoped below.


| Source folder | Topic | Recorded status | Discovery summary / scope |
| --- | --- | --- | --- |
| [age_preserving_transport_basis_20261002](age_preserving_transport_basis_20261002/) | age preserving transport basis | VERIFIED | Fixed-profile gates admit quadratic memory; fixed anchors fail and renewal is not a reduction of arbitrary-gate compression. |
| [aperiodic_query_aggregation_20261001](aperiodic_query_aggregation_20261001/) | aperiodic query aggregation | VERIFIED | Bounded non-scalar events admit quadratic storage; arbitrary aperiodic gates remain outside the theorem. |
| [arbitrary_horizon_log_gap_20261001](arbitrary_horizon_log_gap_20261001/) | arbitrary horizon log gap | VERIFIED | Suffix lookback needs n log n steps, while exact eligibility traces give quadratic memory for the near-diagonal family. |
| [astra_private_survivor_independent_20261008](https://github.com/soma2-stack/AI-Architecture-Research/tree/6297b112bcd7f0bea312a98cc81ecd956127825b/theory/astra_private_survivor_independent_20261008) | Private survivor capture / interior modulation | PARTIAL / REVIEW PENDING | Exact paired histories and reference geometry; full legal-query gain is not established. |
| [astra_route7a_feedback_compression_20261008](astra_route7a_feedback_compression_20261008/) | Complete un-cleared trace-neutral donor feedback compression | VERIFIED IN STATED SCOPE | Author derives a complete common-field row bound and actual-input receiver comparison, then a continuous O(m+N) approximate code without final clear for consecutive three-step trace-neutral donors and distinct strong public captures, under explicit bath/front/query premises. Claims scoped D=o(n) at fixed C_T and Route scaling; no general target resolution or constructive frontier improvement. Long-window compensation remains OPEN; exact constant-field cancellation sharpens the next obligation. |
| [astra_route7a_long_window_20261008](astra_route7a_long_window_20261008/) | Long-window trace-neutral feedback experiments and recent-block code | PENDING REVIEW | Extends corrected sparse chronological evaluator to delayed compensation W=1..64; full M/L/H query searches, independent-control spectra, million-width reference cases. Author derives centered Abel identity, explicit public bath/front sufficient certificate and uniform-in-W recent-block donor code O((m+N) log R). Full D=o(n) corollary is conditional and applies to an explicitly held-high public survivor bank; autonomous public-cohort complement and overall strict-budget target remain OPEN. |
| [astra_route7a_reservoir_20261007](astra_route7a_reservoir_20261007/) | Route 7A reservoir and recent-capture code | PENDING REVIEW | Author derives a public O(m+N) feedback parameter space and legal-query recent-capture code; claims D=o(n) for fixed-source distinct strong public captures with final clear, including high donors at capture. No general signal-mass or Route-7A impossibility claim. Exact trace-neutral no-clear alternative remains OPEN. |
| [astra_separated_strong_capture_20261007](astra_separated_strong_capture_20261007/) | Separated strong-capture bath dissipation and signal budget | PENDING REVIEW | Cone-decomposition storage gives ordinary output dissipation; capture crossing is paid by chronological bath dissipation for gaps at least 100/p, yielding a scoped Lambda<=2 sqrt$K$ N claim. Close captures and unaccounted dense perturbations remain outside scope. |
| [astra_theorem_b_audit_20261007](astra_theorem_b_audit_20261007/) | Independent Theorem B audit | PARTIAL | Abstract width theorem verified after repairing kernel inclusion; exact public segment reduction and Carl–Pajor indexing checked. Legal-query corollary remains conditional on upstream checkpoints and repaired mass theorem. |
| [claude_absolute_energy_review_20261003](claude_absolute_energy_review_20261003/) | claude absolute energy review | VERIFIED | Independent audit: Zero endpoint requires growing absolute energy; this is feasibility, not a memory upper bound. |
| [claude_aperiodic_review_20261001](claude_aperiodic_review_20261001/) | claude aperiodic review | VERIFIED | Independent audit: Bounded non-scalar events admit quadratic storage; arbitrary aperiodic gates remain outside the theorem. |
| [claude_autonomous_energy_upper_review_20261003](claude_autonomous_energy_upper_review_20261003/) | claude autonomous energy upper review | VERIFIED | Independent audit: In the frozen biased family constant absolute energy makes past credit negligible uniformly; forward state still costs n. |
| [claude_bounded_history_radius_review_20261003](claude_bounded_history_radius_review_20261003/) | claude bounded history radius review | VERIFIED | Independent audit: A joint 19/18 lower has local input radius below .02 around a public center whose absolute energy grows. |
| [claude_causal_width_20261002](claude_causal_width_20261002/) | claude causal width | SUPERSEDED | Exact probe absorption and a harmonic signal motivate a superlinear sketch, superseded by the checked joint theorem. |
| [claude_fixed_feature_width_review_20261002](claude_fixed_feature_width_review_20261002/) | claude fixed feature width review | VERIFIED | Independent audit: One joint fixed-feature section establishes floor(n/8) directions; ambient-ball reachability is not assumed. |
| [claude_hypothesis_b_bus_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/f05694454956edab849ebe7d1858131eaca4174c/theory/claude_hypothesis_b_bus_20261015) | Hypothesis B / dense bus counterexample | PROVED IN SELECTED-GROUP SCOPE | PR29 refutes Hypothesis B at D=1; it does not prove high-dimensional memory. |
| [claude_interacting_block_20261002](claude_interacting_block_20261002/) | claude interacting block | HISTORICAL | Scoped one-pulse and bounded-pulse claims verify; interacting-block charts and query hypotheses require later collision analysis. |
| [claude_lemma_m_bus_capacity_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab/theory/claude_lemma_m_bus_capacity_20261015) | Lemma M first-order gather listing | VERIFIED IN STATED SCOPE | PR31 audit verifies first-order theorem and corrected constants; M_rest remains open. |
| [claude_lemma_m_rest_20261016](https://github.com/soma2-stack/AI-Architecture-Research/tree/cef12b3eb6e5a8e6dbc75904253222b57eda188c/theory/claude_lemma_m_rest_20261016) | Lemma M_rest / two-stream operator listing | AUTHOR-PROVED / UNAUDITED | PR32 report only; higher-order and full operator listing remain open. |
| [claude_lemma_u_repair_20261007](claude_lemma_u_repair_20261007/) | Lemma U repair: dependent Walsh characters and the Theorem B-F constant | VERIFIED IN STATED SCOPE | Refutes Lemma U (\|\|U_prot\|\|<=2) and the Gemini Gram/Gershgorin repair for linearly dependent distinct labels: the cross terms do not decay, and at a g_H=1 (or ->1) sup over R of \|\|U_prot\|\| is at least 1+sqrt2 at every legal contrast, with explicit legal witnesses (e.g. 2.07 at R=4095). A new anti-concentration lemma (lazy walks with distinct steps hit any nonzero point with probability <=1/(k+1)) plus the discrete Hardy inequality gives \|\|U_prot\|\|<=2 sqrt(1+(a g_H)^2)<=2 sqrt2 for all distinct labels (<=sqrt2 for independent labels); the supremum is exact at b=g_H/2. Theorem B-F survives as D-q<=8(Lambda/s)^2 (not 4); the log-free Route-6 corollary constant becomes 1.42e10, still conditional. Theorem F untouched. Sharp constant for b<g_H/2 open (conjecture: 1+sqrt2). |
| [claude_log_gap_review_20261001](claude_log_gap_review_20261001/) | claude log gap review | VERIFIED | Independent audit: Suffix lookback needs n log n steps, while exact eligibility traces give quadratic memory for the near-diagonal family. |
| [claude_moment_merger_review_20261001](claude_moment_merger_review_20261001/) | claude moment merger review | VERIFIED | Verifies covariance and counts; refutes convex packet merging and round-robin scheduling as general compression. |
| [claude_moving_spike_remainder_20261002](claude_moving_spike_remainder_20261002/) | claude moving spike remainder | VERIFIED | Exact moving spike plus bounded remainder provides legal-query uppers and certified collisions in sustained charts. |
| [claude_multidonor_joint_section_20261004](claude_multidonor_joint_section_20261004/) | claude multidonor joint section | CONDITIONAL | Exact transfer representation is newly derived; complete compression depends on a sparse timing-signal hypothesis. |
| [claude_multiprobe_memory_20261014](https://github.com/soma2-stack/AI-Architecture-Research/tree/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/claude_multiprobe_memory_20261014) | Multi-probe conditional Theorem 4 | VERIFIED / CONDITIONAL | Thms 2–3 and cutoff checked; Theorem 4 assumes Hypothesis B, which PR29 refutes. |
| [claude_narrow_capture_hub_20261013](https://github.com/soma2-stack/AI-Architecture-Research/tree/c9874081461139373a276efeb47394d50781c0e3/theory/claude_narrow_capture_hub_20261013) | Protected-set / bath / state-comparison foundation | VERIFIED IN STATED FAMILY | PR27 fixed-K public-schedule theorem; not arbitrary schedules or full d_F. |
| [claude_near_critical_review_20261001](claude_near_critical_review_20261001/) | claude near critical review | VERIFIED | Independent audit: Constant-gap worst case is Theta(n); shrinking-gap matching lower bounds were left open here. |
| [claude_neutral_path_tax_20261013](https://github.com/soma2-stack/AI-Architecture-Research/tree/e13311b1d4d6d7ea227f7c9caa1931636cb55502/theory/claude_neutral_path_tax_20261013) | Neutral-path credit tax | LOCAL LEMMA VERIFIED; GLOBAL TAX CONJECTURAL | Lemma 8.1 is a one-step unweighted trace statement; cumulative credit tax is not proved. |
| [claude_operator_dimension_review_20261002](claude_operator_dimension_review_20261002/) | claude operator dimension review | VERIFIED | Independent audit: Observable operator norms and aggregate identities are scoped; ambient operator visibility is not reachable robust dimension. |
| [claude_quadratic_review_20261001](claude_quadratic_review_20261001/) | claude quadratic review | VERIFIED | Independent audit: A joint normalized fixed-hidden section proves Omega_c(n^2) at gamma=c/n, matching finite O(n)-horizon memory. |
| [claude_rotating_gate_review_20261001](claude_rotating_gate_review_20261001/) | claude rotating gate review | VERIFIED | Independent audit: Scalar and fixed-period gates have quadratic encoders; low-rank and fixed-Krylov methods fail within their tested scopes. |
| [claude_route7b_mtab_20261007](claude_route7b_mtab_20261007/) | Route 7B MTAB: exact operator, no-reuse theorem, TV-W | PENDING REVIEW | Derives the exact MTAB feedback-to-protected operator x=C^(-1/2)P0 Phi y (classes read the cumulative signal through monotone measures). Factorisation width theorem (generalises Theorem F) and Theorem NC: for non-crossing public survivor profiles D-q<=((2+sqrt2)/3)^2 (\|\|B\|\| Lambda/s)^2 ~ 1.295(Lambda/s)^2, uniform in classes, horizon, timescales (sharp Haar constant via a Takagi-Landsberg bound). Both proposed MTAB designs (multi-rate, staggered) are non-crossing, so MTAB as designed is refuted: many independent filters (large operator norm) but no mass reuse. Crossing families: weak M-order bound; all legal/idealised crossing families incl. new MTAB-X bands certify gamma<=1.04 (Conjecture MON open). Literal TV-W refuted by repeated filters (not corridor-realizable); strong form TV-W* open in general. Next: prove MON and long-mask passivity. |
| [claude_route_7b_20261007](claude_route_7b_20261007/) | Route 7B inventions and log-free width theorem | PENDING REVIEW | Does not reach D=Omega(n) with mT=o(n^(3/2)). Author-proved (unreviewed): Ky Fan-type sparsity lemma (coindex of l1-ball minus l2-ball is floor(1/r^2), no log), log-free width bound D<=q+(\|\|U\|\| Lambda/s)^2, Lemma U giving a log- and C_CP-free Theorem B variant D-q<=4(Lambda/s)^2 for one-step captures, and Lemma TV (public survivor filters have sup<=1, TV<=1). Candidates: multi-timescale accumulator bank OPEN (leaning negative); private gate-coded captures refuted by rank-one collapse/scaling; track-sweep gate field only reaches the n^(3/2) boundary. Next: TV-filter width conjecture. Lemma U (<=2) refuted as stated for dependent labels; corrected bound 2 sqrt2 and Theorem B-F constant 8 in [claude_lemma_u_repair_20261007](claude_lemma_u_repair_20261007/). |
| [claude_shift_holonomy_audit_20261013](https://github.com/soma2-stack/AI-Architecture-Research/tree/d899895aab81b36a3128a375ae2238b08f73f4af/theory/claude_shift_holonomy_audit_20261013) | QSR shift-holonomy robust section | VERIFIED IN MODIFIED QSR | Does not transfer to frozen dense tanh; finite-size D bound is n/1004. |
| [claude_transport_basis_review_20261002](claude_transport_basis_review_20261002/) | claude transport basis review | VERIFIED | Independent audit: Fixed-profile gates admit quadratic memory; fixed anchors fail and renewal is not a reduction of arbitrary-gate compression. |
| [claude_two_pulse_additivity_20261002](claude_two_pulse_additivity_20261002/) | claude two pulse additivity | VERIFIED | Bounded pulse count caps dimension linearly; the stronger one-pulse construction requires its independent Codex audit. |
| [claude_width_scaling_review_20261001](claude_width_scaling_review_20261001/) | claude width scaling review | VERIFIED | Independent audit: Contractive upper and margin ceiling are valid but loose; the review replaces the quadratic target with a counted linear window. |
| [codex_absolute_history_energy_20261003](codex_absolute_history_energy_20261003/) | codex absolute history energy | VERIFIED | Zero endpoint requires growing absolute energy; this is feasibility, not a memory upper bound. |
| [codex_autonomous_absolute_energy_20261003](codex_autonomous_absolute_energy_20261003/) | codex autonomous absolute energy | VERIFIED | In the frozen biased family constant absolute energy makes past credit negligible uniformly; forward state still costs n. |
| [codex_bounded_history_multiharmonic_20261003](codex_bounded_history_multiharmonic_20261003/) | codex bounded history multiharmonic | ACCEPTED | A joint 19/18 lower has local input radius below .02 around a public center whose absolute energy grows. |
| [codex_causal_suffix_width_20261002](codex_causal_suffix_width_20261002/) | codex causal suffix width | VERIFIED | Suffix metric is nonexpansive; a one-time merge works but a linear causal encoder was not established. |
| [codex_complete_query_normalization_recovery_20261007](codex_complete_query_normalization_recovery_20261007/) | Complete legal-query normalization source recovery | PENDING REVIEW | Exact 7.213 and eta<.001 derivation not recovered; older legal-query metric and component ledgers are identified, with missing calculations stated explicitly. |
| [codex_cross_pr_final_audit_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/codex_cross_pr_final_audit_20261015) | Cross-PR audit #27–28 | INDEPENDENT AUDIT | Verifies scoped dependencies and conditional theorem; preserves full problem as open. |
| [codex_d2_time_varying_repair_20261005](codex_d2_time_varying_repair_20261005/) | time-varying D=2 repair | PENDING REVIEW | Author derivation repairs the chronological sign argument in its scoped auxiliary and full-front model; independent review remains pending. |
| [codex_energy_credit_tradeoff_20261003](codex_energy_credit_tradeoff_20261003/) | codex energy credit tradeoff | SUPERSEDED | Short harmonic packets give superlinear dimension at energy exponent 7/8, with scoped localized tradeoffs. |
| [codex_energy_threshold_improvement_20261003](codex_energy_threshold_improvement_20261003/) | codex energy threshold improvement | SUPERSEDED | Rebalanced joint profiles and modulation yield exponent 3/4 with F^(9/4) energy loss. |
| [codex_filtered_timing_packing_repair_20261005](codex_filtered_timing_packing_repair_20261005/) | filtered timing packing repair | PENDING REVIEW | Revisits filtered timing; a necessary disjoint-packing cap remains unresolved pending review. |
| [codex_frontier_invention_20261006](codex_frontier_invention_20261006/) | coded simultaneous private writing | PENDING REVIEW | Develops coded simultaneous donor controls; its author report explicitly awaits independent hostile review. |
| [codex_history_uniform_leverage_20261005](codex_history_uniform_leverage_20261005/) | history-uniform leverage | PENDING REVIEW | Scoped history-uniform leverage analysis; no broader conclusion is promoted here. |
| [codex_holding_cost_attack_20261003](codex_holding_cost_attack_20261003/) | codex holding cost attack | ACCEPTED | Best accepted packet gives D>=nF/10^7 at norm<=4e7 n^(3/4)F^(3/2); corridor construction is only a transport lemma. |
| [codex_intermediate_gate_credit_20261002](codex_intermediate_gate_credit_20261002/) | codex intermediate gate credit | VERIFIED | Intermediate gate words have a legal coupled lift, a joint linear section, and a uniform low-order chronological expansion. |
| [codex_linear_dimension_frontier_20261006](codex_linear_dimension_frontier_20261006/) | early-capture linear-dimension frontier | VERIFIED IN STATED SCOPE | Strict-budget result, linear boundary, and donor-control-family obstruction; see CURRENT_THEORY.md for the precise claims, caveat, and review calibration. |
| [codex_moving_cycle_parameter_exhaustion_20261007](codex_moving_cycle_parameter_exhaustion_20261007/) | Moving-cycle parameter exhaustion | PENDING REVIEW | Author claims a dimension-independent shared-field variation bound and q_total=o$K$ approximate moving-cycle parameter exhaustion for the fixed-source, no-wrap, publicly segmented one-step-capture family; independent hostile review is pending. |
| [codex_moving_probe_spatial_write_20261005](codex_moving_probe_spatial_write_20261005/) | moving-probe spatial write | PENDING REVIEW | Studies moving-probe gain in shared-corridor writes; not promoted beyond the source status. |
| [codex_multi_donor_joint_section_20261003](codex_multi_donor_joint_section_20261003/) | codex multi donor joint section | PENDING REVIEW | Multi-epoch legal candidates and scoped obstruction derivations do not produce superlinear dimension. |
| [codex_multicolumn_spatial_write_20261005](codex_multicolumn_spatial_write_20261005/) | multicolumn spatial write | PENDING REVIEW | Analyzes compensated shared multicolumn spatial writes; claims remain within the recorded scope pending review. |
| [codex_multiharmonic_consolidation_20261003](codex_multiharmonic_consolidation_20261003/) | codex multiharmonic consolidation | ACCEPTED | Growing-local-radius joint lower reaches Omega(n^(16/15)); no bounded absolute-energy claim. |
| [codex_multiharmonic_lower_20261002](codex_multiharmonic_lower_20261002/) | codex multiharmonic lower | ACCEPTED | Accepted joint 19/18 lower; single-harmonic normalization was corrected and growing-radius exponent strengthened later. |
| [codex_multisurvivor_hadamard_write_20261005](codex_multisurvivor_hadamard_write_20261005/) | multisurvivor Hadamard write | PENDING REVIEW | Scoped shared-corridor multisurvivor and Hadamard write analysis; author checks are not independent review. |
| [codex_online_gate_polynomial_20261002](codex_online_gate_polynomial_20261002/) | codex online gate polynomial | VERIFIED | Causal triangular recurrence and quadratic reference storage verify; exact realization rank is not finite-error memory. |
| [codex_pr24_hostile_review_20261013](https://github.com/soma2-stack/AI-Architecture-Research/tree/50bb5ffabf33b28099238acb6440cb1a349079e3/theory/codex_pr24_hostile_review_20261013) | Independent hostile review of PR24 | VERIFIED IN QSR SCOPE | Checks Lemmas 5.1–5.4 and corrections; no original-architecture transfer. |
| [codex_pr27_repair_verification_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/c9874081461139373a276efeb47394d50781c0e3/theory/codex_pr27_repair_verification_20261015) | PR27 repair verification | VERIFIED IN STATED FAMILY | Corrects credit split, operator order, attenuation, bath, horizon and probe scope. |
| [codex_pr28_repair_verification_20261014](https://github.com/soma2-stack/AI-Architecture-Research/tree/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/codex_pr28_repair_verification_20261014) | PR28 repair verification | VERIFIED / CONDITIONAL | Exact cutoff and dimension restrictions checked; Thm4 remains conditional on B. |
| [codex_pr29_dense_transfer_audit_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/f05694454956edab849ebe7d1858131eaca4174c/theory/codex_pr29_dense_transfer_audit_20261015) | Dense matrix transfer audit | PROVED IN SELECTED-GROUP SCOPE | Verifies prescribed matrix, cancellation, exact support and endpoint transfer. |
| [codex_pr29_independent_audit_20261015](https://github.com/soma2-stack/AI-Architecture-Research/tree/f05694454956edab849ebe7d1858131eaca4174c/theory/codex_pr29_independent_audit_20261015) | Independent Hypothesis B counterexample audit | PROVED IN STATED SCOPE | Lemma E and dense transfer checked; D=1 bus counterexample refutes B only. |
| [codex_pr31_repair_audit_20261016](https://github.com/soma2-stack/AI-Architecture-Research/tree/35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab/theory/codex_pr31_repair_audit_20261016) | Independent PR31 repair audit | VERIFIED IN FIRST-ORDER SCOPE | Checks corrected M1, nine terms, bath floor, ceilings and final error budget. |
| [codex_private_complement_leverage_20261005](codex_private_complement_leverage_20261005/) | private complement leverage | REFUTED | Refutes the proposed all-support complement-leverage cap; auxiliary calculations remain in the folder. |
| [codex_private_renewal_gamma_20261003](codex_private_renewal_gamma_20261003/) | codex private renewal gamma | ACCEPTED | Equal local codes can hide Gamma>.03 and one cheap robust direction; no superlinear dimension follows. |
| [codex_repeated_nearcritical_filter_write_20261005](codex_repeated_nearcritical_filter_write_20261005/) | repeated near-critical filter write | PENDING REVIEW | Author proves a scoped K=2 write; growing-K improvement remains open and independent hostile review is pending. |
| [codex_single_block_spatial_write_20261004](codex_single_block_spatial_write_20261004/) | codex single block spatial write | PENDING REVIEW | Nonuniform masks claim joint logarithmically many modes on one support; independent review remains pending and D is not superlinear. |
| [codex_stationary_parameter_complement_recovery_20261007](codex_stationary_parameter_complement_recovery_20261007/) | Stationary parameter-complement code source recovery | PENDING REVIEW | Exact q_stat<=R(2^R+1) derivation not recovered; stationary geometry ingredients are cited and the missing class-count proof is stated explicitly. |
| [codex_suffix_product_hostile_review_20261003](codex_suffix_product_hostile_review_20261003/) | codex suffix product hostile review | VERIFIED | Scoped paired obstruction verifies with stronger minimum code count and careful energy interpretation. |
| [codex_suffix_product_kernel_attack_20261003](codex_suffix_product_kernel_attack_20261003/) | codex suffix product kernel attack | ACCEPTED | Static quantile codes bound only the paired projected monotone suffix-product channel. |
| [codex_sustained_weak_gate_credit_20261002](codex_sustained_weak_gate_credit_20261002/) | codex sustained weak gate credit | VERIFIED | Sustained and K/t weakening subclasses have finite-error bounds, not a whole-class O(n) theorem. |
| [codex_timing_signal_J_20261004](codex_timing_signal_J_20261004/) | codex timing signal J | VERIFIED | A changing survivor set defeats uniform O(1/m_s) timing entries; large entries still represent one contrast. |
| [codex_two_pulse_corotating_20261002](codex_two_pulse_corotating_20261002/) | codex two pulse corotating | VERIFIED | The improved one-pulse lower is floor(n/4)-2 with arithmetic clarifications; co-rotating diagnostics are not superlinear proofs. |
| [codex_unpaired_corridor_sensitivity_20261003](codex_unpaired_corridor_sensitivity_20261003/) | codex unpaired corridor sensitivity | ACCEPTED | Complete differentiated ledger exposes common-mode private feedback and a short-packet obstruction; full corridor remains open. |
| [gamma_c_over_n_quadratic_20261001](gamma_c_over_n_quadratic_20261001/) | gamma c over n quadratic | VERIFIED | A joint normalized fixed-hidden section proves Omega_c(n^2) at gamma=c/n, matching finite O(n)-horizon memory. |
| [gemini_astra_route7a_feedback_audit_20261008](gemini_astra_route7a_feedback_audit_20261008/) | Hostile audit of Astra's Route 7A un-cleared feedback compression | VERIFIED IN STATED SCOPE | Independent hostile review: verifies exact O_* rank-2 expansion and complete recurrence identity (Eqs. 5-6); verifies terminal feedback row cancellation (e_P-e_T)^T H_t = 0 for T,P>>N, certifying J_*=O(C_T) envelope; verifies 3-step trace-neutral receiver contraction rho<0.995206 and cancellation of incoming trace tau, proving max_i \\|\\|V_i - V_*\\|\\| < 0.084 J_* uniformly; verifies exact public right parameter space dim(E_par)<=4m+4N; verifies Walsh character Chebyshev attenuation and cohort query dilution; verifies Borsuk-Ulam code dimension obstruction D<=O(m+N)=o(n) under explicit inherited premises; verifies that under constant feedback J, long-window variant has identically zero control response; long-window alternative under temporal variations remains OPEN. |
| [gemini_checkpoint_recovery_audit_20261007](gemini_checkpoint_recovery_audit_20261007/) | Checkpoint recovery audit: legal-query normalization and stationary complement | VERIFIED IN STATED SCOPE | Independent mathematical audit: 7.213 verified as conservative tuple-ledger constant 400*sigma/(2*sqrt(2)), while sharp constant is C<=0.048; eta<=8e-9 < 0.001 verified across all channels; stationary complement decomposition proves zero-sum cancellation, common donor mean in V_perp, and exact continuous code q_stat<=R(2^R+1) with q_stat=o$K$. |
| [gemini_gpt6_route7a_audit_20261007](gemini_gpt6_route7a_audit_20261007/) | Hostile audit of GPT-6 Route 7A trace-neutral diameter bound | VERIFIED IN STATED SCOPE | Independent hostile review: verifies Lemma 1 third-gate Lipschitz constant L_*=1.0002005314 uniformly over incoming local traces tau>=0; verifies Lemma 2 reference recurrence difference bound \|\|Delta M_N\|\|<=N sum \|\|Delta G_t\|\| fully tracking J, B feedback; verifies 1.45e-5 coefficient and nu_ref<=1.45e-5 C_T R^(3/2); verifies R<=26 cutoff (diameter < 0.002) for C_T<=1 with finite-n precharge qualification; verifies unit-Euclidean sphere bound R<=137; replicates numerical outputs of finite_probe.py to printed precision; clarifies simplified probe model vs legal frozen-tanh lift; confirms no counterexample to the upper bound exists. |
| [gemini_growing_R_route7a_audit_20261007](gemini_growing_R_route7a_audit_20261007/) | Hostile audit of GPT-6 growing-R local-direct bound | VERIFIED IN STATED SCOPE | Independent hostile review: verifies exact 3-step moving-characteristic response and trace matching; verifies stationary compensator cancellation Delta ell_comp = 0; verifies support of Delta L_N is at most 2m moving donor rows; verifies contraction factor rho <= 0.99520577 < 1 and fresh perturbation \|\|delta_fresh\|\| < 4 eps \|x-y\| via negative discriminant quadratic inequality; verifies uniform row bound \|\|Delta ell_R\|\| < 0.16687; verifies query bound nu_ref(Delta L_N) < 0.00852 sqrt(m/n) and critical threshold R >= 19 for m <= n/R; verifies that bounding L_N does not bound H_N = M_N - L_N, isolating the private feedback channel as the sole surviving mechanism; growing-R Route 7A remains OPEN. |
| [gemini_lemma_u_repair_audit_20261007](gemini_lemma_u_repair_audit_20261007/) | Hostile audit of Claude's Lemma U repair | VERIFIED IN STATED SCOPE | Independent hostile review: verifies Lemma A lazy-RW anti-concentration inequality via Walsh-Fourier expansion and differential identity; verifies discrete Hardy operator domination \|\|K\|\|<=4 giving \|\|P A_cap\|\|<=2 and \|\|U_prot\|\|<=2 sqrt(1+(a g_H)^2)<=2 sqrt2; refutes original Lemma U (<=2) via reproduced finite counterexamples (2.0346 at R=2047, 2.0746 at R=4095); confirms refutation of previous Gemini Gram-decay/Gershgorin repair (ratio > 1e16, off-diagonal row sum 2.2656 > 2.0); verifies certified counterexample at b=0.0025 (r=26, R~6.71e7, \|\|U_prot\|\|>=2.0039); verifies Theorem B-F dimension bound D-q<=floor(8(Lambda/s)^2)=o(n) in stated conditional scope. |
| [gemini_pr26_neutral_hole_audit_20261013](https://github.com/soma2-stack/AI-Architecture-Research/tree/2f3a3d248e02306408195312f3ca258ac8b357e8/theory/gemini_pr26_neutral_hole_audit_20261013) | PR26 neutral-hole audit | SCOPED ALGEBRA VERIFIED; GLOBAL THEOREM OPEN | Broadcast principle passes; robust strict-budget all-boundary construction does not. |
| [gemini_route7a_audit_20261007](gemini_route7a_audit_20261007/) | Focused Route 7A reservoir audit | VERIFIED IN STATED SCOPE | Independent hostile review: verifies public parameter subspace P<=4m+4N via exact Duhamel induction, two-step final-clear contraction on (H_t^S)^perp, legal-query estimate avoiding sqrt(r) via operator norm x survivor l2 bound, continuous recent-capture code q_recent<=(2ell+2)(4m+4N), and D=o(n) for the scoped public strong-capture/final-clear family. Trace-neutral write algebra and legality verified; un-cleared donor feedback alternative preserved OPEN. |
| [gemini_route7a_autonomous_survivor_audit_20261008](https://github.com/soma2-stack/AI-Architecture-Research/tree/075c5ffdb0c08a37245260c55df401654761bc96/theory/gemini_route7a_autonomous_survivor_audit_20261008) | Route 7A autonomous survivor audit | AUDIT RECORD; SCOPED | Source is branch-only; do not infer a complete moving-corridor theorem from it. |
| [gemini_route7b_audit_20261007](gemini_route7b_audit_20261007/) | Focused Route 7B audit (log-free width and mechanisms) | VERIFIED IN STATED SCOPE | Independent hostile review: verifies Lemma F and log-free Theorem F; refutes Lemma U character orthogonality for linearly dependent Walsh characters but verifies operator norm bound \|\|U_prot\|\|<=2; verifies Lemma TV; refutes/clarifies positive monotone filter conditioning claim; verifies Lemma C rank-one collapse; preserves MTAB as OPEN. |
| [gemini_time_varying_nearcritical_filter_bank_20261006](gemini_time_varying_nearcritical_filter_bank_20261006/) | time-varying near-critical filter bank | PENDING REVIEW | Author reports scoped K=3/4 results and a growing-K dilution obstruction; review status is not inferred from author labels. |
| [gpt6_mtab_focused_audit_20261007](gpt6_mtab_focused_audit_20261007/) | Independent focused mathematical review of Claude MTAB | VERIFIED IN STATED SCOPE | Checks exact public survivor operator, factorization Theorem Gamma, non-crossing Haar/Takagi Theorem NC with constant c*=(2+sqrt2)/3, original designs' common order, conditional M-order crossing bound and abstract TV-W counterexample. Public non-crossing mass reuse bounded, but full mT lower bound requires OPEN long-mask passivity/query premises; crossing MON/TV-W* OPEN. Includes independent finite Haar-prefix computations. |
| [gpt6_private_survivor_capture_20261008](https://github.com/soma2-stack/AI-Architecture-Research/tree/f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c/theory/gpt6_private_survivor_capture_20261008) | Private survivor capture versus private interior window modulation | PARTIAL / PENDING INDEPENDENT REVIEW | Balancing survivor +/- pairs with forced private gates preserves public forward bath and same hidden endpoint; naive unforced private +/- survivors fail tanh-sum cancellation. Held-high bank with PRIVATE Walsh-low capture gates admits author-only approximate code O((m+N)log R), conditional on Astra's donor/front/dense/query results and recent inter-capture aggregate proof. Independent private survivor gates at all high-window steps evade this particular common-aggregate code; finite full-rank-two one-step reference signals are ~1e-10 to 1e-9, not robust lower bounds. Geometry-admissible n=1,048,576,m=8,R=4,W=16 passes common endpoint and trace; no million-width optimized legal query. Main D=Omega(n),mT=o(n^(3/2)) OPEN. |
| [gpt6_route7a_chronological_public_20261007](gpt6_route7a_chronological_public_20261007/) | Route 7A corrected chronological reference-feedback simulation | EXPERIMENTAL / CORRECTED REPLAY / PENDING INDEPENDENT REVIEW | TWO load-bearing simulator bugs repaired: stale local sensitivity trace during precharge and double-offset stationary compensator coordinates. See ERRATUM.md and CORRECTED_RESULTS_20261008.md; original RESEARCH.md historical numerical tables and RESULTS.txt are SUPERSEDED. Corrected histories match local traces at each stage, complete endpoint at ~1e-16, and off-donor public gate differences <=2.22e-16. Best found one-step full-M query: 1.28e-9 (R2), 1.74e-9 (R4), 6.66e-9 (R16), 1.80e-8 (R32), 2.23e-8 (R48); separate H at R32=3.18e-9. Five-start query searches at R4,16 marginally improve found scores. Exact frozen reference O and chronological bath/front used, but admitted asymptotic S<=d/100 geometry not met, all legal futures unoptimized, no robust-width theorem; target OPEN. |
| [gpt6_route7a_fullH_spectrum_20261007](gpt6_route7a_fullH_spectrum_20261007/) | Route 7A un-cleared feedback H: matrix-free query optimization and Jacobian spectra | EXPERIMENTAL / PENDING REVIEW | Matrix-free full rank-two O_* recurrence and transpose independently pair-checked; optimized legal one-step and 1/2/4/8-step reference future gates on surrogate (public bath/front gates=1, toy survivor masks, small widths). n=8192,m=16: best full-M one-step response rises 2.38e-8 at R4 to 2.83e-6 at R128, below .002, but only a found query and all+ vs all- pair, not a supremum. For fixed optimized query, H control Jacobian has approximately m dominant singular directions while mR inputs grow (m=4,8 cases); other weak queries can show more directions. No legal lifted construction and no universal H bound. Growing-R robust memory target OPEN. |
| [gpt6_route7a_growing_R_local_20261007](gpt6_route7a_growing_R_local_20261007/) | Growing-R trace-neutral local-direct collapse; full feedback probe | VERIFIED IN STATED SCOPE | Exact moving-characteristic 3-step source-row identity and geometric stage attenuation rho<=0.995206 yield \|\|Delta L_N\|\|_op<0.16687 sqrt(2m), hence reference fixed-feature query <=0.00852 sqrt(m/n), falling below .002 whenever m<=n/R and R>=19. Stationary compensator local rows coincide. FULL private renewal H=M-L is NOT bounded; growing-R Route 7A remains OPEN. Matrix-free exact rank-two structural recurrence probed R<=128 with 12 selected legal-reference adjoints but bath/front and masks are toys, not full frozen-tanh certificates. Includes review handoff. |
| [gpt6_route7a_sparse_geometry_20261008](gpt6_route7a_sparse_geometry_20261008/) | Exact sparse chronological public-bath Gate evaluator and million-width Route 7A reference test | EXPERIMENTAL / PENDING INDEPENDENT REVIEW | Sparse state q*1+delta tracks full rank-two public chronological bath/front and public Walsh survivor excursions; matches corrected dense gate histories to <=4.44e-16 and M^T c to ~3e-16 relative across n=16k,32k,65k. At n=1,048,576,m=8,R=4,L=2048,N=2061,S=2073 meets n>=1e6 and S<=d/100=2621.44; same reference endpoint, exact boundary trace, inputs <.121. All-high legal one-step query value 2.02e-13; one legal box vertex ascent gives 5.37e-11 (FOUND value, not supremum). mR=32 far below cn, dense perturbation/root sigma approximated; no H width theorem. Full Route 7A OPEN. |
| [gpt6_route7a_trace_neutral_20261007](gpt6_route7a_trace_neutral_20261007/) | Route 7A trace-neutral un-cleared donor feedback diameter estimate | VERIFIED IN STATED SCOPE | Derives a uniform gate-Lipschitz/reference-feedback query diameter bound for Astra's exact 3-step family: nu_ref <= 1.45e-5 (N/sqrt(n)) R on all controls x in [-1,1]^(RK), hence <= 1.45e-5 C_T R^(3/2) when N<=C_T sqrt(nR); for C_T<=1 and R<=26 this is below 0.002 (dense correction negligible asymptotically in inherited regime). Natural unit-Euclidean control sphere has stronger bound <=1.45e-5 C_T R (R<=137). Structural full J/B recurrence numerical probes retained but NOT legal-query certificates. Diverging-R Route 7A remains OPEN. |
| [grok_bounded_history_radius_review_20261003](grok_bounded_history_radius_review_20261003/) | grok bounded history radius review | VERIFIED | Independent audit: A joint 19/18 lower has local input radius below .02 around a public center whose absolute energy grows. |
| [grok_causal_suffix_width_review_20261002](grok_causal_suffix_width_review_20261002/) | grok causal suffix width review | VERIFIED | Independent audit: Suffix metric is nonexpansive; a one-time merge works but a linear causal encoder was not established. |
| [grok_energy_credit_tradeoff_review_20261003](grok_energy_credit_tradeoff_review_20261003/) | grok energy credit tradeoff review | VERIFIED | Independent audit: Short harmonic packets give superlinear dimension at energy exponent 7/8, with scoped localized tradeoffs. |
| [grok_energy_threshold_improvement_review_20261003](grok_energy_threshold_improvement_review_20261003/) | grok energy threshold improvement review | VERIFIED | Independent audit: Rebalanced joint profiles and modulation yield exponent 3/4 with F^(9/4) energy loss. |
| [grok_filtered_timing_d2_20261004](grok_filtered_timing_d2_20261004/) | grok filtered timing d2 | SUPERSEDED | The first two-cohort square left an intermediate idle-gate band unproved. |
| [grok_filtered_timing_d2_band_20261004](grok_filtered_timing_d2_band_20261004/) | grok filtered timing d2 band | SUPERSEDED | A narrowed square still left monotonicity in an intermediate gate band unproved. |
| [grok_filtered_timing_d2_monotone_20261004](grok_filtered_timing_d2_monotone_20261004/) | grok filtered timing d2 monotone | PENDING REVIEW | Post-consolidation review found a proof gap: frozen-`A(q)` spectral signs do not establish the sign of the actual time-ordered products with changing `q_t`; the claimed joint D=2 square is not currently established. |
| [grok_filtered_timing_one_block_20261004](grok_filtered_timing_one_block_20261004/) | grok filtered timing one block | ACCEPTED | Narrow accepted observation: in the uniform matched-versus-low family the strong difference is the all-ones coefficient while orthogonal/zero-sum survivor components reproduce; its D=2 and disjoint-packing consequences remain pending. |
| [grok_filtered_timing_width_20261004](grok_filtered_timing_width_20261004/) | grok filtered timing width | HISTORICAL | Exact filtering, long-low-run erasure, and single-cohort flat-window collapse remain useful; the claimed necessary disjoint-packing cap is not established because its argument uses a visibility lower bound in the wrong direction. |
| [grok_holding_cost_attack_review_20261003](grok_holding_cost_attack_review_20261003/) | grok holding cost attack review | VERIFIED | Independent audit: Best accepted packet gives D>=nF/10^7 at norm<=4e7 n^(3/4)F^(3/2); corridor construction is only a transport lemma. |
| [grok_intermediate_gate_review_20261002](grok_intermediate_gate_review_20261002/) | grok intermediate gate review | VERIFIED | Independent audit: Intermediate gate words have a legal coupled lift, a joint linear section, and a uniform low-order chronological expansion. |
| [grok_multiharmonic_16_15_review_20261003](grok_multiharmonic_16_15_review_20261003/) | grok multiharmonic 16 15 review | VERIFIED | Independent audit: Growing-local-radius joint lower reaches Omega(n^(16/15)); no bounded absolute-energy claim. |
| [grok_multiharmonic_lower_review_20261002](grok_multiharmonic_lower_review_20261002/) | grok multiharmonic lower review | VERIFIED | Independent audit: Accepted joint 19/18 lower; single-harmonic normalization was corrected and growing-radius exponent strengthened later. |
| [grok_online_gate_polynomial_review_20261002](grok_online_gate_polynomial_review_20261002/) | grok online gate polynomial review | VERIFIED | Independent audit: Causal triangular recurrence and quadratic reference storage verify; exact realization rank is not finite-error memory. |
| [grok_permitted_query_reach_20261002](grok_permitted_query_reach_20261002/) | grok permitted query reach | HISTORICAL | Rejects a three-term adjoint formula and the one-sign-pattern replacement; diagnostic query searches do not prove width. |
| [grok_private_renewal_gamma_review_20261003](grok_private_renewal_gamma_review_20261003/) | grok private renewal gamma review | VERIFIED | Independent audit: Equal local codes can hide Gamma>.03 and one cheap robust direction; no superlinear dimension follows. |
| [grok_spike_remainder_review_20261002](grok_spike_remainder_review_20261002/) | grok spike remainder review | VERIFIED | Independent audit: Exact moving spike plus bounded remainder provides legal-query uppers and certified collisions in sustained charts. |
| [grok_sustained_weak_gate_review_20261002](grok_sustained_weak_gate_review_20261002/) | grok sustained weak gate review | VERIFIED | Independent audit: Sustained and K/t weakening subclasses have finite-error bounds, not a whole-class O(n) theorem. |
| [grok_timing_signal_J_review_20261004](grok_timing_signal_J_review_20261004/) | grok timing signal J review | VERIFIED | Independent audit: A changing survivor set defeats uniform O(1/m_s) timing entries; large entries still represent one contrast. |
| [near_critical_credit_phase_diagram_20261001](near_critical_credit_phase_diagram_20261001/) | near critical credit phase diagram | VERIFIED | Constant-gap worst case is Theta(n); shrinking-gap matching lower bounds were left open here. |
| [opus_segment_atom_width_20261007](opus_segment_atom_width_20261007/) | Segment-atom width bound (Theorem B) | PENDING REVIEW | Piecewise-parallel survivor readouts between one-step captures reduce TK width atoms to SK<=(2R+2)K; Carl–Pajor Gelfand numbers plus a nuisance-code Borsuk–Ulam map give D<=q+1+C_CP^2 c_B^2 (Lambda/s)^2 [1+log(SK/(D-q-1))]. Conditionally on moving-cycle exhaustion, the original checkpoints and a separated mass bound, D=O(C_T^2 (n/R) log R)=o(n) at Route-6 scaling for the separated low-donor-capture family; Carl–Pajor constant and the reader-support premise remain open. |
| [perplexity_accessibility_proof_draft_20261004](perplexity_accessibility_proof_draft_20261004/) | perplexity accessibility proof draft | PENDING REVIEW | Unique exact-accessibility proof draft is archived with source hashes; it is not an independently reviewed robust theorem. |
| [query_visible_operator_dimension_20261002](query_visible_operator_dimension_20261002/) | query visible operator dimension | VERIFIED | Observable operator norms and aggregate identities are scoped; ambient operator visibility is not reachable robust dimension. |
| [query_weighted_moment_merger_20261001](query_weighted_moment_merger_20261001/) | query weighted moment merger | REFUTED | Covariance/error identities and counts survive, but convex packet merging and round-robin scheduling fail as a general solution. |
| [reachable_fixed_feature_width_20261002](reachable_fixed_feature_width_20261002/) | reachable fixed feature width | VERIFIED | One joint fixed-feature section establishes floor(n/8) directions; ambient-ball reachability is not assumed. |
| [robust_width_scaling_20261001](robust_width_scaling_20261001/) | robust width scaling | SUPERSEDED | Contractive upper and margin ceiling are valid but loose; the review replaces the quadratic target with a counted linear window. |
| [rotating_gate_aggregation_20261001](rotating_gate_aggregation_20261001/) | rotating gate aggregation | VERIFIED | Scalar and fixed-period gates have quadratic encoders; low-rank and fixed-Krylov methods fail within their tested scopes. |
| [sol_k3_discrete_filter_comparison_20261006](sol_k3_discrete_filter_comparison_20261006/) | K=3 discrete filter comparison | REFUTED | Refutes the literal matched-filter word under the recorded exact gate-legality certificate. |


### Experiment collection index (all branches)


| Experiment collection | Search terms | Evidence note |
| --- | --- | --- |
| [ams_audit](../experiments/ams_audit/) | ams audit | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [anisotropic_robust_packing_20260930](../experiments/anisotropic_robust_packing_20260930/) | anisotropic robust packing 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [anisotropic_robust_packing_replay_20261001](../experiments/anisotropic_robust_packing_replay_20261001/) | anisotropic robust packing replay 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [antipodal_robust_dimension_20261001](../experiments/antipodal_robust_dimension_20261001/) | antipodal robust dimension 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [aperiodic_gate_spectrum_20261001](../experiments/aperiodic_gate_spectrum_20261001/) | aperiodic gate spectrum 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [approximate_observability_20260930](../experiments/approximate_observability_20260930/) | approximate observability 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [augmented_accessibility_proof_20260930](../experiments/augmented_accessibility_proof_20260930/) | augmented accessibility proof 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [automated_mechanism_search](../experiments/automated_mechanism_search/) | automated mechanism search | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [automated_mechanism_search_v9](../experiments/automated_mechanism_search_v9/) | automated mechanism search v9 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [cfwm](../experiments/cfwm/) | cfwm | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [claude_7d_direct_audit_20261001](../experiments/claude_7d_direct_audit_20261001/) | claude 7d direct audit 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [claude_8d_review_20261001](../experiments/claude_8d_review_20261001/) | claude 8d review 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [claude_radial_8d_review_20261001](../experiments/claude_radial_8d_review_20261001/) | claude radial 8d review 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [claude_rebalanced_7d_review_20261001](../experiments/claude_rebalanced_7d_review_20261001/) | claude rebalanced 7d review 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [claude_third_order_review_20261001](../experiments/claude_third_order_review_20261001/) | claude third order review 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [cleanroom_7d_interval_20261001](../experiments/cleanroom_7d_interval_20261001/) | cleanroom 7d interval 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [codex_antipodal_hostile_review_20261001](../experiments/codex_antipodal_hostile_review_20261001/) | codex antipodal hostile review 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [csl](../experiments/csl/) | csl | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [efd](../experiments/efd/) | efd | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [endpoint_certificate_20260930](../experiments/endpoint_certificate_20260930/) | endpoint certificate 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [endpoint_width_scaling_20260930](../experiments/endpoint_width_scaling_20260930/) | endpoint width scaling 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [exact_online_credit_stage_a_20260930](../experiments/exact_online_credit_stage_a_20260930/) | exact online credit stage a 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [exact_online_credit_stage_b2_20260930](../experiments/exact_online_credit_stage_b2_20260930/) | exact online credit stage b2 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [exact_online_credit_stage_b_20260930](../experiments/exact_online_credit_stage_b_20260930/) | exact online credit stage b 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [feature_revision_20260930](../experiments/feature_revision_20260930/) | feature revision 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_clean_mask_scaling_20261006](../experiments/finite_n_clean_mask_scaling_20261006/) | finite n clean mask scaling 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_clear_scaling_20261006](../experiments/finite_n_clear_scaling_20261006/) | finite n clear scaling 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_early_capture_20261006](../experiments/finite_n_early_capture_20261006/) | finite n early capture 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_multistage_capture_20261006](../experiments/finite_n_multistage_capture_20261006/) | finite n multistage capture 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_r20_r32_scaling_20261006](../experiments/finite_n_r20_r32_scaling_20261006/) | finite n r20 r32 scaling 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [finite_n_r8_diagnosis_20261006](../experiments/finite_n_r8_diagnosis_20261006/) | finite n r8 diagnosis 20261006 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [fixed_feature_reachable_operator_20261002](../experiments/fixed_feature_reachable_operator_20261002/) | fixed feature reachable operator 20261002 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [future_loss_observability_20260930](../experiments/future_loss_observability_20260930/) | future loss observability 20260930 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [gas0](../experiments/gas0/) | gas0 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [independent_dimension_feasibility_20261001](../experiments/independent_dimension_feasibility_20261001/) | independent dimension feasibility 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [omd_t1](../experiments/omd_t1/) | omd t1 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [prb](../experiments/prb/) | prb | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [radial_taylor_refinement_8d_20261001](../experiments/radial_taylor_refinement_8d_20261001/) | radial taylor refinement 8d 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [rebalanced_7d_section_20261001](../experiments/rebalanced_7d_section_20261001/) | rebalanced 7d section 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [robust_certificate_tightness_20261001](../experiments/robust_certificate_tightness_20261001/) | robust certificate tightness 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [robust_witness_search_20261001](../experiments/robust_witness_search_20261001/) | robust witness search 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [support_aware_robust_dimension_20261001](../experiments/support_aware_robust_dimension_20261001/) | support aware robust dimension 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [target_validation_20260929](../experiments/target_validation_20260929/) | target validation 20260929 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [third_order_antipodal_20261001](../experiments/third_order_antipodal_20261001/) | third order antipodal 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [third_order_antipodal_7d_20261001](../experiments/third_order_antipodal_7d_20261001/) | third order antipodal 7d 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |
| [third_order_antipodal_8d_20261001](../experiments/third_order_antipodal_8d_20261001/) | third order antipodal 8d 20261001 | See contained README / report / result files; finite evidence is not promoted to theorem status. |

### Prototype suite


| Source | PR / commit family | Scope |
| --- | --- | --- |
| [rnn_llm_architecture](https://github.com/soma2-stack/AI-Architecture-Research/tree/192df629e060def0983c4e85f70c4dd01b15b6a0/prototypes/rnn_llm_architecture) | PR #23 | 16 numbered experiments; finite synthetic-task studies and a gated-cell equivalence check. |

### Nine local-only reachable commits


| Commit | Date | Subject | Representative changed path(s) |
| --- | --- | --- | --- |
| `44c9e0e9090e8243f0f0030865e263cc7b21798e` | 2026-10-05 | Repair D2 monotonicity for time-varying corridor dynamics | Codex_Research.md, theory/codex_d2_time_varying_repair_20261005/CHECKS.md |
| `39c371452f2a025974bf0df6b6b920d7ebf91154` | 2026-10-05 | Audit filtered timing packing with complete query bounds | Codex_Research.md, theory/codex_filtered_timing_packing_repair_20261005/CHECKS.md |
| `1992f93915a0a7995595468215af623726b6a1f7` | 2026-10-05 | Analyze history-uniform corridor leverage | theory/codex_history_uniform_leverage_20261005/PROOF.md, theory/codex_history_uniform_leverage_20261005/REPORT.md |
| `644d023c8a929361b5413636a9ac8325d043772d` | 2026-10-05 | Refute all-support complement leverage cap | theory/codex_private_complement_leverage_20261005/PROOF.md, theory/codex_private_complement_leverage_20261005/REPORT.md |
| `9bf66b91cc033ecae589f0b2b630acec01e58118` | 2026-10-05 | Derive compensated shared multicolumn spatial writes | Codex_Research.md, theory/codex_multicolumn_spatial_write_20261005/CHECKS.md |
| `df9ef3379097acc1f1c0e86fa480d94bcf8321d4` | 2026-10-05 | Bound moving-probe gain in shared corridor writes | Codex_Research.md, theory/codex_moving_probe_spatial_write_20261005/CHECKS.md |
| `b484504b30c412d2c19820b0927f0d53008fbe96` | 2026-10-05 | Derive exact multisurvivor filters and scoped write obstructions | Codex_Research.md, theory/codex_multisurvivor_hadamard_write_20261005/CHECKS.md |
| `866df3e25694b3271e7bfc31338d3bb00015511a` | 2026-10-06 | Prove scoped robust two-control repeated near-critical filter writes | Codex_Research.md, theory/codex_repeated_nearcritical_filter_write_20261005/CHECKS.md |
| `eb0374622b332149cd0f67dbb492f203f67c42a0` | 2026-10-06 | Prove scoped robust K=3 and K=4 time-varying filter writes and derive growing-K dilution barrier | theory/gemini_time_varying_nearcritical_filter_bank_20261006/CHECKS.md, theory/gemini_time_varying_nearcritical_filter_bank_20261006/FAILED_ROUTES.md |

### Repository inventories and exclusions

- Concrete remote refs inspected: 82 = 32 mirrored local heads + 18 GitHub branch heads + 32 PR heads. The `origin/HEAD` symbolic ref is excluded from concrete-ref counts.
- Distinct commits reachable from those refs: 494; distinct tracked paths in their tree union: 5583.
- Local-only reachable commit objects: 9; all are listed above. Unreachable-object scan: none found.
- Distinct theory folders: 123; main folders: 106; off-main folders: 17. Experiment collections: 46.
- Branch-name reconciliation: the primary checkout had 32 local branches and GitHub had 18 branches. Fifteen names overlap, 17 are local-only, and three are GitHub-only. The branch tables identify each head SHA.
- PR coverage: all current PRs #1–32; #1–22 merged, #23–32 open, no closed PRs appeared in the queried inventory. PR title/state/head SHA are recorded above.
- Primary-checkout untracked files are outside these ref/tree counts: 17 generated GAS-0 workspaces not exhaustively inspected, two duplicated local PR29 audit trees checked byte-for-byte against tracked counterparts, and one local-only joint audit inspected at summary level.
- The only deleted historical root file found was `PERPLEXITY_WRITE_TEST.md`, a create/edit/delete test artifact, not a research result.
