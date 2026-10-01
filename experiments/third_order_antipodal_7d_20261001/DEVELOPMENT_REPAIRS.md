# Pre-freeze implementation record

Before any new numerical candidate scores or official bounds were collected,
the first test invocation failed during import because `select.py` shadowed
Python's standard-library `select` module. Renamed the new wrapper `choose.py`.
No historical file, accepted kernel, mathematical rule, or input was changed.
The next invocation passed all 12 tests. Reserve 5 CPU seconds in the final
ledger for this failed startup and small uninstrumented development commands;
reported measured CPU is distinguished from this allowance.
