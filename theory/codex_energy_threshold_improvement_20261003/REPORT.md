# Energy-threshold improvement

2026-10-03, Codex. NEW analytic derivation, ready for independent hostile
review. The accepted historical 7/8 theorem remains untouched and accepted.

## Result

**PROVED in the new derivation:** the frozen dense tanh family admits

    d_F = Omega(n log n)
    R_abs = O(n^(3/4) (log n)^(9/4))

at the unchanged epsilon=.001 and actual group-normalized legal late-query
contract. This strictly beats the previous energy exponent 7/8.

The explicit sufficient theorem is: for every integer n>=10^200 and
2<=F<=n^(1/20), one admissible continuous qF-ball history section has

    qF >= nF/10^7,
    ||X||2 <=4*10^7 n^(3/4) F^(9/4),
    common endpoint h=0,
    every boundary antipodal half-margin >.9997.

It starts at zero, counts every raw input, and fits the past cube (-.5,.5)^n.
Nothing is excluded as public baseline energy. These are asymptotic,
fixed-feature continuous-real-state results; they imply no practical width,
bits, VRAM, training efficiency or every-RNN claim. Full-model bounds remain
Omega_c(n^2) to O_c(n^2 log n).

**Scope change inside the allowed history class:** weights, recurrence,
source H=.4*1_l, normalization, future-query family, epsilon and endpoint
are unchanged. The old intermediate gate-deficit subbox is not preserved.
The new duration-adapted gates are proved legal directly. If one additionally
requires that narrower old gate subbox, this improvement is not a theorem
for that restriction.

## 1. Every exponent loss in the old packet

The old signal has F^-5: shared word budget F^-1, resolvent F^-1,
column selection F^-1, bounded-profile spread F^-2. Its leading signal
is proportional to delta T^2/n^(3/2). Its odd tail is bounded by
delta^3 T^4/n^(7/2). Full-width holding costs Theta(nT) squared energy.
Fixed admissible delta therefore needs T of order n^(3/4) times F factors,
giving norm exponent 7/8. This reconstructs accepted scaling; it does not
re-review the accepted theorem.

## 2. Attack A: amplitude and the signed lift

**PROVED.** The tail requires a small accumulated defect kappa=delta T/n,
not a small unscaled delta. A positive square-root lift cannot increase its
baseline indefinitely: its exceptional Householder row costs Theta(sqrt(zeta))
raw input. We pair each cycle state with its negative in EXISTING off-cycle
coordinates. The selected-memory sum is then public zero or sqrt(zeta/n).
All input coordinates stay <.5 even with large delta.

The copied off-cycle gates are not free: their full derivative effect is
bounded and included. The source and parameter accounting are unchanged.

With zeta=.15+2delta, the useful sufficient amplitude scale is

    delta_max ~ n/(T F^(3/2))

with a small constant. This is optimal in order for the stated sufficient
signal/tail ledger, not an optimality claim over all admissible histories.
Physical gates remain in (0,1); their deficit is about 1/T, while total
modulation delta T/n is tiny. Dense transfer and reset add no exponent.

## 3. Attack B: stronger joint spreading

**PROVED.** A shifted-Gaussian net lemma gives a public B with

    dist_l1(By, excluded Fourier space)>=sqrt(d)||y||2/8.

For K=ker(A) intersect [-1,1]^d, use the unique entropy-constrained optimizer

    s_j=argmax_K {128sqrt(dF)(By_j)^T s-sum_i phi(s_i)}.

It is continuous, odd, injective, coordinatewise <1, and exactly excludes
the necessary spatial modes. ONE unit qF-ball is used. On its boundary,

    max_j ||s_j||1 >=d/1024,

improving d/F^2 to order d, the maximum possible order under the coordinate
bound. No per-harmonic normalization or extra physical gate budget is used.
All harmonics still share delta/F. The signal now loses F^3, not F^5.

## 4. Complete new ledger and parameter rule

The actual permitted-query half-margin is bounded below by

    10^-8 delta T^2/(n^(3/2)F^3)
      -100delta T^2/n^2
      -delta^3 T^4/n^(7/2)
      -4*10^-9.

The second term pays node omission, Householder dressing AND the mirror
gates; the third pays all higher odd orders, mixed harmonics and chronological
noncommutation. Even orders cancel exactly on antipodes of the whole word.
The fourth is the dense-reference transfer, not an uncounted approximation.
Residual coordinates are included in the actual legal query.

Use

    T=ceil(10^14 sqrt(n)F^(9/2)),
    delta=10^-6 n/(T F^(3/2)), zeta=.15+2delta.

Leading signal >=1; odd tail <=.0002; twist <=2*10^-60 at the explicit
threshold; dense error <4*10^-9. Thus half-margin >.9997. This is the
analytic proof ledger, not a numerical certification claim.

## 5. Attack C: holding cost

**PROVED limitation of this construction:** squared energy remains Theta(nT).
The source holding cost alone has order nT. Replacing its amplitude by an
autonomous source could remove that cost but leaves active memory near zero
against bias .05, again costing Theta(nT). No n-factor saving is claimed.

**FAILED:** making the active cycle an autonomous constant bath gives a fixed
gate gap; the first failed inequality is b^(T-1)>=2/3. The long T^2 carrier
cannot be imported through such autonomous gaps.

**CONDITIONAL:** sparse or rotating active subsets could save energy, but the
first missing identity is the scalar public resolvent on each harmonic,
Q_t p_j=sum_s (b lambda_j)^s p_j. Nonuniform baseline gates destroy that
commuting identity. No claimed dimension or signal is transferred without
a replacement joint kernel. Fixed positive active fractions only save constants.

