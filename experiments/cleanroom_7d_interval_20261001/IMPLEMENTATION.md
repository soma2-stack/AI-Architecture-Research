# Derivation and arithmetic contract

A multi-index alpha represents the Taylor coefficient D^alpha f / alpha!.
The convolution coefficient (AB)_alpha is sum_{beta+gamma=alpha} A_beta B_gamma;
there is no extra combinatorial factor in coefficient coordinates. Expand
f(a0+A) and f'(a0+A)p and take positive majorants term by term. This yields
the complete second/third derivative rules in the source proof, including
the repeated-index multiplicities and fourth tanh derivative. Final tensor
entries multiply by alpha! and include all ordered permutations.

Each nonnegative bound is a binary arbitrary-precision libmp number. Every
addition, multiplication, division and square root rounds toward +infinity.
Signed point/box values use mpmath.iv, with directed lower/upper endpoints.
Its exp interval uses monotonicity and floor/ceiling rounded endpoint exp.
The new engine stores exact dyadic endpoints in output; decimal displays and
binary64 arrays are summaries. Mathematical validity depends on these
directed library routines, not on precision agreement alone.

Let E >= |I-K_h H_y| over the complete simultaneous box. Invert I-E exactly
as a rational matrix, verify nonnegative inverse, and round its positive
entries upward. With ||E||_infinity<1, Neumann's series gives
|H_y^-1| <= (I-E)^-1 |K_h|. Rational nonsingularity of K_h is also checked.
The forcing bound follows the mean-value/Taylor formula at y=0. Because all
normal widths equal a_h, forcing_i <= (1-eta_h)a_h implies the uniform
infinity-norm self-map. Contraction gives the fixed-h section, not a linear
tangent approximation.

For V=(Gamma;I), W2=(y2;0), implicit derivative bounds are
y2 <= InvBound H''[V,V],
y3 <= InvBound (H'''[V,V,V]+H''[W2,V] with all 3 permutations).
The sensitivity third derivative includes the analogous 3 Hessian terms and
the full sensitivity-normal derivative times y3. Preconditioning is the
frozen K, not a new inverse chosen for these outputs.

Support query inequality uses each parameter column's unique state owner.
For ell=(KL)_i/a_i, mu=(7/8)/(sqrt(n*max(1,sum Rdiag^2))*
sqrt(sum ell_d^2/Rdiag_owner(d)^2)). Compute a conservative lower mu through
upper denominator. This bound applies to arbitrary residual supported
coordinates. Future gate 7/8 is realizable, and fixed h cancels direct future
parameter injections. The proof's antipodal Taylor/topology step is retained.
