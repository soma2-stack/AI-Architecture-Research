# Robust credit dimension: a conditional width-scaling result

2026-10-01. New theoretical derivation for independent review. Accepted exact
accessibility, observability and antipodal dimension theorems are premises.
No new witness, numerical sweep, training, 9D section or architecture is used.

## 1. What is being quantified

For frozen theta=(R,W,b), h'=tanh(Rh+Wx+b), all P=2n^2+n parameters are
independently differentiated. Initially h0=S0=0. Define normalized sensitivities
Z=S D, where D has the SAME kind of frozen group-RMS multipliers used in the
accepted local work: w_R, w_W, w_b on the three parameter blocks. These
multipliers are constants during differentiation, not functions differentiated
through theta. Input-coordinate units remain the declared fixed input SD.
For a FULL normalized nP lower-dimensional claim all three multipliers must
be positive. A zero group RMS produces a degenerate seminorm and removes that
group from the observable quotient; one cannot borrow raw-coordinate dimension
for it. Upper bounds below remain valid with zero multipliers.

At fixed h, permitted future queries give gradient differences Delta Z^T c.
Include their common direct future parameter injection in actual answers.
Let C be the effective adjoint family, normalized so sup_C ||c||_2<=1, as in
the accepted fixed-head loss divided by beta=max(1,||R||_F). Thus

    D_C(Z1,Z2)=sup_C ||(Z1-Z2)^T c||_2 <= ||Z1-Z2||op.

The upper results also hold for immediate arbitrary unit adjoints, a stronger
query contract. Lower results must retain their actual specified query family.

A robust section here means a continuous history lift X(u), u in S^(r-1),
ending at one fixed h, with

    inf_u D_C(Z(X(u)), Z(X(-u))) >= 2 m.

If m>epsilon, the accepted antipodal argument forces a continuous encoder to
use at least r real coordinates. This is a continuous-state dimension claim,
not a bit count. Our collapse bound concerns all such sections, not just flat
SVD boxes or one certification algorithm.

The notation d_rob(n,epsilon) alone is insufficient: it must specify the model
or model class, history domain/budget, query family, normalization and whether
it is a worst-case sufficient-memory minimum or a certified section bound.
The latter is bounded by the former. Universal-over-models and existential
best-model lower bounds are different statements.

## 2. Additional assumptions for the new upper theorem

For every width impose constants independent of n:

    ||R||op <= a < 1, ||W||op <= w,
    |x_t,j| <= B, RMS(b) <= b_*.

The exact-theorem sufficient assumptions may hold simultaneously. No lower
bound on a, invertibility or mixing is needed for this upper theorem.
Since tanh outputs are bounded, ||h_t||_2<=sqrt(n). Group RMS satisfies

    w_R=||R||F/n <= a/sqrt(n),
    w_W=||W||F/n <= w/sqrt(n), w_b<=b_*.

Consequently define the WIDTH-INDEPENDENT injection bound

    C_* = sqrt(a^2 + w^2 B^2 + b_*^2).

These additional hypotheses are NOT entailed by exact accessibility. In
particular a=1, a_n approaching 1, expansive R and unbounded normalization
constants are outside the uniform-contraction conclusion.

## 3. Injection operator and exact expansion

Put G_t=diag(1-h_t^2), A_t=G_t R. For normalized parameter perturbation
phi=(phi_R,phi_W,phi_b), the injection operator is

    B_t phi = G_t (w_R phi_R h_(t-1) + w_W phi_W x_t + w_b phi_b).

Here matrix perturbations use Frobenius norm, jointly Euclidean with bias.
Because parameter blocks and their rows are disjoint,

    B_t B_t^T = G_t^2 [w_R^2 ||h_(t-1)||^2
                       + w_W^2 ||x_t||^2 + w_b^2].

This identity retains the actual coupled injections; it does not grant
independent control of parameter columns. It gives ||B_t||op<=C_* and
||A_t||op<=a. The exact normalized recurrence and its expansion are

    Z_t=A_t Z_(t-1)+B_t,
    Z_t=sum_(s=1)^t A_t ... A_(s+1) B_s.

Discard contributions with age t-s>=H. Uniformly in t and all allowed histories,

    ||Z_t-Z_t^[H]||op <= C_* sum_(j=H)^infinity a^j
                       = C_* a^H/(1-a) = e_H.

For H=0 the retained sum is empty. If H>=t the error is zero; the displayed
tail bound remains safe. No parameter updates or sensitivity staleness occur.

