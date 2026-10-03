# Absolute input energy: center calculation and a frozen-endpoint obstruction

Codex, 2026-10-03. New elementary arguments; independently review these new
arguments if desired. Accepted accessibility, observability, multiharmonic and
local-radius proofs are premises and are not re-reviewed or modified.

## 1. Scope and unchanged units

Use the accepted hard dense tanh family, for integer n >= 200:

    k=floor(n/2), l=n-k, r=k-1, d=floor(n/4),
    a=1-1/n, lambda=1/(100n), b0=1/20,
    U=I-2ww^T/(w^T w), w=e0-1_k/sqrt(k),
    P=P_d direct_sum I_(k-d), O=UPU,
    R0=diag(aO, lambda I_l),
    ||R||op=a, ||R-R0||op <= e_n=4/(10^8 n^2),
    h_t=tanh(R h_(t-1)+x_t+b0 1_n), h_0=0, W=I.

All R,W,b entries are independently differentiated; P_n=2n^2+n. Raw-input
history norm is the Euclidean norm of all concatenated x_t, including public
preparation and reset. Inputs remain in the accepted past cube. None of the
normalization, epsilon=0.001 or permitted late-query family is changed.

The accepted fixed-feature contract ends at **h_T=0**. The new absolute-energy
requirement counts the public center as well as its perturbations. Section 5
uses only the exact state equation to obstruct this requirement. No Frobenius,
RMS, tangent-rank or ambient-operator replacement for query separation is used.

The statements concerning other common endpoints in sections 6--8 are
explicitly scoped; they are not a solution for an enlarged contract.

## 2. The exact current center, including both boundary steps

Put

    s=2/5, z0=3/20, beta=sqrt(z0/n),
    B=atanh(beta), A=atanh(s),
    N=ceil(4n log n)+1,
    p=(0_k, s 1_l), v=(beta 1_k, s 1_l).

Here beta is a hidden-state amplitude, not the public loss-normalization
constant also called beta in earlier theory. Natural log is used.

The frozen positive square-root lift has states

    h_0=0,
    h_1=p                         (source preparation),
    h_2=...=h_(N+1)=v             (N interior states),
    h_(N+2)=0                    (exact reset).

The protected memory coordinate is beta too. At zero section parameter all
defects vanish. These are precisely the center of the accepted local-radius
section, not a newly optimized witness. Define q=atanh(v)-b0 1_n, where atanh
acts coordinatewise. For the actual frozen R its norm is given EXACTLY by

    E_R(n)^2 = ||atanh(p)-b0 1_n||_2^2
               + ||q-Rp||_2^2
               + (N-1)||q-Rv||_2^2
               + ||Rv+b0 1_n||_2^2.                    (1)

This formula needs no evaluation of an exponentially large input array.
If different public square-root signs were chosen, (1) remains valid with
that public v; the closed formula below is for the positive lift used here.

## 3. Exact reference formula and rigorous dense sandwich

The Householder sends 1_k to sqrt(k)e0. Because d>=2, e0^T P e0=0, so

    1_k^T O 1_k = (U1_k)^T P(U1_k) = 0,
    ||O1_k||_2^2=k.                                     (2)

This orthogonality is important: the bias and recurrence do not cancel in
the norm of the center. For R0, the four input types are

    preparation:  (-b0 1_k, (A-b0)1_l),
    first interior: ((B-b0)1_k, (A-b0-lambda s)1_l),
    later interiors: ((B-b0)1_k-a beta O1_k,
                      (A-b0-lambda s)1_l),
    reset: (-a beta O1_k-b0 1_k, -(b0+lambda s)1_l).

Summing squared norms, with N-1 later interiors, proves

    E_0(n)^2 = k{2b0^2 + N[(B-b0)^2+a^2 beta^2]}
             + l{(A-b0)^2 + N(A-b0-lambda s)^2
                         + (b0+lambda s)^2}.            (3)

There is no discarded preparation/reset term. The current center's dense
correction is rigorously bounded in concatenated input norm by

    Delta_n = e_n sqrt(s^2 l + N[beta^2 k+s^2 l]).        (4)

Indeed, input changes from R0 to R are -(R-R0)h_previous. The previous-state
list consists of 0, p and N copies of v. Sum their squared norms and apply
the operator bound. The reverse triangle inequality gives the sharp enclosure

    max(0,E_0-Delta_n) <= E_R <= E_0+Delta_n.             (5)

Formula (1) is the exact answer for the actual R; (3)--(5) are a computable
two-sided bound using only its accepted public perturbation estimate.

