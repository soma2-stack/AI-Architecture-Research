# Status — claude_neutral_path_tax_20261013

**Type:** research on the original frozen dense-tanh contract (d_F, epsilon = .001, legal
queries). **Repository status:** PENDING INDEPENDENT REVIEW.

| Item | Status |
|---|---|
| Original strict-budget problem `D = Ω(n)`, `mT = o(n^(3/2))` | **OPEN** (unchanged); candidate positive resolution under additive coordinate-time |
| Neutral-path tax conjecture at the contract threshold | **OPEN**, with strong numerical/model evidence of falsity |
| "One held neutral path per query-visible direction" principle | **REFUTED** [PROVED, Prop. 2.2] |
| Lemma 8.1 as a tax proof route | **INSUFFICIENT** [PROVED] |
| Householder broadcast/concentration identities | **PROVED** (Lemma 1.1) |
| Hub term ≈ .0025 (vertex) / .0024 (code), n-independent | **[NUMERICAL]** for n = 8k–128k; **[MODEL]** reduced recursion within ≈10% |
| Candidate Theorem H (D = Θ(n), C ≤ 60n, d_F > .002) | **[CONJECTURE]**; margin ≈ 1.2–1.35× |

**Exact next action.** Prove the held-window equilibrium bound: PROOF.md §7, obligations
2–4, with explicit constants. The total relative error must stay under ≈15%.
