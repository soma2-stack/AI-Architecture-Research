# History-uniform adjoint leverage

**Codex, 2026-10-05 — THEORY ONLY**

## Result

**STILL OPEN.** The complete all-query upper bound currently available is the
accepted packing-repair estimate
\[
\Lambda_R(t,S)\le a^v\min\{q_f,\sqrt{s/n}(100+6q_fv)\}+(v+7)e_R,
\qquad v=N-t,\quad s=|S|,
\]
for ordinary support, with \(e_R\le4\cdot10^{-8}n^{-2}\). It includes all
midpoint gate schedules, all future query horizons and preactivation choices,
and the complete Householder/private renewal.

I found an exact reducing decomposition in the reference model. Tuple-wise
zero-sum modes avoid the two Householder functionals and satisfy the sharper
component bound \(200a^v\sqrt{r_S/n}\), where \(r_S\) is the number of
four-site tuples touched by the support. This does not control the full
leverage because the tuple-common/private complement can overlap the same
support.

A legal antisymmetric cycle mode remains visible at at least
\(0.16\sqrt{s/n}\) for ages \(v\asymp\sqrt n\log n\), and gives an
\(n\)-independent positive leverage for \(s=\Theta(n)\). Therefore a bound
with an age factor tending uniformly to zero is false. This does not refute
an age-independent \(O(\sqrt{s/n})\) bound.

## Packing consequence

No new unconditional packet-count or continuous-dimension theorem follows.
The accepted support-window and scalar/localized packing statements retain
their stated scopes. In particular, do not infer \(D=o(\sqrt n)\) for the
complete corridor.

## What remains

Bound the tuple-common/private complement under the exact recurrence
\[
p_{s-1}=a\{C^T\bar G_sp_s+
u(\mathbf1^T\bar G_sp_s)+v_H(e_1^T\bar G_sp_s)\},
\]
uniformly over legal corridor midpoint trajectories and all legal futures,
or build a legal example showing that its leverage exceeds the
\(O(\sqrt{s/n})\) scale. The accepted dense correction contributes at most
\((v+7)e_R\).

No numerical experiment was needed. No historical or current-theory file was
modified. No CPU or GPU computation was run.
