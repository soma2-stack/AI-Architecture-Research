# Frozen dense-tanh research — consolidated Claude/Codex handoff

**Snapshot:** 2026-10-15  
**Purpose:** One navigable record of the active Claude research from PRs #24–#29 and the independent Codex verdicts, including corrections that have not yet been applied to the source PRs.  
**Scope:** The original frozen dense-tanh learning-credit problem. This is a **navigation and status document, not a replacement proof**. Follow pinned source links before relying on a lemma.  
**Repository state at snapshot:** PRs #24–#29 are open/unmerged. This handoff is kept on its own documentation branch.

> **Read this first.** Codex independently verified a legal one-dimensional counterexample to the **original selected-group Hypothesis B** for the **prescribed fully dense matrix with actual sparse-input accounting**. Therefore that Hypothesis B is **REFUTED**. Theorem R_D **as literally written in PR #29 is INCOMPLETE** because it additionally asserts a zero of an optional, stronger full-group listing that has not been proved. The original problem — $D=\Omega(n)$ at $mT=o(n^{3/2})$ under the full $d_F$ metric — remains **OPEN**.

## 1. Frozen problem and non-negotiable definitions

- Recurrent system: fixed near-critical fully dense tanh family; $n$ is state width; $h_0=0$.
- Target: a jointly admissible, continuous, finite-radius section of robust learning-credit dimension $D=\Omega(n)$ with an **exact common endpoint**, for all required antipodal/query tests.
- Resource: $m$ is the **peak actual past-input support** across every step and section parameter, multiplied by the **entire horizon** $T$. Preparation, driven holding, resets, and tails count. Every tiny nonzero actual input counts. **This is not** additive coordinate-time cost $\sum_t |\operatorname{supp} x_t|$.
- Past input cube: individual amplitudes bounded by $1/2$. Future query contract is separate: legal future preactivations lie in $[0.25,0.75]$, and future raw inputs are held fixed under differentiation.
- Accuracy/error target: $\varepsilon=0.001$. Preserve the original group-RMS gradient normalization and distinguish the selected group $d_{F,E}$, with $E=\operatorname{diag}(0,1,\dots,1)$, from the **full** $d_F$ metric.
- Source of the repository-wide contract: [theory/CURRENT_THEORY.md](../../theory/CURRENT_THEORY.md) and [AGENTS.md](../../AGENTS.md). The former is a 2026-10-06 navigation snapshot and predates PR #29; its historical status lines should not override later scoped independent audits.
- Repository convention: author-written “PROVED” is not automatically independently **VERIFIED**; label the exact theorem and quantifier scope.

## 2. Executive status: what can be used now?

| Claim | Status as of this handoff | Evidence / restriction |
|---|---|---|
| Original $D=\Omega(n)$, $mT=o(n^{3/2})$ in full $d_F$ | **OPEN** | No construction or universal obstruction |
| PR #24 QSR theorem | **VERIFIED only in modified QSR scope** | Does not transfer automatically to dense tanh |
| PR #26 Householder / neutral-path-tax candidate | **PARTIAL; general tax OPEN** | Exact identities and finite signals, not peak-width barrier resolution |
| PR #27 fixed-$K$, public-schedule obstruction | **VERIFIED in its scoped probe model** | Does not imply full-metric obstruction |
| PR #28 Theorems 2–3 | **VERIFIED in their stated scopes** | Corollaries retain stated hypotheses |
| PR #28 Theorem 4 | **CONDITIONAL implication** | Its antecedent Hypothesis B is now refuted in the original class |
| PR #29 Lemma E and Theorem R for $R_0$ | **INDEPENDENTLY VERIFIED** | Six error inequalities and exact-rational/interval certificate |
| PR #29 Lemmas D1–D3; **original selected-group B counterexample** for prescribed dense $R$ | **INDEPENDENTLY VERIFIED** | Exact matrix choice, balanced cancellation, actual support and original listing zero |
| **Original Hypothesis B**, under prescribed dense $R$ | **REFUTED** | A legitimate $D=1$ listing zero violates its universal bus bound |
| Literal Theorem R_D including the **optional Proposition 0.2 extended-listing zero** | **INCOMPLETE** | Actual full-group credit scalar $B_T(0,0)$ not shown equal |
| Lemma M / robust bus dimension bound | **OPEN** | A large bus norm does not yield $D=\Omega(n)$ |
| Removing the logarithmic loss | **OPEN** | Old-profile continuous-listing lemma missing |

