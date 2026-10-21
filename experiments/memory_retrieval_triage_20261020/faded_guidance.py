"""Small controlled hint-withdrawal experiment: retain learned addressing after guidance removed?
Two schedules of the SAME privileged alignment+diversity signals; paired prior
always-on and unguided controls. CPU six threads; no GPU.
"""
from __future__ import annotations
import os,sys,json,time
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for e in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):
    os.environ[e]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from write_read_alignment import build,address_guidance,address_probe
from learned_address import evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/"faded_guidance_results.json"
WEIGHTS=HERE/"faded_guidance_weights.pt"
SEEDS=(17,29,43)
SLOTS=(2,4,8)
ARMS=("linear_fade","fade_by_half")
UPDATES=240
BATCH=12

def strength(arm,step):
    # Both conditions get privileged WRITE_i -> QUERY_i alignment help early.
    # All hints explicitly vanish at the end; no hints at inference.
    stop=239 if arm=="linear_fade" else 119
    return max(0.,1.-step/stop) if step<=stop else 0.

def main():
    if OUTPUT.exists() or WEIGHTS.exists():
        raise FileExistsError("Refusing to overwrite prior fade study data")
    torch.set_num_threads(6);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("GPU should be hidden")
    torch.manual_seed(0)
    results={"protocol":{"seeds":SEEDS,"slots":SLOTS,"arms":ARMS,
       "updates":UPDATES,"batch":BATCH,"heldout_histories":96,
       "delays":[16,64,256],"cpu_threads":6,"cuda":False,
       "guidance_starts_at_one":True,"guidance_ends_at_zero":True,
       "reference":"write_read_alignment_results.json and alignment_seed43_results.json"},
       "caveat":"Hints disclose WRITE_i--QUERY_i pairs during early training. Hint fading does NOT establish independent discovery.",
       "runs":[],"complete":False}
    weights={}
    t_all=time.monotonic()
    for seed in SEEDS:
        for slots in SLOTS:
            for arm in ARMS:
                model=build("guided_align",slots,seed)
                opt=torch.optim.AdamW(model.parameters(),lr=.003)
                trainstart=time.monotonic()
                losses=[];helpers=[]
                for step in range(UPDATES):
                    x,y=batch(slots,16,BATCH,100000000+seed*1000003+step*8191+slots*197)
                    ids=query_histories(x,slots)
                    p=model(ids).reshape(slots,len(x),2).transpose(0,1)
                    ce=F.cross_entropy(p.reshape(-1,2),y.reshape(-1))
                    alpha=strength(arm,step)
                    extra=address_guidance(model,slots)[0]*alpha if alpha>0 else ce.new_zeros(())
                    objective=ce+extra
                    if not torch.isfinite(objective).item():raise RuntimeError("Nonfinite")
                    opt.zero_grad(set_to_none=True)
                    objective.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    opt.step()
                    losses.append(float(ce.detach()))
                    helpers.append(float(extra.detach()))
                evseed=900000000+seed*100003+slots*197
                row={"seed":seed,"slots":slots,"arm":arm,
                     "train_wall_s":round(time.monotonic()-trainstart,3),
                     "parameters":sum(v.numel() for v in model.parameters()),
                     "final_ce":round(sum(losses[-20:])/20,5),
                     "mean_last20_aux":round(sum(helpers[-20:])/20,6),
                     "addr":address_probe(model,slots),
                     "eval":{str(delay):evaluation(model,slots,delay,evseed,96)
                             for delay in (16,64,256)}}
                results["runs"].append(row)
                weights[f"{seed}_{slots}_{arm}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                OUTPUT.write_text(json.dumps(results,indent=2),encoding="utf8")
                print("FADE_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(weights,WEIGHTS)
    results["complete"]=True
    results["elapsed_seconds"]=round(time.monotonic()-t_all,3)
    results["weights_file"]=WEIGHTS.name
    OUTPUT.write_text(json.dumps(results,indent=2),encoding="utf8")
    print("FADE_COMPLETE="+json.dumps({"runs":len(results["runs"]),"seconds":results["elapsed_seconds"]}),flush=True)

if __name__=="__main__":
    main()
