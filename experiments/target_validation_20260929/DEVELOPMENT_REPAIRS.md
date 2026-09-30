# Development repairs (before official seeds)

1. Initial unit validation: psutil on Windows requires a string rather than
   pathlib.Path for disk_usage. Passed str(ROOT), without changing any data,
   model, metric or threshold. The failed validation's measured CPU is retained
   in cpu_ledger.jsonl. A subsequently attempted development command failed at
   the same hardware check before Meter construction; conservatively charge
   five CPU seconds for that unmetered command. Charge another five CPU seconds
   for the initial Python dependency/CPU-build probe. These are explicitly
   upper-bound reservations, not measured process CPU. No official seed was read.