**Important logic:** Theorem 4 remains a valid conditional/dichotomy statement; its case “B fails” is realized. Do **not** quote its conditional lower bound as an unconditional barrier, or mark the original conjecture solved.

## 3. Recent PRs and where the work lives

### PR #24 — Shift-holonomy / modified-QSR construction

- [PR #24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24), head [d899895](https://github.com/soma2-stack/AI-Architecture-Research/tree/d899895aab81b36a3128a375ae2238b08f73f4af/theory/claude_shift_holonomy_audit_20261013).
- [Proof](https://github.com/soma2-stack/AI-Architecture-Research/blob/d899895aab81b36a3128a375ae2238b08f73f4af/theory/claude_shift_holonomy_audit_20261013/PROOF.md) · [Status](https://github.com/soma2-stack/AI-Architecture-Research/blob/d899895aab81b36a3128a375ae2238b08f73f4af/theory/claude_shift_holonomy_audit_20261013/STATUS.md).
- Independent review: [PR #25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25), head 50bb5ff.
- Lemmas 5.1–5.3 / Theorem 5.4 survive in **modified QSR**, with its stated queries and metrics. Corrected finite-size Corollary 5.5 has $D=\lfloor n'/1001\rfloor\ge n/1004$, not the false $n/1002$ bound. Corollary 5.6 is only for **augmented QSR**.
- Tanh-equivalence, idealized-adjoint legality and credit-weighted neutral-path tax remain unproved. **Never present QSR as a result for the original frozen model.**

### PR #26 — Householder broadcast and neutral-path tax

- [PR #26](https://github.com/soma2-stack/AI-Architecture-Research/pull/26), head [e13311b](https://github.com/soma2-stack/AI-Architecture-Research/tree/e13311b1d4d6d7ea227f7c9caa1931636cb55502/theory/claude_neutral_path_tax_20261013).
- [Proof](https://github.com/soma2-stack/AI-Architecture-Research/blob/e13311b1d4d6d7ea227f7c9caa1931636cb55502/theory/claude_neutral_path_tax_20261013/PROOF.md) · [Status](https://github.com/soma2-stack/AI-Architecture-Research/blob/e13311b1d4d6d7ea227f7c9caa1931636cb55502/theory/claude_neutral_path_tax_20261013/STATUS.md).
- Exact Householder gather/broadcast identities and a neutral-hole charging identity were developed. The “one neutral path per visible direction” heuristic fails.
- Candidate hub-only signal approximately $0.00245$–$0.00255$ at tested $n=8k$–$128k$; continuous-code examples approximately $0.0024$; reduced model is not a universal proof.
- **Accounting trap:** The candidate’s additive coordinate-time may be $O(n)$, but peak width is about $n/2$ over a horizon of order $n$, so **peak $mT$ is of order $n^2$**. The original strict-budget theorem and generalized neutral-path tax remain OPEN.

### PR #27 — Narrow/fixed-$K$ public-schedule obstruction

- [PR #27](https://github.com/soma2-stack/AI-Architecture-Research/pull/27), head [c987408](https://github.com/soma2-stack/AI-Architecture-Research/tree/c9874081461139373a276efeb47394d50781c0e3/theory/claude_narrow_capture_hub_20261013).
- [Proof](https://github.com/soma2-stack/AI-Architecture-Research/blob/c9874081461139373a276efeb47394d50781c0e3/theory/claude_narrow_capture_hub_20261013/PROOF.md) · [Codex final addendum](https://github.com/soma2-stack/AI-Architecture-Research/blob/c9874081461139373a276efeb47394d50781c0e3/theory/codex_pr27_repair_verification_20261015/FINAL_CROSS_PR_ADDENDUM.md).
- Scoped fixed-$K$ public-probe theorem:
  $$
  mT\ge\frac{2.9\times10^{-10}\,D\sqrt n}{(K+2)(1+\ln K)}.
  $$
- Independent repairs retained the own/bus split, finite nonzero front transport, correct homogeneous post-gate order $a(UGU)P$, and injection $c_t UG_t E v$. Theorem survives in its stated public-schedule/parameter-subspace hypotheses.
- Do **not** extrapolate to arbitrary code-dependent schedules, all query groups, or the original full metric.

### PR #28 — Multiprobe estimates and conditional Theorem 4

- [PR #28](https://github.com/soma2-stack/AI-Architecture-Research/pull/28), head [0cc0a23](https://github.com/soma2-stack/AI-Architecture-Research/tree/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/claude_multiprobe_memory_20261014).
- [Proof, §7.5 including exact Hypothesis B](https://github.com/soma2-stack/AI-Architecture-Research/blob/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/claude_multiprobe_memory_20261014/PROOF.md) · [Independent audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/codex_cross_pr_final_audit_20261015/AUDIT.md).
- Theorem 4’s **conditional** selected-group bound, in its resource/dimension range $2N_3\le D\le n$:
  $$
  mT\ge4.7\times10^{-11}\,D\sqrt n\min(1,890/\ln n).
  $$
- For $D=\Theta(n)$ this yields at best $\Omega(n^{3/2}/\ln n)$ asymptotically **if B were true**. Even with B, it would not rule out strict little-$o(n^{3/2})$.
- **Original Hypothesis B:** At a zero of Theorem 4’s complete original odd listing $\Phi$, the entire **reference-skeleton selected-group bus** must satisfy $\|\sum_l\nu_l\mathrm{bus}_l\|_2\le\tau/4$ for every legal future query. The listing is items (i)–(v), not the later optional added full-credit scalar. $D=1$ is not excluded from B’s universal quantification; the theorem’s separate dimension **corollary** has stronger hypotheses.
- PR #28 predates the counterexample and still describes B as OPEN. That is **historical**, not the newest independently reviewed result.

### PR #29 — Drift capture and the prescribed dense matrix (main current result)

- [PR #29](https://github.com/soma2-stack/AI-Architecture-Research/pull/29), last audited author head [2e46b02](https://github.com/soma2-stack/AI-Architecture-Research/tree/2e46b02d61b8b2cc713546461d1232b578690b8f/theory/claude_hypothesis_b_bus_20261015).
- [PROOF.md §§2.1–2.4](https://github.com/soma2-stack/AI-Architecture-Research/blob/2e46b02d61b8b2cc713546461d1232b578690b8f/theory/claude_hypothesis_b_bus_20261015/PROOF.md) · [Author response](https://github.com/soma2-stack/AI-Architecture-Research/blob/2e46b02d61b8b2cc713546461d1232b578690b8f/theory/claude_hypothesis_b_bus_20261015/REVIEW_RESPONSE.md) · [Verification scripts](https://github.com/soma2-stack/AI-Architecture-Research/tree/2e46b02d61b8b2cc713546461d1232b578690b8f/theory/claude_hypothesis_b_bus_20261015).
- **Mechanism:** Modulated paired arrivals alter near-neutral own credit; a held zero-gate gather spike captures their differences through a Householder bus. A legal uniform future query amplifies the gathered coordinate by $\sqrt k$. Many coherent captures produce an $O(n)$ bus signal while the final own profiles coincide.
- **Quantifiers:** For $n\ge1.5\times10^{18}$ divisible by four, a continuous legal $D=1$ section, $m\le120001$, complete $mT\le2.5\times10^{-5}n^{3/2}$, exact common endpoint and zero of original listing (i)–(v).
- **Lemma E (independently verified):** Six nonnegative coupled majorants for bus differences, front/broadcast and spike, including the full minus-history source terms. The fixed point $X\le b+MX$ has a certified rational super-solution; $E_Y<1018.375<1019$. Coherent accumulation across all arrivals and leakage is included.
- **Dense transfer, Lemma D1:** Original deterministic power-vector recipe really selects both all-ones vectors, hence
  $$
  R=\alpha\left(R_0+\eta\,\frac{\mathbf1\mathbf1^\mathsf T}{n}\right),\qquad 0<\eta\le10^{-8}/n^2.
  $$
  Both $R$ and $R^{-1}$ are dense, and the original operator norm is preserved.
- **Lemma D2:** $Rh=\alpha R_0h+(\alpha\eta/n)(\mathbf1^\mathsf Th)\mathbf1$. Opposite paired state modulations have $\mathbf1^\mathsf T\Delta h=0$, so their dense difference is exactly $\alpha R_0\Delta h$. The autonomous **absolute** trajectory changes, but the shared field does not create differing undriven coordinates.
- **Lemma D3:** Actual inputs are defined only on the driven set, with literal zeros elsewhere. This is **not** a dense inverse lift. Every input is below $0.4732+10^{-40}<0.5$; $m\le120001$; endpoint and the original listing zero are exact, not floating-point coincidences. State/source bounds have an explicit $t=1$ exception.
- **Verified final lower bounds:** Using the audited normalized constants,
  $$
  \|\Gamma_{\rm bus}\|/n>0.11790944697053530,\qquad
  \|\Gamma_{\rm actual}\|/n>0.11790936597053530.
  $$
  In particular $\|\Gamma_{\rm bus}\|>2.08262900298\,\tau>\tau/4$. The bus bound is exactly the reference object in original B; the actual-gradient comparison is separate.
- **Verdict:** The **core selected-group Hypothesis B counterexample for the prescribed dense $R$ is independently VERIFIED**. The **literal Theorem R_D remains INCOMPLETE** solely because it also claims an *optional stronger listing zero*, discussed next.

## 4. Essential corrections from the two latest Codex audits

The user-provided Codex audits dated 2026-10-15 are separate local audit records. Their conclusions are incorporated here. Do not imply those audit files are already committed into PR #29.

1. **Unsupported full-group extension — REMOVE or prove separately.** Proposition 0.2 adds the odd part of the actual full-group credit scalar $B_T(0,0)$. Equal states do **not** make it equal. For the actual dense credit column $b_t$:
   $$
   \Delta b_t(0)=g_0(t)\left[(\alpha a+\alpha\eta/n)\Delta b_{t-1}(0)+(\alpha\eta/n)\sum_{j\ge1}\Delta b_{t-1}(j)\right].
   $$
   The last feedback term was omitted. Codex exhibited an exact short-history counterexample to the inference and a high-precision scaled schedule with nonzero added scalar. Neither disproves the original selected-group B counterexample. **Remove the claim “and of its Prop. 0.2 extension” from Theorem R_D unless independently proved.**
2. **False rounded ratio — FIX.** The claim $0.11790n\ge2.0826\tau$ is false. Use the full audited $>0.11790944697053530n$ bound to obtain the ratio $>2.08262900298$, or weaken the ratio quoted after rounding.
3. **Actual support is not reference support.** Dense-reference inverse lifting generally makes the reference input dense. In the proved construction **actual** inputs are exactly sparse by direct definition, while reference inputs need not be sparse. Remove prose claiming both notions coincide.
4. **First-time and edge cases.** For Lemma D1 at $n=8,9$, use $1<\gamma\le2<k$, not $1<\gamma<2<k$. For transferred bath/source estimates, note $t=1$: $c_1=0$, and the strong front/beta bounds start later.
5. **Earlier historical numerical limits.** The author's drift comparison schedule contained two extra arrivals versus the written theorem; independent reproduction used the written schedule and still passed. Small-$n$ simulations are diagnostic, not theorem-scale proof. A generic right-factor perturbation breaks the dense exact endpoint; the prescribed all-ones structure is essential.
6. **Other exactness warnings.** Bath receiver rows can receive uniform capture/leak even when their own $\delta_i=0$. Finite front gates attenuate rather than perfectly destroy transport. These are already accounted for by Lemma E; do not reintroduce the false simplifications.

**Do not erase the counterexamples or these qualifications when editing author status files.**

## 5. Next mathematical target: Lemma M, not another magnitude cap

The counterexample defeats the statement that **every** legal listing zero has tiny total bus magnitude. It does **not** show the bus has many independent, robustly query-visible dimensions.

**Lemma M remains a proposed replacement, not a theorem.** A useful research program is:

1. Write the exact gathered contribution as a function of past own profiles, especially the spike aggregate $\sum_t\rho_t\kappa_t O_{t-1}(d-1,:)$, along with full bus feedback and leak.
2. Develop an **odd continuous, low-support listing** that controls the number of independent visible bus directions — not just one large coherent norm.
3. Charge long neutral paths to **actual peak-width × full-horizon** budget, including public or code-dependent support, preparation, tails and resets.
4. Prove a dimension bound uniform over every legal future query (and the original full metric before claiming a solution); or find a legal counterexample.
5. Separately address the old-profile window that produces the $\log n$ loss. A proposed continuous weighted listing of old own profiles is still unproved.

Do not reuse PR #28’s already-refuted universal Hypothesis B, do not assume rank-two feedback each step implies rank-two accumulated information, and do not infer large dimension from a $D=1$ signal.

## 6. Resume protocol and authoritative source order

**Immediate housekeeping (scoped edit to PR #29 only, subject to owner approval/workflow):**
- Patch Theorem R_D’s optional extended-listing claim or clearly mark it OPEN.
- Fix the rounded inequality, time-1 exceptions, actual-vs-reference support prose and historical minor errors.
- Keep the **independently verified original B refutation** visible in STATUS/REPORT/PROOF.
- Record both local Codex audits in the project provenance or add them as independent evidence, without overwriting original proofs.

**Then start a new bounded Lemma M proof/counterexample task**, retaining the exact contract. Have another independent model audit any new theorem, with the project’s required multi-model reviews before any external human outreach.

**Read these in order when resuming:**

1. [This handoff](FROZEN_DENSE_TANH_RESEARCH_HANDOFF.md) — verdict and source map.
2. [Original contract and baseline](../../theory/CURRENT_THEORY.md) — read with date caveat.
3. [Original Hypothesis B and Theorem 4](https://github.com/soma2-stack/AI-Architecture-Research/blob/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/claude_multiprobe_memory_20261014/PROOF.md) — exact quantifiers.
4. [Latest PR #29 proof](https://github.com/soma2-stack/AI-Architecture-Research/blob/2e46b02d61b8b2cc713546461d1232b578690b8f/theory/claude_hypothesis_b_bus_20261015/PROOF.md) — Lemma E, D1–D3, Theorem R_D and the **unfixed optional overclaim**.
5. Independent **R0 Codex audit** (user-supplied file AUDIT(1).md, 2026-10-15) — verified Lemma E and first set of corrections.
6. Independent **dense-transfer Codex audit** (user-supplied file AUDIT(2).md, 2026-10-15) — original B refutation proved; optional extended listing unproved.
7. [PR #27 foundation corrections](https://github.com/soma2-stack/AI-Architecture-Research/blob/c9874081461139373a276efeb47394d50781c0e3/theory/codex_pr27_repair_verification_20261015/FINAL_CROSS_PR_ADDENDUM.md) and [PR #28 final cross-audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88/theory/codex_cross_pr_final_audit_20261015/AUDIT.md).
8. [PR #26 neutral-path study](https://github.com/soma2-stack/AI-Architecture-Research/blob/e13311b1d4d6d7ea227f7c9caa1931636cb55502/theory/claude_neutral_path_tax_20261013/PROOF.md) and [PR #24 QSR study](https://github.com/soma2-stack/AI-Architecture-Research/blob/d899895aab81b36a3128a375ae2238b08f73f4af/theory/claude_shift_holonomy_audit_20261013/PROOF.md) for alternate, separately scoped mechanisms.

**Explicit non-goals of this handoff:** no source PR merge; no training or GPU experiments; no modification to AGENTS.md or restricted notebooks; no declaration that the full-metric $n^{3/2}$ question or Lemma M is resolved; no external human outreach.