# Exact transfer matrix and the unresolved joint minimum gain

All symbols and proofs are in PROOF.md. This file isolates the quantity that must be certified before multiplying donor signals.

## Epoch recurrence

For any fixed parameter probe matrix P, X=M P satisfies X_t=A_t X_(t-1)+G_t P, A_t=aG_t O_*. An epoch is the affine operator (Acal_e,Bcal_e), and composition is

    X_final=sum_e (product of ALL later Acal) Bcal_e.

An earlier donor change alters its Bcal and later propagators through the coupled gate/renewal dynamics. Acal and Bcal are private. They are not uncounted public routing coefficients. No first-insertion truncation is used.

## Cohort transfer

For stationary-compensator probe p_h, the exact reset observable on survivor cohort c is

    A_c,h(g)=a q_N [a sum_j K_c,j(g) J_(j-1)(g)+J_T(g)]p_h.

The donor-relative version subtracts D_N p_h. Every donor feeds the SAME vector renewal stream J. Cohorts select different temporal filters through their own gate words; there is no free E-by-C addressing matrix.

Two tuples with equal ENTIRE words have exactly equal private rows. A common last gate only multiplies their earlier difference and does not kill it. C counts public classes of whole schedules, NOT the number of high/low gate values at a single timestep. Parameter-dependent regrouping is not free public data.

## Correct differentiated transfer

For a history parameter theta_e,

    dX_t=A_t dX_(t-1)+dG_t(a O_* X_(t-1)+P).

The last donor correction has derivative

    dg_last=-kappa_* a d(kappa_prev)/(1+a kappa_prev)^2.

These derivatives include every feedback order. For a finite antipodal pair the exact identity is

    F(theta)-F(-theta)=integral_(-1)^1 DF(s theta) theta ds.

A minimum singular value at theta=0 is not a finite-radius lower bound. One needs a legal-query lower on this integral for EVERY boundary theta, including cross-epoch cancellations and trace corrections.

## Public query read-frame

With h_c physical sites per cohort, B=I-c vv^T, v_c=sqrt(h_c), has minimum eigenvalue >.97. This is well-conditioned PUBLIC reading of cohort modes. The actual coefficient is sigma sqrt(l)a/(n sqrt(n)); complementary legal signs supply s_gate>.17. The existence-of-sign lower is

    nu(A)>=sigma sqrt(l)a s_gate/(n sqrt(n))
                  sqrt(h_min)(1-c sum h_c)||X||F.

Frobenius norm occurs only inside a proved legal-query lower. It is not substituted for the permitted-query supremum. Residual bath/front/direct terms must be charged. For equal cohort sizes the certificate loses sqrt(C). Neither good conditioning of B nor rank of DF establishes robustness.

## Exact finite-error codes

- All private input rows belong to one PUBLIC subspace P of dimension q_P<=min(r,4m+4T+2).
- Fixed C whole-word survivor classes plus matched donor tail: mp+(C+2)q_P coordinates suffice for the COMPLETE final sensitivity up to the specified all-query fiber error.
- Without these classes: mp+(m+1)q_P is a general final code.
- Stationary/off-cycle private input quotient has only m+1 coordinates; all tuples and bath give code m+(m+1)^2. Fixed survivor classes/tail reduce it to m+(C+2)(m+1).

These are STATIC continuous codes, not O(n) streaming algorithms. Coordinates of every private row are counted. Public basis construction and supports are genuinely independent of private parameters.

## Single unresolved matrix problem

On a fiber fixing local direct code, Z_N and donor D_N, study the reachable matrix

    Vcal(g)=[V_c,N(g)-D_N(g)]_c

in its actual all-legal-query metric, with growing C. To surpass the accepted cheap one-slider result one must prove a jointly robust ball in this matrix family, or compress the family to O(n) coordinates. An ambient matrix ball, a full local Jacobian, or separately visible epoch axes is not enough. Moving cycle parameter columns or m>>sqrt(n) can escape the stationary-compensator code. This is the remaining obstruction.
