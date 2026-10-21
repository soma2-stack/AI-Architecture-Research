# PR #35 practical memory experiment — final CPU report

**Current disposition (2026-10-21): FROZEN. The proposed 3,000-update rerun is
WITHDRAWN; all historical next-step suggestions below are inactive.** Check
[the canonical claim register in PR38](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md)
before proposing any work.

**EXPERIMENTAL RESULT: the trainable surrogate ran, but did not improve memory.**
All 123 runs completed 600 updates, across 3 seeds. No architecture or breakthrough claim.
[Draft PR #36](https://github.com/soma2-stack/AI-Architecture-Research/pull/36) /
[successful hosted run](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39436715677).

## Resume/status
- Search lens: practical learned recall from PR #35-inspired balanced pairs and shared features.
- Stage: completed frozen CPU screen; results and negative outcomes preserved.
- Strongest surviving candidate: none established by this screen.
- Closed: this surrogate's claimed memory advantage at 600 updates; primitive/unique pair invariant claim (exact ordinary-gated reduction).
- Unresolved: longer-budget optimization, precision during training, and an explicit learning-credit-state architecture faithfully bridging PR #35 to prediction.
- Exact next action: preregister a small two-fact budget comparison up to 3000 updates, including an exactly equivalent compressed-state implementation and GRU controls; separately define the state/cost of a credit-trace bridge before testing it. No next experiment has been launched.

## PASS / FAIL / INCONCLUSIVE

| Question | Result | Actual evidence |
|---|---|---|
| Working trainable model? | **PASS** | 123/123 runs, 73,800 optimizer updates, no skipped or nonfinite-loss/gradient stops |
| Reused test integration? | **PASS** | 109 selected tests pass in each seed job (2.89/5.31/4.52 s); small author reference simulation also completed |
| Fair data/budgets? | **PASS** | Source hashes identical; one training-stream hash per seed/task across all models/widths; identical held-out sets; 600 updates/model |
| Better recall? | **FAIL at this budget** | 0/36 conditions satisfy the fixed three-seed advantage criterion; even 0/108 single-seed conditions beat all 3 gated controls by 5 points |
| Reliably remember the tested fact counts? | **FAIL for pair model** | None of 2/4/8 facts at widths 16/32/64 and any tested delay meets 95% bit+90% whole accuracy in all 3 seeds |
| Useful scaling? | **FAIL under the fixed criterion** | Width 64 does not improve reliably over 32; no size reaches the recall threshold |
| General capacity ceiling / theorem practicality? | **INCONCLUSIVE** | Only 600 updates, finite task/size grid, and a deliberately relaxed forward-memory surrogate; not a faithful trained theorem construction |
| No numeric problems? | **INCONCLUSIVE overall** | No nonfinite outputs; float64 evaluation changes 0 predictions in the precision subset, but literal clipping/conditioning is severe and low-precision training was not tested |

The criterion for exploratory advantage was a 5 percentage-point whole-record gain over equal-width GRU, approximately parameter-matched GRU, and equal-width LSTM, in **every** seed at a condition. This is a descriptive screen, not a significance test.

## What was built

An isolated PyTorch token RNN, [model.py](../../prototypes/pr35_memory/model.py), with learned embedding, write gates, proposals, recurrent fast state and tied output head. Its memory is stored as (p,-p); a fixed row-normalized Vandermonde map shares latent proposals across pairs.
The existing PR #23 token interface, task generator, replay/labels, query expansion, metric functions, tanh/protected implementations, GRU and LSTM wrappers were reused unchanged.
GRU parameter matches are width 10/18/34 against pair widths 16/32/64 (1,020/2,700/8,364 parameters versus 1,011/2,757/8,457; errors +0.89%/-2.07%/-1.10%).

Ablations remove shared coding, replace unit carry by 1-1/width, or remove pair retention. The latter retains counted but gradient-unused gate parameters; the direct proposal ablation has 2,910 parameters versus 2,757, so it is not a perfectly parameter-matched causal isolation.

CreditLab at e8772557a4f266a6ac9bac7cc2d40841509c1bc4 was inspected. It contained a tiny tanh model/foundation tests and a design-only delayed-credit configuration, but no executable delayed-memory training/evaluation harness to reuse. PR #23 supplied the working infrastructure.

## Exact theorem versus approximation

PR #35's proof and simulations were read at aa47ca5ec782d4a70047793d00a44f2f47816f49.
The owner-supplied independent audit of b984ef9347219d62db4dfd39f8f2e263317c9a33 was read from the specified local AUDIT.md. It accepts the principal exact-real dense-transfer and cube-root results and flags severe conditioning, noninjectivity if claimed, and auxiliary scope/rounding issues corrected in the current PR.

The theorem distinguishes **parameter sensitivities after common hidden endpoints**, using frozen prescribed dense tanh dynamics, tiny all-ones coupling, controlled inputs of support<=3, sparse legal pulses and a shared clipped saturation code. Its D is not the number of independently recallable bits.
A deterministic forward model starting at that common endpoint cannot identify the past from the endpoint alone.
The practical surrogate retains balanced signs/shared features but relaxes the dense matrix, input/schedule/legal-query contract, giant clipping gain, exact common endpoint, and primary carry a<1. It does not retain the theorem's credit tensor, gather mechanism or guarantee.

The paired mechanism has an exact ordinary gated-memory implementation on contrasts alone. This preserves reachable transitions, predictions and original-parameter gradient paths at lower state cost. [Full mechanism analysis](MECHANISM.md) answers all 18 candidate questions. No distinctive computational primitive or non-preserved architecture property was found.

## What it remembered

Means over seeds 17/29/43, each with 256 held-out histories and every slot queried. Each model starts fresh on each history.
The initial task includes 16 distractor tokens with random updates/decoy values. Longer tests append 48/240/1008 tokens **without writes**.
Thus labels/prefixes stay fixed across delays; the tests cannot hide recent answer writes in a longer sequence.
The old PR #23 results used longer update bodies, so those historical scores are not directly compared numerically here. All baseline scores below are fresh runs of its implementations on the same new protocol.

Two binary facts, width 64:

| Body tokens / guaranteed no-write tail | Pair: bit / whole | GRU 64: bit / whole | Matched GRU 34: bit / whole | LSTM 64: bit / whole |
|---|---:|---:|---:|---:|
| 16 / 0 | 74.4% / 50.8% | 97.1% / 94.3% | 77.0% / 54.2% | 86.8% / 73.7% |
| 64 / 48 | 54.5% / 29.9% | 87.6% / 75.1% | 76.5% / 53.6% | 75.7% / 51.3% |
| 256 / 240 | 50.2% / 25.5% | 76.9% / 53.8% | 52.4% / 28.4% | 76.2% / 52.3% |
| 1024 / 1008 | 50.7% / 25.9% | 66.1% / 40.8% | 51.0% / 26.2% | 75.7% / 51.3% |

At body 64, pair whole-record scores are 33.20%/26.56%/30.08% across seeds. GRU 64 scores are 91.41%/56.64%/77.34%.
The pair retains 1.090 of 2 bits correct on average at this condition, including chance correctness; the chance-adjusted descriptive excess is 0.180 bits.
After the 1008-token guaranteed hold, pair bit accuracy is 50.65% and whole-record accuracy 25.91%, close to 50%/25%independent guessing.
**These are accuracy measurements, not mutual-information capacity estimates.**

Four binary facts, nominal width 32:

| Model | Bit accuracy @64 | Whole record @64 | Whole varied @64 | Constant answer @64 |
|---|---:|---:|---:|---:|
| pair_shared | 51.1% | 7.2% | 0.3% | 98.3% |
| gru | 65.3% | 14.2% | 1.3% | 83.2% |
| gru_matched | 57.1% | 10.8% | 0.2% | 93.5% |
| lstm | 56.7% | 10.2% | 0.5% | 95.4% |
| tanh | 50.5% | 6.9% | 2.4% | 63.5% |
| protected | 51.7% | 8.2% | 0.2% | 97.3% |
| pair_direct | 50.4% | 7.3% | 0.0% | 99.3% |
| pair_contract | 49.8% | 6.3% | 0.1% | 99.0% |
| pair_no_retain | 54.7% | 9.1% | 0.3% | 95.1% |

At body 64, the main pair model produces one answer for every slot in 98.31% of histories. Its 51.07%per-bit score corresponds to 2.043 of 4 answers correct including chance; it does not mean it reliably stored 2 facts.
At body 256/1024 its constant-answer fraction is 100%.
The only model/size/task condition passing the reliable-memory criterion in every seed was GRU 64 on 2 facts at body 16 (zero added no-write tail):97.14%mean bit accuracy and 94.27% whole-record accuracy, whole-record range 90.23–100%.
No model established reliable 4 or 8 fact recall at this budget.

Full 164-row group/condition table: [summary.csv](summary.csv). Raw seed files contain exact integer correct-counts, every seed score, collapse/varied metrics, baseline scores and data fingerprints.

## Scaling

| Pair width | Parameters | Independent / physical state scalars | 2-fact whole @16 | @64 | @256 | @1024 |
|---|---:|---:|---:|---:|---:|---:|
| 16 | 1011 | 13 / 16 | 43.0% | 28.0% | 25.0% | 23.7% |
| 32 | 2757 | 25 / 32 | 51.0% | 30.3% | 27.3% | 26.4% |
| 64 | 8457 | 49 / 64 | 50.8% | 29.9% | 25.5% | 25.9% |

The 64-wide pair model has roughly 8.4 times as many parameters as the 16-wide model but still fails two-fact separation under the longer hold. Performance is nonmonotone between 32 and 64.
No asymptotic scaling law can be inferred from these 3 sizes and 600 updates. The trainable fast state can also hold information, so these outcomes cannot be assigned solely to the pair subspace.

## Computation and storage

- All 123 runs: **968.4 CPU seconds** of measured training (16.14 CPU minutes), 116,035,200 queried training token positions, one CPU thread per run.
- Sum of seed-screen elapsed times, including evaluations/diagnostics/checkpoints: **1345.3 s** (22.42 runner minutes). End-to-end workflow 13 m 42 s, including setup, with at most 2 hosted jobs simultaneously.
- Peak process-lifetime RSS: **888.9 MiB**. This includes the interpreter/Torch runtime, saved activations and earlier models. It is not per-model peak memory.
- Environment: Python 3.11.17, CPU PyTorch 2.5.1+cpu, NumPy 2.1.3; CUDA build=null. No GPU and no local training.
- Summed linear forward MAC estimate for training:964,480,089,600. This excludes backward, optimizer, nonlinearities, normalization and overhead; it is **not measured total FLOPs**.

| Model (four facts; nominal width 32) | Parameters | State bytes/example | Linear MACs/token estimate | Train CPU s/600 updates | Forward ms |
|---|---:|---:|---:|---:|---:|
| pair_shared | 2757 | 128 | 2628 | 7.29 | 6.38 |
| gru | 7488 | 128 | 7168 | 6.37 | 4.93 |
| gru_matched (actual width 18) | 2700 | 72 | 2520 | 6.23 | 4.89 |
| lstm | 9600 | 256 | 9216 | 6.53 | 5.43 |
| tanh | 3232 | 128 | 3072 | 3.87 | 1.87 |
| protected | 4552 | 128 | 6144 | 7.78 | 6.95 |

Forward latency is the mean over seeds of each run's median of 3 forwards after warmup:8 histories x 4 queries =32 sequences,73 tokens each. These are the existing Python cell wrappers, not a fused-sequence-kernel comparison; host speeds vary.
Pair 32 has 11,028 bytes of trainable parameters,112 buffer bytes,128 physical state bytes and 25 independent state scalars per example. The matched GRU uses 72 state bytes.
The smaller parameter count did **not** give faster inference or training in this comparison.

## What failed and precision

Observed failure: the model usually learns a coarse single-value summary rather than independent slot-addressed memory. This interpretation is supported by constant-answer/varied-pattern metrics, not by a new causal intervention.
Pair 32/four-fact last 100-update loss averages are 0.6431/0.6277/0.6207; some optimization remains incomplete. Failure after 600 updates is not a proof of a hard representational capacity limit.
All sharing/retention/carry ablations also fail reliable four-fact recall. None justifies a claim that the PR #35-specific structure is necessary or beneficial.

**Finite precision in the learned approximation:**36 cast evaluations completed:3 models x 3 seeds x 2 delays x 2 cast dtypes,128 histories each.
Float 64 evaluation changed 0/9,216 bit predictions relative tofloat32in this subset; maximum stored-logit gap across models was 4.321 e-6.
Bfloat 16 changed at most 1.0% of predictions in a case across all models; the pair-model maximum was 0.2%.
Scores are converted tofloat32for common metric storage, the model/code started infloat32, and the models were not retrained at other precisions. This does not rule out precision effects during optimization or extreme near ties.

**Literal theorem code:** independent exact-rational polynomial calculation reproduces a necessary gain lower bound **>5.53 x 10^50 at D=89**, exceedingfloat32's finite range.
In 257 sampled directions, the D=6 clipped code had 99.823% zero local derivatives and bfloat16code outputs differed fromfloat64by up to 1.0; this is a serious end-to-end training/numerics concern, not a refutation of its continuous exact-real guarantee.
The explicit D=2 collision (1,0) versus(99/101,20/101) reproduced identical clipped codes for distinct unit inputs.
For the sampled widths, a=1-1/n rounds to 1 infloat32at n=10^8; at n=65536 the contract field's addition to bias .05 is invisible even infloat64. It may remain representable as a standalone number.

**Pinned author reference:**15 cases at n=1024,H=50,D=2 in each job, using the unchanged original script. Support<=3, max|x|<=0.380094, at least 2 saturated coordinates, endpoint residual<=2.23 e-16. This uses its small-n field/normalization surrogate and is outside theorem-size/gate conditions; its credit readouts are 14.93–18.91, not forward recall scores and not a theorem-scale margin certificate.

## Owner freeze and withdrawal — 2026-10-21

**The proposed 600-versus-3,000-update rerun is WITHDRAWN.** Task 1 found it was a
proposal, not an active or queued research job at the inspected time. The existing
123-run negative result remains the result; no further training is authorized.
Read the [canonical claim register in PR38](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md)
before proposing research or experiments. A failed fixed budget is not a universal
capacity theorem, but it does not authorize another budget study.

The suggestions below are preserved as **historical proposals, inactive under the
owner's research freeze**. They are not a current recommendation or automatic next
action. New work requires explicit owner authorization after checking the register.

### Historical proposals (withdrawn)

1. Distinguish optimization speed from capacity using a new preregistered CPU budget study on 2 facts (e.g.600 versus 3000 updates), matched GRU/LSTM controls and separate initialization/data seed factors. Reuse this dataset and state the new budget before training.
2. Include an explicitly compressed contrast implementation. Verify prediction/gradient/optimizer equivalence with the redundant encoding; do not credit pair duplication with extra memory.
3. Define a **faithful learning-credit-to-prediction bridge** before calling another model an implementation of PR #35. If a feature-credit trace B_t=G_t(RB_(t-1)+c_tE)is retained explicitly, charge its n-by-q state and update cost and compare with ordinary eligibility traces/RTRL/fast-weight memory.
4. Any literal saturation-code training first needs a bounded-gain, finite-precision/error and gradient analysis. A different well-conditioned code would need its own guarantee; the current theorem cannot be imported unchanged.

No extra/GPU experiment was launched after seeing the results.

## Reproduction and preserved evidence

Tested implementation commit: **68388be0787ea63b5029ab8fb8faba2a5747519d**.
Protocol was committed first at **9e0599e5dc61afaffafee42817e0464bdc3c6036**. The protocol's initial note that the full audit was unavailable is chronological; the owner supplied its location and it was read before the implementation run.
Branch: codex/pr 35-trainable-balanced-memory-20261020, stacked draft onto PR #23. Existing source, proofs, branches, saved models, notebooks and AGENTS.md were preserved.

- [Raw seed 17](raw/seed17.json), [seed 29](raw/seed29.json), [seed 43](raw/seed43.json): complete runs and environment/source hashes extracted verbatim from machine-readable hosted log rows.
- [Summary JSON](summary.json), [CSV](summary.csv), [provenance and artifact IDs/digests](PROVENANCE.json).
- [Run and downloadable artifacts](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39436715677):123 new checkpoints, exact source archives and pip-freeze inventories. Hosted artifact expiration is 2027-01-18; raw measurements are also committed here.
- Standard-library summary verification:
```sh
python docs/pr35_memory/summarize.py docs/pr35_memory/raw --output /tmp/pr35-recomputed.json --verify-csv docs/pr35_memory/summary.csv
```
Use a fresh output path. It checks all 123 runs, budgets, source/stream/evaluation equality and every CSV scalar. A separate tiny hosted report-validation workflow runs this check without retraining.
