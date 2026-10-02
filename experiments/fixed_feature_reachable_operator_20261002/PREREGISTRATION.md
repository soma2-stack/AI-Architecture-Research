# Fixed-feature reachable accumulated operators

Prospective numerical diagnostic, 2026-10-02. No robust-dimension theorem.

## Frozen model, queries, source and histories

Read the archived R, R0, O from the previous spectrum experiment, not a new
matrix family. c=1, gamma=1/n, epsilon=1e-3. Widths16/32/64/96; these are
finite-size diagnostics below the sufficient proof-width bound200. No claim
of asymptotic confirmation. Same b=.05, W=I, input cube(-.5,.5)^n,
group-RMS wR=||R||F/n, beta=max(1,||R||F), q=ones/sqrt(n).

Let k=n/2, l=n-k, r=k-1. E selects physical memory coordinates2..k.
One fixed PUBLIC source direction Hsrc=.4*ones_l. Every interior source
state is Hsrc; physical memory coordinate1 stays zero. Only the remaining
memory states vary. h0=hT=0 exactly. H interior steps use the accepted
lookback H=ceil(log(kappa*1.2/(epsilon*gamma))/-log(1-gamma)); T=H+1.
Realize x_t=atanh(h_t)-R h_(t-1)-b. Parameter sensitivities hold these
realized inputs fixed, NOT the inverse-controller formula.

Two official seeds and three aperiodic strategies per width:
random: independent uniform memory entries[-.18,.18];
sparse: on each step, probability1/2 of one uniform coordinate with random
signed amplitude .11--.22, otherwise zero;
dense: independent positive entries .022--.22, with a seeded irregular
timewise multiplier .4--1. Negative signs are not needed for nonscalar gates.
Before operator scoring, deterministically shrink the whole memory history
by .9 until max|x|<=.48. Record shrink factor. Never alter source or endpoint.
This is a declared generator, not post-score tuning. Check gates are
nonscalar, noncommuting and have no period<=H/2.

Novelty search:64 histories per width, cycling the three generators, seeded
independently. Rank by minimum actual one-step BOX-RMS distance to the six
base operators. This is a permitted-query LOWER diagnostic, not a replacement
of the worst-case contract. Then12 mutation proposals, changing a seeded
coordinate/time interval or mixing with another frozen-generator history;
retain only increased score. Each proposal is realized and domain-checked.
One winner per width receives the full spectrum. No search after finite-radius
outcomes. No optimization of epsilon, c, parameters or feature direction.

## Exact selected sensitivity, including actual dense leakage

For raw K=delta R_(remaining,source), exact selected sensitivity is

    K -> B_T K Hsrc,
    B_t=diag(1-h_t^2)[R B_(t-1)+alpha_t E],
    B_0=0; alpha_1=0; alpha_t=1 thereafter.

B is n by r. This recursion uses ACTUAL dense R, not its block surrogate.
It includes gate-history variation. It is not a complete-gradient experiment.
One fixed source does NOT mean one parameter column: K Hsrc has r components
and its selected gradient is wR B^T c Hsrc^T. All unselected parameter groups
are excluded explicitly. Future injections cancel between histories because
their final hidden states agree.

## Query-visible spectra: bounds, not an RMS contract

The physical distance is

    nu(B1-B2)=wR||Hsrc|| sup_allowed_c ||(B1-B2)^T c||.

For one-step gates in[sech²(.5),sech²(.25)], c=R^T g/(beta sqrt(n)).
The exact sign-corner second moment gives a computable LOWER norm:

    Q=R^T[s_g² I+g_mid² 11^T]R/(beta² n).
    wR||Hsrc|| ||Q^(1/2) DeltaB||F <= nu(DeltaB).

ALL permitted continuations obey the accepted upper envelope

    nu(DeltaB)<=kappa*wR||Hsrc|| ||DeltaB||op
                <=kappa*wR||Hsrc|| ||DeltaB||F.

No RMS upper claim. Coordinate-ascent box-corner search returns actual
permitted query examples, hence a numerical LOWER estimate of the supremum.
It is not guaranteed globally optimal. Store query gates for finite tests.

Differentiate B_T with respect to ALL Hr free memory-history entries,
including their actual gate effects. Use analytic forward/reverse propagation.
For efficiency, spectrum uses E^T B, with omitted-row effects bounded by
their derivative Frobenius norm times1/gamma (input whitening) and the
all-query envelope. Subtract this leakage envelope from lower singular
margins; add it to upper margins. No silent reference-family substitution.

Whiten the history tangent by the EXACT Gram of dx/dh, including final reset
and all dense R couplings. Thus singular values use unit TOTAL physical input
history L2 norm. It is an input perturbation scale, not a changed gradient
metric. Report lower-spectrum counts sigma>epsilon and upper-envelope counts
sigma>epsilon, spectra, stable ranks, and ratios /n, /(n ln n), /n^1.5, /n².
These are unit-radius tangent diagnostics, NOT finite robust dimensions.
Fit one-parameter through-origin laws; tiny width range cannot select an
asymptotic exponent confidently. Do not equate upper counts to actual rank.

## Finite-radius evidence and adversarial query examples

For each width select the case with largest lower tangent count, breaking
ties by sum(log(1+(sigma/epsilon)^2)), then lexical case ID. Freeze selection
before finite-radius checks. Test up to min(128,2n) strongest lower modes
and eight strongest upper-envelope modes. Use radii .05,.25,1 in the
whitened input tangent coordinates. Antipodes are constructed by prescribing
h_base +/- radius*dh then re-realizing inputs, retaining source and hT=0.
Reject/report a tested point if it leaves the original cube or |h|<1;
do not shrink that requested radius to obtain a pass. Record actual physical
input distance separately, since nonlinear chart length differs from tangent.

Measure each antipodal pair using numerical optimized allowed box queries
and the all-future upper envelope. Separation>2epsilon gives a numerical
two-history distinction only. It does NOT prove an independent continuous
dimension. Sample16 seeded joint sphere antipodes per radius in the leading
min(lower_count,32) modes; record worst sampled separation and admissibility.
Sampled success is NOT a whole-sphere certificate. Never sum one-axis passes
as a continuous-memory lower bound.

## Development validity, artifacts, resources and stop

Before official runs: development seed only, finite differences of analytic
operator Jacobian, direct input-Gram reconstruction/whitening, actual frozen
parameter BPTT of the selected group, deterministic endpoint realization,
query lower<=sampled lower<=upper, and frozen source invariance. If a check
fails, fix code with recorded repair BEFORE official seeds. Source/config/hash
manifest committed before official results. All spectra, histories, selected
modes, finite query examples, per-case timing and peak RSS preserved compactly.

CPU float64, one process, four BLAS threads. CUDA disabled; no model server
or GPU process. Hard60 process-CPU minutes,30 wall minutes,6GiB process RSS;
preserve completed cases and partial status at cap. No extra widths automatically.
No experiments outside this diagnostic. Stop after report and record update.
