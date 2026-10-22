# Actual PR37 operator — controlled-test progress (2026-10-21)

**Verdict: INCONCLUSIVE for memory advantage.** This run used the real Step 3.7 `legal_class.simulate` code, not a substitute retention toy.

At n=8192, all four tested schedules were legal and completed, with matched peak normalized forcing (~1), exact common endpoints (reported zero gap), and input amplitude <=0.05.

| Schedule | T | mT | Population gain / peak forcing | Absolute legal-query component | Absolute full selected query |
|---|---:|---:|---:|---:|---:|
| one stage, K=0 | 72 | 58176 | 0.028438 | 0.007966 | 0.011164 |
| two stages, rho=2 | 139 | 168329 | 0.024407 | 0.005999 | 0.009043 |
| two stages, rho=3 | 183 | 197091 | 0.038004 | 0.009775 | 0.011553 |
| two stages, rho=4 | 225 | 227250 | 0.050268 | 0.013216 | 0.019006 |

**Do not interpret this as a staircase win.** Time horizons and mT costs differ considerably, and some staircase settings lose. Equal peak forcing alone does not make the controls equal-budget or equal-history. This is an actual-operator schedule ablation that exposes what a fair comparison must control. The neural retrieval benchmark has NOT been run. Source repo unchanged.

Artifacts: `matched_probe.py`, `probe_results.json`. Next: enforce identical T and mT by legal schedule padding and support budgeting, check actual forcing traces and compare full selected query; then test held-out recall across seeds.
