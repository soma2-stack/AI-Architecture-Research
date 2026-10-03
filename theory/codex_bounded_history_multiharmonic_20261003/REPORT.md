# Bounded physical-history radius: superlinearity survives

Codex, 2026-10-03. New proof within the existing multiharmonic family,
internally checked and pending independent hostile review. No old theorem
or independent review is modified. No exponent optimization or new regime.

## Result

For EVERY integer n>=10^900, keep the accepted dense family and choose

    F=floor(n^(1/18)), delta=10^(-4) F/(n log n)^(1/4),
    N=ceil(4n log n)+1, q=floor(floor(n/4)/10^6), D=qF.

ONE joint continuous admitted same-endpoint section has

    physical history radius <0.00970048<0.02,
    D>=n^(19/18)/20,000,000=omega(n),
    every boundary antipodal half-margin >999.999649997999>9>epsilon=0.001.

The physical radius is measured in the SAME Euclidean raw-input-history
units, about the public zero-defect baseline X_n(0). It is uniformly bounded
over widths and all combinations in the ball. All endpoints are exactly h=0;
the head, permitted queries, group-RMS gradient units and epsilon do not change.

This proves a NEW bounded-local-radius omega(n) lower, subject to independent
verification of the new radius argument. It is not a small-width numerical
certificate. The accepted 16/15 growing-radius theorem is not re-reviewed.

## 1. Exact source of the old radius cost

The old bound separately charged atanh(h_t)-atanh(h_t^0) and R Delta h_(t-1)
with a per-step norm O(delta), then summed N+O(1) squared norms. Thus
sqrt(n log n) came from the step count, delta from the full gate-word amplitude,
and harmonic normalization was used only to prove sup ||D_t||<=delta.
Preparation is public; the first varying transition and reset add two
boundary costs. Neither causes the growing sqrt(N) factor.

The lost information was cancellation INSIDE each input transition and
the stronger energy bound of projected profiles, not cancellation between
different physical time slots.

## 2. Sharpest radius bound obtained

Orthogonal projection after saturation gives, jointly and uniformly,

    ||s_f||2<=sqrt(d)/(4F),
    ||c_t||2<=delta sqrt(d)/(4F), sum_i c_t(i)=0,
    ||c_t-Pc_(t-1)||2<=pi delta/(2sqrt(d)).

The actual hidden movement uses phi(c)=sqrt(3/20-c)-sqrt(3/20), not a
linear approximation. Its nonlinear mean is at most
delta^2 d/(4F^2 sqrt(n)); this controls the rank-two Householder correction.
The fixed-h endpoint is reached by the exact accepted reset, not a numerical
compensation solver.

Our rigorous whole-section radius estimate is

    R_history <=delta/F
        +16sqrt(N)[delta/sqrt(n)+delta^2/F^2+delta/n].

This includes every input and the dense perturbation. It is not claimed
sharp. On the OLD 16/15 amplitude/frequency choice, its dominant growing
majorant is O(n^(1/30)sqrt(log n)), instead of O(n^(1/3)sqrt(log n)).
An unbounded upper majorant alone does not establish actual radius divergence.

## 3. Constant-radius balance and dimension

Put eta=10^(-4) and delta=eta F/(n log n)^(1/4). The potentially costly
mean term now obeys

    sqrt(N)*delta^2/F^2<=sqrt(5)eta^2.

The node/twist and small per-step terms are bounded by 3eta each, using
F<=n^(1/18) and log n<=sqrt(n) for n>=200. Including boundaries yields

    R_history<=97eta+48eta^2=0.00970048<1/50.

The same one-ball spreading, odd saturation and injective gate-word mapping
give D=qF>=n^(19/18)/20,000,000. Only boundary antipodes are separated;
arbitrarily tiny interior antipodes are not claimed separated. Borsuk-Ulam
therefore applies exactly in the continuous no-replay encoding contract.

No shorter or multiscale window is needed to settle this question. We retain
the already verified window and all its signal/transfer accounting. The
radius formula exposes the dependence on N, without asserting N is necessary.

## 4. Full finite-error ledger

The UNCHANGED permitted-query ledger is

    H>=10^(-17)delta sqrt(n)/F^5-delta-delta^3 sqrt(n)-e,
    e=epsilon/4+2*10^(-9)=0.000250002.

Under our balance,

    degree1 >=10^(-21)n^(1/36)/(log n)^(1/4),
    all odd degree3+ errors <=eta^3 n^(-1/12)(log n)^(-3/4),
    structural/twist loss <=eta.

Even orders cancel exactly; chronological mixed terms and all harmonic
cross-talk remain inside the reviewed bounds. Dense/polynomial error and
the extra actual-query transfer term are both retained in e. Admissibility
and same endpoint are exact, not ledger omissions.

At n0=10^900, the degree-one lower exceeds1000 and grows thereafter.
Subtracting eta, eta^3 and the full e leaves a half-margin
>999.999649997999. Fourier non-aliasing, the spreading/net conditions and
every floor loss hold for all n>=n0. The enormous n0 is deliberately
sufficient, not a prediction of a practical onset.

## 5. Upper bounds and explicit tradeoff

A bounded LOCAL radius does not imply O(n) in this class: the new section
refutes that upper bound. We do not prove a sharp replacement upper bound.
The ordinary counted-statistic O(n^2) reference-memory upper still applies.
Thus the newly derived bounded-radius fixed-feature interval is

    Omega(n^(19/18)) <= d_fixed-feature(n,epsilon,R=1/50) <= O(n^2).

The explicit same-family tradeoff is

    D=floor(d/10^6)F,
    R_history<=delta/F+16sqrt(N)(delta/sqrt(n)+delta^2/F^2+delta/n),
    H>=10^(-17)delta sqrt(n)/F^5-delta-delta^3 sqrt(n)-e.

These are sufficient joint lower-section conditions, not necessity bounds
on all possible sections. No upper tradeoff is inferred from failure of a
lower ledger. The full-model Omega_c(n^2)--O_c(n^2 log n) gap is unchanged.

## 6. Practical meaning and remaining uncertainty

The accepted superlinear phenomenon can no longer be dismissed solely as
requiring a growing radius of perturbations around the public baseline,
IF this new proof survives review. However, the baseline itself depends
on n and has a long fixed-source trajectory. This is NOT a theorem bounding
absolute input energy ||X|| relative to zero. It also does not establish
finite-bit/VRAM requirements, numerical implementation robustness, training
advantage, architecture novelty or a moderate-width effect.

The decisive new lemma is the exact input-transport cancellation together
with the quadratic small-mean bound. That is the single recommended audit
target, followed by checking its constant-radius balance against the existing
query ledger. No new theorem search or architecture stage begins here.

## Checks and compute

17 exact scalar/power checks pass. Three fixed CPU float64 algebra cases
use (n,F)=(200,2),(256,3),(400,4), fixed seeds610301--610303 and diagnostic
delta=.03. They test exact co-moving and rank-two identities, nonlinear mean,
input-step bound, independently accumulated whole-history radius and reset.
They do NOT claim asymptotic spreading or robust dimension at these widths.

First-run identity discrepancies: cosine <=1.58e-18, rank-two <=5.32e-18.
All measured mean and input-step quantities lie below the analytic majorants.
Two clean passes preserve identical diagnostic values. Total measured
CPU0.15625s, wall0.153353s, peakRAM40,624,128 bytes (38.74MiB).
No GPU/CUDA/framework/model-server use. Startup, administration and JSON
serialization are outside these measured checking intervals. Results are
append-only. Independent reviews and old theorem outputs remain untouched.
