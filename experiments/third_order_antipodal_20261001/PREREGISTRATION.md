# Third-order antipodal certificate: one frozen 6D test

New experiment authorized by the owner on 2026-10-01. No architecture, learning,
new history, wider model or additional endpoint is tested. Stage-1 archive:
commit 1e1b141, following documentation/archive commit 357765a and review b7e1e45.
Prior proxy evidence is development data, not a result of this preregistration.

## Primary question and candidate selection (fixed before official certification)

Can independent width-4 confirmation, horizon37, certify at least six
epsilon-essential continuous memory coordinates at epsilon=1/1000?

Select exactly one candidate among the already archived stage2_proxy outputs
for this endpoint, r=6: highest archived numerical min-beta3 score; ties use
lexicographic filename order. This chooses query_r6_s2 (score1.657420261...).
Do not regenerate an optimization, change the selected history, or replace a
failed candidate. No runner-up certification is authorized in this protocol.

Reconstruct the numerical query-SVD B,L with the original Endpoint code once,
rationalize these to dyadic2^-128, and freeze the actual matrices. Numerical
orthogonality is not assumed by the certificate. Freeze tangent amplitudes by
rounding the selected proxy values DOWN to2^-20. Set the equal normal amplitude
to ceil((51/50)*proxy_ah*2^20)/2^20: a fixed2% rounding-safety allowance declared
now, not a response to a certificate failure. Freeze the exact center rational
preconditioners K_h,K from192-bit interval endpoint jets,100-decimal midpoint
inversion and dyadic2^-128 rounding. No curvature/face result is inspected while
forming this setup. Store all actual inputs and hashes in candidate.json/FROZEN.json.

## Unchanged contract

Same independent recurrence h'=tanh(Rh+Wx+b), diagonal R; same original
parameters/history, support and P=24, n=4. Same parameter-group RMS normalization,
input SD=sqrt(3/32), fixed head q=ones/sqrt(n), beta=max(1,||R||F), permitted
future preactivations[1/4,3/4]^n, support-aware7/8 gate. Same raw local domain:
each history coordinate within +/-1 of the frozen center. No epsilon tuning.

## Rigorous method

1. Regenerate interval endpoint jets and whole simultaneous box h/S Hessian
   majorants using the accepted arithmetic. Verify exact hidden-section
   contraction <3/4, equal normal widths, nonsingular K_h and self-mapping.
2. Extend the majorant recurrence with full third derivatives in ALL chart
   coordinates, including normal-normal-normal and every mixed combination.
   Use dyadic interval tanh/gates and f''''=8h(1-h^2)(2-3h^2); all positive
   tensor algebra is explicitly rounded upward, with no BLAS reassociation.
3. Bound implicit y', y'', y''' and compose the full third derivative of
   s(y(t),t), including s_y y''' and all three s''[y'',y'] terms.
4. Let Phi(z)=A^-1 K(Psi(Az)-Psi(0)); bound its center residual row e0_i and
   whole-cube cubic sum M3_i. Use

       beta3_i = mu_tilde_i*(1-e0_i-M3_i/6).

   For every boundary antipode, some |z_i|=1 and query distance >=2beta3_i.
   Every beta3_i must exceed1/1000. Apply the accepted Borsuk-Ulam argument to
   continuous history encoders. Do NOT infer all2^6 corner-pair separation.
5. Independently regenerate at256bits with the SAME rational B,L,K,K_h and
   amplitudes. Require every inequality again, record all outward differences.

## Validity checks before official run

Development tests use tiny deterministic models/charts, not the primary box's
outcome: fourth derivative identity; third-order chain/product rules; endpoint
RTRL/BPTT equivalence; exact constant linear/polynomial controls; mixed tensor
symmetry/coverage; first/second majorants matching accepted machinery; numerical
autodiff third derivatives dominated at declared tiny chart points; exact
query-margin arithmetic; parameter freeze; CPU execution; hashing/accounting.
Numerical autodiff checks are bug detectors, not certificates. No threshold or
candidate changes based on them. Ordinary code bugs can be repaired on development
checks before final method freeze. All such repairs must be logged.

## Freeze and run order

Write protocol/config and candidate, implement and pass development tests, then
hash/commit the entire executable setup BEFORE official curvature/face evaluation.
The final code freeze and commit identify the method used. Any later code change
invalidates that attempted official result; preserve it and STOP for review.

## Stops and budget

CPU only, one worker/BLAS thread, no model server/GPU. Hard official+development
budget20 measuredCPU minutes, conservative RAM cap2GiB; healthy memory/disk
required. Stop on any mathematical gap, invalid reference, nonfinite value,
hash mismatch, hidden-section failure, beta3 failure, or exhausted budget.
Do not retune or try another candidate. Stop immediately after valid6D success
and256-bit regeneration. No r7 test or secondary epsilon sweep.

## Possible conclusions

- 6D RIGOROUSLY CERTIFIED (then independent review required).
- THIRD-ORDER METHOD FAILS ON FROZEN CANDIDATE (not a dimension upper bound).
- MATHEMATICAL GAP FOUND / IMPLEMENTATION INVALID (identify exact failed step).

Results remain lower bounds on continuous encoding coordinates under the existing
worst-case, late-query, uniform absolute-error contract. No practical hardware,
capability, exact maximum dimension or architecture conclusion follows.
