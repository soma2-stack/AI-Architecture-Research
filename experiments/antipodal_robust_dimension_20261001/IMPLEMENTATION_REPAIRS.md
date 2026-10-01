# Implementation repair (stage 1)

## Defect

`antipodal_kernel.certify_antipodal` has early-return paths for invalid geometry:
- raw history outside the +/-1 domain;
- hidden_jacobian_dominance;
- hidden_section_box_inclusion.

These paths return a bare dict. The other paths return a tuple (result, curvature arrays). The frozen runner
`certify_official.py` always unpacked a tuple, so 48 of the 67 frozen candidates raised
`ValueError: too many values to unpack` before their failure reason was written.

## Why no certified result can be affected

The crash happens only on early returns. Every early return precedes any face-margin computation and is a failure by
construction. All 19 candidates that reached the face test completed normally in the original run. Their result files
are untouched and they are not rerun.

## Repair

- The original crashed result files are preserved unchanged in `results_attempt1_crashed/`, with the list in
  `crashed_ids.txt`.
- `certify_official.py` stays byte-identical. Its FROZEN.json hash still verifies.
- A separate `certify_official_repair.py` differs only in accepting a bare dict as (result, None) on the 192- and
  256-bit paths, and in skipping the curvature save when there is none. `diff --strip-trailing-cr` shows only those
  lines plus the docstring.
- The repair runner still asserts every FROZEN.json hash. It reruns ONLY the 48 crashed ids, with unchanged
  candidates, charts, amplitudes, epsilon and kernel.
- No threshold, amplitude, basis, projection or rule was changed. The defect was found after the official run started,
  from the 1-second error records.

## Observed cause of the early returns (diagnosis, recorded in the rerun)

The screening optimizer drives the hidden half-width a_h to the edge of the inclusion condition
|K_h H(0,t)| <= (1 - eta_h) a_h. The frozen rule rounds a_h DOWN to 2^-20, and the outward forcing bound slightly
exceeds the float proxy. Both push such candidates just over the edge. This is a candidate-construction weakness, not
a mathematical failure of the endpoints. It is disclosed, not retuned within stage 1.
