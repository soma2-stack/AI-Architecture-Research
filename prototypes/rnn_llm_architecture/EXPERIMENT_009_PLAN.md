# Experiment 009 — why does independent two-slot memory fail?

**Status:** preregistered before the confirmatory run. Phase A (exploratory
diagnostics) is complete and archived in
[`reports/experiment_009_exploratory/`](reports/experiment_009_exploratory/README.md).
Phase B (confirmatory) has not been run when this file is committed.
**Scope:** synthetic supervised CPU study. Not a language model, not a
novelty claim, and not evidence about the formal target
`D=Omega(n), mT=o(n^(3/2))`, which remains **OPEN**.

## 1. Question

Experiments 004–008 found that the protected RNN (and GRU/LSTM controls)
almost never retrieves *both* A and B when their final values differ at
delay 64 (≈0–7% A≠B both-correct, below the 25% independent-guess rate),
while single tagged bits survive 256 tokens. Candidate causes named by the
owner: interference between stored values, nonselective protected writes,
insufficient addressability, information loss across transitions, poor
gradient credit assignment, or a task/readout/optimization limitation.

## 2. Phase A findings (exploratory, mostly seed 17; not confirmatory)

All numbers are held-out A≠B both-correct unless stated; raw outputs are in
the exploratory folder.

1. **Last-write-wins signature (D1).** Exp-005-schedule protected models at
   delay 64 (seeds 17, 29) give the same answer to both queries on 96–99.5%
   of histories. Untouched-slot accuracy is 100% when the untouched value
   equals the update value and 28–34% when it differs.
2. **Layer-0 slow gates never train (D3).** After 200 updates every layer-0
   protected gate is ≈0.04–0.09 on every token class and identical for A- and
   B-updates — the initial `sigmoid(-3)`. Successful short-delay models
   (delay 16, 350 updates) learned sharply slot-routed *layer-1* gates
   (e.g. 0.71 vs 0.01 for A vs B updates) but left distractor gates at ≈0.1.
3. **Gradient conflict at the plateau (D4).** On failed delay-64 models the
   gradients of the updated-slot and untouched-slot query losses have cosine
   −0.61 / −0.85 (all parameters): improving one query type hurts the other,
   the signature of the symmetric last-write saddle analysed in §3.3.
4. **Oracle factorial (legacy task, seed 17, 300 updates).** No mask 0.8%;
   *exact closure on non-write tokens without slot routing* (`tag`) 100% at
   64/128/256; slot routing with learned leak elsewhere 9%; both 100%.
   Slot routing is not the bottleneck; leak between writes is.
5. **Budget, not capacity.** With **1500** updates instead of 150–350, the
   *unchanged* original protected model reaches 100% at delay 64 in **3/3
   seeds** (17, 29, 43) after a loss plateau (≈0.46) lasting until update
   ≈700–1000. GRU-w32: 1 seed solved, 1 partial (54%), 1 still on the plateau.
   LSTM-w32: 0/2. Learning rate 0.01 did not solve it within 300 updates.
6. **Length transfer depends on the training task.** Legacy-trained protected
   models (update always at the midpoint) transfer poorly: 128 → 33/26/47%.
   Trained on the randomized task below (2000 updates), protected seed 17
   scored 100% at 32, 64, 128, 256 **and 512** tokens.
7. **Solutions are not gate-closure memories.** In every successful learned
   model, the implied surviving fraction after 512 non-write tokens
   (`exp(512·mean log(1-g))`) is 1e-11 to 1e-200 — GRU overwrites ≈50% of every
   unit at every token and still scores 100% at 512 (seed-29 pilot). Memory
   is carried by recurrent dynamics, not by closed protected channels.
8. **Learned exact-closure gates do not reproduce the oracle.** A
   straight-through hard gate (`protected_hard`) never opened in layer 0
   (100% exactly zero on all token classes) and solved the task only through
   other pathways; hard gate + token shift failed to train; hard-keep GRU had
   pre-clip gradient norms up to 1.3e7 and failed.

