# Implementation repairs and preserved failures

## Raw diagnostic flag type (before any valid diagnostic output)

The first raw-pool diagnostic used bitwise inversion on the archived uint8
confirmation flags. Both 0 and 1 become nonzero, so this accidentally admitted
confirmation IDs. Its saved-rank lookup stopped with KeyError '740' before a
valid diagnostic result file was written. The failed log remains
raw_diagnostic.log, the initial code is preserved in commit 7009d6d, and its
11.703125 CPU seconds / 11.746910 GPU-active wall seconds are charged.

Fix: explicit confirmation == 0, with an assertion that all 32 sampled IDs per
width are search IDs. The seed, count, objective, source pool and thresholds
remain unchanged. Rerun both widths/models using the intended search-only
sample; save a separate retry log. The eight-endpoint primary analysis and
its outputs were not altered. No diagnostic history is promoted or certified.

## High-precision library index type

The first CPU cross-check reached the scalar curvature calculation but mpmath
rejected numpy integer indices selected by unravel_index. The original
high_precision.log and code at b06698b preserve the exception. Convert the
three selected indices to Python ints; no equation, point, numerical precision,
threshold or model changes. Repeat only this failed CPU validation phase and
save high_precision_retry.log. Both attempts are charged. No primary GPU
geometry or existing certificate is rerun.
