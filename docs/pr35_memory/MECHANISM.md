# Mechanism analysis and theorem translation

Classification: **Not novel / existing mechanism**, as far as established computational operations and hard invariants are concerned. This is an empirical engineering study of a parameterization, not a discovery claim.

1. Claimed capability: learn selective recall of 2/4/8 independently queried binary facts under distractors and delayed queries, potentially with better success/cost at a fixed training budget. This is a hypothesis until measured.
2. State: fast vector u and memory contrasts p, physically encoded as [u,p,-p].
3. Transition: explicit gated recurrence in README.md. Main carry a=1; contract ablation a=1-1/w.
4. Reads/writes: recurrent proposal reads u; fast recurrence reads full physical h; input gates read learned token embedding. Both u and p update per token. No external memory is accessed.
5. Trigger: each token; sigmoid gates decide write strength. No hand-coded write/query parser.
6. Learning: full BPTT/AdamW on final token binary cross-entropy, all slot queries; same 600 updates and stream across models.
7. Closest primitive: affine maps, tanh, fixed polynomial features, sigmoid convex-gated updates; none is new.
8. Closest architecture: coupled input/forget gated memory (GRU update/CIFG-style) with a separately coupled fast state. PR #23 protected model is an even closer repository reference.
9. Closest system: PR #23 token model plus capacity_010 benchmark and ordinary supervised trainer.
10. Known machine performs important transitions: yes; ordinary gated recurrence on (u,p) exactly.
11. Decomposition loss: **none for recall or gradients**. Substitute B=[B_u,B_+,B_-] into fast map to obtain B_u*u+(B_+-B_-)*p. Store p once. Every future prediction, parameter-gradient path through the original redundant parameterization and gate update is preserved by synthesis. A minimal reparameterization can additionally replace B_+-B_- by one matrix, changing optimizer geometry unless the optimizer is transformed too.
12. Guarantee/separation: balanced synthesis has zero pair sum; all-ones rank-one multiplication annihilates pure memory differences. Ordinary contrast storage preserves this algebraic property at lower state cost. No distinctive guarantee/resource separation is established.
13. Nature of variation: known recurrent parameterization, fixed feature sharing and redundant state organization. It could prove empirically useful without becoming a new primitive or a distinctive architecture.
14. Historical closest mechanism: constant-error/gated memory in LSTM and leaky/convex recurrence. Exact mechanism-level reduction suffices for the current no-novelty classification; no unsupported exhaustive historical priority claim is made.
15. Modern closest mechanism: GRU-style gating; repository PR #23 Experiment 016's exact protected-memory reduction. These do not by themselves predict empirical optimization outcomes.
16. Primitive falsification: already falsified by the exact state/update reduction.
17. Architecture falsification: any claim of an indispensable pair mechanism is contradicted by compressed-state equivalence; any claim of better learning is decided under the fixed held-out/seed controls.
18. Smallest useful empirical test: the preregistered small CPU screen, because the practical uncertainty concerns learning at finite budgets rather than theorem validity.

## What is retained from PR #35
Balanced signs, exact zero-sum pair encoding, a fixed shared map from fewer latent coordinates to more pairs, and a named contractive carry ablation. Main-model gain is moderate and its code is smooth. No theorem is invoked to bound its recall.

## What is not transferred
Frozen prescribed dense R, alpha normalization, source bath, gather spike, literal clipping at enormous gain, peak actual-input support 3, amplitude<.5, schedule, common endpoint merge, robust legal-query gradient metric, or the theorem's n>=10^16 regime. Learned dynamics and ordinary forward readout would not inherit these statements even if a toy experiment succeeds.

## Why common endpoints matter
PR #35 deliberately erases state differences at the endpoint, while frozen-input parameter sensitivities differ. A deterministic model queried from the common state and same future inputs cannot recall which history occurred unless some additional persistent object is retained. A forward-recall experiment must relax common endpoints or explicitly retain learning-credit state. This prototype relaxes them. It is not an implementation of adaptive online credit memory, and no RTRL-sized tensor is silently charged as a width-w state.

## Numerical issues established before training
The audit's exact-real saturation code need only separate antipodes; the two unit vectors (1,0) and (99/101,20/101) can collide under the D=2 clipped code. It is not a generic invertible fact code.
At D=89 an exact polynomial coefficient ratio bounds necessary gain below by more than 10^50. This is an input-generation conditioning problem, separate from storing b binary values in a floating-point vector.
At sufficiently large n, a=1-1/n rounds to 1; the prescribed dense common-field term becomes invisible when added to a nonzero bias. Tests report where this occurs. Losing the perturbation in ordinary arithmetic does not refute the exact-real theorem.
