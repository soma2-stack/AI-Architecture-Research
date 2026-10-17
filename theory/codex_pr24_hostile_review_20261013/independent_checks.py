"""Independent PR24 verifier; never imports or runs the author's checks.

Uses forward tangent propagation, exact Fraction arithmetic, and finite
differences with realized inputs held fixed. No training, GPU, or optimizer.
Run: python -I independent_checks.py
"""
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import itertools
import json
import math
import platform
import time
from fractions import Fraction as F
from pathlib import Path
import numpy as np

if os.name == "nt":
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)

SEED = 240513
rng = np.random.default_rng(SEED)


def schedule(z, q):
    R, m = z.shape
    zero = z[0, 0] * 0
    return ([np.full(m, zero, dtype=z.dtype) for _ in range(q * R)]
            + list(z.copy()) + list(-z - z * z / 2))


def forward(xs, R, m, exact=False, initial_tangent=False, injection=None,
            bias=None, coupling=None, source_inputs=None):
    """J = dh/db, dh/dh0, or dh/dk for K=k f_s^T (forward mode).

    Destination-coordinate loop deliberately avoids roll/backprop routines.
    For the projected coupling, injection[t] = f_s^T s_(t-1).
    """
    n = R * m
    dtype, zero, one = (object, F(0), F(1)) if exact else (float, 0.0, 1.0)
    h = np.full(n, zero, dtype=dtype)
    J = np.eye(n, dtype=dtype) * one if initial_tangent else np.full((n, n), zero, dtype=dtype)
    source = np.zeros(n)
    for t, x in enumerate(xs):
        out = np.full(n, zero, dtype=dtype)
        Jout = np.full((n, n), zero, dtype=dtype)
        for j in range(n):
            dest = (j + m) % n
            gate = one + h[j] if j < m else one
            out[dest] = h[j] + h[j] * h[j] / 2 if j < m else h[j]
            Jout[dest] = gate * J[j]
        out[:m] += x
        if not initial_tangent:
            scalar = one if injection is None else injection[t]
            for j in range(n):
                Jout[j, j] += scalar
        if bias is not None:
            out += bias
        if coupling is not None:
            out += coupling @ source
        if source_inputs is not None:
            source += source_inputs[t]
        h, J = out, Jout
    return h, J


def direct_coefficients(dz, mu, q):
    """Independent scalar coefficient count: no powers of S, no delta_s.

    Write r has q copies per output block, plus one when its injection
    reaches that block during the write window. Blocks here are zero-based.
    """
    R, m = dz.shape
    dtype = object if dz.dtype == object else float
    terms = dz * mu.reshape(R, m)[::-1]
    a = terms.sum(axis=0)
    out = np.empty((R, m), dtype=dtype)
    out[0] = (q + 1) * a
    for b in range(1, R):
        out[b] = q * a + terms[R - b:].sum(axis=0)
    return out.reshape(-1)


def choose_future(dz, rho_f):
    orientation = np.where(dz.sum(axis=0) >= 0, 1, -1)
    return np.where(dz * orientation >= 0, 0, -rho_f)


def rational_checks():
    identities = adjoints = 0
    for R in [1, 2, 3, 4, 5, 7]:
        for m in [1, 2]:
            n = R * m
            for q in [0, 1, 3]:
                z = np.array([F(-int(v), 8) for v in rng.integers(0, 5, n)], dtype=object).reshape(R, m)
                zp = np.array([F(-int(v), 8) for v in rng.integers(0, 5, n)], dtype=object).reshape(R, m)
                h, J = forward(schedule(z, q), R, m, exact=True)
                hp, Jp = forward(schedule(zp, q), R, m, exact=True)
                assert all(v == 0 for v in h) and all(v == 0 for v in hp)
                # Every adjoint basis vector plus a signed, non-query adjoint.
                mus = list(np.eye(n, dtype=object))
                mus += [np.array([F((-1)**j * (j + 1), 7) for j in range(n)], dtype=object)]
                for mu in mus:
                    assert np.array_equal((J - Jp).T @ mu, direct_coefficients(z - zp, mu, q))
                    identities += 1
                v = np.array([F(-int(k), 8) for k in rng.integers(0, 5, n)], dtype=object).reshape(R, m)
                _, A = forward(list(v) + [np.full(m, F(0), dtype=object)], R, m, exact=True, initial_tangent=True)
                assert np.array_equal(A.T @ np.ones(n, dtype=object), (1 + v[::-1]).reshape(-1))
                adjoints += 1
                for extra in [0, 1, R + 1]:
                    xx = schedule(z, 0) + [np.full(m, F(0), dtype=object)] * extra
                    _, A = forward(xx, R, m, exact=True, initial_tangent=True)
                    expected = np.full((n, n), F(0), dtype=object)
                    diag = (1 + z[::-1]).reshape(-1)
                    for j in range(n):
                        expected[(j + extra * m) % n, j] = diag[j]
                    assert np.array_equal(A, expected)
    return {"exact_pair_identity_cases": identities, "exact_future_adjoint_cases": adjoints,
            "R": [1, 2, 3, 4, 5, 7], "m": [1, 2], "q": [0, 1, 3],
            "initial_state_jacobian_and_padding": "all exact"}