Let

    C_abs = sqrt(2[b0^2+(atanh(s)-b0)^2]).                (6)

Since k/n,l/n tend to 1/2, N/(n log n) tends to 4, B tends to 0, a tends to 1,
lambda tends to 0 and Delta_n/(n sqrt(log n)) tends to 0, (3)--(5) imply

    ||X_n(0)||_2 / [n sqrt(log n)] -> C_abs.

Thus the norm itself grows, not merely an upper majorant. The leading terms
come from N*k*b0^2 memory bias-cancellations and N*l*(atanh(s)-b0)^2 source
maintenance. The small baseline memory amplitude beta does not remove its
required bias cancellation. Preparation/reset add O(n) squared energy and
are lower order here, but they individually grow in norm.

The accepted section has uniform local bound L=0.00970048 (strictly). Hence
EVERY history in that section also satisfies

    E_0-Delta_n-L < ||X_n(y)||_2 < E_0+Delta_n+L,          (7)

with a zero lower truncation if needed at small widths. Consequently the
entire section, not only its public center, has the same absolute-norm
asymptotic. No choice of F or delta changes (3) at the center.

## 4. Current-mechanism energy ledger and attempted changes

The accepted joint dimension and separation are premises:

    D_n=floor(d/10^6)*floor(n^(1/18)),
    D_n >= n^(19/18)/20,000,000, n>=10^900,
    boundary half-margin >999.999649997999.

Its local perturbations remain admissible and exactly reset. Equation (7)
supplies the missing absolute-energy entry. There is no new constant-energy
robust section in this ledger.

Shrinking F/delta, improving co-moving cancellation or sharing harmonic slots
reduces local perturbation cost but leaves center (3) and source preparation
unchanged. Shortening the window reduces its maintenance cost but cannot
remove the preparation/reset cost. Sparse source activity does not make
zero source states free: at source state zero the bias must be cancelled.

More precisely, with a constant public source level s' in the same block,
the reference maintenance input is

    psi_n(s')=atanh(s')-lambda s'-b0,

