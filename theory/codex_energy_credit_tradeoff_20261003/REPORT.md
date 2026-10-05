# Energy–robust-credit tradeoff: results of the new theory stage

2026-10-03. **Status:** new proofs derived and internally checked; independent
hostile review is still required. The five owner-accepted results are premises.
No historical proof was edited or reopened. This is theory for the existing
frozen dense tanh family, with epsilon=0.001 and the original legal queries.

## 1. Updated energy-memory phase diagram

The [complete phase diagram](PHASE_DIAGRAM.md) includes both the accepted-only
starting chart and the chart after this stage. Its new lower bounds are:

| Full absolute history norm | Fixed-feature robust credit lower |
|---|---|
| O(1) | No positive dimension asymptotically, by the accepted upper |
| C n^(1/4) | No positive lower established; small C is impossible |
| n^(1/3) | No positive lower established |
| O(n^(1/2)) | One direction |
| O(n^(2/3)) | Omega(n^(2/3)) |
| O(n^(3/4)) | Omega(n) |
| O(n^(7/8)(log n)^(5/4)) | Omega(n log n), hence superlinear |
| O(n) | Omega(n^(16/15)) |
| O(n sqrt(log n)) | Accepted Omega(n^(16/15)); the new cheaper section also fits |

Every positive lower is a continuous whole-ball section with a common endpoint
and a legal-query antipodal margin. Energy includes preparation, source drive,
bias cancellation, hold, pulse, reset, and dense-model compensation. The lower
at a stated O scale requires its stated sufficient constant.

The localized construction uses one public autonomous source feature
H=sigma*1_l, sigma=tanh(lambda*sigma+.05). The harmonic construction retains
the old H=.4*1_l. Neither multiplies independent source columns. Forward-state
storage, full-model bounds, and local-radius statements stay separate.

## 2. Best one-channel threshold found

**A rigorous sufficient norm is O(sqrt(n)); necessity below this remains open.**

Choose one off-cycle PAIR and its invariant parameter channel
psi=(e_i-e_j)/sqrt(2). After cheap, fully counted public preparation, hold both
coordinates at sqrt(1/(20n)) for 4n steps while controlling the public bath.
Return to the same autonomous reference endpoint. Compare this with the
autonomous hold and interpolate continuously between them.

On psi the exact reference recurrence is M_next=g(aM+1). The near-critical
hold gives M>.93n, while the autonomous hold has M<=1601 for n>=10^6. A fixed
one-step future with preactivations 1/4 and 3/4 on the pair gives antipodal
half-margin >.003 after the dense correction, exceeding epsilon=.001.
The full history norm is conservatively <=2sqrt(n) for sufficiently large n.

This is ONE robust direction implemented with two physical coordinates.
It does not prove a result for every isolated-row schedule or infer dimension
from a collection of individually visible directions.

## 3. Is n^(1/4) sharp or loose?

**Unresolved globally.** No witness at C n^(1/4), nor at n^(1/3), was found.
The scalar hold explains why this particular mechanism does not reach those
scales: fixed visible margin needs T=Theta(n), and a near-zero hold cancels
a nonzero constant autonomous forcing on each controlled coordinate.

For c=sqrt(z/n), T=kappa*n, the leading cost and visible margin are

    R_abs^2 = 2 B_mu^2 kappa*n + O(1)+o(n),
    B_mu -> .05-tanh(.05)>0,

    m(kappa,z) = [sigma_infty*s_gate*(1-mu_infty^2)/2]
                 *[1-exp(-(1+z)kappa)]/(1+z).

The bracket decreases in z. Holding at zero is therefore best at leading
order within this constant-hold calculation; a shallower critical excursion
does not save its leading energy. T=o(n) gives vanishing projected signal;
T>>n pays more after saturation. Fixed-length ramps and reset cost O(1)
squared energy and do not change the exponent.

Crucially, the legal adjoint on the off-cycle channel is O(1/sqrt(n)) before
the public loss factor. Using a freely chosen unit adjoint would overstate
visibility. The resulting channel is visible at order Delta M/n. This is
a restriction-specific matching exponent, not a global lower on energy.
Optimal arbitrary ramp/hold/reset controls and a single isolated physical row
with a freely evolving bath remain open.

There is also a rigorous necessity result for the literal isolated-row
mechanism in a stationary bath. All other gates have a fixed gap; the
off-cycle row/column coupling to that bath is O(1/sqrt(n)). A two-block
backward-adjoint bound makes its ENTIRE selected-gradient signal O(T/n)
for short holds. Thus fixed epsilon needs T=Omega(n). The accepted state-energy
inequality then charges Omega(T) squared energy for holding that coordinate
near zero, giving R_abs=Omega(sqrt(n)). This excludes n^(1/4) for this
restricted mechanism, and matches the pair witness's one-channel exponent.
It does not exclude a different mechanism at the accepted n^(1/4) boundary.

## 4. Best rigorous joint localized construction

