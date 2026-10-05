# Resource policy: user gaming

User hard cap:8 CPU threads combined across this job; GPU usage ZERO.
Chosen numerical settings: one process, one numerical compute thread, no
workers/subprocesses/parallel test runner. Numerical and administrative calls
run sequentially. No other lane's processes are stopped or modified.

Before imports set OMP_NUM_THREADS, OMP_THREAD_LIMIT, MKL_NUM_THREADS,
OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS, BLIS_NUM_THREADS,
VECLIB_MAXIMUM_THREADS,TBB_NUM_THREADS to1; dynamic threading disabled;
CUDA_VISIBLE_DEVICES empty and NVIDIA_VISIBLE_DEVICES=void.

No PyTorch/CUDA/GPU library imports or GPU monitor. psutil checks actual total
process threads and RSS at each stage. Abort if threads>8, RSS>256MiB, or
child workers appear. Record peak working set. No higher-resource retry.

All tests are tiny identities or finite-radius error checks, not brute force.
