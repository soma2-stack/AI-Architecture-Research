# Experiment History and Duplicate-Discovery Guide

Snapshot: 2026-10-17. This archive records existing evidence; it is not a new experiment or a blanket re-audit of every theorem. It separates experiments from proofs, code validation, replays, and proposals. See [AGENTS.md](../AGENTS.md) for governance and [RESEARCH_ATLAS.md](RESEARCH_ATLAS.md) for theorem statuses, branch history, and the theory source index.

## How to use this archive

Before investigating an idea, follow the NEW DISCOVERY CHECK at the top of [RESEARCH_ATLAS.md](RESEARCH_ATLAS.md), search this file’s lookup table, and inspect the linked protocol/results. This file catalogs experiment evidence; the atlas indexes all 123 theory folders.

A **collection** is one top-level experiment folder in the union of accessible refs. A **study** is a separately named protocol/follow-up. A **run** may be a seed, parameter configuration, precision replay, or episode. They are not interchangeable. Some folders have thousands of result rows; others contain one certificate. I report exact collection and native named-study counts rather than pretending every JSON row is an independent discovery. Folder-level labels summarize the main result only; read the detailed entry for mixed outcomes.

- **SUCCESS** means the finite frozen criterion passed. It does not establish a universal theorem or novelty.
- **FAILURE** means the frozen target criterion was missed. It is not an impossibility theorem without a proof.
- **INCONCLUSIVE** means the measured object does not decide the target.
- **PARTIAL** means stages/metrics have mixed outcomes or stopped early.
- **INVALID** means a defect undermines the affected result.
- **NOT RUN** means proposed, gated, interrupted, or expressly unexecuted.

### Counted outcomes at collection level

The primary empirical unit is one top-level collection with executed empirical or numerical work; it is not an individual seed/configuration. Of the 46 collection roots, **34 are primary empirical collections**: 9 have a scoped SUCCESS result, 4 miss their frozen target (FAILURE), 7 are INCONCLUSIVE, 14 are PARTIAL, and 0 are wholly INVALID. **Eight additional roots are replay/review/audit collections** with executed checks. The other four are one proof folder with symbolic checks, one proof-only folder, the AMS-v9 scope stop (no empirical run), and the AMS audit-tool folder. These counts describe folders, not seeds or trials. Within those collections, 16 numbered PR23 studies and 15 EFD studies are separately named; the 34-folder total is not the count of nested runs. The repository has no common run manifest from which to recover a truthful grand total of every seed, configuration, episode, precision replay, and failed attempt without imposing a new arbitrary unit.

The archive identifies **11 explicitly unstarted follow-ons/stages** at native stage granularity: OMD blinded extraction, OMD judge, OMD Phase B, OMD Phase C; the GAS-0 official 105-episode model matrix; AMS v4 Stage 2, v6 Stage 2, v8 Stage 3, and v9 empirical stages; the finite R20/R24/R32 and later-width/age battery; and the clean-mask clearing/capacity follow-up. One further clean-mask K sweep is **incomplete**, having timed out before completion. Other open proof ideas are not counted as proposed experiments. Some executed collections contain invalid attempts (for example a certificate-runner crash or AMS defect candidates); no complete primary empirical collection is classified INVALID because those attempts were isolated and not used as valid measurements.

## 1. Original problem and distinctions

The original target is the frozen prescribed fully dense tanh recurrent architecture, zero initialization, original full fixed-feature gradient metric d_F, legal future queries, and peak actual input width times complete history horizon mT. The desired result is a robust continuous D=Ω(n) section with exact common endpoint and uniform boundary-antipodal separation above 0.002, while mT=o(n^(3/2)). It remains **OPEN**.

- m is the maximum count of nonzero **actual** input coordinates at any time and section parameter; arbitrarily small nonzero values count. This is not total support summed over time, a reference-support convention, or energy.
- mT includes preparation, routing, holding, reset, and tail. Additive coordinate-time is a different budget.
- First-order gathered credit, selected parameter groups, full fixed-feature groups, and original full d_F are different metrics. Transfer needs a proved inequality.
- A large scalar bus readout does not imply large robust memory dimension. PR29 refutes its selected-group scalar Hypothesis B at D=1, not the Ω(n) problem.
- Public schedules, changing public support, input-dependent schedules, private gates, and fixed-support routers are different assumptions.
- Finite interval certificates prove lower bounds for frozen sections under their stated scope. Searches, sampled grids, SVDs, and failed certificates are not global upper bounds.
- QSR and diagonal/reference R0 are modified recurrences, not the original prescribed dense-tanh system.
- A passing harness validates controls/replay, not a new architecture.

## 2. Quick lookup

| Keyword / alternate name | Prior investigation and result | Where | What would be new |
|---|---|---|---|
| Delayed recall, protected subspace, retention gate | PR23 Exp001–016: one-bit retention works; multi-slot training is sensitive; transition is a general gated recurrence | §3; PR23; atlas F-01/N-01/N-02 | A guarantee or resource law not preserved by matched general gated recurrence |
| Two-slot/multi-slot memory | PR23 Exp002–004, 009–013: longer randomized training solves two-slot finite task; four-slot success unreliable | §3 | Robust scaling with matched data/compute/memory budget |
| Query-aware retrieval | PR23 Exp006–007: probe/native readout gap at short delay; more native training closes much of it | §3 | Matched-capacity query decoder that improves robust retrieval |
| Long computation, recurrence, iterative inference | EFD E1/E7: GRU/LSTM extrapolate Z5; recurrent grid CNN improves with iteration; BFS exact | §4 | A property not preserved by ordinary recurrence/algorithms |
| Program composition and library learning | EFD E4/E8: search strong; learned library reduces search on small DSL | §4 | Matched evidence/compute gain beyond known search/compression |
| Latent binding, symbol remapping, functional symbols | EFD E2/Y4–Y4c; PRB Z2–Z4: neural runs weak/variable, CSP/search sometimes exact | §4 | Learned structure beating matched constraint/search on held-out cases |
| Regime separation, concept splitting | EFD E3/E6: expert libraries, probes, clustering, fine-tuning recover some structure | §4 | Robust gain with labels, capacity, and external clustering matched |
| Online credit, eligibility, RTRL | Exact online credit A/B/B2; AMS v9: exact credit matches BPTT; low-rank results inconclusive; v9 stopped before training | §8 | Matched sparse-terminal-feedback advantage over exact RTRL |
| Robust dimension/antipodal sections | Oct 1 studies: rigorous finite sections through 8D and distinct 7D; no maximum | §5; atlas | High-D theorem in original metric and budget |
| Protected Walsh, front saturation, gather | Six finite-N suites and PR27–32: clean masks pass through R16; R≥20 untested; first-order Lemma M scoped; M_rest unaudited | §7; PR31/32 | Uniform full-query/full-metric capacity bound with actual support/full horizon |
| Bus feedback/Hypothesis B | PR29 refutes exact selected-group Hypothesis B at D=1 | Atlas/PR29 | Robust dimension, not another amplitude result |
| Neutral-path tax | PR24 Lemma 8.1 and PR26: one-step unweighted trace deficit scoped; cumulative credit-weighted tax CONJECTURAL | Atlas/PR26 | Prove cumulative inequality under original assumptions |
| AMS/GAS-0 | PR7–20: harnesses/controls pass in places; candidate yield negative or zero at frozen gates; v9 no training | §6 | Candidate passes scope gate and motivating task control |
| Original n^(3/2) barrier | PR27–29: Hypothesis B refuted as stated, original high-D full-metric question OPEN | Atlas | Direct proof/counterexample under unchanged contract |

