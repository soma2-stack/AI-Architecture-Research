# AI-Architecture-Research — Scientific Evidence Audit

**Audit date:** 2026-10-21 (America/Detroit)  
**Repository:** https://github.com/soma2-stack/AI-Architecture-Research  
**Source restriction:** GitHub only. No private local worktrees, uncommitted results, external papers, unpublished audits, or claims from other agents were used as primary evidence.  
**Captured GitHub state:** `main` at `f8a96fb8b8df`; 23 live branches; 37 PRs, of which #1–22 are merged and #23–37 are open. The newer open PRs are **not on `main`**.  
**Audit type:** cross-branch *evidence and consistency review*. GitHub code, reports, saved JSON, workflow status, audit documents, and historical corrections were examined. **Not** an independent execution/rederivation of every mathematical proof or program. A green workflow verifies the job's assertions, not the scientific conclusion.

## Executive finding — what is and is not proved

**The central target remains OPEN:** construct a robust learning-credit family with dimension `D = Ω(n)` at peak-width-times-horizon cost `mT = o(n^(3/2))`, or establish a correctly scoped obstruction. `n` is the recurrent width; `D` is the number of uniformly distinguishable learning-credit directions; `m` is maximum simultaneously driven coordinates; `T` is the complete time horizon. `mT` is **not** the sum of driven coordinates over time. The formal metric uses gradients/sensitivities under legal future queries, **not** ordinary prediction accuracy or an independently learned memory bit count.

Meaningful established research exists, but in **different scopes**:

