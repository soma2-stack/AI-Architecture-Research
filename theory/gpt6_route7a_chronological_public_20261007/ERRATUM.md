# Erratum: stale local trace in chronological Route 7A probe

Date: 2026-10-08. Origin: independent follow-up inspection of `chronological_probe.py`.

**Severity: LOAD-BEARING for the numerical investigation.** This corrects the simulator, not the independent algebraic theorems for Astra's genuine Eq. (25) trace-neutral control.

## Bug

In the version of `chronological_probe.py` preceding GitHub commit `580a27e32b31418ac0c52b420833c917b288c676`, `tau=np.zeros(m)` was initialized before the public precharge. The precharge branch set the donor gate to `GH` but did **not** advance the local sensitivity trace via `tau <- GH*(1+a*tau)`. At the first private write the code therefore used `incoming=0` rather than the true `kappa_L=GH*(1-(a*GH)^L)/(1-a*GH)`, then computed the third gate `d3` from the wrong incoming trace. The stage-3 assertion only checked the incorrect scalar formula against itself, not the real moving-characteristic local row trace.

## Quantitative reproducible example

For `n=65536,R=32,L=ceil(sqrt(n*R))=1449,a=1-1/n,GH=.99999,g*=.9975,epsilon=.0001`:

- True incoming local trace after precharge: `kappa_L=1422.8074462013935`.
- Old code's assumed incoming trace: `0`.
- With opposite controls x=+1 and x=-1, and gates calculated using the stale trace, **actual** outgoing local trace values were `1418.707969208682` and `1418.5185867978812`, differing by **0.18938241080081752**.
- Recomputing gates using the true incoming trace gives outgoing values `1418.6132811622285` and `1418.6132811622288`, differing by approximately `2.3e-13`.

These figures come from independently evaluating the closed-form scalar local sensitivity recurrence and the third-gate compensation formula. They are NOT rerun full numerical M/L/H probe values.

## Repair

The updated script now:
1. Advances `tau=GH*(1+a*tau)` on every public precharge step.
2. Tracks a separate actual `trace_live` updated from the effective per-step donor gate at EVERY step.
3. Checks that `tau` agrees with `trace_live` at each new private stage.
4. Checks that the actual stage-end trace matches the target immediately after phase 3.
5. Reports a maximum stage trace error in the result.

**Important limitation:** Updating the code and checking its textual logic is not the same as executing the full experiment. The post-fix numerical M/L/H results are NOT yet available in this note.

## Status of old evidence and next step

Treat `RESEARCH.md`'s historical numerical signal tables, `RESULTS.txt`, and earlier claims about the relative dominance of H and L as **SUPERSEDED / UNVERIFIED** pending a corrected replay. Exact hidden-state endpoint matching under a final forced reset did not establish sensitivity trace matching, so it never validated the intended donor protocol.

Next mandatory steps: rerun the updated script at the small n,m,R cases; verify near-zero `max_stage_trace_error`, compare new scores against historical values, and obtain independent verification. Only then progress to optimizing H with fully admissible geometry and/or establishing a robust width theorem. The algebraic 26-stage cube bound and independently reviewed growing-R local-direct bound concern the correctly specified analytical trace-neutral family and are not invalidated by this simulation bug.

Do not modify CURRENT_THEORY.md based on this experiment.

## 2026-10-08 second bug, independent validation, and replay

A further check revealed an **off-by-one stationary compensator indexing error**. The array \`stationary\` was already zero-based, yet the original line
\`donor=np.r_[A+1+np.arange(m)+t,B+1+np.arange(m)+t,stationary]-1\`
subtracted one again from stationary positions. It left one intended prepared compensator undriven and put one driven compensator at an unintended site. The repaired expression is
\`donor=np.r_[A+np.arange(m)+t,B+np.arange(m)+t,stationary]\`.
A new runtime assertion verifies that opposite-control schedules have identical gates outside actual intended donor coordinates at every step.

The **fully rerun** corrected simulations and separate matrix-level tests are in [CORRECTED_RESULTS_20261008.md](CORRECTED_RESULTS_20261008.md). Both defects were fixed before those final runs. Key results (full M, optimized one-step query over a pair of all-positive versus all-negative control words):
- \(n=16384,m=4,R=2\): \(1.2835479051\cdot10^{-9}\);
- \(n=32768,m=8,R=4\): \(1.7449642021\cdot10^{-9}\);
- \(n=65536,m=32,R=16\): \(6.6615295674\cdot10^{-9}\);
- \(n=65536,m=64,R=32\): \(1.8040244634\cdot10^{-8}\);
- \(n=65536,m=64,R=48\): \(2.2262559886\cdot10^{-8}\).

Across independent matrix-vector local sensitivity checks, \(\|\Delta L_N \mathbf1\|_\infty\le1.71\cdot10^{-13}\) at the tested widths; off-donor gate differences \(\le2.23\cdot10^{-16}\) (instead of \(2\cdot10^{-4}\) before indexing fix); forward/transpose consistency relative error \(\le5.44\cdot10^{-14}\). The old historical scores in \`RESEARCH.md\` and \`RESULTS.txt\` remain superseded.

Multi-start optimization (five legal box starting gate words, four ascent iterations) returned best \(M=1.745334743\cdot10^{-9},H=2.629870639\cdot10^{-10}\) for \(n=32768,m=8,R=4\), and \(M=6.662535991\cdot10^{-9},H=1.070780484\cdot10^{-9}\) for \(n=65536,m=32,R=16\). This changes the single-start numbers only minimally but is still NOT a global maximum.

These are **finite reference surrogate queries**, not full legal dense-family proofs, and the stronger accepted \(S\le d/100\) asymptotic geometry remains out of range at these widths. Main \(H_N\) robust width problem is OPEN.

