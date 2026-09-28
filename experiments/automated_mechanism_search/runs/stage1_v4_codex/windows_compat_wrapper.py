import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
import types

AMS_ROOT = os.path.join(os.getcwd(), "experiments", "automated_mechanism_search")
if not os.path.isdir(AMS_ROOT):
    raise RuntimeError(f"Expected AMS root under current directory: {AMS_ROOT}")
sys.path.insert(0, os.path.join(AMS_ROOT, "scripts"))
sys.path.insert(0, AMS_ROOT)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Windows CPython lacks Unix resource/getrusage. Stage-1 explicitly adds each
# worker's job CPU, so report parent-only process CPU here and do not double-count.
resource = types.ModuleType("resource")
resource.RUSAGE_SELF = 0
resource.RUSAGE_CHILDREN = 1
class _Usage:
    def __init__(self, user=0.0, system=0.0):
        self.ru_utime = user
        self.ru_stime = system
def _getrusage(who):
    return _Usage(time.process_time(), 0.0) if who == resource.RUSAGE_SELF else _Usage()
resource.getrusage = _getrusage
sys.modules["resource"] = resource

# The frozen runner asks for Unix fork/nice. Use Windows spawn; task randomness
# is explicitly seeded by the frozen runner. Scheduling priority is unavailable.
if not hasattr(os, "nice"):
    os.nice = lambda value: None
_original_get_context = mp.get_context
def _portable_get_context(method=None):
    if method == "fork":
        method = "spawn"
    return _original_get_context(method)
mp.get_context = _portable_get_context

import stage1_v4
stage1_v4.OUT = os.path.join(AMS_ROOT, "runs", "stage1_v4_codex")

if os.environ.get("AMS_PREFLIGHT_ONLY") == "1":
    with open(os.path.join(AMS_ROOT, "config", "run_config_v4.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    with open(os.path.join(AMS_ROOT, "scripts", "stage1_v4.py"), "rb") as f:
        script_sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(AMS_ROOT, "runs", "stage0_v3", "stage0_result.json"), encoding="utf-8") as f:
        stage0 = json.load(f)
    print(json.dumps({"script_sha256": script_sha, "protocol": cfg["config"]["protocol"],
                      "stage0_v3_pass": stage0["pass"], "output": stage1_v4.OUT,
                      "start_methods": mp.get_all_start_methods(), "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES")}, indent=2))
elif __name__ == "__main__":
    raise SystemExit(stage1_v4.main())
