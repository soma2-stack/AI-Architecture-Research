"""Stage-3 matched validation (IMPLEMENTATION_DECISIONS D-S3-1..4 and D-S3-v4; frozen before any
Stage-2 result, implemented here without change of rule).

For each promoted candidate P on its promoted task t: every condition runs on the fresh seeds
10000-10009 over the frozen learning-rate grid and selects its learning rate by the training-side
rule D-LR-1 (`runners.select_lr`).  Conditions:
    P, K(P) (residual removed), A1 (coupling cut), A2 / A3 (persistent registers zeroed / replaced
    by equal-std Gaussian noise at the B switch, every C* regime entry, every 100 steps in F),
    A4 (update_every flipped), A5a / A5b (P's update fed through SGDM / AdamW moments), A6 (best
    generic, k = ceil(FLOPs_P / FLOPs_G) updates per batch), A7 (best generic, hidden width widened
    until params >= P's params + persistent state floats), generics SGD / SGDM / AdamW, the known
    controls (B: GPM, R17, R18, R13; C*: R12, R13, R15), and the robustness perturbations (each
    evolved constant moved to its neighbouring set values, one at a time).
`decide` applies gates 1-6, the Cursor A1 / A7 checks, the known-control comparison, the
robustness add-on and the A2 / A3 requirement, and assigns the D-S3-v4 label."""
from __future__ import annotations

import math
import time
from dataclasses import replace
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .canon import canon, struct_hash
from .controls import GENERIC, make
from .fingerprint import Analysis, fingerprint
from .generate import Gen
from .grammar import (CONSTS, DECAYS, STRUCT_THETAS, TOPK_KS, Node, Program, const, program_from_dict,
                      program_to_dict, tconst, type_of)
from .runners import RUNNERS, select_lr, summarize
from .substrate import DT, Learner, Net, ProgramLearner, learner_flops_per_example
from .tasks import TaskB, TaskCstar, TaskF
from .tier1 import mean_metric, seed_metrics

STAGE3_SEEDS = list(range(10000, 10010))
KNOWN_CONTROLS = {"B": ("GPM", "R17_EWC_SI", "R18_kWTA_sparse_update", "R13_fast_slow"),
                  "Cstar": ("R12_fast_weights", "R13_fast_slow", "R15_three_factor"), "F": ()}
TASK_DIMS = {"B": (TaskB.d_in, TaskB.d_out), "Cstar": (1, 1), "F": (20, 2)}
N_BOOT = 10000
ALPHA = 0.05


# ---------------------------------------------------------------------------
# condition programs
# ---------------------------------------------------------------------------

def coupling_cut(p: Program) -> Program:
    """A1: C1 w_eff / g -> none; C2 routing gates -> 1; C3 STRUCT -> none."""
    a = Analysis(p)
    cs = a.couplings()
    q = p
    if "C1" in cs:
        q = replace(q, w_eff=None, gain=None)
    if "C2" in cs:
        rt = p.reg_types()
        gates = set(a._routing_gates(a.dW))
        from .canon import subst
        new_dW = subst(q.dW, lambda x: tconst(1.0, type_of(x, rt)) if x in gates else None)
        q = replace(q, dW=new_dW)
    if "C3" in cs:
        q = replace(q, struct=None)
    return canon(q, check=False)


def flip_timing(p: Program) -> Program:
    return replace(p, update_every=8 if p.update_every == 1 else 1)


def _neighbours(v: float, grid: Sequence[float]) -> List[float]:
    g = sorted(grid)
    if v not in g:
        return []
    i = g.index(v)
    return [g[j] for j in (i - 1, i + 1) if 0 <= j < len(g)]


def robustness_variants(p: Program) -> List[Tuple[str, Program]]:
    """Each evolved constant moved to each neighbouring value of its frozen set, one at a time:
    register decays, expression constants in the constant set, topk k, struct theta."""
    out: List[Tuple[str, Program]] = []
    for j, r in enumerate(p.regs):
        for v in _neighbours(r.decay, DECAYS):
            regs = tuple(replace(x, decay=v) if k == j else x for k, x in enumerate(p.regs))
            out.append((f"decay[{r.name}]={v}", replace(p, regs=regs)))
    if p.struct is not None:
        for v in _neighbours(p.struct.theta, STRUCT_THETAS):
            out.append((f"theta={v}", replace(p, struct=replace(p.struct, theta=v))))
    for slot, e in p.slot_exprs():
        for path, n in Gen._subtrees(e):
            if n.op == "const":
                vals = _neighbours(n.attr, CONSTS)
                mk = lambda v: const(v)
            elif n.op == "topk":
                vals = _neighbours(n.attr, TOPK_KS)
                mk = lambda v, n=n: Node("topk", n.args, v)
            else:
                continue
            for v in vals:
                out.append((f"{slot}@{path}:{n.op}={v}", Gen._set_slot(p, slot, Gen._replace_at(e, path, mk(v)))))
    return out


