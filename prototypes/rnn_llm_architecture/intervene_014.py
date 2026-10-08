"""Experiment 014: causal state-transplant interventions and memory-separation measurements on saved checkpoints.

Isolated experiment code. Models are rebuilt with the unchanged `capacity_010.build` / `capacity_013.build`, loaded from saved
weights (or, for the GRU-32, reproduced deterministically and verified against Experiment 012), and then only *read*:
no training happens in the intervention stage.

Design (preregistered in EXPERIMENT_014_PLAN.md):
- A pair is two held-out histories that differ in exactly ONE token: the last write of one slot has its value bit flipped.
  Write locations, all other slot values, fillers, decoys and the continuation are identical; exactly one slot's correct
  answer differs (checked with the independent `capacity_010.replay`).
- Both recurrent layers' complete states are read at a cut point after the differing write and re-injected into the
  other history's run, which then continues on the identical suffix.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from . import capacity_012 as c12
from . import capacity_013 as c13
from .model import sum_free_walsh_bank

SLOTS, VALUES, WIDTH = 4, 2, 32
PAIR_SEED_BASE = 300_000_000           # disjoint from training seeds (< 70M), Exp 012 evaluation (100M) and probes (200M)
LATE_GAP = 8                           # "late" cut = 8 history tokens before the query (or just after the write, if later)
LAYER_SETS = {"l0": (0,), "l1": (1,), "both": (0, 1)}
N_BASES = 8
DELAYS = (64, 128, 256)

HERE = Path(__file__).parent
REPORTS = HERE / "reports"

MODELS = {
    "prot_success_43_29": dict(arch="protected", init=43, data=29, role="successful learned-gate protected RNN",
                               weights="experiment_013/weights/protected_i43_d29_s3000.pt", archived="experiment_012/protected_43_29.json"),
    "prot_success_43_43": dict(arch="protected", init=43, data=43, role="successful learned-gate protected RNN (replicate)",
                               weights="experiment_013/weights/protected_i43_d43_s3000.pt", archived="experiment_012/protected_43_43.json"),
    "fixed005_success_43_43": dict(arch="protected_fixed_005", init=43, data=43, role="successful fixed-0.005-gate protected RNN",
                                   weights="experiment_013/weights_confirm/protected_fixed_005_i43_d43_s3000.pt",
                                   archived="experiment_013/confirm/protected_fixed_005_43_43.json"),
    "prot_partial_43_17": dict(arch="protected", init=43, data=17, role="partially trained protected RNN (wv@64 42.9%)",
                               weights="experiment_013/weights/protected_i43_d17_s3000.pt", archived="experiment_012/protected_43_17.json"),
    "prot_partial_29_29": dict(arch="protected", init=29, data=29, role="partially trained protected RNN (wv@64 12.4%)",
                               weights="experiment_013/weights/protected_i29_d29_s3000.pt", archived="experiment_012/protected_29_29.json"),
    "prot_failed_17_17": dict(arch="protected", init=17, data=17, role="failed (plateau) protected RNN",
                              weights="experiment_013/weights/protected_i17_d17_s3000.pt", archived="experiment_012/protected_17_17.json"),
    "gru32_success_43_43": dict(arch="gru32", init=43, data=43, role="successful GRU-32 (ordinary recurrence), reproduced",
                                weights="experiment_014/weights/gru32_i43_d43_s3000.pt", archived="experiment_012/gru32_43_43.json"),
}


# ----------------------------------------------------------------------------------------------------------- models
def build_model(arch: str, init_seed: int):
    if arch == "gru32":
        return c10.build("gru32", SLOTS, VALUES, init_seed)
    return c13.build(arch, init_seed)


def is_protected(model) -> bool:
    return type(model.cells[0]).__name__ == "ProtectedMemoryCell"


def load_model(name: str):
    spec = MODELS[name]
    model = build_model(spec["arch"], spec["init"])
    model.load_state_dict(torch.load(REPORTS / spec["weights"]))
    model.eval()
    return model, spec


def verify_against_archive(model, spec) -> dict:
    """Reconstructed weights must reproduce the archived four-delay evaluation exactly."""
    arch = json.loads((REPORTS / spec["archived"]).read_text(encoding="utf-8-sig"))["runs"][0]
    out, ok = {}, True
    for d in ("64", "128", "256", "512"):
        e = c12.evaluate(model, int(d), seed=c12.eval_seed(int(d)), histories=512, detailed=False)
        same = all(e[k] == arch["eval"][d][k] for k in ("per_slot", "whole", "whole_varied"))
        out[d] = {"reconstructed": {k: e[k] for k in ("per_slot", "whole", "whole_varied")},
                  "archived": {k: arch["eval"][d][k] for k in ("per_slot", "whole", "whole_varied")}, "identical": same}
        ok &= same
    model.eval()
    return {"all_identical": ok, "by_delay": out, "archived_outcome": arch["outcome"]}


def walsh_projector(width: int = WIDTH, channels: int = 8) -> torch.Tensor:
    M = sum_free_walsh_bank(width, channels).sign() / math.sqrt(width)
    return M.T @ M


def random_projectors(n: int = N_BASES, width: int = WIDTH, k: int = 8) -> list[torch.Tensor]:
    out = []
    for i in range(n):
        g = torch.Generator().manual_seed(14_000 + i)
        q, _ = torch.linalg.qr(torch.randn(width, k, generator=g))
        out.append(q @ q.T)
    return out


# ----------------------------------------------------------------------------------------------------------- stepper
@torch.no_grad()
def staged_run(model, hist: torch.Tensor, cut: torch.Tensor | None = None, inter: list[torch.Tensor] | None = None, record: bool = False):
    """Time-major scan of `hist` [B,T] from the zero state, followed by the four query tokens.

    If `inter` (list of per-layer [B,W] replacement states) is given, each sample's states are replaced by `inter` right BEFORE
    it processes token `cut[b]` (cut == T means: after the whole history, before the queries). Returns value logits
    [B,4,2], pre-query states [B,L,W] and, if `record`, all states [B,T,L,W] (state after each token).
    """
    B, T = hist.shape
    L = len(model.cells)
    prot = is_protected(model)
    emb = model.embedding(hist)
    h = [torch.zeros(B, WIDTH) for _ in range(L)]
    nat = torch.zeros(B, T, L, WIDTH) if record else None

    def advance(l, x, hl):
        cell = model.cells[l]
        return cell.step(cell.prepare(x), hl, None) if prot else cell(x, hl)

    for t in range(T):
        if inter is not None:
            m = (cut == t)[:, None]
            if bool(m.any()):
                h = [torch.where(m, inter[l], h[l]) for l in range(L)]
        x = emb[:, t]
        for l in range(L):
            h[l] = advance(l, x, h[l])
            x = model.norms[l](h[l])
            if record:
                nat[:, t, l] = h[l]
    if inter is not None:
        m = (cut == T)[:, None]
        if bool(m.any()):
            h = [torch.where(m, inter[l], h[l]) for l in range(L)]
    logits = []
    for q in range(SLOTS):
        x = model.embedding(torch.full((B,), c10.QUERY_START + q, dtype=torch.long))
        for l in range(L):
            x = model.norms[l](advance(l, x, h[l]))
        logits.append(F.linear(model.final_norm(x), model.embedding.weight)[:, c10.VALUE_START:c10.VALUE_START + VALUES])
    return {"logits": torch.stack(logits, 1), "final": torch.stack(h, 1), "nat": nat}


@torch.no_grad()
def verify_stepper(model, hist: torch.Tensor, k: int = 40) -> dict:
    """Stepper vs the model's own forward (uninterrupted) and vs chunked recurrent inference through `forward(state=...)`."""
    n = min(hist.shape[0], 32)
    hist = hist[:n]
    queries = torch.arange(SLOTS) + c10.QUERY_START
    max_full = max_chunk = max_state = 0.0
    run = staged_run(model, hist, record=True)
    for q in range(SLOTS):
        ids = torch.cat([hist, queries[q].expand(n, 1)], 1)
        ref = model(ids)[0][:, -1, c10.VALUE_START:c10.VALUE_START + VALUES]
        max_full = max(max_full, float((ref - run["logits"][:, q]).abs().max()))
        _, state = model(ids[:, :k])
        chunk = model(ids[:, k:], state)[0][:, -1, c10.VALUE_START:c10.VALUE_START + VALUES]
        max_chunk = max(max_chunk, float((ref - chunk).abs().max()))
        for l in range(len(model.cells)):
            s = state[l] if isinstance(state[l], torch.Tensor) else state[l].hidden
            max_state = max(max_state, float((s - run["nat"][:, k - 1, l]).abs().max()))
    return {"max_abs_logit_diff_stepper_vs_forward": max_full, "max_abs_logit_diff_chunked_vs_uninterrupted": max_chunk,
            "max_abs_state_diff_stepper_vs_forward_state": max_state}


