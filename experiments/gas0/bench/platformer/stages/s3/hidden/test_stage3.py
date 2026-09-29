from platformer.geometry import Rect
from platformer.model import Player,Vec2
from platformer.pressure import plate_weight,update_plate

def test_plate_reports_only_transition_edges():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=True); plate=Rect(0,1.9,3,2.2)
    assert update_plate(player,plate,False)=={"pressed":True,"activated":True,"released":False}
    assert update_plate(player,plate,True)=={"pressed":True,"activated":False,"released":False}

def test_plate_weight_is_positive_for_small_players():
    player=Player("p",Vec2(),Vec2(),width=.5,height=.5)
    assert plate_weight(player)==1
