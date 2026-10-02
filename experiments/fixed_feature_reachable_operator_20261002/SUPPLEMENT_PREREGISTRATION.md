# Prospective input-driven gate coverage supplement

Declared AFTER the primary diagnostic and its analysis.json, BEFORE these
fresh-seed outcomes. Primary results remain unchanged. Reason: primary base
histories/mutations used memory amplitudes at most.22; that is not coverage
of the entire admissible tanh gate range. This supplement tests stronger
ordinary histories, not an ambient operator ball or a new theorem.

Same archived actual dense models, c1, gamma1/n, epsilon.001, source .4ones,
fixed endpoint, input domain, query norms, physical-input whitening, exact
operator recursion, numerical checks and60CPU-minute combined budget.
Widths32/64/96; seeds86101/86102. Two generators, ALL executed:

1. driven_random: independently sampled actual memory inputs uniform[-.4,.4].
2. driven_coherent: a seeded spatial input profile in[.1,.35], with independent
   irregular timewise multipliers .5--1 and coordinate noise[-.025,.025].

At each step prescribe remaining memory h=tanh((R h_previous+b)_memory+u).
Keep protected memory coordinate zero and source exactly Hsrc. Inverse-realize
the other input coordinates, and verify the original cube. Reserve the final8
interior steps for cooling: if an immediate zero memory state can be reached
with |u|<=.48, choose it; otherwise apply -.45sign(Rh+b) on memory inputs.
The final step resets ALL h to zero. Horizon stays the same H+1; verify final
domain membership, and stop on invalid realization rather than rescaling
histories. Source/protected inputs remain those of the accepted inverse chart.

No novelty optimization or screening in this supplement. For each case use
the SAME tangent spectra and physical query lower/envelope diagnostics.
For each width select the supplement winner by the original frozen selection
rule and repeat the original finite radii/axis/joint checks. Do not compare
the changed sampler as a controlled effect of one gate parameter. Report it
as broader admissible-history coverage. Never use failures to retune inputs,
epsilon, budget, queries or seeds. Freeze supplement hashes and commit before
execution. Resource totals include primary300.71875CPU-s and188.0661wall-s.
