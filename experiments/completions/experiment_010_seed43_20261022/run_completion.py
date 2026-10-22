"""Replay only Exp010's unfinished condition; leave the original source untouched."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source = args.source_root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    reference_path = Path(__file__).with_name("original_reference.json")
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    import torch

    assert platform.python_version() == reference["original_environment"]["python"]
    assert torch.__version__ == "2.14.1+cpu"
    assert torch.version.cuda is None and not torch.cuda.is_available()
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == ""
    for name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        assert os.environ.get(name) == "1", name
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True
    ).strip()
    assert source_sha == reference["source_commit"]
    source_hashes = {name: digest(source / name) for name in reference["source_sha256"]}
    assert source_hashes == reference["source_sha256"]
    command = [
        sys.executable, "-m", "prototypes.rnn_llm_architecture.capacity_010",
        "--output", str(output / "result.json"),
        "--tasks", "8x2", "--variants", "delta_rule", "--seeds", "43",
        "--steps", "800", "--batch", "12", "--eval-batch", "128",
        "--eval-every", "200", "--delay", "64", "--eval-delays", "64,256",
        "--max-wall-seconds", "1050",
    ]
    provenance = {
        "source_commit": source_sha,
        "source_sha256": source_hashes,
        "reference_sha256": digest(reference_path),
        "runner_sha256": digest(Path(__file__)),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "environment": {name: os.environ.get(name) for name in (
            "CUDA_VISIBLE_DEVICES", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
            "OPENBLAS_NUM_THREADS", "PYTHONHASHSEED", "GITHUB_RUN_ID", "GITHUB_SHA"
        )},
        "pip_freeze": subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"], text=True
        ).splitlines(),
        "command": command,
        "training_runs_authorized": 1,
        "historical_results_modified": False,
    }
    save(output / "provenance.json", provenance)
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    with (output / "stdout.txt").open("x", encoding="utf-8") as log:
        process = subprocess.run(
            command, cwd=source, stdout=log, stderr=subprocess.STDOUT, timeout=1100
        )
    wall = time.monotonic() - start
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    assert process.returncode == 0, "Original runner failed; do not retry automatically"
    result = json.loads((output / "result.json").read_text(encoding="utf-8"))
    assert result["status"] == "complete" and not result["skipped"]
    assert len(result["runs"]) == 1
    row = result["runs"][0]
    assert (row["variant"], row["slots"], row["values"], row["seed"], row["steps"], row["status"]) == (
        "delta_rule", 8, 2, 43, 800, "complete"
    )
    config = dict(reference["original_shard_config"])
    config.update(variants=["delta_rule"], tasks=[[8, 2]], seeds=[43])
    assert result["config"] == config
    assert result["environment"]["cpu_threads"] == 1
    assert result["environment"]["cuda_available"] is False
    old = reference["original_partial_record"]
    tolerance = reference["prefix_tolerance"]
    checks = {"loss_first": {
        "historical": old["loss_first"], "replay": row["loss_first"]
    }}
    for checkpoint in old["curve"]:
        new = next(item for item in row["curve"] if item["step"] == checkpoint["step"])
        checks[f"loss_at_{checkpoint['step']}"] = {
            "historical": checkpoint["loss"], "replay": new["loss"]
        }
    for check in checks.values():
        check["absolute_difference"] = abs(check["historical"] - check["replay"])
        check["matches"] = math.isclose(check["historical"], check["replay"], **tolerance)
    evaluation = {}
    for delay in ("64", "256"):
        previous, current = old["eval"][delay], row["eval"][delay]
        assert current["histories"] == previous["histories"] == 128
        assert current["varied_count"] == previous["varied_count"]
        evaluation[delay] = {"at_586_updates": previous, "at_800_updates": current}
    verification = {
        "one_condition_only": True, "all_800_updates_completed": True,
        "configuration_matches_original_condition": True,
        "source_hashes_match": True, "original_software_versions_match": True,
        "prefix_tolerance_fixed_before_execution": tolerance,
        "training_prefix_checks": checks,
        "training_prefix_matches": all(item["matches"] for item in checks.values()),
        "evaluation_comparison": evaluation,
        "wall_seconds_including_interpreter_startup": wall,
        "child_cpu_user_seconds": after.ru_utime - before.ru_utime,
        "child_cpu_system_seconds": after.ru_stime - before.ru_stime,
        "child_peak_rss_kib_linux": after.ru_maxrss,
        "scope": "Completion of one fixed-budget screen condition; no architecture-success threshold was registered.",
    }
    save(output / "verification.json", verification)
    print(json.dumps({
        "steps": row["steps"], "prefix_matches": verification["training_prefix_matches"],
        "whole_varied": {delay: row["eval"][delay]["whole_varied"] for delay in ("64", "256")},
        "wall_seconds": wall,
    }))
    assert verification["training_prefix_matches"], "Replay prefix differs; preserve and report, do not retry"


if __name__ == "__main__":
    main()
