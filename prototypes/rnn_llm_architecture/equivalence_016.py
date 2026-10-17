"""Experiment 016 numerical checks: exact equivalence of the protected cell to a rotated matrix-gated recurrence, non-reducibility to a
canonical (diagonal-gate) GRU basis, causal-intervention equivalence on trained checkpoints, invariants and resources. No training."""
from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from . import capacity_013 as c13
from . import intervene_014 as iv
from . import necessity_015 as ne
from .reference_016 import ReferenceModel, mapped_name, original_forward_features

GRID_SEEDS = (0, 1, 2)
GRID_BATCH = (1, 3, 8)
GRID_LEN = (1, 7, 40)
MASKS = ("none", "random", "zeros")


def models_for_grid():
    out = {f"init_seed_{s}": c13.build("protected", s) for s in GRID_SEEDS}
    for name in ("prot_success_43_29", "fixed005_success_43_43"):
        out[name] = iv.load_model(name)[0]
    out["no_retain_seed_5"] = c13.build("protected_no_retain", 5)
    return out


def exact_masks_(model) -> float:
    """Walsh masks are stored as float32 values of +-1/sqrt(n); after a float64 cast they are orthonormal only to ~6e-8.
    Re-derive them exactly in the working dtype (copies only; the original architecture is untouched). Returns the old rounding error."""
    err = 0.0
    for cell in model.cells:
        M = cell.masks
        n = M.shape[1]
        exact = M.sign() / torch.sqrt(torch.tensor(float(n), dtype=M.dtype))
        if not torch.allclose(M.abs().float(), exact.abs().float(), atol=1e-6):
            raise ValueError("not a Walsh bank")
        err = max(err, float((M @ M.T - torch.eye(M.shape[0], dtype=M.dtype)).abs().max()))
        with torch.no_grad():
            cell.masks.copy_(exact)
    return err


def compare(model, ids, mask_kind: str, dtype, seed: int = 0, exact_masks: bool = True) -> dict:
    m = copy.deepcopy(model).to(dtype)
    m.train(False)
    mask_rounding = exact_masks_(m) if exact_masks else None
    ref = ReferenceModel(m)
    B, T = ids.shape
    L, C = len(m.cells), m.cells[0].masks.shape[0]
    g = torch.Generator().manual_seed(seed)
    masks = None
    if mask_kind == "random":
        masks = torch.rand(B, T, L, C, generator=g).to(dtype)
        masks[torch.rand(B, T, L, C, generator=g) < .3] = 0.0
    elif mask_kind == "zeros":
        masks = torch.zeros(B, T, L, C, dtype=dtype)
    x = m.embedding(ids).detach().requires_grad_(True)
    xr = ref.embedding(ids).detach().requires_grad_(True)
    lo, Ho = original_forward_features(m, x, masks)
    lr, Sr, Hr = ref.forward_features(xr, masks)
    w = torch.randn(lo.shape, generator=g).to(dtype)
    (lo * w).sum().backward()
    (lr * w).sum().backward()
    gap = lambda a, b: float((a - b).detach().abs().max())
    out = {"logits": gap(lo, lr), "state": gap(Ho, Hr), "replaced_mask_rounding_error": mask_rounding}
    if masks is None and mask_kind == "none":
        out["features_path_vs_model_forward"] = gap(m(ids)[0], lo)
    cdiff, fdiff = 0.0, 0.0
    for l, cell in enumerate(ref.cells):
        c_o = Ho[:, :, l] @ cell.M.T
        f_o = Ho[:, :, l] - c_o @ cell.M
        cdiff = max(cdiff, gap(c_o, Sr[:, :, l, :cell.k]))
        fdiff = max(fdiff, gap(f_o, Sr[:, :, l, cell.k:] @ cell.N))
    out["protected_coefficients"], out["fast_complement"] = cdiff, fdiff
    rp = dict(ref.named_parameters())
    worst = 0.0
    for name, p in m.named_parameters():
        q = rp[mapped_name(name)]
        if p.grad is None and q.grad is None:
            continue
        a = p.grad if p.grad is not None else torch.zeros_like(p)
        b = q.grad if q.grad is not None else torch.zeros_like(q)
        worst = max(worst, float((a - b).abs().max() / max(float(a.abs().max()), 1e-30)))
    out["param_grad_rel"] = worst
    out["input_grad_rel"] = float((x.grad - xr.grad).abs().max() / x.grad.abs().max().clamp_min(1e-30))
    out["dead_params_same"] = sorted(n for n, p in m.named_parameters() if p.grad is None) == sorted(
        n for n, p in m.named_parameters() if rp[mapped_name(n)].grad is None)
    return out


