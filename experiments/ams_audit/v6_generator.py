"""Independent implementation and audit of the AMS v6 Learnability-Anchored Initial Proposal Generator.

Follows AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md v6 amendment (lines 164-225).
Performs structural proposal audit without training or task evaluation.
"""
from __future__ import annotations

import os
import sys
import random
from typing import Dict, List, Optional, Tuple
from collections import Counter

# Add ams to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "automated_mechanism_search")))

from ams.grammar import (
    Program, Node, RegDecl, Struct, const, typecheck,
    M, O, I, S, GrammarError, LEAF_TYPES, PHASE_LEAVES, UNARY, BINARY,
    TOPK_KS
)
from ams.generate import valid
from ams.fingerprint import fingerprint, Analysis


class V6AnchoredGenerator:
    """Independent implementation of the AMS v6 Learnability-Anchored Initial Proposal Generator."""

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def _sgd_backbone(self) -> Tuple[Node, Node]:
        # dW_base = neg(outer(d_bp, a))
        # db_base = neg(d_bp)
        dW_base = Node("neg", (Node("outer", (Node("leaf", (), "d_bp"), Node("leaf", (), "a"))),))
        db_base = Node("neg", (Node("leaf", (), "d_bp"),))
        return dW_base, db_base

    def _random_activity_expr(self, target_type: str, depth: int, rtypes: Dict[str, str], phase: str = "FORWARD") -> Node:
        """Draw an expression of target_type containing at least one activity leaf from {a, z, h, dphi}."""
        activity_leaves = {"a", "z", "h", "dphi"}
        for _ in range(50):
            node = self._expr(target_type, phase, rtypes, depth)
            leaves = {n.attr for n in node.walk() if n.op == "leaf"}
            if bool(leaves & activity_leaves):
                return node
        # Fallback to guaranteed activity leaf
        leaf_choice = self.rng.choice([l for l in ("z", "h", "dphi") if LEAF_TYPES[l] == target_type] or ["h"])
        return Node("leaf", (), leaf_choice)

    def _leaf(self, t: str, phase: str, rtypes: Dict[str, str]) -> Node:
        opts: List[Node] = [Node("leaf", (), n) for n, lt in LEAF_TYPES.items()
                            if lt == t and n in PHASE_LEAVES[phase] and n != "cvec"]
        opts += [Node("reg", (), n) for n, rt in rtypes.items() if rt == t]
        if t == S:
            opts.append(const(self.rng.choice((-1.0, -0.1, 0.0, 0.1, 0.5, 1.0, 2.0))))
        if not opts:
            raise GrammarError("no_leaf", f"{t} in {phase}")
        return self.rng.choice(opts)

    def _expr(self, t: str, phase: str, rtypes: Dict[str, str], depth: int) -> Node:
        if depth <= 0:
            return self._leaf(t, phase, rtypes)
        cands = [("unary", None)] * 3 + [("binary_TT", None)] * 3
        if t != S:
            cands += [("binary_TS", None)]
        if t == M:
            cands += [("outer", None)] * 2 + [("rowscale", None), ("colscale", None)]
        if t == O:
            cands += [("matvec", None), ("rowsum", None), ("topk", None), ("where", None)]
        if t == I:
            cands += [("matTvec", None), ("colsum", None), ("topk", None), ("where", None)]
        if t == S:
            cands += [("reduce", None)] * 2 + [("dot", None)]

        kind, extra = self.rng.choice(cands)
        d = depth - 1
        sub = lambda tt: self._expr(tt, phase, rtypes, d if self.rng.random() > 0.3 else 0)

        if kind == "unary":
            return Node(self.rng.choice(UNARY), (sub(t),))
        if kind == "binary_TT":
            return Node(self.rng.choice(BINARY), (sub(t), sub(t)))
        if kind == "binary_TS":
            # Note: in this grammar, binary(T, S) has T as first operand, S as second operand!
            return Node(self.rng.choice(BINARY), (sub(t), sub(S)))
        if kind == "outer":
            return Node("outer", (sub(O), sub(I)))
        if kind == "rowscale":
            return Node("rowscale", (sub(M), sub(O)))
        if kind == "colscale":
            return Node("colscale", (sub(M), sub(I)))
        if kind == "matvec":
            return Node("matvec", (sub(M), sub(I)))
        if kind == "matTvec":
            return Node("matTvec", (sub(M), sub(O)))
        if kind == "rowsum":
            return Node("rowsum", (sub(M),))
        if kind == "colsum":
            return Node("colsum", (sub(M),))
        if kind == "topk":
            return Node("topk", (sub(t),), self.rng.choice(TOPK_KS))
        if kind == "where":
            yb = sub(t) if self.rng.random() < 0.7 else sub(S)
            wb = sub(t) if self.rng.random() < 0.5 else sub(S)
            return Node("where", (sub(t), yb, wb))
        if kind == "reduce":
            xt = self.rng.choice([I, O, M])
            return Node(self.rng.choice(("mean", "norm", "amax")), (sub(xt),))
        if kind == "dot":
            xt = self.rng.choice([I, O, M])
            return Node("dot", (sub(xt), sub(xt)))
        raise AssertionError(kind)

    def generate_candidate(self, forced_class: Optional[str] = None) -> Tuple[Program, str]:
        """Generate one initial proposal per v6 specification."""
        c_class = forced_class or self.rng.choice(["C1", "C2", "C3"])
        dW_base, db_base = self._sgd_backbone()

        if c_class == "C1":
            # C1: state -> forward
            # exactly one persistent register of type O or M
            reg_type = self.rng.choice([O, M])
            decay = self.rng.choice([0.5, 0.9, 0.99])
            reg = RegDecl(name="r0", type=reg_type, lifetime="RUN", init="0", decay=decay)
            rtypes = {"r0": reg_type}

            depth = self.rng.choice([1, 2])
            upd = self._random_activity_expr(reg_type, depth, rtypes, phase="STATE")

            # Perturbation: mul(tanh(reg), 0.1)
            reg_node = Node("reg", (), "r0")
            pert = Node("mul", (Node("tanh", (reg_node,)), const(0.1)))

            if reg_type == M:
                w_eff = pert
                gain = None
            else:
                # Type-safe add(O, S): add(pert, 1.0)
                gain = Node("add", (pert, const(1.0)))
                w_eff = None

            prog = Program(regs=[reg], reg_updates=[upd], w_eff=w_eff, gain=gain,
                           dW=dW_base, db=db_base, update_every=1, struct=None, cvec=None)
            return prog, "C1"

        elif c_class == "C2":
            # C2: activity-routed credit/update
            # No persistent register
            depth = self.rng.choice([1, 2])
            # Selector expression must contain activity leaf from {z, h, dphi}
            selector = self._random_activity_expr(O, depth, {}, phase="PARAM")

            # g = add(1.0, mul(tanh(selector), 0.1)) -> in grammar, type is O, operand 1 is O, operand 2 is S
            # pert = mul(tanh(selector), 0.1)
            pert = Node("mul", (Node("tanh", (selector,)), const(0.1)))
            g = Node("add", (pert, const(1.0)))

            dW = Node("rowscale", (dW_base, g))
            db = Node("mul", (db_base, g))

            prog = Program(regs=[], reg_updates=[], w_eff=None, gain=None,
                           dW=dW, db=db, update_every=1, struct=None, cvec=None)
            return prog, "C2"

        elif c_class == "C3":
            # C3: data-dependent structural operation
            decay = self.rng.choice([0.5, 0.9, 0.99])
            reg = RegDecl(name="r0", type=O, lifetime="RUN", init="0", decay=decay)
            rtypes = {"r0": O}

            depth = self.rng.choice([1, 2])
            upd = self._random_activity_expr(O, depth, rtypes, phase="STATE")

            kind = self.rng.choice(["freeze", "reinit"])
            mask = Node("tanh", (Node("reg", (), "r0"),))
            theta = self.rng.choice([0.0, 0.1, 0.5])
            st = Struct(kind=kind, mask=mask, theta=theta)

            prog = Program(regs=[reg], reg_updates=[upd], w_eff=None, gain=None,
                           dW=dW_base, db=db_base, update_every=1, struct=st, cvec=None)
            return prog, "C3"

        raise ValueError(c_class)


