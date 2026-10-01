# Anisotropic robust packing

Read REPORT.md for the complete result and PROOF.md for the new joint
certificate. Classification: ONLY A FEW ROBUST DIRECTIONS SURVIVE.
No learning/model server/GPU/GAS-0 run occurs in this directory.

Primary protocol config.json is frozen at72fa7aa. PRIMARY_FROZEN.json hashes
the SVD results before secondary work. Raw proposals and the incomplete initial
campaign are append-only. Both original campaigns remain separately identified.

Files:
- results_svd.json / verification_svd.json: primary selected regions/replay.
- results_frame.json / verification_frame.json: declared secondary projection.
- certificate_*.json: exact fractions, all mixed-curvature and residual bounds.
- basis_*.json / spectra.csv: raw/scaled spectra and exact rationalized axes.
- summary.json: side-by-side packing, radii, margins and error curves.
- directional_audit.json: every axis and diagnostic failure attribution.
- weak_axis_certificates.json: rigorous weakest-tail/global-majorant removals.
- weak_direction_diagnostics.json: distinct numerical sigma-squared models.
- reconstruction_checks.json: numerical reconstruction, NOT the certificate.
- tests.json / final_checks.json / source_hashes.json: validation/provenance.
- resources.json / cpu_ledger.jsonl: all attempts and resource charges.
- RUNTIME_CORRECTION.md: preserved implementation/output failures.

For authorized reproduction, use a NEW isolated directory with the same
config/source and archived witnesses; do not delete these outputs. Order:
test_engine.py, engine.py svd, verify.py svd, freeze_primary.py, commit freeze,
engine.py frame, verify.py frame, analysis.py, reconstruct.py,
weak_certificates.py, final_checks.py. Frozen output files refuse overwrite.
No new witness or epsilon selection is permitted. End after certification.
