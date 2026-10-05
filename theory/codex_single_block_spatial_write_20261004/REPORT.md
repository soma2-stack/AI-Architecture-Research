# One survivor support: nonuniform spatial writes

2026-10-04. All NEW results below are **PROVED derivations, internally checked, independent hostile review pending**. Accepted historical results and independent reviews are unchanged.

## Plain-language result

Yes: nonuniform gates can turn the existing private common signal into a large zero-sum spatial signal. Briefly erase alternating survivor tuples, restore every survivor high, and clear the nonprotected part. The written zero-sum pattern survives. A different spatial bit can be used for the next write without overwriting the first readout.

This yields a genuine joint section with two robust modes on ONE survivor support, and a general logarithmically growing version. All finished modes occupy the entire same support; no separate permanent survivor block is allocated per direction.

**It still does not yield superlinear dimension.** The price of retaining older reads grows exponentially with the number of written bits.

## Answers and classifications

| Question | Result | Classification |
|---|---|---|
| Theta(kappa) orthogonal mode? | A public high/low spatial mask gives unit zero-sum xi with |xi dot Delta x|>.24kappa before later writes. | PROVED |
| Exact mechanism | Spatial erasure of a private broadcast contrast, then protection in the co-moving zero-sum subspace. | PROVED |
| Two robust modes on one block? | One joint B^2 section, same sites, half-margin>.0024, full norm<8n^(5/8), n>=10^200. | PROVED |
| Largest per-block count established here | Every 2<=R<=floor(log2(n)/8) can coexist in one B^R section. This is a lower, not an optimal maximum. | PROVED |
| Does count grow with n? | R=Theta(log n). | PROVED |
| New D | D=R, hence Theta(log n) at maximal R. | PROVED |
| New coordinate-time | mT<=4*2^R n^(5/4); maximal R gives <=4n^(11/8). | PROVED |
| New full absolute energy | <5*2^(R/2)n^(5/8); maximal R gives <5n^(11/16). | PROVED |
| D=omega(n)? | Not obtained. Complete multi-column corridor remains open. | CONDITIONAL / OPEN |
| Superlinear energy exponent below3/4? | Not proved. 11/16 is the energy exponent for ONLY logarithmic D. | FAILED as a global threshold improvement |

The uniform-gate one-block result is not contradicted: the new history is nonuniform during each write mask. For R=2 both strong state differences are Theta(the total packet credit). As R grows, each retained mode is Theta(n^(3/4)), while total duration is Theta(2^R n^(3/4)); their fraction of TOTAL credit therefore decreases. That loss is paid explicitly.

## Why the joint statement is valid

There is one FIXED unit recurrent-parameter probe v, positive on donor compensators and negative on survivor compensators. Each stage has a donor control theta_e in [-1,1], a public nonuniform survivor mask chi_e, then a public clear interval. All final donor trace corrections are continuous and exact. Survivor schedules are public. Thus all final local traces are the same over the entire section, and the old quantile p=1. Final hidden reset gives the same exact nonzero endpoint to every history.

The mask's private state response on the block is in span{all-ones,chi_e}. Clearing leaves chi_e plus a uniformly small complementary residual. All older spatial characters contain an earlier bit, so a new mask takes chi_K only to chi_K and chi_(K union new_bit); it cannot turn an earlier write into a later single-bit read. The exact character law preserves zero sum at every intermediate step and hence eliminates Householder feedback on the STORED old component.

For arbitrary boundary antipodes of the whole cube, some coordinate is at +/-1. Telescope all controls. The selected coordinate has a fixed finite-amplitude read gap; other coordinate changes have zero ideal read there and only the explicitly bounded complementary residual. This avoids relying on center Jacobians, parameter counts, separate good axes, or monotonicity of intermediate amplitudes. An odd homeomorphism maps B^R to the cube; Borsuk-Ulam gives the continuous credit-memory lower.

Actual legal one-step queries use .25/.75 preactivations on the positive/negative sites of a Walsh character. The same selected query is used for both histories. Its gradient projection onto unit v gives pair distance >.005-9e-9, half-margin>.0024. Full future-query supremum is at least this legal witness; no RMS substitute is used. Dense comparison is charged for the entire horizon once.

## Strong exact negative statements

**PROVED:** every within-tuple zero-sum output functional annihilates PRIVATE reference H=M-L for arbitrary legal tuple gates, because its four rows share V_i. The dense residual is charged, not asserted zero. New useful modes live between tuple means, not inside the three balanced pair modes.

**PROVED, scoped:** any section relying exclusively on a SINGLE fixed parameter probe to witness every antipodal gap has continuous response code in R^n and therefore D<=n. This does not upper-bound the complete fixed-feature operator with many parameter columns.

**PROVED method limitation:** this Walsh scheme uses 2^R equal labels and loses a factor1/2 per later mask, compensated by earlier packet lengths. It cannot produce D=omega(n) cheaply. No universal nonuniform-corridor obstruction follows.

## First failed inequalities / next lemma

- Uniform reproduction of a zero-sum pattern no longer applies during a nonuniform mask: the common private contrast is converted into chi_e, giving (7) in PROOF.md.
- Reusing a spatial bit fails sum chi_K chi_new=0, creating an all-ones component and renewed feedback. Fresh bits fix this in the proved range.
- Replacing the proved 2^R duration cost by O(R) is unsupported: exact old-mode retention coefficient is a product of half-gains.
- Counting several probes as independent robust dimensions is unsupported. One joint ball with uniform legal-query separation is required.

**Single most valuable next lemma:** a multi-probe spatial-write lemma: can a growing set of parameter-column probes share these SAME protected survivor patterns while retaining a uniform joint antipodal legal-query gain, with mT=o(n^(3/2))? This must prove simultaneous independence, not multiply the present count by the number of available columns.

## Checks / resources / global status

312 independent checks PASS: exact Walsh/Householder identities and zero feedback, nonuniform mask formula, repeated-bit failure, within-tuple annihilation, exact scalar corrections, small complete legal histories, common endpoint, public traces, direct local-probe cancellation, full reference energy, and 192/256-bit scalar ledgers. No historical numerical kernel imported. Small histories use a reduced gate-control interval ONLY for algebra checks and establish no dimension; proof uses the full stated controls.

CPU9.0625s, wall9.354616s, peak observed process threads4, every numerical pool1, no workers; peak RAM46,567,424 bytes (44.41MiB); GPU/CUDA calls0. Scalar precision agreement is a numerical cross-check, not interval certification.

Global accepted best remains Omega(n log n) at O(n^(3/4)(log n)^(3/2)). General exponent bracket [1/4,3/4], full-model gap, and absence of practical/VRAM/bit claims are unchanged. Complete corridor is NOT closed. Stop this stage after saving and internally checking the new spatial theorem.
