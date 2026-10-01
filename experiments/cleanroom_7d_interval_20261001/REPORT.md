# Clean-room second implementation of tightened 7D certificate

## SECOND INTERVAL IMPLEMENTATION AGREES

Frozen independent width-4 confirmation, horizon 37 / P24, epsilon1/1000,
seven unchanged axes/amplitudes/output functionals/preconditioners. Both fresh
192- and256-bit outward interval runs PASS. All original 49 source/output files
remain byte-identical. GAS-0/AGENTS/other notebooks were not edited or run.
No 8D, new witness, architecture, learning, Stage C or AMS work occurred.

## Independence and chronology

Author derives from the accepted PROOF.md and PROOF_AFFINE.md, using a separate
mpmath/libmp directed-rounding backend and symmetric Taylor polynomial ring.
No original kernel, interval engine, jet or contraction helper is imported or
copied. Actual deltaW*x/deltaW*dx injections remain present even under affine
cancellation. All 11 coordinates and mixed implicit terms are propagated.

This is independently implemented software, not a blinded independent author:
the author knows the earlier implementation/headline results. The trusted
mpmath arithmetic library remains a dependency; its version/source hashes
are frozen. Candidate metadata not needed for the calculation is ignored.

- Accepted source commit 622e001; accepted certificate first committed 622e001.
- Method/candidate freeze 24f0648, pushed before official execution.
- Both independent outputs frozen f8ce4dd before reading reference arrays.
- Candidate SHA-256: 87895c3f3742b9a97e51eced5f9d1cf0606103290cedac4c2b0b224977c63f82.
- METHOD_FROZEN.json records mathematical source/input/library/preservation hashes.
- REPLAY_OUTPUT_FROZEN.json records the fresh output hashes before comparison.

## Whole-array comparison

All 52,857 entries of all 8 arrays compared at BOTH precisions (105,714 entry
comparisons). Exact-zero patterns agree. New positive majorants use 192/256-bit
rounding instead of per-operation binary64 nextafter rounding, so tiny numerical
differences are expected. Maximum relative difference is1.69853658783692e-13,
well below the prospectively declared1e-10 tolerance. No constants were tuned.

| Array | Entries per precision | Maximum relative difference at256bits |
|---|---:|---:|
| HH | 484 | 6.724e-15 |
| HH3 | 5324 | 9.561e-15 |
| HS | 2904 | 9.541e-15 |
| HS3 | 31944 | 1.277e-14 |
| y2 | 196 | 2.271e-14 |
| y3 | 1372 | 1.641e-13 |
| fixed3 | 8232 | 1.689e-13 |
| selected3 | 2401 | 1.699e-13 |

The complete normal-normal, normal-tangent, tangent-tangent and selected-axis
mixed derivative arrays, implicit y2/y3, fixed3 and selected3 are included.
Exact dyadic arbitrary-precision bounds are in exact_bounds_192/256.json.gz;
NPZ binary64 upward summaries are for comparison, not primary certificates.
The 192/256 NPZ summaries are bitwise identical; exact rational beta values
differ by at most 1.6641927e-58.

## Fixed-h section

New eta_h=0.044064912334239092; accepted 0.044064912334239315.
Equal normal half-width ah=0.014387130737304688.
Forcing upper bounds: 0.0010862841797873676, 0.0017447733399309187, 0.0015222624927422508, 0.0080111851171567432.
Hidden allowance(1-eta_h)ah=0.01375316308262412.
Maximum forcing/allowance=0.58249764574362906.
Raw history-coordinate radius=0.11504400849617027<1.
Rational nonsingularity of K_h/K/W and nonnegative inverse of I-Eh verified.
This certifies the simultaneous curved fixed-h section, not just its tangent.

## Seven face certificates

Here mu is the amplitude-normalized query dual margin for ell=(KL)_i/a_i.
The residual-safe support metric, permitted 7/8 gate and epsilon are unchanged.
Every row proves antipodal separation>2epsilon=0.002 over its ENTIRE face.

