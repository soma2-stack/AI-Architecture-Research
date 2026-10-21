# A quadratic robust section at contraction gap c/n

2026-10-01. New proof for independent hostile review. The accepted bounded-spread
lemma and continuous-encoder antipodal theorem are premises. The constant-gap
regime is not revisited. No architecture, learning or numerical search is used.

## 1. Claim and unchanged contract

For every fixed c>0 and all sufficiently large n, a specified dense tanh family
with ||R||op=1-c/n admits a continuous, EXACT fixed-h history section of dimension

    r_n=floor(d_n l_n/1000)=Omega_c(n^2),

whose boundary antipodal gradient-query half-separation is at least

    1/500 = 0.002 > epsilon=0.001.

Here d_n denotes the orbit length defined below, NOT the earlier exact augmented
endpoint dimension. The result gives an existential worst-case quadratic lower
under the current normalized late-query contract. It is not universal per model.
The complete deterministic specifications are finite; the accepted sign-matrix
selection is exhaustive, not efficiently executable. For positive rational c
the construction is computably explicit; for arbitrary real c the same formulas
and existence argument apply without asserting computation of a noncomputable c.

The recurrence remains

    h_t=tanh(R h_(t-1)+W x_t+b), h0=S0=0,
    S_t=D_theta h_t, theta=(R,W,b), P=2n^2+n.

ALL entries are differentiated independently. Frozen group-RMS normalization
uses w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b); these multipliers are held constant
when differentiating. Inputs stay in (-1/2,1/2)^n. The same input SD merely labels
history coordinates; the gradient error is not rescaled.

The permitted future loss is the accepted scalar head q=1/sqrt(n)*1 divided by
the frozen beta=max(1,||R||F). Its one-step effective adjoint is

    xi(v)=R^T G_f q/beta.

We use only the permitted future input v=(9/20)*1 from the endpoint h=0, giving
preactivation (1/2)*1 when W=I,b=1/20*1, and G_f=kappa I with
kappa=sech^2(1/2)>3/4. No arbitrary immediate adjoint is introduced.
Direct future parameter injections are included in gradient answers and cancel
between histories with the SAME endpoint h=0. In the R block that direct
injection is itself zero at h=0; W/b direct terms need not be zero.

## 2. Width, orbit and repetition constants

Set

    a=1-c/n, delta=1/(100n),
    k=floor(n/2), l=n-k,
    L=max(1,ceil(c)), d=min(k, floor(n/(4cL))).

Take

    n >= n0(c)=ceil(max(64, 8cL, 200 sqrt(cL), 2c)).

Then a>=1/2, d>=1, N=d l>=1000 and

    J=Ld <= n/(4c), a^J >= 1-Jc/n >= 3/4.               (1)

The last step is Bernoulli's inequality for an INTEGER exponent J. These
choices compensate for arbitrary fixed c, not only c<=1: repeat each orbit
L times while shortening its length d. If c<1, L=1 and J=d<=k; if c>=1,
J<=n/(4c)<=n/4. Thus the history horizon T=J+1 is <=n for n>=64.

The following bounds will be used:

    k/n >= 2/5, l/n >= 1/2.

If d=k, L sqrt(d/n)>=3/5. Otherwise floor rounding and n>=8cL imply
d>=n/(8cL), hence

    L sqrt(d/n)>=sqrt(L/(8c))>=7/20.                    (2)

These are conservative uniform constants, since L>=c and 1/sqrt(8)>7/20.

## 3. Slow memory rotation and fast source coordinates

This is a proof parameter family of the SAME standard tanh recurrence, not a
proposed new architecture. Split coordinates into k memory coordinates and l
source coordinates. Write q_m=1/sqrt(n)*1_k and e=1/sqrt(k)*1_k.

Let U be the Householder orthogonal matrix mapping e1 to e:

    U=I-2ww^T/(w^T w), w=e1-e.

It is defined for k>=2. Let P_d be the cyclic shift on d coordinates and put

    O=U (P_d direct_sum I_(k-d)) U^T.

O is orthogonal. The d vectors

    (O^T)^j q_m, j=1,...,d,

are mutually orthogonal, each of norm sqrt(k/n); also (O^T)^d q_m=q_m.
This is verified by conjugating to e1, whose cyclic orbit consists of the d
different coordinate vectors. q remains the FULL uniform allowed head; the
matrix O, not the loss, creates the independent temporal directions.

First analyze the block reference

    R0=diag(a O, delta I_l), W=I, b=1/20*1.

It has k slow singular modes of size a, not just one. It is invertible but
not yet dense. Section 7 makes it dense with a quantified perturbation while
retaining EXACT operator norm a and the final robust margin.

## 4. Joint bounded history section and exact fixed-h compensation

