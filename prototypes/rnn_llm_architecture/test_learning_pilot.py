"""Fast CPU correctness checks; smoke training uses a local toy only here."""
import json

import pytest
import torch

from prototypes.rnn_llm_architecture import learning_pilot as pilot


def test_delayed_balance_and_no_query_leak():
    for d in (1, 16, 64):
        tokens, labels, meta = pilot.make_batch('delayed', d, 128, seed=31)
        assert tokens.shape == (128, d + 2)
        assert labels.sum() == 64
        assert torch.equal(tokens[:, 0] - pilot.BIT0, labels)
        assert (tokens[:, 1:-1] >= pilot.DISTRACTOR_START).all()
        assert (tokens[:, 1:-1] < pilot.DISTRACTOR_END).all()
        assert (tokens[:, -1] == pilot.QUERY).all()
        assert not meta['query_updated'].any()


def test_selective_replay_and_balancing():
    tokens, labels, meta = pilot.make_batch('selective', 16, 2048, seed=99)
    assert tokens.shape == (2048, 23)
    assert ((labels == 0) | (labels == 1)).all()
    assert abs(labels.float().mean().item() - 0.5) < .04
    assert abs(meta['query_updated'].float().mean().item() - .5) < .04
    for row, label in zip(tokens, labels):
        memory = {}
        for t in range(len(row) - 1):
            tok = int(row[t])
            if tok in (pilot.WRITE_A, pilot.WRITE_B):
                memory[tok] = int(row[t + 1]) - pilot.BIT0
        query = int(row[-1]) - pilot.QUERY_A + pilot.WRITE_A
        assert memory[query] == int(label)


def test_deterministic_and_disjoint_generators():
    a = pilot.make_batch('selective', 64, 32, seed=13)
    b = pilot.make_batch('selective', 64, 32, seed=13)
    c = pilot.make_batch('selective', 64, 32, seed=14)
    assert all(torch.equal(x, y) for x, y in zip(a[:2], b[:2]))
    assert not torch.equal(a[0], c[0])
    rng = torch.get_rng_state().clone()
    pilot.make_batch('selective', 64, 32, seed=91)
    assert torch.equal(rng, torch.get_rng_state())


def test_reject_bad_inputs_and_config():
    for values in ({'delays': (0,)}, {'width': 30}, {'models': ('missing',)}, {'steps': 0}):
        with pytest.raises(ValueError):
            pilot.PilotConfig(**values)
    with pytest.raises(ValueError):
        pilot.make_batch('missing', 16, 4, seed=1)


class TinyLearnable(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = torch.nn.Embedding(pilot.VOCAB_SIZE, 8)
        self.gru = torch.nn.GRU(8, 8, batch_first=True)
        self.head = torch.nn.Linear(8, pilot.VOCAB_SIZE)

    def forward(self, ids):
        h = self.gru(self.embedding(ids))[0]
        return self.head(h), None


def test_query_loss_is_trainable():
    torch.manual_seed(1)
    model = TinyLearnable()
    tokens, labels, _ = pilot.make_batch('delayed', 3, 16, seed=8)
    loss = pilot.query_loss(model, tokens, labels)
    loss.backward()
    assert torch.isfinite(loss)
    assert model.embedding.weight.grad.abs().sum() > 0


def test_bounded_training_and_output_protection(tmp_path, monkeypatch):
    monkeypatch.setattr(pilot, 'make_model', lambda name, config, seed: TinyLearnable())
    output = tmp_path / 'exp001.json'
    c = pilot.PilotConfig(models=('gru',), tasks=('delayed',), delays=(2,),
                          seeds=(17,), steps=2, batch_size=4, eval_batch=8,
                          max_wall_seconds=30)
    report = pilot.run_pilot(c, output=output)
    assert report['status'] == 'complete'
    assert report['runs'][0]['steps_completed'] == 2
    assert json.loads(output.read_text())['status'] == 'complete'
    with pytest.raises(FileExistsError):
        pilot.run_pilot(c, output=output)
