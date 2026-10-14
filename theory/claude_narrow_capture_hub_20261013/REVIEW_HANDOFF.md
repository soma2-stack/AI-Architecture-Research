# Review handoff — claude_narrow_capture_hub_20261013

**Question for an independent hostile reviewer.** Is Theorem 1 (PROOF.md §3) correct? It
states: every public-schedule, K-probe-certified robust section of the original model
satisfies `mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))` (`n >= 10^8`).

**Highest-risk steps (please attack these first):**
1. Lemma 2.2 / 2.5: every undriven memory row is an `F_t`-iterate of a chain start; at most
   `m+1` rows per age; the protected set is public and has size `<= (m+1)(Lam+1)`.
2. Lemma 2.4: the induction for the bath floor. In particular, the claim that negative
   excess mass never threatens the floor.
3. Claim 1 (§3): the listed scalars (L1)–(L3) really cut every path by which odd
   information can enter a protected row, including row 1, source rows and row 0.
4. Claim 2 and the remainder: the injectivity of `j -> pred j`, the slope bound, and the
   `W` choice (`e^(kappa W) >= Q^2`).
5. The use of repository bound (20) (`T > .001 sqrt n`) and of the adjoint-norm bound
   `<= (sigma sqrt l/n)||Delta B_T||_F` for all legal future queries.

**Do not read:** restricted lane notebooks (`Codex_Research.md`, `Cursor_Research.md`).
**Do not edit** this folder; write a separate review folder.
**Expected output:** VERIFIED / GAP / COUNTEREXAMPLE for each of steps 1–5, with explicit
constants where a gap is found.
