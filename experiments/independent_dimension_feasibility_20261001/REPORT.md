# Cheap numerical feasibility screen: fixed independent width 4

## Result

Highest promising screened joint dimension: **10D**.
Lowest clearly failing tested joint dimension: **11D**.
The approximate transition is **10–11D for these screened Cartesian sections**.
This is NOT a true robust-dimension ceiling or an upper bound for the model.
The previous rigorously certified 7D result remains unchanged. No higher
dimension was proved and no rigorous certificate was attempted.

Same central endpoint/history/parameters, n=4, T=37, P=24, epsilon=1e-3,
original parameter-RMS/input-SD gradient units, permitted scalar-head queries.
All sampled selected sections enforce the same final hidden state; residuals
are near floating-point rounding. Full fixed-h sensitivity dimension remains 24.

## Main table

These are found actual minima, hence UPPER numerical estimates of the unknown
all-face infima. Positive sampled minima do not prove uniform separation.
The cubic column is a sampled worst penalty mu_i*|Phi_i^(3)|/6, over joint
directions/path points; it is NOT a uniform third-order bound. Units are the
same normalized gradient units as epsilon. Normal usage gives actual sampled
compensation relative to that candidate's declared normal allowance.

| Joint dimension | Weakest actual separation found | Ratio to 2epsilon | Normal used / allowance | Max sampled cubic penalty | Numerical assessment |
|---|---:|---:|---:|---:|---|
| 8 | 0.007857720294 | 3.92886 | 0.010547 / 1 (1.05%) | 0.0010239 | promising |
| 10 | 0.003770524298 | 1.88526 | 0.045011 / 1 (4.5%) | 0.0023729 | promising |
| 11 | 0.001749729435 | 0.874865 | 0.094253 / 0.125 (75.4%) | 0.033309 | below threshold |
| 12 | 0.001378547427 | 0.689274 | 0.027889 / 0.125 (22.3%) | 0.0087428 | below threshold |
| 16 | 0.0001757461049 | 0.0878731 | 0.034909 / 1 (3.49%) | 0.0081946 | below threshold |
| 20 | 5.137116373e-06 | 0.00256856 | 0.032744 / 1 (3.27%) | 0.0045082 | below threshold |
| 24 | 5.757708039e-07 | 0.000287885 | 0.017358 / 1 (1.74%) | 0.0021559 | below threshold |

11D is the one primary binary refinement. The table includes its separate
direct-amplitude improvement and the analogous secondary 12D improvement;
all primary values remain preserved in results.json and dimension_*.json.

## Fixed-h construction and physical domain

Higher-D screening uses last-input normal coordinates, enabling explicit
x_T=W^-1(atanh(h0)-R h_(T-1)-b). This is a different local section chart at
the SAME endpoint, not a new recurrence or a new physical error metric.
Realized input histories are held fixed for parameter sensitivities; the
input compensator is never differentiated with respect to theta. Section
derivatives with respect to tangent variables include compensation correctly.
Numerical checks compare them with finite differences (max error
2.9751e-11).

All amplitude optimizations obey raw-history chart radius<=1, a_i<=4,
a_h<=1. Primary direct sections used radius cap 0.65/normal allowance 1;
secondary uses allowance 0.125 and radius<=0.95, inside those SAME domain rules.
These cap choices influence the approximate transition; no global range claim.

## Query metric

Disjoint independent support makes the permitted-query supremum
D_C=sech^2(1/4)*||diag(R_owner)Delta_s||_2/(sqrt(4)*max(1,||R||_F)).
Here Delta_s is the vector of all 24 normalized supported sensitivity
coordinates. R_owner repeats each diagonal recurrent weight on its six
parameter-sensitivity coordinates; it is not a new normalization.
The same accepted future gate family realizes/approaches this maximum.
The third-order dual proxy retains the conservative 7/8 gate. Fixed h cancels
the future direct-parameter injection. Full supported sensitivities are used,
not selected projections alone; arbitrary residual coordinates are retained.

## Reviewed third-order method plausibility

Ordinary float64 positive majorants, all mixed terms, implicit derivatives,
and both affine tightenings were used ONLY as numerical proxies. Aggregate
third contractions avoid a large third tensor. The known 7D calibration differs
from accepted beta values by at most 3.4694e-18.
No interval arithmetic was invoked in the screen.

For the BEST small proxy-oriented section at each dimension, the table below
reports the weakest proxy face. These are DIFFERENT candidates from the larger
direct-geometry winners in the main table. Proxy penalty is mu*M3/6, with
whole-box NUMERICAL majorants; it is not a rigorous lower certificate.

| Dimension | Proxy beta/epsilon | Linear mu at weak face | Cubic penalty at weak face | Actual sampled ratio on SAME proxy section |
|---|---:|---:|---:|---:|
| 8 | 1.02445 | 0.00146894 | 0.000444488 | 1.29309 |
| 10 | 0.0377852 | 0.000162416 | 0.000124631 | 0.174487 |
| 11 | -0.0271307 | 5.96051e-05 | 8.67357e-05 | 0.0640156 |
| 12 | -0.0768861 | 4.26538e-05 | 0.00011954 | 0.0458164 |
| 16 | -0.470096 | 1.55314e-05 | 0.000485627 | 0.0037123 |
| 20 | -25.3123 | 0.000139353 | 0.0254517 | 0.000242287 |
| 24 | -1.4836 | 6.2755e-05 | 0.00154635 | 1.15875e-06 |

