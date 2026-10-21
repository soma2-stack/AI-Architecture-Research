"""Corrected drift diagnostic: only the guaranteed no-write tail counts.
No parameter updates, 6 CPU threads, no GPU. Saved fade checkpoints only.
"""
import os,sys,time,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):os.environ[k]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from write_read_alignment import build
from run import batch

HERE=Path(__file__).resolve().parent
OUT=HERE/"false_write_probe_corrected_results.json"
if OUT.exists():raise FileExistsError("Keep prior false-write evidence")
torch.set_num_threads(6);torch.set_num_interop_threads(1)
if torch.cuda.is_available():raise RuntimeError("GPU access unexpected")
weights=torch.load(HERE/"faded_guidance_weights.pt",map_location="cpu",weights_only=True)
data={"scope":"No parameter updates, guaranteed-no-write 16-to-N tail token region",
      "seeds":[17,29,43],"arms":["linear_fade","fade_by_half"],
      "histories":8,"delays":[256,1024,4096],
      "runs":[],"complete":False}
start=time.monotonic()
@torch.no_grad()
def run_probe(model,x,body_len):
    embeddings=model.embedding(x)
    b,t=x.shape
    h=embeddings.new_zeros(b,model.gru.hidden_size)
    bank=embeddings.new_zeros(b,model.slots,model.memdim)
    prev=embeddings.new_zeros(b,embeddings.size(-1))
    keys=F.normalize(model.keys,dim=-1)
    before=None
    sum_gates=embeddings.new_zeros(())
    tail_count=0
    for j in range(t):
        cur=embeddings[:,j]
        h=model.gru(cur,h)
        pair=torch.cat((prev,cur),dim=-1)
        gate=torch.sigmoid(model.gate(pair))
        address=F.normalize(model.write_key(prev),dim=-1)
        probs=F.softmax(8*(address@keys.T),dim=-1)
        amount=gate[:,None,:]*probs[:,:,None]
        value=torch.tanh(model.value(cur))[:,None,:]
        bank=bank*(1-amount)+amount*value
        if j==body_len-1:before=bank.clone()
        if j>=body_len:
            sum_gates+=gate.mean()
            tail_count+=1
        prev=cur
    eps=1e-9
    base=before.reshape(b,-1);end=bank.reshape(b,-1)
    denom=(base.norm(dim=1)*end.norm(dim=1)).clamp_min(eps)
    cosine=((base*end).sum(1)/denom).mean()
    diff=(end-base).norm(dim=1)/(base.norm(dim=1)+eps)
    return {"mean_false_gate":round(float(sum_gates/tail_count),7),
            "cumulative_false_gate":round(float(sum_gates),4),
            "bank_cosine_vs_after_write_body":round(float(cosine),5),
            "relative_bank_change":round(float(diff.mean()),5),
            "tail_tokens":tail_count}
for seed in (17,29,43):
    for arm in ("linear_fade","fade_by_half"):
        model=build("guided_align",8,seed)
        model.load_state_dict(weights[f"{seed}_8_{arm}"])
        model.eval()
        evseed=900000000+seed*100003+8*197
        for delay in (256,1024,4096):
            x,y=batch(8,delay,8,evseed)
            body_len=x.size(1)-max(0,delay-16)
            row={"seed":seed,"arm":arm,"delay":delay,"body_tokens":body_len,**run_probe(model,x,body_len)}
            data["runs"].append(row)
            OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
            print("DRIFT="+json.dumps(row,separators=(",",":")),flush=True)
data["complete"]=True
data["elapsed_seconds"]=round(time.monotonic()-start,3)
OUT.write_text(json.dumps(data,indent=2),encoding="utf8")
print("DRIFT_COMPLETE="+json.dumps({"runs":len(data["runs"]),"seconds":data["elapsed_seconds"]}),flush=True)
