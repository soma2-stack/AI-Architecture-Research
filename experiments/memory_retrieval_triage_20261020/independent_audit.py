"""Independent audit plus one paired 2x2 inference intervention. No training.
Reproduce: python -B experiments/memory_retrieval_triage_20261020/independent_audit.py
Preserves all input files; refuses to overwrite its own output.
"""
from __future__ import annotations
import os, sys
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[key] = "6"
sys.dont_write_bytecode = True
import argparse, ast, hashlib, json, math, platform, statistics, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=ROOT / "independent_audit_results.json")
parser.add_argument("--validate-existing", action="store_true", help="Only validate long-horizon parity against original forward")
args = parser.parse_args()
OUT = args.output
VALIDATE_EXISTING = args.validate_existing
if OUT.exists() and not VALIDATE_EXISTING:
    raise FileExistsError(OUT)
ORIGINAL = sorted(p for p in ROOT.iterdir()
                  if p.is_file() and not p.name.startswith("independent_audit"))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
MANIFEST = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in ORIGINAL}
for p in ORIGINAL:
    if p.suffix == ".py":
        ast.parse(p.read_text(encoding="utf-8-sig"))
sys.path.insert(0, str(ROOT))
from write_read_alignment import build
from run import batch
from learned_address import LearnedMemoryRNN
from prototypes.rnn_llm_architecture.capacity_010 import query_histories
import torch
from torch import nn
from torch.nn import functional as F
torch.set_num_threads(6)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
torch.manual_seed(20261020)
assert not torch.cuda.is_available()
assert torch.get_num_threads() <= 6

REPORT = {
    "protocol": {
        "scope": "Independent checkpoint reproduction and ONE paired write-location intervention",
        "cpu_threads": 6, "interop_threads": 1, "gpu": False, "training_updates": 0,
        "experiment_seeds": [17, 29, 43], "experiment_checkpoints": ["linear_fade", "fade_by_half"],
        "experiment_delays": [256, 1024, 4096], "fresh_histories_per_seed": 96,
        "modes": ["normal", "freeze_tail", "freeze_query", "freeze_both"],
        "paired": "Same checkpoint and exactly the same histories in every mode",
        "fresh_eval_seed": "5000000000 + seed*100003 + 8*197 + chunk_start*677",
        "intervention": "oracle KNOWN no-write tail boundary; never a deployable autonomous improvement",
        "primary_falsification": "If freeze_tail restores whole recall >=20 points in each seed at4096, tail drift is a consistent contributor; no sole-cause claim",
        "unchanged": "GRU, read weights, parameters, query update except where specifically ablated",
        "max_wall_seconds": 360,
    },
    "environment": {"python": platform.python_version(), "torch": torch.__version__,
                    "cuda_hidden": os.environ["CUDA_VISIBLE_DEVICES"]},
    "inputs": MANIFEST, "json_inventory": [], "arithmetic_summaries": {},
    "checkpoint_inventory": [], "reproductions": [], "intervention": [], "complete": False,
}
PRIOR_WALL = PRIOR_CPU = 0.
if VALIDATE_EXISTING:
    REPORT = json.loads(OUT.read_text(encoding="utf-8"))
    REPORT["original_execution_source_sha256"] = "3f89b623d4930819156c551b268f95a8aa8669ccc855ac7387c3153f53289129"
    PRIOR_WALL = REPORT["elapsed_wall_s"]
    PRIOR_CPU = REPORT["process_cpu_s"]
START = time.monotonic()
CPU_START = time.process_time()
def budget():
    if time.monotonic() - START > 360:
        raise TimeoutError("Fixed 360s audit budget reached")
def save():
    REPORT["elapsed_wall_s"] = PRIOR_WALL + time.monotonic() - START
    REPORT["process_cpu_s"] = PRIOR_CPU + time.process_time() - CPU_START
    OUT.write_text(json.dumps(REPORT, indent=2, allow_nan=False), encoding="utf-8")

