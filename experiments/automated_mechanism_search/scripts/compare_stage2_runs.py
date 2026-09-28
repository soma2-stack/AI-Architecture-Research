"""Compare the first stopped Stage-2 run with the repaired rerun (raw-program sequence and labels)."""
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(run):
    with gzip.open(os.path.join(HERE, "runs", run, "records.jsonl.gz"), "rt") as f:
        return [json.loads(l) for l in f]


def main(a="stage2", b="stage2_repair1"):
    A, B = load(a), load(b)
    n = min(len(A), len(B))
    first_raw_div = next((i for i in range(n) if A[i]["raw"] != B[i]["raw"] or A[i]["pid"] != B[i]["pid"]), None)
    label_changes = [{"pid": A[i]["pid"], "before": A[i]["label"], "after": B[i]["label"]}
                     for i in range(n if first_raw_div is None else first_raw_div) if A[i]["label"] != B[i]["label"]]
    canon_changes = sum(1 for i in range(n if first_raw_div is None else first_raw_div)
                        if A[i].get("canonical") != B[i].get("canonical") and A[i]["label"] != "defect")
    out = {"run_a": a, "run_b": b, "n_a": len(A), "n_b": len(B), "compared_prefix": n,
           "raw_sequence_identical_over_prefix": first_raw_div is None,
           "first_raw_divergence_index": first_raw_div,
           "label_changes_before_divergence": label_changes,
           "canonical_changes_excluding_former_defects": canon_changes}
    with open(os.path.join(HERE, "runs", b, "comparison_to_stage2.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
