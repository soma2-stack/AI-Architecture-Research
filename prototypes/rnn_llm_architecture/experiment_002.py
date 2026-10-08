"""Experiment 002: bounded length-transfer and counterfactual dual-slot probe.

Training occurs ONLY when run on CLI. This is an exploratory supervised
benchmark, NOT a formal robust credit-dimension measurement.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn, Tensor

from .learning_pilot import (BIT0, BIT1, QUERY_A, QUERY_B, WRITE_A,
    WRITE_B, PilotConfig, evaluate, make_batch, make_model, query_loss)
from .candidates import CandidateConfig, CandidateLanguageModel
from .gated import GatedConfig, GatedLanguageModel

VARIANTS = (
    "tanh_w32", "near_critical_w32", "protected_w32", "gru_w32",
    "lstm_w32", "gru_w24", "lstm_w20", "lstm_forget_w32",
    "protected_random_w32", "protected_no_project_w32", "protected_no_retain_w32",
)


@dataclass(frozen=True)
class Config:
    variants: tuple[str, ...] = VARIANTS
    tasks: tuple[str, ...] = ("delayed", "selective")
    seeds: tuple[int, ...] = (17, 29, 43)
    train_delay: int = 64
    eval_delays: tuple[int, ...] = (64, 128, 256)
    steps: int = 150
    batch_size: int = 16
    eval_batch: int = 512
    lr: float = 0.002
    grad_clip: float = 1.0
    max_wall_seconds: float = 540.0

    def __post_init__(self):
        if not self.variants or len(set(self.variants)) != len(self.variants) or any(v not in VARIANTS for v in self.variants):
            raise ValueError("unknown or duplicated model variants")
        if not self.tasks or any(t not in ("delayed", "selective") for t in self.tasks):
            raise ValueError("invalid tasks")
        if not self.seeds or any(type(s) is not int for s in self.seeds):
            raise ValueError("invalid seeds")
        if self.train_delay < 1 or not self.eval_delays or any(d < 1 for d in self.eval_delays):
            raise ValueError("invalid delays")
        if any(type(n) is not int or n < 1 for n in (self.steps,self.batch_size,self.eval_batch)):
            raise ValueError("invalid steps or batch size")
        if any(not math.isfinite(x) or x <= 0 for x in (self.lr,self.grad_clip,self.max_wall_seconds)):
            raise ValueError("invalid resource parameters")


def build(variant: str, seed: int) -> nn.Module:
    if variant not in VARIANTS:
        raise ValueError("unknown variant")
    if variant in ("tanh_w32", "near_critical_w32", "protected_w32", "gru_w32", "lstm_w32"):
        name = variant.removesuffix("_w32")
        return make_model(name, PilotConfig(), seed)
    if variant in ("gru_w24", "lstm_w20", "lstm_forget_w32"):
        kind = variant.split("_")[0]
        width = 24 if variant == "gru_w24" else 20 if variant == "lstm_w20" else 32
        model = GatedLanguageModel(GatedConfig(vocab_size=16,width=width,layers=2,cell_type=kind,seed=seed))
        if variant == "lstm_forget_w32":
            # PyTorch LSTM gate order is input, forget, cell, output.
            # Sum of the two forget biases initializes to +1.0.
            for cell in model.cells:
                w = cell.hidden_size
                with torch.no_grad():
                    cell.bias_ih[w:2*w].fill_(1.0)
                    cell.bias_hh[w:2*w].zero_()
        return model.cpu()
    variant_opts = {
        "protected_random_w32": {"protected_basis": "random_orthogonal"},
        "protected_no_project_w32": {"project_fast": False},
        "protected_no_retain_w32": {"retain_slow": False},
    }
    return CandidateLanguageModel(CandidateConfig(
        vocab_size=16,width=32,layers=2,cell_type="protected",protected_channels=8,
        seed=seed,**variant_opts[variant])).cpu()


def _slot_targets(prefix_tokens: Tensor, delay: int) -> Tensor:
    """Independently reconstruct [A,B] from the prefix, no answer tokens.

    All samples have WRITE_A/B at positions 0 and 2, and an updated slot
    command at 4+floor(delay/2). Only tokens BEFORE final query are used.
    """
    if prefix_tokens.ndim != 2 or prefix_tokens.shape[1] != delay + 6:
        raise ValueError("selective prefix has incorrect size")
    a_first = prefix_tokens[:, 0] == WRITE_A
    if not torch.equal((prefix_tokens[:, 2] == WRITE_A), ~a_first):
        raise ValueError("initial slot order invalid")
    b0 = prefix_tokens[:, 1] - BIT0
    b1 = prefix_tokens[:, 3] - BIT0
    a = torch.where(a_first, b0, b1)
    b = torch.where(a_first, b1, b0)
    index = 4 + delay // 2
    slot = prefix_tokens[:, index] - WRITE_A
    value = prefix_tokens[:, index + 1] - BIT0
    if not bool(((slot == 0) | (slot == 1)).all()):
        raise ValueError("invalid update slot")
    if not bool(((value == 0) | (value == 1)).all()):
        raise ValueError("invalid update value")
    a = torch.where(slot == 0, value, a)
    b = torch.where(slot == 1, value, b)
    return torch.stack((a,b), dim=1)


@torch.no_grad()
def paired_selective_eval(model: nn.Module, delay: int, *, seed: int, batch: int) -> dict:
    """Query both slots from IDENTICAL prefixes, not sequential queries.

    This exposes a last-write shortcut (roughly 50% pair correctness),
    and measures both updated and untouched subpopulations.
    """
    model.eval()
    ids, targets, meta = make_batch("selective",delay,batch,seed=seed)
    expected = _slot_targets(ids[:, :-1],delay)
    assert torch.equal(expected.gather(1,meta["query_slot"][:,None])[:,0], targets)
    clone_a = ids.clone()
    clone_b = ids.clone()
    clone_a[:, -1] = QUERY_A
    clone_b[:, -1] = QUERY_B
    all_ids = torch.cat((clone_a,clone_b),dim=0)
    pair_logits = model(all_ids)[0][:,-1,BIT0:BIT1+1]
    pred = torch.stack((pair_logits[:batch].argmax(-1),pair_logits[batch:].argmax(-1)),dim=1)
    matched = pred.eq(expected)
    update_slot = meta["update_slot"]
    gathered_update = matched.gather(1,update_slot[:,None])[:,0]
    gathered_untouched = matched.gather(1,(1-update_slot)[:,None])[:,0]
    unequal = expected[:,0] != expected[:,1]
    paired = matched.all(dim=1)
    last_bit = meta["last_written_value"]
    naive_paired = expected.eq(last_bit[:,None]).all(dim=1)
    return {
        "paired_both_accuracy":float(paired.float().mean()),
        "updated_accuracy":float(gathered_update.float().mean()),
        "untouched_accuracy":float(gathered_untouched.float().mean()),
        "unequal_fraction":float(unequal.float().mean()),
        "paired_on_unequal":float(paired[unequal].float().mean()) if bool(unequal.any()) else None,
        "paired_on_equal":float(paired[~unequal].float().mean()) if bool((~unequal).any()) else None,
        "naive_last_write_paired_accuracy":float(naive_paired.float().mean()),
        "pair_loss":float(torch.nn.functional.cross_entropy(pair_logits,torch.cat((expected[:,0],expected[:,1])))),
        "examples":batch,
    }


def execute(config: Config, *, output: Path):
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    torch.set_num_threads(1)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    began = time.monotonic()
    report = {"status":"running","config":asdict(config),
              "environment":{"torch":torch.__version__,"python":platform.python_version(),"device":"cpu"},
              "runs":[],"skipped":[],"scope":"exploratory supervised benchmark, NOT formal D"}
    jobs = [(task,seed,var) for task in config.tasks for seed in config.seeds for var in config.variants]
    try:
        for i,(task,seed,var) in enumerate(jobs):
            if time.monotonic()-began >= config.max_wall_seconds:
                report["skipped"].extend([{"task":t,"seed":s,"variant":v,"reason":"wall_budget"}
                                           for t,s,v in jobs[i:]])
                break
            model = build(var,seed)
            optim = torch.optim.AdamW(model.parameters(),lr=config.lr)
            losses = []
            started = time.monotonic()
            completed = 0
            for step in range(config.steps):
                if time.monotonic()-began >= config.max_wall_seconds:
                    break
                model.train()
                batch_seed = seed*1_000_003 + step*8191 + config.train_delay*17 + (0 if task=="delayed" else 97)
                ids,target,_ = make_batch(task,config.train_delay,config.batch_size,seed=batch_seed)
                optim.zero_grad(set_to_none=True)
                loss = query_loss(model,ids,target)
                if not bool(torch.isfinite(loss)):
                    raise FloatingPointError(f"Nonfinite loss in {var}/{task}/{seed}/{step}")
                loss.backward()
                for p in model.parameters():
                    if p.grad is not None and not bool(torch.isfinite(p.grad).all()):
                        raise FloatingPointError(f"Nonfinite gradient in {var}/{task}/{seed}/{step}")
                torch.nn.utils.clip_grad_norm_(model.parameters(),config.grad_clip)
                optim.step()
                losses.append(float(loss.detach()))
                completed += 1
            metrics = {}
            for delay in config.eval_delays:
                seed_eval = seed+1_000_000
                basic = evaluate(model,task,delay,seed=seed_eval,batch=config.eval_batch)
                if task=="selective":
                    basic["counterfactual_pair"] = paired_selective_eval(
                        model,delay,seed=seed_eval,batch=config.eval_batch)
                metrics[str(delay)] = basic
            row={"task":task,"seed":seed,"variant":var,"steps_completed":completed,
                 "steps_requested":config.steps,"complete":completed==config.steps,
                 "parameters":sum(p.numel() for p in model.parameters() if p.requires_grad),
                 "initial_training_loss":losses[0] if losses else None,
                 "last_training_loss":losses[-1] if losses else None,
                 "evaluation":metrics,"elapsed_seconds":time.monotonic()-started}
            report["runs"].append(row)
            print(json.dumps({"finished":len(report["runs"]),"task":task,"seed":seed,"variant":var,
                              "steps":completed,"accuracy_at_64":metrics[str(config.train_delay)]["accuracy"]}),flush=True)
            if not row["complete"]:
                report["skipped"].extend([{"task":t,"seed":s,"variant":v,"reason":"wall_budget"}
                                           for t,s,v in jobs[i+1:]])
                break
        report["status"]="complete" if not report["skipped"] and all(r["complete"] for r in report["runs"]) else "budget_limited"
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
    p.add_argument("--tasks",default="delayed,selective")
    p.add_argument("--seeds",default="17,29,43")
    p.add_argument("--train-delay",type=int,default=64)
    p.add_argument("--eval-delays",default="64,128,256")
    p.add_argument("--steps",type=int,default=150)
    p.add_argument("--batch",type=int,default=16)
    p.add_argument("--eval-batch",type=int,default=512)
    p.add_argument("--max-wall-seconds",type=float,default=540)
    args=p.parse_args(argv)
    cfg=Config(variants=tuple(args.variants.split(",")),tasks=tuple(args.tasks.split(",")),
               seeds=tuple(map(int,args.seeds.split(","))),train_delay=args.train_delay,
               eval_delays=tuple(map(int,args.eval_delays.split(","))),steps=args.steps,
               batch_size=args.batch,eval_batch=args.eval_batch,max_wall_seconds=args.max_wall_seconds)
    report=execute(cfg,output=args.output)
    print(f"Experiment 002 status: {report['status']}; runs={len(report['runs'])}; skipped={len(report['skipped'])}; seconds={report['elapsed_seconds']:.1f}")


if __name__=="__main__":
    main()
