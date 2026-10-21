"""Single-hint ablation: WRITE/QUERY alignment only vs read-slot diversity only.
Existing shared, original, combined reference arms were trained using exactly
this seed/data/update protocol. CPU-only, 6 threads, no GPU.
"""
from __future__ import annotations
import os,sys,time,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):os.environ[k]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from write_read_alignment import build,address_distributions,address_probe
from learned_address import evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"single_hint_results.json"
CKPT=ROOT/"single_hint_weights.pt"
SEEDS=(17,29,43);SLOTS=(2,4,8)
ARMS=("align_only","diversity_only")
UPDATES=240

def hint(model,slots,arm):
    write,read=address_distributions(model,slots)
    if arm=="align_only":
        # Privileged correspondence: WRITE_i and QUERY_i address same fact.
        return 0.6*((write-read)**2).sum(1).mean()
    eye=torch.eye(slots,device=read.device)
    # No WRITE/QUERY pairing labels, but uses known set of query IDs.
    return 0.4*((read@read.T-eye)**2).mean()

def main():
    if OUT.exists() or CKPT.exists():raise FileExistsError("Refusing overwrite")
    torch.set_num_threads(6);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("CUDA unexpectedly visible")
    torch.manual_seed(0)
    start=time.monotonic()
    out={"protocol":{"seeds":SEEDS,"facts":SLOTS,"arms":ARMS,
       "updates":UPDATES,"batch":12,"eval_delays":[16,64,256],
       "heldout_histories":96,"cpu_threads":6,"gpu":False,
       "align_weight":0.6,"diversity_weight":0.4,
       "reference_arms":"write_read_alignment_results.json plus alignment_seed43_results.json"},
       "caveat":"align_only has privileged WRITE_i-to-QUERY_i pairing; diversity_only only query-token coverage structure; neither represents unconstrained language memory.",
       "runs":[],"complete":False}
    weights={}
    for seed in SEEDS:
        for slots in SLOTS:
            for arm in ARMS:
                model=build("shared",slots,seed)
                opt=torch.optim.AdamW(model.parameters(),lr=.003)
                losses=[];penalties=[]
                t0=time.monotonic()
                for step in range(UPDATES):
                    x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                    ids=query_histories(x,slots)
                    logits=model(ids).reshape(slots,len(x),2).transpose(0,1)
                    ce=F.cross_entropy(logits.reshape(-1,2),y.reshape(-1))
                    aux=hint(model,slots,arm)
                    total=ce+aux
                    if not torch.isfinite(total).item():raise RuntimeError("Nonfinite")
                    opt.zero_grad(set_to_none=True);total.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    opt.step()
                    losses.append(float(ce.detach()));penalties.append(float(aux.detach()))
                evseed=900000000+seed*100003+slots*197
                row={"seed":seed,"facts":slots,"arm":arm,
                  "parameters":sum(v.numel() for v in model.parameters()),
                  "train_seconds":round(time.monotonic()-t0,3),
                  "final_loss":round(sum(losses[-20:])/20,5),
                  "final_aux":round(sum(penalties[-20:])/20,5),
                  "address":address_probe(model,slots),
                  "eval":{str(delay):evaluation(model,slots,delay,evseed,96)
                        for delay in (16,64,256)}}
                out["runs"].append(row)
                weights[f"{seed}_{slots}_{arm}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                OUT.write_text(json.dumps(out,indent=2),encoding="utf8")
                print("SINGLE_HINT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(weights,CKPT)
    out["complete"]=True
    out["elapsed_seconds"]=round(time.monotonic()-start,3)
    out["weights_file"]=CKPT.name
    OUT.write_text(json.dumps(out,indent=2),encoding="utf8")
    print("SINGLE_HINT_COMPLETE="+json.dumps({"runs":len(out["runs"]),"seconds":out["elapsed_seconds"]}),flush=True)

if __name__=="__main__":main()