def exhaustive_signs():
    cases, min_slack, worst_ratio, witness = 0, math.inf, 1.0, None
    for R in range(1, 6):
        m, n = 1, R
        for signs in itertools.product([-1, 0, 1], repeat=R):
            if not any(signs):
                continue
            for rho, rho_f, q in [(0.5, 0.5, 1), (0.5, 0.5, 193), (0.25, 0.125, 3)]:
                dz = rho * np.array(signs, dtype=float).reshape(R, 1)
                v = choose_future(dz, rho_f)
                mu = (1 + v[::-1]).reshape(-1) / math.sqrt(n)
                val = np.linalg.norm(direct_coefficients(dz, mu, q))
                lower = q * R * rho_f * np.abs(dz).sum() / (2*n) - R*np.linalg.norm(dz)/math.sqrt(n)
                min_slack = min(min_slack, val - lower)
                assert val >= lower - 1e-12
                best = max(np.linalg.norm(direct_coefficients(dz, np.array(vv)/math.sqrt(n), q))
                           for vv in itertools.product([1-rho_f, 1], repeat=n))
                if val / best < worst_ratio:
                    worst_ratio = val / best
                    witness = {"R": R, "signs": signs, "rho": rho, "rho_f": rho_f,
                               "q": q, "sign_value": val, "optimal_vertex_value": best}
                # Independent full-history forward derivative for all tiny ternary histories.
                if R <= 3 and q != 193:
                    z1, z2 = (-rho+dz)/2, (-rho-dz)/2
                    fut = list(v) + [np.zeros(m)]
                    _, J1 = forward(schedule(z1, q)+fut, R, m)
                    _, J2 = forward(schedule(z2, q)+fut, R, m)
                    got = (J1-J2).T @ (np.ones(n)/math.sqrt(n))
                    assert np.max(np.abs(got-direct_coefficients(dz, mu, q))) < 1e-12
                cases += 1
    return {"cases": cases, "min_lower_bound_slack": min_slack,
            "worst_sign_query_over_optimal_vertex": worst_ratio, "witness": witness}


def finite_differences_and_source():
    rows = []
    for R, m, q in [(1, 2, 1), (2, 2, 3), (3, 2, 4), (4, 1, 7)]:
        n = R*m
        theta = rng.uniform(-1, 1, (R, m))
        dz = -0.5*theta
        v = choose_future(dz, 0.5)
        future = list(v) + [np.zeros(m)]
        sigma, nt = 0.05, 2*n
        projections, biasgrads = [], []
        fd_bias_err = fd_source_err = prep_bound_ratio = 0.0
        for side in [1, -1]:
            z = -0.25*(1+side*theta)
            xx = schedule(z, q)+future
            _, J = forward(xx, R, m)
            gb = J.T @ (np.ones(n)/math.sqrt(n))
            biasgrads.append(gb)
            for k in range(n):
                e = np.eye(n)[k]*1e-6
                h1, _ = forward(xx, R, m, bias=e)
                h2, _ = forward(xx, R, m, bias=-e)
                fd = (h1-h2).sum()/(2e-6*math.sqrt(n))
                fd_bias_err = max(fd_bias_err, abs(fd-gb[k]))
            # Source preparation explicitly precedes memory accumulation.
            xx = [np.zeros(m)]*R + xx
            src = np.zeros((len(xx), n))
            for r in range(R):
                src[r, r*m:(r+1)*m] = sigma
            before = np.vstack([np.zeros(n), np.cumsum(src, axis=0)[:-1]])
            injection = before.sum(axis=1)/math.sqrt(n)
            _, J = forward(xx, R, m, injection=injection)
            projected = J.T @ (np.ones(n)/math.sqrt(nt)) / nt
            projections.append(projected)
            fs = np.ones(n)/math.sqrt(n)
            for k in range(n):
                K = np.outer(np.eye(n)[k], fs)*1e-6
                h1, _ = forward(xx, R, m, coupling=K, source_inputs=src)
                h2, _ = forward(xx, R, m, coupling=-K, source_inputs=src)
                fd = (h1-h2).sum()/(2e-6*math.sqrt(nt)*nt)
                fd_source_err = max(fd_source_err, abs(fd-projected[k]))
        mu = (1+v[::-1]).reshape(-1)/math.sqrt(nt)
        main = sigma*math.sqrt(n)*direct_coefficients(dz, mu, q)/nt
        prep = projections[0]-projections[1]-main
        prep_bound = sigma*math.sqrt(n)*R*np.linalg.norm(dz)/math.sqrt(nt)/nt
        prep_bound_ratio = np.linalg.norm(prep)/prep_bound
        val = np.linalg.norm(projections[0]-projections[1])
        bound = sigma*math.sqrt(n)/nt*(q*R*0.5*np.abs(dz).sum()/(2*math.sqrt(nt*n))
                                        -2*R*np.linalg.norm(dz)/math.sqrt(nt))
        assert val >= bound-1e-12 and prep_bound_ratio <= 1+1e-12
        assert fd_bias_err < 2e-7 and fd_source_err < 2e-8
        rows.append({"R": R, "m": m, "q": q, "bias_fd_error": fd_bias_err,
                     "source_projection_fd_error": fd_source_err,
                     "prep_error_over_bound": prep_bound_ratio,
                     "projected_pair_distance": val, "sample_inequality": bound})
    return rows


