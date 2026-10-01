# Robust-witness search

This stage tests a witness-selection explanation for small previously certified
finite-error regions. Exact accessibility/observability and accepted packing
theorems are premises. No architecture or model-parameter optimization occurs.
Frozen model definitions, domains, epsilon, candidate seeds, selection and
stopping rules are in config.json; all pool arrays/splits are hashed before
scoring. Widths2/3/4 use matched dense/independent T11/22/37.

Phase A is entirely numerical. Ten thousand exogenous histories per width
are paired between models, split8000/2000 before scoring. Random, scrambled
Sobol and smoother low-amplitude strategies are fixed. Search-only mutation
and finite-difference/SPSA spectral optimization have a fixed equal budget.
They cannot consume or adapt confirmation histories. Full search results and
the implementation are sealed before confirmation scores are inspected.

The primary score rewards many jointly useful directions, then integer
packing bits, then observable range. It combines past tangent conditioning,
the SAME future-query frame, and a simultaneous mixed-curvature proxy.
Stage1/2 prefilters are numerical proxies, not alternate primary objectives.
The curvature proxy follows the accepted derivative recurrence with floating
arithmetic and a whole-box gate enclosure, without outward certification.
Recipe grids are fixed before results. No GPU result is certified.

All18 selected histories/recipes/axes are frozen and committed before Phase B:
best search, runner-up and best untouched confirmation for each model/width.
Only these predefined candidates are evaluated by fresh CPU interval jets,
mixed-curvature/implicit-section bounds, joint projection inverse certificate,
exact query duality and integer packing. No post-failure radius/profile/axis
optimization, replacement or search is allowed. A failed candidate is kept;
runner-up evaluation is authorized here independently of that failure.
Valid nonzero192bit products/margins replay at256bits without changing targets.

The archived witnesses are scored as baselines but are not re-proved. Compare
their already accepted secondary query-frame certificates (dense axes1/2/1,
bits2/2/1; independent axes1/1/0,bits1/1/0) with newly certified lower bounds.
Smaller new certificates do not invalidate archived ones or prove maxima.

Primary epsilon is1e-3 in unchanged input-SD/parameter-RMS gradient units.
No secondary epsilon analysis until primary results are frozen; optional
curves use only the same frozen products. Classification rules are fixed in
config.json; claims are local and empirical, not an all-width resource law.

One CPU/BLAS worker, bounded GPU batches,4GiB process/device caps,60 measured
CPU minutes and30 GPU-active wall minutes. Sample global GPU temperature,
utilization and VRAM, plus our own allocator; stop/reduce at86C and preserve
evidence. No interaction with existing model servers or other lane processes.
Stop after this stage. No width5, architecture invention or training.
