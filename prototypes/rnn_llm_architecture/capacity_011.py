"""Experiment 011: does a longer training budget solve four binary memory slots? CPU-only.

Reuses the Experiment 010 task, generator, label replay, models and optimizer settings
UNCHANGED (capacity_010); only the update budget, evaluation delays and tracking differ.
Every learned model of a paired seed sees a byte-identical training stream (fingerprinted).
Runs ONLY through explicit CLI. The explicit-address delta-rule model is an optional
reference, reported separately and never as a fair learned comparison.
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

from .capacity_010 import (VARIANTS, build, generator_batch, last_marked_value, metrics,
                           predictions, replay)

SLOTS = 4
VALUES = 2
LEARNED = ("protected", "protected_no_retain", "gru24", "gru32")
REFERENCE = ("delta_rule",)
EVAL_SEED_OFFSET = 11_000_000   # far above any training seed for steps <= 3000 (checked in tests)


def training_seed(seed: int, step: int) -> int:
    """Identical to capacity_010.run_one for slots=4, values=2; independent of the model."""
    return seed * 1_000_003 + step * 8191 + SLOTS * 197 + VALUES


def training_batch(cfg: "Config", seed: int, step: int):
    hist = generator_batch(SLOTS, VALUES, cfg.delay, cfg.batch, seed=training_seed(seed, step))
    return hist, replay(hist, SLOTS, VALUES)


@dataclass(frozen=True)
class Config:
    jobs: tuple[tuple[str, int], ...] = tuple((v, s) for s in (17, 29, 43) for v in LEARNED)
    steps: int = 3000
    batch: int = 12
    delay: int = 64
    eval_delays: tuple[int, ...] = (64, 128, 256, 512)
    eval_histories: int = 256
    checkpoint_every: int = 250
    checkpoint_histories: int = 128
    loss_window: int = 50
    lr: float = .002
    clip: float = 1.0
    max_wall_seconds: float = 1800.0

    def __post_init__(self):
        if not self.jobs or len(set(self.jobs)) != len(self.jobs):
            raise ValueError("bad jobs")
        for v, s in self.jobs:
            if v not in VARIANTS or type(s) is not int or s < 0:
                raise ValueError("bad job")
        if self.delay < 7 or not self.eval_delays or any(d < 7 for d in self.eval_delays):
            raise ValueError("bad delays")
        ints = (self.steps, self.batch, self.eval_histories, self.checkpoint_every,
                self.checkpoint_histories, self.loss_window)
        if any(type(x) is not int or x < 1 for x in ints):
            raise ValueError("bad budgets")
        if any(not math.isfinite(x) or x <= 0 for x in (self.lr, self.clip, self.max_wall_seconds)):
            raise ValueError("bad float budgets")


def baselines(x: torch.Tensor, y: torch.Tensor, seed: int) -> dict:
    """Ordinary (non-learned) controls on the same held-out histories."""
    g = torch.Generator(device="cpu").manual_seed(seed + 5)
    guess = torch.randint(VALUES, y.shape, generator=g)
    copy = last_marked_value(x, SLOTS, VALUES)[:, None].expand_as(y)
    return {"independent_guess": metrics(guess, y, VALUES),
            "last_write_copy": metrics(copy, y, VALUES),
            "analytic_guess_per_slot": 1 / VALUES, "analytic_guess_whole": VALUES ** -SLOTS}


@torch.no_grad()
def evaluate(model, delay: int, *, seed: int, histories: int, with_baselines: bool = False) -> dict:
    model.eval()
    x = generator_batch(SLOTS, VALUES, delay, histories, seed=seed)
    y = replay(x, SLOTS, VALUES)
    pred = torch.cat([predictions(model, x[a:a + 32], SLOTS, VALUES).argmax(-1)
                      for a in range(0, histories, 32)])
    out = metrics(pred, y, VALUES)
    out["histories"] = histories
    if with_baselines:
        out["baselines"] = baselines(x, y, seed)
    model.train()
    return out


def eval_seed(seed: int, delay: int) -> int:
    return EVAL_SEED_OFFSET + seed * 100_003 + delay


def run_one(name: str, seed: int, cfg: Config, deadline: float) -> dict:
    model = build(name, SLOTS, VALUES, seed)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    t0, c0 = time.monotonic(), time.process_time()
    stream = hashlib.sha256()
    steps, status, window, windows, checkpoints, losses = 0, "complete", [], [], [], []
    for step in range(cfg.steps):
        if time.monotonic() > deadline:
            status = "time_limit"
            break
        hist, labels = training_batch(cfg, seed, step)
        stream.update(hist.numpy().tobytes())
        opt.zero_grad(set_to_none=True)
        logits = predictions(model, hist, SLOTS, VALUES)
        loss = F.cross_entropy(logits.reshape(-1, VALUES), labels.reshape(-1))
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
        window.append(float(loss.detach()))
        if steps % cfg.loss_window == 0:
            windows.append({"step": steps, "mean_loss": sum(window) / len(window)})
            window = []
        if steps % cfg.checkpoint_every == 0 and steps < cfg.steps:
            ev = evaluate(model, cfg.delay, seed=eval_seed(seed, cfg.delay) + 1, histories=cfg.checkpoint_histories)
            checkpoints.append({"step": steps, "delay": cfg.delay, **{k: ev[k] for k in ("per_slot", "whole", "whole_varied")},
                                "elapsed_s": round(time.monotonic() - t0, 1)})
    train_s, train_cpu = time.monotonic() - t0, time.process_time() - c0
    out = {"variant": name, "reference_only": name in REFERENCE, "seed": seed, "status": status, "steps": steps,
           "parameters": sum(p.numel() for p in model.parameters()),
           "training_stream_sha256": stream.hexdigest(), "loss_windows": windows, "checkpoints": checkpoints,
           "train_wall_s": round(train_s, 2), "train_cpu_s": round(train_cpu, 2),
           "train_token_positions": steps * cfg.batch * (2 * SLOTS + cfg.delay + 1) * SLOTS}
    if steps > 0:
        out["eval"] = {str(d): evaluate(model, d, seed=eval_seed(seed, d), histories=cfg.eval_histories, with_baselines=True)
                       for d in cfg.eval_delays}
    out["total_wall_s"] = round(time.monotonic() - t0, 2)
    return out


def execute(cfg: Config, path: Path) -> dict:
    if path.exists():
        raise FileExistsError(path)
    torch.set_num_threads(1)
    began = time.monotonic()
    deadline = began + cfg.max_wall_seconds
    result = {"status": "running", "experiment": 11, "config": asdict(cfg), "task": {"slots": SLOTS, "values": VALUES},
              "environment": {"torch": torch.__version__, "cpu_threads": torch.get_num_threads(), "python": platform.python_version(),
                              "cuda_available": torch.cuda.is_available(), "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES")},
              "scope": "optimization-vs-capacity screen on a synthetic 4-slot binary task. delta_rule is an explicit-address reference, "
                       "not a fair learned comparison. Low accuracy is not evidence of capacity limits.",
              "runs": [], "skipped": []}
    try:
        for i, (name, seed) in enumerate(cfg.jobs):
            if time.monotonic() > deadline:
                result["skipped"] = [{"variant": n, "seed": s, "reason": "wall_budget"} for n, s in cfg.jobs[i:]]
                break
            row = run_one(name, seed, cfg, deadline)
            result["runs"].append(row)
            e = row.get("eval", {}).get(str(cfg.delay), {})
            print(json.dumps({"done": len(result["runs"]), "of": len(cfg.jobs), "variant": name, "seed": seed, "status": row["status"],
                              "steps": row["steps"], "per_slot": e.get("per_slot"), "whole_varied": e.get("whole_varied"),
                              "wall_s": row["total_wall_s"]}), flush=True)
    finally:
        result["elapsed_seconds"] = round(time.monotonic() - began, 3)
        ok = not result["skipped"] and len(result["runs"]) == len(cfg.jobs) and all(r["status"] == "complete" for r in result["runs"])
        result["status"] = "complete" if ok else "incomplete"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    return result


def parse_jobs(text: str) -> tuple[tuple[str, int], ...]:
    jobs = []
    for item in text.split(","):
        name, _, seed = item.partition(":")
        jobs.append((name, int(seed)))
    return tuple(jobs)


def main(argv=None):
    p = argparse.ArgumentParser(description="Experiment 011: bounded CPU four-slot training-budget study")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--jobs", default=",".join(f"{v}:{s}" for v, s in Config.jobs), help="variant:seed,variant:seed,...")
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--batch", type=int, default=12)
    p.add_argument("--delay", type=int, default=64)
    p.add_argument("--eval-delays", default="64,128,256,512")
    p.add_argument("--eval-histories", type=int, default=256)
    p.add_argument("--checkpoint-every", type=int, default=250)
    p.add_argument("--checkpoint-histories", type=int, default=128)
    p.add_argument("--max-wall-seconds", type=float, default=1800)
    a = p.parse_args(argv)
    cfg = Config(jobs=parse_jobs(a.jobs), steps=a.steps, batch=a.batch, delay=a.delay,
                 eval_delays=tuple(int(x) for x in a.eval_delays.split(",")), eval_histories=a.eval_histories,
                 checkpoint_every=a.checkpoint_every, checkpoint_histories=a.checkpoint_histories,
                 max_wall_seconds=a.max_wall_seconds)
    r = execute(cfg, a.output)
    print(f"Experiment 011: {r['status']} {len(r['runs'])} runs, {len(r['skipped'])} skipped, {r['elapsed_seconds']} seconds")


if __name__ == "__main__":
    main()
