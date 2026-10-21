"""Read-only address mapping diagnostics from saved causal models."""
from __future__ import annotations
import os,sys,json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["OMP_NUM_THREADS"]="4"
os.environ["MKL_NUM_THREADS"]="4"
os.environ["OPENBLAS_NUM_THREADS"]="4"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN
from prototypes.rnn_llm_architecture.capacity_010 import WRITE_START, QUERY_START, VALUE_START
HERE=Path(__file__).resolve().parent
OUT=HERE/"address_diagnostic.json"
if OUT.exists():raise FileExistsError(OUT)
torch.set_num_threads(4)
with torch.no_grad():
    weights=torch.load(HERE/"causal_weights.pt",map_location="cpu",weights_only=True)
    result={"scope":"posthoc learned address mapping of individual tag embeddings; no retraining","runs":[]}
    for seed in (17,29):
        for slots in (2,4,8):
            model=LearnedMemoryRNN(slots,seed=seed)
            model.load_state_dict(weights[f"{seed}-{slots}"])
            model.eval()
            keys=F.normalize(model.keys,dim=-1)
            writes=model.embedding.weight[WRITE_START:WRITE_START+slots]
            queries=model.embedding.weight[QUERY_START:QUERY_START+slots]
            wk=F.normalize(model.write_key(writes),dim=-1)
            qk=F.normalize(model.read_key(queries),dim=-1)
            wp=F.softmax(8*(wk@keys.T),dim=-1)
            qp=F.softmax(8*(qk@keys.T),dim=-1)
            wids=wp.argmax(-1).tolist()
            qids=qp.argmax(-1).tolist()
            vals=model.embedding.weight[VALUE_START:VALUE_START+2]
            gates=[]
            for i in range(slots):
                a=writes[i:i+1].expand(2,-1)
                pair=torch.cat((a,vals),dim=-1)
                gates.append(round(float(torch.sigmoid(model.gate(pair)).mean()),4))
            row={"seed":seed,"slots":slots,"write_slot_argmax":wids,"query_slot_argmax":qids,
                 "unique_write_destinations":len(set(wids)),
                 "unique_read_destinations":len(set(qids)),
                 "matched_write_read_tags":sum(int(a==b) for a,b in zip(wids,qids)),
                 "mean_write_confidence":round(float(wp.max(-1).values.mean()),4),
                 "mean_read_confidence":round(float(qp.max(-1).values.mean()),4),
                 "write_gate_means_by_slot":gates}
            result["runs"].append(row)
            print("ADDRESS_CHECK="+json.dumps(row,separators=(",",":")),flush=True)
    OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    print("ADDRESS_DIAGNOSTIC_COMPLETE="+str(OUT),flush=True)
