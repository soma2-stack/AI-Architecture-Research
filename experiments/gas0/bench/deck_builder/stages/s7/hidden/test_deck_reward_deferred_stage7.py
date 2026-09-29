from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import offer_rewards

def test_deferred_reward_rule_is_enforced():
    battle = create_battle([])
    cards = [Card(str(i), str(i), 1) for i in range(5)]
    offer = offer_rewards(battle, cards)
    assert len(offer) == 3 and len({card.card_id for card in offer}) == 3
