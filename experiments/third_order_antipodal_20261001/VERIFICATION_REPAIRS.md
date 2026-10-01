# Post-result checker repair (not a certificate-method change)

The first check_result.py run stopped at the archive-Git comparison because it
passed Windows backslash paths from BYTE_EXACT_ARCHIVE.json to Git's
colon-separated object lookup, which requires slash paths. A subsequent
diagnostic made the same mistake and produced archive_missing_before_repair.json.
That list is a preserved erroneous diagnostic, not evidence that files are missing.
The checker now converts path separators explicitly and diagnoses a missing
Git object before parsing its size. No frozen method, candidate, bound, result,
epsilon or original archived file was changed. Numerical and symbolic checks
before that archive step had passed, but the overall first checker did not finish.
Failed checker wall time was1.7063s; its CPU time was not persisted. Git-path
diagnostic subprocess CPU was not metered. These administrative costs are
reported separately from the measured experiment ledger.

The corrected Git-path check then exposed26 genuinely untracked ignored logs
(the kernel/cache log, numerical attacks, official and repair runner logs).
Their content was already included in the working-tree archive hash manifest
before the new run and was never changed. Commit c482a73 explicitly adds these
historical log files; the final Git-byte check targets that completed archive.
The earlier archive commits included all frozen certificate inputs/results but
omitted ignored logs. This is a post-result repository-packaging repair, not a
pre-run freeze claimed retroactively, and not a scientific method change.
The second failed checker had1.5774s wall time; CPU was not persisted.

An earlier development test pass, before the final s_y y''' assertion was added,
used5.25CPU-s,6.0479701wall-s and322928640peak bytes. The final test ledger alone
is included in immutable result.json; add this preliminary pass explicitly to
the total rather than silently undercounting it.
