# Prospective rebalanced 7D section experiment

2026-10-01. New owner authorization after the independent numerical audit of
the frozen failed 7D box. That box is an untouched historical control. The audit
is development evidence, not proof of face minima or a fresh holdout.

## Contract

Only independent_n4_confirmation, width4/T37/P24, identical model and base
history, fixed-h requirement, parameter-RMS/input-SD normalized metric,
permitted future preactivations [1/4,3/4]^4, continuous no-replay encoder,
epsilon=1/1000. Use the same realizable 7/8 gate lower margin. No 8D, new witness,
width, model, learning, architecture, GAS-0 or model-server operation.

## Certificate method fixed before search

Use the accepted third-order recurrence, all mixed derivative contractions,
implicit y'/y''/y''', exact fixed-h contraction, support-aware query margins and
antipodal topology criterion. The sole bound refinement is exact signed affine
combination of nominal W with history chart directions BEFORE taking absolute
values, both for W dx and for the W x interval enclosure. Direct deltaW x and
deltaW dx sensitivity injections remain unchanged. PROOF_AFFINE.md proves this
is a tighter valid majorant, not a changed model or metric. No further bound
refinement or query-gate change after results. Accepted source remains untouched;
generated local kernel.py differs only at two explicitly checked substitutions.

## Bases

Start from the historical failed candidate's exact rational normal/tangent B
and output L. Three fixed bases: unchanged; rotation of tangent axes1,2 by
+pi/16; rotation by -pi/16. For rotation O, B_t -> B_t O, L -> O^T L.
No other rotations, mode selection, optimization of basis, or history change.
Round the actual matrices to dyadic2^-128 before numerical selection. No exact
orthogonality assumption is used by interval verification. Keep normal columns.

## Numerical selection

Exactly six runs: three bases x seeds 302701,302702. Two single-thread CPU
workers maximum, each capped320 CPU seconds. Nelder-Mead on eight log amplitudes,
adaptive=True, maxfev800, xatol1e-3, fatol1e-8. Primary objective maximize the
minimum of ALL seven third-order face beta_i/epsilon using the tightened FLOAT
proxy (not a certificate). This explicitly includes mixed joint competition.

Start at the old failed tangent widths, with axis2 increased by15%.
Seed302701 uses this directly. Seed302702 multiplies each by exp(N(0,.15)) from
its fixed RNG. No favorable score is presumed. Initial normal widths are
.005,.008,.012,.02,.04,.08,.16; choose highest valid score, tie smaller normal
width, before optimizer. If none valid, use last width and preserve failures.
These seven calls count. Search guard: all raw widths <=4 and >0.

Every objective evaluation uses the FINAL rounding rules: tangent widths DOWN
to2^-20, equal normal width padded51/50 then UP to2^-20. The numerical objective
therefore includes prospective final rounding/padding. Record all attempts and
invalid proposals. No numerical result is called certified.

Select ONE highest valid score across all six runs, ties lexical job-id.
Even score<1 produces one official negative attempt. No runner-up replacement,
additional search or tuning after official failure. Freeze selected rational
widths/B/L, model/history, 192-bit-center dyadic2^-128 inverses, hashes and
selection records in a second commit BEFORE whole-box official certification.

## Fixed diagnostics, not selection feedback

For the frozen winner, numerical direct fixed-h antipodal distances on all seven
faces: nine fixed L-BFGS-B starts per face (centre, all64 corners screened to take
the four smallest, four Sobol starts seeded 303000+face), maxiter100, ftol1e-14,
gtol1e-9. Failures preserved, no replacement or amplitudes changed. This is only
a numerical lower estimate of minima, never a certificate. Complete before the
official attempt; diagnostics do not influence selection. No 8D diagnostic.

## Validity and official attempt

Before method freeze: accepted eight unit tests plus affine-cancellation,
tightened derivative containment on tiny mixed charts, deterministic rotations,
rounding, source hashes, CPU and no-history-write checks. Validity failures
repaired only before numerical scores, without weakening rules.

One candidate, fresh full mixed third-order jets/majorants at192 AND256 bits,
identical frozen rational inputs. Both precisions are run even after a valid
inequality failure, solely for agreement; runtime/implementation invalidity
stops. PASS requires domain radius<=1, hidden eta<3/4, exact hidden self-map,
nonsingular rational preconditioners, and every beta_i>epsilon at both precisions.
All beta, 2beta, centre residuals, mu, M3/6, hidden forcing/inclusion and active
constraint recorded. A pass gives continuous coordinates>=7, not7 bits or128
pairwise-separated corner states. A failing sufficient bound is not an upper
bound on true robust dimension.

## Resources and stop

CPU only, deterministic float64 selection and192/256 outward certification.
Hard40 measured CPU-minute budget; six worker caps use at most32 minutes, leaving
headroom for setup/certification. >4GiB free RAM, >2GiB disk, concurrent peak
working-set accounting target<2GiB. No GPU or external process interruption.
All raw negative attempts and historical hashes preserved.

Stop after the single official 7D result, arithmetic checks and fixed diagnostics.
If it fails, distinguish amplitude/query-range, hidden inclusion, axis competition,
third-order-majorant and method limitations. Do not conclude an intrinsic ceiling
from failed searches. No post-failure optimization, 8D or architecture work.
