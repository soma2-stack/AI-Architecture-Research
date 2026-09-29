from platformer.geometry import Rect
from platformer.model import Player,Vec2
from platformer.pressure import pressed,update_plate

def test_grounded_player_presses_plate():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=True)
    assert pressed(player,Rect(0,1.9,3,2.2))

def test_airborne_overlap_does_not_press_plate():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=False)
    assert not pressed(player,Rect(0,1.9,3,2.2))
