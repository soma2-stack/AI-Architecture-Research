"""Known-family reference library (AE.2.4 R1-R24 + expressible AE.10 extras), disguised
variants, the family matcher and the non-family residual decomposition K(P) (AE.2.5).

Matching (AE.2.4 "two-layer rediscovery filter"):
  * syntactic: canonical struct hash equal to a reference, or abstract template hash equal
    (constants, decays, register names and update timing abstracted);
  * behavioural: cos(beta(P), beta(R)) >= 0.99 for some reference R (full AE.2.2 vector,
    including register-state changes), maximised over injective register-to-probe-slot
    assignments so that canonical register order cannot hide a match.  Inert extra registers
    (never reaching FORWARD/PARAM/STRUCT) are removed by dead-code elimination first;
  * composite: K(P) == P (every term of P is a known-family term) -> full match.
"""
from __future__ import annotations

import random
from dataclasses import replace
from typing import Dict, List, Optional, Tuple

import numpy as np

from .canon import abstract_sexpr, abstract_hash, canon, replace_reg, simplify, struct_hash, subst
from .grammar import M, O, S, Node, Program, RegDecl, Struct, const, make_program, parse, tconst, typecheck, type_of
from .probes import FAMILY_COS, ProbeRunner, cos

SGD_W = "(neg (outer d_bp a))"
SGD_B = "(neg d_bp)"


def _R(dW, db, **kw) -> Program:
    return make_program(dW, db, **kw)


REFERENCES: Dict[str, Program] = {
    "R1_SGD": _R(SGD_W, SGD_B),
    "R2_signSGD": _R("(neg (sign (outer d_bp a)))", "(neg (sign d_bp))"),
    "R3_momentum": _R("(neg r1)", "(neg r2)", regs=[("r1", M, "RUN", "0", 0.9, "(outer d_bp a)"),
                                                   ("r2", O, "RUN", "0", 0.9, "d_bp")]),
    "R4_rmsprop_adam": _R("(neg (div_s r1 (sqrt_s r2)))", SGD_B,
                          regs=[("r1", M, "RUN", "0", 0.9, "(outer d_bp a)"),
                                ("r2", M, "RUN", "0", 0.999, "(square (outer d_bp a))")]),
    "R5_lion": _R("(neg (sign (add r1 (outer d_bp a))))", "(neg (sign d_bp))",
                  regs=[("r1", M, "RUN", "0", 0.99, "(outer d_bp a)")]),
    "R6_EG_mirror": _R("(neg (mul W (outer d_bp a)))", SGD_B),
    "R7_weight_decay": _R("(sub (neg (outer d_bp a)) (mul W 0.1))", SGD_B),
    "R8_DFA": _R("(neg (outer (mul d_fa dphi) a))", "(neg (mul d_fa dphi))"),
    "R9_hebbian": _R("(outer h a)", "h"),
    "R10_oja": _R("(sub (outer h a) (rowscale W (square h)))", "h"),
    "R11_BCM": _R("(outer (mul h (sub h r1)) a)", "(mul h (sub h r1))",
                  regs=[("r1", O, "RUN", "0", 0.99, "(square h)")]),
    "R12_fast_weights": _R("(neg (outer cvec a))", "(neg cvec)", cvec="d_bp", w_eff="r1",
                           regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]),
    "R13_fast_slow": _R(SGD_W, SGD_B, w_eff="(add r1 r2)",
                        regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)"),
                              ("r2", M, "RUN", "0", 0.999, "(outer h a)")]),
    "R14_diff_plasticity": _R(SGD_W, SGD_B, w_eff="(mul r2 r1)",
                              regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)"),
                                    ("r2", M, "RUN", "0", 0.999, "(neg (mul (outer d_bp a) r1))")]),
    "R15_three_factor": _R("(mul r1 (sub Lbar L))", "(mul h (sub Lbar L))",
                           regs=[("r1", M, "RUN", "0", 0.9, "(outer h a)")]),
    "R16_node_perturbation": _R("(neg (mul (outer xi_O a) (sub L Lbar)))", "(neg (mul xi_O (sub L Lbar)))",
                                w_eff="(outer xi_O a)"),
    "R17_EWC_SI": _R("(sub (neg (outer d_bp a)) (mul (mul r1 (sub W W_ep0)) 0.5))", SGD_B,
                     regs=[("r1", M, "RUN", "0", 0.99, "(square (outer d_bp a))")]),
    "R18_kWTA_sparse_update": _R("(neg (rowscale (outer d_bp a) (topk h 4)))", "(neg (mul d_bp (topk h 4)))"),
    "R19_forward_hard_routing": _R(SGD_W, SGD_B, gain="(topk (matvec W a) 8)"),
    "R20_homeostatic_gain": _R(SGD_W, SGD_B, gain="(recip_s r1)",
                               regs=[("r1", O, "RUN", "1", 0.99, "(abs h)")]),
    "R21_continual_backprop": _R(SGD_W, SGD_B, struct=("reinit", "(add (neg r1) 0.1)", 0.0),
                                 regs=[("r1", O, "RUN", "0", 0.99, "(abs h)")]),
    "R22_forward_forward": _R("(outer cvec a)", "cvec", cvec="(mul h (sub 2 (norm h)))"),
    "R23_synthetic_gradient": _R("(neg (outer cvec a))", "(neg cvec)", cvec="r1",
                                 regs=[("r1", O, "RUN", "0", 0.9, "d_bp")]),
    "R24_loss_shaping": _R("(neg (outer cvec a))", "(neg cvec)", cvec="(mul d_bp (sqrt_s L))"),
    # AE.10 extras expressible in the grammar
    "X1_adagrad_approx": _R("(neg (div_s (outer d_bp a) (sqrt_s r1)))", SGD_B,
                            regs=[("r1", M, "RUN", "0", 0.999, "(square (outer d_bp a))")]),
    "X2_anti_hebbian": _R("(neg (outer h a))", "(neg h)"),
    "X3_eprop_like": _R("(neg (rowscale r1 d_fa))", "(neg d_fa)",
                        regs=[("r1", M, "RUN", "0", 0.9, "(outer dphi a)")]),
    "X4_neuromodulated_hebbian": _R("(mul (outer h a) (sub Lbar L))", "(mul h (sub Lbar L))"),
    "X5_adamw_like": _R("(sub (neg (div_s r1 (sqrt_s r2))) (mul W 0.1))", SGD_B,
                        regs=[("r1", M, "RUN", "0", 0.9, "(outer d_bp a)"),
                              ("r2", M, "RUN", "0", 0.999, "(square (outer d_bp a))")]),
    "X6_nesterov_like": _R("(neg (add r1 (outer d_bp a)))", SGD_B,
                           regs=[("r1", M, "RUN", "0", 0.9, "(outer d_bp a)")]),
    "X7_weight_perturbation": _R("(neg (mul (outer xi_O xi_I) (sub L Lbar)))", "(neg (mul xi_O (sub L Lbar)))",
                                 w_eff="(outer xi_O xi_I)"),
}


