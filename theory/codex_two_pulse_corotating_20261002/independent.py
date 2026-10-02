"""Formula-derived CPU verification. Imports no other project implementation."""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_key] = "4"
import argparse
import hashlib
import json
import math
import platform
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp
import numpy as np
import psutil
import scipy
from scipy.linalg import helmert, svdvals
from scipy.fft import dct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONFIG = json.loads((HERE / "config.json").read_text())
GLO = 1 / math.cosh(.5) ** 2
GHI = 1 / math.cosh(.25) ** 2


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def frozen_manifest():
    paths = [HERE / "PROTOCOL.md", HERE / "config.json", HERE / "independent.py", HERE / "tests.py"]
    paths += [ROOT / "AGENTS.md", ROOT / "theory/reachable_fixed_feature_width_20261002/PROOF.md"]
    paths += sorted((ROOT / "theory/claude_two_pulse_additivity_20261002").glob("*"))
    files = {p.relative_to(ROOT).as_posix(): digest(p) for p in paths if p.is_file()}
    if (HERE / "FROZEN_SETUP.json").exists():
        old = json.loads((HERE / "FROZEN_SETUP.json").read_text())
        assert files == old["sha256"], "A frozen scientific/source file changed."
        return old
    result = {"frozen_utc": datetime.now(timezone.utc).isoformat(), "base_commit": "4a8a2dc6d21c38a7614baf1f3f615e241439eeb7",
              "sha256": files, "versions": {"python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "mpmath": mp.__version__}, "official_outcomes_exist": False}
    dump("FROZEN_SETUP.json", result)
    return result


class Monitor:
    def __init__(self):
        self.p = psutil.Process()
        self.start_cpu = sum(self.p.cpu_times()[:2])
        self.start_wall = time.perf_counter()
        self.peak = self.p.memory_info().rss
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.watch, daemon=True)
        self.thread.start()

    def watch(self):
        while not self.stop_event.wait(.2):
            self.peak = max(self.peak, self.p.memory_info().rss)

    def snapshot(self):
        return {"cpu_seconds": sum(self.p.cpu_times()[:2]) - self.start_cpu,
                "wall_seconds": time.perf_counter() - self.start_wall,
                "peak_rss_bytes": max(self.peak, self.p.memory_info().rss),
                "gpu_seconds": 0, "cuda_used": False, "max_threads_declared": 4}

    def exhausted(self):
        return self.snapshot()["cpu_seconds"] >= CONFIG["cpu_limit_seconds"]


class Family:
    def __init__(self, n):
        self.n, self.k, self.d = n, n // 2, n // 4
        self.l, self.r = n - self.k, self.k - 1
        self.a = 1 - 1 / n
        self.w = -np.ones(self.k) / math.sqrt(self.k)
        self.w[0] += 1
        self.ww = self.w @ self.w
        self.U = np.eye(self.k) - 2 * np.outer(self.w, self.w) / self.ww
        self.O = self.rotate(np.eye(self.k))
        self.R0 = np.zeros((n, n))
        self.R0[:self.k, :self.k] = self.a * self.O
        self.R0[self.k:, self.k:] = np.eye(self.l) / (100 * n)
        perturb = np.random.default_rng(CONFIG["model_seed"]).normal(size=(n, n))
        perturb /= svdvals(perturb, check_finite=False)[0]
        raw = self.R0 + (1e-8 / n ** 2) * perturb
        self.R = self.a * raw / svdvals(raw, check_finite=False)[0]
        self.e = float(svdvals(self.R - self.R0, check_finite=False)[0])
        self.beta = max(1., np.linalg.norm(self.R))
        self.wR = np.linalg.norm(self.R) / n
        self.Hnorm = .4 * math.sqrt(self.l)
        self.eta = self.a * self.Hnorm * self.e * n
        self.E = np.zeros((n, self.r))
        self.E[1:self.k] = np.eye(self.r)
        self.warm_reference = self.geosum(3 * n)
        assert self.e <= 4 / (1e8 * n ** 2) * 1.01

    def house(self, v):
        return v - (2 / self.ww) * np.multiply.outer(self.w, self.w @ v) if v.ndim == 2 else v - 2 * self.w * (self.w @ v) / self.ww

    def rotate(self, v, transpose=False):
        v = self.house(v)
        v = v.copy()
        v[:self.d] = np.roll(v[:self.d], -1 if transpose else 1, axis=0)
        return self.house(v)

    def geosum(self, length):
        coeff = np.bincount(np.arange(length) % self.d, weights=self.a ** np.arange(length), minlength=self.d)
        latent = np.eye(self.k) * ((1 - self.a ** length) / (1 - self.a))
        latent[:self.d, :self.d] = np.column_stack([np.roll(coeff, j) for j in range(self.d)])
        return self.house(self.house(latent.T).T)

    def warm_actual(self):
        # First step has no injection. Thereafter N=3n identical affine steps.
        gate = np.r_[np.ones(self.k), np.full(self.l, .84)]
        A = gate[:, None] * self.R
        C = gate[:, None] * self.E
        result = np.zeros_like(C)
        length = 3 * self.n
        while length:
            if length & 1:
                result = A @ result + C
            length >>= 1
            if length:
                C = A @ C + C
                A = A @ A
        return result

    def query_g(self):
        g = np.full(self.n, GHI)
        g[self.d:self.k] = GLO
        return g

    def history_check(self, locked):
        """Only distinct warmup inputs; full locked physical inputs checked."""
        prev = np.r_[np.zeros(self.k), np.full(self.l, .4)]
        x_first = np.arctanh(prev) - .05
        x_steady = np.arctanh(prev) - self.R @ prev - .05
        maximum = max(np.max(abs(x_first)), np.max(abs(x_steady)))
        xs = []
        for z in locked:
            h = np.r_[z, np.full(self.l, .4)]
            x = np.arctanh(h) - self.R @ prev - .05
            maximum = max(maximum, np.max(abs(x)))
            xs.append(x)
            prev = h
        x = -self.R @ prev - .05
        maximum = max(maximum, np.max(abs(x)))
        xs.append(x)
        endpoint = np.tanh(self.R @ prev + x + .05)
        return float(maximum), float(np.max(abs(endpoint))), np.array(xs)


def single_pulse(f):
    n, k, d, a = f.n, f.k, f.d, f.a
    L = k - d
    Lp = 2 * (L // 2)
    Q = helmert(Lp, full=False).T
    ids = np.arange(d, d + Lp)
    V = f.R @ f.warm_actual() + f.E
    g = f.query_g()
    y = f.R.T @ (f.R.T @ g) / (f.beta * math.sqrt(n))
    affine = -.08 * f.wR * f.Hnorm * (V[ids].T * y[ids]) @ Q
    spectrum = svdvals(affine, check_finite=False)
    ck = 1 / (math.sqrt(k) - 1)
    frac = L / k
    Ec = GLO + (ck + ck ** 2) * GHI - (1 + ck) ** 2 * (frac * GLO + (1 - frac) * GHI)
    mn = 1 - a ** (3 * n + 1)
    closed = .4 * .08 * a ** 2 * mn * math.sqrt(f.l / n) * abs(Ec)
    transfer = .032 * f.e * n ** 1.5
    mp.mp.dps = CONFIG["precision_digits"]
    an = 1 - mp.mpf(1) / n
    cm = 1 / (mp.sqrt(k) - 1)
    gl = mp.sech(mp.mpf(1) / 2) ** 2
    gh = mp.sech(mp.mpf(1) / 4) ** 2
    ee = gl + (cm + cm ** 2) * gh - (1 + cm) ** 2 * (mp.mpf(L) / k * gl + mp.mpf(d) / k * gh)
    high = mp.mpf('.032') * an ** 2 * (1 - an ** (3 * n + 1)) * mp.sqrt(mp.mpf(f.l) / n) * abs(ee)
    rng = np.random.default_rng(771002 + n)
    dirs = [Q[:, 0], Q[:, -1], np.tile([1., -1.], Lp // 2) / math.sqrt(Lp)]
    dirs += [Q @ (v / np.linalg.norm(v)) for v in rng.normal(size=(CONFIG["one_pulse_samples"], Lp - 1))]
    signs = np.tile([1., -1.], Lp // 2)
    z0 = np.zeros(k)
    z0[ids] = signs * math.sqrt(.08)
    _, _, x0 = f.history_check([z0])
    max_input = max_endpoint = max_radius = max_affine_residual = 0.
    base_gate = np.r_[1 - z0 ** 2, np.full(f.l, .84)]
    Bbase = f.R @ (base_gate[:, None] * V) + f.E
    for u in dirs:
        for u in (u, -u):
            z = np.zeros(k)
            z[ids] = signs * np.sqrt(.08 * (1 + u))
            mx, ep, x = f.history_check([z])
            max_input, max_endpoint, max_radius = max(max_input, mx), max(max_endpoint, ep), max(max_radius, np.linalg.norm(x - x0))
            gate = np.r_[1 - z ** 2, np.full(f.l, .84)]
            Bt = f.R @ (gate[:, None] * V) + f.E
            delta = -.08 * f.R[:, ids] @ (u[:, None] * V[ids])
            max_affine_residual = max(max_affine_residual, float(np.max(abs(Bt - Bbase - delta))))
    assert spectrum[-1] > .001 and max_input < .5 and max_endpoint < 1e-12
    assert abs(spectrum[-1] - closed) < transfer + 2e-12
    row = dict(n=n, section_dimension=Lp - 1, actual_whole_sphere_minimum_half_separation=float(spectrum[-1]),
               reference_closed_half_separation=closed, high_precision_reference=str(high),
               dense_transfer_bound=transfer, matrix_norm_error=f.e, all_query_reference_error=f.eta,
               maximum_input=max_input, maximum_endpoint=max_endpoint, sampled_radius=max_radius,
               analytic_physical_radius_bound=math.sqrt(.08) * math.sqrt((25 / 21) ** 2 + a ** 2),
               exact_affine_residual=max_affine_residual, samples=2 * len(dirs),
               minimum_scaled_query_weight=float(min(y[d:k]) * f.beta * math.sqrt(n) / a ** 2),
               maximum_scaled_query_weight=float(max(y[d:k]) * f.beta * math.sqrt(n) / a ** 2), E_formula=Ec,
               model_sha256=hashlib.sha256(f.R.tobytes()).hexdigest(), dtype=str(f.R.dtype), device="cpu")
    np.savez_compressed(HERE / f"single_n{n}.npz", R=f.R, spectrum=spectrum, affine=affine, zero_sum_basis=Q)
    return row


def two_pulse_check(f, gap):
    a, k, d, r = f.a, f.k, f.d, f.r
    O = f.O[1:, 1:]
    A = a * O
    s = gap + 1
    ids = np.arange(d - 1, d - 1 + 2 * ((k - d) // 2))
    V1 = f.geosum(3 * f.n + 1)[1:, 1:]
    Xs = f.geosum(s)[1:, 1:]
    As = np.linalg.matrix_power(A, s)
    g0 = np.ones(r)
    g0[ids] = .92
    V2 = As @ (g0[:, None] * V1) + Xs
    m1 = (1 - a ** (3 * f.n + 1)) / (1 - a)
    ms = (1 - a ** s) / (1 - a)
    alpha = a ** s * .92
    m2 = alpha * m1 + ms
    Lam1 = V1[ids[0]] - m1 * np.eye(r)[ids[0]]
    Lam2 = V2[ids[0]] - m2 * np.eye(r)[ids[0]]
    lam = np.linalg.matrix_power(O, s)[:, ids[0]] - np.eye(r)[:, ids[0]]
    rng = np.random.default_rng(991000 + f.n + gap)
    maxerr = 0.
    for _ in range(8):
        u1 = np.zeros(r); u2 = np.zeros(r)
        u1[ids] = rng.normal(size=len(ids)); u2[ids] = rng.normal(size=len(ids))
        u1 /= np.linalg.norm(u1); u2 /= np.linalg.norm(u2)
        xi = f.R0.T @ rng.uniform(GLO, GHI, f.n) / (f.beta * math.sqrt(f.n))
        y = A.T @ xi[1:k]
        beta = a ** s * (lam @ (g0 * y))
        def endpoint(sign):
            p1 = g0 - sign * .08 * u1
            p2 = g0 - sign * .08 * u2
            return A @ (p2[:, None] * (As @ (p1[:, None] * V1) + Xs)) + np.eye(r)
        actual = (endpoint(1) - endpoint(-1)).T @ xi[1:k] / 2
        form = -.08 * ((alpha * m1 * u1 + m2 * u2) * y + beta * m1 * u1 +
                      alpha * (u1 @ y) * Lam1 + beta * u1.sum() * Lam1 + (u2 @ y) * Lam2)
        maxerr = max(maxerr, np.linalg.norm(actual - form) / max(np.linalg.norm(actual), 1e-30))
    y = A.T @ (f.R0.T @ f.query_g() / (f.beta * math.sqrt(f.n)))[1:k]
    y1 = As.T @ (g0 * y)
    Q = helmert(len(ids), full=False).T
    J = -.08 * f.wR * f.Hnorm * np.column_stack([(V1[ids].T * y1[ids]) @ Q, (V2[ids].T * y[ids]) @ Q])
    spec = svdvals(J, check_finite=False)
    assert maxerr < 2e-9
    return {"n": f.n, "gap": gap, "lemma_relative_error": maxerr,
            "fixed_query_tangent_antipodal_spectrum_above_epsilon": int(sum(spec > .001)),
            "scope": "Exact reference antipodal-linear identity; numerical spectrum is not an all-query dimension cap",
            "alpha": alpha, "m1": m1, "m2": m2, "leak_norm": float(np.linalg.norm(lam)),
            "common_row_error_1": float(np.max(abs(V1[ids] - m1 * np.eye(r)[ids] - Lam1))),
            "common_row_error_2": float(np.max(abs(V2[ids] - m2 * np.eye(r)[ids] - Lam2)))}


def section_basis(f, T, q, seed):
    Q = dct(np.eye(T), type=2, axis=0, norm="ortho").T[:, :q]
    Z = helmert(f.d, full=False).T
    orth, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(f.d - 1, f.d - 1)))
    return Q, Z @ orth


def profiles(f, Q, Z, C, strength, mapping):
    T, q = Q.shape
    div = math.sqrt(T) if strength == "total-budget" else 1.
    B, P = .25 / div, .11 / div
    baseline = np.tile([B, -B], f.d // 2)
    if f.d % 2:
        baseline = np.r_[baseline, 0.]
    field = Q @ C @ Z.T
    if mapping == "spread":
        field = np.tanh(math.sqrt(T * f.d) * field)
        latent = baseline + P / 2 * (field - field.mean(axis=1, keepdims=True))
        radius_bound = (25 / 21 + f.a) * P / 2 * math.sqrt(T * f.d)
    else:
        amplitude = P / (max(np.linalg.norm(Q, axis=1)) * math.sqrt(1 - 1 / f.d))
        latent = baseline + amplitude * field
        radius_bound = (25 / 21 + f.a) * amplitude
    rotated = np.zeros((T, f.k))
    for t in range(T):
        tmp = np.zeros(f.k)
        tmp[:f.d] = np.roll(latent[t], t % f.d)
        rotated[t] = f.house(tmp)
    assert np.max(abs(rotated)) < .401
    return rotated, radius_bound


class Difference:
    """Exact reference sensitivity difference, including both joint trajectories."""
    def __init__(self, f, plus, minus):
        self.f = f
        self.gplus, self.gminus = 1 - plus ** 2, 1 - minus ** 2

    def forward(self, v, gates):
        f = self.f
        vv = np.concatenate([np.zeros((1,) + v.shape[1:]), v], axis=0)
        out = f.warm_reference @ vv
        for g in gates:
            out = (g[:, None] if v.ndim == 2 else g) * (f.a * f.rotate(out) + vv)
        return f.a * f.rotate(out) + vv

    def matvec(self, v):
        return self.forward(v, self.gplus) - self.forward(v, self.gminus)

    def reverse(self, w, gates):
        f = self.f
        out = w.copy()
        p = f.a * f.rotate(w, transpose=True)
        for g in gates[::-1]:
            gp = (g[:, None] if w.ndim == 2 else g) * p
            out += gp
            p = f.a * f.rotate(gp, transpose=True)
        out += f.warm_reference.T @ p
        return out[1:]

    def rmatvec(self, w):
        return self.reverse(w, self.gplus) - self.reverse(w, self.gminus)


def box_lower(f, operator, rng):
    G = np.column_stack([np.full(f.n, GHI), np.full(f.n, GLO), f.query_g()] +
                        [rng.choice([GLO, GHI], size=f.n) for _ in range(3)])
    best = -1.
    bestg = None
    scale = f.Hnorm / (f.n * math.sqrt(f.n))
    for _ in range(CONFIG["query_iterations"] + 1):
        outs = operator.rmatvec(f.R[:, :f.k].T @ G)
        norms = np.linalg.norm(outs, axis=0) * scale
        idx = int(np.argmax(norms))
        if norms[idx] > best:
            best, bestg = float(norms[idx]), G[:, idx].copy()
        gradient = f.R[:, :f.k] @ operator.matvec(outs)
        G = np.where(gradient >= 0, GHI, GLO)
    return max(0., best - 2 * f.eta), bestg


def screen_row(f, T, q, strength, mapping):
    key = f"{f.n}_{T}_{q}_{strength}_{mapping}"
    seed = CONFIG["screen_seed"] + int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed)
    Q, Z = section_basis(f, T, q, seed)
    p = f.d - 1
    dirs = [rng.normal(size=(q, p)), rng.normal(size=(q, p))]
    high = np.zeros((q, p)); high[-1] = rng.normal(size=p)
    cancel = np.zeros((q, p)); cancel[-1] = np.ones(p)
    if q > 1:
        cancel[0] = -1
    else:
        cancel[0] = np.where(np.arange(p) % 2, 1., -1.)
    dirs += [high, cancel]
    dirs = [v / np.linalg.norm(v) for v in dirs]
    center, radbound = profiles(f, Q, Z, np.zeros((q, p)), strength, mapping)
    cxmax, ce, xcenter = f.history_check(center)
    vals, queries, operators, radius, inputmax = [], [], [], [], []
    endpoints = []
    contraction = []
    nonlinear_ratio = []
    for i, C in enumerate(dirs):
        hp, _ = profiles(f, Q, Z, C, strength, mapping)
        hm, _ = profiles(f, Q, Z, -C, strength, mapping)
        op = Difference(f, hp, hm)
        low, g = box_lower(f, op, rng)
        vals.append(low); queries.append(g); operators.append(op)
        for h in (hp, hm):
            mx, ep, xs = f.history_check(h)
            radius.append(float(np.linalg.norm(xs - xcenter)))
            inputmax.append(mx); endpoints.append(ep)
        contraction.append(float(np.sum(np.max(hp ** 2, axis=1))))
        if i == 0:
            hph, _ = profiles(f, Q, Z, .5 * C, strength, mapping)
            hmh, _ = profiles(f, Q, Z, -.5 * C, strength, mapping)
            smaller = Difference(f, hph, hmh)
            y = f.R[:, :f.k].T @ g
            numerator = np.linalg.norm(op.rmatvec(y))
            denominator = 2 * np.linalg.norm(smaller.rmatvec(y))
            nonlinear_ratio.append(float(numerator / max(denominator, 1e-30)))
    weak = int(np.argmin(vals))
    matrix = operators[weak].matvec(np.eye(f.r))
    spectrum = svdvals(matrix, check_finite=False)
    upper = f.a * f.Hnorm / f.n * spectrum[0] + 2 * f.eta
    allquery_fail = bool(upper < 2 * CONFIG["epsilon"])
    # These are diagnostics only. No sampled minimum certifies a sphere.
    frame_mismatch = 0.
    if len(center) > 1:
        g1, g2 = 1 - center[0] ** 2, 1 - center[1] ** 2
        frame_mismatch = float(np.linalg.norm(g2[:, None] * f.O - f.O * g1[None, :]))
    assert max(inputmax + [cxmax]) < .5 and max(endpoints + [ce]) < 1e-12
    row = {"key": key, "n": f.n, "T": T, "q": q, "mapping": mapping, "strength": strength,
           "joint_history_chart_dimension": q * p, "chart_dimension_over_n": q * p / f.n,
           "query_lower_distances": vals, "minimum_sampled_query_lower_distance": min(vals),
           "minimum_lower_ratio_to_2epsilon": min(vals) / .002,
           "weakest_sampled_pair": weak, "weakest_pair_all_query_upper_envelope": float(upper),
           "upper_ratio_to_2epsilon": float(upper / .002), "sampled_all_query_failure_evidence": allquery_fail,
           "sampled_box_passing_pairs": int(sum(v > .002 for v in vals)),
           "pairs": len(vals), "maximum_input": max(inputmax + [cxmax]), "endpoint_error": max(endpoints + [ce]),
           "actual_physical_radius_max_sampled": max(radius), "analytic_physical_radius_bound": radbound,
           "maximum_gate_dissipation_sum_sampled": max(contraction), "rotation_frame_gate_mismatch_F": frame_mismatch,
           "finite_radius_nonlinear_response_ratio": nonlinear_ratio[0], "all_query_dense_error_per_endpoint": f.eta,
           "rigorous_dimension_lower_claim": None, "result_level": "finite-radius CPU float64 diagnostic with analytic dense-transfer bound"}
    np.savez_compressed(HERE / f"screen_{key}.npz", Q=Q, Z=Z, coefficients=np.array(dirs),
                        queries=np.array(queries), weakest_pair_operator_spectrum=spectrum)
    return row


def run():
    frozen_manifest()
    monitor = Monitor()
    rows = []
    pulses = []
    collapses = []
    (HERE / "run.jsonl").touch(exist_ok=False)
    def record(kind, row):
        resource = monitor.snapshot()
        with (HERE / "run.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"kind": kind, **row, "resource": resource}, allow_nan=False) + "\n")
        print(json.dumps({"kind": kind, **row, "resource": resource}, allow_nan=False), flush=True)
        dump("RESOURCE.json", resource)
    for n in CONFIG["one_pulse_widths"]:
        f = Family(n)
        row = single_pulse(f)
        pulses.append(row); record("one_pulse", row)
        if n in (200, 400):
            for gap in (1, f.d // 2):
                row = two_pulse_check(f, gap)
                collapses.append(row); record("two_pulse_identity", row)
        dump("VERIFICATION.json", {"single_pulse": pulses, "two_pulse": collapses, "passed": True})
    record("part1_gate", {"passed": True, "interpretation": "Own analytic proof plus numerical checks, not independent interval regeneration"})
    # Selection/order are prospectively declared; no post-outcome witness search.
    families = {}
    for n in CONFIG["screen_widths"]:
        f = families[n] = Family(n)
        ts = sorted(set([2, math.ceil(math.log(n)), math.ceil(math.sqrt(n)), n // 4, n // 2, n]))
        for T in ts:
            for q in sorted(set([1, min(T, math.ceil(math.log(n))), T])):
                for strength in ("sustained", "total-budget"):
                    if monitor.exhausted():
                        dump("SCREEN.json", {"rows": rows, "complete": False, "stop": "CPU cap"})
                        record("stop", {"reason": "CPU cap", "completed_screen_rows": len(rows)})
                        return
                    row = screen_row(f, T, q, strength, "spread")
                    rows.append(row); record("screen", row)
                    dump("SCREEN.json", {"rows": rows, "complete": False})
    for n, f in families.items():
        for strength in ("sustained", "total-budget"):
            if monitor.exhausted():
                dump("SCREEN.json", {"rows": rows, "complete": False, "stop": "CPU cap"})
                return
            row = screen_row(f, n, math.ceil(math.log(n)), strength, "linear")
            rows.append(row); record("screen_linear_control", row)
    dump("SCREEN.json", {"rows": rows, "complete": True})
    record("finished", {"screen_rows": len(rows), "frozen_source_hashes_still_match": frozen_manifest() is not None})
    monitor.stop_event.set()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("freeze", "run"))
    args = parser.parse_args()
    frozen_manifest() if args.action == "freeze" else run()
