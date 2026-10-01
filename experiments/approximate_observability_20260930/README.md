# Quantitative / approximate observability

Read REPORT.md for the outcome and PROOF.md for complete conditional arguments.

Classification: **ROBUST DIMENSION DEPENDS STRONGLY ON SCALE/HORIZON**.
Not a width-uniform finite-error lower bound or an architecture result.

Freeze6aff41c, implementationaf999ca. Accepted previous proofs and certificates
are read-only dependencies. source_hashes.json records their exact contents.

Reproduction: copy code/config only to a new sibling experiment directory
under experiments (preserve the original artifacts), then `python test_audit.py`
and `python audit.py` there. The runner refuses to overwrite spectra.jsonl. `finalize.py`
exports stored data. All computations CPU-only, one worker, no training.
Do not rerun automatically merely to change a result. New scientific scales
need preregistration before new measurements.

All old results and the premeasurement runtime-check failure are preserved.
Stop here pending independent review. GAS-0, Stage C and AMS v10 are excluded.