with source costs l(atanh(s')-b0)^2 for preparation, N*l*psi_n(s')^2 for
maintenance, and l(b0+lambda s')^2 for reset. Their square roots are norms.
The actual maintenance/reset source correction is at most e_n sqrt(n) per
step. Choosing psi_n(s')=0 removes reference maintenance input, not the
reset cost. Changing s' also changes the feature and signal ledger; no old
robust margin is asserted for that change. Setting b0=0 or changing the
required endpoint would change the frozen model/endpoint contract.

There is a stronger obstruction covering every such proposed redesign next.

## 5. Universal terminal-energy obstruction at the required endpoint

THEOREM (frozen-family feasibility). For ANY nonempty finite history, any
admitted or unrestricted past inputs, and any gate choices, if its actual
last hidden state is h_T=0, then

    ||X||_2 >= L_n
      := (b0-lambda)sqrt(l) - e_n sqrt(n).               (8)

This holds in particular over a whole continuous section; no tangent or
independent-axis argument is involved.

PROOF. Tanh is injective and tanh(0)=0, so the exact last update forces

    x_T=-R h_(T-1)-b0 1_n.

Every previous hidden coordinate has absolute value <1, or is the initial
zero. Let Pi_s project onto the source block. Its reference recurrent image
is lambda h_previous,source; the dense residual is at most e_n sqrt(n).
Therefore

    ||Pi_s R h_previous||_2 <= lambda sqrt(l)+e_n sqrt(n),
    ||x_T||_2 >= ||Pi_s x_T||_2
              >= b0 sqrt(l)-lambda sqrt(l)-e_n sqrt(n).

Finally ||X||_2>=||x_T||_2. This proves (8). It uses the real coupled dynamics,
not a selectable injection or a surrogate query norm. QED.

Since l>=n/2 and n>=200, sqrt(n/l)<=2 and

    b0-lambda-2e_n
      >= 1/20-1/20000-8/(10^8*200^2) > 499/10000,

we obtain the convenient exact consequence

    ||X||_2 > (499/10000)sqrt(n/2),
    ||X||_2^2 > (249001/200000000)n.                    (9)

Thus a fixed absolute budget R requires

    n < (200000000/249001) R^2.                         (10)

For every fixed finite R, the accepted zero-endpoint history class is EMPTY
for all sufficiently large n. No omega(n) robust section, or even a single
nonempty history, can exist there. A zero-length history at h_0=0 is just
one point with zero credit and cannot supply a positive-dimensional section.

One may conventionally assign robust dimension zero to that empty/singleton
class, yielding a vacuous zero-state upper bound. This is not a substantive
O(n) sufficient-statistic theorem. It proves infeasibility of the stated
unchanged-endpoint asymptotic target, not a general bounded-energy compression
theorem for other common endpoints or other models.

## 6. Even changing the endpoint cannot save the same weak-gate window

The following scoped obstruction does not use source H or a final reset.
At two consecutive interior steps in the accepted selected gate cube,

    |h_selected,i| <= 1/(2sqrt(n)).

Signs can be arbitrary. Define L_at=1/(1-1/(4n)), C_n=sqrt(r/(4n)). Then

    ||atanh(h_selected,current)||_2 <= L_at C_n,
    ||Pi_selected R0 h_previous||_2 <= a C_n.

The protected memory coordinate does not contribute here because O fixes e0;
the reference source-to-selected block is zero. The dense correction is
bounded by e_n sqrt(n) regardless of other hidden states. It follows that

    ||x_selected||_2 >= B_n
      := b0 sqrt(r) - (L_at+a) C_n - e_n sqrt(n).        (11)

Use the positive part if B_n<=0. For any N consecutive such interior states,
there are N-1 transitions of this kind, in disjoint physical time slots:

    ||X||_2 >= sqrt(N-1) max(0,B_n).                    (12)

For N=ceil(4n log n)+1 the right side is asymptotic to
b0 sqrt(2) n sqrt(log n). This is a lower bound on actual raw-input energy,
not a claim about visible dimension. At fixed absolute R the number M of
transitions between two weak states must obey M<=R^2/B_n^2 whenever B_n>0.

It precludes maintaining the same long multiharmonic weak-gate window by
shrinking the source, removing reset, duty cycling sources, or changing signs.
Short bursts and different gate regimes could leave this scope; no inherited
multiharmonic margin is claimed for them. Section 5 still prohibits any such
burst construction with the required final h=0 at fixed absolute R.

## 7. Explicit energy--dimension--margin tradeoff

For the ACCEPTED local-radius family, an absolute budget sufficient for the
same D_n and accepted margin is

    R >= E_0(n)+Delta_n+0.00970048.                      (13)

Every member of that family needs at least
E_0(n)-Delta_n-0.00970048. Equations (3)--(7), D_n above and the unchanged
accepted margin are an explicit lower/upper energy ledger for this family.
Asymptotically

    D_n ~ n^(19/18)/(4*10^6),
    R_family ~ C_abs n sqrt(log n).

Eliminating n gives, for this construction only,

    R_family ~ C_abs (4*10^6 D_n)^(18/19)
                          sqrt((18/19)log(4*10^6 D_n)). (14)

This is not a universal minimum-energy law; it is a sharp cost of the existing
section. The construction's lower-bound dimension has not been promoted to
a whole-class upper bound.

For ALL histories with the frozen zero endpoint, (8)--(10) give a universal
necessary width--energy relation, independent of the margin. Therefore the
unchanged contract has no unbounded-width asymptotic at fixed absolute R,
irrespective of epsilon. This is stronger than a tradeoff based on tangent
singular values and has no finite-bit interpretation.

## 8. Boundary of the conclusion and a precisely different open question

For another common endpoint z, the same exact terminal equation gives only

    ||X||_2 >= ||atanh(z_source)-b0 1_l||_2
                  - lambda sqrt(l)-e_n sqrt(n).        (15)

For endpoints near the autonomous biased source equilibrium this can be small.
So (8) must not be quoted as an obstruction to every possible common endpoint.
Indeed a zero-input trajectory has zero input energy and need not end at zero.
No general bounded-energy O(n) theorem for such endpoints follows.

If the owner changes the target to allow those endpoints, the remaining
mathematical question would be the antipodal robust width, in the ACTUAL
accepted query metric, of continuous fixed-endpoint sections inside

    {X: ||X||_2<=R, h_T(X)=z_n},

uniform over public z_n and finite T. At present this analysis gives no
superlinear construction or useful O(n) upper theorem for that enlarged class.
Exact reference storage remains a quadratic fixed-feature upper bound in its
previously established scope. It is not a new solution here.

The accepted growing/local-radius lower bounds and full-model n^2--n^2 log n
gap remain unchanged. Their interpretation is narrower: a robust response to
a small LOCAL perturbation can coexist with a very large absolute drive.
This stage counts that drive and demonstrates its divergence rather than
equating local perturbation energy with total physical input energy.
