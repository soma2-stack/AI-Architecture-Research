"""Level-A canonicalization and structural hashing (Claude Part AE.2.1).

canon(P):
    typecheck -> inline temporaries (EXAMPLE registers, cvec) -> dead-code elimination
    -> constant folding + fixed-point rewrite simplification (<= 20 passes)
    -> commutative operand sorting -> canonical register renaming (first use).
Soundness notes and the exact inlining conditions: IMPLEMENTATION_DECISIONS.md D-CANON-*.
"""
from __future__ import annotations

import hashlib
from dataclasses import replace
from typing import Dict, List, Optional, Tuple

from .grammar import (COMMUTATIVE, M, O, S, Node, Program, RegDecl, Struct, const, is_const,
                      const_value, infer, reads, serialize, sexpr, tconst, type_of, typecheck)

MAX_PASSES = 20


# ---------------------------------------------------------------------------
# substitution helpers
# ---------------------------------------------------------------------------

def subst(n: Node, fn) -> Node:
    """Bottom-up rewrite; fn(node) returns a replacement or None."""
    if n.args:
        new_args = tuple(subst(c, fn) for c in n.args)
        if new_args != n.args:
            n = Node(n.op, new_args, n.attr)
    r = fn(n)
    return n if r is None else r


def replace_reg(n: Node, name: str, repl: Node) -> Node:
    return subst(n, lambda x: repl if (x.op == "reg" and x.attr == name) else None)


def replace_leaf(n: Node, name: str, repl: Node) -> Node:
    return subst(n, lambda x: repl if (x.op == "leaf" and x.attr == name) else None)


def _regs_in(n: Node) -> set:
    return {x.attr for x in n.walk() if x.op == "reg"}


# ---------------------------------------------------------------------------
# temporaries
# ---------------------------------------------------------------------------

def _mix_value(v: Node, init: float, lam: float, t: str) -> Node:
    """lam*init + (1-lam)*v, as an expression of type t."""
    if lam == 0.0:
        base = v
    else:
        base = Node("mul", (v, const(1.0 - lam)))
    if init != 0.0 and lam != 0.0:
        base = Node("add", (base, const(lam * init)))
    return base


def inline_example_registers(p: Program) -> Program:
    changed = True
    while changed:
        changed = False
        rt = p.reg_types()
        for idx, (rd, v) in enumerate(zip(p.regs, p.reg_updates)):
            if rd.lifetime != "EXAMPLE" or rd.init == "noise":
                continue
            other_regs = _regs_in(v) - {rd.name}
            # v may read other EXAMPLE registers (which sit at their reset value in STATE)
            persistent = {r for r in other_regs
                          if next(x for x in p.regs if x.name == r).lifetime != "EXAMPLE"}
            if persistent:
                continue
            init = float(rd.init)
            t = rd.type
            reset = tconst(init, t)
            v0 = replace_reg(v, rd.name, reset)
            for other in other_regs:
                od = next(x for x in p.regs if x.name == other)
                if od.init == "noise":
                    break
                v0 = replace_reg(v0, other, tconst(float(od.init), od.type))
            else:
                after = _mix_value(v0, init, rd.decay, t)
                p = _apply_register_inline(p, idx, before=reset, after=after)
                changed = True
                break
    return p


def _apply_register_inline(p: Program, idx: int, before: Node, after: Node) -> Program:
    """Remove register idx; reads in FORWARD/CREDIT/STATE see `before`, PARAM/STRUCT see `after`."""
    name = p.regs[idx].name
    regs = tuple(r for k, r in enumerate(p.regs) if k != idx)
    ups = tuple(replace_reg(u, name, before) for k, u in enumerate(p.reg_updates) if k != idx)
    return replace(
        p, regs=regs, reg_updates=ups,
        w_eff=None if p.w_eff is None else replace_reg(p.w_eff, name, before),
        gain=None if p.gain is None else replace_reg(p.gain, name, before),
        cvec=None if p.cvec is None else replace_reg(p.cvec, name, before),
        dW=replace_reg(p.dW, name, after),
        db=replace_reg(p.db, name, after),
        struct=None if p.struct is None else replace(p.struct, mask=replace_reg(p.struct.mask, name, after)),
    )


