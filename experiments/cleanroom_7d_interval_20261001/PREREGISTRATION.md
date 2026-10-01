# Second interval implementation: frozen 7D replay

Prospective scope: only the rational candidate copied from
`experiments/rebalanced_7d_section_20261001/candidate.json`, SHA-256
87895c3f3742b9a97e51eced5f9d1cf0606103290cedac4c2b0b224977c63f82.
Independent recurrence, n=4, T=37, P=24, seven tangent axes, epsilon=1/1000.
No candidate selection, optimization, amplitude change, new witness or 8D work.
All frozen numerical data, including both preconditioners, are inputs.

## Independence and chronology

Implement from third_order_antipodal_20261001/PROOF.md and
rebalanced_7d_section_20261001/PROOF_AFFINE.md. Do not import/copy their engines,
interval classes, jet helpers, tensor contractions or tests. Use mpmath/libmp
192/256-bit directed rounding, rather than the former dyadic interval engine
and upward binary64 majorants. Propagate symmetric multivariate Taylor
coefficients by polynomial convolution, rather than the former explicit
ordered-index chain-rule tensor implementation. Independently implement
implicit contractions and rational inverse checks.

The author previously implemented the accepted certificate and knows its
formulas and headline values. This is a separate software implementation and
backend, not a blinded independent author. mpmath is a remaining trusted
numerical dependency. Signed interval polynomials and positive upper bounds
must enclose exact derivatives; high precision alone is not a certificate.

Freeze source/config/tests before official replay. Development tests use
synthetic inputs only. Do not read original generated derivative arrays until
both new precision outputs have been saved. Comparison cannot tune the method.

## Frozen method

The chart is x=x0+sqrt(3/32) B w. Normalize each sensitivity column by the RMS
of its original parameter group R/W/b. Keep deltaW*x and deltaW*dx in all
parameter derivatives. Compute signed W*x0 and W*Btilde before taking absolute
values: these are the two reviewed affine tightenings.

Enclose monotone tanh by separately enclosing its endpoint values through
exp(2a). Evaluate derivative polynomials f',f'',f''',f'''' by outward interval
arithmetic, with the conventional exact interval square for H^2. Majorize
Taylor coefficients of h and S=f'(a)p through degree 3. For a zero-constant
increment A, h coefficients use f'A+f''A^2/2+f'''A^3/6; S uses the product
p*(f'+f''A+f'''A^2/2+f''''A^3/6). Convert coefficients to derivative tensors
by the multi-index factorial. All 11 normal/tangent coordinates participate.

Use the proof's full fixed-h inverse, forcing, implicit y'', y''', and
s_y*y''' terms. Calculate center residual, M3, support-aware query margins,
and beta=mu*(1-e0-M3/6) with outward arithmetic. Check frozen K_h/K exactly
nonsingular, hidden inclusion, raw domain, query realizability and all seven
beta>epsilon. Equal normal widths are preserved. No theorem change.

## Comparison rules and stopping

Compare all eight arrays HH, HH3, HS, HS3, y2, y3, fixed3, selected3 and
all scalar intermediates. Report absolute/relative differences, extrema and
indices. Target agreement is 1e-10 relative (absolute 1e-14 near zero), allowing
the new directed high-precision path to tighten accumulated binary64 rounding.
A different valid interval expression may produce a different enclosure;
report it explicitly rather than force equality. Any failed proof inequality,
unexplained material array discrepancy, source mutation or incorrect test
stops the task. Never adjust data/constants in response.

Check 192/256 agreement, nearly-tight entries, face 1 decomposition, and an
independent high-precision scalar path for sensitive margins. Save exact
dyadic bounds as compressed JSON, plus upward binary64 summaries for comparison.
Compute uses CPU only, one process/thread, no model servers. Resource ceiling:
45 measured CPU minutes for this tiny replay, stop if exceeded. Record CPU/wall,
peak RAM and zero GPU use. Stop after the replay; any 8D–24D feasibility screen
requires a later task.
