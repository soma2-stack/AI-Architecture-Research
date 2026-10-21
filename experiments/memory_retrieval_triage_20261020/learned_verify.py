"""Read-only integrity check for learned-address CPU experiment."""
import ast,hashlib,json,math
from pathlib import Path
here=Path(__file__).resolve().parent
src=here/"learned_address.py"
raw=here/"learned_results.json"
report=here/"LEARNED_ADDRESS_REPORT.md"
ast.parse(src.read_text(encoding="utf-8"))
d=json.loads(raw.read_text(encoding="utf-8"))
assert d["complete"] and len(d["runs"])==6
assert d["protocol"]["cpu_threads"]==4 and d["protocol"]["cuda"] is False
assert d["protocol"]["write_parser_in_forward"] is False
expected={(seed,slots) for seed in (17,29) for slots in (2,4,8)}
assert {(r["seed"],r["slots"]) for r in d["runs"]}==expected
for r in d["runs"]:
    assert r["steps"]==240 and math.isfinite(r["final_loss"])
    assert r["state_scalars"]==32+12*r["slots"]
    assert set(r["eval"])=={"16","64","256"}
    for ev in r["eval"].values():
        assert ev["histories"]==96
        assert all(0<=ev[k]<=1 for k in ("bit","whole","constant"))
mean={s:sum(r["eval"]["256"]["whole"] for r in d["runs"] if r["slots"]==s)/2
      for s in (2,4,8)}
assert abs(mean[2]-.729165)<1e-5
assert abs(mean[4]-.65104)<1e-5
assert abs(mean[8]-.13021)<1e-5
assert "73.16" not in report.read_text(encoding="utf-8") or d["elapsed_seconds"]==73.16
print("VERIFIED 6 complete runs; CPU-only, 4 threads, 2 seeds, 2/4/8 facts.")
print("256-token mean whole-record accuracy:",mean)
for p in (src,raw,report):
    print(p.name, "sha256",hashlib.sha256(p.read_bytes()).hexdigest())
