# Prospective full-history supplement

Frozen after the primary source-only sweep completed and before any full-history
Jacobian outcome was collected. This timing is explicit: it is a SECONDARY
completeness check, not part of the untouched primary preregistration.

The source-only primary limitation motivates this check. No primary configuration,
source file, seed, epsilon, c, history objective or result will be changed.

Use widths 12,16,20,24, fresh seeds 73101,73102, and all three unchanged aperiodic
history strategies. Source signs/memory-history amplitudes and the accepted dense
model recipe are the same. Horizons use the same window formula. These widths
are below n0(1)=200; their scaling is exploratory finite-size evidence.

Compute the COMPLETE fixed-h input tangent map: all H*n hidden-history chart
coordinates, with the exact dense input-chart Gram, are whitened into Euclidean
input units. All independently differentiated R/W/b entries are included in
the exact dense RTRL sensitivity and its chart derivative. The final h is
identically zero. No surrogate/source restriction or frozen-gate derivative
omission is used in this supplement.

The output metric is the same primary one-step BOX-RMS query-response metric,
with its explicit normalized covariance square root. This remains a lower
diagnostic for the permitted supremum, not a replacement of that contract.
Full singular spectra and counts sigma>epsilon are numerical local diagnostics.
Also report prior input-SD and .05-radius linear counts. No finite-radius or
continuous-memory theorem follows.

Derivative implementation uses each coordinate's gate variation plus R feature
injection, current W-input change, and next W-input compensation. Preserve every
second-derivative term implicit in differentiating RTRL. Compare two-step-size
finite differences of actual frozen-parameter gradients before interpretation.

One worker, four BLAS threads, float64 CPU; no CUDA. Supplement cap: 60 process
CPU-minutes, 20 wall-minutes and 8 GiB RAM; these are within the original overall
120 CPU/45 wall budget after adding measured primary usage. Stop and preserve
partial evidence if a cap or numerical check fails. No alternate width or seed
replacement. No theorem or architecture work. Commit this supplement and source
hashes before its official measurements.
