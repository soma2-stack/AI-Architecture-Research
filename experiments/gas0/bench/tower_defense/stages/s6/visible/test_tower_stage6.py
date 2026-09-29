from td.model import Game
from td.pathing import spawn_wave

def test_equal_seeds_replay_wave_health():
    first, second = Game(seed=8), Game(seed=8)
    assert [e.hp for e in spawn_wave(first, 1, 5)] == [e.hp for e in spawn_wave(second, 1, 5)]
