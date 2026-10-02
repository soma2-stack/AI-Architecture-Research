# Independent pulse verification and growing co-rotating profile screen

2026-10-02. **Stronger one-pulse theorem verified with arithmetic clarifications.
No superlinear robust section proved. General fixed-feature width remains open.**

This is independent Codex work, based on the accepted hard rotating/dense tanh
model at c=1, gamma=1/n, epsilon=.001, exact endpoint h=0, one public .4ones
source feature, group-RMS units and actual permitted late queries. Claude's
implementation and numerical outputs were not imported or used as evidence.
Historical files and unrelated lanes were left unchanged.

## A. Did the stronger n/4 theorem independently verify?

**Yes, its substantive conclusion does.** Re-derivation establishes

 m=2floor((floor(n/2)-floor(n/4))/2)-1 >=floor(n/4)-2

joint continuous directions for every n>=200, with whole-section admissibility,
uniform physical total-input radius<.44, exact h=0, actual affine selected
sensitivity, a real allowed query, and antipodal half-margin>.00161.
The tiny actual-dense correction is bounded, not ignored. This improves the
linear lower's constant without changing its asymptotic order.

Independent actual-dense numerical whole-sphere minima of the derived affine map:

| Width | Section dimension | Minimum half-separation | Largest sampled input | Sampled physical radius |
|---:|---:|---:|---:|---:|
|200|49|.00347660539642|.4724515|.3658352|
|256|63|.00325101418427|.4727146|.3704298|
|400|99|.00291433335043|.4730520|.3774420|
|601|149|.00267468240673|.4732513|.3826014|
|1000|249|.00243434687917|.4734106|.3877837|

Every half-separation exceeds epsilon. Every boundary antipode therefore has
full separation>2epsilon. The affine map is mathematically exact; its SVD
minima in the table are ordinary float64 numerical values, not interval
certificates. Closed forms were independently cross-checked at80 decimal digits.

### Claims accepted and qualifications

- Bounded q fixed-time pulses have dimension<=qk: independently proved via
  the pulse-state parameterization and Borsuk-Ulam. A continuous counted exact
  pulse-vector decoder is also supplied. Fixed q gives Theta(n) in the class
  containing the one-pulse section; growing q is not covered.
- Single fixed-query selected-group cap r: independently proved. This is not
  an all-query cap and not a full-parameter gradient cap.
- Householder/common-row and two-pulse antipodal identity: independently derived
  and reproduced at n200/400, gaps1 andd/2; maximum relative identity error
  9.76e-14. The tested zero-sum per-pulse fixed-query spectra have49/99 strong
  values, not twice that. This supports the dominant-channel collapse; it
  does NOT prove a universal O(1) excess for all queries/bases.
- Whole-section admissibility, fixed endpoint, coupling, radius, affine dependence,
  permitted query, uniform margin and dense transfer all independently verified.

### Literal claims rejected / corrected without touching Claude's files

1. a<=.995 for all n>=200 is false. Use a<=1: reset bound<.476 remains
   strictly admissible in the original input cube.
2. The displayed rounded product claimed>=.0016181 is actually
   .001617728346399936. Exact rational replay preserves that failed assertion;
   the valid>.00161 margin, epsilon, model and candidate are unchanged.
3. Actual/reference numerical values agree at displayed precision, not exactly.
4. Co-rotating physical tanh gates are NOT generally stationary under conjugation
   by this Householder-mixed O. An explicit nonzero commutator is proved.
5. The purported necessity of rotating-phase channels beyond the observed
   two-pulse channels is a hypothesis, not established by sampled non-additivity.

See VERIFICATION.md for the complete independent argument and rational_checks.log
for the preserved failed literal arithmetic check.

## B--C. Strongest rigorous lower and upper

For the GENERAL accepted one-fixed-feature family:

 floor(n/4)-2 <= robust continuous credit dimension <=(floor(n/2)-1)^2.

The existing selected-feature quadratic encoder has actual all-query error
<2e-9. The general upper is still O(n^2); no general O(n) or O(n polylog n)
upper was obtained. Full R/W/b memory bounds Omega(n^2) to O(n^2 log n)
remain unchanged. Lower sections from incompatible feature histories cannot
be multiplied to improve that full-model result.

New SCOPED results, requiring independent review:

