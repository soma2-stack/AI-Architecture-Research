# Independent verification of the PR #28 repair

Codex, 2026-10-14. Review baseline: `b66b12d68b8bf45fe187f7e9de64980cd9ef4e6e`.
These corrections are on PR #28's existing `claude/multiprobe-memory-20261014` branch.
No training, GPU use, or attempt to prove Hypothesis B. AGENTS.md and every notebook
were untouched. The author diagnostic scripts/results remain historical and unchanged.

## Verdict and precise scope

The repaired Theorem 4 is a valid **conditional implication** for the explicitly
selected group `d_F,E`, `E=diag(0,1,...,1)`, under Hypothesis B and the declared PR #27
bath/protected-set/state-comparison premises. The repair independently checks the
query proof, source and release bounds, integer projections, complete error ledger,
and resource conversion. It does not claim a full independent audit of all of PR #27.

The group is `{u f_s^T:u_0=0}`, of dimension n-1; its redundant zero column can be
retained in the credit matrix. Its selected memory subgroup is included. The omitted
unmasked row-0 direction and full R/W/b metric are not covered by this proof.

The count alternatives apply without imposing D<=n. The resource conclusion explicitly
requires `2 N_3<=D<=n` (and Cor. 3.5's resource consequence requires
`3,600,008<=D<=n`). The ambient n-by-K response bound does not imply D<=n.

Hypothesis B is **OPEN**. Conditional on it, linear D has the necessary budget
`Omega(n^(3/2)/log n)`. This still permits strict little-o(n^(3/2)) budgets and does
not resolve the original problem. That problem remains **OPEN**.

## Exact query cutoff and independent bound

Use exact `HI=sech^2(.25)`, `LO=sech^2(.75)`, and `r_H=-ln(HI)`.
Set `F_s=ceil(ln(1.01 sqrt(k))/r_H)`. For F>=F_s,

    ||nu||_2 <= HI^F sqrt(k) <= 1/1.01 < 1.

This covers every long query, including arbitrary wraps. For F<F_s, live spikes
remain above U-coordinate 2 because F_s<d-3. Expanding U G U bounds the non-spike
recurrence, while A<=1.3, by

    A_j <= HI A_(j+1)+.1719 HI^(F-j)+5/sqrt(k).

The forcing is bounded by

    gamma[(2HI-LO)(A+1)+HI A+(HI+LO)/2] < 4.943 < 5,

and gamma(HI-LO)/2<.1719. The exact-decay continuous maximum of
HI^x(.3436+.1719x) is below 1.159. Together with
(2+5/(1-HI))/sqrt(k)<.0121 this proves A<1.18 and closes the bootstrap.
The conversion to standard coordinates is below 1.2, including its Householder term.

The previous analytic counterexample n=2^1600, F=8954 remains in the independent
checker as a regression. The old cutoff was 8953; the corrected one is 8959, so
that weight is now listed. At F=8960 the uniform-query spike amplitude is below
.914. No enormous matrices are allocated; the checks use the exact uniform-query
formula in log space, supplemented by finite operator identities.

## Initialization, source, group, and readout bookkeeping

Exactly c_1=0 and Delta c_1=0. After the first update, source-row Lipschitz estimates
give `|c_t-1|<=42.1m/n+.41/n` for t>=2. For m>=1 this is <=42.6m/n. The bound
`|c_t|<=1.0022` holds at all t, including t=1, and also handles m=0. A robust section
with positive dimension has m>=1.

For ordinary rows with weights <=1.2, the pair-source readout is at most
`137m min(T,n)/sqrt(n)`. For the fixed spike list, use the norm bound with no
unnecessary 1.01 factor, and include the j>F ordinary list rows:

    total list weight /sqrt(k) <= max_F F HI^F + 1.2 F_s/sqrt(k) < 6.

For F>=F_s, there are at most F list rows and the same norm bound suffices.
The resulting source-spike coefficient is .02415; the conservative statement is
.0242 n^(3/4). At n>=10^8 the ordinary/spike source contributions fit tau/16 and
tau/64 respectively.

