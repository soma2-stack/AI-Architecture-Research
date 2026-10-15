# Review handoff — claude_hypothesis_b_bus_20261015

Please hostile-review, in this order:
1. **Theorem R** (PROOF.md §2): the construction `C(n)` and Steps 1–9.
   * Legality of every input (Step 2, certified constants).
   * The balance argument (Step 3): paired modulations keep `J` and `Sum'` common, so only
     modulated positions differ.
   * The listing-zero verification against PR #28 Theorem 4's actual listing (Step 5),
     including the window bound `W <= W_tail - 3`.
   * The main term (Step 8), and especially the error bookkeeping of Step 9: leaks,
     including the folded self-leak and the front leak; the `kappa` differences; the
     w-injection; the init term.
2. **Lemma 1.2** (exact U-row recursion) and **Lemma 1.1** (uniform queries read one
   U-coordinate).
3. **Proposition 0.2** (full-group extension) and **Remark 0.1** (width conventions and exact
   endpoints).
4. **§3.2 Lemma M**: is it the right target? Is there a cheap legal family violating it?

A counterexample to Theorem R would be an error in its proof. A counterexample to Lemma M
must be a legal sub-barrier section whose bus readout stays `> tau/4` at some zero of every
listing of the stated size.

Do not read restricted lane notebooks. Write reviews in a separate folder.
