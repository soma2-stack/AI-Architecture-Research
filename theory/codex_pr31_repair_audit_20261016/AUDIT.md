# PR #31 repair and independent mathematical audit

Codex, 2026-10-16. Claude remains lead researcher.

Reviewed base: `b32a2ecae06ec1d762f2cd81a11a0e21d90fe9bb`, branch
`claude/lemma-m-bus-capacity-20261015`. Initial worktree was clean. All changes
are confined to this repair, shared status/navigation and verification records.
No AGENTS.md or restricted notebook was read or edited. No training, GPU or merge.
This commit is local; pushing requires owner approval.

## Verdict

**PROVED after repair:** Proposition M1's identity and corrected bounds; the exact
nine-term decomposition; Lemma B's bath ceiling/gap sum; Lemma C's deviation budget;
Theorem M's first-order gather listing in its existing scope; Proposition M2 as an
implication from OPEN Lemma M' with its stated dimension/count condition.

The headline Theorem M bound is preserved:

```
|Psi_M| <= 9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4,
first-order gather residual <=30tau/256.
```

Its scope remains n>=1e8 divisible by 4, actual input support m<=5e-5 n,
undriven source, one-step legal queries; the off-cycle listing requires public
support envelopes of width at most m. This is not a theorem controlling the
entire bus, all future-query lengths, or the full R/W/b metric.

**REFUTED original assertions:** the off-cycle floor-count inference; the
1800000 lower cutoff's use with a 1800004 premise; the 3.9e7 cutoff's 7.6e14
subcount; the .3404 legal centered-weight bound; the arithmetic source bound
21eta<=1e-42 at n>=1e8. These failures and their corrections are preserved below.
No legal counterexample to the corrected Theorem M was found.

**OPEN:** full Lemma M, Lemma M', Lemma M_rest, the proposed off-cycle
counterexample, general centered-channel listing, F-step queries, code-dependent
off-cycle treatment, logarithm removal and the original full-metric strict-budget
linear-dimension problem. Heuristic candidate failures are not proved refutations.

## 1. GitHub review findings

Four inline findings were present, across two reviews of the same base commit.
The owner's request grouped them as three topics; all mathematical comments
are addressed here.

