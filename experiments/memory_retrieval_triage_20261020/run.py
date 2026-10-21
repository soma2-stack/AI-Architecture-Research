"""Small CPU-only diagnostic; reuses PR23 fact generator and PR36 cell.
No PR35 theorem claim. The hybrid/DeltaRule receive explicit write-grammar
parsing (strong task-specific inductive advantage). All models see same tokens.
"""
from __future__ import annotations
import os,sys
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["OMP_NUM_THREADS"]="4"
os.environ["MKL_NUM_THREADS"]="4"
os.environ["OPENBLAS_NUM_THREADS"]="4"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import argparse,json,time,math,random
import torch
from torch import nn
from torch.nn import functional as F
from prototypes.rnn_llm_architecture.capacity_010 import (
    generator_batch,replay,query_histories,metrics,DeltaRule,
    VALUE_START,FILLER_START,VOCAB,WRITE_START,QUERY_START)
from prototypes.rnn_llm_architecture.candidates import CandidateConfig,CandidateLanguageModel
from prototypes.rnn_llm_architecture.gated import GatedConfig,GatedLanguageModel

# Copied without altering the transition from PR36 model.py at commit 472ea492.
class BalancedPairCell(nn.Module):
    def __init__(self,width=32):
        super().__init__()
        self.width=width;self.latent=width//8
        self.pairs=2*self.latent-1;self.fast=width-2*self.pairs
        self.x_fast=nn.Linear(width,self.fast)
        self.h_fast=nn.Linear(width,self.fast,bias=False)
        self.x_value=nn.Linear(width,self.latent)
        self.h_value=nn.Linear(self.fast,self.latent,bias=False)
        self.x_gate=nn.Linear(width,self.pairs)
        nn.init.constant_(self.x_gate.bias,-3.)
        nn.init.orthogonal_(self.h_fast.weight)
        nodes=torch.linspace(-1,1,self.pairs,dtype=torch.float64)
        code=nodes[:,None]**torch.arange(self.latent,dtype=torch.float64)[None,:]
        code=code/code.norm(dim=1,keepdim=True)
        self.register_buffer("code",code.float())
    def prepare(self,x):
        return self.x_fast(x),self.x_value(x),torch.sigmoid(self.x_gate(x))
    def step(self,prepared,h,write_mask=None):
        f,r=self.fast,self.pairs
        p=.5*(h[...,f:f+r]-h[...,f+r:])
        drive,value,gate=prepared
        new_fast=torch.tanh(drive+self.h_fast(torch.cat((h[...,:f],p,-p),dim=-1)))
        proposal=torch.tanh(F.linear(torch.tanh(value+self.h_value(h[...,:f])),self.code))
        new_p=p+gate*(proposal-p)
        return torch.cat((new_fast,new_p,-new_p),dim=-1)

class PairNet(CandidateLanguageModel):
    def __init__(self,width,seed):
        super().__init__(CandidateConfig(vocab_size=VOCAB,width=width,layers=1,cell_type="tanh",seed=seed))
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed+101)
            self.cells=nn.ModuleList([BalancedPairCell(width)])

class AddressedHybrid(nn.Module):
    """GRU processing plus slot-addressable memory and attention readout.
    Has explicit WRITE-tag/VALUE-token parser, unlike the unrestricted GRU/pair.
    This is a known structured baseline, not a novel equivalent-compute competitor.
    """
    def __init__(self,slots,width=32,memdim=12,seed=17):
        super().__init__()
        self.slots=slots;self.width=width;self.memdim=memdim
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed+303)
            self.embedding=nn.Embedding(VOCAB,width)
            self.gru=nn.GRUCell(width,width)
            self.val_embed=nn.Embedding(2,memdim)
            self.addr=nn.Embedding(slots,memdim)
            self.gain=nn.Parameter(torch.tensor(2.))
            self.head=nn.Linear(width+memdim,2)
    def forward(self,ids):
        b,t=ids.shape
        h=self.embedding.weight.new_zeros(b,self.width)
        bank=self.embedding.weight.new_zeros(b,self.slots,self.memdim)
        pending=torch.full((b,),-1,dtype=torch.long,device=ids.device)
        for j in range(t):
            token=ids[:,j]
            h=self.gru(self.embedding(token),h)
            value=(token>=VALUE_START)&(token<VALUE_START+2)
            valid=value&(pending>=0)
            valuevec=self.val_embed((token-VALUE_START).clamp(0,1))
            # Controlled write to bank, with learnable value vector.
            mask=(pending[:,None]==torch.arange(self.slots,device=ids.device)[None,:])
            mask=(mask&valid[:,None]).unsqueeze(-1).to(bank.dtype)
            bank=bank*(1-mask)+mask*valuevec[:,None,:]
            pending=torch.where((token>=WRITE_START)&(token<WRITE_START+self.slots),
                                token-WRITE_START,-1)
        query=(ids[:,-1]-QUERY_START).clamp(0,self.slots-1)
        keys=F.normalize(self.addr.weight,dim=-1)
        q=keys[query]
        weights=F.softmax(torch.exp(self.gain.clamp(max=3.5))*(q@keys.T),dim=-1)
        read=(weights[:,:,None]*bank).sum(1)
        return self.head(torch.cat((h,read),dim=-1)),weights

