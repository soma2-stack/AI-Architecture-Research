"""Level-C structural fingerprint: AE.2.3 features F1-F26, couplings C1-C3, the
learning-signal rule (AE.1.6), MAP-Elites descriptors (AE.3.2) and the Codex
AR-141 minimum schema fields required by prereg v2 sec. 4 Level C.

All analyses run on the canonical program; `cvec` (when still a slot) is expanded
into the expressions that read it.
"""
from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from .canon import replace_leaf
from .grammar import (ACTIVITY_LEAVES, LEAF_TYPES, LEARNING_SIGNAL_LEAVES, M, O, S, Node, Program,
                      reads, type_of)

DATA_LEAVES = frozenset(set(LEAF_TYPES) - {"tep", "cvec"})
NON_ROUTING_OPS = frozenset({"mean", "norm", "dot", "amax", "rowsum", "colsum", "matvec",
                             "matTvec", "nrm", "unit"})
COUPLING_SUBSETS = [frozenset(s) for s in (("C1",), ("C2",), ("C3",), ("C1", "C2"), ("C1", "C3"),
                                            ("C2", "C3"), ("C1", "C2", "C3"))]
CREDIT_CLASSES = ("bp", "fa", "reward", "mixed")


def expand(p: Program, e: Optional[Node]) -> Optional[Node]:
    if e is None or p.cvec is None:
        return e
    return replace_leaf(e, "cvec", p.cvec)


