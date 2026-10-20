# Status — claude_dense_transfer_20261020 (updated after Codex audit)

Independent Codex audit of PR #35 commit `b984ef9347219d62db4dfd39f8f2e263317c9a33`
(2026-10-20) found both main theorems valid within the exact-real contract. The
auxiliary scope/precision edits made afterward are not a new independent audit.

| Claim | Status after audit | Qualification |
|---|---|---|
| Prescribed dense all-ones matrix and normalization | PROVED | Special rank-one field, `eta <= 1e-8/n^2`; not a generic dense matrix |
| Lemma 2.1D: balanced locality/endpoints | PROVED | Structural result for well-defined all-ones-coupled targets, not a universal gate theorem |
| Lemmas 2.2D–2.3D: legality, bath and front gate | PROVED | Prescribed small-coupling normalization only |
| Lemma 3.1D: gate facts G1–G8 | PROVED | Gate facts checked against inherited PR #34 chain |
| Lemma 3.2D: credit correction | PROVED | `<= 1.5e-8 c_*` per column in prescribed contract |
| **Theorem 6.1D / Corollary 6.2D** | **PROVED in independent Codex audit** | Quarter-root section and original Lemma M counterexample transfer to prescribed dense matrix |
| Proposition 5.1: full-metric lower bounds | PROVED | Full credit distinguished explicitly from selected credit; lower bounds only |
| Proposition 6.1: generic one-step merging | PROVED in stated scope | Not a multi-step impossibility theorem |
| Proposition 7.2: structural transfer | PROVED after scope correction | Actual support **at most** scheduled envelope; quantitative part requires prescribed normalization and gate/source bounds |
| Lemma 9.1: saturation guarantee | PROVED | Exact-real full-spark code; numerical conditioning can be extreme |
| **Theorem 9.2** | **PROVED in independent Codex audit** | `D = floor(floor(n^(1/3))/2400)`, `m <= 3`, `T=n/2`, `n>=1e16` |
| Corollary 9.3: Lemma M refutation | PROVED | Combined listing count; stated constant thresholds |
| Corollary 9.4: sharp listing order | PROVED in stated scope | First-order gather listing, fixed `m=3,T=n/2`, not all metrics |
| General-width concurrent-pair rate | OPEN | Second-order analysis not completed |
| Finite-precision memory implementation | OPEN | Audit showed encoding gain `>10^50` at `D=89` |
| Full dense fixed-feature `D=Omega(n)`, `mT=o(n^(3/2))` | **OPEN** | Centered/second-order bus channels remain unresolved |

PR #34, earlier audits, AGENTS.md and restricted notebooks were not modified.
Nothing was merged; this PR remains draft.
