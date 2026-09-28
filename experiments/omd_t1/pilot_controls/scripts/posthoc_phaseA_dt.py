"""POST-HOC, NON-GATING: at wrong held-out decisions, compare the neural choice with the teacher
victim (planted state and dt). Saved decisions + regenerated teacher trajectories only."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

from omdp import ledger, streams, teachers  # noqa: E402
from omdp.config import CONFIG, EVENT_EVICT  # noqa: E402

PA = os.path.join(HERE, "results", "phaseA")
with ledger.Measured("posthoc_phaseA_dt", "post-hoc non-gating: planted state and dt at wrong decisions"):
    out = {"note": "POST-HOC, NON-GATING; descriptive only", "max_train_dt": {}, "by_controller": {}}
    for s in CONFIG["train_seeds"]:
        req = streams.make_stream(s, CONFIG["train_len"])[0]
        out["max_train_dt"][s] = {c: float(teachers.simulate(c, req, 16)["dt"].max()) for c in CONFIG["controls"]}
    for control in CONFIG["controls"]:
        for hs in CONFIG["heldout_seeds"]:
            req = streams.make_stream(hs, CONFIG["heldout_len"])[0]
            tr = teachers.simulate(control, req, 16)
            for seed in CONFIG["train_seeds"]:
                z = np.load(os.path.join(PA, "heldout_decisions", f"{control}_s{seed}_h{hs}.npz"))
                nv, sl = z["neural_victim_teacher_forced"], z["teacher_slot"]
                ev = np.where(tr["etype"] == EVENT_EVICT)[0]
                w = ev[nv[ev] != sl[ev]]
                if not len(w):
                    continue
                n_dt = tr["dt"][w, nv[w]]
                t_dt = tr["dt"][w, sl[w]]
                out["by_controller"][f"{control}_s{seed}_h{hs}"] = {
                    "errors": int(len(w)),
                    "neural_choice_dt_median": float(np.median(n_dt)), "neural_choice_dt_max": float(n_dt.max()),
                    "teacher_victim_dt_median": float(np.median(t_dt)),
                    "frac_neural_choice_dt_gt_train_max": float(np.mean(n_dt > max(v[control] for v in out["max_train_dt"].values()))),
                    "frac_neural_choice_state_gt_teacher_state": float(np.mean(tr["local"][w, nv[w]] > tr["local"][w, sl[w]])),
                    "frac_neural_choice_state_eq_teacher_state": float(np.mean(tr["local"][w, nv[w]] == tr["local"][w, sl[w]]))}
    with open(os.path.join(PA, "posthoc_error_dt_state.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("max train dt", out["max_train_dt"])
    for k, v in out["by_controller"].items():
        print(k, v)
