# Near-critical robust credit memory: a partial phase diagram

2026-10-01. Theory only. New lower construction for independent mathematical
review; no numerical witnesses, training, local dimension search or architecture.

## 1. Model, units, queries and quantifiers

Fix h_t=tanh(R h_(t-1)+W x_t+b), h0=0, frozen parameters, all
P=2n^2+n entries independently differentiated. S_t=D_theta h_t.
The normalized sensitivity is Z_t=S_t D_theta, where D_theta uses frozen
R/W/b group RMS scales. These scales are NOT differentiated through theta.
The past inputs lie in (-1/2,1/2)^n, the same bounded support convention as
the archived witness search. Input-SD coordinates have sigma_x=sqrt(3/32);
changing the history chart's labels does not rescale the gradient metric.

Use the accepted late scalar head q=1/sqrt(n) * 1, loss divided by the frozen
beta=max(1,||R||F). A one-step future query has effective adjoint

    c(v)=R^T diag(sech^2(Rh+Wv+b)) q / beta.

The permitted future-preactivation box includes [1/4,3/4]^n. Thus the specific
query with every preactivation 1/2 is permitted. Nothing below grants arbitrary
immediate loss vectors to obtain the lower bound. Future direct parameter
injection is included in gradient answers and cancels ONLY at the same h.

At fixed h define D_C(Z1,Z2)=sup_permitted_queries ||(Z1-Z2)^T c||_2.
A continuous fixed-h history section X(u), u in the r-dimensional unit ball,
with boundary antipodal separation >=2m for EVERY u in S^(r-1), m>epsilon,
forces at least r continuous stored coordinates by accepted Borsuk-Ulam.
This is not a count of bits, grid points or strong tangent singular values.

For a model define k_eps as its least worst-case sufficient continuous
sensitivity memory, with endpoint h supplied. A section supplies a lower
bound on k_eps. Our phase diagram's class lower bounds are EXISTENTIAL:
some explicitly specified admissible dense family needs that many coordinates.
They are not universal over every model with the same contraction gap.

Upper bounds assume ||R||op<=a=1-gamma<1, ||W||op<=w, bounded coordinate
inputs |x_j|<=B and RMS(b)<=b_*, with w,B,b_* independent of width.
Then C=sqrt(a^2+w^2 B^2+b_*^2) bounds normalized injection operator norm.
For one or more future steps all permitted effective adjoints satisfy

    ||c||<=kappa_Q=a/beta<=1.

For an enlarged query contract with immediate arbitrary unit adjoints,
replace kappa_Q by 1. The lower construction does not enlarge the contract.

## 2. The accepted recent-window upper, counted precisely

Write A_t=diag(1-h_t^2)R and B_t for the normalized parameter injection.
The accepted contraction argument gives

    ||Z_T-Z_T^[H]||op <= C a^H/gamma.

Retain h_(T-H),...,h_(T-1) and x_(T-H+1),...,x_T: 2Hn numbers on the
fixed-h fiber. The supplied h_T and these retained states determine every
gate in the retained window. An unrestricted query decoder can reconstruct
the Jacobian products and the truncated VJP from these counted quantities.
No discarded input is read, and no forward transition is replayed. Fixed
time padding makes this a continuous history encoder. Decoder temporary work
and time are not constrained by this persistent-coordinate model. This is
not an online-computation or finite-VRAM theorem.

The normalized late-query error is bounded by

    e_H = kappa_Q C a^H/gamma.

Take H=0 if kappa_Q C<=epsilon gamma; otherwise

    H=ceil(log(kappa_Q C/[epsilon gamma])/[-log(1-gamma)]).

Then

    k_eps <= min(nP, 2nH).                                    (U)

Add n when exact h must also be retained. Counting the same h twice is
unnecessary. The usual gamma^-1 logarithm is a conservative simplification,
since -log(1-gamma)>=gamma. Group-RMS normalization is essential to a
width-independent C. Raw gradient units do not have the same statement.

