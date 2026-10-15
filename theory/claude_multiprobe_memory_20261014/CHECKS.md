# Checks — claude_multiprobe_memory_20261014

## Final cross-PR independent audit (2026-10-15)

The current [audit](../codex_cross_pr_final_audit_20261015/AUDIT.md) and
[handoff](../codex_cross_pr_final_audit_20261015/HANDOFF.md) supersede prior unqualified
scope/optimality comments. Historical numerical records below are preserved.

```powershell
python -I theory/codex_cross_pr_final_audit_20261015/checks.py
python -I theory/codex_cross_pr_final_audit_20261015/regressions.py --pr27-root PATH_TO_PR27_CHECKOUT
```

New checks: exact rational gate/constant/ceiling certificates, 48 adversarial query
cases, 480 strict integer choices, 2560 worst-sign weighted-profile cases, 100 release
schedules including never-protected paths, and a two-bus-channel identity regression.
Prior independent foundation/repair suites also pass, including the infinite-tail
bath certificate. Their historical outputs are not overwritten. Fresh and regression
results are in the separate audit folder; no author implementation is imported.
Runtime is about .2 seconds plus 7.5 seconds, CPU only, one thread.

The exact 1/1700 correction preserves Theorem 2's 1.9e-10. Theorem 4's complete
47tau/64 ledger and 4.7e-11 resource coefficient remain valid **conditional on B**,
in the explicitly selected group and resource range 2N3<=D<=n. No B proof was attempted.

Two scripts, both CPU, each under a minute, float64. They verify **exact identities and
finite samples only**. The asymptotic theorems rest on the proofs.

## `python -I exp_identities.py` (torch autograd) → `exp_identities_result.json`

| Check | n, T | Result |
|---|---|---|
| Credit-matrix recursion (0.1) vs autograd, actual `R = R0 + H`, `||H|| = 4e-8/n^2` | 96, 25 / 160, 40 | rel. err. `5.6e-16` / `1.1e-15` |
| One-step legal query gradient `sigma sqrt(l) nu^T B_T` + direct term vs autograd | same | rel. err. `8.1e-16` / `1.6e-15` |
| Gather identity `O^T 1_k = sqrt(k) e_(d-1) + gamma e_0 - (gamma/sqrt k) 1_k` | k = 48 / 80 | `1.8e-15` / `1.2e-14` |
| Readout weights (Lemma 1.2), inline check in the session | k = 50, 400, 2000 | formula err. `<= 1.2e-13`; `max |nu_i| <= .339` off `{0, d-1}`; `nu_(d-1)/sqrt k >= .739` |

## `python -I exp_bus_checks.py` (numpy) → `exp_bus_checks_result.json` (added 2026-10-14)

| Check | Sizes | Result |
|---|---|---|
| A. Local skeleton (3.0): `O x = S x + 1 J(x) + (gamma/sqrt k) Sum(x) e_1`, `x_0 = 0`; column `d-1` of `S` | k = 50, 400 | err `<= 6.3e-15`; column exactly 0 |
| B. Row 0: `nu_0 = a g_0`; reference row-0 credit | n = 200, 800 | `<= 5.3e-15`; `<= 1.4e-15` (rounding) |
| C. U-coordinate gating formula (1.2), rows `>= 1` | k = 50, 400 | `<= 2.3e-15` |
| D. U-coordinate credit dynamics `Y_t = U G_t U (a P Y_(t-1) + c_t U E)`; `u^T Y = 0` | k = 50, 300 | `<= 4.2e-15`; `<= 8e-17` |
| E. Multi-step legal readout weights, `F <= 40`, random and adversarially correlated future gates | n = 800, 4000 | max non-exceptional weight `.21` / `.19` (bound proved: `1.2`) |
| F. Lemma 7.1(c): three-term split of `X_t V_t` (corrected leak coefficient `gamma/sqrt k`); capture coefficient; `Y(0)` update | k = 50, 400, 2000 | `<= 2.7e-15`; `<= 1e-17`; `<= 3.1e-15` |

Check F was added after my own first draft of §7 used the wrong leak coefficient
(`gamma/k`); the draft was corrected before commit.

The original session spot-checks were not independent certification; their rounded
constants are superseded by the repair below. The author tables above are historical
finite diagnostics for the masked E group, not the omitted unmasked row-0 direction.

## Independent repair verification

Run from the repository root:

```powershell
python -I theory/codex_pr28_repair_verification_20261014/checks.py
```

The script imports no author code and writes only its separate `independent_results.json`.
The complete mathematical derivations and scope are in
[VERIFICATION.md](../codex_pr28_repair_verification_20261014/VERIFICATION.md).

| Check | Result |
|---|---|
| Correct exact spike cutoff; old n=2^1600 counterexample | F_s=8959; old F=8954 spike now listed; corrected tail norm below 1 |
| Short-query recurrence and Householder correction | Non-spike majorant below 1.2; long queries use the global norm cap |
| Source initialization | c_1=Delta c_1=0; later near-one estimate and all-timestep upper cap treated separately |
| 109 independently implemented exact-structure float64 checks | Maximum error <8e-15 |
| 36 adversarial future-query samples | No new finite counterexample; samples are diagnostic |
| Integer block choices / weighted profiles | 700 / 250 checks pass |
| Two-history release schedules, including never-protected paths | 300 checks pass |
| Corrected error ledger | <=(47/64)tau+2e-7 sqrt(n)<tau |
| Corrected resource constants and ceilings | All conservative majorants pass; conversion explicitly uses D<=n |

Runtime is approximately one second on CPU; no training or GPU. Hypothesis B is **OPEN**
and was not tested or proved as a conjecture during this repair.
