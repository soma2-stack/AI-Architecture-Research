# Nonzero autonomous endpoints under bounded absolute history energy

Codex, 2026-10-03. **NEW THEOREM, internally checked; independent review
required.** Earlier accepted results and review records are unchanged.

## Result

In the SAME frozen hard dense family, replacing zero by the autonomous
endpoint makes the bounded-energy class genuinely nonempty. However,
**superlinear fixed-feature robust credit does not survive fixed absolute
input energy at sufficiently large width.**

The strongest new result is an upper bound, not a failed-witness inference:

    uniform normalized past-credit query magnitude
      <= sqrt(l)(L_n+H_R)/n
      <= (L_n+H_R)/sqrt(n),

where L_n=O(log n) and H_R is independent of n/horizon for a fixed absolute
budget R_abs. Thus a zero-past-credit decoder becomes epsilon-correct.
Keeping the exact forward state takes n persistent coordinates; credit
needs zero. No replay, clock or public sensitivity cache is necessary.

**Reader path:** PROOF.md sections 1--6, then section 12 (THEOREM 4).
Sections 7--10 preserve a valid but weaker intermediate template argument.
They are not the final encoder or the strongest energy bound.

## 1. Exact endpoint and its scaling — THEOREM

Use the unique public solution

    h*_n=tanh(R h*_n+.05 1_n).

Existence and uniqueness follow from ||R||op=1-1/n<1. Zero input holds it.
There is no distinct autonomous periodic orbit. For every n>=10^6,

    h*_i >=m=1/50,
    m sqrt(n)<=||h*||_2<sqrt(n).

This last lower bound is proved for the exact dense model, using a scalar
fixed-point construction for its Householder/cycle reference and the rigorous
perturbation error <=4/(10^8 sqrt(n)). No large-width floating-point root
calculation is used as proof.

It lies OUTSIDE the old weak-gate cube. At h* the effective recurrent Jacobian
has norm at most a(1-m^2); its gate-induced contraction gap does not shrink
with width. Persistent source H=.4 1_l, prescribed near-identity gates and
the old driven harmonic resolvent are no longer valid assumptions around it.

## 2. Query legality — THEOREM

Given a legal future preactivation v, take x_future=v-Rh-.05 1. This realizes
the same [1/4,3/4]^n preactivation box at ANY current endpoint. Subsequent
queries repeat that construction. Inputs are then frozen for derivatives.

The head, loss normalization and group-RMS units are unchanged:

    q=1_n/sqrt(n), beta_loss=max(1,||R||F), w_R/beta_loss=1/n.

The effective current adjoint has norm <=a/beta_loss. This bounds EVERY
permitted query, not an RMS sample. Future raw inputs may be large; the
accepted constraint is on future preactivations, not their input energy.
The R_abs promise here concerns the ENTIRE PAST raw-input history.

Direct future parameter contributions depend on the common current state
and the future word, so they agree between histories at h*. The decoder
computes them exactly. It discards only the past fixed-feature contribution,
not the whole queried gradient.

## 3. Exact cheap baseline and complete energy ledger — THEOREM

Let z_B=f^B(0) be the zero-input autonomous trajectory from the REQUIRED
public initial state. Choose B so

    kappa^B sqrt(n)<=min(R_abs/2,1/4),
    kappa=10000/10001.

Use B zero inputs and ONE final correction

    x_(B+1)=R(h*-z_B).

This lands exactly at h*. Its FULL absolute history norm is exactly
||R(h*-z_B)||<=a kappa^B sqrt(n), with every preparation and correction counted.
Holding thereafter has exactly zero input cost. All raw input coordinates
are <.5 in magnitude. For R_abs=1, this baseline norm is <.25 and squared
energy <1/16. A longer public zero burn-in makes it arbitrarily cheaper.

Starting at h* for free was NOT assumed. Zero input from zero only approaches
h*; the final correction is essential for this exact endpoint construction.

The fixed bias is part of the unchanged model dynamics. The requested input
budget is sum||x_t||^2; no additional cost for model bias or hidden-state norm
has been silently added or subtracted.

## 4. Best bounded-energy robust section

