# Frozen 8D rigorous third-order antipodal certificate

## Result

**8D RIGOROUSLY CERTIFIED â€” INDEPENDENT REVIEW REQUIRED** at BOTH 192 and 256 bits. Same independent width-4
confirmation endpoint/T37/P24, epsilon=1/1000, parameter-RMS/input-SD
normalization, support-aware permitted queries, fixed-h and continuous encoder
contract. No candidate tuning, new history, 9D/10D, architecture or GAS-0 work.

Under the accepted cube-boundary antipodal theorem, any continuous no-replay encoder satisfying the unchanged permitted gradient-query contract needs k>=8 real coordinates on this section. This is not eight bits or 256 mutually separated grid states.

## Guaranteed face separations (256-bit run)

Every entry below is a WHOLE-FACE outward lower bound, not a midpoint sample.
Required strict separation is >0.002. The cubic penalty is subtracted from
beta; guaranteed separation is twice beta.

| Face | Guaranteed 2beta | Ratio to 2epsilon | Cubic penalty mu*M3/6 | M3 upper |
|---|---:|---:|---:|---:|
| 1 | 0.00251441072689798 | 1.25720536345 | 0.000469713387479 | 1.63197042325 |
| 2 | 0.00206985419852306 | 1.03492709926 | 0.000586172161638 | 2.16953585425 |
| 3 | 0.00246825175892404 | 1.23412587946 | 0.000386973381437 | 1.43226287534 |
| 4 | 0.00212103767568597 | 1.06051883784 | 0.000408274001993 | 1.66779408608 |
| 5 | 0.00240923469521947 | 1.20461734761 | 0.000241077965933 | 1.00053433255 |
| 6 | 0.00205813780521656 | 1.02906890261 | 0.000317562151472 | 1.41491829039 |
| 7 | 0.00204908651163035 | 1.02454325582 | 0.000181383974989 | 0.902462289707 |
| 8 | 0.00204890610576939 | 1.02445305288 | 0.00044448830022 | 1.81554545774 |

Weakest face: 8; separation 0.002048906105769395;
absolute slack 4.890610576939472e-05; relative slack
2.445305288%.

## Exact hidden section

Equal normal half-widths ah=0.0150915571609936.
Hidden contraction eta_h=0.0275170420688897, strictly below 3/4.
Forcing upper vector [0.002289888873436962, 0.004532670014380009, 0.011884575804712486, 0.006426658863595225].
Common forcing limit (1-eta_h)*ah=0.01467628214770949.
Local raw-history radius upper 0.09144065972573101 <=1.
Frozen rational K_hidden and K_selected are independently inverted; center
residuals are included. Uniform self-map/contraction gives the exact curved
fixed-h lift throughout the simultaneous eight-axis box.

## Frozen candidate and accepted method

Primary numerical screen c057e4e, dimension_8.json / query_svd / proxy,
not its larger direct-geometry winner. Candidate SHA256
c83a242f6de829542fcf57c7b98beae6fc90be079d479b169a624e832f27cd0c.
Pre-certification freeze commit dd70f482ce9662ed98235a48944fc84b83dd8b5d.
Amplitudes and all chart entries retain their exact binary64 rational values;
no 20-bit rounding or normal-amplitude inflation. Numerical chart() output L
is frozen with identity K_selected, and numerical inverse K_hidden is frozen.
Rigorous center residuals account for their inexactness.

The local reviewed_kernel.py is byte-identical to the accepted affine-tightened
kernel. Both W*B and W*x affine refinements, actual parameter injections,
all HH/HH3/HS/HS3 mixed terms, y^(2)/y^(3) and s_y*y^(3) are retained. The original
kernel's hard-coded '6D' reason is preserved in raw metadata and overridden
only in the new human-readable label; the generic r equations are unchanged.
Accepted proof and affine formulas are referenced by frozen source hashes;
no theorem or proof mathematics changed.

## Precision, arithmetic and checks

Fresh interval endpoint/box regeneration at 192 and 256 bits, with no reused
curvature outputs. Exact rational downstream replay; maximum beta precision
difference 2.00972e-58. All eight complete derivative arrays
compared, 71104 entries per precision.
Arrays bitwise identical: True.
Dyadic/transcendental intervals have the declared precision; positive tensor
majorants deliberately use the independently reviewed elementary upward
binary64 arithmetic. They are not 256-bit tensors or ordinary GPU estimates.

All 36 final checks pass; tests.json contains the synthetic tests.
Frozen inputs, numerical screen and previous 7D evidence remain unchanged.
There was no retuning, restart or fallback after official bounds.

## Resources and scope

One CPU thread. Measured CPU for setup, passed pre-official tests,
official runs and final checks: 75.750000s (1.262500min).
Separately charge 10 CPU-s for the failed pre-official
test/import process (conservative allowance, not a measurement). Budget-accounted
total is 85.750000s. The synthetic tensor-shape typo and pre-official repair
are preserved in preofficial_repair.json/FROZEN_INITIAL.json; frozen candidate
and reviewed kernel never changed.
Official wall time 77.514635s; complete timing components in
setup_resources.json/tests.json/result.json/checks.json. Peak process RAM
303.945312MiB. GPU/CUDA/own VRAM zero. Budget 1200 CPU-s, RAM 2GiB.

## Stop / next step

STOP. No 9D, 10D or architecture work. The strongest remaining uncertainty is
independent review of this new 8D candidate and its whole-box margin; the
result does not identify the model's maximum robust dimension. Recommend a
bounded independent hostile audit/replay before authorizing further work.

## Publication repair disclosure

The first frozen finalize.py could not parse its report string because a
triple-prime formula closed a triple-single-quoted string. No audit code or
scientific computation ran in that failed export. The frozen original remains
byte-identical. finalize_fixed.py differs ONLY by replacing that report-text
notation with y^(2)/y^(3). It then completed all 36 checks. The repair and
hashes are preserved in postofficial_export_repair.json. Separately charge
1 CPU-s for that failed export. No candidate, kernel, bounds or proof changed.
FINAL_AUDIT.json records publication CPU time and aggregate budget usage.
