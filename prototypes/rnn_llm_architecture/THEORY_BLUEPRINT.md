# Fourth architecture: theory-faithful RNN research design

**Status (2026-10-07): ARCHITECTURE BLUEPRINT + SCOPED CREDIT KERNEL.**
**NOT a complete LLM, a verified new architecture, or a proof of the open theorem.**

This is an additive, fourth research path alongside the three working
`RNNLanguageModel` cells (`tanh`, `near_critical`, `protected`).
The other three are controls and must stay runnable and unchanged.

## Why a fourth path is necessary

The three current models were inspired by the research but do not instantiate
its **frozen dense tanh**, **balanced donor/survivor corridor**, **actual
legal-query**, or **same-endpoint robust learning-credit** contracts.
Training those models would not test the main theory. The fourth path is a
faithful mathematical reference first; only a later, explicitly identified
language-model adapter may translate it to token prediction.

Goal still OPEN:

$$
D=\Omega(n)\quad\text{with}\quad mT=o(n^{3/2}).
$$

Here `D` is *robust learning-credit dimension*, not state width, ordinary
memory capacity, parameter count, or chatbot quality. The frontier's strong
results rely on large asymptotic n and particular admissible histories:
finite n/CPU demonstrations do not verify their asymptotic quantifiers.

## Block design

```text
FULL THEORETICAL PATH (not the existing three LLM cells)

  Frozen biased dense tanh model + selected fixed-source probe family
          |
          v
  Public preparation and source bath   [NOT IMPLEMENTED]
          |
          v
  Exact chronological gates and balanced four-site donor/survivor
  inverse-lift, including moving tracks and stationary compensators
                                       [NOT IMPLEMENTED]
          |
          v
  State/credit propagation:
      M_t = G_t^m (a O_* M_(t-1) + V)
      O_* = C + 1 u^T + e_1 v_H^T
      J_t = u^T M_t, B_t = v_H^T M_t
                         [SCOPED DIRECT MATRIX KERNEL IMPLEMENTED]
          |
          v
  Donor writes -> public Walsh captures -> post-capture trace repair
  -> clearing -> common nonzero reset  [NOT IMPLEMENTED]
          |
          v
  Actual frozen-input gradient queries and group-RMS normalization,
  complete query family, robust antipodal separation and resource ledger
                                       [NOT IMPLEMENTED]
          |
          v
  Architecture interpretation for token prediction (OPTIONAL / UNBUILT)
```

### Mathematical source of the implemented kernel

[Unpaired-corridor recurrence](../../theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md),
sections 1–5, gives `M_0=0`, `r=floor(n/2)-1`,
`a=1-1/n` and `O_*=C+1u^T+e_1v_H^T`; `J,B`
are vector-valued feedback. The same selected response appears in
[linear-dimension frontier](../../theory/codex_linear_dimension_frontier_20261006/PROOF.md),
section 3. `theory_reference.py` implements precisely that selected
linear *sensitivity* recurrence for supplied public/private gate values.
With `V=I` it returns the complete selected `M_t`; with other `V`
it tracks selected parameter directions. It retains `O(r*p)` explicit
sensitivity state; no memory compression is claimed.

It **does not** independently synthesize valid gates, or model the
underlying hidden-state preparation, dense perturbation, legal future
queries, or end-to-end inverse lift. A caller-supplied arbitrary
`gates` tensor is not evidence of an admissible history.

### Full-theory module boundaries for Sol

1. **Frozen reference model** (unimplemented): exact `R_0` and controlled
   `R_actual`, source block, tanh bias/input map, indexing, and independently
   differentiated `R, W, b`, with realized inputs **fixed** during the
   derivative. Cross-check autograd with the exact sensitivity (not the
   derivative of a history-generating inverse-control policy).
2. **Legal history factory** (unimplemented): deterministic, continuously
   parametrized four-site tuples; moving cycle coordinates, stationary
   compensators, donor/survivor labels, public bath/front, zero-start
   preparation, source equilibrium, exact common nonzero endpoint, and
   chronological legal controls. Reject invalid topology, time schedules,
   wrap, or gate bounds.
