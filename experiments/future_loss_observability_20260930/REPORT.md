# Future-loss observability report

**FULL EXACT OBSERVABILITY — CONTINUOUS STATE LOWER BOUND PROVED**

## Exact result and scope

The accepted accessibility theorem is a premise, not rerun. The new proof is in
PROOF.md. On a reachable open fixed-h sensitivity fiber of dimension nP,
any allowed late future-gradient family with adjoint span R^n separates every
sensitivity difference. A continuous exact encoding with no discarded-input
replay/external tape therefore requires at least nP real coordinates. If exact
forward h must also be recoverable, total history-dependent real state requires
n+nP=2n³+n²+n coordinates. RTRL's h/S representation attains that count.

This is a frozen-parameter exact-query theorem in a specified computational
model; it is not a bit, practical memory, runtime, learning or novelty claim.
The new proof has not yet received the two independent reviews that the owner
reports for the prior accessibility theorem.

## Loss contracts and adjoint spaces

| Contract | Adjoint space / span | Observable sensitivity dimension |
|---|---|---:|
| Immediate arbitrary linear loss | C=R^n | nP |
| Unrestricted smooth local loss | Contains arbitrary linear adjoints | nP |
| Any fixed invertible future continuation + arbitrary terminal linear loss | C=J^T R^n=R^n | nP |
| Immediate fixed head H, unrestricted output loss derivatives | span C=im H^T, rank r | rP |
| Fixed continuation + fixed head H | span C=J^T im H^T, rank r | rP |
| Fixed full-support scalar linear head + one variable future input | C contains an open subset of R^n | nP |
| Any nonzero scalar linear head + allowed horizons1,...,n under accepted R/W hypotheses | Union's span is R^n; no one-horizon open-set assertion required | nP |
| Diagonal recurrence + single-coordinate head | Only that coordinate is observed | Intrinsic quotient can be smaller |

For Q=span C of dimension r, the invisible ambient sensitivity subspace consists
of matrices with every column in Q-perp and has dimension(n-r)P. A single
query returns P numbers; the family of possible queries separates nP.

The true future gradient is S^T J^T q+B^T q, with B=D_theta Phi at fixed initial
h. The injection cancels only when comparing equal-h endpoints with the same
future query. It was not discarded from the individual gradient formula.

## Continuous encoding model

All history-dependent buffers count; theta/program constants are fixed. The
query is chosen after encoding, all permitted answers are exact, encoding is
continuous, and there is no external input/history tape or replay of discarded
inputs. Decoder continuity is unnecessary. A local history section from the
accepted full-rank endpoint map makes the result apply even when an encoder
retains irrelevant history and is not a function solely of(h,S).

The proof uses invariance of domain (Hatcher, Theorem2B.3). A continuous injection
from an open nP-dimensional set into fewer real coordinates would, after zero
padding, have an open image in R^(nP) lying in a proper coordinate plane.
For the n+nP total bound, exact-forward recovery is an additional explicit
contract. Immediate linear gradients alone do not observe h.

## Controls and cross-layer consequence

Independent recurrence has P_ind=n²+2n owner-local derivative entries and an
exact closed trace update; persistent upper count is n+P_ind. A full-support
immediate head separates all owner traces with one query. Matching lower bounds
hold on open owner-trace fibers; prior n2/n4 certificates establish those fibers
at the witnessed widths. No new independent accessibility experiment was run.

The saved width3 two-layer endpoint is195-dimensional, with local(h,E)132 and
cross C63. Fixing(h,E) leaves an open63-dimensional cross fiber. Arbitrary upper
linear losses distinguish all63. A fixed full-support upper scalar head after
one future input also suffices at the archived point: exact determinants
R1=161/2048, W1=921/8192, R2=603/8192, W2=1945/16384 are nonzero.
With arbitrary losses on all6 states, all189 supported sensitivities are
observable; preserving forward state gives total195. An upper-head-only total195
claim or arbitrary-width deep theorem is not made.

## Escape routes and remaining questions

Restricted/known loss queries, approximation and finite/discrete seed-generated
history families can genuinely lower the required statistic. BPTT, checkpointing
and retained-history replay are valid exact alternatives outside the no-history
contract. Discontinuous infinite-precision packing is outside continuity.
Continuous nonlinear/factorized encodings cannot beat dimension on the open
family; unbounded decoding time alone cannot resolve a collision.

Nothing quantitative is established about tiny observable directions. Practical
precision, task-relevant queries, restricted target distributions and usefulness
remain open. No Stage C, training, AMS v10 or architecture work was begun.

## Checks/resources and artifacts

25 exact algebra checks passed, including the B term, quotient ranks, full-head
one-step adjoint dimension, sparse interacting path coefficients, a negative
head-observability control, owner traces, cross dimension and archived deep
matrix invertibility. They support the formulas; they are not a proof-assistant
verification of invariance of domain or an independent review of the argument.

Measured symbolic process:1.21875 CPU-s (0.0203125 CPU-min),1.2854523 wall-s;
peak working set123,453,440bytes (117.734375MiB). A separate conservative20s
administrative CPU estimate is charged. No GPU/CUDA/ML/model server was used;
only pure CPU symbolic/rational algebra. Research-session wall time is not
claimed to be measured by the script. Far below45CPU-min limit.

Files: config.json, PROOF.md, REPORT.md, checks.py, checks_result.json and
result.json in this directory; Codex_Research.md/Resume, SHARED_RESEARCH_MAP.md
and the shared CPU ledger record the finalized result. Setup commit0bd9a0d.
Prior proof/certificate files, GAS-0 and independent notebooks were not edited.

## Single recommendation / stop

Independent mathematical review of the observability and continuous-encoding
proof, especially the local history section and forward-state accounting.
STOP after this task; no learning or architecture phase is authorized by it.
