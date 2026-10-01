# Anisotropic robust packing / product entropy

## Classification

**ONLY A FEW ROBUST DIRECTIONS SURVIVE.**

Primary error is exactly epsilon=1e-3 in the PREVIOUS secondary normalized
gradient units. It is a research diagnostic, not a production tolerance.
Primary SVD results were frozen and pushed at86efe2f BEFORE secondary
query-frame projection and epsilon curves. No witness, horizon, epsilon,
model parameter, or metric was tuned. The accepted theorems are premises.

## 1. Dense versus independent result

| Case | n | T | P | Exact fiber D | Primary robust D / bits | Secondary robust D / bits | Old bits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dense | 2 | 11 | 10 | 20 | 1 / 1 | 1 / 2 | 0.0 |
| independent | 2 | 11 | 8 | 8 | 1 / 1 | 1 / 1 | 0.0 |
| dense | 3 | 22 | 21 | 63 | 0 / 0 | 2 / 2 | 0.0 |
| independent | 3 | 22 | 15 | 15 | 1 / 1 | 1 / 1 | 0.0 |
| dense | 4 | 37 | 36 | 144 | 0 / 0 | 1 / 1 | 0.0 |
| independent | 4 | 37 | 24 | 24 | 0 / 0 | 0 / 0 | 0.0 |


The secondary improvement is real within this certificate: dense widths2/3/4
give1/2/1 robust directions and2/2/1 packing bits; independent gives1/1/0
directions and1/1/0 bits. This does NOT certify that the rest of the reachable
region lacks robust directions. These are LOWER certificates from a bounded
grid, not maxima or upper bounds. The same method/units/head convention and
horizons apply to both families. Independent has fewer parameters, explicitly
reported; this is a structural comparison, not a matched capability result.

Dense old raw radii4.24e-17,3.40e-29,1.36e-43 map through the smallest
parameter RMS to normalized ball guarantees1.048e-18,7.509e-31,2.815e-45.
All give zero old bits at this epsilon. The independent old-method radii are
NEW same-method comparators, not previously archived facts:1.124e-13,
3.504e-15,5.009e-18, also zero bits. The certified old effective dimension at
the declared error is zero in all six cases. Bit gains are additive; division
by an old zero-bit bound is undefined.

## 2. Coordinate convention and complete spectra

h units are unchanged. History perturbations are in input SD sqrt(3/32).
S_phi=S_theta D_theta, D_theta=archived R/W/b group RMS. Effective adjoints
use q=ones/sqrt(n), beta=max(1,Frobenius R), and the SAME future preactivation
box[1/4,3/4]^n. Error remains Euclidean in phi-gradient coordinates throughout.
No normalization is chosen to improve the answer. Exact parameter values,
input histories and their hashes are preserved in provenance; no new seed.
Widths2/3/4 use T11/22/37 and archived seeds9502100/9602100/9602100.

All raw and normalized singular values are in spectra.csv; complete100-digit
SVD axes/history frames and70-digit spectra are in basis_*.json. These are
HIGH-PRECISION NUMERICAL, not certified ranks or memory dimensions.

| Case | n | Largest | Middle sorted entry | Smallest | Tangent condition | 100/160-digit discrepancy |
| --- | --- | --- | --- | --- | --- | --- |
| dense | 2 | 0.104198 | 4.00468e-05 | 7.44593e-08 | 1.3994e+06 | not required |
| independent | 2 | 0.0683259 | 0.000812621 | 1.60311e-05 | 4262.09 | not required |
| dense | 3 | 0.114173 | 7.66299e-07 | 1.41365e-13 | 8.07648e+11 | not required |
| independent | 3 | 0.139336 | 0.00126423 | 8.00027e-06 | 17416.4 | not required |
| dense | 4 | 0.105257 | 2.95344e-09 | 2.10695e-20 | 4.99572e+18 | 5.982311140778163142973274428847411454247e-85 |
| independent | 4 | 0.119403 | 0.00113782 | 1.11297e-06 | 107283 | 1.962942064070536291368167062513221301112e-98 |


