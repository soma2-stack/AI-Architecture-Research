# Reachable fixed-feature operator diagnostic

2026-10-02. **Sampled finite-radius core favors linear growth; full reachable
query-visible dimension remains INCONCLUSIVE.** No theorem attempted.

## 1. Scope and provenance

Same accepted hard rotating/dense tanh family, c=1, gamma=1/n,
epsilon=1e-3, group-RMS weights and beta-normalized late scalar head.
Frozen actual dense matrices are loaded from the previous diagnostic's
archives. One PUBLIC raw source direction Hsrc=.4ones_l stays constant at
every interior step. Memory coordinate1 stays zero; coordinates2..k vary.
No ambient operator-ball sample, source-history variation or new architecture.

Primary protocol63292dd was pushed before official outcomes. JSON-only repair
f1935bb preserves the frozen mathematical code. Seven completed width16
spectra were retained without repeating; the unsaved finite output was replayed.
After primary outcomes, broader INPUT-DRIVEN coverage was separately frozen
and pushed at ec665ca before its fresh-seed outcomes. It is secondary, not
a retroactive revision of the primary design. REPAIRS.md preserves two output
serialization defects, both unrelated to derivative/query calculations.

Primary widths16/32/64/96, H=137/289/605/929, T=H+1. Two official seeds per
random/sparse/dense strategy:24 base histories,256 novelty-pool proposals,
48 mutations;28 full spectra. Supplement:12 additional full spectra on
widths32/64/96, two seeds for each of two input-driven patterns. Total340
history proposals across these stages,40 full spectra. Mutations share
lineages; these are not340 statistically independent trials.

These widths are below the accepted sufficient proof-width bound n0(1)=200.
They use the same mathematical family but cannot establish asymptotic scaling.

## 2. The operator is actually reachable and feature-coupled

All histories prescribe h0=hT=0 and realize x_t=atanh(h_t)-R h_(t-1)-b.
All realized inputs stay in(-.5,.5)^n. Sensitivities differentiate parameters
holding those realized inputs fixed. No task, phase or gate oracle is given
to a learner. This is a derivative/operator diagnostic, not learning.

For K=delta R_(remaining,source), the exact actual selected sensitivity is

    delta h_T = B_T K Hsrc,
    B_t=diag(1-h_t^2)[R B_(t-1)+alpha_t E],
    B_0=0, alpha_1=0, alpha_t=1 thereafter.

B has n state rows and r=k-1 parameter-row directions. This uses ACTUAL R
and includes leakage into protected/source states. Parameters are frozen.
Other parameter groups are explicitly outside this experiment. Source
coordinates never vary across histories, so this does not secretly reproduce
the earlier multi-feature/source-history quadratic construction.

The analytic history Jacobian includes every free gate entry and its coupled
propagation/injection. Its spectrum is whitened by the EXACT dx/dh Gram,
including dense R and the final zero reset. Unit tangent radius therefore
means TOTAL physical input-history L2 norm1, not unit per-entry perturbation.
No parameter/query renormalization or change to epsilon occurs.

## 3. Worst-case query contract is retained

Actual physical distance:

    nu(DeltaB)=wR||Hsrc|| sup_allowed_c ||DeltaB^T c||.

Permitted one-step box queries have c=R^T g/(beta sqrt(n)), with
g in[sech²(.5),sech²(.25)]^n and actual future inputs in[.2,.45]^n.

Three DISTINCT notions are used:

* Exact sign-corner second moment: a mathematical LOWER norm on nu, computed
  numerically using Q=R^T(s_g²I+g_mid²11^T)R/(beta²n). Its spectrum supplies
  the lower tangent count. RMS is not substituted as the query contract.
* Seeded box-vertex coordinate ascent: supplies actual permitted queries and
  hence a numerical lower estimate of the supremum for finite differences.
  Global optimization of the box or full future family is not claimed.