1. [Off-cycle rounding](https://github.com/soma2-stack/AI-Architecture-Research/pull/31#discussion_r4289462343).
   The continuous coefficient is about 1.31777108e8. Replacing a real threshold
   x by floor(x) cannot retain a 1.4e8 coefficient. For example x=1.9 gives a
   possible factor 1.9 in the crude count Q/floor(x), where Q=mT.

   **Repair:** N0=max(1,ceil(x)), list integer counts Nj>=N0. Every unlisted
   count satisfies Nj<=ceil(x)-1<x. Thus the residual proof uses x, while
   the count uses Q/ceil(x)<=Q/x. If x<=1, all driven off-cycle rows are listed.
   This avoids doubling the coefficient; the original 1.4e8 count remains valid.

   More explicitly, with C=c_*(Lam+1)(1+C_chain), unlisted leakage satisfies
   S_j<=2C*x*Nj and sum Nj^2<=x*Q. The pair readout is at most
   `4 HI gamma C x^(3/2) sqrt(Q)/sqrt(k)=tau/64` by the definition of x.

2. [Cutoff premise](https://github.com/soma2-stack/AI-Architecture-Research/pull/31#discussion_r4289462353).
   Replace 1800000 by exactly 4*(450000+1)=**1800004**. Its contribution to
   the near block count is at most 900003, below the existing 910000 allowance.

3. [Resume block](https://github.com/soma2-stack/AI-Architecture-Research/pull/31#discussion_r4289462358).
   The exact commented path is `docs/notebooks/Claude_Research.md`, a restricted
   notebook. The owner explicitly prohibited editing restricted notebooks in
   this task. It is therefore unchanged, and that precise line-level request
   is not claimed fixed. Instead the complete unrestricted RESUME.md, STATUS.md,
   REPORT.md, CURRENT_THEORY.md, INDEX.md and 04_RESEARCH_STATE.md now record the
   current lens, stage, verified result, negative findings, unresolved questions
   and next action. Shared navigation explicitly supersedes old next-action
   pointers while retaining the older snapshots. This resolves shared research
   handoff staleness without violating the notebook restriction.

4. [Actual cutoff coefficient](https://github.com/soma2-stack/AI-Architecture-Research/pull/31#discussion_r4299244776).
   The old chosen constant gave (3.9e7)^2/2=7.605e14, exceeding 7.6e14.
   The certificate formerly checked a different, smaller analytic value.
   **Repair:** choose **3.897e7**, exceeding the independently enclosed
   analytic requirement 38962380.07166869. Its exact count coefficient is
   **7.5933045e14**, below 7.6e14. The certificate now checks the chosen
   constant and the exact cutoff floor, not just a rounded analytic minimum.

## 2. Additional audit findings and repairs

### Legal centered-query bound

HI=sech^2(.25), LO=sech^2(.75), so HI-LO=.343429040525..., not .34029....
Take g0=gi=HI and all other gates LO. For a nonzero row i of U,

```
(Ug)_i = (HI-LO)(1+1/sqrt(k)-gamma/k).
```

At k=50000000 this is .343477601856..., a legal counterexample to .3404.
The corrected uniform bound is **.3435**; |w^T nu|<=HI+.3435<1.29 remains valid.
Small-n identity checks now use the actual finite-k box bound rather than a
theorem-scale constant. A random box sample was insufficient to test this extremum.

### Dense source threshold and monotonicity

The standing dimension is 1e8, not the much larger threshold of PR #29's
counterexample. At n=1e8, eta<=1e-24, hence 21eta<=**2.1e-23**; the old
1e-42 arithmetic bound and its claimed 1+1e-30 amplitude envelope do not follow.

Let c^0 be the undriven R0 source and c=c^0+e. The trajectory forcing discrepancy
is at most eta+(1-alpha)lambda<=eta(1+2lambda). Contraction by lambda and
sigma>=.0499 give |e|<=21eta uniformly in time. Use **c_*=1+1e-12** to bound
all amplitudes and the variation constants, with ample slack at n>=1e8.

The actual dense source need not itself be monotone. Nonetheless its discounted
ordering is exact: for t>=3,

```
c_t-a c_(t-1)
 = (c_t^0-c_(t-1)^0)+(1-a)c_(t-1)+(e_t-e_(t-1))
 >= .99/n-42eta > 0.
```

Here c_t>=.99 for t>=2, from source state>=tanh(.05-eta) and the original
sigma bound. For t=2 use c1=0. Adjacent own-profile columns share all later
path factors; the older column has the extra multiplier a*g<=a. Therefore
the weighted own profiles remain **exactly monotone**, including the dense
case, and cycle total variation is at most 2c_max<=2c_*.

The reference credit uses coefficient a, although the actual forward iteration
uses a'=alpha*a. These are different objects; the proof now uses the correct
discounted inequality rather than assuming a monotone actual source. No surrogate
source or changed normalization is needed.

### BV block rounding

The block-size argument also needed integer rounding. Define
B_L=[tau sqrt(k)/(c_b Q)]^2 and use b_L=max(1,ceil(B_L)), capped at k-1.
For B_L<1, singleton blocks give exact zero residual. Otherwise b_L<=2B_L.
For an arbitrary vector of total variation V, the stronger variance bound is

```
||v-Pi_b v||_2 <= sqrt(b)*V/2.
```

Indeed each block's variance is at most its squared oscillation/4, and the
sum of block oscillations is at most V. For the antipodal pair this gives
`HI sqrt(k) sqrt(b_L) TV`, bounded by the earlier allowed
`2 HI sqrt(k) sqrt(B_L) TV`. Thus the ceiling's count Q^2 scaling remains
valid without a hidden floor loss. The count is at most
`(c_b Q/tau)^2+2`; its coefficient is about **2.034068e14<2.1e14**.

### Other exact constants and scope

- The near readout coefficient is .003384024326..., exceeding the old
  displayed .003384 upper bound. Replace it by **.003385**, still below
  .0566/16=.0035375. Negative capture includes c_* explicitly.
- For dense arbitrary histories, the floor and ceiling comparisons use a'
  and the common field |phi|<=eta directly. Their interval bounds at n0 are
  **floor >.02715817>.025** and **ceiling <.10081526<.1009**. The chain maps
  use only a'<=1, so the imported protected lifetime is preserved. The proof
  no longer relies solely on PR #29's construction-specific state lemma.
- The below-bath minimization yields the increasing comparison map
  `G(x)=2 tanh(x/2)` for x>=2b0 and
  `G(x)=tanh(b0)-tanh(b0-x)` otherwise. Independent interval iteration plus
  geometric tail gives gap sum **505.694898184<506**.
- The decomposition contains **nine terms**, not eight. Z=UB'-O is a
  transformed remainder, not literally U times the standard-coordinate bus;
  the exact own-type correction in Proposition M1 is retained.
- The mT=0 case uses an empty listing; it is handled before formulas divide
  by sqrt(mT). All nontrivial uses have integer m,T>=1.
- The average drift identity gives the valid bound
  `average beta'>=s_lo^3/3-.0759/L`, not the unsubstantiated .045/L constant.
  This remains a scoped identity, not a general neutral-path tax.
- Proposition M2's dimension/count condition is essential. The first-order
  theorem plus an OPEN rest listing with arbitrary extra polylog factors does
  not prove a general logarithm-free barrier. The full targets' logarithmic
  overheads also prevent claiming one is literally implied by the other just
  from their polynomial terms. Those conclusions are narrowed explicitly.
- The large-m reduction only implies T<mu*sqrt(2)*n/epsilon. It gives T<d
  when epsilon>4sqrt(2)mu; no general fixed-point closure is proved here.
- The off-cycle candidate's full-scale orthogonal outputs do not prove uniform
  sphere robustness without an odd gain bound and a uniform error estimate.
  The candidate and centered-channel claims remain ANALYSIS/OPEN.

## 3. Independent verification and reproducibility

No independent verifier imports an author module. Run:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
python -I theory/codex_pr31_repair_audit_20261016/verify_constants.py
python -I theory/codex_pr31_repair_audit_20261016/verify_structure.py
```

`verify_constants.py` uses 65-digit outward-rounded intervals and exact
Fractions. It checks the gap comparison via a different direct tanh formula,
the dense floor/ceiling, actual legal gate extrema, source envelope/discount,
chosen cutoff, three listing coefficients, and **2000 integer-boundary cases**.
For off-cycle tails it checks the exact inequality
`sum_(Nj<x) Nj^4<=x^3 sum Nj`, including x<1, x=1, integral and fractional x.
For BV blocks it checks the count and ceiling inequalities across five lengths.

`verify_structure.py` constructs U P U densely and uses **legal actual inputs**
with magnitude<=.49, including attempted holes only when their required input
is legal. Five histories cover short paths, first front entry, longer histories
and the prescribed dense trajectory. It independently checks all nine terms,
the two-channel identity, cycle variation and captured-profile monotonicity.
It also exhausts step/oscillating block examples for lengths 2..65; the variance
bound's worst measured ratio is 1, so the sharp factor is exercised.

These are finite algebra checks, not theorem-scale simulations. The n>=1e8
constants are proved through formulas and intervals. Their input support is
measured from every actual nonzero control, without amplitude thresholding.

Author checks were separately run from their original directory:

```powershell
python -I constants_check.py
python -I exp_two_channel_identity.py
python -I exp_gather_structure.py
python -I exp_offcycle_leak.py
```

All corrected certificates and structural assertions pass. The old random-target
stress script could require illegal past inputs; it now records that fact and
does not describe those runs as legal theorem witnesses. The original experiment
mechanism is preserved. Raw run logs are not committed; result JSON records are.
Only lightweight CPU work was used, with one BLAS thread; no GPU/model training.

## 4. Research handoff

Use `../claude_lemma_m_bus_capacity_20261015/RESUME.md` for the current shared
resume. Claude's next question is general-section second-order gather closure,
followed by query-uniform centered listings. These are open tasks, not conclusions
of this repair. The requested notebook-specific change requires an owner exception
to the explicit restriction; no such edit or permission was inferred.

The repaired first-order theorem survives without increasing its headline count
or changing the original architecture, legal queries, normalization or actual mT
accounting. The original full-metric n^(3/2) problem remains OPEN.