def inline_overwrite_registers(p: Program) -> Program:
    """mix(r, v, 0) -> v when r is not read before its write (only PARAM/STRUCT read it)."""
    changed = True
    while changed:
        changed = False
        for idx, (rd, v) in enumerate(zip(p.regs, p.reg_updates)):
            if rd.decay != 0.0 or rd.lifetime == "EXAMPLE" or rd.init == "noise":
                continue
            early = set()
            for e in [p.w_eff, p.gain, p.cvec] + list(p.reg_updates):
                if e is not None:
                    early |= _regs_in(e)
            if rd.name in early:
                continue
            if _regs_in(v):
                continue  # v reads old register values; PARAM would see new ones
            p = _apply_register_inline(p, idx, before=tconst(0.0, rd.type), after=v)
            changed = True
            break
    return p


def inline_cvec(p: Program) -> Program:
    if p.cvec is None:
        return p
    c = p.cvec
    ups = tuple(replace_leaf(u, "cvec", c) for u in p.reg_updates)
    p = replace(p, reg_updates=ups)
    if _regs_in(c):
        return p   # PARAM/STRUCT would see new register values: keep the slot there
    return replace(
        p,
        dW=replace_leaf(p.dW, "cvec", c),
        db=replace_leaf(p.db, "cvec", c),
        struct=None if p.struct is None else replace(p.struct, mask=replace_leaf(p.struct.mask, "cvec", c)),
    )


def dead_code_elim(p: Program) -> Program:
    live_exprs = [e for e in (p.w_eff, p.gain, p.dW, p.db) if e is not None]
    if p.struct is not None:
        live_exprs.append(p.struct.mask)
    live_regs: set = set()
    cvec_live = False
    upd = {r.name: u for r, u in zip(p.regs, p.reg_updates)}
    frontier = list(live_exprs)
    while frontier:
        e = frontier.pop()
        rs = reads(e)
        if "cvec" in rs and not cvec_live and p.cvec is not None:
            cvec_live = True
            frontier.append(p.cvec)
        for r in rs:
            if r in upd and r not in live_regs:
                live_regs.add(r)
                frontier.append(upd[r])
    keep = [k for k, r in enumerate(p.regs) if r.name in live_regs]
    return replace(
        p,
        regs=tuple(p.regs[k] for k in keep),
        reg_updates=tuple(p.reg_updates[k] for k in keep),
        cvec=p.cvec if cvec_live else None,
    )


# ---------------------------------------------------------------------------
# constant folding and rewrite rules
# ---------------------------------------------------------------------------

def _zero(t: str) -> Node:
    return const(0.0) if t == S else tconst(0.0, t)


def _is_val(n: Node, v: float) -> bool:
    return is_const(n) and const_value(n) == v


def _fold(n: Node, rt: Dict[str, str]) -> Optional[Node]:
    from . import interp
    import numpy as np
    if not n.args or not all(is_const(c) for c in n.args):
        return None
    o = n.op
    t = type_of(n, rt)
    vals = [const_value(c) for c in n.args]
    with np.errstate(all="ignore"):
        if o in interp.UNARY_FN:
            if o in ("nrm",):
                return None
            v = float(interp.UNARY_FN[o](np.float64(vals[0])))
        elif o in interp.BINARY_FN:
            v = float(interp.BINARY_FN[o](np.float64(vals[0]), np.float64(vals[1])))
        elif o == "outer" or o == "rowscale" or o == "colscale":
            v = vals[0] * vals[1]
        elif o == "mean":
            v = vals[0]
        elif o == "amax":
            v = abs(vals[0])
        elif o == "nrm":
            v = 0.0
        elif o == "where":
            v = vals[1] if vals[0] > 0 else vals[2]
        else:
            return None   # dimension-dependent (norm, dot, matvec, rowsum, unit, topk, ...)
    if not np.isfinite(v):
        return None
    return const(v) if t == S else tconst(v, t)