3. **Credit/probe engine** (**partial**): direct `M_t`, `J`, `B`, rank-two
   `O_*`; later add the local `L_t` vs feedback `H_t`, private renewal,
   and row-by-row bath/front response **without** dropping unpaired terms.
4. **Capture/transport mechanism** (unimplemented): accepted early-capture
   donor writes, Walsh survivor captures, *capture before correction*,
   clearing and terminal trace repair, endpoint reconciliation. Keep
   original public capture and control bookkeeping exact.
5. **Actual legal-query oracle** (unimplemented): complete future queries
   in the source contract, group-RMS normalization, `epsilon=.001`,
   permissible future preactivations, antipodal separation, exact/replay
   dense-error charges, and direction-counting. Frozen future raw inputs
   and complete parameter-block sensitivity matter.
6. **Evidence/claims interface** (unimplemented): separate fields for
   numerical observations, contract validity, proven-in-scope conditions,
   assumptions, independent-review status, and open gaps. Measure
   `(n,m,T,K,R,D,mT,||X||)` with definitions from proof, not proxies.
7. **Future LLM integration** (NOT IMPLEMENTED): only once the forward
   recurrent mechanism is defined for arbitrary token embeddings.
   Specify exactly which invariants survive adding token inputs, learned
   weights, nonlinear readout, and training. If they do not survive,
   label the token model **theory-inspired** rather than exact.

## Open results MUST stay open

- The early-capture source gives a strict-budget **sublinear** result
  `D >= n/(10^70 log log n)` and a linear-dimension **boundary**
  construction at `mT=Theta(n^(3/2))`; it does not give the strict-budget
  `D=Omega(n)` theorem.
- Theorem B bounds a particular bounded-write control family. It does NOT
  exclude different histories with diverging jointly protected controls.
- The 2026-10-07 Route-6/Route-7A segment-atom, reservoir, and separated
  capture results have scoped conditional or pending-review statements.
  They are adversarial tests and candidate constraints, not a solved
  universal compression or construction theorem.
- Finite-size clean Walsh measurements through R=16 are
  **diagnostics for a particular recurrence**, not a transferable
  guarantee for a trained LLM.

## Validation gates (CPU first; no training)

- Reproduce exact `O_*` indexing and direct `M_t`, `J_t`, `B_t`;
  compare independently computed full and selected-probe sensitivity.
- Reproduce direct-versus-renewal decomposition, with randomized legal
  histories and fixed-source probes; count full memory/state footprint.
- Cross-check finite differences and autograd **holding realized raw
  inputs fixed**; reject policy-differentiated results.
- Check gate legality, chronological front, source and bath invariants,
  zero-start and common-endpoint reset to numeric tolerances explicitly
  tied to the actual error ledger.
- Match actual legal future queries and group-RMS normalization; check
  all source assumptions and report failing cases.
- Test protected Walsh capture/cross-talk and history cost under finite n;
  report numerical accuracy and discrepancies without promoting them to
  asymptotic proof.
- Keep a reproducible failure/counterexample log, and require hostile
  review before promoting theorem-derived architecture claims.

## What can be executed now

```bash
python -m pytest -q prototypes/rnn_llm_architecture/test_theory_reference.py
python -m pytest -q prototypes/rnn_llm_architecture/test_model.py
```

The first command checks the small, scoped reference equations; the second
preserves the three original engineering controls. Neither runs training.
Tests must actually execute before claiming they passed.

## Non-goals

Do not change `AGENTS.md` or theory proof/ledger evidence; do not merge
PR #23; do not train; do not run AMS Stage 0; do not imply that adding a
`cell_type="theory"` will automatically give us a trainable LLM. Only
expose that switch once a coherent arbitrary-token forward transition
exists and its theoretical relation is explicitly documented.
