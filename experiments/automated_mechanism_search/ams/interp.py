"""Vectorized interpreter for grammar expressions.

Array layout: every value carries leading *batch* dimensions (e.g. (R, B) for
R runs x B examples, or (R, 1) for per-run quantities) followed by trailing
type dimensions:
    S -> ()        I -> (n_in,)        O -> (n_out,)        M -> (n_out, n_in)
Scalars (S) are broadcast to T by appending singleton axes.

All division / log / sqrt / exp forms are the safe forms of AE.1.4.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np

from .grammar import (BINARY, EPS, M, NORMALIZERS, O, REDUCE1, S, STRUCTURAL, UNARY, I, Node,
                      type_of)

TRAIL = {S: 0, I: 1, O: 1, M: 2}


def _x(s: np.ndarray, t: str) -> np.ndarray:
    """Broadcast a scalar-typed array to trailing type t."""
    k = TRAIL[t]
    return s.reshape(s.shape + (1,) * k) if k else s


def _sign(x):
    return np.sign(x)


UNARY_FN: Dict[str, Callable] = {
    "neg": np.negative,
    "abs": np.abs,
    "sign": _sign,
    "square": np.square,
    "sqrt_s": lambda x: np.sign(x) * np.sqrt(np.abs(x) + EPS),
    "log_s": lambda x: np.sign(x) * np.log1p(np.abs(x)),
    "exp_c": lambda x: np.exp(np.clip(x, -10.0, 10.0)),
    "relu": lambda x: np.maximum(x, 0),
    "tanh": np.tanh,
    "sigmoid": lambda x: 0.5 * (1.0 + np.tanh(0.5 * x)),
    "step": lambda x: (x > 0).astype(x.dtype),
    "recip_s": lambda x: np.sign(x) / (np.abs(x) + EPS),
}


def _recip(y):
    return np.sign(y) / (np.abs(y) + EPS)


BINARY_FN: Dict[str, Callable] = {
    "add": np.add,
    "sub": np.subtract,
    "mul": np.multiply,
    "div_s": lambda x, y: x * _recip(y),
    "max": np.maximum,
    "min": np.minimum,
}


def _axes(t: str):
    return (-1,) if t in (I, O) else (-2, -1)


def topk_mask(x: np.ndarray, k: int) -> np.ndarray:
    n = x.shape[-1]
    if k >= n:
        return np.ones_like(x)
    idx = np.argpartition(-x, k - 1, axis=-1)[..., :k]
    m = np.zeros_like(x)
    np.put_along_axis(m, idx, 1.0, axis=-1)
    return m


def nrm(x: np.ndarray) -> np.ndarray:
    mu = x.mean(axis=-1, keepdims=True)
    sd = x.std(axis=-1, keepdims=True)
    return (x - mu) / (sd + EPS)


def unit(x: np.ndarray) -> np.ndarray:
    return x / (np.sqrt(np.sum(x * x, axis=-1, keepdims=True)) + EPS)


class Compiled:
    """A list of expressions compiled into a flat, hash-consed op list."""

    def __init__(self, exprs: Sequence[Node], rtypes: Dict[str, str]):
        self.rtypes = dict(rtypes)
        self.steps: List[Tuple[Node, Tuple[int, ...], str]] = []
        self.index: Dict[Node, int] = {}
        self.outputs = [self._visit(e) for e in exprs]
        self.out_types = [self.steps[i][2] for i in self.outputs]

    def _visit(self, n: Node) -> int:
        if n in self.index:
            return self.index[n]
        ai = tuple(self._visit(c) for c in n.args)
        t = type_of(n, self.rtypes)
        self.index[n] = len(self.steps)
        self.steps.append((n, ai, t))
        return self.index[n]

    def __call__(self, env: Dict[str, np.ndarray], nb: int, dims: Dict[str, int],
                 dtype=np.float32) -> List[np.ndarray]:
        vals: List[np.ndarray] = [None] * len(self.steps)  # type: ignore
        types = [s[2] for s in self.steps]
        for i, (n, ai, t) in enumerate(self.steps):
            o = n.op
            if o == "leaf":
                v = env[n.attr]
            elif o == "reg":
                v = env["reg:" + n.attr]
            elif o == "const":
                v = np.full((1,) * nb, n.attr, dtype=dtype)
            elif o == "tconst":
                val, ty = n.attr
                trail = () if ty == S else ((dims[ty],) if ty in (I, O) else (dims[O], dims[I]))
                v = np.full((1,) * nb + trail, val, dtype=dtype)
            else:
                args = [vals[j] for j in ai]
                ats = [types[j] for j in ai]
                if o in UNARY:
                    v = UNARY_FN[o](args[0])
                elif o in BINARY:
                    x, y = args
                    if ats[1] == S and ats[0] != S:
                        y = _x(y, ats[0])
                    v = BINARY_FN[o](x, y)
                elif o in STRUCTURAL:
                    if o == "outer":
                        v = args[0][..., :, None] * args[1][..., None, :]
                    elif o == "matvec":
                        v = np.matmul(args[0], args[1][..., None])[..., 0]
                    elif o == "matTvec":
                        v = np.matmul(np.swapaxes(args[0], -1, -2), args[1][..., None])[..., 0]
                    elif o == "rowsum":
                        v = args[0].sum(axis=-1)
                    elif o == "colsum":
                        v = args[0].sum(axis=-2)
                    elif o == "rowscale":
                        v = args[0] * args[1][..., :, None]
                    else:  # colscale
                        v = args[0] * args[1][..., None, :]
                elif o in REDUCE1:
                    ax = _axes(ats[0])
                    x = args[0]
                    if o == "mean":
                        v = x.mean(axis=ax)
                    elif o == "norm":
                        v = np.sqrt(np.sum(x * x, axis=ax))
                    else:  # amax: max absolute value (IMPLEMENTATION_DECISIONS D-OPS-1)
                        v = np.abs(x).max(axis=ax)
                elif o == "dot":
                    x, y = np.broadcast_arrays(args[0], args[1])
                    v = np.sum(x * y, axis=_axes(ats[0]))
                elif o in NORMALIZERS:
                    v = nrm(args[0]) if o == "nrm" else unit(args[0])
                elif o == "topk":
                    v = topk_mask(args[0], n.attr)
                elif o == "where":
                    x, y, w = args
                    if ats[1] == S:
                        y = _x(y, t)
                    if ats[2] == S:
                        w = _x(w, t)
                    v = np.where(x > 0, y, w)
                else:  # pragma: no cover
                    raise ValueError(o)
                if v.dtype != dtype:
                    v = v.astype(dtype)
            vals[i] = v
        return [vals[i] for i in self.outputs]


def eval_expr(e: Node, env: Dict[str, np.ndarray], rtypes: Dict[str, str], nb: int,
              dims: Dict[str, int], dtype=np.float32) -> np.ndarray:
    return Compiled([e], rtypes)(env, nb, dims, dtype)[0]


# FLOP cost model per op (per element of the output unless stated) ---------------------
def op_flops(n: Node, ai_types: Sequence[str], t: str, dims: Dict[str, int]) -> int:
    size = {S: 1, I: dims[I], O: dims[O], M: dims[O] * dims[I]}
    o = n.op
    if o in ("leaf", "reg", "const", "tconst"):
        return 0
    if o in UNARY or o in BINARY:
        return size[t]
    if o == "outer" or o in ("rowscale", "colscale"):
        return size[M]
    if o in ("matvec", "matTvec"):
        return 2 * size[M]
    if o in ("rowsum", "colsum"):
        return size[M]
    if o in ("mean", "amax"):
        return size[ai_types[0]]
    if o in ("norm", "dot"):
        return 2 * size[ai_types[0]]
    if o == "nrm":
        return 5 * size[t]
    if o == "unit":
        return 3 * size[t]
    if o == "topk":
        n_ = size[t]
        return n_ * max(1, int(np.ceil(np.log2(max(n_, 2)))))
    if o == "where":
        return size[t]
    raise ValueError(o)


def compiled_flops(c: Compiled, dims: Dict[str, int]) -> int:
    total = 0
    for n, ai, t in c.steps:
        total += op_flops(n, [c.steps[j][2] for j in ai], t, dims)
    return total