# ----------------------------------------------------------------------------------------------------------- pairs
@dataclass
class Pairs:
    delay: int
    tok_a: torch.Tensor
    tok_b: torch.Tensor
    slot: torch.Tensor
    pos: torch.Tensor
    y_a: torch.Tensor
    y_b: torch.Tensor

    @property
    def T(self):
        return self.tok_a.shape[1]

    def cuts(self, mode: str) -> torch.Tensor:
        early = self.pos + 1
        return early if mode == "early" else torch.maximum(early, torch.full_like(early, self.T - LATE_GAP))


def build_pairs(delay: int, n: int = 256) -> Pairs:
    x = c10.generator_batch(SLOTS, VALUES, delay, n, seed=PAIR_SEED_BASE + delay)
    y = c10.replay(x, SLOTS, VALUES)
    last = c12.last_write_positions(x)
    s = torch.arange(n) % SLOTS
    p = last[torch.arange(n), s]
    xb = x.clone()
    flipped = c10.VALUE_START + (1 - (x[torch.arange(n), p] - c10.VALUE_START))
    xb[torch.arange(n), p] = flipped
    yb = c10.replay(xb, SLOTS, VALUES)
    return Pairs(delay, x, xb, s, p, y, yb)


def validate_pairs(P: Pairs) -> dict:
    n = P.tok_a.shape[0]
    diff_tokens = (P.tok_a != P.tok_b).sum(1)
    diff_labels = (P.y_a != P.y_b)
    only_s = diff_labels.sum(1) == 1
    at_s = diff_labels[torch.arange(n), P.slot]
    same_writes = bool(torch.equal((P.tok_a >= c10.WRITE_START) & (P.tok_a < c10.WRITE_START + SLOTS),
                                   (P.tok_b >= c10.WRITE_START) & (P.tok_b < c10.WRITE_START + SLOTS)))
    return {"n": n, "histories_differ_in_exactly_one_token": bool((diff_tokens == 1).all()),
            "exactly_one_label_differs": bool(only_s.all()), "differing_label_is_changed_slot": bool(at_s.all()),
            "identical_write_locations": same_writes,
            "fraction_changed_write_in_initial_prefix": float((P.pos < 2 * SLOTS).float().mean())}


