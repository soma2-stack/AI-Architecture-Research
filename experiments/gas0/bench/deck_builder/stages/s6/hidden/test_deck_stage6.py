from deckgame.rng import RunRNG
from deckgame.model import Card

def test_rng_instances_have_independent_replay():
    a, b, c = RunRNG(5), RunRNG(5), RunRNG(5)
    values = list(range(10))
    assert a.sample(values, 4) == b.sample(values, 4) == c.sample(values, 4)

def test_sampling_is_without_replacement():
    result = RunRNG(7).sample([Card(str(i), str(i), 1) for i in range(8)], 5)
    assert len({card.card_id for card in result}) == 5

def test_battle_instances_own_seeded_streams():
    from deckgame.game import create_battle
    a, b = create_battle([], seed=33), create_battle([], seed=33)
    values = [Card(str(i), str(i), 1) for i in range(6)]
    assert a.rng.sample(values, 3) == b.rng.sample(values, 3)
