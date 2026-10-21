"""Matched CPU screen: unguided base, shared key, and guided write/read alignment.
The guided arm receives a privileged correspondence between WRITE_i and QUERY_i
during TRAINING. This is task-specific extra supervision, not autonomous discovery.
No oracle memory slots, gold writes, or labels enter model.forward at inference.
"""
from __future__ import annotations
import os,sys,time,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):
    os.environ[key]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN, evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories,WRITE_START,QUERY_START
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"write_read_alignment_results.json"
WEIGHTS=ROOT/"write_read_alignment_weights.pt"
SEEDS=(17,29)
SLOTS=(2,4,8)
ARMS=("original","shared","guided_align")
STEPS=240
MATCH_WEIGHT=0.6
SEPARATION_WEIGHT=0.4

def build(arm,slots,seed):
    model=LearnedMemoryRNN(slots,seed=seed)
    if arm!="original": model.read_key=model.write_key
    return model

def address_distributions(model,slots):
    ids=torch.arange(slots)
    keys=F.normalize(model.keys,dim=-1)
    w=F.normalize(model.write_key(model.embedding(ids+WRITE_START)),dim=-1)
    q=F.normalize(model.read_key(model.embedding(ids+QUERY_START)),dim=-1)
    return F.softmax(8*(w@keys.T),dim=-1),F.softmax(8*(q@keys.T),dim=-1)

def address_guidance(model,slots):
    # Supervised tag equivalence and coverage: privileged training guidance.
    wp,qp=address_distributions(model,slots)
    consistency=((wp-qp)**2).sum(dim=1).mean()
    eye=torch.eye(slots)
    # Penalize slots that collapse onto same destination.
    separation=((qp@qp.T-eye)**2).mean()
    return MATCH_WEIGHT*consistency+SEPARATION_WEIGHT*separation,consistency,separation

@torch.no_grad()
def address_probe(model,slots):
    w,q=address_distributions(model,slots)
    wi=w.argmax(dim=1).tolist()
    qi=q.argmax(dim=1).tolist()
    return {"write_ids":wi,"read_ids":qi,
            "unique_writes":len(set(wi)),"unique_reads":len(set(qi)),
            "paired_matches":sum(int(a==b) for a,b in zip(wi,qi))}

def run():
    if OUT.exists() or WEIGHTS.exists():
        raise FileExistsError("Refusing to overwrite existing alignment files")
    torch.set_num_threads(6);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("GPU unexpectedly visible")
    torch.manual_seed(0)
    start=time.monotonic()
    d={"protocol":{"arms":ARMS,"seeds":SEEDS,"slots":SLOTS,"steps":STEPS,
          "batch":12,"eval_histories":96,"delays":(16,64,256),
          "cpu_threads":6,"gpu":False,"lr":0.003,
          "guide_match_weight":MATCH_WEIGHT,
          "guide_separation_weight":SEPARATION_WEIGHT},
       "caveat":"guided_align uses explicit WRITE_i to QUERY_i pairing during training; baseline arms do not. Task-specific privileged supervision. No generalization claim.",
       "runs":[],"complete":False}
    weights={}
    for seed in SEEDS:
        for slots in SLOTS:
            for arm in ARMS:
                model=build(arm,slots,seed)
                optimizer=torch.optim.AdamW(model.parameters(),lr=0.003)
                losses=[];guides=[]
                t0=time.monotonic()
                for step in range(STEPS):
                    x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                    ids=query_histories(x,slots)
                    pred=model(ids).reshape(slots,len(x),2).transpose(0,1)
                    ce=F.cross_entropy(pred.reshape(-1,2),y.reshape(-1))
                    aux=address_guidance(model,slots)[0] if arm=="guided_align" else ce.new_zeros(())
                    loss=ce+aux
                    if not bool(torch.isfinite(loss)):raise RuntimeError("Nonfinite objective")
                    optimizer.zero_grad(set_to_none=True)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    optimizer.step()
                    losses.append(float(ce.detach()));guides.append(float(aux.detach()))
                eval_seed=900000000+seed*100003+slots*197
                row={"seed":seed,"slots":slots,"arm":arm,
                     "parameters":sum(p.numel() for p in model.parameters()),
                     "train_seconds":round(time.monotonic()-t0,3),
                     "final_CE":round(sum(losses[-20:])/20,5),
                     "final_aux":round(sum(guides[-20:])/20,5),
                     "addresses":address_probe(model,slots),
                     "eval":{str(delay):evaluation(model,slots,delay,eval_seed,96)
                             for delay in (16,64,256)}}
                d["runs"].append(row)
                weights[f"{seed}_{slots}_{arm}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                OUT.write_text(json.dumps(d,indent=2),encoding="utf8")
                print("ALIGNMENT_RUN="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(weights,WEIGHTS)
    d["complete"]=True
    d["elapsed_seconds"]=round(time.monotonic()-start,3)
    d["weights_file"]=WEIGHTS.name
    OUT.write_text(json.dumps(d,indent=2),encoding="utf8")
    print("ALIGNMENT_COMPLETE="+json.dumps({"runs":len(d["runs"]),"seconds":d["elapsed_seconds"]}),flush=True)

if __name__=="__main__":run()
