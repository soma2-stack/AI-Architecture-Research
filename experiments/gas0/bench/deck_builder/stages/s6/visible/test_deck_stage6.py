from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rng import RunRNG

def test_run_rng_is_repeatable():
    first, second = RunRNG(44), RunRNG(44)
    a = [Card(str(i), str(i), 1) for i in range(5)]
    b = list(a)
    first.shuffle(a)
    second.shuffle(b)
    assert [card.card_id for card in a] == [card.card_id for card in b]
