"""Exact checks for PROOF.md section 2.

(a) Prop. 2.2: for any credit matrix B' with zero row 0, nu = a O^T (HI 1_k) satisfies
    nu^T B'(:, c) = a HI sqrt(k) (U B')(d-1, c) for every column c.
(b) Prop. 2.3 (first-order separation): in the external probe's 8 histories (n = 256), the
    cross-memory second differences of K_pos, K_neg, K_uni, L_cyc, L_off, W, F_ent on each memory
    column vanish, and the whole interaction equals that of K_bus + L_bus.
Run: python -I exp_exact_checks.py   (writes exp_exact_checks_result.json)
"""
import itertools, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim

HI = 1 / math.cosh(.25) ** 2


def check_a():
    rng = np.random.default_rng(1); worst = 0.0
    for n in (64, 400):
        k, d = n // 2, n // 4; a = 1 - 1 / n
        gam = 1 / (1 - 1 / math.sqrt(k)); u = np.ones(k) / math.sqrt(k); w = -u.copy(); w[0] += 1
        U = np.eye(k) - gam * np.outer(w, w)
        P = np.zeros((k, k))
        for j in range(d - 1):
            P[j + 1, j] = 1
        P[0, d - 1] = 1
        for j in range(d, k):
            P[j, j] = 1
        O = U @ P @ U
        B = rng.normal(size=(k, k)); B[0] = 0
        nu = a * O.T @ (HI * np.ones(k))
        lhs = nu @ B; rhs = a * HI * math.sqrt(k) * (U @ B)[d - 1]
        worst = max(worst, float(np.abs(lhs - rhs).max() / np.abs(lhs).max()))
    return worst


def check_b(n=256, off=(0, 0, 0)):
    runs = {}
    for b in itertools.product((0, 1), repeat=3):
        T, cols, f = m3sim.probe_schedule(n, b, off)
        runs[b] = m3sim.run(n, T, cols, f)
    first = ("Kpos", "Kneg", "Kuni", "Lcyc", "Loff", "W", "Fent")
    worst_first = 0.0; worst_match = 0.0
    for i in range(3):
        for i2 in range(3):
            if i2 == i:
                continue
            for rest in (0, 1):
                def bits(bi, bj):
                    v = [rest] * 3; v[i] = bi; v[i2] = bj; return tuple(v)
                sd = lambda nm: (runs[bits(1, 1)]["parts"][nm][i] - runs[bits(0, 1)]["parts"][nm][i]
                                 - runs[bits(1, 0)]["parts"][nm][i] + runs[bits(0, 0)]["parts"][nm][i])
                worst_first = max(worst_first, max(abs(sd(nm)) for nm in first))
                z = (runs[bits(1, 1)]["Z"][i] - runs[bits(0, 1)]["Z"][i] - runs[bits(1, 0)]["Z"][i] + runs[bits(0, 0)]["Z"][i])
                worst_match = max(worst_match, abs(z - sd("Kbus") - sd("Lbus")))
    return worst_first, worst_match


def main():
    ra = check_a(); rb = check_b()
    out = {"a_uniform_query_identity_rel_residual": ra,
           "b_first_order_second_difference_max": rb[0],
           "b_interaction_minus_second_order_max": rb[1]}
    print(json.dumps(out))
    json.dump(out, open(os.path.join(HERE, "exp_exact_checks_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