def _rewrite(n: Node, rt: Dict[str, str]) -> Optional[Node]:
    o, a = n.op, n.args
    f = _fold(n, rt)
    if f is not None:
        return f
    if o in ("add", "sub"):
        x, y = a
        if _is_val(y, 0.0):
            return x
        if o == "add" and _is_val(x, 0.0) and type_of(y, rt) == type_of(n, rt):
            return y
        if o == "sub" and x == y:
            return _zero(type_of(n, rt))
    if o == "mul":
        x, y = a
        t = type_of(n, rt)
        if _is_val(y, 0.0) or _is_val(x, 0.0):
            return _zero(t)
        if _is_val(y, 1.0) and type_of(x, rt) == t:
            return x
        if _is_val(x, 1.0) and type_of(y, rt) == t:
            return y
        if x == y:
            return Node("square", (x,))
    if o == "neg" and a[0].op == "neg":
        return a[0].args[0]
    if o == "abs" and a[0].op == "abs":
        return a[0]
    if o == "sign" and a[0].op == "square":
        return Node("step", (Node("abs", a[0].args),))
    if o in ("nrm", "unit") and a[0].op == o:
        return a[0]
    if o == "where" and a[1] == a[2] and type_of(a[1], rt) == type_of(n, rt):
        return a[1]
    if o == "outer" and a[0].op == "mul":
        u, v = a[0].args
        if type_of(v, rt) == S and type_of(u, rt) == O:
            return Node("mul", (Node("outer", (u, a[1])), v))
    if o == "rowscale" and a[0].op == "outer":
        oo, ii = a[0].args
        return Node("outer", (Node("mul", (oo, a[1])), ii))
    return None


def _reg_signatures(p: Program) -> Dict[str, str]:
    """Name-free content signature of each register (type, lifetime, init, decay, abstract
    update), iterated so that registers are distinguished by what they read."""
    sig = {r.name: f"{r.type}|{r.lifetime}|{r.init}|{r.decay}" for r in p.regs}
    upd = {r.name: u for r, u in zip(p.regs, p.reg_updates)}
    for _ in range(3):
        new = {}
        for r in p.regs:
            new[r.name] = sig[r.name] + "|" + _keyed(upd[r.name], sig)
        sig = new
    return sig


def _keyed(n: Node, sig: Dict[str, str]) -> str:
    if n.op == "reg":
        return "{" + sig.get(n.attr, "?") + "}"
    if not n.args:
        return sexpr(n)
    inner = " ".join(_keyed(c, sig) for c in n.args)
    return f"({n.op}{'' if n.attr is None else ':' + str(n.attr)} {inner})"


def _sort_commutative(n: Node, rt: Dict[str, str], sig: Dict[str, str]) -> Optional[Node]:
    if n.op in COMMUTATIVE and len(n.args) == 2:
        x, y = n.args
        tx, ty = type_of(x, rt), type_of(y, rt)
        if tx == ty:
            kx, ky = _keyed(x, sig), _keyed(y, sig)
            if (ky, sexpr(y)) < (kx, sexpr(x)):
                return Node(n.op, (y, x), n.attr)
    return None


def simplify(n: Node, rt: Dict[str, str]) -> Node:
    for _ in range(MAX_PASSES):
        m = subst(n, lambda x: _rewrite(x, rt))
        if m == n:
            break
        n = m
    return n


def simplify_program(p: Program) -> Program:
    rt = p.reg_types()
    s = lambda e: None if e is None else simplify(e, rt)
    p = replace(
        p, w_eff=s(p.w_eff), gain=s(p.gain), cvec=s(p.cvec),
        reg_updates=tuple(simplify(u, rt) for u in p.reg_updates),
        dW=simplify(p.dW, rt), db=simplify(p.db, rt),
        struct=None if p.struct is None else replace(p.struct, mask=simplify(p.struct.mask, rt)),
    )
    # neutral slots
    if p.w_eff is not None and _is_val(p.w_eff, 0.0):
        p = replace(p, w_eff=None)
    if p.gain is not None and is_const(p.gain) and min(max(const_value(p.gain), 0.0), 4.0) == 1.0:
        p = replace(p, gain=None)
    if p.struct is not None and is_const(p.struct.mask) and const_value(p.struct.mask) <= p.struct.theta:
        p = replace(p, struct=None)
    return p