The history kernel is that of J_h at the archived point. Rationalized
directions need not be exact null vectors: normal compensation and the actual
interval center absorb their error. Selected rational-frame Gram defects and
rigorous condition upper bounds are in summary.json; they are essentially1.
Physical input SD and parameter RMS factors are accounted for separately.

## 3. Directional/mixed curvature and joint geometry

CPU interval propagation encloses all gates across each simultaneous history
box. Componentwise directional and mixed h/S second derivatives include
tanh third derivatives and the actual deltaR*h,deltaW*x,delta b injections.
All positive binary64 products/sums round upward; no BLAS reduction is used.
An implicit normal correction holds h exactly fixed. Its first and second
derivatives are bounded by an exact-rational nonnegative Neumann inverse.
These bounds feed a scaled multivariate contraction test for selected S
projections. Every mixed term is included; separate one-axis certificates
are never multiplied without the joint test. See PROOF.md and engine.py.

| Case | n | Uniform fixed-h Hessian Frobenius bounds | Projection aspect ratio | Selected K condition | L condition (numerical) |
| --- | --- | --- | --- | --- | --- |
| dense | 2 | [[0.17340296256258736]] | 1 | 1 | 1 |
| independent | 2 | [[0.08352873080998267]] | 1 | 1 | 1 |
| dense | 3 | [[0.07849794684699765, 0.07324251992749369], [0.07324251992749364, 0.07233238828172664]] | 1.24862 | 1.24862 | 1.00647 |
| independent | 3 | [[0.1169821599936683]] | 1 | 1 | 1 |
| dense | 4 | [[0.16199520975155124]] | 1 | 1 | 1 |
| independent | 4 | [[0.16533145241447905]] | 1 | 1 | 1 |


Primary uses dyadic SVD left functionals. Secondary uses a finite-head Gram
dual output projection, with the SAME SVD history directions. The physical
query norm never changes. Rational inverse preconditioners and scaled
Jacobian residuals are saved for every selected certificate. All12 original
regions/margins replay at256 bits with the ORIGINAL preconditioners/radii,
not newly fitted ones; center inverse residuals are below1e-8.

**Geometry limitation:** a Cartesian product is proved in selected sensitivity
PROJECTIONS, with an exact CURVED constant-h lift. No flat full-S tensor box
is asserted. This is sufficient because joint query-dual inequalities hold
even in the presence of unselected residual coordinates.

## 4. Every selected radius, margin and axis contribution

This table chooses the better chart at PRIMARY epsilon; ties keep primary.
All exact fractions, alternate primary/secondary radii and mixed-curvature
arrays are in certificate_*.json and results_*.json. Displayed decimals round
for readability; integer packing never uses displayed values.

| Case | n | Chosen chart | rho_i | mu_i | mu_i rho_i | N_i | Bits/axis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dense | 2 | frame | 0.0159717 | 0.219106 | 0.0034995 | [4] | [2.0] |
| independent | 2 | svd | 0.0215833 | 0.0557814 | 0.00120395 | [2] | [1.0] |
| dense | 3 | frame | 0.0089367, 0.00715727 | 0.184423, 0.185157 | 0.00164813, 0.00132522 | [2, 2] | [1.0, 1.0] |
| independent | 3 | svd | 0.0261493 | 0.0526444 | 0.00137662 | [2] | [1.0] |
| dense | 4 | frame | 0.00972588 | 0.177465 | 0.00172601 | [2] | [1.0] |
| independent | 4 | svd | 0.0194496 | 0.0349315 | 0.000679404 | [1] | [0.0] |


For width3 dense, bits per direction are1+1. Width2 dense has2 bits in one
direction. A one-position axis contributes0 bits, including width4 independent.
Strongest/median/weakest retained observable half-ranges are explicitly in
summary.json. For the two-axis dense3 product these are0.001648/0.001648/
0.001325; its aspect ratio is1.2486. The one-axis products have aspect1,
which says nothing about the shape of the remaining sensitivity tensor.

The full tangent spectra are extremely elongated, but the certified retained
projection products are low dimensional and not strongly elongated. The full
nonlinear reachable-region shape remains unresolved.

