"""CPU numerical diagnostic; no training, theorem or certificate generation."""
import os
for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import argparse
from contextlib import nullcontext
import hashlib
import json
import math
import threading
import time
from pathlib import Path

import numpy as np
import scipy.linalg as la
import psutil
try:
    from threadpoolctl import threadpool_limits, threadpool_info
except ImportError:
    # All library thread caps are set before numerical imports above.
    def threadpool_limits(limits):
        return nullcontext()

    def threadpool_info():
        return [dict(threadpoolctl_available=False, environment_thread_caps=4,
                     torch_threads=1, note="Environment caps precede NumPy/SciPy imports")]

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(x):
    return hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()


class Resources:
    def __init__(self):
        self.start_wall = time.perf_counter()
        self.start_cpu = time.process_time()
        self.peak = psutil.Process().memory_info().rss
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def monitor(self):
        p = psutil.Process()
        while not self.stop.wait(.25):
            self.peak = max(self.peak, p.memory_info().rss)

    def snapshot(self):
        self.peak = max(self.peak, psutil.Process().memory_info().rss)
        return dict(cpu_seconds=time.process_time() - self.start_cpu,
                    wall_seconds=time.perf_counter() - self.start_wall,
                    peak_rss_bytes=self.peak, device="cpu", gpu_seconds=0)

    def check(self):
        s = self.snapshot()
        if (s["cpu_seconds"] > CFG["process_cpu_cap_seconds"] - 120 or
                s["wall_seconds"] > CFG["wall_cap_seconds"] - 60 or
                s["peak_rss_bytes"] > CFG["rss_cap_bytes"]):
            raise RuntimeError("Preregistered resource stop: " + str(s))


def family(n):
    c = CFG["c"]
    a, k = 1-c/n, n//2
    l = n-k
    d = min(k, math.floor(n/(4*c*max(1, math.ceil(c)))))
    w = np.eye(k)[0] - np.ones(k)/math.sqrt(k)
    U = np.eye(k) - 2*np.outer(w, w)/(w@w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)
    O = U@P@U.T
    delta = 1/(100*n)
    R0 = la.block_diag(a*O, delta*np.eye(l))
    # First power-vector choice t=1 from the accepted finite recipe.
    power = np.ones(n)
    inv0 = la.inv(R0)
    if np.any(inv0@power == 0) or np.any(power@inv0 == 0):
        raise RuntimeError("Accepted power-vector t=1 failed; no model replacement")
    C = np.ones((n, n))/n
    for j in range(2*n*n+1):
        eta = 1/(1e8*n*n) * 2.**(-j)
        B = R0 + eta*C
        if np.all(B != 0) and np.all(la.inv(B) != 0):
            break
    else:
        raise RuntimeError("Accepted finite perturbation recipe failed")
    R = a*B/la.svdvals(B)[0]
    beta = max(1., la.norm(R, "fro"))
    kappa = a/beta
    H = math.ceil(math.log(kappa*CFG["window_C"]/(CFG["epsilon"]*(1-a)))/(-math.log(a)))
    return dict(n=n, k=k, l=l, d=d, a=a, delta=delta, R0=R0, R=R, O=O,
                w=w, w2=w@w, beta=beta, kappa=kappa, H=H, T=H+1,
                wR=la.norm(R, "fro")/n, wW=1/math.sqrt(n), wb=.05, eta=eta,
                eta_index=j, e=la.svdvals(R-R0)[0])


def right_O(M, F):
    w = F["w"]
    V = M - (2/F["w2"])*np.outer(M@w, w)
    ix = np.arange(F["k"])
    ix[:F["d"]] = np.roll(ix[:F["d"]], -1)
    V = V[:, ix]
    return V - (2/F["w2"])*np.outer(V@w, w)


def box_cov(F):
    n, k = F["n"], F["k"]
    lo, hi = 1/math.cosh(.5)**2, 1/math.cosh(.25)**2
    mid, sg = (lo+hi)/2, (hi-lo)/2
    Rm = F["R"][:, :k]
    cov = (sg**2*(Rm.T@Rm) + mid**2*np.outer(Rm.sum(0), Rm.sum(0)))/(F["beta"]**2*n)
    return cov