def grid() -> dict:
    res, worst = [], {}
    for mname, model in models_for_grid().items():
        for B in GRID_BATCH:
            for T in GRID_LEN:
                for mk in MASKS:
                    for dtype in (torch.float64, torch.float32):
                        ids = torch.randint(0, 32, (B, T), generator=torch.Generator().manual_seed(B * 100 + T))
                        r = compare(model, ids, mk, dtype)
                        r.update(model=mname, batch=B, length=T, mask=mk, dtype=str(dtype).split(".")[-1])
                        res.append(r)
    raw = [compare(model, torch.randint(0, 32, (3, 40), generator=torch.Generator().manual_seed(1)), "random", torch.float64, exact_masks=False)
           for model in models_for_grid().values()]
    keys = ("logits", "state", "protected_coefficients", "fast_complement", "param_grad_rel", "input_grad_rel")
    for dt in ("float64", "float32"):
        rows = [r for r in res if r["dtype"] == dt]
        worst[dt] = {k: max(r[k] for r in rows) for k in keys}
        worst[dt]["features_path_vs_model_forward"] = max(r.get("features_path_vs_model_forward", 0.0) for r in rows)
        worst[dt]["dead_params_same_all"] = all(r["dead_params_same"] for r in rows)
    passed = (all(worst["float64"][k] <= 1e-10 for k in ("logits", "state", "protected_coefficients", "fast_complement"))
              and worst["float64"]["param_grad_rel"] <= 1e-9 and worst["float64"]["input_grad_rel"] <= 1e-9
              and all(worst["float32"][k] <= 1e-4 for k in ("logits", "state", "protected_coefficients", "fast_complement")))
    worst["float64_with_original_float32_rounded_masks"] = {k: max(r[k] for r in raw) for k in keys}
    return {"cases": len(res), "worst": worst, "exact_equivalence_passed": passed, "rows": res}


def closed_write_invariant() -> dict:
    """Single-step autograd check in float64 on a trained cell: closed channel j keeps c_j and has identity / zero derivatives."""
    model = copy.deepcopy(iv.load_model("prot_success_43_29")[0]).double()
    exact_masks_(model)
    ref = ReferenceModel(model)
    cell, rcell = model.cells[1], ref.cells[1]
    g = torch.Generator().manual_seed(3)
    x = torch.randn(4, 32, generator=g, dtype=torch.float64)
    h = torch.randn(4, 32, generator=g, dtype=torch.float64).requires_grad_(True)
    m = torch.ones(4, 8, dtype=torch.float64)
    m[:, 2] = 0.0
    out = cell.step(cell.prepare(x), h, m)
    c_new, c_old = cell.read_protected(out), cell.read_protected(h)
    drift = float((c_new[:, 2] - c_old[:, 2]).abs().max())
    gh = torch.autograd.grad(c_new[:, 2].sum(), [h] + list(cell.parameters()), allow_unused=True)
    jac_h = gh[0]
    expected = cell.masks[2].expand_as(jac_h)                     # d c_2/d h = M[2] when the channel is closed
    param_grad_max = max((float(t.abs().max()) for t in gh[1:] if t is not None), default=0.0)
    s = rcell.to_s(h.detach())
    s2, _ = rcell.step(x, s, m)
    ref_drift = float((s2[:, 2] - s[:, 2]).abs().max())
    return {"original_closed_channel_drift": drift, "reference_closed_channel_drift": ref_drift,
            "dc_closed_dh_equals_mask_row": float((jac_h - expected).abs().max()), "closed_channel_param_grad_max": param_grad_max}


@torch.no_grad()
def commutators() -> dict:
    """Do the complement gates A(x) = N diag(r(x)) Nᵀ commute across inputs? (Necessary for any fixed basis that makes them diagonal.)"""
    out = {}
    for name in ("prot_success_43_29", "fixed005_success_43_43"):
        model = iv.load_model(name)[0]
        ref = ReferenceModel(model)
        x = c10.generator_batch(4, 2, 64, 16, seed=16_016)
        _, _, H = ref.forward(x)
        inputs = {0: model.embedding.weight[torch.arange(2, 30)], 1: model.norms[0](H[:, :, 0].reshape(-1, 32))[::7][:64]}
        row = {}
        for l, X in inputs.items():
            cell = ref.cells[l]
            _, aux = cell.step(X, torch.zeros(X.shape[0], 32))
            A = aux["A"]
            n = A.shape[0]
            vals = []
            for i in range(n):
                comm = A[i] @ A - A @ A[i]
                vals.append(comm.flatten(1).norm(dim=1) / (A[i].norm() * A.flatten(1).norm(dim=1)))
            v = torch.cat(vals)
            r = aux["r"]
            row[f"layer{l}"] = {"inputs": n, "normalized_commutator_max": float(v.max()), "normalized_commutator_median": float(v.median()),
                                "fast_gate_spread_across_units_median": float((r.max(1).values - r.min(1).values).median())}
        out[name] = row
    return out


