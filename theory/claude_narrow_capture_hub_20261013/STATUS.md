# Status — claude_narrow_capture_hub_20261013

**Type:** author proof (theory) on the original frozen dense-tanh contract, peak width x
horizon budget. **Repository status:** PENDING INDEPENDENT REVIEW.

| Item | Status |
|---|---|
| Original strict-budget problem `D = Omega(n)`, `mT = o(n^(3/2))` (full d_F) | **OPEN** (unchanged) |
| Candidate Theorem H of PR #26 | OPEN; its schedule fails `mT` (`~ n^2/8`) |
| Constraints: Lemmas 1.1–1.3 | PROVED (author) |
| Background: Lemmas 2.1–2.5 (bath identity, floor `.025` for `m <= 5e-5 n`, gaps, protected set) | PROVED (author) |
| Theorem 1: public-schedule K-probe barrier `mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))` | PROVED (author), pending review |
| Narrow-capture / reusable-gate / J-steering redesigns of the hub (1-probe, public schedule) | REFUTED by Theorem 1 |
| Escapes not covered | `K -> infinity` probes (full d_F), code-dependent schedules |

**Exact next action.** Bound the robust dimension carried by the vector-valued channels
(credit rows of the protected rows, the n-dimensional broadcast bus) by a magnitude
argument, or construct a section exploiting them (PROOF.md §6).

## Update: Codex findings P1/P2

- P2 (truncated window): corrected by an exact equal-input-history
  argument when `W=T`.
- P1 (dense perturbation): a new auxiliary-state/credit argument in
  PROOF.md §3 bounds the joint gate-mediated and direct perturbation
  by `3.3e-7` in projected distance when `T<Tcrit`.
- The fine dimension estimate now requires
  `T<Tcrit=2.9e-10*n^(3/2)/(1+ln K)`; for `T>=Tcrit`, the
  resource lower bound follows directly using `D<=nK`.
- **Review status: repairs written; external/independent verification
  remains pending. Do not merge as a verified theorem yet.**

## Verification of the P1/P2 repairs (Claude, 2026-10-14)

See [VERIFICATION_P1_P2.md](VERIFICATION_P1_P2.md). Both repairs were re-derived from the
model equations and are **VERIFIED**:
* P2: exact equal histories when `W = T`;
* P1: the coupled state, gate and credit estimate, with `eta_d < 3.3e-7`.

An independent constant sweep, `verify_p1p2_sweep.py`, found 0 violations. The Codex
re-review of `1f25d1c` reported no major issues.

**Theorem 1 status:** PROVED (author) with verified repairs. No remaining gap is known.
Repository-level VERIFIED still needs a non-author hostile review, because Claude wrote
the original theorem.
