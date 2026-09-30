# Exact Online Credit — Stage A, version 1

Owner-authorized frozen-parameter derivative audit. CPU only, no training,
model server, GAS-0 access, mechanism search, AMS v10 or Stage B/C.
Configuration and implementation are committed before official seeds run.

## Computation

Width n=8, input dimension8, depths1/2/3, horizons32/128; five seeds and
numerical gates in config.json. M1 is dense recurrence at each depth. M2 is
single diagonal recurrence. M3 is diagonal recurrence at depths2/3 with
nonlinear dense spatial mixing. All use, in increasing layer order:

`z_0=x_t; z_l=tanh(h_(l-1,t))` for l>0;
`h_(l,t)=tanh(R_l h_(l,t-1)+W_l z_l+b_l)`.

Dense R is an orthogonal matrix scaled .4. Diagonal R entries are uniform
[.2,.5]. W is seeded Gaussian scaled .4/sqrt(n), b uniform[-.05,.05].
Initial states are zero. Inputs uniform[-.3,.3], q normalized seeded Gaussian,
y uniform[.2,.4]; terminal loss `.5*(q@h_top,T-y)^2`. q/y are not parameters.
PCG64 generators use SeedSequence([seed,stream]); initialization stream1,
inputs/q/y stream2. Each horizon regenerates from that stream; no seed tuning.

## Derivatives

G0: full unrolled autograd BPTT. G1: independently derived analytic Jacobians
A=dF/dprevious_state, B=dF/dparameters; M_new=A M+B, M_0=0.
Within-step spatial dependencies are included recursively in both A and B.
Terminal cotangent contracts M. No optimizer, weight update or truncation.

G2/G3: row-local eligibility for own r,W,b, treating lower inputs as exogenous:
`E_l,t = diag(1-h_l,t^2) [diag(r_l) E_l,t-1 + direct_local_partials]`.
Each unit stores n+2 entries (r, W row, b), total depth*n*(n+2)=P.
G2 single-layer is exact. G3 propagates the terminal learning signal spatially
through current-time W and tanh Jacobians, then contracts local eligibility.
It omits cross-layer temporal credit. This is a transparent published-style
local eligibility approximation, not a claimed reproduction of a particular
LRU/e-prop implementation. The top-layer own-parameter gradient should be
exact; lower layers need not be. Optional SnAp/UORO are deferred to Stage B.

## Tests, gates and interpretation

Unit tests use development seeds/tiny widths. Official grid has60 cases,
150 method evaluations per repeat, three identical timing repeats. Inputs,
parameters and trajectories must match; all parameter hashes unchanged.
Every nondegenerate group: exact G1 (and G2) relative error<1e-8.
Norm<=1e-12: max absolute error<1e-11, label relative/cosine degenerate.
Trajectories maxabs<=1e-14; all finite; |h|<.95 and |terminal error|>1e-6.
Failure stops the sweep. Ordinary implementation repairs require an append-only
correction record and rerunning affected invalid measurements, not retuning seeds.

G3 is not subject to an exactness gate. Report r/R, W, b separately per layer;
also aggregate each layer. Structural difference requires at least one early
layer relative error>1e-4 while exact references/G2 pass. This threshold is
descriptive, not a performance or discovery claim. Otherwise classify using
the owner's Stage-A categories. No asymptotic conclusion or architecture novelty.

## Accounting

One CPU thread, float64. Cap1200 measured process CPU seconds across all
development tests, official sweep and analysis processes; reserve30s before
starting another case. Import/setup time included in process CPU ledger.
Check RAM/disk before each process; sample RSS at .02s. Stop above2GiB RSS or
at budget margin; retain partial raw JSONL. No CUDA build/tensors permissible.

For G1 persistent online sensitivity N*P, N=depth*n; compare n*P explicitly.
Step scratch: A(N*N), B(N*P), old/new M(2*N*P), local Jacobian temporaries;
report named tensor storage through an explicit workspace inventory, including
row-Jacobian temporary buffers. For G2/G3 eligibility=P, terminal readout
cotangents N and gradients P additional query workspace. BPTT saves a graph;
saved_tensors_hooks count unique underlying stored tensor bytes, separating
parameter/input aliases from auxiliary saved storage. Saved tape is an
implementation measurement, not an exact minimal lower bound.

Trajectories T*N are audit-recorder storage in all methods, separately counted;
not claimed as online derivative state. No sensitivity history is retained.
Time each full method call and gradient section; inference median over three
no-grad frozen passes. Report total/inference and derivative/inference ratios.
G1's derivative section includes analytic Jacobian construction and contraction;
G0 section is backward only (graph-building forward overhead separately visible
in total/inference). Small Python implementations/timing overhead do not establish
practical/asymptotic speed laws. No parameter matching/capability benchmark.

Sensitivity support: exact nonzero plus abs>1e-12 counts, per-state-layer vs
parameter-layer blocks, and total fraction. Test lower parameters influence
higher states. Support filling concerns omitted dependencies, not numerical
rank or a lower bound. Local rule is structurally closed within each unit for
its own parameters; stacked global early-layer credit is not generally closed.

Freeze provenance includes config/source hashes, Git commit and CPU-only runtime.
Final report, raw records, summary, tests and resource ledger are preserved.
Stop after Stage A regardless of outcome. Stage B requires owner review and
new authorization.