## 3. PR23: all 16 numbered prototype studies

Source: [PR #23 at 192df629](https://github.com/soma2-stack/AI-Architecture-Research/tree/192df629e060def0983c4e85f70c4dd01b15b6a0/prototypes/rnn_llm_architecture). Finite synthetic CPU runs; per-study protocols and evidence are retained in that tree.

| ID | Test, size, result | Verdict and meaning |
|---|---|---|
| P-001 | Width-16 protected RNN, one tagged bit, delays to 64; 40 runs, 100 updates. Protected recall 100% at 64; A/B overwrite ≈75.8%, matching last-write. | PARTIAL: single-bit retention, not selective slots. |
| P-002 | 66 runs, 3 seeds, 150 updates, delays 64/256. One protected long-delay result 83.3% at 256; random/no-projection matched or beat it; A≠B both-correct 0.7%. | FAILURE for two-slot selectivity. |
| P-003 | 42 cases (7 variants × 2 regimes × 3 seeds), 150 updates, contradictory distractor. Protected recall 100% at 64/87.6% at 256; controls equivalent/better; all-bit distractors ≈54.8%. | PARTIAL; not simultaneous storage. |
| P-004 | Dual-query, 27 runs, 9 variants × 3 seeds, 240 updates. All-pair 51.7%; A≠B both-correct 3.3% at delay 64, worse longer. | FAILURE for target; low-budget GRU/LSTM controls weak. |
| P-005 | State-conditioned gate, 30 runs, 200 updates. Delay-16 +1.3 points but 2/3 regressions; delay-64 −1.7. | FAILURE for this fix. |
| P-006 | 24 runs + 164 posthoc probes, frozen states. Native/probe: delay16 19.9%/89.9%; delay64 3.4%/41%. | PARTIAL; readout bottleneck is a useful clue, probe capacity unmatched. |
| P-007 | Query-aware frozen/joint readout; 18 runs, delay16/64. At delay16, native +150 updates 19.0→86.9%; at 64, native 2.1%, all-state probe 30.8%, joint 3.3%. One train16/test64 run 44.5%, unmatched curriculum. | PARTIAL; short gap largely training; long result weak. |
| P-008 | Curriculum vs shuffle, 36 runs. Protected A≠B at delay128 1.8% vs 2.6%, far below 25% independent-guess reference; one LSTM seed 10.5%. | FAILURE for schedule-only repair. |
| P-009 | Longer training/random timing, 75 local + 75 hosted replications, 5 seeds, 2,000 updates. Learning often began at 500–750 updates. Random writes gave delay128 100%, delay256 91.8%, versus fixed 42%/30%; no-retain learned equally and better at long delay here; matched GRU32 solved similar task. | SUCCESS for finite task; gate necessity/novelty not shown. Corrects early undertraining interpretation. |
| P-010 | Explicit delta-rule address memory vs learned models; 60 runs, 59 at 800 updates, one at 586. Delta-rule solves 2/4/8 slots at delays64/256; learned protected/GRU not reliably >2. | PARTIAL; neural failures not impossibility. |
| P-011 | Four slots, 3,000 updates, 15 runs. Protected and GRU each succeed 2/3 seeds; other runs plateau; delta-rule 100%. | INCONCLUSIVE, seed-sensitive. |
| P-012 | 36-run 3×3 initialization/data factorial. Init explained more variance in this design; protected 2/9, no-retain 0/9, contrary to related P-009. | INCONCLUSIVE/task-specific. |
| P-013 | 18 runs, 3,000 steps: learned gate 6/9 learning, 2/9 two-slot; fixed retention .0474 1/9, .005 4/9, forced g=1 0/9. | PARTIAL; fixed slow retention is a serious control. |
| P-014 | 7 models × 3 lengths × 2 cuts × 61 activation interventions; deterministic replay. Some learned-gate successes localized eight Walsh coefficients at 99–100%; fixed-.005 success used fast complement; GRU distributed. | SUCCESS for checkpoint localization only, not architectural invariant. |
| P-015 | Six models, three delays/timings, about 40 deletions/rescues/transplants. Protected coefficients needed for maintenance in some learned-gate successes; query-time deletions partial; fixed-.005 and GRU contradict universality. | INCONCLUSIVE for query-instant necessity. |
| P-016 | 324 finite transition/gradient/mask cases in float64/32. General gated recurrence algebra matches; error reported ≤≈1e−13; not canonical GRU in a fixed basis when complement gates do not commute. | SUCCESS for scoped equivalence; no novelty established (atlas F-01). |

P-009 is the key overlooked correction: P-001–008 do not show incapacity because training was short and timing constrained. P-014/015 cannot establish gate necessity because other successful organizations exist and P-016 reduces the transition to a general gated recurrence. **DO NOT REPEAT UNLESS** there is a new scaling claim and compute-matched baseline.

## 4. EFD and other synthetic/model experiments

### EFD: 15 named campaigns

Source: [experiments/efd](../experiments/efd/). Scripts and all 15 *_results.json files are present. The small CPU harness uses MLP/Transformer/GRU/LSTM and classical controls.

| Study | Setup and measured output | Verdict |
|---|---|---|
| E1 | S5 five-permutation composition and Z5 mod-5 running sum; train length 1–16, test 256, 3 seeds. Z5 GRU/LSTM/table-fold 100%; Transformers ≈20% long. S5 GRU ≈7–12%, LSTM ≈21–30% at lengths129–256; table fold 74.5–100%. | PARTIAL; task-specific, no general recurrence failure. |
| E1b | S5 undertraining check, GRU/LSTM 20k updates, 3 seeds; factorized program baseline. At129–256, GRU 85.7–86.7%, LSTM95.6–97.5%, program100%. | SUCCESS for longer training; supersedes impossibility reading of E1. |
| E2 | Reuse 13×13 addition/random Latin square under new symbols; nB=6–100, 5 seeds, neural variants and CSP. Neural models low for sparse examples; CSP reaches 100% on Latin from nB=10 and addition from nB=20. | FAILURE for neural remapping advantage in this task; CSP has explicit combinatorial access. |
| E3/E3b | Sequential Boolean regimes; online learners, kNN, expert library, Bayesian memory, meta-trained sequence models; three seeds and tests at 3/5/8 regimes. In E3b, Bayesian memory has the lowest saved mean errors among listed methods for previously seen regimes (first10 ≈.099) and changed regimes (≈.161); its steady-state error is 0. | PARTIAL: useful finite baseline finding, not evidence of a new architecture. E3b is a follow-up, not an independent replication. |
| E4/E4b | Compose digit operators depths2–4 and learn new primitive from examples; search vs meta-trained models; 6k/20k steps. Search scores 1.0 on depths2–4 and .95–.993 on new primitive; neural held-out/deeper scores nearly zero. | FAILURE for this neural target; search has direct DSL access. |
| E5/E5b | Modular-10 equation forests; train ≤6 variables/hop≤2, test up to14/hop≤7; union-find/GRU/Transformer. Union-find 100%; neural determined-answer generalization poor, often UNKNOWN-biased. E5b identity cases improve but full OOD remains weak. | FAILURE for tested neural configurations; not impossibility. |
| E6 | Split 4 superclasses into 8 subclasses in R32; 3 seeds, separations2/3/4, phase1 steps300/3k/20k, 5 labels/class. Frozen linear probe ≈.57/.65/.73; full probe≈.82/.91/.96; phase1 clustering≈.74/.81/.81; raw 1NN≈.62/.74/.85; scratch/fine-tune competitive. | PARTIAL: latent signal remains but ordinary probes/clustering recover it too. |
| E7 | Grid reachability; train 9×9, test 9/15/21/31; fixed CNN, recurrent CNN at20/60/200 iterations, Transformer, BFS. BFS exact; recurrent CNN improves with iterations, at31×31 exact solve roughly .67–1.0 across seeds at60–200; fixed CNN/Transformer poor. | SUCCESS for iterative computation on this task; not new primitive. |
| E8 | Reusable program library; 6 seeds, search budgets100k/1m. Library solves every test type in all six; often 114–357 median expansions. Flat search varies 6.7–100% at100k and improves at1m. | SUCCESS for small program-library efficiency result; overlaps known program induction. |
| Y4 | Infer symbol/style factors from noisy surfaces and partial relation; 5 seeds, ρ=.1… .85. Clustering purity1; exact search ≈.986 test at .1 and 1.0 at higher density. | SUCCESS for search control, not learned primitive. |
| Y4b | True surface IDs and correct K×M family supplied; gradient fitting. Zero perfect restarts at all densities; mean test accuracy ≈.09→.20 as ρ rises. | FAILURE for those optimizer settings, not unidentifiability. |
| Y4c | 5×4 world with four missing cells; 16 surfaces; 5 seeds at ρ=.2/.35/.6; MDL over 16–25 cells. Accuracy .831/.976/1.0; true 5×4 code ≈153–159 bits vs 4×4 ≈209/302/467. | PARTIAL; sparse case imperfect and assumptions constructed. |

EFD’s strongest positive result is E8’s reduced search with a learned library; E1b corrects a short-training conclusion. Both use known computational mechanisms. Do not repeat without matched strong baselines.

### Other model and algorithm studies

| ID | Source, settings, saved result | Verdict |
|---|---|---|
| S-01 Target validation | [target_validation](../experiments/target_validation_20260929/): 3 bounded CPU synthetic targets; 280 T1, 150 T2, 40 diagnostic + 40 control T3 runs. Known optimizer/search controls close/narrow gaps; T3 train fit still ≈16% OOD error. | FAILURE for proposed novelty targets; useful calibration. |
| S-02 Feature revision | [feature_revision](../experiments/feature_revision_20260930/): five seeds, 3 phases, 8k examples/phase, hidden128. Ordinary MLP/optimizer reset nearly closes adaptation gap. | FAILURE for proposed gap, not universal. |
| S-03 CFWM | [cfwm](../experiments/cfwm/): L=10,k=4, 40 episodes/setting, 100–30k demos for commutativity. Oracle signal cuts mean expanded nodes 367,057→4,866 with no loss in the 40 recorded episodes. Learned false-commute rate at threshold .5 falls .994→.523; at 30k examples and threshold .99 it is .273, with missed-commute rate .235. | PARTIAL: oracle-guided search useful; learned detector remains unreliable and stricter thresholds trade false positives for misses/cost. |
| S-04 OMD | [pilot_result](../experiments/omd_t1/pilot_controls/results/pilot_result.json), PR17–18: 3 seeds per LFU/LRU/SIEVE/TWOQ, 12 controllers, 36 held-out pairs. Only3/36 pass ≥99.5% imitation; Phase A stops; extraction/judge/B/C not run. Posthoc errors often correct state class, wrong recency tie-break. | FAILURE at frozen gate; no novelty test followed. |
| S-05 PRB | [prb](../experiments/prb/): Qwen3-VL-4B, Z2 n7, Z3 n5/7/9, Z4 n7 gradient binding, Z4c Latin. Z3 n9 CoT runs range from failure to100%, some hit22k eval cap; direct mapping often0–25%. Z4 free embedding train100% but unseen mostly0–20.5%; Sinkhorn sometimes100%, sometimes near chance. | PARTIAL/INCONCLUSIVE; prompt/search/config effects dominate. |
| S-06 CSL | [csl](../experiments/csl/): 13 saved JSON sweeps and completion logs. Some settings suppress spurious admissions, but the eight-seed audit certified-only loss exceeds full/same-k baseline (seed1 .312 vs .116/.131; seed5 .325 vs .138/.168). Delays/misses vary. | PARTIAL: calibration utility may trade predictive fit; not memory architecture. |
| S-07 GAS-0 controls | [benchmark_validation.json](../experiments/gas0/analysis/benchmark_validation.json): nine generated projects, eight stages each; 9/9 reference replay, no visible/hidden failure; reference/tool oracle RPS1, null .075–.188. | SUCCESS for harness controls only. |
| S-08 GAS-0 model/tool pilots | [analysis](../experiments/gas0/analysis/) and local workspace ledgers: unusable calls, malformed JSON, context/template failures, HTTP500, ledger/commit interruptions; C4 smoke stopped after stages1–3. No official 105-episode matrix. | PARTIAL/NOT RUN at benchmark scale; transport defects are not scientific failures. |

## 5. Robust dimension, endpoint, and query-visible experiments

All entries are finite fixed settings. A pass supports the stated lower certificate; a failure is not an upper bound. The full mathematical status is in the atlas.

| ID | Source and tested setup | Result | Verdict |
|---|---|---|---|
| R-01 | [endpoint certificate](../experiments/endpoint_certificate_20260930/): dense width2, one seed, four endpoints, five interval certificates, T=P+1 at n2. | Full endpoint Jacobian rank at witness. | SUCCESS for local accessibility only. |
| R-02 | [endpoint width](../experiments/endpoint_width_scaling_20260930/): n2/3/4, m=n,P=2n²+n,T=P+1. | Rank n+nP; smallest singular values 9.86e−7,1.91e−12,7.07e−19; mT≈2n³. | PARTIAL; poor conditioning, cubic resource. |
| R-03 | [approximate observability](../experiments/approximate_observability_20260930/): ε=1e−3, widths2–4,horizons11–37,six diagnostics. | Counts depend strongly on scale/horizon; scoped conditional inequalities only. | INCONCLUSIVE globally. |
| R-04 | [fixed-feature reachable operator](../experiments/fixed_feature_reachable_operator_20261002/): widths16/32/64/96,H=137/289/605/929,T=H+1; 340 cases. | Sampled finite-radius core favors roughly linear growth; full query-visible dimension unproved. | INCONCLUSIVE; float64 diagnostic. |
| R-05 | [aperiodic spectrum](../experiments/aperiodic_gate_spectrum_20261001/): W=I,b=.05,c=1,n16…256,ε=1e−3, three strategies/seeds. | Source-only counts n²/8 for n≥64 in primary setup; radius-scaled local-linear count can be zero at radius .05. | INCONCLUSIVE for arbitrary schedules/nonlinear memory. |
| R-06 | [anisotropic packing](../experiments/anisotropic_robust_packing_20260930/): widths2/3/4,T11/22/37. | Primary lower certs dense [1,0,0], independent [1,1,0]; secondary projection dense [1,2,1], independent [1,1,0]. | PARTIAL; no upper and secondary metric differs. |
| R-07 | [anisotropic replay](../experiments/anisotropic_robust_packing_replay_20261001/): n3,P21,T22, frozen rational data, 192/256 bits. | Two-axis replay and 17/17 fresh derivative checks pass. | SUCCESS for same certificate. |
| R-08 | [antipodal stage](../experiments/antipodal_robust_dimension_20261001/) and [Codex audit](../experiments/codex_antipodal_hostile_review_20261001/). | 67 candidates: 19 certificates,48 early failures of chosen sufficient test. Hostile review checked selected 5D independent/4D dense certificates at192/256 bits. | SUCCESS for stated lower certs; failures not ceilings. Runner return-shape crash was repaired. |
| R-09 | [robust witness search](../experiments/robust_witness_search_20261001/): widths2/3/4,horizons11/22/37. | Dense n3 r2→3; dense n4 r1→3; independent n4 r5. | PARTIAL; modest lower-bound gains. |
| R-10 | [certificate tightness](../experiments/robust_certificate_tightness_20261001/): widths3/4,T22/37,eight endpoints. | Sampled grids/projections suggest conservative certificates; no upper. | INCONCLUSIVE. |
| R-11 | [support-aware dimension](../experiments/support_aware_robust_dimension_20261001/): ε=1e−3 and mixed-curvature/support checks. | Highest accepted lower certificate is 4D. | SUCCESS in frozen scope only. |
| R-12 | [dimension feasibility](../experiments/independent_dimension_feasibility_20261001/): n4,T37/P24 sampled sections. | 10D highest promising; 11D lowest clear failure. | INCONCLUSIVE, not a ceiling. |
| R-13 | [third-order 6D](../experiments/third_order_antipodal_20261001/): n4,T37/P24,ε=1e−3,192/256-bit. | Minimum certified separation ≈.003314>.002. | SUCCESS for fixed 6D lower section. |
| R-14 | [third-order 7D attempt](../experiments/third_order_antipodal_7d_20261001/), frozen candidate. | All seven sufficient face inequalities fail; weakest ≈.001598<.002. | FAILURE for candidate, no impossibility. |
| R-15 | [third-order 8D](../experiments/third_order_antipodal_8d_20261001/), n4,T37/P24,ε=1e−3. | Outward intervals; 36 final checks pass. | SUCCESS for fixed 8D lower section. |
| R-16 | [radial refinement](../experiments/radial_taylor_refinement_8d_20261001/), same 8D section. | Weakest bound ≈.002049→.002294; two screened 9D candidates not promising. | SUCCESS for same section, no 9D result. |
| R-17 | [rebalanced 7D](../experiments/rebalanced_7d_section_20261001/) and [clean-room replay](../experiments/cleanroom_7d_interval_20261001/). | Different 7D chart passes at192/256 bits; weakest beta≈.00131116, separation≈.00262232; second implementation agrees. | SUCCESS; not contradiction with R-14 (different chart). |
| R-18 | [7D direct](../experiments/claude_7d_direct_audit_20261001/), [8D](../experiments/claude_8d_review_20261001/), [radial](../experiments/claude_radial_8d_review_20261001/), [rebalanced](../experiments/claude_rebalanced_7d_review_20261001/), [third-order](../experiments/claude_third_order_review_20261001/) review folders. | Audits/searches of frozen candidates. | Verification only; do not count dimensions twice. |

Remember: endpoint rank is local differential accessibility, not robust finite-error memory. Radial refinement is not 9D. The sampled 10D/11D screen is not a ceiling. Source-only and local-radius-scaled spectra differ.

## 6. AMS and benchmark infrastructure

AMS source: [automated_mechanism_search](../experiments/automated_mechanism_search/), PRs #7–16. Frozen stage reports distinguish stops:

| Stage | Actual run and outcome |
|---|---|
| v2 Stage0 | Grammar/interpreter validity; not a discovery search. |
| v3 Stage0 | 512/512 paired Task-B cosines negative; 118/118 checks pass. Stage1 stopped at calibration gates. |
| v4 Stage1 | Five seeds100–104; joint-training representability oracle V1-B-REP fails; no candidate search. |
| v5 Stage1 | Five seeds; frozen gates and generic controls pass at exactly4,000 updates. This validates task/control. |
| v5 Stage2 / repair | First run: 5,782 generated; 364 T0 checks, zero Tier1; six implementation defects. Defects were recorded, not scored. Later exact repair preserved original evidence. |
| v6 | C2 static validation fails; official Stage2 never starts; seed reserved for v7. |
| v7 | 1,000/1,000 static proposals pass; official search 5,544/6,000, eight promotions, all negative in Stage3. Negative for frozen design only. |
| v8 | Presearch tests pass; 42/56 cells filled, 0/42 elites pass frozen 8-seed confirmation; Stage3 not run, locked seeds unused. |
| v9 V0-SCOPE | Formal/literature stop before training: fixed-parameter RTRL does not need intermediate errors and no successful sparse-feedback task control exists. No candidate generated/trained. |

**DO NOT REPEAT UNLESS** a candidate passes V0 and the motivating task has a successful matched control. Do not flatten v5 defects, v6 static failure, v7 negative promotions, v8 zero confirmation, and v9 scope rejection into one outcome.

GAS-0: the nine generated projects and eight-stage harness pass control validation 9/9; reference/tool-oracle RPS=1.0, null=.075–.188. Model/tool pilots show unusable calls, malformed JSON, context/template failures, HTTP500, and ledger/commit interruptions. A C4 smoke run stopped after stages1–3. No official 105-episode model matrix is complete. **DO NOT REPEAT UNLESS** tool/context and ledger/commit paths are end-to-end stable. Harness pass is not model success.

### Implementation errors and corrections

| Record | Defect | Treatment and effect on evidence |
|---|---|---|
| Antipodal certificate runner | An early-return path returned a bare dictionary while the runner assumed a tuple, causing a crash. | A repair runner handles both shapes; frozen inputs and original result hashes were preserved. The crash is not a mathematical failure or certificate. |
| AMS v5 Stage 2 | Replacing a where-gate with its positive scalar branch could change subtree type during family stripping; six proposals raised exceptions. | The proposals were recorded as defects and never scored. They triggered a frozen stop; later protocol work is separately reported. |
| AMS v6 | C2 constructor failed coupling/descriptor static validation. | Official v6 Stage 2 was refused and never started; v7 changed the constructor under the updated protocol. Do not count v6 as a zero-yield search. |
| AMS v7/v8 pipeline | v7 could construct an uncounted candidate at the generation cap; early v8 validation had a parser bug; the old gate-zero syntax did not canonicalize as intended. | v8 added an exact-cap regression, canonical zero branch and corrected validation. The parser-only failures had pytest exit code 0 and were retained as tooling errors. |
| OMD pilot development | Development tests/extraction initially failed; the ledger records debugging and corrected unit tests before the official frozen run. | The official result remains Phase-A 3/36 pass. Development exceptions do not count as independent scientific failures. |
| GAS-0 pilots | Missing ledger, commit handling and feedback-ordering/rollback issues interrupted early attempts; API output/context failures also occurred. | Later smoke fixes tested plan-first feedback and stopped at Stage 3. The 105-episode official matrix was not completed. |
| 8D certificate export | A final export/output-string issue was found after the interval certificate. | Documentation/output repair did not change frozen mathematical data; saved interval checks support only the stated fixed 8D lower bound. |

Crashes, malformed responses, parser errors, and static-gate refusals are not silently recoded as scientific negative results.

## 7. Protected-set, bath, Householder, Route 6/7, Lemma M

| ID | Finite evidence | Verdict / scope |
|---|---|---|
| C-01 [early capture](../experiments/finite_n_early_capture_20261006/) | Reference skeleton n128…1024,m16…64, one seed, four off-cycle carriers, write≈ceil(.4n), clear2n. Retention advantage ≈10×→4,414×; donor norm flat K4…32. | PARTIAL, finite only; no dense perturbation/full-spark theorem. |
| C-02 [multistage capture](../experiments/finite_n_multistage_capture_20261006/) | n256…2048,K8…64,two channels. | PARTIAL; larger cases mostly pass; n256,K8 cross-talk .0176>.001. |
| C-03 [clear scaling](../experiments/finite_n_clear_scaling_20261006/) | 35 clear tests, five width fits, 24 width cases. R≤6 passes .001; legacy R8 misses .00251. Dense perturbation changes n512 response .00115, n1024 below .001. | PARTIAL; finite warning, no threshold theorem. |
| C-04 [R8 diagnosis](../experiments/finite_n_r8_diagnosis_20261006/) | Legacy alias 1 XOR 2=3; sum-free R8 at n2048 leakage1.88452e−5. | SUCCESS for diagnosis, not universal R8 failure. |
| C-05 [clean masks](../experiments/finite_n_clean_mask_scaling_20261006/) | Sum-free masks pass to R16; R8 widths512…4096 leakage .000224→≈.0000188. | SUCCESS in range; higher-K capacity unresolved. |
| C-06 [R20–R32 checkpoint](../experiments/finite_n_r20_r32_scaling_20261006/) | n2048 K sweeps at R8/16 and mask comparison; cross-talk flat in tested K; clean R4–16 passes, legacy aliases fail R8/12/16 near .25%. | PARTIAL: R20/24/32 and later width/age tests NOT RUN. |
| C-07 PR27/PR31 proof chain | Repairs injection/bus credit, post-gate order, attenuation, bath floor, horizon, probes, resource/dimension conversion. | VERIFIED only in stated theorem scopes; proof record, not experiment. |
| C-08 PR32 M_rest | Two-stream structure, non-amplification, operator reduction, centered channel. | AUTHOR-PROVED / PENDING AUDIT. |

C-04 corrects the interpretation of the legacy R8 failure; it does not cover R≥20. **DO NOT REPEAT UNLESS** a run targets a specific open off-cycle/listing, multistep-query, full-metric, actual-support, or R≥20 inequality with a preregistered discriminating threshold.

## 8. Online credit and distinct proof records

- **G-01 Stage A:** width8, depth1/2/3,T32/128,five seeds9401100–9401104,60 cases. Online credit matches BPTT to ≈2e−14 on tested group/layer metrics. **SUCCESS for finite algorithmic equivalence**, not compression or novelty.
- **G-02 Stage B:** 460 configurations (width8/16,T32/128,five seeds) +360 derivative diagnostics, 2,920 method records. Compact factor formats do not close hard cases. **INCONCLUSIVE** for capacity.
- **G-03 Stage B2:** 160 configurations, 20,480 sensitivity calculations; all80/80 selected hard families hit sample ceiling. **INCONCLUSIVE**; finite spectra do not bound nonlinear memory.
- **G-04 AMS-v9:** proposed sparse-terminal-feedback mechanism stopped before training because exact RTRL is a baseline and no successful motivating task control existed. **NOT RUN**.

Sources: [A](../experiments/exact_online_credit_stage_a_20260930/), [B](../experiments/exact_online_credit_stage_b_20260930/), [B2](../experiments/exact_online_credit_stage_b2_20260930/), [v9 scope](../experiments/automated_mechanism_search_v9/runs/v0_scope/REPORT.md).

Related mathematical records are indexed in the atlas, not experiment results: QSR is verified only in modified architecture; PR29 refutes selected-group Hypothesis B at D=1; PR31 first-order gather is scoped; PR32 M_rest unaudited; neutral-path tax conjectural; original n^(3/2) remains open.

## 9. Numerical and computational findings stored with theory proofs

These records live under theory folders/PR proofs rather than the 46 experiment roots. They are included because later work can easily mistake an auxiliary number or symbolic check for an experiment or universal theorem.

| ID | Record | What the saved evidence establishes | What it does not establish |
|---|---|---|---|
| T-01 | PR26 neutral-hole / Householder route, atlas N-05/X-04 | Exact small-size algebra and sampled values around .00245–.00253; reported table values .0144 at n=16,000, .0072 at64,000, .0051 at128,000. A single neutral path can broadcast query-visible credit in the scoped construction. | No all-boundary robust section; background/control can cancel; resource product is about n²/8, outside strict budget; global neutral-path tax remains CONJECTURAL. |
| T-02 | PR29 Lemma E majorant, atlas N-07 | Exact algebra plus a computer-assisted six-variable majorant certificate reports E_Y<1018.375<1019 for its stated recurrence. | It does not by itself transfer the R0 bounds to a different dense dynamics or prove Hypothesis B; transfer assumptions must be checked separately. |
| T-03 | PR31 corrected checks, atlas N-08 | Independent symbolic derivations and lightweight checks cover the nine-term decomposition, bath floor, BV constants, and residual ≤30τ/256 in the stated one-step regime. | Not a global multi-step/full-metric theorem; proof scope and query family remain controlling. |
| T-04 | PR32 numerical examples, atlas N-09 | Reported residuals 5.6e−13, 6.2e−15, 1.1e−14 and one n=65,536 bath example. | Numerical/author evidence only; not independent verification or an asymptotic M_rest proof. |
| T-05 | Theory counterexamples, atlas X-05–X-07 | The general convex moment-merger/round-robin solution is refuted; dependent-label Lemma U constant 2 is false (corrected bound 2√2, scoped theorem constant 8); fixed-anchor renewal is not a reduction for arbitrary aperiodic gates. | Auxiliary covariance/error identities and fixed-profile results survive in their own scope. Do not erase all neighboring lemmas because the general claim failed. |
| T-06 | Route 7A/7B, corridor and filter-bank diagnostics | Multiple proof/review folders contain numerical or exact finite examples, including timing/visibility obstructions, a literal K=3 word counterexample, and conditional energy-credit tradeoffs. The atlas indexes all source folders and statuses. | These are not one experiment family and must not be combined into one theorem. Several D=2, growing-K, moving-corridor and M_rest conclusions remain pending or open. |

The [atlas numerical table](RESEARCH_ATLAS.md) is the canonical source index for N-01–N-12; its X- and O-tables preserve counterexamples/open claims. This section intentionally does not rerun or rederive those proofs.

## 10. Duplicate, contradiction, and reuse map

| Apparent conflict | What actually happened | Do not repeat unless |
|---|---|---|
| P-001–008 fail vs P-009 succeeds | Earlier runs had low updates/fixed timing; longer randomized timing learns the finite two-slot task. | You test scaling with matched compute/data. |
| Protected subspace is necessary vs not | Some checkpoints localize there; fixed slow retention and general gated recurrence also succeed. | You show universal matched causal advantage. |
| Endpoint full rank vs small robust dimension | Conditioning collapses; rank is not finite-error memory. | You certify robust face separation/resources. |
| 7D fail vs 7D pass | Distinct frozen charts; first fails sufficient test, later independently certified. | New chart is prospectively frozen. |
| Radial 8D vs 9D | Same 8D section improved; sampled 9D candidates weak. | New 9D section passes whole-face certificate. |
| R8 legacy fail vs clean pass | Legacy XOR alias; sum-free mask repairs tested case. | New mask mechanism or cross-talk test. |
| R≥20 theoretical discussion vs no finite run | PR32 is author proof attempt; finite checkpoint stopped before R20. | Actual costs and inequality are explicit. |
| Large bus vs dimension | PR29 is D=1 scalar counterexample to Hypothesis B, not Ω(n) dimension. | Result controls robust dimension. |
| Neural task failure vs classical success | CSP/union-find/BFS/delta-rule have explicit algorithmic access. | Compare same information and computation. |
| Y4 search succeeds vs Y4b gradient fails | Exact combinatorial search vs optimization in a provided family. | Match evidence and compute. |
| AMS versions differ | Defect stop, static failure, negative promotions, zero confirmation, pretraining stop are different. | Candidate passes current scope gate. |
| GAS-0 validation vs pilots | Control replay is not model performance; official matrix absent. | Complete frozen model matrix can run. |

## 11. Potentially overlooked evidence

These are leads, not promoted claims.

1. **P-009:** longer randomized training solves the finite two-slot task; corrects the early low-update narrative.
2. **P-006/P-007:** retrieval/readout can bottleneck an encoded state; a capacity-matched decoder could separate representation from optimization.
3. **P-013/P-014:** fixed slow retention .005 succeeded 4/9; learned-gate and fixed-retention successes use different state subspaces.
4. **E1b:** S5 GRU/LSTM extrapolation rises to about 86%/96% at 20k updates.
5. **E7:** iterative grid recurrence improves with inference time; task performance must be reported per compute.
6. **E8:** learned library search solves six small worlds with hundreds of expansions; compare prior program-induction systems before revisiting.
7. **Clean R8 masks:** aliasing, not general capacity, caused the legacy failure.
8. **n=512 perturbation:** one response shift .00115 exceeds .001; carry the dense perturbation explicitly, but this is not a theorem counterexample.
9. **AMS v5 defects:** six crashes were disclosed and excluded from candidate scoring.
10. **CSL:** fewer spurious admissions can cost predictive fit; evaluate both axes.

## 12. Ranked unresolved avenues

| Rank | Direction | Existing evidence and exact missing result | Difficulty / repeat risk |
|---:|---|---|---|
| 1 | Convert bus/gather bound to robust dimension in original full d_F | PR29 gives scalar counterexample; PR31 first-order gather is scoped; PR32 isolates M_rest. Missing: operator/listing control for every legal query and uniform high-D section under actual support/full mT. | Very high; central; avoid amplitude-only reruns. |
| 2 | Direct original n^(3/2) proof/counterexample | Diagnostics show conditioning/radius matter. Missing: D=Ω(n), exact endpoint, legal queries, full d_F, mT=o(n^(3/2)) together. | Very high; do not import QSR/R0/selected metrics/reference support. |
| 3 | Remove log loss only after replacing false Hypothesis B | PR28 conditional chain had log loss but its premise was refuted. Missing: valid replacement premise and sharp counting inequality or matching construction. | Very high; do not refine false premise. |
| 4 | Extend clean finite masks to R≥20 | Sum-free masks pass R≤16; checkpoint stopped. Missing: exact mask/cross-talk bound plus full actual-support/horizon costs. | High; derive threshold before any run. |
| 5 | Matched structure discovery vs search in E8/Y4c/CSL | Small studies show library/search/control strengths. Missing: identical evidence/compute/oracle access and strong matched baselines. | Medium-high; high duplicate risk without preregistration. |

## 13. Complete index of 46 experiment collections

Every top-level root in the union of local and remote refs appears exactly once.

| Collection | Type / headline status | Source |
|---|---|---|
| ams_audit | Validation tools, not a separate experiment | [folder](../experiments/ams_audit/) |
| anisotropic_robust_packing_20260930 | Finite certificates, PARTIAL | [report](../experiments/anisotropic_robust_packing_20260930/REPORT.md) |
| anisotropic_robust_packing_replay_20261001 | Certificate replay, SUCCESS | [report](../experiments/anisotropic_robust_packing_replay_20261001/REPORT.md) |
| antipodal_robust_dimension_20261001 | 67 candidates; specific certificates pass, failed sufficient tests are not ceilings | [report](../experiments/antipodal_robust_dimension_20261001/REPORT.md) |
| aperiodic_gate_spectrum_20261001 | Diagnostic, INCONCLUSIVE | [report](../experiments/aperiodic_gate_spectrum_20261001/REPORT.md) |
| approximate_observability_20260930 | Diagnostic/scoped inequalities, globally INCONCLUSIVE | [report](../experiments/approximate_observability_20260930/REPORT.md) |
| augmented_accessibility_proof_20260930 | Proof plus 47 symbolic checks, not training | [proof](../experiments/augmented_accessibility_proof_20260930/PROOF.md) |
| automated_mechanism_search | AMS v2–v8 stages, mixed, no architecture promoted | [reports](../experiments/automated_mechanism_search/) |
| automated_mechanism_search_v9 | Scope stop before training, NOT RUN | [report](../experiments/automated_mechanism_search_v9/runs/v0_scope/REPORT.md) |
| cfwm | Planning/search pilot, PARTIAL | [log](../experiments/cfwm/cfwm_L10_k4_log.txt) |
| claude_7d_direct_audit_20261001 | Candidate audit | [folder](../experiments/claude_7d_direct_audit_20261001/) |
| claude_8d_review_20261001 | Certificate review | [folder](../experiments/claude_8d_review_20261001/) |
| claude_radial_8d_review_20261001 | Certificate review | [folder](../experiments/claude_radial_8d_review_20261001/) |
| claude_rebalanced_7d_review_20261001 | Certificate review | [folder](../experiments/claude_rebalanced_7d_review_20261001/) |
| claude_third_order_review_20261001 | Certificate review | [folder](../experiments/claude_third_order_review_20261001/) |
| cleanroom_7d_interval_20261001 | Independent interval replay, SUCCESS same chart | [report](../experiments/cleanroom_7d_interval_20261001/REPORT.md) |
| codex_antipodal_hostile_review_20261001 | Hostile replay/audit | [report](../experiments/codex_antipodal_hostile_review_20261001/REPORT.md) |
| csl | Structural-learning sweeps, PARTIAL | [results](../experiments/csl/) |
| efd | 15 named studies, mixed | [source/results](../experiments/efd/) |
| endpoint_certificate_20260930 | Local rank certificate, SUCCESS in scope | [report](../experiments/endpoint_certificate_20260930/REPORT.md) |
| endpoint_width_scaling_20260930 | Rank/conditioning, PARTIAL | [report](../experiments/endpoint_width_scaling_20260930/REPORT.md) |
| exact_online_credit_stage_a_20260930 | Online/BPTT finite check, SUCCESS | [report](../experiments/exact_online_credit_stage_a_20260930/REPORT.md) |
| exact_online_credit_stage_b_20260930 | Compression sweep, INCONCLUSIVE | [report](../experiments/exact_online_credit_stage_b_20260930/REPORT.md) |
| exact_online_credit_stage_b2_20260930 | Sensitivity screen, INCONCLUSIVE | [report](../experiments/exact_online_credit_stage_b2_20260930/REPORT.md) |
| feature_revision_20260930 | Feature-change target, FAILURE for proposed gap | [report](../experiments/feature_revision_20260930/REPORT.md) |
| finite_n_clean_mask_scaling_20261006 | Clean masks through R16, SUCCESS finite | [summary](../experiments/finite_n_clean_mask_scaling_20261006/SUMMARY.md) |
| finite_n_clear_scaling_20261006 | Clear/age/width, PARTIAL | [summary](../experiments/finite_n_clear_scaling_20261006/SUMMARY.md) |
| finite_n_early_capture_20261006 | Donor capture, PARTIAL finite | [summary](../experiments/finite_n_early_capture_20261006/SUMMARY.md) |
| finite_n_multistage_capture_20261006 | Multi-stage, smallest cross-talk miss | [summary](../experiments/finite_n_multistage_capture_20261006/SUMMARY.md) |
| finite_n_r20_r32_scaling_20261006 | TEST1/2 only; R20/24/32 NOT RUN | [summary](../experiments/finite_n_r20_r32_scaling_20261006/SUMMARY.md) |
| finite_n_r8_diagnosis_20261006 | Alias diagnosis / sum-free repair | [summary](../experiments/finite_n_r8_diagnosis_20261006/SUMMARY.md) |
| fixed_feature_reachable_operator_20261002 | Reachable operator diagnostic, INCONCLUSIVE | [report](../experiments/fixed_feature_reachable_operator_20261002/REPORT.md) |
| future_loss_observability_20260930 | Proof, not experiment | [proof](../experiments/future_loss_observability_20260930/PROOF.md) |
| gas0 | Harness pass and incomplete model pilots, PARTIAL | [README](../experiments/gas0/README.md) |
| independent_dimension_feasibility_20261001 | Sampled screen, INCONCLUSIVE | [report](../experiments/independent_dimension_feasibility_20261001/REPORT.md) |
| omd_t1 | Phase A stopped at 3/36, FAILURE | [result](../experiments/omd_t1/pilot_controls/results/pilot_result.json) |
| prb | Qwen3-VL symbolic binding, PARTIAL/INCONCLUSIVE | [logs](../experiments/prb/) |
| radial_taylor_refinement_8d_20261001 | Same 8D section refined, SUCCESS | [report](../experiments/radial_taylor_refinement_8d_20261001/REPORT.md) |
| rebalanced_7d_section_20261001 | Frozen 7D interval certificate, SUCCESS | [report](../experiments/rebalanced_7d_section_20261001/REPORT.md) |
| robust_certificate_tightness_20261001 | Sampled/certificate gap, INCONCLUSIVE maximum | [report](../experiments/robust_certificate_tightness_20261001/REPORT.md) |
| robust_witness_search_20261001 | Frozen witness search, PARTIAL lower gains | [report](../experiments/robust_witness_search_20261001/REPORT.md) |
| support_aware_robust_dimension_20261001 | Finite certificate, SUCCESS in scope | [report](../experiments/support_aware_robust_dimension_20261001/REPORT.md) |
| target_validation_20260929 | Three target screens, FAILURE for novelty gaps | [report](../experiments/target_validation_20260929/REPORT.md) |
| third_order_antipodal_20261001 | 6D interval certificate, SUCCESS | [report](../experiments/third_order_antipodal_20261001/REPORT.md) |
| third_order_antipodal_7d_20261001 | Frozen 7D candidate failed; no upper bound | [report](../experiments/third_order_antipodal_7d_20261001/REPORT.md) |
| third_order_antipodal_8d_20261001 | 8D interval certificate, SUCCESS | [report](../experiments/third_order_antipodal_8d_20261001/REPORT.md) |

### Branch, PR, and historical coverage

Live state checked 2026-10-17: 32 local branch heads, 18 remote branch heads, and PRs #1–32 (22 merged, 10 open, none closed). The full head/commit tables, nine local-only reachable commits, and 123 theory folders are in [RESEARCH_ATLAS.md](RESEARCH_ATLAS.md). PRs #1–6/#21–22 are lane/documentation; #7–16 AMS; #17–18 OMD; #19–20 GAS-0; #23 has the 16 prototypes; #24–32 contain proofs, audits and handoffs. Key heads: PR23 192df629; PR27 c987408; PR28 0cc0a23; PR29 f056944; PR31 35cdb7a; PR32 cef12b3.

The atlas reports 494 reachable commits and 5,583 tracked paths across these refs. This report confirmed live refs/PRs, enumerated all 46 experiment roots, and independently enumerated 123 theory roots; their names match the atlas's 123-row theory index exactly. I cross-checked major saved outputs: six finite-N summaries/progress, 15 EFD results/scripts, prototypes, robust-certificate reports, OMD result/CPU ledger, GAS-0 validator/pilot records, PRB logs/JSONL, CFWM, CSL JSON/logs, and AMS reports.

No scripts/tests/training/simulations/numerical jobs were run. Read-only parsers listed refs/files and summarized stored JSON; experiment modules were not imported. The preexisting untracked atlas and INDEX change were preserved. This is not a line-by-line audit of every raw JSON/JSONL, binary checkpoint, all generated GAS-0 workspaces, 5,583 paths, or 494 commits. Seventeen generated GAS-0 workspaces are local/untracked and not exhaustively opened. Other lane notebooks were not inspected, respecting AGENTS.md. Every collection is indexed, but some raw data remains to inspect at source.

## 14. Chronology

| Period | Discovery |
|---|---|
| PR1–6 | Lane sync, learning dynamics, benchmark suite notes. |
| PR7–16 | AMS versions and frozen gates; different stops retained distinctly. |
| PR17–18 | OMD target screen and Phase A imitation-gate failure; later phases not run. |
| PR19–20 | GAS-0 harness and quality work; control replay distinct from model outcome. |
| Sep 29–Oct 1 | EFD, target/feature screens, endpoint/observability, robust sections to fixed 8D; E1b corrected short-training S5 reading; later distinct 7D chart passed after one candidate failed. |
| Oct 2–8 | Reachable operators, aperiodic spectra, Route7A/7B and corridor analysis, mostly proofs/diagnostics in atlas. |
| PR23–26 | 16 prototypes, QSR scope correction, neutral-path tax remains conjectural. |
| PR27–29 | Protected/gather repairs, conditional theorem, PR29 selected-group Hypothesis B refutation at D=1; high-D remains open. |
| PR30–32 | Handoff, first-order Lemma M, unaudited M_rest. |

## 15. Reproduction and retrieval

This is a read-only archive. For an authorized reproduction, read the protocol/config and frozen hashes first, then use the documented source command. This archive does not authorize running it. Start with REPORT.md/SUMMARY.md, then matching results/checks/run_metadata/progress files; distinguish saved from regenerated evidence. For theorem status, use [RESEARCH_ATLAS.md](RESEARCH_ATLAS.md), the linked PR, and review response. [experiments/INDEX.md](../experiments/INDEX.md) indexes only the six finite-N suites; this document lists all 46 collections.
