# Pre-freeze development corrections

2026-10-01: inspection caught an invalid mixed list/comprehension expression in
the initial draft of freeze.py's source-path list, before running that script or
collecting any official result. Replaced it with the intended explicit list.
This affected only setup-manifest construction, not mathematics, candidate
selection, interval bounds or thresholds. No official result existed.
