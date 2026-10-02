# Reproduction and evidence levels

This directory is append-only completed evidence. Do not run `independent.py
run` here again: it deliberately refuses to overwrite run.jsonl. Make a new
isolated dated theory directory for another replay and copy the source,
protocol/config and development tests there; freeze that replay separately.
There are no dependencies on any Claude Python module or numerical output.
Only source-provenance guards inspect the original handoff file hashes.

Python3.11 with NumPy2.4.6, SciPy1.17.1, mpmath1.3.0, psutil7.2.2; Torch is
needed only for development autograd and the separate adversary. Environment
CUDA_VISIBLE_DEVICES=-1 and four BLAS/OMP threads are imposed before imports.

Commands for CHECKS in this completed directory (they do not run official data):

    python tests.py
    python tests_adversary.py
    python tests_scoped.py

Exact scalar replays/summaries can write their own separately named replay
outputs if preservation is required; the originals are already saved.
Raw single_n*.npz contains generated actual R, affine operator, basis and
spectrum. screen_*.npz contains the history section bases, four coefficient
points, legal query witnesses and finite-difference operator spectrum. Config
and formulas reconstruct the full histories. Adversary NPZ files additionally
contain each selected joint sphere coefficient and its full operator spectrum.

FROZEN_SETUP.json is timestamped BEFORE primary results. FROZEN_ADVERSARY.json
is timestamped AFTER the primary screen and BEFORE its separate adversarial
outcomes; it freezes the selected primary NPZ hashes. The supplement is not
portrayed as prospectively independent of the primary observations.

CLAUDE_SOURCE_SNAPSHOT.zip preserves original handoff bytes for provenance
only, including its old numerical outputs. Those outputs are NOT independent
evidence for this work. PROVENANCE.json hashes both the snapshot and all own
created files. The original handoff was uncommitted at inspection; source
commit4a8a2dc identifies the repository base, not that uncommitted folder.

Evidence levels:

- Algebraic/topological arguments: VERIFICATION.md and SCOPED_THEORY.md.
  These are new author-derived arguments; scope and review requirements explicit.
- CERTIFIED scalar inequalities: rational exact arithmetic with explicit tails.
- HIGH-PRECISION NUMERICAL:80-digit analytic reference constants.
- NUMERICAL finite-radius diagnostics: all matrix/SVD/query/optimization output.
  No interval or full-sphere certificate is claimed for the growing-profile screen.
- Rejected statements/development failures: original failing logs preserved;
  corrections in REPAIRS.md. No threshold or official scientific setup altered.

The complete final decisions are in REPORT.md. No numerical count, sample or
optimization outcome is a theorem about arbitrary aperiodic robust dimension.
