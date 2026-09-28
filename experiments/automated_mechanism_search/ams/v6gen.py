"""Prereg v6 initial-proposal constructor: SGD-anchored architecture residuals.

Every proposal starts from the exact R1 SGD backbone
    dW_base = (neg (outer d_bp a)),  db_base = (neg d_bp),  update_every = 1
and adds exactly one primary coupling class, drawn uniformly from C1 / C2 / C3 (prereg v6).
Mutation and crossover are inherited unchanged from the v5 `Gen`; the v5 random constructor
`Gen.program` is untouched.  Nothing here reads a task, T0, probe or benchmark outcome.

Implementation decisions (IMPLEMENTATION_DECISIONS.md D-V6-*):
  * `add(1.0, X)` is written `(add X 1.0)`: the frozen grammar admits binary operands (T,T) or
    (T,S) only, and `add` is commutative, so the function is identical (D-V6-2).
  * "depth 1-2" = the grow-method depth argument drawn uniformly from {1, 2}; the realized depth
    is then 1 or 2 (D-V6-3).
  * "must include an activity leaf" is a conditional draw: the expression is redrawn until it
    reads a required leaf.  Such redraws are not proposals.  Proposals that fail the grammar or
    node / depth limits are retried, at most 10 attempts per proposal slot with the coupling
    class held fixed, and every attempt counts as generated (D-V6-4).
"""
from __future__ import annotations

from typing import Dict, Iterator, Optional, Tuple

from .generate import MAX_RETRY, Gen, valid
from .grammar import (ACTIVITY_LEAVES, LEARNING_SIGNAL_LEAVES, MAX_DEPTH, MAX_M_REGS, MAX_NODES,
                      MAX_REGS, M, O, STRUCT_KINDS, STRUCT_THETAS, GrammarError, Node, Program,
                      RegDecl, Struct, const, infer, parse, reads, sexpr, typecheck)

V6_CLASSES = ("C1", "C2", "C3")
V6_DECAYS = (0.5, 0.9, 0.99)
V6_C1_REG_TYPES = (O, M)
V6_EXPR_DEPTHS = (1, 2)
V6_ACT_C1 = frozenset({"a", "z", "h", "dphi"})
V6_ACT_C23 = frozenset({"z", "h", "dphi"})
V6_THETAS = (0.0, 0.1, 0.5)
V6_KINDS = ("freeze", "reinit")
V6_MAX_REDRAW = 10000      # guard on the conditional draw only (measured acceptance >= 0.28 per draw)

SGD_W = parse("(neg (outer d_bp a))")
SGD_B = parse("(neg d_bp)")
REG = Node("reg", (), "r1")

assert set(V6_DECAYS) <= {0.0, 0.5, 0.9, 0.99, 0.999}
assert set(V6_THETAS) == set(STRUCT_THETAS) and set(V6_KINDS) == set(STRUCT_KINDS)
assert V6_ACT_C1 <= ACTIVITY_LEAVES and V6_ACT_C23 <= ACTIVITY_LEAVES


def squash_gain(e: Node) -> Node:
    """v6 `add(1.0, mul(tanh(e), 0.1))`, written in the grammar's (T,S) operand order."""
    return Node("add", (Node("mul", (Node("tanh", (e,)), const(0.1))), const(1.0)))


def fast_weight(e: Node) -> Node:
    """v6 `mul(tanh(e), 0.1)`."""
    return Node("mul", (Node("tanh", (e,)), const(0.1)))


class AnchoredGen(Gen):
    """v5 `Gen` plus the v6 anchored constructor (same RNG object, same mutation operators)."""

    def __init__(self, rng):
        super().__init__(rng)
        self.redraws = 0

    def v6_class(self) -> str:
        return self.r.choice(V6_CLASSES)

    def _activity_expr(self, t: str, phase: str, rt: Dict[str, str], need: frozenset) -> Tuple[Node, int]:
        for k in range(V6_MAX_REDRAW):
            e = self.expr(t, phase, rt, self.r.choice(V6_EXPR_DEPTHS), has_cvec=False)
            if reads(e) & need:
                return e, k
        raise RuntimeError("v6 conditional draw exhausted")        # pragma: no cover

    def v6_attempt(self, cls: str) -> Tuple[Program, Dict]:
        """One construction attempt of class `cls`.  Draw order is fixed (reproducibility)."""
        meta: Dict = {"v6_class": cls}
        if cls == "C1":
            t = self.r.choice(V6_C1_REG_TYPES)
            decay = self.r.choice(V6_DECAYS)
            rd = RegDecl("r1", t, "RUN", "0", decay)
            up, k = self._activity_expr(t, "STATE", {"r1": t}, V6_ACT_C1)
            w_eff, gain = (fast_weight(REG), None) if t == M else (None, squash_gain(REG))
            p = Program(1, (rd,), (up,), None, SGD_W, SGD_B, w_eff, gain, None)
            meta.update(reg_type=t, decay=decay, redraws=k, expr_depth=_depth(up, {"r1": t}, "STATE"))
        elif cls == "C2":
            sel, k = self._activity_expr(O, "PARAM", {}, V6_ACT_C23)
            g = squash_gain(sel)
            p = Program(1, (), (), None, Node("rowscale", (SGD_W, g)), Node("mul", (SGD_B, g)))
            meta.update(redraws=k, expr_depth=_depth(sel, {}, "PARAM"))
        elif cls == "C3":
            decay = self.r.choice(V6_DECAYS)
            rd = RegDecl("r1", O, "RUN", "0", decay)
            up, k = self._activity_expr(O, "STATE", {"r1": O}, V6_ACT_C23)
            kind = self.r.choice(V6_KINDS)
            theta = self.r.choice(V6_THETAS)
            p = Program(1, (rd,), (up,), None, SGD_W, SGD_B, None, None,
                        Struct(kind, Node("tanh", (REG,)), theta))
            meta.update(decay=decay, kind=kind, theta=theta, redraws=k, expr_depth=_depth(up, {"r1": O}, "STATE"))
        else:
            raise ValueError(cls)
        self.redraws += meta["redraws"]
        return p, meta

    def v6_attempts(self, cap_check=None) -> Iterator[Tuple[Program, Dict, Optional[str]]]:
        """One proposal slot: pick the class once, then up to MAX_RETRY attempts.  Yields
        (program, meta, invalid_code_or_None) lazily and stops after the first valid attempt.
        cap_check (prereg v8): called before each attempt is constructed; if it returns True the
        slot stops without constructing another candidate (the caller raises BudgetExhausted)."""
        cls = self.v6_class()
        for a in range(1, MAX_RETRY + 1):
            if cap_check is not None and cap_check():
                return
            p, meta = self.v6_attempt(cls)
            meta["attempt"] = a
            code = valid(p)
            yield p, meta, code
            if code is None:
                return


