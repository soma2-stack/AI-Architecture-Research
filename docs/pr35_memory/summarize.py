"""Recompute all scalar summaries from the committed hosted logs' JSON records."""
import argparse
import csv
import itertools
import json
import statistics
from pathlib import Path

def summarize(folder):
    documents=[json.loads((folder/f"seed{s}.json").read_text()) for s in (17,29,43)]
    runs=[r for doc in documents for r in doc["runs"]]
    assert len(runs)==123
    assert all(r["status"]=="complete" and r["steps"]==600 and len(r["eval"])==4 for r in runs)
    assert all(doc["sources"]==documents[0]["sources"] for doc in documents)
    assert len({(r["model"],r["nominal_width"],r["slots"],r["seed"]) for r in runs})==123
    stream={}
    datasets={}
    for r in runs:
        stream.setdefault((r["seed"],r["slots"]),set()).add(r["training_stream_sha256"])
        for delay,e in r["eval"].items():
            datasets.setdefault((r["seed"],r["slots"],delay),set()).add(e["data_sha256"])
            assert e["finite_logits"]
    assert all(len(x)==1 for x in stream.values())
    assert all(len(x)==1 for x in datasets.values())
    rows=[]
    groups={}
    for r in runs:
        groups.setdefault((r["model"],r["nominal_width"],r["slots"]),[]).append(r)
    for (model,width,slots),group in groups.items():
        assert sorted(r["seed"] for r in group)==[17,29,43]
        for delay in ("16","64","256","1024"):
            ev=[r["eval"][delay] for r in group]
            rows.append({
                "model":model,"nominal_width":width,"actual_width":group[0]["actual_width"],
                "slots":slots,"eval_body_tokens":int(delay),"minimum_no_write_hold":int(delay)-16,"seeds":3,
                "per_bit_mean":statistics.mean(x["per_slot"] for x in ev),
                "whole_mean":statistics.mean(x["whole"] for x in ev),
                "whole_min":min(x["whole"] for x in ev),"whole_max":max(x["whole"] for x in ev),
                "whole_varied_mean":statistics.mean(x["whole_varied"] for x in ev),
                "constant_answer_fraction":statistics.mean(x["constant_answer_fraction"] for x in ev),
                "reliable_all3":all(x["per_slot"]>=.95 and x["whole"]>=.90 for x in ev),
                "parameters":group[0]["resources"]["parameters"],
                "state_bytes_per_example":group[0]["resources"]["state_bytes_per_example"],
                "independent_state_scalars":group[0]["resources"]["independent_state_scalars"],
                "linear_MACs_per_token_estimate":group[0]["resources"]["linear_MACs_per_token_estimate"],
                "mean_train_cpu_s":statistics.mean(r["train_cpu_s"] for r in group),
                "mean_forward_ms":statistics.mean(r["latency"]["median_forward_ms"] for r in group)})
    assert len(rows)==164
    lookup={(r["model"],r["nominal_width"],r["slots"],r["seed"]):r for r in runs}
    advantage=[]
    for width,slots,delay in itertools.product((16,32,64),(2,4,8),("16","64","256","1024")):
        passed=[]
        for seed in (17,29,43):
            p=lookup[("pair_shared",width,slots,seed)]["eval"][delay]["whole"]
            passed.append(all(p>=lookup[(b,width,slots,seed)]["eval"][delay]["whole"]+.05
                              for b in ("gru","gru_matched","lstm")))
        advantage.append(all(passed))
    totals={
        "runs":len(runs),"steps":sum(r["steps"] for r in runs),
        "train_cpu_s":sum(r["train_cpu_s"] for r in runs),
        "train_wall_s":sum(r["train_wall_s"] for r in runs),
        "train_tokens":sum(r["train_query_token_positions"] for r in runs),
        "screen_elapsed_sum_s":sum(d["elapsed_wall_s"] for d in documents),
        "peak_RSS_max_bytes":max(d["process_lifetime_peak_RSS_bytes"] for d in documents),
        "advantage_all3_conditions":sum(advantage),
        "reliable_pair_conditions":sum(r["reliable_all3"] for r in rows if r["model"]=="pair_shared")}
    return totals,rows

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--verify-csv",type=Path)
    a=p.parse_args()
    totals,rows=summarize(a.folder)
    if a.verify_csv:
        with a.verify_csv.open(newline="") as f:expected=list(csv.DictReader(f))
        assert len(expected)==len(rows)
        for computed,saved in zip(rows,expected):
            for key,value in computed.items():
                if isinstance(value,bool):assert saved[key].lower()==str(value).lower(),key
                elif isinstance(value,(float,int)):assert abs(float(saved[key])-value)<=1e-8*max(1,abs(value)),key
                else:assert saved[key]==value,key
    if a.output.exists():raise FileExistsError(a.output)
    with a.output.open("x",encoding="utf-8") as f:json.dump({"totals":totals,"rows":rows},f,indent=2)
    print(json.dumps(totals))

if __name__=="__main__":main()