DOCS = {p.name: json.loads(p.read_text(encoding="utf-8-sig"))
        for p in ORIGINAL if p.suffix == ".json"}
for name, doc in DOCS.items():
    rows = doc.get("runs", doc.get("rows", []))
    REPORT["json_inventory"].append({"file": name, "rows": len(rows),
                                      "complete": doc.get("complete", "diagnostic_no_completion_field")})
def group_means(rows, keyfun, valfun):
    groups = {}
    for row in rows:
        groups.setdefault(keyfun(row), []).append(valfun(row))
    return {str(k): {"n": len(v), "mean": statistics.mean(v), "values": v}
            for k,v in groups.items()}
alignment = DOCS["write_read_alignment_results.json"]["runs"] + DOCS["alignment_seed43_results.json"]["runs"]
REPORT["arithmetic_summaries"]["alignment_256"] = group_means(
    alignment, lambda r:(r["slots"],r["arm"]), lambda r:r["eval"]["256"]["whole"])
REPORT["arithmetic_summaries"]["single_hint_256"] = group_means(
    DOCS["single_hint_results.json"]["runs"],lambda r:(r["facts"],r["arm"]),lambda r:r["eval"]["256"]["whole"])
REPORT["arithmetic_summaries"]["fade_256"] = group_means(
    DOCS["faded_guidance_results.json"]["runs"],lambda r:(r["slots"],r["arm"]),lambda r:r["eval"]["256"]["whole"])
REPORT["arithmetic_summaries"]["task_retention"] = group_means(
    DOCS["task_identified_retention_results.json"]["runs"],
    lambda r:(r["source"],r["arm"]),lambda r:r["after"]["old"]["whole"])
REPORT["arithmetic_summaries"]["task_new"] = group_means(
    DOCS["task_identified_retention_results.json"]["runs"],
    lambda r:(r["source"],r["arm"]),lambda r:r["after"]["new"]["whole"])
REPORT["arithmetic_summaries"]["explicit_256"] = group_means(
    DOCS["results.json"]["runs"],lambda r:(r["slots"],r["model"]),
    lambda r:r["evaluation"]["256"]["whole"])

@torch.no_grad()
def history_state(model, x):
    """Common query-free history once; original state equation, no parser."""
    emb = model.embedding(x)
    b = len(x)
    hidden = emb.new_zeros(b, model.gru.hidden_size)
    bank = emb.new_zeros(b, model.slots, model.memdim)
    prev = emb.new_zeros(b, emb.shape[-1])
    keys = F.normalize(model.keys, dim=-1)
    body = 2*model.slots+16
    body_bank = None
    for j in range(x.shape[1]):
        cur = emb[:,j]
        hidden = model.gru(cur, hidden)
        gate = torch.sigmoid(model.gate(torch.cat((prev,cur),-1)))
        probs = F.softmax(8*(F.normalize(model.write_key(prev),dim=-1)@keys.T),-1)
        amount = gate[:,None,:]*probs[:,:,None]
        value = torch.tanh(model.value(cur))[:,None,:]
        bank = bank*(1-amount)+amount*value
        if j == body-1:
            body_bank = bank.clone()
        prev = cur
    return hidden, bank, prev, body_bank

@torch.no_grad()
def query_logits(model, hidden, bank, prev, qids, allow_write=True):
    # Slot-major ordering exactly matches query_histories, including taskB tokens.
    b = len(hidden); s = len(qids)
    h = hidden.repeat(s,1)
    mem = bank.repeat(s,1,1)
    old = prev.repeat(s,1)
    cur = model.embedding(qids).repeat_interleave(b,0)
    h = model.gru(cur,h)
    keys = F.normalize(model.keys,dim=-1)
    if allow_write:
        gate = torch.sigmoid(model.gate(torch.cat((old,cur),-1)))
        probs = F.softmax(8*(F.normalize(model.write_key(old),dim=-1)@keys.T),-1)
        amount = gate[:,None,:]*probs[:,:,None]
        mem = mem*(1-amount)+amount*torch.tanh(model.value(cur))[:,None,:]
    attn = F.softmax(8*(F.normalize(model.read_key(cur),dim=-1)@keys.T),-1)
    found = (attn[:,:,None]*mem).sum(1)
    return model.head(torch.cat((h,found),-1)).reshape(s,b,2).transpose(0,1)