# ----------------------------------------------------------------------------------------------------------- transplants
def transform(kind: str, layers, hr: torch.Tensor, hd: torch.Tensor, proj: torch.Tensor | None, gen: torch.Generator | None = None):
    """New per-layer states for the recipient. hr/hd: [N,L,W] natural states at the cut; proj: [W,W] symmetric projector
    onto the intervened subspace S (designated Walsh, a random 8-d, ...). Layers outside `layers` are left untouched."""
    new = [hr[:, l].clone() for l in range(hr.shape[1])]
    for l in layers:
        r, d = hr[:, l], hd[:, l]
        P = proj[l] if isinstance(proj, (list, tuple)) else proj
        if kind == "full":
            new[l] = d.clone()
        elif kind == "sub":            # take the donor's component in S, keep the recipient's component outside S
            new[l] = r + (d - r) @ P
        elif kind == "comp":           # keep the recipient's component in S, take the donor's component outside S
            new[l] = d + (r - d) @ P
        elif kind == "noise":          # norm-matched random displacement inside S (no donor information)
            mag = ((d - r) @ P).norm(dim=1, keepdim=True)
            u = torch.randn(r.shape, generator=gen) @ P
            new[l] = r + u * mag / u.norm(dim=1, keepdim=True).clamp_min(1e-12)
        elif kind == "sham":
            new[l] = r.clone()
        else:
            raise ValueError(kind)
    return new


