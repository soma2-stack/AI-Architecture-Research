"""Third independent seed for alignment experiment. CPU-only, six threads."""
import os,sys,time,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):os.environ[v]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
import torch.nn.functional as F
from write_read_alignment import build,address_guidance,address_probe,MATCH_WEIGHT,SEPARATION_WEIGHT
from learned_address import evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories

HERE=Path(__file__).resolve().parent
OUT=HERE/"alignment_seed43_results.json"
WEIGHTS=HERE/"alignment_seed43_weights.pt"

def main():
    if OUT.exists() or WEIGHTS.exists():raise FileExistsError("Previous third-seed artifacts exist")
    torch.set_num_threads(6)
    torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("GPU must be disabled")
    torch.manual_seed(0)
    seed=43
    beginning=time.monotonic()
    data={"protocol":{"seed":seed,"slots":[2,4,8],
         "arms":["original","shared","guided_align"],
         "updates":240,"batch_size":12,"eval_histories":96,
         "eval_delays":[16,64,256],"cpu_threads":6,"gpu":False,
         "guided_match_weight":MATCH_WEIGHT,"guided_diversity_weight":SEPARATION_WEIGHT},
         "caveat":"guided_align uses explicit WRITE_i/QUERY_i correspondence during training only",
         "runs":[],"complete":False}
    saved={}
    for slots in (2,4,8):
        for arm in ("original","shared","guided_align"):
            model=build(arm,slots,seed)
            opt=torch.optim.AdamW(model.parameters(),lr=.003)
            losses=[]
            start=time.monotonic()
            for step in range(240):
                x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                ids=query_histories(x,slots)
                scores=model(ids).reshape(slots,len(x),2).transpose(0,1)
                ce=F.cross_entropy(scores.reshape(-1,2),y.reshape(-1))
                extra=address_guidance(model,slots)[0] if arm=="guided_align" else ce.new_zeros(())
                loss=ce+extra
                if not torch.isfinite(loss).item():raise RuntimeError("Nonfinite loss")
                opt.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                opt.step()
                losses.append(float(ce.detach()))
            eval_seed=900000000+seed*100003+slots*197
            row={"seed":seed,"slots":slots,"arm":arm,
                 "parameter_count":sum(p.numel() for p in model.parameters()),
                 "training_wall_s":round(time.monotonic()-start,3),
                 "final_cross_entropy":round(sum(losses[-20:])/20,5),
                 "addresses":address_probe(model,slots),
                 "eval":{str(d):evaluation(model,slots,d,eval_seed,96) for d in (16,64,256)}}
            data["runs"].append(row)
            saved[f"{seed}_{slots}_{arm}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
            OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
            print("SEED43_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(saved,WEIGHTS)
    data["complete"]=True
    data["elapsed_seconds"]=round(time.monotonic()-beginning,3)
    data["weights_file"]=WEIGHTS.name
    OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
    print("SEED43_COMPLETE="+json.dumps({"runs":len(data["runs"]),"seconds":data["elapsed_seconds"]}),flush=True)

if __name__=="__main__":main()
