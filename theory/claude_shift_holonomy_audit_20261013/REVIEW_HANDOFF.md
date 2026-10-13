# Completed independent review: shift-holonomy audit

Independent hostile review is complete. See [Codex review PR #25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25).

The reviewer verified Lemmas 5.1–5.3 and Theorem 5.4 in their stated QSR scope, and the projected-gradient inequality in Corollary 5.6 for the augmented source model. The review found the Corollary 5.5 assertion `floor(n'/1001) >= n/1002` false at `n=1,000,999`; this record now uses the proved correction `D >= n/1004`. The review also narrowed the changing-support input accounting and normalization claims, classified the tanh equivalence as unproved numerical evidence, and retained the neutral-path tax as a conjecture. The original frozen dense-tanh problem remains OPEN.

The review respected the notebook restrictions. `AGENTS.md` remains untouched. The original contract is summarized in `../CURRENT_THEORY.md`.

## Findings retained

1. **Lemma 5.1 — VERIFIED.** Block placement, transport exponents, and the prefix sum are correct. The independent checker propagated forward tangents in rational arithmetic.
2. **Lemma 5.2 — VERIFIED in scope.** Each legal future input realizes the adjoint block paired with its write. This is a QSR query result, not a realization under the original tanh future contract.
3. **Lemma 5.3 — VERIFIED.** Paley–Zygmund, Hoeffding, both covering arguments, operator-norm bound, transfer count, and existence probability check. The theorem gives existence; an arbitrary random draw is not certified.
4. **Theorem 5.4 — VERIFIED in scope.** Its sign query and worst-case window subtraction give uniform separation for every boundary point under the theorem's QSR assumptions.
5. **Corollary 5.5 — corrected.** `D=floor(n'/1001)>=n/1002` fails at `n=1,000,999`. The corrected claim `D>=n/1004` holds for its stated `n>=10^6` range. The asymptotic result is unchanged.
6. **Corollary 5.6 — VERIFIED in augmented-model scope.** The full recurrent-group RMS ratio, projected feature gradient, and preparation term check. The source preparation changes addressed support at public times; `m` bounds simultaneously addressed coordinates, not a fixed m-coordinate input port. The result uses the declared `Q_ne` and projected feature metric, not the complete original model contract or every parameter group.
7. **Lemma 8.1 — VERIFIED locally.** It gives an unweighted trace deficit in its reference/dense-perturbation scope. It does not give credit-weighted contraction or establish the tax conjecture.
8. **Tanh ablation — PROOF GAP for architectural equivalence.** The idealized adjoints are not proved realizable, and finite samples do not establish uniform separation over the sphere. Structural prior art does not replace this quantitative proof.
9. **Neutral-path tax — CONJECTURE.** No change to that status.

## Reproduction

The author's diagnostic checker remains available. It rewrites `checks_result.json`; run it
in a disposable checkout if you want to preserve the committed output:

```powershell
cd theory/claude_shift_holonomy_audit_20261013
python -I checks.py
```

It requires NumPy and Torch on CPU. The independent checker imports no author code and is
in PR #25. To reproduce it without switching this PR #24 checkout, make a separate
worktree at the reviewed PR #25 head and run the checker from the repository root:

```powershell
git worktree add --detach ..\pr24-hostile-review 50bb5ffabf33b28099238acb6440cb1a349079e3
cd ..\pr24-hostile-review
python -I theory/codex_pr24_hostile_review_20261013/independent_checks.py
```

The recorded independent results and detailed scope are in [PR #25](https://github.com/soma2-stack/AI-Architecture-Research/pull/25). No training was started.
