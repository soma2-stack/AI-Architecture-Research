"""POST-HOC, NON-GATING diagnostic of the failed Phase A imitation gate. Uses only saved held-out
decisions (teacher trajectory + teacher-forced neural victims) and regenerated stream segment labels;
no training, extraction or new neural evaluation."""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

from omdp import ledger, streams, teachers  # noqa: E402
from omdp.config import CONFIG, EVENT_EVICT  # noqa: E402

PA = os.path.join(HERE, "results", "phaseA")
with ledger.Measured("posthoc_phaseA", "post-hoc non-gating breakdown of Phase A imitation errors"):
    out = {"note": "POST-HOC, NON-GATING; descriptive only", "by_controller": {}}
    segs = {s: streams.make_stream(s, CONFIG["heldout_len"]) for s in CONFIG["heldout_seeds"]}
    for control in CONFIG["controls"]:
        for seed in CONFIG["train_seeds"]:
            name = f"{control}_s{seed}"
            rec = {}
            for hs in CONFIG["heldout_seeds"]:
                z = np.load(os.path.join(PA, "heldout_decisions", f"{name}_h{hs}.npz"))
                et, sl, nv = z["teacher_etype"], z["teacher_slot"], z["neural_victim_teacher_forced"]
                req, sid, sg = segs[hs]
                ev = np.where(et == EVENT_EVICT)[0]
                wrong = nv[ev] != sl[ev]
                by = collections.defaultdict(lambda: [0, 0])
                for t, w in zip(ev, wrong):
                    k = sg[sid[t]]["type"]
                    by[k][0] += int(w)
                    by[k][1] += 1
                # planted local state of the teacher victim at wrong decisions
                tr = teachers.simulate(control, req, CONFIG["C"])
                vstate = collections.Counter(int(tr["local"][t, sl[t]]) for t in ev[wrong])
                rec[f"h{hs}"] = {"errors": int(wrong.sum()), "evictions": int(len(ev)),
                                 "error_rate_by_segment": {k: {"errors": a, "evictions": b, "rate": round(a / b, 4)}
                                                           for k, (a, b) in sorted(by.items())},
                                 "teacher_victim_planted_state_at_errors": dict(sorted(vstate.items())[:12])}
            out["by_controller"][name] = rec
    with open(os.path.join(PA, "posthoc_error_breakdown.json"), "w") as f:
        json.dump(out, f, indent=1)
    for name, rec in out["by_controller"].items():
        agg = collections.defaultdict(lambda: [0, 0])
        for h in rec.values():
            for k, v in h["error_rate_by_segment"].items():
                agg[k][0] += v["errors"]
                agg[k][1] += v["evictions"]
        print(name, {k: round(a / b, 3) for k, (a, b) in sorted(agg.items())})