Actual and reference query weights are distinguished explicitly. Hypothesis B is
about the R0 readout for the same actual legal future gates. The true readout is

    nu_R^T Delta B = nu_R^T Delta(B-B')
                    +(nu_R-nu_0)^T Delta B' + nu_0^T Delta B'.

The first term is <=8.2e-8 sqrt(n). The query-weight term is <=5.2e-7/sqrt(n),
using `F HI^(F-1)<6.4`. Reference source rows contribute <=.015/sqrt(n).
These unallocated terms together are <2e-7 sqrt(n).

## Integer constants and release

The integer block proof is retained. The coefficient majorants are now
8402 for one-step Cor. 3.5, 1.03e5 for its all-query form, and 2.32e5 for Theorem 4.
The verifier uses conservative lower squared thresholds .0018029 and .0032051,
not equalities with rounded decimals.

Spike block lengths have unrounded coefficient >3e-8 n and, after flooring at
n>=10^8, coefficient >=2e-8 n. Thus ceil(L/b)+1<=12,500,002<1.3e7.
The one-step bound with exact HI has fewer than 1.8e4 blocks. The fixed-list tail
error uses `1.28 HI>1.2`, including the last integer-cutoff row.

The release geometry and start count are preserved. A never-protected path has no
drive/front start: set a_l=infinity, give it no R1 term, and put all earlier
injections in R2. Recent injections are in R3. This avoids charging all time-1
initial paths to a 2m+1 start bound. Short histories instead use
`W=min(T,W'+W_s)`, so t0>=0 and identical complete inputs terminate the proof.

Conservative release bounds, normalized by n, are:

| Term | Verified worst-case majorant | Allocated bound |
|---|---:|---:|
| R2 | .000190183806 | .000191 |
| R3 | .000084703820 | .000085 |
| R1 | .000405909780 | .000410 |
| Sum of allocations | .000686 | <.000690<tau/(32n) |

The R1 intermediate factor is 1.21, not 1.2. Ceiling envelopes are
`4W+Lambda+4<=1.171e6+1.34e4 ln^+y` and
`p<=1.511e6 m(1+ln^+y/151)`.

## Complete error budget and resource conversion

The fractions charged to tau are, in order, bus 1/4, ordinary source 1/16,
spike source 1/64, carrying-cycle profiles 1/4, spikes 1/8, and release 1/32.
Their sum is exactly 47/64. Including dense/query/source-row leftovers gives

    (47/64)tau+2e-7 sqrt(n)<tau.

At the smallest n=10^8, its conservative ratio to tau is below .734375000354.

With D>=2N_3, one of N_1, the quadratic part of N_2, or 2p is >=D/6. The lower
coefficients after including ceilings and revised N_2 are respectively

    .001/(18*1.171e6) >4.7e-11,
    1/(1.511e6 sqrt(6*2.32e5)) >5.6e-10,
    .001/(12*1.511e6) >5.5e-11.

The quadratic branch is proportional to n sqrt(D); D<=n converts it to D sqrt(n).
For y>=1 the other two branch ratios increase, so their minima are at y=.001.
For t=ln^+y<=900 the worst quadratic conversion is at t=900; for t>=900,
t/(1+t/151) increases, so that same endpoint also suffices. The worst ratio to
the claimed coefficient is >1.71. The final factor 890/ln n is conservative after
the stated contradiction branch uses D<=n to bound y by 4.7e-11 n.

Thus the numerical coefficient 4.7e-11 survives. The logarithmic loss is retained;
the finite interval n<=exp(890) is not described as an asymptotic theorem.

## Remaining gaps and non-claims

* Hypothesis B is OPEN; no accumulation/rank-two argument is promoted to its proof.
* PR #27 is an explicit dependency; a full independent certification of that PR is
  outside this repair. Theorem 2 remains a relative implication.
* The unmasked row-0 group and unrestricted-D resource extension are not proved.
* The historical Cor. 3.3 multi-step 553 F extrapolation is marked unverified and
  unused. Its one-step 553 statement retains a conditional remainder and now states
  c_max<=1, with the explicit ceiling-preserving choice N=553.
* Neither a positive strict-budget construction nor a logarithm-free negative
  resolution of the original problem is asserted.

## Reproduction and computation limits

From the repository root:

```powershell
python -I theory/codex_pr28_repair_verification_20261014/checks.py
```

Requires NumPy. Imports no author code. It writes only the separate
`independent_results.json`, including the checked PROOF.md SHA-256. Recorded CPU
runtime is approximately one second. No training or GPU.

The checker independently implements Householder/permutation operations, adversarial
query optimization, weighted block approximations, and two-history release schedules.
It reruns 109 identities, 36 query samples, 700 integer choices, 250 weighted-profile
checks, and 300 release schedules, plus the repaired endpoint/monotonicity arithmetic
and initialization/cutoff regressions. Small finite samples are diagnostics, not
asymptotic proofs; the majorant derivations above and in PROOF.md provide that reasoning.
