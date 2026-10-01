# General dense robust-credit scaling: partial theoretical resolution

**General quadratic-versus-cubic question remains open.** A new conditional
upper theorem resolves one important regime without new experiments.

At fixed epsilon=1e-3, bounded inputs, frozen group-RMS gradient units and
uniform ||R||op<=a<1, counted online factors provide O(n^2) approximate state.
Every cubic-dimensional antipodal section then has half-margin at most

    C_*/(1-a) * a^(ceil[r/(n^2+2n)]-1).

For r=nP this is O(a^(2n+O(1))). Hence nonvanishing cubic margin is impossible
IN THAT CLASS. This does not cover the accepted explicit exact-accessibility
family with ||R||op=1, or a_n approaching one.

No uniform quadratic lower bound is established. At each fixed n, accepted
exact results imply the full cubic lower bound below some positive epsilon_n;
their premises do not bound epsilon_n uniformly. A normalized small-R
counterfamily proves that the qualitative assumptions alone cannot guarantee
even positive robust sensitivity memory at fixed epsilon for delayed-head
queries. This is not an existential best-family impossibility result.

| Regime | Rigorous lower statement | Sufficient-state upper |
|---|---|---|
| General dense, fixed 1e-3 | No uniform quadratic lower proved | nP=2n^3+n^2 |
| General dense, epsilon<epsilon_n | nP, each fixed n | nP |
| Uniformly contractive, RMS units | Matching quadratic lower open | H(n^2+2n), H independent of n at fixed epsilon |
| Independent recurrence | Accepted width-4 local lower 8 | P_ind=n^2+2n exact traces |

All counts exclude supplied fixed h; add n when exact h must be stored.
The new theorem counts all retained derivative factors and injection
coefficients. It does not replay past transitions or claim fast updates.

**Next theorem needed:** a width-uniform antipodal fixed-h section of
dimension >=c n^2 and half-margin >1e-3 in the contractive normalized class
would close that regime at Theta(n^2). A >=c n^3 version outside uniform
contraction would establish cubic scaling for its specific family.

**Recommendation:** independent review of THEORY.md's factored-tail encoding
and exponential-margin corollary first. Do not resume 9D section chasing.

Resource use: documentation/proof reasoning only; no measured numerical
experiment, training, GPU/CUDA or new tensor allocation. No meaningful
experiment CPU/RAM measurement is claimed. Existing evidence, GAS-0 and
other lane notebooks were not modified.
