"""History-variable adversary, not training. Independently reduced reference."""
from independent import *
import torch
torch.set_num_threads(4)
torch.set_default_dtype(torch.float64)


def active_basis(f):
    V = np.zeros((f.k, f.d))
    V[1:f.d, :f.d - 1] = np.eye(f.d - 1)
    V[f.d:, -1] = 1 / math.sqrt(f.k - f.d)
    return V


class Reduced:
    def __init__(self, f, Q, Z, strength="sustained"):
        self.f, self.q, self.p = f, Q.shape[1], Z.shape[1]
        self.T = Q.shape[0]
        V = active_basis(f)
        self.O = torch.tensor(V.T @ f.O @ V, device="cpu")
        self.W = torch.tensor(V.T @ f.warm_reference @ V, device="cpu")
        self.Q = torch.tensor(Q, device="cpu")
        self.Z = torch.tensor(Z, device="cpu")
        self.I = torch.eye(f.d, device="cpu")
        div = math.sqrt(self.T) if strength == "total-budget" else 1.
        self.amplitude = .055 / div
        baseline = np.tile([.25 / div, -.25 / div], f.d // 2)
        if f.d % 2:
            baseline = np.r_[baseline, 0.]
        self.baseline = torch.tensor(baseline, device="cpu")
        self.perm = torch.tensor(np.array([(np.arange(f.d) - t) % f.d for t in range(self.T)]), device="cpu")
        self.warm_scalar = (1 - f.a ** (3 * f.n)) / (1 - f.a)

    def gates(self, C):
        f = self.f
        field = torch.tanh(math.sqrt(self.T * f.d) * (self.Q @ C @ self.Z.T))
        latent = self.baseline + self.amplitude * (field - field.mean(dim=1, keepdim=True))
        rotated = torch.gather(latent, 1, self.perm)
        ck = 1 / (math.sqrt(f.k) - 1)
        common = ck * rotated[:, :1]
        cycle = rotated[:, 1:] + common
        return torch.cat([1 - cycle ** 2, 1 - common ** 2], dim=1)

    def endpoint(self, gates):
        f = self.f
        M = self.W
        scalar = torch.tensor(self.warm_scalar, device="cpu")
        for g in gates:
            M = g[:, None] * (f.a * self.O @ M + self.I)
            scalar = g[-1] * (f.a * scalar + 1)
        return f.a * self.O @ M + self.I, f.a * scalar + 1

    def objective(self, raw):
        C = raw.reshape(self.q, self.p)
        C = C / torch.linalg.vector_norm(C)
        mp_, sp = self.endpoint(self.gates(C))
        mm, sm = self.endpoint(self.gates(-C))
        size = torch.maximum(torch.linalg.matrix_norm(mp_ - mm, ord=2), torch.abs(sp - sm))
        return self.f.a * self.f.Hnorm / self.f.n * size / .002


def freeze():
    paths = [HERE / "ADVERSARY_PROTOCOL.md", HERE / "adversary.py", HERE / "tests_adversary.py", HERE / "SCREEN.json"]
    paths += [HERE / f"screen_{n}_{n}_{math.ceil(math.log(n))}_sustained_spread.npz" for n in (200, 400)]
    value = {"utc": datetime.now(timezone.utc).isoformat(), "after_primary": True,
             "sha256": {p.name: digest(p) for p in paths}}
    path = HERE / "FROZEN_ADVERSARY.json"
    if path.exists():
        old = json.loads(path.read_text())
        assert old["sha256"] == value["sha256"]
    else:
        dump("FROZEN_ADVERSARY.json", value)


def run():
    freeze()
    monitor = Monitor()
    outputs = []
    primary = json.loads((HERE / "SCREEN.json").read_text())["rows"]
    with (HERE / "adversary_trace.jsonl").open("x", encoding="utf-8") as log:
        for n in (200, 400):
            f = Family(n)
            frozen_R = f.R.copy()
            key = f"{n}_{n}_{math.ceil(math.log(n))}_sustained_spread"
            data = np.load(HERE / f"screen_{key}.npz")
            Q, Z = data["Q"], data["Z"]
            reduced = Reduced(f, Q, Z)
            oldrow = next(x for x in primary if x["key"] == key)
            starts = [data["coefficients"][oldrow["weakest_sampled_pair"]],
                      np.random.default_rng(710002 + n).normal(size=(Q.shape[1], Z.shape[1]))]
            for start, value in enumerate(starts):
                value = value / np.linalg.norm(value)
                raw = torch.tensor(value, requires_grad=True, device="cpu")
                moment = torch.zeros_like(raw); variance = torch.zeros_like(raw)
                best = float("inf"); bestC = None
                iterations = 0
                for iteration in range(120):
                    if monitor.snapshot()["cpu_seconds"] >= 600:
                        break
                    obj = reduced.objective(raw)
                    v = float(obj.detach())
                    if v < best:
                        best = v; bestC = (raw / torch.linalg.vector_norm(raw)).detach().numpy().copy()
                    entry = {"n": n, "start": start, "iteration": iteration, "upper_ratio": v, "resource": monitor.snapshot()}
                    log.write(json.dumps(entry) + "\n"); log.flush()
                    iterations = iteration + 1
                    if v < .25:
                        break
                    grad, = torch.autograd.grad(obj, raw)
                    with torch.no_grad():
                        moment.mul_(.9).add_(grad, alpha=.1)
                        variance.mul_(.999).addcmul_(grad, grad, value=.001)
                        step = .025 * (moment / (1 - .9 ** (iteration + 1))) / (torch.sqrt(variance / (1 - .999 ** (iteration + 1))) + 1e-12)
                        raw.sub_(step)
                    assert np.array_equal(f.R, frozen_R), "Only history coefficients may change"
                if bestC is None:
                    continue
                hp, rb = profiles(f, Q, Z, bestC, "sustained", "spread")
                hm, _ = profiles(f, Q, Z, -bestC, "sustained", "spread")
                op = Difference(f, hp, hm)
                matrix = op.matvec(np.eye(f.r))
                upper = f.a * f.Hnorm / n * svdvals(matrix, check_finite=False)[0] + 2 * f.eta
                lower, query = box_lower(f, op, np.random.default_rng(721002 + n + start))
                px, pe, pinputs = f.history_check(hp)
                mx, me, minputs = f.history_check(hm)
                center, _ = profiles(f, Q, Z, np.zeros_like(bestC), "sustained", "spread")
                _, _, cinputs = f.history_check(center)
                row = {"n": n, "start": start, "T": n, "q": Q.shape[1], "section_dimension": bestC.size,
                       "iterations": iterations, "reduced_upper_ratio": best,
                       "independent_full_operator_upper_ratio": float(upper / .002),
                       "actual_query_lower_distance": lower, "maximum_input": max(px, mx),
                       "endpoint_error": max(pe, me), "sphere_coefficient_norm": float(np.linalg.norm(bestC)),
                       "physical_radius": max(float(np.linalg.norm(pinputs - cinputs)), float(np.linalg.norm(minputs - cinputs))),
                       "crosscheck_error": abs(upper / .002 - best), "all_query_pair_failure_evidence": bool(upper < .002),
                       "result_level": "Numerical counterpair, not an interval certificate", "resource": monitor.snapshot()}
                np.savez_compressed(HERE / f"adversary_n{n}_start{start}.npz", C=bestC, query=query, Q=Q, Z=Z,
                                    operator_spectrum=svdvals(matrix, check_finite=False))
                outputs.append(row)
                dump("ADVERSARY.json", {"rows": outputs, "resource": monitor.snapshot()})
                print(json.dumps(row), flush=True)
            if monitor.snapshot()["cpu_seconds"] >= 600:
                break
    dump("ADVERSARY_RESOURCE.json", monitor.snapshot())
    monitor.stop_event.set()
    freeze()


if __name__ == "__main__":
    run() if len(sys.argv) > 1 and sys.argv[1] == "run" else freeze()
