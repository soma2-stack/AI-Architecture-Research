"""Secondary exact dense full-history local spectrum, CPU numerical only."""
import time
import json
import hashlib
import subprocess
from pathlib import Path
import argparse

import run as core
import numpy as np
import scipy.linalg as la

ROOT = Path(__file__).resolve().parent
SEEDS = [73101, 73102]
WIDTHS = [12, 16, 20, 24]


def full_chart(F, hs):
    n, H, T = F["n"], F["H"], F["T"]
    P = 2*n*n+n
    xs = np.arctanh(hs[1:])-hs[:-1]@F["R"].T-.05
    S = np.zeros((n, P))
    old = np.zeros((H+1, n, P))
    gates = 1-hs*hs
    for t in range(1, T+1):
        inject = np.zeros((n, P))
        for i in range(n):
            inject[i, i*n:(i+1)*n] = F["wR"]*hs[t-1]
            inject[i, n*n+i*n:n*n+(i+1)*n] = F["wW"]*xs[t-1]
            inject[i, 2*n*n+i] = F["wb"]
        pre = F["R"]@S+inject
        if t <= H:
            old[t] = pre
        S = gates[t, :, None]*pre
    tail = np.eye(n)
    Phis = np.zeros((T+1, n, n))
    Ps = np.zeros_like(Phis)
    for t in range(T, 0, -1):
        Phis[t] = tail
        Ps[t] = tail*gates[t][None, :]
        tail = Ps[t]@F["R"]
    lo, hi = 1/np.cosh(.5)**2, 1/np.cosh(.25)**2
    mid, sg = (lo+hi)/2, (hi-lo)/2
    root = sg*np.eye(n)+(np.sqrt(sg*sg+n*mid*mid)-sg)*np.ones((n, n))/n
    Q = root@F["R"]/(F["beta"]*np.sqrt(n))
    K = np.empty((n*P, n*H), order="F")
    diag_blocks, sub_blocks = [], []
    previous_chol = None
    for t in range(1, H+1):
        QPhi = Q@Phis[t]
        QP = Q@Ps[t]
        Qnext = Q@Ps[t+1]
        block = np.einsum("aj,jp->apj", QPhi*(-2*hs[t])[None, :], old[t])
        # R feature change at t+1 and W input change at t.
        for j in range(n):
            rows = np.arange(n)*n+j
            block[:, rows, j] += F["wR"]*Qnext
            block[:, n*n+rows, j] += (F["wW"]/gates[t, j])*QP
        # Full next-input compensation: dx_(t+1)=-R dh_t.
        block[:, n*n:2*n*n, :] -= F["wW"]*np.einsum("ai,bj->aibj", Qnext, F["R"]).reshape(n, n*n, n)
        raw = block.reshape(n*P, n)
        D = 1/gates[t]
        gram_diagonal = np.diag(D*D)+F["R"].T@F["R"]
        if previous_chol is None:
            sub = np.zeros((n, n))
            chol = la.cholesky(gram_diagonal, lower=True)
        else:
            off = -D[:, None]*F["R"]
            sub = la.solve_triangular(previous_chol, off.T, lower=True).T
            chol = la.cholesky(gram_diagonal-sub@sub.T, lower=True)
            raw = raw-K[:, (t-2)*n:(t-1)*n]@sub.T
        K[:, (t-1)*n:t*n] = la.solve_triangular(chol, raw.T, lower=True).T
        diag_blocks.append(chol)
        sub_blocks.append(sub)
        previous_chol = chol
    return K, Q, np.array(diag_blocks), np.array(sub_blocks)


def physical_direction(u, chol, sub):
    H, n = u.shape
    z = np.zeros_like(u)
    for t in range(H-1, -1, -1):
        v = u[t].copy()
        if t+1 < H:
            v -= sub[t+1].T@z[t+1]
        z[t] = la.solve_triangular(chol[t].T, v, lower=False)
    return z


def full_check(F, hs, K, Q, chol, sub, seed):
    rng = np.random.default_rng(seed)
    u = rng.normal(size=(F["H"], F["n"]))
    u /= la.norm(u)
    dh = np.zeros_like(hs)
    dh[1:-1] = physical_direction(u, chol, sub)
    dx = dh[1:]/(1-hs[1:]**2)-dh[:-1]@F["R"].T
    if abs(la.norm(dx)-1) > 1e-7:
        raise RuntimeError("Full input-chart whitening failed")
    cov_output = (K@u.ravel()).reshape(F["n"], -1)
    dS = la.solve(Q, cov_output)
    vf = rng.choice([.2, .45], F["n"])
    c = F["R"].T@((1-np.tanh(vf+.05)**2)*np.ones(F["n"])/np.sqrt(F["n"]))/F["beta"]
    expected = dS.T@c
    records = []
    for step in core.CFG["fd_steps"]:
        plus, ep = core.actual_gradient(F, hs+step*dh, c)
        minus, em = core.actual_gradient(F, hs-step*dh, c)
        err = la.norm((plus-minus)/(2*step)-expected)
        records.append(dict(step=step, full_gradient_derivative_error=float(err),
                            expected_norm=float(la.norm(expected)), forward_endpoint_error=max(ep, em)))
        if err > 1e-7 or max(ep, em) > 1e-10:
            raise RuntimeError("Full Jacobian finite-difference disagreement: "+str(records[-1]))
    return dict(input_direction_norm=float(la.norm(dx)), finite_differences=records)


