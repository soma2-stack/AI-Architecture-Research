# PR #27 audit-driven corrections and verification

**Final cross-PR addendum:** [FINAL_CROSS_PR_ADDENDUM.md](FINAL_CROSS_PR_ADDENDUM.md)
corrects a further missing gate on the injection in Lemma 1.3. The historical
snapshot and results below are preserved; the new full-recurrence regression is
`check_full_post_gate.py`. Theorem 1 and the imported foundations are unchanged.

Codex, 2026-10-15. Repair base: `118b1e66ea327af0738249fc613208a544c4df60`, branch
`claude/narrow-capture-hub-20261013`. Compatibility target: PR #28 at
`3746747137bb681ceda9c0f21b19e66d264165d1`.

**Current lens:** repair the exact findings of the independent foundation audit.
**Stage:** proof corrections, CPU verification and publication on the existing branch.
**Strongest preserved result:** the scoped K-probe barrier, with coefficient 2.9e-10.
**Withdrawn directions:** total hole credit bounded by own injections, exact finite
destruction, incorrect post-gate order, a geometric zero subsphere and upward-rounded
thresholds. **Remaining open:** Hypothesis B, the general neutral-path tax, unrestricted
multi-probe strict-budget sections and the original frozen dense-tanh problem.
**Next action:** review this correction record; no attempt to prove B in this phase.

## Verdict

The independently audited foundational results and Theorem 1 are preserved. No change
to the state dynamics, frozen R, input legality, initialization, fixed feature or
recurrent normalization is made. False auxiliary claims are replaced by precise
own-part or explicitly conditional statements; their negative evidence is retained.

The earlier audit was independent of Claude's proof. The same auditor has now applied
the corrections and rerun independently implemented mathematical checks. This does
not claim an additional third-party review of the new commit. Exact identities and
inequalities below supply the mathematical verification; finite tests have their
stated scopes and are not substitutes for uniform proofs.

## What changed and what was preserved

| Finding | Correction | Preserved result |
|---|---|---|
| Total hole credit omits bus arrivals | Exact decomposition b=A+D with own injection and bus delivery recurrences; cycle own bound and off-cycle repeated-coordinate bound stated separately | No homogeneous l2 amplification; cycle-own sqrt(L) bound |
| Post-gate order aP(UGU) | For btilde=Ub, use a(UGU)P, with memory blocks explicit | Exact Householder transport |
| Exact one-step destruction | Require an explicit front-mass condition and retain the nonzero O(1/sqrt(k)) leakage | Conditional front attenuation and exact contrast identity |
| Bath-floor rounding | Rational bounds valid for all integer n>=1e8, including odd n | c0=5e-5, s_lo=.025 unchanged |
| Horizon gap in the floor proof | Compare chains with the same actual J; sum the a-contractive errors geometrically | All-horizon bath and protected-set statements |
| Nonorthogonal probes | Choose an orthonormal basis of the fixed masked span; K is its rank | Same certified parameter span and Theorem 1 |
| Public support versus zeros | Public envelopes of width m; exact-common-support case coincides with actual support; actual dense corrections are charged | Original public-schedule result in its precise accounting scope |
| Subsphere and .33n inference | BU gives an antipodal zero; retain exact tau/Dg and exact gate constants; require one-step certification for the one-step inference | Exact box-support functional |
| Rounded resource ratio 5.9e-4 | Use exact infimum 1/1700 | 2.9e-10 public and 1.9e-10 union coefficients |
| Summaries and source conventions | Correct protected count/state bound, ln K dependence, parameter-group scope and source resets | Lemma/equation numbers and PR #28 imports |

The older author verification and exploration notes have explicit historical correction
notices rather than having their earlier mistakes silently erased. The prior full
audit is copied byte for byte to [AUDIT_20261014.md](AUDIT_20261014.md).
AGENTS.md, CODEOWNERS and all lane notebooks are untouched.

## Exact mathematical checks

### Own content is not total content

For the local memory skeleton S (partial cycle shift, off-cycle identity, no wrap),

```
A_t=G_t^mem[aS A_(t-1)+c_t(Ev)^mem],
D_t=G_t^mem[aS D_(t-1)+a 1_(>=1)J(b_(t-1))
                              +a gamma e1 Sum'(b_(t-1))/sqrt(k)],
b_t=A_t+D_t.
```

