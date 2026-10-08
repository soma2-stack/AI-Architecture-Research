"""Experiment 013 Phase 2 (EXPLORATORY, diagnostic): gate and memory dynamics of reproduced protected-RNN weights.

All inputs are weight snapshots whose training curves were verified bit-for-bit against Experiment 012.
Measures, per run and snapshot:
  * slow-write gate values by token category, layer and channel;
  * protected-coefficient trajectories;
  * gate-implied retention over non-write tokens, and measured state sensitivity (finite-difference gain) over long intervals;
  * linear-probe decodability of every slot value from the pre-query state versus the model's own readout accuracy.
Low gate values alone are NOT evidence of useful retention: the proposal is nonlinear and fed back (see the sensitivity measure).
"""
from __future__ import annotations

import json
import math
import sys
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import torch

from . import capacity_010 as c10
from . import capacity_012 as c12
from . import capacity_013 as c13

PROBE_SEED = 200_000_000
CATS = ("prefix_write", "prefix_value", "marked_write", "marked_value", "decoy_value", "filler", "query")


def categories(ids: torch.Tensor) -> torch.Tensor:
    """Category index per position for query histories [N, 8+delay+1]."""
    n, t = ids.shape
    cat = torch.full((n, t), CATS.index("filler"), dtype=torch.long)
    cat[:, 0:8:2] = CATS.index("prefix_write")
    cat[:, 1:8:2] = CATS.index("prefix_value")
    body = ids[:, 8:-1]
    is_w = (body >= 2) & (body < 6)
    is_v = (body >= 10) & (body < 12)
    prev_w = torch.zeros_like(is_w)
    prev_w[:, 1:] = is_w[:, :-1]
    sub = cat[:, 8:-1]
    sub[is_w] = CATS.index("marked_write")
    sub[is_v & prev_w] = CATS.index("marked_value")
    sub[is_v & ~prev_w] = CATS.index("decoy_value")
    cat[:, 8:-1] = sub
    cat[:, -1] = CATS.index("query")
    return cat


@torch.no_grad()
def trace(model, ids: torch.Tensor):
    """Re-implements CandidateLanguageModel.forward step by step, returning gates, states and logits (checked against model)."""
    x = model.embedding(ids)
    gates, states = [], []
    for cell, norm in zip(model.cells, model.norms):
        prepared = cell.prepare(x)
        h = torch.zeros(ids.shape[0], model.config.width)
        seq = []
        for j in range(ids.shape[1]):
            h = cell.step(tuple(v[:, j] for v in prepared), h)
            seq.append(h)
        raw = torch.stack(seq, 1)
        # effective gate actually applied in step(): retain_slow=False overwrites it with ones
        gates.append(prepared[1] if cell.config.retain_slow else torch.ones_like(prepared[1]))
        states.append(raw)
        x = norm(raw)
    logits = torch.nn.functional.linear(model.final_norm(x), model.embedding.weight)
    return gates, states, logits


def gate_stats(model, ids) -> dict:
    gates, states, logits = trace(model, ids)
    ref = model(ids)[0]
    assert torch.allclose(logits, ref, atol=1e-5), "trace diverged from model.forward"
    cat = categories(ids)
    out = {}
    for layer, g in enumerate(gates):
        rows = {}
        for k, name in enumerate(CATS):
            m = cat == k
            if not bool(m.any()):
                continue
            v = g[m]                       # [count, channels]
            rows[name] = {"mean": float(v.mean()), "median": float(v.median()), "p05": float(v.quantile(.05)), "p95": float(v.quantile(.95)),
                          "per_channel_mean": [round(float(a), 5) for a in v.mean(0)]}
        nonwrite = (cat == CATS.index("filler")) | (cat == CATS.index("decoy_value"))
        keep = (1 - g[nonwrite]).clamp_min(1e-12)
        per_tok = float(torch.exp(torch.log(keep).mean()))           # geometric-mean per-token retention on non-write tokens
        writes = (cat == CATS.index("marked_value")) | (cat == CATS.index("prefix_value"))
        rows["_summary"] = {"geomean_retention_nonwrite": per_tok,
                            "implied_half_life_tokens": (math.log(.5) / math.log(per_tok)) if 0 < per_tok < 1 else None,
                            "retention_over_64_nonwrite_tokens": per_tok ** 64,
                            "write_selectivity_value_over_filler": float(g[writes].mean() / g[cat == CATS.index("filler")].mean()),
                            "mean_abs_coefficient": float(model.cells[layer].read_protected(states[layer]).abs().mean())}
        out[f"layer{layer}"] = rows
    return out


@torch.no_grad()
def sensitivity(model, delay: int, n: int = 128, eps: float = 1e-3, seed: int = 7) -> dict:
    """Finite-difference gain of a layer-0 state perturbation applied right after the initialization prefix,
    measured at the end of the history. Includes the nonlinear proposal and recurrent feedback (not just the gate)."""
    x = c10.generator_batch(4, 2, delay, n, seed=PROBE_SEED + 10 * delay + 1)
    cell = model.cells[0]
    prepared = cell.prepare(model.embedding(x))
    h = torch.zeros(n, model.config.width)
    for j in range(8):
        h = cell.step(tuple(v[:, j] for v in prepared), h)
    g = torch.Generator().manual_seed(seed)
    out = {}
    for name in ("protected", "complement"):
        v = torch.randn(n, model.config.width, generator=g)
        v = cell.synthesize(cell.read_protected(v)) if name == "protected" else cell.complement(v)
        v = v / v.norm(dim=1, keepdim=True)
        a, b = h.clone(), h + eps * v
        for j in range(8, x.shape[1]):
            step = tuple(t[:, j] for t in prepared)
            a, b = cell.step(step, a), cell.step(step, b)
        d = (b - a)
        gain = d.norm(dim=1) / eps
        out[name] = {"median_gain": float(gain.median()), "log10_median_gain": float(torch.log10(gain.median().clamp_min(1e-30))),
                     "protected_part": float(cell.read_protected(d).norm(dim=1).median() / eps),
                     "complement_part": float(cell.complement(d).norm(dim=1).median() / eps)}
    return out