### Historical clarification

The previous author proof's H(n^2+2n) factor store was sufficient but redundant.
The independent bounded review demonstrated the counted 2Hn store above.
Its proposed matching quadratic target under fixed uniform contraction is
therefore impossible. The previous files remain unchanged historical evidence;
this document supersedes that NEXT-THEOREM recommendation, not their provenance.

## 3. Improved margin ceiling and the transition obstruction

For any continuous r-dimensional fixed-h antipodal history section, compose
its boundary with the 2Hn encoder. If 2Hn<r, an antipodal pair encodes identically.
Both exact gradient answers are within e_H of the same decoded answer, hence
their query distance is <=2e_H. Therefore the section's half-margin obeys

    m <= (kappa_Q C/gamma)
         (1-gamma)^(ceil[r/(2n)]-1).                          (M)

Use H=ceil[r/(2n)]-1, which is nonnegative and gives the strict dimensional
inequality. This applies to nonlinear sections, not merely one SVD box.

For r=nP=2n^3+n^2 the exponent is exactly

    n^2+ceil(n/2)-1.

Consequences at fixed epsilon and uniform bounded C:

1. gamma=Theta(1): quadratic margins are O(exp(-c n)); cubic margins are
   O(exp(-c n^2)). Thus a fixed-margin quadratic/cubic lower cannot occur.
2. gamma=Theta(1/n): a cubic section's margin is O(n exp(-c n)); it collapses.
   A quadratic section receives only an O(n exp(-O(1))) ceiling, which is
   nonrestrictive. This is NO quadratic existence proof.
3. gamma=Theta(1/n^2): for cubic sections the ceiling is O(n^2 exp(-O(1))),
   which is nonrestrictive. This is NO cubic existence proof.

A more general necessary condition for a fixed-margin cubic section is that
gamma n^2 not dominate log(kappa_Q C/[epsilon gamma]). This is a necessary
condition only. It contains a logarithmic boundary layer; one must not infer
an exact critical threshold gamma=1/n^2 from it.

## 4. A self-contained bounded-spread lemma

The next construction needs many continuous input coordinates while every
individual input coordinate stays bounded. A plain Euclidean ball inside
the cube would have a vanishing normalized margin. The following nonlinear
odd section avoids that elementary failure.

LEMMA. For every N>=1000 and r=floor(N/1000), a completely specified finite
selection procedure can produce a matrix M in {-1,+1}^{N x r} such that

    ||M||op < 9 sqrt(N),
    ||tanh(Mu)||_2 >= sqrt(N)/16 for every ||u||_2=1.         (L)

Here tanh is componentwise. No matrix is chosen by evaluating a credit
certificate. The finite construction below is proved to terminate.

PROOF OF EXISTENCE. Choose independent random signs for the matrix entries.
For a fixed unit u, X=sum_j sign_j u_j has E X^2=1 and E X^4<=3.
Cauchy-Schwarz gives

    1 <= 1/4 + sqrt(3 Pr[|X|>=1/2]),

so that probability is at least p0=3/16. Different matrix rows are independent.
For N Bernoulli indicators with success probability at least p0, the exponential
Markov bound with lambda=log(2) gives

    Pr[count < p0 N/2] <= exp(-p0 N/8)=exp(-3N/128).

Indeed E exp(-lambda count)<=exp(-p0 N(1-exp(-lambda))), and log(2)<=3/4
gives lambda/2-1/2<=-1/8. If at least 3N/32 rows satisfy |X|>=1/2, then
tanh(1/2)>2/5 gives

    ||tanh(Mu)|| > sqrt(3N/200) > (3/25) sqrt(N).

Fix an eta=1/160 unit-sphere net with at most 321^r points. Such a net follows
from a maximal eta-separated set and disjoint Euclidean eta/2-ball volumes.
The union failure probability for these net lower bounds is at most

    321^r exp(-3N/128) <= exp(-279N/16000),

