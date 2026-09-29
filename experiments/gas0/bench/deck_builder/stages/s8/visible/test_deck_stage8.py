from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.save import load_battle, save_battle

def test_round_trip_preserves_piles_and_poison():
    battle = create_battle([Card("x", "X", 1)], hp=17)
    battle.poison = 2
    restored = load_battle(save_battle(battle))
    assert restored.hp == 17 and restored.poison == 2
    assert restored.deck.draw_pile[0].card_id == "x"
