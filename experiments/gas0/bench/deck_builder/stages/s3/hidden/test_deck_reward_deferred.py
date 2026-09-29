def test_reward_offer_is_deferred():
    import deckgame.rewards as rewards
    assert not hasattr(rewards, "offer_rewards")
