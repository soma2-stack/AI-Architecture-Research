# E5 fact-membership repair

Status: encoding defect reproduced and repaired; no model was trained or evaluated
for task accuracy as part of this repair. This is an experimental-validity fix,
not evidence of improved reasoning or a new architecture.

## Historical results

`e5_results.json` and `e5b_results.json` are preserved byte for byte. Their
Transformer rows used only token embeddings and repeated within-fact role
embeddings, with positionless full attention. This loses which tokens belong to
the same fact. Those rows cannot support a claim that an adequately informed
Transformer cannot solve the task. Do not relabel them as repaired-model scores.
This defect also affects the E5b equality-only variant of the same script.

The GRU and union-find implementations are unchanged. This encoding finding
neither invalidates their recorded measurements nor establishes that their other
experimental assumptions are sound.

## Reproduced counterexample

Query `v0` in these two legal disjoint-chain inputs (all offsets are zero):

| Input | Facts | Correct answer |
| --- | --- | --- |
| A | `v0 = v1; v2 = v3; v1 = 1` | `1` |
| B | `v0 = v3; v2 = v1; v1 = 1` | `UNKNOWN` (class 10) |

Swapping token positions 2 and 6 changes A into B while preserving the multiset
of `(token, within-fact role)` pairs, the padding mask under the same permutation,
and the query position. Without sequence positions, full attention is permutation
equivariant: the fixed query has the same mathematical output for any weights.
Floating-point differences are not usable evidence of distinguishability.

Before the repair, the regression's distinguishability check failed for all three
fixed initializations (0, 1, 2), while the counterexample and legacy-collision
checks passed. No optimizer, backward pass, or training loop was used.

## Smallest encoding change

The E5 Transformer now selects `Block(..., "rope", causal=False)` instead of
`Block(..., "none", causal=False)`, reusing the existing rotary position encoding
in `common.py`. RoPE makes attention depend on relative token positions. Together
with the existing within-fact roles and four-token serialization, this removes
the cross-fact token-permutation symmetry behind the counterexample. It adds no
trainable parameters, learned fact-ID table, or fixed maximum sequence length.

Whole-fact order is still shuffled by the unchanged generator. The repaired
Transformer is sensitive to that order; its ability to generalize across shuffled
orders must be measured in a fresh run. Distinct untrained logits do not show
correct answers, trainability, or a solution to every identifiability issue.

The fact generator, tokenization, role IDs, labels, UNKNOWN class, padding mask,
query readout, loss, optimizer, schedules, training steps, seeds, evaluation
examples, and exact-answer accuracy calculation are unchanged. The GRU,
union-find solver, and shared `common.py` are unchanged. No success threshold was
added or relaxed.

Future normal runs write `e5_rope_results.json` or `e5b_rope_results.json` so that
the original files are not overwritten. Existing command-line behavior is
otherwise unchanged; `quick` includes training and is not a regression command.

## Verification without training

From the repository root, with NumPy and PyTorch installed:

```bash
python -m unittest discover -s experiments/efd -p 'test_e5_encoding.py' -v
E5B=1 python -m unittest discover -s experiments/efd -p 'test_e5_encoding.py' -v
```

The suite checks the opposite labels and original representation collision,
reconstructs the old attention as a negative control, checks that the repaired
model can distinguish the pair across three initializations, and checks query
logits with mixed-length padded batches for both neural models. All checks use
CPU forward inference only. The fixtures are valid for both E5 and E5b.

Verified on Python 3.12.14 / PyTorch 2.14.1+cpu, with one CPU thread:

- All four regression tests pass in default mode and with `E5B=1`.
- The actual default-size Transformer has 1,195,659 parameters before and after
  the repair. Maximum absolute query-logit differences for A versus B were:

  | Initialization seed | Original attention | Repaired attention |
  | --- | ---: | ---: |
  | 0 | 2.38e-7 | 0.01575 |
  | 1 | 3.58e-7 | 0.01417 |
  | 2 | 2.98e-7 | 0.00966 |

- An AST comparison against `a9a644712f16a566f058c63446a0bd7bc8521b79`
  confirms that the only executable changes are the attention-position mode
  and output filenames. The other source change is documentation.
- Original result bytes match their Git blob IDs:
  `e5_results.json`: `36db3f54ba1dd7a9d280ea8950bc621e3ea7a017`;
  `e5b_results.json`: `f4c1086bca3bac07126b4961568348611c9100c1`.

## What still requires a fresh run

Retrain the repaired Transformer under the original budgets and seeds, then run
the original ID and hop-distance evaluation and retain every result, including
failures. Report repaired results separately from the historical files. Until
then, the effect on accuracy and the neural-versus-solver comparison are unknown.