def variants(model) -> list[tuple[str, str, str, tuple[str, ...], object]]:
    """(name, kind, layer-set, family, projector spec). Spec is 'walsh' (cell masks / Walsh bank), 'rand<i>' or None."""
    prot = is_protected(model)
    out = [("sham", "sham", "both", ("control",), None)]
    for ls in LAYER_SETS:
        out.append((f"full_{ls}", "full", ls, ("A_full",), None))
    for ls in LAYER_SETS:
        out.append((f"{'prot' if prot else 'walsh8'}_{ls}", "sub", ls, ("B_protected" if prot else "B_walsh8_no_role",), "walsh"))
        out.append((f"{'fast' if prot else 'walsh_comp24'}_{ls}", "comp", ls, ("C_fast_complement" if prot else "C_walsh_complement",), "walsh"))
        out.append((f"noise_{'prot' if prot else 'walsh8'}_{ls}", "noise", ls, ("F_norm_matched_noise",), "walsh"))
        for i in range(N_BASES):
            out.append((f"rand8_b{i}_{ls}", "sub", ls, ("D_random8",), f"rand{i}"))
            out.append((f"rand24_b{i}_{ls}", "comp", ls, ("D_random24",), f"rand{i}"))
    return out


def projector_for(model, spec, rand) -> list[torch.Tensor] | torch.Tensor | None:
    if spec is None:
        return None
    if spec == "walsh":
        if is_protected(model):
            return [c.masks.T @ c.masks for c in model.cells]
        return walsh_projector()
    return rand[int(spec[4:])]


# ----------------------------------------------------------------------------------------------------------- metrics
def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - r) / d, 4), round((c + r) / d, 4)]


def score(pred_post: torch.Tensor, ctx: dict) -> dict:
    """Metrics over ordered (recipient, donor) pairs. `ctx` carries slot, labels and the un-intervened predictions."""
    s = ctx["slot"]
    idx = torch.arange(len(s))
    lab_r, lab_d = ctx["lab_r"], ctx["lab_d"]
    post_s = pred_post[idx, s]
    switched = post_s == lab_d[idx, s]
    kept = post_s == lab_r[idx, s]
    other = torch.ones_like(pred_post, dtype=torch.bool)
    other[idx, s] = False
    agree = (pred_post == ctx["pred_r"]) & other
    acc_other = ((pred_post == lab_r) & other)
    out = {}
    for tag, m in (("all", torch.ones_like(s, dtype=torch.bool)), ("eligible", ctx["eligible"]), ("fully_eligible", ctx["fully_eligible"])):
        n = int(m.sum())
        row = {"n": n, "fraction_of_pairs": n / len(s)}
        if n:
            row["switch_to_donor"] = float(switched[m].float().mean())
            row["switch_ci95"] = wilson(int(switched[m].sum()), n)
            row["kept_recipient_value"] = float(kept[m].float().mean())
            row["unchanged_slots_agree_with_original"] = float(agree[m].float().sum() / (3 * n))
            row["unchanged_slots_accuracy"] = float(acc_other[m].float().sum() / (3 * n))
        out[tag] = row
    for tag, m in (("eligible_initial_write", ctx["eligible"] & ctx["initial"]), ("eligible_rewritten", ctx["eligible"] & ~ctx["initial"])):
        n = int(m.sum())
        out[tag] = {"n": n, "switch_to_donor": float(switched[m].float().mean()) if n else None}
    return out


