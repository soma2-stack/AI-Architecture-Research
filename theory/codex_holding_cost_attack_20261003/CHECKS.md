# Checks and internal audit

## Resource declaration before computation

RESOURCE_POLICY.md and PLAN.md were written before the numerical runs.
Each script limits all standard numerical pools to ONE before imports.
No workers or parallel test runner. Actual maximum process thread count
was 4, within the owner's total job limit of8. The additional threads are
runtime/helper threads; requested numerical parallelism is1. Runs were
sequential, so their counts do not add. No GPU library/kernel/monitor used.

Every instrumented phase checks process threads, child processes and RSS,
aborting at >8 threads or >256MiB. Original logs are not overwritten.

| Run | Recorded checks | Outcome | CPU seconds | Peak working set |
|---|---:|---|---:|---:|
| checks.py | 61 | PASS | 2.28125 | 56,487,936 bytes |
| checks_autonomous_preparation.py | 13 | PASS | 1.0625 | below first-run peak |

CPU total3.34375s, approx .05573 CPU-minutes. GPU0. Mathematical timers
exclude shell startup/library discovery/documentation. No resource violation.

## Derivation audit

- Accepted theorem is a premise, not re-reviewed. Existing sources retained.
- Exact energy expansion includes signed interference rather than treating
  bias and transport as independent positive costs.
- Source feature is UNIT 1_l/sqrt(l), not scaled to conceal source loss.
- Whole-ball profiles use a shared amplitude. Direct temporal diagonal
  dominance replaces a column-selection bound; old F^-1 word loss is paid.
- Exact ceiling T=ceil(1e14 sqrt(n)F^3), floors, net/excluded-frequency and
  admissible gate/input conditions checked in proof and rational scalar cases.
- Moving bath is PUBLIC because paired positive states plus stationary
  negative compensators have EXACT zero selected sum; exceptional front
  cannot catch the driven corridors before reset.
- Preparation, all active inputs and every dense correction are charged;
  autonomous reference bath has actual zero reference input.
- Reset is a prescribed simultaneous transition, not asymptotic convergence.
- The projected matrix entries are chronological gate products supplied by
  coupled injections; no independent-column or matrix-ball assumption.
- Query supremum is infinity-to-L2, from real independently legal future
  gate values; residual private projected coordinates vanish by exact support.
- All-horizon upper applies only to this projected private block; dense
  error is additive, not a multiplicative claim near zero.
- Sparse harmonic optimized barrier is a limitation of a sufficient ledger;
  it is not a lower bound on actual query-visible widths of other sections.
- Pulse duty rho is analyzed with optimized accumulated modulation. Fixed
  delta would give a different required T scaling and is not conflated.
- General H bound includes the whole history, not just a final phase.
- General exponent bracket and full-model gap remain unchanged.

The new proofs are ready for hostile review, not claimed independently
accepted. All small-width outputs are diagnostics, not dimension certificates.

Administrative diff check initially flagged one extra blank line at the end
of RESUME_ENTRY.md. That whitespace was removed before commit; proof and
numerical inputs/outputs were unchanged. No mathematical check failed.