1. The Oct 6 `main` consolidation records a near-linear strict-budget construction, `D ≥ n/[10^70 log log n]`, in its admissible regime and a linear result `D=Ω(n)` **at** the `Θ(n^(3/2))` boundary. These do not imply linear dimension strictly *below* that boundary. [Main theory](https://github.com/soma2-stack/AI-Architecture-Research/blob/f8a96fb8b8df/theory/CURRENT_THEORY.md).
2. PR #24/#25's modified quadratic-shift recurrence has independently checked lemmas and a linear-dimensional statement **within its changed QSR/augmented metric and public changing-support scope**. It does not solve the original fixed dense tanh contract. The review repaired the finite-size claim from `n/1002` to `n/1004`. [PR24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24) · [PR25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25).
3. PR #27 establishes a **fixed-probe/selected-subspace** resource inequality, including `mT ≥ 2.9×10^-10 D√n/[(K+2)(1+ln K)]` with the stated qualifications. PR #28's stronger theorem is **conditional on Hypothesis B**, with `mT ≥ 4.7×10^-11 D√n min(1,890/ln n)` in a selected group. Neither is a universal full-metric lower bound. [PR27](https://github.com/soma2-stack/AI-Architecture-Research/pull/27) · [PR28](https://github.com/soma2-stack/AI-Architecture-Research/pull/28).
4. PR #29 **refutes the original Hypothesis B** using drift capture even for the prescribed dense matrix/actual support, following an independent repair audit. **Do not conflate** this with the optional *extended full-group* listing, which the audit found incomplete. Refuting B blocks that particular conditional proof route; it does **not** refute the main memory barrier or prove linear capacity. [Final dense audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/f05694454956/theory/codex_pr29_dense_transfer_audit_20261015/AUDIT.md).
5. PRs #33–35 introduce a **sublinear**, exact-real memory family at `m≤3` and `mT≈1.5n`. PR #33's original universal second-order certificate was **refuted** by a huge-`n` counterexample; PR #34 repairs it with a dimension-dependent gate estimate and an all-size envelope. PR #35 states an extension to the prescribed rank-one-perturbed dense matrix and a `D=floor(floor(n^(1/3))/2400)` construction for `n≥10^16`. This is a meaningful **cube-root** capacity lower bound, not `D=Ω(n)`. The PR #35 `STATUS.md` reports an independent Codex acceptance of the main theorems, but **that full independent review is not included in the PR #35 changed-file inventory**; the source proof, scripts, and certificate JSON are available on GitHub. Thus distinguish **reported independent review** from **audit independently inspectable in GitHub**. [PR33 audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/f515e48ed84f/theory/codex_pr33_independent_audit_20261019/AUDIT.md) · [PR34](https://github.com/soma2-stack/AI-Architecture-Research/pull/34) · [PR35](https://github.com/soma2-stack/AI-Architecture-Research/pull/35) · [PR35 status](https://github.com/soma2-stack/AI-Architecture-Research/blob/aa47ca5/theory/claude_dense_transfer_20261020/STATUS.md).
6. PR #37's Codex audits verify several **restricted component identities and cost/listing statements**, while finding multiple false extensions. Step 3.7 at `1a8203e` introduces a variation-ceiling theorem and an exact kernel split, but **the additions have not yet received an independent GitHub-committed audit**. The legal staircase experiment failed to realize the abstract operator amplification. Full centered/second-order channels, generic dense matrices, and the original problem remain open. [PR37](https://github.com/soma2-stack/AI-Architecture-Research/pull/37) · [current status](https://github.com/soma2-stack/AI-Architecture-Research/blob/1a8203e/theory/claude_remaining_channels_20261020/STATUS.md).
7. The trainable protected-memory prototype **does exhibit learnable synthetic retention and causally localized memory in particular checkpoints**, but PR #23 Experiment 016 gives an exact generalized-gated-cell reduction with no distinctive capability demonstrated. PR #36's separate trainable PR35-inspired surrogate fails to outperform GRU/LSTM controls at the frozen 600-update budget. Neither is a demonstration of a novel practical architecture or an operational implementation of the credit-memory theorem. [Experiment 016](https://github.com/soma2-stack/AI-Architecture-Research/blob/192df629/prototypes/rnn_llm_architecture/EXPERIMENT_016_RESULTS.md) · [PR36 results](https://github.com/soma2-stack/AI-Architecture-Research/blob/472ea492/docs/pr35_memory/RESULTS.md).

## Evidence standard and important distinctions

| Label in this report | Meaning |
|---|---|
| **Independently reviewed in scope** | An inspectable GitHub review checks a specifically identified commit, equations, inputs, or scripts. It **does not** promote the result outside that scope. |
| **Proof claimed / certificate recorded** | Author proof and/or machine-readable constant certificate is committed, but complete independent audit was not inspectable here. |
| **Finite numerical observation** | A test shows an outcome at selected settings, not a uniform theorem. |
| **Experimental failure** | A frozen metric or gate failed; the result may concern training, implementation, protocol, or hypothesis, not model impossibility. |
| **Refuted statement** | A counterexample falsifies the stated universal assertion; a narrower replacement may remain true. |
| **Unverified** | There is insufficient committed proof or rerun evidence; do not call this false or proven. |

The main [theory index](https://github.com/soma2-stack/AI-Architecture-Research/blob/f8a96fb8b8df/theory/INDEX.md) contains **108 table rows representing 106 unique folder names**; two entries are duplicated (`codex_complete_query_normalization_recovery_20261007` and `codex_stationary_parameter_complement_recovery_20261007`). Its status labels include 45 `VERIFIED`, 13 `VERIFIED IN STATED SCOPE`, 24 `PENDING REVIEW`, 8 `ACCEPTED`, 6 `SUPERSEDED`, 3 `REFUTED`, and other statuses. These are **folder-level statuses**, not 58 proofs of the central target. The index and `CURRENT_THEORY.md` were frozen around October 6 and do **not** summarize the still-open PR #23–37 findings.

## Formal result-by-result audit: current open PRs

| PR | GitHub evidence and actual verdict | What it cannot establish |
|---|---|---|
| [#23](https://github.com/soma2-stack/AI-Architecture-Research/pull/23) | Runnable baseline models and Experiments 001–016; 127 initial CPU tests; training, causal interventions, exact equivalence checks. | No formal credit-memory theorem; no novel trainable architecture by Exp016. |
| [#24](https://github.com/soma2-stack/AI-Architecture-Research/pull/24) | QSR lemmas + selected normalized corollary; [#25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25) includes independent rational and numerical checks. | Not the frozen dense tanh fixed-port/full-contract theorem. |
| [#25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25) | Hostile correction of #24: finite-size bound, query legality, support convention, and tanh ablation limits. | Does not verify QSR-to-original equivalence. |
| [#26](https://github.com/soma2-stack/AI-Architecture-Research/pull/26) | Householder hub-broadcast algebra, neutral-hole identity, finite `.00245–.00253` hole-component signals. [Independent Gemini review](https://github.com/soma2-stack/AI-Architecture-Research/blob/2f3a3d248e02/theory/gemini_pr26_neutral_hole_audit_20261013/REVIEW.md) supports scoped lemmas. | Peak `m≈n/2`, `T≈n/4` implies `mT≈n²/8`; cheap **additive** coordinate-time does not satisfy required **product** budget. Full asymptotic signal bound open. |
| [#27](https://github.com/soma2-stack/AI-Architecture-Research/pull/27) | Fixed-K public-schedule obstruction reviewed after correcting missing gate, own vs bus credit, and front leakage. | Not universal full-gradient barrier. |
| [#28](https://github.com/soma2-stack/AI-Architecture-Research/pull/28) | Corrected conditional Theorem 4 and multi-probe ingredients. | Hypothesis B subsequently refuted; cannot use conditional claim as unconditional result. |
| [#29](https://github.com/soma2-stack/AI-Architecture-Research/pull/29) | Hypothesis B counterexample: independent R0 audit, then [dense-transfer re-audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/f05694454956/theory/codex_pr29_dense_transfer_audit_20261015/AUDIT.md) closes prescribed-matrix and support gaps. | Optional full-group Proposition 0.2 assertion not proved; only one direction, not linear dimension. |
| [#30](https://github.com/soma2-stack/AI-Architecture-Research/pull/30) | Consolidated handoff document. | Documentation only; no new independent result. |
| [#31](https://github.com/soma2-stack/AI-Architecture-Research/pull/31) | First-order gather listing, two-channel decomposition, and explicit still-open `M_rest`. | Not a global listing of all second-order, centered, F-step channels. |
| [#32](https://github.com/soma2-stack/AI-Architecture-Research/pull/32) | Two-stream bus identity, contraction/no-amplification scope, centered retention investigations. | Full `M_rest` operator listing open. |
| [#33](https://github.com/soma2-stack/AI-Architecture-Research/pull/33) | First-order and local identities survived; [hostile Codex audit](https://github.com/soma2-stack/AI-Architecture-Research/blob/f515e48/theory/codex_pr33_independent_audit_20261019/AUDIT.md) **refuted** its advertised all-`n` second-order certificate. | At #33 commit, Theorem 6.1/Cor 6.2 were OPEN. |
| [#34](https://github.com/soma2-stack/AI-Architecture-Research/pull/34) | Revised gate estimate, exact envelope `eps_SO≤0.374696015` for `n≥31622^4≈10^18`; fixed combined listing count. [Stored JSON](https://github.com/soma2-stack/AI-Architecture-Research/blob/f515e48/theory/claude_lemma_m_three_memory_20261019/envelope_certificate_result.json). | Author's GitHub text says re-audit pending; do not inherit #33's hostile-audit PASS to revised claims automatically. |
| [#35](https://github.com/soma2-stack/AI-Architecture-Research/pull/35) | Prescribed dense rank-one perturbation, exact-balanced-pair endpoint mechanism, full-metric **lower-bound** transfer, cube-root clipped-code construction, certificate `eps_SO≈0.380634<0.381` with strict margin `0.0610>0.0567`. [Stored certificate](https://github.com/soma2-stack/AI-Architecture-Research/blob/aa47ca5/theory/claude_dense_transfer_20261020/skeleton_certificate_result.json). Status reports an independent positive audit not fully committed in this PR. | Not generic dense-matrix theorem, not linear `D`, not numerically practicable training. |
| [#36](https://github.com/soma2-stack/AI-Architecture-Research/pull/36) | **123 completed runs**, 73,800 total optimizer steps, three matched seeds. No advantage condition passed; report-recomputation [workflow success](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39439975390). | Surrogate changes frozen dynamics, carries, encoding, and endpoint; negative result does **not refute** PR35. |
| [#37](https://github.com/soma2-stack/AI-Architecture-Research/pull/37) | Three independent Codex audit folders for Steps 3/3.5/3.6; identities, first-order listing and corrected bounds pass scoped checks, other overclaims fail. Step 3.7 states new variation theorem and kernel split, supported by author checks. | Step 3.7 unaudited on GitHub; no legal amplified staircase or full barrier theorem. |

### Specific falsifications that change the research strategy

**PR #26 — budget mismatch.** The construction uses approximately `22n` **summed** input-coordinate operations, but its simultaneously active width times entire horizon is order `n²`. This is a genuinely different complexity measure. A successful experiment under the first measure is **not** a near-miss under the second.

**PR #29 — a conditional assumption is false.** The intended bus-capacity argument cannot proceed by assuming Hypothesis B. Drift captures can generate a large bus readout despite listed own signals being zero. The independent dense review establishes this under the original intended selected-group B; it explicitly leaves the new extra full-gradient component unsettled.

**PR #33 — testing merely large model sizes was insufficient.** At `n=10^166`, the original displayed second-order coefficient was `2.199…`, versus its advertised maximum `0.5`; by `10^168` its bootstrap precondition also failed. A fixed positive gate-error factor multiplied by `√n` cannot give a uniform asymptotic bound. PR34 replaced this with a gate estimate that shrinks with n; **that is the substantive repair**, not a denser numeric grid. [Independent refutation](https://github.com/soma2-stack/AI-Architecture-Research/blob/f515e48/theory/codex_pr33_independent_audit_20261019/AUDIT.md).

**PR #35 — exact-real theorem is not practical recall.** Its guarantee is about distinguishable **credit/gradient states after the same visible hidden endpoint**. A deterministic forward decoder observing just that common endpoint cannot recover the differing pasts. The clipped Vandermonde encoding can require gain greater than `5.53×10^50` already at `D=89`, according to the recorded independent check cited by PR36. That threatens finite-precision practicality but does not falsify an exact-real proof.

**PR #37 — repeated scope expansion.** Codex found an invalid comparison between a newly expanded source `S′` and an older source `S`, a nonzero-initial-component omission, a stationary-to-transient inference failure, and an omitted kernel term in a proposed listing. The current branch withdraws them, but the new Step 3.7 claims require new independent review. [Audit A](https://github.com/soma2-stack/AI-Architecture-Research/blob/1a8203e/theory/codex_pr37_independent_audit_20261020/AUDIT.md) · [Audit B](https://github.com/soma2-stack/AI-Architecture-Research/blob/1a8203e/theory/codex_pr37_step35_audit_20261020/AUDIT.md) · [Audit C](https://github.com/soma2-stack/AI-Architecture-Research/blob/1a8203e/theory/codex_pr37_step36_audit_20261020/AUDIT.md).

## Empirical evidence: what truly worked

### Mainline numerical theory tests

The six indexed October 6 groups are finite diagnostics only: early capture, multistage capture, clear scaling, R=8 alias diagnosis, clean-mask scaling, and the unfinished R20–R32 checkpoint. The sum-free mask tests passed in their tested settings through `R=16`; alias-prone masks failed at `R=8/12/16`. R20/24/32 **were not run**, so no high-R capacity or asymptotic scaling conclusion is permitted. [Experiment index](https://github.com/soma2-stack/AI-Architecture-Research/blob/f8a96fb8b8df/experiments/INDEX.md) · [checkpoint](https://github.com/soma2-stack/AI-Architecture-Research/blob/f8a96fb8b8df/experiments/finite_n_r20_r32_scaling_20261006/SUMMARY.md).

### PR #23 trainable RNN experiments

The 16 named result documents are all present on the [prototype branch](https://github.com/soma2-stack/AI-Architecture-Research/tree/192df629/prototypes/rnn_llm_architecture). The strongest **positive** findings are constrained: early protected single-bit copy at 64 tokens reached 100% in a few seeds and schedules; Experiment 009 found five-seed success after training beyond the earlier plateau; Experiments 014–015 identified a memory-carrying 8-dimensional subspace in **two successful checkpoint instances**. But the same architecture can store memory in another subspace, GRUs can also solve comparable tasks, and the exact generalized gated recurrence of Experiment 016 reproduces the cell and gradients. This is not a discovered distinct primitive.

### PR #36 practical bridge

The actual [trained surrogate implementation](https://github.com/soma2-stack/AI-Architecture-Research/blob/472ea492/prototypes/pr35_memory/model.py) describes itself as an engineering surrogate; it uses `fast`, `p`, and `-p`, an ordinary convex gate, a fixed row-normalized Vandermonde map, and no oracle write masks. The [summary JSON](https://github.com/soma2-stack/AI-Architecture-Research/blob/472ea492/docs/pr35_memory/summary.json) records 123 complete runs, 968.4 CPU-training seconds, matched streams/evaluation sets, and **zero** conditions beating all controls under the frozen rule. Example: two facts, width 64, 48 guaranteed no-write steps: pair model whole-record accuracy **29.95%**, GRU width 64 **75.13%**, parameter-matched GRU-34 **53.65%**, LSTM width 64 **51.30%**. These are direct comparisons on the *same new task*; do not compare them numerically to older PR23 tasks.

### Mainline automated mechanism search and OMD

* AMS v2 stopped at Stage 0; v3 and v4 at Stage 1. v5 passed Stage 1 but its repaired 6,000-proposal search had **0 Tier-1 evaluations** and **0 promotions**, due to generator/sanity-filter yield. v6 constructor failed static validation before search. v7 completed 1,200 Tier-1 evaluations and promoted eight C* candidates, but **all eight failed Stage 3**. v8 also completed 1,200 Tier-1 evaluations and 42 archive cells, then **0/42 candidates passed independent-seed confirmation**, so Stage 3 did not run. [AMS reports](https://github.com/soma2-stack/AI-Architecture-Research/tree/f8a96fb/experiments/automated_mechanism_search).
* OMD-PILOT-1 failed its Phase-A teacher imitation gate: **3/36 pairs passed**, whereas the rule required success for *all* controls/held-out pairs. No extraction or downstream phases were executed. The [raw pilot JSON](https://github.com/soma2-stack/AI-Architecture-Research/blob/f8a96fb/experiments/omd_t1/pilot_controls/results/pilot_result.json) identifies missing within-class recency tie-breaking rather than out-of-range time extrapolation. This is a stopped pilot, not a failed architecture theorem.
* GAS-0 PR19–20 is design/harness work. A passing harness suite is **not** a demonstrated research architecture; the PR20 description records 24/24 checks and dev baselines, but Phase 2 was not authorized. [PR20](https://github.com/soma2-stack/AI-Architecture-Research/pull/20).

## Branch coverage ledger: all 23 currently live refs

`main` stores merged PR1–22 and Oct6 theory/experiment indexes. Each row below is a *GitHub inventory and relevant-evidence audit*, **not a statement that every file in that branch was re-executed**.

| Branch / immutable head prefix | Disposition |
|---|---|
| `main` `f8a96fb8b8df` | Merged historical AMS/OMD/GAS; 106 unique indexed theory folders; six indexed early finite experiment groups. |
| `prototype/rnn-llm-architecture-v0-20261007` `192df629e060` | PR23 and Experiments 001–016. |
| `claude/shift-holonomy-audit-20261013` `d899895aab81` | PR24 scope-corrected QSR. |
| `codex/pr24-independent-hostile-review` `50bb5ffabf33` | PR25 independent audit. |
| `claude/neutral-path-tax-20261013` `e13311b1d4d6` | PR26 out-of-contract product-cost candidate. |
| `claude/narrow-capture-hub-20261013` `c98740814611` | PR27 fixed-probe obstruction. |
| `claude/multiprobe-memory-20261014` `0cc0a2317520` | PR28 conditional theorem. |
| `claude/hypothesis-b-bus-20261015` `f05694454956` | PR29 B counterexample and two-stage independent review. |
| `docs/claude-research-handoff-20261015` `afb6f3c5d09f` | PR30 no new experiment. |
| `claude/lemma-m-bus-capacity-20261015` `35cdb7a4f3c7` | PR31. |
| `claude/lemma-m-rest-20261016` `cef12b3eb6e5` | PR32. |
| `claude/lemma-m-three-memory-20261019` `d6801c2bb1b3` | PR33 original invalid certificate. |
| `claude/lemma-m-sequential-repair-20261020` `f515e48ed84f` | PR34 repaired certificate. |
| `claude/dense-transfer-20261020` `aa47ca5ec782` | PR35 special dense transfer/cube-root claim. |
| `codex/pr35-trainable-balanced-memory-20261020` `472ea49242d5` | PR36 123-run practical failure. |
| `claude/remaining-channels-20261020` `1a8203e2ced0` | PR37 latest channel repairs; Step 3.7 independent audit pending. |
| `astra/private-survivor-independent-20261008` `6297b112bcd7` | Independent/private survivor research folder; partial/pending index record, not a merged target proof. |
| `codex/route7a-long-window-20261008` `075c5ffdb0c0` | Long-window Route 7A study; index status pending review. |
| `gemini/astra-route7a-feedback-audit-20261008` `1fa6b00018f7` | Scope-limited independent feedback review. |
| `gemini/pr26-neutral-hole-audit-20261013` `2f3a3d248e02` | Independent scoped PR26 review; stored in `REVIEW.md`. |
| `claude/gallant-bardeen-ybxn57` `d8ed873a28ed` | Earlier research-layout snapshot, unassociated with a current open PR; no independent new theorem established by branch existence. |
| `preserve/all-research-20261004` `d1767d0a62db` | Preservation snapshot and manifest, not separate experimental validation. |
| `preserve/local-theory-20261004` `74232f2d1d38` | Preservation snapshot and manifest, not separate experimental validation. |

All branch heads are retrievable from the [GitHub branches API](https://api.github.com/repos/soma2-stack/AI-Architecture-Research/branches?per_page=100); all open/merged PR relationships from the [PR API](https://api.github.com/repos/soma2-stack/AI-Architecture-Research/pulls?state=all&per_page=100). **Do not count branch copies or stacked PR files as independent replications.**

## Bottom line and research decision

**Retain as substantive progress:** near-linear frontier in its stated scope; verified QSR results (modified model); reviewed fixed-probe limits; the actual counterexample to original Hypothesis B; repaired sublinear bus-memory constructions, with source/provenance qualification; exact mechanism and counterexamples that constrain future proofs; the observation that optimization plateaus rather than absolute capacity explain many toy failures.

**Retire or quarantine:** any assertion that the neutral-path hub example meets the original product budget; the original PR33 all-n certificate; the optional unproved full-group extension in PR29; PR37's superseded stationary/initial-content and kernel-free claims; a novel/superior protected-cell claim after Exp016; any interpretation of AMS v7 or v8 as independently confirmed successful candidates.

**Most defensible next mathematical problem:** formulate and independently test a *correctly costed, full-contract* bound for the remaining **cross-history kernel/gate-difference** and centered bus channels (PR37), or produce a **legal peak-width-times-horizon** counterexample. Do **not** run another training sweep to claim progress toward this theorem: current trainable tasks measure different objects.

## Evidence gaps / limits of this audit

This report examined GitHub PR metadata and bodies, branch heads and directory inventories, the main theory and experiment indexes, full representative experiment results 001–016, mainline AMS/OMD stored JSON and runner code, PR29/33/37 independent audit files, PR34/35 certificates and status, PR36 source and 123-run summary, and selected Actions conclusions. **It did not execute all scripts, recompute every JSON/CSV row, mathematically rederive every one of 106 archived folders, diff every historic file or download every historical Actions artifact.** Claims marked independently reviewed refer to **the auditor evidence contained in GitHub**, not a new universal certification by this report. If those stronger activities are required, they remain outstanding independent-reproduction work; they must not be represented as already completed.