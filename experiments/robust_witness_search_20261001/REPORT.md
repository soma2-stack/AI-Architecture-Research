# Robust-witness search

## Classification and direct answer

**ROBUST-WITNESS SEARCH FINDS ONLY SMALL IMPROVEMENT**

At epsilon exactly1e-3, new dense width3 search witnesses certify3 jointly
nontrivial directions,8states,3bits versus the archived2directions,4states,2bits.
Its best untouched confirmation witness certifies only2directions,4states,2bits.
Dense width4 certifies3directions,8states,3bits in BOTH search and confirmation,
versus archived1direction,2states,1bit. These are improved sufficient lower
bounds, but still few directions compared with exact fixed-h dimensions63/144.
The frozen moderate/large criteria were not met; they were not changed.

Thus archived witnesses were not optimal for robust certification. This search
does NOT establish a large robust core or a global robust-dimension ceiling.
Filtering, chosen axes/prefixes, box grids and interval conservatism can miss
larger regions. The tested result supports only a modest local-witness gain.
Independent recurrence also improves, especially at width4, so this is not a
unique architectural benefit of dense interaction.

## Design and immutable inputs

Widths2/3/4, horizons11/22/37, frozen archived parameters, initial h=0,
the same dense and independent families. Dense P10/21/36 and exact supported
fixed-h sensitivity dimensions20/63/144. Independent P8/15/24, supported
dimensions8/15/24. No parameter learning, architecture change or new width.
R/W/b RMS scaling, input SD sqrt(3/32), fixed normalized head/query-frame
conventions and epsilon are unchanged. No GAS-0/server operation.

Search centers lie in[-.5,.5], the archived generator support. Certificate
history perturbations were checked coordinatewise<=1, the existing local
patch domain. Future query preactivations remain[1/4,3/4] under the accepted
fixed-head convention; future inputs may differ from past-generator support,
exactly as in the accepted prior query family. No domain enlargement.

Protocol/config/pools committed before scoring: **1aa89ef**. Implementation
repair/preserved invalid campaign: **5bb034c**. Complete valid search/objective
sealed and committed **deb3a85** before confirmation. All18 histories/axes/
recipes frozen and committed **06eccf9** before interval certification.
`pool_manifest.json`, `models.json`, `SEARCH_SEALED.json` and
`WINNERS_FROZEN.json` contain the input/code/source hashes.

## Phase A: numerical discovery

Ten thousand exogenous histories per width:4000 random,4000 scrambled Sobol,
2000 smooth low-amplitude histories. Deterministic8000/2000 search/confirmation
split. Both models receive the SAME pool/domain/horizon/normalization.
Per model/width, search adds512 Gaussian mutations plus384 spectral/SPSA
evaluations (8parents x16iterations x3evaluations). Confirmation has no
adaptive generation. Valid Phase A counts are:

- 30,000 paired exogenous histories;60,000 model-history evaluations.
- 5,376 adaptive evaluations across six model/width cells.
- **65,376 valid initial/adaptive evaluations total.** Repeated shortlist
  calculations are additional derivative work, not new proposed histories.
- Per cell:128 histories pass stage2 query screening;24 reach full mixed-
  curvature proxy recipe evaluation. Search and confirmation use the same
  shortlist limits; confirmation pool size is smaller by design.

Stage1 emphasizes many strong fixed-h singular directions, not sigma_min.
Stage2 includes accepted dual query margins. The PRIMARY objective is fixed
lexicographic `(joint nontrivial packing directions, integer packing bits,
sum observable ranges)`. A whole simultaneous-box floating curvature majorant,
implicit hidden-section calculation, query-aligned projections and all mixed
terms determine the numerical proxy. Prefixes1/2/3/4/6/8 and the three
amplitudes/two profiles/two normal factors were frozen before results.
Only one selected recipe per winner is certified; no post-failure tuning.

