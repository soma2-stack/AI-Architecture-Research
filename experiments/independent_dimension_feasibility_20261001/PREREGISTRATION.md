# Cheap numerical dimension feasibility screen

Primary requested dimensions: 8,10,12,16,20,24. Same independent width-4
confirmation endpoint, T=37, P=24, full supported fixed-h dimension24.
Same parameter-RMS/input-SD normalization, fixed scalar-head query family,
epsilon=1/1000 and exact fixed-h requirement. Numerical computations are NOT
certificates. Do not invoke an interval kernel, search histories, train models,
add widths, alter previous results or touch GAS-0.

Frozen input: endpoint.json is a byte copy of the accepted7D candidate,
SHA25687895c3f3742b9a97e51eced5f9d1cf0606103290cedac4c2b0b224977c63f82.
Use only its central history/model and original normal/leading7 tangent axes.
The new higher-dimensional charts are sections at that same endpoint.

## Bases and query metric

Two deterministic nested bases, generated before official screening:
1. query-weighted SVD of the fixed-h sensitivity tangent (top24);
2. accepted leading7 tangent directions, with numerical nullspace correction,
   extended by query-weighted SVD of their orthogonal complement.
For the old7D calibration retain its original4 normals. For the higher-D
screen use the four last-input coordinate directions as normals. This ordinary
chart permits explicit numerical fixed-h compensation
x_T=W^-1(atanh(h0)-R h_(T-1)-b), avoiding repeated Newton trajectories.
It changes section coordinates, not endpoint, metric, model or fixed-h contract.
Its realized history is held fixed when differentiating model parameters;
never differentiate the input-generator compensation with respect to theta.
The raw history chart is
x=x0+sqrt(3/32)B(y,t). Normalized sensitivities multiply columns by original
R/W/b group RMS constants. No objective-dependent basis selection or rotation.

For independent support, actual permitted-query distance is
D_C=sech^2(1/4)/(sqrt(4)*max(1,||R||_F))*||diag(R_owner)Delta_s||_2.
Disjoint parameter-column support makes simultaneous maximum gates optimal;
their realization is the same reviewed future input family. The dual
third-order proxy uses the conservative reviewed7/8 gate, not a new query.
Fixed h is enforced by the explicit terminal-input solve; future direct
parameter injections then cancel. Record floating residuals and normal usage.

## Cheap numerical amplitude optimization

Use per-axis amplitudes a_i and equal normal allowance a_h. Constraints:
1e-6<=a_i<=4, 1e-6<=a_h<=1, complete chart raw radius<=1,
same radius convention as the accepted certificate. Optimize maximin proxy
beta_i/epsilon with numerical hidden contraction/self-map guards. Prefixes
inherit neither equal amplitudes nor a prior certificate.

Two deterministic starts per basis: balanced linear query target ratios0.75
and1.5, globally scaled to history radius<=0.4. Seeds404001,404002. At most
160 SPSA steps (two evaluations per step plus current acceptance), bounded
log parameters, step schedules fixed in config. Preserve every proposal.
Choose each initial normal allowance from the fixed grid
1e-4,1e-3,4e-3,.016,.064,.256,1 using the same objective/guards.
Best numerical-valid proxy candidate retained per start; if none is valid,
retain best penalized candidate and flag the failure. No rigorous feedback.

For each dimension, also retain a DIRECT-GEOMETRY stress allocation, balanced
to actual linear face separation2epsilon, scaled upward on the fixed grid
0.5,1,2,4 with tangent raw radius capped0.65 and normal allowance1 (whole
chart radius still<=1). This is a prescribed alternative section,
not an adaptive witness hunt. Select the best of this fixed grid by midpoint
plus8 Sobol points per face, then perform the full face checks. Record the
best normal-grid proxy separately; keep allowance1 for direct geometry.
Direct geometry candidates permit distinguishing
conservative proxy failure from actual sampled collision.

Third-order proxy uses ordinary float64 whole-box positive chain majorants,
including both affine tightenings, all mixed terms and implicit y2/y3 and
s_y y3. Compute only the aggregate third contraction, not a full third tensor,
to keep this cheap. No outward intervals or rigorous claim in this task.

## Actual joint face checks

For the best valid proxy and best balanced direct candidate per basis:
every face gets its midpoint,32 fixed Sobol face points and32 sign corners.
For r<=8 include all face corners. Minimize actual D_C over each face with
analytic implicit-section gradient, L-BFGS-B, at most50 iterations, from
midpoint and two worst sampled points. For r>=16 reduce to24 iterations.
All antipodes move all retained directions jointly, not single-axis checks.
Invalid fixed-h solves/normal limits/domain are failures, never successful scores.
Store every face, extrema, roots, residuals and optimizer status.

Report sampled/optimized actual minimum (an UPPER estimate of the infimum),
numerical proxy minimum, ratios to2epsilon, normal usage, contraction/forcing,
third-order penalties, and the first bottleneck. A found pair below threshold
is a genuine numerical counterexample to THAT section; not an impossibility
theorem for every possible basis or amplitude allocation.

Promising: every searched face has D_C/(2epsilon)>=1.05, numerical fixed-h
solves valid, and accepted chart radius/normal limits respected. Marginal:
ratio in[1,1.05). Clearly failing screened sections: ratio<1 on both bases
and both candidate styles, or no valid section. Method failure is inconclusive.
Rigorous plausibility is graded separately: proxy>epsilon throughout is
promising for the reviewed certificate; proxy failure cannot disprove geometry.

## Small binary refinement / stopping

After the six requested dimensions, if a promising lower dimension and a
clearly failing higher dimension bracket a transition, bisect that one bracket
at most3 times, using IDENTICAL budgets/rules. Do not chase disconnected
positive results. If no clean bracket exists, stop and report uncertainty.
Never attempt certification or go beyond24.

## Validation and resources

Before requested dimensions, sanity-check analytic Jacobians against finite
differences on a tiny synthetic problem and the accepted7D numerical proxy
against its saved values. This is numerical calibration, not re-certification.
Terminal compensation is a pre-freeze implementation decision for cheapness,
not an outcome-driven repair.
Freeze source/config/bases before official screening. Hash prior7D artifacts.
Use one CPU worker/thread; small arrays make CPU cheaper than GPU launch/setup.
Hard task ceiling15 measured CPU-minutes including diagnostics; preserve partial
results if exceeded. No model server or GPU workload. Save timings/RAM/proposals.
Stop after the approximate transition report; no architecture or learning work.
