# Joint anisotropic product certificate

The accepted accessibility, observability and isotropic finite-error theorems
are premises. This document proves only the new certificate and packing rule.
It does not change the physical normalized gradient-error contract.

## Coordinates and the object actually certified

Write sigma_x=sqrt(3/32) and D_theta for the diagonal matrix of archived
R/W/b group RMS values. The measured sensitivity is S_phi=S_theta D_theta.
The future gradient error is the Euclidean norm in these phi coordinates.
Input-history perturbations use unit input-SD coordinates. No singular value
or epsilon is rescaled after inspection of results.
All coordinate/reference normalization constants are evaluated at the frozen
model, not adapted to individual histories or grid points.

At the archived history X0, QR of J_h and SVD of
A_fiber=(J_S D_theta) N sigma_x supply normal directions B_h and tangent
directions B_t. Their 128-bit dyadic approximations are fixed constants.
They need not be exactly orthogonal or exactly in ker(J_h): the center and
nonlinear residual checks below include their actual errors. Write
X(y,t)=X0+sigma_x(B_h y+B_t t), |y_j|<=a_h,j, |t_i|<=a_i.
Define H(y,t)=h(X(y,t))-h(X0) and s(y,t)=vec_supported(S_phi(X(y,t))).

The certificate constructs H(y(t),t)=0 and proves that selected projections
Psi(t)=L s(y(t),t) contain the product
Psi(0)+prod_i[-rho_i,rho_i]. The full S tensor is a CURVED lift of that
projection product. It need not equal a flat S0+U diag(rho) box. This
distinction is essential; the query inequality below holds for arbitrary
unselected residual coordinates, so the weaker geometric claim suffices.

## Uniform directional and mixed curvature

All history coordinates vary simultaneously throughout the certified box.
Interval forward propagation encloses every tanh gate on that entire box.
Let a=Rh+Wx+b and denote derivatives in history directions k,l and one
parameter p by subscripts. Exact formulas are

h_k = f'(a) a_k,
h_kl = f'(a) a_kl + f''(a) a_k a_l,
S_p = f'(a) a_p,
(S_p)_k = f'(a) a_pk + f''(a) a_p a_k,
(S_p)_kl = f'(a) a_pkl
             + f''(a)(a_p a_kl + a_pk a_l + a_pl a_k)
             + f'''(a) a_p a_k a_l.

For tanh, f'=1-h^2, f''=-2h(1-h^2), and
f'''=-2(1-h^2)(1-3h^2). Recurrent a-derivatives include R times every
old derivative and the actual deltaR*h, deltaW*x, delta b injections.
The componentwise nonnegative recurrence includes ALL mixed pairs (k,l),
not just diagonal curvatures. Positive bounds use elementary binary64
operations rounded upward with nextafter. Every sum is explicitly ordered;
there is no BLAS reduction or inferred cancellation in a majorant.

The rigor model assumes correctly rounded IEEE binary64 elementary +,* and
conversion, checked against exact Fraction arithmetic, plus outward dyadic
interval arithmetic. Overflow/NaN invalidates a proposal, not the mathematics.
The Taylor exponential encloses its remaining tail; monotonic endpoint tanh
enclosures avoid a dependency blow-up. SVD midpoint values only initialize
coordinates, not the certificate itself.

## Constant-hidden-state section

Let K_h be a rational approximate inverse of H_y(0,0). An interval center
residual plus the uniform Hessian yields a nonnegative matrix E_h satisfying
|I-K_h H_y(y,t)|<=E_h throughout the box. Require ||E_h||_infinity=eta_h<1.
Use the full second-order bound on H(0,t) to obtain f_h>=|K_h H(0,t)|.
If f_h,j <= (1-eta_h) a_h,j, the map
y -> y-K_h H(y,t) is a contraction and maps the normal box into itself
for every t in the tangent box. Hence a unique y(t) exists there.

The absolute inverse is bounded by
|H_y^-1| <= (I-E_h)^-1 |K_h|.
The right side is calculated by exact rational inversion, justified by the
nonnegative Neumann series because ||E_h||_infinity<1. Thus
|y'| <= (I-E_h)^-1 |K_h| |H_t| = Gamma_bound.
Put V=[Gamma_bound; I]. Componentwise contraction of each uniform Hessian
with V on both indices bounds the implicit derivatives:
|y''| <= |H_y^-1| (|D^2 H| contracted with V,V),
|D^2 s(y(t),t)| <= |D^2 s| contracted with V,V + |s_y| |y''|.
This is the source of the mixed fixed-h curvature table. It includes the
normal compensator and cannot be replaced by independent axis scans.

## Anisotropic inverse-product certificate

The exact center selected derivative is interval-enclosed as
C0=L(s_t-s_y H_y^-1 H_t). Let K be its rational approximate inverse and
A=diag(a_i). Uniform projected mixed curvature yields a matrix E satisfying
|I-K D Psi(t)|<=E. Require
eta=||A^-1 E A||_infinity<1.