def sort_program(p: Program) -> Program:
    rt = p.reg_types()
    sig = _reg_signatures(p)
    s = lambda e: None if e is None else subst(e, lambda x: _sort_commutative(x, rt, sig))
    return replace(
        p, w_eff=s(p.w_eff), gain=s(p.gain), cvec=s(p.cvec),
        reg_updates=tuple(s(u) for u in p.reg_updates), dW=s(p.dW), db=s(p.db),
        struct=None if p.struct is None else replace(p.struct, mask=s(p.struct.mask)),
    )


def rename_registers(p: Program) -> Program:
    order: List[str] = []
    upd = {r.name: u for r, u in zip(p.regs, p.reg_updates)}

    def visit(e: Optional[Node]):
        if e is None:
            return
        for x in e.walk():
            if x.op == "reg" and x.attr not in order:
                order.append(x.attr)

    for e in (p.w_eff, p.gain, p.cvec, p.dW, p.db, None if p.struct is None else p.struct.mask):
        visit(e)
    k = 0
    while k < len(order):
        visit(upd[order[k]])
        k += 1
    for r in p.regs:          # unreachable registers (should not survive DCE)
        if r.name not in order:
            order.append(r.name)
    mapping = {old: f"r{i + 1}" for i, old in enumerate(order)}
    tmp = {old: f"t{i + 1}" for i, old in enumerate(order)}

    def ren(e: Optional[Node], m) -> Optional[Node]:
        if e is None:
            return None
        return subst(e, lambda x: Node("reg", (), m[x.attr]) if x.op == "reg" else None)

    decl = {r.name: r for r in p.regs}
    regs = tuple(replace(decl[old], name=mapping[old]) for old in order)
    ups = tuple(ren(upd[old], mapping) for old in order)
    return replace(
        p, regs=regs, reg_updates=ups,
        w_eff=ren(p.w_eff, mapping), gain=ren(p.gain, mapping), cvec=ren(p.cvec, mapping),
        dW=ren(p.dW, mapping), db=ren(p.db, mapping),
        struct=None if p.struct is None else replace(p.struct, mask=ren(p.struct.mask, mapping)),
    )


def canon(p: Program, check: bool = True) -> Program:
    if check:
        typecheck(p)
    p = inline_example_registers(p)
    p = inline_cvec(p)
    p = dead_code_elim(p)
    prev = None
    for _ in range(MAX_PASSES):
        p = simplify_program(p)
        p = inline_overwrite_registers(p)
        p = dead_code_elim(p)
        p = rename_registers(p)
        p = sort_program(p)
        p = rename_registers(p)
        cur = serialize(p)
        if cur == prev:
            break
        prev = cur
    return p


def struct_hash(p: Program) -> str:
    """sha256 of the serialized canonical program (input must already be canonical)."""
    return hashlib.sha256(serialize(p).encode()).hexdigest()


def canon_hash(p: Program) -> str:
    return struct_hash(canon(p))


def abstract_sexpr(n: Node) -> str:
    """S-expression with constants and register names abstracted (for template matching)."""
    if n.op == "const":
        return "C"
    if n.op == "tconst":
        return f"C@{n.attr[1]}"
    if n.op == "reg":
        return "R"
    if n.op == "leaf":
        return n.attr
    inner = " ".join(abstract_sexpr(c) for c in n.args)
    return f"({n.op} {inner})"


def abstract_hash(p: Program) -> str:
    """Hash of the canonical program with constants, decays and register names abstracted."""
    parts = [f"ue", "regs:" + ",".join(sorted(f"{r.type}{r.lifetime[0]}" for r in p.regs))]
    for slot, e in p.slot_exprs():
        key = "reg" if slot.startswith("reg:") else slot
        parts.append(f"{key}={abstract_sexpr(e)}")
    if p.struct is not None:
        parts.append("struct=" + p.struct.kind)
    parts.sort()
    return hashlib.sha256("|".join(parts).encode()).hexdigest()
