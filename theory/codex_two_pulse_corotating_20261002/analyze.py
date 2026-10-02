"""Compact summaries of preserved outputs; no new witness selection."""
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run():
    primary = json.loads((HERE / "SCREEN.json").read_text())
    verification = json.loads((HERE / "VERIFICATION.json").read_text())
    adversary = json.loads((HERE / "ADVERSARY.json").read_text())
    rows = primary["rows"]
    keys = list(rows[0])
    with (HERE / "screen_summary.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader(); writer.writerows(rows)
    summary = {"primary_complete": primary["complete"], "screen_count": len(rows), "antipodal_pairs": sum(r["pairs"] for r in rows),
               "n": {}, "maximum_endpoint_error": max(r["endpoint_error"] for r in rows),
               "maximum_input": max(r["maximum_input"] for r in rows),
               "one_pulse_maximum_affine_residual": max(r["exact_affine_residual"] for r in verification["single_pulse"]),
               "two_pulse_maximum_relative_error": max(r["lemma_relative_error"] for r in verification["two_pulse"])}
    for n in (200, 400, 1000):
        rr = [r for r in rows if r["n"] == n]
        summary["n"][n] = {"sections": len(rr), "all_four_sampled_box_pairs_pass": sum(r["sampled_box_passing_pairs"] == 4 for r in rr),
                           "has_sampled_all_query_upper_below_threshold": sum(r["sampled_all_query_failure_evidence"] for r in rr),
                           "cycle_family_rigorous_cap": (n // 4) ** 2 + 1,
                           "largest_tested_history_chart": max(r["joint_history_chart_dimension"] for r in rr),
                           "T_n_log_profile_sustained": next(r for r in rr if r["T"] == n and r["q"] == math.ceil(math.log(n)) and r["mapping"] == "spread" and r["strength"] == "sustained")}
    resources = [json.loads((HERE / name).read_text()) for name in ("RESOURCE.json", "ADVERSARY_RESOURCE.json")]
    resources.append(json.loads((HERE / "CHANNEL_DIAGNOSTIC.json").read_text())["resource"])
    summary["resource"] = {"measured_cpu_seconds": sum(r["cpu_seconds"] for r in resources),
                           "measured_wall_seconds": sum(r["wall_seconds"] for r in resources),
                           "peak_rss_bytes": max(r["peak_rss_bytes"] for r in resources),
                           "gpu_seconds": 0, "cuda_used": False, "scope": "Measured official numerical runners; import/test/admin overhead separate"}
    summary["adversary"] = adversary["rows"]
    (HERE / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("n", "adversary")}))
    for n, record in summary["n"].items():
        print(n, {k: v for k, v in record.items() if k != "T_n_log_profile_sustained"})


if __name__ == "__main__":
    run()