# ---------------------------------------------------------------------------
# learners / hooks used only by Stage 3
# ---------------------------------------------------------------------------

class ProgramThroughOptimizer(ProgramLearner):
    """A5a / A5b: P's update Delta is treated as a negative gradient g = -Delta and fed through
    SGDM (heavy ball, beta 0.9) or AdamW moments (b1 0.9, b2 0.999, eps 1e-8, wd 0.01), with the
    same constants as the generic controls."""

    def __init__(self, prog: Program, mode: str):
        super().__init__(prog, name=f"P_{mode}")
        self.mode = mode

    def init(self, net):
        super().init(net)
        z = lambda: [[np.zeros_like(w), np.zeros_like(b)] for w, b in zip(net.W, net.b)]
        self.m, self.v, self.t = z(), z(), 0

    def updates(self, net, tr, cache):
        deltas = super().updates(net, tr, cache)
        self.t += 1
        out = []
        for l, (dW, db) in enumerate(deltas):
            gs = (-dW.astype(np.float64), -db.astype(np.float64))
            ds = []
            for j in range(2):
                if self.mode == "SGDM":
                    self.m[l][j] = 0.9 * self.m[l][j] + gs[j]
                    ds.append(-self.m[l][j])
                else:
                    self.m[l][j] = 0.9 * self.m[l][j] + 0.1 * gs[j]
                    self.v[l][j] = 0.999 * self.v[l][j] + 0.001 * gs[j] ** 2
                    mh = self.m[l][j] / (1 - 0.9 ** self.t)
                    vh = self.v[l][j] / (1 - 0.999 ** self.t)
                    ds.append(-mh / (np.sqrt(vh) + 1e-8))
            if self.mode == "AdamW":
                ds[0] = ds[0] - 0.01 * net.W[l]
            out.append((ds[0].astype(DT), ds[1].astype(DT)))
        return out


def event_steps(task: str) -> set:
    if task == "B":
        return {TaskB.n1}
    if task == "Cstar":
        return {t for _, t in TaskCstar(STAGE3_SEEDS[0]).entries if t > 0}
    return set(range(100, TaskF.n_updates, 100))


class RegisterHook:
    """A2 (mode 'zero') / A3 (mode 'noise'): persistent (non-EXAMPLE) registers are reset at the
    task events, before that step's update.  Noise has, per run, layer and register, the standard
    deviation of the register's current values; its stream is fixed by the run seed."""

    def __init__(self, mode: str, task: str):
        self.mode, self.task = mode, task
        self.events = event_steps(task)
        self.n_events = 0

    def __call__(self, tr, t, task):
        if t not in self.events or not isinstance(tr.L, ProgramLearner):
            return
        L, net = tr.L, tr.net
        self.n_events += 1
        for l in range(net.nl):
            for rd in L.prog.regs:
                if rd.lifetime == "EXAMPLE":
                    continue
                cur = L.regs[l][rd.name]
                if self.mode == "zero":
                    L.regs[l][rd.name] = np.zeros_like(cur)
                else:
                    new = np.empty_like(cur)
                    for r in range(cur.shape[0]):
                        g = np.random.default_rng([net.seeds[r], 7331, t, l])
                        sd = float(np.std(cur[r].astype(np.float64)))
                        new[r] = g.normal(0.0, sd, cur[r].shape).astype(DT)
                    L.regs[l][rd.name] = new


def _factory(spec: Dict):
    kind = spec["kind"]
    if kind == "program":
        prog = program_from_dict(spec["program"])
        return lambda: ProgramLearner(prog, name=spec.get("name", "P"))
    if kind == "opt_swap":
        prog = program_from_dict(spec["program"])
        return lambda: ProgramThroughOptimizer(prog, spec["mode"])
    if kind == "named":
        return make(spec["name"])
    raise ValueError(kind)


def run_s3_job(job: Dict) -> Dict:
    """Worker entry.  job = {cid, cond, task, spec, seeds, inner?, hidden?, hook?}."""
    t0 = time.process_time()
    hook = RegisterHook(job["hook"], job["task"]) if job.get("hook") else None
    try:
        res = RUNNERS[job["task"]](_factory(job["spec"]), job["seeds"], hook=hook,
                                   inner=job.get("inner", 1), hidden=job.get("hidden", 32))
    except Exception as ex:                                          # recorded, never silent
        res = {"error": repr(ex)}
    res["cpu_s"] = time.process_time() - t0
    res["cid"], res["cond"] = job["cid"], job["cond"]
    if hook is not None:
        res["hook_events"] = hook.n_events
    return res


