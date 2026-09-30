# Bounded proof development — what is proved and what is missing

## 1. Exact dimension counts (all widths, no empirical extrapolation)

For h_t=tanh(R hprev+W x_t+b), input width m=n, all entries of R,W,b
independently differentiated, zero fixed initial state:

- P(n)=2n²+n.
- State dimension n; global derivative array nP(n).
- No dependency-graph zeros in the dense parameterized family: every parameter
  can affect its own state row, and future dense recurrent edges can carry that
  effect to every other row. This is a structural allowance, not independence.
- Allowed endpoint dimension d(n)=n+nP(n)=2n³+n²+n.
- Counting minimum T(n)=ceil(d/n)=2n²+n+1=P(n)+1.

This proves how the *allowed* coordinate count scales. It does not prove that
all coordinates are independently reachable for arbitrary n.

For independent/diagonal recurrence, off-diagonal recurrent parameters are absent,
Pind=n²+2n; parameters have one output owner. Supported S entries=Pind,
identically zero entries=(n-1)Pind. dind=n²+3n and Tind=n+3. Exact owner-local
eligibilities store Pind numbers. Full rank in that space remains quadratic,
whereas the unrestricted dense endpoint allowance is cubic.

For two dense recurrent layers with current-time nonlinear mixing, per-layer
p=2n²+n, totalP=2p, state2n. Lower states do not depend on upper parameters:
np forced zeros; supported S3np. ddeep=2n+3np. Local base(h,E) dimension
2n+2np; upper-state/early-parameter cross block has np coordinates.

## 2. Analytic genericity: fixed width and horizon only

For every certified architecture/width/horizon, the selected minor determinant
is real analytic in real parameters and input history. The recurrent unroll,
its parameter derivative, and its mixed derivatives are finite compositions and
derivatives of real tanh/affine maps, hence analytic throughout the real domain.
One rigorously nonzero point shows that determinant is not identically zero.
Its zero set has measure zero and empty interior in the connected domain.
Thus full endpoint rank holds on an open dense, full-measure set of joint
parameters/inputs for THAT fixed width and horizon. At the exact certified
parameter slice the same conclusion holds for input history alone.

