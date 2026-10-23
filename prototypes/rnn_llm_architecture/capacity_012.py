"""Experiment 012: initialization seed x training-data seed factorial on the four-slot binary task. CPU-only.

Same task, generator, models and optimizer as Experiments 010/011 (imported unchanged). The ONLY change is that the
three randomness sources, which Experiment 011 tied to one number, are separate streams:

  init_seed  -> model initialization only (config.seed inside fork_rng)
  data_seed  -> training stream only (same formula as Experiment 011, so init==data cells replay Experiment 011 exactly)
  EVAL_SEED  -> ONE fixed held-out set per delay, shared by every model and independent of both of the above

Runs ONLY through explicit CLI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from .capacity_010 import QUERY_START, VALUE_START, WRITE_START, build, generator_batch, last_marked_value, predictions, replay
from .capacity_011 import baselines

SLOTS, VALUES = 4, 2
ARCHS = ("protected", "protected_no_retain", "gru24", "gru32")
SEEDS = (17, 29, 43)
EVAL_BASE = 100_000_000            # above every training seed used (< 70M); asserted in tests
CHECKPOINT_EVAL_SEED = 100_001_000
AGE_EDGES = (8, 16, 32, 64, 128, 256)

# ---- preregistered outcome definitions (fixed before the confirmatory run; calibrated only on Exp 011 curves) ----
ONSET_LOSS = 0.50      # a 50-update window mean below this counts as "learning"
SUCCESS_WHOLE_VARIED = 0.90


def training_seed(data_seed: int, step: int) -> int:
    return data_seed * 1_000_003 + step * 8191 + SLOTS * 197 + VALUES


def eval_seed(delay: int) -> int:
    return EVAL_BASE + delay


def learning_onset(windows: list[dict], window_len: int = 50, threshold: float = ONSET_LOSS):
    """Learning onset = number of optimizer updates completed BEFORE the first window from which EVERY later
    window mean loss is below `threshold` (sustained to the end of training). None if the last window is not below it.
    Each window dict carries `step` = updates completed at the window END."""
    if not windows or windows[-1]["mean_loss"] >= threshold:
        return None
    k = len(windows) - 1
    while k > 0 and windows[k - 1]["mean_loss"] < threshold:
        k -= 1
    return windows[k]["step"] - window_len


def outcome_class(onset, whole_varied_64) -> str:
    if onset is None:
        return "plateau_only"                       # initial convergence only; never sustained learning
    if whole_varied_64 is not None and whole_varied_64 >= SUCCESS_WHOLE_VARIED:
        return "success"
    return "partial"


@dataclass(frozen=True)
class Config:
    jobs: tuple[tuple[str, int, int], ...] = tuple((a, i, d) for a in ARCHS for i in SEEDS for d in SEEDS)
    steps: int = 3000
    batch: int = 12
    delay: int = 64
    eval_delays: tuple[int, ...] = (64, 128, 256, 512)
    eval_histories: int = 512
    checkpoint_every: int = 250
    checkpoint_histories: int = 128
    loss_window: int = 50
    lr: float = .002
    clip: float = 1.0
    max_wall_seconds: float = 1800.0

    def __post_init__(self):
        if not self.jobs or len(set(self.jobs)) != len(self.jobs):
            raise ValueError("bad jobs")
        for a, i, d in self.jobs:
            if a not in c10.VARIANTS or type(i) is not int or type(d) is not int or i < 0 or d < 0:
                raise ValueError("bad job")
        if self.delay < 7 or not self.eval_delays or any(x < 7 for x in self.eval_delays):
            raise ValueError("bad delays")
        if any(type(x) is not int or x < 1 for x in (self.steps, self.batch, self.eval_histories, self.checkpoint_every,
                                                       self.checkpoint_histories, self.loss_window)):
            raise ValueError("bad budgets")
        if any(not math.isfinite(x) or x <= 0 for x in (self.lr, self.clip, self.max_wall_seconds)):
            raise ValueError("bad float budgets")


def last_write_positions(tokens: torch.Tensor) -> torch.Tensor:
    """[B,S] token index of each slot's most recent marked VALUE write (same semantics as capacity_010.replay)."""
    b, t = tokens.shape
    pos = torch.full((b, SLOTS), -1, dtype=torch.long)
    pending = torch.full((b,), -1, dtype=torch.long)
    for j in range(t):
        tok = tokens[:, j]
        valid = (tok >= VALUE_START) & (tok < VALUE_START + VALUES) & (pending >= 0)
        for s in range(SLOTS):
            pos[:, s] = torch.where(valid & (pending == s), torch.full_like(pos[:, s], j), pos[:, s])
        pending = torch.where((tok >= WRITE_START) & (tok < WRITE_START + SLOTS), tok - WRITE_START, torch.full_like(pending, -1))
    return pos


