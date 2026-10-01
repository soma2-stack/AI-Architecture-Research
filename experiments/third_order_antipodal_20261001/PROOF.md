# Odd antipodal certificate with full implicit third-order control

Notation and the fixed-h existence premise are the accepted stage-1 ones.
We prove the new remainder criterion, not accessibility/observability again.

## Scalar recurrence derivatives

Let a=Rh+Wx+b, p=RS+deltaR h+deltaW x+delta b. Entrywise h_new=f(a),
S_new=f'(a)p, f=tanh. For chart indices i,j,k, at frozen parameters:

    h_ijk_new = f' a_ijk + f''(a_ij a_k+a_ik a_j+a_jk a_i)
                 + f''' a_i a_j a_k.

    S_ijk_new = f' p_ijk
      + f''[p a_ijk+p_i a_jk+p_j a_ik+p_k a_ij
                         +p_ij a_k+p_ik a_j+p_jk a_i]
      + f'''[p(a_ij a_k+a_ik a_j+a_jk a_i)
                         +p_i a_j a_k+p_j a_i a_k+p_k a_i a_j]
      + f'''' p a_i a_j a_k.

Here a_i=R h_i+W x_i, a_ij=R h_ij, a_ijk=R h_ijk because chart history is affine.
p derivatives include the actual coupled deltaR h derivatives and deltaW x_i;
there is no independently selectable parameter-column injection assumption.

Writing H=tanh(a),

    f'=1-H^2, f''=-2H(1-H^2),
    f'''=-2(1-H^2)(1-3H^2),
    f''''=8H(1-H^2)(2-3H^2).

Interval enclosures of H and these polynomials give whole-box derivative bounds.
Absolute-value chain rules with upward arithmetic majorize every tensor component.
Initial h,S and derivatives are zero; induction in time proves the majorants.

## Exact hidden section and implicit derivatives

Let H(y,t)=h(x0+sigma B(y,t))-h0. Equal normal widths, eta_h<3/4, forcing
inclusion and nonsingular K_h give a unique fixed point y(t) with H=0 throughout
the closed tangent box. Uniform contraction gives Lipschitz continuity; H_y
is nonsingular throughout the box. The analytic implicit-function theorem gives
local smooth extensions near every section point, including boundary points.
Thus differentiation along interior segments and closed limits is legitimate.

Write w(t)=(y(t),t), v_i=D_i w, w_ij=D_ij w and w_ijk=D_ijk w. Then

    y_i = -H_y^-1 H_ti,
    y_ij = -H_y^-1 H''[v_i,v_j],
    y_ijk = -H_y^-1(H'''[v_i,v_j,v_k]
                  +H''[w_ij,v_k]+H''[w_ik,v_j]+H''[w_jk,v_i]).

w_ij=(y_ij,0) and w_ijk=(y_ijk,0). The exact componentwise inverse bound
(I-Eh)^-1 |K_h| controls H_y^-1. All third-derivative contractions include
the simultaneous normal/tangent cross terms, with no assumed negligible term.

For normalized sensitivity s(w(t)):

    D_ijk(s o w) = s'''[v_i,v_j,v_k]
        +s''[w_ij,v_k]+s''[w_ik,v_j]+s''[w_jk,v_i]+s_y y_ijk.

The final term and all three mixed Hessian terms are mandatory. Fixed parameter
RMS weights are constants in this differentiation.

## Antipodal remainder

Psi(t)=L s(w(t)), A=diag(a_i), Phi(z)=A^-1 K(Psi(Az)-Psi(0)). Let
C0=D_t Psi(0), E0>=|I-KC0|, e0_i=sum_j E0_ij a_j/a_i.
Let T3_abc bound |D_abc Psi| on the ENTIRE section. Define

    M3_i >= (1/a_i) sum_mabc |K_im| T3_mabc a_a a_b a_c.

For z in the cube, g_i(s)=Phi_i(sz), s in[-1,1], has |g_i'''(s)|<=M3_i.
Taylor expansion at zero with integral remainder gives

    g_i(1) = g_i(0)+g_i'(0)+g_i''(0)/2+R_plus,
    g_i(-1)= g_i(0)-g_i'(0)+g_i''(0)/2+R_minus,
    |R_plus|, |R_minus| <= M3_i/6.

The second-order terms cancel exactly; hence

    |Phi_i(z)-Phi_i(-z)-2(DPhi(0)z)_i| <= M3_i/3.

At a face |z_i|=1, |(DPhi(0)z)_i|>=1-e0_i. Therefore

    |Phi_i(z)-Phi_i(-z)| >= 2(1-e0_i-M3_i/6).

Define ell_tilde_i=(K L)_i/a_i. The accepted residual-safe query inequality
holds for arbitrary full supported sensitivity differences, including all
unselected coordinates:

    D_C >= mu_tilde_i |ell_tilde_i Delta s|.

The realizable 7/8-gate support metric is unchanged. Since h is exactly fixed,
the same future control gives that gate for both histories and its direct
parameter term cancels. Thus D_C>=2 beta3_i for antipodal pairs on face i,
beta3_i=mu_tilde_i(1-e0_i-M3_i/6).

If ALL beta3_i>epsilon, the accepted cube-boundary Borsuk-Ulam collision
argument gives k>=r for any continuous encoder answering every permitted late
query to uniform absolute error epsilon without external history.

This criterion concerns antipodal pairs only. It does not extend the stage-1
all-corner-pair finite-state argument. A passing6D result means at least six
continuous coordinates; it does not automatically mean64 finite memory states.
