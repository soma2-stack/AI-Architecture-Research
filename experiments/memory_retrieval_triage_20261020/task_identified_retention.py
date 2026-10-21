"""Task-identifiable two-mapping retention pilot.
Two DISJOINT query vocabularies: old QUERY_0..7=14..21, new QUERY_B_0..7=32..39.
Old QUERY_i means WRITE_i; new QUERY_B_i means WRITE_((i+3)%8).
Both are learnable from answer CE only, no explicit pairing loss.
Contrasting new-only and 50/50 rehearsal after matched pretrained checkpoints.
Six CPU threads, CUDA hidden. Existing checkpoints and reports never overwritten.
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
import torch.nn as nn
import torch.nn.functional as F
from write_read_alignment import build
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories,QUERY_START,VOCAB

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"task_identified_retention_results.json"
WEIGHTS=ROOT/"task_identified_retention_weights.pt"
SEEDS=(17,29,43)
SLOTS=8
SHIFT=3
TASK_B_START=VOCAB   # first eight tokens beyond the old vocabulary
STEPS=240
BATCH_SIZE=12
HISTORIES=96
ARMS=("new_only","rehearsal")
SOURCES=("faded_pretrain","unguided_pretrain")

def source_file(seed,src):
    if src=="faded_pretrain":
        return ROOT/"faded_guidance_weights.pt",f"{seed}_{SLOTS}_linear_fade"
    return (ROOT/("alignment_seed43_weights.pt" if seed==43 else "write_read_alignment_weights.pt"),
            f"{seed}_{SLOTS}_shared")

def setup(seed,src):
    path,key=source_file(seed,src)
    weights=torch.load(path,map_location="cpu",weights_only=True)
    model=build("shared",SLOTS,seed)
    model.load_state_dict(weights[key],strict=True)
    old=model.embedding.weight.detach().clone()
    assert len(old)==VOCAB==32 and old.shape[1]==32
    newembed=nn.Embedding(TASK_B_START+SLOTS,old.shape[1])
    with torch.no_grad():
        newembed.weight[:VOCAB].copy_(old)
        # Start B symbols with the old query embeddings. They do NOT already
        # encode the shifted B target mapping, which must be learned via CE.
        newembed.weight[TASK_B_START:TASK_B_START+SLOTS].copy_(
            old[QUERY_START:QUERY_START+SLOTS])
    model.embedding=newembed
    assert model.read_key is model.write_key
    return model, path.name, key

def inputs(x,task):
    ids=query_histories(x,SLOTS)
    if task=="B":
        ids=ids.clone()
        ids[:,-1]=TASK_B_START+(ids[:,-1]-QUERY_START)
    return ids

def targets(y,task):
    if task=="B":
        # B_i is a new token with unambiguous truth WRITE_(i+SHIFT)%8.
        return y[:,[(i+SHIFT)%SLOTS for i in range(SLOTS)]]
    return y

def logits(model,x,task):
    ids=inputs(x,task)
    return model(ids).reshape(SLOTS,len(x),2).transpose(0,1)

def loss_on(model,x,y,task):
    return F.cross_entropy(logits(model,x,task).reshape(-1,2),
                           targets(y,task).reshape(-1))

@torch.no_grad()
def eval_one(model,seed,task,delay=256):
    model.eval()
    cbits=0;cwhole=0
    for start in range(0,HISTORIES,16):
        x,y=batch(SLOTS,delay,min(16,HISTORIES-start),
                  960000000+seed*100003+SLOTS*197+start*677)
        correct=logits(model,x,task).argmax(-1).eq(targets(y,task))
        cbits+=int(correct.sum())
        cwhole+=int(correct.all(1).sum())
    return {"bit":round(cbits/(HISTORIES*SLOTS),5),
            "whole":round(cwhole/HISTORIES,5),"histories":HISTORIES}

def eval_pair(model,seed):
    return {"old":eval_one(model,seed,"A"),"new":eval_one(model,seed,"B")}

def main():
    if OUT.exists() or WEIGHTS.exists():
        raise FileExistsError("Refusing to overwrite previous task-identified results")
    for seed in SEEDS:
        for src in SOURCES:
            path,_=source_file(seed,src)
            if not path.is_file():raise FileNotFoundError(path)
    torch.set_num_threads(6)
    torch.set_num_interop_threads(1)
    if torch.cuda.is_available():
        raise RuntimeError("GPU visible; abort")
    torch.manual_seed(0)
    result={"protocol":{"seeds":SEEDS,"sources":SOURCES,"arms":ARMS,
        "slots":SLOTS,"old_queries":"14..21, old_i means WRITE_i",
        "new_queries":"32..39, new_i means WRITE_(i+3 mod 8)",
        "no_ambiguous_token_targets":True,"explicit_query_task_identity":True,
        "new_query_tokens_initialized_as_copies_of_old_query_tokens":True,
        "old_query_tokens_and_embeddings_preserved_at_initialization":True,
        "answer_cross_entropy_only":True,"explicit_correspondence_guidance":False,
        "updates":STEPS,"batch_per_half":BATCH_SIZE,
        "total_histories_per_update":2*BATCH_SIZE,
        "new_only_batches":"two independent B batches each update",
        "rehearsal_batches":"one B and one A batch each update",
        "eval_delay":256,"histories_per_task":HISTORIES,
        "cpu_threads":6,"gpu":False,"learning_rate":0.003},
        "caveat":"Separate task-specific query tokens provide extra learnable embeddings (8x32 parameters); this is a controlled identifiable retention test, NOT zero-shot symbol generalization.",
        "runs":[],"complete":False}
    saved={}
    started=time.monotonic()
    # Check ground-truth remapping explicitly.
    yy=torch.arange(SLOTS).view(1,SLOTS)
    assert targets(yy,"B").tolist()[0]==[(i+SHIFT)%SLOTS for i in range(SLOTS)]
    for seed in SEEDS:
        for src in SOURCES:
            for arm in ARMS:
                model,source,key=setup(seed,src)
                before=eval_pair(model,seed)
                opt=torch.optim.AdamW(model.parameters(),lr=.003)
                timer=time.monotonic();losses=[]
                for step in range(STEPS):
                    # Identical primary B training stream for both arms.
                    x_b,y_b=batch(SLOTS,16,BATCH_SIZE,
                         1300000000+seed*1000003+step*8191+SLOTS*197)
                    # Second batch: old facts during rehearsal, otherwise
                    # independently generated new-task facts.
                    x_2,y_2=batch(SLOTS,16,BATCH_SIZE,
                         1500000000+seed*1000003+step*9173+SLOTS*197)
                    task2="A" if arm=="rehearsal" else "B"
                    model.train()
                    objective=(loss_on(model,x_b,y_b,"B")+
                               loss_on(model,x_2,y_2,task2))/2
                    if not torch.isfinite(objective).item():
                        raise RuntimeError("Nonfinite loss")
                    opt.zero_grad(set_to_none=True)
                    objective.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    opt.step()
                    losses.append(float(objective.detach()))
                after=eval_pair(model,seed)
                row={"seed":seed,"source":src,"arm":arm,
                    "checkpoint_file":source,"checkpoint_key":key,
                    "parameters":sum(p.numel() for p in model.parameters()),
                    "training_wall_seconds":round(time.monotonic()-timer,3),
                    "initial_ce":round(sum(losses[:20])/20,5),
                    "final_ce":round(sum(losses[-20:])/20,5),
                    "before":before,"after":after}
                result["runs"].append(row)
                saved[f"{seed}_{src}_{arm}"]={
                    k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
                print("TASK_IDENT_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(saved,WEIGHTS)
    result["complete"]=True
    result["elapsed_seconds"]=round(time.monotonic()-started,3)
    OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    print("TASK_IDENT_COMPLETE="+json.dumps({"runs":len(result["runs"]),"seconds":result["elapsed_seconds"]}),flush=True)

if __name__=="__main__":main()