def long_accumulation_source():
    rows = []
    for R, m in [(1, 2), (3, 2), (5, 3)]:
        n, q, sigma = R*m, 193, .05
        theta = rng.choice([-1., 1.], (R,m))
        dz = -.5*theta
        v = choose_future(dz,.5)
        gradients = []
        for side in [1,-1]:
            xs = [np.zeros(m)]*R + schedule(-.25*(1+side*theta),q)
            endpoint, _ = forward(xs,R,m)
            assert np.max(np.abs(endpoint)) == 0
            xs += list(v)+[np.zeros(m)]
            # s_(t-1) is ramped by exactly m source writes each prep step.
            c = sigma*math.sqrt(n)*np.minimum(np.arange(len(xs))/R,1)
            _, J = forward(xs,R,m,injection=c)
            gradients.append(J.T @ (np.ones(n)/math.sqrt(2*n))/(2*n))
        distance = np.linalg.norm(gradients[0]-gradients[1])
        lower = sigma*math.sqrt(n)/(2*n)*(q*R*.5*np.abs(dz).sum()/(2*math.sqrt(2*n*n))
                                             -2*R*np.linalg.norm(dz)/math.sqrt(2*n))
        assert distance >= lower > 0
        rows.append({"R":R,"m":m,"q":q,"full_forward_tangent_distance":distance,
                     "positive_sample_bound":lower})
    return rows


def code_and_boundary():
    # D=2: enumerate all angular breakpoints |g.y|=1/4 exactly up to float64,
    # plus each intervening interval; unlike random samples, covers every cell.
    N, D = 2000, 2
    G = rng.choice([-1., 1.], (N, D))
    events = []
    for row in np.unique(G, axis=0):
        phi = math.atan2(row[1], row[0])
        for value in [-0.25, 0.25]:
            alpha = math.acos(value/math.sqrt(2))
            events.extend([(phi+alpha)%(2*math.pi), (phi-alpha)%(2*math.pi)])
    events = sorted(set(events))
    angles = events + [(events[i]+(events[(i+1)%len(events)]+(2*math.pi if i+1==len(events) else 0)))/2 for i in range(len(events))]
    fractions = [float(np.mean(np.abs(G@np.array([math.cos(a),math.sin(a)])) >= .25-1e-12)) for a in angles]
    # With D=2, four possible rows reduce the continuous minimum to these cells.
    assert min(fractions) >= 1/16
    # Continuous-sphere search: axes, balanced pairs, row-null directions,
    # least singular vector, and seeded samples. Diagnostic, not a certificate.
    N3, D3 = 3000, 3
    G3 = rng.choice([-1.,1.], (N3, D3))
    ys = list(np.eye(D3))
    ys += [np.array(s, dtype=float) for s in itertools.product([-1,0,1], repeat=D3) if any(s)]
    _, _, vh = np.linalg.svd(G3, full_matrices=False)
    ys += [vh[-1]]
    ys += list(rng.normal(size=(200, D3)))
    ys = [y/np.linalg.norm(y) for y in ys]
    minfrac = min(np.mean(np.abs(G3@y) >= .25) for y in ys)
    # A deliberately bad G defeats the unjustified claim "any random draw is certified".
    bad = np.ones((2000, 2))
    bady = np.array([1.,-1.])/math.sqrt(2)
    badsat = int(np.sum(np.abs(bad@bady) >= .25))
    assert badsat == 0
    # n=2002, m=2, R=1001 meets Theorem 5.4 exactly. D=2 code has
    # cell-certified thickness, and sampled boundary gradients test the bound.
    R, m, q, n = 1001, 2, 193, 2002
    lower = .5*R*(q*.5*(n-D)/(32*n)-1)
    gaps = []
    for angle in angles + list(np.linspace(0, 2*math.pi, 100, endpoint=False)):
        y = np.array([math.cos(angle), math.sin(angle)])
        theta = np.r_[np.clip(4*G@y, -1, 1), y].reshape(R,m)
        dz = -.5*theta
        mu = (1+choose_future(dz,.5)[::-1]).reshape(-1)/math.sqrt(n)
        gaps.append(float(np.linalg.norm(direct_coefficients(dz,mu,q))))
    assert min(gaps) >= lower
    return {"D2_N": N, "D2_min_saturated_fraction_over_all_angular_cells": min(fractions),
            "D3_N": N3, "D3_adversarial_directions": len(ys), "D3_min_sample_fraction": float(minfrac),
            "bad_matrix_saturated_count": badsat, "bad_matrix_null_direction": bady.tolist(),
            "theorem_regime_boundary_checks": {"n": n, "D": D, "R": R, "m": m,
               "min_sample_gap": min(gaps), "uniform_proved_bound": lower,
               "note": "Algebra evaluated via independently checked coefficient formula; not full trajectory."}}


