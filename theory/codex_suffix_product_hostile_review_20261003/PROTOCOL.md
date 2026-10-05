# Independent hostile review protocol

2026-10-03. Target: the unaccepted theorem in
`theory/codex_suffix_product_kernel_attack_20261003/`.

The original files are read-only. This review is a fresh mathematical
derivation and a separately written diagnostic implementation. It is not a
clean replay of the author's test script. No original test code is imported,
called, or copied. The review does not assume the new obstruction is true.

## Fixed scope

The accepted paired corridor lift, frozen model, normalized query contract,
and epsilon=.001 are premises. Recheck the dependencies that the new proof
uses: strict row monotonicity, physical support, all-future adjoint upper
bound, dense comparison, public residuals, and exact common endpoint.
No unpaired or full-model upper bound is intended.

## Predetermined attacks

1. Construct a flat-row inverse discontinuity, and determine whether such
   a row is reachable. Test legal nearly flat rows at 256 and 384 bits.
2. Put a quantile exactly on a row knot and perturb from both sides.
3. Construct distinct legal rows with exactly equal codes, align their
   errors across maximally overlapping supports, and maximize over signs.
4. Test sharp column-overlap examples and all three rectangular regimes.
5. Independently implement Householder-cycle transport, including greedy
   non-scalar future gates, and compare to the analytic adjoint envelope.
6. Check ceiling arithmetic with integer arithmetic; check the p=1 regime.
7. Read and hash all original artifacts; inspect every original recorded
   check without treating the original outputs as independent evidence.

The analytic derivation supplies uniform statements. Numerical examples
can falsify identities but do not certify the all-history theorem.

## Resources before tests

One Python process, no workers, every numerical thread pool set to ONE
before importing libraries. CUDA_VISIBLE_DEVICES is empty and
NVIDIA_VISIBLE_DEVICES is void. No GPU library or GPU monitor is used.
Abort if process threads exceed eight, a child appears, or working memory
exceeds 192 MiB. No brute-force history search. Small sign enumeration is
limited to at most eight rows; larger aligned examples have an exact sign
maximizer by construction. High precision is CPU mpmath, not a certificate
based on unbounded floating-point claims.

Evidence is written once to this folder. A failed check is preserved and
reported; the theorem's constants will not be tuned to repair a failure.
