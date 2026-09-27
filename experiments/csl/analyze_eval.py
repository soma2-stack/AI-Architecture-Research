import json, numpy as np, collections
res = json.load(open("eval_results.json"))
by = collections.defaultdict(list)
for r in res: by[(r["config"], r["policy"])].append(r)
def ms(v):
    v=[x for x in v if x is not None]
    return ("%.4f±%.4f" % (np.mean(v), np.std(v)/np.sqrt(len(v)))) if v else "-"
def mi(v):
    v=[x for x in v if x is not None]
    return ("%.0f" % np.median(v)) if v else "-"
for cfg in ["A_pilot","B_highdim","C_weak","D_null"]:
    print("=== ", cfg)
    orc = np.mean([r["avg_loss"] for r in by[(cfg,"ORACLE")]])
    print("  ORACLE loss %.4f" % orc)
    for pol in ["CSL","HW","NRT","L1"]:
        v = by[(cfg,pol)]
        if not v: continue
        line = f"  {pol:4s} loss {ms([r['avg_loss'] for r in v])}  regret {np.mean([r['avg_loss'] for r in v])-orc:.4f}"
        if pol != "L1":
            sp = [r["spurious"] for r in v]; ad=[r["admissions"] for r in v]
            line += f" | spurious/run mean {np.mean(sp):.2f} (runs with >=1: {sum(1 for s in sp if s>0)}/{len(sp)}) admissions {np.mean(ad):.1f} final {np.mean([r['final_size'] for r in v]):.1f}"
            line += f" | det-delay med {mi([r['det_delay_median'] for r in v])} missed {sum(r['det_missed'] for r in v)}/{sum(r['n_new_rules'] for r in v)} | ret-delay med {mi([r['ret_delay_median'] for r in v])} ret-missed {sum(r['ret_missed'] for r in v)}"
        else:
            line += f" | spurious-in-structure avg {np.mean([r['spurious_avg_structure'] for r in v]):.2f} final size {np.mean([r['final_size'] for r in v]):.1f}"
        print(line)
