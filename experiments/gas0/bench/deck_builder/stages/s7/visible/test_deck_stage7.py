from deckgame.game import create_battle
from deckgame.render import next_card_label
from deckgame.rewards import choose_reward, offer_rewards
from deckgame.model import Card

def test_empty_draw_preview_is_safe():
    assert next_card_label(create_battle([])) == "No cards"

def test_claimed_reward_enters_deck():
    battle = create_battle([])
    offer = offer_rewards(battle, [Card(str(i), str(i), 1) for i in range(5)])
    selected = choose_reward(battle, offer[0].card_id)
    assert selected in battle.deck.draw_pile