def run_structural_proposal_audit(n_samples: int = 1000, seed: int = 2026092899) -> Dict:
    gen = V6AnchoredGenerator(seed=seed)
    
    class_counts = Counter()
    type_valid_count = 0
    node_constraints_count = 0
    reg_constraints_count = 0
    coupling_detected_counts = Counter()
    descriptor_counts = Counter()
    c2_routing_gate_present = 0
    c2_pure_rule_collapse = 0

    proposals = []
    for i in range(n_samples):
        p, c_class = gen.generate_candidate()
        class_counts[c_class] += 1

        # 1. Type validity check
        v_code = valid(p)
        if v_code is None:
            type_valid_count += 1
        
        # 2. Node count / depth constraints
        # Max nodes <= 45, max nodes per expr <= 15, depth <= 4
        all_nodes = sum(len(list(e.walk())) for e in (p.w_eff, p.gain, p.dW, p.db) if e)
        if p.struct and p.struct.mask:
            all_nodes += len(list(p.struct.mask.walk()))
        all_nodes += sum(len(list(u.walk())) for u in p.reg_updates)
        if all_nodes <= 45:
            node_constraints_count += 1

        # 3. Register constraints
        n_regs = len(p.regs)
        if c_class == "C1" and n_regs == 1 and p.regs[0].lifetime == "RUN":
            reg_constraints_count += 1
        elif c_class == "C2" and n_regs == 0:
            reg_constraints_count += 1
        elif c_class == "C3" and n_regs == 1 and p.regs[0].lifetime == "RUN" and p.regs[0].type == O:
            reg_constraints_count += 1

        # 4. Fingerprint & Coupling Analysis
        if v_code is None:
            fp = fingerprint(p)
            couplings = fp["couplings"]
            coupling_detected_counts[tuple(sorted(couplings))] += 1

            desc = fp["descriptor"]
            if desc is not None:
                descriptor_counts[tuple(desc)] += 1
            else:
                descriptor_counts["NONE (COLLAPSE)"] += 1

            if c_class == "C2":
                a = Analysis(p)
                gates = a._routing_gates(p.dW)
                if gates:
                    c2_routing_gate_present += 1
                if not couplings:
                    c2_pure_rule_collapse += 1

    return {
        "n_samples": n_samples,
        "class_counts": dict(class_counts),
        "type_valid_count": type_valid_count,
        "node_constraints_count": node_constraints_count,
        "reg_constraints_count": reg_constraints_count,
        "coupling_detected_counts": {str(k): v for k, v in coupling_detected_counts.items()},
        "descriptor_counts": {str(k): v for k, v in descriptor_counts.items()},
        "c2_routing_gate_present": c2_routing_gate_present,
        "c2_pure_rule_collapse": c2_pure_rule_collapse,
    }


if __name__ == "__main__":
    res = run_structural_proposal_audit(1000, 2026092899)
    import json
    print(json.dumps(res, indent=2))
