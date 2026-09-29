from td.model import Enemy, Game, Tower
from td.pathing import advance_enemy, remaining_distance
from td.render import render_board, render_game


def test_path_clamps_to_exit():
    enemy = Enemy("e", 19, 3, 3)
    assert advance_enemy(enemy, 5)
    assert enemy.progress == 20


def test_remaining_distance_never_negative():
    assert remaining_distance(Enemy("e", 22, 1, 1)) == 0


def test_board_contains_tower_and_enemy_markers():
    game = Game(enemies=[Enemy("e", 3, 1, 1)])
    game.towers.append(Tower("t", 5, 0))
    rendered = render_board(game)
    assert rendered[3] == "E"
    assert rendered[5] == "T"


def test_rendered_status_is_text():
    game = Game(enemies=[Enemy("live", 0, 1, 1)])
    assert "Lives 20" in render_game(game)


def test_escape_decrements_lives_once():
    from td.pathing import move_enemies

    game = Game(lives=2, enemies=[Enemy("e", 19, 1, 1)])
    assert move_enemies(game) == ["e"]
    assert game.lives == 1
    assert move_enemies(game) == []
    assert game.lives == 1
