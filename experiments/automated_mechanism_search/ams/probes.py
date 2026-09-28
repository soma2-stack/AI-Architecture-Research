"""Level-B behavioural equivalence on the frozen v2 probe corpus.

The serialized corpus config/behavioral_probes_v2.json is authoritative (prereg v2 sec. 4).
It is verified by its git blob SHA before any behavioural deduplication and is never
regenerated as a substitute.

Behaviour vector (AE.2.2): for each of the 16 probes, one FORWARD + one full update of a
single layer, collecting (h, unit(vec dW), unit(db), unit(dr_j) for register slots 1..4),
concatenated in probe order.  Duplicates: round(beta, 6) identical or cos >= 0.999.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import PROBE_BLOB_SHA
from .grammar import GAIN_MAX, I, M, O, REG_CLIP, S, Program, reads
from .interp import Compiled

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_PATH = os.path.join(HERE, "config", "behavioral_probes_v2.json")
DUP_COS = 0.999
FAMILY_COS = 0.99
N_PROBES = 16
PI, PO = 8, 6
SLOT_PAD = PO * PI
VEC_FIELDS = ("W", "b", "a", "d_bp", "d_fa", "e", "xi_I", "xi_O")
SCALAR_FIELDS = ("L", "dL", "Lbar", "tep")


class ProbeCorpusError(Exception):
    pass


def git_blob_sha(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_corpus(path: str = CORPUS_PATH, expected_sha: str = PROBE_BLOB_SHA) -> List[Dict]:
    """Load and verify the frozen corpus.  Raises ProbeCorpusError on any mismatch."""
    if not os.path.exists(path):
        raise ProbeCorpusError(f"probe corpus missing: {path}")
    sha = git_blob_sha(path)
    if sha != expected_sha:
        raise ProbeCorpusError(f"probe corpus blob {sha} != frozen {expected_sha}")
    with open(path) as f:
        d = json.load(f)
    if d.get("schema_version") != "AMS-BEHAVIOR-PROBES-V2":
        raise ProbeCorpusError("schema_version mismatch")
    if d.get("probe_dims") != {"I": PI, "O": PO}:
        raise ProbeCorpusError("probe_dims mismatch")
    probes = d["probes"]
    if len(probes) != N_PROBES:
        raise ProbeCorpusError(f"{len(probes)} probes, expected {N_PROBES}")
    out = []
    for k, p in enumerate(probes):
        if p["id"] != k:
            raise ProbeCorpusError("probe ids out of order")
        q = {f: np.asarray(p[f], np.float64) for f in VEC_FIELDS}
        for f in SCALAR_FIELDS:
            q[f] = np.float64(p[f])
        shapes = {"W": (PO, PI), "b": (PO,), "a": (PI,), "d_bp": (PO,), "d_fa": (PO,), "e": (PO,),
                  "xi_I": (PI,), "xi_O": (PO,)}
        for f, sh in shapes.items():
            if q[f].shape != sh:
                raise ProbeCorpusError(f"probe {k} field {f} shape {q[f].shape}")
        bank = p["register_bank"]
        if [s["slot"] for s in bank] != [1, 2, 3, 4]:
            raise ProbeCorpusError(f"probe {k} register bank slots")
        q["bank"] = [{I: np.asarray(s["I"], np.float64), O: np.asarray(s["O"], np.float64),
                      M: np.asarray(s["M"], np.float64)} for s in bank]
        for s in q["bank"]:
            if s[I].shape != (PI,) or s[O].shape != (PO,) or s[M].shape != (PO, PI):
                raise ProbeCorpusError(f"probe {k} register bank shapes")
        out.append(q)
    # W_ep0 is not a corpus field; frozen derivation: W of the next probe (D-PROBE-2)
    for k, q in enumerate(out):
        q["W_ep0"] = out[(k + 1) % N_PROBES]["W"].copy()
    return out


def regeneration_check(path: str = CORPUS_PATH) -> Dict:
    """Verification aid only (the JSON is authoritative): replay the documented xorshift32
    stream and report, per field, whether all values equal round(u * scale, 8) for a single
    field-constant scale.  Scalar fields use an undocumented mapping and are reported as such."""
    with open(path) as f:
        d = json.load(f)
    state = int(d["sampler"]["seed_u32"])

    def nxt():
        nonlocal state
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
        return state

    pairs: Dict[str, List[Tuple[float, float]]] = {}
    for p in d["probes"]:
        for f in ("W", "b", "a", "d_bp", "d_fa", "e", "L", "dL", "Lbar", "xi_I", "xi_O", "tep"):
            for v in np.ravel(np.asarray(p[f], np.float64)):
                u = ((nxt() % 2000001) - 1000000) / 1000000
                pairs.setdefault(f, []).append((u, float(v)))
        for s in p["register_bank"]:
            for t in ("I", "O", "M"):
                for v in np.ravel(np.asarray(s[t], np.float64)):
                    u = ((nxt() % 2000001) - 1000000) / 1000000
                    pairs.setdefault("reg_" + t, []).append((u, float(v)))
    report = {}
    for f, pr in pairs.items():
        us = np.array([u for u, _ in pr])
        vs = np.array([v for _, v in pr])
        nz = np.abs(us) > 1e-3
        scales = np.round(vs[nz] / us[nz], 6)
        scale = float(np.median(scales))
        exact = bool(np.all(np.abs(np.round(us * scale, 8) - vs) <= 1e-9))
        report[f] = {"n": len(pr), "scale": scale, "exact": exact}
    return report


# ---------------------------------------------------------------------------
# one-step probe evaluation
# ---------------------------------------------------------------------------

class ProbeRunner:
    def __init__(self, corpus: Optional[List[Dict]] = None):
        self.corpus = corpus if corpus is not None else load_corpus()
        self._cache: Dict[str, Dict[str, object]] = {}

    def _compiled(self, p: Program) -> Dict[str, object]:
        """Per-program compiled phases (performance only; D-S2v4-1)."""
        from .grammar import serialize
        key = serialize(p)
        c = self._cache.get(key)
        if c is None:
            rt = p.reg_types()
            fwd = [e for e in (p.w_eff, p.gain) if e is not None]
            c = {"fwd": Compiled(fwd, rt) if fwd else None,
                 "cvec": Compiled([p.cvec], rt) if p.cvec is not None else None,
                 "state": Compiled(list(p.reg_updates), rt) if p.regs else None,
                 "param": Compiled([p.dW, p.db], rt)}
            if len(self._cache) > 256:
                self._cache.clear()
            self._cache[key] = c
        return c

    def step(self, p: Program, q: Dict, slot_of: Optional[Dict[str, int]] = None):
        """One FORWARD + update of a single tanh layer on probe q (float64)."""
        rt = p.reg_types()
        cc = self._compiled(p)
        dims = {I: PI, O: PO}
        if slot_of is None:
            slot_of = {r.name: k for k, r in enumerate(p.regs)}
        regs_old = {r.name: q["bank"][slot_of[r.name]][r.type] for r in p.regs}
        env = {"a": q["a"], "W": q["W"], "b": q["b"], "W_ep0": q["W_ep0"], "tep": q["tep"],
               "xi_I": q["xi_I"], "xi_O": q["xi_O"]}
        for k, v in regs_old.items():
            env["reg:" + k] = v
        with np.errstate(all="ignore"):
            W_eff, g = q["W"], None
            fwd = [e for e in (p.w_eff, p.gain) if e is not None]
            if fwd:
                outs = cc["fwd"](env, 0, dims, np.float64)
                k = 0
                if p.w_eff is not None:
                    W_eff = q["W"] + outs[0]
                    k = 1
                if p.gain is not None:
                    g = np.clip(outs[k], 0.0, GAIN_MAX)
            z = W_eff @ q["a"]
            if g is not None:
                z = g * z
            z = z + q["b"]
            h = np.tanh(z)
            env.update({"z": z, "h": h, "dphi": 1.0 - h * h, "d_bp": q["d_bp"],
                        "d_fa": q["d_fa"], "e": q["e"], "L": q["L"], "dL": q["dL"],
                        "Lbar": q["Lbar"]})
            if p.cvec is not None:
                env["cvec"] = cc["cvec"](env, 0, dims, np.float64)[0]
            new = dict(regs_old)
            if p.regs:
                vs = cc["state"](env, 0, dims, np.float64)
                for rd, v in zip(p.regs, vs):
                    new[rd.name] = np.clip(rd.decay * regs_old[rd.name] + (1 - rd.decay) * v,
                                           -REG_CLIP, REG_CLIP)
            for k, v in new.items():
                env["reg:" + k] = v
            dW, db = cc["param"](env, 0, dims, np.float64)
            dW = np.broadcast_to(dW, (PO, PI))
            db = np.broadcast_to(db, (PO,))
        dr = {rd.name: np.broadcast_to(new[rd.name] - regs_old[rd.name], regs_old[rd.name].shape)
              for rd in p.regs}
        return h, dW, db, dr

    @staticmethod
    def _unit(x: np.ndarray) -> np.ndarray:
        x = np.ravel(x).astype(np.float64)
        n = np.linalg.norm(x)
        return x / n if n > 0 and np.isfinite(n) else np.zeros_like(x)

    def beta(self, p: Program, slot_of: Optional[Dict[str, int]] = None) -> np.ndarray:
        """Full behaviour vector (AE.2.2): per probe (h, unit dW, unit db, unit dr in bank
        slots 1..4).  Register k (canonical order) occupies slot k unless `slot_of` is given."""
        if slot_of is None:
            slot_of = {r.name: k for k, r in enumerate(p.regs)}
        inv = {v: k for k, v in slot_of.items()}
        parts = []
        for q in self.corpus:
            h, dW, db, dr = self.step(p, q, slot_of)
            parts += [h, self._unit(dW), self._unit(db)]
            for k in range(4):
                v = np.zeros(SLOT_PAD)
                if k in inv:
                    u = self._unit(dr[inv[k]])
                    v[:u.size] = u
                parts.append(v)
        return np.concatenate([np.ravel(x) for x in parts])

    def beta_all(self, p: Program) -> List[np.ndarray]:
        """Full behaviour vector under every injective register-to-slot assignment."""
        names = [r.name for r in p.regs]
        return [self.beta(p, dict(zip(names, perm)))
                for perm in itertools.permutations(range(4), len(names))]

    def beta_ext(self, p: Program, slot_of: Optional[Dict[str, int]] = None) -> np.ndarray:
        """External behaviour (h, unit dW, unit db) only -- diagnostic, not used for gating."""
        parts = []
        for q in self.corpus:
            h, dW, db, _ = self.step(p, q, slot_of)
            parts += [h, self._unit(dW), self._unit(db)]
        return np.concatenate([np.ravel(x) for x in parts])


def finite(v: np.ndarray) -> bool:
    return bool(np.all(np.isfinite(v)))


def cos(u: np.ndarray, v: np.ndarray) -> float:
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 1.0 if nu == nv else 0.0
    return float(np.dot(u, v) / (nu * nv))


class DuplicateIndex:
    """Stores behaviour vectors of accepted programs; flags duplicates (AE.2.2)."""

    def __init__(self):
        self.exact: Dict[str, str] = {}
        self.vecs: List[np.ndarray] = []
        self.ids: List[str] = []
        self._mat = None

    @staticmethod
    def exact_key(b: np.ndarray) -> str:
        r = np.round(b, 6) + 0.0
        return hashlib.sha256(r.tobytes()).hexdigest()

    def find(self, b: np.ndarray) -> Optional[Tuple[str, float, str]]:
        k = self.exact_key(b)
        if k in self.exact:
            return self.exact[k], 1.0, "exact"
        if self.vecs:
            if self._mat is None or self._mat.shape[0] != len(self.vecs):
                self._mat = np.stack(self.vecs)
            n = np.linalg.norm(b)
            if n > 0:
                sims = self._mat @ (b / n)
                j = int(np.argmax(sims))
                if sims[j] >= DUP_COS:
                    return self.ids[j], float(sims[j]), "cosine"
        return None

    def add(self, pid: str, b: np.ndarray):
        self.exact[self.exact_key(b)] = pid
        n = np.linalg.norm(b)
        self.vecs.append(b / n if n > 0 else b)
        self.ids.append(pid)
        self._mat = None
