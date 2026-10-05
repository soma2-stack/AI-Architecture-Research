"""Freeze source hashes, then verify preservation and the legal-spike formula.

python audit.py --freeze
python audit.py --verify
No historical file is written; no existing output is overwritten.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE_FOLDERS = [
    "theory/codex_energy_credit_tradeoff_20261003",
    "theory/grok_energy_credit_tradeoff_review_20261003",
    "theory/codex_multiharmonic_lower_20261002",
    "theory/codex_bounded_history_multiharmonic_20261003",
]


def manifest():
    files = [ROOT / "AGENTS.md"]
    for folder in SOURCE_FOLDERS:
        files.extend(p for p in (ROOT/folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts)
    return {str(p.relative_to(ROOT)).replace("\\", "/"):
            hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


def spike():
    results = []
    for n in [200, 256, 601, 1000, 50000]:
        k, d = n//2, n//4
        tau = 1/math.sqrt(k)
        gamma = 1/(1-tau)
        w = np.full(k, -tau)
        w[0] += 1
        def U(v):
            return v-gamma*w*np.dot(w, v)
        middle = U(np.ones(k))
        middle[:d] = np.roll(middle[:d], -1)
        c = (1-1/n)/math.cosh(.25)**2*U(middle)/math.sqrt(n)
        formula = (1-1/n)/math.cosh(.25)**2*(math.sqrt(k)-gamma/math.sqrt(k))/math.sqrt(n)
        assert abs(c[d-1]-formula) < 1e-13
        assert formula > .58
        results.append({"n": n, "legal_spike_value": formula,
                        "direct_row_discrepancy": float(abs(c[d-1]-formula)),
                        "spike_times_sqrt_n": formula*math.sqrt(n)})
    return results


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) == 2 else ""
    if mode not in ["--freeze", "--verify"]:
        raise SystemExit("Use --freeze or --verify")
    destination = HERE/("PROVENANCE.json" if mode == "--freeze" else "FINAL_AUDIT.json")
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite {destination.name}")
    start, cpu = time.perf_counter(), time.process_time()
    hashes = manifest()
    if mode == "--freeze":
        data = {
            "base_git_HEAD": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "source_hashes": hashes,
            "notebook_worktree_sha256_before_our_addition": hashlib.sha256((ROOT/"Codex_Research.md").read_bytes()).hexdigest(),
            "preexisting_tracked_changes": ["Claude_Research.md", "Codex_Research.md", "experiments/gas0/README.md"],
            "index_initially_empty": True,
            "scope": "New folder and additive Codex resume only; no historical proof/review changed.",
            "hash_timing": "Source receipt collected after deriving the new proof; all source reads were read-only.",
        }
    else:
        before = json.loads((HERE/"PROVENANCE.json").read_text(encoding="utf-8"))["source_hashes"]
        assert hashes == before, "A frozen historical source changed"
        checks = json.loads((HERE/"checks_result.json").read_text(encoding="utf-8"))
        assert checks["status"] == "PASS"
        assert hashlib.sha256((HERE/"checks.py").read_bytes()).hexdigest() == checks["script_sha256"]
        data = {"status": "PASS", "all_frozen_source_hashes_unchanged": True,
                "frozen_source_count": len(hashes), "legal_spike_checks": spike(),
                "checks_script_matches_saved_run": True,
                "important_sources": {k: v for k, v in hashes.items() if k.endswith("PROOF.md") or k.endswith("REPORT.md")},
                "GPU_used": False}
    data.update({"CPU_seconds": time.process_time()-cpu, "wall_seconds": time.perf_counter()-start})
    destination.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"written": destination.name, "source_count": len(hashes),
                      "status": data.get("status", "FROZEN"), "CPU_seconds": data["CPU_seconds"]}))


if __name__ == "__main__":
    main()
