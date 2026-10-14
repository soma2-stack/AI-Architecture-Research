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
