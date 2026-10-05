# New-stage mathematical audit and numerical evidence

2026-10-03. Only NEW arguments were examined. The owner-accepted upper and
historical lower proofs were used as premises. Independent hostile review
of the new results has not yet occurred.

## Written internal audit

| Issue | Resolution in PROOF.md |
|---|---|
| Actual derivative versus inverse-input control | Every realized raw input is fixed for differentiation |
| Source feature | Localized H=sigma*1 is explicitly distinguished from old harmonic H=.4*1 |
| Autonomous preparation | Reference burn-in, exact landing and actual dense compensation all counted |
| One direction versus many dimensions | Pair hold proves one interval; joint spread pulse and packets prove whole balls |
| Literal isolated-row mechanism | Section 4A bounds its whole selected query signal in a stationary bath; no global optimality claim |
| Multi-pair bath coupling | Clamped public fixed point and radial contraction bound the clamp input; stationary-bath cube violation avoided |
| Endpoint | Localized pulse pairs have zero sum and exact common bath endpoint; packets reset exactly to zero |
| Cross-talk | Reference pair projections invariant; harmonic kernel estimated jointly, including rounded modes |
| Startup | Complete temporal periods cancel the exact finite startup term |
| Spatial rounding | Paid by F*pi*T^2/(2d); exact-cycle corollary needs no rounding |
| Profile saturation / injectivity | Accepted quantitative spreading lemma generalized only to another orthogonal Fourier frame; whole-ball maps remain injective |
| Physical queries | Coordinatewise future preactivations 1/4 or 3/4; flat head and original group normalization retained |
| Error coefficients | Query perturbations bounded using an upper coefficient, independently of signal's lower coefficient |
| Higher-order words | Full chronological odd tail bounded; even degrees cancel, including mixed harmonics |
| Absolute energy | Four-type center formula pays bias/source/prepare/reset; dense and section displacement norms also charged |
| Dimension upper | Counted actual state/input window; older actual sensitivity is erased only after a legal-query error bound |
| Full model versus selected feature | New lower sections do not multiply source columns or close the accepted full-model gap |
| Local radius versus absolute norm | No local perturbation radius is substituted for total input norm |

## Numerical scope

Run `checks.py` with a single CPU thread. All numerical findings below are
**NUMERICAL EVIDENCE**, not independent mathematical verification.

The final run has 32 successful checks: 14 scalar/rational or exponent
certificates and 18 finite packet diagnostics. It also records 64 scalar
schedule samples and 12 reference localized clamp/pulse samples.

### Finite packet identities

| n | T | F | Rounded spatial modes | Minimum eigenvalue of symmetric real kernel | Startup residual |
|---|---|---|---|---|---|
| 50,000 | 99 | 2 | 126, 253 | 49.2737680 (>T/4) | 1.8831e-15 |
| 65,600 | 73 | 2 | 225, 449 | 36.4285557 (>T/4) | 2.3285e-15 |

The physical first-order versus ideal-column discrepancies are approximately
1.2850e-7 and 4.1603e-8; both are below the analytic twist majorants. The
degree-3 and degree-5 coefficients are computed directly to avoid subtracting
large sensitivities. Direct plus/minus subtraction has a roughly 1e-12
roundoff error, larger than the tiny theoretical tail here. Its diagnostic
uses an explicitly recorded 1e-11 roundoff allowance and supplies no tail
certificate. All-order control comes from the written induction.

The random projected profiles in these diagnostics are not a sample-based
proof of the spreading lemma. The data do not certify dimension at these n.

### Reference multi-pair schedules

At n=8192, public zero-input preparation is followed by a clamp and ONE
sampled boundary pulse. The reference full raw-input energy includes the
pulse and reset; preparation costs zero input in R0. The stored dense
compensation majorant is tiny and separate. The rigorous s/n allowance is
not met by these small-width samples; they are guidance, not theorem instances.

| Pairs s | Hold T | Full reference norm | Sampled fixed-query half-margin | Margin after n/2 zero-input steps |
|---|---|---|---|---|
| 16 | 4096 | 2.721884 | .000564874 | 6.4932e-6 |
| 16 | 20480 | 2.721943 | .001188828 | 1.3665e-5 |
| 64 | 10240 | 5.443844 | .001891260 | 2.0428e-5 |
| 256 | 5120 | 10.888256 | .002598677 | 2.1769e-5 |

The endpoint differences for the sampled antipodes are zero at floating
precision, and all sampled maximum raw-input coordinates are below .406.
These rows show hold saturation and loss during autonomous spacing. They
prove no sphere-wide minimum, joint dimension, asymptotic exponent, or dense
finite-width witness. Some small-width margins exceeding epsilon at small
energy do not contradict the accepted asymptotic impossibility theorem.

### Scalar one-channel schedule

The diagnostic uses the limiting reference bath mu=sigma=tanh(.05), explicitly
not an actual finite-width fixed point. Vary n from 10^4 to 10^10, near-critical
depth z in {0,.05,.5,1}, and duration kappa in {.1,.3,1,4}. The leading
constant-hold formulas give:

* mu_infty: .04995837496.
* Holding drive B_mu,infty: .00004162504.
* Chosen-query half-margin ceiling: .00427858382.
* Epsilon-level duration coefficient: .266210505.
* Leading absolute-norm coefficient: .00003037262*sqrt(n).

These constants optimize only the stated leading constant-hold formula.
They do not prove a globally optimal depth, ramp, bath policy, or history.

## Resource record

Three bounded diagnostic runs were used while adding roundoff-aware and
multi-pair checks. Aggregate measured diagnostic CPU: 25.734375 seconds;
aggregate measured wall time: 25.9945242 seconds. Final run CPU: 15.0625
seconds; wall: 15.2612578 seconds; peak process working set: 57,483,264 bytes
(approximately 54.82 MiB). One CPU thread, zero GPU/CUDA use, no training or
background service. Startup and administrative reading/writing are excluded.
The first run's peak-memory capture was unavailable and was repaired for
subsequent runs; its reported zero is not asserted to mean zero memory.

## Remaining verification targets

Independent hostile review should focus on NEW sections 4A, 5-6, and 7-9A:
the isolated-row backward-adjoint estimate, clamped-bath input bound, rounded
finite packet kernel, whole-ball injectivity, physical L1 conversion and full
error/energy ledger. The accepted absolute-energy upper is not a review target.
