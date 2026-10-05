# Monotonicity of the idle-donor overlap

2026-10-04. The intermediate band is closed. No third channel.

## Result

On the bath-inclusive reduced system, for every idle donor gate
`g in [0.9992, g_H]` and every public gate `q in [0.99, 0.9992]`,

```text
d beta / dg <= 0.
```

The overlap is therefore minimized at `g = g_H`, where the zero-sum projection theorem gives

```text
Omega(g) >= kappa/6 - 16000 n/M.
```

For `n >= 10^{200}` the error is `< 10^{-47} kappa`, and the existing square is a genuine `D = 2` section. The uniform legal-query margin on the boundary of `[-1,1]^2` is `> 0.009`. The energy remains `< 8 n^{5/8}`.

## Variation of constants

The reduced step is affine, `s |-> A(q) s + b`, and `b` does not depend on `g`: the idle donor has zero probe injection, so `g` multiplies a source-free row. Differentiating the trajectory gives

```text
d_{t+1} = A(q_t) d_t + pre_t e_{D2},
pre_t = a (Y_{D2} + h sigma)_t,
d_T = sum_{k < T} Phi(T, k+1) (pre_k e_{D2}).
```

`Phi` is the time-ordered product of the `A(q)`'s. The active-survivor component is

```text
d Y_{S1} / dg = sum_{k < T} pre_k G_{T-1-k},
G_m = (Phi_m e_{D2})_{S1}.
```

Two facts give the sign: `pre_k >= 0`, and `G_m <= 0`.

## The Green's function is nonpositive

For a frozen `q` the map is `A = D + r sig^T`, with `D` diagonal and every entry of `sig_i r_i` strictly negative (`-c` on private sites, `alpha a q < 0` on the bath). The secular function

```text
f(lambda) = sig · (lambda I - D)^{-1} r
```

therefore has negative residues at the diagonal poles. For nonreal `lambda = x+iy`,

```text
Im f(lambda) = -y sum_i |sig_i r_i| / |lambda - d_i|^2,
```

so `Im f != 0`. Every eigenvalue is real.

`S1` and `S2` share the diagonal entry `d_S = a g_H`, which is strictly larger than `a g`, `a q`, and `a g_L` on this band. The antisymmetric vector `e_{S1} - e_{S2}` is an exact eigenvector of eigenvalue `d_S` and is never excited by a symmetric impulse on `D2`. In the symmetric subspace there is exactly one eigenvalue `lambda_+` in the interval `(max(a g, a q, a g_L), d_S)`, because `f` is strictly decreasing from `+infinity` to `-infinity` there and the equation `f(lambda) = 1` has one root. There is no eigenvalue above `d_S`: for `lambda > d_S` every secular term is negative, so `f(lambda) < 0`.

Any eigenvalue `<= -1/2` would have `f(lambda) < 1` for `n >= 10^6`, because each denominator is at least `1.4` and the total numerator mass is at most about `|alpha| + O(n^{-1/2})`. Thus every other eigenvalue satisfies `|lambda| < lambda_+`.

Normalize right and left eigenvectors by `v_i = r_i/(lambda - d_i)` and `w_i = sig_i/(lambda - d_i)`. Then `w·v < 0`, and the `S1` residue of the impulse `e_{D2}` has the sign of `1/((lambda - d_S)(lambda - a g))`. That product is negative only for `lambda_+`. Every other residue is nonnegative. Their sum equals the time-zero `S1` component, which is `0`, so the dominant residue equals minus the sum of the others.

Hence for `t >= 1`,

```text
G_t <= |amp_+| (-lambda_+^t + nu^t) < 0,
```

with `nu < lambda_+`, and `G_0 = 0`. The secular gap is uniform for every frozen `q` in `[0.99, 0.9992]`. The `S1` update itself, `u_{S1}' = a g_H (u_{S1} + h sigma)`, does not use `q` except through `sigma`, and the same residue comparison applies at every frozen value the public gate takes.

## The source is nonnegative

On the forced trajectory the coordinates

```text
Q2 = -(Y_{S1} + h sigma),   P = Y_{D2} + h sigma,
Y_{D1}, Y_{S2}, Z
```

stay nonnegative and satisfy `Q2 >= Y_{S2}`. The next pre-gate input `P'` has numerator, over the negative denominator `2 c h - 1`, equal to

```text
c_Q (Q2 - Y_{S2}) + c_P P + c_1 Y_{D1} + c_Z Z + c_iota iota,
```

because the coefficients of `Q2` and `Y_{S2}` are exact negatives of each other. For `n >= 10^{200}` and gates in the legal ranges, every one of `c_Q, c_P, c_1, c_Z, c_iota` is negative. Each variable in the display is nonnegative, so the numerator is nonpositive and `P' >= 0`.

The ordering `Q2 >= Y_{S2}` is preserved because only `S1` receives the direct injection `-iota`. Each step widens `Q2 - Y_{S2}` by a positive multiple of `iota`, while `h sigma` remains smaller than that injection. Thus `pre_t = a P_t >= 0` for every `t`.

## The bad term

The term `2 a (g - g_H) n_2` is nonpositive, and a cone that treats `n_2` as an independent coordinate cannot absorb it. On the forced trajectory that term is not independent. Variation of constants writes

```text
n_2(T) = - d Y_{S1}/dg = - sum_k pre_k G_{T-1-k}.
```

Every `pre_k` is nonnegative and every `G` is nonpositive, so `n_2(T) >= 0` and `d Y_{S1}/dg <= 0`. The bad term is the survivor piece of this same expansion; once the source and the Green's function are signed, it cannot flip the overlap derivative.

## Conclusion for the square

`beta(g)` is minimized at `g = g_H` on `[0.9992, g_H]`. The matched history contributes `-kappa/2`. The high-gate idle history contributes `-kappa/3` up to the complement `e` with `||e|| <= 16000 n/M`. Therefore

```text
Omega(g) >= kappa/6 - 16000 n/M
```

for every idle gate in the band, and the proved `kappa/4` geometry remains available below `0.9992`. Every boundary point of `[-1,1]^2` has one coordinate at absolute value `1`, so one channel is a matched-versus-low pair. A legal one-step query supported on that channel's survivor block converts a gap of `kappa/6` into

```text
nu > 0.009 > 0.002.
```

Trace corrections, the common endpoint, and `||X||_2 < 8 n^{5/8}` are unchanged. This is one two-dimensional section. It is not a license to add a third channel, and it is not `D = omega(n)`.