def batch(slots,delay,size,seed):
    x=generator_batch(slots,2,16,size,seed=seed)
    if delay>16:
        g=torch.Generator().manual_seed(seed+81000019)
        tail=torch.randint(FILLER_START,FILLER_START+8,(size,delay-16),generator=g)
        noise=torch.randint(VALUE_START,VALUE_START+2,tail.shape,generator=g)
        tail=torch.where(torch.rand(tail.shape,generator=g)<.25,noise,tail)
        x=torch.cat((x,tail),dim=1)
    return x,replay(x,slots,2)

def make(name,slots,seed,width):
    if name=="gru":
        return GatedLanguageModel(GatedConfig(vocab_size=VOCAB,width=width,layers=1,cell_type="gru",seed=seed))
    if name=="pair":
        return PairNet(width,seed)
    if name=="hybrid":
        return AddressedHybrid(slots,width,seed=seed)
    if name=="delta":
        return DeltaRule(slots,2,seed)
    raise ValueError(name)

def logit(model,name,x,slots):
    ids=query_histories(x,slots)
    if name=="hybrid":
        raw=model(ids)[0]
    elif name=="delta":
        raw=model(ids)
    else:
        raw=model(ids)[0][:,-1,VALUE_START:VALUE_START+2]
    return raw.reshape(slots,len(x),2).transpose(0,1)

@torch.no_grad()
def ev(model,name,slots,delay,seed,histories):
    model.eval()
    correct=0;bits=0;whole=0;constant=0
    for i in range(0,histories,16):
        x,y=batch(slots,delay,min(16,histories-i),seed+i*677)
        pred=logit(model,name,x,slots).argmax(-1)
        match=pred.eq(y)
        correct+=int(match.sum());whole+=int(match.all(1).sum())
        constant+=int((pred.min(1).values==pred.max(1).values).sum())
        bits+=y.numel()
    return {"bit":round(correct/bits,5),"whole":round(whole/histories,5),
            "constant":round(constant/histories,5),"histories":histories}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--steps",type=int,default=180)
    p.add_argument("--batch",type=int,default=12)
    p.add_argument("--histories",type=int,default=64)
    p.add_argument("--seeds",default="17,29")
    p.add_argument("--slots",default="2,4")
    p.add_argument("--width",type=int,default=32)
    p.add_argument("--output",default=str(Path(__file__).with_name("results.json")))
    a=p.parse_args()
    if Path(a.output).exists():
        raise FileExistsError(f'Refusing to overwrite existing experiment: {a.output}')
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    torch.manual_seed(0);random.seed(0)
    if torch.cuda.is_available():raise RuntimeError("GPU should be invisible; abort")
    names=["gru","pair","hybrid","delta"]
    results={"scope":"diagnostic only; hybrid/delta have explicit grammar; not apples-to-apples architecture proof",
             "protocol":{"train_updates":a.steps,"batch":a.batch,"heldout_histories":a.histories,
                         "slots":a.slots,"seeds":a.seeds,"width":a.width,"eval_delays":[16,64,256],
                         "cpu_threads":torch.get_num_threads(),"cuda_visible":False},
             "runs":[]}
    start=time.monotonic()
    for seed in [int(s) for s in a.seeds.split(",")]:
        for slots in [int(s) for s in a.slots.split(",")]:
            for name in names:
                model=make(name,slots,seed,a.width)
                opt=torch.optim.AdamW(model.parameters(),lr=.002)
                losses=[];beg=time.monotonic()
                for step in range(a.steps):
                    x,y=batch(slots,16,a.batch,100000000+seed*1000003+step*8191+slots*197)
                    opt.zero_grad(set_to_none=True)
                    loss=F.cross_entropy(logit(model,name,x,slots).reshape(-1,2),y.reshape(-1))
                    if not bool(torch.isfinite(loss)):raise RuntimeError("nonfinite "+name)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    opt.step()
                    losses.append(float(loss.detach()))
                traintime=round(time.monotonic()-beg,2)
                evaluations={str(d):ev(model,name,slots,d,900000000+seed*100003+slots*197,a.histories)
                             for d in [16,64,256]}
                state_scalars=(a.width if name=="gru" else
                    a.width if name=="pair" else slots*12+a.width if name=="hybrid" else slots*32)
                row={"seed":seed,"slots":slots,"model":name,
                     "params":sum(v.numel() for v in model.parameters()),
                     "state_scalars":state_scalars,
                     "training_wall_seconds":traintime,
                     "initial_loss":round(sum(losses[:min(20,len(losses))])/min(20,len(losses)),4),
                     "final_loss":round(sum(losses[-min(20,len(losses)):])/min(20,len(losses)),4),
                     "evaluation":evaluations}
                results["runs"].append(row)
                with open(a.output,"w",encoding="utf8") as f:json.dump(results,f,indent=2)
                print("RESULT_JSON="+json.dumps(row,separators=(",",":")),flush=True)
    results["elapsed_seconds"]=round(time.monotonic()-start,2)
    results["complete"]=True
    with open(a.output,"w",encoding="utf8") as f:json.dump(results,f,indent=2)
    print("FINAL="+json.dumps({"runs":len(results["runs"]),"time":results["elapsed_seconds"],"file":a.output}),flush=True)
if __name__=="__main__":main()