# ---------------------------------------------------------------------------
# Disguised variants (Stage-0 test AE.6 item 5)
# ---------------------------------------------------------------------------

def _swap_commutative(n: Node) -> Node:
    from .grammar import COMMUTATIVE
    from .grammar import type_of as _t

    def fn(x: Node):
        if x.op in COMMUTATIVE and len(x.args) == 2:
            return Node(x.op, (x.args[1], x.args[0]), x.attr)
        return None
    return subst(n, fn)


def disguise_reorder(p: Program) -> Program:
    """Swap operands of commutative ops where typing allows (same-type operands)."""
    rt = p.reg_types()
    from .grammar import COMMUTATIVE

    def fn(x: Node):
        if x.op in COMMUTATIVE and len(x.args) == 2 and type_of(x.args[0], rt) == type_of(x.args[1], rt):
            return Node(x.op, (x.args[1], x.args[0]), x.attr)
        return None
    s = lambda e: None if e is None else subst(e, fn)
    return replace(p, dW=s(p.dW), db=s(p.db), cvec=s(p.cvec), w_eff=s(p.w_eff), gain=s(p.gain),
                   reg_updates=tuple(s(u) for u in p.reg_updates))


def disguise_rescale(p: Program) -> Program:
    """Multiply the parameter update by a constant (absorbed by the tuned learning rate)."""
    return replace(p, dW=Node("mul", (p.dW, const(2.0))), db=Node("mul", (p.db, const(2.0))))