Use the accepted bounded-spread lemma at N=d l and r=floor(N/1000): its specified
sign matrix M has

    ||tanh(Mu)||_2 >= sqrt(N)/16 for every ||u||_2=1.

For u in the closed r-dimensional unit ball, reshape

    vec(H(u))=(2/5) tanh(Mu)

into a d by l source matrix. All entries have absolute value <2/5,
H(-u)=-H(u), and on the boundary

    ||H(u)||F >= sqrt(d l)/40.                          (3)

For t=1,...,J=Ld, prescribe the ACTUAL hidden trajectory

    h_t(u)=(0_k, H_s(u)), s=1+((t-1) mod d),
    h0=0, h_T=0 at T=J+1.

For a fixed model R, define the realized inputs

    x_t(R,u)=atanh(h_t(u))-R h_(t-1)(u)-b.              (4)

Then the same standard recurrence has that trajectory exactly, simultaneously
over the whole ball, including the exact endpoint h_T=0. This accounts for all
mixed nonlinear interactions in the fixed-h lift; no independent-axis
compensation or infinitesimal tangent assertion substitutes for it.

At R0, the memory inputs equal -b. The source inputs satisfy

    |x_t,j| <= atanh(2/5)+delta*(2/5)+1/20 < 0.477.

For example, the series bound
atanh(2/5)<=2/5+(2/5)^3/3+(2/5)^5/[5(1-(2/5)^2)]<17/40
certifies the input-domain slack. The final zero hidden state obeys the same
bound. The dense perturbation's additional input change is bounded in section 7.

CRITICAL: sensitivity differentiation holds EACH REALIZED INPUT fixed. One
does NOT differentiate (4) through R or W. Doing so would compute a controlled
total derivative, not the accepted frozen-input parameter sensitivity.

The chart is continuous and injective on the ball: the accepted spread lemma
implies M has full column rank, tanh is injective, and all source rows occur in
the trajectory. Thus it defines genuine independent section coordinates.

## 5. Actual coupled R-sensitivity injection and query formula

At the block reference, memory states are zero and their gates are exactly I
on EVERY history in this section. The source gates need not be near one; they
do not multiply propagation inside the memory block. Let K denote an arbitrary
k by l perturbation of the R memory-row/source-column block. Its injection at
transition t+1 is the actual coupled K H_s, not selectable sensitivity columns.

For the permitted one-step future query,

    xi_m = kappa a O^T q_m/beta.

For n>=n0, ||R0||F>1, so beta=||R0||F and

    w_R/beta=(||R0||F/n)/||R0||F=1/n.                  (5)

Thus the normalized R-block gradient is

    g_ms(H)=(kappa/n) sum_(t=1)^J
                a^(J+1-t) (O^T)^(J+1-t) q_m H_s^T.

All powers follow from exact RTRL or the equivalent backward adjoint recursion:
there are J-t memory transitions after the injection at t+1 and one extra R
from the allowed future query. No gradient-method approximation is used.

Group the L repeats of row s and set

    B_L=sum_(j=0)^(L-1) a^(j d).

Then

    g_ms(H)=(kappa/n) B_L sum_(s=1)^d
                   a^(d+1-s) (O^T)^(d+1-s) q_m H_s^T. (6)

The d temporal vectors in (6) are orthogonal. Therefore, for antipodes,

    (1/2)||g_ms(H)-g_ms(-H)||F
       >= (kappa/n) sqrt(k/n) a^d B_L ||H||F,
    a^d B_L >= L a^(Ld) >= 3L/4.                      (7)

The Euclidean norm of the FULL gradient dominates the norm of this selected
parameter block. Residual R/W/b coordinates cannot cancel this bound.

## 6. Uniform margin and quadratic section dimension

Combining (2), (3), (7), kappa>3/4 and the width ratios gives

    m_ref >= (9/16)(L/40) sqrt(k/n) sqrt(d/n) sqrt(l/n).

Use sqrt(k/n)>=3/5 and sqrt(l/n)>=7/10. In the uncapped case (2) gives

    m_ref >= (9/16)(1/40)(3/5)(7/20)(7/10)
           =1323/640000=0.0020671875.                  (8)

If d=k, the same calculation with L sqrt(d/n)>=3/5 gives the stronger
567/160000=0.00354375. The weaker value in (8) is uniform over BOTH cases and
over every fixed c>0 at all n>=n0(c). It exceeds epsilon without changing units.

For the dimension, if d=k then N=d l>=n^2/5. Otherwise N>=n^2/(16cL).
Since N>=1000, floor(N/1000)>=N/2000. Consequently

    r >= min(1/10000, 1/(32000 cL)) n^2 = Omega_c(n^2). (9)

The constant depends on the FIXED c; this is not a joint n,c scaling claim.
The accepted spread lemma is essential: a naive linear sphere inside the
per-entry bounded history cube would lose the required Frobenius radius.

