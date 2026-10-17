# Hostile review: independent private-survivor echoes

**PENDING REVIEW. Overall PARTIAL. No robust linear memory construction.**

## Read in order

1. [INDEPENDENT_CHECKPOINT.md](INDEPENDENT_CHECKPOINT.md): committed as `185320f` before competitor inspection.
2. [RESEARCH.md](RESEARCH.md): full scope, additional post-comparison monotone local code, cost and unresolved feedback.
3. [EXPERIMENTS.md](EXPERIMENTS.md) and [COMPARISON.md](COMPARISON.md): complete numerical tables, protocol matching and limitations.

## Three claims to audit separately

1. Reciprocal private survivor boundary gates have an exactly public homogeneous product. The local old precharge cancels and the source-row bound is (1) in the independent checkpoint. Check no-wrap source indexing and do NOT assume different rows are orthogonal.
2. The fixed-gap echo, including private trace-neutral donors, admits a continuous recent-block code `q<=2hm+(2h+2)P`, `P<=6m+6N`, with the stated all-query residual. Check that ACTUAL common-field aggregates are coded, all private banks contract, final reset feedback is included, and bath/front terms are not omitted. The resulting `D=o(n)` is conditional on inherited dense/query premises and only covers fixed-gap echoes.
3. Arbitrary survivor LOCAL gate words over `S=O(R^2)` have a continuous `O(m)` approximate code at fixed query tolerance. Check monotonicity of suffix products, cancellation of precharge by coding Pi, bin endpoint coverage, coefficient support, the factor from two physical copies, and the actual ordinary-row query bound. This theorem does NOT control complete H.

## Highest risks and explicit nonclaims

- The constant .073 and front remainder `30000(N+1250)/n` are inherited estimates, not numerically certified at these finite widths. Recheck their transfer to the enlarged private survivor bank.
- The public right parameter space must contain complete feedback directions, including donor compensators and all moving private tracks. Formal matrix rank is not robust code dimension.
- Every private opposite pair is forced throughout the history. Leaving a changed pair autonomous would invalidate the public forward bath/front induction used here.
- Source sigma=.05 and the reference operator are numerical proxies for the admitted exact source root/dense lift. No finite experiment independently certifies that lift.
- The local monotone code can have enormous tolerance-dependent constants. Its asymptotic statement does not demonstrate practical compression at the reported widths.
- The fixed-gap proof does not extend to weak echoes with contraction `1-Theta(1/R)`.
- Found query scores lower-bound a restricted search, not upper-bound all legal queries. Eight-control spectra at one fixed query are not robust continuous dimension.
- Comparison harmonizes exactly two PUBLIC competitor operations (preparation and reset), documents both, and also includes unmodified competitor replays. Private schedules are not changed in the pinned snapshot.
- Product-matched interior controls change the control subspace/count. Their smaller score is not a universal causal or capacity theorem.

## Exact dependencies

- [Original frozen/query contract](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md), section 9: actual future adjoints and fixed-feature normalization; follow its model/source definitions.
- [Prior complete feedback proof](../astra_route7a_feedback_compression_20261008/PROOF.md), sections 1-2: full rank-two chronology and field; section 4, equations (18)-(22): bath/front including terminal; section 5: right parameter support; section 7: continuous code/Borsuk-Ulam conclusion.
- [Baseline long-window report](../astra_route7a_long_window_20261008/RESEARCH.md), section 3: compensation legality; section 4: sufficient public bath/front certificate; section 6: exact block aggregates, donor contraction and .073 coefficient; section 7: inherited front/dense conditions; section 9: absolute-history cost.
- [Gemini audit](../gemini_astra_route7a_feedback_audit_20261008/PROOF.md): scope of the earlier feedback theorem. It does not independently verify the new claims in this folder.
- Baseline implementation: [long_window.py](../astra_route7a_long_window_20261008/long_window.py). New implementation: [private_echo.py](private_echo.py).
- Competitor source: commit `f8a96fb8b8dfe0c072e82dc57b8c23cbc20de89c`, `theory/gpt6_private_survivor_capture_20261008/private_survivor_variant.py`; byte-exact local snapshot and hash in [COMPETITOR_PROVENANCE.json](COMPETITOR_PROVENANCE.json). Historical competitor files remain untouched.

## Reproduction and evidence

Use commands in EXPERIMENTS.md with one BLAS thread. Runners resume completed data. For fresh reproduction use a separate copy without result JSONs; preserve these archives. `test_math.py` checks monotone coding, block aggregates and cross-protocol endpoints. Independent run validation checks dense/sparse chronology and transpose duality. All are numerical consistency tests, not theorem proofs.

## Reviewer decision requested

Return separately VERIFIED / PARTIAL / REFUTED / OPEN for: local echo bound; fixed-gap complete code; arbitrary-word local monotone code; implementation/query validity; fair comparison. Identify the first load-bearing gap before optimizing constants.

## Single next obligation

After equalizing the local survival code, prove an `o(n)` approximate code for complete H in weak echoes at legal-query tolerance .001, or construct a legal uniformly robust antipodal family that refutes it. No inference from scalar score or nonzero Jacobian rank is sufficient.
