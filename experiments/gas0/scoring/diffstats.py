"""Compare changed paths and churn against reference patches."""
from __future__ import annotations

import subprocess


def changed_files(workspace, base):
    proc = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=workspace,
                          capture_output=True, text=True, check=True)
    return set(proc.stdout.splitlines())


def diff_lines(workspace, base):
    proc = subprocess.run(["git", "diff", "--numstat", base, "HEAD"], cwd=workspace,
                          capture_output=True, text=True, check=True)
    total = 0
    for line in proc.stdout.splitlines():
        a, d, _ = line.split("\t", 2)
        if a.isdigit() and d.isdigit():
            total += int(a) + int(d)
    return total


def compare(workspace, base, reference_files, reference_lines):
    files = changed_files(workspace, base)
    return {"unnecessary_files": sorted(files - set(reference_files)),
            "churn_ratio": diff_lines(workspace, base) / max(1, reference_lines)}