def intervention_suite(model, P: Pairs, mode: str, rand: list[torch.Tensor]) -> dict:
    """All state-transplant interventions for one delay and one cut mode; both transfer directions pooled."""
    n = P.tok_a.shape[0]
    cut = P.cuts(mode)
    run_a = staged_run(model, P.tok_a, record=True)
    run_b = staged_run(model, P.tok_b, record=True)
    idx = torch.arange(n)
    ha, hb = run_a["nat"][idx, cut - 1], run_b["nat"][idx, cut - 1]              # states after the token before the cut
    hist = torch.cat([P.tok_a, P.tok_b])
    cuts = torch.cat([cut, cut])
    hr, hd = torch.cat([ha, hb]), torch.cat([hb, ha])
    pred_orig = torch.cat([run_a["logits"].argmax(-1), run_b["logits"].argmax(-1)])
    pred_don = torch.cat([run_b["logits"].argmax(-1), run_a["logits"].argmax(-1)])
    ctx = {"slot": torch.cat([P.slot, P.slot]), "lab_r": torch.cat([P.y_a, P.y_b]), "lab_d": torch.cat([P.y_b, P.y_a]),
           "pred_r": pred_orig}
    s2 = ctx["slot"]
    i2 = torch.arange(2 * n)
    ok_r = pred_orig[i2, s2] == ctx["lab_r"][i2, s2]
    ok_d = pred_don[i2, s2] == ctx["lab_d"][i2, s2]
    ctx["eligible"] = ok_r & ok_d
    ctx["fully_eligible"] = (pred_orig == ctx["lab_r"]).all(1) & (pred_don == ctx["lab_d"]).all(1)
    ctx["initial"] = torch.cat([P.pos, P.pos]) < 2 * SLOTS
    out = {"cut_mode": mode, "pairs": n, "ordered_pairs": 2 * n,
           "original_changed_slot_accuracy": float(torch.cat([ok_r]).float().mean()),
           "fraction_eligible": float(ctx["eligible"].float().mean()), "variants": {}}
    gen = torch.Generator().manual_seed(14_500 + P.delay)
    sham_gap = 0.0
    for name, kind, ls, family, spec in variants(model):
        proj = projector_for(model, spec, rand)
        layers = LAYER_SETS[ls]
        if kind == "sham":
            new = transform("sham", layers, hr, hr, None)           # donor == recipient (same history, same state)
        else:
            new = transform(kind, layers, hr, hd, proj, gen)
        res = staged_run(model, hist, cuts, new)
        if kind == "sham":
            sham_gap = float((res["logits"] - torch.cat([run_a["logits"], run_b["logits"]])).abs().max())
        out["variants"][name] = {"family": family[0], "layers": ls, **score(res["logits"].argmax(-1), ctx)}
    out["sham_max_abs_logit_diff"] = sham_gap
    return out


# ----------------------------------------------------------------------------------------------------------- phase 5
def subspace_parts(model, h: torch.Tensor):
    """Split states [..., L, W] into designated-protected (or Walsh-8 for the GRU) and complement norms per layer."""
    if is_protected(model):
        Ps = [c.masks.T @ c.masks for c in model.cells]
    else:
        Ps = [walsh_projector()] * len(model.cells)
    prot = torch.stack([h[..., l, :] @ Ps[l] for l in range(len(Ps))], -2)
    return prot, h - prot


