"""Small algebra cross-checks for the new scoped contraction obstruction."""
import unittest
from fractions import Fraction as F
import numpy as np
from independent import Family
from adversary import active_basis


class ScopedTests(unittest.TestCase):
    def test_projection_gram_and_gate_comparison(self):
        f = Family(24)
        V = active_basis(f)
        O = V.T @ f.O @ V
        e = np.eye(f.d)[:, -1]
        fast = np.eye(f.d) - np.outer(e, e)
        q = e @ O @ e
        gram = fast + O.T @ fast @ O
        self.assertAlmostEqual(np.linalg.eigvalsh(gram)[0], 1 - abs(q), places=13)
        gb = .99 * fast + np.outer(e, e)
        bound = np.sqrt(1 - (1 - .99 ** 2) * (1 - abs(q)) / 1.01 ** 2)
        self.assertLessEqual(np.linalg.norm(gb @ O @ gb, 2), bound + 1e-14)
        rng = np.random.default_rng(18)
        for _ in range(12):
            g1 = np.diag(np.r_[rng.uniform(.84, .99, f.d - 1), rng.uniform(.95, 1.)])
            g2 = np.diag(np.r_[rng.uniform(.84, .99, f.d - 1), rng.uniform(.95, 1.)])
            self.assertLessEqual(np.linalg.norm(g2 @ O @ g1 @ O, 2), bound + 1e-14)

    def test_rational_constants_and_monotone_overlap_bounds(self):
        delta = F(199, 20402)
        self.assertLess(4 / delta + 1, 412)
        self.assertLess(F(3, 10) * 412 / 1000000 + F(1, 1000000) + F(2, 10 ** 9), F(1, 1000))
        for k in (100, 128, 200, 500, 10000):
            ck = 1 / (np.sqrt(k) - 1)
            for L in (k // 2, (k + 1) // 2):
                q = 1 - L * ck ** 2
                self.assertGreater(q, 0)
                self.assertLessEqual(q, .5 + 1e-14)


if __name__ == "__main__":
    unittest.main(verbosity=2)
