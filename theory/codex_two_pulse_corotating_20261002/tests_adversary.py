import unittest
import numpy as np
import torch
from adversary import Family, Reduced, active_basis, profiles, Difference, section_basis


class ReducedTests(unittest.TestCase):
    def test_invariant_block_and_full_numerical_agreement(self):
        f = Family(24)
        Q, Z = section_basis(f, 12, 4, 12)
        C = np.random.default_rng(13).normal(size=(4, f.d - 1)); C /= np.linalg.norm(C)
        V = active_basis(f)
        self.assertLess(np.max(abs(V.T @ V - np.eye(f.d))), 2e-15)
        self.assertLess(np.max(abs(f.O @ V - V @ (V.T @ f.O @ V))), 2e-15)
        reduced = Reduced(f, Q, Z, "total-budget")
        value = float(reduced.objective(torch.tensor(C)).detach())
        hp, _ = profiles(f, Q, Z, C, "total-budget", "spread")
        hm, _ = profiles(f, Q, Z, -C, "total-budget", "spread")
        full = Difference(f, hp, hm).matvec(np.eye(f.r))
        expected = f.a * f.Hnorm / f.n * np.linalg.svd(full, compute_uv=False)[0] / .002
        self.assertLess(abs(expected - value), 2e-11)
        actual = 1 - hp ** 2
        self.assertLess(np.max(abs(actual[:, 1:f.d] - reduced.gates(torch.tensor(C)).numpy()[:, :-1])), 2e-15)
        self.assertLess(np.max(abs(actual[:, f.d:] - actual[:, f.d:f.d + 1])), 2e-15)

    def test_history_objective_gradient_finite_difference(self):
        f = Family(24)
        Q, Z = section_basis(f, 8, 3, 14)
        rng = np.random.default_rng(15)
        raw = rng.normal(size=(3, f.d - 1))
        direction = rng.normal(size=raw.shape); direction /= np.linalg.norm(direction)
        reduced = Reduced(f, Q, Z)
        x = torch.tensor(raw, requires_grad=True)
        g, = torch.autograd.grad(reduced.objective(x), x)
        e = 1e-5
        fd = float((reduced.objective(torch.tensor(raw + e * direction)) - reduced.objective(torch.tensor(raw - e * direction))).detach()) / (2 * e)
        expected = np.sum(g.detach().numpy() * direction)
        self.assertLess(abs(fd - expected) / max(1., abs(expected)), 2e-7)
        self.assertEqual(str(x.device), "cpu")


if __name__ == "__main__":
    unittest.main(verbosity=2)
