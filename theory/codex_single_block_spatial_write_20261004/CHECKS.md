# Internal checks and theorem audit

The new theorem needs independent hostile review. Numerical checks do not substitute for proof.

## Load-bearing analytic checks

1. State pairing and differentiated response remain distinct. All formulas use full reference O_*, not a paired product projection.
2. Incoming survivor zero-sum credit is invariant under ALL donor controls and cancels in a one-coordinate comparison. Complement is bounded after each clear using the accepted nonperturbative two-step result.
3. Coordinate-change response on survivor rows is uniform BEFORE its mask. Equal survivor gates, equal forcing and identical input prefix make this exact, even when other controls were nonzero.
4. Mask writes an all-support balanced character with finite gain>.24kappa. Its low half is erased; its high half changes by the full Householder coupling bound, not an omitted feedback term.
5. Prior characters contain an old bit. Every new mask has a fresh bit, so both character products remain zero-sum and never excite J/B. Old-character gain1/2 is explicitly paid.
6. Public local scalar traces after every write imply future last-gate corrections independent of earlier controls. This makes the coordinate telescoping homogeneous after each completed stage.
7. Complement residual <=2N n^-6 per coordinate; all R coordinate changes charged. Endpoint controls are sufficient because a cube boundary contains a coordinate at +/-1. No intermediate monotonicity or affine control claim used.
8. Radial odd homeomorphism supplies ONE Euclidean ball; all gates legal for EVERY parameter combination, one final common endpoint, all raw energy counted.
9. Unit probe v fixed across stages, signs and queries. All direct local responses on v are public; final differences are private. Other gradient coordinates unrestricted. Query is a real .25/.75 permitted pattern, same on the pair; gradient projection gives a lower.
10. Dense perturbation charged over entire total horizon once. Earlier incorrect dense display not reused.
11. R=Theta(log n) is not omega(n); maximum total-duration credit and per-mode credit are distinguished. Full-model and global threshold claims unchanged.

## Numerical records

checks.py is independent, with no old kernel imports. 312 PASS records: scalar trace and mask identities, legal small histories and endpoints, direct local cancellation, and four192/256 scalar-ledger comparisons (n10^200 and10^400, R2 andmaximal R). Small complete histories use [.995,.99501] donor controls because their short tails are only an algebra check; no robust margin is claimed there. The actual theorem's full [.995,1-n^-2] control range is handled analytically with the long tail.

At extreme widths geometric sums are evaluated with log1p/expm1 of the loss1/n+1/n^2-1/n^3. Printed fractions1 mean precision/display rounding, not an exact equality. The proof uses conservative .998 and .999 inequalities.

## Compute

One process, libraries limited to one thread before imports, no workers/overlapping numerical jobs. Observed process threads4<=8; peakRSS46,567,424bytes (44.41MiB), CPU9.0625s, wall9.354616s. Guard: threads8, RSS160MiB, no children. GPU/CUDA0. No PyTorch, training, brute-force search or SVD.

Historical input hashes are in SOURCE_HASHES.json. FINAL_AUDIT.json verifies unchanged dependencies and exact checked-script hash. Only this new folder and its additive Codex resume entry may be committed; unrelated changes are preserved.
