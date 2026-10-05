# Single-block spatial write protocol

2026-10-04. Theory only. No independent notebook or historical proof edits.

Analytic target: a public nonuniform mask converts one private common-mode write into a zero-sum spatial mode. Restore high gates and damp the orthogonal complement. Investigate distinct Walsh masks so earlier writes remain zero-sum during later masks, with triangular readouts. Prove a JOINT cube boundary statement before calling any directions robust.

Definitions to freeze before checks: m tuples, same fixed survivor half for ALL stages; constant tuple labels carrying distinct Walsh bits; one fixed unit stationary-compensator parameter probe; stage e length ceil(3*2^(R-e)*n^(3/4)); common donor trace correction; mask length ceil(2000 log n); clear length 100000 ceil(n/m)ceil(log n); final public reset only. Scope R<=floor(log2(n)/8), n>=10^200.

Do not count interleaved masks as independent survivor blocks: each finished write occupies every survivor tuple, and all survivors are restored high. Readouts are orthogonal zero-sum patterns on the SAME full support. Distinguish growing R from superlinear D.

Checks use one Python process with numerical pools ONE, no workers, no CUDA/GPU imports or calls, observed threads<=8 and RSS<=160MiB guard. Small identities and scalar ledgers only. No large search or SVD. Stop on failed check or resource violation. Record tests separately from the proof.