def state_digest(state):
    h = hashlib.sha256()
    for key,tensor in sorted(state.items()):
        h.update(key.encode()); h.update(str(tensor.shape).encode())
        h.update(tensor.contiguous().numpy().tobytes())
    return h.hexdigest()

CACHE = {}
@torch.no_grad()
def measure(model, slots, seed, delay=256, histories=96, qids=None, target_order=None):
    budget()
    qids = torch.arange(14,14+slots) if qids is None else torch.tensor(qids)
    target_order = list(range(slots)) if target_order is None else target_order
    cachekey=(state_digest(model.state_dict()),slots,seed,delay,histories,tuple(qids.tolist()),tuple(target_order))
    if cachekey in CACHE:
        return CACHE[cachekey], True
    bc=wc=constant=0; maxerr=0.; digest=hashlib.sha256()
    for start in range(0,histories,16):
        x,y=batch(slots,delay,min(16,histories-start),seed+start*677)
        digest.update(x.numpy().tobytes())
        st=history_state(model,x)
        scores=query_logits(model,*st[:3],qids)
        # Verify against original full forward, not merely another helper.
        if start==0:
            tiny=x[:2]
            refids=tiny.repeat(slots,1)
            refids=torch.cat((refids,qids.repeat_interleave(2)[:,None]),1)
            reference=model(refids).reshape(slots,2,2).transpose(0,1)
            ts=history_state(model,tiny)
            fast=query_logits(model,*ts[:3],qids)
            maxerr=float((fast-reference).abs().max())
            if maxerr>2e-5 or not torch.equal(fast.argmax(-1),reference.argmax(-1)):
                raise AssertionError(("prefix_cache_parity",maxerr))
        pred=scores.argmax(-1)
        ok=pred.eq(y[:,target_order])
        bc+=int(ok.sum());wc+=int(ok.all(1).sum())
        constant+=int((pred.min(1).values==pred.max(1).values).sum())
    result={"bit":bc/(histories*slots),"whole":wc/histories,
            "constant":constant/histories,"correct_bits":bc,"correct_records":wc,
            "histories":histories,"source_forward_max_logit_error":maxerr,
            "history_sha256":digest.hexdigest()}
    CACHE[cachekey]=result
    return result,False

FILES = {}
def checkpoint(name):
    if name not in FILES:
        FILES[name]=torch.load(ROOT/name,map_location="cpu",weights_only=True)
        states=FILES[name]
        REPORT["checkpoint_inventory"].append({
            "file":name,"states":len(states),
            "finite":all(bool(torch.isfinite(t).all()) for v in states.values() for t in v.values()),
            "state_digests":{key:state_digest(v) for key,v in states.items()}})
    return FILES[name]

def load_model(filename,key,slots,seed,shared=True):
    state=checkpoint(filename)[key]
    m=build("shared" if shared else "original",slots,seed)
    vocab=state["embedding.weight"].shape[0]
    if vocab !=32:
        m.embedding=nn.Embedding(vocab,32)
    m.load_state_dict(state,strict=True);m.eval()
    return m