# ---------------------------------------------------------------------------
# resource matching
# ---------------------------------------------------------------------------

def flops(task: str, learner: Learner, hidden: int = 32) -> float:
    d_in, d_out = TASK_DIMS[task]
    net = Net(d_in, d_out, [0], hidden=hidden)
    return learner_flops_per_example(net, learner)


def compute_matched_k(task: str, p: Program, generic: str) -> int:
    return int(math.ceil(flops(task, ProgramLearner(p)) / flops(task, make(generic)())))


def capacity_matched_hidden(task: str, p: Program) -> Tuple[int, int, int]:
    d_in, d_out = TASK_DIMS[task]
    net = Net(d_in, d_out, [0])
    target = net.n_params() + ProgramLearner(p).state_floats(net)
    h = 32
    while Net(d_in, d_out, [0], hidden=h).n_params() < target:
        h += 1
    return h, target, Net(d_in, d_out, [0], hidden=h).n_params()


# ---------------------------------------------------------------------------
# statistics and decision
# ---------------------------------------------------------------------------

def summary(task: str, res: Dict) -> Dict:
    if res.get("error"):
        return {"stable": False, "error": res["error"]}
    s = summarize(task, select_lr(res, STAGE3_SEEDS))
    if s["stable"]:
        s["seed_metric"] = seed_metrics(task, s)
        s["metric"] = mean_metric(task, s)
    return s


def wilcoxon_greater(d: Sequence[float]) -> float:
    """One-sided paired Wilcoxon signed-rank p for median(d) > 0 (zeros dropped; all-zero -> 1)."""
    from scipy.stats import wilcoxon
    d = np.asarray(d, float)
    if not np.any(d != 0):
        return 1.0
    return float(wilcoxon(d, alternative="greater").pvalue)


