# Accepted checkpoint and new absolute-energy question

2026-10-03. This record supersedes the pending-review status in older Codex
resume entries. Historical proofs, reports, outputs and reviews are preserved.

## Accepted, not re-reviewed in this stage

1. **Growing local radius:** the reviewed multiharmonic construction proves
   a fixed-feature continuous causal lower bound Omega(n^(16/15)).
2. **Width-independent LOCAL radius:** following the owner's Claude VERIFIED
   and Grok VERIFIED checkpoint, for every integer n >= 10^900 there is one
   admitted continuous same-endpoint section with

       ||X_n(y) - X_n(0)||_2 < 0.02,
       D >= n^(19/18) / 20,000,000,
       boundary antipodal half-margin > 999.999649997999,
       epsilon = 0.001.

   Hence d_fixed(n, epsilon, LOCAL radius <= 0.02) = Omega(n^(19/18)).
3. **Full model:** the accepted bounds remain
   Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

The local radius is around the public, width-dependent raw-input history
X_n(0). Its absolute norm is not bounded uniformly in width. History length
may grow. These statements give no finite-bit/VRAM, practical-onset, learning,
architecture or every-RNN guarantee. Fixed-feature sections cannot simply be
multiplied into a full-model lower bound.

## New result in this directory

The public center has absolute norm asymptotic to

    sqrt(2[(1/20)^2 + (atanh(2/5)-1/20)^2]) n sqrt(log n),

approximately 0.53313 n sqrt(log n). PROOF.md gives an exact reference formula
and a two-sided bound for the actual frozen dense R.

More decisively, the unchanged dense family with its required endpoint h=0
has **no** uniformly bounded-absolute-energy histories for all sufficiently
large widths. Every nonempty history ending at h=0 requires

    ||X||_2 >= (1/20 - 1/(100n)) sqrt(ceil(n/2))
                - 4/(10^8 n^(3/2)).

This is a feasibility obstruction, not a query-norm relaxation or an O(n)
compression theorem. It applies irrespective of source profiles, gates,
history length and section parameterization.

Even if the final endpoint were changed, a long window in the accepted
intermediate gate cube incurs growing bias-cancellation energy. Thus that
specific multiharmonic mechanism cannot be made absolute-energy bounded by
amplitude/frequency/duty-cycle changes alone.

A theorem allowing a different common endpoint or a different public bias
would be a different scope. No general O(n) credit-memory theorem for that
enlarged bounded-energy class is claimed here.

## Provenance

The two review verdicts are accepted from the owner's message. Grok's saved
review report is hashed without re-review. No separate Claude bounded-radius
review folder was located by the scoped filename inventory; no review record
has been fabricated. Source hashes are recorded in PROVENANCE.json.
