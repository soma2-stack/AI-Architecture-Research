"""Experiment 013: is the protected RNN's learned slow-write gate necessary, or does a fixed write rate suffice? CPU-only.

Isolated experiment code; candidates.py and every earlier module are imported UNCHANGED.

Fixed-gate controls start from the exact `protected` model of the same init seed (identical initial weights, Walsh masks,
recurrent operator, slow feedback, fast gate, width, optimizer) and replace ONLY the slow-write gate output that
`ProtectedMemoryCell.prepare` returns, `sigmoid(slow_gate(x))`, with a constant g. The coefficient update in `step()` is
untouched:  c_t = c_{t-1} + g * (P tanh(drive + U h_{t-1}) - c_{t-1}).
With g = 1 this is exactly `protected_no_retain` (verified bit-for-bit in tests).

The training loop, data streams, evaluation sets, outcome definitions and record format are those of Experiment 012
(capacity_012), so Experiment 012 runs of `protected` / `protected_no_retain` are directly comparable and reused.
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
import types
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

from . import capacity_010 as c10
from . import capacity_012 as c12

SLOTS, VALUES = c12.SLOTS, c12.VALUES
SIGMOID_MINUS_3 = 1.0 / (1.0 + math.exp(3.0))       # 0.0474258731775668
FIXED = {"protected_fixed_0474": SIGMOID_MINUS_3, "protected_fixed_005": 0.005,
         "protected_fixed_1": 1.0}                    # fixed_1 == protected_no_retain (validation only)
REUSED = ("protected", "protected_no_retain")
ARCHS = REUSED + tuple(FIXED)


def _fixed_prepare(self, x):
    """Same drive and fast gate as ProtectedMemoryCell.prepare; slow gate output replaced by a constant."""
    c = self.slow_gate.out_features
    return (self.x_to_candidate(x), x.new_full((*x.shape[:-1], c), self._fixed_slow_write),
            torch.sigmoid(self.fast_gate(x)))


def fix_slow_gate(model, value: float):
    if not 0.0 < value <= 1.0:
        raise ValueError("fixed write rate must lie in (0, 1]")
    for cell in model.cells:
        if type(cell).__name__ != "ProtectedMemoryCell" or not cell.config.retain_slow:
            raise ValueError("fixed gate applies only to the original retaining protected cell")
        cell._fixed_slow_write = float(value)
        cell.prepare = types.MethodType(_fixed_prepare, cell)
    return model


def build(name: str, init_seed: int):
    if name in REUSED:
        return c10.build(name, SLOTS, VALUES, init_seed)
    if name in FIXED:
        return fix_slow_gate(c10.build("protected", SLOTS, VALUES, init_seed), FIXED[name])
    raise ValueError(f"unknown architecture {name}")


def live_parameter_count(model) -> int:
    """Parameters that receive a nonzero gradient on one real training batch."""
    x = c10.generator_batch(SLOTS, VALUES, 64, 12, seed=1)
    y = c10.replay(x, SLOTS, VALUES)
    model.zero_grad(set_to_none=True)
    F.cross_entropy(c10.predictions(model, x, SLOTS, VALUES).reshape(-1, VALUES), y.reshape(-1)).backward()
    n = sum(p.numel() for p in model.parameters() if p.grad is not None and bool(p.grad.abs().sum() > 0))
    model.zero_grad(set_to_none=True)
    return n


@dataclass(frozen=True)
class Config:
    jobs: tuple[tuple[str, int, int], ...] = tuple((a, i, d) for a in ("protected_fixed_0474", "protected_fixed_005")
                                                   for i in c12.SEEDS for d in c12.SEEDS)
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
    save_weights_at: tuple[int, ...] = ()

    def __post_init__(self):
        if not self.jobs or len(set(self.jobs)) != len(self.jobs):
            raise ValueError("bad jobs")
        for a, i, d in self.jobs:
            if a not in ARCHS or type(i) is not int or type(d) is not int or i < 0 or d < 0:
                raise ValueError("bad job")
        if self.delay < 7 or not self.eval_delays or any(x < 7 for x in self.eval_delays):
            raise ValueError("bad delays")
        if any(type(x) is not int or x < 1 for x in (self.steps, self.batch, self.eval_histories, self.checkpoint_every,
                                                       self.checkpoint_histories, self.loss_window)):
            raise ValueError("bad budgets")
        if any(not math.isfinite(x) or x <= 0 for x in (self.lr, self.clip, self.max_wall_seconds)):
            raise ValueError("bad float budgets")
        if any(type(s) is not int or s < 0 or s > self.steps for s in self.save_weights_at):
            raise ValueError("bad weight-save steps")


def run_one(name: str, init_seed: int, data_seed: int, cfg: Config, deadline: float, weights_dir: Path | None = None) -> dict:
    """Identical procedure to capacity_012.run_one (verified by tests), plus optional weight snapshots."""
    model = build(name, init_seed)
    init_id = c12.init_fingerprint(model)
    live = live_parameter_count(model)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    saved = []

    def snapshot(step):
        if weights_dir is not None and step in cfg.save_weights_at:
            weights_dir.mkdir(parents=True, exist_ok=True)
            p = weights_dir / f"{name}_i{init_seed}_d{data_seed}_s{step}.pt"
            torch.save({k: v.detach().clone() for k, v in model.state_dict().items()}, p)
            saved.append({"step": step, "file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})

    snapshot(0)
    t0, c0 = time.monotonic(), time.process_time()
    stream = hashlib.sha256()
    steps, status, window, windows, checkpoints, per_step = 0, "complete", [], [], [], []
    for step in range(cfg.steps):
        if time.monotonic() > deadline:
            status = "time_limit"
            break
        hist = c10.generator_batch(SLOTS, VALUES, cfg.delay, cfg.batch, seed=c12.training_seed(data_seed, step))
        labels = c10.replay(hist, SLOTS, VALUES)
        stream.update(hist.numpy().tobytes())
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(c10.predictions(model, hist, SLOTS, VALUES).reshape(-1, VALUES), labels.reshape(-1))
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
            ev = c12.evaluate(model, cfg.delay, seed=c12.CHECKPOINT_EVAL_SEED, histories=cfg.checkpoint_histories, detailed=False)
            checkpoints.append({"step": steps, "delay": cfg.delay, **{k: ev[k] for k in ("per_slot", "whole", "whole_varied")}})
        snapshot(steps)
    out = {"architecture": name, "init_seed": init_seed, "data_seed": data_seed, "status": status, "steps": steps,
           "fixed_slow_write": FIXED.get(name), "parameters": sum(p.numel() for p in model.parameters()), "live_parameters": live,
           "init_fingerprint_sha256": init_id, "training_stream_sha256": stream.hexdigest(),
           "loss_per_step": per_step, "loss_windows": windows, "checkpoints": checkpoints, "saved_weights": saved,
           "train_wall_s": round(time.monotonic() - t0, 2), "train_cpu_s": round(time.process_time() - c0, 2)}
    if steps > 0:
        out["eval"] = {str(d): c12.evaluate(model, d, seed=c12.eval_seed(d), histories=cfg.eval_histories, with_baselines=True)
                       for d in cfg.eval_delays}
    out["total_wall_s"] = round(time.monotonic() - t0, 2)
    onset = c12.learning_onset(windows, cfg.loss_window)
    out["learning_onset_step"] = onset
    wv = out.get("eval", {}).get(str(cfg.delay), {}).get("whole_varied")
    out["outcome"] = c12.outcome_class(onset, wv) if steps > 0 and status == "complete" else f"incomplete:{status}"
    return out


def execute(cfg: Config, path: Path, weights_dir: Path | None = None) -> dict:
    if path.exists():
        raise FileExistsError(path)
    torch.set_num_threads(1)
    began = time.monotonic()
    deadline = began + cfg.max_wall_seconds
    # "experiment": 12 keeps the record format readable by experiment_012_report; "experiment_013" marks provenance.
    result = {"status": "running", "experiment": 12, "experiment_013": True, "config": asdict(cfg), "task": {"slots": SLOTS, "values": VALUES},
              "preregistered": {"onset_loss": c12.ONSET_LOSS, "success_whole_varied": c12.SUCCESS_WHOLE_VARIED, "eval_base_seed": c12.EVAL_BASE},
              "environment": {"torch": torch.__version__, "cpu_threads": torch.get_num_threads(), "python": platform.python_version(),
                              "cuda_available": torch.cuda.is_available(), "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES")},
              "runs": [], "skipped": []}
    try:
        for i, (name, init_seed, data_seed) in enumerate(cfg.jobs):
            if time.monotonic() > deadline:
                result["skipped"] = [{"architecture": n, "init_seed": a, "data_seed": b, "reason": "wall_budget"} for n, a, b in cfg.jobs[i:]]
                break
            row = run_one(name, init_seed, data_seed, cfg, deadline, weights_dir)
            result["runs"].append(row)
            e = row.get("eval", {}).get(str(cfg.delay), {})
            print(json.dumps({"done": len(result["runs"]), "of": len(cfg.jobs), "arch": name, "init": init_seed, "data": data_seed,
                              "status": row["status"], "outcome": row["outcome"], "onset": row["learning_onset_step"],
                              "whole_varied": e.get("whole_varied"), "wall_s": row["total_wall_s"]}), flush=True)
    finally:
        result["elapsed_seconds"] = round(time.monotonic() - began, 3)
        ok = not result["skipped"] and len(result["runs"]) == len(cfg.jobs) and all(r["status"] == "complete" for r in result["runs"])
        result["status"] = "complete" if ok else "incomplete"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description="Experiment 013: fixed slow-write-rate controls (bounded, CPU)")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--jobs", default=",".join(f"{a}:{i}:{d}" for a, i, d in Config.jobs), help="arch:init_seed:data_seed,...")
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--eval-histories", type=int, default=512)
    p.add_argument("--checkpoint-every", type=int, default=250)
    p.add_argument("--save-weights-at", default="", help="comma-separated update counts at which to save weights")
    p.add_argument("--weights-dir", type=Path)
    p.add_argument("--max-wall-seconds", type=float, default=1800)
    a = p.parse_args(argv)
    save = tuple(int(s) for s in a.save_weights_at.split(",") if s)
    if save and a.weights_dir is None:
        p.error("--weights-dir is required with --save-weights-at")
    cfg = Config(jobs=c12.parse_jobs(a.jobs), steps=a.steps, eval_histories=a.eval_histories, checkpoint_every=a.checkpoint_every,
                 save_weights_at=save, max_wall_seconds=a.max_wall_seconds)
    r = execute(cfg, a.output, a.weights_dir)
    print(f"Experiment 013: {r['status']} {len(r['runs'])} runs, {len(r['skipped'])} skipped, {r['elapsed_seconds']} seconds")


if __name__ == "__main__":
    main()
