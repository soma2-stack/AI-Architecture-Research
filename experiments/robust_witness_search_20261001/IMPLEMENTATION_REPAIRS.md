# Execution defects preserved

The first Phase-A search mutated its local X/ids variables by appending adaptive
histories. The following independent model inherited that augmented local
array, instead of starting with its own fresh copy of the paired frozen pool.
This contaminated resource parity (independent initial count8896 versus8000).

The complete first attempt is preserved as invalid. No confirmation scores had
been opened. The driver now obtains a fresh X/ids copy inside EACH model loop;
an added unit test explicitly simulates appended adaptive data and checks that
the next model receives exactly the original8000 IDs and values.

The protocol, primary objective, epsilon, pool/split hashes, data domain,
architecture/parameters, optimization strategy and per-model valid-attempt
budgets are unchanged. Both models rerun from scratch under that corrected
bookkeeping, rather than retaining a favorable result from the invalid attempt.
All invalid compute is still charged in resources.jsonl and the shared ledger.

The initial fixed-hidden-frame unit check used pool_n3 history0, which belongs
to the confirmation split. It tested only a nullspace residual and positive
query margins; no primary/packing score was computed or inspected, and the
objective was already specified. That test now uses the dedicated development
RNG instead. This prior low-level diagnostic exposure is disclosed; history0
cannot be described as untouched if it becomes the selected confirmation
winner. No candidate is replaced or objective changed to hide this anomaly.
