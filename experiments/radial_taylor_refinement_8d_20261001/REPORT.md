# Third-order margin refinement on the SAME accepted 8D section

## Decision

**SUBSTANTIAL IMPROVEMENT**. Fixed independent width4/T37/P24 confirmation endpoint,
epsilon1e-3, normalized metric, permitted query family, exact fixed-h and
continuous encoder contract unchanged. Candidate byte-identical; no new axes
or amplitudes. Freeze commit 902d4490e675f99e9d0ada18462c06f955e16e07. The new method requires
independent review; no claim that it has already been independently audited.

New weakest guaranteed antipodal separation **0.002294334371825969**,
face 7, relative slack **14.716719%**.
Old weakest separation 0.002048906105769395, slack 2.4453053%.
Slack multiplier 6.0183563.
Frozen success criterion: at least DOUBLE old weakest absolute slack.

## All face bounds and recovered curvature slack (256 bits)

Penalties here are subtracted from beta; separation is2beta. Recovery compares
the complete old whole-box remainder with the new integrated upper remainder.

| Face | Old separation | New separation | Old cubic penalty | New penalty | Penalty recovered |
|---|---:|---:|---:|---:|---:|
| 1 | 0.0025144107269 | 0.00302936350751 | 0.000469713387479 | 0.000212236997175 | 54.8156% |
| 2 | 0.00206985419852 | 0.00277678702705 | 0.000586172161638 | 0.000232705747376 | 60.3008% |
| 3 | 0.00246825175892 | 0.00296942135264 | 0.000386973381437 | 0.00013638858458 | 64.755% |
| 4 | 0.00212103767569 | 0.00264521787383 | 0.000408274001993 | 0.000146183902919 | 64.1947% |
| 5 | 0.00240923469522 | 0.00272087882262 | 0.000241077965933 | 8.52559022308e-05 | 64.6355% |
| 6 | 0.00205813780522 | 0.00246653989967 | 0.000317562151472 | 0.000113361104244 | 64.3027% |
| 7 | 0.00204908651163 | 0.00229433437183 | 0.000181383974989 | 5.87600448907e-05 | 67.6046% |
| 8 | 0.00204890610577 | 0.00260388101541 | 0.00044448830022 | 0.000167000845399 | 62.4285% |

## Attribution, not candidate tuning

| Fixed method component | Weakest separation | Relative slack |
|---|---:|---:|
| Accepted control | 0.00204890610577 | 2.44531% |
| Exact elimination / native gates | 0.00228262814412 | 14.1314% |
| Exact elimination / sharp gates / whole box | 0.00228310167582 | 14.1551% |
| Sharp gates / radial Taylor | 0.00229433437183 | 14.7167% |

All components were frozen prospectively. Exact final-input substitution
retains parameter sensitivities computed with realized inputs HELD FIXED;
it does not differentiate a parameter-dependent history generator. Signed
affine output coefficients are combined before absolute bounds. Sharp gates
use complete polynomial-critical-point lists with outward radical enclosures.
Eight fixed radial boxes cover BOTH halves of each antipodal segment with
exact Taylor integral weights; every joint mixed derivative is retained.
They are derivative subdomains, not a smaller 8D section. PROOF.md gives the
factor1/2 and exact section-identity derivation.

## Hidden section / query unchanged

The reviewed original control regenerated at both precisions with every
complete array identical to accepted archived values. Eta_h=0.0275170420688897;
forcing=[0.002289888873436962, 0.004532670014380009, 0.011884575804712486, 0.006426658863595225], below common limit
0.0146762821477095.
The SAME full curved hidden section supplies valid histories throughout the
original amplitudes. Query mu and center e0 are the unchanged control values;
no extra query power or metric rescaling. At all face margins >epsilon the
accepted continuous encoder argument retains k>=8, not bits/grid states.

## Conditional numerical 9D feasibility

- Seed 410901: proxy beta/epsilon 0.409104; found actual separation ratio 0.69865079; normal usage 0.0169064; NOT PROMISING IN SCREENED SECTION.
- Seed 410902: proxy beta/epsilon 0.33913005; found actual separation ratio 0.63391936; normal usage 0.00569303; NOT PROMISING IN SCREENED SECTION.
Status: COMPLETE. These are sampled numerical minima, not lower-bound proofs.

This phase uses the preregistered two-start balanced per-axis SPSA rules and
fixed endpoint. Winners saved before fresh joint face attacks, no validation
feedback. It invokes NO interval engine for9D. No rigorous9D, 10D, training,
architecture, Stage C or AMS work was authorized or performed.

## Precision, tests, provenance, resources

Both192/256 regenerated from scratch. Maximum beta difference
2.30613e-58. All 53 complete array groups compared;
bitwise identical across precisions: True.
Scalar intervals use declared precision; positive tensors use reviewed
elementary upward binary64, not ordinary midpoint arithmetic.
Synthetic tests and 140 final exact/arithmetic/array/provenance
checks pass. All frozen inputs and previous evidence hashes preserved.
One CPU thread, measured total 150.234375 CPU-s (2.503906min), peak
306.210938MiB. GPU/CUDA/own VRAM zero. Separate repair/import allowances,
if any, are disclosed in repair records and must not be described as measured.
No GAS-0 or other lane notebook touched.

## Stop / remaining uncertainty

STOP after this stage. No global robust-dimension ceiling or architecture
advantage follows. The strongest remaining uncertainty is independent audit
of the new algebraic elimination and radial coefficient bound. Recommend a
bounded independent review/replay of this refinement before any higher-D
rigorous certificate. No further work starts automatically.
