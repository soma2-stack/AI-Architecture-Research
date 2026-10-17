"""Experiment 008: precommitted short-to-long two-slot memory curriculum.

Contrasts monotone 16/32/64/128 scheduling with a shuffled schedule carrying
exactly the same token lengths, plus fixed-64 and fixed-128 controls. All
architectures retain their original paired-query token head and recurrent cell.
CPU-only small synthetic pilot; not a theorem about robust learning credit D.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import platform
import time

import torch

from .experiment_005 import make_variant, paired_query_loss
from .experiment_002 import paired_selective_eval

VARIANTS = ("protected_w32", "gru_w32", "lstm_w32")
SCHEDULES = ("curriculum", "shuffled", "fixed64", "fixed128")
STAGES = (16, 32, 64, 128)
EVAL_DELAYS = (16, 64, 128, 256)


@dataclass(frozen=True)
class Config:
    variants: tuple[str, ...] = VARIANTS
    seeds: tuple[int, ...] = (17, 29, 43)
    schedules: tuple[str, ...] = SCHEDULES
    steps_per_stage: int = 60
    batch_size: int = 16
    eval_examples: int = 256
    learning_rate: float = .002
    grad_clip: float = 1.
    max_wall_seconds: float = 720.

    def __post_init__(self):
        if not self.variants or len(set(self.variants)) != len(self.variants) or any(x not in VARIANTS for x in self.variants):
            raise ValueError("invalid variants")
        if not self.schedules or len(set(self.schedules)) != len(self.schedules) or any(s not in SCHEDULES for s in self.schedules):
            raise ValueError("invalid schedules")
        if not self.seeds or len(set(self.seeds)) != len(self.seeds) or any(type(x) is not int or x < 0 for x in self.seeds):
            raise ValueError("invalid seeds")
        if any(type(v) is not int or v < 1 for v in (self.steps_per_stage, self.batch_size, self.eval_examples)):
            raise ValueError("invalid counts")
        if any(not math.isfinite(x) or x <= 0 for x in (self.learning_rate, self.grad_clip, self.max_wall_seconds)):
            raise ValueError("invalid hyperparameters")


def make_schedule(kind: str, steps_per_stage: int, *, seed: int) -> tuple[int, ...]:
    if kind not in SCHEDULES or type(steps_per_stage) is not int or steps_per_stage < 1 or type(seed) is not int or seed < 0:
        raise ValueError("invalid schedule inputs")
    length = len(STAGES) * steps_per_stage
    if kind == "fixed64":
        return (64,) * length
    if kind == "fixed128":
        return (128,) * length
    ordered = tuple(d for d in STAGES for _ in range(steps_per_stage))
    if kind == "curriculum":
        return ordered
    rng = torch.Generator(device="cpu").manual_seed(seed * 2909 + 8008)
    order = torch.randperm(length, generator=rng).tolist()
    return tuple(ordered[i] for i in order)


def sample_seed(seed: int, delay: int, occurrence: int) -> int:
    """Same examples at a given delay/occurrence in shuffled and curriculum.

    Depends on neither model nor schedule nor global step; avoids treating
    different sample streams as a curriculum gain.
    """
    if any(type(x) is not int or x < 0 for x in (seed, delay, occurrence)) or delay < 1:
        raise ValueError("invalid seed arguments")
    return 19_000_001 + seed * 1_000_003 + delay * 10_007 + occurrence * 8191


def train_condition(variant: str, seed: int, kind: str, config: Config, *, began: float):
    model = make_variant(variant, seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    sequence = make_schedule(kind, config.steps_per_stage, seed=seed)
    seen = Counter()
    completed = 0
    first_loss = last_loss = None
    stages = []
    t0 = time.monotonic()
    for index, delay in enumerate(sequence):
        if time.monotonic() - began >= config.max_wall_seconds:
            break
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = paired_query_loss(model, delay, config.batch_size, seed=sample_seed(seed, delay, seen[delay]))
        seen[delay] += 1
        if not bool(torch.isfinite(loss)):
            raise FloatingPointError(f"nonfinite loss: {variant}/{kind}/{seed}/{index}")
        loss.backward()
        if any(p.grad is not None and not bool(torch.isfinite(p.grad).all()) for p in model.parameters()):
            raise FloatingPointError(f"nonfinite gradient: {variant}/{kind}/{seed}/{index}")
        torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
        optimizer.step()
        completed += 1
        last_loss = float(loss.detach())
        if first_loss is None:
            first_loss = last_loss
        if completed % config.steps_per_stage == 0:
            stages.append({"completed_updates": completed, "last_training_loss": last_loss,
                           "length_counts": {str(k): int(v) for k, v in sorted(seen.items())}})
    # Partial runs are explicit, and NOT treated as full comparable conditions.
    evaluations = {}
    if completed == len(sequence):
        evaluations = {str(delay): paired_selective_eval(
            model, delay, seed=1_000_000 + seed, batch=config.eval_examples)
            for delay in EVAL_DELAYS}
    return {"variant": variant, "seed": seed, "schedule": kind,
            "steps_requested": len(sequence), "steps_completed": completed,
            "complete": completed == len(sequence), "parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
            "batch_size": config.batch_size,
            "length_counts": {str(k): int(v) for k, v in sorted(seen.items())},
            "training_examples": completed * config.batch_size,
            "approx_training_tokens": int(sum(k*v for k,v in seen.items()) * config.batch_size),
            "train_loss_first": first_loss, "train_loss_last": last_loss,
            "stages": stages, "evaluation": evaluations, "elapsed_seconds": time.monotonic()-t0}


def execute(config: Config, *, output: Path):
    if output.exists():
        raise FileExistsError("refusing to overwrite prior evidence")
    torch.manual_seed(0)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    began = time.monotonic()
    report = {"status":"running", "config":asdict(config),
              "environment":{"python":platform.python_version(), "torch":torch.__version__,
                             "device":"cpu", "cpu_threads":torch.get_num_threads()},
              "scope":"bounded paired-query training curriculum, not robust credit dimension D",
              "runs":[],"skipped":[]}
    # Rotate schedule priority across seeds to reduce time-budget selection bias.
    jobs = [(variant, seed, config.schedules[(j + i) % len(config.schedules)])
            for i, seed in enumerate(config.seeds) for j in range(len(config.schedules))
            for variant in config.variants]
    try:
        for i,(variant,seed,kind) in enumerate(jobs):
            if time.monotonic()-began >= config.max_wall_seconds:
                report["skipped"].extend({"variant":v,"seed":s,"schedule":k,"reason":"wall_budget"}
                                         for v,s,k in jobs[i:])
                break
            record=train_condition(variant,seed,kind,config,began=began)
            report["runs"].append(record)
            print(json.dumps({"finished":len(report["runs"]),"variant":variant,"seed":seed,
                  "schedule":kind,"steps":record["steps_completed"],
                  "unequal_at_128":record["evaluation"].get("128",{}).get("paired_on_unequal")}),flush=True)
            if not record["complete"]:
                report["skipped"].extend({"variant":v,"seed":s,"schedule":k,"reason":"wall_budget"}
                                         for v,s,k in jobs[i+1:])
                break
        report["status"] = "complete" if (len(report["runs"])==len(jobs) and
                              all(x["complete"] for x in report["runs"]) and not report["skipped"]) else "budget_limited"
    finally:
        report["elapsed_seconds"] = time.monotonic()-began
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open("x",encoding="utf-8") as f:
            json.dump(report,f,indent=2)
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--variants",default=",".join(VARIANTS))
    p.add_argument("--seeds",default="17,29,43")
    p.add_argument("--schedules",default=",".join(SCHEDULES))
    p.add_argument("--steps-per-stage",type=int,default=60)
    p.add_argument("--batch",type=int,default=16)
    p.add_argument("--eval-examples",type=int,default=256)
    p.add_argument("--max-wall-seconds",type=float,default=720.)
    a=p.parse_args(argv)
    c=Config(variants=tuple(a.variants.split(",")),seeds=tuple(map(int,a.seeds.split(","))),
             schedules=tuple(a.schedules.split(",")),steps_per_stage=a.steps_per_stage,
             batch_size=a.batch,eval_examples=a.eval_examples,max_wall_seconds=a.max_wall_seconds)
    r=execute(c,output=a.output)
    print(f"Experiment 008: {r['status']}; runs={len(r['runs'])}; skipped={len(r['skipped'])}; seconds={r['elapsed_seconds']:.1f}",flush=True)


if __name__=="__main__":
    main()
