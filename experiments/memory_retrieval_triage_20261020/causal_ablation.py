"""Causal intervention on learned-address RNN memory; CPU only.
Six fresh training runs, same deterministic streams and updates as learned_address.py.
At held-out inference, intervene on existing states, without retraining.
"""
from __future__ import annotations
import os,sys,time,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"):
    os.environ[name]="4"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories

HERE=Path(__file__).resolve().parent
OUT=HERE/"causal_results.json"
WEIGHTS=HERE/"causal_weights.pt"
MODES=("normal","zero_bank","reverse_bank","uniform_read","zero_gru")

def states(model,ids):
    b,t=ids.shape
    x=model.embedding(ids)
    h=x.new_zeros(b,model.gru.hidden_size)
    bank=x.new_zeros(b,model.slots,model.memdim)
    old=x.new_zeros(b,x.shape[-1])
    keys=F.normalize(model.keys,dim=-1)
    for j in range(t):
        cur=x[:,j]
        h=model.gru(cur,h)
        gate=torch.sigmoid(model.gate(torch.cat((old,cur),dim=-1)))
        address=F.normalize(model.write_key(old),dim=-1)
        probs=F.softmax(8*(address@keys.T),dim=-1)
        amount=gate[:,None,:]*probs[:,:,None]
        proposed=torch.tanh(model.value(cur))[:,None,:]
        bank=bank*(1-amount)+amount*proposed
        old=cur
    q=F.normalize(model.read_key(x[:,-1]),dim=-1)
    attn=F.softmax(8*(q@keys.T),dim=-1)
    return h,bank,attn

def logits_from_states(model,h,bank,attn,mode):
    if mode=="zero_bank":bank=torch.zeros_like(bank)
    elif mode=="reverse_bank":bank=bank.flip(1)
    elif mode=="uniform_read":attn=torch.ones_like(attn)/model.slots
    elif mode=="zero_gru":h=torch.zeros_like(h)
    elif mode!="normal":raise ValueError(mode)
    read=(attn[:,:,None]*bank).sum(1)
    return model.head(torch.cat((h,read),dim=-1))

@torch.no_grad()
def evaluate(model, slots, seed, delay, histories=96):
    model.eval()
    stats={m:dict(bits=0,whole=0,changed=0) for m in MODES}
    max_logit_error=0.
    for i in range(0,histories,16):
        x,y=batch(slots,delay,min(16,histories-i),seed+i*677)
        ids=query_histories(x,slots)
        h,bank,attn=states(model,ids)
        preds={}
        for mode in MODES:
            logits=logits_from_states(model,h,bank,attn,mode)
            if mode=="normal":
                expected=model(ids)
                max_logit_error=max(max_logit_error,float((logits-expected).abs().max()))
                if max_logit_error>1.e-5:
                    raise RuntimeError("Causal reconstruction differs from original forward")
            lg=logits.reshape(slots,len(x),2).transpose(0,1)
            preds[mode]=lg.argmax(-1)
            correct=preds[mode].eq(y)
            stats[mode]["bits"]+=int(correct.sum())
            stats[mode]["whole"]+=int(correct.all(1).sum())
        for mode in MODES:
            stats[mode]["changed"]+=int(preds[mode].ne(preds["normal"]).sum())
    return {k:{"bit":round(v["bits"]/(slots*histories),5),
               "whole":round(v["whole"]/histories,5),
               "prediction_change":round(v["changed"]/(slots*histories),5),
               "correct_records":v["whole"]} for k,v in stats.items()},max_logit_error

def main():
    if OUT.exists() or WEIGHTS.exists():
        raise FileExistsError("Refusing to overwrite prior causal results or weights")
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    if torch.cuda.is_available():
        raise RuntimeError("Unexpected GPU access")
    torch.manual_seed(0)
    tic=time.monotonic()
    result={"protocol":{"seeds":[17,29],"slots":[2,4,8],"updates":240,
             "batch":12,"eval_delays":[64,256],"heldout_histories":96,
             "cpu_threads":4,"gpu":False,"intervention_only_at_evaluation":True},
            "runs":[],"complete":False}
    checkpoint={}
    for seed in (17,29):
        for slots in (2,4,8):
            trained=LearnedMemoryRNN(slots,seed=seed)
            optimizer=torch.optim.AdamW(trained.parameters(),lr=.003)
            losses=[]
            start=time.monotonic()
            for step in range(240):
                x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                ids=query_histories(x,slots)
                logits=trained(ids).reshape(slots,len(x),2).transpose(0,1)
                loss=F.cross_entropy(logits.reshape(-1,2),y.reshape(-1))
                if not bool(torch.isfinite(loss)):
                    raise RuntimeError("Nonfinite loss")
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(trained.parameters(),1.)
                optimizer.step()
                losses.append(float(loss.detach()))
            evseed=900000000+seed*100003+slots*197
            evals={}
            diffs={}
            for delay in (64,256):
                evals[str(delay)],diffs[str(delay)]=evaluate(trained,slots,evseed,delay)
            row={"seed":seed,"slots":slots,"train_wall_s":round(time.monotonic()-start,3),
                 "final_loss":round(sum(losses[-20:])/20,5),
                 "eval":evals,"normal_forward_max_logit_error":diffs}
            result["runs"].append(row)
            checkpoint[f"{seed}-{slots}"]={k:v.detach().cpu().clone()
                    for k,v in trained.state_dict().items()}
            OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
            print("ABLATION_RUN="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(checkpoint,WEIGHTS)
    result["complete"]=True
    result["elapsed_wall_s"]=round(time.monotonic()-tic,3)
    result["weights_file"]=WEIGHTS.name
    OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    print("ABLATION_COMPLETE="+json.dumps({
        "count":len(result["runs"]),"elapsed_wall_s":result["elapsed_wall_s"],
        "output":str(OUT)}),flush=True)
if __name__=="__main__":
    main()
