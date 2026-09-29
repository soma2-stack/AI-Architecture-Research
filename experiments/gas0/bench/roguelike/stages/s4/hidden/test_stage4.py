from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_repeated_poison_ticks_do_not_double_damage():
    player=Player("p","Hero",Point(0,0),10,10); book=StatusBook(); book.apply_poison("p",2,4)
    assert tick_poison(player,book)==4 and tick_poison(player,book)==4
    assert player.hp==2
