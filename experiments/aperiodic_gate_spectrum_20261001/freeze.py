"""Hash prospective diagnostic inputs, without generating official histories."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parent.parent
sources = [root/"config.json", root/"PREREGISTRATION.md", root/"run.py", root/"freeze.py",
           repo/"AGENTS.md", repo/"theory/rotating_gate_aggregation_20261001/PROOF.md",
           repo/"theory/gamma_c_over_n_quadratic_20261001/PROOF.md",
           repo/"theory/aperiodic_query_aggregation_20261001/PROOF.md"]
record = dict(parent_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
              python=sys.version, platform=platform.platform(),
              inputs={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              official_results_collected=False,
              development_results="Three n=16/H=32 development cases; saved separately; no official histories scored.")
destination = root/"FROZEN.json"
if destination.exists():
    raise RuntimeError("Refusing to replace the frozen manifest")
destination.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
print(json.dumps(record, indent=2))
