# Numerical evidence, not a robust-dimension certificate

45 numerical and19 exact rational recorded checks PASS. Scripts and raw
records are in checks.py/checks_result.json and
exact_path_checks.py/exact_path_result.json; no original kernel code was
imported. Numerical work
was intended to falsify the exact decomposition and differential, not to
estimate robust dimension by raw rank.

## Small matrix checks

At n=1024, reference R0 only, m=2,T=8: direct UPU agrees with the open shift
plus rank-two identity; all active feedback rows are equal across their
four-site tuple; exact local kernels and private weighted kernels agree
with the full r-by-r recurrence. Balanced OUTPUT modes remove feedback.
The public reset transmits feedback as predicted. Its measured total
feedback norms .37750 and .37513 INCLUDE public response: these are not
private-margin measurements.

These small-width tests are algebra checks below the accepted n>=10^6
range and outside the conservative S<=d/100 theorem placement restriction.
They do not constitute a new certified witness or asymptotic result.
Measured raw inputs stayed in the cube, but the accepted large-width lift
and energy theorem remain the rigorous premises.

Joint R/W/b central differences, with the SAME realized inputs frozen,
gave l2 errors1.66e-10 and2.43e-10 at step sizes1e-5 and1e-6. A separate
fixed-feature action agrees with the complete differentiated recurrence.

## Equal local information, nonzero remaining feedback

For m=1,T=3, fix oldest product k1 and sum k1+k2+k3, vary k2 by +/-1e-5
and k3 oppositely, then recover the three gates by the triangular inverse.
All quantile levels lie in the first interpolation interval, so the local
quantile code is identical; the exact compensator trace is identical too.
Both endpoint states agree numerically.

The remaining feedback difference had Frobenius norm3.75342e-6. This norm
is recorded ONLY to check nonidentity, never as the permitted-query metric.
A direct legal one-step gate optimization gave an observable lower estimate
7.01901e-11 for the feedback difference, and5.34410e-10 for the COMPLETE
credit difference. Thus private feedback does exist, but this example is
far below epsilon. It neither refutes compression nor proves a new robust
dimension. Equal local codes do not imply the actual observed metric must
be large.

## Query dilution failure

The explicit legal all-high one-step query reads the terminal cycle
coordinate at approximately.664688878053054 for n=10^6. Independent
192/256-bit CPU evaluations agree to40 recorded digits. This supports
the exact formula in PROOF(23). It shows why the paired ordinary-row
8/n ledger cannot be extended blindly to every Householder component.
It does NOT show the reachable feedback can exploit that coordinate in
an independently high-dimensional robust way.

## Resources

One numerical process, no workers, every numerical pool1 before imports;
observed peak process threads4. Math CPU.796875s; wall.864349s; peak working
set98,877,440 bytes (94.30MiB). GPU/CUDA ZERO. No OOM, crash, resource-limit
failure, broad gate search, training or singular-rank dimension inference.

The exact rational follow-up ran sequentially and used.203125 CPU seconds,
21.38MiB peak working set and4 process threads. It validates the single-
insertion prefix-suffix formula independently and checks the short-packet
constant exactly. Total math CPU across both runs is1.000000 seconds;
overall peak RAM remains94.30MiB. No GPU or worker was used in either run.