def phase5(model, P: Pairs, rand: list[torch.Tensor]) -> dict:
    """Local perturbation stability versus memory separation, on pairs whose changed write is in the initial prefix
    (so the identical suffix is at least `delay` tokens long)."""
    sel = P.pos < 2 * SLOTS
    n = int(sel.sum())
    ta, tb, cut = P.tok_a[sel], P.tok_b[sel], P.pos[sel] + 1
    idx = torch.arange(n)
    ra, rb = staged_run(model, ta, record=True), staged_run(model, tb, record=True)
    na, nb = ra["nat"], rb["nat"]
    T, L = ta.shape[1], na.shape[2]
    ha, hb = na[idx, cut - 1], nb[idx, cut - 1]
    d0 = (hb - ha).norm(dim=-1)                                      # [n,L] initial memory displacement per layer
    gen = torch.Generator().manual_seed(14_900 + P.delay)

    def perturbed(kind):
        if kind == "full":
            u = torch.randn(ha.shape, generator=gen)
        else:
            Ps = [c.masks.T @ c.masks for c in model.cells] if is_protected(model) else [walsh_projector()] * L
            u = torch.stack([torch.randn(n, WIDTH, generator=gen) @ Ps[l] for l in range(L)], 1)
        u = u / u.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        if kind == "prot":
            mag = (subspace_parts(model, hb - ha)[0]).norm(dim=-1)
        else:
            mag = d0
        new = ha + u * mag[..., None]
        res = staged_run(model, ta, cut, [new[:, l] for l in range(L)], record=True)
        return res["nat"]

    npert = {"random_full_space": perturbed("full"), "random_in_designated_subspace": perturbed("prot")}
    rels = [r for r in (0, 1, 2, 4, 8, 16, 32, 64, 128, 256) if r <= P.delay]
    tstar = torch.clamp(cut[:, None] - 1 + torch.tensor(rels)[None, :], max=T - 1)       # [n,R]
    gather = lambda arr: arr[idx[:, None], tstar]                                          # [n,R,L,W]
    A, B = gather(na), gather(nb)
    spread = (na[:, T - 1][:-1] - na[:, T - 1][1:]).norm(dim=-1).median(0).values            # natural spread between distinct histories
    out = {"delay": P.delay, "pairs_used": n, "relative_times": rels, "initial_displacement_median": d0.median(0).values.tolist(),
           "natural_state_spread_at_end_median": spread.tolist()}
    def persistence(dist):                                                   # [n,R,L] -> median ratio to initial displacement
        return (dist / d0[:, None, :].clamp_min(1e-12)).median(0).values.T.tolist()      # [L][R]
    dmem = (B - A).norm(dim=-1)
    out["memory_displacement_ratio"] = persistence(dmem)
    for name, arr in npert.items():
        out[f"{name}_displacement_ratio"] = persistence((gather(arr) - A).norm(dim=-1))
    pa, ca = subspace_parts(model, A)
    pb, cb = subspace_parts(model, B)
    out["memory_displacement_ratio_protected_part"] = persistence((pb - pa).norm(dim=-1))
    out["memory_displacement_ratio_complement_part"] = persistence((cb - ca).norm(dim=-1))
    out["memory_separation_at_end_over_natural_spread"] = ((nb[:, T - 1] - na[:, T - 1]).norm(dim=-1).median(0).values / spread).tolist()
    # interpolation / mixture test: does a half-way state snap to one of the two memory states, or stay in between?
    fa, fb = ra["final"].reshape(n, -1), rb["final"].reshape(n, -1)
    axis = fb - fa
    dend = axis.norm(dim=1)
    valid = dend > 1e-6
    lab_b = P.y_b[sel][idx, P.slot[sel]]
    interp = {}
    for alpha in (0.25, 0.5, 0.75):
        mixed = ha + alpha * (hb - ha)
        res = staged_run(model, ta, cut, [mixed[:, l] for l in range(L)])
        tau = ((res["final"].reshape(n, -1) - fa) * axis).sum(1) / dend.clamp_min(1e-12) ** 2
        off = ((res["final"].reshape(n, -1) - fa) - tau[:, None] * axis).norm(dim=1) / dend.clamp_min(1e-12)
        pred_s = res["logits"].argmax(-1)[idx, P.slot[sel]]
        interp[str(alpha)] = {"valid_pairs": int(valid.sum()), "tau_median": float(tau[valid].median()),
                              "fraction_near_an_endpoint(|tau| or |tau-1| < 0.15)": float((((tau.abs() < .15) | ((tau - 1).abs() < .15)) & valid).float().sum() / valid.sum().clamp_min(1)),
                              "fraction_predicting_B_value": float((pred_s == lab_b).float().mean()),
                              "off_axis_distance_median": float(off[valid].median()), "linear_reference_tau": alpha}
    out["interpolation"] = interp
    out["final_state_axis_length_median"] = float(dend.median())
    return out


