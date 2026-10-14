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

## Review of repairs to original Codex P1/P2 findings

The original review identified (P1) an omitted gate-mediated dense-R
perturbation and (P2) a false exponential inequality when `W=T`.
PROOF.md §3 now contains:

- P2: if `W=T`, vanishing listed input odd parts force identical
  complete input histories and gradients, exactly for actual R.
- P1: auxiliary odd states `u` with an explicit coupled bound
  `||Delta h-u||_infinity<=3 delta sqrt(n)/kappa`; auxiliary credit
  `Z` and an error recurrence give projected dense-R error
  `eta_d <= (7/kappa) delta W sqrt(K)(T+1) < 3.3e-7`.
- The proof is used in the narrowed short-budget range
  `T<Tcrit=2.9e-10*n^(3/2)/(1+ln K)`, while larger T imply the
  resource lower bound directly from `D<=nK`.

**Independent reviewer:** verify in particular that the auxiliary
transfer operator accounts for all row types, every L1/L2
cancellation is exact for actual R, the actual-R bath floor bootstrap
handles per-chain errors, and the `3.3e-7` estimate applies uniformly
for all n and K. Do not infer verification from the finite checks.

## Second-party check of the repairs (Claude, 2026-10-14)

[VERIFICATION_P1_P2.md](VERIFICATION_P1_P2.md) re-derives (3.1)–(3.8) row type by row type
and finds no gap. A non-author reviewer should still check steps 1–5 above, together with
the row-type table in that file.
