# Four RNN architecture paths — implementation and comparison

Architecture development only. No training, optimizer, parameter updates,
collector, RL, GPU experiment, proof-status edit, or main-branch change.
The strict target **D=Omega(n), mT=o(n^(3/2)) remains OPEN**.

## Paths and preserved controls

| Path | Executable implementation | What it establishes |
|---|---|---|
| 1. Standard RNN | `candidates.StandardCell`; `CandidateLanguageModel(cell_type="tanh")` | Ordinary dense tanh baseline with orthogonal recurrent / Xavier input initialization and zero biases. |
| 2. Near-critical | `candidates.NearCriticalCell`; `CandidateLanguageModel(cell_type="near_critical")` | Frozen norm-controlled recurrence with configurable gap, leak, and orthogonal/identity/Householder-cycle operators. |
| 3. Protected memory | `candidates.ProtectedMemoryCell`; `CandidateLanguageModel(cell_type="protected")` | Explicit selective Walsh-coefficient writes and a projected fast complement, with mechanism-removal switches. |
| 4. Full theoretical reference | `full_reference.FrozenTanhReference`, `CorridorCreditEngine`, controlled-history and protocol helpers | Exact established forward/sensitivity algebra, chronological balanced controls, selected legal-query answers. A mathematical reference, with explicit gaps, rather than a fourth trained token model. |

The original three cells, their token wrapper, and original credit kernel
are unchanged in [model.py](model.py) and [theory_reference.py](theory_reference.py).
[frozen_sources.json](frozen_sources.json) records their hashes at
`a8cd2f11bb86c67c7fc1ae752793077f4bef493a`. Regression tests enforce these
source hashes. Historical research hashes are a provenance snapshot; they
do not prohibit subsequent owner-authorized research on other branches.

The improved token models share the original embedding, layer-normalization
placement, tied head, width, layer count, and returned-state convention.
Copying identical weights reproduces all three original recurrences. The
protected slow gate changes from retention to write probability; migrating
original weights requires negating the slow-gate weight and bias. Tests do
this explicitly. Improvements remain separate from the original controls.

## Candidate equations and interfaces

Standard: `h'=tanh(W_x x+W_h h+b)`. The recurrent matrix remains fully
trainable in a future phase. Its orthogonal initialization is an ordinary
baseline choice; no spectral constraint after future learning is implied.

Near-critical: `h'=h+alpha[tanh(W_x x+a Q h+b)-h]`, where
`a=1-gap`, default `gap=1/n`, and `0<alpha<=1`. `Q` is frozen orthogonal.
For fixed input the cell Jacobian norm is at most `1-alpha+alpha*a`.
Tanh saturation can make the actual gradient much smaller. This bound does
not include the separate inter-layer normalization/head. Gaps rounding to
zero contraction in the selected precision are rejected. Identity and
Householder-cycle alternatives are individually tested; none is presumed
better, and the latter is not the exact fourth-path operator.

Protected: `q=P h`, `u=P tanh(W_x x+W_h h+b)`,
`q'=q+w*(u-q)`, `w=sigmoid(G_s x)*write_mask`.
The fast component mixes `h-P^T q` and the proposal complement with a
coordinate gate, then projects out `P^T P` again. Consequently `P h'=q'`
when `P P^T=I`, to floating-point tolerance. An externally closed write
preserves its coefficient and its gradient path; open channels can
interfere through the proposal. The state is still exactly `n` coordinates.

The implementations batch input projections across time/layers and batch
the tied output head. Recurrence remains sequential. This reduces Python
and small-matrix call overhead, while using temporary sequence tensors.
Float32 and float64 initialization are explicit. `CandidateConfig.seed`
uses a local CPU RNG scope and leaves the caller's RNG unchanged.

`CandidateLanguageModel.forward(ids, state=None, return_history=False,
reset_mask=None, write_masks=None)` returns logits and one `[B,n]` state
per layer, with optional `[B,T,L,n]` history. Empty chunks preserve state.
Reset masks are `[B,T]` and reset each example **before** its selected
token. Write masks are `[B,T,L,R]`. No state is cached inside a model.
Gradients cross chunks unless callers explicitly use `detach_state` or
reset. Inputs, state, device, precision and mask ranges are checked.

## Mathematical reference: implemented scope

The implementation follows [unpaired-corridor equations](../../theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md),
[holding-cost lift](../../theory/codex_holding_cost_attack_20261003/PROOF.md),
[early capture](../../theory/codex_linear_dimension_frontier_20261006/PROOF.md),
and the [Route-7A local trace identity](../../theory/astra_route7a_reservoir_20261007/PROOF.md).

* `CorridorOperator` implements the exact open cycle shift, stationary
  complement, and **both** rank-two Householder terms. Independently
  assembled `U P U` matrices verify the indexing, orthogonality, forward
  action, transpose, and spectrum, including odd widths.
