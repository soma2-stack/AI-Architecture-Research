# Interpretation and numerical-screen audit notes

The major improvement is exact last-input elimination, not radial subdivision
alone. With the candidate unchanged, weakest relative slack progresses:
2.4453% control -> 14.1314% elimination with native gates -> 14.1551% sharp
gates -> 14.7167% radial integration. Do not present this as evidence that
subdivision alone solved whole-box conservativeness. All refinements were
prospectively frozen before official bounds.

The two numerical 9D sections are NOT an upper bound or an exhaustive search.
Both have valid sampled fixed-h lifts. The actual worst face is7 in both:
D_C=0.00139730158 and0.00126783872, below0.002. Sampled normal usage is only
1.69% and0.57%; hidden inclusion is not the observed actual bottleneck.
The numerical proxy instead has its weakest face9. Its linear dual margins
are0.0007200202 and0.0006161673, already belowepsilon before third-order losses.
Thus improving the remainder alone cannot certify THESE selected projection/
amplitude allocations. This does NOT mean the allowed query family is
intrinsically too weak or that the new ninth direction is absent: unselected
residuals can add actual query separation. More/different allocations may work.

Both 80-step SPSA runs used frozen rules, same query_svd basis, one start each,
and no feedback from face attacks. All480 adaptive evaluations and both
selected winners are saved. Recordkeeping limitation: the14 initial normal-grid
scores were evaluated deterministically but not saved individually. Their
inputs/rules are recoverable from frozen source; counts include them. Do not
claim every initial score has a raw record. No rerun or extra optimization was
performed to repair that omission.

The pre9_gate.json arithmetic/source audit ran after official8D and BEFORE
the numerical9D screen; its0.046875 measured CPU-seconds are separate from the
main finalizer total. FINAL_AUDIT.json adds this and publication checking CPU.
No scientific run failed and no post-freeze scientific source repair occurred.
An ordinary publication checker then falsely matched the digit9 in 192-bit
filenames as a supposed9D interval output. Its initial source is preserved;
publication_repair.json records the fix to an exact allowed-filename list.
Separately charge1CPU-s for that failed bookkeeping process. Candidate, source
freeze, mathematical method and scientific results remain unchanged.

The new exact-elimination/radial proof still needs an independent hostile
review. The accepted8D theorem/method was used as control, not re-reviewed.
Scope remains this endpoint/section/metric/continuous encoder contract.
