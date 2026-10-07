# Independent Review Handoff

## Claim under review

The author derivation claims that zero-initial strong balanced captures with \(b\approx.0025\), donors low at capture, and at least \(\lceil100/p\rceil\) ordinary steps between captures satisfy
\[
\Lambda\le2\sqrt K\,N,\qquad f(R)=O(1).
\]
It includes the complete chronological bath/front recurrence. Close captures and unaccounted dense perturbations are outside scope. The index status is PENDING REVIEW, not VERIFIED.

## Claims to verify

1. The cone decomposition (6)â€“(7) exactly represents the stated weighted absolute-state potential, and its output term is exactly \(|S_w|\).
2. Cone invariance and ordinary dissipation (8)â€“(11) hold for arbitrary legal donor gates and the inherited bath-deficit premise.
3. The survivor group mean gate at capture is \(\bar g\); verify signs and coefficients in (13)â€“(16), including exact \(A-Q\) cancellation with the Walsh ledger.
4. Independently calculate .0035 from the gate bounds; check the bath recurrence (17), constants .0007 and .021p, and integrated output \(Z_0/(40p)\).
5. Audit signed packet splitting, preservation of the represented core state, its compatibility with the Walsh ledger, disjoint payment windows, and the final truncated-window terminal-storage payment.
6. Verify that the canonical crossing charge is dominated by the packet crossing charge.
7. Check the complete global front chronology (22), including first-front and terminal contributions, the \(4\cdot10^6\) front sum, \(C_\rho=2\cdot10^{10}\), and the small-gain premise \(np\ge160C_\rho\).
8. Verify (24)â€“(25), including the .15 capture-payment and .05 front margins.
9. Check the probe-bank conversion, its induced \(\ell_1\) norm below 1.84, and final constant 2.
10. Confirm that the intended legal Route-6 construction supplies the spacing, bath interval, and cone premises at every charged step.

## Repository dependencies

- Exact group recurrence, group weights, source normalization, and witness/probe identities: theory/codex_frontier_invention_20261006/PROOF.md, especially sections 3 and 6.
- Walsh capture transfer and protected capture convention: theory/codex_linear_dimension_frontier_20261006/PROOF.md, capture and protected-row sections.
- Exact chronological bath/front recurrence: theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md, equations (10)â€“(14).
- Probe-basis identity: theory/codex_frontier_invention_20261006/PROOF.md, section 3.

## Requested verdict

Please return separate decisions:

- Cone decomposition and ordinary dissipation: VERIFIED / PARTIAL / REFUTED / OPEN
- Capture identity and Walsh transfer: VERIFIED / PARTIAL / REFUTED / OPEN
- Bath payment for separated captures: VERIFIED / PARTIAL / REFUTED / OPEN
- Front small-gain: VERIFIED / PARTIAL / REFUTED / OPEN
- Final Lambda bound in stated scope: VERIFIED / PARTIAL / REFUTED / OPEN

Do not extend the verdict to close-capture histories or dense perturbations without a separate proof.\n