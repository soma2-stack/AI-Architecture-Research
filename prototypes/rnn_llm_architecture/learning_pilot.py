"""EXPERIMENT 001: bounded, reproducible CPU-only supervised memory pilot.

Runs only on explicit CLI invocation; importing this module never trains.
No RL, no formal learning-credit measurement, no external datasets/GPU.
The theory reference is deliberately excluded: it is not a token LLM.
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
from torch import Tensor
import torch.nn.functional as F

MODELS = ("tanh", "near_critical", "protected", "gru", "lstm")
TASKS = ("delayed", "selective")
BIT0, BIT1, QUERY, WRITE_A, WRITE_B, QUERY_A, QUERY_B = 2, 3, 4, 5, 6, 14, 15
DISTRACTOR_START, DISTRACTOR_END = 8, 14  # exclusive; unrelated to labels
VOCAB_SIZE = 16


@dataclass(frozen=True)
class PilotConfig:
    models: tuple[str, ...] = MODELS
    tasks: tuple[str, ...] = TASKS
    delays: tuple[int, ...] = (16, 64)
    seeds: tuple[int, ...] = (17, 29)
    width: int = 32
    layers: int = 2
    protected_channels: int = 8
    batch_size: int = 16
    eval_batch: int = 256
    steps: int = 100
    learning_rate: float = 0.002
    grad_clip: float = 1.0
    max_wall_seconds: float = 1200.0

    def __post_init__(self):
        if not self.models or any(x not in MODELS for x in self.models):
            raise ValueError("models must be chosen from known trainable architectures")
        if not self.tasks or any(x not in TASKS for x in self.tasks):
            raise ValueError("unknown task")
        if not self.delays or any(not isinstance(d, int) or d < 1 for d in self.delays):
            raise ValueError("delays must be positive integers")
        if not self.seeds or any(not isinstance(s, int) for s in self.seeds):
            raise ValueError("seeds must be integers")
        if (self.width < 2 or self.width & (self.width - 1)
                or not 1 <= self.protected_channels <= self.width // 2):
            raise ValueError("width must be power of two; protected channels in 1..width/2")
        if any(not isinstance(v, int) or v < 1 for v in
               (self.layers, self.batch_size, self.eval_batch, self.steps)):
            raise ValueError("layers, batch sizes, steps must be positive")
        if not (math.isfinite(self.learning_rate) and self.learning_rate > 0
                and math.isfinite(self.grad_clip) and self.grad_clip > 0
                and math.isfinite(self.max_wall_seconds) and self.max_wall_seconds > 0):
            raise ValueError("learning rate, clipping and wall budget must be positive finite")


def _generator(seed: int) -> torch.Generator:
    return torch.Generator(device="cpu").manual_seed(seed)


def make_batch(task: str, delay: int, batch: int, *, seed: int) -> tuple[Tensor, Tensor, dict[str, Tensor]]:
    """Independent seeded examples. Labels only appear at the initial write(s).

    Outputs [B,T] integer tokens, binary query labels, and diagnostic strata.
    Query tokens contain slot identity, never answer value. Distractors carry
    no binary target, and train/held-out seeds are disjoint by construction.
    """
    if task not in TASKS or delay < 1 or batch < 1:
        raise ValueError("invalid task, delay or batch size")
    rng = _generator(seed)
    filler = torch.randint(DISTRACTOR_START, DISTRACTOR_END,
                           (batch, delay), generator=rng, dtype=torch.long)
    bits = torch.randint(0, 2, (batch, 2), generator=rng, dtype=torch.long)
    if task == "delayed":
        # Force exact label balance for even batches to avoid seed/label skew.
        labels = (torch.randperm(batch, generator=rng) % 2).long()
        ids = torch.cat((labels[:, None] + BIT0, filler,
                         torch.full((batch, 1), QUERY, dtype=torch.long)), dim=1)
        return ids, labels, {"query_updated": torch.zeros(batch, dtype=torch.bool)}
    # Initial slot order randomized: model must use A/B write identities.
    a, b = bits[:, 0], bits[:, 1]
    order = torch.randint(0, 2, (batch,), generator=rng).bool()
    write_1 = torch.where(order, WRITE_B, WRITE_A)
    write_2 = torch.where(order, WRITE_A, WRITE_B)
    bit_1 = torch.where(order, b, a) + BIT0
    bit_2 = torch.where(order, a, b) + BIT0
    update_slot = torch.randint(0, 2, (batch,), generator=rng)
    update_value = torch.randint(0, 2, (batch,), generator=rng)
    query_slot = torch.randint(0, 2, (batch,), generator=rng)
    # Controlled update changes one slot; the other must survive distractors.
    a_final = torch.where(update_slot == 0, update_value, a)
    b_final = torch.where(update_slot == 1, update_value, b)
    labels = torch.where(query_slot == 0, a_final, b_final)
    p = delay // 2
    ids = torch.cat((write_1[:, None], bit_1[:, None],
                     write_2[:, None], bit_2[:, None], filler[:, :p],
                     (WRITE_A + update_slot)[:, None], (BIT0 + update_value)[:, None],
                     filler[:, p:], (QUERY_A + query_slot)[:, None]), dim=1)
    return ids.long(), labels.long(), {
        "query_updated": query_slot == update_slot,
        "update_slot": update_slot, "query_slot": query_slot,
        "last_written_value": update_value,
    }


def make_model(name: str, config: PilotConfig, seed: int):
    """Use repository implementations, NOT stand-in reimplementations."""
    if name in ("gru", "lstm"):
        from .gated import GatedConfig, GatedLanguageModel
        model = GatedLanguageModel(GatedConfig(
            vocab_size=VOCAB_SIZE, width=config.width, layers=config.layers,
            cell_type=name, seed=seed))
    else:
        from .candidates import CandidateConfig, CandidateLanguageModel
        model = CandidateLanguageModel(CandidateConfig(
            vocab_size=VOCAB_SIZE, width=config.width, layers=config.layers,
            protected_channels=config.protected_channels, cell_type=name, seed=seed))
    return model.cpu()


def query_loss(model, ids: Tensor, target: Tensor) -> Tensor:
    logits = model(ids)[0][:, -1, BIT0:BIT1 + 1]
    return F.cross_entropy(logits, target)


@torch.no_grad()
def evaluate(model, task: str, delay: int, *, seed: int, batch: int) -> dict:
    model.eval()
    ids, targets, strata = make_batch(task, delay, batch, seed=seed)
    logits = model(ids)[0][:, -1, BIT0:BIT1 + 1]
    labels = logits.argmax(dim=-1)
    correct = labels.eq(targets)
    result = {"accuracy": float(correct.float().mean()),
              "loss": float(F.cross_entropy(logits, targets)),
              "examples": batch,
              "positive_fraction": float(targets.float().mean())}
    if task == "selective":
        updated = strata["query_updated"]
        result["updated_query_accuracy"] = (float(correct[updated].float().mean())
                                            if updated.any() else None)
        result["untouched_query_accuracy"] = (float(correct[~updated].float().mean())
                                              if (~updated).any() else None)
        # Reveals why a naive "last observed value" shortcut is dangerous.
        naive = strata["last_written_value"].eq(targets)
        result["last_value_shortcut_accuracy"] = float(naive.float().mean())
    return result


def _source_sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_pilot(config: PilotConfig, *, output: Path, smoke: bool = False) -> dict:
    """Bounded CPU run; never modify existing evidence or replace output."""
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing experiment output: {output}")
    torch.set_num_threads(1)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    began = time.monotonic()
    report = {"status": "running", "config": asdict(config), "smoke": smoke,
              "environment": {"torch": torch.__version__, "python": platform.python_version(),
                              "device": "cpu", "threads": torch.get_num_threads()},
              "runs": [], "skipped": [], "scope": "supervised CPU pilot only; NOT formal D"}
    # Interleave models by common dataset condition, not favorite architecture.
    jobs = [(task, delay, seed, name) for task in config.tasks
            for delay in config.delays for seed in config.seeds for name in config.models]
    steps = min(config.steps, 25) if smoke else config.steps
    try:
        for ix, (task, delay, seed, name) in enumerate(jobs):
            if time.monotonic() - began >= config.max_wall_seconds:
                report["skipped"].extend([dict(task=t, delay=d, seed=s, model=m,
                                               reason="wall_budget") for t,d,s,m in jobs[ix:]])
                break
            model = make_model(name, config, seed)
            optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
            initial = evaluate(model, task, delay, seed=seed + 1_000_000, batch=config.eval_batch)
            losses = []
            completed = 0
            run_start = time.monotonic()
            for step in range(steps):
                if time.monotonic() - began >= config.max_wall_seconds:
                    break
                model.train()
                # The same (task, delay, seed, step) yields identical examples
                # for all models; independent of global model RNG.
                batch_seed = seed * 1_000_003 + step * 8191 + delay * 17 + (0 if task == "delayed" else 97)
                ids, y, _ = make_batch(task, delay, config.batch_size, seed=batch_seed)
                optimizer.zero_grad(set_to_none=True)
                loss = query_loss(model, ids, y)
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"nonfinite loss in {name} {task} {delay} {seed} step {step}")
                loss.backward()
                for p in model.parameters():
                    if p.grad is not None and not torch.isfinite(p.grad).all():
                        raise FloatingPointError(f"nonfinite gradients in {name} step {step}")
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
                optimizer.step()
                losses.append(float(loss.detach()))
                completed += 1
            final = evaluate(model, task, delay, seed=seed + 1_000_000, batch=config.eval_batch)
            run = {"model": name, "task": task, "delay": delay, "seed": seed,
                   "steps_completed": completed, "steps_requested": steps,
                   "complete": completed == steps,
                   "train_loss_first": losses[0] if losses else None,
                   "train_loss_last": losses[-1] if losses else None,
                   "initial": initial, "final": final,
                   "parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
                   "elapsed_seconds": time.monotonic() - run_start}
            report["runs"].append(run)
            print(json.dumps({"finished": len(report["runs"]), "model": name,
                              "task": task, "delay": delay, "seed": seed,
                              "steps": completed, "accuracy": final["accuracy"]}), flush=True)
            if not run["complete"]:
                report["skipped"].extend([dict(task=t, delay=d, seed=s, model=m,
                                               reason="wall_budget") for t,d,s,m in jobs[ix+1:]])
                break
        report["status"] = "complete" if not report["skipped"] and all(x["complete"] for x in report["runs"]) else "budget_limited"
    finally:
        report["elapsed_seconds"] = time.monotonic() - began
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    return report


def _split_list(raw: str, convert=str):
    return tuple(convert(x.strip()) for x in raw.split(",") if x.strip())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", default=",".join(MODELS))
    parser.add_argument("--tasks", default=",".join(TASKS))
    parser.add_argument("--delays", default="16,64")
    parser.add_argument("--seeds", default="17,29")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--eval-batch", type=int, default=256)
    parser.add_argument("--width", type=int, default=32)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--max-wall-seconds", type=float, default=1200)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    config = PilotConfig(models=_split_list(args.models), tasks=_split_list(args.tasks),
                         delays=_split_list(args.delays, int), seeds=_split_list(args.seeds, int),
                         width=args.width, layers=args.layers, steps=args.steps,
                         batch_size=args.batch, eval_batch=args.eval_batch,
                         max_wall_seconds=args.max_wall_seconds)
    result = run_pilot(config, output=args.output, smoke=args.smoke)
    print(f"Experiment status: {result['status']}; runs: {len(result['runs'])}; "
          f"skipped: {len(result['skipped'])}; elapsed: {result['elapsed_seconds']:.2f}s")


if __name__ == "__main__":
    main()
