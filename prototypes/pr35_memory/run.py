"""Fixed CPU screen. Reuses PR23 task/labels/models; does not overwrite evidence."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import os
import platform
try:
    import resource
except ImportError:
    resource = None
import statistics
import subprocess
import time
from pathlib import Path
from functools import lru_cache
import torch
import torch.nn.functional as F
from prototypes.rnn_llm_architecture.capacity_010 import (
    generator_batch, replay, query_histories, metrics, last_marked_value,
    VALUE_START, VOCAB, FILLER_START)
from prototypes.rnn_llm_architecture.candidates import CandidateConfig, CandidateLanguageModel
from prototypes.rnn_llm_architecture.gated import GatedConfig, GatedLanguageModel
from .model import BalancedPairLanguageModel, PAIR_VARIANTS
from .precision import diagnostics

DELAYS = (16, 64, 256, 1024)
MODELS = ("pair_shared", "gru", "lstm", "gru_matched")

def count(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def build(name, width, seed):
    if name in PAIR_VARIANTS:
        return BalancedPairLanguageModel(width, seed, name)
    if name in ("gru", "lstm"):
        return GatedLanguageModel(GatedConfig(vocab_size=VOCAB, width=width, layers=1,
                                              cell_type=name, seed=seed))
    return CandidateLanguageModel(CandidateConfig(vocab_size=VOCAB, width=width, layers=1,
                                  protected_channels=width//4, cell_type=name, seed=seed))

@lru_cache(maxsize=None)
def matched_width(width):
    target = count(build("pair_shared", width, 0))
    # Before training; never pick a width from test accuracy.
    return min(range(2, 129), key=lambda w: (abs(count(build("gru", w, 0))-target), w))

def batch(slots, delay, size, seed):
    """PR23 updates confined to first16 distractors; then a true no-write hold.

    This prevents long-delay tests from quietly introducing recent answer writes.
    At16 the generator is unchanged. Longer evals differ from old PR23 evals.
    """
    x = generator_batch(slots, 2, 16, size, seed=seed)
    if delay > 16:
        g = torch.Generator().manual_seed(seed + 81_000_019)
        tail = torch.randint(FILLER_START, FILLER_START+8, (size, delay-16), generator=g)
        noise = torch.randint(VALUE_START, VALUE_START+2, tail.shape, generator=g)
        tail = torch.where(torch.rand(tail.shape, generator=g)<.25, noise, tail)
        x = torch.cat((x, tail), dim=1)
    return x, replay(x, slots, 2)

def logits(model, x, slots):
    raw = model(query_histories(x, slots))[0][:, -1, VALUE_START:VALUE_START+2]
    return raw.reshape(slots, len(x), 2).transpose(0, 1)

def _sha(tensor):
    return hashlib.sha256(tensor.detach().cpu().contiguous().numpy().tobytes()).hexdigest()

@torch.no_grad()
def evaluate(model, slots, delay, seed, histories=256, details=False):
    model.eval()
    x, y = batch(slots, delay, histories, seed)
    scores = torch.cat([logits(model, x[i:i+16], slots).float()
                        for i in range(0, histories, 16)])
    pred = scores.argmax(-1)
    result = metrics(pred, y, 2)
    result.update({"correct_bits": int(pred.eq(y).sum()), "total_bits": int(y.numel()),
                   "correct_records": int(pred.eq(y).all(1).sum()), "histories": histories,
                   "nominal_fact_bits": slots, "minimum_no_write_hold": delay-16,
                   "bits_correct": slots*result["per_slot"],
                   "excess_bits_correct": slots*max(0., 2*result["per_slot"]-1),
                   "constant_answer_fraction": float((pred.max(1).values==pred.min(1).values).float().mean()),
                   "last_write_whole": float(last_marked_value(x,slots,2)[:,None].eq(y).all(1).float().mean()),
                   "data_sha256": _sha(x), "labels_sha256": _sha(y),
                   "finite_logits": bool(torch.isfinite(scores).all())})
    return (result, scores, pred) if details else result

def resources(model, name, width):
    w, v = width, VOCAB
    # Linear multiply-accumulates only; exclude nonlinearities, norms, indexing.
    if name.startswith("pair"):
        c = model.cells[0]
        d = c.x_value.out_features
        mac = w*c.fast + w*c.fast + w*d + c.fast*d + w*c.pairs + d*c.pairs + v*w
        state = w
        effective = c.fast+c.pairs
    elif name in ("gru", "gru_matched", "lstm"):
        gates = 4 if name=="lstm" else 3
        mac = 2*gates*w*w + v*w
        state = 2*w if name=="lstm" else w
        effective = state
    else:
        mac = (3*w*w + 8*w*(w//4) + v*w) if name=="protected" else 2*w*w+v*w
        state=effective=w
    item=model.embedding.weight.element_size()
    return {"parameters":count(model), "parameter_bytes":sum(p.numel()*p.element_size() for p in model.parameters()),
            "buffer_bytes":sum(b.numel()*b.element_size() for b in model.buffers()),
            "state_scalars":state, "independent_state_scalars":effective, "state_bytes_per_example":state*item,
            "linear_MACs_per_token_estimate":mac,
            "MAC_scope":"linear layers plus tied head; excludes elementwise ops/norms; not measured FLOPs"}

@torch.no_grad()
def latency(model, slots, seed):
    x,_=batch(slots,64,8,seed)
    ids=query_histories(x,slots)
    model.eval()
    model(ids)
    values=[]
    for _ in range(3):
        start=time.perf_counter();model(ids);values.append(time.perf_counter()-start)
    return {"median_forward_ms":1000*statistics.median(values),
            "query_sequences":len(ids),"tokens_per_sequence":ids.shape[1]}

@torch.no_grad()
def precision_checks(model, slots, seed):
    out={}
    for delay in (64,1024):
        _, ref_scores, ref_pred=evaluate(model,slots,delay,seed,histories=128,details=True)
        rows={}
        for name in ("float64","bfloat16"):
            candidate=copy.deepcopy(model).to(dtype=getattr(torch,name))
            try:
                m, scores, pred=evaluate(candidate,slots,delay,seed,histories=128,details=True)
                rows[name]={"metrics":m,"prediction_disagreement":float(pred.ne(ref_pred).float().mean()),
                            "max_abs_logit_gap":float((scores-ref_scores).abs().max())}
            except (RuntimeError,TypeError) as exc:
                rows[name]={"status":"unsupported","error":str(exc)}
        out[str(delay)]=rows
    return out

def source_hashes():
    root=Path(__file__).resolve().parents[2]
    paths=list(Path(__file__).parent.glob("*.py"))
    old=root/"prototypes"/"rnn_llm_architecture"
    paths += [old/p for p in ("capacity_010.py","model.py","candidates.py","gated.py")]
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def run_one(name,width,slots,seed,args,deadline,outdir):
    actual=matched_width(width) if name=="gru_matched" else width
    model=build("gru" if name=="gru_matched" else name,actual,seed)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.002)
    stream=hashlib.sha256();windows=[];losses=[];status="complete";steps=0
    start=time.monotonic();cpu=time.process_time()
    for step in range(args.steps):
        if time.monotonic()>deadline:
            status="wall_budget";break
        x,y=batch(slots,16,args.batch,100_000_000+seed*1_000_003+step*8191+slots*197)
        stream.update(x.numpy().tobytes())
        model.train();optimizer.zero_grad(set_to_none=True)
        loss=F.cross_entropy(logits(model,x,slots).reshape(-1,2),y.reshape(-1))
        if not bool(torch.isfinite(loss)):
            status="nonfinite_loss";break
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
            status="nonfinite_gradient";break
        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        optimizer.step();steps+=1;losses.append(float(loss.detach()))
        if steps%100==0:
            windows.append({"step":steps,"loss":statistics.mean(losses[-100:]),"preclip_grad_norm":float(norm)})
    row={"model":name,"nominal_width":width,"actual_width":actual,"slots":slots,"seed":seed,
         "steps":steps,"requested_steps":args.steps,"status":status,"training_stream_sha256":stream.hexdigest(),
         "train_wall_s":time.monotonic()-start,"train_cpu_s":time.process_time()-cpu,"loss_windows":windows,
         "loss_first":losses[0] if losses else None,"loss_last":losses[-1] if losses else None,
         "resources":resources(model,name,actual),
         "train_query_token_positions":steps*args.batch*slots*(2*slots+17)}
    if name=="gru_matched":
        target=count(build("pair_shared",width,seed))
        row["parameter_match"]={"target":target,"relative_mismatch":(count(model)-target)/target}
    if steps==args.steps and status=="complete":
        evseed=9_000_000_000+seed*100_003+slots*197
        row["eval"]={str(d):evaluate(model,slots,d,evseed,args.histories) for d in DELAYS}
        row["latency"]=latency(model,slots,evseed+1)
        if width==32 and slots==4 and name in ("pair_shared","gru","lstm"):
            row["precision"]=precision_checks(model,slots,evseed+2)
    checkpoint=outdir/f"{name}-w{width}-s{slots}-seed{seed}.pt"
    if checkpoint.exists():raise FileExistsError(checkpoint)
    torch.save({"model":model.state_dict(),"model_name":name,"width":actual,"seed":seed,
                "steps":steps,"slots":slots,"code_commit":os.environ.get("GITHUB_SHA")},checkpoint)
    row["checkpoint"]=checkpoint.name
    return row

def jobs(seed):
    # Interleave architectures under identical conditions. No checkpoint selection.
    out=[(name,width,slots,seed) for width in (16,32,64) for slots in (2,4,8) for name in MODELS]
    out += [(n,32,4,seed) for n in ("tanh","protected","pair_direct","pair_contract","pair_no_retain")]
    return out

def execute(args):
    if args.output.exists():raise FileExistsError(args.output)
    args.output.mkdir(parents=True)
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True);torch.manual_seed(0)
    start=time.monotonic();deadline=start+args.max_seconds
    environment={"torch":torch.__version__,"python":platform.python_version(),"platform":platform.platform(),
                 "cpu":platform.processor(),"logical_cpus":os.cpu_count(),"threads":torch.get_num_threads(),
                 "cuda_build":torch.version.cuda,"cuda_visible":os.environ.get("CUDA_VISIBLE_DEVICES"),
                 "runner":os.environ.get("RUNNER_NAME"),"commit":os.environ.get("GITHUB_SHA")}
    result={"environment":environment,"args":vars(args).copy(),"sources":source_hashes(),"runs":[],"skipped":[],
            "theory_precision":diagnostics(),"scope":"exploratory recall screen; no theorem or novelty validation"}
    result["args"]["output"]=str(args.output)
    for i,job in enumerate(jobs(args.seed)):
        if time.monotonic()>deadline:
            result["skipped"]=[list(j) for j in jobs(args.seed)[i:]];break
        row=run_one(*job,args,deadline,args.output)
        result["runs"].append(row)
        # Complete machine-readable row in hosted log, including negative outcomes.
        print("RESULT_JSON="+json.dumps(row,allow_nan=False,separators=(",",":")),flush=True)
        with (args.output/"runs.jsonl").open("a",encoding="utf-8") as handle:
            handle.write(json.dumps(row,allow_nan=False)+"\n")
        if row["status"] in ("nonfinite_loss","nonfinite_gradient"):
            result["skipped"]=[list(j) for j in jobs(args.seed)[i+1:]];break
    result["elapsed_wall_s"]=time.monotonic()-start
    result["process_lifetime_peak_RSS_bytes"]=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 if resource is not None and platform.system()=="Linux" else None)
    result["RSS_scope"]="Linux process lifetime high-water; includes library/interpreter; not per-model peak"
    result["status"]="complete" if not result["skipped"] and all(r["steps"]==args.steps and r["status"]=="complete" for r in result["runs"]) else "incomplete"
    with (args.output/"results.json").open("x",encoding="utf-8") as handle:
        json.dump(result,handle,indent=2,allow_nan=False)
    print("RUN_META_JSON="+json.dumps({k:v for k,v in result.items() if k!="runs"},separators=(",",":")),flush=True)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--seed",type=int,choices=(17,29,43),required=True)
    p.add_argument("--steps",type=int,default=600)
    p.add_argument("--batch",type=int,default=12)
    p.add_argument("--histories",type=int,default=256)
    p.add_argument("--max-seconds",type=float,default=900)
    a=p.parse_args()
    if min(a.steps,a.batch,a.histories,a.max_seconds)<=0:p.error("positive budgets required")
    execute(a)

if __name__=="__main__":main()
