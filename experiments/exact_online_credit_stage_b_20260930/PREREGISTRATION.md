# Exact Online Credit Stage B — version 1

CPU-only frozen-parameter structure audit authorized by owner; no GAS-0 access,
training, learning experiment, AMS v10 or Stage C. Stage A is read-only history.
Freeze source/config before official measurements; unit validation uses seed9400900.
Five official seeds9401100–04 (same as Stage A), float64, one CPU worker/thread.

## Equations and controlled grids

Main grid n=8, T=32/128, depth d=1/2/3:
`h_l,t=tanh(R_l h_l,t-1+W_l z_l,t+b_l)`;
`z_0=x_t; z_l=tanh(h_(l-1),t)` for l>0.
Zero initial state. Terminal `.5*(q@h_top,T-y)^2`, q/y fixed, not parameters.
Input uniform[-.3,.3], W Gaussian .4/sqrt(n), b uniform[-.05,.05],
unit-normalized Gaussian q and y uniform[.2,.4]. Initialization SeedSequence
[seed,1]; independent input SeedSequence[seed,stream], base stream2. q/y come
from separate [seed,3], making T32 a strict input-prefix of T128 with same loss.

Block axis: k=1/2/4/8, R consists of n/k trainable k*k blocks, others identically
absent. k1 diagonal uniform[.2,.5]; k>1 orthogonal blocks scaled .4.
P=d*(n*k+n*n+n). Rank axis: r=0/1/2/4/8,
R=diag(D)+U V^T; D uniform[.2,.5], U/V shape n*r. Jointly scale random U/V
so ||UV^T||2=.2 before freezing. r0 has no U/V parameters.
P=d*(n*n+2*n+2*n*r). These different parameterizations are reported, not
performance-matched architectures. Rank1 may already be a dense dependency
graph; do not predict strictly increasing support fraction for r1/2/4/8.

Mixing-location control: single-layer block k1. Five modes:
none: raw recurrent h output; fixed_linear: fixed orthogonal F*h output;
trainable_linear: M*h output; nonlinear_trainable: tanh(M*h) output;
feedback: tanh(M*h) output AND
`h_t=tanh(D*tanh(M*h_prev)+W*x+b)`.
M/F orthogonal scaled .4. Readout-only M parameters never enter state recurrence;
their direct terminal gradient is explicitly added and their state sensitivity
is zero. Feedback M does enter both state and readout. No extra hidden history.

Compact exact positive control: one layer, linear activation, R diagonal with
every frozen r_j=.35 (r parameters still individually differentiated). W/b
trainable. Known shared recurrence factor gives S_W=I tensor e_x,
S_b=e_b I, S_r=diag(e_h), with
`e_x=.35 e_x+x; e_b=.35 e_b+1; e_h=.35 e_h+h_prev`.
2n+1 persistent derivative values, plus query workspace. Test both widths/T/all
seeds. This restricted control does not imply exact sharing with general tanh.

Width16 runs only after all width8 gates pass: block k1/4/16 and rank r0/1/8,
depth1/3, both T and all seeds; positive control also width16. No width32 or
T256. Main320 width8 cases,120 width16 cases,20 positive-control cases=460.

## Methods and exactness

BPTT full graph independently checks analytic RTRL. Explicit within-time
Jacobians A/B, S_new=A S+B, parameters immutable. Compare every group and
every layer; nondegenerate relative gradient error<1e-8. Nearzero norm<=1e-12
uses maxabs<1e-11. CPU tensors, identical forward/input/parameter hashes,
trajectory maxabs<=1e-14, finite S/gradient/states, |h|<.95 and terminal
residual>1e-6. Failure stops interpretation; generic fixes documented and affected
invalid outputs preserved. No individual-seed adjustment.

Exact graph-support packed online RTRL: derive A/B Boolean support from
architecture, not a numerical threshold. Closure K=B_support union A_support*K
until fixed. Group parameter columns with identical reachable-state sets; keep
only those row/column blocks. Update each block with A_rows,rows*Sblock+B_rows,cols.
Reconstruct for audit, compare matrix AND group gradient to full references.
Store values, int64 row/column indices and any live metadata; count all. A/B and
reconstruction are temporary full-matrix scratch, disclosed: this implementation
tests compact persistent state, not a fully optimized sparse execution engine.
Raw local/SnAp are not considered exact unless they pass both gates.

SnAp1/2: same packed recurrence but fixed masks K1=B_support,
K2=B_support union A_support*B_support. This is one direct recurrent-core
transition versus two; within-time spatial chains count inside the recurrent
core. It is graph reachability truncation, not TBPTT/window truncation. Intended
approximation errors are results, not invalidity. If K2 equals closure, it must
agree exactly; if not, measure omitted dependencies and gradient error.

Same-layer block-only mask removes cross-layer credit and cross-recurrent-block
credit; terminal direct head derivatives remain. Its error is a separate local
control, not a claimed reproduction of a published algorithm.

Full sensitivity matrix SVD: minimum retained rank with relative Frobenius tail
<=1e-13; factors L(N*k),R(k*P), singular values folded into L. Test final
reconstruction<1e-8 and all group gradients. Online SVD-recompressed RTRL on
the preregistered lowrank subset updates from factors, reconstructs temporarily,
then recompresses each step. Count persistent factors and N*P/QR/SVD scratch;
no hidden history/full persistent fallback. If fixed rank1/2/4 reconstructions
fail, label rejected approximation, not exact. Full-rank factors may cost MORE
than raw S. Offline compressed snapshot is not a cheap online representation.

