# Separately frozen adversarial supplement

2026-10-02. This is explicitly AFTER the primary screen, not a rewritten
primary preregistration. The primary outputs remain untouched. Purpose: try
to destroy the apparent superlinear signal from four sampled antipodes.

Targets fixed now: sustained bounded-spread sections at T=n, q=ceil(ln n),
for n=200 and400. They have history-chart dimensions294 and594. Keep their
exact primary time/space bases, baseline, amplitude, metric and epsilon.

Two starts per target: the primary weakest sampled-lower direction and a
fresh sphere point drawn using seed710002+n. No replacement histories or axes.
Optimize the unit coefficient sphere only, not model parameters. Objective is
the ALL-QUERY operator-norm upper envelope divided by2epsilon, not an RMS
norm or raw rank. A compact invariant block lets the SAME reference operator
be evaluated exactly with d by d matrices and one scalar.

Predeclared algorithm:120 normalized-coefficient gradient steps per start,
Adam-style history-variable updates with step.025, betas.9/.999, stabilizer
1e-12. Stop a start if upper-ratio<.25. Stop supplement cleanly at600 measured
CPU seconds; preserve incomplete starts. Torch float64 CPU, no CUDA; no neural
training, no model optimizer, no change to R/W/b or epsilon.

For each selected point recompute the FULL reference matrix independently
with primary NumPy propagation. Compare its operator norm, legal box-query
lower estimate, actual input-domain checks, exact endpoint and physical radius.
This double-implementation check is numerical, not an interval certificate.
Preserve every optimization trace and coefficient. A subthreshold upper
envelope defeats THAT joint sphere numerically, not every possible basis.

Before outcomes, hash this protocol, the two new source/test files and each
target's frozen primary NPZ. Save the new tests and prospective manifest.
Source and all primary outputs are read only during this supplement.
