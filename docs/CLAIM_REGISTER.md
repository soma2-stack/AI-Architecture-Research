# Canonical claim register

**Updated:** 2026-10-21
**Repository:** [soma2-stack/AI-Architecture-Research](https://github.com/soma2-stack/AI-Architecture-Research)
**Purpose:** A concise, evidence-linked record of major research claims and their current scope. This is a curated register, not a re-audit of every historical theory folder.

> **Central target — OPEN.** Robust growing-dimensional learning-credit separation under the required resource budget remains open: establish a family with D = Ω(n) at peak-width-times-horizon cost mT = o(n^(3/2)), or prove a correctly scoped obstruction. Exact-real credit/gradient distinguishability, selected-subspace bounds, finite synthetic recall, and ordinary prediction accuracy are not interchangeable evidence for this target.

Status counts in this version: **8 VERIFIED (within scope), 15 REFUTED, 6 PARTIAL, 2 OPEN, 2 NOT RUN** (33 records). “VERIFIED” means the stated limited claim has evidence; it does not extend beyond the listed assumptions or commit.

## Evidence basis and revision map

The two repository-wide October 21 reports are source inventories and consistency audits, not fresh proof derivations or blanket reruns:

- [Scientific evidence audit](audits/SCIENTIFIC_EVIDENCE_AUDIT_2026-10-21.md), repository state commit 841928e60092b50e323b57a92bc6b17a85b96280; it records that its GitHub snapshot was main at f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c, before the open PRs.
- [Experiment failure and repetition audit](audits/EXPERIMENT_FAILURE_AND_REPETITION_AUDIT_2026-10-21.md), same repository commit and snapshot. It checks stored reports and raw results, documents known protocol failures, and identifies runs that were never performed.

The PR head SHAs below identify the evidence revision referred to in this register; a PR’s current head can differ from an earlier reviewed commit.

| PR | Evidence head SHA |
|---|---|
| #23 | 192df629e060def0983c4e85f70c4dd01b15b6a0 |
| #24 | d899895aab81b36a3128a375ae2238b08f73f4af |
| #25 | 50bb5ffabf33b28099238acb6440cb1a349079e3 |
| #26 | e13311b1d4d6d7ea227f7c9caa1931636cb55502 |
| #27 | c9874081461139373a276efeb47394d50781c0e3 |
| #28 | 0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88 |
| #29 | f05694454956edab849ebe7d1858131eaca4174c |
| #30 | afb6f3c5d09f0ffbaba23aca1dfa2db4fb73b347 |
| #31 | 35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab |
| #32 | cef12b3eb6e5a8e6dbc75904253222b57eda188c |
| #33 | d6801c2bb1b311b3d132312535b87c86064d2eb9 |
| #34 | f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb |
| #35 | aa47ca5ec782d4a70047793d00a44f2f47816f49 |
| #36 | 472ea49242d5d06e4da646938fe3ff2a70b56c66 |
| #37 | 87af5508b224fdf21d5c40aba26e68ef85f27fa1 |

Additional pinned revisions relevant to audit scope:

- PR34’s independent Codex audit at 39af3a97dab0c20628c837e2b72da8c7e70a4e3d is preserved locally at E:\AI-Architecture-Research\theory\codex_pr34_fresh_audit_20261020\AUDIT.md (SHA-256 26a2bbbeb6638d7b40a22c04cd4e419b33dd69b95d9fa2cd249e12f60ca7a186). It is not present in the PR34 GitHub files.
- PR35’s independent Codex audit targets b984ef9347219d62db4dfd39f8f2e263317c9a33, at E:\AI-Architecture-Research\theory\codex_pr35_independent_audit_20261020\AUDIT.md (SHA-256 7ea8df109fe3ab18004977c488e8b8bd62d8d465fa6f59d733f5ccf0f3f6ccf2). It is not present in the PR35 GitHub files. It checks PR35’s principal dense-transfer and cube-root claims and inspects inherited final PR34 source, but is not a separate exact-commit PR34 verdict.
- PR37 Step 3.7’s independent audit is committed in the PR37 branch at theory/codex_pr37_step37_audit_20261021/AUDIT.md. It targets source commit 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad; the PR branch later contains documentation corrections at 87af5508b224fdf21d5c40aba26e68ef85f27fa1. The audit file is preserved verbatim in that branch.

## Claims

### Trainable memory and PR23–PR30

#### C01 — The PR23 protected-memory prototype can learn its tested synthetic copy tasks

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #23, prototypes/rnn_llm_architecture/EXPERIMENT_009_RESULTS.md, source head 192df629e060def0983c4e85f70c4dd01b15b6a0; cross-checked in the October 21 Experiment Failure and Repetition Audit.
- **Limit:** Experiment 009 reports 5/5 seeds reaching 100% under its trained task and conditions. This is a finite benchmark result, not robust long-delay recall or evidence for a new architecture.
- **Further work:** Only if a new task targets a specific unresolved mechanism and uses locked, matched controls.

#### C02 — The existing protected cell demonstrates a distinct new primitive or architecture

- **Status:** REFUTED
- **Evidence:** PR #23, EXPERIMENT_016_RESULTS.md and its equivalence checks, source head 192df629e060def0983c4e85f70c4dd01b15b6a0; October 21 Scientific Evidence Audit.
- **Limit:** The tested cell and gradients reduce to a generalized gated recurrence to about 8e-14 maximum float64 logit difference over 324 cases. This does not prove literal equivalence to a vanilla GRU; it removes the demonstrated novelty claim for this cell.
- **Further work:** Do not repeat the same cell experiment. A materially different state transition would need a new reduction and falsification test.

#### C03 — PR24/25’s QSR result establishes the original fixed dense-tanh contract

- **Status:** REFUTED
- **Evidence:** PRs #24–25, corrected QSR statements and independent rational/numerical checks, source heads in the revision map; October 21 Scientific Evidence Audit.
- **Limit:** The result is for a modified quadratic-shift recurrence, augmented metric, and public changing-support scope. It does not transfer to the original frozen dense-tanh contract.
- **Further work:** No transfer claim is justified without a separate valid reduction.

#### C04 — The revised QSR claims hold in their stated scope

- **Status:** VERIFIED (within scope)
- **Evidence:** PRs #24–25, QSR lemmas/corollary and PR25’s independent checks, source heads in the revision map; October 21 Scientific Evidence Audit.
- **Limit:** The review corrected the finite-size factor from n/1002 to n/1004 and clarified query legality/support conventions. It does not verify equivalence with the original model.
- **Further work:** No new experiment is needed for the checked QSR statement; keep the scope qualifier attached.

#### C05 — PR26’s neutral-hole construction meets the required peak-width-times-horizon budget

- **Status:** REFUTED
- **Evidence:** PR #26, construction and cost accounting at e13311b1d4d6d7ea227f7c9caa1931636cb55502; independent review theory/gemini_pr26_neutral_hole_audit_20261013/REVIEW.md at 2f3a3d248e02306408195312f3ca258ac8b357e8; October 21 Scientific Evidence Audit.
- **Limit:** Tested finite hole signal is about 0.00245–0.00253, but peak m≈n/2 and horizon T≈n/4 give mT≈n²/8. A small summed support cost is not the required product budget.
- **Further work:** Retire this route for the original budget unless its resource law changes.

#### C06 — PR27 proves a fixed-K selected-subspace resource inequality

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #27, corrected fixed-probe/public-schedule statement at c9874081461139373a276efeb47394d50781c0e3; October 21 Scientific Evidence Audit.
- **Limit:** Under its listed qualifications the bound is mT ≥ 2.9×10^-10 D√n / ((K+2)(1+ln K)). It is a selected-subspace/fixed-K result, not a full-gradient universal barrier.
- **Further work:** Useful as a scoped lemma; a full-metric transfer remains separate work.

#### C07 — PR28’s stronger multi-probe result is unconditional

- **Status:** PARTIAL
- **Evidence:** PR #28, corrected conditional Theorem 4 and multi-probe ingredients at 0cc0a2317520cc342fdfdedfd9bb2c4be9a4ae88; the PR29 counterexample and audit below.
- **Limit:** The bound depends on Hypothesis B. PR29 refutes that hypothesis in the intended selected-group setting, so this conditional route does not establish an unconditional barrier.
- **Further work:** Do not use it as unconditional evidence; only a proof with a replacement premise would justify continuation.

#### C08 — PR29’s original Hypothesis B holds

- **Status:** REFUTED
- **Evidence:** PR #29, counterexample and final dense-transfer audit theory/codex_pr29_dense_transfer_audit_20261015/AUDIT.md at source f05694454956edab849ebe7d1858131eaca4174c; October 21 Scientific Evidence Audit.
- **Limit:** The audit closes the prescribed-matrix and support gaps for the intended selected-group B. It does not prove the main barrier or refute all memory capacity.
- **Further work:** Retire Hypothesis B and proofs that require it.

#### C09 — PR29’s optional extended full-group Proposition 0.2 is established

- **Status:** OPEN
- **Evidence:** PR #29 and its audit at f05694454956edab849ebe7d1858131eaca4174c; October 21 Scientific Evidence Audit.
- **Limit:** The audit explicitly leaves this stronger full-group listing unresolved. Refuting B only blocks that conditional proof route.
- **Further work:** Only if it becomes necessary to a precise surviving central claim.

#### C10 — PR30 adds an independent mathematical result

- **Status:** REFUTED
- **Evidence:** PR #30 handoff/documentation commit afb6f3c5d09f0ffbaba23aca1dfa2db4fb73b347; October 21 Scientific Evidence Audit.
- **Limit:** It consolidates context and adds no independent theorem or experiment.
- **Further work:** None; cite it as documentation only.

### PR31–PR36 mathematical and empirical claims

#### C11 — PR31’s first-order gather listing is valid in its stated scope

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #31, first-order gather/two-channel listing at 35cdb7a4f3c7f3ae1df7ed1941547428a9b774ab; October 21 Scientific Evidence Audit and linked PR37 audit history.
- **Limit:** The listing explicitly leaves M_rest open; it is not a complete second-order, centered, or F-step listing.
- **Further work:** Do not promote it to a full metric result.

#### C12 — PR32 closes the remaining full operator listing

- **Status:** PARTIAL
- **Evidence:** PR #32, two-stream bus identity and contraction claims at cef12b3eb6e5a8e6dbc75904253222b57eda188c; October 21 Scientific Evidence Audit.
- **Limit:** The scoped bus identity/contraction result is useful, but full M_rest remains open.
- **Further work:** Yes, only for the unresolved full operator term needed by the central target.

#### C13 — PR33’s universal second-order certificate is valid for all n

- **Status:** REFUTED
- **Evidence:** PR #33, theory/codex_pr33_independent_audit_20261019/AUDIT.md, audit source f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb; October 21 Scientific Evidence Audit.
- **Limit:** The displayed coefficient is about 2.199 at n=10^166, exceeding the claimed 0.5; the bootstrap premise also fails by n=10^168. This refutes that certificate, not all later repairs.
- **Further work:** No; preserve as a retired negative result.

#### C14 — PR34’s repaired R0 theorem and envelope are supported at the previously audited revision

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #34, theory/claude_lemma_m_three_memory_20261019/envelope_certificate_result.json and independent audit theory/codex_pr34_fresh_audit_20261020/AUDIT.md at audited commit 39af3a97dab0c20628c837e2b72da8c7e70a4e3d; audit file SHA-256 is recorded above.
- **Limit:** The checked result is R0-scoped, with D≥n^(1/4)/161, m=3, mT=1.5n, n≥10^18, and envelope ε_SO≤0.374696015. It is not a linear-dimension result.
- **Further work:** Preserve the scope. C15 records the narrow exact-commit PASS for Lemma 5.0R and Proposition 5.4; it does not extend this audit verdict to every PR34 result.

#### C15 — Lemma 5.0R and Proposition 5.4 pass at PR34 commit f515e48

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #34 final source f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb; independent audit at 39af3a97dab0c20628c837e2b72da8c7e70a4e3; Task 3’s direct comparison of the three files changed between those commits.
- **Limit:** The Task 3 comparison establishes a narrow exact-commit PASS for Lemma 5.0R and Proposition 5.4, including the reviewed tightened .3747 assertion and positive front-gate bound. It is not a standalone independent audit of every PR34 result. The original audit file remains local-only; this register does not claim a permanent audit artifact exists.
- **Further work:** No further review is needed for these two claims. Other PR34 claims remain limited to their separately cited audit scope.

#### C16 — PR35’s main dense-transfer and cube-root construction pass independent review at the audited revision

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #35 independent Codex audit targets b984ef9347219d62db4dfd39f8f2e263317c9a33 (local-only path and SHA-256 above); PR35 theory/claude_dense_transfer_20261020/STATUS.md.
- **Limit:** The audit establishes, for that pinned revision, an exact-real prescribed dense rank-one-perturbed construction with D=floor(floor(n^(1/3))/2400), m≤3, mT≤1.5n, for n≥10^16; it is cube-root, not Ω(n). Current PR head aa47ca5ec782d4a70047793d00a44f2f47816f49 is one commit later; GitHub compare shows that commit modifies CHECKS.md, PROOF.md, REPORT.md, RESUME.md, STATUS.md, and exp_skeleton.py. The audit verdict does not automatically cover those edits. The full audit is not committed in PR35.
- **Further work:** Keep the audit artifact available and obtain a focused source-delta review before applying its verdict to the current PR head.

#### C16a — PR34’s 0.374696015 envelope and PR35’s 0.380634258447 certificate are not directly comparable

- **Status:** PARTIAL
- **Evidence:** PR #34 theory/claude_lemma_m_three_memory_20261019/envelope_certificate_result.json at f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb; PR #35 theory/claude_dense_transfer_20261020/skeleton_certificate_result.json at aa47ca5ec782d4a70047793d00a44f2f47816f49; independent PR34/PR35 audit scopes and commits are listed above.
- **Limit:** The records certify 0.374696015 and 0.380634258447 in different certificate contexts. The available audits/reports do not establish a common normalization and identical quantifiers that would make the values directly comparable; their difference alone is not evidence of contradiction.
- **Further work:** No new proof review is required for this register entry. A direct numerical comparison is justified only if a later claim depends on the certificates being interchangeable.

#### C17 — PR35’s exact-real result already demonstrates a numerically practical trainable memory

- **Status:** REFUTED
- **Evidence:** PR #35 theorem at audited commit b984ef9347219d62db4dfd39f8f2e263317c9a33; local independent PR35 audit; PR #36, docs/pr35_memory/RESULTS.md and summary.json at 472ea49242d5d06e4da646938fe3ff2a70b56c66.
- **Limit:** The theorem distinguishes credit/gradient states after a common visible endpoint; this is not an ordinary decoder’s past-token recall guarantee. The independent audit records required gain above 5.53×10^50 already at D=89, a serious finite-precision obstacle, not a refutation of exact-real mathematics.
- **Further work:** A practical bridge remains an empirical question; do not represent the theorem as a trained architecture.

#### C18 — The PR36 balanced-pair surrogate beats GRU/LSTM at its frozen budget

- **Status:** REFUTED
- **Evidence:** PR #36, docs/pr35_memory/summary.json, RESULTS.md, prototypes/pr35_memory/model.py, source head 472ea49242d5d06e4da646938fe3ff2a70b56c66; recomputation workflow run 39439975390; October 21 Scientific Evidence Audit.
- **Limit:** 123 completed runs (600 updates each; three matched seeds) yielded zero conditions meeting the registered all-control advantage rule. At width 64/two facts/48 no-write steps: pair model 29.95% whole-record recall, GRU-64 75.13%, parameter-matched GRU-34 53.65%, LSTM-64 51.30%. The comparison is fair within this surrogate task, not against PR23’s different tasks.
- **Further work:** No repeat of the unchanged surrogate. A new test needs a mechanism hypothesis and a reason to expect the frozen failure mode to change.

#### C19 — PR36’s negative result falsifies PR35’s mathematical theorem

- **Status:** REFUTED
- **Evidence:** PR #36 task and surrogate documentation/results at 472ea49242d5d06e4da646938fe3ff2a70b56c66; PR #35 exact-real theorem/audit at b984ef9347219d62db4dfd39f8f2e263317c9a33; October 21 Scientific Evidence Audit.
- **Limit:** PR36 changes the dynamics, carry, encoding, and endpoint and tests trained prediction. It is a negative result for that engineering surrogate, not the theorem’s credit-gradient claim.
- **Further work:** No theorem retest follows from this experiment alone.

### PR37 audited results

#### C20 — Theorem 11.3 passes with the audited bath and parameter restrictions

- **Status:** VERIFIED (within scope)
- **Evidence:** PR #37, theory/codex_pr37_step37_audit_20261021/AUDIT.md, exact audited source 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad; documentation-corrected branch head 87af5508b224fdf21d5c40aba26e68ef85f27fa1.
- **Limit:** The audit requires ε_P≤1, 0≤r≤1, 0≤r̂<1, retains initial/capture terms, and restricts the bath. Do not use it to support the broader negative-bath claim.
- **Further work:** No further work on the corrected theorem statement; broader bath cases require separate proof.

#### C21 — Corollary 11.5’s signed-monotone factor-two variation bound holds generally

- **Status:** REFUTED
- **Evidence:** PR #37 Step 3.7 audit at 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad; corrected documentation at 87af5508b224fdf21d5c40aba26e68ef85f27fa1.
- **Limit:** The audit gives φ=(-1,+1) with variation 3, exceeding the claimed bound 2. The factor-two statement needs fixed-sign monotonicity; the constant-forcing conclusion also requires a constant bath.
- **Further work:** General signed-monotone bound is closed; any broader replacement needs new proof.

#### C22 — Proposition 11.6’s operator amplification is established as legal physical-history amplification

- **Status:** PARTIAL
- **Evidence:** PR #37 Step 3.7 audit, exact source 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad; corrections at 87af5508b224fdf21d5c40aba26e68ef85f27fa1.
- **Limit:** Operator-level amplification is distinct from attainability by legal histories. Near-attainment requires a joint hierarchy and correct size/settling-time limits; the reported 0.9 mass exceeds physical capacity.
- **Further work:** Only if a legal-history construction is needed for a surviving resource claim.

#### C23 — Proposition 11.7’s common-query identity and cost-dependent kernel extension are both closed

- **Status:** PARTIAL
- **Evidence:** PR #37 Step 3.7 audit at 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad; corrected status in branch head 87af5508b224fdf21d5c40aba26e68ef85f27fa1.
- **Limit:** The common-terminal-query identity passes in scope; differing queries require an additional terminal term. The useful cost-dependent kernel bound remains OPEN.
- **Further work:** Further work is justified only for the cost-dependent bound if it bears on the central target.

#### C24 — The audited legal staircase gains establish robust growing-dimensional separation

- **Status:** PARTIAL
- **Evidence:** PR #37 Step 3.7 audit at 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad, preserved in the branch at 87af5508b224fdf21d5c40aba26e68ef85f27fa1.
- **Limit:** Matched-forcing legal gains are finite: population-L1 2.315760×/3.044170× and legal retainer-readout 2.011900×/2.533122× for K=2/K=3. A selected full-column response of 69.4441 at n=10^12 normalizes to only 2.4532×10^-12. This does not establish robust dimension scaling or the required cost separation.
- **Further work:** No staircase optimization is justified absent a new hypothesis; retain as a bounded negative/diagnostic result.

### Retired searches and incomplete runs

#### C25 — AMS v7/v8 produced independently confirmed novel candidates

- **Status:** REFUTED
- **Evidence:** October 21 Scientific Evidence Audit, source snapshot f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c; experiments/automated_mechanism_search/runs/stage3_v7/results.json, stage2_v8_confirm/confirmation.json, and ams/confirm.py.
- **Limit:** v7’s eight promotions all failed Stage 3; v8 had 0/42 candidates pass independent-seed confirmation. This closes those tested grammars and gates, not every possible mechanism.
- **Further work:** Do not rerun unchanged search; specify a new candidate family and a measurable reason it can pass the frozen funnel.

#### C26 — OMD-PILOT-1 passed its Phase-A gate and downstream extraction was tested

- **Status:** REFUTED
- **Evidence:** experiments/omd_t1/pilot_controls/results/pilot_result.json at snapshot f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c; October 21 Experiment Failure and Repetition Audit.
- **Limit:** Only 3/36 held-out teacher-imitation pairs reached 99.5%, failing the all-controls rule. Phases B/C were not run; diagnosis points to within-class recency tie-breaking, not time extrapolation.
- **Further work:** No downstream claim is supported; reopening requires a repaired, prespecified Phase-A gate.

#### C27 — The finite masked-capture battery establishes high-R scaling

- **Status:** NOT RUN
- **Evidence:** experiments/finite_n_r20_r32_scaling_20261006/SUMMARY.md and experiments/INDEX.md at f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c; October 21 Scientific Evidence Audit.
- **Limit:** Clean sum-free masks passed only in tested cases through R=16; alias-prone masks failed at R=8/12/16. The R20/R24/R32 battery was not run.
- **Further work:** Only if a specific scaling claim survives cheaper analysis and the result could change the central decision.

#### C28 — GAS-0 demonstrates a new learned architecture

- **Status:** NOT RUN
- **Evidence:** PR #20, harness and PR description at head 8e64c850aea05586dbbcd178f2b396f0de4ebe19; main snapshot f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c and October 21 Scientific Evidence Audit.
- **Limit:** 24/24 harness checks and development baselines are not a Phase 2 experiment. Phase 2 was not authorized or run.
- **Further work:** No architecture claim is justified from the harness.

#### C29 — Historical theory-index labels certify the original target

- **Status:** REFUTED
- **Evidence:** theory/INDEX.md and theory/CURRENT_THEORY.md at f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c; October 21 Scientific Evidence Audit.
- **Limit:** The index contains 108 rows/106 unique folders with mixed statuses and predates open PR23–37. Folder-level “VERIFIED” or “ACCEPTED” labels do not certify the central target.
- **Further work:** Use this register and exact source audits for current claims; do not infer target status from index counts.

#### C30 — PR37’s Step 3.7 audit is absent from GitHub

- **Status:** REFUTED
- **Evidence:** PR #37 branch head 87af5508b224fdf21d5c40aba26e68ef85f27fa1, file theory/codex_pr37_step37_audit_20261021/AUDIT.md; audit source 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad.
- **Limit:** The PR37 audit is preserved verbatim on its branch after Task 4 documentation corrections. This does not make PR34/PR35 local audits publicly available.
- **Further work:** None for preservation; cite the exact audit source revision.

#### C31 — PR34 and PR35 independent audit records are fully inspectable in their PRs

- **Status:** REFUTED
- **Evidence:** PR #34 and #35 changed-file inventories at heads f515e48ed84f31f525d6b583cc4d9fb9ff8bbeeb and aa47ca5ec782d4a70047793d00a44f2f47816f49; local audit paths and SHA-256 digests listed above; October 21 Scientific Evidence Audit.
- **Limit:** The independent audit files remain local-only. PR35 status reports positive review, and its external-to-PR audit can be identified and hashed, but GitHub readers cannot inspect that full audit from those PRs.
- **Further work:** Yes for reproducibility/provenance: preserve the existing audit artifacts in an approved public record; do not recreate them.

#### C32 — The required robust growing-dimensional learning-credit separation is established

- **Status:** OPEN
- **Evidence:** October 21 Scientific Evidence Audit at 841928e60092b50e323b57a92bc6b17a85b96280, especially its central-target definition and PR23–37 scope table; PRs #23–37 at the SHAs above.
- **Limit:** No cited result establishes robust D=Ω(n) at mT=o(n^(3/2)) under the original contract. PR35 is a scoped exact-real cube-root result; PR36 fails its matched practical surrogate comparison; PR37 component results and staircase gains do not close the missing full-metric/cost argument.
- **Further work:** Yes. This remains the project’s primary open research question, but new work should begin with a precise surviving claim and the cheapest falsification route.

## Evidence gaps and use

This register prioritizes the major PR23–37 claims and the October 21 audits. It does not re-derive all proofs, rerun historical scripts, rehash checkpoint binaries, or certify every one of the 106 unique theory folders. Those omissions are intentional and are not positive evidence. The independent PR34/PR35 audit files are identified by exact path and hash but remain local-only. Task 3’s direct diff review resolves the exact-commit gap narrowly for Lemma 5.0R and Proposition 5.4 at f515e48; it does not create a permanent audit artifact or a standalone verdict for all PR34 results. The October 21 mainline reports are evidence inventories, not substitute audits.

Do not cite an author status line as independent verification. For each claim, retain the pinned source SHA and the exact audit scope. If a later commit changes a relevant proof, code path, assumption, or result, the verdict does not automatically transfer.
