# Review handoff — claude_multiprobe_memory_20261014

The first round of findings (Codex P2 ×2; GPT-6 items 1–5) is answered in
[REVIEW_RESPONSE.md](REVIEW_RESPONSE.md). Please hostile-review the **repaired** text, in
this order:
1. **Theorem 4** (§7.5), conditional on Hypothesis B:
   * the soft-weighted carrying set `C(theta)` and its count `p`;
   * the release argument (Step 4): every protected position on the path of a row
     outside `C` lies on a chain started before `T - W' - Lam`;
   * the error budget `47/64 tau`;
   * the resource case split.
2. **Lemma 7.1** (U-coordinates): the claim that information moves between U-paths only
   through `X_t`, and the three-term split.
3. **Lemma 1.2'** (all legal queries): the recursion
   `A_j <= HI A_(j+1) + .1719 gamma HI^(F-j) + 4.9/sqrt(k)` and the spike bookkeeping.
4. **Cor. 3.5**: the integer block choice and the corrected constants; whether (H3) can be
   discharged for natural constructions.
5. **Theorem 2**: written out relative to PR #27; it needs PR #27's lemmas to be
   independently verified.
6. **Hypothesis B** (open): attempt a proof, e.g. via the U-path reformulation of §7.6, or
   a counterexample. A counterexample must store `>= tau/4` of the separation in the bus
   at the zeros of the state-only listing.

Do not read restricted lane notebooks. Write the review in a separate folder.
