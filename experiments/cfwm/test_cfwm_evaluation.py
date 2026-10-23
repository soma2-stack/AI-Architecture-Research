"""CFWM evaluation accounting checks; no predicate training."""
from pathlib import Path
import sys
import unittest
from unittest import mock

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfwm_experiment as cfwm


class CFWMValidityTests(unittest.TestCase):
    def test_total_time_includes_precompute_training_and_diagnostics(self):
        clock = [0.]
        events = []
        class Planner:
            def __init__(self, *args):
                events.append("init")
            def precompute(self):
                events.append("precompute")
                clock[0] += 5.
                return self
        def evaluate(*args):
            events.append("search")
            clock[0] += 7.
            return {"secs": 7., "lost": 2, "longer": 1}
        with mock.patch.object(cfwm, "Planner", Planner), mock.patch.object(cfwm, "evaluate", evaluate), \
                mock.patch.object(cfwm.time, "perf_counter", side_effect=lambda: clock[0]):
            row = cfwm.evaluate_pipeline(None, [], "learned", 4, training_secs=11., diagnostic_secs=13.)
        self.assertEqual(events, ["init", "precompute", "search"])
        self.assertEqual(row["setup_secs"], 5.)
        self.assertEqual(row["pipeline_secs"], 12.)
        self.assertEqual(row["total_secs"], 36.)
        self.assertEqual(row["secs"], 7.)
        self.assertEqual((row["lost"], row["longer"]), (2, 1))

    def test_tiny_real_pipeline_without_training(self):
        world = cfwm.LineWorld(3, 1)
        tasks = [((0,), (2,), 2)]
        # Zero logits + threshold .99 means no learned pruning. No fitted weights.
        net = torch.nn.Linear(world.k * world.L + 2 * world.A, 1)
        with torch.no_grad():
            net.weight.zero_()
            net.bias.zero_()
        for mode in ("none", "oracle", "learned"):
            with self.subTest(mode=mode):
                row = cfwm.evaluate_pipeline(world, tasks, mode, 2, net=net, training_secs=0.)
                self.assertEqual((row["lost"], row["longer"], row["n"]), (0, 0, 1))
                self.assertGreaterEqual(row["total_secs"], row["setup_secs"])
                self.assertEqual(row["training_secs"], 0.)

    def test_unknown_training_cost_is_not_silently_zero(self):
        with mock.patch.object(cfwm, "Planner"), mock.patch.object(cfwm, "evaluate", return_value={"secs": 0.}):
            row = cfwm.evaluate_pipeline(None, [], "learned", 0, net=object())
        self.assertIsNone(row["training_secs"])
        self.assertIsNone(row["total_secs"])


if __name__ == "__main__":
    unittest.main()