def compare(label,model,slots,evseed,expected,delay=256,histories=96,qids=None,target_order=None):
    observed,cached=measure(model,slots,evseed,delay,histories,qids,target_order)
    keys=[k for k in ("bit","whole","constant") if k in expected]
    errors={k:abs(observed[k]-expected[k]) for k in keys}
    match=all(v<=5.01e-6 for v in errors.values())
    REPORT["reproductions"].append({"case":label,"match":match,"expected":expected,
                                    "observed":observed,"max_accuracy_error":max(errors.values()),
                                    "duplicate_reproduction_reused":cached})
    if not match:
        print("REPRO_MISMATCH",label,errors,flush=True)

def reproduce():
    specifications=[
        ("causal_results.json","causal_weights.pt","causal"),
        ("shared_address_sixthreads.json","shared_address_sixthreads.pt","shared"),
        ("collision_regularizer_results.json","collision_regularizer_weights.pt","collision"),
        ("write_read_alignment_results.json","write_read_alignment_weights.pt","alignment"),
        ("alignment_seed43_results.json","alignment_seed43_weights.pt","alignment"),
        ("single_hint_results.json","single_hint_weights.pt","hint"),
        ("faded_guidance_results.json","faded_guidance_weights.pt","fade"),
    ]
    for jf,wf,kind in specifications:
        d=DOCS[jf]
        for r in d.get("runs",d.get("rows",[])):
            slots=r.get("slots",r.get("facts"));seed=r["seed"]
            arm=r.get("arm",r.get("model","original"))
            key=f"{seed}-{slots}" if kind=="causal" else f"{seed}_{slots}_{arm}"
            shared=kind!="causal" and arm not in ("original","baseline")
            model=load_model(wf,key,slots,seed,shared)
            expected=r["eval"]["256"]["normal"] if kind=="causal" else r["eval"]["256"]
            compare(f"{jf}:{key}:256",model,slots,900000000+seed*100003+slots*197,expected)
        save();print("REPRODUCED",jf,flush=True)
    for r in DOCS["task_identified_retention_results.json"]["runs"]:
        seed=r["seed"];src=r["source"];arm=r["arm"]
        model=load_model("task_identified_retention_weights.pt",f"{seed}_{src}_{arm}",8,seed)
        evseed=960000000+seed*100003+8*197
        compare(f"task:{seed}:{src}:{arm}:old",model,8,evseed,r["after"]["old"])
        compare(f"task:{seed}:{src}:{arm}:new",model,8,evseed,r["after"]["new"],
                qids=list(range(32,40)),target_order=[(i+3)%8 for i in range(8)])
        # Reconstruct pre-adaptation inputs, including copied query embeddings.
        original=load_model(r["checkpoint_file"],r["checkpoint_key"],8,seed)
        old=original.embedding.weight.detach().clone()
        original.embedding=nn.Embedding(40,32)
        original.embedding.weight[:32].copy_(old)
        original.embedding.weight[32:].copy_(old[14:22])
        compare(f"task_before:{seed}:{src}:{arm}:old",original,8,evseed,r["before"]["old"])
        compare(f"task_before:{seed}:{src}:{arm}:new",original,8,evseed,r["before"]["new"],
                qids=list(range(32,40)),target_order=[(i+3)%8 for i in range(8)])
    save();print("REPRODUCED task_identified_retention",flush=True)
    for r in DOCS["novel_pair_adaptation_results.json"]["runs"]:
        model=load_model("novel_pair_adaptation_weights.pt",f'{r["seed"]}_{r["arm"]}',8,r["seed"])
        evseed=970000000+r["seed"]*100003+8*197
        for label,qids in (("old_pairs",list(range(14,22))),("new_pairs",[14+(i+3)%8 for i in range(8)])):
            compare(f'novel:{r["seed"]}:{r["arm"]}:{label}',model,8,evseed,r["after"][label],qids=qids)
    # The learned-results rows have no saved weights of their own; a repeated
    # run's matching causal weights corroborate numbers, not historical identity.
    REPORT["missing_historical_checkpoints"]=["results.json baseline24",
                                             "learned_results.json original6 (causal rerun available)"]
    save()

