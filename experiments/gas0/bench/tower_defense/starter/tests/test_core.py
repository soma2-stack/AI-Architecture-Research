from td.game import summary, tick
from td.model import Enemy, Game


def test_tick_advances_clock_and_path():
    game = Game(enemies=[Enemy("e", 1, 4, 4)])
    result = tick(game)
    assert result["tick"] == 1
    assert game.enemies[0].progress == 2


def test_summary_reports_resources_and_enemy_count():
    game = Game(lives=9, money=12, enemies=[Enemy("e", 2, 3, 3)])
    assert summary(game) == {
        "wave": 0,
        "lives": 9,
        "money": 12,
        "enemies": 1,
        "furthest": 2,
    }


def test_dead_enemy_is_not_counted_as_active():
    game = Game(enemies=[Enemy("dead", 3, 0, 3, False), Enemy("live", 2, 2, 2)])
    assert summary(game)["enemies"] == 1


def test_validation_rejects_duplicate_ids():
    from td.model import validate_game

    game = Game(enemies=[Enemy("x", 0, 2, 2), Enemy("x", 1, 2, 2)])
    try:
        validate_game(game)
    except ValueError as error:
        assert "unique" in str(error)
    else:
        raise AssertionError("duplicate identifiers were accepted")


def test_run_ticks_keeps_sequential_clock():
    from td.game import run_ticks

    game = Game()
    assert [row["tick"] for row in run_ticks(game, 3)] == [1, 2, 3]


def test_wave_complete_for_empty_game():
    from td.waves import wave_complete

    assert wave_complete(Game())