@torch.no_grad()
def final_states(model, x):
    _, states, _ = trace(model, x)
    hs = [s[:, -1] for s in states]                      # pre-query state after the full history, per layer
    coeff = [model.cells[i].read_protected(h) for i, h in enumerate(hs)]
    comp = [model.cells[i].complement(h) for i, h in enumerate(hs)]
    return {"full": torch.cat(hs, 1).numpy(), "protected": torch.cat(coeff, 1).numpy(), "complement": torch.cat(comp, 1).numpy()}


def probe(model, delay: int, n_train: int = 2048, n_test: int = 1024) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    x = c10.generator_batch(4, 2, delay, n_train + n_test, seed=PROBE_SEED + delay)
    y = c10.replay(x, 4, 2).numpy()
    feats = final_states(model, x)
    out = {}
    for name, f in feats.items():
        pred = np.zeros((n_test, 4), dtype=int)
        for s in range(4):
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000))
            clf.fit(f[:n_train], y[:n_train, s])
            pred[:, s] = clf.predict(f[n_train:])
        hit = pred == y[n_train:]
        varied = y[n_train:].max(1) != y[n_train:].min(1)
        out[name] = {"per_slot": float(hit.mean()), "per_slot_index": hit.mean(0).round(4).tolist(), "whole": float(hit.all(1).mean()),
                     "whole_varied": float(hit.all(1)[varied].mean())}
    model.eval()
    with torch.no_grad():
        mp = torch.cat([c10.predictions(model, x[n_train + a:n_train + a + 32], 4, 2).argmax(-1) for a in range(0, n_test, 32)]).numpy()
    hit = mp == y[n_train:]
    varied = y[n_train:].max(1) != y[n_train:].min(1)
    out["model_readout"] = {"per_slot": float(hit.mean()), "whole": float(hit.all(1).mean()), "whole_varied": float(hit.all(1)[varied].mean())}
    return out


def coefficient_examples(model, k: int = 3) -> dict:
    x = c10.generator_batch(4, 2, 64, k, seed=PROBE_SEED + 999)
    _, states, _ = trace(model, x)
    return {"tokens": x.tolist(), "layer0_coefficients": model.cells[0].read_protected(states[0]).round(decimals=4).tolist()}


def analyse_run(args) -> dict:
    record_path, weights_dir = args
    torch.set_num_threads(1)
    r = json.loads(Path(record_path).read_text(encoding="utf-8-sig"))["runs"][0]
    name, i, d = r["architecture"], r["init_seed"], r["data_seed"]
    ids = c10.query_histories(c10.generator_batch(4, 2, 64, 256, seed=c12.eval_seed(64)), 4)
    snaps = []
    for s in r["saved_weights"]:
        model = c13.build(name, i)
        model.load_state_dict(torch.load(Path(weights_dir) / s["file"]))
        model.eval()
        row = {"step": s["step"], "gates": gate_stats(model, ids), "probe64": probe(model, 64)}
        if s["step"] in (0, 3000):
            row["sensitivity"] = {str(dl): sensitivity(model, dl) for dl in (64, 256)}
            row["probe256"] = probe(model, 256)
        if s["step"] == 3000:
            row["coefficient_examples"] = coefficient_examples(model)
        snaps.append(row)
    return {"architecture": name, "init_seed": i, "data_seed": d, "outcome": r["outcome"], "onset": r["learning_onset_step"],
            "whole_varied_64": r["eval"]["64"]["whole_varied"], "snapshots": snaps}


def main(argv=None):
    a = argv or sys.argv[1:]
    records = sorted(p for p in Path(a[0]).glob("*_*_*.json"))
    with get_context("spawn").Pool(min(len(records), 7)) as pool:
        res = pool.map(analyse_run, [(str(p), a[1]) for p in records])
    Path(a[2]).write_text(json.dumps({"label": "EXPLORATORY diagnostics (Experiment 013 Phase 2)", "runs": res}, indent=1),
                          encoding="utf-8", newline="\n")
    for r in res:
        last = r["snapshots"][-1]
        g0, g1 = last["gates"]["layer0"], last["gates"]["layer1"]
        print(r["architecture"], r["init_seed"], r["data_seed"], r["outcome"],
              "| L0 gate mv/filler %.3f/%.3f L1 %.3f/%.3f" % (g0["marked_value"]["mean"], g0["filler"]["mean"], g1["marked_value"]["mean"], g1["filler"]["mean"]),
              "| probe full %.3f prot %.3f comp %.3f readout %.3f" % (last["probe64"]["full"]["per_slot"], last["probe64"]["protected"]["per_slot"],
                                                                     last["probe64"]["complement"]["per_slot"], last["probe64"]["model_readout"]["per_slot"]))


if __name__ == "__main__":
    main()