## 4. Online factored storage: no trajectory replay

For each retained injection retain

    Q_(t,s)=A_t ... A_(s+1) G_s, v_s=h_(s-1), x_s.

Its sensitivity action is exactly

    phi -> Q_(t,s) (w_R phi_R v_s + w_W phi_W x_s + w_b phi_b).

Storage per term is q_n=n^2+2n real scalars. Normalization/model parameters
are fixed public constants, not history-dependent memory. One may count the
new diagonal Q more tightly; we intentionally use the safe n^2 count.

On the next step multiply each retained Q by A_(t+1), append Q=G_(t+1) with
the new injection coefficients, and discard the oldest term if necessary.
This never reruns any past recurrent transition, reads an external history
tape, or reconstructs a discarded trajectory. x_s and v_s are counted
injection coefficients, although x_s numerically equals a recent input.
If a stronger model forbids retaining even these counted coefficients, this
upper theorem does not apply to that model; the accepted continuous-summary
model does not impose that restriction.

A VJP query uses

    g_R=sum_s w_R (Q_s^T c) v_s^T,
    g_W=sum_s w_W (Q_s^T c) x_s^T,
    g_b=sum_s w_b Q_s^T c.

The exact current hidden state costs n more coordinates when it is not
supplied. Future dynamics and their direct injection can be computed from h
when a query arrives. Query error is <=e_H because ||c||<=1. All buffers are
included. This is a storage theorem; multiplying H dense matrices is not
asserted to be fast, and decoder outputs contain P gradient coordinates.

For fixed endpoint horizon t, padding with zero terms makes this encoder a
continuous map of the past history into R^(H q_n), including discarded-history
dependence in the retained propagated factors. Deterministic queue positions
are public schedule data, not hidden continuous coordinates.

### Theorem 1: quadratic sufficient memory under uniform contraction

For 0<a<1 choose

    H=max(0, ceil(log(C_*/[epsilon(1-a)])/log(1/a))).

For C_*=0 use H=0. Then H q_n continuous coordinates suffice on a fixed-h
fiber, and n+H q_n suffice including exact h. At fixed positive epsilon and
uniform a,C_*, this is O(n^2), independent of history length. It does NOT
prove an Omega(n^2) lower bound. At a=0, one latest injection suffices; the
logarithmic formula is replaced by this direct observation.

## 5. Exponential margin ceiling for cubic sections

Let an r-dimensional antipodal section as in section 1 exist. Compose its
continuous history lift with the H-term factor encoder. If H q_n<r,
Borsuk-Ulam forces an antipodal pair to have identical encoded factors.
At fixed h, identical factors give identical approximate answers to every
query. Triangle inequality and the uniform tail bound imply

    D_C(Z(u),Z(-u)) <= 2 e_H.

Therefore its guaranteed half-margin m MUST satisfy m<=e_H. Set

    H=ceil(r/q_n)-1 >= 0.

Then H q_n<r, proving

    m <= [C_*/(1-a)] a^(ceil(r/(n^2+2n))-1).                 (1)

For r=nP=2n^3+n^2,

    r/q_n = (2n^2+n)/(n+2) = 2n-3+6/(n+2).

Thus full cubic sections have m <= constant * a^(2n+O(1)) under the uniform
assumptions. More generally r>=c n^3 forces m=O(a^(c n+O(1))). This is an
arbitrary-width exponential UPPER bound on a robust antipodal margin, not an
inference from width-2/3/4 conditioning or a numerical upper bound.

For r=Theta(n^2), (1) has only a constant exponent: it does not force margin
decay. It also does not establish that any quadratic robust section exists.

With width-dependent a_n,C_n, replace a,C_* in (1). If a_n=1-c/n, then
a_n^(2n) approaches exp(-2c) and 1/(1-a_n) grows like n: this obstruction no
longer proves collapse. Exact accessibility's explicit unscaled family has
||R||op=1, so it is NOT covered by the uniform a<1 assumption. Saturation may
contract particular trajectories but no uniform contraction follows merely
from its existence. Dense interaction by itself is not the controlling
assumption in (1).

## 6. Why no positive universal lower bound follows from the accepted hypotheses

This is a normalized all-width counterfamily, not a new experiment. Let

    A_n=I-11^T/(n+1), R_n=delta A_n, W_n=I, b_n=1,
    0<epsilon<=1, delta=epsilon/[4(B+2)].

