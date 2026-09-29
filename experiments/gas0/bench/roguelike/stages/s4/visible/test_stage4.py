from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_applies_configured_damage_once():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook(); book.apply_poison("p",1,4)
    assert tick_poison(player,book)==4 and player.hp==4
