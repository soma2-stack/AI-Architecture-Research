# Query-visible operator dimension: partial theoretical result

2026-10-02. **ARBITRARY APERIODIC MEMORY LOG GAP STILL OPEN.**
New author-derived lemmas require independent review. No experiment ran.
The hostile review of d609d4d is accepted, including rejection of basis
renewal as a reduction of the general problem. Historical evidence is preserved.

## 1. Strongest results

**Exact aggregate identity, with full counting.** For each actual history,
complete remaining-block credit can be written using p=2n+1=O(r) operator
matrices, at every horizon and for every allowed future query:

    M_j,t=a G_t O_* M_j,t-1+f_(t,j) G_t,
    Zbar_t Phi=sum_j M_j,t Phi e_j.

This is exact for the reference; actual normalized query error is at most the
accepted delta_dense. It includes gate-history variation. But storing these
history-dependent matrices costs p r^2+(l+1)p credit coordinates, Theta(n^3),
plus n if current h is not supplied. It is a regrouping of reference RTRL,
NOT a quadratic encoder or a novel method. It exposes why a bare O(r)
operator count is insufficient: the operators themselves need representation.

**Finite-error metric obstruction.** At c=1 the actual query norm preserves
r^2 robust coordinates on an AMBIENT accumulated-operator Frobenius ball of
radius n/4. Any public linear subspace of dimension less than r^2 has uniform
query approximation error >.004851 at epsilon=.001. An abstract continuous
encoder for that ball needs at least r^2 coordinates; its packing has at least
1.617^(r^2) states separated by more than2epsilon.

**No admissible history lift of that ball was proved.** It lies inside the
generic credit norm allowance, which is not the same as being reachable.
This is NOT a new recurrent-memory lower or a logarithmic lower. It disproves
only a metric-only claim that normalization must hide almost all operator
directions at the accumulated-credit scale.

## 2. Precise definition and quantifiers

Frozen variables: c>0, gamma=c/n, epsilon=1e-3, group-RMS normalization,
accepted rotating/dense tanh family and normalized late scalar-head queries.
Primary comparisons use the existing h=0 endpoint, not new witnesses.
k=floor(n/2), l=n-k, r=k-1, p=2n+1.

For an operator T and a shared raw source feature H, define

    nu_H(T)=w_R ||H|| sup_(allowed c_q)||T^T E^T c_q||.

The query-visible linear approximation dimension q_Q(K,eta) is the least
dimension of a subspace approximating every member of a compact set K within
eta in THIS norm. Separately q_joint(X,e) allows approximated kernels to
preserve the full feature-coupled credit of one history X within error e.

| Object | Result | What it does not establish |
| --- | --- | --- |
| Exact invisible operator subspace | {0} | Finite-radius robustness |
| Active coupled aggregates in one history | O(r) operators, exactly | Quadratic counted state |
| Individual relevant kernels in one history | O(r log r) sufficient retained templates | Optimality, cheap basis storage or an online aggregate |
| Ambient accumulated-operator ball | r^2 robust coordinates at c=1 | Reachability by actual histories |
| Actual jointly robust aperiodic operator section | Unresolved | No new Omega(r^2) operator theorem |
| Quadratic structured approximation of all actual histories | Unresolved | No universal O(n^2) encoder |

A public subspace for all histories, a history-dependent subspace for one
history, and a jointly robust continuous same-endpoint section are different
claims. This stage does not substitute one for another.

## 3. Physical finite-error bounds

For H=(2/5)1_l, the permitted one-step preactivation box [1/4,1/2]^n gives

    lambda_H ||T||F <=nu_H(T)<=Lambda_H ||T||op,
    lambda_H=s_g(a-e)||H||/(n sqrt(n)),
    Lambda_H=a||H||/n,
    s_g>7/100, e<=4/(10^8 n^2).

The lower is derived from actual allowed sign-corner queries; the upper covers
ALL allowed continuations. Frobenius norm is translated to a physical query
margin here, not treated as the query contract by itself. No unit-adjoint
replacement, per-entry parameter scaling or epsilon adjustment is used.

At the natural accumulated radius n/4, lambda_H times radius exceeds .004851.
At general c the radius n/(4c) gives that constant divided by c; this report
does not claim the same epsilon result when that margin becomes insufficient.

