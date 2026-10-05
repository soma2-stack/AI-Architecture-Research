# Gaming-safe compute policy

Owner limit: eight CPU threads TOTAL; GPU prohibited.

This stage uses ONE numerical Python process and ONE numerical thread.
Before importing numpy/mpmath, force:

    OMP_NUM_THREADS=1
    MKL_NUM_THREADS=1
    OPENBLAS_NUM_THREADS=1
    NUMEXPR_NUM_THREADS=1
    VECLIB_MAXIMUM_THREADS=1
    BLIS_NUM_THREADS=1
    TBB_NUM_THREADS=1
    OMP_DYNAMIC=FALSE
    MKL_DYNAMIC=FALSE
    CUDA_VISIBLE_DEVICES=
    NVIDIA_VISIBLE_DEVICES=void

No PyTorch, CUDA, GPU numerical library, inference, multiprocessing, worker
process, parallel test runner, or GPU monitor is used. No other research
process is killed or suspended. Checks use small arrays and scalar arithmetic.

threadpoolctl is not installed and is not installed for this stage. Environment
limits are set before imports, and actual process threads are recorded.
psutil records total process threads and RAM at every instrumented phase.
Abort at >8 process threads or >256 MiB working set. No retry with more
resources. Computation is secondary to the analytic proofs.
