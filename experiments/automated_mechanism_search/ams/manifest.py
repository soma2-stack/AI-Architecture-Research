"""Immutable run configuration and run manifest (git commit, packages, seeds, machine,
config hash, benchmark generator hashes, grammar / collision-library versions, CPU)."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from typing import Dict

from . import COLLISION_LIBRARY_VERSION, GRAMMAR_VERSION, PROBE_BLOB_SHA, PROTOCOL_VERSION

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_V2 = os.path.join(HERE, "config", "run_config.json")        # historical v2 record (unchanged)
CONFIG_V3 = os.path.join(HERE, "config", "run_config_v3.json")     # v3 record (Stage-0 PASS, v3 Stage 1)
CONFIG_V4 = os.path.join(HERE, "config", "run_config_v4.json")     # v4 record (v4 Stage 1)
CONFIG = os.path.join(HERE, "config", "run_config_v5.json")

RUN_CONFIG = {
    "protocol": PROTOCOL_VERSION,
    "grammar_version": GRAMMAR_VERSION,
    "collision_library_version": COLLISION_LIBRARY_VERSION,
    "probe_corpus": {"path": "config/behavioral_probes_v2.json", "git_blob_sha": PROBE_BLOB_SHA},
    "substrate": {"hidden": [32, 32], "activation": "tanh", "dtype": "float32", "init": "glorot_normal",
                  "program_shared_across_layers": True},
    "grammar_limits": {"max_regs": 4, "max_M_regs": 2, "max_nodes": 40, "max_depth": 5, "max_struct": 1},
    "lr_grid": [1e-3, 1e-2, 1e-1],
    "seeds": {"stage1": [100, 101, 102, 103, 104], "tier1": [1000, 1001, 1002], "sanity": [500],
              "stage3": list(range(10000, 10010)), "tier3": list(range(20000, 20010))},
    "budget": {"generated": 6000, "sanity": 3000, "tier1": 1200, "promoted": 20, "N_INIT": 200,
               "offspring": 50, "G_MAX": 20, "patience": 5, "p_crossover": 0.2, "q_min": 0.15,
               "per_cell": 1, "per_task": 8},
    "taskB_stage0_gate_v3": {"seeds": [100, 101, 102, 103, 104, 1000, 1001, 1002], "pairs_per_seed": 64,
                             "gradient": "first-layer weight matrix, batch-mean 0.5||e||^2",
                             "init": "glorot_normal", "seed_mean_cos_lt": 0.0, "frac_pairs_negative_min": 0.90},
    "stage1_v5": {"mandatory": ["M2_v4_B_fit", "M3_B_interference", "V1_B_REP", "M4_F_failure", "M5_detector",
                                "M6_controls_run", "M7_v4_Cstar_sanity", "V3_F", "V_D"],
                  "M2_v4_fit_reduction_min": 0.95, "V1_B_REP": {"updates": 4000, "batch": [16, 16], "final": True,
                  "rel_err_reduction_min": 0.95, "optimizers": ["SGD", "SGDM", "AdamW"], "rule": "any optimizer"},
                  "M7_v4_generic_hl_censored_max_exclusive": 64,
                  "diagnostic_only": ["V1_B", "V2_Cstar"]},
    "thresholds": {"dup_cos": 0.999, "family_cos": 0.99,
                   "B_forgetting_pp": 40, "B_retention": 80, "B_T2_mse_ratio": 1.25,
                   "C_hl_reduction": 0.5, "C_tau": 0.05, "F_train": 0.98, "F_sgg_pp": 15,
                   "F_gate_train": 0.98, "F_gate_ood_max": 0.25, "F_gate_sgg_min": 75, "B_fit_mse": 1e-3},
    "compute": {"cpu_only": True, "cpu_cap_hours": 30.0, "timeout_s_per_seed": 120, "mem_mb": 512},
}


def config_hash(cfg: Dict = RUN_CONFIG) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()


def write_or_verify_config(path: str = CONFIG) -> str:
    """Write the immutable run configuration once; afterwards refuse to run if it changed."""
    h = config_hash()
    if os.path.exists(path):
        with open(path) as f:
            stored = json.load(f)
        if stored.get("sha256") != h or config_hash(stored["config"]) != h:
            raise RuntimeError("run_config.json differs from the frozen RUN_CONFIG; refusing to run")
        return h
    with open(path, "w") as f:
        json.dump({"sha256": h, "config": RUN_CONFIG}, f, indent=1, sort_keys=True)
    return h


def _git(*args) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=HERE, text=True).strip()
    except Exception:
        return "unknown"


def build_manifest(stage: str, extra: Dict) -> Dict:
    import numpy
    import scipy
    try:
        import pytest
        pv = pytest.__version__
    except Exception:
        pv = None
    from .tasks import generator_fingerprint
    return {
        "stage": stage,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain")),
        "packages": {"python": sys.version.split()[0], "numpy": numpy.__version__,
                     "scipy": scipy.__version__, "pytest": pv},
        "machine": {"platform": platform.platform(), "processor": platform.processor(),
                    "nproc": os.cpu_count(), "mem_total_mb": _meminfo()},
        "gpu_used": False,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "config_sha256": config_hash(),
        "grammar_version": GRAMMAR_VERSION,
        "collision_library_version": COLLISION_LIBRARY_VERSION,
        "probe_blob_sha": PROBE_BLOB_SHA,
        "benchmark_generator_hashes_seed100": generator_fingerprint(100),
        **extra,
    }


def _meminfo():
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    return int(line.split()[1]) // 1024
    except OSError:
        return None
