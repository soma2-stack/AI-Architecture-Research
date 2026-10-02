# Reachable fixed-feature width: bounded theory result

2026-10-02. **PARTIAL THEORETICAL ADVANCE; GENERAL GROWTH UNRESOLVED.**
New arguments require independent hostile review. No numerical experiments,
new history search, architecture, training, or GAS-0 work.

## Strongest theorem obtained

For the unchanged actual rotating/dense family at c=1, gamma=1/n and
epsilon=1e-3, every integer n>=200 admits ONE continuous same-endpoint history
section with

    m=floor((floor(n/2)-floor(n/4))/2) >=floor(n/8)

independent fixed-feature directions. The public source stays H=.4ones_l;
the endpoint is exactly h=0. All combinations in the section remain inside
the original input cube. The total physical history-input L2 radius about
its center is below .2, independent of width.

Over the entire section, the ACTUAL permitted-query metric obeys

    D_Q(u,v) >=.0013 ||u-v||_2.

Every boundary antipodal pair consequently has query separation>.0026,
strictly above 2epsilon=.002. A continuous no-replay encoder answering all
allowed selected-source queries needs at least m real coordinates.
This is a finite-radius JOINT lower, not tangent rank or separate axes.
It is NOT a certificate at the old numerical radius .05.

The proof uses a constant-source warmup, a simultaneous paired-coordinate
gate pulse, and an exact zero reset. Paired memory states have opposite
signs, so the entire pulse vector is stationary under the frozen rotation.
Squared amplitudes depend affinely on the section coordinates, which makes
the exact selected sensitivity affine on the whole section, including the
dense perturbation. One fixed allowed future input suffices; the query is
not an arbitrary adjoint, and no RMS contract is substituted.

## Best finite-error upper and lower

| Quantity | Lower obtained | Upper available | Resolved? |
|---|---:|---:|---|
| One fixed feature, continuous credit at h=0 | floor(n/8) | (floor(n/2)-1)^2 | No |
| One fixed feature, public linear operator approximation width | floor(n/8) | (floor(n/2)-1)^2 | No |
| Constructed affine patch itself | m | m | Yes, for this patch only |
| Complete arbitrary-aperiodic credit memory | accepted Omega_c(n^2) | accepted O_c(n^2 log n) | No change |

The selected-feature upper is a counted r x r reference sensitivity updated
using actual gates. Its all-query error is at most

    eta_n=a ||H|| e/(n gamma^2) <2e-9 for n>=200.

It stores r^2 credit entries, plus up to n actual forward-state entries while
streaming. It is not full R/W/b credit and not a new generic compressor.
No O(n) or O(n polylog n) upper, and no robust superlinear lower, was proved.

## Weak mixed tail and dissipation

The strong core now has an explicit jointly admissible example. The weak
mixed tail remains unclassified: it may contain jointly redundant directions
or a genuinely superlinear robust section.

PROOF.md sections 9--10 derive a finite gate-difference Duhamel identity and
a source-weighted Gram bound using the accepted adjoint-dissipation budget.
It covers finite changes, actual gates, the coupled source injection, and
all permitted queries. It also retains a necessary term where a gate equals
one and hence has no dissipation. The bound is conditional: no uniform small
Gram tail or low-dimensional family is established. It must not be called a
solution or a reduced equivalent form of the original compression problem.

## Consequence for n^2 versus n^2 log n

Neither side of the full accepted gap changes. A future O(n) fixed-feature
bound would still require compatible simultaneous feature summaries and a
counted continuous online update. Conversely, a superlinear fixed-feature
section cannot simply be repeated over incompatible histories to obtain a
logarithmic full-memory lower.

**Next step:** independently audit the finite joint section and its dense
correction; then seek a finite-radius worst-query tail bound for multigate
innovations. No new numerical sweep is recommended here.

## Evidence and resources

- Rigorous status: mathematical derivations, conditional on accepted frozen
  family/query bounds and the accepted continuous antipodal theorem. New
  derivations have not yet received independent hostile review.
- Checks: manual identity, normalization, complete-ball admissibility,
  exact affine sensitivity, dense correction, strict margin, storage, and
  finite gate-difference audits; detailed in CHECKS.md.
- No automated tests, numerical simulations, SVD, tensor calculations,
  benchmark, or training were added or run in this theory-only task.
- Experimental CPU time: 0; GPU/CUDA time: 0. Administrative reading/writing
  and proof reasoning were not CPU-profiled; no measured peak RAM is claimed.
  No model server or GPU process was launched by this work.
- Original diagnostic, accepted proofs, AGENTS.md, other-lane notebook edits,
  and unrelated GAS-0 changes were preserved.
- New files: PROOF.md, REPORT.md, CHECKS.md, PROVENANCE.json in this directory.
  Only the Codex resume and shared research status receive new entries.

Stop after this stage. No gamma=1/n^2, architecture, or learning work.