The equality is exact for reference credit. A cycle own path has distinct parameter
positions, so Cauchy–Schwarz gives the retained c_max sqrt(L) bound. An off-cycle own
path repeats v_j and is bounded by c_max |v_j| min(T,n). Actual dense forcing requires
its separate perturbation charge.

The old total bound is refuted by a legal neutral hole j>=d with v=e_(d-1): its own
injection is zero, yet B3(j)>0 through the bus. The archived checker retains the
n=128, T=3, m=1 counterexample with total credit .12124873254040437 and maximum raw
input .05. It is not a counterexample to the repaired theorem.

### Correct transport and nonzero leakage

For post-gate reference credit,

```
U G_t a O U = a (U G_t U)P,
Ou=e1+(gamma/sqrt(k))(e0-u).
```

Under the additional condition |Sum'|>=s_lo k/2 at n>=1e8, the front preactivation
has magnitude >=s_lo sqrt(k)/2-2, giving g1<=4exp(-s_lo sqrt(k)+4). Hence

```
||aGO(alpha u)|| <=a|alpha|[g1+gamma||e0-u||/sqrt(k)].
```

The bath floor alone does not supply that mass condition. All exact finite tanh gates
are positive, and R0 is invertible: no nonzero homogeneous packet is annihilated.
The exact identity ||G(alpha u)-alpha gbar u||=|alpha|std(g) is retained. Nothing here
bounds accumulated repeated bus transport or proves the neutral-path tax or B.

### All-horizon chain error and bath induction

Using the same actual J in each virtual F_t chain gives

```
e_(r+1)<=a e_r+rho,
e_A<=rho(1-a^A)/(1-a)<=min(A rho,n rho)<=4e-8/sqrt(n).
```

With gamma<=7071/7070, (m+1)/k<=10002/99999999 and n rho<=4e-12,

```
bath preactivation >=1/20-(7071/7070)^2[224(10002/99999999)+4e-12]-3/7070
                    =.027164853275575...,
atanh(.025) <=2399/95940=.025005211590577....
```

The independent certificate evaluates these as exact Fractions. The excess series is
certified by upward-rounded integer operations plus its full tail, with start-1 upper
bound 221.021047106976...<223. The moving-bath gap decrement exceeds .29 s_lo^3, so
Lambda=450000 is retained. Protected size is (m+1)(Lambda+1), ordinary outside states
exceed .0124, and kappa remains .00015.

### State-only comparison and source reset

The separate coupled comparison still assumes W<=T<=n^(3/2). It uses auxiliary
differences, not independently generated R0 histories with different global fields.
The source convention is explicit: retain actual initial source differences and
reset freshly scheduled sources whose actual predecessor/input differences are listed
as zero. Unscheduled sources use their lambda self-map. Memory and row-0 resets retain
their original meaning. This makes the auxiliary construction consistent with both
the full K-probe listing and PR #28's state-only listing.

The preserved bounds are

```
||u_s||2<=2sqrt(n)q^s,   ||u_s||infinity<=2q^s,
||Delta h-u||infinity<=3delta sqrt(n)/kappa.
```

The credit Sum listing is explicitly over j=1,...,k-1, excluding row 0 even for actual
R. This is the Sum' used in the front identity. The r-th credit column is B(:,r)=C v_r;
the old extra B v_r notation is removed. A pre-window protected row is connected to
its protected ancestor at t0, not asserted to have the same row index at both times.

They use no credit cancellations. For the credit estimate, the full listing supplies
the additional credit cancellations. Both direct H forcing and the exact gate term
Delta g=-(h+ +h-)Delta h are included. The analytic W-ratio cap is 297739.880799...,
giving eta<=3.223530442776e-7<3.3e-7 in the short-budget branch. The auxiliary query
remainder is analytically <1.46e-11. W=T uses exact equal histories instead.

## Reproduction and measured results

From the repository root, with Python 3.11.9 and NumPy 2.4.6:

```powershell
python -I theory/codex_pr27_repair_verification_20261015/check_foundations.py
python -I theory/codex_pr27_repair_verification_20261015/check_repairs.py
python -I theory/claude_narrow_capture_hub_20261013/checks.py
python -I theory/claude_narrow_capture_hub_20261013/verify_p1p2_sweep.py
```

All four completed successfully. CPU only; BLAS/OMP threads were limited to one.
The foundation suite took about 7 seconds, the new repair-specific suite about .25
seconds, and the author diagnostics about one second plus the small constant sweep.
There was no training or GPU use. No n-by-n array at theorem-scale n was allocated;
the n=100000001 reference histories use identical-coordinate cohorts and a short wake.

| Independent repair check | Result |
|---|---|
| Full credit equals own plus bus, 60 steps at n=32,33,64,101 | Maximum residual 1.19e-13 |
| Cycle own bound and off-cycle geometric bound | Maximum bound ratios .999383 and .719519 |
| Correct post-gate order | Maximum residual 6.09e-15; wrong order differs by up to 2.7051 |
| Exact uniform/contrast identity | Maximum norm error 5.56e-17 |
| Explicit front condition, positive/negative mass and odd/even n | 288 cases pass; no bath-implies-mass assumption used |
| Scalar box functional | All 64 vertices for 200 vectors, maximum error 8.89e-16 |
| Geometric error summation beyond n^(3/2) | Exact rational bounds pass |
| Integer floor edges | Odd/even n and m-threshold changes pass |
| Fresh source reset with nonzero auxiliary predecessor | Actual predecessor difference zero; forcing identity error <3.1e-17 |
| Public/union resource coefficients | Exact 1/1700 gives 2.94117647e-10 and 1.96078431e-10, preserving stated coefficients |

[results.json](results.json) preserves the full foundation suite, including the original
counterexamples and negative controls. [repair_results.json](repair_results.json)
records the new checks, a hash of the corrected proof, and the pinned PR #28 proof hash.
Neither checker imports the author implementation. The author diagnostics were run
additionally and their tracked checks_result.json was refreshed.

The foundation suite's small, manually initialized comparison fixture is not a robust
section from zero to a common endpoint. Its outside-scope perturbation stress and
step-13 loss of a positivity premise are clearly marked. Only the first 12 steps of
that fixture satisfy its checked comparison premises. Finite diagnostics do not prove
uniform separation over every boundary point; the structural/analytic proofs provide
the uniform statements. The infinite-series and bath-margin checks are exact
computer-assisted certificates rather than float-grid evidence.

## PR #28 compatibility and remaining unproved claims

PR #28 remains at 3746747 and is unmodified. Imported Lemmas 2.1–2.5, estimates
(3.1)–(3.8) and constants retain their numbers and values. The strengthened bath
comparison requires no new assumptions. Theorem 4's state-only use stays inside
T<=2.5e-5 n^(3/2), so it does not extrapolate the coupled-state horizon scope.

Its group {u f_s^T:u0=0} includes source directions; this note's fixed probes use
memory rows 1..k-1. The shared state estimates do not depend on the parameter group.
PR #28's own source-channel and credit decomposition remain responsible for its
larger group. Nothing here upgrades a selected-group bound into a full-gradient bound.

PR #28 Theorem 2 still prints the old intermediate 5.9e-4. The correct 1/1700 gives
its advertised coefficient 1.9e-10, so its conclusion does not require a branch edit.
The residual editorial discrepancy is documented rather than silently changing PR #28.

The repaired foundations support Theorem 4 **conditional on B**, in exactly its
declared setup. Its resource claim additionally requires 2N3<=D<=n and remains

```
mT>=4.7e-11 D sqrt(n) min(1,890/ln n).
```

For linear D this is Omega(n^(3/2)/log n) asymptotically, not a universal exclusion of
strict little-o(n^(3/2)) budgets. The never-protected release case and 47tau/64
allocation are compatible with the repaired bath/protected/state lemmas.

**Still unproved:** Hypothesis B, the general neutral-path tax, and a solution to the
original frozen dense-tanh strict-budget problem. The front-mass condition is not
derived from the bath floor alone. No attempt to prove B was made. No claim of a new
primitive, architecture equivalence, or discovery follows. Neither PR is merged.