The dual norm is not optimized over every allowed adjoint or every equivalent
tensor functional. In particular, independent recurrence's structural zeros
may permit a sharper dual representation than the generic full-tensor inverse
used here. Some reconstructed query distances greatly exceed their guaranteed
margin. The tables therefore do not establish a dense-over-independent
architectural advantage; both certificate conservatism and true geometry
remain alternative explanations for the small counts.

## 5. Sharper actual future-query inequality

Gamma=(1/4)I+(5/8)11^T gives allowed gates7/8 and5/8. At fixed h, invertible
W realizes these future inputs. Put C_tilde=R^T Gamma. For tensor functional
L_i, B_i=C_tilde^-1 L_i and
mu_i=1/[sqrt(n) beta sum_j norm2(B_i[j,:])]. Outward lower enclosures are used.
For ANY sensitivity difference, D_C>=mu_i*abs(delta projection_i).
Thus this guarantee survives changes in all the other coordinates. Direct
future parameter injection cancels because h is fixed. There is no unjustified
Frobenius/sqrt(n) replacement or independently multiplied axis assumption.

Coordinate spacing is17epsilon/(8mu_i), strictly larger than2epsilon/mu_i.
N_i=floor(2rho_i mu_i/(17epsilon/8))+1 is exact Fraction arithmetic. Product
states>=product N_i and bits>=sum log2 N_i. This is deterministic uniform
finite-state/no-replay memory, not bytes/VRAM or a stochastic average-case bound.

## 6. Why directions were discarded

| Case | n | A small tangent | B curvature bound | C query bound | D joint failure | E conservative/untested | F interval width | G units | H other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dense | 2 | 12 | 2 | 1 | 0 | 0 | 0 | 4 | 0 |
| independent | 2 | 2 | 1 | 2 | 0 | 0 | 0 | 2 | 0 |
| dense | 3 | 50 | 1 | 6 | 0 | 0 | 0 | 4 | 0 |
| independent | 3 | 3 | 2 | 4 | 0 | 0 | 0 | 5 | 0 |
| dense | 4 | 126 | 2 | 9 | 0 | 0 | 0 | 6 | 0 |
| independent | 4 | 4 | 4 | 7 | 0 | 0 | 0 | 9 | 0 |


Counts are diagnostic attributions within the DECLARED certificate/grid,
not a proof of a physical cause or global impossibility. A: tangent amplitude
too small even before this dual penalty at the largest declared half-length;
G: the SAME history direction clears that diagnostic in raw parameter units
but not declared normalized units; B: uniform curvature bounds limit the
certified range; C: finite-query dual lower margin is insufficient. D/E/F/H
were not uniquely attributed by that rule. Stronger query/curvature certificates
may rescue directions; the unsearched tail is not declared intrinsically dead.
The per-axis audit uses nontrivial positions in ANY tested joint product;
such findings from different boxes are never pooled into one robust dimension.

Multiaxis proposal failures are substantial despite zero D in this attribution
table: mixed-sensitivity-curvature failures total
1223;
normal-Jacobian failures total334;
normal-box-inclusion failures total36.
Every rejected proposal is preserved. Zero F is consistent with successful
192/256-bit checks, not a claim that interval overestimation is absent.
Here proposals are local certificate boxes, not new mechanisms or witnesses.

## 7. Weak-direction versus curvature attack

The following are actual CERTIFIED reduced-square comparators using an
UNCHANGED global curvature majorant within each witness. No discarded axis
is silently removed from the main theorem. Additional top4/8/16 cases and
exact rational inequalities are in weak_axis_certificates.json.

