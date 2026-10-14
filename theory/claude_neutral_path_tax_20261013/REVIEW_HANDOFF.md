# Review handoff — neutral-path tax / Householder hub construction

**Read:** PROOF.md (§§0–8), REPORT.md (A–G), CHECKS.md. **Do not read** the restricted lane
notebooks (`docs/notebooks/Codex_Research.md`, `docs/notebooks/Cursor_Research.md`). The
contract is in `../CURRENT_THEORY.md` and `../codex_holding_cost_attack_20261003/PROOF.md`
§1.

**Scope warning.** Nothing here proves or refutes the neutral-path tax or the original
problem. Candidate Theorem H is a conjecture backed by finite-n exact computations and a
derived reduced model. Lemma 1.1, Lemma 2.1 and Proposition 2.2 are claimed as proved.

## Highest-value attack points

1. **Contract fidelity.** Check each of the following.
   * Is d_F exactly the selected-source projection used in (0.1)? Does `E` mask row 0 and
     the source rows, and is `w_R/beta = 1/n`?
   * Is the one-step legal query correctly modeled? Future preactivations should lie in
     `[.25,.75]`, gates in `[sech^2(.75), sech^2(.25)] = [.5966, .9401]`, with head
     `1_n/sqrt(n)`.
   * Do the past inputs stay in `(-1/2,1/2)` (max `.447`)?
   * Is the endpoint exactly common? The argument is that balanced pairs keep `J` public.
2. **Cost accounting.** The driven coordinate-time is ≈ `(3/4) W n`. The peak width is
   ≈ `n/2` for `W` steps. Is the repository's `mT` additive coordinate-time, as in the Route
   7A ledger ("`O(nR)` coordinate-time" added to `mN`), or peak width × horizon? Theorem H
   matters only under the additive reading.
3. **Lemma 1.1(d,e) and Lemma 2.1.** These should be routine algebra; the numerical check
   agrees to `1e-15`.
4. **Prop. 2.2(iii).** Verify the exact single-write pair formula. Write gates are
   multiplicative, and the later transport is common.
5. **Reduced model (PROOF.md §5).** Are all neglected terms really `O(n^(-1/2))`? The
   candidates are:
   * the bath credit on written rows;
   * injections during the window;
   * the hole-credit spread across holes;
   * the background shift of `J` during the window;
   * the front and wake.

   Is the mass-equilibrium ceiling `sum |Delta| -> 2 sqrt(k) c_h` the correct limit? Does
   continuous-code saturation only change the rate?
6. **Decomposition (4.1).** The "hole term" is defined against a no-hole control. Check
   that the triangle inequality is applied to the same supremum functional.
7. **Dense transfer.** The repository's standard bound is claimed negligible at horizon
   `n/4`. Re-derive the constant for this horizon and credit size.

## Reproduction

    cd theory/claude_neutral_path_tax_20261013
    python -I run_checks.py          # ~80 s, all assertions must pass
    python -I scaling_run.py 64000 30 # ~10 min single thread

## Suggested verdict vocabulary

For each of Lemma 1.1, Lemma 2.1, Prop. 2.2 and the reduced-model derivation, use one of:
VERIFIED, PROOF GAP, COUNTEREXAMPLE, MIS-SCOPED. For Theorem H, use STILL CONJECTURAL,
SUPPORTED, or REFUTED (with reason).