def age_bucket(age: int, rewritten: bool) -> str:
    if not rewritten:
        return "initial_only"
    lo = 1
    for e in AGE_EDGES:
        if age <= e:
            return f"{lo}-{e}"
        lo = e + 1
    return f"{lo}+"


def pattern_ids(bits: torch.Tensor) -> torch.Tensor:
    return (bits << torch.arange(SLOTS)).sum(1)


def analyze(pred: torch.Tensor, x: torch.Tensor, y: torch.Tensor) -> dict:
    """Aggregate counts (not just rates) so later analysis can pool across runs."""
    out = c10.metrics(pred, y, VALUES)
    n = x.shape[0]
    out["histories"] = n
    out["per_slot_index"] = pred.eq(y).float().mean(0).tolist()
    out["pred_pattern_counts"] = torch.bincount(pattern_ids(pred), minlength=16).tolist()
    out["true_pattern_counts"] = torch.bincount(pattern_ids(y), minlength=16).tolist()
    last = last_marked_value(x, SLOTS, VALUES)[:, None].expand_as(y)
    varied = y.max(1).values != y.min(1).values
    same = pred.max(1).values == pred.min(1).values
    copy = pred.eq(last).all(1)
    out["collapse"] = {"all_slots_same_prediction": float(same.float().mean()),
                       "predicts_last_write_everywhere": float(copy.float().mean()),
                       "varied_all_slots_same_prediction": float(same[varied].float().mean()) if bool(varied.any()) else None,
                       "varied_predicts_last_write_everywhere": float(copy[varied].float().mean()) if bool(varied.any()) else None}
    pos = last_write_positions(x)
    t = x.shape[1]
    buckets: dict[str, list[int]] = {}
    for s in range(SLOTS):
        correct = pred[:, s].eq(y[:, s])
        for i in range(n):
            p = int(pos[i, s])
            key = age_bucket(t - p, p >= 2 * SLOTS)
            row = buckets.setdefault(key, [0, 0])
            row[0] += 1
            row[1] += int(correct[i])
    out["by_last_write_age"] = {k: {"n": v[0], "correct": v[1]} for k, v in sorted(buckets.items())}
    newest = pos.argmax(1)
    hit_new = pred.gather(1, newest[:, None]).squeeze(1).eq(y.gather(1, newest[:, None]).squeeze(1))
    mask = torch.ones_like(y, dtype=torch.bool)
    mask[torch.arange(n), newest] = False
    hit_other = pred.eq(y)[mask]
    out["most_recently_written_slot"] = {"n": n, "correct": int(hit_new.sum())}
    out["other_slots"] = {"n": int(mask.sum()), "correct": int(hit_other.sum())}
    return out


@torch.no_grad()
def evaluate(model, delay: int, *, seed: int, histories: int, with_baselines: bool = False, detailed: bool = True) -> dict:
    model.eval()
    x = generator_batch(SLOTS, VALUES, delay, histories, seed=seed)
    y = replay(x, SLOTS, VALUES)
    pred = torch.cat([predictions(model, x[a:a + 32], SLOTS, VALUES).argmax(-1) for a in range(0, histories, 32)])
    out = analyze(pred, x, y) if detailed else {**c10.metrics(pred, y, VALUES), "histories": histories}
    if with_baselines:
        out["baselines"] = baselines(x, y, seed)
    model.train()
    return out


def init_fingerprint(model) -> str:
    h = hashlib.sha256()
    for k, v in model.state_dict().items():
        h.update(k.encode())
        h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def run_one(name: str, init_seed: int, data_seed: int, cfg: Config, deadline: float) -> dict:
    model = build(name, SLOTS, VALUES, init_seed)          # init_seed ONLY influences initialization
    init_id = init_fingerprint(model)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    t0, c0 = time.monotonic(), time.process_time()
    stream = hashlib.sha256()
    steps, status, window, windows, checkpoints, per_step = 0, "complete", [], [], [], []
    for step in range(cfg.steps):
        if time.monotonic() > deadline:
            status = "time_limit"
            break
        hist = generator_batch(SLOTS, VALUES, cfg.delay, cfg.batch, seed=training_seed(data_seed, step))   # data_seed ONLY
        labels = replay(hist, SLOTS, VALUES)
        stream.update(hist.numpy().tobytes())
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(predictions(model, hist, SLOTS, VALUES).reshape(-1, VALUES), labels.reshape(-1))
        if not bool(torch.isfinite(loss)):
            status = "nonfinite_loss"
            break
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
            status = "nonfinite_grad"
            break
        torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.clip)
        opt.step()
        steps += 1
        v = float(loss.detach())
        per_step.append(round(v, 6))
        window.append(v)
        if steps % cfg.loss_window == 0:
            windows.append({"step": steps, "mean_loss": sum(window) / len(window)})
            window = []
        if steps % cfg.checkpoint_every == 0 and steps < cfg.steps:
            ev = evaluate(model, cfg.delay, seed=CHECKPOINT_EVAL_SEED, histories=cfg.checkpoint_histories, detailed=False)
            checkpoints.append({"step": steps, "delay": cfg.delay, **{k: ev[k] for k in ("per_slot", "whole", "whole_varied")}})
    out = {"architecture": name, "init_seed": init_seed, "data_seed": data_seed, "status": status, "steps": steps,
           "parameters": sum(p.numel() for p in model.parameters()),
           "init_fingerprint_sha256": init_id, "training_stream_sha256": stream.hexdigest(),
           "loss_per_step": per_step, "loss_windows": windows, "checkpoints": checkpoints,
           "train_wall_s": round(time.monotonic() - t0, 2), "train_cpu_s": round(time.process_time() - c0, 2)}
    if steps > 0:
        out["eval"] = {str(d): evaluate(model, d, seed=eval_seed(d), histories=cfg.eval_histories, with_baselines=True)
                       for d in cfg.eval_delays}
    out["total_wall_s"] = round(time.monotonic() - t0, 2)
    onset = learning_onset(windows, cfg.loss_window)
    out["learning_onset_step"] = onset
    wv = out.get("eval", {}).get(str(cfg.delay), {}).get("whole_varied")
    out["outcome"] = outcome_class(onset, wv) if steps > 0 and status == "complete" else f"incomplete:{status}"
    return out


