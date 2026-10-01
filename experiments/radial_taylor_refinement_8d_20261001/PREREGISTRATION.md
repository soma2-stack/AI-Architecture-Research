# Prospective 8D third-order margin refinement

Only the frozen accepted independent width-4 confirmation 8D section is
officially certified. Candidate SHA c83a242f6de829542fcf57c7b98beae6fc90be079d479b169a624e832f27cd0c
is byte-copied unchanged. Endpoint/T37/P24, axes, amplitudes, epsilon 1/1000,
normalization, scalar-head query family, exact fixed-h, and continuous no-replay
encoder contract unchanged. No new witness, rigorous 9D, 10D or architecture.

## Frozen refinement (three components)

1. Replace natural interval products for tanh derivatives by maxima of their
   explicit polynomials in h=tanh(a). Check endpoints and ALL real critical
   points using outward radical enclosures. Take the minimum of this bound
   and the independently valid reviewed natural interval bound. All recurrence
   derivatives/parameter injections and upward tensor arithmetic unchanged.
2. For the last-input normal chart, substitute the exact last-input solution
   AFTER constructing the frozen-parameter RTRL sensitivity. This gives an
   exact affine combination of h_(T-1) and S_(T-1) for each selected output.
   Combine signed coefficients before absolute bounds. This eliminates only
   cancelling implicit-section terms, not any physical parameter sensitivity.
3. Integrate the odd third-order remainder over eight fixed radial intervals
   [0,1/8],...,[7/8,1]. Bound each interval using its upper-radius prefix box,
   then exact rational weights. See PROOF.md. No adaptive subdivision.

Regenerate the ORIGINAL whole-box certificate at 192 and 256 bits as control.
This proves unchanged hidden inclusion; compare complete arrays with archived
ones. Compute separate elimination-only, elimination+sharp-gates whole-box,
and final radially integrated penalties to attribute recovered slack.
Never interpret small nested boxes as changed candidate amplitudes.

## Success and stop (frozen before official values)

All eight final face bounds must strictly exceed 2epsilon at BOTH precisions.
Substantial success additionally requires the weakest absolute slack to be
at least DOUBLE the accepted weakest slack, using exact archived rational
values. This is approximately >=4.89061058% relative slack, versus 2.44530529%.
No choice of success threshold after observing results. If this fails, stop:
no 9D screen, no alternate candidate, no more bins or retuning.

Stop on source/history mutation, invalid hidden section, nonfinite derivatives,
inconsistent arithmetic, precision disagreement, or exhausted budget. Record
failures without deleting them. New method needs independent review even on PASS.

## Conditional cheap numerical 9D screen (ONLY after substantial success)

Same central endpoint/metric/query/epsilon; query_svd first nine tangent
directions from the already frozen bases.npz. Four existing last-input normals.
No history search or unrelated bases. Two deterministic balanced starts with
linear beta/epsilon targets 1.0 and 1.5, normal grid
1e-4,1e-3,.004,.016,.064,.256,1; amplitudes in [1e-6,4], normal in [1e-6,1],
raw-history radius<=1. Fixed SPSA seeds 410901/410902, 80 steps each, three
evaluations/step, learning rate .12/(1+step/40)^.602, perturbation
.08/(1+step/50)^.101, log coordinates and clipped gradient [-10,10].
Primary objective: maximin numerical refined beta/epsilon, transformed by
2 atan(ratio)/pi; invalid hidden/radius conditions penalized as in code.
Use the same eight radial weights and sharp-gate/eliminated-prefix formulas.
Do not call any interval kernel for r=9. Preserve all proposals. Select two
numerical winners before face attacks; never feed attacks back into optimization.
Per face: midpoint,64 seeded Sobol points,64 seeded sign corners, then three
L-BFGS-B starts (midpoint/two worst samples), max60 iterations, analytic
fixed-h gradients. Report actual found minimum (upper estimate of infimum),
numerical proxy, hidden usage and bottleneck. No 9D lower-dimension claim.
Promising if valid samples and both proxy and sampled ratios >=1.05; marginal
if >=1 but below1.05; failed section if a found pair is below1. Method failure
or invalid lift is separately classified. No retries based on surprise.

## Resources and records

One CPU worker; no GPU needed for tiny interval arithmetic. Max1200 measured
CPU-seconds for the entire stage, reserving120s for the optional 9D screen,
plus separately recorded failed-process charges. RAM ceiling2GiB. No CUDA or
model servers; GAS-0 untouched. Freeze code, candidate, exact formulas,
constants and input hashes; commit/push BEFORE official bounds. Synthetic
tests precede official runs. Store raw full arrays, radial bounds, exact
arithmetic, precision comparisons, resources, failures and reports only here.
STOP after failed improvement or improved8D+numerical9D result.