# ---------------------------------------------------------------------------
# structural invariants (used by the tests and the static validation; no evaluation)
# ---------------------------------------------------------------------------

def _depth(e: Node, rt, phase: str) -> int:
    return infer(e, rt, phase, False)[1]


def v6_invariants(p: Program, meta: Dict) -> Dict[str, bool]:
    """Constructor-level checks of the v6 specification for one valid proposal."""
    cls = meta["v6_class"]
    out: Dict[str, bool] = {}
    try:
        info = typecheck(p)
        out["type_valid"] = True
        out["within_node_depth_limits"] = info["nodes"] <= MAX_NODES and max(info["depths"].values()) <= MAX_DEPTH
    except GrammarError:
        out["type_valid"] = out["within_node_depth_limits"] = False
        return out
    out["register_limits"] = len(p.regs) <= MAX_REGS and sum(r.type == M for r in p.regs) <= MAX_M_REGS
    out["update_every_1"] = p.update_every == 1
    out["no_cvec"] = p.cvec is None
    closure_dW = reads(p.dW)
    out["backprop_signal_in_dW"] = "d_bp" in closure_dW and bool(closure_dW & LEARNING_SIGNAL_LEAVES)
    if cls in ("C1", "C3"):
        out["backbone_exact"] = p.dW == SGD_W and p.db == SGD_B
    else:
        out["backbone_exact"] = (p.dW.op == "rowscale" and p.dW.args[0] == SGD_W and
                                 p.db.op == "mul" and p.db.args[0] == SGD_B)
    if cls == "C1":
        ok = len(p.regs) == 1
        if ok:
            r, up = p.regs[0], p.reg_updates[0]
            rt = {"r1": r.type}
            ok = (r.name == "r1" and r.type in V6_C1_REG_TYPES and r.lifetime == "RUN" and r.init == "0"
                  and r.decay in V6_DECAYS and _depth(up, rt, "STATE") in (1, 2)
                  and bool(reads(up) & V6_ACT_C1) and p.struct is None)
            if r.type == M:
                ok = ok and p.w_eff == fast_weight(REG) and p.gain is None
            else:
                ok = ok and p.gain == squash_gain(REG) and p.w_eff is None
        out["class_template_exact"] = ok
    elif cls == "C2":
        ok = (not p.regs and p.w_eff is None and p.gain is None and p.struct is None
              and p.dW.op == "rowscale" and p.db.op == "mul" and p.dW.args[1] == p.db.args[1])
        if ok:
            g = p.dW.args[1]
            sel = g.args[0].args[0].args[0] if (g.op == "add" and g.args[0].op == "mul"
                                                and g.args[0].args[0].op == "tanh") else None
            ok = (sel is not None and g == squash_gain(sel) and _depth(sel, {}, "PARAM") in (1, 2)
                  and bool(reads(sel) & V6_ACT_C23))
        out["class_template_exact"] = ok
    else:
        ok = len(p.regs) == 1 and p.struct is not None
        if ok:
            r, up = p.regs[0], p.reg_updates[0]
            ok = (r.name == "r1" and r.type == O and r.lifetime == "RUN" and r.init == "0"
                  and r.decay in V6_DECAYS and _depth(up, {"r1": O}, "STATE") in (1, 2)
                  and bool(reads(up) & V6_ACT_C23) and p.w_eff is None and p.gain is None
                  and p.struct.kind in V6_KINDS and p.struct.theta in V6_THETAS
                  and p.struct.mask == Node("tanh", (REG,)))
        out["class_template_exact"] = ok
    return out


def describe(p: Program) -> str:
    return " | ".join(f"{s}={sexpr(e)}" for s, e in p.slot_exprs())