1. One fixed co-rotating profile (arbitrary public T, all admissible profiles):
   an exact profile/Floquet description uses r+1 persistent coordinates,
   plus n forward state if needed. It contains the T1 stronger lower section.
   Its worst-case credit memory is Theta(n). Decoder transient work is unbounded.
2. Changing zero-sum LATENT-CYCLE profiles: exact reference credit is one
   scalar NC trace plus a d-by-d active matrix. d^2+1 coordinates suffice
   with the all-query dense-error ledger. At n200/400/1000 this is
   2501/10001/62501. Any joint section larger than this has an actual
   finite-error antipodal collision, regardless of sampled points.
3. Long SUSTAINED profiles with even d: all active cycling coordinates have
   gates<=.99 and the single remaining slow coordinate has rotation overlap
   <=.5. A two-step transport contracts by
   lambda=sqrt(1-199/20402), uniformly over profile changes. The selected
   active credit's all-query contribution is bounded by

   .3[sqrt(n) lambda^floor(T/2)+412/sqrt(n)]+eta_n.

   For T>=sqrt(n) this tends to zero. A conservative explicit example is
   n>=10^12: one EXACT scalar trace answers all selected-feature queries
   with error<.000125. Thus this long, sustained construction cannot support
   a width-uniform superlinear section. The huge crossover bound is not a
   practical prediction for the tested widths. Short ln(n) blocks and
   weakening gates evade this obstruction.

These bounds concern selected fixed-feature queries, not the entire learner.
Proofs and full assumptions: SCOPED_THEORY.md.

## D. Numerical scaling of growing age profiles

The prospectively frozen primary screen evaluated102 sections /408 JOINT
antipodal pairs, n200/400/1000, with T in
{2,ceil ln n,ceil sqrt n,n/4,n/2,n}. Temporal modes q were1,ceil ln n,andT
(duplicates removed). Four sphere directions per section is deliberately a
SCREEN, not enough to certify its whole boundary.

The history charts use actual coupled physical gates, exact endpoint resetting,
and both sustained and total-dissipation-scaled amplitudes. A separate linear
Euclidean-ball control prevents confusing a broad nonlinear history image with
a small fixed physical perturbation. All whole-ball admissibility is proved.

Query measurement never changes the contract:

- six legal one-step box starts/three sign iterations give a LOWER estimate;
- the weakest sampled pair's FULL operator norm gives an all-permitted-query
  UPPER ENVELOPE, with2eta dense corrections;
- small box lower values alone never establish failure for all future queries;
- these numerical bounds are not interval-certified.

Most favorable initial long-window, q~ln n sustained examples:

| n,T=n | History-chart dimension | Minimum of4 sampled legal-query LOWER distances | Weakest pair all-query UPPER | Largest sampled radius |
|---:|---:|---:|---:|---:|
|200|294|.00798124|.16380038|.54702|
|400|594|.01023994|.13691702|.80344|
|1000|1743|.00328025|.03476862|1.53479|

Threshold is.002. These chart counts grow like n ln n BY CONSTRUCTION;
they are NOT measured robust dimensions. Fifty-five of102 sections pass all
four sampled box pairs;12 contain a sampled pair whose all-query upper is
below threshold. Largest history charts9800/39600/249000 exceed the exact
cycle-family cap: a whole-sphere robustness claim for them is rigorously false.

At T=n the total-budget q~ln n charts have weakest-pair all-query upper
ratios.4763/.5980/.4725 and sampled radii.03457/.03106/.02985. Thus those
particular finite sections exhibit numerical collisions. All three total-budget
linear controls also have numerical upper failures. The sustained linear
control has an upper failure at n1000; its n200/400 brackets remain unresolved.

The histories show substantial finite nonlinear effects; they are not tangent
or raw-matrix-rank counts. Full mixed charts, query witnesses, operator spectra,
query/radius/dissipation curves and seeds are saved in screen_*.npz and CSV/JSON.

### Adversarial follow-up, separately frozen AFTER primary observations

Fixed targets: n200/400,T=n,q=ceil ln n, sustained spread. Two sphere starts,
120 history-gradient iterations each, minimizing an all-query spectral-norm
upper, not RMS. The model parameters never change. A separate reduced Torch
implementation is checked against full NumPy propagation. No new witness/basis
or epsilon is substituted after outcomes.

