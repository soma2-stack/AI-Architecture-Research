"""Run a script and append CPU/wall/peak-RSS (Linux) to outputs/compute.txt."""
import resource, subprocess, sys, time
script, out = sys.argv[1], sys.argv[2]
t0 = time.perf_counter()
with open(out, "w") as fh:
    subprocess.run([sys.executable, script], stdout=fh, check=True)
r = resource.getrusage(resource.RUSAGE_CHILDREN)
with open("outputs/compute.txt", "a") as fh:
    fh.write(f"{script}: cpu_user={r.ru_utime:.2f}s cpu_sys={r.ru_stime:.2f}s wall={time.perf_counter()-t0:.2f}s peak_rss={r.ru_maxrss/1024:.1f}MiB\n")
