"""Random typed program generation (grow method, depth 2-4) and the AE.3.5 mutation /
crossover operators.  Generation is uniform over the typed grammar: it never
intentionally instantiates an excluded family (prereg v2 sec. 3)."""
from __future__ import annotations

import random
from dataclasses import replace
from typing import Dict, List, Optional, Tuple

from .grammar import (BINARY, CONSTS, DECAYS, INITS, LIFETIMES, M, MAX_M_REGS, O, PHASE_LEAVES,
                      S, STRUCT_KINDS, STRUCT_THETAS, TOPK_KS, UNARY, UPDATE_EVERY, I, GrammarError,
                      LEAF_TYPES, Node, Program, RegDecl, Struct, const, slot_phase, typecheck)

MUTATION_P = (("point_op", 0.25), ("subtree", 0.20), ("leaf_swap", 0.15), ("const", 0.10),
              ("register", 0.10), ("rewire_forward", 0.08), ("gate", 0.07), ("struct", 0.03),
              ("timing", 0.02))
P_CROSS = 0.2
MAX_RETRY = 10


class Gen:
    # Zero branch of the m_gate `where` variant.  v5-v7 historical behaviour: a literal 0.0, which is
    # outside the frozen constant set, so that variant always produced an invalid offspring.  Prereg
    # v8 repairs it in `ams.v8gen.V8Gen` with the grammar-legal (sub 1.0 1.0); this default keeps the
    # recorded v5-v7 traces reproducible.
    where_zero = None

    def __init__(self, rng: random.Random):
        self.r = rng

    # ------------------------------------------------------------------ leaves
    def leaf(self, t: str, phase: str, rtypes: Dict[str, str], has_cvec: bool = True) -> Node:
        opts: List[Node] = [Node("leaf", (), n) for n, lt in LEAF_TYPES.items()
                            if lt == t and n in PHASE_LEAVES[phase] and (n != "cvec" or has_cvec)]
        opts += [Node("reg", (), n) for n, rt in rtypes.items() if rt == t]
        if t == S:
            opts.append(const(self.r.choice(CONSTS)))
        if not opts:
            raise GrammarError("no_leaf", f"{t} in {phase}")
        return self.r.choice(opts)

    # ------------------------------------------------------------------ expressions
    def expr(self, t: str, phase: str, rtypes: Dict[str, str], depth: int, has_cvec: bool = True) -> Node:
        """Grow method: stop at depth 0 or with probability 0.3 (never at the top level)."""
        if depth <= 0:
            return self.leaf(t, phase, rtypes, has_cvec)
        cands = []
        cands += [("unary", None)] * 3
        cands += [("binary_TT", None)] * 3
        if t != S:
            cands += [("binary_TS", None)]
        if t == M:
            cands += [("outer", None)] * 2 + [("rowscale", None), ("colscale", None)]
        if t == O:
            cands += [("matvec", None), ("rowsum", None), ("norm1", "nrm"), ("norm1", "unit"),
                      ("topk", None), ("where", None)]
        if t == I:
            cands += [("matTvec", None), ("colsum", None), ("norm1", "nrm"), ("norm1", "unit"),
                      ("topk", None), ("where", None)]
        if t == S:
            cands += [("reduce", None)] * 2 + [("dot", None)]
        kind, extra = self.r.choice(cands)
        d = depth - 1
        sub = lambda tt: self.expr(tt, phase, rtypes, d if self.r.random() > 0.3 else 0, has_cvec)
        if kind == "unary":
            return Node(self.r.choice(UNARY), (sub(t),))
        if kind == "binary_TT":
            return Node(self.r.choice(BINARY), (sub(t), sub(t)))
        if kind == "binary_TS":
            return Node(self.r.choice(BINARY), (sub(t), sub(S)))
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
        if kind == "norm1":
            return Node(extra, (sub(t),))
        if kind == "topk":
            return Node("topk", (sub(t),), self.r.choice(TOPK_KS))
        if kind == "where":
            yb = sub(t) if self.r.random() < 0.7 else sub(S)
            wb = sub(t) if self.r.random() < 0.5 else sub(S)
            return Node("where", (sub(t), yb, wb))
        if kind == "reduce":
            xt = self.r.choice([I, O, M])
            return Node(self.r.choice(("mean", "norm", "amax")), (sub(xt),))
        if kind == "dot":
            xt = self.r.choice([I, O, M])
            return Node("dot", (sub(xt), sub(xt)))
        raise AssertionError(kind)

    def depth(self) -> int:
        return self.r.randint(2, 4)

    # ------------------------------------------------------------------ programs
    def reg_decl(self, name: str, allow_M: bool) -> RegDecl:
        types = [I, O] + ([M] if allow_M else [])
        return RegDecl(name, self.r.choice(types), self.r.choice(LIFETIMES), self.r.choice(INITS),
                       self.r.choice(DECAYS))

    def program(self) -> Program:
        n = self.r.choice([0, 1, 1, 2, 2, 3, 4])
        regs: List[RegDecl] = []
        for k in range(n):
            nm = sum(r.type == M for r in regs)
            regs.append(self.reg_decl(f"r{k + 1}", nm < MAX_M_REGS))
        rt = {r.name: r.type for r in regs}
        has_cvec = True
        w_eff = self.expr(M, "FORWARD", rt, self.depth()) if self.r.random() < 0.4 else None
        gain = self.expr(O, "FORWARD", rt, self.depth()) if self.r.random() < 0.2 else None
        cvec = self.expr(O, "CREDIT", rt, self.depth(), has_cvec=False)
        ups = tuple(self.expr(r.type, "STATE", rt, self.depth()) for r in regs)
        dW = self.expr(M, "PARAM", rt, self.depth())
        db = self.expr(O, "PARAM", rt, self.depth())
        st = None
        if self.r.random() < 0.15:
            st = Struct(self.r.choice(STRUCT_KINDS), self.expr(O, "STRUCT", rt, self.depth()),
                        self.r.choice(STRUCT_THETAS))
        return Program(self.r.choice(UPDATE_EVERY), tuple(regs), ups, cvec, dW, db, w_eff, gain, st)

    # ------------------------------------------------------------------ mutation helpers
    def _slots(self, p: Program) -> List[Tuple[str, Node]]:
        return p.slot_exprs()

    @staticmethod
    def _subtrees(e: Node, path=()) -> List[Tuple[Tuple[int, ...], Node]]:
        out = [(path, e)]
        for k, c in enumerate(e.args):
            out += Gen._subtrees(c, path + (k,))
        return out

    @staticmethod
    def _replace_at(e: Node, path: Tuple[int, ...], new: Node) -> Node:
        if not path:
            return new
        k = path[0]
        args = list(e.args)
        args[k] = Gen._replace_at(args[k], path[1:], new)
        return Node(e.op, tuple(args), e.attr)

    @staticmethod
    def _set_slot(p: Program, slot: str, e: Node) -> Program:
        if slot.startswith("reg:"):
            nm = slot[4:]
            ups = tuple(e if r.name == nm else u for r, u in zip(p.regs, p.reg_updates))
            return replace(p, reg_updates=ups)
        if slot == "struct":
            return replace(p, struct=replace(p.struct, mask=e))
        return replace(p, **{slot: e})

    def _typed_subtree(self, p: Program):
        from .grammar import type_of
        slot, e = self.r.choice(self._slots(p))
        path, node = self.r.choice(self._subtrees(e))
        return slot, e, path, node, type_of(node, p.reg_types())

    # ------------------------------------------------------------------ AE.3.5 operators
    def mutate(self, p: Program) -> Program:
        ops, ws = zip(*MUTATION_P)
        which = self.r.choices(ops, ws)[0]
        return getattr(self, "m_" + which)(p)

    def m_point_op(self, p):
        from .grammar import type_of
        slot, e, path, node, t = self._typed_subtree(p)
        if node.op in UNARY:
            new = Node(self.r.choice(UNARY), node.args)
        elif node.op in BINARY:
            new = Node(self.r.choice(BINARY), node.args)
        elif node.op in ("mean", "norm", "amax"):
            new = Node(self.r.choice(("mean", "norm", "amax")), node.args)
        elif node.op in ("nrm", "unit"):
            new = Node(self.r.choice(("nrm", "unit")), node.args)
        elif node.op in ("rowsum",):
            new = node
        else:
            return self.m_subtree(p)
        return self._set_slot(p, slot, self._replace_at(e, path, new))

    def m_subtree(self, p):
        slot, e, path, node, t = self._typed_subtree(p)
        new = self.expr(t, slot_phase(slot), p.reg_types(), self.r.randint(0, 3), p.cvec is not None)
        return self._set_slot(p, slot, self._replace_at(e, path, new))

    def m_leaf_swap(self, p):
        slot, e = self.r.choice(self._slots(p))
        leaves = [(pa, n) for pa, n in self._subtrees(e) if not n.args]
        path, node = self.r.choice(leaves)
        from .grammar import type_of
        t = type_of(node, p.reg_types())
        new = self.leaf(t, slot_phase(slot), p.reg_types(), p.cvec is not None)
        return self._set_slot(p, slot, self._replace_at(e, path, new))

    def m_const(self, p):
        choices = ["decay", "init", "k", "theta", "c"]
        w = self.r.choice(choices)
        if w in ("decay", "init") and p.regs:
            k = self.r.randrange(len(p.regs))
            r = p.regs[k]
            r2 = replace(r, decay=self.r.choice(DECAYS)) if w == "decay" else replace(r, init=self.r.choice(INITS))
            return replace(p, regs=tuple(r2 if j == k else x for j, x in enumerate(p.regs)))
        if w == "theta" and p.struct is not None:
            return replace(p, struct=replace(p.struct, theta=self.r.choice(STRUCT_THETAS)))
        for slot, e in self.r.sample(self._slots(p), len(self._slots(p))):
            nodes = [(pa, n) for pa, n in self._subtrees(e) if n.op in ("const", "topk")]
            if nodes:
                path, n = self.r.choice(nodes)
                new = const(self.r.choice(CONSTS)) if n.op == "const" else Node("topk", n.args, self.r.choice(TOPK_KS))
                return self._set_slot(p, slot, self._replace_at(e, path, new))
        return p

    def m_register(self, p):
        if p.regs and (len(p.regs) >= 4 or self.r.random() < 0.4):
            if self.r.random() < 0.5:     # change lifetime
                k = self.r.randrange(len(p.regs))
                r2 = replace(p.regs[k], lifetime=self.r.choice(LIFETIMES))
                return replace(p, regs=tuple(r2 if j == k else x for j, x in enumerate(p.regs)))
            k = self.r.randrange(len(p.regs))          # remove: reads become an init-typed leaf
            nm = p.regs[k].name
            from .canon import replace_reg
            rt = p.reg_types()
            t = rt[nm]
            def repl(slot):
                return self.leaf(t, slot_phase(slot), {n: v for n, v in rt.items() if n != nm}, p.cvec is not None)
            q = replace(p, regs=tuple(r for j, r in enumerate(p.regs) if j != k),
                        reg_updates=tuple(u for j, u in enumerate(p.reg_updates) if j != k))
            for slot, e in q.slot_exprs():
                q = self._set_slot(q, slot, replace_reg(e, nm, repl(slot)))
            return q
        names = {r.name for r in p.regs}
        nm = next(f"r{k}" for k in range(1, 9) if f"r{k}" not in names)
        rd = self.reg_decl(nm, sum(r.type == M for r in p.regs) < MAX_M_REGS)
        rt = dict(p.reg_types()); rt[nm] = rd.type
        up = self.expr(rd.type, "STATE", rt, self.depth(), p.cvec is not None)
        q = replace(p, regs=p.regs + (rd,), reg_updates=p.reg_updates + (up,))
        # make it read somewhere
        slot, e = self.r.choice([s for s in q.slot_exprs() if s[0] in ("dW", "db", "w_eff", "gain")])
        from .grammar import type_of
        path, node = self.r.choice(self._subtrees(e))
        if type_of(node, rt) == rd.type:
            q = self._set_slot(q, slot, self._replace_at(e, path, Node("reg", (), nm)))
        return q

    def m_rewire_forward(self, p):
        rt = p.reg_types()
        if self.r.random() < 0.6:
            new = self.expr(M, "FORWARD", rt, self.depth()) if (p.w_eff is None or self.r.random() < 0.7) else None
            return replace(p, w_eff=new)
        new = self.expr(O, "FORWARD", rt, self.depth()) if (p.gain is None or self.r.random() < 0.7) else None
        return replace(p, gain=new)

    def m_gate(self, p):
        if self.r.random() < 0.5:
            # remove a top-level gate if present
            if p.dW.op == "rowscale" and p.dW.args[1].op in ("topk", "where"):
                return replace(p, dW=p.dW.args[0])
        sel = self.expr(O, "PARAM", p.reg_types(), 1, p.cvec is not None)
        if self.r.random() < 0.5:
            g = Node("topk", (sel,), self.r.choice(TOPK_KS))
        else:
            g = Node("where", (sel, const(1.0), const(0.0) if self.where_zero is None else self.where_zero))
        return replace(p, dW=Node("rowscale", (p.dW, g)))

    def m_struct(self, p):
        if p.struct is not None and self.r.random() < 0.5:
            return replace(p, struct=None)
        return replace(p, struct=Struct(self.r.choice(STRUCT_KINDS),
                                        self.expr(O, "STRUCT", p.reg_types(), self.depth(), p.cvec is not None),
                                        self.r.choice(STRUCT_THETAS)))

    def m_timing(self, p):
        return replace(p, update_every=8 if p.update_every == 1 else 1)

    def crossover(self, a: Program, b: Program) -> Program:
        """Swap a random subtree of the same slot kind and type from b into a."""
        from .grammar import type_of
        sa = dict(a.slot_exprs())
        sb = dict(b.slot_exprs())
        common = [s for s in ("w_eff", "gain", "cvec", "dW", "db", "struct") if s in sa and s in sb]
        if not common:
            return a
        slot = self.r.choice(common)
        ea, eb = sa[slot], sb[slot]
        pa, na = self.r.choice(self._subtrees(ea))
        ta = type_of(na, a.reg_types())
        donors = [n for _, n in self._subtrees(eb)
                  if type_of(n, b.reg_types()) == ta and not ({x.attr for x in n.walk() if x.op == "reg"} - set(a.reg_types()))
                  and all(a.reg_types().get(x.attr) == b.reg_types().get(x.attr) for x in n.walk() if x.op == "reg")]
        if not donors:
            return a
        return self._set_slot(a, slot, self._replace_at(ea, pa, self.r.choice(donors)))


def valid(p: Program) -> Optional[str]:
    try:
        typecheck(p)
        return None
    except GrammarError as e:
        return e.code
    except Exception as e:  # pragma: no cover
        return "error:" + type(e).__name__
