# Exact last-input elimination and radial third-order integration

This refines bounds, not the accepted accessibility, observability or topology
theorems. Parameters, histories, sections, units and future queries unchanged.

## 1. Exact fixed-h section and sensitivity (distinct derivatives)

Let D=diag(r), h*=the accepted endpoint hidden state, g*=1-(h*)^2,
v=h_(T-1), and U=S_(T-1). W is nonsingular. The last four normal directions
are last-input coordinate vectors, and all earlier normal entries are zero.
The existing whole-box certificate supplies a unique exact fixed-h lift.
Its final input must therefore be

    x_T = W^-1(atanh(h*) - D v - b).

Sensitivities are derivatives with respect to parameters holding the REALIZED
input history fixed. DO NOT differentiate this input construction with respect
to parameters. Substitute its value only AFTER the RTRL update:

    S_T[i,R_i]   = g*_i (r_i U[i,R_i] + v_i),
    S_T[i,W_ij]  = g*_i (r_i U[i,W_ij] + x_T,j),
    S_T[i,b_i]   = g*_i (r_i U[i,b_i] + 1).

These are identities for the original parameter sensitivities, not a new
gradient of a parameter-dependent data generator. Now differentiate with
respect to the tangent HISTORY coordinates t at frozen parameters. The
normalized coordinates have constant group RMS weights w_p. For a frozen row
ell=(K L)_i/a_i, the selected Phi coordinate is ell*s(t), up to a constant.
Because normalized U already includes w_p, define

    C_S[i,p] = ell[i,p] g*_(owner p) r_(owner p),
    C_h[i,k] = ell[i,R_k] w_R g*_k
        - r_k sum_(j,l) ell[i,W_jl] w_W g*_j (W^-1)_(l,k).

Bias has no extra v term. Then, up to a constant,

    ell*s_T(t) = sum_p C_S[i,p] (w_p U_p(t))
                     + sum_k C_h[i,k] v_k(t).

This exact affine combination holds for EVERY t in the simultaneous full
eight-axis box. Residual/unselected supported coordinates remain present in
the full sensitivity difference and the accepted query duality. C_h combines
signed terms before absolute values; interval coefficient enclosures contain
the true coefficients. All last-step implicit terms are eliminated by an
identity, not omitted. The result is architecture/chart specific; no claim
that every chart or architecture has such an elimination.

Thus full mixed third derivatives are bounded using the unchanged prefix
recurrence through T-1 and the coefficient upper bounds. All R/W/b injections
through the prefix remain. Normal directions do not affect that prefix.

## 2. Sharp gate bounds

For H=tanh(a), its first four derivatives are polynomials

    p1(H)=1-H^2,
    p2(H)=-2H+2H^3,
    p3(H)=-2+8H^2-6H^4,
    p4(H)=16H-40H^3+24H^5.

On a closed activation interval, the maximum absolute value of a polynomial
is attained at an endpoint or a critical point (a nonzero interior maximum
of |p| has p'=0; zeros cannot exceed a positive maximum).
Critical points:

    p1: 0;
    p2: +/-sqrt(1/3);
    p3: 0, +/-sqrt(2/3);
    p4: +/-sqrt((15+sqrt(105))/30),
        +/-sqrt((15-sqrt(105))/30).

Outward interval radicals enclose every root. Include any root enclosure
intersecting the activation interval; exclude only provably disjoint ones.
Evaluate polynomials with interval Horner arithmetic at endpoints/root
enclosures. Taking the minimum with the reviewed natural product bound is
valid because both independently upper-bound the same derivative. No point
float calculation or sampled root establishes these certified extrema.

## 3. Radial remainder

Let A=diag(a), z on the unit cube boundary, and
g_i(s)=Phi_i(s z)=ell_i*(sensitivity at t=s A z minus its center).
For |s|<=lambda, the prefix histories lie in the affine box |t_j|<=lambda*a_j.
Let M_i(lambda) bound |g_i'''(s)| there for ALL |z_j|<=1: contract every mixed
third-derivative upper bound with the ORIGINAL a_j, not lambda*a_j. The prefix
does not depend on the hidden normals. Existing full-box hidden inclusion
ensures these are histories on the SAME original exact section.

Integral Taylor remainder and odd cancellation give

    |g_i(1)-g_i(-1)-2g_i'(0)|
      <= integral_0^1 (1-s)^2 M_i(s) ds.

There is no missing factor2: each half has Taylor weight (1-s)^2/2, and the
two absolute remainder bounds add. For partition l_j=(j-1)/8,u_j=j/8,
M_i(u_j) applies to the whole jth radial segment on BOTH signs. Set

    w_j = ((1-l_j)^3 - (1-u_j)^3)/3,
    B_i = (1/2) sum_j w_j M_i(u_j).

The weights are exact positive rationals and sum to1/3. A constant M recovers
B=M/6 exactly. Each M_i(u_j) may be capped by the independently valid old
whole-section M3_i; this is a predetermined minimum of proven upper bounds.
At |z_i|=1 the unchanged center residual gives |g_i'(0)|>=1-e0_i, hence

    D_C >= 2 mu_i (1-e0_i-B_i) = 2 beta_i.

The same mu_i and arbitrary-residual-safe query inequality apply. If all
beta_i>epsilon, invoke the already accepted antipodal continuous encoding
argument for k>=8. No stronger bit/grid-state or global dimension claim.

## 4. Checks and uncertainty

Regenerate the accepted control and compare arrays. Prove root lists by
polynomial differentiation; synthetic interval checks at both precisions.
Cross-check the exact last-step identity numerically against direct frozen
RTRL, including off-center compensated histories. Verify all mixed tensors,
exact weight arithmetic and precision agreement. New computational refinement
still requires an independent implementation/proof audit after its result.
