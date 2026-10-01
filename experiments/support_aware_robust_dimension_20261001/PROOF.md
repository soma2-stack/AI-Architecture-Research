# Continuous sections at finite gradient error

Accepted fixed-h product geometry and the independently reviewed query norms
are premises. No accessibility, exact-state, or isotropic theorem is reproved.

Let a product chart give a unique continuous curved lift s(w) at constant h,
with Ls(w)-Ls(0)=w in prod[-rho_i,rho_i]. The two accepted contractions imply
nonsingular H_y and selected derivative everywhere on their simultaneous
domain; their inverse functions give a C1 lift on the interior, continuously
extended to the closed target box. Retained coordinates vary while all other
projection coordinates are set to zero. Unselected FULL sensitivity coordinates
are not set to zero and are included in every derivative bound below.

## Residual-safe lower bound

For independent recurrence, every parameter p is owned by one state row i(p).
The exact allowed query metric is
D_C(DeltaS)^2=sum_p c_high,i(p)^2 DeltaS_i(p),p^2,
where c_high,i=sech^2(1/4) R_ii/(sqrt(n) beta). The permitted rational gate7/8
gives a lower weighted Euclidean norm. Thus the reviewed Cauchy-Schwarz bound
gives D_C>=max_i mu_i |Delta w_i| for every supported residual difference.
For dense recurrence use the accepted invertible finite query frame and its
full-tensor dual inequality. No off-owner restriction is imposed on dense.

Put w_i=rho_i z_i and b_i=mu_i rho_i. Then for retained r coordinates,
D_C(s(z),s(z')) >= max_i b_i |z_i-z'_i|
                    >= min_i(b_i)/sqrt(r) ||z-z'||_2.
This is a genuine finite-radius lower Lipschitz bound, not midpoint rank.

## Epsilon-essential dimension

Assume b_i>epsilon on every retained coordinate. Suppose a continuous encoder
to R^k, k<r, answered all permitted gradients to uniform absolute error epsilon
on this section. Restrict it to the cube boundary. Identify S^(r-1) with that
boundary by v->v/||v||_infinity, an odd homeomorphism. Borsuk-Ulam supplies
opposite z,-z with equal code (the case r=1 uses the two-point sphere).
Some |z_i|=1, so query distance is at least2min(b_i)>2epsilon. A common decoder
cannot approximate both answers within epsilon, by the triangle inequality.
Contradiction: k>=r under this continuous finite-dimensional no-replay model.
The same coordinate lower bound guarantees separation for any pair with
||z-z'||_2>2epsilon/m, where m=min(b_i)/sqrt(r), when that condition is nonempty.
The antipodal condition deliberately uses the cube boundary, retaining its
anisotropic geometry instead of forcing an inscribed Euclidean round ball.

This proves a lower bound only. r is not the number of finite states and a
large finite binary coding grid does not automatically satisfy this argument.

## Whole-section upper Lipschitz bound

Let the accepted chart variables be (y,t), normal then tangent. Whole-box
Hessian majorants give componentwise |Ds|<=|Ds(0)|+sum_k |D^2s| a_k. The
hidden implicit derivative is bounded by Gamma from the accepted normal
Neumann inverse. Hence |d s(y(t),t)/dt|<=B_s,t+B_s,y Gamma=:F.

With A=diag(a_i) and nonnegative E>=|A^-1(I-K D Psi)A|, ||E||inf<1,
|D Psi^-1| <= A(I-E)^-1 A^-1 |K|.
All entries of the right side are evaluated by exact rational arithmetic from
outward bounds. For z coordinates, multiply this inverse by diag(rho), keep
the retained columns, and multiply by F. Its Frobenius norm is an outward upper
bound M on ||Ds/Dz||2. Since the query adjoints have norm<=1,
D_C<=||DeltaS||F<=M||Delta z||2 on the convex target box. The straight segment
used here lies in TARGET coordinates, not the curved image in sensitivity space.
This proves the required global upper/lower Lipschitz pair (m,M).

## Scope

The result is epsilon-essential continuous coordinate dimension on one bounded
section. It is not a finite-bit theorem, global maximal dimension, compression
algorithm, learning advantage, production noise model, or architecture claim.
Vanishing radii can make a large topological chart irrelevant at epsilon. Failed
new products or noisy packing slopes cannot prove an upper dimension ceiling.
