# Report — the remaining memory channels (Steps 3, 3.5, 3.6, 3.7)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Audits:** the three earlier Codex audits (`ac759bb`, `c48640d`, `18f8005`) and the independent
  Step 3.7 audit are preserved verbatim; none was edited.
* **Verification:** Step 3.7 was audited against source commit
  `1a8203e2ced0a68017f27e507c1a92c4fb9c91ad`; its audit and supporting records are in
  `theory/codex_pr37_step37_audit_20261021/`.

## Step 3.7: repairs (PROOF.md §R3; `repairs3_check.py`)

| Claim | Outcome |
|---|---|
| (10.6) unweighted-tail bound and Conjecture 10.5 | **REFUTED**, withdrawn. Exact scalar witness `200000399/79992000`. Legal zero-input family: ratio `6.533` at `n = 2^18`, `T = 5300` (limit `6.613`; Codex `6.611` at `n = 1e8`). Unweighted tails count forcing that every bath row has forgotten; the filtered content stays `~.5` of the scale. |
| §10.8 tail-listing route | withdrawn as written: it misses the kernel term (now Prop. 11.7) |
| Prop. 10.3 | frozen bath stated (necessary); `<=` at `F^ext = 0`; source specialisation for the source-leak forcing only |
| Theorem 7.5' | `.660504` (not `.6605`). Witness: initial mean plus `Acq` = total. Displayed bound `2.2762e-8`; the recorded `1.8226e-8` is the older bound. |
| Cor. 10.2 | `1 <= W <= L`, `<=` at `W = L`; explicit initial-vector norm |
| Prop. 10.4, Lemma 7.2, `phase2_check` note | first-step boundary; `a' s_t/2`; nominal `P` capped at 3000 |

## Step 3.7: new mathematics (PROOF.md §11; independent Codex audit)

* **Theorem 11.3 — PASS in scope.** The exact variation bound includes initial and capture terms.
  Its valid scope is eps P <= 1, 0 <= r <= 1, and a nonnegative bath reference strictly below
  one; anti-holes, signed feedback, and a nonautonomous bath are allowed within those conditions.
  The literal negative-bath extension is **FAIL** and outside the theorem.
* **Corollary 11.5 — PARTIAL.** The constant-forcing ceiling requires both constant Fext and a
  constant bath. The general signed-monotone factor-two claim is **FAIL**: phi=(-1,+1) has
  V(phi)=3 > 2 max|phi|=2. Factor two holds for fixed-sign monotone sequences; the general factor
  is three.
* **Proposition 11.6 — PARTIAL, operator-level.** Finite operator gains pass; the claimed universal
  constant-times-stationary-ceiling bound is **FAIL** at operator level. Near-attainment requires joint hierarchy,
  settling-time, and system-size limits. The published .9 scaled largest group and rho_N=20 give
  total scaled population about .9474, above physical off-cycle capacity about .5; rescaling the
  largest group to .4 fits and retains similar finite gains. The conditional cost argument is not a
  universal resource ceiling.
* **Proposition 11.7 — PASS in scope.** The exact split and kernel bound use a common query. Distinct
  queries require an additional terminal term. A useful cost-dependent bound on the kernel remains
  **OPEN**.
* **Legal staircase — PARTIAL.** The earlier pulse schedule (F) failed, but an independent
  matched-forcing legal construction gives population-L1 gains of 2.315760x / 3.044170x at two /
  three stages, and legal retainer-readout gains of 2.011900x / 2.533122x. For the three-stage
  n=1e12 run, the selected full-column response is 69.4441 but normalizes to only 2.4532e-12.
  These are finite numerical results, not a robust dimension theorem.

## Meaning for the original target

* Per-history response is bounded by normalized forcing variation plus explicit initial and
  capture terms, under the audited positive-bath assumptions.
* Across histories, the remaining terms include forcing variation and the kernel difference. Neither
  has a useful bound in terms of legal resource cost here.
* No dimension theorem or full-metric bound is established. **The original problem remains OPEN.**

## Earlier steps (unchanged in substance)

* *Step 3:* the ledger, Theorem M_F, Lemma 1.3, Lemma D, Prop. R1, Lemma R.
* *Step 3.5:* staggered resets give a finite-`n` constant gain.
* *Step 3.6:* Theorem 7.5', Theorem 10.1, Cor. 10.2, Prop. 10.3 (frozen bath), Prop. 10.4, and
  the contrast-pump experiment (saturates).

## Step 3.7 closeout

The independent audit is preserved at theory/codex_pr37_step37_audit_20261021/AUDIT.md. Its raw
results and verification manifest are alongside the report. The cost-dependent kernel bound,
variation-versus-cost reduction, and robust dimension result remain open. No further experiments are
included in this update.
