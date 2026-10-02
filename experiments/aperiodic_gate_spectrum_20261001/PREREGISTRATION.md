# Aperiodic gate spectrum diagnostic

Prospective configuration, 2026-10-01. No new theorem or certification.

## Primary question and scope

At fixed c=1, gamma=1/n and epsilon=1e-3, measure whether the number of
query-visible LOCAL directions in the recent source-feature history behaves
more like n^2 or n^2 log n. Use the accepted hard rotating/dense parameter
recipe; no model fitting, architecture change or witness optimization.
Widths 16--128 are finite-size diagnostics below the accepted sufficient
proof-width bound n0(1)=200. Widths 200 and 256 are in that range.

This experiment cannot prove a memory dimension or an asymptotic law. In
particular singular vectors are infinitesimal, the source subspace is only
part of the full history tangent space, and a linear spectrum is not a jointly
robust nonlinear section. The source map is the one proposed in the bounded
aperiodic review. Its restriction is declared before looking at results.

## Histories, window and fixed-h chart

For each width calculate H=ceil(log(kappa_Q*1.2/[epsilon*gamma])/-log(a)),
where a=1-1/n, beta=max(1,||R||F), kappa_Q=a/beta. Use H freely specified
hidden states, then one exact zero reset, so T=H+1. h0=hT=0.
Source states are independent seeded signs times .3, keeping their base
gates equal to .91. Three frozen memory-history strategies:

* diffuse: independent uniform signs/amplitudes in [-.4/sqrt(n),.4/sqrt(n)];
* random_pulse: zero odd states, even states have one randomly chosen coordinate
  2..k at a random positive amplitude .15--.30;
* query_adversarial_pulse: the same pulse/zero alternation, select a coordinate
  maximizing a query-weighted deviation of the running transport from its
  mean-scalar gate replacement, excluding recently used coordinates. Random
  amplitudes break repetition. This is a declared greedy construction, not
  post-result optimization.

All are nonscalar and aperiodic in their complete gate sequence. Odd zero
steps in pulse strategies do not make the varying even gates periodic.
The greedy procedure uses a normalized running k by k transport; it is a
history-generation diagnostic, not a proposed encoder. Each history must
pass input-domain, endpoint and aperiodicity checks; do not rescale or replace
failed histories. Preserve and stop at an invalid generated history.

Realize x_t=atanh(h_t)-R h_(t-1)-b. For a source perturbation, keep memory h
and final h fixed and recompute the realized inputs. Sensitivities themselves
differentiate parameters holding every realized input fixed. Do not confuse
that with differentiating the controlled inverse formula through parameters.

## Query normalization and measurable spectra

Use frozen group RMS w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b), the accepted
head q=1/sqrt(n)*1 and beta-normalized final scalar loss. Epsilon is unchanged.

A supremum over permitted queries is not a Hilbert norm and has no single
ordinary SVD. Report THREE Euclidean diagnostic maps rather than raw rank:

1. Primary lower diagnostic: RMS responses over ALL sign vertices of the
   permitted one-step gate box [sech^2(.5),sech^2(.25)]^n. The exact covariance
   is (g_mid^2*11^T+s_g^2*I)/(beta^2 n), pulled back by actual R. This describes
   real future inputs in [.2,.45]^n and does not drop head normalization.
2. Secondary lower diagnostic: RMS over a seeded bank of 32 actual continuations
   of lengths 1,2,4,8, inputs uniform in [-.45,.45]. Every continuation is
   simulated on the actual frozen model; direct future injections do not vary
   with the fixed-h history. Record its adjoint covariance.
3. Upper envelope: kappa_Q times the Frobenius norm of the SAME encoded
   sensitivity variation. It bounds every permitted query of that component,
   but can substantially overcount truly visible directions. It is not an
   upper bound for omitted history subspaces/components.

The scalable reference propagates with G_actual R0 and uses actual group
weights/query covariances. Source-only variation does not change memory gates.
It produces every memory-output R/W parameter response, including both
injections, and zero memory bias response. It omits fast source-output
gate derivatives and tiny dense-coupling derivatives. Those limitations must
be reported and numerical full-model cross-checks must pass before interpretation.

For source time s, memory parameter-row propagation is B_s=Phi_(T,s)G_s.
The derivative columns are B_(s+1) for R and B_s/.91-delta B_(s+1) for W.
Use the covariance square root on the STATE axis before forming the spectrum;
do not use the rank or singular values of a raw sensitivity snapshot.
Each source coordinate supplies one copy of this time-to-query kernel.

Physical source-input whitening uses the tridiagonal chart Gram with diagonal
(.91^-2+delta^2) and off-diagonal -delta/.91, including the final reset.
Numerically cross-check its unit norm in the actual dense input chart. Primary
counts use one unit of Euclidean physical input-history perturbation; also
publish the previously used input-SD scaling sqrt(3/32) separately. Epsilon
in output units never changes. Publish counts at radius .05 separately; these
are still linear diagnostics, not certified finite-radius dimensions.

## Spectrum, correlations and scaling

Compute the full time-kernel singular spectrum using its Gram matrix. Replicate
each value l times for the declared source subspace. Record count sigma>epsilon,
count/(n^2), count/(n^2 log n), stable rank, spectral gaps near epsilon, tail
energy, and mean temporal correlations by lag and by orbit residue. Save full
spectra, not just a selected prefix. Cross-check a small spectrum with direct SVD.

Keep the scalar/zero-memory control at seed 62101 for each width as a numerical
positive control for temporal sharing; it is not a repeat of prior proofs.
Fit counts against A*n^2 and B*n^2 log n through the origin, separately by
strategy and metric, plus a free log-log exponent. Report errors, leave-one-
width-out errors and finite-range/model uncertainty. Do not select a new
objective, c, epsilon, window or perturbation scale after inspecting results.

Selected threshold/leading/tail modes receive permitted-box vertex coordinate
ascent to estimate actual query separation. It yields NUMERICAL lower estimates
of the worst query and cannot certify a maximum. Counts from RMS, sampled
continuations and the envelope remain distinct.

## Cross-checks, resources and stopping

Before official measurements, development-seed checks compare direct fixed-input
autograd/BPTT gradients and finite-difference derivatives to the scalable map,
and reproduce physical input norm, final h and query covariance. Official
widths 16,64,200,256 repeat selected checks. Two FD steps are recorded. A
per-unit discrepancy above epsilon/10 stops interpretation and is preserved.
No formal unit suite is added/run; these are numerical validation measurements.

CPU float64, one worker, four BLAS threads, torch CPU runtime. Maximum 120
process CPU-minutes, 45 wall-minutes, 8 GiB process RAM. Stop conservatively
before the cap and report partial results. No GPU, model server or GAS-0 use.
No theorem or architecture work. Freeze config/source hashes and commit the
setup before official results. Historical evidence and accepted theory remain
unchanged. Store raw per-case records, histories, models, spectra and resource
records in this isolated directory.
