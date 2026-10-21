"""Read-only probe: compare trained address collisions for original vs shared keys."""
from __future__ import annotations
import os, sys, json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["OMP_NUM_THREADS"]="6"
os.environ["MKL_NUM_THREADS"]="6"
os.environ["OPENBLAS_NUM_THREADS"]="6"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
from pathlib import Path
import torch
from torch.nn import functional as F
from shared_address_sixthreads import construct
from prototypes.rnn_llm_architecture.capacity_010 import WRITE_START,QUERY_START
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"shared_address_probe.json"
if OUT.exists():raise FileExistsError(OUT)
torch.set_num_threads(6)
saved=torch.load(ROOT/"shared_address_sixthreads.pt",map_location="cpu",weights_only=True)
stats=[]
with torch.no_grad():
    for seed in (17,29):
        for slots in (2,4,8):
            for kind in ("baseline","shared"):
                model=construct(kind,slots,seed)
                model.load_state_dict(saved[f"{seed}_{slots}_{kind}"])
                model.eval()
                code=F.normalize(model.keys,dim=-1)
                w=F.normalize(model.write_key(model.embedding.weight[WRITE_START:WRITE_START+slots]),dim=-1)
                q=F.normalize(model.read_key(model.embedding.weight[QUERY_START:QUERY_START+slots]),dim=-1)
                wp=F.softmax(8*(w@code.T),dim=-1)
                qp=F.softmax(8*(q@code.T),dim=-1)
                wi=wp.argmax(dim=-1).tolist()
                qi=qp.argmax(dim=-1).tolist()
                row={"seed":seed,"slots":slots,"model":kind,
                    "write_slots":wi,"query_slots":qi,
                    "unique_write":len(set(wi)),"unique_read":len(set(qi)),
                    "same_tag_write_read_matches":sum(a==b for a,b in zip(wi,qi)),
                    "write_confidence":round(float(wp.max(-1).values.mean()),4),
                    "read_confidence":round(float(qp.max(-1).values.mean()),4)}
                stats.append(row)
                print("PROBE="+json.dumps(row,separators=(",",":")),flush=True)
OUT.write_text(json.dumps({"scope":"read only; hard address argmax diagnostics after training","rows":stats},indent=2),encoding="utf8")
print("PROBE_COMPLETE=12",flush=True)
