# PR35 trainable balanced-pair memory experiment

A small PyTorch recurrent token model and a bounded CPU comparison with the existing PR23 models. This is an engineering surrogate, not an implementation or validation of PR35's learning-credit theorem.

Read [PROTOCOL.md](PROTOCOL.md) for the frozen comparisons, budgets, criteria and exact theorem/approximation boundary. New source is isolated here; all earlier model code and evidence stay unchanged. The draft PR is stacked on PR23 to reuse its tested code without modifying it.

## Run
Python3.11; CPU PyTorch2.5.1, NumPy2.1.3, pytest8.3.4. From repository root:
```sh
python -m pytest -q prototypes/pr35_memory/test_memory.py
python -m prototypes.pr35_memory.run --seed 17 --output results/pr35-seed17 --steps 600 --max-seconds 900
```
Repeat seeds29,43 with distinct output directories. The new GitHub Actions workflow does this remotely, with at most two concurrent CPU jobs. No GPU is used. Source, full results, checkpoints and dependency inventory are uploaded as artifacts.

## Transition and state
For width w divisible by8, d=w/8, r=2d-1, fast dimension f=w-2r. State is (u,p,-p), width w, with only f+r independent coordinates.
```
u' = tanh(A x + B [u,p,-p] + b)
v  = tanh(C x + D u + c)
q  = tanh(M v)
g  = sigmoid(E x + e)
p' = a p + g * (q - a p)
h' = [u',p',-p']
```
M is a fixed, row-normalized r-by-d Vandermonde feature map; its floating64 construction is stored in float32. Code sharing has no certified saturation or decoding guarantee. The trainable gates have no grammar parser or oracle write mask.
Main a=1; pair_contract uses a=1-1/w. Pair_direct removes sharing by proposing r independent values; pair_no_retain sets g=1 (its unused gate parameters remain counted). Embedding, LayerNorm, tied head and caller-owned streaming/reset interface are reused from PR23.

**Known reduction:** replace (p,-p) by p and substitute their difference into B. Every transition, gradient and recall prediction is preserved, with fewer state scalars. Balanced pairs give an exact zero-sum representation, not extra independent storage or a new primitive. The experiment asks about training bias only; it cannot establish novel computation.

## Audit implications
The full local audit at E:/AI-Architecture-Research/theory/codex_pr35_independent_audit_20261020/AUDIT.md was read after the owner supplied its location. It reviews immutable b984ef9347219d62db4dfd39f8f2e263317c9a33. Current PR35 aa47ca5 includes scope/rounding corrections. The audit accepts the exact-real principal constructions, rejects global code injectivity if claimed, and gives an exact code gain lower bound >10^50 already at D89.
We do not upload/copy that private-local audit. The new precision diagnostic independently computes its rational conditioning obstruction, a D2 clipping collision, small-D saturation and gradient saturation fractions, and loss of contract terms under ordinary precision. A small pinned author simulation runs separately (n1024,H50,D2), outside the theorem-size regime; its equal endpoints do not imply forward recall.

## Measurement limits
Capacity is measured only over 2/4/8 facts, with finite held-out histories and three paired seeds. Bits-correct includes random guessing; excess bits-correct is descriptive and is not mutual information. Failure after600 updates is not proof of insufficient representational capacity.
Long-delay evaluation appends a no-write tail after the original16-token update body. This is stricter than rerunning the old generator with more updates spread over a longer sequence: last writes cannot become more recent as the requested hold grows. Labels and prefixes match across delays.
Parameter matching and equal-width matching are both reported. Training budgets match updates/examples, not FLOPs or elapsed time. FLOP-like counts are explicitly linear MAC estimates; process peak RSS includes the Python/Torch runtime and earlier models. Precision casting tests are not retraining in low precision.
