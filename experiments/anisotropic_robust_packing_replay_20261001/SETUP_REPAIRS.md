# Pre-measurement replay-wrapper repairs

The first source-pinning attempt rejected byte inequality caused by Git's LF
versus working-copy CRLF conversion. Source snapshots still use exact git-blob
bytes. The manifest records both byte and text equality. No scientific input
was changed.

The first test execution (`tests.json`) had two jet-construction errors because
AST extraction omitted the original `@dataclass` decorator, plus one thread
check failure because the kernel imported NumPy before setting the one-thread
environment. The replay wrapper now preserves that decorator and sets the
environment before the first NumPy import. The successful repeat is recorded
separately in `tests_attempt1.json`. Both executions remain in the CPU ledger.

These are isolation-wrapper repairs, not changes to the frozen mathematics,
axes, amplitudes, constants, interval formulas, or certificate conditions.
No official certificate run had begun when these repairs were made.