GPU runtime: isolated `cupy-cuda12x[ctk]==14.2.0`, CUDA12.9 component wheels,
float64, batch128. CPU/GPU derivative and curvature calculations were
cross-checked. Torch's existing CPU installation and all model servers were
left alone. Runtime package versions are in runtime_packages.txt.
Runtime installation follows [CuPy's official installation documentation](https://docs.cupy.dev/en/stable/install.html).
No GPU midpoint, SVD, proxy or exploratory output is labeled CERTIFIED.

### Baseline / selected numerical scores

Each score pair is baseline/new. Primary pairs are approximate directions,bits.

| Width | Model | Role | Stage1 | Stage2 | Primary proxy |
| --- | --- | --- | --- | --- | --- |
| 2 | dense | best_search | 13.7471 / 15.2249 | 4.5707 / 4.9420 | 1,2.000 / 2,2.000 |
| 2 | dense | untouched_confirmation | 13.7471 / 14.4585 | 4.5707 / 4.8833 | 1,2.000 / 2,2.585 |
| 2 | independent | best_search | 8.9530 / 10.1088 | 2.3297 / 2.5680 | 0,0.000 / 1,1.000 |
| 2 | independent | untouched_confirmation | 8.9530 / 9.4604 | 2.3297 / 2.5044 | 0,0.000 / 1,1.000 |
| 3 | dense | best_search | 20.3751 / 20.6626 | 4.5780 / 4.6884 | 2,2.000 / 3,3.000 |
| 3 | dense | untouched_confirmation | 20.3751 / 20.6459 | 4.5780 / 4.6822 | 2,2.000 / 2,2.000 |
| 3 | independent | best_search | 17.8227 / 18.9208 | 4.0764 / 4.3375 | 1,1.000 / 1,1.000 |
| 3 | independent | untouched_confirmation | 17.8227 / 18.0489 | 4.0764 / 4.1751 | 1,1.000 / 1,1.000 |
| 4 | dense | best_search | 24.5492 / 25.7475 | 4.0628 / 4.5721 | 1,1.000 / 3,3.000 |
| 4 | dense | untouched_confirmation | 24.5492 / 25.7471 | 4.0628 / 4.5719 | 1,1.000 / 3,3.000 |
| 4 | independent | best_search | 24.2289 / 27.7583 | 4.7443 / 6.8126 | 0,0.000 / 1,1.585 |
| 4 | independent | untouched_confirmation | 24.2289 / 27.6331 | 4.7443 / 6.7936 | 0,0.000 / 2,2.585 |

All per-history spectra and stage1 scores are preserved in compressed NPZ;
full finalist spectra/curvature/query comparisons are in
conditioning_comparison.json and geometry_comparison.json.

## Phase B: rigorous CPU certification

All18 preregistered candidates passed192bit certification AND verification
of their original product/margins at256bits. **Zero certificate failures.**
Fresh interval RTRL/input jets regenerated endpoint derivatives; no previous
Jacobian or curvature cache was used. All normal-normal, normal-tangent,
tangent-tangent and mixed selected-axis majorants were generated on the
complete simultaneous history box. Implicit normal compensation keeps h
exactly fixed; scaled contraction certifies the entire selected product.
Arbitrary unselected sensitivity differences are included in query duality.
CPU mpmath100digits initializes a rational preconditioner once, not a new
search recipe. Uniform intervals and explicit upward majorants verify it.

The integer rule is exactly
`delta_i=17epsilon/(8mu_i)`, `N_i=floor(2rho_i/delta_i)+1`.
Different product grid points have query separation>=17epsilon/8>2epsilon.
Reported log2(state counts) is the exact symbolic bit bound; decimals are
rounded views. A literal integer-width binary memory requires the ceiling.

| Width | Model | Archived directions/bits | Role | Certified directions | States | Exact bits lower bound |
| --- | --- | --- | --- | ---: | ---: | --- |
| 2 | dense | 1 / 2.000 | best_search | 2 | 4 | 2 |
| 2 | dense | 1 / 2.000 | untouched_confirmation | 2 | 6 | log2(6) |
| 2 | independent | 1 / 1.000 | best_search | 1 | 2 | 1 |
| 2 | independent | 1 / 1.000 | untouched_confirmation | 1 | 2 | 1 |
| 3 | dense | 2 / 2.000 | best_search | 3 | 8 | 3 |
| 3 | dense | 2 / 2.000 | untouched_confirmation | 2 | 4 | 2 |
| 3 | independent | 1 / 1.000 | best_search | 1 | 2 | 1 |
| 3 | independent | 1 / 1.000 | untouched_confirmation | 1 | 2 | 1 |
| 4 | dense | 1 / 1.000 | best_search | 3 | 8 | 3 |
| 4 | dense | 1 / 1.000 | untouched_confirmation | 3 | 8 | 3 |
| 4 | independent | 0 / 0.000 | best_search | 1 | 3 | log2(3) |
| 4 | independent | 0 / 0.000 | untouched_confirmation | 2 | 6 | log2(6) |

Runner-ups match the best-search direction/state counts in every cell; all
three roles and their complete certificates are in summary.csv/json and
certificates/. Dense width4 has3x the archived direction count,3x its bit
bound and4x its distinguishable-state count; width3 search gains one axis/
one bit and2x states, but confirmation does not repeat that gain. Dense width2
search gains one axis but no bits; confirmation has6states versus archived4.
Independent width4 search/confirmation improves from an archived0-bit
certificate to3/6states; a bit-ratio to zero is undefined.

## Conditioning, curvature and query interpretation

| Width | Model | Role | Largest singular-value ratio | Effective rank baseline -> new | Counts>=1e-3 baseline -> new |
| --- | --- | --- | ---: | --- | --- |
| 2 | dense | best_search | 1.055 | 3.554 -> 3.794 | 6 -> 6 |
| 2 | dense | untouched_confirmation | 1.081 | 3.554 -> 3.601 | 6 -> 6 |
| 2 | independent | best_search | 1.080 | 2.475 -> 2.694 | 4 -> 5 |
| 2 | independent | untouched_confirmation | 1.100 | 2.475 -> 2.536 | 4 -> 4 |
| 3 | dense | best_search | 1.044 | 5.545 -> 5.302 | 9 -> 9 |
| 3 | dense | untouched_confirmation | 1.042 | 5.545 -> 5.299 | 9 -> 9 |
| 3 | independent | best_search | 1.076 | 4.213 -> 4.470 | 8 -> 9 |
| 3 | independent | untouched_confirmation | 1.072 | 4.213 -> 4.200 | 8 -> 8 |
| 4 | dense | best_search | 1.154 | 8.091 -> 7.639 | 15 -> 12 |
| 4 | dense | untouched_confirmation | 1.154 | 8.091 -> 7.635 | 15 -> 12 |
| 4 | independent | best_search | 2.627 | 6.888 -> 6.273 | 13 -> 14 |
| 4 | independent | untouched_confirmation | 2.725 | 6.888 -> 5.791 | 13 -> 12 |

These are NUMERICAL tangent diagnostics, not certified memory dimensions.
In particular dense width4's count>=1e-3 decreases15->12, and effective rank
decreases8.091->about7.64 despite its better product certificate. Its largest
singular value rises only~15%; width3 rises~4%. Improving raw spectral richness
alone therefore does not explain the certified gains. Local directional/
mixed curvature and query alignment matter jointly. Raw projection mu or
curvature entries are not directly invariant under changes of L; compare
observable products mu*rho in the unchanged physical gradient metric.
No factorial causal ablation of these contributions was performed.

Every retained/discarded coordinate in each frozen recipe has its exact mu,
rho, observable range, N and bit contribution stored in the certificate;
all uniform raw Hessian tensors are compressed in curvature_*_192/256.npz.
The scalar spectra remain GPU numerical values; the product/range/query
conditions are rigorous under the accepted rounding model.

## Search versus untouched confirmation

Width3 dense loses the third certified direction on confirmation: possible
selection/adaptive-witness overfitting or rare favorable histories. Do not
report that third direction as a replicated confirmation property.
Width4 dense repeats3directions/8states, so its local gain is not confined to
adaptively optimized search histories. Width2 dense and width4 independent
have stronger confirmation packings than their search winners. No broad
distributional guarantee follows from comparing two selected extrema.

## Secondary epsilon arithmetic

Primary summary was frozen in PRIMARY_FROZEN.json before secondary counts
at1e-2/1e-4 were calculated. secondary_epsilon_curves.json uses ONLY the same
certified products/margins, not new axes or reoptimized boxes. It does not
change primary epsilon or classification and does not extrapolate outside
the certified region.

## Implementation anomalies, validation and limits

The first search attempt improperly carried dense adaptive histories into
the following independent model, breaking matched counts. It is preserved
under invalid_attempt1/; both models reran from scratch after an isolation
test was added. No confirmation primary scores had been opened, and no
objective, scientific threshold or budget-per-valid-model was changed.

An early nullspace/margin unit check used confirmation history0 at width3;
it did not inspect a robust score or tune the objective. The test now uses
dedicated development randomness. That low-level exposure is disclosed;
none of the six frozen confirmation winners is that history. Their scores
were first inspected only after the complete search/code seal.

Eight current numerical/split/parity checks pass;12 accepted interval/jet/
curvature machinery checks pass. Final artifact checks verify18 winners,
exact packing arithmetic,256bit original-target verification, frozen hashes
and preservation of all98 prior evidence files.
No search/certificate hardware safety failures, NaNs or OOMs occurred.

A bounded staged/prefix search and conservative local sufficient certificate
cannot establish that only three robust directions actually exist. No
arbitrary-width robust law, finite-precision VRAM requirement, SGD advantage,
learning result or architecture discovery is claimed.

## Resources

All attempts/tests/checks, including the invalid campaign, are charged:

- CPU **872.109375s / 14.535156min** (60s administrative estimate separately).
- GPU-active-phase wall UPPER bound **714.735485s / 11.912258min**;
 2s preflight estimate separately. Kernel-only GPU time was not measured.
- Sum of post-import job wall times **961.331241s**; whole interactive
  documentation/wait time not metered.
- Peak process RAM **784.722656MiB**.
- Peak GLOBAL VRAM **1752.000MiB**, including pre-existing contexts;
  peak our CuPy allocator pool **160.144MiB**, excluding library/context
  overhead. Do not interpret the pool as complete process VRAM.
- Peak GPU temperature **44C**, below the80C preferred/86C stop limits.
- Frozen neural parameters; no optimizer learning, model inference server,
  GAS-0, Stage C, AMS v10, new architecture or width5 operation.

## Frozen winner history hashes

Full histories and rationalized axes/functionals are in frozen_winners.json.
Its SHA and selection metadata are sealed in WINNERS_FROZEN.json.

| Width | Model | Role | ID | History SHA-256 |
| --- | --- | --- | --- | --- |
| 2 | dense | best_search | spsa_5_12 | 68a3518a24e682ee4ee50619b4b7740b0c9258c0e5acaae534ffeb63f599ed95 |
| 2 | dense | runner_up | spsa_6_4 | d326d810b0c50e43b60cbe7edc91b0e1d1685e902a6ef9473fbe9ae0a8cf1f9b |
| 2 | dense | untouched_confirmation | 7283 | a467954ed9662ea76575cc4bf7e70e20437a765e04857f1ef2e950b235eff98c |
| 2 | independent | best_search | spsa_3_21 | d80aa465221cc51476e8e4e2bb63d607db7871c3049a61085dc76eb496abef61 |
| 2 | independent | runner_up | spsa_2_21 | 96957a3998ee43a5656890f2c20141ed3a7a9ed9f2a45ca673c2fbe829a1408d |
| 2 | independent | untouched_confirmation | 1251 | 324ed0c4ab294ffea76c4bbfbbfdc84a79745d71e86abf69fa674fb0d029dc43 |
| 3 | dense | best_search | spsa_11_18 | b24bed74cef80cb127f4b281dc457300783ebc057886a8b7cab4944bdc47632e |
| 3 | dense | runner_up | spsa_10_2 | 196a2bfeb45324b91acedeb1d1b72bca3eacbab9009089d80de12b38672e4cd0 |
| 3 | dense | untouched_confirmation | 8255 | 996fba6a342650ebc9751c1a1b7cafe6f317da47a720051101336fe79e0ee0e8 |
| 3 | independent | best_search | spsa_15_5 | 62c71422cdf55100f6f36c2c4dca88d220ab751544fcf197632142dfdeb20ed0 |
| 3 | independent | runner_up | spsa_15_11 | 3f67f4291c52af87a2c8f3dd12db65b4c84f10751b60e5d07c6f214c8d30116f |
| 3 | independent | untouched_confirmation | 3560 | 1932a3b0c3e977dec26e93bd18d6bae3581ee4b128574b21fdbea5372866bc75 |
| 4 | dense | best_search | spsa_15_0 | 82d8a9e9e00ce4c630169d03c853b5e3fd3f028d86b11a3e49fad217d542adf1 |
| 4 | dense | runner_up | spsa_13_11 | ec422b3a5eb6d34b4d6ae1a23c046d338a1f8683e836ef26299132d22603d432 |
| 4 | dense | untouched_confirmation | 8971 | 91041887128c61e07cfe05e61bd2863d4e55db5f9c0a78196c4040c7b8b87e53 |
| 4 | independent | best_search | spsa_7_0 | b28554bd0e8741b1e635b6017da2bb5bd5cf307b82f2ed15093f5ed26dbdc353 |
| 4 | independent | runner_up | spsa_10_0 | 6a283cec108f10384ef1fbca93feb616bbcd0e98396b5edd2adf730ab9ce8d9d |
| 4 | independent | untouched_confirmation | 9242 | 10e5809b0d89a055a08a19c2c3e6f1ca797ff192a631312108642fc03983444d |

## Single recommended next step

Independent hostile review of the newly certified three-axis dense products
and the sealed search/confirmation validity. Stop here; these small local
gains do not authorize architecture invention or learning experiments.