* `FrozenTanhReference` implements `R0=diag(a O, I_l/(100n))`, `W=I`,
  bias `.05`, coordinate-zero invariance, autonomous source equilibrium,
  and zero-start/streaming forward computation. A caller-supplied
  recurrent matrix can be checked against the norm/perturbation bounds;
  the default and all reported controlled fixtures explicitly use **R0**.
  A norm check at finite precision is not an exact dense-realization proof.
* `FourSiteGeometry` reproduces the two moving positive tracks and two
  stationary negative compensators. It rejects wrapping, terminal/front
  overlap and insufficient bath support. Full lift premises
  `n>=10^6, S<=d/100` are separately exposed and optionally required.
* `realize_four_site_history` prepares from zero, realizes prescribed
  balanced amplitudes, advances the nondriven global bath/front and source,
  counts actual-operator corrections everywhere, and resets driven sites
  to the shared nonzero ordinary state. Saturated autonomous front states
  never require inverse tanh. Realized raw inputs are detached before
  parameter differentiation. Endpoint equality and past-cube validity
  are checked numerically, rather than declared from dimensions.
* `orthonormal_probe_bank` implements the donor/survivor `W H` bank.
  `survivor_walsh` repeats each character across complete four-site tuples.
  Chronological moving support is explicit.
* `early_capture_schedule` implements writes, **one-step capture before
  correction**, low-donor tails, exact final local-trace correction,
  public clear and a final reset in the history realization. Finite
  correction gates outside the admitted interval are rejected.
* `trace_neutral_schedule` implements precharge, Route-7A three-step
  trace-neutral writes, **high donors at capture**, optional public
  release, and no complementary final clear. It matches local traces;
  complete private feedback is retained. No robust benefit is asserted.
* `CorridorCreditEngine` stores `L,H` and computes `M=L+H`, with complete
  vector `J=u^T M` and `B=v_H^T M`. It implements the exact coupled renewal
  recurrence at every chronological step; no first-order truncation,
  pairing shortcut or public-feedback substitution is used.
* `fixed_source_scan` tracks **physical** sensitivity for any chosen
  `delta R=(E V) f_s^T`, including every selected parameter column. Taking
  `V=I_r` obtains the full fixed-source slice at quadratic cost. The
  optional dense operator retains source/coordinate-zero leakage. Full
  `[n,p]` row probes also track the complete source-feature parameter action,
  including public source/coordinate-zero rows; this is checked against
  independent general recurrent directions.
* `directional_scan` implements independent `R,W,b` derivatives in raw
  units, including preparation `W,b` terms. Fixed-input autograd and
  finite differences independently verify it. It does not invent a
  normalized full-parameter robust-section theorem.
* Legal futures have supplied preactivations in `[.25,.75]`, length at
  least one, and realized frozen raw inputs. The adjoint pulls the
  `1/sqrt(n)` head through **every** future step. The selected recurrent
  group/loss ratio is exactly `1/n`; both normalizers are held fixed.
  `normalized_past_answer` evaluates a supplied query. Direct future
  injections cancel between histories only at the same endpoint, as
  checked against differentiated complete past+future replay.

This makes the established components runnable, but does not synthesize
the full asymptotic clipped continuous-ball code or certify its entire
boundary. Supplied finite queries are **lower witnesses** for a supremum,
never a computation of the supremum or of `D`. The reference is deliberately
separate from token approximation. Missing mechanisms have fail-closed
`ResearchGap` interfaces; see [LIMITATIONS.md](LIMITATIONS.md).

## Fair comparison and resource accounting

[comparison_configs.json](comparison_configs.json) defines matching token
widths 16/32/64, layer/vocabulary/seed controls, isolated recurrence options,
protected ablations, and exact finite-reference fixtures.
[validation.py](validation.py) provides both a common real-valued cell
scan and token-wrapper checks. The common scan compares equal width and
identical real inputs; path 4 consumes raw controls and has different
state semantics. It is not a parameter-matched LLM comparison.

Measured token counts at `n=32, L=2, vocabulary=97, R=8`, float32:

| Path | Trainable parameters | Buffer values | Persistent forward state per example | Estimated MACs/token |
|---|---:|---:|---:|---:|
| Standard | 7,456 | 0 | 64 values / 256 bytes | 7,200 |
| Near-critical | 5,408 | 2,048 | 64 values / 256 bytes | 7,200 |
| Protected | 10,096 | 512 | 64 values / 256 bytes | 13,344 |

These counts also match the respective original controls. Matching width
does **not** match trainable parameters: near-critical freezes `L*n^2`
entries, while protected adds gate parameters. Adding unused parameters
would conceal rather than fix this difference. A later training phase
must report both equal-width and independently budget-matched variants;
changing width changes embedding/head capacity and must be disclosed.

