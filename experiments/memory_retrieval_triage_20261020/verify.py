"""Read-only integrity checks for the local retrieval experiment."""
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent
script = root / "run.py"
results_path = root / "results.json"
report = root / "REPORT.md"
ast.parse(script.read_text(encoding="utf-8"))
d = json.loads(results_path.read_text(encoding="utf-8"))
assert d.get("complete") is True
assert d["protocol"]["cpu_threads"] <= 10
assert d["protocol"]["cuda_visible"] is False
assert d["protocol"]["train_updates"] == 180
assert len(d["runs"]) == 24
expected = {(s,n,m) for s in (17,29) for n in (2,4,8)
            for m in ("gru","pair","hybrid","delta")}
found = {(r["seed"],r["slots"],r["model"]) for r in d["runs"]}
assert found == expected
assert len(found) == len(d["runs"])
for row in d["runs"]:
    assert row["params"] > 0 and row["state_scalars"] > 0
    assert row["final_loss"] >= 0 and row["training_wall_seconds"] > 0
    assert set(row["evaluation"]) == {"16","64","256"}
    for measurement in row["evaluation"].values():
        assert measurement["histories"] == 96
        assert all(0 <= measurement[k] <= 1 for k in ("bit","whole","constant"))
        if row["model"] in ("hybrid","delta"):
            assert measurement["bit"] == measurement["whole"] == 1.0
for n in (2,4,8):
    for model in ("gru","pair"):
        for r in [x for x in d["runs"] if x["slots"] == n and x["model"] == model]:
            assert r["evaluation"]["256"]["whole"] < 1
text = report.read_text(encoding="utf-8")
for key in ("PASS (structured recall)", "FAIL (distinctive hybrid advantage)",
            "exact-real", "CPU", "180", "24/24"):
    assert key in text, key
print("VERIFIED: 24 unique completed runs, 2 seeds, 3 fact counts, 3 delays,")
print("GPU disabled; attention advantage not established; files readable.")
for p in (script,results_path,report):
    print(f"{p.name}: {p.stat().st_size} bytes SHA256={hashlib.sha256(p.read_bytes()).hexdigest()}")