| Width,start | Legal-query LOWER distance | All-query UPPER envelope |
|---:|---:|---:|
|200,0|.001152904|.015992250|
|200,1|.006253467|.017588527|
|400,0|.002162379|.019173338|
|400,1|.002989173|.014434116|

The first lower is below threshold, but its upper is well above it. None of
these brackets proves an all-query collision or uniform robust separation.
The reduced/full ratios differ only by the deliberately added2eta/.002
ledger, within about1e-13 after subtracting that ledger. Optimization failure
is not a theorem. Every trace, coefficient, and cross-check is retained.

Additional READ-ONLY decomposition of frozen query witnesses found their
responses are in the interacting active block: scalar NC squared-norm shares
are at most6e-26. The initial strong responses are not explained away by one
scalar alone. This is about these particular queries, not worst-case geometry.

## E--H. Superlinear evidence, proof, linear classes, and loophole

- **Evidence for omega(n):** suggestive sampled n ln n chart responses, weakened
  by adversarial results, limited queries/samples, width-dependent radii and
  the sustained long-window asymptotic contraction obstruction. No reliable
  scaling law for ACTUAL robust dimension can be fitted from this screen.
- **Proof of omega(n): NONE.** No section has a verified worst-antipodal margin
  in every direction as its dimension grows superlinearly.
- **Evidence/proof for Theta(n):** rigorous for bounded fixed-time pulses and
  the one-fixed-profile subclass; NOT for arbitrary aperiodic profiles.
- **Strongest remaining loophole:** a growing short/weak-gate age-profile
  section in the noncommuting d-block whose mixed directions remain jointly
  query-visible. T about ln n leaves warmup credit uncontrolled by the
  long-window theorem; scaling gate amplitudes down removes its fixed gap.

There is no basis for declaring the general n^2 versus n^2 log n problem solved.

## I. Single recommended next theorem

Bound the FINITE-RADIUS, actual-worst-query width of the reduced active block
C'=G_A(aO_A C+I), with the true coupled latent profiles, specifically the
short-window and weakening-gate regimes. Seek an O(d) finite-error bound or
one joint omega(d) antipodal section. This is more precise than asserting
stationary rotated gates or extrapolating the four-point screen.

## Validation, resources, provenance, and stopping

-12 final automated tests pass:8 base,2 independent reduced-kernel/gradient,
  2 scoped contraction-algebra tests. Selected sensitivity vs independent
  full autograd; frozen CPU parameters; forward endpoint; binary warmup;
  affine finite sphere; forward/adjoint identity; real future inputs;
  reduced/full geometry; gradient finite differences; gate/projection energy.
-11 valid scalar inequalities replay exactly with rational positive-series
  tail enclosures. Two literal arithmetic claims are explicitly rejected.
  A failed small-width development test and the failed literal scalar claim
  are preserved. Neither changes official science or outcomes.
- Maximum one-pulse affine residual1.79e-12; endpoint error1.39e-17; all primary
  inputs remain inside the original cube. Whole-section bounds, not sampled
  checks alone, establish admissibility.
- Main runner277.4375 CPU-s; adversary280.34375 CPU-s; read-only channel
  diagnostic resource is separately saved. Roughly9.3 measured CPU-min total
  and6.2 active wall-min. Imports/development tests/reporting overhead is
  additional, small and unprofiled; no claim of exact all-task CPU accounting.
- Sampled peak process RAM472,956,928 bytes(.4405 GiB). CPU at most4 declared
  threads. GPU/CUDA workloads, time and attributable VRAM are0. No model
  server or other process was operated.
- Prospective config/code/hash manifests precede official primary and adversary
  outcomes separately. Base repository commit4a8a2dc; original Claude handoff
  was UNCOMMITTED and is identified by per-file hashes, not a fabricated source
  commit. Original bytes are snapshotted for provenance, not used as new evidence.
- Own source, independent raw results, tests/failures, exact scalar checks,
  analysis, mathematical verification, scoped lemmas and state pointer are
  committed only after internal consistency review. No historical evidence,
  AGENTS.md, Claude notebook, GAS-0 file or workload was modified.

STOP after this stage. No architecture, training, new contraction regime,
or broader witness campaign follows automatically.
