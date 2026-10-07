# Current theory — 2026-10-06

Authoritative navigation snapshot, consolidated from the preservation-complete base `d1767d0a62dba90b03fd21e512b3db0c4efcd133` and the missing Claude folders. This document records existing evidence and owner acceptance; it introduces no new theorem. [INDEX.md](INDEX.md) covers all historical theory folders.

## Current state — 2026-10-06 (authoritative hierarchy)

This hierarchy supersedes the dated moving-corridor next-action statements retained below. It records the stated scope and review evidence; it does not strengthen the source proofs.

1. **Baseline contract.** The frozen dense tanh / robust learning-credit contract, normalization, legal-query conditions, and energy conventions are given in [Scope / contract](#scope--contract) below.
2. **Established absolute-energy and global results.** The previously reviewed absolute-energy and full-model results in the table below remain scoped to their stated families; this consolidation does not extend them.
3. **Absolute-history exponent bracket.** The fixed-feature absolute-history-norm exponent bracket remains `[1/4,3/4]`, up to its stated slow or polylogarithmic factors.
4. **Multicolumn and repeated-write progression.** The [multicolumn spatial-write](codex_multicolumn_spatial_write_20261005/) and [repeated near-critical filter-write](codex_repeated_nearcritical_filter_write_20261005/) records, alongside [multisurvivor Hadamard writes](codex_multisurvivor_hadamard_write_20261005/) and [moving-probe writes](codex_moving_probe_spatial_write_20261005/), document scoped construction attempts and limits. Their repository statuses are recorded individually in the index; author-local `PROVED` labels alone do not confer verification.
5. **Coded-donor spreading.** The [frontier-invention record](codex_frontier_invention_20261006/) develops simultaneous coded donor controls. Its source-level claims and independent-review status remain distinguished in the index.
6. **Early-capture linear frontier.** The [linear-dimension frontier](codex_linear_dimension_frontier_20261006/) records early capture before trace repair, its scoped finite-stage donor-control obstruction, and the linear boundary. Review status: **VERIFIED IN STATED SCOPE**, with mixed evidence recorded below: Gemini and Grok verified in scope; Sonnet verified in scope with an inherited-premise caveat; Perplexity/Sol found insufficient evidence for complete independent certification, no counterexample, and support for the core algebra, topology, and obstruction.
7. **Best strict-budget result.** `D >= n/[10^70 log log n]` with `mT=o(n^(3/2))`, within the source construction's admissible regime.
8. **More generally.** The early-capture result allows arbitrarily slowly diverging dilution within its stated admissible regime; this does not assert linear dimension at strict little-o budget.
9. **Linear boundary.** The same protocol reaches `D=Omega(n)` at `mT=Theta(n^(3/2))`.
10. **Scoped bounded-stage obstruction.** The obstruction applies to the specified donor-control family. It is not a universal RNN impossibility result and does not exclude other architectures or unrestricted control families.
11. **Main open problem.** Establish `D=Omega(n)` with `mT=o(n^(3/2))`, or prove an appropriately scoped obstruction. The finite-stage result does not settle the unrestricted problem.
12. **Finite-size protected-channel evidence. EXPERIMENTAL / FINITE-SIZE ONLY.** [Clean-mask scaling](../experiments/finite_n_clean_mask_scaling_20261006/) reports numerical protected Walsh-channel checks through `R=16`. The later [R20–R32 checkpoint](../experiments/finite_n_r20_r32_scaling_20261006/CHECKPOINT.md) found no K-dependent degradation over the tested values at `R=8,16`; sum-free masks passed the finite `0.1%` cross-talk target through `R=16`, while alias-prone legacy masks failed at `R=8,12,16`. At `n=2048`, fully independent labels are limited to six dimensions and the matched independent-family run was only available at `R=4`. Higher-order XOR-relation counts alone did not explain leakage; no clean-mask finite-size capacity limit was observed through `R=16`. These results do not prove an asymptotic theorem or change theorem status. See [experiment index](../experiments/INDEX.md).

**Next theoretical direction:** grow `R` jointly protected controls per donor group without an `R`-fold write-duration cost. The current open problem is the strict-budget linear-dimension result above; the older `D=2` repair action is not current.

## Archived detailed snapshot — 2026-10-04

The detailed status narrative below is preserved for provenance. Where it conflicts with the authoritative 2026-10-06 hierarchy above, the hierarchy and newer folder records govern. Historical proof-gap statements remain history, not current next actions.

## Scope / contract

The current theory studies robust continuous learning-credit memory, especially the fixed-feature quantity `d_F`, for a frozen dense tanh family. The active near-critical regime is `c=1`, `gamma=1/n`, and `epsilon=0.001`. Gradients use the accepted group-RMS normalization and the supremum over actual legal future queries, whose preactivations lie in `[0.25,0.75]`. Future inputs are frozen when differentiating; their preactivation contract differs from the admissible past-input cube.

Lower bounds require one jointly admissible continuous finite-radius section with the same exact endpoint and uniform boundary-antipodal query separation. Whole absolute past-input norm counts preparation, holding, corrections, and reset. Local radius instead measures movement around a public center. All history-dependent persistent coordinates count. Public model constants and temporary arithmetic have the exclusions in the source contract. Static codes used for topological obstructions are not automatically causal online encoders.

## Current accepted results

Repository status convention: owner disposition and independent review are separate axes. `ACCEPTED` records owner/project disposition; `VERIFIED` requires independent review evidence in the stated scope. A preserved report's own words such as `PROVED` are author-local claims and do not by themselves create repository-level `VERIFIED` status.

| Contract / result | Current statement | Evidence and status |
|---|---|---|
| Growing local radius, all-admitted fixed-feature histories | `Omega(n^(16/15))`, with `D >= n^(16/15)/(2*10^11)`; the reviewed explicit regime uses `n >= 10^75` and local-radius majorant `48 n^(1/3) sqrt(log n)` | **ACCEPTED; independently reviewed in this scope**: [consolidation](codex_multiharmonic_consolidation_20261003/), [Grok review](grok_multiharmonic_16_15_review_20261003/) |
| Width-independent LOCAL radius | Radius `<0.02` around public `X_n(0)`, `D >= n^(19/18)/20,000,000`, half-margin `>999.999649997999` for `n >= 10^900` | **ACCEPTED**: [proof](codex_bounded_history_multiharmonic_20261003/), [Claude review](claude_bounded_history_radius_review_20261003/), [Grok review](grok_bounded_history_radius_review_20261003/) |
| Best superlinear construction charged by ABSOLUTE history energy | `D >= nF/10^7`, `||X||_2 <= 4*10^7 n^(3/4)F^(3/2)`, half-margin `>0.9997`, `n >= 10^200`, `2 <= F <= n^(1/16)` | **ACCEPTED**: [holding-cost proof](codex_holding_cost_attack_20261003/), [Grok review](grok_holding_cost_attack_review_20261003/) |
| Logarithmic packet choice | `F=floor(log n)` gives `d_F=Omega(n log n)` at `R_abs=O(n^(3/4)(log n)^(3/2))` | Same accepted packet; strongest current superlinear absolute-energy result |
| Fixed absolute energy, frozen biased family | Past-credit query magnitude `<= (L_n+H_R)/sqrt(n)` with `L_n=O(log n)` and width/horizon-independent `H_R` for fixed `R_abs`; tends to zero. Exact forward state remains `n` coordinates | **VERIFIED**: [autonomous energy theorem, Theorem 4](codex_autonomous_absolute_energy_20261003/PROOF.md), [Claude review](claude_autonomous_energy_upper_review_20261003/) |
| Zero endpoint feasibility | `||X|| > 0.0499 sqrt(n/2)` and sharper approximately `0.05 sqrt(n)-0.709`; fixed-energy zero-endpoint class eventually empty | **VERIFIED**: [absolute-energy proof](codex_absolute_history_energy_20261003/), [Claude review](claude_absolute_energy_review_20261003/). Feasibility only |
| Full-model near-critical bounds | `Omega_c(n^2) <= d_rob <= O_c(n^2 log n)` for arbitrary horizon; finite `O_c(n)` horizon already matches quadratic order | **VERIFIED**: [quadratic construction](gamma_c_over_n_quadratic_20261001/), [Claude review](claude_quadratic_review_20261001/), [log-gap note](arbitrary_horizon_log_gap_20261001/), [review](claude_log_gap_review_20261001/) |

The general fixed-feature constructive/necessary **absolute-history-norm exponent** bracket remains **[1/4, 3/4]**, up to slow/polylog factors; the exponent is for `R_abs=||X||_2`, not squared energy. The necessary `1/4` edge follows from the scoped actual-query upper in the autonomous-energy proof; it is not a matching superlinear-dimension law. The sufficient edge is the packet above. The old `7/8` packet and `3/4` packet with log power `9/4` are **SUPERSEDED** as best energy bounds, not refuted.

The local-radius center has no width-independent absolute norm. Finite history radius at each width is not a uniform absolute-energy promise. History length may grow. Constant absolute energy can therefore make credit negligible without contradicting either local-radius lower bound. The autonomous theorem covers the frozen family and its endpoint choices; it does not resolve the full-model worst case.

## Moving-corridor status

**The complete moving-corridor mechanism remains OPEN.** Its history construction has an exact common nonzero endpoint and `||X||_2 <= 2 sqrt(m(T+2)+1)`; this is an upper bound, not a reversible energy lower bound.

1. **ACCEPTED — paired projected channel only.** Monotone suffix-product rows admit a static continuous quantile code. The strongest code cap is

   `D <= min(mT, m[max(1,ceil(16000 sqrt(mT min(m,T))/n))-1])`,

   and hence `D < 16000 mT/sqrt(n)`. Thus superlinear dimension in this channel needs `mT=omega(n^(3/2))`. This does not control unpaired private sensitivity or prove causal compression. [Proof](codex_suffix_product_kernel_attack_20261003/), [hostile review](codex_suffix_product_hostile_review_20261003/).

2. **ACCEPTED — full sensitivity exposes private renewal.** Pairing cancels public state and balanced output modes, not differentiated credit. The common-mode response obeys `V_(i,t)=a g_(i,t)(V_(i,t-1)+J_(t-1))`, with `J_t=u^T M_t`; prefix-suffix crossovers and all Householder renewals remain. The old paired `8/n` coefficient does not bound this channel. Short complete packets have distance `<0.095982(T+1)/sqrt(n)`; `T+1<=0.020 sqrt(n)` precludes robust sections. [Ledger/proof](codex_unpaired_corridor_sensitivity_20261003/). Owner acceptance is explicit; a dedicated review folder is absent.

3. **ACCEPTED / Grok VERIFIED — local-code counterexample.** Equal old local codes can have `Gamma>0.03`, actual pair distance `>0.03-8e-9`, and a continuous `D=1` section with half-margin `>0.014999996`. Main family: `mT<=11n^(5/4)`, norm `<8n^(5/8)`. Log-budget family: `mT<=11n(log n)^2`, norm `<8sqrt(n)log n`. These are cheap signals, not superlinear dimension. [Proof](codex_private_renewal_gamma_20261003/), [Grok review](grok_private_renewal_gamma_review_20261003/).

4. **VERIFIED — changing survivors defeat pointwise-small timing.** `||J_t||_2 < 2.01 min(t,n)/sqrt(n)` remains valid; a centered universal `O(1/m_s)` entry bound fails. Many large entries form one coherent contrast. [Timing proof](codex_timing_signal_J_20261004/), [Grok review](grok_timing_signal_J_review_20261004/). Claude's imported [joint transfer](claude_multidonor_joint_section_20261004/) is **CONDITIONAL** as a complete compression theorem: its sparse-resummation premise is not established, and its literal small-entry route is defeated. Exact transfer identities are author-derived, pending independent review; their preservation does not certify them.

5. **PARTIALLY ESTABLISHED / PENDING REVIEW — filtered timing and the claimed `D=2` completion.** The exact suffix-filter identity, long-low-run erasure estimate, and single-cohort flat-high-window collapse in the [filtered note](grok_filtered_timing_width_20261004/) remain useful in their stated scopes. However, its disjoint-packing restriction is **not established as a necessary bound**: the displayed argument derives a support-size necessity from a visibility lower bound, which does not supply the required upper bound on the complete query signal. The first `D=2` and band notes remain incomplete. The later [monotonicity report](grok_filtered_timing_d2_monotone_20261004/) is now **PENDING REVIEW / PROOF GAP**: its sign argument is proved for powers of a frozen `A(q)` but does not establish the same sign for the actual time-ordered product with changing `q_t`; the spectral derivation also contains sign typos. Therefore the joint `D=2` square, its `>0.009` margin, and downstream claims that require that theorem are **not established from the current evidence**. This is a proof-gap finding, not a counterexample to `D=2`. [Historical square](grok_filtered_timing_d2_20261004/), [historical band](grok_filtered_timing_d2_band_20261004/).

6. **ACCEPTED only as a narrow matched-versus-low observation — uniform one-block gates.** In the preserved [one-block note](grok_filtered_timing_one_block_20261004/), the zero-sum/orthogonal survivor component is reproduced in both matched and low-donor histories, while the strong difference lies in the all-ones coefficient up to the stated complement. Keep that algebraic observation in its present uniform-gate probe family. Do **not** treat the note's claimed best `D=2` section or its disjoint-packing `D=o(sqrt(n))` consequence as established; those depend on the unresolved `D=2` and packing arguments above. This is not a theorem for arbitrary nonuniform gates.

7. **PENDING REVIEW — newest nonuniform spatial writes, corridor head `c682b27`.** [Codex spatial-write folder](codex_single_block_spatial_write_20261004/) claims two robust modes on one support and one joint `B^R` for `2<=R<=floor(log2(n)/8)`, half-margin `>0.0024`, `mT<=4*2^R n^(5/4)`, norm `<5*2^(R/2)n^(5/8)`. It uses a single fixed parameter probe, fresh Walsh spatial masks, and zero-sum protection. At maximal `R`, absolute-history-norm exponent `11/16` supports only logarithmic dimension; it does not improve the superlinear threshold. Internal checks are not independent review. Its single-probe response cap `D<=n` is also pending review. [Codex multidonor analysis](codex_multi_donor_joint_section_20261003/) remains **PENDING REVIEW**.

**Dense-error correction:** a previous displayed bracket was algebraically wrong. The reconstructed dense pair comparison is approximately `1.4e-12` at `n=10^6`, with conservative pair charge `<=8e-9` retained. The short-packet result does not depend on the bad display. See [unpaired ledger](codex_unpaired_corridor_sensitivity_20261003/), [renewal derivation](codex_private_renewal_gamma_20261003/), and [timing review](grok_timing_signal_J_review_20261004/). No historical display is edited here.

## Historical exact open problem — 2026-10-04 snapshot (superseded)

First repair or independently resolve the `D=2` time-varying-propagator gap and the filtered-timing packing inference. Then independently review the pending nonuniform spatial-write theorem. If those steps survive, determine whether a growing family of **parameter-column probes can share the same protected survivor patterns** in one jointly admissible continuous section, with uniform actual-query antipodal distance `>0.002` and `D=omega(n)` while `mT=o(n^(3/2))`. Counting columns, donor epochs, large timing entries, or separately robust directions does not answer this. No complete-corridor finite-error code or such superlinear lower section is established.

The broader target remains a constructive absolute-history-norm exponent strictly below `3/4`, or a stronger scoped obstruction. The full-model logarithmic gap remains separate.

## Known dead / closed routes

- **REFUTED as general solution:** convex transport averaging and round-robin packet scheduling. Auxiliary covariance/error identities survive. [Review](claude_moment_merger_review_20261001/).
- **REFUTED as a reduction:** fixed-anchor basis renewal does not solve arbitrary aperiodic gates. Fixed-profile encoders survive. [Review](claude_transport_basis_review_20261002/).
- **VERIFIED collisions:** old sustained superlinear-looking charts are not robust sections; this does not prove a class-wide linear upper. [Moving-spike analysis](claude_moving_spike_remainder_20261002/), [review](grok_spike_remainder_review_20261002/).
- **Closed only in scope:** paired projected suffix products below the `mT` budget; sufficiently short complete corridors; and, inside the studied uniform one-block matched-versus-low family, the orthogonal/zero-sum survivor-mode cancellation. The unresolved `D=2` completion and disjoint-packing necessity are not closed results.
- **REFUTED:** uniformly small equal-code private renewal and centered pointwise `O(1/m_s)` timing bounds. Integrated/query-weighted alternatives remain open.

## Things we must not infer

Continuous-coordinate dimension is not bits, finite-precision storage, VRAM, or training cost. Exact rank, tangent rank, monomial count, parameter count, and packing are not robust continuous dimension. One frozen family is not every RNN. Asymptotic thresholds give no practical-onset or architecture-success claim. Numerical checks do not prove asymptotic theorems. A norm upper bound on a history cannot be reversed into an energy lower bound. STATIC code obstructions do not implement an online encoder.

The [Perplexity accessibility packet](perplexity_accessibility_proof_draft_20261004/) is **DRAFT**, with provenance; committing it does not establish robust finite-error accessibility. Independent review records and archival notebooks are preserved unchanged. Missing dedicated reviews and pending status are recorded in [INDEX_LEDGER.json](INDEX_LEDGER.json).
