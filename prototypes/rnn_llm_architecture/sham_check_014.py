"""Experiment 014 post-hoc check of the sham-gap validity gate: is the gap logic or float32 batch-size rounding?

The sham run pushes the 2n recipient histories through one batch; the reference logits came from two batches of n.
Different batch sizes can select different BLAS kernels. We compare the sham run with a clean reference computed on the
SAME 2n batch (expected gap ~0) and report prediction agreement.
"""
import json
import sys
from pathlib import Path

import torch

from . import intervene_014 as iv


def check(name: str) -> dict:
    torch.set_num_threads(1)
    model, _ = iv.load_model(name)
    out = {}
    for delay in iv.DELAYS:
        for mode in ("late", "early"):
            P = iv.build_pairs(delay, 256)
            cut = P.cuts(mode)
            hist = torch.cat([P.tok_a, P.tok_b])
            cuts = torch.cat([cut, cut])
            n = P.tok_a.shape[0]
            idx = torch.arange(2 * n)
            clean_split = torch.cat([iv.staged_run(model, P.tok_a, record=False)["logits"], iv.staged_run(model, P.tok_b)["logits"]])
            ref = iv.staged_run(model, hist, record=True)
            hr = ref["nat"][idx, cuts - 1]
            sham = iv.staged_run(model, hist, cuts, [hr[:, l] for l in range(hr.shape[1])])["logits"]
            out[f"{delay}_{mode}"] = {"gap_vs_split_batches": float((sham - clean_split).abs().max()),
                                      "gap_vs_same_batch": float((sham - ref["logits"]).abs().max()),
                                      "predictions_identical": bool(torch.equal(sham.argmax(-1), clean_split.argmax(-1)))}
    return out


if __name__ == "__main__":
    res = {m: check(m) for m in iv.MODELS}
    Path(sys.argv[1]).write_text(json.dumps(res, indent=1), encoding="utf-8", newline="\n")
    for m, r in res.items():
        print(m, "max gap vs split %.1e | vs same batch %.1e | predictions identical everywhere %s" % (
            max(v["gap_vs_split_batches"] for v in r.values()), max(v["gap_vs_same_batch"] for v in r.values()),
            all(v["predictions_identical"] for v in r.values())))
