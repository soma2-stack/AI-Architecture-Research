# Repeated near-critical filter writing: report

Codex, 2026-10-06. THEORY ONLY. **Author result: PROVED K=2; pending independent
hostile review. Growing-K improvement: STILL OPEN.** No historical theorem,
CURRENT_THEORY.md, AGENTS.md, or main was changed.

## Result in plain English

Repeated writes can leave two independent, robust private spatial signals
after the donor traces have been exactly matched. Keeping both donors and
three different survivor filters very close to criticality lets the credit
grow throughout the same interval. The weaker signal is extremely small per
step, so this proof uses an enormous fixed duration coefficient. It is a
theoretical two-control milestone, not an improved dimension frontier.

### PROVED — scoped joint two-control theorem

For every integer n>=10^1000, use five equal cohorts within one corridor,
two continuously controlled donor rates and three public survivor rates:

    eta=10^-6, delta=10^-30,
    lambda=(eta+delta theta_1,3eta+delta theta_2,eta,2eta,3eta),
    g_i=1-lambda_i/W, W=ceil(10^60 n^(3/4)), theta in B^2.

Both donor controls write at EVERY primary step. After an exact low-tail
trace correction and one common public reset:

| Quantity | New author bound |
|---|---|
| Joint robust dimension achieved | D=2 |
| Complete finite two-spatial-read minimum gain | >=10^-54 W |
| Actual legal-query boundary pair distance | >1000 |
| Antipodal half-margin | >500 at epsilon=.001 |
| Full duration | T=W+ceil(1000 log n) |
| Coordinate-time budget | mT<10^60 n^(5/4)=o(n^(3/2)) |
| Full absolute raw-input norm | <3*10^30 n^(5/8) |
| Physical driven support | 4m, m=5 floor(sqrt(n)/10) |

The gain matrix is a COMPLETE finite **control-to-spatial-read** matrix for
one fixed unit witness in an exactly orthonormal two-parameter-probe space.
It is not an assertion that a K-column gradient matrix has this minimum
singular value for every control. Both spatial reads overlap the same three
survivor cohorts; no separate write epoch or full history is used.

## Why this differs from a single pulse

The controlled gates differ by delta/W at every primary step. The existing
credit is order W and is modified repeatedly. The exact projected flow is
therefore W times a finite rate-dependent response, with uniform complete
error <=W^2/n+sqrt(n). The matched survivor local forcing is public; only
the private response differs. Its two zero-sum spatial moments survive the
common high tail and reset exactly in the reference system.

This is not one donor pulse followed by waiting. There is no substitution
of a public filter for a private chronological write. The accepted pulse
obstruction is unchanged.

## Full dynamics and error ledger

PROOF.md gives the exact full propagator and rank-two Volterra identities.
The new reduction uses an artificial uniformly high comparison on ALL
driven sites, whose sum-zero subspace is exactly reducing. Complete
complement damping bounds its forced response by 16000(1+4eta)n/m. Actual
cohort gate differences feed that complement only at order eta/W. This
includes all bath, front, terminal and Householder renewals.

| Charge | Uniform bound / treatment |
|---|---|
| Complement-to-cohort forcing | 4eta B/W per step, B<35000 sqrt(n) |
| a<1 drift, forcing and discrete-flow error | combined state error E=W^2/n+sqrt(n) |
| Weak continuum direction | sigma_min(J_0)>=eta^3/10^5=10^-23 |
| Whole-ball nonlinear rate error | Jacobian variation <=delta/3 |
| Exact donor trace correction | independent continuous final gates, deviation <2N n^-5 |
| Survivor tail/reset | exact protected multiplier beta>.97 |
| Dense normalized state comparison | <=e_R N(N-1)/2 per history |
| Complete normalized pair query charge | <=8e-9, using corrected inherited ledger |

No uncharged source trajectory, control-policy derivative or omitted raw
input is used. The public center is NOT subtracted from energy. The inverse
lift, source preparation, donor/survivor holding, compensators, dense lift,
trace corrections and reset all count in the inherited full norm bound.

## General K: no improved dilution theorem

**PROVED, narrow limitation:** simply enlarging the equal-cohort,
bounded-constant-rate filter bank is badly conditioned. Its continuum
centered protected-read Jacobian has

    sigma_min <= 2 exp(ell) ell^K/K!, ell=4eta.

A common polynomial survivor-output approximation and Borsuk--Ulam also
give a finite antipodal protected-read upper for this family; see (26).
This does not compress other credit components or arbitrary time-varying
survivor words. A small singular value of a theta-dependent matrix alone
would not prove that finite upper; the polynomial-output argument is needed.

**STILL OPEN:** designing time-varying public near-critical survivor words
and repeated donor codes with uniform gain kappa/K^alpha, alpha<1/2, for
growing K. No new K-dependent robust lower or polynomial dimension exponent
is proved. The verified beta=3/16 remains the frontier.

## Answers to the requested questions

1. Repeated simultaneous writing escapes the single-pulse obstruction in
   this new K=2 family.
2. K=2 is author-proved robust on EVERY antipodal B^2 boundary pair.
3. The complete post-correction/reset finite protected matrix has minimum
   gain >=10^-54 W, in the normalized M v coordinates.
4. For fixed rates and controls, protected gain is Theta(W), hence Theta(T).
5. The local donor traces match exactly; both private zero-sum survivor
   reads retain the above gain. The high tail/reset multiplier is >.97.
6. Growing-K lower scaling is unproved. The immediate constant-rate
   extension has the factorial protected-filter limitation above.
7. No alpha<1/2 result for growing K is achieved.
8. No beta improvement: best verified polynomial dimension stays 3/16.
9. This new D=2 section has mT=o(n^(3/2)) and energy exponent 5/8. It is not
   superlinear dimension and does not lower the superlinear threshold.
10. Independent review should attack the complete five-cohort reduction,
    fourth-order weak determinant, finite-radius uniform bound, exact trace
    matching and protected reset, normalized query and dense comparison.

## Evidence and repository scope

39 small checks passed: exact rational signs/determinant, a full
Householder four-step replay, and 100-digit finite-antipode samples. The
weakest sampled continuum gain was about 3.40206*10^-22. These are
**NUMERICAL EVIDENCE / algebra checks**, not an asymptotic proof.

Final check run: .203125 CPU seconds, peak observed process threads 4,
one arithmetic thread/no workers, peak working set 19,767,296 bytes,
GPU/CUDA usage ZERO. No large model, dataset, training or search was run.

The independent branch starts from b484504, preserving the reviewed prior
multisurvivor checkpoint. Concurrent test work in the primary checkout is
not imported or overwritten. Root navigation predates the user's later
acceptance notices; those notices are the checkpoint premises here.

Global superlinear result, absolute-energy bracket [1/4,3/4], and full-model
gap are unchanged. No practical width, bits, VRAM, training, architecture or
all-RNN inference follows. Stop after this requested branch is pushed.
