# Independently derived common positive coordinates

Author derivation, independent review pending. This note expands PROOF.md (8).

## Four-state chronological subsystem

The two equally gated high survivor components are equal for an idle-donor impulse. Collapse them to H, with combined weight 2 mu. Normalize each homogeneous step by a g_H. In order (D,I,H,bath):

    W=(mu,mu,2mu,w_b), gamma=4mu+w_b, delta=gamma-1,
    A_t=diag(d_D,d_I,1,d_b,t) (I-1 W^T).

Here d_D=g_L/g_H, d_I=g/g_H, d_b,t=q_t/g_H. The positive-coordinate map, in order (P,r_D,r_I,r_b), is

    T = [ mu  mu  2mu-1  w_b ]
        [  1   0    -1    0  ]
        [  0   1    -1    0  ]
        [  0   0    -1    1  ].

Its determinant is delta>0. It becomes ill-conditioned as n grows; it is a proof coordinate system, not a numerical memory implementation.

Define

    B_t=mu(1-d_D)+mu(1-d_I)+w_b(1-d_b,t).

Direct multiplication gives T A_t = M_t T, with

    M_t = [ B_t-delta  mu d_D  mu d_I  w_b d_b,t ]
          [  1-d_D       d_D      0         0    ]
          [  1-d_I        0      d_I        0    ]
          [  1-d_b,t      0       0       d_b,t  ].

Every entry is nonnegative, since B_t-delta>.0006. This is a COMMON cone: no eigenbasis depends on q_t and no matrices are required to commute. Therefore

    T A_t ... A_s = M_t ... M_s T

for the genuine chronological product. An idle impulse has (P,r_D,r_I,r_b)=(mu,0,1,0), all nonnegative. At the next step its high value is H_next=-P. At every later step H remains nonpositive.

The inverse relation is H=-U, U=(mu r_D+mu r_I+w_b r_b-P)/delta. Alternatively retain U as a redundant variable with U_next=P. This redundant realization is useful for the rational checks.

## Forced source sign

For the five-state forced system let S=W_5^T z, with W_5=(mu,mu,mu,mu,w_b), and direct forcing (s,-s,0,0,0). Let high gate g_H apply to the two survivor components. Exactly:

    S_next = a(g_H-sum_i w_i g_i) S
           + a sum_nonH w_i(g_i-g_H) z_i
           + mu s(g_L-g_H).

The cone z_D,z_I,z_b>=0, S<=0 is invariant. The bath deficit signs the first coefficient; the remaining terms are nonpositive. Thus the idle-gate derivative injection a(z_I-S) is nonnegative. Variation of constants with the chronological Green function above proves beta_5'(g)<=0 for every changing q word.

## Full system distinction

The complete corridor has an exceptional front. Its aggregate rho cannot be omitted in an exact reduction. The cone signs only the auxiliary recurrence obtained by dropping rho, while retaining q_t exactly. PROOF.md (10)--(14) bounds the full-minus-auxiliary error uniformly, then transfers the finite read margin. No exact monotonicity claim for the full front-inclusive trajectory is made.

The saved SymPy check verifies both identities as zero symbolic residuals. Rational changing-q tests independently reproduce the two coordinate evolutions. These checks support the hand derivation; they do not replace it.