using log(321)<6 and r<=N/1000.

For completeness the matrix operator bound also needs no assumed theorem.
For fixed unit v,u, E exp(t v^T M u)<=exp(t^2/2), because independent signs
have cosh(s)<=exp(s^2/2) and sum_(i,j) v_i^2 u_j^2=1. Hence
Pr[|v^T M u|>4 sqrt(N)]<=2 exp(-8N). Use 1/4-nets in both unit spheres,
with at most 9^(N+r) pairs. Approximation in the two arguments gives
||M||op<=2 max_net |v^T M u|. Therefore

    Pr[||M||op>8 sqrt(N)] <= 2 exp((N+r)log(9)-8N)
                           <= 2 exp(-7N/2),

where r<=N and log(9)<9/4 suffice. The sum of the two failure probabilities
is less than one at N>=1000. Thus a matrix meets both strict selection
conditions: ||M||op<9 sqrt(N), and all first-net values >3sqrt(N)/25.

Since componentwise tanh is 1-Lipschitz, every unit u is within 1/160 of a
net point and

    ||tanh(Mu)|| >= (3/25-9/160)sqrt(N)
                  = (51/800)sqrt(N) > sqrt(N)/16.

This proves (L).

DETERMINISTIC SPECIFICATION. Fix a deterministically constructed algebraic
eta-net before selecting M; a maximal separated net may be specified using
algebraic sphere points and finite real-algebraic covering tests. Enumerate
all sign matrices. Dovetail outward-precision checks of the two STRICT finite
selection conditions; use a fixed precision/index ordering to select the
first certified matrix. Spectral bounds are algebraic, and tanh net values
admit outward bounds. The positive probability proof ensures termination.
No compact infinite condition is used in the selection algorithm: the
uniform conclusion follows from the finite net and the Lipschitz bound.

This is a deterministic, computable specification, NOT an efficient or
closed-form matrix formula. Exhaustive selection is not executed here. The
exponential construction cost is irrelevant to an existence/lower theorem,
but it must not be advertised as an efficient implementation.

## 5. Explicit dense recurrent family and fixed-h section

For n>=2000 put N=floor(n/2), r=floor(N/1000), and choose the specified M above.
Let q=1/sqrt(n)*1, choose ANY a in [1/2,1), and set

    delta=1/(100n),
    R=delta I + (a-delta) q q^T,
    W=I, b=(1/20)*1.

All recurrent entries are nonzero; all off-diagonal entries are positive.
The family is genuinely dense, not independent block recurrence. R has
eigenvalues a once and delta n-1 times, so ||R||op=a and gamma=1-a exactly.
It is invertible, and

    R^-1=delta^-1 I + (a^-1-delta^-1)q q^T

has every entry nonzero. W is invertible. All R,W,b entries are independently
differentiated, with P=2n^2+n, even though their BASE VALUES have this pattern.
There is no tying of parameter perturbations to a or delta.

The frozen RMS scales are positive. In particular w_W=1/sqrt(n), w_b=1/20,
and beta=max(1,sqrt(a^2+(n-1)delta^2))<5/4, uniformly in width.

For u in the closed r-dimensional unit ball define v(u)=tanh(Mu), and

    z(u)=(2/5) ( v(u), -v(u), 0_if_n_is_odd ).

The pairing ensures q^T z=q^T tanh(z)=0 EXACTLY. Each coordinate has absolute
value <2/5. On the boundary, the lemma and 2N>=n/2 give

    ||z(u)|| >= (2/5) sqrt(2N)/16 >= sqrt(n)/60.           (Z)

Define the TWO-STEP realized input history

    x1(u)=z(u)-b,
    h1(u)=tanh(z(u)),
    x2(u)=-R h1(u)-b=-delta h1(u)-b.

