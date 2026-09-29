from deckgame.game import create_battle
from deckgame.model import Card
from deckgame.rewards import choose_reward, offer_rewards

def test_offer_has_frozen_count_and_distinct_ids():
    battle = create_battle([])
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    offer = offer_rewards(battle, cards)
    assert len(offer) == 3
    assert len({card.card_id for card in offer}) == 3

def test_offer_is_repeatable_for_same_seed():
    cards = [Card(str(i), str(i), 1) for i in range(6)]
    a, b = create_battle([]), create_battle([])
    a.seed = b.seed = 21
    assert [x.card_id for x in offer_rewards(a, cards)] == [x.card_id for x in offer_rewards(b, cards)]

def test_unoffered_reward_cannot_be_chosen():
    battle = create_battle([])
    offer_rewards(battle, [Card(str(i), str(i), 1) for i in range(4)])
    try:
        choose_reward(battle, "missing")
    except ValueError:
        pass
    else:
        raise AssertionError("unoffered reward was accepted")
