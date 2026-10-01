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

After both official replays passed, the documentation writer initially used
Windows' default cp1252 decoding on the UTF-8 proof-insertion text. It stopped
before shared-state/ledger edits. Explicit UTF-8 decoding repaired the writer.
The generated bounds were not rerun or changed; administrative compute is
included in the separately labeled estimate.

The initial unified patch used Windows CRLF output against the committed LF
proof. A read-only apply check exposed this formatting mismatch. The patch
is now saved as UTF-8 bytes with LF; its source remains the unchanged committed
proof. This was a documentation serialization issue, not a mathematical or
numerical discrepancy.
