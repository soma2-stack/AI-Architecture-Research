# Diagnostic field interpretation

The preserved `diagnostics.json` field named
`relative_reduction_required_in_M3` is a misleading name: its formula is the
maximum fraction of the present cubic majorant that could be retained while
reaching equality at epsilon. Required reduction is one minus this fraction.
A negative value (face 2) means even zero cubic penalty cannot suffice with the
frozen certified query margin and amplitudes. Do not interpret this value as a
demonstrated feasible tightening. No output or certificate has been rewritten.

The three component fractions are diagnostics of positive upper majorants, not
fractions of actual curvature. The first failed face is face 1; the weakest
face is face 5. All seven sufficient face inequalities fail. This does not
establish that the true section lacks 7D robustness.