def constants_rounding_and_scope():
    op_squared = 8*(1.001*math.log(9)+1)
    exp_rate = 1/128-math.log(241)/1000
    failure520 = math.exp(-exp_rate*520)+2*math.exp(-520)
    assert math.sqrt(op_squared) < 5.06
    assert 16*op_squared/120**2 < 1/16
    assert failure520 < 1
    n = 1000999
    R, m = math.isqrt(n), n//math.isqrt(n)
    D = (m*R)//1001
    assert D*1002 < n
    violations, corrected_min = 0, math.inf
    for width in range(1000000, 1100000):
        rr = math.isqrt(width)
        dd = (width//rr*rr)//1001
        violations += dd*1002 < width
        corrected_min = min(corrected_min, dd*1004/width)
    assert corrected_min >= 1
    # Reach a negative gate in the LITERAL nonexpansive Q_ne set? No:
    # from [-1,0], w(u) is in [-1/2,0]; input >=-1/2 keeps state >=-1.
    # Negative future inputs achieve the boundary -1 only as a limit of cycles.
    hmin = 0.
    for _ in range(100):
        hmin = hmin+.5*hmin*hmin-.5
        assert -1 <= hmin <= 0
    # Trace deficit alone does not give a directional contraction bound.
    a = 199/200
    previous = np.array([-.05/a, 0.])
    gates = 1-previous**2
    assert np.dot(gates*np.array([0.,1.]), gates*np.array([0.,1.])) == 1
    return {"operator_norm_squared_coefficient": op_squared,
            "transfer_fraction": 16*op_squared/120**2,
            "failure_exponent_coefficient": exp_rate, "failure_bound_at_520": failure520,
            "nonvacuous_N_min": 1000,
            "bias_gap_coefficient": .5*(193/64.064-1),
            "transplant_margin": .05/(2*math.sqrt(2))*.5*(193/64.064-2),
            "rounding_counterexample": {"n": n,"R":R,"m":m,"n_prime":m*R,"D":D,"n_over_1002":n/1002},
            "floor_violations_in_first_100000_widths": violations,
            "corrected_D_over_n_over_1004_min_in_scan": corrected_min,
            "lemma8_reference_squared_threshold": (.05-math.atanh(.01))**2,
            "trace_deficit_example": {"previous":previous.tolist(),"trace_deficit":float(np.sum(previous**2)),
                                     "orthogonal_credit_gate_gain": 1.0}}


def main():
    start = time.perf_counter()
    results = {"environment": {"python": platform.python_version(),"numpy":np.__version__,
                              "seed":SEED,"threads":1,"author_code_imported":False}}
    for name, fn in [("exact",rational_checks), ("signs",exhaustive_signs),
                     ("finite_difference_and_source",finite_differences_and_source),
                     ("long_accumulation_source",long_accumulation_source),
                     ("code",code_and_boundary), ("constants",constants_rounding_and_scope)]:
        results[name] = fn()
        print(name+": "+json.dumps(results[name]), flush=True)
    results["runtime_seconds"] = time.perf_counter()-start
    results["status"] = "PASS: scoped identities and bounds; literal floor counterexample reproduced"
    Path(__file__).with_name("independent_results.json").write_text(
        json.dumps(results,indent=2)+"\n", encoding="utf-8", newline="\n")
    print(results["status"]+f" ({results['runtime_seconds']:.2f}s)")


if __name__ == "__main__":
    main()