For a desired output difference w with |w_i|<=rho_i, the scaled Newton map
t -> t-K(Psi(t)-Psi(0)-w)
contracts in ||A^-1 t||_infinity and preserves the tangent box whenever
sum_i |K_ji| rho_i <= (1-eta) a_j for every j.
Banach's theorem therefore gives a history attaining EVERY point of the
projection product, with hidden state exactly unchanged.

The implementation proposes rho0_i=sigma_i a_i and multiplies by the exact
rational factor min(1,0.9 min_j[(1-eta)a_j/sum_i|K_ji|rho0_i]).
Its validity is in the verified inequality, not in treating sigma_i as an
exact singular value. There is no global sigma_min in this formula.
The scaled preconditioner controls cross-direction effects jointly; its
condition number is reported, not used to change the gradient norm.

## Directional future-query margin that survives residual coordinates

Let Gamma_q=(1/4)I+(5/8)11^T. Its columns have one gate 7/8 and other
gates 5/8, both rigorously inside sech^2([1/4,3/4]). R and W are invertible
at all archived witnesses. Thus these gates are realized by allowed one-step
future inputs at the fixed h. For the accepted q=1/sqrt(n) and
beta=max(1,||R||_F), actual adjoints are
c_j=R^T Gamma_q[:,j]/(sqrt(n) beta).
Define C_tilde=R^T Gamma_q.

Embed projection row L_i in its n-by-P supported tensor. Because C_tilde is
invertible, write L_i=C_tilde B_i, B_i=C_tilde^-1 L_i. For ANY sensitivity
difference DeltaS_phi, including arbitrary residual directions,
|<L_i,DeltaS_phi>| <= sqrt(n) beta sum_j ||B_i[j,:]||_2
                              max_j ||DeltaS_phi^T c_j||_2.
Therefore D_C(S1,S2)>=mu_i |Psi_i(S1)-Psi_i(S2)|, where
mu_i=1/(sqrt(n) beta sum_j||B_i[j,:]||_2).
The displayed mu_i is a rigorous lower enclosure, not a numerical estimate.
No cancellation assumption, full query ball, or Frobenius/sqrt(n) loss is
needed for this coordinate-specific joint inequality.

The future gradient includes direct parameter injection at the new step;
that term cancels between these histories ONLY because h is exactly equal.
Future query inputs are held fixed when differentiating the model parameters.

## Integer product packing

If two histories share one deterministic memory state, uniform absolute
error<=epsilon for every permitted query forces their query distance<=2epsilon.
Choose coordinate spacing delta_i=17epsilon/(8mu_i)>2epsilon/mu_i.
Inside [-rho_i,rho_i], exactly
N_i=floor(2rho_i/delta_i)+1
equally spaced positions beginning at -rho_i fit. These floors use exact
Fraction arithmetic, never rounded displayed radii. Every pair of different
product points differs by at least delta_i in some coordinate i, so the
JOINT dual query inequality makes their distance strictly >2epsilon.
Hence memory states>=prod_i N_i and bits>=sum_i log2 N_i.
An axis with N_i=1 contributes zero bits. The reported robust dimension is
the number of jointly certified axes with N_i>1, NOT a tangent rank.

This is a deterministic finite-state/no-replay, worst-case-query bound on
one local chart in the stated normalized units. It is not a byte/VRAM,
production-noise, optimizer, learning-advantage, or arbitrary-width result.
Failure of this sufficient certificate is not nonexistence of a larger region.

## Secondary projections and weak-axis comparator

Only after primary freezing, the finite query frame is used to choose different
output functionals. Let G=C_tilde C_tilde^T and Gram_ij=<U_i,G U_j> on supported
tensor entries. Midpoint initialization L_j=G sum_k U_k (Gram^-1)_kj is dyadically
rationalized. The actual center residual and mixed-curvature checks verify it;
no numerical Gram identity is assumed exact. The history axes are unchanged.
The same dual query formula recomputes mu_j for these new L_j. Consequently
rho_j is a projection half-range, not a silently rescaled physical tolerance.

For the weak-axis comparison only, the accepted global-majorant inverse
inequalities are applied to H plus the first r selected projections. The raw
global Hessian majorant, full-history basis infinity norm and output row-norm
bound are held UNCHANGED as r varies at each witness. A sparse rational SVD
block preconditioner is checked against the actual interval center; ignored
off-diagonal and tangent-normal entries are included in its residual eta.
With inverse norm M and common majorant Lambda, the comparator uses
a=min(1,(1-eta)/(2M Lambda)), rho=(1-eta)a/(2M), and safe half-range rho/2.
These are sufficient certified regions, not estimates of the maximal patch.
No accepted theorem is reproved. The separate sigma_min-squared models are
explicitly numerical counterfactuals, not interchangeable with these certificates.

General verification background: S. M. Rump, Verification methods: rigorous
results using floating-point arithmetic, Acta Numerica19 (2010),287-449.
https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf
This implementation does not use INTLAB and that reference does not verify
this code. The mathematical conditions and arithmetic assumptions above
must themselves be independently audited.