# ----------------------------------------------------------------------------------------------------------- driver
def analyze_model(name: str, n_pairs: int = 256) -> dict:
    torch.set_num_threads(1)
    t0 = time.monotonic()
    model, spec = load_model(name)
    rand = random_projectors()
    res = {"model": name, "spec": {k: spec[k] for k in ("arch", "init", "data", "role")}, "protected_family": is_protected(model),
           "weights_sha256": hashlib.sha256((REPORTS / spec["weights"]).read_bytes()).hexdigest(),
           "archive_verification": verify_against_archive(model, spec)}
    pairs = {d: build_pairs(d, n_pairs) for d in DELAYS}
    res["pair_validation"] = {str(d): validate_pairs(p) for d, p in pairs.items()}
    res["stepper_verification"] = verify_stepper(model, pairs[64].tok_a)
    res["interventions"] = {str(d): {m: intervention_suite(model, p, m, rand) for m in ("late", "early")} for d, p in pairs.items()}
    res["phase5"] = {str(d): phase5(model, p, rand) for d, p in pairs.items()}
    res["wall_s"] = round(time.monotonic() - t0, 1)
    return res


def reproduce_gru32(init: int = 43, data: int = 43) -> dict:
    """Deterministically retrain the Experiment 012 GRU-32 run with weight snapshots; verify against the archive."""
    torch.set_num_threads(1)
    wdir = REPORTS / "experiment_014" / "weights"
    cfg = c13.Config(jobs=(("protected", init, data),), save_weights_at=(0, 3000))
    orig = c13.build
    c13.build = lambda name, i: c10.build("gru32", SLOTS, VALUES, i) if name == "gru32" else orig(name, i)
    try:
        row = c13.run_one("gru32", init, data, cfg, float("inf"), wdir)
    finally:
        c13.build = orig
    arch = json.loads((REPORTS / "experiment_012" / f"gru32_{init}_{data}.json").read_text(encoding="utf-8-sig"))["runs"][0]
    row["verification_vs_experiment_012"] = {"loss_per_step_identical": row["loss_per_step"] == arch["loss_per_step"],
                                            "eval_identical": row["eval"] == arch["eval"], "outcome": [row["outcome"], arch["outcome"]]}
    return row


def main(argv=None):
    p = argparse.ArgumentParser(description="Experiment 014: state-transplant interventions (no training except --stage reproduce)")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--stage", choices=("intervene", "reproduce"), default="intervene")
    p.add_argument("--jobs", default="", help="model id (launcher shard)")
    p.add_argument("--pairs", type=int, default=256)
    p.add_argument("--max-wall-seconds", type=float, default=1800)
    a = p.parse_args(argv)
    if a.output.exists():
        raise FileExistsError(a.output)
    res = reproduce_gru32() if a.stage == "reproduce" else analyze_model(a.jobs, a.pairs)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump({"experiment": 14, "stage": a.stage, "result": res}, f, indent=1)
    print(f"Experiment 014 {a.stage} {a.jobs}: done")


if __name__ == "__main__":
    main()