| Case | n | Kept region | Axes | Certified common half-range | Improvement vs all axes | Bits at1e-3 |
| --- | --- | --- | --- | --- | --- | --- |
| dense | 2 | all | 20 | 3.73716e-19 | 1 | 0.0 |
| dense | 2 | minus bottom1 | 19 | 2.86433e-17 | 76.6446 | 0.0 |
| dense | 2 | minus ~5% | 19 | 2.86433e-17 | 76.6446 | 0.0 |
| dense | 2 | minus ~10% | 18 | 6.00025e-17 | 160.556 | 0.0 |
| dense | 2 | top1 | 1 | 5.95755e-07 | 1.59414e+12 | 0.0 |
| independent | 2 | all | 8 | 2.33077e-13 | 1 | 0.0 |
| independent | 2 | minus bottom1 | 7 | 3.72945e-12 | 16.0009 | 0.0 |
| independent | 2 | minus ~5% | 8 | 2.33077e-13 | 1 | 0.0 |
| independent | 2 | minus ~10% | 8 | 2.33077e-13 | 1 | 0.0 |
| independent | 2 | top1 | 1 | 4.90993e-06 | 2.10657e+07 | 0.0 |
| dense | 3 | all | 63 | 3.24247e-31 | 1 | 0.0 |
| dense | 3 | minus bottom1 | 62 | 1.67649e-29 | 51.7042 | 0.0 |
| dense | 3 | minus ~5% | 60 | 6.48448e-28 | 1999.86 | 0.0 |
| dense | 3 | minus ~10% | 57 | 1.07448e-25 | 331377 | 0.0 |
| dense | 3 | top1 | 1 | 1.14493e-07 | 3.53104e+23 | 0.0 |
| independent | 3 | all | 15 | 6.37055e-15 | 1 | 0.0 |
| independent | 3 | minus bottom1 | 14 | 1.86616e-13 | 29.2935 | 0.0 |
| independent | 3 | minus ~5% | 15 | 6.37055e-15 | 1 | 0.0 |
| independent | 3 | minus ~10% | 14 | 1.86616e-13 | 29.2935 | 0.0 |
| independent | 3 | top1 | 1 | 1.44329e-06 | 2.26557e+08 | 0.0 |
| dense | 4 | all | 144 | 3.1162e-46 | 1 | 0.0 |
| dense | 4 | minus bottom1 | 143 | 6.40413e-44 | 205.511 | 0.0 |
| dense | 4 | minus ~5% | 137 | 1.06772e-41 | 34263.7 | 0.0 |
| dense | 4 | minus ~10% | 130 | 2.24643e-38 | 7.20889e+07 | 0.0 |
| dense | 4 | top1 | 1 | 2.96022e-09 | 9.49948e+36 | 0.0 |
| independent | 4 | all | 24 | 7.00261e-18 | 1 | 0.0 |
| independent | 4 | minus bottom1 | 23 | 2.94588e-15 | 420.683 | 0.0 |
| independent | 4 | minus ~5% | 23 | 2.94588e-15 | 420.683 | 0.0 |
| independent | 4 | minus ~10% | 22 | 9.13659e-15 | 1304.74 | 0.0 |
| independent | 4 | top1 | 1 | 4.59545e-08 | 6.56249e+09 | 0.0 |


Removing only the weakest dense direction improves the common radius by
roughly77x/52x/206x at widths2/3/4. Removing more of the tail improves it much
further, but even TOP1 retains zero packing bits under the global majorant.
Thus the weakest direction is important but not the sole limitation. The
directional curvature enclosure and query-aligned projection also matter.
The separate sigma_min-squared counterfactuals in weak_direction_diagnostics.json
are HIGH-PRECISION NUMERICAL models, not certificates. No percentage of the
TRUE reachable geometry is inferred from these sufficient bounds.

## 8. Secondary error curve, no retuning

Each curve reuses its frozen PRIMARY-epsilon-selected chart. No radii, axes,
or normalization are reoptimized at secondary epsilon. These are diagnostic
tolerances only. D is jointly certified nontrivial coordinate count.

