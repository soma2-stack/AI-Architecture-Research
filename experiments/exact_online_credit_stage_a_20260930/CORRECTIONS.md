# Append-only implementation correction record

1. After the first official sweep, source inspection found that G1 local Python
variables A/B retained the preceding step's scratch Jacobians until the next
assignment; G2/G3 likewise retained the last direct-partial row buffer. The
reported compact between-step storage therefore did not describe actual object
lifetime. Exactness and trajectories were valid, but resource accounting needed
repair. Explicitly release A/B and direct after their use. This changes no model,
derivative formula, seed, gate or numerical computation. Preserve the first
sweep in pre_resource_lifetime_fix/. Commit the correction before rerunning
   the official sweep; use only the corrected sweep for final resource conclusions.
   Add a weak-reference unit test proving A/B are released before the next step.
   Double the analytic scratch inventory bound to cover overlap during Python
   per-layer variable rebinding. Persistent storage counts remain exact.

2. Meter wall_seconds is timed after Python/Torch imports; CPU seconds includes
imports. Label it post-import job wall rather than full launch-to-exit wall.
Peak RSS is sampled after imports, not an OS-wide allocation maximum. These
scope limits are disclosed; neither affects the CPU hard cap or exactness gates.
