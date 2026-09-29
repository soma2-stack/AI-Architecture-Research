from platformer.dash import dash
from platformer.model import Player,Vec2

def test_dash_preserves_airborne_vertical_velocity():
    player=Player("p",Vec2(0,0),Vec2(1,7),on_ground=False)
    assert dash(player,1,12,4)
    assert player.velocity==Vec2(12,7) and player.dash_ticks==4
