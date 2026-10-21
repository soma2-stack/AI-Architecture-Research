"""Preregistered small screen: learned slot writes and reads, no token-ID parser.
Reuses the prior memory triage task and evaluation. Only CPU, ≤4 threads.
The model sees token embeddings and their order; it does not receive WRITE IDs,
VALUE IDs, QUERY IDs, explicit addresses, or oracle write masks.
"""
import os,sys
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["OMP_NUM_THREADS"]="4"
os.environ["MKL_NUM_THREADS"]="4"
os.environ["OPENBLAS_NUM_THREADS"]="4"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
import argparse,json,random,time
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F
from run import batch,logit,ev
from prototypes.rnn_llm_architecture.capacity_010 import WRITE_START, VALUE_START

class LearnedMemoryRNN(nn.Module):
    """Learned write gate, address and value encoders, content read attention.
    Learns token semantics solely from end-task loss. Has a recurrent GRU state.
    Does NOT have any explicit token ID branching in forward.
    """
    def __init__(self, slots, width=32, memdim=12, seed=17):
        super().__init__()
        self.slots=slots
        self.memdim=memdim
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed+515)
            self.embedding=nn.Embedding(32,width)
            self.gru=nn.GRUCell(width,width)
            self.keys=nn.Parameter(torch.randn(slots,memdim)*.3)
            self.write_key=nn.Linear(width,memdim)
            self.read_key=nn.Linear(width,memdim)
            self.gate=nn.Sequential(nn.Linear(2*width,48),nn.Tanh(),nn.Linear(48,1))
            nn.init.constant_(self.gate[-1].bias,-2.)
            self.value=nn.Linear(width,memdim)
            self.head=nn.Linear(width+memdim,2)
        self.last_diagnostic=None

    def forward(self, ids, diagnostics=False):
        b,t=ids.shape
        x=self.embedding(ids)
        h=x.new_zeros(b,self.gru.hidden_size)
        memory=x.new_zeros(b,self.slots,self.memdim)
        old=x.new_zeros(b,x.shape[-1])
        gates=[]
        addresses=F.normalize(self.keys,dim=-1)
        for j in range(t):
            cur=x[:,j,:]
            h=self.gru(cur,h)
            pair=torch.cat([old,cur],dim=-1)
            gate=torch.sigmoid(self.gate(pair))
            key=F.normalize(self.write_key(old),dim=-1)
            probs=F.softmax(8*(key @ addresses.T),dim=-1)
            amount=gate[:,None,:]*probs[:,:,None]
            new_value=torch.tanh(self.value(cur))[:,None,:]
            memory=memory*(1-amount)+amount*new_value
            if diagnostics:gates.append(gate.squeeze(-1))
            old=cur
        q=F.normalize(self.read_key(x[:,-1]),dim=-1)
        attn=F.softmax(8*(q @ addresses.T),dim=-1)
        found=(attn[:,:,None]*memory).sum(1)
        pred=self.head(torch.cat((h,found),dim=-1))
        if diagnostics:return pred,torch.stack(gates,dim=1),attn
        return pred

def evaluation(model, slots, delay, seed, histories):
    model.eval()
    cbits=0;cwhole=0;cconstant=0
    with torch.no_grad():
        for start in range(0,histories,16):
            x,y=batch(slots,delay,min(16,histories-start),seed+start*677)
            from prototypes.rnn_llm_architecture.capacity_010 import query_histories
            all_ids=query_histories(x,slots)
            pred=model(all_ids).reshape(slots,len(x),2).transpose(0,1).argmax(-1)
            same=pred.eq(y)
            cbits+=int(same.sum());cwhole+=int(same.all(1).sum())
            cconstant+=int((pred.max(1).values==pred.min(1).values).sum())
    return dict(bit=round(cbits/(histories*slots),5),whole=round(cwhole/histories,5),
                constant=round(cconstant/histories,5),histories=histories)