def histories(F, strategy, seed):
    n, k, l, H = (F[x] for x in ("n", "k", "l", "H"))
    names = ["diffuse", "random_pulse", "query_adversarial_pulse", "scalar_control"]
    rng = np.random.default_rng(np.random.SeedSequence([seed, n, names.index(strategy)]))
    hs = np.zeros((H+2, n))
    hs[1:H+1, k:] = CFG["source_amplitude"]*rng.choice([-1., 1.], (H, l))
    if strategy == "diffuse":
        hs[1:H+1, :k] = rng.uniform(-1, 1, (H, k))*CFG["diffuse_memory_amplitude"]/math.sqrt(n)
    elif strategy in ("random_pulse", "query_adversarial_pulse"):
        running = np.eye(k)
        Q = box_cov(F)
        used = []
        cooldown = max(1, min(F["d"], k//3))
        for t in range(1, H+1):
            B = F["a"]*(F["O"]@running)
            if t % 2 == 0:
                if strategy == "random_pulse":
                    i = int(rng.integers(1, k))
                else:
                    QB = Q@B
                    score = np.diag(Q)*np.sum(B*B, axis=1) - (2/k)*np.sum(B*QB, axis=1)
                    eligible = np.ones(k, bool)
                    eligible[0] = False
                    if used:
                        eligible[used[-cooldown:]] = False
                    score[~eligible] = -np.inf
                    i = int(np.argmax(score))
                    used.append(i)
                hs[t, i] = CFG["pulse_memory_amplitude"]*rng.uniform(.5, 1.)
            gate = 1-hs[t, :k]**2
            running = gate[:, None]*B
            running /= max(la.norm(running, "fro"), 1e-300)
    xs = np.arctanh(hs[1:]) - hs[:-1]@F["R"].T - .05
    if np.max(np.abs(xs)) >= .5:
        raise RuntimeError("Generated history left original input domain")
    gates = 1-hs[1:H+1, :k]**2
    nonscalar = np.max(np.ptp(gates, axis=1))
    # Minimal period of a finite word, allowing a partial final repetition.
    words = [np.round(g, 14).tobytes() for g in gates]
    prefix = np.zeros(H, dtype=int)
    for t in range(1, H):
        p = prefix[t-1]
        while p and words[t] != words[p]:
            p = prefix[p-1]
        if words[t] == words[p]:
            p += 1
        prefix[t] = p
    period = H-int(prefix[-1])
    commutator = max(la.norm(g[:, None]*F["O"]-F["O"]*g[None, :], "fro") for g in gates)
    if strategy != "scalar_control" and (nonscalar <= 1e-12 or period <= H//2 or commutator <= 1e-12):
        raise RuntimeError("History did not pass non-scalar/aperiodic checks")
    info = dict(history_sha256=digest(hs), inputs_sha256=digest(xs),
                max_abs_input=float(np.max(np.abs(xs))), fixed_h=float(la.norm(hs[-1])),
                min_finite_word_period=period, max_gate_coordinate_spread=float(nonscalar),
                max_gate_rotation_commutator=float(commutator),
                mean_memory_gate_damage=float(np.mean(1-gates)))
    return hs, xs, info


def propagation(F, hs):
    k, T = F["k"], F["T"]
    B = np.zeros((T+1, k, k))
    tail = np.eye(k)
    for t in range(T, 0, -1):
        B[t] = tail*(1-hs[t, :k]**2)[None, :]
        tail = F["a"]*right_O(B[t], F)
    return B


def continuation_bank(F, seed):
    rng = np.random.default_rng(np.random.SeedSequence([seed, F["n"], 741]))
    n = F["n"]
    cs, queries = [], []
    for length in CFG["continuation_lengths"]:
        for _ in range(CFG["continuations_per_length"]):
            xs = rng.uniform(-.45, .45, (length, n))
            h = np.zeros(n)
            gates = []
            for x in xs:
                h = np.tanh(F["R"]@h+x+.05)
                gates.append(1-h*h)
            p = np.ones(n)/(math.sqrt(n)*F["beta"])
            for g in reversed(gates):
                p = F["R"].T@(g*p)
            cs.append(p)
            queries.append(xs)
    return np.array(cs), queries


def whiten_columns(K, F):
    D = 1/(1-CFG["source_amplitude"]**2)
    gram_diag = D*D+F["delta"]**2
    diag_previous = math.sqrt(gram_diag)
    K[:, 0] /= diag_previous
    for i in range(1, F["H"]):
        sub = -D*F["delta"]/diag_previous
        diag = math.sqrt(gram_diag-sub*sub)
        K[:, i] = (K[:, i]-sub*K[:, i-1])/diag
        diag_previous = diag
    return K


def history_direction(v, F):
    # delta h=L^-T v; transpose back substitution for the input-chart Gram.
    H, delta = F["H"], F["delta"]
    D = 1/(1-CFG["source_amplitude"]**2)
    ds = np.empty(H)
    subs = np.zeros(H)
    ds[0] = math.sqrt(D*D+delta*delta)
    for i in range(1, H):
        subs[i] = -D*delta/ds[i-1]
        ds[i] = math.sqrt(D*D+delta*delta-subs[i]**2)
    ans = np.zeros_like(v)
    ans[-1] = v[-1]/ds[-1]
    for i in range(H-2, -1, -1):
        ans[i] = (v[i]-subs[i+1]*ans[i+1])/ds[i]
    return ans


def kernel(F, B, factor):
    H, k, m = F["H"], F["k"], factor.shape[0]
    # Temporary matrix multiplication is chunked; no GPU or huge Jacobian tensor.
    K = np.empty((2*m*k, H), order="F")
    D = 1/(1-CFG["source_amplitude"]**2)
    for s in range(1, H+1):
        now, nxt = factor@B[s], factor@B[s+1]
        K[:m*k, s-1] = F["wR"]*nxt.ravel()
        K[m*k:, s-1] = F["wW"]*(D*now-F["delta"]*nxt).ravel()
    return whiten_columns(K, F)


def spectral_summary(s, F):
    eps, l, n = CFG["epsilon"], F["l"], F["n"]
    count = int(np.count_nonzero(s > eps))*l
    energy = float(s@s)
    idx = np.flatnonzero(s > eps)
    return dict(visible_count=count, temporal_visible_count=count//l,
                count_over_n2=count/n**2, count_over_n2logn=count/(n**2*math.log(n)),
                input_sd_visible_count=int(np.count_nonzero(s*CFG["secondary_input_scale"] > eps))*l,
                radius_005_linear_visible_count=int(np.count_nonzero(s*CFG["safe_direction_radius"] > eps))*l,
                count_at_1e2=int(np.count_nonzero(s > .01))*l,
                count_at_1e4=int(np.count_nonzero(s > .0001))*l,
                stable_rank_per_source=energy/max(float(s[0]**2), 1e-300),
                top=float(s[0]), median=float(np.median(s)), tail=float(s[-1]),
                tail_energy_below_epsilon=float(np.sum(s[s<=eps]**2)/max(energy, 1e-300)),
                epsilon_gap=(float(s[idx[-1]]/max(s[idx[-1]+1], 1e-300))
                             if len(idx) and idx[-1]+1<len(s) else None))


def correlations(gram, F):
    norms = np.sqrt(np.maximum(np.diag(gram), 1e-300))
    ans = {}
    for lag in sorted(set([1, F["d"], 2*F["d"], F["n"], 2*F["n"]])):
        if lag < len(gram):
            vals = np.diag(gram, lag)/(norms[:-lag]*norms[lag:])
            ans[str(lag)] = dict(mean=float(np.mean(vals)), mean_absolute=float(np.mean(np.abs(vals))))
    return ans


def mode_sensitivities(F, B, v):
    z = history_direction(v, F)
    D = 1/(1-CFG["source_amplitude"]**2)
    SR = F["wR"]*np.einsum("tij,t->ij", B[2:], z)
    SW = F["wW"]*(D*np.einsum("tij,t->ij", B[1:-1], z)-
                          F["delta"]*np.einsum("tij,t->ij", B[2:], z))
    return z, SR, SW


def optimize_box(F, SR, SW, seed):
    # Allowed one-step query optimization; returns a numerical LOWER estimate.
    n, k = F["n"], F["k"]
    Y = F["R"][:, :k]@np.concatenate([SR, SW], axis=1)/(F["beta"]*math.sqrt(n))
    M = Y@Y.T
    lo, hi = 1/math.cosh(.5)**2, 1/math.cosh(.25)**2
    rng = np.random.default_rng(seed)
    best, best_g = -1., None
    for j in range(12):
        g = (np.full(n, hi) if j == 0 else np.full(n, lo) if j == 1 else
             np.where(rng.integers(0, 2, n), hi, lo))
        for _ in range(12):
            changes = 0
            product = M@g
            for i in range(n):
                target = lo if g[i] == hi else hi
                diff = target-g[i]
                gain = 2*diff*product[i]+diff*diff*M[i, i]
                if gain > 1e-20:
                    g[i] = target
                    product += diff*M[:, i]
                    changes += 1
            if not changes:
                break
        value = float(g@M@g)
        if value > best:
            best, best_g = value, g.copy()
    vf = np.arccosh(1/np.sqrt(best_g))-.05
    return math.sqrt(max(best, 0)), vf


def actual_gradient(F, hs, cq):
    import torch
    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float64)
    xs = np.arctanh(hs[1:])-hs[:-1]@F["R"].T-.05
    Rp = torch.tensor(F["R"], requires_grad=True)
    Wp = torch.eye(F["n"], requires_grad=True)
    bp = torch.full((F["n"],), .05, requires_grad=True)
    h = torch.zeros(F["n"])
    for x in xs:
        h = torch.tanh(Rp@h+Wp@torch.tensor(x)+bp)
    g = torch.autograd.grad(torch.tensor(cq)@h, (Rp, Wp, bp))
    return np.concatenate([F["wR"]*g[0].detach().numpy().ravel(),
                           F["wW"]*g[1].detach().numpy().ravel(),
                           F["wb"]*g[2].detach().numpy()]), float(h.detach().norm())


def crosscheck(F, hs, B, v, seed):
    z, SR, SW = mode_sensitivities(F, B, v)
    j = F["k"]+F["l"]//3
    dh = np.zeros_like(hs)
    dh[1:-1, j] = z
    dx = dh[1:]/(1-hs[1:]**2)-dh[:-1]@F["R"].T
    norm = la.norm(dx)
    if abs(norm-1) > 1e-7:
        raise RuntimeError("Dense input-chart normalization disagreement")
    actual_distance, vf = optimize_box(F, SR, SW, seed)
    c = F["R"].T@((1-np.tanh(vf+.05)**2)*np.ones(F["n"])/math.sqrt(F["n"]))/F["beta"]
    expected = np.zeros(2*F["n"]**2+F["n"])
    expected[:F["n"]**2].reshape(F["n"], F["n"])[:F["k"], j] = SR.T@c[:F["k"]]
    expected[F["n"]**2:2*F["n"]**2].reshape(F["n"], F["n"])[:F["k"], j] = SW.T@c[:F["k"]]
    records = []
    for step in CFG["fd_steps"]:
        plus, hp = actual_gradient(F, hs+step*dh, c)
        minus, hm = actual_gradient(F, hs-step*dh, c)
        fd = (plus-minus)/(2*step)
        err = la.norm(fd-expected)
        records.append(dict(step=step, full_gradient_derivative_error=float(err),
                            full_derivative_norm=float(la.norm(fd)),
                            proxy_query_derivative=float(la.norm(expected)),
                            fixed_h_forward_error=max(hp, hm)))
        if err > CFG["crosscheck_error_cap"] or max(hp, hm) > 1e-10:
            raise RuntimeError("Full dense derivative cross-check failed: "+str(records[-1]))
    radius = CFG["safe_direction_radius"]
    plus_h, minus_h = hs+radius*dh, hs-radius*dh
    xp = np.arctanh(plus_h[1:])-plus_h[:-1]@F["R"].T-.05
    xm = np.arctanh(minus_h[1:])-minus_h[:-1]@F["R"].T-.05
    if max(np.abs(xp).max(), np.abs(xm).max()) >= .5:
        raise RuntimeError("Selected finite perturbation is inadmissible")
    plus, hp = actual_gradient(F, plus_h, c)
    minus, hm = actual_gradient(F, minus_h, c)
    return dict(input_direction_norm=float(norm), finite_difference=records,
                optimized_box_unit_direction_estimate=actual_distance,
                radius_005_actual_half_separation=float(la.norm(plus-minus)/2),
                radius_005_linear_prediction=radius*actual_distance,
                finite_radius_max_abs_input=float(max(np.abs(xp).max(), np.abs(xm).max())),
                finite_radius_fixed_h_error=max(hp, hm))


def run_case(F, strategy, seed, resources, output, development=False):
    start_c, start_w = time.process_time(), time.perf_counter()
    case = f"n{F['n']:03d}_{strategy}_s{seed}"
    hs, xs, info = histories(F, strategy, seed)
    B = propagation(F, hs)
    cs, queries = continuation_bank(F, seed)
    factors = dict(box_rms=la.cholesky(box_cov(F), lower=True).T,
                   continuation_rms=cs[:, :F["k"]]/math.sqrt(len(cs)),
                   all_query_envelope=F["kappa"]*np.eye(F["k"]))
    metrics, spectra, modes = {}, {}, None
    for name, factor in factors.items():
        resources.check()
        K = kernel(F, B, factor)
        gram = K.T@K
        values, V = la.eigh(gram, check_finite=False, driver="evd")
        negative = float(min(values.min(), 0))
        order = np.argsort(values)[::-1]
        vals = values[order]
        s = np.sqrt(np.maximum(vals, 0))
        metrics[name] = spectral_summary(s, F)
        metrics[name]["negative_gram_eigenvalue"] = negative
        metrics[name]["correlations_by_lag"] = correlations(gram, F)
        spectra[name] = s
        if name == "box_rms":
            ix = np.flatnonzero(s > CFG["epsilon"])
            picks = sorted(set([0, int(ix[-1]) if len(ix) else 0,
                                min(len(s)-1, int(ix[-1])+1) if len(ix) else len(s)//2,
                                min(len(s)-1, 2*F["d"])]))
            modes = [(p, V[:, order[p]].copy()) for p in picks]
            metrics[name]["query_optimized_modes"] = []
            for p, v in modes:
                _, SR, SW = mode_sensitivities(F, B, v)
                dist, _ = optimize_box(F, SR, SW, seed+p)
                metrics[name]["query_optimized_modes"].append(dict(index=p, rms_singular_value=float(s[p]),
                                                                   optimized_box_distance=dist,
                                                                   ratio_to_epsilon=dist/CFG["epsilon"]))
        if development or (F["n"] == 16 and strategy == "scalar_control"):
            direct = la.svdvals(K, check_finite=False)
            direct = np.pad(direct, (0, len(s)-len(direct)))
            metrics[name]["direct_svd_max_absolute_difference"] = float(np.max(np.abs(s-direct)))
        del K, gram, V
        resources.check()
    checks = []
    if development or (F["n"] in CFG["crosscheck_widths"] and seed == CFG["seeds"][0] and strategy != "scalar_control"):
        # Leading and near-threshold/right-tail directions; fixed rule before results.
        for p, v in modes[:2]:
            ck = crosscheck(F, hs, B, v, seed+p)
            ck["mode_index"] = p
            checks.append(ck)
    result = dict(case=case, n=F["n"], c=CFG["c"], gamma=1-F["a"], epsilon=CFG["epsilon"],
                  horizon=F["T"], relevant_window=F["H"], source_tangent_dimension=F["H"]*F["l"],
                  full_parameter_count=2*F["n"]**2+F["n"], strategy=strategy, seed=seed,
                  beta=F["beta"], wR=F["wR"], wW=F["wW"], w_b=F["wb"],
                  dense_perturbation_norm=F["e"], actual_R_sha256=digest(F["R"]),
                  history=info, metrics=metrics, full_dense_crosschecks=checks,
                  cpu_seconds=time.process_time()-start_c, wall_seconds=time.perf_counter()-start_w,
                  resources=resources.snapshot(), proof_width_condition=F["n"]>=200,
                  limitations="source-only tangent; memory-output surrogate; finite-width/RMS numerical diagnostic, not robust dimension")
    output.mkdir(exist_ok=True)
    write_json(output/(case+".json"), result)
    np.savez_compressed(output/(case+"_spectra.npz"), **spectra)
    np.savez_compressed(output/(case+"_history.npz"), hidden_states=hs,
                        inputs=xs, query_adjoints=cs)
    print(json.dumps(dict(case=case, H=F["H"], counts={m:v["visible_count"] for m,v in metrics.items()},
                          cpu=result["cpu_seconds"], wall=result["wall_seconds"])), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    resources = Resources()
    output = ROOT/("development" if args.development else "results")
    output.mkdir(exist_ok=True)
    status, done = "complete", []
    try:
        with threadpool_limits(limits=CFG["threads"]):
            if args.development:
                F = family(16)
                F["H"], F["T"] = 32, 33  # development only; never official horizon.
                for name in CFG["strategies"]:
                    done.append(run_case(F, name, CFG["development_seed"], resources, output, True)["case"])
            else:
                for n in CFG["widths"]:
                    resources.check()
                    F = family(n)
                    np.savez_compressed(output/f"model_n{n}.npz", R=F["R"], R0=F["R0"], O=F["O"])
                    for name in ["scalar_control"]+CFG["strategies"]:
                        seeds = CFG["seeds"][:1] if name == "scalar_control" else CFG["seeds"]
                        for seed in seeds:
                            resources.check()
                            filename = output/f"n{n:03d}_{name}_s{seed}.json"
                            if filename.exists():
                                raise RuntimeError("Refusing to overwrite official record "+str(filename))
                            done.append(run_case(F, name, seed, resources, output)["case"])
    except Exception as exc:
        status = "stopped"
        write_json(output/"stop_record.json", dict(error=repr(exc), done=done, resources=resources.snapshot()))
        raise
    finally:
        write_json(output/"resource_summary.json", dict(status=status, cases=len(done), **resources.snapshot(),
                                                     threadpool_info=threadpool_info()))
        resources.stop.set()


if __name__ == "__main__":
    main()
