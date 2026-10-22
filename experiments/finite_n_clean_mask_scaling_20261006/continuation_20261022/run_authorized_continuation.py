"""Owner-authorized completion of the original MAIN-21 finite recurrence tests.

This imports the original runner and reference recurrence without changing their
equations. Only the convenience wall-clock cutoffs are disabled. The script
executes the originally listed n=2048, K=32, sum-free R=20/24/32 cases and the
n=1024, K=16, R=8 clear multipliers 0.5/1/2/4. Existing equivalent K-scaling
rows are provenance-checked and reused rather than rerun.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parent
REPO = EXPERIMENT.parents[1]
sys.path.insert(0, str(EXPERIMENT))

import torch

torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)

# The original runner repeats set_num_interop_threads(1) during import. PyTorch
# rejects a second call after initialization, so suppress only that redundant
# setter; the one-thread setting above remains active for the entire run.
_set_interop_threads = torch.set_num_interop_threads
torch.set_num_interop_threads = lambda _count: None
try:
    import run_clean_scaling as original
finally:
    torch.set_num_interop_threads = _set_interop_threads

OUT = HERE
GPU_TARGET_C = 81
GPU_HARD_STOP_C = 86
VRAM_HARD_LIMIT_MIB = 10 * 1024
SAMPLE_INTERVAL_SECONDS = 10


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def gpu_sample() -> dict[str, float | int]:
    proc = subprocess.run(
        ["nvidia-smi", "--query-gpu=temperature.gpu,memory.used,utilization.gpu,power.draw",
         "--format=csv,noheader,nounits"],
        check=True, capture_output=True, text=True, timeout=10,
    )
    row = proc.stdout.strip().splitlines()[0].split(",")
    return {
        "temperature_c": float(row[0].strip()),
        "memory_used_mib": int(float(row[1].strip())),
        "utilization_percent": int(float(row[2].strip())),
        "power_w": float(row[3].strip()),
    }


class SafetyMonitor:
    def __init__(self) -> None:
        self.stop = threading.Event()
        self.cool = threading.Event()
        self.finished = threading.Event()
        self.reason: str | None = None
        self.thread: threading.Thread | None = None
        self.last: dict[str, float | int] | None = None
        self.error: str | None = None

    def sample_once(self) -> dict[str, float | int]:
        row = gpu_sample()
        row["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        self.last = row
        if row["temperature_c"] > GPU_HARD_STOP_C:
            self.reason = f"GPU temperature exceeded {GPU_HARD_STOP_C} C: {row['temperature_c']} C"
            self.stop.set()
        elif row["memory_used_mib"] >= VRAM_HARD_LIMIT_MIB:
            self.reason = f"GPU memory reached {VRAM_HARD_LIMIT_MIB} MiB: {row['memory_used_mib']} MiB"
            self.stop.set()
        if row["temperature_c"] > GPU_TARGET_C:
            self.cool.set()
        else:
            self.cool.clear()
        return row

    def _loop(self) -> None:
        log = OUT / "gpu_telemetry.csv"
        new_file = not log.exists()
        while not self.finished.is_set():
            try:
                row = self.sample_once()
                with log.open("a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        "timestamp_utc", "temperature_c", "memory_used_mib",
                        "utilization_percent", "power_w",
                    ])
                    if new_file:
                        writer.writeheader()
                        new_file = False
                    writer.writerow(row)
            except Exception as exc:  # retain telemetry failure in provenance
                self.error = f"{type(exc).__name__}: {exc}"
            self.finished.wait(SAMPLE_INTERVAL_SECONDS)

    def start(self) -> None:
        self.sample_once()
        if self.stop.is_set():
            raise RuntimeError(self.reason)
        self.thread = threading.Thread(target=self._loop, name="gpu-safety-monitor", daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.finished.set()
        if self.thread:
            self.thread.join(timeout=15)


def reused_k_conditions() -> dict:
    main21_path = EXPERIMENT / "results.json"
    main25_path = EXPERIMENT.parent / "finite_n_r20_r32_scaling_20261006" / "results.json"
    main21_meta = json.loads((EXPERIMENT / "run_metadata.json").read_text(encoding="utf-8"))
    main25_meta = json.loads((main25_path.parent / "run_metadata.json").read_text(encoding="utf-8"))
    main21 = json.loads(main21_path.read_text(encoding="utf-8"))["cases"]
    main25 = json.loads(main25_path.read_text(encoding="utf-8"))["cases"]
    expected_ref = main21_meta["source_sha256"]["reference_cuda.py"]
    found_ref = main25_meta["source_reference_sha256"]
    if expected_ref != found_ref:
        raise RuntimeError(f"K evidence recurrence hash mismatch: MAIN21={expected_ref}, MAIN25={found_ref}")

    sources = {}
    rows = []
    for k in (8, 16, 32, 64):
        if k == 32:
            row = main21["reproduce_n2048_K32_R8_sum_free_c2"]
            source = "../results.json#reproduce_n2048_K32_R8_sum_free_c2"
            source_path = main21_path
        else:
            row = next(v for v in main25.values()
                       if v.get("n") == 2048 and v.get("K") == k and v.get("R") == 8
                       and v.get("family") == "sum_free" and v.get("clear_mult") == 2.0)
            source = f"../../finite_n_r20_r32_scaling_20261006/results.json#{row['case_name']}"
            source_path = main25_path
        fields = (row.get("n"), row.get("K"), row.get("R"), row.get("family"), row.get("clear_mult"))
        if fields != (2048, k, 8, "sum_free", 2.0):
            raise RuntimeError(f"Unexpected K source row for K={k}: {fields}")
        if row.get("m") != 128 or row.get("clear_steps") != 8192 or row.get("total_steps") != 91921:
            raise RuntimeError(f"MAIN21 K={k} geometry mismatch: m/clear/total={row.get('m')}/{row.get('clear_steps')}/{row.get('total_steps')}")
        if row.get("walsh_masks") != [1, 3, 5, 7, 9, 11, 13, 15]:
            raise RuntimeError(f"Unexpected K={k} mask construction")
        if k != 32 and row.get("equal_age_steps") != 256:
            raise RuntimeError(f"Unexpected K={k} inherited equal-age diagnostic condition")
        metrics = row["metrics"]
        rows.append({
            "K": k,
            "complete_crosstalk": metrics["max_complete_normalized_crosstalk"],
            "protected_crosstalk": metrics["max_protected_normalized_crosstalk"],
            "oldest_newest_diagonal_ratio": metrics["oldest_newest_diagonal_ratio"],
            "max_absolute_leakage": metrics["max_complete_absolute_leakage"],
            "source": source,
            "source_sha256": sha256(source_path),
            "equal_age_steps_recorded": row.get("equal_age_steps"),
            "endpoint_reuse_note": (
                "The inherited MAIN25 rows recorded additional read-only age-256 checkpoints. "
                "The original recurrence only uses equal_age_steps to collect observations; it does "
                "not alter state transitions. The endpoint matrix and geometry match MAIN21."
            ) if k != 32 else "Exact MAIN21 completed K=32 endpoint case; reused without rerun.",
        })
    values = [x["complete_crosstalk"] for x in rows]
    result = {
        "experiment": "MAIN-21 clean-mask K scaling",
        "status": "RECOVERED_FROM_EXISTING_COMPLETED_CASES; NO_RERUN",
        "source_reference_sha256": expected_ref,
        "n": 2048, "R": 8, "family": "sum_free", "clear_multiplier": 2.0,
        "threshold": 0.001,
        "complete_crosstalk_range": [min(values), max(values)],
        "complete_crosstalk_peak_to_peak": max(values) - min(values),
        "rows": rows,
        "provenance": {
            "main21_results": str(main21_path.relative_to(REPO)),
            "main25_results": str(main25_path.relative_to(REPO)),
            "main21_reference_sha256": expected_ref,
            "main25_reference_sha256": found_ref,
            "same_core_reference": expected_ref == found_ref,
        },
    }
    atomic_json(OUT / "reused_k_comparison.json", result)
    return result


def write_config() -> dict:
    runner_hash = sha256(EXPERIMENT / "run_clean_scaling.py")
    ref_hash = sha256(EXPERIMENT / "reference_cuda.py")
    config = {
        "experiment_id": "MAIN-21",
        "continuation_authorization_date": "2026-10-22",
        "authorization": "Owner explicitly reopened MAIN-21 only in this task; prior withdrawal remains historical and is superseded only for this continuation.",
        "original_convenience_time_cap": {"seconds": 5400, "status": "disabled for this owner-authorized continuation only"},
        "scientific_criteria_changed": False,
        "primary_threshold": {"complete_normalized_crosstalk_strictly_less_than": 0.001},
        "conditions_to_execute": [
            {"name": "higher_R_n2048", "n": 2048, "K": 32, "R": [20, 24, 32], "family": "sum_free", "clear_multiplier": 2.0, "equal_age_steps": None},
            {"name": "clean_clear_sweep_n1024", "n": 1024, "K": 16, "R": 8, "family": "sum_free", "clear_multiplier": [0.5, 1.0, 2.0, 4.0], "equal_age_steps": None},
        ],
        "conditions_reused_without_rerun": "K=8/16/64 from completed MAIN25 TEST1 rows and K=32 from MAIN21's original completed R=8 reproduction; see reused_k_comparison.json. The separate MAIN25 n=4096 TEST3 is not run or continued.",
        "source": {
            "repo_head_before_continuation": "341369b45073e02d2796e4687d318004e812899c",
            "runner": "experiments/finite_n_clean_mask_scaling_20261006/run_clean_scaling.py",
            "runner_sha256": runner_hash,
            "reference": "experiments/finite_n_clean_mask_scaling_20261006/reference_cuda.py",
            "reference_sha256": ref_hash,
        },
        "execution": {
            "device": "cuda:0",
            "required_gpu": "NVIDIA GeForce RTX 3060",
            "dtype": "torch.float64",
            "cuda_required": True,
            "cpu_fallback": False,
            "torch_threads": 1,
            "inter_op_threads": 1,
            "thread_env": {"OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"},
            "target_gpu_temperature_c_max": GPU_TARGET_C,
            "mandatory_stop_gpu_temperature_c_above": GPU_HARD_STOP_C,
            "mandatory_stop_gpu_memory_mib_at_or_above": VRAM_HARD_LIMIT_MIB,
            "monitor_interval_seconds": SAMPLE_INTERVAL_SECONDS,
            "wall_time_cap_seconds": None,
        },
        "notes": [
            "Only original runner control flow and the original CUDA float64 recurrence are used for new cases.",
            "The original wall and optional cutoffs are overridden in memory; original source files are not modified.",
            "MAIN-25 TEST3 at n=4096 remains out of scope and untouched.",
            "No training, optimization, or new mask family is included.",
        ],
    }
    atomic_json(OUT / "continuation_config.json", config)
    return config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="continue from this folder's saved cases without rerunning completed rows")
    args = parser.parse_args()
    existing_results = OUT / "results.json"
    existing_progress = OUT / "progress.json"
    existing_metadata = OUT / "run_metadata.json"
    if existing_results.exists() and not args.resume:
        raise RuntimeError("Saved continuation results already exist; pass --resume to preserve and continue them.")
    prior_data = json.loads(existing_results.read_text(encoding="utf-8")) if existing_results.exists() else None
    prior_progress = json.loads(existing_progress.read_text(encoding="utf-8")) if existing_progress.exists() else {}
    prior_metadata = json.loads(existing_metadata.read_text(encoding="utf-8")) if existing_metadata.exists() else {}
    prior_runtime = float(prior_data.get("runtime_seconds", 0.0)) if prior_data else 0.0
    config = write_config()
    reuse = reused_k_conditions()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable; the original protocol forbids CPU fallback.")
    torch.cuda.set_device(0)
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    gpu_name = torch.cuda.get_device_name(0)
    if "RTX 3060" not in gpu_name:
        raise RuntimeError(f"Unexpected GPU for this authorized run: {gpu_name}")

    monitor = SafetyMonitor()
    first = monitor.sample_once()
    if first["temperature_c"] > GPU_TARGET_C:
        raise RuntimeError(f"Preflight temperature exceeds target; cool before starting: {first}")
    if first["memory_used_mib"] >= VRAM_HARD_LIMIT_MIB:
        raise RuntimeError(f"Preflight GPU memory violates limit: {first}")
    monitor.start()

    original.OUT = OUT
    original.START = time.perf_counter() - prior_runtime
    original.WALL_LIMIT = 10**12
    original.OPTIONAL_STOP = 10**12
    original.ref.START = original.START
    original.ref.LIMIT = 10**12
    original.ref.guard = lambda: safe_guard(monitor)
    original.DATA = prior_data or {
        "description": "Owner-authorized MAIN-21 continuation; original CUDA float64 recurrence; no training.",
        "cases": {}, "mask_diagnostics": {}, "test_verdicts": {},
        "runtime_seconds": 0.0, "errors": [], "skipped": [],
        "reused_k_comparison": "reused_k_comparison.json",
    }
    original.COMPLETED = list(original.DATA.get("cases", {}))
    original.FAILED = list(prior_progress.get("failed_tests", []))
    original.SKIPPED = list(prior_progress.get("skipped_tests", []))
    original.PLANNED = list(prior_progress.get("completed_tests", [])) + list(prior_progress.get("pending_tests", []))

    metadata = {
        "experiment": "MAIN-21",
        "status": "RUNNING",
        "start_timestamp_utc": prior_metadata.get("start_timestamp_utc", datetime.now(timezone.utc).isoformat()),
        "run_segments": list(prior_metadata.get("run_segments", [])) + [datetime.now(timezone.utc).isoformat()],
        "python_version": sys.version,
        "pytorch_version": torch.__version__,
        "cuda_runtime_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda:0", "gpu_name": gpu_name,
        "gpu_total_memory_bytes": torch.cuda.get_device_properties(0).total_memory,
        "dtype": "torch.float64",
        "preflight_gpu_sample": first,
        "initial_torch_allocated_vram_bytes": int(torch.cuda.memory_allocated()),
        "initial_torch_reserved_vram_bytes": int(torch.cuda.memory_reserved()),
        "torch_num_threads": torch.get_num_threads(),
        "torch_num_interop_threads": torch.get_num_interop_threads(),
        "thread_env": {k: os.environ.get(k) for k in config["execution"]["thread_env"]},
        "resource_policy": config["execution"],
        "original_wall_limit_disabled": True,
        "original_wall_limit_seconds": 5400,
        "original_reference_wall_limit_seconds": 3500,
        "overrides_applied": {
            "run_clean_scaling.WALL_LIMIT": "1e12 seconds",
            "run_clean_scaling.OPTIONAL_STOP": "1e12 seconds",
            "reference_cuda.LIMIT": "1e12 seconds",
            "scientific recurrence, dimensions, masks, clear schedule and thresholds": "unchanged",
        },
        "reused_k_source": reuse["provenance"],
        "monitor_log": "gpu_telemetry.csv",
    }
    atomic_json(OUT / "run_metadata.json", metadata)

    try:
        # Reuse existing K=8/16/32/64 data; execute only original missing rows.
        for clear in (0.5, 1.0, 2.0, 4.0):
            original.run_case("authorized_clear", 1024, 16, 8, "sum_free", clear)
        for r in (20, 24, 32):
            original.run_case("authorized_higher_R", 2048, 32, r, "sum_free", 2.0)
        original.DATA["test_verdicts"]["clear_sweep_complete"] = True
        original.DATA["test_verdicts"]["higher_R_sweep_complete"] = True
        original.DATA["test_verdicts"]["primary_threshold"] = 0.001
        status = "COMPLETE"
    except Exception as exc:
        original.DATA["errors"].append({
            "time_seconds": original.elapsed(), "type": type(exc).__name__,
            "message": str(exc), "traceback": traceback.format_exc(),
        })
        status = "STOPPED_FOR_SAFETY" if monitor.stop.is_set() else "FAILED_OR_INTERRUPTED"
    finally:
        monitor.close()
        torch.cuda.synchronize()
        metadata.update({
            "status": status,
            "end_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "total_runtime_seconds": original.elapsed(),
            "peak_allocated_vram_bytes": int(torch.cuda.max_memory_allocated()),
            "peak_reserved_vram_bytes": int(torch.cuda.max_memory_reserved()),
            "last_gpu_sample": monitor.last,
            "safety_stop_reason": monitor.reason,
            "telemetry_error": monitor.error,
            "max_temperature_c_sampled": None,
            "max_memory_used_mib_sampled": None,
        })
        telemetry = OUT / "gpu_telemetry.csv"
        if telemetry.exists():
            try:
                samples = list(csv.DictReader(telemetry.open(encoding="utf-8", newline="")))
                if samples:
                    metadata["max_temperature_c_sampled"] = max(float(x["temperature_c"]) for x in samples)
                    metadata["max_memory_used_mib_sampled"] = max(int(x["memory_used_mib"]) for x in samples)
            except Exception as exc:
                metadata["telemetry_error"] = f"{type(exc).__name__}: {exc}"
        atomic_json(OUT / "run_metadata.json", metadata)
        original.DATA["runtime_seconds"] = original.elapsed()
        atomic_json(OUT / "results.json", original.DATA)
        progress = {
            "status": status,
            "completed_tests": original.COMPLETED,
            "failed_tests": original.FAILED,
            "skipped_tests": original.SKIPPED,
            "pending_tests": [x for x in original.PLANNED if x not in original.COMPLETED and x not in original.FAILED and x not in original.SKIPPED],
            "elapsed_runtime_seconds": original.elapsed(),
            "peak_allocated_vram_bytes": int(torch.cuda.max_memory_allocated()),
            "peak_reserved_vram_bytes": int(torch.cuda.max_memory_reserved()),
            "max_temperature_c_sampled": metadata["max_temperature_c_sampled"],
            "max_memory_used_mib_sampled": metadata["max_memory_used_mib_sampled"],
            "safety_stop_reason": monitor.reason,
        }
        atomic_json(OUT / "progress.json", progress)
    print(json.dumps({"status": status, "completed": original.COMPLETED,
                      "runtime_seconds": original.elapsed(), "safety_stop": monitor.reason,
                      "max_temp_c": metadata["max_temperature_c_sampled"],
                      "max_memory_mib": metadata["max_memory_used_mib_sampled"]}, indent=2))
    return 0 if status == "COMPLETE" else 2


def safe_guard(monitor: SafetyMonitor) -> None:
    original.ref._original_guard()
    if monitor.stop.is_set():
        raise RuntimeError(monitor.reason or "GPU safety stop")
    if monitor.cool.is_set():
        print(f"GPU above {GPU_TARGET_C} C target; pausing at recurrence guard until cool.", flush=True)
        torch.cuda.synchronize()
        while monitor.cool.is_set():
            if monitor.stop.is_set():
                raise RuntimeError(monitor.reason or "GPU safety stop during cooldown")
            time.sleep(2)


if __name__ == "__main__":
    # Retain the original engine's allocation guard and add monitored limits.
    original.ref._original_guard = original.ref.guard
    raise SystemExit(main())