## 6. Attack D: optimized frontier

The signal minus odd tail is

    (T/sqrt(n)) [A kappa/F^3-kappa^3], A=10^-8.

Its exact maximum is 2 A^(3/2)T/(3sqrt(3n)F^(9/2)). Thus this sufficient
method needs and achieves T of order sqrt(n)F^(9/2).

| Choice | Joint dimension lower | Absolute input norm upper |
|---|---:|---:|
| F=floor(log n) | Omega(n log n) | O(n^(3/4)(log n)^(9/4)) |
| F=floor(log log n) | Omega(n log log n) | O(n^(3/4)(log log n)^(9/4)) |
| F=floor(n^beta), 0<beta<=1/20 | n^(1+beta)/(2*10^7) | 4*10^7 n^(3/4+9beta/4) |
| beta=1/45 | Omega(n^(46/45)) | O(n^(4/5)) |
| beta=1/27 | Omega(n^(28/27)) | O(n^(5/6)) |

The infimum power exponent for a positive power superlinear gain is 3/4;
every slightly larger exponent works. Exactly 3/4 in this proof has a
diverging slow factor, not a positive power gain. The general asymptotic
range F=o(n^(1/11)) follows from kernel rounding; the explicit all-width
theorem conservatively uses F<=n^(1/20).

Constructively, in the admitted F range,

    D >= c n [R_abs/(C_E n^(3/4))]^(4/9)

by selecting an integer F below that expression. This is not a matching
upper or a global Pareto optimum. Retaining the old profiles with the
balanced lift would already give exponent 3/4 but a worse F^(15/4) norm.
Spreading alone at fixed old gate amplitude only changes F factors.

## 7. Attack E: impossibility side

**No improved general impossibility exponent was proved.** The accepted
O((log n+R_abs^2)/sqrt(n)) zero-credit error still rules out positive robust
credit when R_abs=o(n^(1/4)). A proposed uniform row-leverage dilution fails:
an actual legal constant-preactivation future has

    c_(d-1)=a sech^2(1/4)[sqrt(k)-gamma_U/sqrt(k)]/sqrt(n)
          ->sech^2(1/4)/sqrt(2)>0.

Thus max_i|c_i|<=C/sqrt(n) is false. An off-cycle bound cannot charge the
moving cycle spike. A Gramian/tangent spectrum or packing count does not
prove a continuous online coordinate upper. The smallest missing upper-side
step is a joint observable quotient bound for energy-limited reachable credit
that includes overlap with that legal spike.

The updated exponent bracket is **1/4 necessary, 3/4 sufficient with slow
factors**, not a sharp threshold. No full-model theorem changed.

## 8. Failed or incomplete routes

| Route | Status | First failed or missing inequality |
|---|---|---|
| Increase delta but retain the old gate subbox | FAILED as exponent improvement | True variation remains bounded independent of n |
| Increase baseline in the old all-positive lift | FAILED | Exceptional input grows like sqrt(zeta) and leaves the past cube |
| Improve spread only, keep delta bounded | FAILED as exponent improvement | Fixed leading signal still needs T=Omega(n^(3/4)) |
| Balanced lift plus scaled delta | PROVED | All added off-cycle sensitivity errors explicitly paid |
| Entropy-constrained joint profiles | PROVED | max profile L1 >=d/1024 on the entire boundary |
| Autonomous active bath / unchanged pulse-and-coast proof | FAILED | b^(T-1)>=2/3 fails with a fixed gate gap |
| Vanishing active fraction / duty-cycle scheme | CONDITIONAL | No scalar harmonic Q_t identity for noncommuting baseline |
| Global query-row dilution upper | FAILED | Legal spike has order-one coordinate leverage |
| Universal sharper energy-width upper | CONDITIONAL | Continuous reachable query quotient not bounded |

No heuristic is inserted into the phase diagram.

## 9. Checks, evidence, and next action

checks.py independently exercises the balanced row identity, inverse-lift
input cube, rounded finite kernel, mirror injection/error, exact antipodal
chronological recurrence, entropy stationarity and Fourier exclusions.
At n=50,000, F=2, T=73, delta=20, kernel sigma_min=35.089 versus the
required 18.25. Actual odd residual on sampled columns was 2.62*10^-10,
far below its conservative majorant. These are **NUMERICAL CHECKS**, not a
theorem about a sampled robust dimension or an interval certificate.

Explicit threshold parameters at n=10^200 and 10^240 were cross-checked at
240 and 320 decimal digits, agreeing to all 65 reported digits. Ceilings
use exact integer square roots. The proof itself uses analytic bounds.
100-digit entropy stationarity checks agreed with exact excluded modes.

All mathematical checks passed. One first run failed only in Windows RAM
reporting; INITIAL_CHECK_FAILURE.txt preserves that error. The repaired run
used .75 CPU seconds, .791 wall seconds, peak RAM 49,864,704 bytes; no GPU,
training, architecture work, or large sweep. These timings are process
measurements, not an estimate of total reasoning time.

The separate final audit verified 25 historical source hashes and direct
legal-spike arithmetic. It caught and repaired a missing 1/sqrt(k) factor
in that NEW auxiliary upper-side formula; the exact correction and failed
values are preserved in AUDIT_REPAIRS.md. No main lower-bound constant or
accepted historical formula was changed. The resume insertion preserves
every prior notebook byte, including pre-existing uncommitted work.

**Next action:** independently hostile-review the new quotient-spreading,
entropy profile, balanced-lift and large-delta correction ledger before
accepting the improved threshold as a project premise. After that, the
unresolved lower-energy question is whether nT can be avoided without losing
the joint harmonic carrier. Historical evidence and reviews were preserved.
