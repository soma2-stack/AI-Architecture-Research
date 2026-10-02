# Append-only implementation repair record

## 1. NumPy boolean JSON serialization

After the seven width16 spectra completed, the finite-radius output writer
raised TypeError because np.bool_ is not standard-JSON serializable. The
numerical computation itself did not fail. All seven spectra, histories,
selection hashes and the failed execution log/stop record are preserved.

The frozen run.py and every mathematical/configuration input remain unchanged.
resume.py imports that frozen module and overrides only its JSON writer to
convert NumPy scalars using .item(). It resumes completed spectra without
repeating them, reruns the affected unsaved finite-radius calculation, and
carries the earlier CPU/wall/RSS accounting into the same hard budget.
No threshold, query, width, history, ranking or radius was changed. This is
an output bookkeeping defect, not evidence for or against operator dimension.
This repair is committed before collecting further official measurements.

## 2. Supporting cross-check writer

The separately written post-run cross-check encountered the same NumPy bool
serialization issue when printing its first successful check. Cast the
combined pass predicate to a Python bool. Preserve crosscheck_execution.log;
write the rerun to crosscheck_execution_v2.log. No official diagnostic source,
result, candidate or threshold changed. The supporting check is repeated
because its output was unsaved, not because the numerical outcome was unwanted.