For n>=2, ||A_n||op=1 and A_n^-1=I+11^T. All inverse entries are nonzero;
R,W are invertible and all parameters remain independently differentiated.
Exact arbitrary-width accessibility therefore applies on the bounded open
input cube, for every n. The positive RMS scales are

    w_R<=delta/sqrt(n), w_W=1/sqrt(n), w_b=1.

Then C_*<=sqrt(delta^2+B^2+1)<=B+2 and ||Z_t||op<=C_*/(1-delta).
For the ACCEPTED delayed fixed-head queries, ||c||<=delta/beta<=delta.
Consequently

    ||Z_t^T c|| <= delta C_*/(1-delta) < epsilon.

A decoder storing exact h but ZERO sensitivity coordinates can answer with
only the common future-injection gradient, uniformly over all histories.
For multiple future steps the adjoint contracts further. Thus even a positive
universal sensitivity-memory lower bound at fixed epsilon is impossible from
the qualitative theorem assumptions with this normalized delayed query family.

This does not cover immediate arbitrary unit losses; their adjoints do not
contain the delta factor. It does not disprove an existential best-family
quadratic or cubic lower bound under quantitative constraints. It also does
not change any archived endpoint, epsilon, or certificate.

## 7. Strongest established lower and upper bounds, with quantifiers

GENERAL DENSE, FIXED EPSILON: exact storage nP=2n^3+n^2 (+n for h) gives
O(n^3) sufficient continuous state. No width-uniform Omega(n^2) lower bound is
established here. The existing independent n=4 k>=8 result is local and does
not supply an arbitrary-width dense lower bound. Universal-over-allowed-models
lower bounds fail by section 6.

GENERAL DENSE, WIDTH-DEPENDENT EPSILON: accepted accessibility, positive
normalization multipliers and full-span queries give a positive local radius
and query margin at each fixed n.
Hence there exists epsilon_n>0 for each n such that k>=nP when epsilon<epsilon_n.
Together with exact storage this gives Theta(n^3) continuous coordinates in
that width-dependent-error regime. No uniform positive lower bound for
epsilon_n is known. The archived tiny isotropic radii are sufficient constants,
not upper bounds on the best possible margins.

UNIFORMLY CONTRACTIVE, NORMALIZED, BOUNDED CLASS: new sufficient state
O(n^2 log(C_*/[epsilon(1-a)])); at fixed epsilon this is O(n^2). Cubic
antipodal margins decay exponentially by (1). A matching quadratic lower
bound remains unproved. With RAW parameter coordinates the injection bound
instead scales O(sqrt(n)), yielding O(n^2 log(n/epsilon)) by this same method;
this unit change must not be hidden.

INDEPENDENT CONTROL: P_ind=n^2+2n supported exact sensitivities suffice, plus
n hidden coordinates. Full rank inside its supported space or eight robust
coordinates at n=4 does not establish uniform robust Omega(P_ind).

## 8. The missing theorem that would settle the next gap

Quadratic target: construct an explicit admissible dense family, continuous
fixed-h history sections X_n:S^(r_n-1)->histories with r_n>=c n^2, and prove

    inf_u D_C(Z(X_n(u)), Z(X_n(-u))) >= 2 m0,
    m0>1e-3 independent of n,

under the SAME RMS units, normalized query family, bounded input domain and
specified horizon budget. If the family is uniformly contractive, Theorem 1
would make this a matching Theta(n^2) result at that tolerance. It requires
joint separation for all antipodes, not individually strong axes, an exact
rank witness, or more independent blocks without controlling query dilution.

Cubic alternative: construct such a section with r_n>=c n^3 in a nonuniformly
contractive/near-isometric family, while proving uniform forward conditioning,
finite fixed-h inclusion and actual query separation. This would establish
Theta(n^3) for that family. Theorem 1 shows it cannot be accomplished inside
the uniform-contraction class. Failure to construct it is not a general
cubic impossibility theorem.

The single recommended next step is an independent hostile mathematical
review of the factored-tail upper theorem and its antipodal margin corollary,
especially the counted no-replay state and normalized injection bound, before
trying to prove either matching construction. No new section search is needed
for that review.

## 9. Scope and limitations

These new proofs are author-derived, not independently reviewed or formally
machine-verified. Only accepted antipodal topology is invoked. No learning,
bit/VRAM lower bound, runtime separation or architectural novelty follows.
An O(n^2) sufficient state is not an Omega(n^2) necessary state. Local patches,
chosen sections and global memory minima must remain distinguished. No
empirical width extrapolation or claim that all cubic directions collapse
in all dense networks is made.