**8D is plausible for the existing certificate method**, but its best proxy
margin is only ~2.45%; prospective exact rounding/bounds would still need proof.
**10D is geometrically promising but the reviewed global bound does not pass**.
Its large direct section fails the majorant hidden guards before a full M3
bound is formed. This must not be misreported as a nonexistent section.
For 11D and 12D the selected secondary sections also fail global majorant guards,
yet actual fixed-h solves remain valid. Their decisive negative evidence is
an ACTUAL below-threshold antipodal pair, not proxy failure alone.

| Dimension | Strongest observed bottleneck | Plausibility of certification |
|---|---|---|
| 8D | Small proxy margin after the third-order penalty | Plausible; numerical proxy has only 2.45% slack |
| 10D | Global hidden/curvature majorants on the larger section | Actual geometry promising; present proxy does not pass |
| 11D | Face 1 loses separation under joint amplitude competition | Selected boxes fail; no impossibility statement |
| 12D | Face 1 loses separation despite a stronger new direction | Selected boxes fail |
| 16D | Weak tail, face 16 | Not promising in screened sections |
| 20D | Much weaker tail, face 20 | Not promising in screened sections |
| 24D | Very weak tail, face 22 | Not promising in screened sections |

## Bottlenecks and refinement provenance

At 11D the added eleventh face itself passes strongly; face 1 fails from joint
nonlinear interference/amplitude competition. After rebalancing, its ratio is
~0.874865; the eleventh face ratio is~2.943. At 12D face 1 remains the limiter,
~0.689274; the new twelfth face is~1.329. Thus the failure cannot be described
as simple disappearance of the newest direction.

At 16D,20D,24D the weak tail becomes the limiter (faces 16,20,22 respectively).
Query-weighted tangent condition numbers rise from ~34 at 8D to ~2.45 million at 24D.
Fixed-h numerical formation succeeds throughout; it is the query separation
and joint nonlinear geometry that fail in the tested products.

Primary method frozen/pushed bc7bc61 before scores. All 6 requested dimensions
ran, then one 11D binary refinement. The first bracket was 10D/11D; its 11D
failure was on an old strong axis. Secondary direct-amplitude rules were
explicitly frozen AFTER those observations in 4c10ea5, BEFORE secondary scores.
This is disclosed as an adaptive diagnostic, not retrospective preregistration.
All 111 primary records are unchanged. It remains cheap numerical research.

Secondary winners were hashed/saved before validation. Search-pool ratios
11D~2.738 and12D~1.209 collapsed under independent fresh face attacks to
~0.875 and~0.689. This is concrete optimization-pool overfitting; no validation
counterexample was fed back into search. As 12D failed, further 14/15 refinement
was not run. All failed proposals are preserved.

## Checks and limits

Selected worst pairs were independently recomputed at 60/90 decimal digits,
using original rational model/history and binary-frozen numerical axes/amplitudes.
Maximum float/high-precision separation difference is
3.4694e-18. This is numerical
validation, NOT an interval proof. Sampled third derivatives include terminal
compensation and actual parameter injections; diagnostics.json stores every
axis penalty, spectrum and high-precision pair.

Basis overlap: minimum absolute diagonal 1, maximum off-diagonal
3.2113e-12. The two proposed bases are effectively sign-equivalent.
Their agreement is weak evidence; this did NOT broadly test unrelated bases.
Other bases, ellipsoids or non-Cartesian sections could improve 11D or more.
No useful global robust-dimension upper bound has been established.

The strongest remaining uncertainty is whether a different joint geometry
avoids the strong first-axis collapse. This screen locates an approximate
failure region for its charts, not the model's intrinsic maximum dimension.

## Resources and files

28 primary amplitude runs /
13636 numerical proxy evaluations;
8 secondary runs /
9608 numerical objective evaluations.
One CPU worker/thread; measured CPU 2.431510 minutes, summed computation
wall 147.227974s, peak RAM 104.30469 MiB. Setup/import/Git allowance 15 CPU-s
separately. The 900 CPU-s cap was respected. GPU/CUDA/own VRAM 0. No model server,
GAS-0, training, width 5, Stage C, AMS or architecture work.

Sanity, frozen-source, original-evidence, primary-record, query-pair precision,
section-usage and resource checks pass. New source/results live only in this
directory; shared map and Codex resume are updated append-only. No old negative
results or 7D artifacts were overwritten. OUTPUT_MANIFEST.json records hashes.
A report-string syntax error prevented the first summary export; it was fixed
without running or changing any scientific computation. The failed export
and repair are recorded in summary_export_failure.json.

## Stop

Stop here. No certification is authorized by this task. Current method's
strongest practical certificate prospect is 8D; 10D needs tighter geometric
control before a serious certificate attempt. A new owner task must select
the next step. No 11D impossibility, architecture superiority or discovery claim.