The cheap baseline supplies a feasible zero-dimensional section. No positive
epsilon-robust antipodal dimension is possible once the upper theorem's
sufficient width condition holds, at ANY common endpoint and public horizon.
Consequently no omega(n) section, exponent or positive asymptotic half-margin
is established here. This conclusion applies to all joint sparse-packet,
harmonic, wavelet, burst and amplitude schedules inside the same energy budget,
not just candidates attempted independently.

If exact forward state is maintained during the history, an explicit continuous
causal encoder is

    E_t=h_t in R^n,
    E_(t+1)=tanh(R E_t+x_(t+1)+b).

The query decoder starts the past selected sensitivity at zero and computes
the supplied future's direct contributions from the TRUE stored h_t. At a
public terminal h*, no private hidden-state summary is needed for this query.
No credit, clock, gate word or history tape is stored.

## 5. Strongest exact theorem and all-query margin bound

For the selected memory-row/source-column R block, hence for every fixed
source direction in that block, let

    L_n=ceil(log(100sqrt(n))/log(10001/10000)),
    B_R=ceil(10000(1+10000R_abs)^2), H_R=B_R+10000.

For n>=10^6, every finite raw-input history of norm <=R_abs has

    ||past sensitivity||_(Euclidean parameter group -> hidden l2)
                 <=sqrt(l)(L_n+H_R).

Under the ACTUAL permitted-query supremum, normalized past-gradient error
from dropping this sensitivity is at most

    delta_0(n,R_abs)=sqrt(l)(L_n+H_R)/n.               (A)

This tends to zero uniformly in horizon at any fixed R_abs. For epsilon=.001,
one explicit sufficient condition for delta_0<=epsilon/2 is

    n>=ceil(max{10^80,(40008/epsilon)^(20/9),(4H_R/epsilon)^2}). (B)

For R_abs=1, n>=10^80 is sufficient. This enormous bound is NOT a practical
onset estimate. Our coarse formula is useless at moderate widths.

Every antipodal pair at a common endpoint and common time has half-distance
<=delta_0. At (B), this is <=.0005<.001, ruling out any positive-dimensional
section with the required half-margin. Unlike the old zero-endpoint result,
the class is not empty: section 3 gives exact feasible histories.

Counted persistent state: **n total forward coordinates; 0 credit coordinates**.
This is a theorem about this fixed-feature query contract. PROOF.md section 13
also checks all three accepted normalized gradient groups within the SAME
bounded-energy family. Their total past error is bounded by

    1.1(L_n+H_R)/sqrt(n)
         +2R_abs[sqrt(L_n)+sqrt(H_R)]/n ->0.

Thus the n-state/zero-credit decoder still works if the query must return
every R,W,b entry. Its explicit full-gradient onset is given in (43); at
R_abs=1, epsilon=.001, n>=10^80 suffices. This is not a theorem for other
loss/normalization models or RNN families, and not the unrestricted
full-model worst case.
Temporary query computation/output storage is excluded as in the accepted
model; no working-RAM, runtime, finite-bit or VRAM bound is inferred.

## 6. Nonlinear and transport ledger — THEOREM

The decisive global scalar inequality is

    |atanh(z)-atanh(p)| >=(1+p^2/4)|z-p|, |p|>=m.

It follows by integrating atanh'>=1+y^2; the average square is
(p^2+pz+z^2)/3>=p^2/4. Applied against h* it gives radial contraction
||h_t-h*||<=kappa||R(h_previous-h*)+x_t||.

After L_n, the entire time-l2 deviation from h* is <1+10000R_abs. Therefore
at most B_R time steps can have deviation >m/2. At other times every gate
is <=9999/10000; at exceptional times transport norm is still <=a<1.
The sum of all past transport envelopes is <=H_R. Fresh coupled injection
norm is bounded by sqrt(l), giving (A).

This ledger is global and nonlinear. It includes all mixed effects, all source
and gate-history variations, dense corrections and all past input slots. No
Taylor truncation or old epsilon/4 approximation ledger is used in (A).

For mechanism interpretation only, the exact local expansion is

    u_next=G* v - h* .* (1-(h*)^2) .* v^2 + r3,
    v=R u_previous+x, ||r3||_2 <=||v||_6^3/3.

The nonzero quadratic term prevents assuming the old odd/even parity. The
old harmonic signal also loses its growing n/f resolvent at the autonomous
state. Neither observation alone is the impossibility proof; (A) is.