## 7. Fully dense perturbation with explicit error control

The block calculation alone is not the final family. This section produces
nonzero entries of R and R^-1 without assuming density by naming it.

Choose integer power vectors u_*=(1,t,...,t^(n-1)) and v_* of the same form
so all entries of R0^-1 u_* and v_*^T R0^-1 are nonzero. Each forbidden entry
is a nonzero polynomial of degree <=n-1. Selecting the first admissible
integer from {1,...,n(n-1)+1} separately for each vector succeeds by the finite
root bound. The vectors themselves have all positive nonzero entries.

Put C=u_* v_*^T/(||u_*|| ||v_*||), so ||C||op=1 and all entries are nonzero.
Try the fixed finite list

    eta_j=1/(10^8 n^2) * 2^(-j), j=0,...,2n^2.

Select the first j for which B=R0+eta_j C and B^-1 have every entry nonzero.
B is invertible throughout this list: ||R0^-1||op=1/delta and
eta_j/delta<=1/(10^6 n)<1.

Why does the list succeed? A base-zero entry of B becomes nonzero immediately;
a base-nonzero entry has at most one exceptional eta. Sherman-Morrison gives

    B^-1=R0^-1 - eta (R0^-1 u_*)(v_*^T R0^-1)
                  /[||u_*|| ||v_*||+eta v_*^T R0^-1 u_*].

Every base-zero inverse entry becomes nonzero, because both factors were made
nonzero. Every base-nonzero inverse entry has at most one root after clearing
the nonvanishing denominator. There are at most 2n^2 bad values in total, and
the list has 2n^2+1 distinct candidates. The selection is finite and explicit.

Now define the FINAL recurrence matrix

    R=(a/||B||op) B.

It is dense and invertible, all inverse entries are nonzero, and ||R||op=a
EXACTLY. W=I, b=1/20*1 remain unchanged. The rescaling formula defines base
values ONLY; all entries of the final R are still independently differentiated.
There is no restriction of perturbations to this parameter-family formula.

Let e_R=||R-R0||op. Since eta<a/2, the spectral triangle inequalities give

    e_R <= 2a eta/(a-eta) <=4 eta <=4/(10^8 n^2).        (10)

Use (4) with this final R. The entire prescribed hidden trajectory and all its
gates are identical to the reference. Its extra coordinatewise input variation
is <=e_R*(2/5)sqrt(l)<0.001, so EVERY past input still lies in the same cube.
The final h_T=0 section and the future input v=(9/20)*1 remain exact.

We must also transfer the normalized gradient, not merely forward states.
For both R and R0, beta=||R||F>1, because ||R0||F>=a sqrt(k)>2 and the perturbation
has Frobenius norm <=sqrt(n)e_R. Thus (5) holds separately for both models.
For any prescribed history, write A_t(R)=G_t R. The FULL normalized R-gradient
for the selected permitted query equals

    g_R(R;u)=(kappa/n) sum_(s=1)^T
        [G_s A_(s+1)(R)^T ... A_T(R)^T R^T q] h_(s-1)^T. (11)

All G_s and h_s are identical across the two models, and all matrix factors
have operator norm <=1. A product of T-s+1 R-dependent factors changes by at
most (T-s+1)e_R, by telescoping. Consequently

    ||g_R(R;u)-g_R(R0;u)||F
      <= (kappa/n) e_R (2/5)sqrt(l) T(T+1)/2
      <= (2/5)n^(3/2)e_R
      <= (8/(5*10^8))/sqrt(n) < 10^-6.                 (12)

This is uniform over the WHOLE section, including all mixed source-coordinate
movements. No unbounded hidden sensitivity has been omitted: (11) is the exact
finite-history adjoint expression for every independently differentiated R
entry. Its source gates can be nonlinear but are explicitly retained.

Project onto the selected memory/source R block, apply the triangle inequality
to the two antipodes, and divide by two. The final dense family's half-margin
is at least m_ref-10^-6, hence

    m_dense > 1/500=0.002 > epsilon=0.001.              (13)

This finishes the genuinely dense family, rather than treating the block
reference as the answer. It does NOT impose a lower bound on every mixing
coefficient: many added couplings are small. No such assumption belongs to
the accepted dense/query contract. Per-entry relative parameter units, instead
of the accepted GROUP-RMS units, would be a different problem and could suppress
these cross-parameter directions.

## 8. Continuous-memory lower theorem

For the final dense family, the entire r-dimensional ball has the same exact
endpoint h_T=0 and a continuous realized-history lift. Suppose its encoder
stores k_mem<r continuous real coordinates, and later answers every permitted
query with absolute normalized gradient error <=epsilon.