def semantic_checks():
    import task_identified_retention as task
    x,y=batch(8,16,32,20261020)
    a=task.inputs(x,"A");b=task.inputs(x,"B")
    assert torch.equal(a[:,:-1],b[:,:-1])
    assert set(a[:,-1].tolist()).isdisjoint(set(b[:,-1].tolist()))
    assert not ((x>=32)&(x<40)).any()
    expected_b=torch.stack([y[:,(i+3)%8] for i in range(8)],1)
    assert torch.equal(task.targets(y,"B"),expected_b)
    # Independent grammar interpreter.
    parsed=[]
    for hist in x.tolist():
        values=[None]*8
        for i in range(1,len(hist)):
            if 2<=hist[i-1]<10 and hist[i] in (10,11):
                values[hist[i-1]-2]=hist[i]-10
        parsed.append(values)
    assert torch.equal(torch.tensor(parsed),y)
    import novel_pair_adaptation as old
    ambiguous_examples=0
    old_ids=old.tokens(x,False)
    remap_ids=old.tokens(x,True)
    for j in range(8):
        # Same query symbol14+j requests y_j in old task; y_(j-3) in shifted task.
        ambiguous_examples+=int(y[:,j].ne(y[:,(j-3)%8]).sum())
    REPORT["task_semantics"]={
        "corrected_disjoint_queries":True,"corrected_independent_labels_match":True,
        "new_tokens_not_in_histories":True,"independent_grammar_replay_match":True,
        "old_ambiguous_label_pairs_in_32x8_queries":ambiguous_examples,
        "correction_changes_permutation_direction":True,
        "old_query_j_target":"(j-3)%8","corrected_new_query_j_target":"(j+3)%8",
        "remark":"Old and new adaptation scores are not a same-permutation reproduction."}
    # Audit exact seed spaces for historic training and eval.
    train={100000000+s*1000003+t*8191+n*197
           for s in (17,29,43) for t in range(240) for n in (2,4,8)}
    evaluation={900000000+s*100003+n*197+start*677
                for s in (17,29,43) for n in (2,4,8) for start in range(0,96,16)}
    assert train.isdisjoint(evaluation)
    REPORT["data_splits"]={"training_evaluation_seed_overlap":0,
                          "heldout_reuse_across_adaptive_experiments":True,
                          "warning":"Historical fixed sets function as validation sets, not an untouched final test"}
    # Budget confound is mathematical, no new training needed.
    REPORT["retention_budget_audit"]={"updates_each":240,"histories_each":5760,
        "new_only_new_histories":5760,"rehearsal_new_histories":2880,
        "rehearsal_old_histories":2880,"equal_new_task_exposure":False}
    # Duplicate trained controls are not independent seeds/replications.
    by={}
    for inv in REPORT["checkpoint_inventory"]:
        for key,d in inv["state_digests"].items():
            by.setdefault(d,[]).append(inv["file"]+":"+key)
    REPORT["duplicate_weight_groups"]=[v for v in by.values() if len(v)>1]
    save()