class Analysis:
    def __init__(self, p: Program):
        self.p = p
        self.rt = p.reg_types()
        self.upd = {r.name: expand(p, u) for r, u in zip(p.regs, p.reg_updates)}
        self.decl = {r.name: r for r in p.regs}
        self.dW = expand(p, p.dW)
        self.db = expand(p, p.db)
        self.w_eff = p.w_eff
        self.gain = p.gain
        self.mask = None if p.struct is None else expand(p, p.struct.mask)
        self._closure: Dict[str, Set[str]] = {}

    # transitive leaf dependencies through registers
    def closure(self, e: Optional[Node]) -> Set[str]:
        if e is None:
            return set()
        out: Set[str] = set()
        seen: Set[str] = set()
        stack = [e]
        while stack:
            x = stack.pop()
            for name in reads(x):
                if name in self.upd:
                    if name not in seen:
                        seen.add(name)
                        stack.append(self.upd[name])
                else:
                    out.add(name)
        return out

    def reg_data_dependent(self, name: str) -> bool:
        return bool(self.closure(self.upd[name]) & DATA_LEAVES)

    def regs_read(self, e: Optional[Node]) -> Set[str]:
        return set() if e is None else {x.attr for x in e.walk() if x.op == "reg"}

    # ------------------------------------------------------------------ couplings
    def c1(self) -> bool:
        fr = self.regs_read(self.w_eff) | self.regs_read(self.gain)
        return any(self.reg_data_dependent(r) for r in fr)

    def _routing_gates(self, e: Optional[Node]) -> List[Node]:
        """topk/where nodes reachable from the root without passing a reduction, whose
        selector reads activity (a, z, h, dphi)."""
        out: List[Node] = []
        if e is None:
            return out

        def go(x: Node):
            if x.op in NON_ROUTING_OPS:
                return
            if x.op in ("topk", "where") and (reads(x.args[0]) & ACTIVITY_LEAVES):
                out.append(x)
            for c in x.args:
                go(c)

        go(e)
        return out

    def c2(self) -> bool:
        return bool(self._routing_gates(self.dW))

    def c3(self) -> bool:
        return self.mask is not None and bool(self.closure(self.mask) & DATA_LEAVES)

    def couplings(self) -> FrozenSet[str]:
        s = set()
        if self.c1():
            s.add("C1")
        if self.c2():
            s.add("C2")
        if self.c3():
            s.add("C3")
        return frozenset(s)

    def learning_signal(self) -> bool:
        return bool(self.closure(self.dW) & LEARNING_SIGNAL_LEAVES)

    # ------------------------------------------------------------------ descriptors
    def credit_class(self) -> str:
        c = self.closure(self.dW)
        bp, fa, err = "d_bp" in c, "d_fa" in c, "e" in c
        rew = bool(c & {"L", "dL"})
        if bp and not (fa or err or rew):
            return "bp"
        if fa and not (bp or rew):
            return "fa"
        if rew and not (bp or fa or err):
            return "reward"
        return "mixed"

    def state_footprint(self) -> str:
        return "synapse" if any(r.type == M and r.lifetime != "EXAMPLE" for r in self.p.regs) \
            else "feature"

    def descriptor(self) -> Optional[Tuple[int, int, int]]:
        cs = self.couplings()
        if not cs:
            return None
        return (COUPLING_SUBSETS.index(cs), CREDIT_CLASSES.index(self.credit_class()),
                0 if self.state_footprint() == "feature" else 1)

    # ------------------------------------------------------------------ helpers for F1..F26
    @staticmethod
    def _nodes(e: Optional[Node]) -> List[Node]:
        return [] if e is None else list(e.walk())

    def _all_exprs(self) -> List[Node]:
        es = [e for e in (self.w_eff, self.gain, self.dW, self.db, self.mask) if e is not None]
        es += list(self.upd.values())
        return es

    def _is_activity_product(self, x: Node) -> bool:
        if x.op != "outer":
            return False
        left = self.closure(x.args[0])
        right = self.closure(x.args[1])
        return bool(left & {"h", "z", "dphi"}) and not (left & LEARNING_SIGNAL_LEAVES) \
            and not (left & {"d_bp", "d_fa"}) and "a" in right

    def _is_grad_like(self, x: Node) -> bool:
        if x.op != "outer":
            return False
        return bool(self.closure(x.args[0]) & {"d_bp", "d_fa", "e"}) and "a" in self.closure(x.args[1])

    def _contains(self, e: Optional[Node], pred) -> bool:
        return any(pred(x) for x in self._nodes(e))

    def _additive_terms(self, e: Node) -> List[Node]:
        if e.op in ("add", "sub"):
            return self._additive_terms(e.args[0]) + self._additive_terms(e.args[1])
        if e.op == "neg" or (e.op == "mul" and e.args[1].op == "const"):
            return self._additive_terms(e.args[0])
        return [e]

    def _reg_role(self, name: str) -> Dict[str, bool]:
        v = self.upd[name]
        tms = self._additive_terms(v)
        return {
            "activity": self._contains(v, self._is_activity_product)
            or bool(reads(v) & {"h"} and self.decl[name].type != M and not (self.closure(v) & LEARNING_SIGNAL_LEAVES)),
            "grad": any(self._is_grad_like(t) for t in tms) or (
                self.decl[name].type == O and any(t.op == "leaf" and t.attr == "d_bp" for t in tms)),
            "sq_grad": self._contains(v, lambda x: x.op in ("square", "abs") and self._contains(x.args[0], self._is_grad_like)),
        }

    def features(self) -> Dict[str, int]:
        f: Dict[str, int] = {}
        allr: Set[str] = set()
        for e in self._all_exprs():
            allr |= reads(e)
        dWc = self.closure(self.dW)
        dW_regs = self.regs_read(self.dW)
        roles = {r: self._reg_role(r) for r in self.upd}
        f["F1_global_bp"] = int("d_bp" in allr)
        scalar_of_h = self._contains(self.dW, lambda x: x.op in ("norm", "mean", "dot", "amax") and "h" in reads(x))
        no_err = not (dWc & {"d_bp", "d_fa", "e"})
        f["F2_local_objective"] = int(scalar_of_h and no_err)
        f["F3_transpose"] = int(any(x.op == "matTvec" for e in self._all_exprs() for x in e.walk()))
        f["F4_fixed_feedback"] = int("d_fa" in allr)
        elig = False
        for r in dW_regs:
            if roles[r]["activity"]:
                for x in self._nodes(self.dW):
                    if x.op in ("mul", "rowscale", "colscale", "where") and r in self.regs_read(x) and \
                            (self.closure(x) & (LEARNING_SIGNAL_LEAVES | {"Lbar"})):
                        elig = True
        f["F5_eligibility_trace"] = int(elig)
        f["F6_momentum"] = int(any(roles[r]["grad"] for r in dW_regs))
        sm = False
        for x in self._nodes(self.dW):
            if x.op == "div_s" and any(roles[r]["sq_grad"] for r in self.regs_read(x.args[1])):
                sm = True
            if x.op == "recip_s" and any(roles[r]["sq_grad"] for r in self.regs_read(x.args[0])):
                sm = True
        f["F7_second_moment"] = int(sm)
        fw_regs = self.regs_read(self.w_eff)
        f["F8_fast_weights"] = int(any(self.decl[r].type == M and roles[r]["activity"] for r in fw_regs))
        mregs = [r for r in fw_regs if self.decl[r].type == M]
        fastslow = any(self.decl[r].decay < 0.99 or self.decl[r].lifetime == "EPISODE" for r in mregs)
        if len(mregs) >= 2:
            ks = {(self.decl[r].decay, self.decl[r].lifetime) for r in mregs}
            fastslow = fastslow or len(ks) >= 2
        f["F9_fast_slow"] = int(fastslow)
        f["F10_fixed_point"] = 0
        hebb_thresh = self._contains(self.dW, self._is_activity_product) and no_err
        f["F11_local_energy"] = int(f["F2_local_objective"] or (hebb_thresh and scalar_of_h))
        f["F12_explicit_memory"] = 0
        f["F13_routing"] = int(bool(self._routing_gates(self.dW)) or bool(self._routing_gates(self.gain)))
        mp = False
        for x in self._nodes(self.dW):
            if x.op == "mul" and any((c.op == "leaf" and c.attr == "W") or
                                     (c.op == "reg" and self.decl[c.attr].type == M) for c in x.args):
                mp = True
        f["F14_multiplicative_plasticity"] = int(mp)
        f["F15_normalization"] = int(self._contains(self.dW, lambda x: x.op in ("nrm", "unit")) or
                                     any(self._contains(self.upd[r], lambda x: x.op in ("nrm", "unit"))
                                         for r in dW_regs))
        f["F16_orthogonal_projection"] = 0
        imp_gate = False
        for x in self._nodes(self.dW):
            if x.op in ("mul", "rowscale", "colscale", "where"):
                for r in self.regs_read(x):
                    if self.decl[r].decay >= 0.99 and roles[r]["sq_grad"]:
                        imp_gate = True
        f["F17_freezing"] = int((self.p.struct is not None and self.p.struct.kind == "freeze") or imp_gate)
        f["F18_structural_growth"] = int(self.p.struct is not None and self.p.struct.kind == "reinit")
        hebb = False
        for e in [self.dW] + list(self.upd.values()):
            for x in self._nodes(e):
                if self._is_activity_product(x):
                    hebb = True
        f["F19_hebbian"] = int(hebb)
        oja = hebb and self._contains(self.dW, lambda x: x.op == "rowscale" and x.args[0].op == "leaf"
                                      and x.args[0].attr == "W" and "h" in reads(x.args[1]))
        f["F20_oja_decay"] = int(oja)
        rm = False
        for x in self._nodes(self.dW):
            if x.op in ("mul", "rowscale", "colscale"):
                for c in x.args:
                    if type_of(c, self.rt) == S and (self.closure(c) & {"L", "dL"}):
                        rm = True
        f["F21_reward_modulated"] = int(rm)
        f["F22_perturbation"] = int(bool(allr & {"xi_I", "xi_O"}) and bool(dWc & {"L", "dL"}))
        f["F23_anchor_consolidation"] = int("W_ep0" in self.closure(self.dW) or imp_gate)
        f["F24_gain_modulation"] = int(self.gain is not None and bool(self.regs_read(self.gain)))
        ls = False
        if self.dW.op in ("neg", "mul", "outer"):
            core = self.dW.args[0] if self.dW.op == "neg" else self.dW
            if core.op == "mul" and core.args[0].op == "outer":
                ls = bool(self.closure(core.args[1]) & {"L", "dL"}) and "d_bp" in reads(core.args[0].args[0])
            if core.op == "outer" and core.args[0].op == "mul":
                u, v = core.args[0].args
                ls = ("d_bp" in reads(u) and bool(self.closure(v) & {"L", "dL"}) and type_of(v, self.rt) == S)
        f["F25_loss_shaping"] = int(ls)
        cp = False
        for r, rd in self.decl.items():
            if rd.type == O and "d_bp" in self.closure(self.upd[r]):
                for x in self._nodes(self.dW):
                    if x.op == "outer" and r in self.regs_read(x.args[0]):
                        cp = True
                if self.p.cvec is not None and r in self.regs_read(self.p.cvec):
                    cp = True
        f["F26_credit_predictor"] = int(cp)
        return f

    def codex_schema(self) -> Dict[str, object]:
        """AR-141 minimum fields (prereg v2 sec. 4 Level C).  None = not determinable."""
        f = self.features()
        dWc = self.closure(self.dW)
        return {
            "global_gradient": bool(f["F1_global_bp"]),
            "local_gradient": bool(f["F2_local_objective"] or f["F11_local_energy"] or f["F19_hebbian"]),
            "fixed_feedback": bool(f["F4_fixed_feedback"]),
            "transpose_required": bool(f["F3_transpose"]) or bool(f["F1_global_bp"]),
            "momentum_state": bool(f["F6_momentum"]),
            "second_moment_state": bool(f["F7_second_moment"]),
            "eligibility_state": bool(f["F5_eligibility_trace"]),
            "fast_weights": bool(f["F8_fast_weights"]),
            "fast_slow_state": bool(f["F9_fast_slow"]),
            "activation_dependent_update": bool(dWc & {"h", "z", "dphi"}),
            "input_dependent_routing": bool(self._routing_gates(self.dW)) and any(
                "a" in reads(g.args[0]) for g in self._routing_gates(self.dW) + self._routing_gates(self.gain)),
            "normalization": bool(f["F15_normalization"]),
            "projection": False,
            "fixed_point_or_root_solve": False,
            "parameter_birth_reinit_freeze": bool(f["F17_freezing"] or f["F18_structural_growth"]),
            "test_time_update": True,          # online stream: every step both predicts and updates
            "meta_learned_update": False,      # no outer loop by construction
            "persistent_state_lifetimes": sorted({r.lifetime for r in self.p.regs if r.lifetime != "EXAMPLE"}),
            "forward_depends_on_learning_state": bool(self.c1()),
        }


def fingerprint(p: Program) -> Dict[str, object]:
    a = Analysis(p)
    cs = a.couplings()
    return {
        "features": a.features(),
        "couplings": sorted(cs),
        "learning_signal": a.learning_signal(),
        "credit_class": a.credit_class(),
        "state_footprint": a.state_footprint(),
        "descriptor": a.descriptor(),
        "codex": a.codex_schema(),
    }
