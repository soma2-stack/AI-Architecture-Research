"""Paired CPU diagnostic: baseline learned address vs shared read/write keys.
Only change is parameter tying; no true-address labels or token rules.
Six CPU intra-op threads, single inter-op thread, no GPU.
"""
import os, sys, json, time
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["OMP_NUM_THREADS"] = "6"
os.environ["MKL_NUM_THREADS"] = "6"
os.environ["OPENBLAS_NUM_THREADS"] = "6"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
from pathlib import Path
import torch
from torch.nn import functional as F
from learned_address import LearnedMemoryRNN, evaluation
from run import batch
from prototypes.rnn_llm_architecture.capacity_010 import query_histories
HERE = Path(__file__).resolve().parent
OUT = HERE / "shared_address_sixthreads.json"
CKPT = HERE / "shared_address_sixthreads.pt"

def construct(kind, slots, seed):
    model = LearnedMemoryRNN(slots, seed=seed)
    if kind == "shared":
        model.read_key = model.write_key
    return model

def run():
    if OUT.exists() or CKPT.exists():
        raise FileExistsError("Results exist; refusing to overwrite")
    torch.set_num_threads(6)
    torch.set_num_interop_threads(1)
    if torch.cuda.is_available():
        raise RuntimeError("GPU must be disabled")
    torch.manual_seed(0)
    start = time.monotonic()
    rows = []
    params = {"comparison": "learned address (separate read/write) vs shared projection",
              "seeds": [17,29], "slots": [2,4,8], "models": ["baseline","shared"],
              "steps": 240, "batch": 12, "eval_histories": 96,
              "eval_delays": [16,64,256], "cpu_threads": 6, "gpu": False,
              "lr": 0.003, "training_streams_matched": True}
    result = {"protocol": params, "rows": rows, "complete": False}
    checkpoints = {}
    for seed in params["seeds"]:
        for slots in params["slots"]:
            for kind in params["models"]:
                model = construct(kind, slots, seed)
                optimizer = torch.optim.AdamW(model.parameters(), lr=params["lr"])
                losses = []
                t0 = time.monotonic()
                for step in range(params["steps"]):
                    x,y = batch(slots,16,12,100000000+seed*1000003+step*8191+slots*197)
                    ids = query_histories(x,slots)
                    prediction = model(ids).reshape(slots,len(x),2).transpose(0,1)
                    loss = F.cross_entropy(prediction.reshape(-1,2),y.reshape(-1))
                    if not torch.isfinite(loss).item():
                        raise RuntimeError("Nonfinite loss")
                    optimizer.zero_grad(set_to_none=True)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    optimizer.step()
                    losses.append(float(loss.detach()))
                evseed = 900000000+seed*100003+slots*197
                tests = {str(d): evaluation(model,slots,d,evseed,96) for d in [16,64,256]}
                row = {"seed":seed,"slots":slots,"model":kind,
                       "parameters":sum(p.numel() for p in model.parameters()),
                       "elapsed_training_s":round(time.monotonic()-t0,3),
                       "loss_last_20":round(sum(losses[-20:])/20,5),
                       "eval":tests}
                rows.append(row)
                checkpoints[f"{seed}_{slots}_{kind}"]={n:p.detach().cpu().clone()
                                  for n,p in model.state_dict().items()}
                OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
                print("PAIRED_RESULT="+json.dumps(row,separators=(",",":")),flush=True)
    torch.save(checkpoints,CKPT)
    result["complete"] = True
    result["elapsed_s"] = round(time.monotonic()-start,3)
    result["checkpoint"] = CKPT.name
    OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    print("PAIRED_COMPLETE="+json.dumps({"count":len(rows),"elapsed_s":result["elapsed_s"]}),flush=True)

if __name__ == "__main__":
    run()
