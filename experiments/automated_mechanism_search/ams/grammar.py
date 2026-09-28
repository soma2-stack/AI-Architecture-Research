"""Typed mechanism grammar (Claude Part AE.1), frozen by preregistration v2.

A program has the slots
    HEADER  update_every in {1, 8}
    REGS    <= 4 registers (<= 2 of type M): (name, type, lifetime, init, decay)
    FORWARD W_eff := W [+ E_M] ;  g := 1 | clip(E_O, 0, 4)
    CREDIT  cvec := E_O
    STATE   r_j <- mix(r_j, E_type(r_j), decay_j)        (right-hand sides see old values)
    PARAM   dW := E_M ; db := E_O                         (registers already updated)
    STRUCT  none | reinit(step(E_O - theta)) | freeze(step(E_O - theta))

Expressions are immutable trees of `Node`.  The slot templates ("W +", "clip",
"mix", "step(. - theta)") are not counted as AST nodes.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from typing import Dict, Iterator, List, Optional, Tuple

S, I, O, M = "S", "I", "O", "M"
ALL_TYPES = (S, I, O, M)
VEC_TYPES = (I, O)
REG_TYPES = (I, O, M)

LIFETIMES = ("EXAMPLE", "EPISODE", "RUN")
INITS = ("0", "1", "noise")
DECAYS = (0.0, 0.5, 0.9, 0.99, 0.999)
CONSTS = (-1.0, -0.5, 0.1, 0.5, 1.0, 2.0)
TOPK_KS = (1, 4, 8)
STRUCT_THETAS = (0.0, 0.1, 0.5)
STRUCT_KINDS = ("reinit", "freeze")
UPDATE_EVERY = (1, 8)

MAX_REGS = 4
MAX_M_REGS = 2
MAX_NODES = 40
MAX_DEPTH = 5
STRUCT_PERIOD = 100
REG_CLIP = 1e3
GAIN_MAX = 4.0
EPS = 1e-6

LEAF_TYPES: Dict[str, str] = {
    "a": I, "xi_I": I,
    "b": O, "z": O, "h": O, "dphi": O, "d_bp": O, "d_fa": O, "e": O, "xi_O": O, "cvec": O,
    "W": M, "W_ep0": M,
    "L": S, "dL": S, "Lbar": S, "tep": S,
}

PHASES = ("FORWARD", "CREDIT", "STATE", "PARAM", "STRUCT")
_FWD = frozenset({"a", "xi_I", "xi_O", "b", "W", "W_ep0", "tep"})
_CRD = _FWD | {"z", "h", "dphi", "d_bp", "d_fa", "e", "L", "dL", "Lbar"}
_STA = _CRD | {"cvec"}
PHASE_LEAVES = {"FORWARD": _FWD, "CREDIT": _CRD, "STATE": _STA, "PARAM": _STA, "STRUCT": _STA}

UNARY = ("neg", "abs", "sign", "square", "sqrt_s", "log_s", "exp_c", "relu", "tanh",
         "sigmoid", "step", "recip_s")
BINARY = ("add", "sub", "mul", "div_s", "max", "min")
COMMUTATIVE = ("add", "mul", "max", "min", "dot")
STRUCTURAL = {
    "outer": ((O, I), M),
    "matvec": ((M, I), O),
    "matTvec": ((M, O), I),
    "rowsum": ((M,), O),
    "colsum": ((M,), I),
    "rowscale": ((M, O), M),
    "colscale": ((M, I), M),
}
REDUCE1 = ("mean", "norm", "amax")
REDUCE2 = ("dot",)
NORMALIZERS = ("nrm", "unit")
SELECT = ("topk", "where")
ALL_OPS = UNARY + BINARY + tuple(STRUCTURAL) + REDUCE1 + REDUCE2 + NORMALIZERS + SELECT

LEARNING_SIGNAL_LEAVES = frozenset({"d_bp", "d_fa", "e", "L", "dL"})
ACTIVITY_LEAVES = frozenset({"a", "z", "h", "dphi"})


class GrammarError(Exception):
    """Raised for ill-typed or oversize programs. `code` is a short reason label."""

    def __init__(self, code: str, msg: str = ""):
        super().__init__(f"{code}: {msg}")
        self.code = code


@dataclass(frozen=True)
class Node:
    op: str
    args: Tuple["Node", ...] = ()
    attr: object = None

    # ---- convenience -------------------------------------------------------
    def walk(self) -> Iterator["Node"]:
        yield self
        for c in self.args:
            yield from c.walk()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return sexpr(self)


def leaf(name: str) -> Node:
    if name not in LEAF_TYPES:
        raise GrammarError("unknown_leaf", name)
    return Node("leaf", (), name)


def reg(name: str) -> Node:
    return Node("reg", (), name)


def const(v: float) -> Node:
    return Node("const", (), float(v))


def tconst(v: float, t: str) -> Node:
    """Typed constant (internal; produced only by the canonicalizer)."""
    return Node("tconst", (), (float(v), t))


def op(name: str, *args: Node, attr=None) -> Node:
    return Node(name, tuple(args), attr)


def is_const(n: Node) -> bool:
    return n.op in ("const", "tconst")


def const_value(n: Node) -> float:
    return n.attr if n.op == "const" else n.attr[0]


@dataclass(frozen=True)
class RegDecl:
    name: str
    type: str
    lifetime: str
    init: str
    decay: float


@dataclass(frozen=True)
class Struct:
    kind: str
    mask: Node
    theta: float


@dataclass(frozen=True)
class Program:
    update_every: int
    regs: Tuple[RegDecl, ...]
    reg_updates: Tuple[Node, ...]
    cvec: Optional[Node]
    dW: Node
    db: Node
    w_eff: Optional[Node] = None
    gain: Optional[Node] = None
    struct: Optional[Struct] = None

    def reg_types(self) -> Dict[str, str]:
        return {r.name: r.type for r in self.regs}

    def slot_exprs(self) -> List[Tuple[str, Node]]:
        """All (slot, expression) pairs, in fixed slot order."""
        out: List[Tuple[str, Node]] = []
        if self.w_eff is not None:
            out.append(("w_eff", self.w_eff))
        if self.gain is not None:
            out.append(("gain", self.gain))
        if self.cvec is not None:
            out.append(("cvec", self.cvec))
        for r, u in zip(self.regs, self.reg_updates):
            out.append((f"reg:{r.name}", u))
        out.append(("dW", self.dW))
        out.append(("db", self.db))
        if self.struct is not None:
            out.append(("struct", self.struct.mask))
        return out


SLOT_PHASE = {"w_eff": "FORWARD", "gain": "FORWARD", "cvec": "CREDIT", "dW": "PARAM",
              "db": "PARAM", "struct": "STRUCT"}


def slot_phase(slot: str) -> str:
    return "STATE" if slot.startswith("reg:") else SLOT_PHASE[slot]


# ---------------------------------------------------------------------------
# Type checking
# ---------------------------------------------------------------------------

def infer(n: Node, rtypes: Dict[str, str], phase: str, has_cvec: bool = True,
          internal: bool = False) -> Tuple[str, int, int]:
    """Return (type, depth, node_count). Leaves have depth 0."""
    o = n.op
    if o == "leaf":
        name = n.attr
        if name not in LEAF_TYPES:
            raise GrammarError("unknown_leaf", str(name))
        if name not in PHASE_LEAVES[phase]:
            raise GrammarError("phase_violation", f"{name} not available in {phase}")
        if name == "cvec" and not has_cvec:
            raise GrammarError("phase_violation", "cvec read but not defined")
        return LEAF_TYPES[name], 0, 1
    if o == "reg":
        if n.attr not in rtypes:
            raise GrammarError("unknown_register", str(n.attr))
        return rtypes[n.attr], 0, 1
    if o == "const":
        if not internal and n.attr not in CONSTS:
            raise GrammarError("bad_const", str(n.attr))
        return S, 0, 1
    if o == "tconst":
        if not internal:
            raise GrammarError("bad_const", "typed constants are internal")
        return n.attr[1], 0, 1
    kids = [infer(c, rtypes, phase, has_cvec, internal) for c in n.args]
    ts = [k[0] for k in kids]
    depth = 1 + max((k[1] for k in kids), default=0)
    count = 1 + sum(k[2] for k in kids)

    def need(cond: bool, msg: str):
        if not cond:
            raise GrammarError("ill_typed", f"{o}: {msg} (got {ts})")

    if o in UNARY:
        need(len(ts) == 1, "arity")
        t = ts[0]
    elif o in BINARY:
        need(len(ts) == 2, "arity")
        a, b = ts
        need(a == b or b == S, "binary operands must be (T,T) or (T,S)")
        t = a
    elif o in STRUCTURAL:
        sig, t = STRUCTURAL[o]
        need(tuple(ts) == sig, f"signature {sig}")
    elif o in REDUCE1:
        need(len(ts) == 1 and ts[0] in (I, O, M), "reduction of I/O/M")
        t = S
    elif o in REDUCE2:
        need(len(ts) == 2 and ts[0] == ts[1] and ts[0] in (I, O, M), "dot(X,X)")
        t = S
    elif o in NORMALIZERS:
        need(len(ts) == 1 and ts[0] in VEC_TYPES, "normalizer of I/O")
        t = ts[0]
    elif o == "topk":
        need(len(ts) == 1 and ts[0] in VEC_TYPES, "topk of I/O")
        if n.attr not in TOPK_KS:
            raise GrammarError("bad_const", f"topk k={n.attr}")
        t = ts[0]
    elif o == "where":
        need(len(ts) == 3 and ts[0] in VEC_TYPES, "where(x>0,y,w) with x in I/O")
        need(ts[1] in (ts[0], S) and ts[2] in (ts[0], S), "where branches T or S")
        t = ts[0]
    else:
        raise GrammarError("unknown_op", o)
    return t, depth, count


def typecheck(p: Program, internal: bool = False, limits: bool = True) -> Dict[str, object]:
    """Validate a program against AE.1.  Returns size information.

    `internal=True` admits canonicalizer-produced typed constants and folded
    constants outside the constant set; generated programs are checked with
    internal=False.
    """
    if p.update_every not in UPDATE_EVERY:
        raise GrammarError("bad_header", f"update_every={p.update_every}")
    if limits and len(p.regs) > MAX_REGS:
        raise GrammarError("oversize", f"{len(p.regs)} registers")
    if sum(r.type == M for r in p.regs) > MAX_M_REGS:
        raise GrammarError("oversize", "more than 2 M registers")
    names = [r.name for r in p.regs]
    if len(set(names)) != len(names):
        raise GrammarError("bad_reg", "duplicate register names")
    if len(p.reg_updates) != len(p.regs):
        raise GrammarError("bad_reg", "each register needs exactly one update")
    for r in p.regs:
        if not re.fullmatch(r"r\d+", r.name):
            raise GrammarError("bad_reg", r.name)
        if r.type not in REG_TYPES:
            raise GrammarError("bad_reg", f"type {r.type}")
        if r.lifetime not in LIFETIMES:
            raise GrammarError("bad_reg", f"lifetime {r.lifetime}")
        if r.init not in INITS:
            raise GrammarError("bad_reg", f"init {r.init}")
        if r.decay not in DECAYS:
            raise GrammarError("bad_reg", f"decay {r.decay}")
    if p.struct is not None:
        if p.struct.kind not in STRUCT_KINDS:
            raise GrammarError("bad_struct", p.struct.kind)
        if p.struct.theta not in STRUCT_THETAS:
            raise GrammarError("bad_struct", f"theta {p.struct.theta}")
    rt = p.reg_types()
    has_cvec = p.cvec is not None
    expected = {"w_eff": M, "gain": O, "cvec": O, "dW": M, "db": O, "struct": O}
    total = 0
    depths = {}
    for slot, e in p.slot_exprs():
        t, d, c = infer(e, rt, slot_phase(slot), has_cvec, internal)
        want = rt[slot[4:]] if slot.startswith("reg:") else expected[slot]
        if t != want:
            raise GrammarError("ill_typed", f"slot {slot} has type {t}, needs {want}")
        if limits and d > MAX_DEPTH:
            raise GrammarError("oversize", f"slot {slot} depth {d}")
        total += c
        depths[slot] = d
    if limits and total > MAX_NODES:
        raise GrammarError("oversize", f"{total} nodes")
    return {"nodes": total, "depths": depths}


def node_types(n: Node, rtypes: Dict[str, str]) -> Dict[Node, str]:
    """Type of every subtree (phase checks skipped)."""
    out: Dict[Node, str] = {}

    def go(x: Node) -> str:
        if x in out:
            return out[x]
        for c in x.args:
            go(c)
        t = infer(x, rtypes, "PARAM", True, True)[0] if x.op != "leaf" else LEAF_TYPES[x.attr]
        out[x] = t
        return t

    go(n)
    return out


def type_of(n: Node, rtypes: Dict[str, str]) -> str:
    if n.op == "leaf":
        return LEAF_TYPES[n.attr]
    return infer(n, rtypes, "PARAM", True, True)[0]


def reads(n: Node) -> set:
    """Set of leaf names and register names read by an expression."""
    s = set()
    for x in n.walk():
        if x.op == "leaf":
            s.add(x.attr)
        elif x.op == "reg":
            s.add(x.attr)
    return s


# ---------------------------------------------------------------------------
# S-expression serialization / parsing
# ---------------------------------------------------------------------------

def fmt_const(v: float) -> str:
    v = float(v)
    if v == 0:
        v = 0.0  # normalize -0.0
    return format(v, ".12g")


def sexpr(n: Node) -> str:
    if n.op == "leaf" or n.op == "reg":
        return n.attr
    if n.op == "const":
        return fmt_const(n.attr)
    if n.op == "tconst":
        return f"{fmt_const(n.attr[0])}@{n.attr[1]}"
    inner = " ".join(sexpr(c) for c in n.args)
    if n.op == "topk":
        return f"(topk {inner} {n.attr})"
    return f"({n.op} {inner})"


_TOK = re.compile(r"\(|\)|[^\s()]+")


def parse(s: str) -> Node:
    toks = _TOK.findall(s)
    pos = 0

    def atom(t: str) -> Node:
        if t in LEAF_TYPES:
            return Node("leaf", (), t)
        if re.fullmatch(r"r\d+", t):
            return Node("reg", (), t)
        if "@" in t:
            v, ty = t.split("@")
            return tconst(float(v), ty)
        try:
            return const(float(t))
        except ValueError:
            raise GrammarError("parse", f"bad atom {t!r}")

    def expr() -> Node:
        nonlocal pos
        t = toks[pos]
        pos += 1
        if t != "(":
            return atom(t)
        name = toks[pos]
        pos += 1
        args = []
        attr = None
        while toks[pos] != ")":
            args.append(expr())
        pos += 1
        if name == "topk":
            if len(args) != 2 or args[1].op != "const":
                raise GrammarError("parse", "topk needs (topk x k)")
            attr = int(args[1].attr)
            args = args[:1]
        if name not in ALL_OPS:
            raise GrammarError("unknown_op", name)
        return Node(name, tuple(args), attr)

    n = expr()
    if pos != len(toks):
        raise GrammarError("parse", "trailing tokens")
    return n


def program_to_dict(p: Program) -> dict:
    return {
        "update_every": p.update_every,
        "regs": [
            {"name": r.name, "type": r.type, "lifetime": r.lifetime, "init": r.init,
             "decay": r.decay, "update": sexpr(u)}
            for r, u in zip(p.regs, p.reg_updates)
        ],
        "w_eff": None if p.w_eff is None else sexpr(p.w_eff),
        "gain": None if p.gain is None else sexpr(p.gain),
        "cvec": None if p.cvec is None else sexpr(p.cvec),
        "dW": sexpr(p.dW),
        "db": sexpr(p.db),
        "struct": None if p.struct is None else
        {"kind": p.struct.kind, "theta": p.struct.theta, "mask": sexpr(p.struct.mask)},
    }


def program_from_dict(d: dict) -> Program:
    regs = tuple(RegDecl(r["name"], r["type"], r["lifetime"], str(r["init"]), float(r["decay"]))
                 for r in d["regs"])
    ups = tuple(parse(r["update"]) for r in d["regs"])
    st = d.get("struct")
    return Program(
        update_every=int(d["update_every"]),
        regs=regs,
        reg_updates=ups,
        cvec=None if d.get("cvec") is None else parse(d["cvec"]),
        dW=parse(d["dW"]),
        db=parse(d["db"]),
        w_eff=None if d.get("w_eff") is None else parse(d["w_eff"]),
        gain=None if d.get("gain") is None else parse(d["gain"]),
        struct=None if st is None else Struct(st["kind"], parse(st["mask"]), float(st["theta"])),
    )


def serialize(p: Program) -> str:
    return json.dumps(program_to_dict(p), sort_keys=True, separators=(",", ":"))


def make_program(dW: str, db: str, cvec: Optional[str] = None, regs=(), w_eff: Optional[str] = None,
                 gain: Optional[str] = None, struct=None, update_every: int = 1) -> Program:
    """Build a program from s-expression strings.

    regs: iterable of (name, type, lifetime, init, decay, update_sexpr).
    struct: None or (kind, mask_sexpr, theta).
    """
    rd = tuple(RegDecl(n, t, lt, str(ini), float(dec)) for n, t, lt, ini, dec, _ in regs)
    ru = tuple(parse(u) for *_, u in regs)
    return Program(
        update_every=update_every,
        regs=rd,
        reg_updates=ru,
        cvec=None if cvec is None else parse(cvec),
        dW=parse(dW),
        db=parse(db),
        w_eff=None if w_eff is None else parse(w_eff),
        gain=None if gain is None else parse(gain),
        struct=None if struct is None else Struct(struct[0], parse(struct[1]), float(struct[2])),
    )


def pretty(p: Program) -> str:
    lines = [f"HEADER  update_every={p.update_every}"]
    for r, u in zip(p.regs, p.reg_updates):
        lines.append(f"REG     {r.name}: {r.type} {r.lifetime} init={r.init} decay={r.decay}"
                     f"  <- {sexpr(u)}")
    lines.append(f"FORWARD W_eff := W" + ("" if p.w_eff is None else f" + {sexpr(p.w_eff)}")
                 + " ; g := " + ("1" if p.gain is None else f"clip({sexpr(p.gain)},0,4)"))
    lines.append(f"CREDIT  cvec := {'-' if p.cvec is None else sexpr(p.cvec)}")
    lines.append(f"PARAM   dW := {sexpr(p.dW)} ; db := {sexpr(p.db)}")
    lines.append("STRUCT  " + ("none" if p.struct is None else
                                f"{p.struct.kind}(step({sexpr(p.struct.mask)} - {p.struct.theta}))"))
    return "\n".join(lines)


def with_(p: Program, **kw) -> Program:
    return replace(p, **kw)
