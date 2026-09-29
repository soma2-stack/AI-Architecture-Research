from platformer.dash import advance_dash,dash,dash_ready
from platformer.model import Player,Vec2

def test_left_dash_preserves_negative_vertical_velocity():
    player=Player("p",Vec2(),Vec2(3,-5),on_ground=False)
    assert dash(player,-1,8,2) and player.velocity==Vec2(-8,-5)

def test_zero_direction_does_not_start_dash():
    player=Player("p",Vec2(),Vec2(2,4))
    assert not dash(player,0) and dash_ready(player)

def test_dash_duration_counts_down_without_changing_vertical_speed():
    player=Player("p",Vec2(),Vec2(0,9),on_ground=False); dash(player,1,3,2)
    assert advance_dash(player) and not advance_dash(player)
    assert player.velocity.y==9 and dash_ready(player)
