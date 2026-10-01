# Exact affine-combination majorant refinement

This is a preregistered refinement of a triangle bound in the accepted kernel,
not a new antipodal theorem. All reviewed third-order/implicit formulas apply.

At fixed model parameters, the affine history chart is
x_t=x0_t+Btilde_t w, Btilde=sqrt(3/32) B, |w_k|<=a_k.
Define exact coefficients C_t=W Btilde_t and v_t=W x0_t.
Then W x_t=v_t+C_t w. Outward interval arithmetic encloses each C_ik and v_i.
Writing r_i=sum_k sup|C_ik| a_k gives
W x_t in [lower(v_i)-r_i,upper(v_i)+r_i].
The preactivation enclosure is R h_prev+b plus this interval. This keeps linear
input correlations that were lost in separately bounding each x_j before W.

For chart derivatives, D_k(W x_t)=C_ik exactly. Thus
|D_k a_i| <= sum_j |R_ij| |D_k h_prev,j| + sup|C_ik|.
This replaces the looser sum_j |W_ij| sup|Btilde_jk|. All higher direct chart
derivatives of W x_t vanish because the history chart is affine.

Crucially W is only fixed for differentiation with respect to w. Parameter
sensitivity is still taken with respect to independent original parameters:
deltaW x_t and deltaW D_k x_t remain in p and its derivatives, using the original
raw input intervals and Btilde entries. They are NOT replaced with zero or
discarded. Likewise deltaR h and its derivatives remain unchanged.

Outward C and v enclosures, positive upward arithmetic for sums/products, and
the same tanh interval gate polynomials establish valid |h''|,|h'''|,|S''|,|S'''|
majorants by the accepted induction in time. All normal-tangent and tangent-
tangent terms, y'', y''' and S_y y''' remain in the accepted contractions.
Rational inverse and fixed-h inclusion conditions are unchanged. Query metric,
7/8 realizability margin, epsilon, and topology step are unchanged.

The local generated source is checked against the accepted source: exactly two
substitutions, preserving every other line. A passing result should still have
independent review of this explicit refinement and its implementation.