For 4*10^6<=s<=10^(-12)n, use s off-cycle pairs. Clamp them to zero, allow
the bath to evolve under its public autonomous reference dynamics, and use
one bounded-spread pulse to encode a D=floor(s/1000)-dimensional ball.
The pulse has states (+sqrt(.11+.05v_j),-sqrt(.11+.05v_j)), followed by a
common reset to zero on the pairs. Here v(y)=tanh(Ay) is odd and has
||v(y)||>=sqrt(s)/16 on every unit boundary point.

The bath is independent of y because every pulse pair has zero sum. Its
clamp input stays below .06 under the conservative s/n allowance. Pulse and
reset inputs stay strictly inside the past cube. A fixed legal query sees
every boundary antipode with half-margin >.01. The selected projections
have exactly zero reference cross-talk; actual dense leakage costs <4e-9.

| Quantity | Proven localized bound |
|---|---|
| Hold duration | T=ceil(1000n/sqrt(s))<=n |
| Squared full energy E(n,s) | O(n sqrt(s)) |
| Absolute norm | <=100 sqrt(n) s^(1/4) |
| Robust dimension | >=floor(s/1000) |
| Visible half-margin | >.01 |
| Dense cross-talk error | <4e-9 |
| Endpoint pulse/reset squared cost | O(s) |

Hence

    d_F >= Omega(min{n,R_abs^4/n^2}),

in the construction range, with the explicit constants/threshold in PROOF.md
section 6. This proves linear dimension at O(n^(3/4)) energy. It supplies
no superlinear dimension by itself.

## 5. Lowest energy found for omega(n)

**O(n^(7/8)(log n)^(5/4)), improving the previous n sqrt(log n) cost.**

The improvement is a shorter version of the existing harmonic mechanism.
Take exactly T temporal steps, temporal frequencies 2pi*j/T, and actual
spatial frequencies obtained by rounding d*j/T to the cycle's integer modes.
Complete temporal cosine periods cancel the startup term in the EXACT finite
source resolvent. A weighted cosine Gram estimate, with the rounding error
charged, treats all harmonics together.

The complete actual legal-query half-margin ledger is

    M >= 10^(-18) delta*T^2/(n^(3/2)*F^5)
           -100 delta*T^2/n^2
           -delta^3*T^4/n^(7/2)-4e-9.                 (P)

The terms are respectively the physical query-visible signal, node/Householder
loss, all odd nonlinear chronological orders, and actual dense/query transfer.
Even orders cancel exactly. Mixed harmonics are included. No raw-rank or
arbitrary-adjoint argument appears.

Choose delta=10^(-10), F=floor(log n), and
T=ceil(10^15*n^(3/4)*F^(5/2)). Then the positive term is at least 100, both
variable losses vanish asymptotically, and the full absolute norm is
<=2sqrt(n(T+2)). The joint dimension is qF>=n*floor(log n)/10^7 eventually.
The constants are deliberately conservative; this is not a practical-onset
claim or a finite-width numerical construction.

A simpler power corollary is

    R_abs=O(n^(9/10)), d_F=Omega(n^(101/100)).

There is also a complete-cycle corollary: T=d, exact temporal/spatial frequency
agreement, F=floor(n^(1/15)/10^4), delta=10^(-10)/F^(5/2), give

    R_abs=O(n), d_F>=n^(16/15)/(2*10^11).

This preserves the accepted dimension exponent at a smaller absolute cost.
It is a separate new theorem, leaving the old accepted history and its
original energy record intact. The archived polynomial approximation contract
is not silently asserted; these claims concern the actual gradient metric.

## 6. Strongest dimension-dependent upper obtained

The accepted energy-to-bad-step count gives B_R=O(1+R_abs^2). Retain the
last L_n+B_R+J steps, where J=O(log(n/epsilon)) forces all older actual
sensitivity below epsilon under every legal query. Store the window's actual
states and inputs as counted private coordinates. No discarded history is read.

