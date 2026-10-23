"""E5 encoding regressions: CPU forward checks only; no optimizer or training.

Run from the repository root:
    python -m unittest discover -s experiments/efd -p 'test_e5_encoding.py' -v
"""
from collections import Counter
from pathlib import Path
import sys
import unittest

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e5_missing as e5


FACTS_A = [("v", 0, 1, 0), ("v", 2, 3, 0), ("c", 1, 1)]
FACTS_B = [("v", 0, 3, 0), ("v", 2, 1, 0), ("c", 1, 1)]


def inputs(facts):
    tok, fpos = e5.encode(facts, 0)
    return torch.tensor([tok]), torch.tensor([fpos])


class E5EncodingTests(unittest.TestCase):
    def test_opposite_answers_collide_under_old_token_role_representation(self):
        # Both fixtures are legal disjoint chains, including in E5b's zero-offset case.
        self.assertEqual(e5.solve(FACTS_A, 0), 1)
        self.assertEqual(e5.solve(FACTS_B, 0), e5.UNK)
        ta, pa = e5.encode(FACTS_A, 0)
        tb, pb = e5.encode(FACTS_B, 0)
        self.assertEqual(Counter(zip(ta, pa)), Counter(zip(tb, pb)))
        self.assertEqual(ta.index(e5.QRY), tb.index(e5.QRY))
        self.assertEqual(ta[-4:], [e5.QRY, 0, e5.PAD, e5.PAD])
        self.assertEqual(pa, [0, 1, 2, 3] * 4)
        self.assertEqual(pb, pa)
        # The swap crosses fact boundaries but preserves within-fact token roles.
        swapped = ta.copy()
        swapped[2], swapped[6] = swapped[6], swapped[2]
        self.assertEqual(swapped, tb)

    def test_legacy_attention_cannot_separate_counterexample(self):
        for seed in (0, 1, 2):
            with self.subTest(seed=seed), torch.random.fork_rng(devices=[]):
                torch.manual_seed(seed)
                model = e5.TF(d=32, layers=2).eval()
                # Reconstruct the original positionless attention as a negative control.
                for block in model.blocks:
                    block.pos = "none"
                with torch.inference_mode():
                    a, b = model(*inputs(FACTS_A)), model(*inputs(FACTS_B))
                torch.testing.assert_close(a, b, atol=1e-6, rtol=1e-6)

    def test_current_attention_can_separate_counterexample_without_training(self):
        for seed in (0, 1, 2):
            with self.subTest(seed=seed), torch.random.fork_rng(devices=[]):
                torch.manual_seed(seed)
                model = e5.TF(d=32, layers=2).eval()
                with torch.inference_mode():
                    a, b = model(*inputs(FACTS_A)), model(*inputs(FACTS_B))
                self.assertEqual(tuple(a.shape), (1, 11))
                self.assertTrue(torch.isfinite(a).all().item())
                self.assertTrue(torch.isfinite(b).all().item())
                self.assertFalse(torch.allclose(a, b, atol=1e-6, rtol=1e-6))
                # Different logits demonstrate distinguishability, not correct answers.

    def test_padding_does_not_change_query_logits(self):
        short_t, short_p = e5.encode(FACTS_A, 0)
        long_t, long_p = e5.encode(FACTS_B + [("c", 4, 2)], 0)
        padding = len(long_t) - len(short_t)
        tok = torch.tensor([short_t + [e5.PAD] * padding, long_t])
        fpos = torch.tensor([short_p + [0] * padding, long_p])
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(7)
            for model in (e5.TF(d=32, layers=2), e5.GRUm(d=32)):
                with self.subTest(model=type(model).__name__), torch.inference_mode():
                    model.eval()
                    batch = model(tok, fpos)
                    single_short = model(torch.tensor([short_t]), torch.tensor([short_p]))
                    single_long = model(torch.tensor([long_t]), torch.tensor([long_p]))
                    torch.testing.assert_close(batch[:1], single_short, atol=1e-6, rtol=1e-6)
                    torch.testing.assert_close(batch[1:], single_long, atol=1e-6, rtol=1e-6)


if __name__ == "__main__":
    unittest.main()
