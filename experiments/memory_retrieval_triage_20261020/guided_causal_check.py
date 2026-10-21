"""Causal readout ablation of saved guided-alignment models; no retraining."""
from __future__ import annotations
import os,sys,json,time
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for nm in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):os.environ[nm]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from write_read_alignment import build
from causal_ablation import evaluate
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"guided_causal_results.json"
if OUT.exists():raise FileExistsError(OUT)
torch.set_num_threads(6)
torch.set_num_interop_threads(1)
if torch.cuda.is_available():raise RuntimeError("GPU unavailable required")
weights=torch.load(ROOT/"write_read_alignment_weights.pt",map_location="cpu",weights_only=True)
runs=[]
start=time.monotonic()
for seed in (17,29):
    for slots in (2,4,8):
        model=build("guided_align",slots,seed)
        model.load_state_dict(weights[f"{seed}_{slots}_guided_align"])
        evseed=900000000+seed*100003+slots*197
        result,error=evaluate(model,slots,evseed,256,96)
        row={"seed":seed,"slots":slots,"max_normal_logit_error":error,"eval":result}
        runs.append(row)
        print("GUIDED_CAUSAL="+json.dumps(row,separators=(",",":")),flush=True)
out={"scope":"inference-only causal interventions on previously trained guided alignment checkpoints",
     "gpu":False,"cpu_threads":6,"runs":runs,"complete":True,
     "elapsed":round(time.monotonic()-start,3)}
OUT.write_text(json.dumps(out,indent=2),encoding="utf8")
print("GUIDED_CAUSAL_COMPLETE="+str(len(runs)),flush=True)