@torch.no_grad()
def intervention():
    for seed in (17,29,43):
        for arm in ("linear_fade","fade_by_half"):
            model=load_model("faded_guidance_weights.pt",f"{seed}_8_{arm}",8,seed)
            fingerprint=state_digest(model.state_dict())
            for delay in (256,1024,4096):
                budget()
                stats={k:{"correct_bits":0,"correct_records":0,"rescued_records":0,"harmed_records":0}
                       for k in ("normal","freeze_tail","freeze_query","freeze_both")}
                total_hash=hashlib.sha256()
                for start in range(0,96,16):
                    x,y=batch(8,delay,16,5000000000+seed*100003+8*197+start*677)
                    total_hash.update(x.numpy().tobytes())
                    # Verify parser labels and no valid writes anywhere in tail.
                    body=32
                    assert not ((x[:,body:]>=2)&(x[:,body:]<10)).any()
                    h,mem,prev,atbody=history_state(model,x)
                    preds={}
                    for mode in stats:
                        bank=atbody if mode in ("freeze_tail","freeze_both") else mem
                        write=mode not in ("freeze_query","freeze_both")
                        scores=query_logits(model,h,bank,prev,torch.arange(14,22),write)
                        assert torch.isfinite(scores).all()
                        preds[mode]=scores.argmax(-1)
                    normal=preds["normal"].eq(y).all(1)
                    for mode in stats:
                        ok=preds[mode].eq(y);whole=ok.all(1)
                        stats[mode]["correct_bits"]+=int(ok.sum())
                        stats[mode]["correct_records"]+=int(whole.sum())
                        stats[mode]["rescued_records"]+=int((whole&~normal).sum())
                        stats[mode]["harmed_records"]+=int((~whole&normal).sum())
                for v in stats.values():
                    v.update({"bit":v["correct_bits"]/(96*8),"whole":v["correct_records"]/96,"histories":96})
                assert state_digest(model.state_dict())==fingerprint
                row={"seed":seed,"arm":arm,"delay":delay,"no_write_tail_tokens":delay-16,
                     "history_sha256":total_hash.hexdigest(),"modes":stats}
                REPORT["intervention"].append(row)
                print("INDEPENDENT_INTERVENTION="+json.dumps(row,separators=(",",":")),flush=True)
                save()

@torch.no_grad()
def validate_long_reference():
    """Numerical parity at the actual4096-token horizon; no new intervention."""
    weights = torch.load(ROOT / "faded_guidance_weights.pt", map_location="cpu", weights_only=True)
    records = []
    for seed in (17,29,43):
        for arm in ("linear_fade","fade_by_half"):
            model=build("shared",8,seed)
            model.load_state_dict(weights[f"{seed}_8_{arm}"],strict=True)
            model.eval()
            x,_=batch(8,4096,16,5000000000+seed*100003+8*197)
            x=x[:2]
            reference=model(query_histories(x,8)).reshape(8,2,2).transpose(0,1)
            st=history_state(model,x)
            cached=query_logits(model,*st[:3],torch.arange(14,22))
            error=float((cached-reference).abs().max())
            same=torch.equal(cached.argmax(-1),reference.argmax(-1))
            assert error<=2e-5 and same,(seed,arm,error)
            records.append({"seed":seed,"arm":arm,"delay":4096,
                            "histories":2,"max_abs_logit_error":error,
                            "predictions_identical":same})
    REPORT["long_reference_parity"]=records
    REPORT["validation_script_sha256"]=sha(Path(__file__))
    REPORT["original_files_unchanged"]=all(sha(ROOT/name)==v["sha256"] for name,v in REPORT["inputs"].items())
    assert REPORT["original_files_unchanged"]
    save()
    print("LONG_REFERENCE_PARITY="+json.dumps(records),flush=True)

if VALIDATE_EXISTING:
    validate_long_reference()
else:
    try:
        with torch.inference_mode():
            reproduce()
            semantic_checks()
            intervention()
            validate_long_reference()
        REPORT["original_files_unchanged"]=all(sha(ROOT/name)==v["sha256"] for name,v in MANIFEST.items())
        assert REPORT["original_files_unchanged"]
        REPORT["all_checkpoint_scores_reproduced"]=all(r["match"] for r in REPORT["reproductions"])
        REPORT["complete"]=True
        save()
        print("INDEPENDENT_AUDIT_COMPLETE",json.dumps({
            "reproductions":len(REPORT["reproductions"]),
            "matches":sum(r["match"] for r in REPORT["reproductions"]),
            "intervention_conditions":len(REPORT["intervention"]),
            "seconds":REPORT["elapsed_wall_s"]}),flush=True)
    except Exception as exc:
        REPORT["error"]=repr(exc)
        save()
        raise