## 7. Energy--dimension--margin tradeoff

For a positive-dimensional section with half-margin >epsilon, (A) implies
L_n+H_R>epsilon sqrt(n). A conservative explicit necessary condition is

    R_abs > [sqrt((epsilon sqrt(n)-10002log n-10001)/10000)-1]/10000,

when the right side is real and positive. Thus even ONE robust direction
requires growing absolute energy, asymptotically at least

    (sqrt(epsilon)/10^6)n^(1/4)(1-o(1))-10^(-4).

The constant is deliberately conservative. This is not the sharp energy
threshold, not a dimension-dependent optimum and not a lower construction.
It supersedes the weaker intermediate n^(1/6)/log^(5/6) estimate retained in
the auxiliary derivation.

The accepted multiharmonic section supplies superlinearity at cost roughly
.53313 n sqrt(log n) with its OLD zero endpoint. That is not an established
sufficient energy for a new h* superlinear section; transporting the old
section to h* with preserved margin has not been proved. No claim closing
the sharp growing-energy threshold is made.

## 8. Endpoint comparison

| Endpoint | Cheap baseline | Holding | Bounded-energy superlinearity |
| --- | --- | --- | --- |
| Autonomous h* | Public zero burn-in + arbitrarily small exact landing pulse | Exactly zero input | Excluded asymptotically by (A) |
| Nearby common z | Finite landing may be cheap; no optimality theorem | Holding norm >=(1+m^2/4-a)||z-h*|| per step | Same upper applies |
| Distinct autonomous periodic orbit | Does not exist | Not applicable | Not a loophole |
| Public finite-time z_T=f^T(0) | EXACTLY zero-input baseline | Evolves under zero input rather than holding fixed | Same upper applies |

So h* is unique for stationary zero-cost holding. The time-specific z_T can
be even cheaper for a query at a chosen public time. Neither is claimed
universally optimal for every finite landing problem. Endpoint choice does
not evade the all-history bounded-energy upper in this family.

## 9. Numerical evidence and remaining uncertainty

43 checks passed across three new arithmetic records. Exact rational
constants and the explicit rotation-row identity agree. Scalar bounds agree
at 80/120 decimal precision. Those high-precision values are NUMERICAL checks;
the all-width theorem is the analytic proof, not a floating-point certificate.

Final bound (A), R_abs=1:

| n | delta_0 upper, numerical evaluation |
| --- | --- |
| 10^80 | 7.0724890055e-29 |
| 10^900 | 7.0725557640e-439 |

Small REFERENCE fixed-point diagnostics: n=200 has minimum coordinate
-0.11760216435; n=2000 has -0.00222571106. These negative minima are retained
and emphasize that the positive-coordinate theorem is only asserted at its
explicit large-width threshold. They do not decide robust memory at moderate
width. No new witness was optimized and no dimension was inferred from rank.

Strongest uncertainty: the sharp energy growth required to restore robust
credit, and all practical onset/conditioning questions, remain open. The new
proof itself still needs independent hostile review, especially the scalar
reference fixed-point construction, radial secant and all-query injection bound.

## 10. Project consequence, resources and provenance

Accepted growing-local Omega(n^(16/15)), bounded-local Omega(n^(19/18)) and
full-model Omega_c(n^2)--O_c(n^2 log n) claims are unchanged. Constant ABSOLUTE
energy defines a different class. In this family it cannot sustain the old
forced near-critical gate behavior at large width. Normalization matters:
this is fixed absolute error in the accepted units, not relative error.
The finite-error conclusion uses the fixed normalized head/loss family.
It does not cover unrestricted immediate losses or a relative-error contract.

Measured arithmetic CPU total .171875 seconds; peak RAM 36,921,344 bytes
(35.21 MiB); GPU/CUDA/model-server/training use zero. Import/administrative
time excluded from the arithmetic timers. No practical resource lower bound.

New work only in this Codex directory and an additive Codex resume entry.
Historical proofs, outputs, reviews, independent notebooks and GAS-0 preserved.
PROVENANCE.json records source hashes and the new-stage files.

**Single next step:** independent hostile review of THEOREM 1, Lemma 2 and
THEOREM 4; do not begin another construction, architecture or training stage.