## 3. Mathematical analysis

**3.1 Input-only gates cannot route in layer 0.** The protected slow gate is
`g_t = sigmoid(G x_t + b)`. At a value token, `x_t` is the embedding of
`BIT0`/`BIT1` regardless of whether `WRITE_A`, `WRITE_B` or a distractor
preceded it, so layer-0 gates are identical for A-writes, B-writes and
unmarked bits. Routing therefore has to happen through the proposal (content)
or in layer 1, whose input `LN(h^0_t)` does carry the preceding token. The
2-layer model is *expressively* capable of routed writes (observed at delay
16), so addressability is a learnability, not an expressivity, limit.

**3.2 Sigmoid gates leak exponentially.** For a passive slow coefficient
`q_t = (1-g_t) q_{t-1} + g_t u_t`, the contribution of a write at time `s` is
attenuated by `prod_{t>s}(1-g_t)`. With the initial `g≈0.047`, a value
written 64 tokens before the query keeps `0.953^64≈4.6%` of its (already
0.047-scaled) write, while independent distractor proposals accumulate a
stationary noise of `0.047/sqrt(1-0.953²)≈0.15` proposal norms. A write 32
tokens before the query keeps `0.953^32≈21%`, ≈4.6× more than the initial
writes,
so the earliest learnable function is "answer the last write". Exact
retention over unbounded `T` by gate closure needs `g=0` exactly, which a
sigmoid never reaches; Adam bounds each logit's movement to about
`lr·steps·(1+||x||_1)`, so a 200-update budget cannot make gate closure
sharp. The oracle `tag` mask supplies exact zeros from initialization, giving
an undecayed, noise-free signal path — consistent with Phase A item 4.

**3.3 Symmetric last-write saddle.** Under a slot-agnostic write and a
query-agnostic readout, a perturbation that closes the update gate for the
non-addressed slot helps untouched-slot queries and hurts updated-slot
queries by the same first-order amount, and a query-specific readout has
nothing slot-specific to read. Escape needs second-order (joint) movement, so
the loss plateaus; this is the classic saddle/plateau phenomenon (Saxe et al.
2014; Dauphin et al. 2014). Short delays break the symmetry because the fast
state still carries slot-specific information to the query.

**3.4 Passive integrator versus attractor.** A passive leaky integrator has
no restoring force: any per-token leak `epsilon` destroys the bit after
`~1/epsilon` tokens, and noise added to the state is never removed. A
nonlinear recurrent map with stable fixed points for each (A,B) value pair
corrects small perturbations and can hold the pair indefinitely *without*
gate closure (bistable latching: Bengio, Simard & Frasconi 1994; Vecoven et
al. 2021). Bengio et al. also show robust latching implies vanishing
gradients, which predicts a slow, plateau-limited learning phase (§3.3).

## 4. Hypotheses and falsifiers (decision rules fixed in advance)

A run "solves" length `L` when held-out A≠B both-correct ≥ **0.90**
(512 histories, ≈256 unequal pairs). Seeds 17, 29, 43, 59, 71.

- **H1 — optimization budget/plateau.** Earlier failures were stopped on a
  plateau. *Supported* if the original `protected_w32` solves the training
  length (64) in ≥3/5 seeds within 2000 updates while scoring <0.25 at the
  first checkpoint (250 updates, i.e. the old budget range).
  *Falsified* if ≤1/5 seeds solve 64.
- **H2 — fixed-timing training task causes length failure.** *Supported* if,
  on the **legacy** evaluation task, two-slot-trained `protected_w32` beats
  legacy-trained `protected_w32` by ≥20 percentage points (mean) at 128 and
  256 with the same sign in ≥4/5 seeds. *Falsified* if the mean difference is
  <10 points or the sign agrees in ≤2/5 seeds.