This gives the new, conservative upper

    d_all <= min{C_epsilon*n[1+R_abs^2+log(n/epsilon)],
                 C'_epsilon*n^2*log(n/epsilon)}.

For one public source feature the accepted reference store also gives

    d_F <= min{r^2,C_epsilon*n[1+R_abs^2+log(n/epsilon)]},
    r=floor(n/2)-1.

The accepted zero-credit decoder supersedes this estimate whenever its
error certificate is <=epsilon, especially R_abs=o(n^(1/4)). The upper
does not exclude superlinearity at the intermediate positive power scales.
The all-gradient statement is restricted to the SAME frozen energy-promised
family; the accepted broader full-model n^2 versus n^2 log n gap is unchanged.

## 7. Explicit d_rob versus R_abs tradeoffs and efficiency

There is no matching law. The rigorous construction bounds are:

* One direction at R_abs<=2sqrt(n), sufficiently large n.
* Localized D>=floor(s/1000) whenever
  4*10^6<=s<=min{10^(-12)n,(R_abs/(100sqrt(n)))^4}.
* Short packets: for F->infinity, F=o(n^(1/20)),
  D>=c*nF at R_abs<=C*n^(7/8)*F^(5/4). Equivalently, choosing an
  admissible integer F, D>=c*n[R_abs/(C*n^(7/8))]^(4/5).
* Complete-cycle D>=n^(16/15)/(2*10^11) at O(n) norm.

These coexist with the preceding upper and the accepted zero-credit regime.
The general packet inequality (P), admission conditions, and full energy bound
provide a parameterized tradeoff beyond the stated corollaries.

A natural achieved efficiency is I=D/R_abs^2, using a JOINT section's
dimension and its full squared input norm. The localized family achieves
I=Omega(sqrt(s)/n), reaching Omega(n^(-1/2)) at s=Theta(n). The short
packet family achieves I=Omega(n^(-3/4)*F^(-3/2)). These are achieved
ratios, not upper limits, bits, joules, physical VRAM, or runtime measures.

## 8. Failed constructions and unresolved variants

* The n^(1/4) constant off-cycle hold gives too little projected scalar
  accumulation. This kills that witness, not the global possibility.
* A forcibly stationary bath while clamping s rows requires an exceptional
  row input of order s/sqrt(n), violating the cube for large s. Letting the
  unclamped bath evolve resolves this obstruction in the joint proof.
* Counting separately visible axes does not prove robust dimension. Both
  new many-channel proofs use whole balls and every boundary antipode.
* Keeping the old low spatial frequencies in a short packet loses the
  temporal Gram bound. Rounded widely separated spatial modes remove the loss.
* Autonomous relaxation gaps damp the old carrier. Their zero input cost
  does not make separated packet margins independently addable.
* Subtracted baselines or free source/bias drive would falsify the energy
  comparison. The harmonic construction explicitly pays O(nT) squared energy.
* T=o(n^(3/4)) with bounded delta cannot be certified by this weak-gate
  packet's main bound, even for F=1. This is a proof limitation, not an upper
  on arbitrary stronger pulses or moving localized windows.

Sparse near-critical windows, duty cycles, moving localized windows, multiscale
or phase-coded packet trains remain open beyond the two constructions proved
here. They were not converted into unsupported lower bounds.

## 9. Numerical evidence, separated from theorems

[CHECKS.md](CHECKS.md) and [NUMERICAL_EVIDENCE.json](NUMERICAL_EVIDENCE.json)
record small CPU diagnostics. They check finite packet identities, reference
one/multiple-pair schedules, delay losses, and scalar constant-hold behavior.
None supplies an asymptotic dimension theorem or a sphere-wide sampled margin.

The asymptotic-bath scalar diagnostic gives mu_infty approximately .049958375,
the holding drive .0000416250, and for its particular one-step query an
epsilon-level leading hold length approximately .26621*n. Its leading norm
coefficient is approximately .000030373*sqrt(n). These are numerical
constant-optimization findings for that restricted schedule. They do not
prove a global optimum or finite-width dense witness at those constants.

Some finite reference samples can have small absolute energy and a visible
single antipode. The accepted upper is asymptotic with conservative constants;
such samples do not contradict it. Numerical zero-input relaxation visibly
reduces their margin. Formal odd coefficients were checked separately from
floating subtraction, whose roundoff floor is too large to certify a tiny tail.

## 10. Exact remaining exponent gap

| Question | Necessary exponent from accepted upper | New sufficient exponent | Open interval |
|---|---|---|---|
| First fixed-epsilon direction | >=1/4 | 1/2 | [1/4,1/2] |
| omega(n) credit dimension | >=1/4 | 7/8, with polylog factor | [1/4,7/8] |

At R=n^(3/4), the joint lower is linear; the upper does not prove a linear
ceiling. There is no superlinear impossibility theorem at 1/2, 2/3, or 3/4.
There is no new full-model or constant-local-radius matching law.

## 11. Strongest theorem justified by this stage

For the frozen dense family, unchanged epsilon=0.001 and legal future-query
contract, all sufficiently large widths admit ONE continuous same-endpoint
fixed-feature history section with full absolute norm
O(n^(7/8)(log n)^(5/4)) and dimension Omega(n log n). Every unit-boundary
antipode has actual permitted-query half-margin greater than epsilon.

The construction pays every past input and all dense, Householder, startup,
cross-harmonic, reset, and nonlinear errors. This is an author-derived theorem
awaiting independent hostile review. It is not an accepted project checkpoint
until that review is complete.

## 12. Recommended next attack

First hostile-review the NEW short-packet finite kernel/rounding/error ledger
and the clamped-bath joint section. The accepted energy upper needs no rereview.

Then prove a query-visible localized energy upper. The present bad-step
certificate charges every bad time with a global operator norm. The off-cycle
visibility calculation loses an additional sqrt(n), while cycle transport
requires shared space/time support. A bound that charges those supports under
the actual legal query metric could separate one-channel and superlinear
thresholds, possibly excluding superlinearity below a stronger exponent.

In parallel as a mathematical alternative, seek a moving sparse weak-gate
packet that retains the physical L1 signal while paying fewer than n driven
coordinates per step. Its startup, bath coupling, full source/bias cost and
joint antipodal margin must be proved together. A rigorous exponent below
7/8, or a superlinear impossibility above 1/4, would narrow the remaining gap.