Then h2=tanh(Rh1+x2+b)=0 exactly for EVERY u. The histories stay inside
(-1/2,1/2)^n: |x1_j|<9/20, and |x2_j|<=delta+1/20<1/2.
This is a joint curved fixed-h section, not individually compensated axes.
It has a continuous ball lift and injective chart, since (L) implies M has
full column rank and componentwise tanh is injective. No hidden-section
approximation or curvature majorant is required.

When computing parameter sensitivity, the REALIZED x1,x2 are held fixed.
The derivative of this parameter-dependent HISTORY FORMULA is NOT included.
Differentiating the compensator together with theta would incorrectly make
the sensitivity vanish and would change the query contract.

## 6. Uniform antipodal query margin: full calculation

Let G1=diag(sech^2(z)). For antipodes, z(-u)=-z(u), h1(-u)=-h1(u), while G1
is identical. At h2=0 the second-step gate is I. For a W parameter direction,

    S2_W deltaW = R G1 deltaW x1 + deltaW x2.

Choose the single permitted future input v_f=(9/20)*1. At h2=0 it gives
future preactivation (1/2)*1. With kappa=sech^2(1/2)>3/4,

    c = kappa R^T q/beta = kappa a q/beta.

This is an actual allowed late query; no arbitrary adjoint is inserted.
The normalized W-gradient difference between the antipodes is

    Delta g_W
      = 2 w_W [G1 R^T c z^T - delta c tanh(z)^T]
      = (2 w_W kappa a/beta)
          [a G1 q z^T - delta q tanh(z)^T].                (G)

The direct future parameter injection is the same at h2=0, so cancels.
Other R/b-gradient blocks cannot cancel the Euclidean W-block norm.
Using ||q||=1, ||tanh(z)||<=||z||, and |z_i|<=2/5,

    ||G1 q|| >= 1-(2/5)^2 = 21/25,
    ||Delta g||_2 >= ||Delta g_W||F
      >= (2 w_W kappa a/beta) [a(21/25)-delta] ||z||.

For a>=1/2, delta<=1/200, beta<5/4, (Z) and w_W=1/sqrt(n), the
HALF-separation is at least

    m >= (3/4)(1/2)(4/5)(83/200)(1/60)
       = 83/40000 = 0.002075 > epsilon=0.001.             (P)

This bound holds jointly for ALL unit u at EVERY n>=2000. Its constants are
deliberately conservative. It gives a real finite-radius robust section;
no tangent rank, empirical singular spectrum or interval midpoint is used.

### Theorem: a uniform linear robust lower bound

For the specified dense tanh family, any continuous no-discarded-replay
encoder answering every allowed late query within epsilon=1e-3, with exact
h2=0 supplied, requires at least

    r=floor(floor(n/2)/1000)=Omega(n)

persistent real coordinates. Proof: if k<r, Borsuk-Ulam on the boundary
sphere forces equal memories for antipodes; uniform error permits distance
at most 2epsilon, contradicting (P).

The same uniform margin works for ANY chosen a_n in [1/2,1). In particular
it works for gamma=1/2, gamma=1/(2n), and gamma=1/(2n^2). Thus a linear lower
is real in all three regimes, but this construction does NOT amplify its
dimension when gamma shrinks. Its horizon is two, not order 1/gamma.

## 7. Phase diagram: what actually matches

Fix epsilon=1e-3, bounded normalization/injection constants and the same late
query contract. Class lower bounds mean that some admissible family requires
that many coordinates; class upper bounds hold for every family in the class.

| Gap | Strongest proved class lower HERE | Strongest general class upper used HERE | Match? |
|---|---|---|---|
| gamma=Theta(1) | Omega(n), margin >=0.002075 in specified dense family | O(n) | YES: worst-case Theta(n) |
| gamma=Theta(1/n) | Omega(n), same margin | O(n^2 log n), capped by O(n^3) | NO quadratic lower proved |
| gamma=Theta(1/n^2) | Omega(n), same margin | O(n^3) using exact RTRL cap | NO cubic lower proved |

