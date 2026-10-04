# Resource policy

User maximum: eight CPU threads TOTAL for this job; GPU/CUDA zero. This stage uses one numerical process at a time, no worker pools, and numerical library limits of one thread. Repository reads and writes are sequential with numerical work. No subagents or background helpers are launched. The user's other applications are not controlled.

Before numerical imports set OMP_NUM_THREADS, OMP_THREAD_LIMIT, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS, BLIS_NUM_THREADS, VECLIB_MAXIMUM_THREADS, and TBB_NUM_THREADS to 1; disable dynamic and nested pools. Set CUDA_VISIBLE_DEVICES empty and NVIDIA_VISIBLE_DEVICES=void. No GPU library is imported. Record total observed Python process threads including runtime/helper threads, not only BLAS limits.

Hard stop: >8 threads, a child process, or >160 MiB process working set. No retry with increased resources. Small computations support identities and can falsify them; they do not certify asymptotic robust dimension.