def gate_probe(model,slots):
    """Audit-only: find whether learned gates discriminate actual write pairs."""
    from prototypes.rnn_llm_architecture.capacity_010 import query_histories
    x,_=batch(slots,16,64,707707)
    ids=query_histories(x[:8],slots)
    with torch.no_grad():
        _,gates,attn=model(ids,diagnostics=True)
    # This condition is used only AFTER training, for diagnostic labeling.
    prev=ids[:,:-1]
    curr=ids[:,1:]
    valid=(prev>=WRITE_START)&(prev<WRITE_START+slots)&(curr>=VALUE_START)&(curr<VALUE_START+2)
    vals=gates[:,1:]
    return {"marked_gate":round(float(vals[valid].mean()),4),
            "other_gate":round(float(vals[~valid].mean()),4),
            "max_query_attention":round(float(attn.max(1).values.mean()),4)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--steps",type=int,default=240)
    p.add_argument("--seeds",default="17,29")
    p.add_argument("--slots",default="2,4,8")
    p.add_argument("--histories",type=int,default=96)
    p.add_argument("--max-seconds",type=float,default=300)
    p.add_argument("--output",default=str(Path(__file__).with_name("learned_results.json")))
    a=p.parse_args()
    out=Path(a.output)
    if out.exists():raise FileExistsError(out)
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_available():raise RuntimeError("GPU unexpectedly accessible")
    start=time.monotonic()
    torch.manual_seed(0);random.seed(0)
    result={"protocol":{"steps":a.steps,"seeds":a.seeds,"slots":a.slots,"histories":a.histories,
                        "delays":[16,64,256],"cpu_threads":4,"cuda":False,
                        "oracle_addresses":False,"write_parser_in_forward":False},
            "warning":"pilot only, not equal compute/memory comparison; explicit oracle old hybrid and delta controls",
            "runs":[],"complete":False}
    for seed in map(int,a.seeds.split(",")):
        for slots in map(int,a.slots.split(",")):
            if time.monotonic()-start>a.max_seconds:
                result["stop_reason"]="wall_budget"
                out.write_text(json.dumps(result,indent=2),encoding="utf-8")
                print("BUDGET_STOP",flush=True)
                return
            model=LearnedMemoryRNN(slots,seed=seed)
            optim=torch.optim.AdamW(model.parameters(),lr=.003)
            losses=[]
            tic=time.monotonic()
            for step in range(a.steps):
                x,y=batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                from prototypes.rnn_llm_architecture.capacity_010 import query_histories
                ids=query_histories(x,slots)
                logits=model(ids).reshape(slots,len(x),2).transpose(0,1)
                loss=F.cross_entropy(logits.reshape(-1,2),y.reshape(-1))
                if not bool(torch.isfinite(loss)):raise RuntimeError("Nonfinite loss")
                optim.zero_grad(set_to_none=True);loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                optim.step()
                losses.append(float(loss.detach()))
            row={"seed":seed,"slots":slots,"steps":a.steps,
                 "parameters":sum(z.numel() for z in model.parameters()),
                 "state_scalars":32+slots*12,
                 "train_seconds":round(time.monotonic()-tic,2),
                 "initial_loss":round(sum(losses[:20])/20,5),
                 "final_loss":round(sum(losses[-20:])/20,5),
                 "gate_probe":gate_probe(model,slots),
                 "eval":{str(d):evaluation(model,slots,d,900000000+seed*100003+slots*197,a.histories)
                        for d in [16,64,256]}}
            result["runs"].append(row)
            out.write_text(json.dumps(result,indent=2),encoding="utf-8")
            print("LEARNED_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    result["complete"]=True;result["elapsed_seconds"]=round(time.monotonic()-start,2)
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("COMPLETE="+json.dumps({"runs":len(result["runs"]),"seconds":result["elapsed_seconds"]}),flush=True)

if __name__=="__main__":main()