In the middle regime cubic fixed-margin sections are impossible by (M).
Quadratic scaling, a logarithmic enhancement, or substantially smaller
memory are all consistent with these bounds. In the third regime a cubic
transition is permitted by the upper analysis but NOT established.
At each FIXED width, exact accessibility still gives cubic lower dimension
below some epsilon_n>0; this does not say epsilon_n stays above 1e-3.

## 8. Why contraction gap alone is not a complete phase coordinate

The construction's dense R has one slow collective eigenmode and n-1 fast
modes, with beta bounded. Its linear section already exists at horizon two.
Shrinking the contraction gap does not itself create more independent
slow sensitivity injections. This distinguishes a worst-case CLASS diagram
from a claim that every individual family's memory undergoes a transition.

Conversely if ||R||F>=c0 sqrt(n), then beta>=c0 sqrt(n) and kappa_Q<=a/(c0 sqrt(n)).
Under constant gamma and bounded C,

    ||Z_T^T c|| <= C a/(gamma c0 sqrt(n))

uniformly over every past history. Once this is <=epsilon, storing exact h
and ZERO sensitivity coordinates suffices for the accepted delayed queries,
by outputting just the common future-injection gradient. High stable rank
can therefore make the SAME normalized head contract weaker as width grows.
This does not contradict our low-stable-rank existential lower, nor does it
apply to immediate arbitrary unit losses.

Further obstacles to a superlinear construction are:

- Many slow propagation directions are needed, not merely one eigenvalue
  near one. Propagation and parameter injections share the same trajectory.
- tanh saturation can change effective contraction G_t R far more than the
  nominal gamma. Keeping gates close to one restricts allowed hidden-state
  excursions and nonlinear diversity.
- The group-RMS factors and beta must stay in the declared contract. Dropping
  beta or rescaling the head/epsilon would invalidate a claimed match.
- Separate large face ranges do not prove a jointly robust section. For
  quadratic/cubic lower dimensions every antipodal point must stay separated.
- Fixed-h compensation must be joint and must hold inputs fixed during
  parameter differentiation.
- The 1/gamma logarithmic upper uses a geometric-tail sufficient bound; it
  is not a proof that the logarithm is necessary.

These are proved quantitative obstructions or specific missing proof steps,
not a theorem that no quadratic/cubic construction exists.

## 9. Single next theorem to pursue

Prove OR REFUTE a near-critical quadratic section theorem: an explicitly
specified dense family with gamma=c/n, inputs in the existing cube, the
accepted RMS/beta/head contract, and a continuous exact fixed-h section of
dimension >=c' n^2 with uniform antipodal half-margin >1e-3.

A proof would establish an actual linear-to-at-least-quadratic transition
while the cubic exclusion in that regime remains valid. A refutation for a
well-defined sufficiently broad family would identify which of query dilution,
gate contraction or injection coupling defeats the putative transition.
Do NOT claim a full class refutation from failure of one proposed family.

Before relying on the new linear theorem, independent review should check its
bounded-spread lemma, finite deterministic selection specification, exact
fixed-h compensation and the held-input W-gradient calculation. No local
width-4 dimension search or new architecture is needed for that review.

## 10. Status and resource scope

The upper-window improvement is owner-accepted and independently reviewed.
The bounded-spread lemma and lower construction are new author-derived proofs,
not independently reviewed or formally machine-verified. All steps are stated
above, with explicit rational inequalities where possible.
No new experiments or automated tests were run. No matrix selection algorithm
was executed. No CPU/GPU training, witness search or interval certification was
performed. No measured experiment CPU/RAM claim is made for proof reasoning.
Historical evidence, accepted local certificates, GAS-0 and other notebooks
remain untouched. This is a continuous-coordinate theorem, not bit complexity,
GPU memory, useful learning, fast decoding or architectural superiority.