def bootstrap_ci(d: Sequence[float], seed: int = 12345) -> Tuple[float, float]:
    d = np.asarray(d, float)
    g = np.random.default_rng(seed)
    means = d[g.integers(0, len(d), (N_BOOT, len(d)))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def holm(pvals: Dict[str, float]) -> Dict[str, bool]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, stop = len(items), {}, False
    for i, (k, p) in enumerate(items):
        if stop or p > ALPHA / (m - i):
            stop = True
            out[k] = False
        else:
            out[k] = True
    return out


def tau(task: str, m_G: float) -> float:
    return {"B": 40.0, "Cstar": 0.5 * m_G, "F": 0.10}[task]


def _m(s: Optional[Dict]) -> float:
    """Seed-mean metric; an unstable / failed condition counts as infinitely bad (lower is better)."""
    return s["metric"] if (s and s.get("stable")) else math.inf


def trivial_ok(task: str, s: Dict) -> bool:
    if task == "B":
        var = np.mean([float(np.var(TaskB(sd).Y2_eval.astype(np.float64))) for sd in STAGE3_SEEDS])
        return s["T2_final_mse"] <= 0.5 * var
    if task == "Cstar":
        return s["R0_pre_shift"] <= 0.25
    return s["train_acc"] >= 0.80


def threshold_ok(task: str, sP: Dict, sG: Dict) -> bool:
    if task == "B":
        return (sG["metric"] - sP["metric"] >= 40 and sP["retention"] >= 80
                and sP["T2_final_mse"] <= 1.25 * sG["T2_final_mse"])
    if task == "Cstar":
        return sP["metric"] <= 0.5 * sG["metric"] and sP["return_ok_count"] >= 8
    return sP["train_acc"] >= 0.98 and sP["sgg"] <= 15 and sP["metric"] <= sG["metric"] - 0.10


def pre_decide(task: str, S: Dict[str, Dict], has_persistent: bool, flops_ratio: float) -> Dict:
    """Everything except the Holm step (which needs all promoted pairs)."""
    from scipy.stats import ttest_ind
    sP = S["P"]
    gens = {g: S[g] for g in GENERIC if S[g].get("stable")}
    G = min(gens, key=lambda g: gens[g]["metric"]) if gens else None
    out: Dict = {"best_generic": G}
    out["gate1_stable"] = bool(sP.get("stable"))
    if not out["gate1_stable"] or G is None:
        out["label_hint"] = "NEGATIVE"
        return out
    sG = S[G]
    mP, mG = sP["metric"], sG["metric"]
    D = mG - mP
    T = tau(task, mG)
    out.update(m_P=mP, m_G=mG, delta=D, tau=T)
    out["gate2_learns"] = bool(trivial_ok(task, sP))
    diffs = np.array(sG["seed_metric"]) - np.array(sP["seed_metric"])
    out["per_seed_G_minus_P"] = diffs.tolist()
    out["threshold_ok"] = bool(threshold_ok(task, sP, sG))
    out["wilcoxon_p"] = wilcoxon_greater(diffs)
    out["bootstrap_ci"] = bootstrap_ci(diffs)
    out["bootstrap_excludes_0"] = out["bootstrap_ci"][0] > 0
    rob = {k: mG - _m(v) for k, v in S.items() if k.startswith("rob:")}
    out["robustness"] = {k: {"delta": d, "retains_half": bool(d >= 0.5 * D)} for k, d in rob.items()}
    out["robustness_ok"] = (sum(v["retains_half"] for v in out["robustness"].values()) >= 0.7 * len(rob)) if rob else True
    mK, mA1 = _m(S.get("K")), _m(S.get("A1"))
    out["gate4a_K_drops_half"] = bool(mG - mK <= 0.5 * D)
    out["gate4b_P_beats_K_by_half_tau"] = bool(mK - mP >= T / 2)
    out["gate4c_A1_drops_half"] = bool(mG - mA1 <= 0.5 * D)
    if S.get("A1", {}).get("stable"):
        out["cursor_A1_welch_p"] = float(ttest_ind(S["A1"]["seed_metric"], sP["seed_metric"],
                                                   equal_var=False, alternative="greater").pvalue)
    else:
        out["cursor_A1_welch_p"] = 0.0                               # A1 unstable: degradation certain
    out["cursor_A1_ok"] = out["cursor_A1_welch_p"] < 0.01
    mA = _m(S["AdamW"])
    out["gate5_A5b_keeps_half"] = bool((mA - _m(S.get("A5b"))) >= 0.5 * (mA - mP))
    mA6, mA7 = _m(S.get("A6")), _m(S.get("A7"))
    out["gate6_beats_A6_A7"] = bool(mA6 - mP >= T and mA7 - mP >= T)
    out["flops_ratio_vs_SGD"] = flops_ratio
    out["gate6_flops_ok"] = flops_ratio <= 3.0
    out["cursor_A7_ok"] = not (math.isfinite(mA7) and abs(mA7 - mP) <= 0.05 * abs(mP))
    ctrls = {c: S[c] for c in KNOWN_CONTROLS[task] if S.get(c, {}).get("stable")}
    if ctrls:
        c = min(ctrls, key=lambda k: ctrls[k]["metric"])
        pc = wilcoxon_greater(np.array(ctrls[c]["seed_metric"]) - np.array(sP["seed_metric"]))
        out["known_control"] = {"control": c, "m_control": ctrls[c]["metric"], "wilcoxon_p": pc,
                                "ok": bool(mP < ctrls[c]["metric"] and pc < 0.05)}
    else:
        out["known_control"] = {"control": None, "ok": True, "note": "N/A (no stable known control)"}
    if has_persistent:
        out["A2_A3_drop_half"] = bool(mG - _m(S.get("A2")) <= 0.5 * D or mG - _m(S.get("A3")) <= 0.5 * D)
    else:
        out["A2_A3_drop_half"] = None
    out["recorded"] = {k: _m(S.get(k)) for k in ("A2", "A3", "A4", "A5a", "A5b", "A6", "A7", "K", "A1")}
    return out


def label(d: Dict, holm_ok: bool) -> str:
    if not d.get("gate1_stable") or not d.get("gate2_learns", False):
        return "NEGATIVE"
    d["gate3"] = bool(d["threshold_ok"] and holm_ok and d["bootstrap_excludes_0"])
    if not d["gate3"]:
        return "NEGATIVE"
    if not (d["gate4a_K_drops_half"] and d["gate4b_P_beats_K_by_half_tau"]):
        return "REDISCOVERY"
    top = [d["gate4c_A1_drops_half"], d["cursor_A1_ok"], d["gate5_A5b_keeps_half"], d["gate6_beats_A6_A7"],
           d["gate6_flops_ok"], d["cursor_A7_ok"], d["known_control"]["ok"], d["robustness_ok"],
           d["A2_A3_drop_half"] is not False]
    if not all(top):
        return "INTERESTING EMPIRICAL MECHANISM — NOVELTY AUDIT REQUIRED"
    return "POSSIBLE ARCHITECTURE CANDIDATE — CROSS-LANE AUDIT REQUIRED"