@torch.no_grad()
def causal_equivalence() -> dict:
    """Exp 015 S-zero removal (mid) and Exp 014-style protected twin transplant (late) on original vs reference."""
    out = {}
    for name in ("prot_success_43_29", "fixed005_success_43_43"):
        model = iv.load_model(name)[0]
        ref = ReferenceModel(model)
        P = ne.build_pairs(64, 64)
        hist, twin = torch.cat([P.tok_a, P.tok_b]), torch.cat([P.tok_b, P.tok_a])
        Ps = model.cells[1].masks.T @ model.cells[1].masks
        rows = {}
        for label, timing in (("S_zero_mid", "mid_continuation"), ("S_twin_late", "late")):
            cut = (ne.cut_times(P, timing) if timing != "late" else P.cuts("late")).repeat(2)
            nat_twin = ne.run_events(model, twin, record=True)["nat"][:, :, 1]
            donor = nat_twin[torch.arange(hist.shape[0]), cut - 1]
            fn = (lambda h: h - h @ Ps) if label == "S_zero_mid" else (lambda h, d=donor: h - h @ Ps + d @ Ps)
            a = ne.run_events(model, hist, [(cut, 1, fn)])["logits"]
            b = ref_run_events(ref, hist, [(cut, 1, fn)])
            rows[label] = {"max_abs_logit_gap": float((a - b).abs().max()), "predictions_identical": bool(torch.equal(a.argmax(-1), b.argmax(-1)))}
        out[name] = rows
    return out


@torch.no_grad()
def ref_run_events(ref, hist, events):
    """Reference-model analogue of necessity_015.run_events: edits are expressed in h coordinates and mapped to rotated coordinates."""
    B, T = hist.shape
    emb = ref.embedding(hist)
    s = [torch.zeros(B, 32) for _ in ref.cells]

    def fire(t):
        for times, layer, fn in events:
            msk = (times == t)[:, None]
            if bool(msk.any()):
                cell = ref.cells[layer]
                s[layer] = torch.where(msk, cell.to_s(fn(cell.to_h(s[layer]))), s[layer])

    for t in range(T):
        fire(t)
        x = emb[:, t]
        for l, (cell, norm) in enumerate(zip(ref.cells, ref.norms)):
            s[l], _ = cell.step(x, s[l])
            x = norm(cell.to_h(s[l]))
    fire(T)
    logits = []
    for q in range(4):
        x = ref.embedding(torch.full((B,), c10.QUERY_START + q, dtype=torch.long))
        for l, (cell, norm) in enumerate(zip(ref.cells, ref.norms)):
            x = norm(cell.to_h(cell.step(x, s[l])[0]))
        logits.append(F.linear(ref.final_norm(x), ref.embedding.weight)[:, c10.VALUE_START:c10.VALUE_START + 2])
    return torch.stack(logits, 1)


def resources() -> dict:
    n, k, v, L = 32, 8, 32, 2
    prot = c13.build("protected", 1)
    out = {"parameters": {"protected": sum(p.numel() for p in prot.parameters()),
                          "protected_formula": v * n + L * (3 * n * n + n * k + 4 * n + k) + 2 * n,
                          "protected_live": 8016, "protected_fixed_gate_or_no_retain_live": 8016 - L * (n * k + k),
                          "gru24": sum(p.numel() for p in c10.build("gru24", 4, 2, 1).parameters()),
                          "gru32": sum(p.numel() for p in c10.build("gru32", 4, 2, 1).parameters())},
           "state_dimension_per_layer": {"protected": n, "gru24": 24, "gru32": 32},
           "macs_per_token_per_layer": {
               "protected_input_only (parallel over time)": n * n + n * k + n * n,
               "protected_recurrent (as implemented)": n * n + 7 * n * k,
               "protected_projection_overhead_within_recurrent": 7 * n * k,
               "reference_dense_matrix_gate_recurrent": n * n + 2 * n * k + (n - k) * (n - k) * n + 2 * (n - k) ** 2 + 2 * (n - k) * n,
               "reference_if_gate_applied_implicitly N(r⊙Nᵀz)": n * n + 2 * n * k + 4 * (n - k) * n,
               "gru24_input_only": 3 * 24 * 24, "gru24_recurrent": 3 * 24 * 24,
               "gru32_input_only": 3 * 32 * 32, "gru32_recurrent": 3 * 32 * 32},
           "gates_depend_on_state": {"protected": False, "gru": True}}
    torch.set_num_threads(1)
    ids = torch.randint(0, 32, (64, 72), generator=torch.Generator().manual_seed(9))
    timing = {}
    with torch.no_grad():
        for name, m in (("protected", prot), ("reference_dense_gate", ReferenceModel(prot)), ("gru24", c10.build("gru24", 4, 2, 1)),
                        ("gru32", c10.build("gru32", 4, 2, 1))):
            m(ids)
            t0 = time.perf_counter()
            for _ in range(5):
                m(ids)
            timing[name] = round((time.perf_counter() - t0) / 5 * 1000, 2)
    out["cpu_forward_ms_batch64_len72_1thread"] = timing
    return out


def main(argv=None):
    a = argv or sys.argv[1:]
    t0 = time.monotonic()
    res = {"grid": grid(), "closed_write_invariant": closed_write_invariant(), "commutators": commutators(),
           "causal_equivalence": causal_equivalence(), "resources": resources()}
    res["wall_s"] = round(time.monotonic() - t0, 1)
    Path(a[0]).parent.mkdir(parents=True, exist_ok=True)
    Path(a[0]).write_text(json.dumps(res, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in res.items() if k != "grid"} | {"grid": {k: v for k, v in res["grid"].items() if k != "rows"}}, indent=1))


if __name__ == "__main__":
    main()