| Face | M3 upper | mu lower | beta lower | Separation >=2beta | Result |
|---|---:|---:|---:|---:|---|
| 1 | 3.22682057374949 | 0.00284299307421488 | 0.00131402165039756 | 0.00262804330079512 | PASS |
| 2 | 0.524466694915698 | 0.00250771745039072 | 0.00228851506989258 | 0.00457703013978516 | PASS |
| 3 | 2.14264467898407 | 0.00203992999868278 | 0.00131145580581984 | 0.00262291161163967 | PASS |
| 4 | 1.15361150894215 | 0.00356477028066345 | 0.00287937694357873 | 0.00575875388715747 | PASS |
| 5 | 1.7374075714147 | 0.00184558074651354 | 0.00131115975273857 | 0.00262231950547713 | PASS |
| 6 | 2.00224147974257 | 0.00196872925941725 | 0.00131175069515257 | 0.00262350139030514 | PASS |
| 7 | 1.1287717557238 | 0.00161496810619905 | 0.00131114637542034 | 0.00262229275084068 | PASS |

Weakest face7 separation>=0.0026222927508406792.
This retains continuous-encoder k>=7 under the accepted contract. It is NOT
7bits,128 pairwise-separated corners, a maximum dimension or practical memory.

## Nearly-tight entries and face 1

New HH3[1,0,0,0] and HS[11,0,0] bounds match the reference to rounding-level
differences (indices and values in comparison.json). A separate signed
univariate chain-rule path scans all 2,048 corners plus center, at 90 digits,
and rechecks the largest sampled value at 120 digits. Ratios actual/bound:
0.998956214663513 and
0.997308563447582; no violation.
These finite numerical checks are NOT uniform certificates; the interval
induction establishes the uniform bound. They confirm the small~0.1% slack
has not been consumed by the1e-13 implementation differences.

Face 1 M3: accepted3.226820573749615; independent3.2268205737494946.
Its third-order penalty is0.0015289714238173142,
beta=0.0013140216503975616. Holding other terms fixed, M3
would have to increase by factor1.2053809806422398
to erase its strict margin. This is a diagnostic, not permission to change bounds.

Exact rational contraction independently verifies ALL 7 M3 upper bounds from
the saved selected3 tensor. A separate100-decimal-digit Decimal path verifies
all 7 query margins; exact squared inequalities and rational beta arithmetic
verify outward direction and strict separation. No ordinary floating-point
cosine or threshold argument establishes certification.

Separate90/120-digit nonlinear fixed-h face 1 midpoint-antipode checks agree:
Phi1 difference=1.99986042588295119883232497726798179277,
numerical dual-query lower estimate=0.00568558934018164249557325450566630858.
Normal compensation~3.41304e-6 is insideah; residuals~1.53e-92/1.21e-122.
This is supporting numerical evidence at one pair, not the all-face proof.

## Validation, repairs, resources

12 synthetic tests passed before freeze, 12 passed in final repeat; 78 exact
comparison/consistency checks and10 final provenance/resource checks pass.
Tests cover directed arithmetic, high-precision tanh gates, repeated/mixed
Taylor indices, signed center/autograd agreement, second/third bounds,
affine cancellation with retained parameter injections, matrix inverses,
frozen inputs, contraction indexing, CPU enforcement and forbidden imports.

One POST-RESULT comparison export bug (numpy.int64 JSON index) is preserved
in comparison_export_failure.json. Formatting conversion only was repaired;
all mathematical checks had passed. No frozen source or output was modified.
No numerical or certificate disagreement was found.

Measured CPU 124.015625s = 2.066927minutes.
Summed measured computation wall 125.946073s, excluding assistant/Git pauses.
Failed export charged 1 CPU-s; unmeasured setup/import/Git allowance 30 CPU-s,
listed separately rather than presented as measured time.
Peak monitored process RAM 286.023438MiB (final synthetic tests);
official replay peaks~62.61/64.46MiB. Initial development test RAM was not
monitored; the same test suite was monitored in the final repeat.
One CPU process/thread, GPU/CUDA0, ownVRAM0; GPU temperature not sampled because
no GPU work was launched. No model server or unrelated process was touched.

## Single recommended next step

Technically ready for a separately preregistered CHEAP NUMERICAL 8D–24D
feasibility screen at the SAME endpoint/metric/query contract, with fixed
candidate rules and a small budget. This means section dimensions 8–24,
not new widths. It does not predict 8D will pass and does not authorize new
official certificates, architecture design or learning. No such screen ran.
STOP here and obtain the next owner authorization.

## Files and scope

All new source, tests, frozen inputs, directed bounds, comparison records,
numerical supporting checks and manifests live in this isolated directory.
Only Codex_Research.md, SHARED_RESEARCH_MAP.md and the new-directory raw-byte
attribute rule were updated outside it. Preexisting changes in Claude's
notebook and GAS-0 remain unstaged and untouched. OUTPUT_MANIFEST.json lists
every new artifact and its hash.