- **H3 — protected-channel retention is not the mechanism used.**
  *Supported* if `protected_no_retain_w32` (slow gate forced open) solves 64
  in at least as many seeds as `protected_w32` minus one **and** every solved
  `protected_w32` run has implied 512-token non-write retention <0.01 in both
  layers. *Falsified* otherwise.
- **H4 — attractor (error-correcting) memory.** *Supported* for an
  architecture if, in ≥3 of its seeds that solve 64, A≠B accuracy after state
  noise of 0.5×RMS **plus** a 64-token distractor tail is ≥ the accuracy
  queried immediately after the same noise, and ≥0.9. *Falsified* if
  noise damage persists or worsens after the tail.
- **H5 — learned exact closure supplies the oracle's benefit.** *Supported*
  if `protected_hard_w32` or `protected_hard_shift_w32` reaches 0.9 at 64 no
  later than the `tag` oracle's median checkpoint + 250 updates in ≥3/5
  seeds **and** solves 512 in ≥3/5 seeds. *Falsified* otherwise (expected
  from Phase A item 8).
- **H6 — standard gated RNNs.** Descriptive comparison of solved-seed counts
  per length, first checkpoint ≥0.9, parameters, state size and runtime for
  GRU/LSTM (equal width 32 and ≈parameter-matched GRU-24/LSTM-20) against the
  protected family. "Better" requires a higher solved-seed count at 512 *and*
  no worse count at 64.

## 5. Task

`make_two_slot_batch` (body length `delay`, total prefix `4+delay`):
`WRITE_A a`/`WRITE_B b` in random order; body of benign distractors (ids
8–13) with 25% of positions replaced by **unmarked bit tokens** (same ids as
values: conflicting information); **1–3 marked updates** `WRITE_X v` at
uniformly random non-overlapping positions; then `QUERY_A` or `QUERY_B`.
Labels come only from `replay_slots`, which writes slot X at a bit token iff
the immediately preceding token is `WRITE_X`; tests cross-check it against
the generator. Both queries are asked of the identical prefix. About 50% of
histories have A≠B; random update positions remove fixed-timing shortcuts.

Shortcut baselines on the same held-out histories (A≠B both-correct):
random guessing (≈25%), last marked write (0%), last bit token (0%),
initial values only (≈38%), sticky address — unmarked bits written to the
last named slot (≈38%). The legacy Experiment 004 generator is also
evaluated (64/128/256) for comparability.

## 6. Arms (all CPU, 2000 AdamW updates, lr 0.002, clip 1, batch 16 histories × 2 queries)

| Arm | Params | State floats | Purpose |
|---|---:|---:|---|
| `protected_w32` | 7,504 | 64 | original control |
| `protected_no_retain_w32` | 7,504 | 64 | mechanism removal: slow gate forced open |
| `protected_shift_w32` | 8,016 | 128 | address access: gate also reads `x_{t-1}` (soft) |
| `protected_hard_w32` | 7,504 | 64 | learned exactly-closable gate (straight-through) |
| `protected_hard_shift_w32` | 8,016 | 128 | both |
| `tanh_w32` | 4,864 | 64 | ordinary RNN |
| `gru_w32`, `lstm_w32` | 13,376 / 17,600 | 64 / 128 | equal-width standard controls |
| `gru_w24`, `lstm_w20` | 7,728 / 7,160 | 48 / 80 | ≈parameter-matched standard controls |
| `gru_keep3_w32` | 13,376 | 64 | GRU with keep-gate bias +3 (retention prior) |
| `gru_hard_w32` | 13,376 | 64 | GRU with hard straight-through keep gate |
| `oracle_tag_protected_w32` | 7,504 | 64 | **upper-bound diagnostic**: true write events, exact closure elsewhere |
| legacy-trained `protected_w32`, `gru_w32` | — | — | H2: trained on the Exp-004 generator |

All protected-family arms start from the identical seeded weights of
`protected_w32`; token-shift weights start at zero. Every arm sees the same
training histories per seed. No learned arm receives write masks; the oracle
arm is reported in a separate table and never ranked as an architecture.