Kronecker/shared-factor tests for each W group: S_W reshape(N,n,n), rearrange
to (N*n,n), SVD into sum of Kronecker products with factors (N,n) and (1,n).
Other parameter groups kept explicitly; count every number. Test rank1 and
minimum rank achieving1e-13 tail, reconstruction and group gradients. Also retain
the exact evolving unfused sum of per-step W factors: A propagates each left
factor; new direct W term is one factor per step. Count all T factors, not just
one. Execute this online for depth1 blocks k1/k8 and rank0/rank1 at n8,T32,
all seeds. For depth>1 offline rearrangement is a snapshot test only.
Unfused factors store T*(N*n+n) per W group; no history disguised as a buffer.

Block/layer triangular zero entries are exploited by graph closure. Examine
per-output-owner W slices for shared rank patterns; no claim that all possible
factorizations have been enumerated. UORO omitted to prioritize exact work.

## Measurements and numerical diagnostics

Per case/method: P,N,N*P; persistent values, index bytes, derivative bytes,
query/peak scratch scope, sampled peak RSS; inference and derivative time per
step, inclusive total/inference and gradient-section/inference ratios, CPU time.
Two timing repeats, no seed selection. BPTT saved tape counted by unique storage
hooks; aliases separated. Full-process CPU includes imports; process age wall
includes imports, sampled RSS starts after imports. Numerical diagnostic/storage
reconstruction overhead separate from method runtime. Reference SVD etc use
full-S scratch and cannot be called cheap online methods.

Checkpoint S at t1/2/4/8/16/32/64/128 (only t<=T): exact nonzero and thresholds
1e-14/1e-12/1e-10; full singular spectra/ranks; cross-layer blocks for all i<=j,
with size/support/rank/spectrum. Retain checkpoint arrays outside online state as
audit data, separately counted. Connectivity closure counts also recorded, even
when conditioning makes some entries tiny.

Sensitivity-family diagnostic: for config-selected nine n8 families, each seed
FIXED parameters, eight independently generated input streams10–17 at T32.
Flatten exact final S, stack and center; report SVD/rank at three relative cutoffs,
maximum rank7. Also pooled40 matrices per family across seeds (cap39), explicitly
mixing parameter settings. Sample counts may ceiling the dimension; this is NOT
a lower bound. Diagnostic streams never used to tune the experiment. Store hashes
and full S, not only singular values. These runs also check BPTT/RTRL validity.

## Classification frozen before results

Invalid: any intended-exact reference/online sparse/positive-control disagreement,
parameter/data/device violation, NaN/Inf or invalid accounting. Approximation and
proposed-compression failure are not invalidity if correctly labeled.

Known exact structure closes: a tested ONLINE method (not offline snapshot,
full-matrix stored fallback or unfused growing history) passes every group and
matrix gate at widths8/16 across rich rank/block/depth settings; storage/P<=4
and derivative/inference ratio<=4, with bounded history-independent state. These
finite thresholds are screening definitions, not asymptotic proof.

Structural Pareto gap survives only if all exact references pass; block support
per parameter expands predictably for k1->k8/k16 in >=4/5 seeds per horizon;
rank0->rank1 expands support in >=4/5 (higher ranks may saturate); depth creates
nonzero lower-to-upper blocks; local error>1e-4 in >=4/5 rich depth3 cases;
tested online exact structures for rich depth3 cost>=4P or fail reconstruction;
width16 rich packed storage/P is>=1.5 times width8 for both full block and
rank1/8 at depth3; no tested cheap exact online method closes all settings.
Threshold/support/rank-cutoff conclusions must be stable. Saturated family-span
dimension is an explicitly bounded, inconclusive diagnostic and cannot support
a universal claim. If numerical ranks themselves are cutoff-unstable or exact
compression ambiguous enough to undermine these criteria: INCONCLUSIVE.

## Budget/stops

2700 measured CPU seconds for every numerical process incl development, analysis
and any repairs; reserve60s before new case; RSS2GiB, free RAM4GiB/disk2GiB.
One thread; check CPU/RAM/device before experiment. Stop cleanly with partial
artifacts if cap approached; never expand width/horizon or drop gates. Track
shared project ledger too (legacy30h headroom currently>24h).
Commit freeze before official seeds. Stop after Stage B. No Stage C/learning.

## Primary-source implementation anchors

Menick et al., *A Practical Sparse Approximation for RTRL*, arXiv2006.07232v1,
Section3: fixed influence sparsity determined by n-step graph reachability.
[Primary paper](https://arxiv.org/pdf/2006.07232).
Mujika et al., NeurIPS2018, *Approximating RTRL with Random Kronecker Factors*,
Section4/Lemmas1–2: immediate derivatives have a Kronecker factorization;
merging sums back into one factor is an approximation. We test deterministic
exact sums/rearrangements, not their stochastic estimator.
[Primary paper](https://proceedings.neurips.cc/paper_files/paper/2018/file/dba132f6ab6a3e3d17a8d59e82105f4c-Paper.pdf).
