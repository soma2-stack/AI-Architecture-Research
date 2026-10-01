# Bounded direct-amplitude refinement after primary numerical screen

This is explicitly POST-PRIMARY-SCREEN and prospective for a separate numerical
refinement. Do not overwrite primary results/proposals/faces. No certificate.
Primary found10D promising,11D failing only on face1 (other10 faces pass),
12D near-threshold on many old axes,16D and higher substantially weak.
The old direct allocations used tangent radius cap0.65 and normal allowance1,
despite actual normal usage<0.05. This can create a false ceiling.

Keep endpoint/epsilon/query/norm/model/history/fixed-h exactly unchanged.
Use same two frozen bases and full local-domain condition radius<=1.
Use equal normal allowance0.125, within original[1e-6,1] constraints. Actual
fixed-h solves must respect it. Per-axis amplitudes remain in[1e-6,4].
This is a different declared amplitude optimization, not a changed error unit.

Refine11D and12D first. If12D becomes promising, bisect12..16 at14 and then
13 or15, at most two extra dimensions. If12D fails, stop at10/11/12 bracket.
No additional16/20/24 searches; keep their primary negative results.

Actual maximin objective: minimum D_C/(2epsilon) over a fixed pool containing
each face midpoint,8 deterministic Sobol points,8 sign corners, and the primary
screen's saved adversarial points. Pool is fixed before this refinement.
Use two starts/seeds408001/408002 per basis, log amplitudes,400 SPSA steps,
learning rate0.12, perturbation0.08 with the same schedules as primary.
Scale raw radius back to at most0.95 (including0.125 normal allocation) if
needed. Penalize any sampled hidden usage above0.125; no invalid point may pass.
No basis search. Starts are the archived primary direct allocation when
available; otherwise balanced actual linear ranges with tangent radius0.65.

After optimization freeze winner amplitude vectors before NEW face attacks.
Validation uses the primary full-face rules plus32 separately seeded new Sobol
face points and three new optimization starts per face. Add counterexamples
found in validation to the RECORD, not back into optimization. Do not retune
that dimension after validation. Track initial and fresh validation separately.
Thresholds unchanged: sampled minratio>=1.05 promising, <1 failure, otherwise
marginal. All conclusions remain specific to screened sections, not global
robust-dimensional upper bounds.

Total task CPU limit remains900s, combining primary, refinement and summaries.
If reference outputs mutate, stop. No rigorous kernel or interval arithmetic.
The extra diagnostic clarifies allocation versus weak directions; it is not
a replacement of the primary experiment or a retrospective preregistration.