Individual bounded transport packets are much weaker. Their selected-group
query norm is at most .4/sqrt(n). Nevertheless an actual constant-source,
scalar-gate history with exact terminal h=0 has accumulated selected query
norm >.0058 sqrt(n)-delta_dense at c=1 for large n divisible4. Thus packets
can individually be epsilon-small while their sum is strongly visible.
This analytic control is already quadratically encodable; it supplies no
new independent age bands or operator dimensions.

## 4. Correct joint error, not a pointwise spectral threshold

For actual gates and the actual shared features f_s, kernel errors obey

    error=sup_c ||sum_s (Q_s-Qhat_s)^T E^T c f_s^T||F.

For a sufficient feature-uniform estimate only, if un-discounted unit kernels
are each approximated within eta, error<=C eta/gamma. The sufficient tolerance
is therefore eta=gamma(epsilon-delta_dense)/C, of order epsilon/n.
There may be sharper cancellation, but it has not been bounded uniformly.
Independent arbitrary feature tuples are never used to prove a lower.

Retaining H exact recent kernels gives tail<=C kappa_Q a^H/gamma. The accepted
H=O_c(n log n) is enough at fixed epsilon. This yields at most O(r log r)
relevant per-history templates, and preserves the accepted counted window
upper O(n^2 log n). A per-history Omega(r^2) REQUIRED-template assertion in
this same finite-error sense would conflict with that upper. Families of
histories have different quantifiers and may still carry larger joint geometry.

## 5. What happens to the proposed positive/negative directions?

**Positive:** O(r) active aggregate operators already exist exactly, but have
cubic explicit storage. No continuous quadratic recursive description was
derived. The strong correlation diagnostic neither constructs that description
nor bounds the coupled residual for all histories. Query-average SVD is only
a lower diagnostic, not a uniform-error upper.

**Negative:** The query metric alone permits r^2 finite-error operator
coordinates at the natural allowance. Actual gate-semigroup reachability of
that finite radius remains unproved. Algebraic matrix-span generation does
not supply it. No jointly robust Omega(n^2 log n) family was obtained.

Even an admissible r^2 operator section would not automatically yield the log:
if the source feature stays in one fixed public direction H, arbitrary actual
aperiodic gates have the exact selected-block recursion

    M_t=aG_t O_*M_t-1+alpha_t G_t,
    K ->E M_t K H,
    h_(t-1),source=alpha_t H.

It costs r^2 credit coordinates plus current h if needed, has delta_dense
actual error, and includes period-1. It is a restricted selected-block
control, not a complete-gradient solution. Independent feature directions
and their age-dependent coupling are essential to any additional lower.

## 6. Smallest remaining mathematical obstruction

There is no established smaller equivalent reduction of the general problem.
The concrete missing geometric estimate is the accumulation-aware JOINT query
width of ACTUALLY REACHABLE, feature-coupled aperiodic kernels, including their
finite-radius gate variation. An O(r) result with a counted continuous
recursive operator description would be sufficient for one upper route.
An actual robust operator section would advance the lower route, but extra
age/feature independence would still need proof before claiming the log.

The full-query metric and normalization are now explicit; merely hiding an
exact algebraic subspace cannot do the work. No basis-renewal, convex-packet
or ill-conditioned real-packing proposal is advertised as a solution.

## 7. Checks, records and recommendation

PROOF.md supplies all derivations, including exact aggregate counting,
perpendicular-subspace width, finite packing, admissible accumulation control,
tail budgeting and a finite-chart criterion translating query-composed
singular values plus mixed remainder bounds into genuine robust sections.
New lemmas require independent hostile review.

Manual algebra, units, coupling, endpoint/query domains, counts and finite
radius checks only. No tests or numerical experiment were requested or run.
GPU/CUDA time0; no model server, training or GAS-0 work. Routine administrative
CPU/wall time and RAM unprofiled. Original proofs/review outputs are preserved.

Exact source/manuscript hashes: PROVENANCE.json. State updates: Codex_Research.md
and SHARED_RESEARCH_MAP.md. The primary approximation-theory reference is
Pinkus's 1985 Springer book; the proof here is self-contained and makes no
new mathematical-novelty claim.

**Single recommended next theorem:** prove/refute a uniform finite-radius
joint-query width estimate for the actual coupled kernels, WITH counted
continuous operator structure; do not turn a pointwise O(r) direction count
into an uncounted-basis encoder. Stop this stage.