The zero-set theorem is given with proof in Boris Mityagin,
[The Zero Set of a Real Analytic Function](https://arxiv.org/html/1512.07276),
Proposition0. No genericity transfer from one width to another is claimed.
This statement also supplies no quantitative conditioning or probability bound
for a finite rational grid of inputs, and no guarantee for every parameter slice.

## 3. Width-extension attempt and exact missing step

First resolve the horizon issue analytically. At fixed x and parameters, write
the augmented one-step map as hnew=H(h), Snew=A(h)S+B(h,x), A=diag(tanh')R.
Its Jacobian in(h,vecS) is block triangular with diagonal blocks A and the
P-column lift of A. Therefore its determinant is(det A)^(P+1). If det R!=0,
all real tanh derivatives are positive and this augmented map is locally
invertible. Appending any fixed inputs preserves a full endpoint-rank witness.
Thus a certified width-n witness at T0 extends to every T>=T0 at the same
parameters, without new computations. Exact rational R determinants are checked
in validation.json. This is a SAME-WIDTH horizon extension, not a width induction.

Suppose a witness for width n exists. A candidate extension introduces one unit
and all dense parameter directions; P(n+1)-P(n)=4n+3, and
d(n+1)-d(n)=6n²+8n+4.

Start at a disconnected block embedding diag(Rn,r), then turn both coupling
directions on with epsilon. At epsilon0, sensitivities from parameters owned by
the new output row to old states, and vice versa, are identically zero for every
input history. The same is true of their input derivatives. Repeating independent
blocks therefore cannot certify the new full endpoint.

Ordering old and new input/output coordinates gives a block Jacobian. If an old
square submatrix remains invertible, elimination reduces the desired determinant
to det(Jold)*det(Hnew), where Hnew is the Schur complement for the newly introduced
endpoint directions and the remaining input coordinates. The local-invertibility
argument above preserves the old block at a later terminal time if its R block
is invertible. It still does not supply the missing new directions.

Analyticity allows an epsilon expansion. A valid induction must explicitly show
that the leading coefficient of det(Hnew(epsilon)) is nonzero for some selected
input sequence, accounting for all6n²+8n+4 new directions. This has NOT been shown.
Individual nonzero temporal paths do not prevent dependence or cancellation
among whole Jacobian rows. The stored n3/n4 determinants certify concrete finite
instances; they do not identify a symbolic epsilon coefficient for arbitrary n.
There is no recovered triangular pulse schedule or recursive determinant formula.

**Precise proof failure:** missing nonzero leading Schur-complement determinant,
not a discovered obstruction or a proof of compression. Do not promote this
attempt into an arbitrary-width theorem.

## 4. A proved auxiliary all-width algebra fact (not endpoint accessibility)

Assume W invertible and R invertible with every entry nonzero. Input controls can
set each next h anywhere in(-1,1)^n by
x=W^-1(atanh(h)-R hprev-b). Thus the diagonal gate
G=diag(1-h_i²) ranges over diagonals with entries in(0,1], and the state Jacobian
is A=G R.

The UNITAL algebra generated by these A matrices is all M_n(R):

1. G=I yields R. R^-1 is a polynomial in R by Cayley-Hamilton/invertibility.
2. A R^-1=G. The linear span of the admissible G matrices contains every diagonal
   matrix unit Eii (the admissible set has an open diagonal interior).
3. Eii R Ejj=Rij Eij, and Rij!=0, so every matrix unit Eij is in the algebra.

For instance R=alpha I+beta 11^T with positive alpha,beta and W=I meets these
conditions at every width. This demonstrates that nonlinear gate products need
not live in a fixed small matrix algebra as width grows. It uses linear
combinations of products from multiple control sequences. It DOES NOT show
that the same single input history independently varies every sensitivity
coordinate. Injection terms B_t=partial_theta f remain coupled to those same
states/inputs. Resolving that compatibility is exactly the missing accessibility
step. No primary ARBITRARY-WIDTH classification follows from this auxiliary fact.

## 5. Why the linear control is different

For common diagonal gamma at the fixed point, h=W ex+b eb,
S_W=I tensor ex, S_R=diag(eh), S_b=eb I. At fixed T, eb constant and ex/eh
have2n input-dependent coordinates, proving rank<=2n even if S looks dense.

A broader linear-family observation can be proved without new experiments:
for h_t=R hprev+W x_t+b and h0=0, the endpoint is affine in input history.
For each input channel, impulse-response sequences R^k W and their parameter
derivatives satisfy a scalar recurrence of order at most2n. Indeed, if chi is
the degree-n characteristic polynomial and E the time shift, chi(E)R^k W=0;
differentiate with respect to any parameter to obtain
chi(E)D_theta(R^k W)=-(D_theta chi)(E)R^k W. Applying chi(E) again gives zero.
W derivatives satisfy the original recurrence, and bias sensitivities have no
input dependence. Hence the span of impulse endpoint columns per input channel
has dimension at most2n, giving endpoint input rank<=2nm (<=2n² for m=n).
This is a linear-system rank restriction, not a bound for tanh. Time-varying G_t
and tanh second derivatives invalidate this fixed-coefficient argument.

## 6. Relation to existing system theory

Albertini and Dai Pra's1995 paper
[Forward accessibility for recurrent neural networks](https://www.research.unipd.it/handle/11577/2509993)
has a primary repository abstract describing an algebraic accessibility
characterization. Its manuscript link returned403 in this audit. No uninspected
theorem is claimed to settle this parameter-sensitivity lift. Hidden-state
accessibility or parameter identifiability alone is not the endpoint question.
Next proof work should inspect whether an applicable theorem covers this exact
augmented discrete-time lift before developing a new induction.

## 7. Scope and next mathematical step

Finite-width full-rank certificates support the cubic allowed-state count at
those widths. No arbitrary-width induction, finite-precision storage bound,
gradient-query observability, task utility, architecture claim, or learning
experiment follows. The next bounded mathematical question is whether the
fully actuated tanh sensitivity lift has a constructive accessibility proof,
or whether a specific pulse schedule yields a provably nonzero Schur complement.
Stop here; no Stage C, observability experiment, AMS v10, or width5 sweep.