def case(F, strategy, seed, resources, folder):
    start_c, start_w = time.process_time(), time.perf_counter()
    hs, xs, info = core.histories(F, strategy, seed)
    K, Q, chols, subs = full_chart(F, hs)
    resources.check()
    checks = full_check(F, hs, K, Q, chols, subs, seed)
    gram = K.T@K
    del K
    resources.check()
    eigs = la.eigvalsh(gram, check_finite=False, driver="evd")
    negative = float(min(0, eigs.min()))
    s = np.sqrt(np.maximum(eigs[::-1], 0))
    eps, n = core.CFG["epsilon"], F["n"]
    count = int(np.count_nonzero(s>eps))
    result = dict(n=n, strategy=strategy, seed=seed, c=1., epsilon=eps, H=F["H"], T=F["T"],
                  full_input_tangent_dimension=n*F["H"], P=2*n*n+n,
                  visible_count=count, count_over_n2=count/n**2,
                  count_over_n2logn=count/(n*n*np.log(n)),
                  input_sd_visible_count=int(np.count_nonzero(s*core.CFG["secondary_input_scale"]>eps)),
                  radius_005_linear_count=int(np.count_nonzero(s*.05>eps)),
                  top=float(s[0]), median=float(np.median(s)), tail=float(s[-1]),
                  tail_energy_below_epsilon=float(np.sum(s[s<=eps]**2)/np.sum(s*s)),
                  negative_gram_eigenvalue=negative, history=info, checks=checks,
                  cpu_seconds=time.process_time()-start_c, wall_seconds=time.perf_counter()-start_w,
                  resources=resources.snapshot(), metric="complete dense BOX-RMS fixed-h Jacobian",
                  limitation="secondary small-width numerical tangent; not finite-radius robust memory dimension")
    name = f"n{n:03d}_{strategy}_s{seed}"
    if (folder/(name+".json")).exists():
        raise RuntimeError("Refusing to overwrite full-history case")
    core.write_json(folder/(name+".json"), result)
    np.savez_compressed(folder/(name+"_spectra.npz"), box_rms=s)
    np.savez_compressed(folder/(name+"_history.npz"), hidden_states=hs, inputs=xs)
    print(json.dumps(dict(case=name, full_visible_count=count, cpu=result["cpu_seconds"], wall=result["wall_seconds"])), flush=True)


def freeze():
    files = [ROOT/"full_history.py", ROOT/"FULL_HISTORY_SUPPLEMENT.md", ROOT/"run.py", ROOT/"config.json"]
    obj = dict(timing="After primary source-only results; before any full-history Jacobian outcomes",
               widths=WIDTHS, seeds=SEEDS, epsilon=.001, c=1.,
               source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
               inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    path = ROOT/"FULL_HISTORY_FROZEN.json"
    if path.exists():
        raise RuntimeError("Supplement already frozen")
    core.write_json(path, obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        freeze()
        return
    frozen = json.loads((ROOT/"FULL_HISTORY_FROZEN.json").read_text())
    for name, hashed in frozen["inputs"].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != hashed:
            raise RuntimeError("Frozen supplement source changed: "+name)
    # Stricter, separately recorded sub-budget; primary usage remains separately saved.
    core.CFG["process_cpu_cap_seconds"] = 3600
    core.CFG["wall_cap_seconds"] = 1200
    resources = core.Resources()
    folder = ROOT/"full_history_results"
    folder.mkdir(exist_ok=True)
    complete = []
    status = "complete"
    try:
        with core.threadpool_limits(limits=4):
            for n in WIDTHS:
                F = core.family(n)
                for strategy in core.CFG["strategies"]:
                    for seed in SEEDS:
                        resources.check()
                        case(F, strategy, seed, resources, folder)
                        complete.append([n, strategy, seed])
    except Exception as exc:
        status = "stopped"
        core.write_json(folder/"stop_record.json", dict(error=repr(exc), complete=complete, resources=resources.snapshot()))
        raise
    finally:
        core.write_json(folder/"resource_summary.json", dict(status=status, cases=len(complete), **resources.snapshot()))
        resources.stop.set()


if __name__ == "__main__":
    main()