def disguise_inert_register(p: Program) -> Program:
    """Add an extra register that is updated but never read."""
    names = {r.name for r in p.regs}
    if len(p.regs) >= 4:
        return p
    nm = next(f"r{k}" for k in range(1, 9) if f"r{k}" not in names)
    rd = RegDecl(nm, O, "RUN", "0", 0.9)
    return replace(p, regs=p.regs + (rd,), reg_updates=p.reg_updates + (parse("h"),))


def disguise_rename(p: Program) -> Program:
    """Rename registers in reverse order and permute declarations."""
    if len(p.regs) < 2:
        return p
    names = [r.name for r in p.regs]
    mapping = dict(zip(names, ["r9", "r8", "r7", "r6"][:len(names)]))

    def ren(e):
        if e is None:
            return None
        return subst(e, lambda x: Node("reg", (), mapping[x.attr]) if x.op == "reg" else None)
    regs = tuple(replace(r, name=mapping[r.name]) for r in p.regs)[::-1]
    ups = tuple(ren(u) for u in p.reg_updates)[::-1]
    return replace(p, regs=regs, reg_updates=ups, dW=ren(p.dW), db=ren(p.db), cvec=ren(p.cvec),
                   w_eff=ren(p.w_eff), gain=ren(p.gain),
                   struct=None if p.struct is None else replace(p.struct, mask=ren(p.struct.mask)))


DISGUISES = {"reorder": disguise_reorder, "rescale": disguise_rescale,
             "inert_register": disguise_inert_register, "rename": disguise_rename}


# ---------------------------------------------------------------------------
# additive-term decomposition
# ---------------------------------------------------------------------------

def terms(e: Node, rt) -> List[Node]:
    """Signed additive terms at the top level (sign and scalar-constant factors stripped)."""
    if e.op == "add":
        return terms(e.args[0], rt) + terms(e.args[1], rt)
    if e.op == "sub":
        return terms(e.args[0], rt) + terms(e.args[1], rt)
    if e.op == "neg":
        return terms(e.args[0], rt)
    if e.op == "mul" and e.args[1].op == "const":
        return terms(e.args[0], rt)
    if e.op == "mul" and e.args[0].op in ("const", "tconst"):
        return terms(e.args[1], rt)
    return [e]


def strip_gates(e: Node, rt) -> Node:
    """Replace topk/where gates by neutral 1 (where -> its positive branch)."""
    def fn(x: Node):
        if x.op == "topk":
            return tconst(1.0, type_of(x, rt))
        if x.op == "where":
            return x.args[1]
        return None
    return simplify(subst(e, fn), rt)


