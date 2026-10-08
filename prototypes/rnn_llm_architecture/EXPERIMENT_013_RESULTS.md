# Experiment 013 — results: learned slow-write gate versus fixed write rate

**Status: complete.** Phase 1 audit (no training), Phase 2 exploratory diagnostics on 7 deterministically reproduced runs,
Phase 3 confirmatory fixed-gate matrix: **18/18 runs complete**, 0 skipped, 0 failed, 3,000 updates each. New training
wall-clock: Phase 2 reproduction 287 s + pilot 33 s + confirmatory 644 s = **≈ 16 min** (budget 60 min); no launch held by
the memory/temperature guards. Plan: [`EXPERIMENT_013_PLAN.md`](EXPERIMENT_013_PLAN.md), committed in `52430c1` before the
confirmatory matrix. Synthetic four-slot binary task; 9 runs per condition; descriptive, not statistically definitive;
**no architecture-level, novelty or formal learning-credit claim.** `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Evidence

| what | where |
|---|---|
| Phase 1 audit (autograd liveness, initial gates, mask orthonormality, init identity, stream statistics) | [`reports/experiment_013/audit_phase1.json`](reports/experiment_013/audit_phase1.json) (`audit_013.py`) |
| Phase 2 reproduced runs (bit-for-bit vs Exp 012) + weights at 0–3,000 updates | `reports/experiment_013/reproduced/`, `reports/experiment_013/weights/` |
| Phase 2 / Phase 3 diagnostics (gates by token, coefficients, perturbation gain, probes) | `reports/experiment_013/diagnostics_phase2.json`, `diagnostics_confirm.json` (`diagnose_013.py`) |
| Phase 3 raw per-run JSON + logs, final weights | `reports/experiment_013/confirm/`, `reports/experiment_013/weights_confirm/` |
| Generated tables, summary, learning-curve figure | [`confirm/tables.md`](reports/experiment_013/confirm/tables.md), `confirm/summary.json`, `confirm/figures/learning_curves_A_B_C_D.png` |

Regenerate: `python -m prototypes.rnn_llm_architecture.experiment_013_report prototypes/rnn_llm_architecture/reports/experiment_013/confirm prototypes/rnn_llm_architecture/reports/experiment_012`.

## Phase 1 — established by code inspection and autograd

- Coefficient update per layer: `c_t = (1 − g_t)⊙c_{t−1} + g_t⊙M tanh(W_x x_t + b + U h_{t−1})`, `g_t = sigmoid(W_g x_t + b_g)`, with
  Walsh rows `M` orthonormal (deviation 6e-8). This is a coupled input/forget (GRU-update-gate-style) convex update on a fixed
  8-dimensional subspace; the 24-dimensional complement is a separate GRU-style convex update with retention gate `sigmoid(W_r x + 1)`.
  The gate reads only the layer input `x_t`, not the state.
- `retain_slow=False` sets `g_t ≡ 1` (`c_t = M p_t`, no slow memory). `slow_gate` is still computed but receives **no gradient**:
  **528 dead parameters; 7,488 live of 8,016 allocated.** The fixed-gate controls B and C have the same 7,488 live parameters.
- `protected` and `protected_no_retain` start from **identical weights**; the Experiment 012 comparison therefore removed retention,
  the slow time constant, gate learnability/input dependence and 528 trainable parameters **simultaneously**, and could not isolate
  the benefit of learning the gate.
- The initial gate is **not** the constant `sigmoid(−3)`: Xavier-initialized `W_g` gives layer-0 gates of 0.025–0.084 across task tokens.
- The three training streams have essentially identical aggregate statistics (rewrites, varied fraction, never-rewritten slots).

## Phase 3 — confirmatory fixed-gate matrix (preregistered)

| cond | slow-write gate | live params | learned (onset) | success | mean whole-varied @64 / 128 / 256 / 512 | mean per-slot@64 |
|---|---|---:|---:|---:|---|---:|
| **A** `protected` (Exp 012, reused) | learned `sigmoid(W_g x + b_g)` | 8,016 | **6/9** | **2/9** | 35.6 / 36.2 / 35.2 / 26.4 % | 81.9 % |
| **B** `protected_fixed_0474` | constant 0.0474 = `sigmoid(−3)` | 7,488 | 1/9 | 0/9 | 3.7 / 3.7 / 3.9 / 3.5 % | 69.1 % |
| **C** `protected_fixed_005` | constant 0.005 | 7,488 | 4/9 | 1/9 | 23.1 / 22.0 / 18.2 / 13.0 % | 76.9 % |
| **D** `protected_no_retain` (Exp 012, reused) | constant 1 (forced overwrite) | 7,488 | 0/9 | 0/9 | 0.0 / 0.0 / 0.0 / 0.1 % | 67.6 % |

Validity: B/C start from the exact `protected` weights of their init seed; only the gate output differs (tests: g = 1 reproduces D
bit-for-bit; the training loop reproduces Experiment 012 bit-for-bit; coefficient equation checked). Six A cells and one D cell were
re-run with this code and matched Experiment 012 exactly, so reusing A and D is valid.

**3 × 3 whole-varied@64 (outcome, onset); rows = init seed, columns = data seed**

| init \ data | A 17 | A 29 | A 43 | B 17 | B 29 | B 43 | C 17 | C 29 | C 43 |
|---|---|---|---|---|---|---|---|---|---|
| **17** | 0.2 P | 0.0 P | 0.2 P | 0.0 P | 0.0 P | 0.0 P | 0.0 P | 0.0 P | 0.0 P |
| **29** | 25.2 Pa (1900) | 12.4 Pa (1200) | 39.9 Pa (1300) | 0.0 P | 0.0 P | 0.0 P | 0.2 P | 12.4 Pa (1550) | 39.0 Pa (2800) |
| **43** | 42.9 Pa (1850) | **100 S** (1550) | **99.5 S** (2250) | 0.0 P | 33.3 Pa (1800) | 0.0 P | 47.0 Pa (1200) | 9.6 P | **100 S** (1300) |

D: all nine cells plateau_only (0.0–0.2 %).

**Paired comparisons by the preregistered rule** (X outperforms Y ⇔ higher class in ≥ 4/9 cells, lower in ≤ 1, and ≥ 20 points mean
whole-varied@64; comparable ⇔ neither outperforms and learned/success counts within 1):

| X vs Y | X higher / lower class (cells) | Δ mean wv@64 | learned X/Y | success X/Y | verdict |
|---|---|---:|---|---|---|
| A vs B | 6 / 0 | +31.9 | 6/1 | 2/0 | **A outperforms B** |
| A vs C | 2 / 0 | +12.5 | 6/4 | 2/1 | **inconclusive** |
| A vs D | 6 / 0 | +35.6 | 6/0 | 2/0 | A outperforms D |
| C vs D | 4 / 0 | +23.1 | 4/0 | 1/0 | **C outperforms D** |
| B vs D | 1 / 0 | +3.7 | 1/0 | 0/0 | comparable |
| B vs C | 1 / 4 | −19.4 | 1/4 | 0/1 | inconclusive (C better in 4 cells, but the 20-point threshold is missed by 0.6 points) |

Additional descriptive facts: C reached onset *earlier* than A in its two shared learning cells with init 43 (43/17: 1200 vs 1850;
43/43: 1300 vs 2250) but stayed on the plateau in 43/29 where A succeeded. C's single success transfers like A's
(whole-varied 100 / 99.8 / 87.5 / 48.1 % at 64–512 tokens vs A's successes 99.8 / 99.8 / 95.1 / 55.8 %). Under strong fixed
retention, rewritten slots are recalled *better* than never-rewritten ones (80.7 % vs 74.2 % at delay 64), so slow retention did
not prevent updating. **Init 17 never learned under any gate condition (0/12 across A–D)**; init 43 was the best row in A, B and C.

## Phase 2 — gate and memory dynamics (EXPLORATORY; reproduced weights, then all Phase 3 weights)

- **Layer-0 gates stay at their initial level with no write selectivity.** In all six learned-gate runs the layer-0 gate is
  0.038–0.056 on every token category (marked value / filler ratio 1.0–1.35), implying a gate-only half-life of 13–18 tokens.
- **Layer-1 gates change but not in a consistent selective way.** The marked-value gate rises from ≈ 0.05–0.11 at initialization to
  0.15–0.18 after training in every run; the filler gate closes (0.02–0.03) in some runs (29/29 partial, 43/29 success, and 0.044 in
  the *failed* 17/17) but not in others (0.12–0.17: 43/43 success, 43/17 partial, 17/43 failed). Write selectivity is therefore neither
  necessary for success (43/43) nor sufficient (17/17).
- **Information is absent rather than unread in the learned-gate runs.** Linear probes on the pre-query state match the model's readout
  within ≈ 2.5 points in all reproduced runs (e.g. failed 0.67–0.70 vs readout 0.67; success 1.000 vs 1.000), also at 256 tokens.
  The probe exceeds the readout by 4–8 points in three fixed-gate runs (B 43/29, C 29/43, C 43/29), a modest readout gap only seen there.
- **Recall is not explained by linear retention.** A small layer-0 perturbation after the prefix shrinks by ≈ 10× over 64 tokens and
  ≈ 1,000–3,000× over 256 tokens in learned-gate runs, yet successful runs recall 95–100 % at 256 tokens: values appear to be held by
  contracting, attractor-like dynamics rather than by near-lossless slow retention. With fixed g = 0.005 the protected-subspace gain stays
  ≈ 0.9 (near-lossless), but length transfer is no better than A's.
- **The successful-versus-failed initialization difference is NOT explained.** A candidate marker — initial perturbation gain, which ranks
  43 > 29 > 17 under A and B, matching success — is **falsified** by condition C, where the order reverses (17: 1.47 > 29: 1.33 > 43: 1.30)
  while init 17 still never learns.

## Answers

1. **Does the original learned gate contribute to successful learning?** Relative to freezing the gate at its initial bias, **yes**: A
   outperforms B (6/9 vs 1/9 learned, 2 vs 0 successes, higher class in 6 cells, lower in none). But A does **not** outperform a slower
   fixed rate (A vs C inconclusive), and the diagnostics show no consistent input-dependent write selectivity. The most economical reading is
   that what matters is the **effective write rate the model ends up with** (learned gates move it; layer-1 value gates triple), not adaptive,
   token-selective writing. Alternatives not excluded: A's 528 extra trainable parameters, and its token-dependent *initial* gate function
   (0.025–0.084) versus B's constant.
2. **Is fixed retention sufficient?** **Not established, not excluded.** g = 0.0474 is insufficient (≈ forced overwrite); g = 0.005 recovers
   much of A (4/9 learned, 1 success, outperforms D) but is not "comparable" by the preregistered rule (learned 6 vs 4). The **adaptive-write
   hypothesis is unsupported** by this experiment (A fails to outperform C), and the fixed-rate-sufficiency hypothesis is unresolved.
3. **Are successful vs failed initializations explained?** **No.** The init effect persists without any gate learning (init 17: 0/12 learned in
   A–D; init 43 best in A, B, C), so it resides in the non-gate weights. The one candidate marker tested was falsified.
4. **Hypotheses:**
   - *Merely retaining state* — **falsified as sufficient**: B retains at 0.0474 and is comparable to forced overwrite. Retention helps only at a
     slower rate (C outperforms D).
   - *Slow fixed memory-update rate* — **partially supported**: 0.005 recovers most learning; equivalence to the learned gate unresolved.
   - *Learned input-dependent write gates* — **unsupported**: no advantage over C; no consistent token selectivity; selectivity neither necessary
     nor sufficient in the reproduced runs.
   - *Other recurrent dynamics* — **supported as the residual explanation, mechanism unknown**: initialization of non-gate weights dominates;
     memory is attractor-like rather than linearly retained.
   - Exploratory "initial perturbation gain predicts success" — **falsified**.
5. **Strongest remaining argument for a distinctive advantage:** within the protected family, learning the slow write rate (or using a slow
   enough fixed one) is what separates learning from not learning four slots under this budget. That is not distinctive: the coefficient
   update is a GRU-style coupled gate on a fixed subspace, and in Experiment 012 an ordinary GRU-24 learned at least as often (8/9 learned,
   2/9 success, 40.4 % vs A's 6/9, 2/9, 35.6 %). **No evidence here that the protected mechanism offers anything beyond ordinary gated
   recurrence** on this task.

## Limitations

Nine runs per condition, one per cell, three init and three data seeds; the paired rules are coarse thresholds and two verdicts
(A vs C, B vs C) are inconclusive by small margins; only two fixed rates were tested; per-layer or per-channel fixed rates and A's
initial gate function were not matched; diagnostics are exploratory and cover 7 reproduced + 18 fixed-gate runs; probes are linear; the
perturbation measure covers layer 0 only. Local execution (PyTorch 2.13.0+cu130, CUDA hidden, Python 3.11.9); no hosted replication.
Experiments 001–012 code and evidence, frozen files and `AGENTS.md` are unchanged; nothing was pushed.
