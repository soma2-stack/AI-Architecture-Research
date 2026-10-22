# Experiment inventory — 2026-10-21

**Complete deduplicated register:** [MASTER_REGISTER.md](MASTER_REGISTER.md) covers all 46 main-tree experiment folders, the numbered PR23 branch experiments, nested EFD/PRB/AMS protocols, the preserved memory-retrieval campaign, and named withdrawn or unrun proposals. It records execution separately from scientific outcome and explains its counting rule.

**Current authorization: experiments are frozen unless the owner explicitly approves
a specific run.** Read the [claim register](../docs/CLAIM_REGISTER.md) before proposing
or running one. The register from [PR38](https://github.com/soma2-stack/AI-Architecture-Research/pull/38)
is merged and authoritative on main. Historical commands, permissions, and “next test”
suggestions in preserved folders are inactive. No new run was made to produce this
inventory.

The [canonical closed/unrun table](../docs/CLAIM_REGISTER.md#closed-and-unrun-experiment-records)
records exact loose-end states, source revisions and missing records. All 46
top-level experiment folders below were inventoried by existing file presence and
report/status inspection, not by re-executing their programs or independently
re-auditing every certificate. ARCHIVED/STOPPED are lifecycle states, not mathematical
proof verdicts. Use **PASSED**, **FAILED**, **INCONCLUSIVE**, **INVALID**, **NOT RUN**,
or **STOPPED** for the recorded run outcome. **ARCHIVED** describes preservation and
does not imply a successful result. Existing reviewed finite certificates retain
their source reviews and do not solve the growing-dimensional target.

PR23's settled Experiments001–016 and PR36's123-run negative surrogate are on their
open PR branches (register C01–C02 and C18–C19). The proposed PR36 3,000-update rerun
and PR37 repeat C5 are WITHDRAWN; C5 decision is NO-GO.

## Start a newly authorized experiment

Use [EXPERIMENT_TEMPLATE.md](EXPERIMENT_TEMPLATE.md) and its folder convention. Give
the run a unique `EXP-YYYYMMDD-NNN` ID, link the claim-register ID and its source SHA,
and name the hypothesis, control, matched budget, seeds, data split, and decision
threshold before running anything. Keep configuration, code, logs, raw per-seed results,
and a concise conclusion in that run's folder. Record PASS, FAIL, INCONCLUSIVE, INVALID,
NOT RUN, or STOPPED for execution outcome; record scientific claim status separately.
The index below covers the 46 existing top-level experiment folders. Follow each link
to its report or primary evidence for the exact measured values and implementation;
this index records no results beyond those existing reports.

| Research question | Existing comparison / outcome | Claim records |
|---|---|---|
| Can a protected recurrent cell learn the tested copy tasks? | [PR23 Experiments001–016](https://github.com/soma2-stack/AI-Architecture-Research/pull/23); six architecture paths include GRU/LSTM baselines. See its branch's source and results plus the [claim register](../docs/CLAIM_REGISTER.md#trainable-memory-and-pr23pr30). | C01–C02 |
| Does balanced-pair memory beat ordinary recurrent baselines? | [PR36](https://github.com/soma2-stack/AI-Architecture-Research/pull/36)'s frozen 123-run surrogate was negative; its proposed 3,000-update rerun is withdrawn. Preserved local retrieval artifacts are indexed on [the preservation revision](https://github.com/soma2-stack/AI-Architecture-Research/tree/41f1c80dc87d38f4e5ee9f962ff4ddba40a4d12a/experiments/memory_retrieval_triage_20261020). | C18–C19 |
| Do finite capture and clean-mask constructions scale? | Existing finite-size reports record positive tests through their stated widths and failed/unfinished larger cases; see the linked summaries below. | C27 and [closed/unrun records](../docs/CLAIM_REGISTER.md#closed-and-unrun-experiment-records) |
| Do Route 7A simulations establish the general target? | No. The corrected replay is awaiting independent review; the conditional long-window result and C5 NO-GO are scoped in the register. Repeat C5 is withdrawn. | [Route 7A and private survivors](../docs/CLAIM_REGISTER.md#route-7a-and-private-survivors) |
| Did automated mechanism searches find a supported new candidate? | AMS v2–v8 are archived; v9 stopped before training. No independently confirmed candidate. | C25 |

These links are navigation aids, not new comparisons or verdicts. For each historical
entry below, its named `REPORT.md`, `SUMMARY.md`, result JSON, or folder is the source
for exact numbers, model identity, code, and logs where available. The inventory was
not expanded by re-running experiments or inferring missing fields.

| Existing folder / evidence entry | Execution / archival disposition |
|---|---|
| [ams_audit](ams_audit/) | ARCHIVED search/audit artifacts and code ([stage 3 v7](ams_audit/audit_stage3_v7.py)); no new search authorization |
| [anisotropic_robust_packing_20260930](anisotropic_robust_packing_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [anisotropic_robust_packing_replay_20261001](anisotropic_robust_packing_replay_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [antipodal_robust_dimension_20261001](antipodal_robust_dimension_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [aperiodic_gate_spectrum_20261001](aperiodic_gate_spectrum_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [approximate_observability_20260930](approximate_observability_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [augmented_accessibility_proof_20260930](augmented_accessibility_proof_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [automated_mechanism_search](automated_mechanism_search/README.md) | ARCHIVED v2–v8 outcomes; no independently confirmed surviving candidate |
| [automated_mechanism_search_v9](automated_mechanism_search_v9/runs/v0_scope/REPORT.md) | STOPPED before training; numeric stages NOT RUN |
| [cfwm](cfwm/) | ARCHIVED computationally-focused working-memory test; entry point [cfwm_experiment.py](cfwm/cfwm_experiment.py), raw output [cfwm_L10_k4.json](cfwm/cfwm_L10_k4.json) and [log](cfwm/cfwm_L10_k4_log.txt); claims not re-audited here |
| [claude_7d_direct_audit_20261001](claude_7d_direct_audit_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [claude_8d_review_20261001](claude_8d_review_20261001/REVIEW.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [claude_radial_8d_review_20261001](claude_radial_8d_review_20261001/REVIEW.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [claude_rebalanced_7d_review_20261001](claude_rebalanced_7d_review_20261001/REVIEW.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [claude_third_order_review_20261001](claude_third_order_review_20261001/REVIEW.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [cleanroom_7d_interval_20261001](cleanroom_7d_interval_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [codex_antipodal_hostile_review_20261001](codex_antipodal_hostile_review_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [csl](csl/) | ARCHIVED continual-symbolic-learning experiments; entry point [csl_experiment.py](csl/csl_experiment.py), example stored results [eval_results.json](csl/eval_results.json) and [log](csl/active_log.txt); scientific claims not re-audited here |
| [efd](efd/) | ARCHIVED E1–E8/Y4 experiment scripts and raw outputs; start at [E1 code](efd/e1_compose.py), [E1 results](efd/e1_results.json), and [log](efd/e1_log.txt); scientific claims not re-audited here |
| [endpoint_certificate_20260930](endpoint_certificate_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [endpoint_width_scaling_20260930](endpoint_width_scaling_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [exact_online_credit_stage_a_20260930](exact_online_credit_stage_a_20260930/REPORT.md) | ARCHIVED completed stage record; not authorization to continue |
| [exact_online_credit_stage_b2_20260930](exact_online_credit_stage_b2_20260930/REPORT.md) | STOPPED / inconclusive; use corrected_single_thread report; no StageC |
| [exact_online_credit_stage_b_20260930](exact_online_credit_stage_b_20260930/REPORT.md) | ARCHIVED completed stage record; not authorization to continue |
| [feature_revision_20260930](feature_revision_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [finite_n_clean_mask_scaling_20261006](finite_n_clean_mask_scaling_20261006/SUMMARY.md) | PARTIAL finite tests; original K batch stopped, clean clear sweep NOT RUN |
| [finite_n_clear_scaling_20261006](finite_n_clear_scaling_20261006/SUMMARY.md) | ARCHIVED finite numerical evidence; no asymptotic claim |
| [finite_n_early_capture_20261006](finite_n_early_capture_20261006/SUMMARY.md) | ARCHIVED finite numerical evidence; no asymptotic claim |
| [finite_n_multistage_capture_20261006](finite_n_multistage_capture_20261006/SUMMARY.md) | ARCHIVED finite numerical evidence; no asymptotic claim |
| [finite_n_r20_r32_scaling_20261006](finite_n_r20_r32_scaling_20261006/SUMMARY.md) | PARTIAL completed TEST1/2; TEST3 R20/24/32 NOT RUN |
| [finite_n_r8_diagnosis_20261006](finite_n_r8_diagnosis_20261006/SUMMARY.md) | ARCHIVED finite numerical evidence; no asymptotic claim |
| [fixed_feature_reachable_operator_20261002](fixed_feature_reachable_operator_20261002/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [future_loss_observability_20260930](future_loss_observability_20260930/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [gas0](gas0/README.md) | ARCHIVED harness/dev/pilot history; official Phase2 NOT AUTHORIZED |
| [independent_dimension_feasibility_20261001](independent_dimension_feasibility_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [omd_t1](omd_t1/pilot_controls/results/pilot_result.json) | STOPPED PhaseA; B/C NOT RUN |
| [prb](prb/) | PARTIAL inventory; see [gradient probe](prb/z4_grad.py), [stored Z4 output](prb/z4_n7.jsonl), and [Z4c script](prb/z4c_latin.py). m20 seeds 1–3 are not in the repository; Z4c is NOT RUN. See register. |
| [radial_taylor_refinement_8d_20261001](radial_taylor_refinement_8d_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [rebalanced_7d_section_20261001](rebalanced_7d_section_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [robust_certificate_tightness_20261001](robust_certificate_tightness_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [robust_witness_search_20261001](robust_witness_search_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [support_aware_robust_dimension_20261001](support_aware_robust_dimension_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [target_validation_20260929](target_validation_20260929/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [third_order_antipodal_20261001](third_order_antipodal_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [third_order_antipodal_7d_20261001](third_order_antipodal_7d_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |
| [third_order_antipodal_8d_20261001](third_order_antipodal_8d_20261001/REPORT.md) | ARCHIVED report/certificate/review; retain exact source scope, no automatic replay |

## Historical October6 finite-size index (preserved)

All “current” wording below is dated history; it is not a work queue or instruction
to complete the unrun cases.

# Experiment index

## Current finite-size evidence — 2026-10-06

All entries below are **NUMERICAL FINITE-SIZE EVIDENCE ONLY**. They do not prove asymptotic theorems, certify architecture novelty, or change theorem status. Results and thresholds are preserved as recorded; no experiment was regenerated.

| Experiment | Contents / current reading |
|---|---|
| [Early capture](finite_n_early_capture_20261006/) | Finite coded-donor capture and signal-retention checks; the tested structured clipped code is not the theorem's full-spark/Gaussian code. |
| [Multistage capture](finite_n_multistage_capture_20261006/) | Multiple capture and trace-correction checks; cross-talk misses the stated threshold in the smallest case and improves with width. |
| [Clear scaling](finite_n_clear_scaling_20261006/) | Clearing, multichannel, age, and control sweeps; the legacy R=8 channel set misses the 0.1% threshold. |
| [R=8 diagnosis](finite_n_r8_diagnosis_20261006/) | Diagnoses alias-prone masks and compares a sum-free R=8 family; the finite comparison is not a general scaling result. |
| [Clean-mask scaling](finite_n_clean_mask_scaling_20261006/) | Clean protected Walsh channels pass the recorded finite tests through R=16; R=20/24/32 were not run in this completed folder. |
| [R20–R32 scaling checkpoint](finite_n_r20_r32_scaling_20261006/) | **CHECKPOINT / PARTIAL BATTERY.** TEST 1 K scaling and TEST 2 mask-family comparison are complete; TEST 3 R=20/24/32 and later width, matched-age, and higher-R tests were not run. K scaling was flat over tested values; sum-free masks passed through R=16, while alias-prone legacy masks failed at R=8/12/16 around 0.25%. No clean-mask capacity limit was observed in this scope. |

See each folder's `SUMMARY.md`, `results.json`, `run_metadata.json`, and `progress.json` where present for measured values and run provenance. Useful plots and the scripts needed to reproduce the recorded protocol are retained.

## Local archival evidence preserved — 2026-10-21

Historical memory-retrieval triage scripts, raw results, reports and twelve checkpoints are preserved at [the local-evidence archival revision](https://github.com/soma2-stack/AI-Architecture-Research/tree/41f1c80dc87d38f4e5ee9f962ff4ddba40a4d12a/experiments/memory_retrieval_triage_20261020). Local prototype history remains on that preservation branch. This is artifact availability; it adds no independent performance verdict or permission to resume experiments. The [cleanup execution record](../docs/audits/REPOSITORY_CLEANUP_AUDIT.md) accounts for ignored files and embedded GAS-0 workspaces retained outside the working repository.
