# Robust-witness search

See REPORT.md, config.json and PREREGISTRATION.md. Final primary verdict and
all18 candidate comparisons are in summary.json/csv. Winners are frozen in
frozen_winners.json; proof conditions are in certificates/. Original archived
evidence is never overwritten. invalid_attempt1 preserves the parity defect.

Execution order (completed; do not rerun over outputs):

1. setup.py; test_search.py in the isolated CuPy venv; test_certificate.py on CPU.
2. search.py search; seal.py search; commit before confirmation.
3. search.py confirmation; seal.py winners; commit before certification.
4. certify.py on CPU; analyze.py; finish_records.py.

The isolated .venv is ignored. Install cupy-cuda12x[ctk]==14.2.0 only there.
CPU numerical/interval dependencies are inherited from the existing CPU
Python environment. Do not operate any model server or GAS-0.

No further research is run automatically.