For vocabulary `v`, width `n`, layers `L`, channels `R`, unique token
parameter counts are:

* Standard: `v*n + L*(2n^2+3n)+2n`.
* Near-critical: `v*n + L*(n^2+3n)+2n`, plus `L*n^2` frozen buffers.
* Protected: `v*n + L*(3n^2+nR+4n+R)+2n`, plus `L*nR` mask buffers.

Default dense cell MAC estimates are `2n^2`, `2n^2`, and `3n^2+8nR`;
the shared head adds `v*n`. Multiply MACs by approximately two for
multiply/add FLOPs. Nonlinearities, normalization, memory traffic and
allocator/Python overhead are excluded. Persistent forward state is
`B*L*n`; logits cost `B*T*v` elements and requested history `B*T*L*n`.
Temporary batched projections and autograd tapes also grow with `T`.
No measured process peak-memory claim is made from tensor payload counts.

For the reference, public constants are `O(n)`; forward state is `n`.
With `p` fixed-source directions, physical sensitivity costs `n*p` values;
split selected renewal costs `2*r*p` and one public step count. `J,B` are
temporary `p`-vectors in this implementation. For `p=r`, credit storage is
quadratic. General independent `R/W` direction buffers cost another
`2*p*n^2+p*n`; tracking every parameter block explicitly would be cubic
in width. Reference arithmetic is `O(n*p)` per step; an actual dense
operator requires `O(n^2*p)` work and `n^2` extra constants. Offline raw
histories, states, gates and optional credit traces are all counted.

Theoretical independently differentiable parameter space `2n^2+n` is
reported separately from zero trainable parameters of the frozen module.
None of parameter counts, persistent-state width, tangent rank or gradient
norms is robust continuous learning-credit dimension.

## Actual CPU results

The initial original suite passed **35 tests**. The completed suite includes
all originals plus candidate, full-reference and shared-accounting checks.
The final executed count, command and timings are recorded in
[reports/TEST_RESULTS.md](reports/TEST_RESULTS.md).

Checks cover shapes, matched-weight equations, empty chunks, uninterrupted
versus streamed execution, reset and detach gradients, local RNG isolation,
float32/64 stability to 1,024 steps, analytic/finite-difference derivatives,
independent dense operators, spectra, complete renewal, balanced histories,
source/preparation terms, endpoint equality, Walsh transport, trace repair,
high-donor/no-clear recurrence, complete legal future answers and exact
parameter/state/payload accounting. An SVD tests an entire finite
two-step complementary space with varying chronological outside gates,
including front and terminal coordinates.

Deterministic cell diagnostic at width 32 with identical small real inputs
and a fixed unit reader, 1,024-step initial-state gradient norms:

| Path | Measured gradient norm |
|---|---:|
| Standard | `7.29e-7` |
| Near-critical | `3.14e-17` |
| Protected | `3.38e-2` |
| Reference | `2.98e-21` |

All were finite. These are one untrained initialization and one reader,
with unequal parameterization and different state semantics. They establish
no recall, learning-credit dimension, intelligence or inference ranking.
In particular, a frozen near-critical norm does not automatically preserve
gradients better than an ordinary orthogonal-initialized trainable cell.

The deterministic protected fixture updates one coefficient for 256 steps;
closed-channel drift is `7.11e-14` and Gram error `1.11e-16` in float64.
The same structural invariant survives substituting a random orthonormal
bank. A separate test exhibits cubic Walsh aliasing despite pairwise
sum-free labels. Thus the invariant alone does not confer Walsh-specific
novelty or learned cross-talk resistance.

The full-history fixture uses `n=2048,m=8,T=44,mT=352`. All past raw
coordinates are within the cube; max magnitude is `0.10857`, absolute
history norm `0.76855`, forward replay discrepancy `1.87e-16`, endpoint
pair discrepancy zero in this fixture, probe Gram error `2.22e-16`, and
donor local trace-match errors zero. Its one supplied legal-query pair
norm is **`1.36e-9`**, far below `2*epsilon=.002`. Four clear steps do not
certify theorem-scale clearing; source lift/asymptotic premises are false
at this width. This is an equation diagnostic with a weak finite signal.

Measured payload for that retained input/state/gate history is 2,277,376
bytes. Reference forward state is 16,384 bytes; split selected credit
is 32,736 bytes at two directions. These are tensor payloads, not RSS.

[reports/cpu_validation.json](reports/cpu_validation.json) contains the
actual per-horizon data, inventories, matched-weight discrepancies,
seven-repeat forward timing medians, scope flags, configuration and source
hashes. Timings use one CPU thread, no gradients, batch 2, 64 tokens,
float32, and two warmups. They are local measurements, not training
throughput, hardware-independent guarantees or extrapolated asymptotics.

