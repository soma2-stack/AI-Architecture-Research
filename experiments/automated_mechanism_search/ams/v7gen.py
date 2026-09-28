"""Prereg v7 initial-proposal constructor: v6 SGD-anchored C1 / C3 unchanged, C2 replaced by
detector-aligned bounded activity routing.

C2 (v7): selector = O-typed PARAM-phase grammar draw at depth 0-1 reading at least one of
{z, h, dphi}; route = topk(selector, k), k uniform over {1, 4, 8}, or where(selector, 1.0, 0.0),
chosen uniformly;
    dW = add(dW_base, mul(rowscale(dW_base, route), 0.1))
    db = add(db_base, mul(mul(db_base, route), 0.1))
with dW_base = (neg (outer d_bp a)), db_base = (neg d_bp), update_every = 1.

Implementation decisions (IMPLEMENTATION_DECISIONS.md D-V7-*):
  * The frozen constant set is {-1, -0.5, 0.1, 0.5, 1, 2}; a literal 0.0 is not a legal
    generated constant (typecheck: bad_const).  The `where` route's 0.0 branch is therefore
    spelled `(sub 1.0 1.0)`, a legal S-typed expression equal to 0 that the unchanged
    canonicalizer folds back to 0: the canonical program -- the one the pipeline hashes,
    fingerprints, probes and evaluates -- is exactly `where(selector, 1, 0)` (D-V7-2).
  * "depth 0-1" = the grow-method depth argument drawn uniformly from {0, 1} (D-V7-3).
  * Accounting as in v6 (D-V6-4), now stated by v7: activity-leaf redraws are conditional
    sampling and are not counted; instantiated programs that fail validation are counted, at
    most 10 attempts per requested proposal with the class held fixed (D-V7-4).
Nothing here reads a task, T0, probe or benchmark outcome.
"""
from __future__ import annotations

from typing import Dict, Tuple

from .grammar import (LEARNING_SIGNAL_LEAVES, MAX_DEPTH, MAX_M_REGS, MAX_NODES, MAX_REGS, TOPK_KS, M,
                      O, GrammarError, Node, Program, const, reads, typecheck)
from .v6gen import (SGD_B, SGD_W, V6_ACT_C23, V6_MAX_REDRAW, AnchoredGen, _depth, v6_invariants)

V7_CLASSES = ("C1", "C2", "C3")
V7_SELECTOR_DEPTHS = (0, 1)
V7_ACT_C2 = V6_ACT_C23                      # {z, h, dphi}
V7_ROUTES = ("topk", "where")
V7_TOPK_KS = (1, 4, 8)
V7_RESIDUAL = 0.1
ZERO_S = Node("sub", (const(1.0), const(1.0)))      # legal spelling of the scalar 0.0 branch

assert V7_TOPK_KS == TOPK_KS


def route_node(kind: str, sel: Node, k=None) -> Node:
    if kind == "topk":
        return Node("topk", (sel,), k)
    return Node("where", (sel, const(1.0), ZERO_S))


def c2_updates(route: Node) -> Tuple[Node, Node]:
    """dW = add(dW_base, mul(rowscale(dW_base, route), 0.1)); db = add(db_base, mul(mul(db_base, route), 0.1))."""
    dW = Node("add", (SGD_W, Node("mul", (Node("rowscale", (SGD_W, route)), const(V7_RESIDUAL)))))
    db = Node("add", (SGD_B, Node("mul", (Node("mul", (SGD_B, route)), const(V7_RESIDUAL)))))
    return dW, db


class DetectorAlignedGen(AnchoredGen):
    """v6 `AnchoredGen` with the v7 C2 rule; C1 / C3, slot logic, retries, mutation and crossover
    are inherited unchanged.  Metadata key "v6_class" is kept as the class key for all anchored
    constructors; "constructor" says which one."""

    def _c2_selector(self) -> Tuple[Node, int]:
        for k in range(V6_MAX_REDRAW):
            e = self.expr(O, "PARAM", {}, self.r.choice(V7_SELECTOR_DEPTHS), has_cvec=False)
            if reads(e) & V7_ACT_C2:
                return e, k
        raise RuntimeError("v7 conditional draw exhausted")        # pragma: no cover

    def v6_attempt(self, cls: str) -> Tuple[Program, Dict]:
        if cls != "C2":
            p, meta = super().v6_attempt(cls)
            meta["constructor"] = "v7"
            return p, meta
        sel, k = self._c2_selector()                 # draw order: selector, route kind, k
        kind = self.r.choice(V7_ROUTES)
        kk = self.r.choice(V7_TOPK_KS) if kind == "topk" else None
        route = route_node(kind, sel, kk)
        dW, db = c2_updates(route)
        p = Program(1, (), (), None, dW, db)
        meta = {"v6_class": "C2", "constructor": "v7", "route": kind, "k": kk, "redraws": k,
                "expr_depth": _depth(sel, {}, "PARAM")}
        self.redraws += k
        return p, meta


def v7_invariants(p: Program, meta: Dict) -> Dict[str, bool]:
    """Constructor-level checks of the v7 specification for one emitted proposal."""
    cls = meta["v6_class"]
    if cls != "C2":
        return v6_invariants(p, meta)                # v6 C1 / C3 rules carry forward unchanged
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
    cl = reads(p.dW)
    out["backprop_signal_in_dW"] = "d_bp" in cl and bool(cl & LEARNING_SIGNAL_LEAVES)
    ok_shape = (p.dW.op == "add" and len(p.dW.args) == 2 and p.dW.args[1].op == "mul"
                and p.dW.args[1].args[0].op == "rowscale" and p.db.op == "add" and len(p.db.args) == 2
                and p.db.args[1].op == "mul" and p.db.args[1].args[0].op == "mul")
    route = p.dW.args[1].args[0].args[1] if ok_shape else None
    out["backbone_exact"] = bool(ok_shape and p.dW.args[0] == SGD_W and p.dW.args[1].args[0].args[0] == SGD_W
                                 and p.db.args[0] == SGD_B and p.db.args[1].args[0].args[0] == SGD_B)
    out["residual_scale_0.1"] = bool(ok_shape and p.dW.args[1].args[1] == const(V7_RESIDUAL)
                                     and p.db.args[1].args[1] == const(V7_RESIDUAL))
    ok = ok_shape and not p.regs and p.w_eff is None and p.gain is None and p.struct is None
    ok = ok and p.db.args[1].args[0].args[1] == route and (p.dW, p.db) == c2_updates(route)
    if ok:
        sel = route.args[0]
        if route.op == "topk":
            ok = route.attr in V7_TOPK_KS and meta.get("route") == "topk" and meta.get("k") == route.attr
        else:
            ok = (route.op == "where" and route.args[1] == const(1.0) and route.args[2] == ZERO_S
                  and meta.get("route") == "where")
        ok = ok and _depth(sel, {}, "PARAM") in V7_SELECTOR_DEPTHS and bool(reads(sel) & V7_ACT_C2)
    out["class_template_exact"] = bool(ok)
    return out
