# Experiment 010 — scaling capacity of recurrent memory

**Status: plan / screen, not a breakthrough claim.** Does not modify any original model or theory files. Experiment 009 demonstrated both the original protected RNN and matched GRU can learn two-slot binary recall at 64 tokens with sufficient updates. Novelty is unproven. Formal `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Falsifiable question

Does the protected-memory RNN preserve/retrieve **more independent slot values** than established recurrent controls when the number of slots grows from 2 to 4 to 8 and values from 2 to 4? Is slow retention specifically necessary? The earlier two-slot study already shows it may not be.

## Task and semantics

- Each history initializes every slot in a random order with `WRITE_<slot>,VALUE_<value>` pairs, followed by 64 training tokens (25% unmarked decoy values) and 1–3 uniformly randomized nonoverlapping marked rewrites.
- Both inputs and independently replayed labels are deterministic under a seed; holdout uses disjoint seeds.
- One query per slot, all from the same prefix, without one query modifying another. Training supervises all queries. No learned model receives final labels, privileged oracle masks or future tokens.
- Two or four possible values. Capacity conditions `(slots,values)`: `(2,2),(4,2),(8,2),(4,4),(8,4)`. Held-out delays 64,256.
- **Primary metric** `whole_varied`: all slots correct on histories with at least two different final values; secondary `whole`, per-slot accuracy, and every seed. Independent-uniform whole-memory guess baseline `(1/values)^slots`. Last-written-value copy has 0% `whole_varied` by construction. Structured oracle token replay is exactly 100% and **not** a learned baseline.

## Models and fair claims

- Original protected, protected without slow retention, GRU width24 (~parameter matched), GRU width32 (equal width), and the **known structured key/value delta-rule reference**.
- The delta-rule reference is given the WRITE/QUERY event grammar and uses the explicit slot address in those tokens, an intentional *extra inductive bias*; it must **not** be counted as a fair generic-RNN victory or novel primitive. It is an existence/upper-bias check, distinct from an oracle fed the labels. All other models see exactly the same token stream and training examples.
- Measure parameters and elapsed CPU time. Width-24 GRU is only approximately size-matched; confirm actual counts. Same updates alone do not match FLOPs/tokens, particularly for 8 queries.

## Resource and execution plan

1. Tiny CPU unit tests and smoke training for shape/semantics; check numerical gradients and exclusive output creation.
2. Bounded initial CPU screening **not guaranteed to fully converge** (200–800 update range). Choose one prespecified budget before observing results. Earlier Exp009 plateau ended at 500–750 updates, so a run shorter than 1000 updates is *screening only*; cannot establish architecture capacity limits.
3. If a control fails and other controls succeed at the screen budget, **do not infer lower capacity** without increased updates and matched training. Preserve missing/skipped configurations and timeouts in JSON.
4. Only escalate to a longer five-seed confirmation if the screen finds a reproducible capacity boundary; record the decision and a separate preregistration first. No hidden, repeatedly tuned sweep.

CPU only on a GitHub runner; fixed global wall budget, no user GPU or personal computer access needed. PR #23 remains draft, main unchanged. No more than one matrix starts at a time.
