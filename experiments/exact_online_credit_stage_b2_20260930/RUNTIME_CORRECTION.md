# Stage B2 runtime correction — before corrected measurements

The first measured attempt (freeze1d34874) set Torch to one thread, but run.py
imported NumPy/SciPy before core.py set BLAS environment limits. A post-run DLL
audit confirms both OpenBLAS pools initialized24 threads. Thus the original
single-thread timing specification was violated. Parameters, derivatives, seeds,
data and float64 CPU execution were correct; no CUDA/GPU occurred. Whole-process
CPU meter included all threads, and was below the1800s cap. Its timing claims
are nonconforming. Preserve ALL first-attempt outputs at their existing paths.
No original raw records or configuration are rewritten/deleted.

Generic implementation repair: set CUDA/BLAS environment before any numerical
imports in entry points. Assert actual NumPy AND SciPy pool counts==1 using
OpenBLAS runtime API, not only torch.get_num_threads(). New regression unit test.
No model equation, seed, threshold, tolerance, algorithm, task, horizon or width
changes. Core/structures source copies and config remain byte-identical.

Corrected results go in corrected_single_thread/. Its config is an exact copy
of the first freeze. Commit/push this correction BEFORE corrected measurement.
The CPU cap1800 AND family-start cutoff1000 apply CUMULATIVELY including original
measurements, failed tests and analysis. Do not reset the budget for this repair.
All new measurements stop according to these same rules; preserve partial family
results if1000s start cutoff prevents full repetition. Primary conclusions must
use corrected artifacts; original family evidence is marked nonconforming runtime.

Optional archive lookup also corrected (matrices/ prefix). Independent post-run
comparison verified140 shared snapshots; original flags preserved. Finalization
had a metadata KeyError on the administrative reserve's missing job field;
fixed report generation only, CPU still charged, no ledger write on failed attempt.
No learning, GAS-0, GPU, Stage C or AMS v10.