Borsuk-Ulam on the boundary sphere makes some antipodes share memory. Their
decoded answers for the SINGLE permitted query above agree. Triangle inequality
then gives exact gradient distance <=2epsilon, contradicting (13).

Therefore

    k_mem>=r=Omega_c(n^2).

This is a joint finite-error continuous dimension statement, not merely
independent axes with large tangent derivatives. It is not a bit count, or a
claim that all pairs of arbitrarily close section points have a fixed minimum
distance. It imposes no continuity requirement on the decoder, only on the
history encoder. With h supplied there is no extra hidden-state count.

## 9. Bottlenecks resolved by the construction

- **Slow-mode multiplicity:** k=Theta(n) memory singular modes are near-critical;
  d=Theta_c(n) independent directions of the head's backward orbit are used.
  One slow mode would supply only one temporal row of the cross-gradient.
- **Query dilution:** beta is Theta(sqrt(n)), so c has small norm. But the
  R-group RMS weight is beta/n, giving the EXACT cancellation (5). The remaining
  1/n factor is offset by ||H||F=Theta_c(n), jointly over every antipode.
  Neither beta nor epsilon is dropped, and the allowed q is not redesigned.
- **Tanh gates:** source coordinates have moderate nonlinear activations while
  memory coordinates stay at zero, with gates exactly one. Source curvature
  does not directly contract the reference memory orbit. Dense leakage is
  included by (11)--(12), not declared harmless without a bound.
- **Coupled injection:** the real perturbation K acts on the actual H_s vector.
  Orthogonal temporal adjoints turn that injection into a full matrix of
  distinguishable gradient coordinates. Parameter columns are never controls.
- **Fixed h:** all histories are compensated simultaneously by (4), with
  realized inputs held fixed during gradient differentiation.

The construction uses standard recurrence and standard control-theoretic
parameter choices. It is evidence for the stated credit-memory lower bound,
not a new architecture or a practical advantage of exact gradients.

## 10. Upper bound, strongest obstruction and logarithmic gap

The owner-accepted upper remains, at gamma=c/n and fixed c,epsilon,

    k_eps<=O_c(n^2 log n)

for all horizons, bounded input/W/bias constants, the same units and arbitrary
query decoding work. The exact nP cap is weaker here asymptotically. The lower
above makes a UNIVERSAL o(n^2) sufficient-memory theorem impossible for this
class under the current contract. Option B is therefore false for the class
as presently defined, if this new construction passes independent review.

The existing margin ceiling still excludes cubic fixed-margin sections at
this SAME c/n gap. It supplies no stronger general obstruction closing the
remaining log n gap. No more near-critical regime is studied here.

There is a stronger horizon-specific conclusion: the constructed section uses
T<=n. At any fixed horizon T<=n, the counted 2Tn state/input store reconstructs
the full exact frozen sensitivity and answers all future queries without
discarded replay. Thus this family's O(n)-horizon problem has matching
Theta_c(n^2) continuous credit memory. The log n factor is not necessary for
THIS horizon; no conclusion follows for arbitrary-length histories.

The general log n arises from the sufficient tail estimate C a^H/gamma,
whose prefactor is order n before query improvements. It is not a demonstrated
number of independent robust age bands. In (6) repeated orbit periods aggregate
into the same d by l gradient block; storing each period separately is redundant
for that block. This makes the logarithm plausibly removable in structured
families, but does NOT prove it is technical for all dense recurrences.

No Omega(n^2 log n) section or uniform O(n^2) arbitrary-horizon encoder is
obtained. The log's necessity is OPEN, not fundamental or eliminated by claim.

## 11. Next theorem

After independent review of (5)--(13), pursue an arbitrary-horizon O_c(n^2)
continuous sufficient-memory theorem at gamma=c/n, with unchanged normalized
late queries and no discarded history tape. It must compress/aggregate old
credit rather than simply retain n log n time steps.

If that cannot hold, the falsifying result would be a jointly robust
Omega(n^2 log n) family under the same contract. The next question is now the
logarithmic gap, not whether quadratic robustness exists, provided this proof
survives review. No architecture design or other gap regime is authorized.

## 12. Status and resources

New author-derived proof; independent review is REQUIRED before acceptance.
No world-first mathematical novelty claim is made: the construction combines
standard orthogonal control choices with the accepted section/topological tools.
The accepted earlier theorem/lemma is invoked, not rerun. No numerical
experiment, matrix search, training, tensor computation, GPU/CUDA or automated
test was executed. The finite matrix recipes were not run. No experiment CPU
time or peak RAM measurement is claimed for writing/proof reasoning.
All historical artifacts and GAS-0 remain unchanged. Parameter count, input
domain, normalization, epsilon, late query and continuous encoder semantics
remain as declared. There is no practical bit/VRAM/runtime/learning lower bound.
