from td.model import Game
from td.pathing import spawn_wave

def test_rng_streams_are_owned_by_game():
    a, b, c = Game(seed=2), Game(seed=2), Game(seed=2)
    out_a = [e.hp for e in spawn_wave(a, 1, 4)]
    out_b = [e.hp for e in spawn_wave(b, 1, 4)]
    out_c = [e.hp for e in spawn_wave(c, 1, 4)]
    assert out_a == out_b == out_c

def test_distinct_seed_changes_generated_wave():
    a, b = Game(seed=1), Game(seed=9)
    assert [e.hp for e in spawn_wave(a, 1, 8)] != [e.hp for e in spawn_wave(b, 1, 8)]
