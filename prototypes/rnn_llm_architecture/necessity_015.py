"""Experiment 015: causal NECESSITY and selectivity of layer-1 protected coefficients in already-trained networks.

Read-only use of saved checkpoints (models and loaders from intervene_014, verified there to reproduce the archives exactly).
No training. Interventions edit the layer-1 recurrent state of the *current* run at chosen times, then the run continues on
the unchanged suffix and the four queries are read.

Removal of a subspace S (projector P, 8-d unless stated) from a layer-1 state h:
  mean     h - hP + mu P            mu = time-matched population mean of natural layer-1 states (reference histories)
  zero     h - hP
  twin     h - hP + h_twin P        natural state of the paired history that differs only in the target slot's value
  same/diff h - hP + h_ref P        natural state of an UNRELATED reference history whose target slot holds the same / the other value
  normrand h + u, u in S random, |u| = |(mu - h) P_protected|   (magnitude matched to the protected mean-removal)
Rescue: after a removal at time k, at the query time the S-component is reset to the clean run's own S-component (the
complement keeps whatever it evolved into); the control rescue resets the complement instead.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from . import capacity_012 as c12
from . import intervene_014 as iv

SLOTS, VALUES, WIDTH = 4, 2, 32
PAIR_SEED_BASE = 400_000_000      # fresh held-out pairs (Exp 014 used 300M); disjoint from training (<70M), eval (100M), probes (200M)
REF_SEED_BASE = 410_000_000       # reference histories for population means and natural unrelated donors
N_REF = 512
DELAYS = (64, 128, 256)
TIMINGS = ("after_write", "mid_continuation", "before_query")
LAYER = 1
MODELS = ("prot_success_43_29", "prot_success_43_43", "fixed005_success_43_43", "gru32_success_43_43",
          "prot_failed_17_17", "prot_partial_43_17")


# ------------------------------------------------------------------------------------------------ data
def build_pairs(delay: int, n: int = 256, base: int = PAIR_SEED_BASE) -> iv.Pairs:
    """Same construction as intervene_014.build_pairs (flip the value of one slot's LAST write) with a fresh seed."""
    x = c10.generator_batch(SLOTS, VALUES, delay, n, seed=base + delay)
    y = c10.replay(x, SLOTS, VALUES)
    last = c12.last_write_positions(x)
    s = torch.arange(n) % SLOTS
    p = last[torch.arange(n), s]
    xb = x.clone()
    xb[torch.arange(n), p] = c10.VALUE_START + (1 - (x[torch.arange(n), p] - c10.VALUE_START))
    return iv.Pairs(delay, x, xb, s, p, y, c10.replay(xb, SLOTS, VALUES))


def cut_times(P: iv.Pairs, timing: str) -> torch.Tensor:
    """Index of the token BEFORE which layer-1 state is edited (T = after the whole history, right before the query)."""
    after = P.pos + 1
    if timing == "after_write":
        return after
    if timing == "mid_continuation":
        return after + (P.T - after) // 2
    return torch.full_like(after, P.T)


def values_over_time(x: torch.Tensor) -> torch.Tensor:
    """[B,T,S] stored value of each slot after each token (-1 = not yet written); same semantics as replay."""
    b, t = x.shape
    cur = torch.full((b, SLOTS), -1, dtype=torch.long)
    pending = torch.full((b,), -1, dtype=torch.long)
    out = torch.empty((b, t, SLOTS), dtype=torch.long)
    for j in range(t):
        tok = x[:, j]
        val = (tok >= c10.VALUE_START) & (tok < c10.VALUE_START + VALUES) & (pending >= 0)
        for s in range(SLOTS):
            cur[:, s] = torch.where(val & (pending == s), tok - c10.VALUE_START, cur[:, s])
        pending = torch.where((tok >= c10.WRITE_START) & (tok < c10.WRITE_START + SLOTS), tok - c10.WRITE_START, torch.full_like(pending, -1))
        out[:, j] = cur
    return out


# ------------------------------------------------------------------------------------------------ stepper with callbacks
@torch.no_grad()
def run_events(model, hist: torch.Tensor, events=(), record: bool = False):
    """Time-major scan like intervene_014.staged_run, but each event (times[B], layer, fn) replaces the CURRENT layer state
    h_l by fn(h_l) for samples whose time equals t, right before token t (t == T: before the queries)."""
    B, T = hist.shape
    L = len(model.cells)
    prot = iv.is_protected(model)
    emb = model.embedding(hist)
    h = [torch.zeros(B, WIDTH) for _ in range(L)]
    nat = torch.zeros(B, T, L, WIDTH) if record else None
    applied = []

    def advance(l, x, hl):
        cell = model.cells[l]
        return cell.step(cell.prepare(x), hl, None) if prot else cell(x, hl)

    def fire(t):
        for times, layer, fn in events:
            m = (times == t)[:, None]
            if bool(m.any()):
                new = fn(h[layer])
                applied.append((t, layer, new, m))
                h[layer] = torch.where(m, new, h[layer])

    for t in range(T):
        fire(t)
        x = emb[:, t]
        for l in range(L):
            h[l] = advance(l, x, h[l])
            x = model.norms[l](h[l])
            if record:
                nat[:, t, l] = h[l]
    fire(T)
    logits = []
    for q in range(SLOTS):
        x = model.embedding(torch.full((B,), c10.QUERY_START + q, dtype=torch.long))
        for l in range(L):
            x = model.norms[l](advance(l, x, h[l]))
        logits.append(F.linear(model.final_norm(x), model.embedding.weight)[:, c10.VALUE_START:c10.VALUE_START + VALUES])
    return {"logits": torch.stack(logits, 1), "final": torch.stack(h, 1), "nat": nat}


# ------------------------------------------------------------------------------------------------ setup per model / delay
def designated_projector(model) -> torch.Tensor:
    return model.cells[LAYER].masks.T @ model.cells[LAYER].masks if iv.is_protected(model) else iv.walsh_projector()


class Context:
    """Everything one (model, delay) needs: pairs, clean runs, reference bank, time-matched means."""

    def __init__(self, model, delay: int, n_pairs: int = 256):
        self.model, self.delay = model, delay
        self.P = build_pairs(delay, n_pairs)
        self.hist = torch.cat([self.P.tok_a, self.P.tok_b])                  # recipients: both members of every pair
        self.twin = torch.cat([self.P.tok_b, self.P.tok_a])
        self.slot = torch.cat([self.P.slot, self.P.slot])
        self.lab = torch.cat([self.P.y_a, self.P.y_b])
        self.lab_twin = torch.cat([self.P.y_b, self.P.y_a])
        self.pos = torch.cat([self.P.pos, self.P.pos])
        self.n = self.hist.shape[0]
        self.T = self.hist.shape[1]
        clean = run_events(model, self.hist, record=True)
        self.nat = clean["nat"][:, :, LAYER]                                   # [N,T,W] recipient layer-1 states
        self.pred = clean["logits"].argmax(-1)
        self.nat_twin = run_events(model, self.twin, record=True)["nat"][:, :, LAYER]
        ref = c10.generator_batch(SLOTS, VALUES, delay, N_REF, seed=REF_SEED_BASE + delay)
        self.ref_nat = run_events(model, ref, record=True)["nat"][:, :, LAYER]    # [R,T,W]
        self.ref_vals = values_over_time(ref)                                       # [R,T,S]
        self.mu = self.ref_nat.mean(0)                                              # [T,W] time-matched mean
        g = torch.Generator().manual_seed(15_000 + delay)
        bank = self.ref_nat[:, 2 * SLOTS:].reshape(-1, WIDTH)
        self.bank = bank[torch.randperm(bank.shape[0], generator=g)[:20000]]
        self.Ps = designated_projector(model)
        self.rand = iv.random_projectors()
        i = torch.arange(self.n)
        self.target_ok = self.pred[i, self.slot] == self.lab[i, self.slot]
        self.all_ok = (self.pred == self.lab).all(1)
        twin_pred = run_events(model, self.twin)["logits"].argmax(-1)
        self.twin_ok = twin_pred[i, self.slot] == self.lab_twin[i, self.slot]

    def at(self, arr_t, cut):
        """arr_t [N,T,W] -> state after token cut-1 for each sample ([N,W]); cut == 0 never occurs (writes start at token 1)."""
        return arr_t[torch.arange(self.n), cut - 1]

    def unrelated_donor(self, cut: torch.Tensor, same: bool) -> tuple[torch.Tensor, torch.Tensor]:
        """Natural layer-1 state of a reference history whose target slot holds the same / the other value at that time."""
        want = self.lab[torch.arange(self.n), self.slot] if same else 1 - self.lab[torch.arange(self.n), self.slot]
        donor = torch.zeros(self.n, WIDTH)
        ok = torch.zeros(self.n, dtype=torch.bool)
        for b in range(self.n):
            t = int(cut[b]) - 1
            vals = self.ref_vals[:, t, int(self.slot[b])]
            order = (torch.arange(N_REF) + (b * 37) % N_REF) % N_REF
            hit = order[vals[order] == want[b]]
            if len(hit):
                donor[b] = self.ref_nat[int(hit[0]), t]
                ok[b] = True
        return donor, ok

    def nn_ratio(self, states: torch.Tensor, natural: torch.Tensor) -> float:
        """Median distance to the nearest natural reference state, relative to the same quantity for unedited states."""
        d = torch.cdist(states, self.bank).min(1).values
        d0 = torch.cdist(natural, self.bank).min(1).values
        return float(d.median() / d0.median().clamp_min(1e-12))


# ------------------------------------------------------------------------------------------------ variants
def remove(h, P, ref):
    return h - h @ P + (0 if ref is None else ref @ P)


def removal_variants(ctx: Context, timing: str):
    """Returns {name: (events, info)}; info carries the per-sample donor value expectations and validity masks."""
    cut = cut_times(ctx.P, timing).repeat(2)
    Ps, I = ctx.Ps, torch.eye(WIDTH)
    Pc = I - Ps
    h0 = ctx.at(ctx.nat, cut)
    mu = ctx.mu[cut - 1]
    twin = ctx.at(ctx.nat_twin, cut)
    same, ok_same = ctx.unrelated_donor(cut, True)
    diff, ok_diff = ctx.unrelated_donor(cut, False)
    mag = ((mu - h0) @ Ps).norm(dim=1, keepdim=True)
    gen = torch.Generator().manual_seed(15_100 + ctx.delay)
    out = {}
    ev = lambda fn: [(cut, LAYER, fn)]
    out["sham"] = (ev(lambda h: h.clone()), {})
    out["S_mean"] = (ev(lambda h: remove(h, Ps, mu)), {})
    out["S_zero"] = (ev(lambda h: remove(h, Ps, None)), {})
    out["S_twin"] = (ev(lambda h: remove(h, Ps, twin)), {"donor_value": "twin"})
    out["S_unrelated_same"] = (ev(lambda h: remove(h, Ps, same)), {"valid": ok_same, "donor_value": "same"})
    out["S_unrelated_diff"] = (ev(lambda h: remove(h, Ps, diff)), {"valid": ok_diff, "donor_value": "diff"})
    out["C_mean"] = (ev(lambda h: remove(h, Pc, mu)), {})
    out["C_twin"] = (ev(lambda h: remove(h, Pc, twin)), {"donor_value": "twin"})
    out["C_unrelated_diff"] = (ev(lambda h: remove(h, Pc, diff)), {"valid": ok_diff, "donor_value": "diff"})
    out["full_mean"] = (ev(lambda h: mu.clone()), {})
    out["full_twin"] = (ev(lambda h: twin.clone()), {"donor_value": "twin"})
    u_full = torch.randn(ctx.n, WIDTH, generator=gen)
    out["fullspace_normrand"] = (ev(lambda h, u=u_full / u_full.norm(dim=1, keepdim=True) * mag: h + u), {})
    for i, R in enumerate(ctx.rand):
        out[f"R8_mean_b{i}"] = (ev(lambda h, R=R: remove(h, R, mu)), {})
        u = torch.randn(ctx.n, WIDTH, generator=gen) @ R
        out[f"R8_normrand_b{i}"] = (ev(lambda h, u=u / u.norm(dim=1, keepdim=True).clamp_min(1e-12) * mag: h + u), {})
        out[f"R24_mean_b{i}"] = (ev(lambda h, R=R: remove(h, I - R, mu)), {})
    if timing != "before_query":
        T = torch.full_like(cut, ctx.T)
        orig_T = ctx.at(ctx.nat, T)
        out["S_mean_rescue_S"] = ([(cut, LAYER, lambda h: remove(h, Ps, mu)), (T, LAYER, lambda h: remove(h, Ps, orig_T))], {})
        out["S_mean_rescue_C"] = ([(cut, LAYER, lambda h: remove(h, Ps, mu)), (T, LAYER, lambda h: remove(h, Pc, orig_T))], {})
        out["C_mean_rescue_C"] = ([(cut, LAYER, lambda h: remove(h, Pc, mu)), (T, LAYER, lambda h: remove(h, Pc, orig_T))], {})
        for i, R in enumerate(ctx.rand[:2]):
            out[f"R8_mean_b{i}_rescue_R"] = ([(cut, LAYER, lambda h, R=R: remove(h, R, mu)), (T, LAYER, lambda h, R=R: remove(h, R, orig_T))], {})
    return cut, h0, out


def score(ctx: Context, pred: torch.Tensor, info: dict) -> dict:
    i = torch.arange(ctx.n)
    s = ctx.slot
    valid = info.get("valid", torch.ones(ctx.n, dtype=torch.bool))
    tgt = pred[i, s] == ctx.lab[i, s]
    other = torch.ones_like(pred, dtype=torch.bool)
    other[i, s] = False
    oth_acc = ((pred == ctx.lab) & other).float().sum(1) / 3
    oth_agree = ((pred == ctx.pred) & other).float().sum(1) / 3
    dv = info.get("donor_value")
    if dv == "twin":
        donor = pred[i, s] == ctx.lab_twin[i, s]
    elif dv == "diff":
        donor = pred[i, s] != ctx.lab[i, s]
    else:
        donor = None
    res = {}
    elig_twin = ctx.target_ok & ctx.twin_ok
    for tag, m in (("all", valid), ("eligible", valid & (elig_twin if dv == "twin" else ctx.target_ok)), ("fully_eligible", valid & ctx.all_ok)):
        n = int(m.sum())
        row = {"n": n, "fraction": n / ctx.n}
        if n:
            row.update({"target_acc": float(tgt[m].float().mean()), "target_ci95": iv.wilson(int(tgt[m].sum()), n),
                        "other_acc": float(oth_acc[m].mean()), "other_agree_with_original": float(oth_agree[m].mean())})
            if donor is not None:
                row["donor_value_rate"] = float(donor[m].float().mean())
        res[tag] = row
    return res


def analyze(name: str, n_pairs: int = 256) -> dict:
    torch.set_num_threads(1)
    t0 = time.monotonic()
    model, spec = iv.load_model(name)
    out = {"model": name, "spec": {k: spec[k] for k in ("arch", "init", "data", "role")}, "protected_family": iv.is_protected(model),
           "weights_sha256": hashlib.sha256((iv.REPORTS / spec["weights"]).read_bytes()).hexdigest(),
           "archive_verification": iv.verify_against_archive(model, spec), "delays": {}}
    for d in DELAYS:
        ctx = Context(model, d, n_pairs)
        same_as_014 = iv.staged_run(model, ctx.hist[:32])["logits"]
        dd = {"pair_validation": iv.validate_pairs(ctx.P),
              "stepper_vs_014_stepper_max_logit_gap": float((run_events(model, ctx.hist[:32])["logits"] - same_as_014).abs().max()),
              "original": {"target_acc": float(ctx.target_ok.float().mean()), "all_four_correct": float(ctx.all_ok.float().mean()),
                           "eligible_target": int(ctx.target_ok.sum()), "n": ctx.n},
              "timings": {}}
        for timing in TIMINGS:
            cut, h0, vs = removal_variants(ctx, timing)
            nat_ratio_base = h0
            tres = {}
            for vname, (events, info) in vs.items():
                res = run_events(model, ctx.hist, events)
                row = score(ctx, res["logits"].argmax(-1), info)
                if len(events) == 1:
                    new = events[0][2](h0.clone())
                    row["off_distribution_nn_ratio"] = ctx.nn_ratio(new, nat_ratio_base)
                    row["edit_norm_median"] = float((new - h0).norm(dim=1).median())
                if vname == "sham":
                    row["sham_max_abs_logit_gap"] = float((res["logits"] - run_events(model, ctx.hist)["logits"]).abs().max())
                tres[vname] = row
            dd["timings"][timing] = {"cut_median": float(cut.float().median()), "variants": tres}
        out["delays"][str(d)] = dd
    out["wall_s"] = round(time.monotonic() - t0, 1)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Experiment 015: protected-coefficient necessity interventions (no training)")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--jobs", required=True, help="model id")
    p.add_argument("--pairs", type=int, default=256)
    p.add_argument("--max-wall-seconds", type=float, default=1200)
    a = p.parse_args(argv)
    if a.output.exists():
        raise FileExistsError(a.output)
    res = analyze(a.jobs, a.pairs)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump({"experiment": 15, "result": res}, f, indent=1)
    print(f"Experiment 015 {a.jobs}: done in {res['wall_s']} s")


if __name__ == "__main__":
    main()
