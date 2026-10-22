# Research Method

## Phase 1 — Map Existing Ideas

Before proposing new architectures, build a compact map of major existing model families and the assumptions they rely on.

Examples to examine include:

- Transformers
- recurrent neural networks
- convolutional networks
- state-space models
- graph neural networks
- diffusion models
- energy-based models
- Mixture-of-Experts
- reinforcement learning systems
- world models
- neurosymbolic systems
- memory-augmented networks
- retrieval-based systems
- agentic systems

For each family, identify:

1. What information goes in.
2. What computation it performs.
3. What it predicts or produces.
4. How it learns.
5. Where knowledge is stored.
6. What scales well.
7. What scales badly.
8. Important assumptions it makes.

## Phase 2 — Question the Assumptions

Actively question assumptions that modern AI commonly accepts.

Examples:

- Must intelligence predict tokens?
- Must a model have fixed layers?
- Must knowledge live mainly in weights?
- Must training and inference be separate?
- Must the whole network participate in every prediction?
- Must backpropagation train everything?
- Must perception, reasoning, and memory use similar representations?
- Must input be converted into tokens or embeddings?
- Must computation proceed in a mostly fixed direction?
- Must a model produce an answer directly?
- Must the network remain mostly static after training?
- Must one global objective train the entire system?
- Must intelligence be represented by one large model?
- Must reasoning be a sequence?

Generate additional assumptions yourself.

## Phase 3 — Broad Idea Search

Generate at least **20 substantially different architecture ideas**.

Do not make 20 variations of one concept.

Deliberately explore different computational principles.

For every idea record:

- name
- one-sentence concept
- fundamental computational unit
- what it consumes
- what it produces
- how it learns
- why it could be useful
- what makes it different
- closest known idea
- biggest weakness
- confidence that it is actually novel

Do not deeply develop them yet.

Breadth comes first.

## Phase 4 — Elimination

Reject or merge ideas that are:

- duplicates
- minor variations
- impractical without a clear benefit
- already established research under another name
- merely engineering systems around existing models
- impossible to test meaningfully
- missing a clear use case

Record why each rejected idea was rejected.

## Phase 5 — Develop the Strongest Five

Take the strongest five surviving ideas and develop them substantially.

For each one explain:

1. Architecture name.
2. Plain-English explanation.
3. Fundamental computational unit.
4. Input representation.
5. Internal representation.
6. Computation flow.
7. Output representation.
8. Learning mechanism.
9. Inference mechanism.
10. Memory mechanism.
11. Scaling behavior.
12. Suitable hardware.
13. Training requirements.
14. Expected strengths.
15. Expected weaknesses.
16. Closest existing research.
17. What may actually be new.
18. Smallest useful prototype.

Use diagrams, equations, or pseudocode only when they add real clarity.

## Phase 6 — Novelty Check

For every serious candidate, actively search for related prior work.

Try to disprove the novelty claim.

Ask:

- Does essentially this already exist?
- Is this just a renamed known architecture?
- Is the novelty only in application?
- Is the idea genuinely architectural?
- Which component is actually new?

If novelty becomes weak, downgrade or reject the proposal.

## Phase 7 — Prototype Design

For the strongest remaining ideas, design inexpensive experiments that could falsify them.

A prototype should answer a clear question such as:

> Does this mechanism learn X more efficiently than a small Transformer baseline?

Prefer experiments that can be run at small scale before proposing large training runs.

The purpose of the prototype is not to prove the architecture is revolutionary.

The purpose is to determine whether the underlying mechanism deserves further work.