| Case | n | Frozen chart | epsilon1e-2 D/bits | PRIMARY1e-3 D/bits | epsilon1e-4 D/bits |
| --- | --- | --- | --- | --- | --- |
| dense | 2 | primary_SVD | 0 / 0 | 1 / 1 | 1 / 3.70044 |
| dense | 2 | selected_secondary_frame | 0 / 0 | 1 / 2 | 1 / 5.04439 |
| independent | 2 | primary_SVD | 0 / 0 | 1 / 1 | 1 / 3.58496 |
| independent | 2 | selected_secondary_frame | 0 / 0 | 1 / 1 | 1 / 3.45943 |
| dense | 3 | primary_SVD | 0 / 0 | 0 / 0 | 1 / 3.16993 |
| dense | 3 | selected_secondary_frame | 0 / 0 | 2 / 2 | 2 / 7.70044 |
| independent | 3 | primary_SVD | 0 / 0 | 1 / 1 | 1 / 3.70044 |
| independent | 3 | selected_secondary_frame | 0 / 0 | 1 / 1 | 1 / 4 |
| dense | 4 | primary_SVD | 0 / 0 | 0 / 0 | 1 / 1.58496 |
| dense | 4 | selected_secondary_frame | 0 / 0 | 1 / 1 | 1 / 4.08746 |
| independent | 4 | primary_SVD | 0 / 0 | 0 / 0 | 1 / 2.80735 |
| independent | 4 | selected_secondary_frame | 0 / 0 | 0 / 0 | 1 / 3 |


At1e-2 all bounds are zero. At1e-4 the secondary dense charts give approximately
5.044/7.700/4.087 bits, still only1/2/1 directions. Exact dimension is not
replaced by this scale-dependent sufficient robust count.

## 9. Validation and evidence strength

-12 focused unit tests passed, including outward arithmetic, wide tanh
  monotonicity/range, mixed-curvature versus CPU autodiff, exact affine product
  control, joint query duality with residual coordinates, CPU/frozen parameters,
  and integer-safe spacing.
-8 final artifact checks passed. Primary hashes and all5 archived source hashes
  are unchanged. All12 original selected certificates replay at256 bits.
-Width4 spectra independently agree at100/160 digits.
-15 grid points reconstructed numerically, followed by100-digit CPU forward
  evaluation. Nontrivial pair query distances exceed2epsilon. This is
  HIGH-PRECISION NUMERICAL validation, not the rigorous existence certificate.
-One interval dependency overflow campaign was preserved and corrected before
  primary completion;172.9375CPU-s remain charged. Two output/import errors
  are documented in RUNTIME_CORRECTION.md. No result or threshold was hidden,
  erased, or tuned. Original scientific config unchanged.

CERTIFIED here means a computer-assisted enclosure under explicit IEEE,
dyadic/Taylor and exact-rational arithmetic assumptions. New fixed-h/product
proof and implementation still need independent review; no proof assistant
verification is claimed. Ordinary singular spectra, shape descriptions and
failure attributions are not mathematical certificates.

Verification background: [Rump, Verification methods, Acta Numerica2010](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf).
Such sufficient tests establish a region when they pass; failure alone does
not exclude other regions. The cited work does not certify this implementation.

## 10. Resources, files and stop

Measured CPU:1020.359375s = 17.005990minutes,
including failed attempts and process imports. Process-wall sum:
1045.818513s (not total human research elapsed time).
An additional5s failed-import estimate plus20s administration estimate is
charged separately, giving1045.359375s total charged.
Peak process RAM:437567488bytes (417.296875MiB).
Single-worker numerical jobs/one BLAS thread. Well inside45CPU-minute cap.

GPU/CUDA UNUSED. GPU time0, stage GPU allocations0bytes. Device temperature
not measured because this stage launched no GPU workload; owner's unrelated
GPU usage is not reported as zero. Tiny n<=4 matrices and required exact
interval/rational computations made CPU the appropriate resource. No model
server, GPU dependency installation or GAS-0 operation occurred.

New files are confined to this directory: preregistration/config; interval,
engine, verification, reconstruction, analysis and checking code; all raw
attempts/spectra/bases; primary freeze; exact certificates and replays;
curvature/query/radius/packing/failure metadata; resources, report and proof.
Outside it only Codex_Research.md, SHARED_RESEARCH_MAP.md and the shared CPU
ledger are updated. Prior negatives and unrelated local/staged work preserved.

Commits:72fa7aa preregistration; e41e609 implementation;86efe2f verified primary
freeze/push. The completion commit contains this report and all secondary
evidence; obtain its exact SHA from git log or the owner's final response.

**Single next step:** independent hostile replay/review of the width3 two-axis
curved fixed-h contraction and query-duality product certificate. The result
does not justify an architecture, arbitrary-width robust scaling, production
memory claim, training, Stage C or AMS v10. STOP after this stage.