* kappa*wR||Hsrc||||DeltaB||op: the accepted ALL-continuation upper envelope.
  Its Frobenius relaxation supplies a Euclidean tangent-envelope spectrum.

Projected spectrum calculations subtract/add an omitted-state query envelope.
It is at most1.6e-10 here, far below epsilon. Finite tests use ALL actual B
rows. Bounds are mathematically valid identities/inequalities evaluated in
float64; no outward interval certification or new dimension proof is claimed.
The two spectra have DIFFERENT singular vectors: matching their index does
not bracket one specific direction. Count comparisons are diagnostic.

## 4. Strongest primary spectra and normalized counts

These are numerical unit-input-radius TANGENT lower counts, NOT certified
continuous robust dimensions.

| n | H / T | strongest lower count | count/n | count/(n ln n) | same-case envelope count |
|---|---|---:|---:|---:|---:|
|16|137 /138|20|1.2500|.4508|39|
|32|289 /290|69|2.1563|.6222|157|
|64|605 /606|149|2.3281|.5598|614|
|96|929 /930|230|2.3958|.5249|1264|

Full spectra, individual patterns and spectral landmarks: TABLES.md,
analysis.json, archive/*.npz, spectra.png. Lower spectra have a strong core
and weaker tail, rather than a theorem-level exact finite-rank cutoff.
At n96, lower modes48/96/192/230 have scales
.021538/.003402/.001238/.001007; the final mode is2.15e-8.

All-four-width through-origin fits have RMSE:
n:9.59; n ln n:6.49; n^1.5:15.45; n²:30.42.
Thus n ln n actually fits the ENTIRE small sample slightly better than n.
Do not hide this. The descriptive largest-three-width log-log exponent is
1.097; the all-four exponent is1.346. The range is too narrow and sampler
shrink factors differ to identify an asymptotic exponent. No confidence or
model-selection inference from correlated search cases is claimed.

Random broad irregular histories are strongest at widths32/64/96. Sparse
pulses yield13--14/28--29/50/77--80 lower counts. Positive dense irregular
gates yield20/54--59/109/155--164. Novelty search yields20/69/148/191:
its final objective values improve distance from base operators, but do not
beat the strongest base direction counts. Distinct operators are not the
same as a higher-dimensional robust neighborhood.

## 5. Non-infinitesimal actual-query checks

For each selected case, test nonlinear fixed-h antipodes at radii.05/.25/1
in the input-whitened tangent chart, then re-realize the actual inputs. A
requested radius is rejected if inadmissible, not shrunk to manufacture a
pass. Separation uses actual allowed queries, threshold STRICTLY>.002.

| n | tested lower axes | admissible at.05 | separated at.05 | separated at.25 | admissible/separated at1 |
|---|---:|---:|---:|---:|---|
|16|32|32|10|24|3 /3|
|32|64|64|21|47|7 /7|
|64|128|128|44|96|1 /1|
|96|128|128|61|97|0 /0|

At.25, admissible axes are32/64/115/97 respectively. Finite.05 passes/n are
.625/.656/.688/.635. Their n-fit RMSE1.40 beats n ln n4.15, n^1.56.86,
and n²11.01. This is the strongest finite-radius evidence for a linear-sized
core. Axes are counted once; we do not add eight overlapping envelope axes.

Also sample16 JOINT sphere antipodes in the leading20 dimensions at n16
and32 dimensions at the other widths. All.05 samples are admissible, and
their minimum permitted-query separations are
.004742/.006859/.012031/.011681, exceeding.002.
That is numerical evidence on those sampled spheres, not a whole-sphere
bound or20D/32D certificate. The 61 or97 one-axis passes likewise do NOT
prove61 or97 jointly independent robust continuous dimensions.

Nonlinearity is not negligible: some weak tested modes have a symmetric
midpoint-deviation/antipodal-difference ratio as high as27.3 at radius.05.
That ratio is only a diagnostic, not a derivative-variation upper bound.
The unit-radius charts usually leave the input domain; their tangent counts
cannot be promoted to finite-error sections of that size.

## 6. Broader admissible gates: separately prospective supplement

Primary base memory amplitudes were<=.22. The supplement instead chooses
actual memory inputs and simulates their nonlinear response, retains the
same fixed source, and cools before an exact final reset. It reaches hidden
amplitudes.81--.96 and gate spreads up to.918, with actual inputs<=.463.
All complete gate words remain aperiodic, nonscalar and noncommuting.

| n | driven random lower counts | driven coherent lower counts | supplement best finite.05 axes |
|---|---|---|---:|
|32|32 /32|32 /29|11|
|64|52 /49|42 /59|14|
|96|60 /56|68 /56|16|

These ordinary stronger-gate examples do NOT improve the primary best.
Stronger state excitation also dissipates accumulated old credit; it is not
a monotone route to more visible directions. The supplement does not prove
that EVERY strong-gate history behaves this way. Raw input-derived samples
are not adversarial global maxima of the reachable family.

## 7. Validity, resource use and limitations

Development validation: selected exact RTRL vs BPTT relative error4.05e-16,
analytic history FD3.08e-9, physical tangent norm1 within6e-12.
Post-run checks at all four widths: selected BPTT error<=3.21e-15,
FD<=3.33e-8, input norm error<=4e-13, spectral replay<=7.32e-16.
Actual future-loss gradient distances match the numerical query calculation
within2.62e-14 relative error. Supplement BPTT checks<=1.45e-14 and FD<1e-9.
All checked tensors CPU float64; parameters unchanged; all frozen input
hashes unchanged. Maximum recorded forward endpoint roundoff is below4e-14.
No CUDA/GPU, training, model server or GAS-0 operation occurred.

Primary+supplement measured process CPU467.109375s, active wall292.661962s.
Checks add.671875+.421875CPU-s; primary archival analysis adds.578125CPU-s.
Supplement archival is separately recorded in archive_resources.json.
Total measured compute is approximately7.82CPU minutes and4.9 active wall
minutes, plus small unprofiled interpreter/development/repair/plot overhead
(conservatively allocate10CPU-s). Peak process RSS2,044,604,416bytes=1.904GiB.
This stays far below the frozen60CPU-minute/30wall-minute/6GiB limits.
GPU time0, VRAM0 for this experiment; existing model-server activity untouched.

Compact archive preserves ALL histories, actual operators, complete spectra,
finite query examples and FULL winning mode banks. Nonwinning full mode banks
remain local, immutable and hash-manifested; they are regenerable from frozen
code/histories. This avoids pushing redundant large intermediate arrays.
Execution/repair logs are preserved as text, including failed output writes.

## 8. Interpretation and next theorem

**Measured:** a linear-sized finite-axis separated core is reproducible;
aperiodic novelty optimization and stronger input-driven gates did not reveal
a larger finite core. Unit tangent counts grow modestly faster than n over
the smallest width, and permit both n and n ln n explanations on this range.

**Unresolved:** full-query upper envelopes still have many more modes than
the lower diagnostic. Gate/input histories sample only part of the actual
reachable family. All-pair/whole-sphere finite-radius control is missing.
No robust-memory dimension or universal encoder follows from this experiment.
The general Omega_c(n²) to O_c(n² ln n) credit-memory gap is unchanged.

**Single next theorem to attempt:** a horizon-uniform finite-radius width
bound in the ACTUAL permitted-query norm for the reachable one-fixed-feature
operator family, controlling the weak mixed tail and joint gate variation.
Seek a linear-width upper or a jointly robust superlinear countersection.
Do not infer either from RMS spectra, individual axis successes, raw rank
or the ambient operator ball. A later encoder must also count its adaptive
basis and coefficients. Stop this diagnostic; no architecture or other gap.