## 7. Measurements

Per run: A≠B both-correct (primary) and overall/per-slot accuracy at
delays 32, 64 (trained), 128, 256, 512; learning curve every 250 updates;
first checkpoint ≥0.9 and ≥0.99; legacy-task scores; frozen-state linear
probe (fit at 64 on 2048 histories, tested at 64 and unchanged at 256);
gate statistics by token class with implied 512-token retention;
state-perturbation recovery (noise 0.5 and 1.0 × feature RMS, immediate vs
after a 64-token distractor tail); loss trace; max pre-clip gradient norm;
NaN/inf detection; parameter count; recurrent-state floats; runtime.

## 8. Resources and integrity

CPU only (`CUDA_VISIBLE_DEVICES=''`), one thread per worker, 4 workers,
75 runs, global wall cap 4,500 s; unfinished runs are recorded as
`wall_budget`, errors as `error: ...`. Output JSON is exclusive-create and
records source SHA-256 hashes, environment and per-run status. The full
prototype test suite must pass first. A GitHub Actions workflow
(`rnn-exp009-cpu.yml`) replicates the same configuration per seed on hosted
CPUs and uploads raw JSON. No GPU, no external data, no change to earlier
architectures, experiments, theory claims, `AGENTS.md` or `main`.

## 9. Theory boundary

`event_gated.py` changes the recurrence, so these formal assumptions no
longer hold for those arms: (i) the hard gate's forward map is piecewise
constant in its parameters and the straight-through backward pass is a
surrogate, not the true gradient, so no learning-credit quantity defined
through actual gradients applies to it; (ii) closed channels contribute
exact identity Jacobian blocks, unlike contracting or near-critical dense
tanh transitions; (iii) token shift enlarges the recurrent state by `w`
floats per layer, so state dimension is no longer `n`; (iv) all weights are
trained, unlike the frozen-family theorem setting. Nothing here bears on
`D=Omega(n), mT=o(n^(3/2))`.

## 10. Prior art for the mechanisms tested

Exact-copy binary update gates with straight-through gradients: Skip RNN
(Campos et al., 2018), HM-RNN COPY (Chung, Ahn & Bengio, 2017),
straight-through estimator (Bengio, Léonard & Courville, 2013). Token shift /
short causal convolution before gating: RWKV (Peng et al., 2023), H3 (Fu et
al., 2023), Mamba (Gu & Dao, 2023). Gate-bias retention priors: chrono
initialization (Tallec & Ollivier, 2018). Attractor latching and its gradient
cost: Bengio, Simard & Frasconi (1994); bistable recurrent cells (Vecoven,
Ernst & Drion, 2021). Addressed slot or key–value memory that the owner's
"explicitly addressed protected memory" would approach: NTM (Graves et al.,
2014), Recurrent Entity Networks (Henaff et al., 2017), fast-weight / delta
rule memories (Schlag, Irie & Schmidhuber, 2021; Yang et al., 2024). None of
the Experiment 009 variants is claimed as a new primitive or architecture.

## 11. Reproduction

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' python -m pytest -q -o addopts= \
  -p no:cacheprovider prototypes/rnn_llm_architecture
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' python -m prototypes.rnn_llm_architecture.experiment_009 \
  --output prototypes/rnn_llm_architecture/reports/experiment_009_results.json \
  --progress /tmp/rnn-exp009-progress.jsonl \
  --variants protected_w32,protected_no_retain_w32,protected_shift_w32,protected_hard_w32,protected_hard_shift_w32,tanh_w32,gru_w32,lstm_w32,gru_w24,lstm_w20,gru_keep3_w32,gru_hard_w32,oracle_tag_protected_w32 \
  --legacy-variants protected_w32,gru_w32 --seeds 17,29,43,59,71 --steps 2000 \
  --workers 4 --max-wall-seconds 4500
```
