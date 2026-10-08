"""POST-HOC (not preregistered) Experiment 014 check: do the protected-subspace and fast-complement transplants switch the SAME pairs?

Per eligible ordered pair (late cut, layer 1, both transfer directions) records whether the protected/Walsh-8 transplant and the
complement transplant each switched the changed slot, plus per-changed-slot switch rates."""
import json
import sys
from pathlib import Path

import torch

from . import intervene_014 as iv


def one(name: str, delay: int = 64) -> dict:
    torch.set_num_threads(1)
    model, _ = iv.load_model(name)
    P = iv.build_pairs(delay, 256)
    n = P.tok_a.shape[0]
    cut = P.cuts("late")
    idx = torch.arange(n)
    ra, rb = iv.staged_run(model, P.tok_a, record=True), iv.staged_run(model, P.tok_b, record=True)
    ha, hb = ra["nat"][idx, cut - 1], rb["nat"][idx, cut - 1]
    hist, cuts = torch.cat([P.tok_a, P.tok_b]), torch.cat([cut, cut])
    hr, hd = torch.cat([ha, hb]), torch.cat([hb, ha])
    slot = torch.cat([P.slot, P.slot])
    lab_r, lab_d = torch.cat([P.y_a, P.y_b]), torch.cat([P.y_b, P.y_a])
    i2 = torch.arange(2 * n)
    pr, pd = torch.cat([ra["logits"], rb["logits"]]).argmax(-1), torch.cat([rb["logits"], ra["logits"]]).argmax(-1)
    elig = (pr[i2, slot] == lab_r[i2, slot]) & (pd[i2, slot] == lab_d[i2, slot])
    proj = iv.projector_for(model, "walsh", None)
    sw = {}
    for kind in ("sub", "comp"):
        new = iv.transform(kind, (1,), hr, hd, proj)
        post = iv.staged_run(model, hist, cuts, new)["logits"].argmax(-1)
        sw[kind] = post[i2, slot] == lab_d[i2, slot]
    both, only_p, only_c = sw["sub"] & sw["comp"], sw["sub"] & ~sw["comp"], ~sw["sub"] & sw["comp"]
    neither = ~sw["sub"] & ~sw["comp"]
    f = lambda m: float((m & elig).sum() / elig.sum())
    return {"n_eligible": int(elig.sum()), "both_switch": f(both), "only_protected": f(only_p), "only_complement": f(only_c), "neither": f(neither),
            "per_slot_switch_protected": [float((sw["sub"] & elig & (slot == s)).sum() / (elig & (slot == s)).sum()) for s in range(4)],
            "per_slot_switch_complement": [float((sw["comp"] & elig & (slot == s)).sum() / (elig & (slot == s)).sum()) for s in range(4)]}


if __name__ == "__main__":
    res = {m: one(m) for m in iv.MODELS}
    Path(sys.argv[1]).write_text(json.dumps({"label": "POST-HOC, not preregistered", "late_cut_layer1_64_tokens": res}, indent=1), encoding="utf-8", newline="\n")
    for m, r in res.items():
        print(f"{m:24s} n={r['n_eligible']:3d} both {r['both_switch']:.2f} only-prot {r['only_protected']:.2f} only-comp {r['only_complement']:.2f} neither {r['neither']:.2f} | per-slot prot", [round(x, 2) for x in r['per_slot_switch_protected']])