def execute(cfg: Config, path: Path) -> dict:
    if path.exists():
        raise FileExistsError(path)
    torch.set_num_threads(1)
    began = time.monotonic()
    deadline = began + cfg.max_wall_seconds
    result = {"status": "running", "experiment": 12, "config": asdict(cfg), "task": {"slots": SLOTS, "values": VALUES},
              "preregistered": {"onset_loss": ONSET_LOSS, "success_whole_varied": SUCCESS_WHOLE_VARIED, "eval_base_seed": EVAL_BASE},
              "environment": {"torch": torch.__version__, "cpu_threads": torch.get_num_threads(), "python": platform.python_version(),
                              "cuda_available": torch.cuda.is_available(), "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES")},
              "runs": [], "skipped": []}
    try:
        for i, (name, init_seed, data_seed) in enumerate(cfg.jobs):
            if time.monotonic() > deadline:
                result["skipped"] = [{"architecture": n, "init_seed": a, "data_seed": b, "reason": "wall_budget"} for n, a, b in cfg.jobs[i:]]
                break
            row = run_one(name, init_seed, data_seed, cfg, deadline)
            result["runs"].append(row)
            e = row.get("eval", {}).get(str(cfg.delay), {})
            print(json.dumps({"done": len(result["runs"]), "of": len(cfg.jobs), "arch": name, "init": init_seed, "data": data_seed,
                              "status": row["status"], "steps": row["steps"], "outcome": row["outcome"], "onset": row["learning_onset_step"],
                              "whole_varied": e.get("whole_varied"), "wall_s": row["total_wall_s"]}), flush=True)
    finally:
        result["elapsed_seconds"] = round(time.monotonic() - began, 3)
        ok = not result["skipped"] and len(result["runs"]) == len(cfg.jobs) and all(r["status"] == "complete" for r in result["runs"])
        result["status"] = "complete" if ok else "incomplete"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
    return result


def parse_jobs(text: str) -> tuple[tuple[str, int, int], ...]:
    jobs = []
    for item in text.split(","):
        name, init_seed, data_seed = item.split(":")
        jobs.append((name, int(init_seed), int(data_seed)))
    return tuple(jobs)


def main(argv=None):
    p = argparse.ArgumentParser(description="Experiment 012: init-seed x data-seed factorial (bounded, CPU)")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--jobs", default=",".join(f"{a}:{i}:{d}" for a, i, d in Config.jobs), help="arch:init_seed:data_seed,...")
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--batch", type=int, default=12)
    p.add_argument("--delay", type=int, default=64)
    p.add_argument("--eval-delays", default="64,128,256,512")
    p.add_argument("--eval-histories", type=int, default=512)
    p.add_argument("--checkpoint-every", type=int, default=250)
    p.add_argument("--checkpoint-histories", type=int, default=128)
    p.add_argument("--max-wall-seconds", type=float, default=1800)
    a = p.parse_args(argv)
    cfg = Config(jobs=parse_jobs(a.jobs), steps=a.steps, batch=a.batch, delay=a.delay,
                 eval_delays=tuple(int(x) for x in a.eval_delays.split(",")), eval_histories=a.eval_histories,
                 checkpoint_every=a.checkpoint_every, checkpoint_histories=a.checkpoint_histories, max_wall_seconds=a.max_wall_seconds)
    r = execute(cfg, a.output)
    print(f"Experiment 012: {r['status']} {len(r['runs'])} runs, {len(r['skipped'])} skipped, {r['elapsed_seconds']} seconds")


if __name__ == "__main__":
    main()
