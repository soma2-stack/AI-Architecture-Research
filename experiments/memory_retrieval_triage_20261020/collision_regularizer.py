"""CPU-only matched experiment: learned address, shared, collision-regularized.
The new penalty uses final query tokens only, without true slot assignments.
"""
import os,sys,json,time,math
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):
    os.environ[k]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN,evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"collision_regularizer_results.json"
CKPT=ROOT/"collision_regularizer_weights.pt"
SEEDS=(17,29)
SLOTS=(2,4,8)
NAMES=("original","shared","collision_penalty")
STEPS=240
LAMBDA=0.4

def make(name,slots,seed):
    m=LearnedMemoryRNN(slots,seed=seed)
    if name!="original":
        m.read_key=m.write_key
    return m

def query_distribution(model,query_ids):
    z=model.embedding(query_ids)
    q=F.normalize(model.read_key(z),dim=-1)
    k=F.normalize(model.keys,dim=-1)
    return F.softmax(8*(q@k.T),dim=-1)

def collision_loss(model,ids):
    # Query tokens in input itself, not oracle memory-slot labels.
    query_ids=torch.unique(ids[:,-1],sorted=True)
    assert len(query_ids)==model.slots
    probs=query_distribution(model,query_ids)
    gram=probs@probs.T
    return ((gram-torch.eye(model.slots,device=gram.device))**2).mean()

@torch.no_grad()
def address_metrics(model,slots):
    from prototypes.rnn_llm_architecture.capacity_010 import QUERY_START,WRITE_START
    qtokens=torch.arange(QUERY_START,QUERY_START+slots)
    wtokens=torch.arange(WRITE_START,WRITE_START+slots)
    reads=query_distribution(model,qtokens).argmax(-1).tolist()
    write=F.normalize(model.write_key(model.embedding(wtokens)),dim=-1)
    keys=F.normalize(model.keys,dim=-1)
    writes=F.softmax(8*(write@keys.T),dim=-1).argmax(-1).tolist()
    return {"unique_read_slots":len(set(reads)),
            "unique_write_slots":len(set(writes)),
            "matching_write_read_slots":sum(a==b for a,b in zip(reads,writes)),
            "read_assignments":reads,"write_assignments":writes}

def main():
    if OUT.exists() or CKPT.exists():raise FileExistsError("Refuse to overwrite")
    torch.set_num_threads(6);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("GPU must be hidden")
    torch.manual_seed(0)
    start=time.monotonic()
    results={"protocol":{"seeds":SEEDS,"slots":SLOTS,"models":NAMES,
       "steps":STEPS,"batch":12,"heldout_histories":96,
       "eval_delays":[16,64,256],"cpu_threads":6,"gpu":False,
       "penalty_weight":LAMBDA,"extra_label_supervision":False},
       "runs":[],"complete":False}
    weights={}
    for seed in SEEDS:
        for slots in SLOTS:
            for name in NAMES:
                model=make(name,slots,seed)
                optim=torch.optim.AdamW(model.parameters(),lr=0.003)
                losses=[];penalties=[]
                tic=time.monotonic()
                for step in range(STEPS):
                    x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                    ids=query_histories(x,slots)
                    scores=model(ids).reshape(slots,len(x),2).transpose(0,1)
                    loss=F.cross_entropy(scores.reshape(-1,2),y.reshape(-1))
                    penalty=collision_loss(model,ids) if name=="collision_penalty" else loss.new_zeros(())
                    obj=loss+LAMBDA*penalty
                    if not torch.isfinite(obj).item():raise RuntimeError("Nonfinite loss")
                    optim.zero_grad(set_to_none=True)
                    obj.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    optim.step()
                    losses.append(float(loss.detach()));penalties.append(float(penalty.detach()))
                eval_seed=900000000+seed*100003+slots*197
                row={"seed":seed,"slots":slots,"model":name,
                    "parameters":sum(p.numel() for p in model.parameters()),
                    "train_seconds":round(time.monotonic()-tic,3),
                    "final_loss":round(sum(losses[-20:])/20,5),
                    "final_penalty":round(sum(penalties[-20:])/20,5),
                    "address":address_metrics(model,slots),
                    "eval":{str(d):evaluation(model,slots,d,eval_seed,96) for d in (16,64,256)}}
                results["runs"].append(row)
                weights[f"{seed}_{slots}_{name}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                OUT.write_text(json.dumps(results,indent=2),encoding="utf8")
                print("COLLISION_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(weights,CKPT)
    results["complete"]=True
    results["elapsed_seconds"]=round(time.monotonic()-start,3)
    results["checkpoint"]=CKPT.name
    OUT.write_text(json.dumps(results,indent=2),encoding="utf8")
    print("COLLISION_COMPLETE="+json.dumps({"runs":len(results["runs"]),
          "elapsed_seconds":results["elapsed_seconds"]}),flush=True)

if __name__=="__main__":main()