class FamilyLibrary:
    def __init__(self, runner: Optional[ProbeRunner] = None, refs: Optional[Dict[str, Program]] = None):
        self.runner = runner or ProbeRunner()
        self.raw = dict(REFERENCES if refs is None else refs)
        self.canon: Dict[str, Program] = {k: canon(v) for k, v in self.raw.items()}
        self.hash = {struct_hash(p): k for k, p in self.canon.items()}
        self.abs = {}
        for k, p in self.canon.items():
            self.abs.setdefault(abstract_hash(p), k)
        self.bref = {k: self.runner.beta(p) for k, p in self.canon.items()}
        self._build_templates()

    def _build_templates(self):
        self.t_dW, self.t_db, self.t_weff, self.t_gain, self.t_reg, self.t_mask = (set() for _ in range(6))
        from .fingerprint import expand
        for p in self.canon.values():
            rt = p.reg_types()
            for t in terms(expand(p, p.dW), rt):
                self.t_dW.add(abstract_sexpr(t))
            for t in terms(expand(p, p.db), rt):
                self.t_db.add(abstract_sexpr(t))
            if p.w_eff is not None:
                for t in terms(p.w_eff, rt):
                    self.t_weff.add(abstract_sexpr(t))
            if p.gain is not None:
                self.t_gain.add(abstract_sexpr(p.gain))
            for u in p.reg_updates:
                self.t_reg.add(abstract_sexpr(expand(p, u)))
            if p.struct is not None:
                self.t_mask.add(abstract_sexpr(p.struct.mask))

    # ------------------------------------------------------------------ matching
    def match(self, p: Program, b_all: Optional[List[np.ndarray]] = None) -> Optional[Dict]:
        """Full-family match of a canonical program, or None."""
        h = struct_hash(p)
        if h in self.hash:
            return {"family": self.hash[h], "how": "syntactic", "sim": 1.0}
        ah = abstract_hash(p)
        if ah in self.abs:
            return {"family": self.abs[ah], "how": "template", "sim": 1.0}
        best = self.nearest(p, b_all)
        if best["sim"] >= FAMILY_COS:
            return {"family": best["family"], "how": "behavioral", "sim": best["sim"]}
        return None

    def nearest(self, p: Program, b_all: Optional[List[np.ndarray]] = None) -> Dict:
        if b_all is None:
            b_all = self.runner.beta_all(p)
        best, bestk = -2.0, None
        for k, rb in self.bref.items():
            s = max(cos(b, rb) for b in b_all)
            if s > best:
                best, bestk = s, k
        return {"family": bestk, "sim": float(best)}

    # ------------------------------------------------------------------ K(P)
    def decompose(self, p: Program) -> Tuple[Program, Dict]:
        """Nearest known-family decomposition K(P): keep known-family terms, gates that wrap
        family terms are neutralised, non-family terms/registers/couplings are neutralised.
        Returns (canonical K(P), info)."""
        from .fingerprint import expand
        rt = p.reg_types()
        info = {"dropped_terms": [], "stripped_gates": [], "inert_registers": [], "dropped_slots": []}

        def keep_terms(e: Optional[Node], tmpl: set, slot: str, zero_t: str) -> Optional[Node]:
            """Term analysis on the cvec-expanded form; kept terms stay in their original
            (unexpanded) form so CREDIT-phase register semantics are preserved."""
            if e is None:
                return None
            repl_map = {}
            n_kept = 0
            for t in terms(e, rt):
                sig = abstract_sexpr(expand(p, t))
                if sig in tmpl:
                    n_kept += 1
                    continue
                st = strip_gates(t, rt)
                if st != t and abstract_sexpr(expand(p, st)) in tmpl:
                    repl_map[t] = st
                    n_kept += 1
                    info["stripped_gates"].append(slot)
                    continue
                info["dropped_terms"].append((slot, sig))
                tt = type_of(t, rt)
                repl_map[t] = const(0.0) if tt == S else tconst(0.0, tt)
            if n_kept == 0:
                return None
            out = subst(e, lambda x: repl_map.get(x))
            return simplify(out, rt)

        dW = keep_terms(p.dW, self.t_dW, "dW", M)
        db = keep_terms(p.db, self.t_db, "db", O)
        w_eff = keep_terms(p.w_eff, self.t_weff, "w_eff", M)
        gain = p.gain if (p.gain is not None and abstract_sexpr(p.gain) in self.t_gain) else None
        if p.gain is not None and gain is None:
            info["dropped_slots"].append("gain")
        st = p.struct if (p.struct is not None and abstract_sexpr(p.struct.mask) in self.t_mask) else None
        if p.struct is not None and st is None:
            info["dropped_slots"].append("struct")
        q = replace(p, dW=dW if dW is not None else tconst(0.0, M),
                    db=db if db is not None else tconst(0.0, O), w_eff=w_eff, gain=gain, struct=st,
                    cvec=None if p.cvec is None else p.cvec)
        # registers whose update is not a family template become inert (held at init)
        for rd, u in zip(p.regs, p.reg_updates):
            if abstract_sexpr(expand(p, u)) not in self.t_reg:
                info["inert_registers"].append(rd.name)
                init = 0.0 if rd.init == "noise" else float(rd.init)
                idx = [r.name for r in q.regs].index(rd.name)
                repl = tconst(init, rd.type)
                q = replace(q, regs=tuple(r for r in q.regs if r.name != rd.name),
                            reg_updates=tuple(replace_reg(x, rd.name, repl)
                                              for k, x in enumerate(q.reg_updates) if k != idx),
                            dW=replace_reg(q.dW, rd.name, repl), db=replace_reg(q.db, rd.name, repl),
                            w_eff=None if q.w_eff is None else replace_reg(q.w_eff, rd.name, repl),
                            gain=None if q.gain is None else replace_reg(q.gain, rd.name, repl),
                            cvec=None if q.cvec is None else replace_reg(q.cvec, rd.name, repl),
                            struct=None if q.struct is None else replace(q.struct, mask=replace_reg(q.struct.mask, rd.name, repl)))
        typecheck(q, internal=True, limits=False)
        k = canon(q, check=False)
        return k, info

    def has_residual(self, p: Program) -> bool:
        k, _ = self.decompose(p)
        return struct_hash(k) != struct_hash(p)
