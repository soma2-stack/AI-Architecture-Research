# Stationary parameter-complement code: source recovery record

Date: 2026-10-07. Author: Codex. Repository status: **PENDING REVIEW**.

## Recovery result

The exact original derivation of
\[
q_{\rm stat}\le R(2^R+1)
\]
was **not recovered** from the available Codex notebook, main-branch research files, or reachable Git history. The count appears in the later moving-cycle author report as an upstream checkpoint, without the classification/counting proof. This record does not reconstruct the missing proof and does not label the equation established.

## Recovered stationary geometry

The repository does document stationary subspaces used by related constructions. In `theory/codex_linear_dimension_frontier_20261006/PROOF.md` §3, lines 121–159, each four-site tuple has two moving positive cycle coordinates and two stationary negative off-cycle compensators. The donor/survivor partition and probe bank are specified there; the selected tuple sum is balanced, and the chosen probe columns are stationary, zero-sum, and fixed by the reference recurrent operator. The same file §6, lines 234–259, gives public stationary donor traces at stage entrances and exact trace matching after capture.

In `theory/codex_frontier_invention_20261006/PROOF.md` §3, lines 117–153, stationary donor indicators are combined with a shared survivor indicator to form an orthonormal probe bank. The formulas establish \(V^TV=I\) and that each selected probe is stationary, zero-sum, and fixed by \(O_*\). These facts support the existence of some stationary zero-sum directions. They are not a classification of the entire parameter complement.

`theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md` §4, lines 108–145, records four-site modes, stationary compensators, and local row recurrences. §5, lines 147–202, records the common bath response. `theory/codex_holding_cost_attack_20261003/PROOF.md` §4, lines 139–201, records stationary compensators and a public bath construction. These are relevant ingredients, not the missing code proof.

## Requested classes: recovered versus missing

| Class / step requested | What is recovered | What is missing |
|---|---|---|
| Within-donor stationary zero-sum directions | Stationary tuple/group indicators and selected zero-sum fixed probes occur in the cited construction proofs. | A decomposition of every within-donor stationary parameter direction, with a proof of which coefficients are public, cancel, or remain history-dependent. |
| Survivor-mask-class zero-sum directions | The construction has Walsh-labeled survivor sites and public capture masks; §8 of the early-capture proof gives a one-step capture identity. | A full basis/class decomposition across all \(R\) mask stages and proof that each discarded direction is query-irrelevant or represented by the proposed code. |
| Stationary bath zero-sum directions | The bath/common mode and stationary compensators are described in the recurrence proofs. | An explicit bath zero-sum subspace, its action through reset/final clear, and a proof of cancellation or harmlessness for every legal query. |
| Why these directions are public/cancel/harmless | Several selected modes are fixed by \(O_*\); balanced tuple sums cancel; trace correction is public and exact in the construction. | The universal statement that all omitted stationary directions fall into these harmless classes. |
| Remaining stationary mean directions | Public donor traces and stage-entrance means are named in the early-capture proof. | The exact list of independent private means and the continuous code map storing them. |
| Exact count \(R(2^R+1)\) | The claimed count is quoted in the later author-local report. | The actual counting argument: why there are precisely at most \(2^R+1\) relevant mean classes per stage, why no cross-stage dependence adds more, and why each code coordinate suffices quantitatively. |
| Route-6 asymptotics | The intended scaling \(R\asymp\log\log n\), \(K\asymp n/R\) is stated in the current checkpoint. | A proof that the count applies to the actual Route-6 history family and a careful growth calculation from a specified definition of \(R(n)\). |

## What the claimed asymptotic would imply, conditionally

If the count were proved and if \(R\asymp\log\log n\), \(K\asymp n/R\), then
\[
\frac{R(2^R+1)}K
=\frac{R^2(2^R+1)}n.
\]
For any fixed-constant interpretation of \(R\asymp\log\log n\), \(2^R\) is at most a fixed power of \(\log n\), so this ratio tends to zero. This verifies only the algebraic consequence CONDITIONAL on the proposed count. It does not prove that count or its applicability to Route 6.

## Status and review requirement

The exact stationary-complement code derivation remains missing. The file paths above provide the recovered geometry and component lemmas; they must not be cited as proof of \(q_{\rm stat}\le R(2^R+1)\). A complete derivation must define the code, prove continuity, identify every stationary parameter-response class, establish equality of codes implies the required query-relevant residual bound, and count the code coordinates with all stage and mask factors exposed.

No experiment was used. `CURRENT_THEORY.md` was not changed.
