# Documentation-only clarifications to the frozen proof

Source: `experiments/anisotropic_robust_packing_20260930/PROOF.md` at
`1e4bf42dfa9f1a312d23b4a752738280d5861a4b`. The original file remains
unchanged. These paragraphs are insertion text for review, not a new theorem
or revised numerical certificate.

## Insert in “Constant-hidden-state section”, after the self-map condition

For this instantiated width-3 certificate all three normal half-widths are
equal: `a_h,1=a_h,2=a_h,3=1/8`. Therefore the normal box is the ball
`||y||_infinity <= 1/8` in the unweighted infinity norm. For fixed tangent
coordinate t, the mean-value estimate for `T_t(y)=y-K_h H(y,t)` gives
`|T_t(y)_j| <= |K_h H(0,t)|_j + sum_k E_h,jk |y_k|`.
Consequently `f_h,j + eta_h/8 <= 1/8` proves self-mapping of the complete
simultaneous box. This unweighted step relies on the equal instantiated
normal half-widths; it is not asserted for unequal normal widths.

The forcing bound uses `H(0,0)=0` and the explicit Taylor mean-value integral

`H(0,t) = H_t(0,0)t + integral_0^1 (1-s) D_tt^2 H(0,s t)[t,t] ds`.

The line segment `(0,s t)` lies inside the full box. Thus, componentwise,

`|H(0,t)_j| <= sum_i |H_t(0,0)_ji| a_i
                  + (1/2) sum_i sum_k HH_j,n+i,n+k a_i a_k`.

Multiplication by `|K_h|` produces the displayed forcing majorant f_h. Both
ordered mixed terms are included; their factor 1/2 comes from the integral.

The residual condition also implies `K_h H_y` is nonsingular at every point
in the box: its difference from identity has infinity norm below one, so a
Neumann-series inverse exists. Since both factors are square, K_h and H_y
are nonsingular. Hence a fixed point of `y-K_h H(y,t)` satisfies `H(y,t)=0`
exactly. In particular the contraction constructs a curved fixed-h section,
not merely a section with a small hidden-state residual.

## Insert in “Anisotropic inverse-product certificate”, before Banach conclusion

At every t in the tangent box the scaled residual satisfies

`||A^-1 (I-K D Psi(t)) A||_infinity <= eta < 1`.

Therefore `A^-1 K D Psi(t) A` is nonsingular by the Neumann-series criterion.
The diagonal A is nonsingular because its half-widths are positive; both K
and D Psi(t) are square. It follows that K is nonsingular. At the Banach
fixed point, `K(Psi(t)-Psi(0)-w)=0` therefore implies
`Psi(t)=Psi(0)+w` exactly. This establishes exact target attainment for every
point of the jointly certified projection rectangle, without assuming the
unselected sensitivity coordinates vanish or remain constant.
