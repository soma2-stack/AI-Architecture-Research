"""Cheap evaluation regressions. No training loops or model downloads."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e2_surface as e2
import e4_compose_fewshot as e4
import e7_repeat as e7
import e8_library as e8


class EvaluationValidityTests(unittest.TestCase):
    def test_e4_padding_is_not_evidence(self):
        rng = np.random.default_rng(5)
        short, _ = e4.episode(("R", "S"), rng)
        long, _ = e4.episode(("R", "S"), rng, K=5)
        tok = torch.tensor([short + [13] * (len(long) - len(short)), long])
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(3)
            for model in (e4.TFModel(d=32, layers=1), e4.GRUModel(d=32)):
                with self.subTest(model=type(model).__name__), torch.inference_mode():
                    model.eval()
                    single = model(torch.tensor([short]))
                    padded = model(tok)[:1]
                    torch.testing.assert_close(single, padded, atol=1e-6, rtol=1e-6)

    def test_e7_bfs_prediction_is_scored_against_labels(self):
        # A deliberately wrong label must lower even the classical reference score.
        x = torch.tensor([[[[0., 0.], [1., 0.]], [[1., 0.], [0., 0.]]]])
        wrong = torch.zeros(1, 2, 2)
        with mock.patch.object(e7, "batch", return_value=(x, wrong)) as batch:
            result = e7.job(("bfs", 1))
        self.assertEqual(batch.call_count, 4)
        for metrics in result["res"].values():
            self.assertEqual(metrics["solved"], 0.)

    def test_e7_bfs_connectivity(self):
        x = torch.tensor([[[[0., 1., 0.], [0., 1., 0.], [1., 0., 0.]],
                           [[1., 0., 0.], [0., 0., 0.], [0., 0., 0.]]]])
        expected = torch.tensor([[[True, False, False], [True, False, False], [False, False, False]]])
        self.assertTrue(torch.equal(e7.bfs_predict(x) > 0, expected))

    def test_e8_arms_get_identical_demonstrations(self):
        seen = []
        def search(demos, ops, lib, budget, **kwargs):
            seen.append(copy.deepcopy(demos))
            stats = kwargs.get("stats")
            if stats is not None:
                stats["programs_evaluated"] = stats.get("programs_evaluated", 0) + 1
                stats["primitive_steps"] = stats.get("primitive_steps", 0) + 1
            return ("R",), 1
        with mock.patch.object(e8, "search", side_effect=search):
            e8.job((1, 10))
        self.assertEqual(len(seen), 12 + 3 * 15)
        self.assertEqual(seen[12:27], seen[27:42])
        self.assertEqual(seen[12:27], seen[42:57])

    def test_e8_budget_counts_only_evaluated_programs(self):
        program, count = e8.search([([0] * 6, [8] * 6)], ["R"], {}, budget=2)
        self.assertIsNone(program)
        self.assertEqual(count, 2)

    def test_e8_macro_cost_counts_primitive_work(self):
        stats = {}
        program, count = e8.search([([0], [3])], ["A"], {"A": ("S", "S", "S")}, 1, stats=stats)
        self.assertEqual(program, ("A",))
        self.assertEqual(count, 1)
        self.assertEqual(stats["programs_evaluated"], 1)
        self.assertEqual(stats["primitive_steps"], 3)

    def test_e8_library_total_includes_acquisition_and_verification(self):
        def search(demos, ops, lib, budget, stats=None):
            stats["programs_evaluated"] += 1
            stats["primitive_steps"] += 2
            return ("R",), 1
        with mock.patch.object(e8, "search", side_effect=search):
            result = e8.job((1, 10))["res"]
        acq = result["acquisition"]
        self.assertEqual(acq["programs_evaluated"], 12)
        self.assertEqual(acq["primitive_steps"], 24)
        for arm in ("flat", "library"):
            row = result[arm]
            initial = acq["primitive_steps"] if arm == "library" else 0
            self.assertEqual(row["total_primitive_steps"], initial + row["search_primitive_steps"]
                             + row["verification_primitive_steps"])
            self.assertAlmostEqual(row["total_secs"], row["acquisition_secs"] + row["test_secs"])
            self.assertEqual(row["test_instances_sha256"], result["test_instances_sha256"])
        self.assertEqual(result["library"]["acquisition_secs"], acq["secs"])
        self.assertIsNone(result["oracle_lib"]["total_secs"])
        self.assertIsNone(result["oracle_lib"]["total_primitive_steps"])

    def test_e8_real_tiny_job_has_finite_reconciled_costs(self):
        result = e8.job((1, 3))
        json.dumps(result, allow_nan=False)
        for arm in ("flat", "library"):
            row = result["res"][arm]
            self.assertLessEqual(row["test_programs"], 15 * 3)
            self.assertGreaterEqual(row["total_primitive_steps"], row["search_primitive_steps"])
            self.assertGreaterEqual(row["total_secs"], row["acquisition_secs"])

    def test_e2_capped_enumeration_is_not_claimed_exhaustive(self):
        table = np.add.outer(np.arange(3), np.arange(3)) % 3
        with mock.patch.object(e2, "P", 3):
            _, count, details = e2.csp_predict(table, [], [(0, 1)], cap=2, return_details=True)
            self.assertEqual(count, 2)
            self.assertTrue(details["cap_reached"])
            self.assertFalse(details["enumeration_exhaustive"])
            _, count, details = e2.csp_predict(table, [], [(0, 1)], cap=10, return_details=True)
            self.assertEqual(count, 6)
            self.assertTrue(details["enumeration_exhaustive"])


if __name__ == "__main__":
    unittest.main()
