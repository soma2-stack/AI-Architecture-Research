"""Development-only tests. No historical code or numerical output is imported."""
import unittest
import numpy as np
from scipy.linalg import helmert
from independent import Family, Difference, GHI, GLO, profiles, section_basis, box_lower, single_pulse


class IndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = Family(24)

    def test_householder_rotation_and_period(self):
        f = self.f
        self.assertLess(np.max(abs(f.O.T @ f.O - np.eye(f.k))), 5e-15)
        self.assertLess(np.max(abs(np.linalg.matrix_power(f.O, f.d) - np.eye(f.k))), 2e-14)
        self.assertLess(np.max(abs(f.O[:, 0] - np.eye(f.k)[:, 0])), 2e-15)
        v = np.random.default_rng(5).normal(size=(f.k, 7))
        self.assertLess(np.max(abs(f.rotate(v) - f.O @ v)), 5e-15)
        self.assertLess(np.max(abs(f.rotate(v, True) - f.O.T @ v)), 5e-15)

    def test_leak_and_zero_sum_stationarity(self):
        f = self.f
        ck = 1 / (np.sqrt(f.k) - 1)
        ell = np.full(f.k, -ck ** 2)
        ell[0] += ck ** 2
        ell[1] += ck
        for c in range(f.d, f.k):
            self.assertLess(np.max(abs(f.O[:, c] - np.eye(f.k)[:, c] - ell)), 2e-15)
        u = np.r_[np.zeros(f.d), np.arange(f.k - f.d, dtype=float)]
        u[f.d:] -= np.mean(u[f.d:])
        self.assertLess(np.max(abs(f.O @ u - u)), 2e-15)

    def test_geometric_and_binary_warmup(self):
        f = self.f
        direct = np.zeros((f.k, f.k))
        for _ in range(3 * f.n):
            direct = f.a * f.O @ direct + np.eye(f.k)
        self.assertLess(np.max(abs(direct - f.warm_reference)), 8e-13)
        gate = np.r_[np.ones(f.k), np.full(f.l, .84)]
        B = np.zeros_like(f.E)
        for _ in range(3 * f.n):
            B = gate[:, None] * (f.R @ B + f.E)
        self.assertLess(np.max(abs(B - f.warm_actual())), 2e-13)

    def test_bptt_selected_group_and_frozen_cpu(self):
        import torch
        torch.set_num_threads(4)
        torch.set_default_dtype(torch.float64)
        f = self.f
        old = f.R.copy()
        rng = np.random.default_rng(7)
        hs = [np.zeros(f.n)]
        hs += [np.r_[rng.uniform(-.06, .06, f.k), np.full(f.l, .4)] for _ in range(8)]
        hs += [np.zeros(f.n)]
        xs = [np.arctanh(hs[t]) - f.R @ hs[t - 1] - .05 for t in range(1, len(hs))]
        R = torch.tensor(f.R, device="cpu", requires_grad=True)
        h = torch.zeros(f.n, device="cpu")
        for x in xs:
            h = torch.tanh(R @ h + torch.tensor(x, device="cpu") + .05)
        xi = rng.normal(size=f.n)
        loss = h @ torch.tensor(xi, device="cpu")
        grad, = torch.autograd.grad(loss, R)
        B = np.zeros_like(f.E)
        for t, state in enumerate(hs[1:], 1):
            B = (1 - state ** 2)[:, None] * (f.R @ B + (0 if t == 1 else 1) * f.E)
        expected = np.outer(B.T @ xi, np.full(f.l, .4))
        got = grad[1:f.k, f.k:].detach().numpy()
        self.assertLess(np.linalg.norm(got - expected) / np.linalg.norm(expected), 3e-14)
        self.assertEqual(str(R.device), "cpu")
        self.assertEqual(str(h.device), "cpu")
        self.assertTrue(np.array_equal(old, f.R))
        self.assertLess(float(h.detach().abs().max()), 1e-14)

    def test_matrix_free_sensitivity_and_adjoint(self):
        f = self.f
        rng = np.random.default_rng(9)
        hp = rng.uniform(-.2, .2, size=(7, f.k))
        hm = rng.uniform(-.2, .2, size=(7, f.k))
        op = Difference(f, hp, hm)
        matrix = op.matvec(np.eye(f.r))
        v, w = rng.normal(size=f.r), rng.normal(size=f.k)
        self.assertLess(abs(w @ op.matvec(v) - v @ op.rmatvec(w)), 2e-12)
        self.assertLess(np.max(abs(matrix @ v - op.matvec(v))), 2e-13)
        self.assertLess(np.max(abs(matrix.T @ w - op.rmatvec(w))), 2e-13)

    def test_joint_section_and_actual_query(self):
        f = self.f
        Q, Z = section_basis(f, 9, 4, 10)
        self.assertLess(np.max(abs(Q.T @ Q - np.eye(4))), 2e-15)
        self.assertLess(np.max(abs(Z.sum(axis=0))), 2e-15)
        rng = np.random.default_rng(11)
        C = rng.normal(size=(4, f.d - 1)); C /= np.linalg.norm(C)
        hp, radius = profiles(f, Q, Z, C, "total-budget", "spread")
        hm, _ = profiles(f, Q, Z, -C, "total-budget", "spread")
        self.assertLess(np.max(abs(hp[:, 0])), 2e-15)
        maximum, endpoint, _ = f.history_check(hp)
        self.assertLess(maximum, .5)
        self.assertLess(endpoint, 1e-14)
        self.assertGreater(radius, 0)
        low, g = box_lower(f, Difference(f, hp, hm), rng)
        v = np.arccosh(1 / np.sqrt(g)) - .05
        self.assertGreaterEqual(float(v.min()), .2 - 1e-14)
        self.assertLessEqual(float(v.max()), .45 + 1e-14)
        xi = f.R.T @ (1 - np.tanh(v + .05) ** 2) / (f.beta * np.sqrt(f.n))
        answer = f.wR * f.Hnorm * np.linalg.norm(Difference(f, hp, hm).rmatvec(xi[:f.k]))
        self.assertAlmostEqual(low, max(0., answer - 2 * f.eta), places=13)

    def test_spread_chart_is_not_fictitious_stationary_gate(self):
        f = self.f
        z = np.zeros(f.k)
        z[:f.d] = np.arange(f.d) / 100
        z[:f.d] -= z[:f.d].mean()
        h = f.house(z)
        hn = f.rotate(h)
        mismatch = (1 - hn ** 2)[:, None] * f.O - f.O * (1 - h ** 2)[None, :]
        self.assertGreater(np.linalg.norm(mismatch), 1e-5)

    def test_pulse_affine_whole_section_not_tangent(self):
        f = self.f
        rng = np.random.default_rng(12)
        V = f.R @ f.warm_actual() + f.E
        ids = np.arange(f.d, f.d + 2 * ((f.k - f.d) // 2))
        Q = helmert(len(ids), full=False).T
        u = Q @ rng.normal(size=Q.shape[1]); u /= np.linalg.norm(u)
        signs = np.tile([1., -1.], len(ids) // 2)
        def endpoint(u):
            z = np.zeros(f.k); z[ids] = signs * np.sqrt(.08 * (1 + u))
            g = np.r_[1 - z ** 2, np.full(f.l, .84)]
            return f.R @ (g[:, None] * V) + f.E
        pred = -.16 * f.R[:, ids] @ (u[:, None] * V[ids])
        self.assertLess(np.max(abs(endpoint(u) - endpoint(-u) - pred)), 2e-14)


if __name__ == "__main__":
    unittest.main(verbosity=2)
