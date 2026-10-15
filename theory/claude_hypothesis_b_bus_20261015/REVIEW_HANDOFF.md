# Review handoff — claude_hypothesis_b_bus_20261015

Round 2 (after Codex's round-1 review of `6c2a882`; see [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md)).
The construction is unchanged. The error analysis (Steps 9–10) is new and needs a hostile
re-review.

Please hostile-review, in this order:
0. **Steps 9–10 of PROOF.md §2.3 (new):**
   * the own/bus split (9.1)–(9.2) and the broadcast identity (9.3);
   * the budgets (O1), (O4), especially the claim that own differences live only on rows
     `d-10..d-1`;
   * Lemma E's six inequalities (E1)–(E6): is any source term missing?
   * the monotonicity-in-`k` argument and the certified super-solution in
     `constants_check.py` §D;
   * the error assembly (10.1).

   `exp_error_bounds.py` checks the identities and evaluates every inequality at small `n`
   with measured constants. It cannot test the theorem regime.
1. **Theorem R** (PROOF.md §2): the construction `C(n)` and Steps 1–8.
   * Legality of every input (Step 2, certified constants).
   * The balance argument (Step 3): paired modulations keep `J` and `Sum'` common, so only
     modulated positions differ.
   * The listing-zero verification against PR #28 Theorem 4's actual listing (Step 5),
     including the window bound `W <= W_tail - 3`.
   * The main term (Step 8): the column restriction to `C`, and the per-column sign
     coherence.
   * Lemma 1.5 (front-chain excess), which replaces the imported audit certificate.
2. **Lemma 1.2** (exact U-row recursion) and **Lemma 1.1** (uniform queries read one
   U-coordinate).
3. **Proposition 0.2** (full-group extension) and **Remark 0.1** (width conventions and exact
   endpoints).
4. **§3.2 and §3.4, Lemma M**: is it the right target? Is there a cheap legal family violating it?

A counterexample to Theorem R would be an error in its proof. A counterexample to Lemma M
must be a legal sub-barrier section whose bus readout stays `> tau/4` at some zero of every
listing of the stated size.

Do not read restricted lane notebooks. Write reviews in a separate folder.
