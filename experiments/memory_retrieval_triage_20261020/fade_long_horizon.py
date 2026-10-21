"""Held-out, read-only long-horizon check on saved faded-guidance models.
Eight facts. Frozen checkpoints. No GPU, 6 CPU threads, no retraining.
"""
from __future__ import annotations
import os,sys,json,time
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):os.environ[k]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from learned_address import evaluation
from write_read_alignment import build
from causal_ablation import evaluate as causal_evaluate

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"fade_long_horizon_results.json"
if OUT.exists():raise FileExistsError("Do not overwrite existing check")
torch.set_num_threads(6)
torch.set_num_interop_threads(1)
if torch.cuda.is_available():raise RuntimeError("Unexpected GPU visibility")
models=torch.load(ROOT/"faded_guidance_weights.pt",map_location="cpu",weights_only=True)
data={"protocol":{"seeds":[17,29,43],"slots":8,"arms":["linear_fade","fade_by_half"],
                  "eval_histories":32,"delays":[256,1024],
                  "longer_delay_extra_horizon":4096,"longer_horizon_histories":16,
                  "cpu_threads":6,"gpu":False,"read_only":True},
      "runs":[],"complete":False}
start=time.monotonic()
for seed in (17,29,43):
    for arm in ("linear_fade","fade_by_half"):
        model=build("guided_align",8,seed)
        model.load_state_dict(models[f"{seed}_8_{arm}"])
        evseed=900000000+seed*100003+8*197
        res={str(delay):evaluation(model,8,delay,evseed,32) for delay in (256,1024)}
        if seed==17:
            res["4096"]=evaluation(model,8,4096,evseed,16)
        # causal ablation of the same 1024-token batch: verify bank dependence.
        ci,err=causal_evaluate(model,8,evseed,1024,16)
        row={"seed":seed,"arm":arm,"evaluation":res,
             "causal1024":{"normal":ci["normal"],"zero_bank":ci["zero_bank"],
                           "uniform_read":ci["uniform_read"],"max_reference_error":err}}
        data["runs"].append(row)
        OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
        print("LONG_HORIZON="+json.dumps(row,separators=(",",":")),flush=True)
data["complete"]=True
data["elapsed_seconds"]=round(time.monotonic()-start,3)
OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
print("LONG_HORIZON_COMPLETE="+json.dumps({"runs":len(data["runs"]),"seconds":data["elapsed_seconds"]}),flush=True)