## Independent criticism and cheapest decisive next work

| Architecture | Strongest advantage | Failure mode / known mechanisms | Distinctive-removal consequence | Evidence still needed | Cheapest future decision |
|---|---|---|---|---|---|
| Standard | Simple trustworthy dense reference; ordinary trainable flexibility. | Tanh saturation, vanishing/exploding trained recurrence; Elman RNN and orthogonal initialization are known. | Removing ordinary recurrence removes temporal state; batching only changes implementation overhead. | All token prediction/recall quality is **NOT YET TESTED**; post-training spectral behavior requires measurements. | First small separately authorized token/recall run with a standard gated control, using the frozen original and candidate. |
| Near-critical | Explicit frozen norm and exact cell-level Lipschitz control. | Contraction and saturation still erase credit; frozen features can limit adaptation. Orthogonal/unitary RNNs, reservoir computing, and leaky recurrence are known. | Removing spectral control loses the norm guarantee; identity can preserve the bound with very different mixing. | Learned usefulness, preferred gap/operator/leak, and cost/quality gains are **NOT YET TESTED**. No robust-D theorem transfers to this surrogate. | Matched gap/operator/leak comparison after the standard run; include the standard baseline's often stronger initial gradients. |
| Protected | Closed-channel selective overwrite has an explicit projection invariant and direct gradient access. | Proposal/gates can couple open channels; gate saturation may block writing; projected state need not be coordinate-bounded by one. LSTM-style gating, multiple timescales and orthogonal subspace memory are known. | Removing fast projection leaks into protected reads; removing retention loses selective persistence. Random orthogonal substitution preserves the main invariant. | Selective **learned** writing, delayed retrieval, nonlinear interference, benefit over LSTM/GRU/equal-budget projected memory are **NOT YET TESTED**. Walsh-specific benefit needs stronger proof or data. | Tiny delayed recall/selective overwrite task with projection/retention/feedback/basis ablations, with equal-width and equal-budget gated controls. |
| Theoretical reference | Faithful chronological algebra and normalized fixed-input query oracle; no dropped unpaired renewal. | Extremely large theorem thresholds, weak finite signals, prescribed controls and source feature; dense differentiation is costly. Householder transport, Walsh characters, inverse control, eligibility sensitivities and Borsuk–Ulam are existing tools. | Removing early capture can expose stored credit to correction drift; dropping unpaired feedback changes the actual equations. Decomposing these known operations does not by itself settle the scoped robust-dimension/cost property. | Strict-budget linear D, unrestricted Route-6/7A, practical onset and a coherent exact token adapter all remain open; token usefulness is **NOT YET TESTED**. | Untrained normalized fixed-input sensitivity/collision checks for the no-clear alternative, followed by a mathematical joint-section or compression proof. Do not train this reference as an LLM. |

Classify paths 1–2 as known recurrent mechanisms and path 3 as a conceptual
architecture candidate assembled from known operations. The closed-channel
invariant has an ordinary orthogonal-coordinate implementation; no new
primitive is established. Path 4 is a mathematical reference for a scoped
research property, not proof of a new computational primitive or of model
superiority. Relevant prior-art anchors are Elman (1990), Jaeger (2001),
Hochreiter–Schmidhuber LSTM (1997), orthogonal/identity initialization
(Le et al., 2015), unitary RNNs (Arjovsky et al., 2016), and Clockwork RNNs
(Koutnik et al., 2014). This mapping is a conservative mechanism comparison,
not an exhaustive priority/novelty certification.

**Recommendation:** begin the later authorized training phase with the
standard candidate and an ordinary gated RNN control; then prioritize the
protected model with its ablations. Near-critical variants merit a small
controlled comparison rather than a presumption of improvement. Keep path
4 on the mathematical validation track until token transitions and the
missing proof obligations are specified. A simpler model winning is a
valid result. No training was started in this work.

## Reproduction

Python 3.12 and isolated CPU dependencies used for this report:

```bash
python -m venv /tmp/rnn-architecture-venv
/tmp/rnn-architecture-venv/bin/pip install 'torch==2.14.1+cpu' --index-url https://download.pytorch.org/whl/cpu
/tmp/rnn-architecture-venv/bin/pip install 'pytest==9.1.1'
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /tmp/rnn-architecture-venv/bin/python -m pytest -q prototypes/rnn_llm_architecture
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /tmp/rnn-architecture-venv/bin/python -m prototypes.rnn_llm_architecture.validation --output /tmp/rnn-validation.json
```

Run from repository root. The CLI only performs forward/backward diagnostics;
it contains no optimizer or weight updates. Benchmark times vary; source
hashes and deterministic numerical results establish the report's scope.
