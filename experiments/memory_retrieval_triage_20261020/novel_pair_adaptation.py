"""Can pretrained neural memory relearn a NEW query->write pairing from end-task labels alone?
Eight already-seen WRITE and QUERY token IDs, but entirely unseen shifted correspondence.
This is ADAPTATION, not zero-shot generalization or truly novel vocabulary.
Use paired starting checkpoints from previous guided-fade and unguided shared-key runs.
All optimization after remapping uses ONLY answer CE; no address or identity labels.
"""
from __future__ import annotations
import os,sys,json,time
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):
    os.environ[k]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
import torch.nn.functional as F
from write_read_alignment import build,address_probe
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories,QUERY_START

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"novel_pair_adaptation_results.json"
WEIGHTS=ROOT/"novel_pair_adaptation_weights.pt"
SEEDS=(17,29,43)
ARMS=("faded_pretrain","unguided_pretrain")
SLOTS=8
SHIFT=3  # Derangement of all eight logical query identities.
STEPS=240
BATCH_SIZE=12
EVAL_N=96

def load_start(seed,arm):
    if arm=="faded_pretrain":
        src=ROOT/"faded_guidance_weights.pt"
        key=f"{seed}_{SLOTS}_linear_fade"
    else:
        src=(ROOT/"alignment_seed43_weights.pt" if seed==43 else ROOT/"write_read_alignment_weights.pt")
        key=f"{seed}_{SLOTS}_shared"
    ckpt=torch.load(src,map_location="cpu",weights_only=True)
    model=build("shared",SLOTS,seed)
    model.load_state_dict(ckpt[key],strict=True)
    return model,src.name,key

def tokens(history,shifted):
    ids=query_histories(history,SLOTS)
    if shifted:
        ids=ids.clone()
        # The underlying WRITE slot has not changed. Only the QUERY SYMBOL
        # for it changes; no oracle address enters model.forward().
        ids[:,-1]=QUERY_START+(ids[:,-1]-QUERY_START+SHIFT)%SLOTS
    return ids

@torch.no_grad()
def evaluate(model,seed,shifted,delay=256):
    model.eval()
    total_bit=0;total_whole=0
    for start in range(0,EVAL_N,16):
        x,y=batch(SLOTS,delay,min(16,EVAL_N-start),
                  970000000+seed*100003+SLOTS*197+start*677)
        logits=model(tokens(x,shifted)).reshape(SLOTS,len(x),2).transpose(0,1)
        ok=logits.argmax(-1).eq(y)
        total_bit+=int(ok.sum());total_whole+=int(ok.all(1).sum())
    return {"bit":round(total_bit/(EVAL_N*SLOTS),5),
            "whole":round(total_whole/EVAL_N,5),"histories":EVAL_N}

def evaluation_pair(model,seed):
    return {"old_pairs":evaluate(model,seed,False),
            "new_pairs":evaluate(model,seed,True)}

def main():
    if OUT.exists() or WEIGHTS.exists():
        raise FileExistsError("Refusing to overwrite existing new-pair experiment")
    for seed in SEEDS:
        for arm in ARMS:
            source=("faded_guidance_weights.pt" if arm=="faded_pretrain" else
                    ("alignment_seed43_weights.pt" if seed==43 else "write_read_alignment_weights.pt"))
            if not (ROOT/source).is_file():
                raise FileNotFoundError(source)
    torch.set_num_threads(6);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():
        raise RuntimeError("GPU must be hidden")
    torch.manual_seed(0)
    results={"protocol":{"seeds":SEEDS,"arms":ARMS,"facts":SLOTS,
        "novel_mapping":"QUERY_(i+3 mod 8) denotes WRITE_i",
        "previously_seen_tokens":True,
        "all_eight_correspondences_unseen_in_pretraining":True,
        "new_mapping_end_task_labels_during_adaptation":True,
        "explicit_new_mapping_supervision":False,
        "optimizer_updates":STEPS,"batch_size":BATCH_SIZE,
        "heldout_histories":EVAL_N,"eval_delay":256,
        "cpu_threads":6,"gpu":False,"lr":0.003,
        "checkpoint_sources":"faded_guidance_weights.pt, write_read_alignment_weights.pt, alignment_seed43_weights.pt"},
        "limitation":"Adapting to unseen correspondence among already-seen tokens using answer labels is NOT zero-shot autonomy or held-out vocabulary generalization.",
        "runs":[],"complete":False}
    weights={}
    started=time.monotonic()
    for seed in SEEDS:
        for arm in ARMS:
            model,source,key=load_start(seed,arm)
            before=evaluation_pair(model,seed)
            optimizer=torch.optim.AdamW(model.parameters(),lr=.003)
            train_t=time.monotonic();losses=[]
            model.train()
            for step in range(STEPS):
                x,y=batch(SLOTS,16,BATCH_SIZE,
                          1200000000+seed*1000003+step*8191+SLOTS*197)
                pred=model(tokens(x,True)).reshape(SLOTS,len(x),2).transpose(0,1)
                loss=F.cross_entropy(pred.reshape(-1,2),y.reshape(-1))
                if not bool(torch.isfinite(loss)):
                    raise RuntimeError("Nonfinite")
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                optimizer.step()
                losses.append(float(loss.detach()))
            after=evaluation_pair(model,seed)
            row={"seed":seed,"arm":arm,"source":source,"checkpoint_key":key,
                "parameters":sum(v.numel() for v in model.parameters()),
                "steps":STEPS,"train_wall_seconds":round(time.monotonic()-train_t,3),
                "training_loss_first20":round(sum(losses[:20])/20,5),
                "training_loss_last20":round(sum(losses[-20:])/20,5),
                "before":before,"after":after,"address_after":address_probe(model,SLOTS)}
            results["runs"].append(row)
            weights[f"{seed}_{arm}"]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
            OUT.write_text(json.dumps(results,indent=2),encoding="utf8")
            print("NOVEL_PAIR_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(weights,WEIGHTS)
    results["complete"]=True
    results["seconds"]=round(time.monotonic()-started,3)
    OUT.write_text(json.dumps(results,indent=2),encoding="utf8")
    print("NOVEL_PAIR_COMPLETE="+json.dumps({"runs":len(results["runs"]),"seconds":results["seconds"]}),flush=True)

if __name__=="__main__":
    main()
