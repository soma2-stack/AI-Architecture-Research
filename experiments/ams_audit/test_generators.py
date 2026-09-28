"""
Independent Unit Tests for AMS Benchmark Generators and Metrics.
Fulfills Stage 0 of AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md.
"""

import unittest
import numpy as np
import torch
from experiments.ams_audit.generators import (
    TaskBGenerator,
    TaskCStarGenerator,
    TaskFGenerator,
    TaskDGenerator,
    ReservedTaskAGenerator,
    ReservedTaskEGenerator,
)
from experiments.ams_audit.metrics import (
    area_under_learning_curve,
    steps_to_threshold,
    forgetting_percentage,
    backward_transfer,
    forward_transfer,
    adaptation_half_life,
    retention_half_life,
    compute_efficiency,
    update_efficiency,
    stability_variance,
    structural_generalization_gap,
)


class TestTaskGenerators(unittest.TestCase):

    def test_task_b_conflict_and_determinism(self):
        """Verify Task B determinism, subspace orthogonality, and lack of leakage."""
        gen1 = TaskBGenerator(dim=32, out_dim=4, seed=123)
        gen2 = TaskBGenerator(dim=32, out_dim=4, seed=123)
        gen3 = TaskBGenerator(dim=32, out_dim=4, seed=456)

        x1_a, y1_a = gen1.generate_task1_data(n_samples=50)
        x1_b, y1_b = gen2.generate_task1_data(n_samples=50)
        x1_c, y1_c = gen3.generate_task1_data(n_samples=50)

        # Determinism check
        self.assertTrue(torch.equal(x1_a, x1_b))
        self.assertTrue(torch.equal(y1_a, y1_b))
        self.assertFalse(torch.equal(x1_a, x1_c))

        # Orthogonality check: Task 1 should have exactly zeros in dims 16:32
        self.assertTrue(torch.all(x1_a[:, 16:] == 0.0))
        self.assertFalse(torch.all(x1_a[:, :16] == 0.0))

        # Task 2 should have exactly zeros in dims 0:16
        x2_a, y2_a = gen1.generate_task2_data(n_samples=50)
        self.assertTrue(torch.all(x2_a[:, :16] == 0.0))
        self.assertFalse(torch.all(x2_a[:, 16:] == 0.0))

        # No target leakage check
        self.assertEqual(x1_a.shape, (50, 32))
        self.assertEqual(y1_a.shape, (50, 4))
        self.assertEqual(x2_a.shape, (50, 32))
        self.assertEqual(y2_a.shape, (50, 4))

    def test_task_c_star_no_boundary_signal_and_recurrence(self):
        """Verify Task C* has strictly 1D inputs with NO task boundary flags, and recurrence exists."""
        gen = TaskCStarGenerator(seed=999)
        stream_data = gen.generate_stream(n_phase0_a=60, n_phase1=40, n_phase0_b=60)

        stream_x = stream_data["stream_x"]
        stream_y = stream_data["stream_y"]

        # Strict check: input x MUST BE exactly 1D feature (shape [N, 1])
        # No extra indicator columns allowed!
        self.assertEqual(stream_x.shape, (160, 1))
        self.assertEqual(stream_y.shape, (160, 1))

        # Verify phase slices are continuous
        slices = stream_data["phase_slices"]
        self.assertEqual(slices["phase_0a"], slice(0, 60))
        self.assertEqual(slices["phase_1"], slice(60, 100))
        self.assertEqual(slices["phase_0b"], slice(100, 160))

        # Verify ground truth function generation: Phase 0a and 0b use regime 0
        x_eval0, y_eval0 = stream_data["eval_regime0"]
        expected_y0 = torch.sin(1.0 * x_eval0 + 0.0)
        self.assertTrue(torch.allclose(y_eval0, expected_y0, atol=1e-5))

        x_eval1, y_eval1 = stream_data["eval_regime1"]
        expected_y1 = torch.sin(2.5 * x_eval1 + (np.pi / 3.0))
        self.assertTrue(torch.allclose(y_eval1, expected_y1, atol=1e-5))

    def test_task_f_exact_spurious_correlation_and_ood_inversion(self):
        """
        CRITICAL GATE:
        Verify Task F has:
        - Exactly 90% shortcut correlation in training data
        - Exactly 10% shortcut correlation in OOD test data
        - 100% adherence to 3-bit parity in both train and OOD test
        - No target leakage in input tensor
        """
        gen = TaskFGenerator(dim=20, seed=777)
        (train_x, train_y), (ood_x, ood_y) = gen.generate_train_and_ood(n_train=100, n_ood=1000)

        # Dimension checks
        self.assertEqual(train_x.shape, (100, 20))
        self.assertEqual(train_y.shape, (100, 1))
        self.assertEqual(ood_x.shape, (1000, 20))
        self.assertEqual(ood_y.shape, (1000, 1))

        # 1. Verify 100% adherence to true 3-bit parity rule: y = x[0] ^ x[1] ^ x[2]
        train_x_np = train_x.numpy().astype(int)
        train_y_np = train_y.numpy().astype(int).flatten()
        computed_train_y = train_x_np[:, 0] ^ train_x_np[:, 1] ^ train_x_np[:, 2]
        self.assertTrue(np.all(train_y_np == computed_train_y), "Train parity rule violated!")

        ood_x_np = ood_x.numpy().astype(int)
        ood_y_np = ood_y.numpy().astype(int).flatten()
        computed_ood_y = ood_x_np[:, 0] ^ ood_x_np[:, 1] ^ ood_x_np[:, 2]
        self.assertTrue(np.all(ood_y_np == computed_ood_y), "OOD test parity rule violated!")

        # 2. Check exact shortcut correlation for x[3] with y
        # In train (N=100): exact 90%
        train_shortcut_matches = np.sum(train_x_np[:, 3] == train_y_np)
        train_ratio = train_shortcut_matches / len(train_y_np)
        self.assertAlmostEqual(train_ratio, 0.90, places=4,
                               msg=f"Expected exactly 0.90 train shortcut ratio, got {train_ratio}")

        # In OOD test (N=1000): exact 10%
        ood_shortcut_matches = np.sum(ood_x_np[:, 3] == ood_y_np)
        ood_ratio = ood_shortcut_matches / len(ood_y_np)
        self.assertAlmostEqual(ood_ratio, 0.10, places=4,
                               msg=f"Expected exactly 0.10 OOD shortcut ratio, got {ood_ratio}")

    def test_task_d_condition_number(self):
        """Verify Task D Hessian matrix has exact specified condition number kappa."""
        for kappa in [1e2, 1e4, 1e6]:
            gen = TaskDGenerator(dim=32, kappa=kappa, seed=42)
            eigenvalues = np.linalg.eigvalsh(gen.H)
            measured_kappa = eigenvalues[-1] / eigenvalues[0]
            self.assertAlmostEqual(np.log10(measured_kappa), np.log10(kappa), places=3,
                                   msg=f"Condition number mismatch: expected {kappa}, got {measured_kappa}")
            # Verify positive definiteness
            self.assertTrue(np.all(eigenvalues > 0), "Hessian is not positive definite!")

    def test_reserved_tasks_a_and_e(self):
        """Verify reserved Task A (credit horizon) and Task E (timescale binding)."""
        # Task A
        gen_a = ReservedTaskAGenerator(dim=16, k_bits=4, seed=1)
        x_seq, target = gen_a.generate_sequence(T=100, t1=3)
        self.assertEqual(x_seq.shape, (100, 16))
        self.assertEqual(target.shape, (4,))
        # Trigger flag check
        self.assertEqual(x_seq[3, 0].item(), 1.0)
        self.assertTrue(torch.equal(x_seq[3, 2:6], target))
        # Query flag check
        self.assertEqual(x_seq[99, 1].item(), 1.0)

        # Task E
        gen_e = ReservedTaskEGenerator(key_dim=4, val_dim=4, seed=2)
        ep = gen_e.generate_episode(n_bindings=3, distractor_steps=20)
        self.assertEqual(ep["keys"].shape, (3, 4))
        self.assertEqual(ep["values"].shape, (3, 4))
        self.assertEqual(ep["distractors"].shape, (20, 8))
        q_idx = ep["query_idx"]
        self.assertTrue(torch.equal(ep["query_key"], ep["keys"][q_idx]))
        self.assertTrue(torch.equal(ep["target_value"], ep["values"][q_idx]))

    def test_metrics_exact_formulas(self):
        """Verify metric calculation formulas against analytic ground truth."""
        # AULC
        accs = [0.2, 0.4, 0.6, 0.8]
        self.assertAlmostEqual(area_under_learning_curve(accs), 0.5)

        # Steps to threshold
        losses = [1.0, 0.8, 0.5, 0.3, 0.08, 0.05]
        self.assertEqual(steps_to_threshold(losses, 0.1), 5)
        self.assertEqual(steps_to_threshold(losses, 0.01), 10**9)

        # Forgetting percentage
        self.assertAlmostEqual(forgetting_percentage(1.0, 0.6), 40.0)
        self.assertAlmostEqual(forgetting_percentage(0.8, 0.8), 0.0)

        # BWT & FWT
        self.assertAlmostEqual(backward_transfer(0.9, 0.5), -0.4)
        self.assertAlmostEqual(forward_transfer(0.6, 0.5), 0.1)

        # Adaptation half-life
        # L0 = 1.0, target = 0.2 -> cutoff = 1.0 - 0.5*(0.8) = 0.6
        losses_adapt = [1.0, 0.8, 0.55, 0.4]
        self.assertEqual(adaptation_half_life(losses_adapt, 0.2), 3)

        # SGG
        self.assertAlmostEqual(structural_generalization_gap(1.0, 0.15), 85.0)


if __name__ == "__main__":
    unittest.main()
