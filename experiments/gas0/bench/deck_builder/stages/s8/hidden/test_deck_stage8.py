from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import offer_rewards
from deckgame.save import load_battle, save_battle

def test_round_trip_preserves_random_continuation():
    battle = create_battle([])
    battle.seed = 19
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    offer_rewards(battle, cards)
    payload = save_battle(battle)
    expected = [card.card_id for card in offer_rewards(battle, cards)]
    restored = load_battle(payload)
    assert [card.card_id for card in offer_rewards(restored, cards)] == expected

def test_round_trip_preserves_poison_and_reward_offer():
    battle = create_battle([])
    battle.poison = 4
    cards = [Card(str(i), str(i), 1) for i in range(5)]
    offer_rewards(battle, cards)
    restored = load_battle(save_battle(battle))
    assert restored.poison == 4
    assert [card.card_id for card in restored.reward_offer] == [card.card_id for card in battle.reward_offer]
